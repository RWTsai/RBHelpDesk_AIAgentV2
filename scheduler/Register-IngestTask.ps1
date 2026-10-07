# 把 scheduler\run_ingest.cmd 註冊成 Windows 排程工作（每 N 分鐘跑一輪文件匯入）。
# 請用「以系統管理員身分執行」開啟 PowerShell。
#
#   .\Register-IngestTask.ps1              每 5 分鐘一輪
#   .\Register-IngestTask.ps1 -Minutes 10
#   .\Register-IngestTask.ps1 -Unregister  移除
param([int]$Minutes = 5, [switch]$Unregister)

$Task = 'RBIT_IngestDocs'
$Cmd  = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) 'run_ingest.cmd'

if ($Unregister) {
    Unregister-ScheduledTask -TaskName $Task -Confirm:$false
    Write-Host "已移除 $Task"
    return
}

if (-not (Test-Path $Cmd)) { Write-Host "找不到 $Cmd" -ForegroundColor Red; return }

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

Write-Host "已註冊 $Task（每 $Minutes 分鐘）"
Write-Host "  手動跑   Start-ScheduledTask -TaskName $Task"
Write-Host "  看狀態   Get-ScheduledTask -TaskName $Task | Get-ScheduledTaskInfo"
Write-Host "  看輸出   Get-Content .\logs\ingest_task.log -Tail 50 -Encoding UTF8"
