param([string]$SkillsRoot = (Join-Path $env:USERPROFILE '.agents\skills'))
$ErrorActionPreference = 'Stop'
$bundleRoot = $PSScriptRoot
$folders = @('devflow', 'frontend-design', 'ui-ux-pro-max', 'taste-skill', 'ponytail', 'caveman', 'ui-taste', 'superpowers', 'diagram-design', 'open-code-review', 'security-audit')
if (Test-Path -LiteralPath $SkillsRoot) {
    $legacy = @(Get-ChildItem -LiteralPath $SkillsRoot -Force | Where-Object {
        $_.Name -in @('reverse-engineered', 'find-reverse-engineered') -or $_.Name -like 'reverse-engineered-*'
    })
    if ($legacy.Count -gt 0) { throw 'Legacy installation found. Archive verified old entries outside discovery first; nothing changed.' }
}
New-Item -ItemType Directory -Force -Path $SkillsRoot | Out-Null
foreach ($folder in $folders) {
    $source = (Resolve-Path -LiteralPath (Join-Path $bundleRoot "skills\$folder")).Path
    $alreadyLinked = @(Get-ChildItem -LiteralPath $SkillsRoot -Force | Where-Object {
        $_.LinkType -and @($_.Target | Where-Object { $_ -eq $source }).Count -gt 0
    })
    if ($alreadyLinked.Count -gt 0) {
        Write-Output "Already linked: $folder"
        continue
    }
    $destination = Join-Path $SkillsRoot "devflow-kit-$folder"
    if (Get-Item -LiteralPath $destination -Force -ErrorAction SilentlyContinue) {
        throw "Existing entry at $destination; inspect it before installing. Nothing was overwritten."
    }
    New-Item -ItemType Junction -Path $destination -Target $source | Out-Null
    Write-Output "Linked: $folder -> $source"
}
