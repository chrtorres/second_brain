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
   A name present in the listing is not enough; check 5 decides where it points.
5. **Exact target**: every skill lives canonically in `<repo-root>/.agents/skills`.
   In each publish dir, every link named after a canonical skill must resolve to
   exactly `<repo-root>/.agents/skills/<name>`:
   ```bash
   [ "$(realpath -m "<publish-dir>/<name>")" = "<repo-root>/.agents/skills/<name>" ]
   ```
   A link that resolves into another repository, or under `<workspace-root>/.agents`,
   fails even when a `SKILL.md` exists there. Report a link whose name matches no
   canonical skill.

For each failing workspace link, report the correct target: the relative path from
`<workspace-root>/.cursor/skills` to `<repo-root>/.agents/skills/<name>`:

```bash
python3 -c 'import os,sys; print(os.path.relpath(sys.argv[1], sys.argv[2]))' "<repo-root>/.agents/skills/<name>" "<workspace-root>/.cursor/skills"
```

Repoint it with `ln -sfn <target> <link>` only when the user asks for the fix.
Then rerun checks 1 to 5 on that link and confirm `<link>/SKILL.md` matches the
canonical file byte for byte (`cmp`).

## Trust the detector before trusting a pass

The broken-link scan (`find -xtype l`) must be proven to flag breakage, or its
clean result means nothing. Inject a known-bad link, confirm it is caught, then
remove it:

```bash
ln -s ./__does_not_exist__ "<publish-dir>/__faulttest__"
find "<publish-dir>" -maxdepth 1 -xtype l -name __faulttest__ -print  # must print it
rm -f "<publish-dir>/__faulttest__"
```

The exact-target check needs its own known-bad case. In a temporary directory, create
`<temp>/.cursor/skills/<name>` → `../../.agents/skills/<name>`. It resolves under
`<temp>/.agents`, so check 5 must fail on it. Delete the temporary directory
afterward.

If either known-bad link is not flagged, stop and report that check as unverified.
Always delete the temporary links afterward and leave the tree exactly as found.

## Report

State `<repo-root>`, `<workspace-root>`, whether the workspace root is a git repo,
and for each required publish dir: broken-link count, resolve/frontmatter pass
count over total, exact-target pass count over total, any parity gaps, and each
failing link with its current text and its correct target. Note that discovery/wiring was verified,
not each skill's runtime behavior. A check that did not run is unverified. Make no
changes to the tree except a repoint the user asked for (the fault-test links are
created and removed).
