---
name: knowledge-capture
description: (ePost) Use after completing a task — capture learnings, save patterns, record post-mortems to docs/
user-invocable: false
disable-model-invocation: true

metadata:
  agent-affinity: [epost-debugger, epost-fullstack-developer, epost-researcher, epost-code-reviewer, epost-planner, epost-journal-writer]
  keywords: [capture, learn, persist, record, post-mortem, retrospective]
  platforms: [all]
  triggers: ["capture learnings", "save pattern", "record finding", "what did we learn"]
  connections:
    requires: [knowledge-retrieval]
---

# Knowledge Capture Skill

## Purpose

Post-task workflow for capturing learnings and persisting knowledge to `docs/` directory for team-wide reuse.

## When Active

- After debugging (root cause found)
- After implementation (new pattern used)
- After research (technology decision made)
- After review (convention established)
- After architecture work (ADR needed)
- After documenting system structure
- After writing feature guides

## Capture Workflow

### 1. Identify
**What was learned?**
- Root cause of a bug
- New implementation pattern
- Technology choice rationale
- Coding convention
- Architectural decision
- System structure insight
- Feature deep-dive

### 2. Categorize
**Which category fits?**

See `knowledge-retrieval/references/knowledge-base.md` for schema, categories, and significance thresholds.

### 3. Check Existing
**Already documented?**

```bash
# Search docs index
jq '.entries[] | select(.tags[] | contains("your-topic"))' docs/index.json

# Grep for similar entries
grep -r "your topic" docs/ --include="*.md"
```

If exists: Update existing entry instead of creating duplicate

### 4. Write Entry
**Use appropriate template**

See "Entry Templates" section below for category-specific formats.

### 5. Update Index
**Modify `docs/index.json`**

1. Add entry to `entries` array
2. Include `agentHint` (when should agents check this) and `audience` (["agent", "human"])
3. Update `updatedAt` timestamp
4. Sort by category, then by ID

### 6. Cross-Reference
**Link related entries**

Add IDs to `related` array:
```yaml
related: [ADR-0001, PATTERN-005, FINDING-012]
```

## Entry Templates

### ADR (Architecture Decision)

**Full template in**: `knowledge-retrieval/references/knowledge-base.md`

```markdown
---
id: ADR-NNNN
title: [Active voice decision]
status: proposed
created: YYYY-MM-DD
tags: [architecture, domain]
---

# ADR-NNNN: [Title]

## Context
[Situation, constraints, driving forces]

## Decision
[What we're doing]

## Consequences
**Positive**: [benefits]
**Negative**: [trade-offs]

## Alternatives Considered
**Option A**: [pros, cons, rejection reason]
```

### Architecture (System Structure)

```markdown
---
id: ARCH-NNNN
title: [System aspect being documented]
status: current
created: YYYY-MM-DD
tags: [architecture, system-design]
---

# ARCH-NNNN: [Title]

## Overview
[What this documents]

## Components
[Module/component descriptions and relationships]

## Data Flow
[How data moves through the system]
```

### Pattern (Implementation)

```markdown
---
id: PATTERN-NNNN
title: [Pattern name]
status: active
created: YYYY-MM-DD
tags: [technology, domain]
---

# PATTERN-NNNN: [Title]

## When to Use
[Scenario where pattern applies]

## Implementation
[Code example]

## Caveats
[Limitations, gotchas]
```

### Convention (Coding Standard)

```markdown
---
id: CONV-NNNN
title: [Convention rule]
status: active
created: YYYY-MM-DD
tags: [code-style, language]
---

# CONV-NNNN: [Title]

**Rule**: [Convention statement]

**Good**: [Example following rule]

**Bad**: [Example violating rule]

**Rationale**: [Why this convention]

**Enforcement**: [Linter rule, review checklist]
```

### Feature (Deep-Dive Guide)

```markdown
---
id: FEAT-NNNN
title: [Feature name]
status: current
created: YYYY-MM-DD
tags: [feature, domain]
---

# FEAT-NNNN: [Title]

## Overview
[Feature purpose and scope]

## Usage
[How to use/configure]

## Implementation
[Key implementation details]

## Known Limitations
[Gotchas, edge cases]
```

### Finding (Debug Root Cause)

```markdown
---
id: FINDING-NNNN
title: [Short symptom description]
status: resolved
created: YYYY-MM-DD
tags: [technology, bug-type]
---

# FINDING-NNNN: [Title]

**Symptom**: [Observable behavior]

**Root Cause**: [Underlying issue]

**Resolution**: [Fix applied]

**Prevention**: [How to avoid future occurrences]
```

## Compact Writing Tips

- **Bullets** over paragraphs
- **Tables** for comparisons
- **Code blocks** for examples
- **Bold** for key terms
- **Links** for references
- **Numbers** not words ("3 steps" not "three steps")
- **Active voice** ("use X" not "X should be used")

## Example Capture Session

**Scenario**: Debugged infinite render loop in Dashboard

**1. Identify**
> Learned: Object literal in useEffect deps causes infinite loop

**2. Categorize**
> Category: Finding (debug root cause)

**3. Check Existing**
```bash
grep -r "useEffect.*loop" docs/findings/
# No matches, create new entry
```

**4. Write Entry**
> File: `docs/findings/FINDING-0012-object-literal-useeffect-loop.md`

```markdown
---
id: FINDING-0012
title: Object literal in useEffect dependency causes infinite loop
status: resolved
created: 2026-02-08
updated: 2026-02-08
tags: [react, hooks, performance, debugging]
related: [PATTERN-005]
---

# FINDING-0012: Object literal in useEffect dependency causes infinite loop

**Symptom**: Dashboard component re-renders continuously, browser freezes

**Root Cause**: useEffect dependency array contains object literal `{ id: userId }`, creating new reference each render

**Resolution**:
1. Extract to useMemo: `const deps = useMemo(() => ({ id: userId }), [userId])`
2. Or use primitive: `useEffect(() => {...}, [userId])`

**Prevention**:
- Enable ESLint `react-hooks/exhaustive-deps`
- Prefer primitive dependencies
- Use React DevTools Profiler to catch render loops
```

**5. Update Index**
```json
{
  "id": "FINDING-0012",
  "title": "Object literal in useEffect dependency causes infinite loop",
  "category": "finding",
  "status": "resolved",
  "audience": ["agent", "human"],
  "path": "docs/findings/FINDING-0012-object-literal-useeffect-loop.md",
  "tags": ["react", "hooks", "performance", "debugging"],
  "agentHint": "check when debugging infinite re-renders or useEffect dependency issues",
  "related": ["PATTERN-005"]
}
```

**6. Cross-Reference**
> Link to `PATTERN-005` (React hooks best practices)

## Integration with Other Skills

### Post-Debugging
```
debugging → find root cause → knowledge-capture → create FINDING
```

### Post-Implementation
```
implementer → discover pattern → knowledge-capture → create PATTERN
```

### Post-Research
```
research → make decision → knowledge-capture → create ADR
```

### Post-Review
```
code-review → identify convention → knowledge-capture → create CONV
```

### Post-Architecture
```
architect → make decision → knowledge-capture → create ADR
architect → document system → knowledge-capture → create ARCH
```

## File Operations

### Create Knowledge Entry

```bash
# 1. Determine next ID
jq -r '[.entries[] | select(.category == "finding") | .id] | sort | last' docs/index.json

# 2. Create file in appropriate directory
# docs/findings/FINDING-NNNN-title.md

# 3. Update docs/index.json (add entry with agentHint + audience)
```

### Update Existing Entry

```bash
# 1. Find entry
ENTRY_PATH=$(jq -r '.entries[] | select(.id == "FINDING-0012") | .path' docs/index.json)

# 2. Edit file at $ENTRY_PATH

# 3. Update index entry fields + updatedAt timestamp
```

## Quality Checklist

Before finalizing entry:

- [ ] Category appropriate for learning type
- [ ] ID follows `PREFIX-NNNN` format
- [ ] Frontmatter complete (no missing fields)
- [ ] Title descriptive (5-10 words)
- [ ] Tags relevant and specific
- [ ] Content concise (use bullets, code blocks)
- [ ] Cross-references added to `related`
- [ ] Index updated (entry + agentHint + audience)
- [ ] File saved to correct category directory

## Related Skills

- `knowledge-retrieval` — Knowledge system structure, conventions, and search
- `debug` — Debugging methodology (source of findings)
- `code-review` — Review process (source of conventions)
- `research` — Research methodology (source of decisions)
- `auto-improvement` — Auto-triggered when significance threshold met on session Stop

## References

- `knowledge-retrieval/references/knowledge-base.md` — Knowledge system overview, ADR templates, capture guidelines
