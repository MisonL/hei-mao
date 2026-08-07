[Diagnostics.CodeAnalysis.SuppressMessageAttribute("PSAvoidUsingWriteHost", "", Justification = "Installer TUI uses host colors only when output is interactive.")]
param(
    [string]$PetId = "",
    [string]$BaseUrl = "",
    [string]$InstallDir = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$DefaultBaseUrl = "https://raw.githubusercontent.com/MisonL/hei-mao/main"
$PetSubdir = ""
$PetJsonSha256 = ""
$SpritesheetSha256 = ""
$InstallerScriptRoot = $PSScriptRoot
$script:StepIndex = 0
$script:StepTotal = 4

function Test-Text {
    param([AllowNull()][string]$Value)
    return -not [string]::IsNullOrEmpty($Value)
}

function Set-PetConfiguration {
    $requestedPetId = $PetId
    if (-not (Test-Text $requestedPetId)) {
        $requestedPetId = $env:HEI_MAO_PET_ID
    }
    if (-not (Test-Text $requestedPetId)) {
        $requestedPetId = "hei-mao"
    }

    switch ($requestedPetId) {
        "hei-mao" {
            $script:PetJsonSha256 = "dafa673543839e1742fd78b766549877c249286930b3a9ae47903b9c6f2e5802"
            $script:SpritesheetSha256 = "dd5f50c1f34010784af94c801a5042963e8aae6031f520fdd43f2b099811453a"
            $script:PetSubdir = ""
        }
        "hei-mao-quality" {
            $script:PetJsonSha256 = "c7539a98ae2767ab70c69e31c588f7e977e440307dc8bca791fff3bc8350eb07"
            $script:SpritesheetSha256 = "1e22f95b918ab423d1b4bede9af93761e89ff39c5a961ee3728c671b0dd05f9f"
            $script:PetSubdir = "pets/$requestedPetId"
        }
        "hei-mao-butler" {
            $script:PetJsonSha256 = "903f3c673f510048fb3daf498976d0a99e958edc6ee969c2790b8555be89daf4"
            $script:SpritesheetSha256 = "1e59bcd0024b4f381e740655e2457df490773e7038ea3f77f073f3ac5ca46304"
            $script:PetSubdir = "pets/$requestedPetId"
        }
        "hei-mao-chef" {
            $script:PetJsonSha256 = "d210cb46a995d378de755b3eb40815c3a114476bc25120bd184677b0ec5dd43a"
            $script:SpritesheetSha256 = "32a4df73b3ecc58c0f1488025a841fb7be7c93127d3f0134f22d6c799580d957"
            $script:PetSubdir = "pets/$requestedPetId"
        }
        default {
            throw "Unsupported pet id: $requestedPetId. Supported ids: hei-mao, hei-mao-quality, hei-mao-butler, hei-mao-chef."
        }
    }

    $script:PetId = $requestedPetId
}

$script:UseColor = (-not [System.Console]::IsOutputRedirected) -and (-not (Test-Text $env:NO_COLOR))
$script:UseAnimation = $script:UseColor -and (-not (Test-Text $env:HEI_MAO_NO_ANIMATION))

function Write-TuiLine {
    param(
        [string]$Text,
        [System.ConsoleColor]$Color = [System.ConsoleColor]::Gray
    )

    if ($script:UseColor) {
        Write-Host $Text -ForegroundColor $Color
        return
    }

    Write-Output $Text
}

function Write-PigFrame {
    param([int]$Frame)

    $eyes = "o   o"
    $tail = "~"
    if ($Frame -eq 1) {
        $eyes = "-   -"
        $tail = ")"
    }
    elseif ($Frame -eq 2) {
        $tail = "("
    }

    Write-Output "       #####"
    Write-Output '     .-""""-.'
    Write-Output "    /  $eyes  \"
    Write-Output "   |    (oo)   |$tail"
    Write-Output "   |  /|____|\ |"
    Write-Output "    \ HEI MAO/"
    Write-Output "     '------'"
}

function Write-Intro {
    Write-Output ""
    Write-TuiLine "==================================================" ([System.ConsoleColor]::Cyan)
    Write-TuiLine " Hei Mao Codex Pet Installer" ([System.ConsoleColor]::Cyan)
    Write-TuiLine "==================================================" ([System.ConsoleColor]::Cyan)

    if (-not $script:UseAnimation) {
        Write-PigFrame 0
        return
    }

    try {
        $startY = [System.Console]::CursorTop
        $windowBottom = [System.Console]::WindowTop + [System.Console]::WindowHeight - 1
        if (($windowBottom - $startY) -lt 7) {
            Write-PigFrame 0
            return
        }
    }
    catch {
        Write-PigFrame 0
        return
    }

    foreach ($frame in @(0, 1, 2, 1, 0)) {
        [System.Console]::SetCursorPosition(0, $startY)
        Write-PigFrame $frame
        Start-Sleep -Milliseconds 120
    }
}

function Write-Step {
    param([string]$Message)
    $script:StepIndex += 1
    $line = "[{0}/{1}] {2}" -f $script:StepIndex, $script:StepTotal, $Message
    Write-TuiLine "" ([System.ConsoleColor]::Gray)
    Write-TuiLine $line ([System.ConsoleColor]::Cyan)
}

function Write-Detail {
    param([string]$Message)
    Write-TuiLine "      $Message" ([System.ConsoleColor]::DarkGray)
}

function Write-Success {
    param([string]$Message)
    Write-TuiLine "[OK] $Message" ([System.ConsoleColor]::Green)
}

function Write-Failure {
    param([string]$Message)
    Write-TuiLine "[ERROR] $Message" ([System.ConsoleColor]::Red)
}

function Get-UserHome {
    if ($HOME) {
        return $HOME
    }

    if ($env:USERPROFILE) {
        return $env:USERPROFILE
    }

    throw "HOME is not set. Set CODEX_HOME or HOME before running this installer."
}

function Save-RemoteFile {
    param(
        [string]$Url,
        [string]$Path
    )

    $client = New-Object System.Net.WebClient
    try {
        $client.DownloadFile($Url, $Path)
    }
    finally {
        $client.Dispose()
    }
}

function Test-Sha256 {
    param(
        [string]$Path,
        [string]$ExpectedHash
    )

    $actualHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
    if ($actualHash -ne $ExpectedHash) {
        $fileName = Split-Path -Leaf $Path
        throw "SHA256 mismatch for $fileName. Expected $ExpectedHash but got $actualHash."
    }

    $okName = Split-Path -Leaf $Path
    Write-Detail "SHA256 ok: $okName"
}

function Copy-OrDownloadAsset {
    param(
        [string]$TempDir,
        [string]$ResolvedBaseUrl
    )

    $scriptDir = $null
    if ($InstallerScriptRoot) {
        $scriptDir = $InstallerScriptRoot
    }

    $hasBaseOverride = (Test-Text $BaseUrl) -or (Test-Text $env:HEI_MAO_BASE_URL)
    $hasLocalAssets = $false
    if ($scriptDir) {
        $localAssetRoot = $scriptDir
        if (Test-Text $PetSubdir) {
            $localAssetRoot = Join-Path $scriptDir $PetSubdir
        }
        $localManifest = Join-Path $localAssetRoot "pet.json"
        $localSheet = Join-Path $localAssetRoot "spritesheet.webp"
        $hasLocalAssets = ((Test-Path -LiteralPath $localManifest) -and (Test-Path -LiteralPath $localSheet))
    }

    if ((-not $hasBaseOverride) -and $hasLocalAssets) {
        Write-Detail "Source: local files"
        Write-Detail "Path: $localAssetRoot"
        Copy-Item -LiteralPath (Join-Path $localAssetRoot "pet.json") -Destination (Join-Path $TempDir "pet.json") -Force
        Copy-Item -LiteralPath (Join-Path $localAssetRoot "spritesheet.webp") -Destination (Join-Path $TempDir "spritesheet.webp") -Force
        return
    }

    if (Test-Path -LiteralPath $ResolvedBaseUrl) {
        $localAssetRoot = $ResolvedBaseUrl
        if (Test-Text $PetSubdir) {
            $localAssetRoot = Join-Path $ResolvedBaseUrl $PetSubdir
        }
        Write-Detail "Source: local files"
        Write-Detail "Path: $localAssetRoot"
        Copy-Item -LiteralPath (Join-Path $localAssetRoot "pet.json") -Destination (Join-Path $TempDir "pet.json") -Force
        Copy-Item -LiteralPath (Join-Path $localAssetRoot "spritesheet.webp") -Destination (Join-Path $TempDir "spritesheet.webp") -Force
        return
    }

    $trimmedBaseUrl = $ResolvedBaseUrl.TrimEnd("/")
    if (Test-Text $PetSubdir) {
        $trimmedBaseUrl = "$trimmedBaseUrl/$PetSubdir"
    }
    Write-Detail "Source: GitHub raw"
    Write-Detail "URL: $trimmedBaseUrl"
    Save-RemoteFile "$trimmedBaseUrl/pet.json" (Join-Path $TempDir "pet.json")
    Save-RemoteFile "$trimmedBaseUrl/spritesheet.webp" (Join-Path $TempDir "spritesheet.webp")
}

function Test-Asset {
    param([string]$TempDir)

    $manifestPath = Join-Path $TempDir "pet.json"
    $sheetPath = Join-Path $TempDir "spritesheet.webp"

    if (-not (Test-Path -LiteralPath $manifestPath)) {
        throw "pet.json is missing."
    }

    if (-not (Test-Path -LiteralPath $sheetPath)) {
        throw "spritesheet.webp is missing."
    }

    $manifestItem = Get-Item -LiteralPath $manifestPath
    $sheetItem = Get-Item -LiteralPath $sheetPath
    if (($manifestItem.Length -le 0) -or ($sheetItem.Length -le 0)) {
        throw "Downloaded assets are empty."
    }

    $manifest = Get-Content -LiteralPath $manifestPath -Raw | ConvertFrom-Json
    if ($manifest.id -ne $PetId) {
        throw "pet.json does not describe the expected pet id: $PetId"
    }

    Test-Sha256 -Path $manifestPath -ExpectedHash $PetJsonSha256
    Test-Sha256 -Path $sheetPath -ExpectedHash $SpritesheetSha256
}

try {
    Set-PetConfiguration
    Write-Intro
    Write-Step "Prepare target"

    $resolvedBaseUrl = $DefaultBaseUrl
    if (Test-Text $env:HEI_MAO_BASE_URL) {
        $resolvedBaseUrl = $env:HEI_MAO_BASE_URL
    }
    if (Test-Text $BaseUrl) {
        $resolvedBaseUrl = $BaseUrl
    }

    $userHome = Get-UserHome
    $codexHome = Join-Path $userHome ".codex"
    if (Test-Text $env:CODEX_HOME) {
        $codexHome = $env:CODEX_HOME
    }

    $resolvedInstallDir = Join-Path (Join-Path $codexHome "pets") $PetId
    if (Test-Text $env:HEI_MAO_INSTALL_DIR) {
        $resolvedInstallDir = $env:HEI_MAO_INSTALL_DIR
    }
    if (Test-Text $InstallDir) {
        $resolvedInstallDir = $InstallDir
    }

    $tempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("hei-mao-" + [System.Guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $tempDir -Force | Out-Null
    Write-Detail "Target: $resolvedInstallDir"
    Write-Detail "Work dir: $tempDir"

    try {
        Write-Step "Fetch assets"
        Copy-OrDownloadAsset -TempDir $tempDir -ResolvedBaseUrl $resolvedBaseUrl

        Write-Step "Validate package"
        Test-Asset -TempDir $tempDir
        Write-Success "Package metadata and spritesheet are valid."

        Write-Step "Install files"
        New-Item -ItemType Directory -Path $resolvedInstallDir -Force | Out-Null
        Copy-Item -LiteralPath (Join-Path $tempDir "pet.json") -Destination (Join-Path $resolvedInstallDir "pet.json") -Force
        Copy-Item -LiteralPath (Join-Path $tempDir "spritesheet.webp") -Destination (Join-Path $resolvedInstallDir "spritesheet.webp") -Force
        Write-Detail "Wrote: pet.json"
        Write-Detail "Wrote: spritesheet.webp"
    }
    finally {
        if (Test-Path -LiteralPath $tempDir) {
            Remove-Item -LiteralPath $tempDir -Recurse -Force
        }
    }

    Write-Output ""
    Write-Success "$PetId pet installed."
    Write-Detail "Install dir: $resolvedInstallDir"
    Write-Detail "Next: Codex App settings -> Appearance -> Pets -> Refresh -> $PetId"
    Write-Output ""
    exit 0
}
catch {
    Write-Output ""
    Write-Failure "Installation failed."
    Write-Error $_
    exit 1
}
