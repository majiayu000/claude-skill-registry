---
name: multi-model-discovery
description: Use Gemini to find existing solutions before building from scratch. Leverages Google Search grounding to discover code examples, libraries, and best practices to avoid reinventing the wheel.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, Task, TodoWrite
x-version: 1.0.0
x-category: platforms
x-tags:
  - gemini
  - research
  - discovery
  - multi-model
  - code-reuse
x-author: context-cascade
x-verix-description: |
  [assert|neutral] multi-model-discovery skill for finding existing solutions [ground:given] [conf:0.95] [state:confirmed]
---

<!-- S0 META-IDENTITY -->

# Multi-Model Discovery Skill



---

## LIBRARY-FIRST PROTOCOL (MANDATORY)

**Before writing ANY code, you MUST check:**

### Step 1: Library Catalog
- Location: `.claude/library/catalog.json`
- If match >70%: REUSE or ADAPT

### Step 2: Patterns Guide
- Location: `.claude/docs/inventories/LIBRARY-PATTERNS-GUIDE.md`
- If pattern exists: FOLLOW documented approach

### Step 3: Existing Projects
- Location: `D:\Projects\*`
- If found: EXTRACT and adapt

### Decision Matrix
| Match | Action |
|-------|--------|
| Library >90% | REUSE directly |
| Library 70-90% | ADAPT minimally |
| Pattern exists | FOLLOW pattern |
| In project | EXTRACT |
| No match | BUILD (add to library after) |

---

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

## Purpose

Use Gemini CLI's Google Search grounding capability to discover existing solutions before implementing from scratch. This skill embodies the principle: **"Don't reinvent the wheel."**

## When to Use This Skill

- Before implementing a new feature (find existing solutions first)
- When researching best practices for a technology
- When looking for code examples or patterns
- When evaluating libraries or frameworks
- When unsure if a problem has already been solved
- Before writing boilerplate code that might exist

## When NOT to Use This Skill

- For implementation tasks (use codex-iterative-fix instead)
- When you already know the solution exists in the codebase
- For debugging existing code (use smart-bug-fix)
- For codebase analysis (use gemini-codebase-onboard)

## Workflow

### Phase 1: Research Query Formulation

1. Analyze the implementation goal
2. Formulate search queries for:
   - Existing libraries/packages
   - Code examples on GitHub
   - Best practice guides
   - Common patterns

### Phase 2: Gemini Discovery Execution

```bash
# Execute via delegate.sh wrapper
./scripts/multi-model/delegate.sh gemini "Find existing solutions for: {goal}"

# Or via gemini-yolo.sh
./scripts/multi-model/gemini-yolo.sh "How do others implement {feature}? Find code examples and libraries." task-id research
```

### Phase 3: Results Synthesis

1. Claude synthesizes Gemini's findings
2. Evaluate options:
   - Use existing library
   - Adapt existing pattern
   - Build from scratch (last resort)
3. Document decision rationale

## Success Criteria

- Existing solution found and evaluated
- Build vs buy decision made with evidence
- Time saved by avoiding reinvention
- Quality improved by using proven patterns

## Example Usage

### Example 1: Auth Implementation

```text
User: "Implement user authentication"

Discovery Process:
1. Gemini search: "What are best practices for auth in Node.js?"
2. Gemini search: "Find existing auth libraries: passport, next-auth, lucia"
3. Gemini search: "Code examples for JWT authentication Node.js"

Output:
- Recommended: next-auth (well-maintained, 40k+ stars)
- Alternative: lucia-auth (newer, type-safe)
- Pattern found: middleware-based validation
```

### Example 2: PDF Generation

```text
User: "Generate PDF reports from data"

Discovery Process:
1. Gemini search: "PDF generation libraries JavaScript 2024"
2. Gemini search: "Compare pdfkit vs puppeteer vs react-pdf"
3. Gemini search: "Production PDF generation best practices"

Output:
- Simple PDFs: pdfkit (lightweight)
- Complex layouts: puppeteer (HTML to PDF)
- React apps: react-pdf
```

## Integration with Meta-Loop

```
META-LOOP PROPOSE PHASE:
    |
    +---> multi-model-discovery
    |         |
    |         +---> Gemini: Find existing solutions
    |         +---> Claude: Evaluate options
    |         +---> Decision: Build vs Adapt vs Use
    |
    +---> Continue to IMPLEMENT phase
```

## Memory Integration

Results stored at:
- Key: `multi-model/discovery/{project}/{task_id}`
- Tags: WHO=multi-model-discovery, WHY=avoid-reinvention

## Invocation Pattern

```bash
# Via router (automatic detection)
./scripts/multi-model/multi-model-router.sh "Find existing solutions for X"

# Direct Gemini call
bash -lc "gemini 'How do others implement X? Find code examples and libraries.'"
```

## Related Skills

- `gemini-research`: General research with search grounding
- `gemini-megacontext`: Full codebase analysis
- `codex-iterative-fix`: After discovery, for implementation
- `literature-synthesis`: Academic research synthesis

<!-- S4 SUCCESS CRITERIA -->

## Verification Checklist

- [ ] Gemini search executed with clear queries
- [ ] Multiple solutions discovered and compared
- [ ] Build vs buy decision documented
- [ ] Memory-MCP updated with findings
- [ ] Decision rationale captured

<!-- PROMISE -->

[commit|confident] <promise>MULTI_MODEL_DISCOVERY_COMPLETE</promise>
