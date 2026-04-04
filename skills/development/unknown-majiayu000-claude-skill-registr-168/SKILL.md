---
name: writing-claude-md-files
description: Use when creating or updating CLAUDE.md files for projects or subdirectories - covers top-level vs domain-level organization, capturing architectural intent and contracts, and mandatory freshness dates
---

# Writing CLAUDE.md Files

## Core Principle

CLAUDE.md files bridge Claude's statelessness. They preserve context so humans don't re-explain architectural intent every session.

**Key distinction:**
- **Top-level**: HOW to work in this codebase (commands, conventions)
- **Subdirectory**: WHY this piece exists and what it PROMISES (contracts, intent)

## File Hierarchy

Claude automatically reads CLAUDE.md files from current directory up to root:

```
project/
├── CLAUDE.md                    # Project-wide: tech stack, commands, conventions
└── src/
    └── domains/
        ├── auth/
        │   └── CLAUDE.md        # Auth domain: purpose, contracts, invariants
        └── billing/
            └── CLAUDE.md        # Billing domain: purpose, contracts, invariants
```

**Depth guideline:** Typically one level (domain). Occasionally two (subdomain). Rarely more.

## Top-Level CLAUDE.md

Focuses on project-wide WHAT and HOW.

### What to Include

| Section | Purpose |
|---------|---------|
| Tech Stack | Framework, language, key dependencies |
| Commands | Build, test, run commands |
| Project Structure | Directory overview with purposes |
| Conventions | Naming, patterns used project-wide |
| Boundaries | What Claude can/cannot edit |

### Template

```markdown
# [Project Name]

Last verified: [DATE - use `date +%Y-%m-%d`]

## Tech Stack
- Language: TypeScript 5.x
- Framework: Next.js 14
- Database: PostgreSQL
- Testing: Vitest

## Commands
- `npm run dev` - Start dev server
- `npm run test` - Run tests
- `npm run build` - Production build

## Project Structure
- `src/domains/` - Domain modules (auth, billing, etc.)
- `src/shared/` - Cross-cutting utilities
- `src/infrastructure/` - External adapters (DB, APIs)

## Conventions
- Functional Core / Imperative Shell pattern
- Domain modules are self-contained
- See domain CLAUDE.md files for domain-specific guidance

## Boundaries
- Safe to edit: `src/`
- Never touch: `migrations/` (immutable), `*.lock` files
```

## Subdirectory CLAUDE.md (Domain-Level)

Focuses on WHY and CONTRACTS. The code shows WHAT; these files explain intent.

### What to Include

| Section | Purpose |
|---------|---------|
| Purpose | WHY this domain exists (not what it does) |
| Contracts | What this domain PROMISES to others |
| Dependencies | What it uses, what uses it, boundaries |
| Key Decisions | ADR-lite: decisions and rationale |
| Invariants | Things that must ALWAYS be true |
| Gotchas | Non-obvious traps |

### Template

```markdown
# [Domain Name]

Last verified: [DATE - use `date +%Y-%m-%d`]

## Purpose
[1-2 sentences: WHY this domain exists, what problem it solves]

## Contracts
- **Exposes**: [public interfaces - what callers can use]
- **Guarantees**: [promises this domain keeps]
- **Expects**: [what callers must provide]

## Dependencies
- **Uses**: [domains/services this depends on]
- **Used by**: [what depends on this domain]
- **Boundary**: [what should NOT be imported here]

## Key Decisions
- [Decision]: [Rationale]

## Invariants
- [Thing that must always be true]

## Key Files
- `index.ts` - Public exports
- `types.ts` - Domain types
- `service.ts` - Main service implementation

## Gotchas
- [Non-obvious thing that will bite you]
```

## Freshness Dates: MANDATORY

Every CLAUDE.md MUST include a "Last verified" date.

**CRITICAL:** Use Bash to get the actual date. Do NOT hallucinate dates.

```bash
date +%Y-%m-%d
```

**Why mandatory:** Stale CLAUDE.md files are worse than none. The date signals when contracts were last confirmed accurate.

## Heuristics: Top-Level vs Subdirectory

| Question | Top-level | Subdirectory |
|----------|-----------|--------------|
| Applies project-wide? | Yes | |
| New engineer needs on day 1? | Yes | |
| About commands/conventions? | Yes | |
| About WHY a component exists? | | Yes |
| About contracts between parts? | | Yes |
| Changes when the domain changes? | | Yes |

**Rule of thumb:**
- Top-level = "How to work here"
- Subdirectory = "Why this exists and what it promises"

## When to Create Subdirectory CLAUDE.md

Create when:
- Domain has non-obvious contracts with other parts
- Architectural decisions affect how code should evolve
- Invariants exist that aren't obvious from code
- New sessions consistently need the same context re-explained

Don't create for:
- Trivial utility folders
- Implementation details that change frequently
- Content better captured in code comments

## Updating CLAUDE.md Files

When updating any CLAUDE.md:

1. **Update the freshness date** using Bash `date +%Y-%m-%d`
2. **Verify contracts still hold** - read the code, check invariants
3. **Remove stale content** - better short and accurate than long and wrong
4. **Keep token-efficient** - <300 lines top-level, <100 lines subdirectory

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Describing WHAT code does | Focus on WHY it exists, contracts it keeps |
| Missing freshness date | Always include, always use Bash for real date |
| Too much detail | Subdirectory files should be <100 lines |
| Duplicating parent content | Subdirectory inherits parent; don't repeat |
| Stale contracts | Update when domain changes; verify dates |

## Checklist

**Top-level:**
- [ ] Tech stack listed
- [ ] Key commands documented
- [ ] Project structure overview
- [ ] Freshness date (from `date +%Y-%m-%d`)

**Subdirectory:**
- [ ] Purpose explains WHY (not what)
- [ ] Contracts: exposes, guarantees, expects
- [ ] Dependencies and boundaries clear
- [ ] Key decisions with rationale
- [ ] Invariants documented
- [ ] Freshness date (from `date +%Y-%m-%d`)
- [ ] Under 100 lines
