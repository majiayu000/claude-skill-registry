---
name: steering-matcher
description: Match file paths against steering file glob patterns to determine applicable steering guidance. Use when orchestrator needs to inject context-aware guidance based on files being modified.
license: MIT
metadata:
version: 1.0.0
model: claude-haiku-4-5
---

# Steering File Matcher Skill

## Triggers

| Trigger Phrase | Operation |
|----------------|-----------|
| `match steering for these files` | get_applicable_steering.py |
| `which steering applies to this task` | Pattern match against changed files |
| `inject steering context` | Return applicable steering sorted by priority |

## Purpose

This skill helps orchestrator determine which steering files to inject into agent context based on the files being modified.

- Match file paths against glob patterns in steering file front matter
- Return applicable steering files sorted by priority
- Enable token-efficient context injection (30%+ savings)

## When to Use

Use this skill when:

- Orchestrator needs to inject context-aware steering based on files being modified
- You want to scope agent guidance to only relevant files (token optimization)
- Matching file paths against `applyTo` glob patterns in steering front matter

Use manual file reading instead when:

- You already know which steering file applies
- The task affects a single known steering domain

## Quick Usage

### Using get_applicable_steering.py Script

The script in `.claude/skills/steering-matcher/scripts/get_applicable_steering.py` handles pattern matching.

```bash
# Match files against steering patterns
python3 .claude/skills/steering-matcher/scripts/get_applicable_steering.py \
    --files "src/claude/analyst.md" ".agents/security/TM-001-auth-flow.md" \
    --steering-path ".agents/steering"

# Output: JSON array of objects with name, path, apply_to, priority
```

## Process

This skill integrates with the orchestrator workflow:

1. **Task Analysis**: Orchestrator identifies files affected by task
2. **Pattern Matching**: Use this skill to find applicable steering
3. **Context Injection**: Include matched steering in agent prompt
4. **Token Optimization**: Only inject relevant guidance

### Standard Orchestrator Workflow

```bash
# 1. Identify files from task
# 2. Get applicable steering
python3 .claude/skills/steering-matcher/scripts/get_applicable_steering.py \
    --files "src/claude/security.md" ".agents/security/SR-001-oauth-review.md"

# 3. Inject into agent context
# Output: JSON with name, path, apply_to, priority sorted by priority descending
```

## Implementation

See `scripts/get_applicable_steering.py` for the Python implementation.

## Testing

Run pytest to verify pattern matching:

```bash
pytest .claude/skills/steering-matcher/tests/
```

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Hardcoding steering file paths | Bypasses pattern matching, breaks on restructuring | Use get_applicable_steering.py |
| Injecting all steering files | Token bloat, irrelevant context | Match against changed files only |
| Ignoring priority ordering | Lower-priority guidance may contradict higher | Process results in priority order |

## Verification

After execution:

- [ ] Returned steering files match the `applyTo` patterns for the given files
- [ ] Results are sorted by priority (highest first)
- [ ] No duplicate steering entries in output

## Scripts

### get_applicable_steering.py

Matches file paths against steering glob patterns and returns applicable guidance.

```bash
python3 .claude/skills/steering-matcher/scripts/get_applicable_steering.py --files <file1> [<file2> ...]
```

## Related

- [Steering System README](../../../.agents/steering/README.md)
- [Enhancement Project Plan](../../../.agents/planning/enhancement-PROJECT-PLAN.md)
- [Orchestrator Agent](../../../src/claude/orchestrator.md)
