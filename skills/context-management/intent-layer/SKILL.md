---
name: intent-layer
description: >
  Set up hierarchical Intent Layer (AGENTS.md files) for codebases.
  Use when initializing a new project, adding context infrastructure to an existing repo,
  user asks to set up AGENTS.md, add intent layer, make agents understand the codebase,
  or scaffolding AI-friendly project documentation.
---

# Intent Layer

Hierarchical AGENTS.md infrastructure so agents navigate codebases like senior engineers.

## Core Principle

**Only ONE root context file.** CLAUDE.md and AGENTS.md should NOT coexist at project root. Child AGENTS.md in subdirectories are encouraged for complex subsystems.

## Workflow

```
1. Detect state
   scripts/detect_state.sh /path/to/project
   → Returns: none | partial | complete

2. Route
   none/partial → Initial setup (steps 3-5)
   complete     → Maintenance (step 6)

3. Measure [gate - show table first]
   scripts/analyze_structure.sh /path/to/project
   scripts/estimate_tokens.sh /path/to/each/source/dir

4. Decide
   No root file  → Ask: CLAUDE.md or AGENTS.md?
   Has root file → Add Intent Layer section + child nodes if needed

5. Execute
   Use references/templates.md for structure
   Use references/node-examples.md for real-world patterns
   Validate: one root, READ-FIRST directive, <4k tokens per node

6. Maintenance mode (when state=complete)
   Ask user:
   a) Audit nodes     → Use references/capture-protocol.md for SME questions
   b) Find candidates → Re-measure tokens, suggest new nodes
   c) Both
```

## When to Create Child Nodes

| Signal | Action |
|--------|--------|
| >20k tokens in directory | Create AGENTS.md |
| Responsibility shift | Create AGENTS.md |
| Hidden contracts/invariants | Document in nearest ancestor |
| Cross-cutting concern | Place at LCA |

Do NOT create for: every directory, simple utilities, test folders (unless complex).

## Capture Questions

When documenting existing code, ask:
1. What does this area own? What's out of scope?
2. What invariants must never be violated?
3. What repeatedly confuses new engineers?
4. What patterns should always be followed?

## Resources

**Scripts:**
- `scripts/detect_state.sh` - Check Intent Layer state (none/partial/complete)
- `scripts/analyze_structure.sh` - Find semantic boundaries
- `scripts/estimate_tokens.sh` - Measure directory complexity

**References:**
- `references/templates.md` - Root and child node templates
- `references/node-examples.md` - Real-world examples
- `references/capture-protocol.md` - SME interview protocol
