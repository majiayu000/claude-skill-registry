---
name: learned-patterns
description: Manage learned patterns - list, view, archive, boost or penalize confidence. Use when you want to see what patterns Claude has learned, review pattern effectiveness, or manage the pattern library.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
infer: false
---

# Learned Patterns Management

Manage the auto-learning pattern library. View, list, archive, and adjust confidence of learned patterns.

## Quick Commands

```
/learned-patterns                    # List all active patterns
/learned-patterns list               # Same as above
/learned-patterns list backend       # List patterns in category
/learned-patterns view <id>          # View pattern details
/learned-patterns archive <id>       # Archive a pattern
/learned-patterns boost <id>         # Increase confidence (+10%)
/learned-patterns penalize <id>      # Decrease confidence (-15%)
/learned-patterns stats              # Show pattern statistics
```

## Actions

### List Patterns

List all active patterns with confidence scores:

```
/learned-patterns list
/learned-patterns list backend       # Filter by category
/learned-patterns list --low         # Show low confidence (< 50%)
/learned-patterns list --high        # Show high confidence (> 70%)
```

**Execute**: Run the list script to display patterns:

```bash
node .claude/skills/learned-patterns/scripts/list-patterns.cjs [category] [--low|--high]
```

### View Pattern Details

View full details of a specific pattern:

```
/learned-patterns view <pattern-id>
```

Shows:
- Pattern type and category
- Wrong/right content
- Keywords and file patterns
- Confidence score and history
- Related files

**Execute**: Run the view script:

```bash
node .claude/skills/learned-patterns/scripts/view-pattern.cjs <pattern-id>
```

### Archive Pattern

Remove a pattern from active injection (soft delete):

```
/learned-patterns archive <pattern-id> [reason]
```

Pattern is moved to `archive/` directory but not deleted.

**Execute**: Run the archive script:

```bash
node .claude/skills/learned-patterns/scripts/archive-pattern.cjs <pattern-id> [reason]
```

### Boost Confidence

Manually increase pattern confidence by 10%:

```
/learned-patterns boost <pattern-id>
```

Use when you want to prioritize a pattern or confirm it's useful.

**Execute**: Run the boost script:

```bash
node .claude/skills/learned-patterns/scripts/adjust-confidence.cjs <pattern-id> boost
```

### Penalize Confidence

Manually decrease pattern confidence by 15%:

```
/learned-patterns penalize <pattern-id>
```

Use when a pattern is causing issues or needs review.

**Execute**: Run the penalize script:

```bash
node .claude/skills/learned-patterns/scripts/adjust-confidence.cjs <pattern-id> penalize
```

### Statistics

Show pattern library statistics:

```
/learned-patterns stats
```

Shows:
- Total patterns by category
- Average confidence scores
- Injection frequency
- Confirmation/conflict ratios

**Execute**: Run the stats script:

```bash
node .claude/skills/learned-patterns/scripts/pattern-stats.cjs
```

## Pattern Lifecycle

```
┌─────────────────────────────────────────────────────────────┐
│  DETECTION (UserPromptSubmit)                               │
│    └── User correction detected → Candidate created         │
│    └── Confidence: 40% (implicit) or 80% (explicit)         │
│                                                             │
│  CONFIRMATION                                               │
│    └── User confirms → Pattern saved                        │
│    └── User rejects → Pattern discarded                     │
│                                                             │
│  INJECTION (SessionStart/PreToolUse)                        │
│    └── Relevant patterns injected based on context          │
│    └── Max 5 patterns, ~400 tokens                          │
│                                                             │
│  FEEDBACK LOOP                                              │
│    └── Pattern followed → Confidence +5%                    │
│    └── Pattern ignored → Confidence -10%                    │
│                                                             │
│  DECAY & PRUNING                                            │
│    └── 30 days unused → Confidence decays                   │
│    └── Below 20% → Auto-archived                            │
└─────────────────────────────────────────────────────────────┘
```

## Storage Structure

```
.claude/learned-patterns/
├── index.yaml              # Pattern lookup index
├── backend/                # Backend C#/.NET patterns
│   ├── validation-result.yaml
│   └── repository-pattern.yaml
├── frontend/               # Frontend Angular/TS patterns
│   ├── component-base.yaml
│   └── store-pattern.yaml
├── workflow/               # Development workflow patterns
│   └── todo-tracking.yaml
├── general/                # Cross-cutting patterns
│   └── code-style.yaml
└── archive/                # Archived patterns
    └── backend/
        └── old-pattern.yaml
```

## Pattern Schema

```yaml
id: pat_abc123
category: backend
type: anti-pattern | best-practice | preference | convention
trigger:
  keywords: [validation, exception, throw]
  file_patterns: ["*CommandHandler.cs", "*Service.cs"]
  context: "Use PlatformValidationResult for validation"
content:
  wrong: "throw new ValidationException()"
  right: "return PlatformValidationResult.Invalid()"
  rationale: "Framework uses result pattern, not exceptions"
metadata:
  source: explicit-teaching | user-correction
  confidence: 0.75
  first_seen: 2025-01-10
  last_confirmed: 2025-01-12
  occurrences: 3
  confirmations: 2
  conflicts: 0
  related_files:
    - src/Services/Growth/UseCaseCommands/Employee/SaveEmployeeCommand.cs
tags: [validation, cqrs, backend]
```

## Confidence Thresholds

| Threshold | Meaning |
|-----------|---------|
| 80-100% | High confidence, always injected when relevant |
| 50-79% | Medium confidence, injected with context match |
| 30-49% | Low confidence, injected only on strong match |
| 20-29% | Very low, candidate for review |
| < 20% | Auto-archived |

## Related Commands

| Command | Purpose |
|---------|---------|
| `/learn` | Explicitly teach a new pattern |
| `/code-patterns` | View static code patterns documentation |

## Troubleshooting

### Patterns Not Injecting

1. Check confidence: `node .claude/skills/learned-patterns/scripts/view-pattern.cjs <id>`
2. Verify file patterns match current context
3. Check if pattern was archived

### Too Many Patterns Injecting

1. Review low-confidence patterns: `/learned-patterns list --low`
2. Archive irrelevant patterns
3. Adjust MIN_RELEVANCE_SCORE in pattern-constants.cjs

### Pattern Conflicts

If patterns conflict with documentation:
1. Pattern is automatically blocked on save
2. Update docs/claude/*.md if pattern should override
3. Or archive the conflicting pattern

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
