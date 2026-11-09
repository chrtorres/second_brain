#!/usr/bin/env python3
"""Run the finger-curl acceptance checks from movement/finger.

Do not copy check_animation.py here. A relocated copy fails to import
animate_finger and then fails to find straight.obj. This launcher keeps
cwd and imports on the original project.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from finger_project import run_in_finger  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(run_in_finger("check_animation.py"))
