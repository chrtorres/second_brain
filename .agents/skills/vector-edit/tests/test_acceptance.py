"""Lock the vector-edit acceptance boundaries.

A garment check must fail on an untouched white shirt. The same check must
pass on a shirt that has become a tank top. Equality follows the comparison
written in the procedure.
"""

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import acceptance


def white_shirt(shape=(634, 597, 3)):
    image = np.zeros(shape, dtype=np.uint8)
    image[280:410, 145:250] = (230, 220, 210)
    for x, y in acceptance.COLLAR + acceptance.CUFF:
        image[y, x] = (230, 220, 210)
    return image


def tank_top(source):
    image = source.copy()
    skin = np.array([200, 130, 70], dtype=np.uint8)
    cloth = np.array([230, 220, 210], dtype=np.uint8)
    image[280:410, 145:250] = skin
    image[300:380, 180:230] = cloth
    for x, y in acceptance.COLLAR + acceptance.CUFF:
        image[y, x] = skin
    return image


def test_garment_checks_fail_on_untouched_shirt():
    source = white_shirt()
    result = acceptance.evaluate(source, source)
    for name in acceptance.GARMENT_CHECKS:
        assert result[name] is False
    for name in acceptance.PRESERVATION_CHECKS:
        assert result[name] is True


def test_edited_shirt_passes_every_check():
    source = white_shirt()
    edited = tank_top(source)
    result = acceptance.evaluate(edited, source)
    assert all(result.values())
    assert acceptance.bare_arm_count(edited) >= acceptance.SKIN_MIN
    assert acceptance.tank_cloth_count(edited) >= acceptance.FABRIC_MIN


def test_bare_arm_boundary():
    source = white_shirt()
    low = source.copy()
    high = source.copy()
    skin = np.array([200, 130, 70], dtype=np.uint8)
    # Fill from the top-left of the count window. 2499 fails and 2500 passes.
    low[280:410, 145:250].reshape(-1, 3)[:2499] = skin
    high[280:410, 145:250].reshape(-1, 3)[:2500] = skin
    assert acceptance.bare_arm_count(low) == 2499
    assert acceptance.bare_arm_count(high) == 2500
    assert acceptance.evaluate(low, source)["bare arm skin in the torso window"] is False
    assert acceptance.evaluate(high, source)["bare arm skin in the torso window"] is True


def test_tank_cloth_boundary():
    image = np.zeros((634, 597, 3), dtype=np.uint8)
    cloth = np.array([230, 220, 210], dtype=np.uint8)
    image[280:410, 145:250].reshape(-1, 3)[:1499] = cloth
    assert acceptance.tank_cloth_count(image) == 1499
    assert acceptance.evaluate(image, image)["tank cloth remains in the torso window"] is False
    image[280:410, 145:250].reshape(-1, 3)[1499] = cloth
    assert acceptance.tank_cloth_count(image) == 1500
    assert acceptance.evaluate(image, image)["tank cloth remains in the torso window"] is True


def test_pixel_class_boundaries():
    assert acceptance.white_cloth((116, 116, 116)) is True
    assert acceptance.white_cloth((115, 115, 115)) is False
    assert acceptance.white_cloth((160, 106, 116)) is True  # chroma 54
    assert acceptance.white_cloth((160, 105, 116)) is False  # chroma 55
    assert acceptance.white_cloth((160, 160, 116)) is True  # red-blue 44
    assert acceptance.white_cloth((160, 160, 115)) is False  # red-blue 45

    assert acceptance.skin_pixel((146, 90, 100)) is True  # red-blue 46
    assert acceptance.skin_pixel((145, 90, 100)) is False  # red-blue 45
    assert acceptance.skin_pixel((101, 60, 50)) is True
    assert acceptance.skin_pixel((100, 60, 50)) is False
    assert acceptance.skin_pixel((101, 56, 40)) is True
    assert acceptance.skin_pixel((101, 55, 40)) is False
    assert acceptance.skin_pixel((101, 109, 50)) is True  # red equals green minus 8
    assert acceptance.skin_pixel((101, 110, 50)) is False


def test_change_outside_window_fails():
    source = white_shirt()
    edited = source.copy()
    edited[274, 135] = (1, 2, 3)
    assert acceptance.outside_matches(edited, source) is False
    edited = source.copy()
    edited[275, 134] = (1, 2, 3)
    assert acceptance.outside_matches(edited, source) is False
    edited = source.copy()
    edited[275, 135] = (9, 9, 9)
    edited[415, 260] = (8, 8, 8)
    assert acceptance.outside_matches(edited, source) is True


def test_preserve_probe_must_match():
    source = white_shirt()
    edited = source.copy()
    x, y = acceptance.PRESERVE[0]
    edited[y, x] = (1, 2, 3)
    assert acceptance.preserve_matches(edited, source) is False


def test_alignment_and_feather_boundaries():
    assert acceptance.alignment_continues(80) is True
    assert acceptance.alignment_continues(79) is False
    assert acceptance.feather_keeps_source(0.02) is False
    assert acceptance.feather_keeps_source(0.019) is True


def test_thresholds_stay_fixed():
    assert acceptance.SKIN_MIN == 2500
    assert acceptance.FABRIC_MIN == 1500
    assert acceptance.INLIER_MIN == 80
    assert acceptance.FEATHER_KEEP_BELOW == 0.02
    assert set(acceptance.GARMENT_CHECKS) == {
        "collar probes are skin",
        "cuff probes are not white cloth",
        "bare arm skin in the torso window",
    }
