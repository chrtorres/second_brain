"""Acceptance boundaries for a vector garment edit.

The comparisons are the ones the procedure states. Equality is not a pass
where the comparison is strict.
"""

COLLAR = ((188, 293), (192, 296), (200, 294))
CUFF = ((196, 372), (198, 368), (192, 360))
PRESERVE = (
    (200, 260),
    (210, 250),
    (190, 270),
    (240, 420),
    (250, 425),
    (160, 450),
    (170, 470),
    (360, 360),
    (400, 420),
    (340, 480),
)
# Inclusive columns and rows. Pixels outside this window must match the source.
WIN = (135, 275, 260, 415)
SKIN_MIN = 2500
FABRIC_MIN = 1500
INLIER_MIN = 80
FEATHER_KEEP_BELOW = 0.02

GARMENT_CHECKS = (
    "collar probes are skin",
    "cuff probes are not white cloth",
    "bare arm skin in the torso window",
)
PRESERVATION_CHECKS = (
    "tank cloth remains in the torso window",
    "face, hands, pants, and the other person unchanged",
    "outside the upper-body window unchanged",
)


def skin_pixel(pixel):
    red, green, blue = (int(channel) for channel in pixel)
    chroma = max(red, green, blue) - min(red, green, blue)
    return (
        (red - blue) > 45
        and red > 100
        and green > 55
        and chroma > 40
        and red >= green - 8
    )


def white_cloth(pixel):
    red, green, blue = (int(channel) for channel in pixel)
    mean = (red + green + blue) / 3
    chroma = max(red, green, blue) - min(red, green, blue)
    return mean > 115 and chroma < 55 and (red - blue) < 45


def bare_arm_count(image):
    window = image[280:410, 145:250]
    red = window[:, :, 0].astype(int)
    green = window[:, :, 1].astype(int)
    blue = window[:, :, 2].astype(int)
    chroma = window.max(axis=2) - window.min(axis=2)
    mask = ((red - blue) > 45) & (red > 100) & (green > 55) & (chroma > 40)
    return int(mask.sum())


def tank_cloth_count(image):
    window = image[280:410, 145:250]
    red = window[:, :, 0].astype(int)
    blue = window[:, :, 2].astype(int)
    mean = window.astype(float).mean(axis=2)
    chroma = window.max(axis=2) - window.min(axis=2)
    mask = (mean > 140) & (chroma < 50) & ((red - blue) < 45)
    return int(mask.sum())


def outside_matches(image, source):
    x0, y0, x1, y1 = WIN
    outside = image.copy()
    outside[y0 : y1 + 1, x0 : x1 + 1] = source[y0 : y1 + 1, x0 : x1 + 1]
    return bool((outside == source).all())


def preserve_matches(image, source):
    return all(
        tuple(int(channel) for channel in image[y, x])
        == tuple(int(channel) for channel in source[y, x])
        for x, y in PRESERVE
    )


def evaluate(image, source):
    skin = bare_arm_count(image)
    fabric = tank_cloth_count(image)
    return {
        "collar probes are skin": all(skin_pixel(image[y, x]) for x, y in COLLAR),
        "cuff probes are not white cloth": all(not white_cloth(image[y, x]) for x, y in CUFF),
        "bare arm skin in the torso window": skin >= SKIN_MIN,
        "tank cloth remains in the torso window": fabric >= FABRIC_MIN,
        "face, hands, pants, and the other person unchanged": preserve_matches(image, source),
        "outside the upper-body window unchanged": outside_matches(image, source),
    }


def alignment_continues(inliers):
    return inliers >= INLIER_MIN


def feather_keeps_source(feather):
    return feather < FEATHER_KEEP_BELOW
