---
name: verify-before-completion
description: >-
  Defines observable acceptance checks before implementation, then runs and
  repairs until every mandatory check passes and any scored checks meet the
  threshold. Use when implementing or modifying a deliverable whose completion
  must be demonstrated through observable acceptance checks.
---

# Verify before completion

Discover this project's commands, paths, frameworks, and dependencies from the tree. Do not reuse another project's hosts, ports, models, or directories.

Write the acceptance definition before implementing. Completion means that definition passed on the final version.

## Define acceptance before implementation

Translate the request into observable requirements. Map each requirement to a verification method: a command, an interaction, or an inspected state.

Split checks into:

- Mandatory checks. Every one must pass.
- Scored checks, only when a rubric is meaningful. Declare the denominator and the threshold before running them.

Use the threshold the user stated, including whether equality passes. A bar stated as ">95%" does not pass at 95%. When the user states no threshold and the checks form a meaningful rubric, the default bar is >=95% of the scored checks. When the task has no meaningful rubric, do not invent a percentage. Use mandatory pass/fail checks only.

## Establish trustworthy checks

Use assertions that fail when the behavior is wrong. A source-text or status-code check can pass while the behavior is still wrong, so prefer an observed outcome.

Where practical, run a new check against a known-bad input or a controlled fault before trusting its pass. A check that passes on both the broken and fixed behavior does not count.

Cover the relevant normal flow, edge cases, and failure behavior.

For UI work, perform the actual browser interactions and inspect the visible states. API or markup tests do not establish UI acceptance. Author CSS can override the `hidden` attribute, so confirm what is on screen, not only the attribute or the page source.

Score application behavior separately from external model accuracy and from whether an outside service is available. Do not repair a product defect by editing an answer key, and do not treat a wrong external answer as a product failure.

## Implement, verify, and repair

Run the relevant checks. Diagnose each failure and fix its cause. After each fix, rerun the checks that fix can affect. On the final version, run the complete acceptance suite.

When a defect is found that the existing checks did not catch, add a regression check for that failure when practical.

## Preserve evaluation integrity

Do not lower the threshold, remove failing cases, weaken assertions, or add trivial checks to improve the score.

Correct a faulty test only when a requirement shows the test is wrong, and state that reason.

A required check that was skipped or not executed is unverified.

For nondeterministic behavior, define the number of trials and the scoring rule before the first trial. Do not repeat runs until one favorable run passes.

## Continue until acceptance is demonstrated or blocked

Completion requires every mandatory check to pass and the scored checks to meet the declared threshold, on the final version.

Continue while each repair cycle produces a measurable change in the results. If three consecutive repair cycles produce no measurable progress, reassess the approach.

If still blocked, or a missing dependency, access restriction, or resource limit prevents verification, report the work as incomplete. Include the evidence gathered and the smallest next step that would unblock verification.

Do not claim completion because testing stopped.

## Report evidence

State what was verified and which final version was tested. Include passed/total, how the score was calculated, mandatory-check status, and remaining limitations.

Describe a percentage as the result on the cases that ran. It is not proof of overall correctness or reliability.
