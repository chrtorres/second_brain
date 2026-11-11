---
name: verify-unity-game-playable
description: Gets a Unity project running on Linux without root and proves it is playable with an automated playthrough, a known-bad control, and real keyboard and mouse input, while the user's original files stay unchanged. Use when a user hands over a Unity project or archive, cannot run it, and wants it run and verified as fully playable.
---

# Verify Unity game playable

Work in a sandbox and leave the user's original project or archive unchanged. The user's game is the subject; the verification harness never ships in what the user plays.

## 1. Record and sandbox

1. Record the real tree before anything runs: `git status --short` of each repository nearby and a hash of the archive or project file. Note any directory listing you will compare later.
2. Extract a copy into a temporary directory outside the real tree, along with a marker file. Keep two copies: an untouched **original** (the known-bad control) and a **fixed** copy for repairs.
3. Read the project: `ProjectSettings/ProjectVersion.txt` (exact editor version), `Packages/manifest.json` (available modules), the scripts, and any README play instructions.
4. Write the acceptance definition before changing code. Cover: compiles with 0 errors, the scene exists, no exceptions during play, HUD visible, the core loop (spawn, move, damage, rewards, win, lose), every listed control, and a standalone build that launches.

## 2. Install the exact editor without root

1. Get the download URL for the exact version from `https://services.api.unity.com/unity/editor/release/v1/releases?version=<version>&platform=LINUX&architecture=X86_64`.
2. Download the `.tar.xz` in the background. Extract it to `~/Unity/Hub/Editor/<version>/` so Hub can locate it.
3. Get Unity Hub's `.deb` from the Hub apt repository's `Packages` index and unpack it with `dpkg-deb -x` into a user directory. Launch `unityhub-bin --no-sandbox`.
4. The editor refuses to compile or build until a license exists. The user must sign in through Hub, which activates a Personal license. That step is theirs; if it is not done, stop and report the work as incomplete.
5. If the browser says no app can open the login callback, register the handler. Write `~/.local/share/applications/unityhub.desktop` with `Exec=<path>/unityhub-bin --no-sandbox %U` and `MimeType=x-scheme-handler/unityhub;`. Then run `xdg-mime default unityhub.desktop x-scheme-handler/unityhub`, have the user retry the sign-in, and confirm a license file appears under `~/.config/unity3d/Unity/licenses/`.

## 3. Read the code for defects

Check for these before building:

- `GUI.skin`, or styles built from it, accessed outside `OnGUI`. This throws "You can only call GUI functions from inside OnGUI". Build the styles lazily inside `OnGUI`.
- Logic that treats a `Destroy`ed object as gone in the same frame. Destruction is deferred to the end of the frame, so a second hit can pay a reward twice. Check list membership or a dead flag instead.

Apply each fix to the fixed copy only.

## 4. Build headless

1. Add an editor-only build script to both sandbox copies. Launch it with `-batchmode -executeMethod`. It registers an `EditorApplication.update` callback that waits, with a timeout, for the project's own bootstrap to save the scene. Then it calls `BuildPipeline.BuildPlayer` for `StandaloneLinux64` and calls `EditorApplication.Exit` with the result. Do not pass `-quit`, or the editor exits before the bootstrap runs.
2. Build both copies. Grep the editor log for `error CS` and for the script's pass and fail markers.

## 5. Automated playthrough probe

1. Add a runtime probe to both copies. It is inert unless the player is launched with a probe argument. It attaches through `RuntimeInitializeOnLoadMethod` and drives the game by reflection on its private fields and methods.
2. Check initial state, timing of the first enemy wave, movement, placement costs and refusals, upgrade, sell, pause, a full win, restart, and a full loss.
3. Count `LogType.Exception` and `LogType.Error` through `Application.logMessageReceived`.
4. Account for the economy with a whole-run ledger computed from the game's own rules. Without leaks, kills must equal the number of enemies spawned. Final credits must equal starting credits, plus the probe's own spending, plus one reward per enemy, plus every wave bonus.
   - A frame-to-frame diff cannot be the gate. It misses enemies that spawn and die within a single frame.
   - Coroutine checks run before `LateUpdate` in the same frame, so the final frame's events are not yet audited.
5. Re-baseline the ledger after the probe calls restart.
6. Take screenshots with `ReadPixels`, writing PPM files, when the manifest lacks the screencapture or imageconversion modules. Do not add packages to the project under test. Convert the PPMs to PNG outside Unity and read them to confirm the HUD, win screen and loss screen are visible.
7. Run the original first. Each check you trust must fail there for the known defect. Then run the fixed build. Use generous timeouts on the original: per-frame exception spam slows it down.

## 6. Real input

1. Run the fixed player windowed with the probe in watch mode. Each frame it writes state to a file: the game's fields, `Input.mousePosition`, and the live screen positions of the targets it needs, such as pads, a placed tower and the HUD buttons.
2. Drive the player with XTEST from python-xlib in a virtual environment. Calibrate first: move the pointer to a known root position, read the mouse position Unity reports, and derive the offset. The X window includes client-side decorations, so its geometry is not the game area.
3. Re-read target positions after any camera orbit or zoom.
4. Reject a state read unless it contains the last field. The game rewrites the file every frame, so reads can be torn.
5. Exercise every listed key, click and button. Confirm each change from the game's state, not from the action alone.

## 7. Repair loop and final run

1. When a check fails, decide whether the game or the harness is wrong. Change a check only when a game rule shows the check is wrong, and say which rule.
2. Rerun the affected checks after each fix. On the final build, rerun the complete automated suite and the input suite.
3. Re-check the real tree against the record. Report any new paths you did not create rather than deleting them.

## 8. Deliver

1. Copy the fixed project to a user location outside the repositories and remove the probe.
2. Build the player with the build script, then delete the script.
3. Confirm the probe is absent from `Assembly-CSharp.dll`, and diff the scripts against the original so the only changes are the fixes.
4. Launch the game for the user and check its log for exceptions.
5. Report passed/total for each suite, the defects fixed with control-versus-fixed evidence, how to launch the build or open the project in Hub, and what was not exercised, such as the editor's Play button.
