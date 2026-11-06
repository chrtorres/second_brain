---
name: diagnose-skill-invocation
description: >-
  Diagnoses why a skill behaved unexpectedly in a thread by separating skill
  defects from invocation, sequencing, and repo-wiring mismatches. Use when a
  skill seems not to work as intended, returns "unverified", or produces a
  result that feels useless.
---

# Diagnose skill invocation

A skill that looks broken is usually a skill invoked in the wrong context, the
wrong sequence, or against the wrong repository. Confirm whether the skill
actually misbehaved before concluding it has a defect.

## Gather what was invoked

List the skills named by slash commands in the thread, and every file attached
alongside them (an `AGENTS.md`, a working-agreements file, a target file). Note
the order they were invoked in.

## Read each invoked skill

Read the skill's `SKILL.md`, not the author's summary. Record two things per
skill: the condition that is supposed to trigger it, and the inputs or prior
steps it depends on. A skill that audits or verifies another artifact names the
artifact and the context it compares against; running it without that pairing is
the common failure.

## Map the repository topology

Do not assume one machine's directory names. Discover from the tree:

- Which directories are git repositories (`git -C <dir> rev-parse --show-toplevel`).
- Whether the IDE workspace root is itself a git repository. It may be a
  non-git parent of the repo that owns the skills.
- Where the canonical skills live (`<repo>/.agents/skills/`).
- Which repository the actual work in the thread happened in.

## Verify publication

For each skill in question, resolve its symlinks and confirm each points at the
canonical directory:

- `<repo>/.cursor/skills/<name>` and `<repo>/.claude/skills/<name>` resolve to
  `<repo>/.agents/skills/<name>`.
- When the workspace root is a non-git parent of `<repo>`, a
  `<workspace-root>/.cursor/skills/<name>` link resolves to that same canonical
  directory. The slash menu reads `.cursor/skills/`.

A link resolving anywhere else, or a missing workspace link, explains a skill
that "isn't found" or loads the wrong copy.

## Check governance

Confirm the attached `AGENTS.md` or working-agreements file belongs to the
repository the work was done in. An agreements file attached from a sibling
repository governs with the wrong rules even while the skills themselves resolve
correctly.

## Check sequence and inputs

Confirm each skill ran at the moment it was meant to, with the inputs it
requires. An auditing skill run before its subject exists, or without the prompt
and context that generated the subject, has nothing to compare and correctly
degrades. The fix is ordering (produce the artifact first, then audit it), not
editing the skill.

## Distinguish honest degradation from failure

A verification skill reporting "unverified" for a check it could not run, or
naming a limitation it could not inspect, is working as designed — it is refusing
to over-claim, not malfunctioning. Treat that as correct behavior. Only a verdict
that contradicts the filesystem or the skill's own text is a real defect.

## Report

State the root cause in terms of which category it falls in: a usage or
sequencing mismatch, a repo-wiring or governance mismatch, a broken symlink, or
a genuine skill defect. Cite the filesystem evidence for each claim. Say which
checks ran and what remains unverified.
