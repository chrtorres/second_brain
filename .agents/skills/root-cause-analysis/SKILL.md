---
name: root-cause-analysis
description: >-
  Traces a failing acceptance check to the condition that makes its first
  assertion fail, repairs that condition, and records the evidence. Use when
  a mandatory check fails and a later pass has to be tied to the repaired
  cause.
---

# Root cause analysis

The first failing assertion is the symptom. The cause is the condition that makes that assertion fail. A later pass counts only on the version where that condition was repaired and the same checks were run again.

## Accept before changing the subject

Write the acceptance definition before editing the thing under test. Every mandatory check must pass. When no rubric was stated, do not invent a percentage. A bar stated as greater than a number does not pass when the result equals that number.

## Prove the check can fail

Run the check against a known-bad input before trusting a pass. The known-bad run must fail. A check that passes on both the broken behavior and the fixed behavior does not count. If the known-bad input does not fail the check, stop and report the check as unverified.

## Name the symptom, then the cause

Run the check on the real subject. Record the first failing assertion. That text is the symptom.

The cause is the condition that makes that assertion fail. Confirm it from the inputs the check actually reads. A copy of the same thing on a path the check does not read does not explain the failure.

## Repair the cause

Change the condition that failed the assertion. Do not remove the failing case, weaken the assertion, or add a trivial check so the result looks better.

Re-run the checks that repair can affect. On the final version, run the complete acceptance suite. Every mandatory check must pass on that version. A required check that was skipped or not executed is unverified.

If three consecutive repair cycles produce no measurable change in the results, stop and reassess the approach. Do not claim completion because testing stopped.

## Record the evidence

Write a concise record of the final version. Include what was verified, passed and total, how the score was calculated, mandatory-check status, the known-bad result, the first failing assertion, the cause, the repair, and what was not tried. When there is no scored rubric, say there is no percentage.

Before trusting that record, run the same content check against a record that omits those facts. That run must fail. A content check that passes on the incomplete record does not count. The record does not replace the acceptance run: the checks themselves must have been executed on the final version.
