# AVE Windows / Android Bridge

Local-only bridge design for the AVE development workstation.

## Purpose

This bridge is intended to let a local automation client inspect a Windows development machine and Android Studio emulator through existing command-line tools:

- Windows PowerShell / CMD
- Android SDK `adb`
- Android Studio emulator (`emulator` / `avdmanager`)
- Frida CLI when installed (`frida`, `frida-ps`, `frida-trace`)
- Git and project files

## Security model

The bridge MUST bind to `127.0.0.1` only. It must not expose a raw unauthenticated shell to the LAN or Internet. Commands should be implemented as explicit operations/allowlists rather than accepting arbitrary shell text from remote clients.

Recommended operations:

- `system_info`
- `project_tree`
- `adb_devices`
- `adb_shell_readonly`
- `emulator_list`
- `frida_devices`
- `frida_processes`
- `git_status`
- `run_tests`

Destructive operations should require an explicit local confirmation step.

## Important limitation

Running this bridge on Windows does NOT automatically give a ChatGPT conversation direct access to localhost. A ChatGPT connector/agent integration is still required to invoke the bridge from a conversation. The bridge itself is therefore kept local and safe by default.

## Android / Frida

For emulator inspection, first ensure `adb devices` sees the emulator. For Frida, ensure the matching `frida-server` is running inside the emulator/device and that the host-side Frida tools can enumerate it.
