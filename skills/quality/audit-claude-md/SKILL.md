# audit-claude-md Skill

Audit and refactor CLAUDE.md files to eliminate bloat, enforce context engineering best practices, and create folder-level CLAUDE.md files for complex domain-specific instructions.

## Quick Start

Run the audit command to analyze all CLAUDE.md files:

```bash
/audit-claude-md
```

Or audit a specific file:

```bash
/audit-claude-md path/to/CLAUDE.md
```

## What This Audits

### Line Count Analysis

| File Type | Warning | Maximum |
|-----------|---------|---------|
| Feature CLAUDE.md | 100 lines | 200 lines |
| Project CLAUDE.md | 150 lines | 300 lines |
| Root CLAUDE.md | 300 lines | 400 lines |

### Vague Language Detection

Prohibited patterns that degrade LLM instruction-following:
- "should probably" → Use MUST, SHOULD, or MAY
- "might want to" → Be specific or omit
- "you could" → Use imperative voice
- "consider maybe" → Decide and state clearly
- "it's good to" → Use SHOULD or MUST
- "try to" → State the requirement directly

### Required Sections

**Root CLAUDE.md** must have:
- `## WHAT This Is` - Purpose and scope
- `## WHY This Approach` - Rationale
- `## HOW To Use It` - Instructions

### Quality Scoring

| Component | Weight |
|-----------|--------|
| Line count | 30% |
| Vague language | 25% |
| Strong modals (MUST/SHOULD/NEVER) | 15% |
| Required sections | 15% |
| External references | 10% |
| Freshness | 5% |

### Grades

- **A (80-100)**: Excellent - Follows best practices
- **B (60-79)**: Good - Minor improvements needed
- **C (40-59)**: Needs Improvement - Significant issues
- **F (0-39)**: Critical - Major refactoring required

## Refactoring Recommendations

### If Line Count Exceeds Maximum

1. Extract deep-dive content to `docs/references/`
2. Keep only essential instructions in CLAUDE.md
3. Add links to reference documentation
4. Use progressive disclosure pattern

### If High Vague Language Count

Replace uncertain language with strong modals:
- "should probably" → "MUST" or "SHOULD"
- "might want to" → "Consider" or omit
- "you could" → Direct imperative

### If Missing WHAT/WHY/HOW

Add the framework structure:

```markdown
## WHAT This Is
Brief description of purpose and scope.

## WHY This Approach
- Reason 1
- Reason 2

## HOW To Use It
### Quick Start
...
```

## Scripts

- `.spec-flow/scripts/bash/audit-claude-md.sh` - Comprehensive audit
- `.claude/hooks/claude-md-validator.sh` - Pre-edit validation hook

## Configuration

Rules defined in `.spec-flow/config/claude-md-rules.yaml`
