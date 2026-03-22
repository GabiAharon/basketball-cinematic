# NBA Stats Daily Scheduler Setup
# Run this script in PowerShell as Administrator to set up daily stats fetching

$taskName = "NBA Stats Daily Update"
$batPath = "C:\Users\gabia\Desktop\Claude Code\basketball-cinematic\update_stats.bat"

# Create the scheduled task action
$action = New-ScheduledTaskAction -Execute $batPath

# Trigger: every day at 06:00
$trigger = New-ScheduledTaskTrigger -Daily -At 06:00

# Settings
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Remove existing task if it exists
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Register the task
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Fetches latest NBA player stats daily for Basketball Cinematic Showcase"

Write-Host ""
Write-Host "Task '$taskName' created successfully!" -ForegroundColor Green
Write-Host "Schedule: Daily at 06:00 AM" -ForegroundColor Cyan
Write-Host "Script: $batPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "To verify: Get-ScheduledTask -TaskName '$taskName'" -ForegroundColor Yellow
Write-Host "To run now: Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor Yellow
Write-Host "To remove: Unregister-ScheduledTask -TaskName '$taskName'" -ForegroundColor Yellow
