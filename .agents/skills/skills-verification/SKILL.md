---
name: skills-verification
description: >-
  Compares a saved skill with the prompt and context that generated it and
  reports matches, gaps, and additions. Use when auditing a skill against the
  prompt and context that generated it.
---

# Skills verification

Compare the skill that was written with the prompt and context that were supposed to produce it. Read the skill file and the links that publish it. Read the prompt, the context it names, and any project agreements that prompt says to read. Do not score the skill from the author's summary alone.

Discover the git repository and the IDE workspace root from the tree. The workspace root may be a parent of that repository and may not itself be a git repository. Do not treat one machine's directory names as the rule.

## Judgments

Judge each material requirement in the prompt and in those agreements.

- Met: the skill satisfies the requirement.
- Partial: the skill covers part of the requirement and leaves a material part out or ambiguous.
- Missing: the skill has no corresponding content.
- Added: the skill states a constraint the prompt does not.

Observed means the skill text, the prompt, or the filesystem shows it. Predicted means a judgment about behavior that was not run. A count of these verdicts classifies the texts that were read. Do not report that count as a pass threshold or as proof the skill works.

## Checks

Run these and report the observed paths. A check that was not run is unverified.

- Frontmatter keys are only `name` and `description`. The description says what the skill does and when to use it. The `name` matches the folder name and uses only lowercase letters, digits, and hyphens.
- The heading is that name with hyphens replaced by spaces and the first character capitalized. A proper noun or established capitalization from the procedure may keep its capitals.
- When the prompt supplied a name that matches those name rules, the folder name is that supplied name. A different derived name fails.
- Each symlink's resolved path is the canonical skill directory in the git repository that owns the skill. A link that resolves anywhere else fails, including a workspace link that resolves under the workspace root's `.agents` directory.
- Before trusting a symlink check, compare it with a known-bad target that points at the workspace root's `.agents` directory. A check that passes on that target does not count.
- Files the prompt said not to change are unchanged, including working-agreement files and skills other than the one under audit.

## Procedure fidelity

Keep each prompt condition that changes whether the procedure passes, fails, or stops. That includes numeric thresholds, equality boundaries, and stop conditions. Do not treat a strict boundary as passed.

A skill that reverses a settled instruction fails that requirement. An instruction to ask the user, including which repository owns the work, fails when the skill says not to ask.

A session-specific host, port, model name, or directory in the skill fails when the prompt says to discover those from the project.

Packaging and path rules belong in the skill only when they are the procedure the prompt asked to save.

## Report

State the skill path that was read, the prompt it was compared with, and each verdict with the evidence for it. Say which checks ran and what remains unverified. Do not rewrite the skill as part of the audit.
