---
name: analyse
description: Analyze GitHub issues, Pull Requests (PRs), Discussions, and repo health for an Open Source Software (OSS) project. Summarizes long threads, assesses PR readiness, detects duplicates, extracts reproduction steps, and generates repo health stats. Uses gh Command Line Interface (CLI) for GitHub Application Programming Interface (API) access. Complements oss-maintainer agent.
argument-hint: <number|health|dupes [keyword]|contributors|ecosystem> [--reply]
allowed-tools: Read, Bash, Write, Agent
context: fork
---

<objective>

Analyze GitHub issues and PRs to help maintainers triage, respond, and decide quickly. Produces actionable, structured output — not just summaries.

</objective>

<inputs>

- **$ARGUMENTS**: one of:
  - Number (e.g. `42`) — issues, PRs, and discussions share a unified index; auto-detects the type
  - `health` — generate repo issue/PR health overview
  - `dupes [keyword]` — find potential duplicate issues
  - `contributors` — top contributor activity and release cadence
  - `ecosystem` — downstream consumer impact analysis for library maintainers
  - `--reply`: after analysis, spawn oss-maintainer to draft a contributor-facing reply from the report. Valid for issue, PR, and discussion modes only — silently ignored for health/dupes/contributors/ecosystem.

</inputs>

<workflow>

## Flag parsing

If `$ARGUMENTS` contains `--reply`, strip it and set `REPLY_MODE=true`. Pass the remaining arguments into the mode-dispatch below. If the resolved mode is health/dupes/contributors/ecosystem, `REPLY_MODE` is silently ignored.

## Auto-Detection (for numeric arguments)

Issues, PRs, and discussions share a unified running index — a given number can only be one type. Detect in two steps:

```bash
# Step 1: try the issues API (covers both issues and PRs)
ITEM=$(gh api "repos/{owner}/{repo}/issues/$ARGUMENTS" 2>/dev/null)

if [ -n "$ITEM" ]; then
  # Found — distinguish issue from PR by presence of pull_request key
  TYPE=$(echo "$ITEM" | jq -r 'if .pull_request then "pr" else "issue" end')
else
  # Step 2: not an issue/PR — try discussions via GraphQL
  DISC=$(gh api graphql -f query='
    query($owner:String!,$repo:String!,$number:Int!){
      repository(owner:$owner,name:$repo){
        discussion(number:$number){ title }
      }
    }' -f owner='{owner}' -f repo='{repo}' -F number=$ARGUMENTS \
    --jq '.data.repository.discussion.title' 2>/dev/null)
  [ -n "$DISC" ] && TYPE="discussion" || TYPE="unknown"
fi

# Route: pr → PR Analysis | issue → Issue Analysis | discussion → Discussion Analysis
# unknown → print "Item #N not found" and stop
```

## Mode: Issue Analysis

```bash
# Fetch issue details
gh issue view $ARGUMENTS --json number,title,body,labels,comments,createdAt,author,state

# Fetch all comments
gh issue view $ARGUMENTS --comments
```

Produce:

````
## Issue #[number]: [title]

**State**: [open/closed] | **Author**: @[author] | **Age**: [X days]
**Labels**: [current labels]

### Summary
[2-3 sentence plain-language summary of the issue]

### Thread Verdict
[If thread contains a verified/confirmed solution: extract it here with attribution]
[If no verified solution: "No confirmed solution in thread." — skip thread detail]

### Root Cause Hypotheses

| # | Hypothesis | Probability | Reasoning |
|---|-----------|-------------|-----------|
| 1 | [most likely cause] | [high/medium/low] | [why — reference specific code paths] |
| 2 | [alternative cause] | [medium/low] | [why] |
| 3 | [less likely] | [low] | [why] |

### Code Evidence

For the top hypothesis, trace through relevant code:

```[language]
# [file:line] — [what this code does and why it relates to the hypothesis]
[relevant code snippet]
```

### Suggested Labels

[labels to add/remove based on analysis]

### Suggested Response

[draft reply — or "close as duplicate of #X"]

[Use Markdown formatting: wrap function/class/method names in backticks (`func_name`), wrap code samples in fenced blocks with language tag]

### Priority

[Critical / High / Medium / Low] — [rationale]

````

Write the full report to `tasks/output-analyse-issue-$ARGUMENTS-$(date +%Y-%m-%d).md` using the Write tool — **do not print the full analysis to terminal**.

Read the compact terminal summary template from `.claude/skills/_shared/terminal-summaries.md` — use the **Issue Summary** template. Replace `[skill-specific path]` with `tasks/output-analyse-issue-$ARGUMENTS-$(date +%Y-%m-%d).md`.

**⛔ DO NOT STOP — `REPLY_MODE=true`**: Skip the Confidence block entirely. Proceed **immediately** to the "Draft contributor reply" section. Your response is not complete until you have spawned oss-maintainer and written the reply file.

## Mode: PR Analysis

Run all three `gh` commands in parallel — they are independent API calls:

```bash
# --- run these three in parallel ---

# PR metadata
gh pr view $ARGUMENTS --json number,title,body,labels,reviews,statusCheckRollup,files,additions,deletions,commits,author

# CI status
gh pr checks $ARGUMENTS

# Files changed
gh pr diff $ARGUMENTS --name-only
```

Produce:

```
## PR #[number]: [title]

**Author**: @[author] | **Size**: +[additions]/-[deletions] lines, [N] files
**CI**: [passing/failing/pending]

### Recommendation
[🟢 Approve / 🟡 Minor Suggestions / 🟠 Request Changes / 🔴 Block] — [one-sentence justification]

### Completeness
_Legend: ✅ present · ⚠️ partial · ❌ missing · 🔵 N/A_
- [✅/⚠️/❌/🔵] Clear description of what changed and why
- [✅/⚠️/❌/🔵] Linked to a related issue (`Fixes #NNN` or `Relates to #NNN`)
- [✅/⚠️/❌/🔵] Tests added/updated (happy path, failure path, edge cases)
- [✅/⚠️/❌/🔵] Docstrings (Google style — Napoleon) for all new/changed public APIs
- [✅/⚠️/❌/🔵] No secrets or credentials introduced
- [✅/⚠️/❌/🔵] Linting and CI checks pass

### Quality Scores
- Code: n/5 [emoji] — [reason]
- Testing: n/5 [emoji] — [reason]
- Documentation: n/5 [emoji] — [reason]

### Risk: n/5 [low / medium / high] [emoji] — [brief description]
- Breaking changes: [none / detail]
- Performance: [none / detail]
- Security: [none / detail]
- Compatibility: [none / detail]

### Must Fix
1. [blocking issue]

### Suggestions (non-blocking)
1. [improvement]

### Next Steps
1. [most important action for the author]
2. [second action]
```

Write the full report to `tasks/output-analyse-pr-$ARGUMENTS-$(date +%Y-%m-%d).md` using the Write tool — **do not print the full analysis to terminal**.

Read the compact terminal summary template from `.claude/skills/_shared/terminal-summaries.md` — use the **PR Summary** template. Replace `[entity-line]` with `PR #$ARGUMENTS — [title]` and replace `[skill-specific path]` with `tasks/output-analyse-pr-$ARGUMENTS-$(date +%Y-%m-%d).md`.

**⛔ DO NOT STOP — `REPLY_MODE=true`**: Skip the Confidence block entirely. Proceed **immediately** to the "Draft contributor reply" section. Your response is not complete until you have spawned oss-maintainer and written the reply file.

## Mode: Discussion Analysis

When `$ARGUMENTS` starts with `discussion` (e.g., `discussion 15`), route directly here.

```bash
DISC_NUM=${ARGUMENTS#discussion }

gh api graphql -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      discussion(number: $number) {
        title
        body
        author { login }
        category { name }
        answer { body author { login } createdAt }
        comments(first: 50) {
          nodes { body author { login } createdAt }
        }
        labels(first: 10) { nodes { name } }
        closed
        closedAt
        createdAt
      }
    }
  }' -f owner='{owner}' -f repo='{repo}' -F number=$DISC_NUM
```

If the query returns null for `discussion`, output:

```
⚠ Discussions not enabled or discussion #[number] not found on this repository.
```

and stop.

Produce:

```
## Discussion #[number]: [title]

**State**: [open/closed] | **Author**: @[author] | **Age**: [X days]
**Category**: [category name]
**Labels**: [current labels, or "none"]

### Summary
[2-3 sentence plain-language summary of the discussion topic and current state]

### Thread Verdict
[If discussion has a marked answer: extract it here with attribution]
[If no marked answer: "No accepted answer." — note the most useful response if one is clear]

### Key Viewpoints

| # | Position | Author | Support Level |
|---|----------|--------|---------------|
| 1 | [main viewpoint or request] | @[author] | [high/medium/low engagement] |
| 2 | [alternative viewpoint] | @[author] | [medium/low] |

### Actionable Outcome
[concrete recommendation — e.g. "convert to issue", "mark as answered", "add to docs", "close as resolved"]

### Suggested Labels
[labels to add/remove based on discussion content]
```

Write the full report to `tasks/output-analyse-discussion-$DISC_NUM-$(date +%Y-%m-%d).md` using the Write tool — **do not print the full analysis to terminal**.

Read the compact terminal summary template from `.claude/skills/_shared/terminal-summaries.md` — use the **Discussion Summary** template. Replace `[skill-specific path]` with `tasks/output-analyse-discussion-$DISC_NUM-$(date +%Y-%m-%d).md`.

**⛔ DO NOT STOP — `REPLY_MODE=true`**: Skip the Confidence block entirely. Proceed **immediately** to the "Draft contributor reply" section. Your response is not complete until you have spawned oss-maintainer and written the reply file.

## Mode: Repo Health Overview

Run all three `gh` commands in parallel — they are independent API calls:

```bash
# --- run these three in parallel ---

# Open issues count and age distribution
gh issue list --state open --json number,createdAt,labels --limit 200

# Stale issues (no activity > 90 days)
gh issue list --state open --json number,title,updatedAt --limit 200 | \
  jq '[.[] | select(.updatedAt < (now - 7776000 | todate))]'

# Open PRs
gh pr list --state open --json number,title,createdAt,reviews,statusCheckRollup
```

Produce:

```
## Repo Health: [repo]

### Issue Summary
- Open issues: [N]
- Stale (>90 days): [N] — [list top 5]
- Needs triage (no labels): [N]
- Bugs: [N] | Enhancements: [N] | Questions: [N]

### PR Summary
- Open PRs: [N]
- Awaiting review: [N]
- CI failing: [N]
- Stale (>30 days): [N]

### Recommended Actions
1. [most urgent triage action]
2. [second]
3. [third]
```

Write the full report to `tasks/output-analyse-health-$(date +%Y-%m-%d).md` using the Write tool — **do not print the full analysis to terminal**.

Read the compact terminal summary template from `.claude/skills/_shared/terminal-summaries.md` — use the **Repo Health Summary** template. Replace `[skill-specific path]` with `tasks/output-analyse-health-$(date +%Y-%m-%d).md`.

## Mode: Duplicate Detection

```bash
# Search existing issues for keyword
gh issue list --state all --search "$ARGUMENTS" --json number,title,state --limit 50
```

Group by similarity and output:

```
## Potential Duplicates for: "[keyword]"

### Group 1: [theme]
- #[N]: [title] ([state])
- #[N]: [title] ([state])
Canonical: #[oldest open issue] — suggest closing others as duplicates

### Unique (not duplicates)
- #[N]: [title] — [why it's distinct]

### Recommendations
1. Close #[N] as duplicate of #[canonical] — add comment: "Closing as duplicate of #[canonical]"
2. [Next highest-impact triage action]
3. [Any label additions or reassignments]
```

Write the full report to `tasks/output-analyse-dupes-$(date +%Y-%m-%d).md` using the Write tool — **do not print the full analysis to terminal**.

Read the compact terminal summary template from `.claude/skills/_shared/terminal-summaries.md` — use the **Duplicate Detection Summary** template. Replace `[skill-specific path]` with `tasks/output-analyse-dupes-$(date +%Y-%m-%d).md`.

## Mode: Contributor Activity

```bash
# Top contributors in last 90 days
gh api "repos/{owner}/{repo}/stats/contributors" \
  | jq '[.[] | {author: .author.login, commits: .total, last_week: .weeks[-1]}] | sort_by(-.commits) | .[:10]'

# Release cadence
gh release list --limit 20 --json tagName,publishedAt \
  | jq '[.[] | .publishedAt[:10]]'
```

Produce:

```
## Contributor Activity: [repo]

### Top Contributors (90 days)
| Author | Commits | Trend |
|--------|---------|-------|
| @... | N | ... |

### Release Cadence
- Average: [N days] between releases
- Last release: [date] ([tag])
- Overdue? [yes/no based on cadence]

### Recommendations
1. [Most urgent action — e.g., "cut overdue release", "review stale PRs", "thank top contributor"]
2. [Bus factor concern if ≥60% commits from one author — suggest onboarding new contributors]
3. [Cadence suggestion if overdue]
```

Write the full report to `tasks/output-analyse-contributors-$(date +%Y-%m-%d).md` using the Write tool — **do not print the full analysis to terminal**.

Read the compact terminal summary template from `.claude/skills/_shared/terminal-summaries.md` — use the **Contributor Activity Summary** template. Replace `[skill-specific path]` with `tasks/output-analyse-contributors-$(date +%Y-%m-%d).md`.

## Mode: Ecosystem Impact (for library maintainers)

When assessing the impact of a change on downstream users:

Replace `mypackage` in the commands below with the actual package name (e.g., from `gh repo view --json name --jq .name`).

```bash
# Find downstream dependents on GitHub
gh api "search/code" --field "q=from mypackage import language:python" \
  --jq '[.items[].repository.full_name] | unique | .[]'

# Check PyPI reverse dependencies (who depends on us?)
# Requires johnnydep: pip install johnnydep (not installed by default — skip if unavailable)
# johnnydep mypackage --fields=name --reverse 2>/dev/null || echo "johnnydep not available — skipping PyPI reverse deps"

# Check conda-forge feedstock dependents
gh api "search/code" --field "q=mypackage repo:conda-forge/*-feedstock filename:meta.yaml" \
  --jq '[.items[].repository.full_name] | .[]'
```

Produce:

```
## Ecosystem Impact: [change description]

### Downstream Consumers Found
- [repo]: uses [specific API being changed]

### Breaking Risk
- [High/Medium/Low] — [N] known consumers of changed API
- Migration path: [available / needs documentation]

### Recommended Communication
- [create migration guide / add deprecation warning / notify maintainers directly]
```

Write the full report to `tasks/output-analyse-ecosystem-$(date +%Y-%m-%d).md` using the Write tool — **do not print the full analysis to terminal**.

Read the compact terminal summary template from `.claude/skills/_shared/terminal-summaries.md` — use the **Ecosystem Impact Summary** template. Replace `[skill-specific path]` with `tasks/output-analyse-ecosystem-$(date +%Y-%m-%d).md`.

## Draft contributor reply (--reply only)

If `REPLY_MODE` is not set, skip this step.

**Reuse vs recreate**: reuse an existing report only if it exists *and* the item hasn't had new activity since it was written.

```bash
TODAY=$(date +%Y-%m-%d)
# Expected report paths by mode:
# PR:         tasks/output-analyse-pr-$NUMBER-$TODAY.md
# Issue:      tasks/output-analyse-issue-$NUMBER-$TODAY.md
# Discussion: tasks/output-analyse-discussion-$DISC_NUM-$TODAY.md
REPORT_FILE="tasks/output-analyse-<type>-$NUMBER-$TODAY.md"

DRIFT=false
if [ -f "$REPORT_FILE" ]; then
  # Compare report mtime against item's last-activity timestamp from GitHub
  REPORT_MTIME=$(stat -f %m "$REPORT_FILE" 2>/dev/null || stat -c %Y "$REPORT_FILE")
  UPDATED_AT=$(gh api "repos/{owner}/{repo}/issues/$NUMBER" --jq '.updated_at' 2>/dev/null)
  UPDATED_TS=$(date -d "$UPDATED_AT" +%s 2>/dev/null || date -j -f "%Y-%m-%dT%H:%M:%SZ" "$UPDATED_AT" +%s 2>/dev/null)
  [ "$UPDATED_TS" -gt "$REPORT_MTIME" ] && DRIFT=true
fi
```

Decision:

- Report exists **and** `DRIFT=false` → reuse it; go straight to the oss-maintainer spawn.
- Report missing **or** `DRIFT=true` → run the full analysis first (mode steps above), then continue. When drift triggered, note it in the terminal summary: `[analysis refreshed — new activity since last report]`.

**Spawn oss-maintainer** with:

- The report file path
- The item number and contributor handle (from the analysis data)
- **For PR mode** — prompt: "Read the report at `<path>`. Produce the standard two-part contributor reply per your `<voice>` block: (1) overall PR comment in GitHub Markdown (full MD: headers, bullets, code blocks, `> blockquotes`, links) — `@handle` open, scope line, one prose paragraph per blocking/high issue; items also in the inline table get one clause only, not a full paragraph; nit/low items as a single 'Minor:' line only; decisive close; (2) inline comments table with columns `| Importance | Confidence | File | Line | Comment |` — Importance and Confidence as the two leftmost columns; ordered high → medium → low, then most confident first within each tier; nit/low items omitted from the table entirely. Use all blocking and high findings. No column-width line-wrapping in prose. Write your full output to `tasks/output-reply-<type>-<number>-$(date +%Y-%m-%d).md` using the Write tool. Return ONLY a one-line summary: `overall=N_issues blocking=N | inline=N_rows | → tasks/output-reply-<type>-<number>-<date>.md`"
- **For issue/discussion mode** — prompt: "Read the report at `<path>` for context, then fetch the full thread (`gh issue view <number> --comments` or equivalent GraphQL for discussions) and read every comment. Write your reply as a participant who has followed this thread from the start — not as an outsider summarising it. Rules: (1) If someone in the thread already gave the correct answer, credit them by @handle and build on what they said; do not re-explain what they already covered clearly — add only what is genuinely missing. (2) If a newer version fixes the issue, that is the resolution — state it directly and do not list workarounds alongside it; workarounds only belong in a reply when no fix exists. (3) Be constructive: acknowledge the reporter's situation and validate what is correct in their understanding. (4) Be resolute: if the issue is resolved, explained, or a duplicate, say so plainly and close it — do not hedge or leave it open-ended. (5) One short comment in plain GitHub Markdown; no inline table. Write your full reply to `tasks/output-reply-<type>-<number>-$(date +%Y-%m-%d).md` using the Write tool. Return ONLY a one-line summary: `reply=N_sentences resolved=<yes|no|partial> | → tasks/output-reply-<type>-<number>-<date>.md`"

Print compact terminal summary:

```
  [PR]    Overall comment — N issues  |  Inline comments — N rows
  [Issue] Reply — N sentences
          [analysis refreshed — new activity since last report]  ← only if drift detected

  Reply:  tasks/output-reply-<type>-<number>-<date>.md
```

End your response with a `## Confidence` block per CLAUDE.md output standards — this is always the **absolute last thing**. If `REPLY_MODE=true`, place this block **after** completing the reply step above, never after the analysis alone.

</workflow>

<notes>

- This skill uses mode dispatch (`## Mode: X` sections) rather than sequential numbered steps — each mode is self-contained
- Always use `gh` CLI — never hardcode repo URLs
- Run `gh auth status` first if commands fail; user may need to authenticate
- For closed issues/PRs, note the resolution so history is useful
- Don't post responses without explicit user instruction — only draft them
- **Forked context**: this skill runs with `context: fork` — it operates without access to the current conversation history. All required context (PR number, issue URL, branch name) must be provided as the skill argument or in your prompt.
- Follow-up chains:
  - Issue with confirmed bug → `/develop fix` to diagnose, reproduce with test, and apply targeted fix
  - Issue is a feature request → `/develop feature` for TDD-first implementation
  - Issue with code smell or structural problem → `/develop refactor` for test-first improvements
  - PR with quality concerns → `/review` for comprehensive multi-agent code review
  - Draft responses or comments to be posted publicly → use `--reply` to auto-draft via oss-maintainer; or invoke oss-maintainer manually for custom framing

</notes>
