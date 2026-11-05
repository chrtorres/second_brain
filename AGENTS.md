# Working agreements

- Inspect the repo before editing. Do not assume a stack, layout, or tool that is not already in the tree.
- Prefer a small change that does the task. Leave unrelated refactoring alone.
- Before adding a dependency, a top-level directory, or a new service, state the choice and the tradeoff, then continue.
- Add a dependency only when the current stack cannot do the task, and say why.
- Run a check only when the repo has one. Report a test as passed only if that command ran and succeeded.
- State blockers and anything left undone.
- Put a reusable procedure in `.agents/skills/<name>/SKILL.md` instead of copying it into this file.
- When a task reveals a procedure worth reusing, save its verified steps in
  `.agents/skills/<name>/SKILL.md`, with `name` and `description` frontmatter.
  The canonical file stays `.agents/skills/<name>/SKILL.md`. Keep per-skill
  symlinks under this repo's `.cursor/skills/` and `.claude/skills/`. When the
  IDE workspace root is a parent of this repo and is not itself a git repo,
  also symlink the skill directory into `<workspace-root>/.cursor/skills/<name>`.
  The slash menu reads `.cursor/skills/`; `.claude/skills/` is the compatibility copy.
  Avoid creating skills for incidental, task-specific steps.