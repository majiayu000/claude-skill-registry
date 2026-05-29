---
name: cross-review-policy
version: "1.0.0"
category: _internal
description: "Cross-Review Policy Skill"
---

# Cross-Review Policy Skill

> Version: 1.0.0
> Category: Workflows
> Triggers: Completing AI work, code review, presenting to user

## Quick Reference

### Core Rule

**ALL work performed by Claude Code or Google Gemini MUST be reviewed by OpenAI Codex.**

### Review Flow

```
Claude/Gemini performs task
         ↓
    Commit changes
         ↓
    Codex reviews
         ↓
    Feedback needed?
    ├── No → Present to user (APPROVED)
    └── Yes → Implement fixes
                   ↓
              Iteration < 3?
              ├── Yes → Re-commit → Codex reviews
              └── No → Present to user (LIMIT_REACHED)
```

### Maximum Iterations: 3

| Iteration | Status | Action |
|-----------|--------|--------|
| 1 | First review | Codex reviews original commit |
| 2 | Second review | Codex reviews fix commit |
| 3 | Final review | Last chance for approval |
| 3+ | Limit reached | Present to user regardless |

## Commands

```bash
# Trigger cross-review loop
./scripts/ai-review/cross-review-loop.sh --max-iterations 3

# Check review status
./scripts/ai-review/review-manager.sh list

# Check iteration status
./scripts/ai-review/review-manager.sh iteration-status <review_id>

# Force complete (skip remaining iterations)
./scripts/ai-review/review-manager.sh force-complete <review_id>
```

## Commit Message Formats

### Original Work Commit
```
<type>: <description>

<body>

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Review Fix Commit
```
fix(review): <description>

Addresses Codex review feedback (iteration N/3)
Review-ID: <review_id>
Original-Commit: <original_sha>

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Review Types Covered

| Review Type | Trigger |
|-------------|---------|
| Code Reviews | Every commit |
| SPARC Gate-Pass | Phase completion |
| QA Reviews | Feature completion |
| Security Reviews | Security-sensitive changes |
| Architecture Reviews | Architectural changes |

## Provider Mapping

| Primary Agent | Reviewer |
|--------------|----------|
| Claude Code | OpenAI Codex |
| Google Gemini | OpenAI Codex |
| OpenAI Codex | N/A (is the reviewer) |

## Exit Conditions

Review loop exits when ANY condition is met:
1. **APPROVED**: Codex approves the changes
2. **MAX_ITERATIONS**: 3 iterations completed
3. **FORCE_COMPLETE**: User forces completion
4. **NO_CHANGES**: No actionable feedback

## Exceptions (NOT Required)

- Documentation-only changes (pure markdown/text)
- Configuration files (non-code config)
- Emergency hotfixes (with explicit user override)
- User-initiated commits (non-AI commits)

## Full Reference

See: @docs/modules/ai/CROSS_REVIEW_POLICY.md

---

*Use this when completing AI work, understanding review requirements, or managing review iterations.*
