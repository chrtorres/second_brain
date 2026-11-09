#!/usr/bin/env python3
"""Locate the finger project and run a named file from that directory.

The implementation in movement/finger is not relocatable. Skill package
scripts and tests are launchers; they do not copy the mesh pipeline.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def locate_finger() -> Path:
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "movement" / "finger"
        if (candidate / "animate_finger.py").is_file() and (
            candidate / "check_animation.py"
        ).is_file():
            return candidate
    raise SystemExit("movement/finger not found from this skill package")


def run_in_finger(script_name: str) -> int:
    finger = locate_finger()
    script = finger / script_name
    if not script.is_file():
        raise SystemExit(f"{script} is missing")
    os.chdir(finger)
    os.execv(sys.executable, [sys.executable, str(script), *sys.argv[1:]])
    return 1
