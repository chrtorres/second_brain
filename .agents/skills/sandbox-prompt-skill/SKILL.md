---
name: sandbox-prompt-skill
description: >-
  Runs a prompt in a temporary workspace, then reads the skill that prompt
  wrote and confirms the real repository is unchanged. Use when a prompt would
  write a skill or run a procedure and that trial must stay off the real tree.
---

# Sandbox prompt skill

Run the prompt in a temporary workspace. Read the skill it wrote, or record that it wrote none. The real repository stays unchanged. Do not treat the runner's summary as the result.

## Record the real tree

From the real repository, record `git status --short` and the hash of one file the trial must not change. The temporary workspace is a directory outside that repository.

## Build the sandbox

The temporary workspace root is not a git repository when the real workspace root is not a git repository. Inside it, create the git repositories the prompt can write to, with the same parent and child relationship as the real tree.

Copy in only the files the prompt must follow. Add a marker file the prompt is not supposed to change.

## Run

Run the prompt only inside the temporary workspace. Do not point that run at the real repository.

## Read the result

Read the files the run added. A claim that a skill was written counts only when its `SKILL.md` is read from the sandbox. A claim that nothing was written counts only when the sandbox has no new files from the run.

The real repository fails the trial when `git status --short` or the marker hash differs from the record. Do not copy the sandbox result into the real repository as part of the trial.
