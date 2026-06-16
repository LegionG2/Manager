$ErrorActionPreference = "Stop"

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$mainPath = Join-Path $repoRoot "main.py"
$shortcutPath = Join-Path ([Environment]::GetFolderPath("Desktop")) "Manager.lnk"

if (-not (Test-Path $mainPath)) {
    throw "Nie znaleziono main.py w: $repoRoot"
}

$targetPath = $null
$arguments = $null

$venvPythonw = Join-Path $repoRoot ".venv\Scripts\pythonw.exe"
if (Test-Path $venvPythonw) {
    $targetPath = $venvPythonw
    $arguments = "`"$mainPath`""
} else {
    $pythonw = Get-Command "pythonw.exe" -ErrorAction SilentlyContinue
    if ($pythonw) {
        $targetPath = $pythonw.Source
        $arguments = "`"$mainPath`""
    } else {
        $pyw = Get-Command "pyw.exe" -ErrorAction SilentlyContinue
        if ($pyw) {
            $targetPath = $pyw.Source
            $arguments = "-3 `"$mainPath`""
        } else {
            $python = Get-Command "python.exe" -ErrorAction SilentlyContinue
            if ($python) {
                $targetPath = $python.Source
                $arguments = "`"$mainPath`""
            }
        }
    }
}

if (-not $targetPath) {
    throw "Nie znaleziono pythonw.exe, pyw.exe ani python.exe."
}

$wshShell = New-Object -ComObject WScript.Shell
$shortcut = $wshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.Arguments = $arguments
$shortcut.WorkingDirectory = $repoRoot
$shortcut.Description = "Uruchom Manager"
$shortcut.IconLocation = "$targetPath,0"
$shortcut.Save()

Write-Host "Utworzono skrót:" $shortcutPath
Write-Host "Target:" $targetPath
Write-Host "Arguments:" $arguments
