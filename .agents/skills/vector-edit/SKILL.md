---
name: vector-edit
description: >-
  Replaces a garment in a photograph by segmenting cloth with color vectors
  and aligning a photographic plate with feature vectors, then accepts the
  edit only when the untouched photo fails the garment checks and the saved
  edit passes them. Use when asked to change clothing in a photo with vector
  analysis, including changing a shirt into a tank top, and the rest of the
  photo must stay unchanged.
---

# Vector edit

Change one garment in a photograph. Keep every pixel outside that person's upper body identical to the source. A flat color painted into a geometric outline is not a finished edit.

Write the acceptance checks before editing. Run the garment checks on the untouched source first. Completion is those checks on the saved file, plus a look at the full frame.

## Checks

Use mandatory pass/fail checks. Do not invent a percentage. These boundaries are strict. A value that does not satisfy the comparison fails.

Skin pixel, all of these:

- red minus blue is greater than 45
- red is greater than 100
- green is greater than 55
- max channel minus min channel is greater than 40
- red is greater than or equal to green minus 8

White-cloth pixel for the cuff check, all of these:

- mean of the three channels is greater than 115
- max channel minus min channel is less than 55
- red minus blue is less than 45

Count window: rows `[280, 410)` and columns `[145, 250)`.

Bare-arm count: pixels in that window with red minus blue greater than 45, red greater than 100, green greater than 55, and max minus min greater than 40. Pass when the count is greater than or equal to 2500. 2499 fails.

Tank-cloth count: pixels in that window with mean greater than 140, max minus min less than 50, and red minus blue less than 45. Pass when the count is greater than or equal to 1500. 1499 fails.

Upper-body window, inclusive: columns 135 through 260, rows 275 through 415. Every pixel outside that window must equal the source.

Garment checks, which must fail on the untouched source:

- Each collar probe is a skin pixel.
- Each cuff probe is not a white-cloth pixel.
- The bare-arm count passes.

Preservation checks, which must already pass on the source:

- The tank-cloth count passes.
- Face, hands, pants, and the other person match the source at their probes.
- Every pixel outside the upper-body window matches the source.

A garment check that passes on the source does not count. Do not lower 2500 or 1500, drop a probe, or move a failing check out of the garment set. Probe coordinates belong to the source photograph: put collar probes on the collar and cuff probes on the rolled cuff before editing, and keep those coordinates fixed.

## Segment the cloth

On the source, mark cloth with color vectors inside the person's upper body:

- not skin, where skin is red minus blue greater than 60, red greater than 90, green greater than 40, and red greater than green minus 5
- mean greater than 88 and less than 252
- max minus min less than 50
- red minus blue less than 50

Close the mask with a 2-iteration binary closing, fill holes, and keep it inside the upper-body region and off skin. Dilate by 5 pixels. Then cut away the face (rows before 282), the hands (rows from 405), and the other person (columns from 250). Keep original forearm skin on rows after 392.

## Do not accept a flat fill

Painting a median skin color into a capsule or polygon can pass a few probes and still look like a sticker. Reject that result. These failures came from that approach:

- The rolled cuff stays white when the arm shape stops above it. The cuff probes exist to catch that.
- A gap between the neckline and the arm leaves a white band and then a near-black band. The bare arm has to start at the strap.
- Copying nearby tree pixels into the sleeve turns bright cloth into a black hole. Do not fill the arm that way.
- Driving the arm color toward the darkest forearm hairs, or blurring in pixels from outside the mask, turns the arm black.
- Probe passes are not enough. Look at the full frame.

## Align a photographic plate

Make a plate of the same scene in which that person wears the new garment. Align it to the source with feature vectors:

- Set the random seed to 0 before RANSAC. Run alignment once. Do not repeat it until one favorable run appears.
- ORB with 900 keypoints and a fast threshold of 0.05, on both grayscale images.
- Cross-checked descriptor matches.
- A similarity transform from RANSAC with a minimum of 3 samples, a residual threshold of 3, and 4000 trials.
- Stop when the model is missing or the inlier count is less than 80. 80 inliers continues. 79 stops.
- Warp the plate through the inverse transform into the source frame, linear order, preserving range. Clip to 0 through 255.

## Composite

Feather the cloth mask with a Gaussian of sigma 1.2. Where the feather is less than 0.02, write the source pixel unchanged. 0.02 is not less than 0.02, so that value may still blend. Blend the warped plate over the source by the feather everywhere else.

If any changed pixel falls outside the upper-body window, stop and do not treat the file as finished.

Save a new file. Leave the source bytes unchanged.

## Accept

Run every check on the saved file. Every garment check and every preservation check must pass. Then look at the full frame: the new garment must read as that garment, the bare limb must meet the existing skin, and the other person and the background must be the original photograph.

The tests in `tests/` lock these boundaries. Run them after any change to a threshold. They do not replace looking at the full frame, and they do not edit the photograph.
