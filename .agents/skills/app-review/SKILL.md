---
name: app-review
description: >-
  Reviews a running application against requirements taken from its window
  and tests, then records the result in a canvas and a dated log.
  Use when asked to run an application, canvas it, find its requirements,
  and write a review log.
---

# App review

Discover the application from the tree named in the request. Read its start command, window copy, and tests. Do not assume a stack, and do not reuse another project's hosts, ports, models, or directories.

## Requirements and acceptance

When the tree has no requirements document, the requirements are the behaviors the window and the tests describe. Do not invent requirements to fill the review.

Write the acceptance definition before running. Mandatory checks must all pass. For scored checks, use the bar the user stated, including whether equality passes. A bar stated as greater than a number does not pass when the result equals that number. When the user states no threshold and the checks form a rubric, the bar is >=95% of the scored checks. When there is no meaningful rubric, do not invent a percentage.

A check has to perform the action it judges. Waiting for a result without performing the action does not count. Prefer an observed outcome. The `hidden` attribute does not establish what is on screen. Confirm computed display and a box with size, or a screenshot of that state.

Correct a faulty check only when a requirement shows the check is wrong, and state that reason. Then run the complete set again on the final checks. Do not drop a failing case, weaken an assertion, or add a trivial check to raise the score.

## Run and observe

Start the application with its start command. The review waits until that process is still running and a window of the application is up. Record the start output, the window title, and the window size, using a window query the session permits. If the process exits before a window exists, stop and report that output. Do not review source in place of the window.

When the start command launches Electron, also record that a renderer process exists for that application and that the start output does not contain the SUID sandbox fatal.

Leave that window running when the user asked to start the application. Do not edit the application as part of the review.

Score application behavior separately from an outside model's answers and from whether an outside service is available. Do not treat a wrong external answer as a product failure. When a behavior depends on a model, check it on another window of the same build pointed at a stand-in with known replies. Say which window each result came from.

When a check supplies a chosen folder instead of using the system folder dialog, the file list can be judged. The dialog itself stays not tried.

## Record

Write the log in the workspace `app-reviews` directory. Create that directory when it is missing. The file name is the window title, a dot, the review date as `ddmmyy`, and `.log`. Day, month, and year are each two digits with no separators. The sixth of November 2026 is `061126`. Keep spaces that are in the window title.

The log is concise prose. State what the application is, the version that was running, how it was started, where the requirements came from, what was seen, the score, and what was not tried. A check that was not run is unverified. Describe a percentage as the result on the cases that ran. It is not proof of overall correctness.

Canvas the same findings: the score, what showed up for each check that ran, and what was not tried. The canvas and the log must agree. Report passed and total, how the score was calculated, mandatory-check status, and the checks that were not run.
