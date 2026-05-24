---
name: skill-curator
description: "Autonomous skill lifecycle manager. Reviews skill-compounder drafts, promotes high-confidence patterns, merges duplicates, archives low-quality drafts. Zero manual review required - runs on every session start."
---

# Skill Curator

Autonomous skill lifecycle system. Works in partnership with `skill-compounder` to close the loop: observe -> draft -> review -> promote.

## The Pipeline

```
1. You work normally (no manual action needed)
2. skill-compounder (Stop hook) detects successful patterns
3. Draft written to ~/.claude/skills-drafts/
4. skill-curator (SessionStart hook) reviews all drafts
5. Drafts are either:
   - PROMOTED to ~/.claude/skills/ (confidence >= 80, no duplicates)
   - MERGED with existing similar skill
   - ARCHIVED to ~/.claude/skills-drafts/archive/ (confidence < 50)
   - KEPT in drafts for next review (50-79, needs more evidence)
```

## Promotion Criteria

A draft is auto-promoted when ALL of these are true:

| Criterion | Threshold |
|-----------|-----------|
| Confidence | >= 80 |
| Occurrences | >= 3 (or category is error-recovery) |
| Uniqueness | Not duplicate of existing skill |
| Age | Less than 14 days old |
| Category | One of: repeated-workflow, error-recovery, domain-pattern |

## Archive Criteria

A draft is auto-archived when ANY of these are true:

- Confidence < 50 (not reproducible)
- Age > 14 days without promotion (stale)
- Duplicate of existing promoted skill

## Duplicate Detection

Before promoting, check against existing skills:
1. **Name match** - exact directory name
2. **Category + description overlap** - same category, 4+ keyword overlap

If duplicate found, either merge evidence into existing skill or archive.

## Draft File Format

Drafts live in `~/.claude/skills-drafts/<name>.md`:

```yaml
---
name: pattern-abc123
description: "Procedural pattern: Read -> Edit -> Test -> Commit"
category: repeated-workflow
confidence: 85
occurrences: 7
source_session: s-xyz789
generated_at: 2026-04-12T03:45:00Z
status: draft
---
```

When promoted, `status: draft` becomes `status: active`.

## Integration

- **skill-compounder** (Stop hook): Generates drafts from session observations
- **self-learner**: Provides error-pattern data that feeds skill-compounder
- **canavar**: Cross-trains all agents when skill is promoted
- **layered-recall**: Makes new skills queryable via Depth 1-3 pattern

## Metrics

Tracked in `~/.claude/skill-evolution.jsonl`:
- draft_generated_at
- promoted_at
- time_to_promotion
- usage_after_promotion
- retention_rate (still active after 30 days)

## Safety

- **No manual override needed** - runs silently on session start
- **No destructive actions** - drafts/skills are moved, not deleted
- **Rollback via git** - all promoted skills are in git history
- **High threshold** - 80+ confidence prevents low-quality promotion
