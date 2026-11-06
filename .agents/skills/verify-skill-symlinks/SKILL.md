---
name: verify-skill-symlinks
description: Verifies that every canonical skill under .agents/skills/ is published through working symlinks in each slash-menu location, so the forward-slash commands are discoverable and functional. Use when asked to verify that a repo's skill symlinks and slash commands work, or after pulling changes that add, move, or republish skills.
---

# Verify skill symlinks

Confirm every canonical skill is published through resolving symlinks in each
location the slash menu reads, and that each resolves to a well-formed `SKILL.md`.
This checks discovery and wiring; it does not execute each skill's procedure.

## Discover the roots

Do not hardcode paths from another machine or session. Derive them from the tree.

- `<repo-root>`: the git repository that holds `.agents/skills/` (the canonical copy).
- `<workspace-root>`: the IDE workspace directory (may be a parent of `<repo-root>`).

The in-repo publish dirs are `<repo-root>/.cursor/skills` (slash menu) and
`<repo-root>/.claude/skills` (compatibility copy).

`<workspace-root>` is **not** a git repository when this fails:

```bash
git -C "<workspace-root>" rev-parse --is-inside-work-tree
```

When `<workspace-root>` is a non-git parent of `<repo-root>`, the skills must
**also** be published into `<workspace-root>/.cursor/skills`, because the parent
slash menu reads that directory and does not descend into the nested repo. Include
that directory in every check below. When `<workspace-root>` is `<repo-root>`
itself, that extra directory does not apply.

## Mandatory checks

All must pass. There is no scored rubric.

1. **No broken/dangling symlinks** in any publish dir:
   ```bash
   find "<dir>" -maxdepth 1 -xtype l -print   # any output = a broken link
   ```
2. **Every symlink resolves to a real `SKILL.md`**: `readlink -f` the link and
   confirm `<resolved>/SKILL.md` is a file.
3. **Each `SKILL.md` has `name` and `description` frontmatter** — the requirement
   for a functional slash command. A link that resolves but whose target lacks
   either key fails.
4. **Parity** — every canonical skill is present in each required publish dir, with
   none missing:
   ```bash
   comm -23 <(ls -1 "<repo-root>/.agents/skills" | sort) \
            <(ls -1 "<publish-dir>" | sort)      # any line = missing in that dir
   ```
   For the workspace-root dir, compare against the basenames of its links that
   point into this repo's `.agents/skills`.

Links in `<workspace-root>/.cursor/skills` that point into a *different* repo are
not failures; skip them rather than flag them.

## Trust the detector before trusting a pass

The broken-link scan (`find -xtype l`) must be proven to flag breakage, or its
clean result means nothing. Inject a known-bad link, confirm it is caught, then
remove it:

```bash
ln -s ./__does_not_exist__ "<publish-dir>/__faulttest__"
find "<publish-dir>" -maxdepth 1 -xtype l -name __faulttest__ -print  # must print it
rm -f "<publish-dir>/__faulttest__"
```

If the known-bad link is not flagged, stop and report the check as unverified.
Always delete the temporary link afterward and leave the tree exactly as found.

## Report

State `<repo-root>`, `<workspace-root>`, whether the workspace root is a git repo,
and for each required publish dir: broken-link count, resolve/frontmatter pass
count over total, and any parity gaps. Note that discovery/wiring was verified,
not each skill's runtime behavior. A check that did not run is unverified. Make no
changes to the tree (the fault-test link is created and removed).
