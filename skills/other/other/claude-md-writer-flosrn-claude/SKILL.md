---
name: claude-md-writer
description: Use when analyzing a codebase directory, module, component, or architectural layer to generate a localized CLAUDE.md. Triggers on "write CLAUDE.md for", "document this module", "analyze for CLAUDE.md", "create context for this directory", "CLAUDE.md localisé", "documenter ce module".
---

# Codebase Analysis for Localized CLAUDE.md

Systematic methodology to analyze a codebase area and produce a CLAUDE.md that helps AI agents understand and work effectively with that specific code.

**Core insight:** AI agents can read code. They need synthetic understanding: WHY the code exists, HOW it fits together, and WHAT conventions to follow. Don't document what's obvious from reading files.

## When to Use

- Adding CLAUDE.md to a module, package, or directory
- Onboarding AI agents to a complex area of a codebase
- Documenting architectural boundaries in a monorepo
- Creating context for a component library, API layer, or service

**Don't use for:**
- Root-level project CLAUDE.md (use `claude-md-management:claude-md-improver`)
- Simple directories with 1-3 files (not worth the token cost)
- Test directories (conventions belong in root CLAUDE.md)

## How Localized CLAUDE.md Works

Claude Code loads subdirectory CLAUDE.md files **on-demand** - only when reading or writing files in that directory. This means:
- They don't bloat the context window for unrelated work
- They provide focused, relevant context at the right moment
- Keep them **under 150 lines** - they compete with conversation history

## Analysis Methodology: SMED

Four phases, each with specific exploration actions:

### Phase 1: SCAN - Structural Overview

**Goal:** Understand the shape and size of the target area.

```bash
# Run these commands on the target directory
tree -L 2 <target>
wc -l <target>/**/*.{ts,tsx,js,jsx,py,go,rs} 2>/dev/null | tail -1
```

**Extract:**
- Total files and lines of code (complexity indicator)
- Directory structure and organization pattern (flat, nested, feature-based, layer-based)
- File naming patterns (PascalCase components, kebab-case utils, etc.)
- Entry points (index files, barrel exports, main modules)

### Phase 2: MAP - Architecture & Relationships

**Goal:** Understand how this area connects to the rest of the system.

**Actions:**
1. Read entry points / barrel files to see public API surface
2. Search for imports FROM this directory (who depends on us?)
3. Search for imports INTO this directory (who do we depend on?)
4. Identify the architectural role: UI layer? Data layer? Service? Shared lib?

```bash
# Find who imports from this directory
grep -r "from.*<dirname>" --include="*.ts" --include="*.tsx" -l
# Find external dependencies used here
grep -r "from " <target> --include="*.ts" -h | sort -u | head -30
```

**Extract:**
- Upstream dependencies (what this code needs)
- Downstream consumers (what needs this code)
- Architectural boundaries (what should NOT cross in/out)
- Shared state or communication patterns (context, events, stores)

### Phase 3: EXTRACT - Conventions & Patterns

**Goal:** Identify the implicit rules developers follow here.

**Actions:**
1. Read 3-5 representative files (most recent, most imported, largest)
2. Look for repeated patterns: error handling, data fetching, state management
3. Check for local configuration (tsconfig, eslint overrides, package.json)
4. Look for existing README or documentation

**Extract:**
- Naming conventions specific to this area
- Code patterns that repeat (HOCs, hooks, factory functions, etc.)
- Error handling approach
- Testing patterns (co-located tests? separate directory?)
- Configuration or environment specifics

### Phase 4: DISTILL - Key Decisions

**Goal:** Understand WHY things are this way, not just what they are.

**Actions:**
1. Check git log for major architectural changes: `git log --oneline --since="1 year ago" -- <target> | head -20`
2. Look for ADR files, decision comments, or TODO/FIXME/HACK annotations
3. Identify non-obvious choices (Why this library? Why this pattern? Why this structure?)

**Extract:**
- Architectural decisions and their rationale
- Known technical debt or planned migrations
- Constraints that aren't obvious from code alone

## Output Template

Generate the CLAUDE.md using ONLY the sections relevant to the target. Skip sections that add no value. Every line must justify its token cost.

```markdown
# [Directory Name]

## Purpose
[1-2 sentences: WHY this exists. What problem does it solve? What role does it play in the system?]

## Structure
[tree output of the directory - gives instant spatial orientation. Then annotate ONLY non-obvious roles.]

## Key Patterns
[Code conventions specific to THIS directory. Only patterns an AI agent wouldn't infer from reading 2-3 files.]

## Dependencies
[Upstream: what this needs. Downstream: what needs this. Boundaries: what should NOT be imported.]

## Anti-Patterns
[What NOT to do here. Common mistakes. Things that look right but aren't.]

## Working Here
[Commands to test/build/lint this specific area. Verification criteria.]

## Decisions
[Non-obvious architectural choices and WHY. Condensed ADR format.]
```

### Section Guidelines

| Section | Include When | Skip When |
|---------|-------------|-----------|
| Purpose | Always | Never |
| Structure | >5 files | 3 files or fewer (obvious at a glance) |
| Key Patterns | Local conventions differ from project root | Same patterns as root CLAUDE.md |
| Dependencies | Complex dependency graph or boundaries | Self-contained module |
| Anti-Patterns | Known pitfalls exist | No known traps |
| Working Here | Module-specific commands exist | Same as root commands |
| Decisions | Non-obvious choices were made | Everything is standard/obvious |

## Quality Checklist

Before finalizing the CLAUDE.md:

- [ ] **Under 150 lines** - If longer, you're documenting WHAT instead of WHY
- [ ] **No code documentation** - Don't restate what functions do (AI reads code)
- [ ] **No generic advice** - "Write clean code" is noise. Be specific.
- [ ] **Actionable anti-patterns** - Each one prevents a real mistake
- [ ] **Testable verification** - "Run X to verify" not "make sure it works"
- [ ] **No duplication with root** - Check parent CLAUDE.md, don't repeat

## Common Mistakes

| Mistake | Why It's Bad | Fix |
|---------|-------------|-----|
| Describing every file's purpose | Token waste, AI reads code | Use tree for structure, annotate only non-obvious roles |
| Restating function signatures | AI reads code better than docs | Document intent and constraints |
| Copy-pasting root conventions | Duplicated context, double token cost | Reference root: "Follow root conventions" |
| Writing for humans not agents | Different information needs | Focus on WHY, boundaries, anti-patterns |
| Including generated/vendored files | Noise | Explicitly exclude from analysis |
| Making CLAUDE.md too long | Gets ignored (priority saturation) | Ruthlessly cut to <150 lines |

## Example: Good vs Bad

**Bad** (describes what AI sees by reading files):
```markdown
## Files
- `UserCard.tsx` - A React component that displays user information
- `UserCard.test.tsx` - Tests for UserCard
- `types.ts` - TypeScript types for user data
- `utils.ts` - Utility functions
```

**Good** (tree for orientation + synthetic understanding):
```markdown
## Purpose
User profile components. Shared across dashboard, admin panel, and public profiles.
Must render server-side (RSC) - no client hooks in top-level components.

## Structure
├── components/
│   ├── user-card.tsx        # Orchestrator - manages search/display states
│   ├── user-avatar.tsx
│   └── rating-badge.tsx
├── lib/
│   ├── types.ts
│   └── utils.ts
└── index.ts                 # Public API - only export what consumers need

## Anti-Patterns
- Don't add `"use client"` to card components - they must stay RSC-compatible
- Don't import from `@/features/admin` - these are shared components
- Don't add user-specific data fetching here - consumers pass data via props
```

**Key distinction:** Tree gives spatial orientation (5 seconds to grasp structure). File descriptions restate what AI reads in the code. Annotate only non-obvious roles in the tree.

## Parallel Analysis with Subagents

For large directories, dispatch parallel Explore agents:

1. **Structure agent** - SCAN phase (tree, file counts, organization)
2. **Dependencies agent** - MAP phase (imports analysis, consumer search)
3. **Patterns agent** - EXTRACT phase (read representative files, identify conventions)

Synthesize their findings before DISTILL phase, which requires judgment.
