## Ensure that Blender is installed
if (-not (Get-Command blender -ErrorAction SilentlyContinue)) {
    $time = Get-Date -Format HH:mm:ss
    [Console]::Error.WriteLine("[$time] ERROR    Blender is not in PATH")
    exit 1
}

## Filter args from unused Python flags
$argsFiltered = @()
foreach ($arg in $args) {
    if ($arg -eq "-I" -or $arg -eq "-c") {
        continue
    }
    $argsFiltered += $arg
}

## Process args
if ($argsFiltered.Count -eq 0) {
    $time = Get-Date -Format HH:mm:ss
    [Console]::Error.WriteLine("[$time] ERROR    At least one argument is required")
    exit 2
}

if ($argsFiltered.Count -gt 1) {
    $pythonPrelude = "import sys`nsys.argv=[sys.argv[0],*sys.argv[sys.argv.index('--')+1:]]"
}
else {
    $pythonPrelude = "import sys`nsys.argv=[sys.argv[0]]"
}

if ($argsFiltered.Count -eq 1) {
    $otherArgs = @()
}
else {
    $otherArgs = @("--") + $argsFiltered[1..($argsFiltered.Count - 1)]
}

## Run Python expression in a Blender process
$tempScript = [System.IO.Path]::Combine([System.IO.Path]::GetTempPath(), "simforge_blender_$( [guid]::NewGuid().ToString('N') ).py")
$exitCode = 0
try {
    Set-Content -Path $tempScript -Value ($pythonPrelude + "`n" + $argsFiltered[0])

    $blenderArgs = @(
        "--factory-startup"
        "--background"
        "--offline-mode"
        "--quiet"
        "--enable-autoexec"
        "--python-exit-code"
        "1"
        "--python"
        $tempScript
    ) + $otherArgs

    if ($env:SF_LOG_LEVEL -eq "debug") {
        $time = Get-Date -Format HH:mm:ss
        [Console]::Error.WriteLine("[$time] DEBUG    blender $($blenderArgs -join ' ')")
    }

    & blender @blenderArgs
    $exitCode = $LASTEXITCODE
}
finally {
    if (Test-Path $tempScript) {
        Remove-Item -Force $tempScript
    }
}

exit $exitCode
