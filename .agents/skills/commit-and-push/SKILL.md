---
name: commit-and-push
description: >-
  Commit the current changes with a concise message passed through git
  commit -m, then push the current branch to its existing remote. Use when
  the user asks to push the latest changes to remote and to include a
  concise but detailed commit.
---

# Commit and push

The directory is already a git repository and the current branch already tracks a remote. Do not change git config. Do not use `git commit --amend`, `--no-verify`, interactive git flags, or force push.

## Check

From the repository root:

```bash
git rev-parse --show-toplevel
git status
git diff
git diff --staged
git log -12 --oneline
git branch -vv
```

Stop if `git status` shows a clean working tree. Read untracked and modified paths before staging. Do not stage secrets (`.env`, credentials, keys).

```bash
git status -u
```

## Commit and push

Stage only the paths that belong in this commit.

```bash
git add <paths>
git commit -m "$(cat <<'EOF'
<subject>

<body>
EOF
)"
git status
git push origin HEAD
```

`<subject>` is one line that names the change. `<body>` is one or two sentences on why it exists. Both must match the staged diff.

## Verify

The commit prints `[<branch> <hash>] <subject>` and a file summary. `git status` then shows the branch ahead of `origin/<branch>` by 1 commit and `nothing to commit, working tree clean`. The push prints `<old>..<new>  HEAD -> <branch>`.
