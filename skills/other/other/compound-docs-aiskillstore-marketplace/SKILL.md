---
name: compound-docs
description: Capture solved problems as searchable documentation with pattern detection. This skill auto-triggers when users confirm a fix worked ("that worked", "it's fixed", "working now") or manually via /compound command.
version: 0.1.0-beta
license: MIT
compatibility: opencode
---

# compound-docs

> Each documented solution compounds your team's knowledge. The first time 
> you solve a problem takes research. Document it, and the next occurrence 
> takes minutes. Knowledge compounds.

This skill is inspired by [Every.to's compound-engineering plugin](https://github.com/EveryInc/compound-engineering-plugin).

## Auto-Invoke Triggers

This skill auto-triggers when the user says:
- "that worked"
- "it's fixed"
- "working now"
- "problem solved"
- "that did it"

Manual command: `/compound`

## Workflow

### Step 1: Detect Trigger

When a trigger phrase is detected or `/compound` is invoked:

1. Confirm the problem is actually solved (not still in progress)
2. Check if the fix is worth documenting

**Skip documentation for trivial fixes:**
- Simple typos
- Obvious syntax errors (missing semicolon, bracket)
- Single-line fixes that were immediately obvious

If skipping, briefly explain why: "This was a simple typo fix - skipping documentation."

### Step 2: Gather Context

Read [schema.yaml](schema.yaml) to get valid enum values, then extract from the conversation:

| Field | Required | Description |
|-------|----------|-------------|
| Symptom | Yes | Error message or observable behavior |
| Category | Yes | From schema.yaml `category.values` (or add new) |
| Component | No | From schema.yaml `component.values` (or add new) |
| Root cause | No | From schema.yaml `root_cause.values` (or add new) |
| Solution | Yes | The fix that worked |
| Prevention | No | How to avoid this in the future |

**If a value doesn't exist in schema.yaml:**
1. Add the new value to the appropriate enum in `schema.yaml`
2. If it's a new category, create the directory: `mkdir -p {output_dir}/{new-category}`

**If critical info is missing, ask:**

```
To document this fix, I need a few details:

1. Category: What type of issue was this?
   [list current values from schema.yaml]
   Or suggest a new category if none fit
```

### Step 3: Check for Similar Issues

Before creating a new doc, search for similar existing issues:

1. **Keyword match** - Search `{output_dir}/` for error message fragments or key symptom phrases
2. **File path match** - Check if the same files are involved in existing docs
3. **Import/dependency match** - Check if the same libraries or modules are mentioned

```bash
# Example searches
grep -rl "ErrorMessage" docs/solutions/
grep -l "path/to/file" docs/solutions/**/*.md
```

**If potential matches found:**

```
Found potentially related issues:
- docs/solutions/integration/api-timeout-20250102.md
- docs/solutions/integration/auth-header-missing-20250105.md

Are any of these the same or related issue? (y/n)
```

If related, add to the `related` field in frontmatter.

### Step 4: Create Documentation

**Validate against schema.yaml:**
1. Read schema.yaml for current valid enum values
2. Ensure all required fields are present
3. Ensure enum values exist (or add them first)

**Generate filename:**
- Format: `{sanitized-symptom}-{YYYYMMDD}.md`
- Sanitize: lowercase, replace spaces with hyphens, remove special chars, truncate to 80 chars

**Create file at:** `{output_dir}/{category}/{filename}`

**Ensure directory exists:**
```bash
mkdir -p {output_dir}/{category}
```

**Use the Solution Doc Template below.**

### Step 5: Pattern Promotion

After creating the doc, check if this issue has occurred multiple times.

**If similar issues >= threshold (default: 2):**

```
This issue has occurred {N} times:
- {link to issue 1}
- {link to issue 2}
- {link to current issue}

Promote to patterns.md? This surfaces it prominently for future sessions.
1. Yes - Add to patterns
2. No - Keep as regular doc only
```

**If yes:** Append to `{output_dir}/patterns.md` using the Pattern Template below.

## Solution Doc Template

```markdown
---
date: {YYYY-MM-DD}
category: {category}
symptoms:
  - {symptom 1}
  - {symptom 2}
component: {component}
root_cause: {root_cause}
tags: [{keyword1}, {keyword2}]
related: []
---

# {Problem Title}

## Problem

{1-2 sentence description of what went wrong}

## Symptoms

- {What you observed - error messages, behavior, etc.}

## What Didn't Work

- {Attempted solution 1} - {Why it failed}
- {Attempted solution 2} - {Why it failed}

## Solution

{Description of the fix}

```{language}
# Before (broken)
{code before}

# After (fixed)
{code after}
```

## Why This Works

{Technical explanation of the root cause and why the solution addresses it}

## Prevention

{How to avoid this in the future - tests, linting rules, patterns to follow}
```

## Pattern Template

When adding to `patterns.md`:

```markdown
## {Pattern Name}

**Occurrences:** {N} times ({link1}, {link2}, ...)

### WRONG

```{language}
{code that causes the problem}
```

### CORRECT

```{language}
{code that fixes it}
```

**Why:** {Technical explanation}

**When this applies:** {Context or conditions when this pattern is relevant}
```

## Integration

### Reference in AGENTS.md

Add to your project's AGENTS.md to ensure patterns are checked:

```markdown
## Required Reading

Before making changes, review known patterns:
- [Solution Patterns](docs/solutions/patterns.md)
```

### Consuming Solutions

Other workflows can discover and apply documented solutions:

**Search by keyword:**
```bash
grep -rl "keyword" docs/solutions/
```

**Search by category:**
```bash
ls docs/solutions/deployment/
```

**Search by tag:**
```bash
grep -l "tags:.*docker" docs/solutions/**/*.md
```

`patterns.md` is the primary integration point - check it first for critical patterns before making changes.

## Example Scenario

**User:** "That worked! The Docker build was failing because of the cache issue."

**Agent response:**

```
Great! Let me document this fix.

**Reading schema.yaml...**
Current categories: developer-experience, deployment, ui, integration, performance, testing
Current components: (none yet)
Current root_causes: (none yet)

**Gathering context...**

From our conversation:
- Symptom: Docker build failing with "layer not found" error
- Category: deployment
- Component: docker (adding to schema.yaml)
- Root cause: stale-cache (adding to schema.yaml)
- Solution: Added `--no-cache` flag and updated base image tag
- Prevention: Pin base image versions, use `docker system prune` periodically

**Updating schema.yaml...**
Added 'docker' to component.values
Added 'stale-cache' to root_cause.values

**Checking for similar issues...**
No related issues found.

**Creating documentation...**
Created: docs/solutions/deployment/docker-layer-not-found-20250106.md

Documentation complete.
```
