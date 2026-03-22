---
name: compound-docs
description: Document solved problems for knowledge persistence
---

# Compound Documentation Skill

Manages solution documentation in `docs/solutions/` for knowledge persistence across sessions.

## Overview

When you solve a problem, document it so the solution can be found and reused later.

## What do you want to do?

1. **Document a solution** → Use `/compound` workflow
2. **Find existing solutions** → See "Searching Solutions" below
3. **Promote to pattern** → See "Pattern Promotion" below
4. **Validate schema** → See "YAML Validation" below

---

## Instrumentation

```bash
# Log usage when using this skill
Call MCP `call_tool_logger_manager` { action: "logSkill", name: "compound-docs", outcome: "manual" }
```

## Searching Solutions

```bash
# Search by keyword
grep -r "keyword" docs/solutions/

# Search by tag
grep -l "tags:.*performance" docs/solutions/**/*.md

# Search by problem type
ls docs/solutions/performance-issues/
```

## Pattern Promotion

When an issue occurs 3+ times:

1. Search for similar solutions:
   ```bash
   grep -r "similar terms" docs/solutions/
   ```

2. Add to critical patterns:
   ```bash
   # Edit docs/solutions/patterns/critical-patterns.md
   ```

3. Format:
   ```markdown
   ### Pattern #{N}: {Name}
   
   **Problem:** {What goes wrong}
   
   **❌ WRONG:**
   ```code
   {incorrect}
   ```
   
   **✅ CORRECT:**
   ```code
   {correct}
   ```
   ```

## YAML Validation

All solutions must have valid frontmatter:

```yaml
---
date: "YYYY-MM-DD"
problem_type: "{from schema.yaml}"
severity: "critical|high|medium|low"
symptoms:
  - "symptom 1"
root_cause: "{from schema.yaml}"
tags:
  - tag1
---
```

See `docs/solutions/schema.yaml` for valid enum values.

## Documenting Failures & Learnings

When documenting solutions, capture the full journey:

### What to Include
- ✅ Failed attempts with explanations
- ✅ Incorrect assumptions and corrections
- ✅ Key insights from mistakes
- ✅ Course corrections and why
- ✅ Time investment (helps prioritize future similar issues)

### Example Pattern
```markdown
## Investigation Steps

| Attempt | Hypothesis | Result |
|---------|------------|--------|
| 1. Check API logs | API might be timing out | ❌ No timeouts found |
| 2. Review database queries | N+1 query suspected | ❌ Queries were optimized |
| 3. Check cache invalidation | Cache might be stale | ✅ Found cache not clearing |

## Lessons Learned

### Mistakes Made
- **Assumption:** Assumed the API was the bottleneck
  - **Why wrong:** Didn't check cache layer first
  - **Correction:** Should always check cache before API

### Key Breakthrough
- **Insight:** Realized cache invalidation logic was only running on UPDATE, not DELETE
  - **Impact:** Led directly to the solution
```

> [!TIP]
> **Document the journey, not just the destination.** Future readers learn from understanding WHY failed approaches didn't work.

## References

- Schema: `docs/solutions/schema.yaml`
- Template: `docs/solutions/templates/solution-template.md`
- Patterns: `docs/solutions/patterns/critical-patterns.md`
