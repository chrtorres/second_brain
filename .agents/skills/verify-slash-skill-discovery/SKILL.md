---
name: verify-slash-skill-discovery
description: >-
  Verifies that project skills are discovered for the Agent slash menu
  alongside built-in skills. Use when verifying that project skills are
  discovered for the Agent slash menu alongside built-in skills, or when a
  slash menu is missing project skills.
---

# Verify slash skill discovery

Set `W` to the IDE workspace root. Set the skills under test to the project skill ids that must appear. Scan only these roots:

- `W/.cursor/skills`
- `W/.agents/skills`
- `~/.cursor/skills-cursor`

Do not search the rest of the workspace. A `SKILL.md` that exists only under a nested repo does not count when `W` is not a git repo.

## Write the checker

Write `/tmp/slash-skill-discovery.test.mjs`. Do not add a script file to the repo. Use `node:assert/strict`. Do not catch assertion failures. Exit 0 only when every assertion passes.

Walk each scan root with `fs.readdir` and `{ withFileTypes: true }`, starting at depth 0. If `readdir` throws `ENOENT` or `ENOTDIR`, skip that directory. If a child is a symlink, `fs.stat` it and descend when the target is a directory; skip the child when `stat` throws. Treat a symlink to a file as a file. Skip child directory names that start with `.` or are `node_modules`, `__pycache__`, `dist`, or `build`. Do not read a directory at depth greater than 10. Collect every file named `SKILL.md`.

The skill id is the parent directory name of the walked path. Keep the walked path. Do not resolve it.

A path passes the slash predicate when all of the following hold:

- Replace `\` with `/`.
- The normalized path ends with `SKILL.md`.
- Trim leading and trailing `/`, wrap the result in `/`, and require that string to include one of `/.cursor/skills/`, `/.agents/skills/`, `/.claude/skills/`, `/.codex/skills/`, `/.grok/skills/`, `/.cursor/skills-cursor/`.

The slash set is the collected files that pass the predicate.

Read frontmatter from the first `---` block. Take the line that starts with `name:`, trim the remainder, and strip one matching pair of quotes.

## Assert

Assert every skill id under test is in the slash set.

For each slash-set path of a skill under test, assert:

- The path passes the slash predicate.
- `W/.cursor/skills` plus a path separator is a prefix of the path. Symlink paths count.
- The file reads as non-empty UTF-8.
- Frontmatter `name:` equals the parent directory name.

Assert at least one directory name from `~/.cursor/skills-cursor` is in the slash set. List that directory with `fs.readdir` and `{ withFileTypes: true }`. Keep real directories, and keep symlinks whose `fs.stat` target is a directory. Skip names that start with `.` or are `node_modules`, `__pycache__`, `dist`, or `build`.

When a skill under test is inside a repo nested under `W`, walk that repo's `.cursor/skills` with the same walker and call the result the control. Do not add the control walk to the scan roots. Assert the control contains that skill id. Assert no accepted slash-set path for that id is a control path.

Print `pass` after the assertions.

## Run

```bash
node /tmp/slash-skill-discovery.test.mjs
```

Pass only when that command exits 0.
