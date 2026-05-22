---
name: github-actions-claude
description: Setup and troubleshoot GitHub Actions workflows using anthropics/claude-code-action for automated PR reviews. Use when creating CI/CD workflows that leverage Claude for code review, research validation, or automated feedback.
---

# GitHub Actions with Claude Code Action

Guide for setting up `anthropics/claude-code-action@v1` for automated PR reviews.

## Quick Reference

**Action**: `anthropics/claude-code-action@v1`
**GitHub App**: https://github.com/apps/claude
**Only supports**: `pull_request` events (NOT `push`)

## Required Setup

### 1. Install Claude GitHub App

Go to https://github.com/apps/claude and install on your repository.

### 2. Add API Key Secret

Repository Settings > Secrets > Actions > New secret:
- Name: `ANTHROPIC_API_KEY`
- Value: Your Anthropic API key

### 3. Create Workflow File

```yaml
name: Code Review

on:
  pull_request:
    branches: [main, master]

permissions:
  contents: read
  pull-requests: write
  issues: write

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          prompt: |
            Review this PR for code quality and security issues.
```

## Critical Learnings

### OIDC Token Bootstrap Problem

By default, the action uses OIDC token exchange for authentication. This creates a chicken-and-egg problem:

- OIDC validation **requires the workflow file to exist on the default branch**
- The first PR adding the workflow will always fail OIDC validation

**Error message**: "Workflow validation failed. The workflow file must exist and have identical content to the version on the repository's default branch."

**Solution**: Use explicit GitHub token to bypass OIDC validation:

```yaml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    github_token: ${{ secrets.GITHUB_TOKEN }}  # Bypass OIDC
```

### Event Type Restrictions

**Only `pull_request` events are supported.**

```yaml
# WRONG - will fail with "Unsupported event type: push"
on:
  push:
    branches: [main]

# CORRECT
on:
  pull_request:
    branches: [main]
```

### Invalid Parameters

These parameters will show warnings:
- `allowed_tools` - NOT a valid input

Valid inputs:
- `anthropic_api_key` - API key from secrets
- `github_token` - GitHub token for auth bypass
- `prompt` - The review prompt
- `trigger_phrase` - Default "@claude"
- `label_trigger` - Default "claude"
- `show_full_output` - Set to `true` for debug logs
- `use_bedrock`, `use_vertex`, `use_foundry` - Alternative providers

### File Writes Don't Persist

When asking Claude to use the Write tool to create files, those files don't persist to the main checkout directory. The action runs in an isolated environment.

**Wrong approach**:
```yaml
prompt: |
  ...
  Use the Write tool to create review-report.md
# Trying to read that file later - IT WON'T EXIST
```

**Correct approach**: Let the action post comments directly or parse the execution output.

## Extracting Review Output

The action outputs `execution_file` - path to JSON with Claude's conversation. To post as PR comment:

```yaml
- name: Run Review
  id: review
  uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    github_token: ${{ secrets.GITHUB_TOKEN }}
    prompt: |
      Review the code and format your response with:
      - **Status**: PASS, WARN, or FAIL
      - **Summary**: Brief summary
      - **Issues Found**: List of issues

- name: Post Review Comment
  uses: actions/github-script@v7
  with:
    script: |
      const fs = require('fs');
      const executionFile = '${{ steps.review.outputs.execution_file }}';
      let reviewContent = 'See job summary';

      if (executionFile && fs.existsSync(executionFile)) {
        const output = JSON.parse(fs.readFileSync(executionFile, 'utf8'));

        // Output is usually a top-level array with type: 'assistant' events
        if (Array.isArray(output)) {
          const assistantMessages = output.filter(m => m.type === 'assistant');
          if (assistantMessages.length > 0) {
            const allTexts = assistantMessages
              .map(m => {
                const content = m.message?.content || m.content;
                if (Array.isArray(content)) {
                  return content.filter(c => c.type === 'text').map(c => c.text).join('\n');
                }
                return typeof content === 'string' ? content : '';
              })
              .filter(t => t.length > 0);
            // Use longest text (likely the final review)
            if (allTexts.length > 0) {
              reviewContent = allTexts.reduce((a, b) => a.length > b.length ? a : b, '');
            }
          }
        }
      }

      await github.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.issue.number,
        body: `## Code Review Report\n\n${reviewContent}`
      });
```

## Execution Output Format

The `execution_file` contains a JSON array with events:

```json
[
  {"type": "user", "message": {"content": [...]}},
  {"type": "assistant", "message": {"content": [{"type": "text", "text": "..."}]}},
  {"type": "tool_use", ...},
  {"type": "tool_result", ...},
  {"type": "assistant", "message": {"content": [{"type": "text", "text": "Final review..."}]}}
]
```

Key points:
- Events use `type` field, not `role` field
- Content is often an array of `{type: 'text', text: '...'}`
- The final assistant message usually contains the review

## Status Extraction

To extract review status (PASS/WARN/FAIL) from Claude's output:

```javascript
const statusPatterns = [
  /\*\*Status\*\*:?\s*(PASS|WARN|FAIL)/i,
  /Status:?\s*\*\*(PASS|WARN|FAIL)\*\*/i,
  /##\s*Status:?\s*\*\*(PASS|WARN|FAIL)\*\*/i,
  /Status:?\s*(PASS|WARN|FAIL)/i
];

let reviewStatus = 'UNKNOWN';
for (const pattern of statusPatterns) {
  const match = reviewContent.match(pattern);
  if (match) {
    reviewStatus = match[1].toUpperCase();
    break;
  }
}
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| "Unsupported event type: push" | Change trigger to `pull_request` |
| "Could not fetch an OIDC token" | Add `id-token: write` to permissions OR use explicit `github_token` |
| "Claude Code is not installed" | Install at https://github.com/apps/claude |
| "Bad credentials" | Check `ANTHROPIC_API_KEY` secret is set |
| "Unexpected input 'allowed_tools'" | Remove - not a valid parameter |
| "Workflow validation failed" | Use `github_token` to bypass OIDC on first PR |

## Complete Example

See `/.github/workflows/code-review.yml` for a full example with:
- Research code-methodology alignment review
- Quality code review (security, correctness, performance)
- Comment extraction and posting
- Status-based merge blocking

## Related Skills

- **requesting-code-review** - For manual code review requests
- **research-code-reviewer** agent - For research-specific validation
