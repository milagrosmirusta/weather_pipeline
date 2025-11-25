# set_env.ps1
$env:DAGSTER_HOME = "$PSScriptRoot\dagster_home"
Write-Host "✅ DAGSTER_HOME configurado en: $env:DAGSTER_HOME"