---
name: doc-navigator
description: Efficiently navigate codebase documentation during Research phase. Use instead of Grep/Glob for finding architectural decisions, feature specs, and technical docs. Maps topics to doc locations for fast context retrieval. If codebase lacks documentation structure, provides patterns to establish one.
---

# Doc Navigator

Navigate codebase documentation efficiently by checking known doc locations first, before resorting to grep/glob searches.

## When to Use

- Finding architectural decisions (ADRs)
- Locating feature specs or API docs
- Researching codebase before implementation
- Suggesting documentation structure for new projects
- Alternative to grep/glob for doc discovery

## Quick Start

1. Check for docs directory at project root
2. Scan for common doc file patterns
3. If docs exist → map topics to locations
4. If no docs → suggest documentation structure (see `references/doc-patterns.md`)

## Common Documentation Locations

Check these locations in order:

```
project-root/
├── docs/                    # Primary documentation
│   ├── architecture/        # System design, ADRs
│   ├── features/            # Feature specs
│   ├── api/                 # API documentation
│   └── guides/              # How-to guides
├── .github/                 # GitHub-specific docs
│   └── docs/
├── README.md                # Project overview
├── ARCHITECTURE.md          # High-level architecture
├── CONTRIBUTING.md          # Contribution guidelines
└── doc/ or documentation/   # Alternative doc folders
```

## Topic-to-Location Mapping

| Looking for... | Check first |
|----------------|-------------|
| Project overview | `README.md` |
| Architecture/design | `docs/architecture/`, `ARCHITECTURE.md`, `docs/adr/` |
| Feature specs | `docs/features/`, `docs/specs/` |
| API reference | `docs/api/`, `api-docs/`, OpenAPI/Swagger files |
| Setup/installation | `docs/guides/setup.md`, `INSTALL.md` |
| Database schema | `docs/database/`, `docs/schema/`, `prisma/schema.prisma` |
| Data types/models | `docs/types/`, `docs/models/`, `src/types/`, `src/models/` |
| Style guide | `docs/style-guide.md`, `docs/conventions.md`, `.eslintrc`, `STYLE.md` |
| Environment config | `docs/config/`, `.env.example`, `docs/environment.md` |
| Testing strategy | `docs/testing/`, `tests/README.md` |
| Deployment | `docs/deployment/`, `docs/infrastructure/` |
| ADRs (decisions) | `docs/adr/`, `docs/decisions/`, `architecture/decisions/` |
| ADRs (fallback) | `CHANGELOG.md`, `git log`, PR descriptions, code comments |

## Discovery Workflow

```
1. ls docs/ (or doc/, documentation/)
   ↓ exists?
   YES → scan structure, build topic map
   NO  → check for standalone doc files (*.md in root)
         ↓ found?
         YES → use available docs
         NO  → suggest creating docs structure
               (see references/doc-patterns.md)
```

## Automated Discovery

Run the scanner script to map available documentation:

```bash
python3 scripts/scan_docs.py [project-path]
```

Output: JSON map of topics → file locations

## When Docs Don't Exist

If the codebase lacks documentation:

1. Inform user: "No documentation structure found"
2. Offer to create starter docs: `view references/doc-patterns.md`
3. Suggest minimal viable structure based on project type

## Finding Decisions Without ADRs

If no formal ADRs exist, extract architectural context from:

```
CHANGELOG.md        → Breaking changes, migration rationale
git log             → Commits w/ "migrate", "refactor", "replace"
PR/MR descriptions  → Discussion threads on major changes
Issue tracker       → Closed RFCs, architecture proposals
Code comments       → // DECISION:, // WHY:, // HACK:
```

See `references/doc-patterns.md` → "Fallback: When No ADRs Exist" for git commands & reconstruction templates.

## Integration with Research Phase

Use doc-navigator BEFORE grep/glob when:
- Starting work on unfamiliar codebase
- Looking for architectural context
- Understanding feature implementations
- Finding API contracts or schemas

Fall back to grep/glob when:
- Docs don't cover the specific topic
- Need to find implementation details in code
- Searching for specific function/class usage

---

Ref: `references/doc-patterns.md` for documentation templates when establishing new docs.
