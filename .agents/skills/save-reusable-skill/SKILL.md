---
name: save-reusable-skill
description: >-
  Saves a verified procedure as the project's canonical skill file and the
  symlinks that publish it to the slash menu. Use when a task has a reusable
  procedure to keep, when the user asks to save a workflow as a skill, or when
  a cloned repository's skills are missing from the slash menu because the
  workspace root is a parent of that repository and is not a git repository.
---

# Save reusable skill

Save the verified procedure from the conversation.

If the user supplied a name, use it when it contains only lowercase letters, digits, and hyphens, is within 64 characters, and does not end with a hyphen. If the supplied name does not match that form, write no files and report the name. If the user did not supply a name, derive it from the procedure while saving. If the user supplied the condition for using the skill, use that condition in the description.

The skill belongs to the git repository of the project the procedure was verified in. Discover `<repo-root>` and `<workspace-root>` on this machine from the conversation and the project tree. A directory layout from another machine is not a path here. The IDE workspace root may be a parent of that repository and may not itself be a git repository. Sibling repositories under the workspace do not make ownership ambiguous when the verified procedure is inside one repository, or when the user named that repository. Ask which repository owns the skill only when those facts do not identify one repository. Write no files while that question is unanswered. Call the chosen repository `<repo-root>`.

`<workspace-root>` is not a git repository when this command fails:

```bash
git -C "<workspace-root>" rev-parse --is-inside-work-tree
```

## Name, heading, and description

Complete these while saving.

- `name`: the procedure's action in lowercase words separated by hyphens. Use only letters, digits, and hyphens. Omit the articles a, an, and the. Keep the name within 64 characters, and do not end it with a hyphen. The folder name is this `name`. If `<repo-root>` already has a skill for the same procedure, reuse that skill's name and update that skill.
- If this `name` is already used by a different procedure, leave that skill in place and report the collision. Write no new skill under that name.
- Heading: replace each hyphen in `name` with a space and capitalize the first character. Where the procedure capitalizes a proper noun or an established name, keep that capitalization. Do not write a separate title.
- `description`: what the procedure does, then `Use when` and the condition that should invoke it. If the user supplied that condition, use it. Otherwise take it from the procedure.

## Write

Write `<repo-root>/.agents/skills/<skill-name>/SKILL.md`. This is the only copy of the skill. Do not create `<workspace-root>/.agents`.

When the user asks to publish the cloned skills because they are missing from the slash menu, and this conversation has no new procedure, publish the existing canonical skills and do not invent a skill. When the conversation has no procedure and the user did not ask to publish existing skills, write no files and say so.

## Symlinks

Create these after the canonical directory exists:

- `<repo-root>/.claude/skills/<skill-name>` → `../../.agents/skills/<skill-name>`
- `<repo-root>/.cursor/skills/<skill-name>` → `../../.agents/skills/<skill-name>`

Use that relative target only for those two directories inside `<repo-root>`. `.claude/skills/` is the compatibility copy.

The slash menu reads `<workspace-root>/.cursor/skills` and `<workspace-root>/.agents/skills`. A `SKILL.md` that exists only under a nested repository is not listed when `<workspace-root>` is not a git repository. A fresh clone has the in-repo links only, so those skills stay off the parent workspace's slash menu until they are published.

When `<workspace-root>` is a parent of `<repo-root>` and `<workspace-root>` is not a git repository, publish every canonical skill into `<workspace-root>/.cursor/skills`. Do this for skills already in the clone and for the skill saved in this conversation. Create `<workspace-root>/.cursor/skills` if it is missing. Do not create `<workspace-root>/.agents`.

For each published name, the link is `<workspace-root>/.cursor/skills/<skill-name>`. Compute its target as the relative path from `<workspace-root>/.cursor/skills` to `<repo-root>/.agents/skills/<skill-name>`:

```bash
python -c 'import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "<repo-root>/.agents/skills/<skill-name>" "<workspace-root>/.cursor/skills"
```

When `<repo-root>` is a direct child of `<workspace-root>`, that target includes the child directory's name. Keep every intermediate directory when the repository sits deeper under the workspace. The target `../../.agents/skills/<skill-name>` is for the two in-repo links only. From `<workspace-root>/.cursor/skills`, that same string resolves under `<workspace-root>/.agents`.

When `<workspace-root>` is `<repo-root>`, the in-repo `.cursor/skills` link is the slash path. Do not add a link in the parent directory unless the user identified a parent directory as the workspace they open and that parent is not a git repository. If they did, publish every canonical skill to that parent with the same relative-target rule.

Apply the existing-path rules to every link this procedure creates.

## Existing paths

Inspect existing files first. If this skill already exists in `<repo-root>`, update it so the verified procedure is present. If a symlink already resolves to that canonical directory, leave it. If a file or symlink already occupies one of these paths and resolves somewhere else, leave it and report it. Do not overwrite unrelated files or symlinks.

This task writes the skill file and those symlinks. Do not implement the procedure in project code while saving it. Do not copy the procedure into a working-agreement file.

If both reusable steps and incidental task steps are present, save the reusable procedure and leave the incidental steps out.

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
- When `<workspace-root>` is a non-git parent of `<repo-root>`, `<workspace-root>/.cursor/skills/<skill-name>/SKILL.md` reads the canonical file. A file that is only at `<repo-root>/.cursor/skills/<skill-name>/SKILL.md` is not that parent slash path.

Before trusting the workspace-link check, point that same check at a known-bad link in a temporary directory: `<temp>/.cursor/skills/<skill-name>` → `../../.agents/skills/<skill-name>`. Resolved, it lands under `<temp>/.agents`, not at the canonical directory. A check that passes on that known-bad link does not count. Delete the temporary directory afterward. Do not put that target on the real `<workspace-root>/.cursor/skills/<skill-name>` link. If the known-bad link passes, stop and report the check as unverified.

Report `<workspace-root>`, whether it is a git repository, each link text, and each resolved path.

Say which checks ran and what remains unverified. A check that did not run is unverified. Saving the skill does not execute the procedure in the conversation.
