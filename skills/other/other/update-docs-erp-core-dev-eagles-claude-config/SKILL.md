---
name: update-docs
description: Universal documentation generator powered by a tech writers agents team (5 specialized agents)
argument-hint: "<target> [--preview] [--verbose] [--force] [--stack=<name>]"
tags: [documentation, diataxis, arc42, c4, eraser-io, universal, tech-writers-team]
agent: doc-orchestrator
user-invocable: true
---

# Update Documentation -- Tech Writers Agents Team

Generate world-class documentation for ANY project using a team of 5 specialized agents. Follows Diataxis, Arc42, C4 Model, Stripe, Google Style Guide, Microsoft Learn, Rust Book, and 12-Factor patterns.

## The Team

| Agent | Role | Analogy |
|-------|------|---------|
| **doc-orchestrator** | Lead -- detects stack, dispatches team, merges results | Editor-in-Chief |
| **doc-hub-architect** | Designs docs/ structure, creates INDEX hub | Information Architect |
| **doc-official-writer** | Official project docs (Diataxis 4-quadrant) | Senior Technical Writer |
| **doc-code-analyst** | Deep code docs (teaches everything to anyone) | Staff Engineer |
| **doc-diagram-artist** | Eraser.io diagrams (C4, Arc42, ERD, flows) | Visual Designer |

## What To Do

1. **Parse target and flags** from `$ARGUMENTS`. Default target is `all` if none specified.

2. **Detect project stack(s)** by scanning root for identifying files:
   - `.csproj`/`.sln` = .NET | `pom.xml` = Java | `go.mod` = Go | `Cargo.toml` = Rust
   - `package.json` = Node.js (sub-detect deps) | `requirements.txt` = Python
   - `angular.json` = Angular | `next.config.js` = Next.js | `pubspec.yaml` = Flutter
   - 30+ more stacks supported (see doc-orchestrator agent for full list)

3. **Dispatch agents** based on target (use Task tool for parallel execution):

   | Target | Agents Dispatched | Output Directory |
   |--------|-------------------|-----------------|
   | `hub` | doc-hub-architect | `docs/INDEX.md` |
   | `official` | doc-official-writer + doc-diagram-artist | `docs/project/` (11 docs) |
   | `deep` | doc-code-analyst + doc-diagram-artist | `docs/code/` (13 docs) |
   | `diagrams` | doc-diagram-artist | `docs/diagrams/` (8 diagrams) |
   | `codemap` | doc-code-analyst (quick) | `docs/code/01-CODEBASE-MAP.md` |
   | `api` | doc-official-writer (quick) | `docs/project/06-API-REFERENCE.md` |
   | `memory` | doc-orchestrator (self) | Refresh MEMORY.md counters |
   | `claude` | doc-orchestrator (self) | Update CLAUDE.md active context |
   | `all` | ALL agents in parallel | Full `docs/` generation |

4. **Post-process**: Cross-link all documents, verify all markdown links resolve, report summary.

5. **Verify**: Check no empty documents, all diagrams have valid URLs, hub links to every doc.

## Documentation Architecture

### Layer 1: Official Project Documentation (`docs/project/`)
Follows **Diataxis** (4 content types) + **Arc42** (architecture template) + **Stripe** (API docs):

| Document | Type | Framework |
|----------|------|-----------|
| OVERVIEW.md | Explanation | Arc42 S1-S2 |
| QUICKSTART.md | Tutorial | Microsoft Learn |
| TUTORIALS.md | Tutorial | Rust Book |
| ARCHITECTURE.md | Explanation | Arc42 S3-S9 + C4 |
| HOWTO-GUIDES.md | How-to | Diataxis |
| API-REFERENCE.md | Reference | Stripe (use-case-first) |
| DEPLOYMENT.md | Reference | 12-Factor App |
| CONFIGURATION.md | Reference | 12-Factor III |
| SECURITY.md | Explanation | OWASP + GDPR |
| GLOSSARY.md | Reference | Arc42 S12 |
| ADR/ | Explanation | Arc42 S9 |

### Layer 2: Deep Code Documentation (`docs/code/`)
Follows **Rust Book** progressive teaching (TL;DR -> Plain English -> Technical -> Deep Dive):

| Document | What It Teaches |
|----------|-----------------|
| CODEBASE-MAP.md | Every file and its responsibility |
| ARCHITECTURE-PATTERNS.md | All design patterns with real code |
| DATA-FLOW.md | Request lifecycle end-to-end |
| DATA-MODEL.md | All entities and relationships |
| CLASS-HIERARCHY.md | Interfaces, implementations, composition |
| ALGORITHMS.md | Core algorithms with complexity analysis |
| ERROR-HANDLING.md | Error types and recovery patterns |
| TESTING-STRATEGY.md | Test pyramid and coverage map |
| PERFORMANCE.md | Bottlenecks and optimization |
| SECURITY-INTERNALS.md | Auth implementation and GDPR mechanics |
| DEPENDENCIES.md | Every dependency and why it was chosen |
| CONVENTIONS.md | Naming, file org, commit style |
| TECHNICAL-DEBT.md | Known issues and refactoring candidates |

### Layer 3: Diagrams (`docs/diagrams/`)
Generated via **Eraser.io API** following **C4 Model**:

System Context (C4 L1) | Container (C4 L2) | Component (C4 L3) | Data Model (ERD) | API Flow (Sequence) | Deployment | Security Flow | Data Flow

## Arguments

- `<target>`: One of `hub`, `official`, `deep`, `diagrams`, `codemap`, `api`, `memory`, `claude`, `all`
- `--preview`: Show planned files and sections without writing anything
- `--verbose`: Show agent dispatch log and scan details
- `--force`: Overwrite existing docs (default: merge/update non-destructively)
- `--stack=<name>`: Override auto-detection (e.g., `--stack=dotnet`)

## Examples

```bash
/update-docs all                    # Full documentation generation
/update-docs official --preview     # Preview official docs without writing
/update-docs deep                   # Generate deep code documentation
/update-docs diagrams               # Regenerate all Eraser.io diagrams
/update-docs codemap                # Quick: codebase map only
/update-docs api                    # Quick: API reference only
/update-docs memory                 # Refresh EAGLES MEMORY.md counters
/update-docs hub                    # Generate documentation hub INDEX
```

## Verification

After running, verify:
1. `docs/INDEX.md` exists and links to all generated documents
2. `docs/project/` contains 11+ documents following Diataxis types
3. `docs/code/` contains 13+ documents with progressive teaching structure
4. `docs/diagrams/` contains Eraser.io diagram URLs
5. All code snippets reference real source files (never invented)
6. Writing style follows Google Developer Docs guidelines
