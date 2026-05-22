---
name: doc-hygiene
description: Documentation hygiene — anti-drift rules, count elimination, and living document maintenance
---

# Documentation Hygiene

> Prevent documentation drift through structural rules — not manual vigilance.

## The Count Problem

Hardcoded counts (e.g., "109 skills", "28 instructions", "6 agents") in prose become stale within days during active development. Every count is a future bug.

### Rules

| Rule | Do | Don't |
|------|----|-------|
| **No counts in prose** | "See the skills catalog for the current list" | "Alex has 109 skills" |
| **Counts in tables OK** | Tables with `| Count | Value |` format are scannable and updatable | Counts buried in paragraphs |
| **Single source of truth** | One canonical location per metric | Same count in 5 files |
| **Link, don't copy** | "See [SKILLS-CATALOG.md]" | Duplicate the catalog inline |
| **Timestamp proximity** | Counts near a "Last Updated" date are acceptable | Undated counts |

### Canonical Sources

The filesystem is always the source of truth. Derive counts from directories, not from prose.

| Metric | Canonical Source | Why |
|--------|-----------------|-----|
| Skill count | `.github/skills/` directory count (or generated catalog if present) | Filesystem is truth |
| Instruction count | `.github/instructions/` directory listing | Filesystem is truth |
| Prompt count | `.github/prompts/` directory listing | Filesystem is truth |
| Agent count | `.github/agents/` directory listing | Filesystem is truth |
| Muscle count | `.github/muscles/` directory listing | Filesystem is truth |
| Command count | `package.json` `contributes.commands` (if applicable) | Code is truth |
| Synapse count | Brain QA validation output | Validated at runtime |

### Acceptable Count Locations

Counts are **tolerated** (not encouraged) in these specific locations because they serve as dashboards:

| File | Purpose | Update Cadence |
|------|---------|----------------|
| `copilot-instructions.md` Memory Stores table | AI working context | Per release |
| `ROADMAP-UNIFIED.md` Current State | Release tracking | Per release |
| `README.md` architecture tree | User-facing overview | Per release |

All other files should use **descriptive references** instead of counts.

## Document Freshness

### Staleness Indicators

| Signal | Action |
|--------|--------|
| Count doesn't match filesystem | Fix count or replace with reference |
| "Last Updated" older than 30 days on living doc | Review for accuracy |
| Version number doesn't match current release | Update or archive |
| References to removed/renamed files | Fix or remove reference |

### Living vs Historical Documents

| Type | Examples | Count Policy |
|------|----------|-------------|
| **Living** | README, copilot-instructions, ROADMAP, USER-MANUAL | Minimize counts; keep current |
| **Historical** | Research papers, competitive analyses, archived docs | Counts are snapshots — leave as-is |
| **Generated** | SKILLS-CATALOG, TRIFECTA-CATALOG | Counts are output of audit — OK |

## Docs-as-Architecture

Documentation in a cognitive architecture IS architecture. Apply the same engineering rigor to docs that you would to code:

| Code Concept | Docs Equivalent |
|-------------|-----------------|
| Broken import | Broken cross-reference link |
| Stale dependency | Stale count or version number |
| Orphan module | File not linked from any index |
| Circular dependency | Two files claiming to be source of truth |
| Dead code | Archived content still linked from living docs |

**Principle**: If a doc change would break another doc's accuracy, it's a breaking change. Treat it as such.

## Link Integrity

### Rules

| Rule | Enforcement |
|------|-------------|
| Every markdown link in living docs must resolve | Grep + verify during audit |
| Every important file in a folder should be linked from its `README.md` | Orphan check |
| Moving a file requires updating ALL references in the same commit | Grep for filename in all .md files before moving |
| Archived docs removed from active indexes | Don't link to `archive/` from living docs |
| Use relative paths within doc trees | `./architecture/FILE.md` not absolute paths |

### Orphan Detection

A file is orphaned if it exists in a doc folder but is not referenced by any index or parent document. Orphans are either:
- **Forgotten knowledge** → add to appropriate index
- **Stale artifacts** → archive or delete

## Consolidation Protocol

When reorganizing documentation:

1. **Plan the target structure** — Define subdirectories by audience/purpose
2. **Grep before moving** — Find ALL references to files being moved
3. **Move + update in one operation** — Never leave broken references, even briefly
4. **Verify post-move** — Re-run link integrity check after consolidation
5. **Update indexes** — All `README.md` index files must reflect the new structure

### Standard Directory Structure

Adapt this pattern to your project. The key is audience-separated folders:

| Directory Pattern | Audience | Content Type |
|-------------------|----------|-------------|
| `docs/guides/` | Users | How-to, setup, reference cards |
| `docs/architecture/` | Developers + AI | System design, catalogs, mapping |
| `docs/features/` | Developers | Feature specs, gap analyses |
| `docs/platforms/` | Platform devs | Heir-specific documentation |
| `docs/operations/` | Maintainers | Checklists, processes, audits |
| `docs/research/` | Strategists | Papers, competitive analysis |
| `docs/archive/` | Historical | Superseded or completed docs |

## Multi-Audience Awareness

Different documentation serves different readers. Misplacing content wastes everyone's time.

| Audience | Needs | Style |
|----------|-------|-------|
| **End Users** | Setup, commands, quick reference | Step-by-step, minimal jargon |
| **Developers** | Architecture, APIs, extension points | Conceptual + code examples |
| **AI (Alex brain)** | Skills, instructions, prompts | Terse, structured, action-oriented |
| **Contributors** | Onboarding, conventions, governance | Procedural, welcoming |

**Rule**: Before writing, ask "Who reads this?" and place it accordingly.

## Multi-Layer Documentation Strategy

Complex topics benefit from layered depth:

| Layer | Purpose | Example |
|-------|---------|---------|
| **Executive summary** | 30-second overview | README.md intro paragraph |
| **Visual diagram** | Spatial understanding | Mermaid diagrams, architecture charts |
| **Detailed inventory** | Comprehensive reference | SKILLS-CATALOG, AGENT-CATALOG |
| **Code-level detail** | Implementation specifics | Inline comments, SKILL.md files |

Not every topic needs all four layers, but important architecture should have at least summary + detail.

## Timing: Ship First, Document After

Skills and patterns written after successful real-world delivery are worth 10x those written from theory. The recommended flow:

1. **Build it** — Get the feature working
2. **Ship it** — Validate in real usage
3. **Document it** — Capture battle-tested knowledge while fresh
4. **Never skip step 3** — Undocumented shipped work is invisible work

Exception: Architecture Decision Records (ADRs) should be written BEFORE implementation.

## Drift Detection During Meditation

Meditation and dream sessions are natural checkpoints for doc freshness:

| Check | During |
|-------|--------|
| Version numbers in living docs match current release | Meditation consolidation |
| Framework names in stack descriptions are current | Dream maintenance |
| Diagram labels match actual component names | Synapse validation |
| README "What's New" reflects recent work | Post-release meditation |

## Doc Audit Checklist

When reviewing documentation after development work:

1. **Search for changed metrics** — Did we add/remove skills, instructions, agents, commands?
2. **Grep for stale counts** — `\b{old_count}\b` across all `.md` files
3. **Check canonical sources** — Do dashboards match filesystem?
4. **Verify cross-references** — Do links point to files that still exist?
5. **Timestamp check** — Are "Last Updated" dates current on living docs?
6. **Orphan check** — Are there files in doc folders not linked from any index?
7. **Audience check** — Is each doc in the right directory for its audience?

## CHANGELOG Best Practices

| Practice | Rationale |
|----------|-----------|
| Log architectural decisions, not just code changes | Future self needs the "why" |
| Explain **why**, not just **what** | "Added muscles" < "Established muscles as Motor Cortex, separate from memory trifecta" |
| One entry per user-visible change | Avoid implementation noise |
| Use `### Added`, `### Changed`, `### Fixed`, `### Removed` | Keep It Structured |
| Never skip a version | Git tags should match CHANGELOG headers |

## Preflight Validation

For release scripts or CI, automated count checks can catch drift early:

```powershell
# Example: Verify skill count in copilot-instructions matches filesystem
$actual = (Get-ChildItem .github/skills -Directory).Count
$documented = [regex]::Match((Get-Content .github/copilot-instructions.md -Raw), '(\d+) skills').Groups[1].Value
if ($actual -ne $documented) { Write-Warning "Skill count drift: $actual actual vs $documented documented" }
```

Integrate similar checks into your project's QA or pre-publish scripts.
