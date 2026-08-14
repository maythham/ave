$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$env:AVE_BRIDGE_PORT = if ($env:AVE_BRIDGE_PORT) { $env:AVE_BRIDGE_PORT } else { '8765' }
if (-not $env:AVE_BRIDGE_TOKEN) {
  $env:AVE_BRIDGE_TOKEN = Read-Host 'Enter a local AVE bridge token'
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { throw 'Python is not on PATH.' }
if (-not (Get-Command adb -ErrorAction SilentlyContinue)) { Write-Warning 'adb is not on PATH.' }
if (-not (Get-Command emulator -ErrorAction SilentlyContinue)) { Write-Warning 'emulator is not on PATH.' }
if (-not (Get-Command frida -ErrorAction SilentlyContinue)) { Write-Warning 'frida is not on PATH.' }
python (Join-Path $here 'bridge.py')
