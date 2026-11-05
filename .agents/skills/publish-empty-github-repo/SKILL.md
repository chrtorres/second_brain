---
name: publish-empty-github-repo
description: >-
  Initialize a local git repository, commit the existing project files, set an
  SSH origin, and push main to an empty GitHub repository. Use when the user
  asks to put a local project on GitHub, create the local git repo, set the
  remote, and push, and the GitHub repository already exists with no README
  and no commits.
---

# Publish an empty GitHub repository

The GitHub repository must already exist, with no README, no commits, and no other generated files. Do not change git config. Use the existing SSH key for `github.com`.

## Check

From the project directory:

```bash
git status
```

Stop if this directory is already a git repository.

```bash
ssh -o StrictHostKeyChecking=accept-new -T git@github.com
```

Authentication succeeded when the output is `Hi <user>! You've successfully authenticated, but GitHub does not provide shell access.` Exit code 1 is expected. Use `<user>` as the GitHub owner unless the user named a different owner. Remote form: `git@github.com:<owner>/<repo>.git`.

## Initialize and commit

```bash
git init -b main
git status
git diff
```

Stage the project files. Do not stage secrets (`.env`, credentials, keys).

```bash
git add <paths>
git commit -m "$(cat <<'EOF'
<subject>

<body>
EOF
)"
```

## Set the remote and push

```bash
git remote add origin git@github.com:<owner>/<repo>.git
git push -u origin main
```

## Verify

```bash
git status
git remote -v
git log -1 --oneline
```

`git status` shows `Your branch is up to date with 'origin/main'` and a clean working tree. `git remote -v` shows that same SSH URL for fetch and push.
