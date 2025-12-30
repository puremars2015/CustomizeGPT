# Uninstall Claude Code
# Run this script in PowerShell after closing Claude Code

Write-Host "Claude Code Uninstaller" -ForegroundColor Cyan
Write-Host "======================" -ForegroundColor Cyan
Write-Host ""

# Uninstall Claude Code
Write-Host "Removing Claude Code installation..." -ForegroundColor Yellow
$claudeCodePath = "$env:LOCALAPPDATA\Programs\claude-code"
$claudeExePath = "$env:LOCALAPPDATA\Microsoft\WindowsApps\claude.exe"

if (Test-Path $claudeCodePath) {
    Remove-Item -Path $claudeCodePath -Recurse -Force
    Write-Host "Removed: $claudeCodePath" -ForegroundColor Green
} else {
    Write-Host "Not found: $claudeCodePath" -ForegroundColor Gray
}

if (Test-Path $claudeExePath) {
    Remove-Item -Path $claudeExePath -Force
    Write-Host "Removed: $claudeExePath" -ForegroundColor Green
} else {
    Write-Host "Not found: $claudeExePath" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Claude Code has been uninstalled." -ForegroundColor Green
Write-Host ""

# Ask about removing configuration files
$removeConfig = Read-Host "Do you want to remove all settings and configuration files? (y/n)"

if ($removeConfig -eq 'y' -or $removeConfig -eq 'Y') {
    Write-Host ""
    Write-Host "Removing configuration files..." -ForegroundColor Yellow

    $claudeDir = "$env:USERPROFILE\.claude"
    $claudeJson = "$env:USERPROFILE\.claude.json"

    if (Test-Path $claudeDir) {
        Remove-Item -Path $claudeDir -Recurse -Force
        Write-Host "Removed: $claudeDir" -ForegroundColor Green
    } else {
        Write-Host "Not found: $claudeDir" -ForegroundColor Gray
    }

    if (Test-Path $claudeJson) {
        Remove-Item -Path $claudeJson -Force
        Write-Host "Removed: $claudeJson" -ForegroundColor Green
    } else {
        Write-Host "Not found: $claudeJson" -ForegroundColor Gray
    }

    Write-Host ""
    Write-Host "All Claude Code files have been removed." -ForegroundColor Green
} else {
    Write-Host "Configuration files were kept." -ForegroundColor Gray
}

Write-Host ""
Write-Host "Uninstallation complete!" -ForegroundColor Cyan
Write-Host ""
Pause
