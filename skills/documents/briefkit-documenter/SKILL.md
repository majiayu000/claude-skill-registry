---
name: briefkit-documenter
description: Create interface-first documentation using BRIEF system v3. Generate BRIEF.md files with inputs/outputs contracts, validate against spec, convert PRDs/specs to BRIEFs, and support multi-surface applications (Web/Mobile/API). Use when creating module documentation, establishing documentation standards, or documenting legacy code.
allowed-tools: [Read, Write, Edit, Grep, Glob]
version: 1.0.0
---

# Briefkit Documenter

## Purpose

Generate and maintain BRIEF.md files for module documentation. Creates agent-friendly, human-readable docs that prioritize interfaces over implementation.

## When to Use

- Creating module documentation (new or existing code)
- Converting PRDs/specs to BRIEFs
- Validating existing documentation
- Setting up repository-wide documentation standards
- Multi-surface applications (Web/Mobile/API)

## Quick Start

### Generate a BRIEF
```
1. Analyze module code and boundaries
2. Generate BRIEF.md with all required sections
3. Mark uncertain content with INFERRED
4. Validate against rules
5. Request human review
```

### Required Sections
Every BRIEF must have these sections in order:
1. `# <Module> — BRIEF` (title)
2. Purpose & Boundary
3. Interface Contract (Inputs → Outputs)
4. Dependencies & Integration Points
5. Work State (Planned / Doing / Done)
6. SPEC_SNAPSHOT (YYYY-MM-DD)
7. Decisions & Rationale
8. Local Reference Index (if submodules)
9. Answer Pack (YAML)

See SPECIFICATION.md for complete specifications.

### Validation
```
Tier-1 Blockers: Missing BRIEF, Interface Contract, INFERRED markers, invalid YAML, >200 lines
Tier-2 Warnings: Missing/stale snapshot, broken links, missing Answer Pack
```
Full rules in references/SPECIFICATION.md

## Resources

### Core References
- `PATTERNS.md` - Practical patterns and templates
- `EXAMPLES.md` - 8 complete real-world examples
- `PHILOSOPHY.md` - Philosophy and methodology
- `SPECIFICATION.md` - Authoritative v3 specification

## Example Workflows

### 1. New Module Documentation
```
User: "Document the auth module"
→ Analyze code → Extract interfaces → Generate BRIEF → Validate → Deliver
```

### 2. Legacy Code Documentation
```
User: "Document this undocumented module"
→ Infer from code → Heavy INFERRED markers → Generate BRIEF → Request review
```

More workflows in PATTERNS.md

## Quick Reference Searches

Find content quickly using grep:

```bash
# In SPECIFICATION.md
grep "^### [0-9]\." references/SPECIFICATION.md    # List numbered sections
grep "Required.*:" references/SPECIFICATION.md     # Find required fields
grep "Tier-[12]" references/SPECIFICATION.md       # Find validation tiers

# In PATTERNS.md
grep "^## .* Pattern$" references/PATTERNS.md      # List all patterns
grep "DO\|DON'T" references/PATTERNS.md           # Find do/don't lists

# In EXAMPLES.md
grep "^### Example [0-9]:" references/EXAMPLES.md  # List inline examples (2 quick-start)
ls references/examples/*.md                         # List specialized examples (6 files)
grep "Multi-Surface" references/EXAMPLES.md        # Find multi-platform examples

# In PHILOSOPHY.md
grep "Interface-First" references/PHILOSOPHY.md    # Find interface-first mentions
grep "^### Why" references/PHILOSOPHY.md          # Find rationale sections

# Universal search
grep -r "validation" references/                   # Find validation info
grep -r "INFERRED" references/                    # Find INFERRED marker guidance
```

## Philosophy

Interface-first: Document WHAT before HOW. See PHILOSOPHY.md for deep dive.

## Next Steps

1. Try: Create a BRIEF for an existing module
2. Validate: Check existing BRIEFs
3. Learn: Read EXAMPLES.md for patterns
4. Deep dive: Explore PHILOSOPHY.md

---
Version: 1.0.0 | Based on: BRIEF System v3
