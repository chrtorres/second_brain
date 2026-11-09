---
name: review-prompt
description: >-
  Reviews a prompt by explaining each instruction and exercising its
  load-bearing claims in a sandbox that leaves the real tree unchanged, then
  writes a dated findings log. Use when asked to review a prompt, explain each
  point and what it does, and export the findings to a prompt-review log.
---

# Review prompt

Review the prompt by explaining every instruction and by running the claims that decide whether the prompt works. The findings log is the file this review adds to the real workspace. The sandbox result stays in the sandbox.

## Record the real tree

From the real repository the prompt could write to, record `git status --short` and the hash of one file the review must not change. The sandbox is a directory outside that repository and outside the workspace.

The sandbox workspace root is not a git repository when the real workspace root is not a git repository. Inside it, create the git repositories the prompt can write to, with the same parent and child relationship as the real tree. Copy in only the files the prompt must follow. Add a marker file the prompt is not supposed to change.

Before exercising the prompt, list the mandatory checks. A review is done when every one has been run and reported, or reported as unverified with the reason.

## Exercise the prompt

Run the prompt's load-bearing claims only inside the sandbox. Read the files the run added. A summary of the run is not the result.

Explain each instruction: what it tells the agent to do, and what doing it produced.

Run a claim before treating it as true.

- A test the prompt says passes is unverified until that test is executed. Record a failure as a failure.
- When the prompt tells the agent to move or reorganize files, run the artifact from the new location. A pass in the original location leaves the new layout unverified.
- When the prompt names an output the agent must preserve, run that output after it is preserved.

## Write the log

Write `<workspace-root>/prompt-review/<title>.mmddyy-hhmmss.log`.

`<workspace-root>` is the IDE workspace root. `<title>` names the prompt under review, in lowercase words separated by hyphens. The timestamp is local time as month, day, year, hour, minute, second: `mmddyy-hhmmss`.

The log states:

- what the prompt is and what running it does
- each instruction and what it does
- the commands that ran and their results
- whether `git status --short` and the recorded file hash still match
- which checks ran and which did not

A check that did not run is unverified.

## Stop

Re-read `git status --short` and the recorded file hash after the sandbox run. The real repository fails the review when either differs from the record. Say so in the log. Leave the sandbox result in the sandbox.
