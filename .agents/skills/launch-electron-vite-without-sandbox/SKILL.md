---
name: launch-electron-vite-without-sandbox
description: >-
  Starts an electron-vite app when Linux rejects the setuid sandbox helper.
  Use when Electron aborts because chrome-sandbox is not root-owned mode 4755,
  or when disabling only the setuid sandbox reports that no sandbox is usable.
---

# Launch Electron Vite without sandbox

The setuid sandbox helper aborts Electron before application code runs when `chrome-sandbox` is not owned by root with mode 4755. A switch set in the main process cannot prevent that abort. The flag has to be on the Electron command line.

1. Start the project the way it starts Electron, with no sandbox flag added. Record the exit status and stderr.

2. Stop if that launch stays up. Do not add `--no-sandbox`.

3. When stderr says the SUID sandbox helper is not configured and requires mode 4755, do not change the helper's owner or mode. That requires root and does not survive reinstalling Electron.

4. Launch again with only the setuid sandbox disabled (`--disable-setuid-sandbox` on the Electron command line). If that process stays up, keep that flag and stop. Do not disable the sandbox entirely.

5. When that launch exits saying there is no usable sandbox because unprivileged user namespaces are blocked, pass electron-vite `--noSandbox` on every script that starts Electron, including dev and preview. electron-vite turns that option into `--no-sandbox` on the spawned Electron process.

6. Acceptance requires both results on the final scripts:
   - The unflagged start still exits with the SUID sandbox fatal. A check that passes without that failure does not show the flag is still required.
   - The flagged start stays running. Its output contains the electron-vite start notice and does not contain the SUID fatal. The Electron command line includes `--no-sandbox`, and a renderer process exists for that app.

7. On a Wayland session, an X11 window-tree listing does not show the window. Do not treat that absence as a failed launch. Confirm the process command line and the renderer, or use a window query the session actually permits.
