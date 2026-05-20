---
name: secure-pr
description: Run security review, then create a PR and watch CI checks
---

## Secure PR Workflow

Follow these steps in order. Do not skip any step.

### Step 1 — Pre-flight checks

Run the linter and tests locally. If either fails, fix the issues before continuing.

```
ruff check .
ruff format --check .
pytest
```

### Step 2 — Security review

Run the `/security-review` slash command to perform a full security review of all pending changes. This reviews the diff for:
- Hardcoded secrets or API keys
- Injection vulnerabilities
- Unsafe data handling
- Dependency issues
- Any other security concerns

**Do not proceed to step 3 until the security review is complete and all findings are addressed.**

### Step 3 — Create the PR

Create the pull request using the standard format:

```
gh pr create --title "<short title>" --body "$(cat <<'EOF'
## Summary
<bullet points summarizing changes>

## Security Review
- [x] Security review completed via `/security-review`
- [x] No hardcoded secrets or API keys
- [x] No injection vulnerabilities found

## Test plan
<bulleted checklist of testing done>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 4 — Watch CI checks

After the PR is created, wait for all CI checks (lint, test, CodeQL) to complete:

```
gh pr checks --watch
```

Report the final status of each check to the user. If any check fails, investigate the failure, fix it, push the fix, and re-watch.
