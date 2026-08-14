# AVE Windows / Android Bridge

Local bridge for inspecting the Windows development environment, Android Studio Emulator/AVD, ADB and Frida.

## What is implemented

`bridge.py` is a dependency-free Python HTTP service bound **only to `127.0.0.1`** and protected by `X-AVE-Token`.

Read endpoints:

- `GET /health`
- `GET /system`
- `GET /adb/devices`
- `GET /adb/packages`
- `GET /adb/prop?name=ro.product.cpu.abilist`
- `GET /emulator/avds`
- `GET /frida/processes`
- `GET /frida/devices`

Controlled actions:

- `POST /emulator/start` with `{ "avd": "NAME" }`
- `POST /emulator/stop` with `{ "serial": "emulator-5554" }`

There is deliberately **no arbitrary shell endpoint**. Commands use argument arrays (`shell=False`) and inputs are validated.

## Windows start

From PowerShell:

```powershell
$env:AVE_BRIDGE_TOKEN = "choose-a-long-random-token"
.\start_bridge.ps1
```

Or let the launcher ask for the token:

```powershell
.\start_bridge.ps1
```

The default address is `http://127.0.0.1:8765`.

## Android Emulator

Android's official command-line workflow supports `emulator -list-avds` and `emulator -avd NAME`; ADB can then inspect and control the running emulator. The emulator appears to ADB as a device. See the Android documentation linked from the project notes.

## Frida

The host needs the Frida CLI and the emulator/device needs a compatible Frida setup. The official Frida Android workflow uses ADB to deploy/start `frida-server` on suitable rooted environments and then verifies connectivity with `frida-ps -U`.

## Important limitation: ChatGPT connectivity

Running this service does **not** automatically give a ChatGPT conversation access to localhost. A connector/agent capable of reaching the local service is still required. Do not expose this port to the Internet just to make it reachable; if remote access is eventually required, use an authenticated, narrowly scoped connector or private network path.

## Safety

Do not put the token in Git. Do not commit secrets. Keep the listener on loopback. Destructive Android/file operations are intentionally absent from this first version.
