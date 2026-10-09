$taskDir=$PSScriptRoot
$taskCache=Join-Path $taskDir 'cache'
$env:TEMP=Join-Path $taskCache 'temp'
$env:TMP=$env:TEMP
$env:TMPDIR=$env:TEMP
$env:PYTHONPYCACHEPREFIX=Join-Path $taskCache 'python-bytecode'
$env:XDG_CACHE_HOME=$taskCache
$env:PYTHONIOENCODING='utf-8'
New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
$taskPython='C:/Users/nakan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
if(-not (Test-Path -LiteralPath $taskPython)){ $taskPython=(Get-Command python -ErrorAction Stop).Source }
& $taskPython (Join-Path $taskDir 'reexport.py') @args
exit $LASTEXITCODE
