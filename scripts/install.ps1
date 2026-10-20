<#
.SYNOPSIS
    convermem All-in-One Installer & Skills Synchronizer
.DESCRIPTION
    Installs the convermem Python package locally (editable mode),
    and synchronizes the /convermem slash command skill into AI agent config directories
    (Antigravity, Claude Code, Cursor, OpenCode) with zero extra steps.
#>

[CmdletBinding()]
param (
    [Parameter(Mandatory=$false)]
    [ValidateSet("All", "Antigravity", "Claude", "Cursor", "OpenCode")]
    [string]$TargetAgent = "All"
)

Write-Host "===============================================================" -ForegroundColor Cyan
Write-Host " 🧠 convermem: Universal All-in-One Installer & Sync Engine" -ForegroundColor Yellow
Write-Host "===============================================================" -ForegroundColor Cyan

# 1. Check Python runtime
Write-Host "`n[1/4] Checking Python runtime..." -ForegroundColor Green
try {
    $pyVer = python --version
    Write-Host "  -> Python detected: $pyVer" -ForegroundColor White
} catch {
    Write-Error "Python is not found. Please install Python 3.10+ to continue."
    exit 1
}

# 2. Install / Register CLI tool locally
Write-Host "`n[2/4] Installing convermem Python package..." -ForegroundColor Green
$currentDir = $PSScriptRoot
$repoRoot = (Get-Item $currentDir).Parent.FullName

Push-Location $repoRoot
try {
    pip install -e . --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  -> convermem CLI installed successfully!" -ForegroundColor Green
    } else {
        Write-Warning "  -> pip install finished with warnings or non-zero exit code."
    }
} finally {
    Pop-Location
}

# 3. Synchronize Skills to AI Agent paths (scmdsolution cross-drive sync engine)
Write-Host "`n[3/4] Registering /convermem Slash Command across AI Agents..." -ForegroundColor Green
$skillSource = Join-Path $repoRoot ".agents\skills\convermem\SKILL.md"

if (-not (Test-Path $skillSource)) {
    # Fallback to SKILL.md in root if present
    $skillSource = Join-Path $repoRoot "SKILL.md"
}

$targetDirs = @()
$agentMap = @{
    "Antigravity" = "$env:USERPROFILE\.gemini\config\skills"
    "Claude"      = "$env:USERPROFILE\.claude\skills"
    "Cursor"      = "$env:USERPROFILE\.cursor\skills"
    "OpenCode"    = "$env:USERPROFILE\.agents\skills"
}

if ($TargetAgent -eq "All") {
    foreach ($key in $agentMap.Keys) {
        $path = $agentMap[$key]
        $parentDir = Split-Path $path -Parent
        if (Test-Path $parentDir) {
            $targetDirs += $path
        }
    }
    # Always include Antigravity if none auto-detected
    if ($targetDirs.Count -eq 0) {
        $targetDirs += $agentMap["Antigravity"]
    }
} else {
    $targetDirs += $agentMap[$TargetAgent]
}

foreach ($target in $targetDirs) {
    if (-not (Test-Path $target)) {
        New-Item -ItemType Directory -Path $target -Force | Out-Null
    }
    
    Write-Host "`nTarget AI Directory: $target" -ForegroundColor Yellow
    $destDir = Join-Path $target "convermem"
    if (-not (Test-Path $destDir)) {
        New-Item -ItemType Directory -Path $destDir -Force | Out-Null
    }

    if (Test-Path $skillSource) {
        Copy-Item -Path $skillSource -Destination (Join-Path $destDir "SKILL.md") -Force
        Write-Host "  [★] Registered Slash Command: /convermem" -ForegroundColor Cyan
    } else {
        Write-Warning "  -> SKILL.md source file not found at $skillSource"
    }
}

# 4. Clean Cache
Write-Host "`n[4/4] Cleaning temporary cache files..." -ForegroundColor Green
Get-ChildItem -Path $repoRoot -Filter "__pycache__" -Recurse -Directory -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path $repoRoot -Filter "*.pyc" -Recurse -File -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Host "  -> Cache cleaned!" -ForegroundColor White

Write-Host "`n===============================================================" -ForegroundColor Cyan
Write-Host " ✨ convermem is completely installed and ready to use!" -ForegroundColor Yellow
Write-Host " Next Steps:" -ForegroundColor White
Write-Host " 1. Run 'convermem --help' in your terminal." -ForegroundColor White
Write-Host " 2. Type '/convermem' in your AI chat to preserve verbatim context!" -ForegroundColor White
Write-Host "===============================================================" -ForegroundColor Cyan
