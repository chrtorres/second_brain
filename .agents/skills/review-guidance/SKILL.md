---
name: review-guidance
description: >-
  Reviews a guide against the program it describes and reports
  evidence-based findings without editing the guide. Use when asked to
  review a README or other guidance and return independent findings.
---

# Review guidance

Read any working agreements the task names. Establish the guide's purpose from the guide and the project it describes. Decide which claims can change what a reader does, and how each claim will be checked, before judging it. Do not edit the guide.

## What a finding is

Support a material finding with the observed behavior and its practical consequence. Separate defects, conditional risks, preferences, and uncertainty. Do not add findings to fill a quota. A finished review can say the guide needs changes or that no material issues were found.

Recommend the smallest change that corrects each defect.

## Checks

Prefer an observed outcome. A claim can match the source and still mislead the reader.

- Error catalog: send an invalid body and a nearby valid body that has the wrong shape. Record the status and the error string for each. A documented string can be real while the stated cause belongs to a different string.
- On-screen placement: perform the action and record where the result appears relative to the control a reader would use. Source order and the `hidden` attribute do not establish that position.
- Visible history: after a failed send that leaves the user's text on screen, send a follow-up and read the message list that was posted. The visible turn can be absent from that list.
- Restart: define how many trials will run before the first trial. After the server process has exited, start it again on the same port while TIME-WAIT entries remain and nothing is listening. Separately, start a second process while the first is still listening. Address already in use was observed when the second process bound during the first process's life. When the server enables address reuse, as Python's `HTTPServer` does, TIME-WAIT entries after exit did not block the next bind.
- Startup status: call the status route with the upstream closed before treating a successful status as proof the upstream is reachable.
- Pass bar: use the bar the guide states. A bar stated as greater than a number does not pass when the result equals that number. Do not invent a percentage for the review.

## Finish

State what was checked, which version was checked, and which claims were not run. A claim that was not run is unverified. Stay within the guide that was named. Do not treat the end of checking as proof the guide is correct.
