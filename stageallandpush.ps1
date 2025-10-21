param(
    [string]$commitMessage = "Update: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
)

# Set error action preference
$ErrorActionPreference = "Stop"

try {
    Write-Host "Staging all changes..." -ForegroundColor Cyan
    git add .
    
    Write-Host "Creating commit with message: $commitMessage" -ForegroundColor Cyan
    git commit -m $commitMessage
    
    Write-Host "Pushing changes to remote..." -ForegroundColor Cyan
    git push origin main
    
    Write-Host "`nDone! Changes have been successfully pushed to the repository." -ForegroundColor Green
} catch {
    Write-Host "`nAn error occurred:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    exit 1
}
