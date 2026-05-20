---
name: vibe-structured-output
description: Enforces structured output format for analyses, reports, and recommendations — Executive Summary, Detailed Analysis, Next Steps, Metrics. Prevents wall-of-text responses.
user-invocable: true
---

# vibe-structured-output

Structure aids comprehension. Every analysis should be scannable before it's readable.

## When to Use This Skill

- Producing any analysis, report, or recommendation
- When the output will be shared with others
- When multiple stakeholders with different needs will read the output
- When the response would otherwise be a wall of text

## When NOT to Use This Skill

- Simple yes/no answers
- Code-only responses
- Casual conversation
- When the user asks for a specific format

## The Format

Every structured output has 4 sections:

### 1. Executive Summary (5-10 lines)
- **Type**: [Analysis | Report | Recommendation | Audit]
- **Confidence**: High / Medium / Low
- **Key Finding**: [One sentence]
- **Recommended Actions**: [Count]
- **Urgency**: Immediate / High / Medium / Low

### 2. Detailed Analysis
Tables, sections, evidence. This is the meat.
- Use tables for comparisons
- Use bullet lists for findings
- Reference specific files/lines
- Include data, not opinions

### 3. Next Steps
Numbered, actionable items:
1. [Action] — [Owner, if known] — [Priority]
2. [Action] — [Owner, if known] — [Priority]

### 4. Metrics (If Applicable)
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| [name] | [value] | [value] | ✓/⚠/✗ |

## Anti-Patterns

- Starting with implementation details instead of summary
- Mixing analysis with recommendations
- Opinions without evidence
- Actions without owners or priorities
- Metrics without targets
