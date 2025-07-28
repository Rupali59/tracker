# GitHub Statistics Tracker - Daily Update Script
# Run this script daily to update your Obsidian daily notes with GitHub activity

Write-Host "🚀 Starting GitHub Statistics Tracker - Daily Update..." -ForegroundColor Green

try {
    # Check if Python is available
    $pythonVersion = python --version 2>$null
    if (-not $?) {
        Write-Host "❌ Python is not installed or not in PATH" -ForegroundColor Red
        Write-Host "Please install Python from https://python.org" -ForegroundColor Yellow
        exit 1
    }
    
    # Check if required files exist
    if (-not (Test-Path "scheduler.py")) {
        Write-Host "❌ scheduler.py not found" -ForegroundColor Red
        Write-Host "Please run this script from the tracker directory" -ForegroundColor Yellow
        exit 1
    }
    
    # Run the scheduler
    Write-Host "📊 Running GitHub statistics tracker..." -ForegroundColor Cyan
    python scheduler.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Daily update completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "❌ Daily update failed with exit code $LASTEXITCODE" -ForegroundColor Red
    }
    
} catch {
    Write-Host "❌ Error running daily update: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 