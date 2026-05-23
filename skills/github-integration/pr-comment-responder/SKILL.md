---
name: pr-comment-responder
version: 1.0.0
description: PR review coordinator who gathers comment context, acknowledges every
  piece of feedback, and ensures all reviewer comments are addressed systematically.
  Triages by actionability, tracks thread conversations, and maps each comment to
  resolution status. Use when handling PR feedback, review threads, or bot comments.
license: MIT
model: claude-sonnet-4-5
metadata:
  argument-hint: Specify the PR number or review comments to address
---
# PR Comment Responder

Coordinates PR review responses through context gathering, comment tracking, and orchestrator delegation.

## Triggers

| Phrase | Action |
|--------|--------|
| "respond to PR comments" | Full workflow |
| "address review feedback" | Full workflow |
| "handle PR #123 comments" | Target specific PR |
| "Review PR 806 comments... github.com/.../pull/806" | Extract PR from text/URL |

## Quick Reference

### Context Inference (Phase -1)

**ALWAYS extract PR context from prompt first. Never prompt for information already provided.**

```powershell
# Extract PR number and owner/repo from user prompt
$context = pwsh .claude/skills/github/scripts/utils/Extract-GitHubContext.ps1 -Text "[prompt]" -RequirePR
```

Supported patterns:

- Text: `PR 806`, `PR #806`, `pull request 123`, `#806`
- URLs: `github.com/owner/repo/pull/123`

See [references/workflow.md](references/workflow.md) Phase -1 for full details.

### Tools

| Operation | Script |
|-----------|--------|
| **Context extraction** | `Extract-GitHubContext.ps1` |
| PR metadata | `Get-PRContext.ps1` |
| Comments | `Get-PRReviewComments.ps1 -IncludeIssueComments` |
| Reviewers | `Get-PRReviewers.ps1` |
| Reply | `Post-PRCommentReply.ps1` |
| Reaction | `Add-CommentReaction.ps1` |
| Resolve thread | `Resolve-PRReviewThread.ps1` |

### Reviewer Priority

| Priority | Reviewer | Signal |
|----------|----------|--------|
| P0 | cursor[bot] | 100% actionable |
| P1 | Human reviewers | High |
| P2 | coderabbitai[bot] | ~50% |
| P2 | Copilot | ~44% |

### Workflow Phases

0. **Context inference**: Extract PR number from prompt (BLOCKING)
1. **Memory init**: Load `pr-comment-responder-skills` memory
2. **Context gather**: PR metadata, reviewers, all comments
3. **Acknowledge**: Batch eyes reactions
4. **Generate map**: `.agents/pr-comments/PR-[N]/comments.md`
5. **Delegate**: Each comment to orchestrator
6. **Implement**: Via orchestrator delegation
7. **Verify**: All comments addressed, CI passing

See [references/workflow.md](references/workflow.md) for full phase details.

### Verification Gates

Before completion, verify:

- [ ] All comments resolved (COMPLETE or WONTFIX)
- [ ] No new comments after 45s wait
- [ ] CI checks passing
- [ ] All threads resolved
- [ ] Commits pushed

See [references/gates.md](references/gates.md) for gate implementation.

### Response Templates

See [references/templates.md](references/templates.md) for:

- Won't Fix responses
- Clarification requests
- Resolution replies

### Bot Handling

See [references/bots.md](references/bots.md) for:

- Copilot follow-up PR handling
- CodeRabbit commands
- cursor[bot] patterns
