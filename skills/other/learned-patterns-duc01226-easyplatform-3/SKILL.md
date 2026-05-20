---
name: learned-patterns
description: "[Tooling & Meta] Manage learned patterns - list, view, archive, boost or penalize confidence. Use when you want to see what patterns Claude has learned, review pattern effectiveness, or manage the pattern library."
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
infer: false
---

# Learned Patterns Management

Manage the auto-learning pattern library. View, list, archive, and adjust confidence.

## Summary

**Goal:** View, list, archive, boost, or penalize learned patterns in the auto-learning pattern library.

- **List patterns:** `node scripts/list-patterns.cjs [category] [--low|--high]`
- **View details:** `node scripts/view-pattern.cjs <id>`
- **Adjust confidence:** `node scripts/adjust-confidence.cjs <id> boost|penalize` (+10% / -15%)
- **Archive:** `node scripts/archive-pattern.cjs <id> [reason]`
- **Stats:** `node scripts/pattern-stats.cjs`

**Key Principles:**
- Patterns auto-decay after 30 days unused; below 20% confidence = auto-archived
- Lifecycle: Detection (40-80%) -> Confirmation -> Injection -> Feedback Loop -> Decay
- Max 5 patterns injected per context (~400 tokens)

## Quick Commands

```
/learned-patterns                    # List all active patterns
/learned-patterns list [category]    # List patterns (optionally filtered)
/learned-patterns list --low|--high  # Filter by confidence
/learned-patterns view <id>          # View pattern details
/learned-patterns archive <id>       # Archive a pattern
/learned-patterns boost <id>         # Increase confidence (+10%)
/learned-patterns penalize <id>      # Decrease confidence (-15%)
/learned-patterns stats              # Show pattern statistics
```

## Script Execution

| Action         | Script                                                                                      |
| -------------- | ------------------------------------------------------------------------------------------- |
| List           | `node .claude/skills/learned-patterns/scripts/list-patterns.cjs [category] [--low\|--high]` |
| View           | `node .claude/skills/learned-patterns/scripts/view-pattern.cjs <id>`                        |
| Archive        | `node .claude/skills/learned-patterns/scripts/archive-pattern.cjs <id> [reason]`            |
| Boost/Penalize | `node .claude/skills/learned-patterns/scripts/adjust-confidence.cjs <id> boost\|penalize`   |
| Stats          | `node .claude/skills/learned-patterns/scripts/pattern-stats.cjs`                            |

## Pattern Lifecycle

```
DETECTION (UserPromptSubmit)
  └── Confidence: 40% (implicit) or 80% (explicit /learn)

CONFIRMATION
  └── User confirms → saved | User rejects → discarded

INJECTION (SessionStart/PreToolUse)
  └── Relevant patterns injected (max 5, ~400 tokens)

FEEDBACK LOOP
  └── Followed → +5% | Ignored → -10%

DECAY & PRUNING
  └── 30 days unused → decay | Below 20% → auto-archived
```

## Confidence Thresholds

| Range   | Behavior                      |
| ------- | ----------------------------- |
| 80-100% | Always injected when relevant |
| 50-79%  | Injected with context match   |
| 30-49%  | Injected only on strong match |
| 20-29%  | Candidate for review          |
| < 20%   | Auto-archived                 |

## Pattern Schema

```yaml
id: pat_abc123
category: backend
type: anti-pattern | best-practice | preference | convention
trigger:
  keywords: [validation, exception]
  file_patterns: ["*CommandHandler.cs"]
content:
  wrong: "throw new ValidationException()"
  right: "return PlatformValidationResult.Invalid()"
  rationale: "Framework uses result pattern, not exceptions"
metadata:
  source: explicit-teaching | user-correction
  confidence: 0.75
  first_seen: 2025-01-10
  occurrences: 3
  confirmations: 2
  conflicts: 0
```

## Troubleshooting

- **Not injecting**: Check confidence, file pattern match, archived status
- **Too many injecting**: Archive irrelevant patterns, review `--low` confidence list
- **Conflicts with docs**: Pattern auto-blocked; update docs or archive pattern

## Related

- `/learn` - Teach a new pattern
- `/code-patterns` - View static code patterns documentation


## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
