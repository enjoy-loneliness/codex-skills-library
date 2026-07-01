---
name: collab-project-sync-audit
description: Pre-change synchronization and deployment audit workflow for any shared or multi-person repository. Use before modifying, deploying, debugging, or reviewing projects where multiple collaborators may push to the same branch, especially when the user says to pull latest first, mentions多人协作, same-branch collaboration, server deployment drift, or asks whether local/remote/production are in sync.
---

# Collab Project Sync Audit

Use this skill before making changes in a shared project. Its job is to prevent stale-code edits, accidental overwrites, and deployment drift.

## Core Rule

Do not edit first. Inspect, sync, and report the baseline first. If any step fails, resolve or clearly report the blocker before changing files.

## Pre-Change Workflow

1. Identify the repository roots involved in the request.
   - Start from the current working directory.
   - If the task mentions frontend/backend, monorepo packages, workers, mobile apps, or server deploys, locate each related repo before editing.
   - Ignore unrelated services unless the user explicitly expands scope.

2. Check local state for every affected repo.
   - Run `git status --short`.
   - Run `git rev-parse --abbrev-ref HEAD` and `git remote -v` when the branch or remote is unclear.
   - If the worktree has user changes, do not overwrite them. Work around them or ask if they block the task.

3. Pull latest safely before edits.
   - Prefer `git pull --ff-only origin <branch>`.
   - If sandbox permissions block `.git/FETCH_HEAD`, rerun with approval rather than skipping the pull.
   - If fast-forward fails, stop and report the divergence; do not create merge commits unless the user asks.

4. Compare local, remote, and deployment when deployment matters.
   - Record local HEAD after pulling.
   - For servers, check whether the deployed directory is a git repo. If it is, verify `git status --short`, HEAD, remote, branch, and `git pull --ff-only` capability.
   - If the deployed directory is not a git repo, report that deployment cannot be updated by normal pull until it is initialized or replaced by a clone.
   - Check process/container status and health endpoints only for the services in scope.

5. Only after the baseline is clean, make code changes.
   - Keep changes scoped to the request.
   - Build/test the affected repos.
   - Commit and push only when the user has allowed that project to be pushed automatically.

6. Deploy only the services in scope.
   - Avoid broad deploy scripts if they also modify unrelated services, Nginx sites, databases, or secrets outside scope.
   - Prefer targeted build/restart commands for the named service.
   - Validate public URLs or health endpoints after deployment.

## Git Pull Repair Checklist

Use when a server repo cannot pull.

- Confirm whether the remote is SSH or HTTPS.
- Test authentication from the same user that runs `git pull`.
- If an SSH key exists but is not used, set repo-local config:
  `git config core.sshCommand "ssh -i /path/to/key -o IdentitiesOnly=yes"`
- If no key has repository access, ask the user to add the server public key as a GitHub Deploy Key or provide an approved credential flow.
- After authentication works, run `git fetch origin <branch>`.
- If files were manually copied into the repo and match remote HEAD, use a non-working-tree-destructive index alignment such as `git reset --mixed origin/<branch>`; avoid `git reset --hard` unless the user explicitly approves.
- Finish by proving `git pull --ff-only origin <branch>` returns `Already up to date`.

## Reporting

Summarize:

- Repos checked and their HEAD commits.
- Whether each repo pulled cleanly.
- Any dirty worktrees and who likely caused them.
- Deployment state: running version, health checks, and public endpoint results.
- Any blockers before edits.
