---
name: phx:pr-review
description: Address PR review comments — fetch, categorize, draft responses, optionally fix code. Use whenever the user has PR feedback to address, mentions review comments, or shares a PR URL or number. Also use when the user asks to respond to or fix reviewer suggestions.
effort: high
argument-hint: <PR number or URL> [--fix]
disable-model-invocation: true
---

# PR Review Response

Fetch PR review comments, categorize them, draft responses,
and optionally apply code fixes.

## Usage

```
/phx:pr-review 42              # Address comments on PR #42
/phx:pr-review 42 --fix        # Address + apply code fixes
/phx:pr-review https://...     # Full URL also works
```

## Arguments

`$ARGUMENTS` = PR number (or URL), optionally followed by `--fix`.

## Workflow

### Step 1: Fetch PR Context

```bash
# Get PR metadata
gh pr view {number} --json title,body,state,baseRefName,headRefName

# Get all review comments (inline + general)
gh api repos/{owner}/{repo}/pulls/{number}/comments --paginate
gh api repos/{owner}/{repo}/pulls/{number}/reviews --paginate

# Get the diff for context
gh pr diff {number}
```

Parse the PR number from `$ARGUMENTS`. If a URL, extract the
number from it. Detect `--fix` flag.

### Step 2: Categorize Comments

Group each comment into one of these categories:

| Category | Signal | Action |
|----------|--------|--------|
| **Code change** | "should be", "change to", "use X instead" | Draft fix + response |
| **Question** | "why", "what if", "how does" | Draft explanation |
| **Nitpick** | "nit:", style-only, formatting | Quick acknowledgment |
| **Praise** | "nice", "good", "LGTM" | No action needed |
| **Discussion** | Architecture, trade-offs, alternatives | Draft thoughtful response |

### Step 3: Map to Code Locations

For each code-change comment:

1. Find the file and line from the comment's `path` and `position`
2. Read the current code at that location
3. Understand the reviewer's suggestion in context
4. Check if the suggestion conflicts with Iron Laws

### Step 4: Draft Responses

For each comment, draft a response following patterns in
`${CLAUDE_SKILL_DIR}/references/response-patterns.md`.

Present ALL draft responses to the user for review:

```
## PR #{number}: {title}
### {n} comments to address

**Code changes ({n}):**
1. {file}:{line} — {reviewer suggestion} → {proposed fix}

**Questions ({n}):**
1. {question summary} → {draft answer}

**Nitpicks ({n}):**
1. {nit} → Acknowledged

**Discussion ({n}):**
1. {topic} → {draft response}
```

### Step 5: Apply Fixes (if --fix)

If `--fix` flag provided AND user approves:

1. Apply code changes from approved code-change responses
2. Run `mix compile --warnings-as-errors && mix test`
3. If tests pass, present the changes
4. Do NOT commit or push — leave that to the user

### Step 6: Post Responses (with user approval)

**STOP and ask user to review all draft responses.**

After user approves (may edit some):

```bash
# Post each response as a reply to the original comment
gh api repos/{owner}/{repo}/pulls/{number}/comments/{id}/replies \
  -f body="{response}"
```

## Iron Laws

1. **NEVER auto-post responses** — Always show drafts and get explicit approval
2. **NEVER dismiss a review** — Only the reviewer should dismiss
3. **Iron Laws override reviewer suggestions** — If a reviewer suggests code that violates an Iron Law, explain why in the response
4. **Keep responses constructive** — Acknowledge the feedback, explain reasoning
5. **Separate fixes from responses** — Apply code changes in a separate step

## Integration

```text
PR receives review comments
       ↓
/phx:pr-review {number}  ← YOU ARE HERE
       ↓
   Fix code? → --fix flag applies changes
       ↓
   Post responses (after user approval)
       ↓
   Push changes → user handles git push
```

## Next Steps

After addressing review comments, suggest follow-up:

```
- `/phx:plan` — Create a plan if findings reveal scope gaps
- `/phx:verify` — Run full verification before pushing
- Push changes — user handles git push
```

## References

- `${CLAUDE_SKILL_DIR}/references/response-patterns.md` — Response templates and common patterns
