---
name: doc-maintenance
description: "Systematic documentation audit and maintenance. This skill should be used when documentation may be stale, missing, or misorganized — after feature work, refactors, dependency upgrades, or as a periodic health check. It prescribes folder structure for docs/ and manual/, dispatches haiku subagents for codebase/doc scanning, and routes doc creation to specialized agents (reference-builder, technical-writer, learning-guide) with docs-architect as quality gate."
---

# Documentation Maintenance

Systematically audit, organize, and remediate project documentation by comparing the codebase
against existing docs to find staleness, gaps, and misorganization.

## When to Trigger

- After merging a feature branch or completing a refactor
- After dependency upgrades or API changes
- When onboarding surfaces confusion about project docs
- Periodic maintenance (monthly or per-release)
- When `scripts/doc_audit.py` is run manually and reports findings

## Workflow Overview

```
Phase 1: Audit       → Run deterministic scan + haiku search agents
Phase 2: Triage      → Classify findings by severity and action type
Phase 3: Remediate   → Dispatch specialized agents to fix/create docs
Phase 4: Quality     → docs-architect reviews all changes
```

---

## Phase 1: Audit

### Step 1a — Run the deterministic scan

Execute the bundled audit script to get a baseline report:

```bash
python3 skills/doc-maintenance/scripts/doc_audit.py
```

The script produces a structured report covering:
- Broken internal links (markdown `[text](path)` pointing to missing files)
- Orphan docs (files not linked from any other doc or README)
- Missing required structure (expected folders/files absent from `docs/` or `manual/`)
- Stale timestamp indicators (files unchanged for >90 days with code siblings that changed)
- Empty or stub files (< 3 lines of content)

Pass `--json` for machine-readable output. Pass `--root PATH` to override project root detection.

### Step 1b — Dispatch haiku search agents

After the deterministic scan, launch parallel haiku subagents to perform deeper analysis.
Use `model: "haiku"` on all Task calls in this phase to minimize cost.
See `references/agent-dispatch.md` for full prompt templates.

**Agent 1 — Code-to-doc coverage scan** (`subagent_type: "Explore"`, `model: "haiku"`):
Search the codebase for public APIs, CLI commands, config schemas, and exported modules.
Cross-reference against existing docs. Report anything undocumented.

**Agent 2 — Doc-to-code freshness scan** (`subagent_type: "Explore"`, `model: "haiku"`):
Read each doc file and verify the code constructs it references still exist and match
current signatures/behavior. Report mismatches.

**Agent 3 — Structure compliance scan** (`subagent_type: "Explore"`, `model: "haiku"`):
Compare current `docs/` and `manual/` layout against the prescribed folder structure
in `references/folder-structure.md`. Report missing folders, misplaced files, naming violations.

**Agent 4 — Diagram opportunity scan** (`subagent_type: "Explore"`, `model: "haiku"`):
Scan all markdown files for ASCII/text diagrams (box-drawing characters, arrow notation,
indented tree structures beyond a few simple nodes) that should be converted to Mermaid.
Also identify sections describing flows, architectures, state machines, sequences, or
relationships where a diagram would add clarity but none exists. Report the file path,
line range, diagram type (flowchart, sequence, state, ER, etc.), and whether it is a
conversion or a net-new diagram.

Launch all four agents in parallel.

### Step 1c — Merge results

Combine the script output with agent findings into a single audit report. Deduplicate
overlapping findings. The report becomes the input for Phase 2.

---

## Phase 2: Triage

Classify each finding into one of these action categories:

| Category | Description | Example |
|----------|-------------|---------|
| **stale** | Doc exists but references outdated code/behavior | CLI flag renamed but docs show old name |
| **missing** | No doc exists for a documented-worthy item | Public API endpoint with no reference doc |
| **orphan** | Doc exists but is unreachable / unlinked | Guide file not in any index or nav |
| **misplaced** | Doc exists but is in the wrong folder | Tutorial sitting in `docs/architecture/` |
| **irrelevant** | Doc covers removed functionality | Guide for a deleted feature |
| **structural** | Folder structure deviates from prescribed layout | Missing `docs/security/` folder |
| **diagram-convert** | ASCII/text diagram should be Mermaid | Complex box-drawing flowchart in architecture doc |
| **diagram-missing** | Section would benefit from a diagram | Multi-step process described only in prose |

Assign severity:
- **P0** — User-facing doc is factually wrong (manual/)
- **P1** — Developer doc references nonexistent code
- **P2** — Missing doc for public API or feature
- **P3** — Structural / organizational issues
- **P4** — Minor staleness, cosmetic

---

## Phase 3: Remediate

Route each finding to the appropriate specialist agent. Use the Task tool with
the subagent types listed below. See `references/agent-dispatch.md` for detailed
prompt templates.

| Doc type | Subagent type | Target location |
|----------|---------------|-----------------|
| API reference docs | `reference-builder` | `docs/reference/` or `docs/api/` |
| Architecture docs | `technical-writer` | `docs/architecture/` |
| Developer guides (style, local dev, workflows) | `technical-writer` | `docs/development/` |
| Testing docs | `technical-writer` | `docs/testing/` |
| Security docs | `technical-writer` | `docs/security/` |
| User-facing tutorials | `learning-guide` | `manual/tutorials/` |
| User-facing how-to guides | `learning-guide` | `manual/guides/` |
| User-facing getting started | `learning-guide` | `manual/getting-started/` |
| Plans and proposals | `technical-writer` | `docs/plans/` |
| ASCII diagram conversion | `mermaid-expert` | Inline in existing doc |
| New diagrams for prose sections | `mermaid-expert` | Inline in existing doc |

**Parallel dispatch:** Group independent remediation tasks and dispatch them simultaneously.
Only serialize when one doc depends on another (e.g., an API reference needed before a tutorial
that links to it). Dispatch up to 4 remediation agents in parallel per batch.

**For updates to existing docs:** Provide the agent with the current file contents and the
specific finding to fix. Instruct it to make minimal, targeted edits.

**For new docs:** Provide the agent with the relevant source code, the target file path,
and the folder-structure spec so it follows naming conventions.

---

## Phase 4: Quality Gate

After all remediation agents complete, dispatch a single `docs-architect` agent to review
the full set of changes. The quality gate checks:

1. **Accuracy** — Do docs match current code?
2. **Completeness** — Are all public interfaces covered?
3. **Organization** — Does folder structure match the prescribed layout?
4. **Cross-references** — Are all internal links valid?
5. **Consistency** — Tone, formatting, heading levels
6. **No orphans** — Every new doc is linked from an index or parent doc

If the quality gate fails, loop back to Phase 3 for the specific issues flagged.
Maximum 2 remediation loops before escalating to the user.

---

## Folder Structure

The prescribed folder layout is defined in `references/folder-structure.md`. Summary:

### `docs/` — Internal / developer documentation

```
docs/
├── architecture/    — System design, ADRs, component diagrams
├── development/     — Developer guides: style, local setup, issue tracking
├── plans/           — Proposals, RFCs, roadmaps
├── reviews/         — Code review records, audit reports
├── testing/         — Test strategy, coverage reports, test plans
├── reports/         — Generated reports, metrics, analysis
├── security/        — Security policies, threat models, audit findings
├── api/             — Internal API docs (OpenAPI specs, gRPC protos)
├── reference/       — CLI reference, config reference, manpages
├── ideas/           — Exploratory notes, spikes, brainstorms
└── archive/         — Deprecated docs preserved for history
```

### `manual/` — User-facing documentation (project root)

```
manual/
├── getting-started/ — Installation, quickstart, first steps
├── guides/          — How-to guides for common tasks
├── tutorials/       — Step-by-step learning paths
├── reference/       — User-facing command/config reference
└── troubleshooting/ — FAQ, common errors, known issues
```

### `README.md` — Project root

The main README is audited for accuracy but not reorganized. Findings about the README
are reported as stale/missing items for manual remediation.

---

## Anti-Patterns

- Do not delete docs without confirming the feature they describe is truly removed
- Do not reorganize docs without updating all internal cross-references
- Do not create stub files just to fill the folder structure — only create docs with real content
- Do not duplicate content between `docs/` and `manual/` — link instead
- Do not move user-facing docs into `docs/` or developer docs into `manual/`
