---
name: skill-evolution
description: Analyze, evolve, and rollback skills based on usage patterns. Use when evolving skills, improving skill definitions, updating skill content.
context: inherit
version: 1.0.0
author: SkillForge
tags: [skill-management, evolution, versioning, analytics]
user-invocable: true
---

# Skill Evolution Manager

Enables skills to automatically improve based on usage patterns, user edits, and success rates. Provides version control with safe rollback capability.

## When to Use

- Reviewing how skills are performing across sessions
- Identifying patterns in user edits to skill outputs
- Applying learned improvements to skill templates
- Rolling back problematic skill changes
- Tracking skill version history and success rates

## Quick Reference

| Command | Description |
|---------|-------------|
| `/skf:skill-evolution` | Show evolution report for all skills |
| `/skf:skill-evolution analyze <skill-id>` | Analyze specific skill patterns |
| `/skf:skill-evolution evolve <skill-id>` | Review and apply suggestions |
| `/skf:skill-evolution history <skill-id>` | Show version history |
| `/skf:skill-evolution rollback <skill-id> <version>` | Restore previous version |

---

## How It Works

The skill evolution system operates in three phases:

```
COLLECT                    ANALYZE                    ACT
───────                    ───────                    ───
┌─────────────┐           ┌─────────────┐           ┌─────────────┐
│ PostTool    │──────────▶│ Evolution   │──────────▶│ /skf:skill  │
│ Edit        │  patterns │ Analyzer    │ suggest   │ evolve      │
│ Tracker     │           │ Engine      │           │ command     │
└─────────────┘           └─────────────┘           └─────────────┘
     │                          │                          │
     ▼                          ▼                          ▼
┌─────────────┐           ┌─────────────┐           ┌─────────────┐
│ edit-       │           │ evolution-  │           │ versions/   │
│ patterns.   │           │ registry.   │           │ snapshots   │
│ jsonl       │           │ json        │           │             │
└─────────────┘           └─────────────┘           └─────────────┘
```

### Edit Pattern Categories

The system tracks these common edit patterns:

| Pattern | Description | Detection |
|---------|-------------|-----------|
| `add_pagination` | User adds pagination to API responses | `limit.*offset`, `cursor.*pagination` |
| `add_rate_limiting` | User adds rate limiting | `rate.?limit`, `throttl` |
| `add_error_handling` | User adds try/catch blocks | `try.*catch`, `except` |
| `add_types` | User adds TypeScript/Python types | `interface\s`, `Optional` |
| `add_validation` | User adds input validation | `validate`, `Pydantic`, `Zod` |
| `add_logging` | User adds logging/observability | `logger\.`, `console.log` |
| `remove_comments` | User removes generated comments | Pattern removal detection |
| `add_auth_check` | User adds authentication checks | `@auth`, `@require_auth` |

### Suggestion Thresholds

| Threshold | Default | Description |
|-----------|---------|-------------|
| Minimum Samples | 5 | Uses before generating suggestions |
| Add Threshold | 70% | Frequency to suggest adding pattern |
| Auto-Apply Confidence | 85% | Confidence for auto-application |
| Rollback Trigger | -20% | Success rate drop to trigger rollback |

---

## Subcommand: Report (Default)

**Usage:** `/skf:skill-evolution`

Shows evolution report for all tracked skills.

### Implementation

```bash
# Run the evolution engine report
"${CLAUDE_PROJECT_DIR}/.claude/scripts/evolution-engine.sh" report
```

### Sample Output

```
Skill Evolution Report
══════════════════════════════════════════════════════════════

Skills Summary:
┌────────────────────────────┬─────────┬─────────┬───────────┬────────────┐
│ Skill                      │ Uses    │ Success │ Avg Edits │ Suggestions│
├────────────────────────────┼─────────┼─────────┼───────────┼────────────┤
│ api-design-framework       │     156 │     94% │       1.8 │          2 │
│ database-schema-designer   │      89 │     91% │       2.1 │          1 │
│ fastapi-patterns           │      67 │     88% │       2.4 │          3 │
└────────────────────────────┴─────────┴─────────┴───────────┴────────────┘

Summary:
  Skills tracked: 3
  Total uses: 312
  Overall success rate: 91%

Top Pending Suggestions:
1. 93% | api-design-framework | add add_pagination
2. 88% | api-design-framework | add add_rate_limiting
3. 85% | fastapi-patterns | add add_error_handling
```

---

## Subcommand: Analyze

**Usage:** `/skf:skill-evolution analyze <skill-id>`

Analyzes edit patterns for a specific skill.

### Implementation

```bash
# Run analysis for specific skill
"${CLAUDE_PROJECT_DIR}/.claude/scripts/evolution-engine.sh" analyze "$SKILL_ID"
```

### Sample Output

```
Skill Analysis: api-design-framework
────────────────────────────────────
Uses: 156 | Success: 94% | Avg Edits: 1.8

Edit Patterns Detected:
┌──────────────────────────┬─────────┬──────────┬────────────┐
│ Pattern                  │ Freq    │ Samples  │ Confidence │
├──────────────────────────┼─────────┼──────────┼────────────┤
│ add_pagination           │    85%  │ 132/156  │       0.93 │
│ add_rate_limiting        │    72%  │ 112/156  │       0.88 │
│ add_error_handling       │    45%  │  70/156  │       0.56 │
└──────────────────────────┴─────────┴──────────┴────────────┘

Pending Suggestions:
1. 93% conf: ADD add_pagination to template
2. 88% conf: ADD add_rate_limiting to template

Run `/skf:skill-evolution evolve api-design-framework` to review
```

---

## Subcommand: Evolve

**Usage:** `/skf:skill-evolution evolve <skill-id>`

Interactive review and application of improvement suggestions.

### Implementation

When this subcommand is invoked:

1. **Get Suggestions:**
```bash
SUGGESTIONS=$("${CLAUDE_PROJECT_DIR}/.claude/scripts/evolution-engine.sh" suggest "$SKILL_ID")
```

2. **For Each Suggestion, Present Interactive Options:**

Use `AskUserQuestion` to let the user decide on each suggestion:

```json
{
  "questions": [{
    "question": "Apply suggestion: ADD add_pagination to template? (93% confidence, 132/156 users add this)",
    "header": "Evolution",
    "options": [
      {"label": "Apply", "description": "Add this pattern to the skill template"},
      {"label": "Skip", "description": "Skip for now, ask again later"},
      {"label": "Reject", "description": "Never suggest this again"}
    ],
    "multiSelect": false
  }]
}
```

3. **On Apply:**
   - Create version snapshot first
   - Apply the suggestion to skill files
   - Update evolution registry

4. **On Reject:**
   - Mark suggestion as rejected in registry
   - Won't be suggested again

### Applying Suggestions

When a user accepts a suggestion, the implementation depends on the suggestion type:

**For `add` suggestions to templates:**
- Add the pattern to the skill's template files
- Update SKILL.md with new guidance

**For `add` suggestions to references:**
- Create new reference file in `references/` directory

**For `remove` suggestions:**
- Remove the identified content
- Archive in version snapshot first

---

## Subcommand: History

**Usage:** `/skf:skill-evolution history <skill-id>`

Shows version history with performance metrics.

### Implementation

```bash
# Run version manager list
"${CLAUDE_PROJECT_DIR}/.claude/scripts/version-manager.sh" list "$SKILL_ID"
```

### Sample Output

```
Version History: api-design-framework
══════════════════════════════════════════════════════════════

Current Version: 1.2.0

┌─────────┬────────────┬─────────┬───────┬───────────┬────────────────────────────┐
│ Version │ Date       │ Success │ Uses  │ Avg Edits │ Changelog                  │
├─────────┼────────────┼─────────┼───────┼───────────┼────────────────────────────┤
│ 1.2.0   │ 2026-01-14 │    94%  │   156 │       1.8 │ Added pagination pattern   │
│ 1.1.0   │ 2026-01-05 │    89%  │    80 │       2.3 │ Added error handling ref   │
│ 1.0.0   │ 2025-11-01 │    78%  │    45 │       3.2 │ Initial release            │
└─────────┴────────────┴─────────┴───────┴───────────┴────────────────────────────┘
```

---

## Subcommand: Rollback

**Usage:** `/skf:skill-evolution rollback <skill-id> <version>`

Restores a skill to a previous version.

### Implementation

1. **Confirm with User:**

Use `AskUserQuestion` for confirmation:

```json
{
  "questions": [{
    "question": "Rollback api-design-framework from 1.2.0 to 1.0.0? Current version will be backed up.",
    "header": "Rollback",
    "options": [
      {"label": "Confirm Rollback", "description": "Restore version 1.0.0"},
      {"label": "Cancel", "description": "Keep current version"}
    ],
    "multiSelect": false
  }]
}
```

2. **On Confirm:**
```bash
"${CLAUDE_PROJECT_DIR}/.claude/scripts/version-manager.sh" restore "$SKILL_ID" "$VERSION"
```

3. **Report Result:**
```
Restored api-design-framework to version 1.0.0
Previous version backed up to: versions/.backup-1.2.0-1736867234
```

---

## Data Files

| File | Purpose | Format |
|------|---------|--------|
| `.claude/feedback/edit-patterns.jsonl` | Raw edit pattern events | JSONL (append-only) |
| `.claude/feedback/evolution-registry.json` | Aggregated suggestions | JSON |
| `.claude/feedback/metrics.json` | Skill usage metrics | JSON |
| `skills/<cat>/<name>/versions/` | Version snapshots | Directory |
| `skills/<cat>/<name>/versions/manifest.json` | Version metadata | JSON |

---

## Auto-Evolution Safety

The system includes safety mechanisms:

1. **Version Snapshots**: Always created before changes
2. **Rollback Triggers**: Auto-alert if success rate drops >20%
3. **Human Review**: High-confidence suggestions require approval
4. **Rejection Memory**: Rejected suggestions aren't re-suggested

### Health Monitoring

The system monitors skill health and can trigger warnings:

```
WARNING: api-design-framework success rate dropped from 94% to 71%
Consider: /skf:skill-evolution rollback api-design-framework 1.1.0
```

---

## References

- [Evolution Analysis Methodology](references/evolution-analysis.md)
- [Version Management Guide](references/version-management.md)

---

## Related Skills

- `configure` - Configure SkillForge settings
- `doctor` - Diagnose SkillForge issues
- `feedback-dashboard` - View comprehensive feedback metrics