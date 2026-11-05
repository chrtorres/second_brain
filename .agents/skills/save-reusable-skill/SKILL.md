---
name: save-reusable-skill
description: >-
  Saves a verified procedure as the project's canonical skill file and the
  symlinks that publish it. Use when a task has a reusable procedure to keep,
  or when the user asks to save a workflow as a skill.
---

# Save reusable skill

Save the verified procedure from the conversation.

If the user supplied a name, use it when it contains only lowercase letters, digits, and hyphens, is within 64 characters, and does not end with a hyphen. If the supplied name does not match that form, write no files and report the name. If the user did not supply a name, derive it from the procedure while saving. If the user supplied the condition for using the skill, use that condition in the description.

The skill belongs to the git repository of the project the procedure was verified in. Discover that repository from the conversation and the project tree. The IDE workspace root may be a parent of that repository and may not itself be a git repository. If more than one git repository could own the procedure, ask which one. Call the chosen repository `<repo-root>`.

## Name, heading, and description

Complete these while saving.

- `name`: the procedure's action in lowercase words separated by hyphens. Use only letters, digits, and hyphens. Omit the articles a, an, and the. Keep the name within 64 characters, and do not end it with a hyphen. The folder name is this `name`. If `<repo-root>` already has a skill for the same procedure, reuse that skill's name and update that skill.
- If this `name` is already used by a different procedure, leave that skill in place and report the collision. Write no new skill under that name.
- Heading: replace each hyphen in `name` with a space and capitalize the first character. Where the procedure capitalizes a proper noun or an established name, keep that capitalization. Do not write a separate title.
- `description`: what the procedure does, then `Use when` and the condition that should invoke it. If the user supplied that condition, use it. Otherwise take it from the procedure.

## Write

Write `<repo-root>/.agents/skills/<skill-name>/SKILL.md`. This is the only copy of the skill. Do not create `<workspace-root>/.agents`.

## Symlinks

Create these after the canonical directory exists:

- `<repo-root>/.claude/skills/<skill-name>` → `../../.agents/skills/<skill-name>`
- `<repo-root>/.cursor/skills/<skill-name>` → `../../.agents/skills/<skill-name>`

Use that relative target only for those two directories inside `<repo-root>`. The slash menu reads `.cursor/skills/`. `.claude/skills/` is the compatibility copy.

When the IDE workspace root is a parent of `<repo-root>` and is not itself a git repository, also create `<workspace-root>/.cursor/skills/<skill-name>`. Its target is the relative path from `<workspace-root>/.cursor/skills/` to `<repo-root>/.agents/skills/<skill-name>`. Compute that relative path from those two directories. Do not reuse `../../.agents/skills/<skill-name>` for this link.

## Existing paths

Inspect existing files first. If this skill already exists in `<repo-root>`, update it so the verified procedure is present. If a symlink already resolves to that canonical directory, leave it. If a file or symlink already occupies one of these paths and resolves somewhere else, leave it and report it. Do not overwrite unrelated files or symlinks.

This task writes the skill file and those symlinks. Do not implement the procedure in project code while saving it. Do not copy the procedure into a working-agreement file.

If the conversation contains no procedure a later task can reuse, write no files and say so. If both reusable steps and incidental task steps are present, save the reusable procedure and leave the incidental steps out.

## Skill content

Keep verified steps, reusable lessons from failures, and any condition that changes whether the procedure passes, fails, or stops. Keep numeric thresholds, equality boundaries, and stop conditions as stated. Do not treat a strict boundary as passed.

Omit discussion, debugging history, and incidental task details. Packaging and path rules in the conversation stay in this task. Do not copy them into the skill body. Discover commands, paths, frameworks, and dependencies from the project the skill belongs to. Do not copy session-specific hosts, ports, model names, or directories into the skill.

Frontmatter must contain only `name` and `description`. The description must explain what the skill does and when to use it. The `name` must match the folder name. Add scripts, references, or assets only when the procedure cannot be followed without them.

## Checks

After saving, run these checks and report the observed paths:

- Frontmatter keys are only `name` and `description`.
- The `name` matches the folder name and uses only lowercase letters, digits, and hyphens.
- The heading is that name with hyphens replaced by spaces and the first character capitalized. A proper noun or established capitalization from the procedure may keep its capitals.
- The description states what the skill does and when to use it.
- Each symlink's resolved path is `<repo-root>/.agents/skills/<skill-name>`. A link that resolves anywhere else fails, including a workspace link that resolves under `<workspace-root>/.agents`.

Say which checks ran and what remains unverified. A check that did not run is unverified. Saving the skill does not execute the procedure in the conversation.
