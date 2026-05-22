---
name: context:doc-analyze
description: Analyze documentation needs with tiered approach. Use when user asks to "analyze docs", "find missing docs", "plan documentation", "what docs do I need", or needs to understand documentation coverage for a domain or feature.
---

# Doc Analyze Skill

Tiered documentation analysis for understanding what atomic docs exist, identifying gaps, and planning new documentation.

## Auto-Triggers

This skill should be invoked when the user:
- Asks "what docs do I need for X"
- Asks "analyze docs for X"
- Asks "find missing docs"
- Asks "plan documentation for X"
- Mentions needing to understand documentation coverage
- Wants to audit docs for a domain/feature

## Execution Instructions

When this skill is invoked, check the ARGUMENTS provided:

### If argument is a domain or topic:

**MANDATORY FIRST STEP:** Use the Read tool to read `context/workflows/ralph/components/doc-analysis.md` (relative to project root). DO NOT proceed without reading this file first - it contains the full tiered analysis workflow.

1. Determine the tier based on flags:
   - No flags → T1 + T2 (lookup + gap creation if needed)
   - `--deep` → T3 (full Opus parallel analysis)
   - `--gap-analysis` → T3 with 5th gap explorer agent

2. For T1 (always):
   - Read `context/README.md` to understand index structure
   - Extract keywords from the topic/domain
   - Search for matching blocks, foundations, stacks
   - Report matches and missing docs

3. For T2 (when gaps found):
   - Evaluate if gaps are critical (not well-known libs)
   - For critical gaps, spawn atomic-doc-creator agent
   - Report created docs

4. For T3 (`--deep`):
   - Launch 4 parallel Opus agents as described in the workflow
   - Synthesize findings
   - Present convergence, divergence, and recommended plan

### If no argument:

Show the usage documentation below.

---

## Usage

```
/doc-analyze <domain> [--deep] [--gap-analysis]
```

## Arguments

| Argument | Description |
|----------|-------------|
| `<domain>` | The domain, topic, or feature to analyze (e.g., "frontend", "auth", "testing") |
| `--deep` | Use Tier 3 (Opus parallel analysis) for comprehensive coverage |
| `--gap-analysis` | Include 5th gap explorer agent in T3 analysis |

## Examples

```bash
# Quick lookup - what docs exist for auth?
/doc-analyze auth

# Find docs for frontend patterns
/doc-analyze frontend

# Deep analysis for a new domain
/doc-analyze frontend --deep

# Full audit with gap explorer
/doc-analyze api --deep --gap-analysis
```

## Tiers

| Tier | Model | What It Does | When Used |
|------|-------|--------------|-----------|
| T1 | Haiku | Fast index lookup | Always |
| T2 | Sonnet | Create missing docs | When T1 finds critical gaps |
| T3 | Opus | Parallel 4-agent analysis | With `--deep` flag |

## Output

### T1 + T2 Output

```markdown
## Doc Analysis: <domain>

### Found
- context/blocks/construct/react.md
- context/foundations/test/test-component-vitest-rtl.md

### Created (T2)
- context/blocks/patterns/form-validation.md [REVIEW]

### Still Missing
- SSR patterns (no existing doc, not created)
```

### T3 Output

```markdown
## Doc Analysis: <domain>

### Convergence
- All agents agree: need X, Y, Z docs

### Divergent Insights
- Agent 1 (Stack→Down): Found need for bundler config docs
- Agent 3 (Problem→Down): Identified SSR gap

### Open Questions
- Which state management approach?
- SSR vs CSR decision?

### Recommended Plan
1. Create bundler config foundation
2. Add SSR decision doc to docs/
3. ...
```

## Related

- @context/workflows/ralph/components/doc-analysis.md - Full component docs
- @context/blocks/docs/atomic-documentation.md - Atomic doc structure
- @.claude/agents/atomic-doc-creator.md - Gap creation agent
