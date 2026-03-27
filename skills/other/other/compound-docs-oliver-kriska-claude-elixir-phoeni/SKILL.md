---
name: compound-docs
description: Searchable solution documentation system with YAML frontmatter. Builds institutional knowledge from solved problems. Use proactively when consulting past solutions before investigating new issues.
effort: low
user-invocable: false
---

# Compound Docs — Institutional Knowledge Base

Searchable, categorized solution documentation that makes each
debugging session easier than the last.

## Directory Structure

```
.claude/solutions/
├── ecto-issues/
├── liveview-issues/
├── oban-issues/
├── otp-issues/
├── security-issues/
├── testing-issues/
├── phoenix-issues/
├── deployment-issues/
├── performance-issues/
└── build-issues/
```

## Iron Laws

1. **ALWAYS search solutions before investigating** — Check
   `.claude/solutions/` for existing fixes before debugging
2. **YAML frontmatter is MANDATORY** — Every solution needs
   validated metadata per `${CLAUDE_SKILL_DIR}/references/schema.md`
3. **One problem per file** — Never combine multiple solutions
4. **Include prevention** — Every solution documents how to
   prevent recurrence

## Solution File Format

```markdown
---
module: "Accounts"
date: "2025-12-01"
problem_type: runtime_error
component: ecto_schema
symptoms:
  - "Ecto.Association.NotLoaded on user.posts"
root_cause: missing_preload
severity: medium
tags: [preload, association, n-plus-one]
---

# Association NotLoaded on User Posts

## Symptoms
Ecto.Association.NotLoaded raised when accessing user.posts
in UserListLive after filtering.

## Root Cause
Query in Accounts context missing preload for :posts.

## Solution
Added `Repo.preload(:posts)` to `list_users/1`.

## Prevention
Use n1-check skill before shipping list views.
```

## Searching Solutions

```bash
# Search by symptom
grep -rl "NotLoaded" .claude/solutions/
# Search by tag
grep -rl "tags:.*preload" .claude/solutions/
# Search by component
grep -rl "component: ecto" .claude/solutions/
```

## Integration

- `/phx:compound` creates solution docs here
- `/phx:investigate` searches here before debugging
- `/phx:plan` consults for known risks
- `learn-from-fix` feeds into this system

## References

- `${CLAUDE_SKILL_DIR}/references/schema.md` — YAML frontmatter validation schema
- `${CLAUDE_SKILL_DIR}/references/resolution-template.md` — Full solution template
