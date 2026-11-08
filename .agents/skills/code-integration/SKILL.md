---
name: code-integration
description: >-
  Integrates a conversation engine into a code editor so the assistant keeps
  the conversation, can read, write, delete, and execute, and shows edits as
  added and removed highlights. Use when abstracting specific implementations
  where unnecessary to encourage a broader target audience.
---

# Code integration

Discover the editor, the conversation engine, the test command, and the project boundary from the tree. Do not copy another project's host, port, model, or directory into the integration.

## Acceptance

Write the observable checks before editing. Mandatory checks must all pass. When no threshold is stated and the checks form a rubric, the bar is at least 95 percent of the scored checks. A bar stated as greater than a number does not pass when the result equals that number. When the checks are not a rubric, do not invent a percentage.

A percentage is the result on the cases that ran. It is not proof of overall correctness.

## Engine

Send each model call through the conversation engine. Each send includes the conversation so far. When a send fails, drop the user turn that received no reply.

When the engine's send returns only reply text and hides tool calls, call the same engine instance's chat method and surface the tool calls. Do not keep a second transcript that the engine does not send.

The request that reaches the model is the evidence. A body that contains only the latest user turn fails the history check. A client that is not the engine fails the engine check. Run both against a known-bad input before trusting a pass. A check that passes on the known-bad input does not count.

## Permissions

The assistant's primary job is coding work. The role text that is sent names permission to read files, write files, delete files, and execute commands.

- Read puts the file text into the next turn.
- Write creates or replaces a text file and records the text before and after.
- Delete removes the file.
- Execute runs in the project directory and returns the process output. The result is the output, not a copy of the command text.

A path outside the project, a hidden name, and a symlink do not return the file's contents. A result that contains a secret from outside the project fails. Run that leak check on a string that does contain the secret before trusting a pass. That known-bad string must fail the check.

An empty reply, a failed request, and an unreachable endpoint stay errors. They do not become an edit.

## Highlights

Show an edit as added lines and removed lines in the editor. Added highlighting is green. Removed highlighting is red. Read the computed color and the box. Each highlighted region has a width and a height greater than zero. A gray color is neither green nor red. Run that color check on gray before trusting a green or red pass.

The proposed replacement stays out of the editor buffer until it is accepted. Accept applies it and clears the highlights. An edit the assistant has already written shows the same colors on the resulting text.

A class name or a hidden attribute does not establish what is on screen.

## Finish

Run the project's test command on the final version. Score the product separately from the wording of an outside model. Do not drop a failing case, weaken an assertion, or add a trivial check to raise the score. If three repair cycles produce no measurable change, reassess. A required check that was not run is unverified.
