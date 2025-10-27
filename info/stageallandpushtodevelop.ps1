# Stage, commit and push changes with a single command
param(
    [string]$commitMessage = "Update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
)

# Set error action preference
$ErrorActionPreference = "Stop"

try {
    # Configure Git to handle line endings properly
    git config --global core.autocrlf true

    # Get status before staging
    Write-Host "`nChecking repository status..." -ForegroundColor Cyan
    git status

    # Stage all changes
    Write-Host "`nStaging all changes..." -ForegroundColor Cyan
    git add .

    # Create commit
    Write-Host "`nCreating commit with message: $commitMessage" -ForegroundColor Cyan
    git commit -m $commitMessage

    # Push changes
    Write-Host "`nPushing changes to remote..." -ForegroundColor Cyan
    git push origin develop

    # Show final status
    Write-Host "`nRepository status after push:" -ForegroundColor Green
    git status

    Write-Host "`n✅ Success! Changes have been pushed to the repository." -ForegroundColor Green
}
catch {
    Write-Host "`n❌ An error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host "`nCheck the error above and try again." -ForegroundColor Yellow
    exit 1
}
