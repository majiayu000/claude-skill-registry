---
name: ensure-prod
description: Verifies that the latest main commit is deployed to production. Checks CI pipeline, fixbot activity, and k8s pod status. Use when you want to confirm a deploy completed or troubleshoot why prod is behind.
allowed-tools: Bash, Read, Grep, Glob, WebFetch, mcp__kubernetes__kubectl_get, mcp__kubernetes__kubectl_describe, mcp__kubernetes__kubectl_logs, ToolSearch
---

# Ensure Main is on Prod

Verify that the current HEAD of main is deployed to the production k8s cluster. If it's not, diagnose why and take corrective action.

## Step 1: Compare git HEAD with what's actually running on prod

```bash
# Get current HEAD
git rev-parse HEAD
```

**IMPORTANT:** You must verify against the **actual running pods**, not just Argo CD's sync status. Argo CD's `REVISION` field reflects the git manifest revision, NOT the container image — a "Synced" app can still be running old pods if the image build hasn't finished or the rollout hasn't completed.

Check what's actually running using **both** of these methods (run in parallel):

1. **Public build-info endpoint** (most reliable — shows exactly what the running pod reports):
   Use WebFetch on `https://abaci.one/api/build-info` and extract `git.commit` and `git.commitShort`. This also shows `environment`, `git.isDirty`, and build timestamp.

2. **Pod image inspection** via Kubernetes MCP:
   Use `kubectl_describe` on one of the abaci-app pods in the `abaci` namespace. Look at the `Image` field — the tag or digest tells you which build is running. Cross-reference with the image updater annotations if needed.

**Match criteria:** HEAD matches prod when the build-info endpoint's `git.commit` equals `git rev-parse HEAD`. If they don't match, proceed to Step 2.

## Step 2: Check CI pipeline

```bash
# Recent workflow runs
gh run list --limit 5

# Check if the latest run on main succeeded
gh run list --branch main --limit 3
```

- **If a build is in progress**: Report "build in progress" with the run URL and estimated time (~13min for full build). Stop and let the user decide whether to wait.
- **If the latest build succeeded**: Argo CD image updater should pick it up within a few minutes. Check if the image updater has seen it (see Step 4).
- **If the latest build failed**: Go to Step 3.

## Step 3: Check fixbot activity

```bash
# Open fixbot issues
gh issue list --label fixbot --state open

# Recent fixbot PRs
gh pr list --label fixbot --state open
```

- **If a fixbot PR exists**: Review it with `gh pr view <number>`. If checks pass and the fix looks correct, tell the user it's ready to merge. If it needs judgment, explain what needs review.
- **If a fixbot issue exists but no PR yet**: Fixbot is still working on it. Report the issue and wait.
- **If no fixbot activity**: Check if the diagnostic workflow ran: `gh run list --workflow "Diagnose CI Failure" --limit 3`. If it didn't, the failure may be too new or fixbot itself failed. Investigate the CI failure manually.

## Step 4: Check Argo CD image updater

If CI passed but pods haven't rolled, check the image updater:

Use the Kubernetes MCP to:
1. Check `kubectl logs -n argocd -l app.kubernetes.io/name=argocd-image-updater --tail=30` for recent activity
2. Check `kubectl get applications -n argocd` for sync status

If the image updater hasn't picked up the new image yet, it may just need a few more minutes. Report the status.

## Step 5: Verify pod rollout

Once pods are rolling, monitor via the Kubernetes MCP:
1. `kubectl get pods -n abaci -l app=abaci-app` — check that pods are running the new revision
2. If pods are in CrashLoopBackOff or ImagePullBackOff, report the error

## Step 6: Report

Provide a clear summary:
- Current HEAD SHA (short)
- Prod SHA (from build-info endpoint, short)
- Argo CD revision (short) — note if this differs from what pods are actually running
- CI status (passed/failed/in-progress)
- Fixbot status (if relevant)
- Pod status
- Any build metadata issues (e.g. environment showing "development" instead of "production", dirty flag set incorrectly)

## Edge case: fixbot committed directly to main

If you discover fixbot committed directly to main (check `git log --oneline -5` for commits by github-actions bot that aren't merge commits), push an empty commit to trigger a clean CI run:

```bash
git pull
git commit --allow-empty -m "ci: trigger build after fixbot commit <sha>"
git push
```

Then re-enter this procedure from Step 2.
