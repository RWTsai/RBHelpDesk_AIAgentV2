# 把 run_ingest.cmd 註冊成 Windows 排程工作（每 N 分鐘跑一輪文件匯入）。
# 請用「以系統管理員身分執行」開啟 PowerShell。
#
#   .\Register-IngestTask.ps1              每 5 分鐘一輪
#   .\Register-IngestTask.ps1 -Minutes 10
#   .\Register-IngestTask.ps1 -Unregister  移除
#
# 注意：這個檔必須存成「UTF-8 含 BOM」。Windows PowerShell 5.1 沒看到 BOM
# 會用 cp950 讀，中文會變亂碼並造成語法錯誤。
param([int]$Minutes = 5, [switch]$Unregister)

$Task = 'RBIT_IngestDocs'

if ($Unregister) {
    Unregister-ScheduledTask -TaskName $Task -Confirm:$false
    Write-Host "已移除 $Task"
    return
}

# 放在 scheduler\ 或專案根目錄都可以
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$Cmd = @((Join-Path $here 'run_ingest.cmd'),
         (Join-Path $here 'scheduler\run_ingest.cmd')) |
       Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $Cmd) { Write-Host "找不到 run_ingest.cmd" -ForegroundColor Red; return }

$action  = New-ScheduledTaskAction -Execute $Cmd
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) `
             -RepetitionInterval (New-TimeSpan -Minutes $Minutes)

# IgnoreNew：上一輪還在解析大檔時不要疊第二輪上去
# StartWhenAvailable：主機關機錯過的時段，開機後補跑一次
$settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable

# S4U：不存密碼，但不論使用者有沒有登入都會跑（代價是存取不到網路磁碟）
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" `
               -LogonType S4U -RunLevel Highest

Register-ScheduledTask -TaskName $Task -Action $action -Trigger $trigger `
    -Settings $settings -Principal $principal -Force | Out-Null

Write-Host "已註冊 $Task（每 $Minutes 分鐘）：$Cmd"
Write-Host "  手動跑   Start-ScheduledTask -TaskName $Task"
Write-Host "  看狀態   Get-ScheduledTask -TaskName $Task | Get-ScheduledTaskInfo"
Write-Host "  看輸出   Get-Content logs\ingest_task.log -Tail 50 -Encoding UTF8"
