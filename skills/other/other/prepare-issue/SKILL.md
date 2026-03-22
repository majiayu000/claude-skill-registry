---
name: prepare-issue
categories: [github]
description: >
  Create a single GitHub issue and immediately triage it — dedup check,
  classification (recipe:implementation or recipe:remediation), mixed-concern
  detection, and label application. Use when user says "open an issue",
  "create an issue", "file an issue", or "file a bug". The user-facing
  counterpart to report_bug.
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo '[SKILL: prepare-issue] Preparing issue...'"
          once: true
---

# prepare-issue Skill

Create a GitHub issue and immediately triage it with LLM classification.

## When to Use

- User says "open an issue", "create an issue", "file an issue", or "file a bug"
- User says "make a new issue", "open a GitHub issue", or "create a GitHub issue"
- User says "I want to open up a GitHub issue" or any similar natural phrasing
- User describes a bug or feature and wants it recorded as a GitHub issue
- User provides `/autoskillit:prepare-issue` directly

## Interface

```
/autoskillit:prepare-issue [--issue N] [--split] [--dry-run] [--repo owner/repo] [description...]
```

- `description...` — free-form text describing the problem or feature (becomes issue title + body)
- `--issue N` — adopt and triage an existing unlabeled issue instead of creating new
- `--split` — when mixed concerns detected, create sub-issues automatically
- `--dry-run` — show classification and labels without creating or editing anything
- `--repo owner/repo` — target repository (falls back to gh default repo context)

## Workflow

### Step 1: Parse Arguments

Parse ARGUMENTS for:
- `--issue N` → set `issue_number = N`, skip dedup
- `--split` → set `split = true`
- `--dry-run` → set `dry_run = true`
- `--repo owner/repo` → set `repo = "owner/repo"`
- Remaining tokens → `description`

### Step 2: Authenticate

```bash
gh auth status
```

Fail fast with a clear error if authentication is not available.

### Step 3: Resolve Repo

If `--repo owner/repo` was provided, use it. Otherwise rely on `gh`'s default repo context.
Confirm access:

```bash
gh repo view --json owner,name
```

### Step 4: Dedup Check (skip if `--issue N` provided)

Extract multiple keyword sets from the description — individual key terms and 2–3 phrase
combinations that capture the core topic. For each keyword set, search open issues:

```bash
gh issue list --state open --search "{keyword-set}" \
    --json number,title,url,body --limit 10
```

Run searches for each keyword set and deduplicate results by issue number. Collect all unique
candidates.

If candidates are found, display them all in a numbered list with number, title, and URL:

```
━━━ Possible Duplicates Found ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Found {N} open issue(s) that may be related:

  [1] #{number} — {title}
      {url}

  [2] #{number} — {title}
      {url}

  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Options:
  [1]–[{N}]  Add to / extend an existing issue (enter a number)
  C          Create a new issue anyway

Your choice [C]:
```

**If the user enters C (or presses Enter):** Continue to Step 4a.

**If the user enters a number [1]–[N] (extend existing):**

1. Ask: *"Add your context as a comment or edit the issue body? [comment/edit, default: comment]"*
2. If **comment** (default):
   ```bash
   gh issue comment {selected_number} --body "{description as additional context}"
   ```
3. If **edit**:
   ```bash
   # Fetch current body and append new context using a temp file to avoid shell injection
   gh issue view {selected_number} --json body -q .body > /tmp/issue_edit_body.txt
   printf '\n## Additional Context\n\n%s' "{description}" >> /tmp/issue_edit_body.txt
   gh issue edit {selected_number} --body-file /tmp/issue_edit_body.txt
   ```
4. Set `issue_number = selected_number` (no new issue will be created).
5. Fetch the updated issue for triage:
   ```bash
   gh issue view {selected_number} --json number,title,body,labels,url
   ```
6. **Continue to Step 6 (LLM Classification)** on this existing issue, then proceed through
   Steps 7, 7a, 8, and 9 to apply labels and requirements. Emit the result block with the
   existing issue's number and URL, then exit.

**If no candidates found:** Continue directly to Step 4a.

### Step 4a: Show Draft and Confirm

Before creating any new issue, display the proposed title and body to the user and wait
for explicit approval:

```
━━━ Draft Issue ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title: {title}

Body:
{body}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Create this issue? [Y/n/edit]
```

- **Y (or Enter):** Proceed to Step 5.
- **n:** Abort. Output a `prepare-issue-result` block with `"aborted": true` and exit.
- **edit:** Accept edited title and/or body from the user, redisplay, and re-prompt.

This gate fires for every new-issue creation path. Skip this step when `--issue N` is
provided (adopting an existing issue) or when `--dry-run` is active.

### Step 5: Create Issue or Adopt Existing

**Creating new:**
Derive a concise title (first sentence of description, max 80 chars) and a structured
body from the full description:

```bash
gh issue create \
    --title "{title}" \
    --body "{body}"
```

Capture the returned issue URL and extract the issue number from it.

**Adopting existing (`--issue N`):**

```bash
gh issue view N --json number,title,body,labels,url
```

Use the fetched data as the issue context.

### Step 6: LLM Classification

Analyze the issue title + body using in-context reasoning:

| Signal | Route | Issue Type |
|--------|-------|------------|
| Existing behavior broken / error traceback present | `remediation` | `bug` |
| New feature / enhancement with clear acceptance criteria | `implementation` | `enhancement` |
| "X doesn't support Y" / clearly absent feature | `implementation` | `enhancement` |
| Large/ambiguous scope / unclear root cause | `remediation` | `enhancement` |

Record: `route` (implementation|remediation), `issue_type` (bug|enhancement),
`confidence` (high|low), `rationale` (one sentence).

### Step 7: Confidence Gate

If `confidence == "low"`:
- Present classification + rationale to user
- Ask: **"Classify as recipe:{route} ({issue_type})? [Y/n]"**
- If user overrides: record their chosen route/type

### Step 7a: Requirement Generation (recipe:implementation only)

Skip if route is `recipe:remediation` — proceed directly to Step 8.

If route is `recipe:implementation`:

1. Trace backward from the goal in the issue title and body:
   - Ask: "What must be true for this functionality to exist?"
   - Each answer is a requirement. Stop when you reach implementation choices.
2. Group requirements by co-implementation concern. Name each group with a short
   uppercase abbreviation (2–5 letters). Example groups: AUTH, API, DATA, UI, CLI.
3. Format each requirement as: `**REQ-{GRP}-NNN:** {single-sentence condition}.`
   - NNN is zero-padded, resets per group (001, 002, ...).
   - Requirements are conditions, not instructions: "The system must X" not "Do X".
4. Fetch the current issue body:
   ```bash
   gh issue view {N} --json body -q .body
   ```
5. If `## Requirements` section already exists in the body: skip (idempotent).
6. If `--dry-run` is set: print the generated requirements to stdout but do NOT call
   `gh issue edit`. Set `requirements_generated: true`, `requirements_appended: false`.
7. Otherwise, append the Requirements section:
   ```bash
   gh issue edit {N} --body "$(gh issue view {N} --json body -q .body)

## Requirements

### {Group Name}

- **REQ-{GRP}-001:** ...
- **REQ-{GRP}-002:** ...

### {Group 2 Name}

- **REQ-{GRP2}-001:** ..."
   ```
8. If the issue is too vague for clean requirement extraction (no clear goal,
   contradictory claims, or entirely implementation-prescriptive): do not force it.
   Instead: post a comment flagging the issue as needs more detail, suggest
   remediation routing if the goal is unclear. Set `requirements_generated: false`.
9. On success: set `requirements_generated: true`, `requirements_appended: true`.

### Step 8: Mixed-Concern Detection

Examine whether the issue blends distinct concern categories (e.g., bug fix + new feature,
investigation + implementation work). Criteria: the issue describes two separate,
independently-completable outcomes.

If mixed concerns detected:
- Notify user: *"This issue mixes {concern_a} and {concern_b}. Consider splitting."*
- If `--split` is set: create a sub-issue for each concern via `gh issue create`,
  link them back to the parent with a comment, and track all sub-issue numbers.

### Step 9: Label Application

If `--dry-run`: skip this step, print a preview of what would be applied, emit result
block, exit.

Otherwise:

```bash
# Ensure labels exist (idempotent)
gh label create "recipe:implementation" --force \
    --description "Route: proceed directly to implementation" \
    --color "0E8A16"
gh label create "recipe:remediation" --force \
    --description "Route: investigate/decompose before implementation" \
    --color "D93F0B"
gh label create "bug" --force \
    --description "Existing behavior is broken" \
    --color "d73a4a"
gh label create "enhancement" --force \
    --description "New feature or request" \
    --color "a2eeef"

# Apply triage labels (use the route determined in Step 6)
gh issue edit {issue_number} --add-label "recipe:implementation"
# or, for remediation route:
gh issue edit {issue_number} --add-label "recipe:remediation"
gh issue edit {issue_number} --add-label "{issue_type}"
```

## Critical Constraints

**NEVER:**
- Create or modify GitHub issues without explicit user intent
- Apply labels not in the defined set (`recipe:implementation`, `recipe:remediation`, `bug`, `enhancement`)
- Skip the dedup check when creating a new issue (unless `--issue N` is provided)
- Proceed past Step 2 (Auth) if `gh auth status` fails
- Create a GitHub issue without displaying the draft and receiving explicit Y confirmation
  (unless `--issue N` or `--dry-run` is active)

**ALWAYS:**
- Confirm repo access with `gh repo view` before any issue operations
- Use `--force` on all `gh label create` calls for idempotency
- Emit the result block (`---prepare-issue-result---`) even on dry-run
- Respect `--dry-run`: never create or edit anything when this flag is set

## Output

Emit to stdout for recipe capture:

```
---prepare-issue-result---
{
  "issue_url": "https://github.com/owner/repo/issues/N",
  "issue_number": N,
  "route": "recipe:implementation",
  "issue_type": "enhancement",
  "confidence": "high",
  "rationale": "...",
  "labels_applied": ["recipe:implementation", "enhancement"],
  "dry_run": false,
  "sub_issues": [],
  "requirements_generated": true,
  "requirements_appended": true
}
---/prepare-issue-result---
```
