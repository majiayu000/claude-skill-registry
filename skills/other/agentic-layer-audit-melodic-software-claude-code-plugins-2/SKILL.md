---
name: agentic-layer-audit
description: Audit codebase for agentic layer coverage and identify gaps. Use when assessing agentic layer maturity, identifying investment opportunities, or evaluating primitive coverage.
allowed-tools: Read, Grep, Glob
---

# Agentic Layer Audit Skill

Evaluate a codebase's agentic layer maturity and identify investment opportunities.

## When to Use

- Assessing current agentic layer coverage
- Identifying gaps in automation
- Planning agentic layer investments
- Measuring progress toward 50%+ agentic time

## Core Concept

> "Am I working on the agentic layer or am I working on the application layer?"

This skill helps answer that question by auditing what exists.

## Audit Checklist

### 1. Commands Directory

Check for `.claude/commands/` or equivalent:

```markdown
Look for:
- chore.md      # Chore planning template
- bug.md        # Bug fix template
- feature.md    # Feature planning template
- implement.md  # Implementation HOP
- test.md       # Test execution template
- review.md     # Review template
```

### 2. Specs Directory

Check for `specs/` or equivalent:

```markdown
Look for:
- Issue-based specs (issue-*.md)
- Generated plans (chore-*.md, feature-*.md)
- Deep specs (complex multi-file architectures)
```

### 3. ADW Directory

Check for `adws/` or equivalent:

```markdown
Look for:
- adw_modules/agent.py  # Core agent execution
- Gateway scripts (adw_prompt.py, adw_slash_command.py)
- Composed workflows (adw_*_*.py)
- Triggers (trigger_*.py)
```

### 4. Hooks Directory

Check for `.claude/hooks/` or equivalent:

```markdown
Look for:
- pre_tool_use hooks
- post_tool_use hooks
- user_prompt_submit hooks
```

### 5. Agent Output Directory

Check for `agents/` or equivalent:

```markdown
Look for:
- ADW ID directories
- State files (adw_state.json)
- Output files (cc_*.jsonl, cc_*.json)
```

### 6. Worktree Support

Check for `trees/` or equivalent:

```markdown
Look for:
- Git worktree setup
- Isolation configuration
- Port allocation patterns
```

## Coverage Scoring

| Component | Points | Present? |
| --- | --- | --- |
| .claude/commands/ | 20 | |
| specs/ | 15 | |
| adws/ | 25 | |
| adw_modules/agent.py | 20 | |
| hooks/ | 10 | |
| agents/ | 5 | |
| trees/ | 5 | |

Total: 100 points

| Score | Level | Recommendation |
| --- | --- | --- |
| 0-20 | None | Start with minimum viable layer |
| 21-40 | Basic | Add composed workflows |
| 41-60 | Developing | Add hooks and triggers |
| 61-80 | Advanced | Add worktree isolation |
| 81-100 | Complete | Focus on optimization |

## Key Memory References

- @agentic-layer-structure.md - What to look for
- @the-guiding-question.md - Why this matters
- @agentic-vs-application.md - Layer separation

## Output Format

```markdown
## Agentic Layer Audit Report

**Project:** {name}
**Audit Date:** {date}
**Coverage Score:** {score}/100

### Components Found
- [x] .claude/commands/ (5 templates)
- [x] specs/ (12 specs)
- [ ] adws/ (not found)
- [ ] hooks/ (not found)

### Maturity Level
{Level} - {Recommendation}

### Gaps Identified
1. No ADW scripts for workflow orchestration
2. No hooks for event-driven automation
3. No worktree isolation for parallelization

### Recommended Investments
1. Create adws/adw_modules/agent.py
2. Add gateway script (adw_prompt.py)
3. Create composed workflow for common tasks

### Time Investment Analysis
- Current: ~20% agentic layer
- Target: 50%+ agentic layer
- Gap: Need 30% more investment in agentic work
```

## Anti-Patterns to Identify

- Commands exist but no specs (templates unused)
- Specs exist but no ADWs (manual execution)
- Many one-off scripts instead of composed workflows
- Application layer dominant (>70% of codebase)

## Version History

- **v1.0.0** (2025-12-26): Initial release

---

## Last Updated

**Date:** 2025-12-26
**Model:** claude-opus-4-5-20251101
