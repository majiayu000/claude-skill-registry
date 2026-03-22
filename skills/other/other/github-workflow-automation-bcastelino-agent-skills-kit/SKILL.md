---
name: github-workflow-automation
description: "Automate GitHub workflows with AI assistance. Includes PR reviews, issue triage, CI/CD integration, and Git operations. Use when automating GitHub workflows, setting up PR review automation, creating CI/CD pipelines, or integrating AI into DevOps."
---

# GitHub Workflow Automation

> Patterns for automating GitHub workflows with AI assistance, inspired by [Gemini CLI](https://github.com/google-gemini/gemini-cli) and modern DevOps practices.

## When to Use This Skill

- Automating PR reviews with AI
- Setting up issue triage automation
- Creating GitHub Actions workflows
- Integrating AI into CI/CD pipelines
- Automating Git operations (rebases, cherry-picks)

> Full YAML workflow files are in [references/workflow_examples.md](references/workflow_examples.md).

---

## 1. Automated PR Review

Create `.github/workflows/ai-review.yml` triggered on `pull_request: [opened, synchronize]`.

**Flow:** checkout with `fetch-depth: 0` → collect changed files and diff via `git diff` → send to an LLM (e.g., Claude) → post the response as a PR review comment.

Key elements:
- Permissions: `pull-requests: write`, `contents: read`
- Use `actions/github-script@v7` to call the AI API and `pulls.createReview`
- Store the API key in `secrets.ANTHROPIC_API_KEY`

Review output should follow this structure: **Summary → What looks good → Potential Issues → Suggestions → Security Notes**.

For focused reviews, filter changed files with `grep -E '\.(ts|tsx|js|jsx|py|go)$'` before sending to the model.

---

## 2. Issue Triage Automation

### Auto-label on Open

Create `.github/workflows/issue-triage.yml` triggered on `issues: [opened]`.

**Flow:** read issue title & body → call AI with a classification prompt → apply labels (`bug`, `enhancement`, `question`, area labels) → if bug with no repro steps, post a comment asking for details.

**Triage prompt returns JSON:**

```json
{
  "type": "bug | feature | question | docs | other",
  "severity": "low | medium | high | critical",
  "area": "frontend | backend | api | docs | ci | other",
  "summary": "one-line summary",
  "hasReproSteps": true,
  "suggestedLabels": [],
  "suggestedAssignees": []
}
```

### Stale Issue Management

Use `actions/stale@v9` on a daily cron. Mark issues stale after 60 days, close after 14 more. Exempt labels: `pinned`, `security`, `in-progress`.

---

## 3. CI/CD Integration

### Smart Test Selection

Trigger on `pull_request`. Determine which test suites to run by inspecting changed paths:

| Changed path prefix | Suites to run |
|:---------------------|:--------------|
| `src/api/` | `api` |
| `src/frontend/` | `frontend` |
| `src/database/` | `database`, `api` |
| *(none matched)* | `all` |

Use a matrix strategy with `fromJson()` to fan out the test jobs.

### Deploy with AI Risk Assessment

On push to `main`, gather commits since last tag, send to AI for risk analysis (`low / medium / high`). Fail the pipeline when risk is `high` to force manual review. Follow with a deployment job gated by the `production` environment.

### Rollback Automation

Create a `workflow_dispatch` workflow that accepts a `reason` input. Find the latest stable tag with `git tag -l 'v*' --sort=-version:refname | head -1`, deploy it, and notify the team via Slack.

---

## 4. Git Operations

### Automated Rebasing

Listen for `/rebase` in PR comments via `issue_comment: [created]`. Checkout the PR, `git rebase origin/main`, and `git push --force-with-lease`. Comment the result.

### Smart Cherry-Pick

AI-assisted cherry-pick flow:

1. Get commit info and diff against target branch.
2. Ask AI whether conflicts are likely and suggest a resolution strategy.
3. If conflicts expected, create a feature branch, cherry-pick, then resolve each conflict file with AI guidance.
4. Otherwise, cherry-pick directly.

### Branch Cleanup

Weekly cron workflow that lists branches not updated in 30+ days (excluding `main`/`develop`). Creates a housekeeping issue listing stale branches for team review.

---

## 5. On-Demand Assistance

### @mention Bot

Listen for `@ai-helper` in issue/PR comments. Extract the question text, gather context (PR diff or issue body via `gh` CLI), send both to the AI, and post the response as a comment.

### Available Commands

| Command | Description |
|:--------|:------------|
| `@ai-helper explain` | Explain the code in this PR |
| `@ai-helper review` | Request AI code review |
| `@ai-helper fix` | Suggest fixes for issues |
| `@ai-helper test` | Generate test cases |
| `@ai-helper docs` | Generate documentation |
| `/rebase` | Rebase PR onto main |
| `/update` | Update PR branch from main |
| `/label <name>` | Add a label |
| `/assign @user` | Assign to user |

---

## 6. Repository Configuration

### CODEOWNERS

Map directories and file globs to teams in `.github/CODEOWNERS`:

```
* @org/core-team
/src/frontend/ @org/frontend-team
/src/api/ @org/backend-team
/.github/ @org/devops-team
/src/auth/ @org/security-team
```

### Branch Protection

Use `repos.updateBranchProtection` via `actions/github-script` to enforce:
- Required status checks (`test`, `lint`, `ai-review`) with strict mode
- At least 1 approving review from code owners; dismiss stale reviews
- Linear history required; no force pushes or deletions

---

## Best Practices

### Security
- Store API keys in GitHub Secrets
- Use minimal permissions in workflows
- Validate all inputs; don't expose sensitive data in logs

### Performance
- Cache dependencies; use matrix builds for parallel testing
- Skip unnecessary jobs with path filters
- Use self-hosted runners for heavy workloads

### Reliability
- Add timeouts to all jobs
- Handle rate limits gracefully with retry logic
- Always have rollback procedures

---

## Resources

- [Gemini CLI GitHub Action](https://github.com/google-github-actions/run-gemini-cli)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub REST API](https://docs.github.com/en/rest)
- [CODEOWNERS Syntax](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
