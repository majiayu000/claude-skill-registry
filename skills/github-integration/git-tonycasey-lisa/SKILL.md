---
name: git
description: "GitHub and Git workflow helpers; triggers on 'create pr', 'pr checks', 'retrigger tests', 'bump version', 'push'."
---

## Purpose
Model-neutral helper for GitHub and Git workflows including PR management, CI triggers, version bumping, and branch operations.

## Triggers
Use when the user says: "create a pr", "check pr status", "retrigger tests", "toggle test label", "pr checks", "bump version", "push to remote".

## How to use

### Check PR Status
```bash
# View PR checks
gh pr checks <PR_NUMBER> --repo <owner/repo>

# View PR details
gh pr view <PR_NUMBER> --repo <owner/repo>
```

### Retrigger CI Tests
When a PR test fails and a fix is pushed, tests don't automatically re-run. Toggle the "TEST" label to trigger:

```bash
# Remove and re-add TEST label to trigger CI
gh pr edit <PR_NUMBER> --repo <owner/repo> --remove-label "TEST"
sleep 2
gh pr edit <PR_NUMBER> --repo <owner/repo> --add-label "TEST"
```

### Check CircleCI Pipeline Status
```bash
# Get latest pipeline for a branch
curl -s -H "Circle-Token: $(cat ~/.circleci/cli.yml | grep token | awk '{print $2}')" \
  "https://circleci.com/api/v2/project/gh/<owner>/<repo>/pipeline?branch=<BRANCH>" \
  | jq '.items[0] | {number, state, created_at}'

# Get workflow status for a pipeline
curl -s -H "Circle-Token: $(cat ~/.circleci/cli.yml | grep token | awk '{print $2}')" \
  "https://circleci.com/api/v2/pipeline/<PIPELINE_ID>/workflow" \
  | jq '.items[] | {name, status}'
```

### Poll CI Until Completion
```bash
# Poll current branch (10 min timeout, 1 min interval)
# Update OWNER and REPO in the script first
.lisa/skills/git/scripts/poll-ci.sh

# Poll specific branch
.lisa/skills/git/scripts/poll-ci.sh feature-branch
```

Exit codes:
- `0` - CI passed
- `1` - CI failed
- `2` - CI canceled
- `3` - Timeout (10 minutes)
- `4` - CircleCI token not found
- `5` - No pipeline found for branch

### Bump Version
Bump the semantic version in package.json before pushing:

```bash
# Bump minor version (default): 1.2.3 → 1.3.0
lisa bump-version

# Bump patch version: 1.2.3 → 1.2.4
lisa bump-version patch

# Bump major version: 1.2.3 → 2.0.0
lisa bump-version major
```

Output (JSON to stdout):
```json
{
  "status": "ok",
  "bumpType": "minor",
  "oldVersion": "1.2.3",
  "newVersion": "1.3.0",
  "file": "/path/to/package.json"
}
```

## Workflow: Push with Version Bump

**When pushing changes to remote**, bump the version first:

1. **Bump version** (default: minor):
   ```bash
   lisa bump-version
   ```

2. **Commit the version bump**:
   ```bash
   git add package.json
   git commit -m "chore: bump version to $(node -p "require('./package.json').version")"
   ```

3. **Push to remote**:
   ```bash
   git push
   ```

**One-liner for bump + commit + push**:
```bash
lisa bump-version && \
git add package.json && \
git commit -m "chore: bump version to $(node -p \"require('./package.json').version\")" && \
git push
```

## Workflow: PR Created

**When a Pull Request is created**, follow these steps:

1. **Create the PR** with the TEST label:
   ```bash
   gh pr create --title "[TICKET-123] - Title" --body "..." --label "TEST"
   ```

2. **Update Jira tickets** to "Code Review" status (see jira skill)

3. **Monitor CI** - Check if tests pass:
   ```bash
   gh pr checks <PR_NUMBER> --repo <owner/repo>
   ```

## Workflow: PR Test Failure

**When CI tests fail on a PR:**

1. **Identify the failure** - Check CircleCI logs or GitHub checks
2. **Push a fix** - Commit and push the fix to the branch
3. **Retrigger tests** - Toggle the TEST label:
   ```bash
   gh pr edit <PR_NUMBER> --repo <owner/repo> --remove-label "TEST" && \
   sleep 2 && \
   gh pr edit <PR_NUMBER> --repo <owner/repo> --add-label "TEST"
   ```
4. **Monitor** - Watch for the new pipeline to complete

## I/O Contract (examples)

### PR Checks
```
gh pr checks 1266
Run linter    pass    1m28s    https://github.com/...
ci/circleci   pass    5m12s    https://circleci.com/...
```

### CircleCI Pipeline Status
```json
{
  "number": 6162,
  "state": "created",
  "created_at": "2026-01-13T17:27:10.963Z"
}
```

### CircleCI Workflow Status
```json
{
  "name": "test",
  "status": "running"
}
```

## Cross-model checklist
- Claude: Use concise commands; prefer gh CLI for GitHub operations
- Gemini: Explicit commands; avoid model-specific tokens

## Notes
- Requires `gh` CLI authenticated with GitHub
- Requires CircleCI CLI/token for pipeline status
- TEST label triggers CI workflow via GitHub Actions/CircleCI integration
