---
name: gha
description: GitHub Actions workflow management — trigger, monitor, and debug CI runs
user-invocable: true
disable-model-invocation: true
---

# /gha — GitHub Actions Manager

Quick access to GitHub Actions workflows via `gh` CLI.

## Commands

### Check CI Status
```bash
gh run list --limit 5
```

### View Specific Run
```bash
gh run view <run-id>
gh run view <run-id> --log-failed  # Show only failed step logs
```

### Watch Running Workflow
```bash
gh run watch <run-id>
```

### Trigger Workflow
```bash
gh workflow run <workflow-name> --ref <branch>
```

### Rerun Failed Jobs
```bash
gh run rerun <run-id> --failed
```

## Common Workflows

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| CI | Push to PR | TypeScript check + Vitest + Playwright |
| Deploy Preview | PR to develop | Vercel preview deployment |
| Production | Merge to main | Vercel production deployment |

## Usage Patterns

- **After pushing a PR:** `gh run list --limit 1` to check CI started
- **CI failed:** `gh run view <id> --log-failed` to see failure details
- **Flaky test:** `gh run rerun <id> --failed` to retry just the failed job
- **Deploy status:** `gh run list --workflow=deploy.yml --limit 3`

## Tips
- Use `--json` flag for machine-readable output
- `gh run download <id> -n <artifact>` to get test artifacts
- Combine with `/task-complete` which auto-checks CI before merge
