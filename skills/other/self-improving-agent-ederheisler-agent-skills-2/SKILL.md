---
name: self-improvement
description: "Captures learnings, errors, and corrections to enable continuous improvement. Use when: (1) A command or operation fails unexpectedly, (2) User corrects the agent ('No, that's wrong...', 'Actually...'), (3) User requests a capability that doesn't exist, (4) An external API or tool fails, (5) The agent realizes its knowledge is outdated or incorrect, (6) A better approach is discovered for a recurring task. Also review learnings before major tasks."
metadata:
  author: eder
  version: "1.0"
---

# Self-Improvement Skill

Log learnings and errors to markdown files for continuous improvement. Coding agents can later process these into fixes, and important learnings get promoted to project memory.

**Not for** general Q&A, coding tasks, or ad-hoc reasoning. Use only to log, review, and promote learnings/errors/feature requests.

**Context discipline:** Do not open whole log files; append directly or read only a small slice around the target entry.

## Memory Index (progressive loading)

| Purpose | Path |
|---------|------|
| Learnings log | .learnings/LEARNINGS.md |
| Errors log | .learnings/ERRORS.md |
| Feature requests | .learnings/FEATURE_REQUESTS.md |
| Formats reference | references/formats.md |
| Examples | references/examples.md |
| Promotion guide | references/promotion.md |
| Review workflow | references/review.md |

Maintain this table when adding new reference files; keep descriptions short so only the needed file is opened.

## Progressive Loading Rules

- Do not load whole log files by default. Append directly to the correct file; if you must inspect, read only the relevant entry or a small surrounding slice.
- Use grep/search first to find matching IDs or keywords before opening anything large.
- Only load reference files (formats/examples/promotion/review) when you need their content.

## Quick Reference

| Situation | Action | Details |
|-----------|--------|---------|
| Command/operation fails | Log to `.learnings/ERRORS.md` | [Format](references/formats.md#error-entry-format) |
| User corrects you | Log to `.learnings/LEARNINGS.md` | Category: `correction` |
| User wants missing feature | Log to `.learnings/FEATURE_REQUESTS.md` | [Format](references/formats.md#feature-request-format) |
| API/external tool fails | Log to `.learnings/ERRORS.md` | Include integration details |
| Knowledge was outdated | Log to `.learnings/LEARNINGS.md` | Category: `knowledge_gap` |
| Found better approach | Log to `.learnings/LEARNINGS.md` | Category: `best_practice` |
| Similar to existing entry | Link with `See Also` | Consider priority bump |
| Broadly applicable learning | Promote to CLAUDE.md/AGENTS.md | [Guide](references/promotion.md) |

## Setup

Create `.learnings/` directory in project root:

```bash
mkdir -p .learnings
```text

Copy template files from `assets/` or create files with headers:

- `LEARNINGS.md` - Corrections, insights, knowledge gaps
- `ERRORS.md` - Technical failures and bugs
- `FEATURE_REQUESTS.md` - Requested capabilities

Templates available in `assets/` directory.

## Core Workflow

### 1. Log the Entry

When you encounter a triggering situation:

0. **Search first**: `grep -r "keyword" .learnings/` to avoid duplicates; link if related.
1. Determine entry type (learning, error, or feature request)
2. Generate ID: `TYPE-YYYYMMDD-XXX` (e.g., `LRN-20250108-001`)
3. Append entry to appropriate file without loading the full file; if you need context, read only the nearby lines for the target section.
4. Use the format from [references/formats.md](references/formats.md)

**Quick format overview:**

```markdown
## [TYPE-YYYYMMDD-XXX] category_or_name

**Logged**: 2025-01-08T12:00:00Z
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: frontend | backend | infra | tests | docs | config

### Summary
One-line description

### Details / Error / Requested Capability
[Context specific to entry type]

### Suggested Action / Fix / Implementation
What should be done

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- See Also: [related entry IDs]

---
```

See [references/formats.md](references/formats.md) for complete templates and [references/examples.md](references/examples.md) for real examples.

### 2. Resolve When Fixed

Update the entry when addressed:

1. Change `**Status**: pending` → `**Status**: resolved`
2. Add resolution block:

```markdown
### Resolution
- **Resolved**: 2025-01-09T10:00:00Z
- **Commit/PR**: abc123 or #42
- **Notes**: Brief description of fix
```

### 3. Promote If Applicable

When a learning is broadly applicable, promote to permanent documentation:

- **CLAUDE.md**: Project context, conventions, architecture
- **AGENTS.md**: Automation workflows, tool usage patterns

See [references/promotion.md](references/promotion.md) for detailed promotion guidelines.

## Detection Triggers

Log automatically when you notice:

**Corrections** → learning with `correction` category:

- "No, that's not right..."
- "Actually, it should be..."
- "You're wrong about..."

**Feature Requests** → feature request entry:

- "Can you also..."
- "I wish you could..."
- "Is there a way to..."

**Knowledge Gaps** → learning with `knowledge_gap` category:

- User provides information you didn't know
- Documentation you referenced is outdated
- API behavior differs from your understanding

**Errors** → error entry:

- Command returns non-zero exit code
- Exception or stack trace
- Unexpected output or behavior

## Priority Guidelines

| Priority | When to Use |
|----------|-------------|
| `critical` | Blocks core functionality, data loss risk, security issue |
| `high` | Significant impact, affects common workflows, recurring issue |
| `medium` | Moderate impact, workaround exists |
| `low` | Minor inconvenience, edge case, nice-to-have |

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `grep -r "keyword" .learnings/`
2. **Link entries**: Add `**See Also**: ERR-20250110-001` in Metadata
3. **Bump priority** if issue keeps recurring
4. **Consider systemic fix**:
   - Missing documentation → promote to CLAUDE.md
   - Missing automation → promote to AGENTS.md
   - Architectural problem → create tech debt ticket

## Periodic Review

Review `.learnings/` regularly to:

- Resolve fixed items
- Promote applicable learnings
- Link related entries
- Escalate recurring issues

See [references/review.md](references/review.md) for review commands and workflow.

## Best Practices

1. **Log immediately** - context is freshest right after the issue
2. **Be specific** - future agents need to understand quickly
3. **Include reproduction steps** - especially for errors
4. **Link related files** - makes fixes easier
5. **Suggest concrete fixes** - not just "investigate"
6. **Use consistent categories** - enables filtering
7. **Promote aggressively** - if in doubt, add to CLAUDE.md
8. **Review regularly** - stale learnings lose value

## Reference Documentation

- [references/formats.md](references/formats.md) - Complete entry format specifications
- [references/examples.md](references/examples.md) - Real-world examples with all fields
- [references/promotion.md](references/promotion.md) - Guidelines for promoting to project memory
- [references/review.md](references/review.md) - Commands and workflow for periodic review

## Assets

- [assets/LEARNINGS_template.md](assets/LEARNINGS_template.md) - Template file for learnings
- [assets/ERRORS_template.md](assets/ERRORS_template.md) - Template file for errors
- [assets/FEATURE_REQUESTS_template.md](assets/FEATURE_REQUESTS_template.md) - Template file for features
