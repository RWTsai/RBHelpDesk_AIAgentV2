<#
.SYNOPSIS
    把 scheduler/ingest_docs.py 註冊成 Windows 排程工作（文件匯入／同步）。

.DESCRIPTION
    採「每 N 分鐘跑一次 --once」而不是常駐 --loop：
      * 程式中途被砍、主機重開，排程器下一輪自動補上，不用人去盯常駐程序還在不在
      * --once 每輪開頭會呼叫 reset_stuck()，把卡在 Processing 的文件放回 Pending
      * 同時只允許一個執行個體（IgnoreNew），上一輪還沒跑完就跳過這一輪，不會疊起來

    這支腳本做三件事：
      1. 檢查 Python 直譯器確實裝了 ingest_docs.py 要用的套件
      2. 產生 scheduler\run_ingest.cmd 包裝檔（設定工作目錄、UTF-8 輸出、轉向 log）
      3. 註冊／更新排程工作

    必須用「以系統管理員身分」開啟的 PowerShell 執行。

.PARAMETER TaskName
    排程工作名稱，預設 RBIT_IngestDocs。

.PARAMETER IntervalMinutes
    每幾分鐘跑一輪，預設 5（和 .env 的 INGEST_INTERVAL_SEC=300 一致）。

.PARAMETER Python
    python.exe 完整路徑。不給就自動找（py -3 → python）。

.PARAMETER UserName
    執行帳號，例如 ROYALBASE\svc_rbit。不給就用目前登入的帳號。

.PARAMETER Password
    搭配 UserName 使用。有給密碼才會存成「不論使用者登入與否都執行」並且拿得到網路磁碟；
    沒給密碼用 S4U（不存密碼），那種模式存取不到 UNC 路徑。
    DOC_DROP_FOLDER 若指向網芳就一定要給密碼。

.PARAMETER RunNow
    註冊完立刻跑一次，並把這一輪的輸出印出來。

.PARAMETER Unregister
    只移除排程工作，不做其他事。

.EXAMPLE
    .\Register-IngestTask.ps1 -RunNow

.EXAMPLE
    .\Register-IngestTask.ps1 -UserName 'ROYALBASE\svc_rbit' -Password 'xxxx' -IntervalMinutes 5

.EXAMPLE
    .\Register-IngestTask.ps1 -Unregister
#>
[CmdletBinding()]
param(
    [string]$TaskName        = 'RBIT_IngestDocs',
    [int]   $IntervalMinutes = 5,
    [string]$Python          = '',
    [string]$UserName        = '',
    [string]$Password        = '',
    [switch]$RunNow,
    [switch]$Unregister
)

$ErrorActionPreference = 'Stop'

function Info($m) { Write-Host "[OK]   $m" -ForegroundColor Green }
function Warn($m) { Write-Host "[注意] $m" -ForegroundColor Yellow }
function Die ($m) { Write-Host "[失敗] $m" -ForegroundColor Red; exit 1 }

# ---------- 0) 權限 ----------
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()
           ).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) { Die '請用「以系統管理員身分執行」開啟 PowerShell 再跑這支腳本。' }

# ---------- 1) 移除模式 ----------
if ($Unregister) {
    if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Info "已移除排程工作 $TaskName"
    } else {
        Warn "找不到排程工作 $TaskName，不用移除"
    }
    exit 0
}

# ---------- 2) 路徑 ----------
# 這支腳本放在 scheduler\ 底下，專案根目錄就是上一層
$ScriptDir   = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = (Resolve-Path (Join-Path $ScriptDir '..')).Path
$IngestPy    = Join-Path $ScriptDir 'ingest_docs.py'
$EnvFile     = Join-Path $ProjectRoot '.env'
$LogDir      = Join-Path $ProjectRoot 'logs'
$Wrapper     = Join-Path $ScriptDir 'run_ingest.cmd'

if (-not (Test-Path $IngestPy)) { Die "找不到 $IngestPy，請把這支 ps1 放在 scheduler\ 資料夾裡。" }
if (-not (Test-Path $EnvFile))  { Die "找不到 $EnvFile。連線字串與資料夾設定都在 .env，沒有它跑不起來。" }
if (-not (Test-Path $LogDir))   { New-Item -ItemType Directory -Path $LogDir | Out-Null }

Info "專案根目錄：$ProjectRoot"

# ---------- 3) 找 Python 並驗證套件 ----------
if (-not $Python) {
    foreach ($probe in @('py -3 -c "import sys;print(sys.executable)"',
                         'python -c "import sys;print(sys.executable)"')) {
        try {
            $out = cmd /c $probe 2>$null
            if ($LASTEXITCODE -eq 0 -and $out) { $Python = ($out | Select-Object -Last 1).Trim(); break }
        } catch { }
    }
}
if (-not $Python -or -not (Test-Path $Python)) {
    Die '找不到 python.exe。請用 -Python "C:\Python\Python313\python.exe" 指定。'
}

# 這台機器上通常不只一套 Python（Anaconda 很常見）。排程器用的那一套沒裝套件的話，
# 要到半夜跑起來才會失敗，所以先在這裡驗一次。
$need = 'tiktoken,openai,dotenv,pyodbc,yaml,requests'
$probeCode = "import importlib.util as u;print(','.join([m for m in '$need'.split(',') if u.find_spec(m) is None]))"
$miss = (& $Python -c $probeCode) -join ''
if ($LASTEXITCODE -ne 0) { Die "$Python 無法執行。" }
if ($miss.Trim()) {
    Die "$Python 缺少套件：$miss`n       先執行： `"$Python`" -m pip install -r `"$ProjectRoot\requirements.txt`""
}
Info "Python：$Python（套件齊全）"

# ---------- 4) 產生包裝批次檔 ----------
# 為什麼要多包一層 .cmd：
#   * 排程器的「動作」沒辦法做輸出轉向，但 traceback 一定要留下來
#   * utils/logger.py 的 LOG_DIR 是相對路徑 "logs"，工作目錄不對，log 就會散到別的地方
#   * 用 %~dp0.. 推算專案根目錄，批次檔內不出現中文路徑，省掉編碼問題
$cmdBody = @"
@echo off
rem === RBIT 文件匯入（Register-IngestTask.ps1 產生，可以手動雙擊測試）===
rem 工作目錄一定要是專案根目錄：logger 的 logs\ 是相對它找的
cd /d "%~dp0.."

set "PYTHONIOENCODING=utf-8"
set "PYTHONUNBUFFERED=1"
set "LOGFILE=%CD%\logs\ingest_task.log"

rem 超過 10MB 就換一個檔，避免無限長大
if exist "%LOGFILE%" for %%A in ("%LOGFILE%") do if %%~zA GTR 10485760 move /y "%LOGFILE%" "%LOGFILE%.1" >nul 2>&1

echo.>> "%LOGFILE%"
echo ========== %DATE% %TIME% start ==========>> "%LOGFILE%"
"$Python" "scheduler\ingest_docs.py" --once >> "%LOGFILE%" 2>&1
set RC=%ERRORLEVEL%
echo ========== %DATE% %TIME% exit=%RC% ==========>> "%LOGFILE%"
exit /b %RC%
"@

# cmd.exe 讀批次檔用的是 OEM 字碼頁（繁中 Windows 是 cp950），不是 UTF-8
[System.IO.File]::WriteAllText($Wrapper, $cmdBody, [System.Text.Encoding]::GetEncoding(950))
Info "已產生 $Wrapper"

# ---------- 5) 註冊排程工作 ----------
$action = New-ScheduledTaskAction -Execute $Wrapper -WorkingDirectory $ProjectRoot

# 兩個觸發：一分鐘後開始、之後每 N 分鐘一輪；另外開機也跑一次。
# RepetitionDuration 給 10 年＝實質無限（PowerShell 5.1 對 TimeSpan::MaxValue 有時會出錯，不用它）
$t1 = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
        -RepetitionInterval (New-TimeSpan -Minutes $IntervalMinutes) `
        -RepetitionDuration (New-TimeSpan -Days 3650)
$t2 = New-ScheduledTaskTrigger -AtStartup
try { $t2.Delay = 'PT1M' } catch { }

$settings = New-ScheduledTaskSettingsSet `
    -MultipleInstances IgnoreNew `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Hours 2) `
    -RestartCount 3 -RestartInterval (New-TimeSpan -Minutes 5)
$settings.Hidden = $true

if (-not $UserName) { $UserName = "$env:USERDOMAIN\$env:USERNAME" }

if ($Password) {
    # 密碼存進排程器 → 不論使用者有沒有登入都會跑，而且拿得到網路磁碟
    $principal = New-ScheduledTaskPrincipal -UserId $UserName -LogonType Password -RunLevel Highest
    $register  = @{ User = $UserName; Password = $Password }
} else {
    # S4U：不用存密碼，一樣不論登入與否都會跑，但沒有網路認證
    $principal = New-ScheduledTaskPrincipal -UserId $UserName -LogonType S4U -RunLevel Highest
    $register  = @{}
    Warn 'S4U 模式（沒存密碼）：存取不到 UNC／網路磁碟。'
    Warn 'DOC_DROP_FOLDER 若指向網芳，請加 -UserName/-Password 重跑一次。'
}

$task = New-ScheduledTask -Action $action -Trigger @($t1, $t2) -Settings $settings -Principal $principal
$task.Description = "RBIT 文件 GraphRAG 匯入：每 $IntervalMinutes 分鐘掃一次後台上傳／本機資料夾／Google Drive／OneDrive，把新增或變更的文件解析入庫。"

if (Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue) {
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Warn "已存在的 $TaskName 先移除再重建"
}
Register-ScheduledTask -TaskName $TaskName -InputObject $task @register | Out-Null
Info "已註冊排程工作 $TaskName（每 $IntervalMinutes 分鐘，執行帳號 $UserName）"

# ---------- 6) 立刻跑一次 ----------
if ($RunNow) {
    Write-Host ''
    Write-Host '--- 立刻執行一輪 ---' -ForegroundColor Cyan
    Start-ScheduledTask -TaskName $TaskName
    $logFile = Join-Path $LogDir 'ingest_task.log'
    for ($i = 0; $i -lt 90; $i++) {
        Start-Sleep -Seconds 2
        $info = Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo
        if ($info.LastTaskResult -ne 267009) { break }   # 267009 = 還在執行中
    }
    $info = Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo
    Write-Host ("結束碼：{0}（0 代表成功）" -f $info.LastTaskResult)
    if (Test-Path $logFile) {
        Write-Host "--- $logFile 最後 40 行 ---" -ForegroundColor Cyan
        Get-Content $logFile -Tail 40 -Encoding UTF8
    }
}

Write-Host ''
Write-Host '常用指令：' -ForegroundColor Cyan
Write-Host "  手動跑一次    Start-ScheduledTask -TaskName $TaskName"
Write-Host "  看上次結果    Get-ScheduledTask -TaskName $TaskName | Get-ScheduledTaskInfo"
Write-Host "  看執行輸出    Get-Content '$LogDir\ingest_task.log' -Tail 50 -Wait -Encoding UTF8"
Write-Host "  看程式日誌    Get-Content '$LogDir\$(Get-Date -Format yyyy-MM-dd).log' -Tail 50 -Encoding UTF8"
Write-Host "  停用／啟用    Disable-ScheduledTask / Enable-ScheduledTask -TaskName $TaskName"
Write-Host "  移除          .\Register-IngestTask.ps1 -Unregister"
