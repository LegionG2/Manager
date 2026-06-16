$ErrorActionPreference = "Stop"

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$mainPath = Join-Path $repoRoot "main.py"
$vbsPath = Join-Path $repoRoot "Start_Manager.vbs"
$shortcutPath = Join-Path ([Environment]::GetFolderPath("Desktop")) "Manager.lnk"
$assetsDir = Join-Path $repoRoot "assets"
$iconPath = Join-Path $assetsDir "manager.ico"

if (-not (Test-Path $mainPath)) {
    throw "Nie znaleziono main.py w: $repoRoot"
}

if (-not (Test-Path $vbsPath)) {
    throw "Nie znaleziono Start_Manager.vbs w: $repoRoot"
}

if (-not (Test-Path $assetsDir)) {
    New-Item -ItemType Directory -Path $assetsDir | Out-Null
}

# Prosta lokalna ikona Managera. Skrypt zapisuje ja do assets\manager.ico,
# zeby skrot mial wlasna ikone bez recznego kopiowania plikow.
$iconBase64 = @"
AAABAAEAQEAAAAAAIACpAwAAFgAAAIlQTkcNChoKAAAADUlIRFIAAABAAAAAQAgGAAAAqmlx3gAA
A3BJREFUeJztm8tPE1EUxj8oKLGggClGQoihapRUjA9sBg2aEOSR6IpIKPwDbtwaF65cGBeuXbkw
sbjRSIyhYvCFCBLAJwEJQZQFYBoTSRAKCHXRNMzrdmbazrmddn67uffOzDnfPXPOnektYGNjY5PB
ZCV6gR1ubzgZhsTL8vRQQj7EdTJvp1nEI0a20RNS1XkgPtt0K8a6uOvwGaP3TCrBiX7Vdr3RoGuQ
mvO8HZejJoQeETQHyJ1PNcflyIXQEsFQDkh15wHjNsYUQDz7VnA+ithWrcTIFCCVs71RYvmi6xGw
0uxH0Wuz4XVAuqEqgFWffTl6coEdAbwN4I0tAG8DeGMLwNsA3mS8ADnJulDvnasodRUy+2/fD+Bu
V5+ua926cgkXao8x+9+MfsPlm/eMmqgKWQS0NQhwZGvfbndhPhprqggsikAmQKmrEOdOHtIc11rv
RW6Og8CiCKQ5oKP5dMz+HIcDree9RNZEIBXA66nAgfI9zP4GwQNXUQGhRRyqQHuTwOzraK4htCSC
6QKs/9uQHF+sPY4CZ55inMddhqMHy2OeawamC9Az+FVynLc9Fy111YpxarP/bOCLaXZFMV2ARy+G
EVpdl7S1NQrIztr6WFu8Kx+NNUckY2YXfqPvw6TZ5pkvwOLSCp70fZS0lZUU4eyJrZLYWn8K23Kl
azJ/YBBhgq+SJEnQHxhQtEVDXq30LYfW8PjlCIVpNAJMzf7C0Nh3SZtQtR8VZSVoEDwoKd4p6et6
PYqllVUK0+jKoFoUtDcJaJclv3A4DH/3IJVZyXsZ0uLV8ATmgn8kL0wtddWKZe+7z1OYmQtSmUUX
ARubm3jQI51ZtTW/P0A3+wDxSvBh7whCa+vMfqrSJ4ZUgMWlZTx9+4nZHyl9tL/Ikb8L+LuVyRCg
LX1iyAWY/LmA4fEZRTtl6RPD5ZugPAqoS58YsjIo5vn7MVS2XONxawUZ/1U44wXg8giYhdM3Lzn+
27lX8xzVCBDvrGLtw0slnL55hfPR9n033ADYu8WYW8issklCzXE1xn2dqr7qygFWiIJ4YQqQ6C5s
CvTOPgBUdvqMb5GxWi6IB0NlMB1F0BRA/igEJ/rTSgjLb5dPtAroXghFI0EuBO9ocMKd0PmGl8Kp
Vh1+XJ/WHMOafSDN/jQlL3WxHLexsbGxAfAfUrsODmojczQAAAAASUVORK5CYII=
"@

try {
    $cleanIconBase64 = $iconBase64 -replace '\s', ''
    [System.IO.File]::WriteAllBytes($iconPath, [Convert]::FromBase64String($cleanIconBase64))
} catch {
    Write-Warning "Nie udalo sie utworzyc wlasnej ikony. Skrot zostanie utworzony bez niej. Szczegoly: $($_.Exception.Message)"
    $iconPath = $null
}

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = [string]$vbsPath
$shortcut.WorkingDirectory = [string]$repoRoot
$shortcut.Description = "Manager"

if ($iconPath -and (Test-Path $iconPath)) {
    $shortcut.IconLocation = "$iconPath,0"
}

$shortcut.Save()

Write-Host "Skrót utworzony: $shortcutPath"
if ($iconPath -and (Test-Path $iconPath)) {
    Write-Host "Ikona: $iconPath"
}
Write-Host "Uruchamianie: $vbsPath"