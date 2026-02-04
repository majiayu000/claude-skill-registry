---
name: check-codex
description: Check for pending Codex (GitHub AI) feedback on current branch's PR. Use to review and address AI suggestions before merge. This is the rate-limiting step before merge.
model_tier: haiku
parallel_hints:
  can_parallel_with: [startup, pr-reviewer]
  must_serialize_with: []
  preferred_batch_size: 1
context_hints:
  max_file_context: 20
  compression_level: 2
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "P1.*critical"
    reason: "P1 critical issues are merge blockers requiring human review"
  - pattern: "security|credential"
    reason: "Security-related feedback requires human verification"
---

# Check Codex Feedback Skill

> **Purpose:** Fetch and present Codex review comments for the current PR
> **Created:** 2025-12-28
> **Trigger:** `/check-codex` command
> **Aliases:** `/codex`, `/codex-feedback`

---

## When to Use

- After creating/updating a PR (wait 1-10 min for Codex to respond)
- At session start (integrated with `/startup`)
- Before merging a PR (Codex is the rate-limiting step)
- When notified of new Codex feedback

---

## Required Actions

When this skill is invoked, Claude MUST:

### Step 1: Get Current PR

```bash
# Get PR for current branch
BRANCH=$(git branch --show-current)
PR_NUMBER=$(gh pr view --json number -q '.number' 2>/dev/null)

if [ -z "$PR_NUMBER" ]; then
  echo "No PR found for branch: $BRANCH"
  echo "Create a PR first: gh pr create"
  exit 0
fi

REPO=$(gh repo view --json nameWithOwner -q '.nameWithOwner')
echo "Checking Codex feedback for PR #${PR_NUMBER} on ${REPO}..."
```

### Step 2: Fetch Codex Comments

```bash
# Fetch inline review comments from Codex
INLINE_COMMENTS=$(gh api repos/${REPO}/pulls/${PR_NUMBER}/comments \
  --jq '.[] | select(.user.login == "chatgpt-codex-connector[bot]") | {
    path: .path,
    line: .line,
    body: .body,
    created_at: .created_at,
    url: .html_url
  }')

# Fetch top-level reviews from Codex
REVIEWS=$(gh api repos/${REPO}/pulls/${PR_NUMBER}/reviews \
  --jq '.[] | select(.user.login == "chatgpt-codex-connector[bot]") | {
    state: .state,
    body: .body,
    submitted_at: .submitted_at,
    url: .html_url
  }')
```

### Step 3: Parse Priority Levels

Extract priority from Codex badge format:
- `![P1 Badge]...P1-red` = **Critical** (must fix before merge)
- `![P2 Badge]...P2-yellow` = **Important** (should fix)
- `![P3 Badge]...P3-blue` = **Suggestion** (nice to have)

### Step 4: Present Feedback

Output structured feedback in this format:

```markdown
## Codex Feedback for PR #[number]

**Branch:** `[branch-name]`
**Status:** [N] comment(s) pending

### [P1/P2/P3] `[file:line]`
[Issue description from Codex]

**Suggested Fix:**
[Codex's recommendation]

[View on GitHub](url)

---

### Summary
- **P1 (Critical):** [count]
- **P2 (Important):** [count]
- **P3 (Suggestion):** [count]

### Next Steps
1. Address P1 issues first (merge blockers)
2. Address P2 issues (recommended)
3. Consider P3 suggestions (optional)

Would you like me to address these issues?
```

---

## Codex Bot Identifier

- **Username:** `chatgpt-codex-connector[bot]`
- **User ID:** `199175422`
- **Type:** Bot

---

## Error Handling

| Scenario | Response |
|----------|----------|
| No PR for branch | "No PR found for branch: [name]. Create with `gh pr create`" |
| No Codex feedback yet | "No Codex feedback yet. Codex typically responds within 1-10 minutes." |
| API rate limit | Retry with exponential backoff |
| Network error | Graceful timeout with message |

---

## Options

### Default: Current Branch PR
```
/check-codex
```

### All Open PRs with Codex Feedback
```
/check-codex --all
```

Shows summary of all PRs with pending Codex comments.

---

## Integration Points

### With `/startup` and `/startupO`

At session start, automatically check for Codex feedback:
- If P1 issues exist: Flag as blockers
- If P2 issues exist: Note in summary
- If no PR or no feedback: Skip silently

### With PR Reviewer

After addressing Codex feedback, run `/review-pr` for human-level review.

### With RELEASE_MANAGER

Before creating final PR or merge request, verify Codex feedback addressed.

---

## Example Session

**User:** `/check-codex`

**Claude:**

```markdown
## Codex Feedback for PR #491

**Branch:** `claude/repo-cleanup-priorities-MHRhY`
**Status:** 1 comment pending

### [P2] `docs/changelog.md:3`
**Issue:** Fix mkdocs/nav references to deleted changelog

Deleting `docs/changelog.md` leaves mkdocs.yml still pointing at `changelog.md`
(line 223) and docs/README.md still linking to it (line 216). MkDocs treats
missing nav targets as build errors.

**Suggested Fix:**
- Update `mkdocs.yml` line 223 to reference `CHANGELOG.md`
- Update `docs/README.md` line 216 link

[View on GitHub](https://github.com/.../pull/491#discussion_r2649434837)

---

### Summary
- **P1 (Critical):** 0
- **P2 (Important):** 1
- **P3 (Suggestion):** 0

### Next Steps
1. Fix mkdocs.yml reference to changelog
2. Fix docs/README.md link
3. Commit and push

Would you like me to address these issues?
```

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `startup` | Calls check-codex at session start |
| `startupO` | Calls check-codex at ORCHESTRATOR session start |
| `pr-reviewer` | Complementary - human review after addressing Codex |
| `pre-pr-checklist` | Includes Codex feedback check |

---

## Quick Reference

```bash
# Check current PR for Codex feedback
gh api repos/$(gh repo view --json nameWithOwner -q '.nameWithOwner')/pulls/$(gh pr view --json number -q '.number')/comments \
  --jq '.[] | select(.user.login == "chatgpt-codex-connector[bot]")'
```

---

## Codex Interfaces (Feb 2026)

The Codex ecosystem now includes multiple interfaces:

| Interface | Purpose | This Skill Covers |
|-----------|---------|-------------------|
| **macOS App** | Multi-agent parallel work, automations | No (user-facing) |
| **CLI** | CI/CD pipelines, scripting | Partial (headless) |
| **Web (Cloud)** | Quick tasks, PR reviews | Yes (primary) |
| **IDE Extension** | In-editor assistance | No |

### macOS App Capabilities (New Feb 2, 2026)

The Codex app introduces:
- **Multi-agent parallel execution** - up to 30 min per agent
- **Worktree isolation** - each agent gets isolated copy
- **Automations** - scheduled background tasks
- **Review queue** - completed work for your review

### Default Automations

| Automation | Output | When |
|------------|--------|------|
| Daily Bug Scan | PR with fixes | Daily 6am |
| Test Gap Detection | PR with tests | Daily 7am |
| Nightly CI Report | Summary comment | Nightly 11pm |
| CI Monitor | Grouped failures | On CI failure |
| Issue Triage | Label suggestions | On new issue |

### Automation Output Interpretation

When checking feedback from automations (vs manual `@codex review`):

```json
{
  "automation": "Daily Bug Scan",
  "status": "completed",
  "branch": "codex/bug-scan-20260202",
  "pr_url": "https://github.com/.../pull/806"
}
```

**Action:** Review the auto-created PR, merge if valid.

---

## Documentation References

- **Human Guide:** `docs/tools/CODEX_APP.md`
- **LLM Reference:** `.claude/dontreadme/tools/CODEX_INTEGRATION.md`

---

*Codex feedback is the rate-limiting step before merge. Address issues early, merge smoothly.*
