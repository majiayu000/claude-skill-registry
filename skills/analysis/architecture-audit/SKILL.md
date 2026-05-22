---
name: architecture-audit
description: Perform comprehensive software architecture audits to identify improvements for robustness, changeability, and testability. Use when asked to audit, review, or analyze a codebase's architecture, or when asked to suggest structural improvements. Triggers include "architecture audit", "audit the codebase", "review architecture", "architectural analysis", "code structure review", or explicit "/architecture-audit".
---

# Architecture Audit

Analyze a codebase's architecture and provide actionable recommendations to improve robustness, changeability, and testability.

## Audit Process

1. **Understand scope** - Identify target directories/modules
2. **Map structure** - Explore directory layout and key files
3. **Analyze each dimension** - Work through checklist systematically
4. **Synthesize findings** - Identify patterns and root causes
5. **Generate report** - Deliver prioritized recommendations

## Step 1: Scope & Context

Determine audit scope:
- Full codebase or specific modules?
- Any known pain points to focus on?
- Primary language(s) and frameworks?

Use Glob and Grep to understand:
```
# Directory structure
ls -la, tree (if available)

# Key configuration files
package.json, requirements.txt, go.mod, Cargo.toml, etc.

# Entry points
main.*, index.*, app.*
```

## Step 2: Structure Mapping

Build mental model of the codebase:
- Identify top-level organization (by feature, layer, or domain?)
- Map module boundaries and dependencies
- Note test location and structure
- Identify configuration management approach

## Step 3: Systematic Analysis

Work through each dimension. Load [references/audit-checklist.md](references/audit-checklist.md) for detailed patterns to assess.

**Key dimensions:**
1. Code Organization
2. Dependency Management
3. Coupling & Cohesion
4. Testability
5. Error Handling
6. Architectural Patterns

For each dimension, assess and note:
- Current state (what exists)
- Issues found (specific examples with file:line)
- Severity (critical/weak/adequate/strong)

## Step 4: Synthesis

Look for patterns across dimensions:
- Root causes behind multiple symptoms
- Quick wins (high impact, low effort)
- Strategic improvements (require planning)

## Step 5: Report Generation

Use this report structure:

```markdown
# Architecture Audit Report

## Executive Summary
[2-3 sentences: overall health assessment and top priorities]

## Scope
[What was audited, any limitations]

## Findings by Category

### Code Organization
**Assessment:** [Strong/Adequate/Weak/Critical]
[Key findings with specific file references]

### Dependency Management
**Assessment:** [Strong/Adequate/Weak/Critical]
[Key findings with specific file references]

### Coupling & Cohesion
**Assessment:** [Strong/Adequate/Weak/Critical]
[Key findings with specific file references]

### Testability
**Assessment:** [Strong/Adequate/Weak/Critical]
[Key findings with specific file references]

### Error Handling
**Assessment:** [Strong/Adequate/Weak/Critical]
[Key findings with specific file references]

### Architectural Patterns
**Assessment:** [Strong/Adequate/Weak/Critical]
[Key findings with specific file references]

## Prioritized Recommendations

### Immediate (Quick Wins)
1. [Specific action] - [Why it matters]
2. ...

### Short-term (1-2 sprints)
1. [Specific action] - [Why it matters]
2. ...

### Long-term (Strategic)
1. [Specific action] - [Why it matters]
2. ...

## Summary Table

| Category | Assessment | Priority Issues |
|----------|------------|-----------------|
| Code Organization | ... | ... |
| Dependency Management | ... | ... |
| Coupling & Cohesion | ... | ... |
| Testability | ... | ... |
| Error Handling | ... | ... |
| Architectural Patterns | ... | ... |
```

## Key Principles

- **Be specific** - Reference actual files and line numbers
- **Prioritize impact** - Focus on changes that matter most
- **Stay practical** - Recommendations should be actionable
- **Consider context** - Small project != enterprise system
