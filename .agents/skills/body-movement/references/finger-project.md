# Finger project (referenced in place)

The verified pipeline lives in workspace-relative `movement/finger`.
This skill does not copy those files. `scripts/` and `tests/` are
launchers that `chdir` there and exec the original modules.

## Entry points

- Animate: `python3 scripts/animate_finger.py` (from this skill), or
  `python3 animate_finger.py` from `movement/finger`.
- Validate: `python3 tests/check_animation.py` (from this skill), or
  `python3 check_animation.py` from `movement/finger`.

## Joints and full-curl target

Stations in mesh parameter s: MCP 0.00, PIP 0.44, DIP 0.70.
Full curl degrees (MCP, PIP, DIP): 70, 90, 60.
Zero flexion reproduces the rest mesh (`straight.obj`).

## Acceptance (mandatory, no scored rubric)

Known-bad controls must fail first: a naive straight-to-full vertex lerp
must fall outside 90%–110% volume, and a forced 1 mm offset must fail A3.

- A1 `videos/finger_curl.gif` exists and has at least 24 frames.
- A2 tip displacement straight-to-full is greater than 10 mm; frames change.
- A3 frame 0 matches rest within 1e-6 m on every vertex.
- A4 every frame's skin volume stays within 90% to 110% of straight.
- A5 no non-adjacent triangle intersection.
- A6 median nail-to-skin gap stays within 0.15 mm of straight.
- A7 is skipped when no Unity sandbox marker is present.

A volume ratio of 0.90 is inside the band; a tip move of 10 mm is not
greater than 10 mm.

## Out of scope

`check_rig.py`, `check_v004.py`, `check_v003.py`, and `check_iteration.py`
need `movement/Versions/v00x/` and embed a host-absolute sim-world path.
They are not packaged as passing tests.

`check_animation.py` compares frame 0 to
`sim-world/finger/v004/Finger.obj` when that file exists on the machine.
That path is not portable. When it is absent, the check uses local rest
vertices. Do not rewrite the working file.

Unity Editor playback of `FingerUnity/` is unverified when no editor runs.
