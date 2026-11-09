---
name: body-movement
description: >-
  Builds, poses, and animates the anatomical index-finger mesh with the
  MCP/PIP/DIP rig, then verifies the curl against volume, self-intersection,
  and nail-gap checks. Use when posing or animating the finger, extending
  the movement rig to new joints or digits, or regenerating the curl video
  from the existing rest mesh.
---

# Body movement

This package always has `scripts/` and `tests/`. Add `assets/` or
`references/` only when they hold files. `references/finger-project.md`
records joints, thresholds, and limits. There is no `assets/` directory;
the curl video stays in `movement/finger/videos`.

The mesh pipeline is not portable. `scripts/` and `tests/` launch the
files in workspace-relative `movement/finger`; they do not copy them.
Do not paste `check_animation.py` into `tests/`.

## Prerequisites

- Python 3 with Pillow (`PIL`). No other third-party package is required.
- The finger project files: `generate_finger.py`, `rig_finger.py`,
  `animate_finger.py`, `render_views.py`, `check_animation.py`,
  `acceptance.md`, `straight.obj`, and (after a render) `videos/finger_curl.gif`.

Owning repository for this skill is `second_brain`. The verified procedure
lives in the sibling `movement/finger` tree, which is not a git repository.

## Procedure

1. Pose and animate with `animate_finger.py`. It loads the rest mesh
   `straight.obj` (zero flexion), binds it to the centerline from
   `generate_finger.py`, and poses with `rig_finger.py`. Frame 0 reproduces
   the rest mesh. The curl eases to MCP 70, PIP 90, DIP 60 degrees and back
   on one frozen perspective camera with one shared scale.
2. Joint stations in mesh parameter s: MCP 0.00, PIP 0.44, DIP 0.70. Flexion
   is a rotation about the lateral axis toward the palm, blended across the
   rings already in the mesh so a cross-section keeps its rest shape.
3. Outputs land in `videos/`: `frames/`, `finger_curl.gif`, `finger_curl.webp`,
   `keyframes/`, and `unity/FingerFrames.txt` (baked OBJ frames for the Unity
   animator).

From this skill:

```
python3 scripts/animate_finger.py
```

From `movement/finger`:

```
python3 animate_finger.py
```

## Verify

From this skill:

```
python3 tests/check_animation.py
```

From `movement/finger`:

```
python3 check_animation.py
```

Mandatory checks. No scored rubric. Known-bad controls run first and must
fail before a pass counts: a naive straight-to-full vertex lerp must fall
outside the 90%-110% volume band, and a forced 1 mm offset must fail A3.

A pass requires all of:

- A1 `videos/finger_curl.gif` exists and has at least 24 frames.
- A2 fingertip displacement straight-to-full is greater than 10 mm, and
  adjacent frames differ.
- A3 frame 0 matches the rest mesh within 1e-6 m on every vertex.
- A4 every frame's skin volume stays within 90% to 110% of straight.
- A5 no frame reports a non-adjacent triangle intersection.
- A6 median nail-to-skin gap stays within 0.15 mm of straight.
- A7 is skipped when no Unity sandbox marker is present.

Do not treat a strict boundary as passed. A volume ratio of 0.90 is inside
the band; a tip move of 10 mm is not greater than 10 mm.

## Out of scope

`check_rig.py`, `check_v004.py`, `check_v003.py`, and `check_iteration.py`
belong to the sim-world finger version lineage. They require a
`movement/Versions/v00x/` tree that this project does not have, and they
embed absolute sim-world paths. They fail from `movement/finger`. Do not
copy them, and do not claim they passed.

`generate_finger.py` and `rig_finger.py` as command-line programs also
expect a parent Unity layout (`Assets/Models`, `Versions/v004`). The
verified animation path imports them as modules from `animate_finger.py`.
Do not run them as mains from this directory.

## Known limitations

- The acceptance test is not relocatable. A copy of `check_animation.py`
  in `tests/` fails with `ModuleNotFoundError: animate_finger`; adding the
  siblings to `PYTHONPATH` then fails on missing `straight.obj` and
  `videos/`. The packaged `tests/check_animation.py` is a launcher.
- `check_animation.py` compares frame 0 to an absolute sim-world rest mesh
  when that file exists on the machine. That path is not portable. When the
  file is absent, the check falls back to the local rest vertices.
- Unity editor playback of `FingerUnity/` stays unverified when no Unity
  editor runs. GIF/WEBP stand in for MP4 when ffmpeg is absent.
