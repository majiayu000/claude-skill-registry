---
name: ln-160-docs-skill-extractor
description: "Extracts procedural content from project docs into .claude/commands skills. Use when docs contain deploy, test, or troubleshoot procedures."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-160-docs-skill-extractor

**Type:** L2 Coordinator
**Category:** 1XX Documentation Pipeline
**Workers:** ln-161-skill-creator, ln-162-skill-reviewer

Scans project documentation, identifies procedural content, and extracts it into executable `.claude/commands/*.md` files. Declarative documentation stays in markdown; this skill only routes procedural sections into command form.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project docs, test docs, and optional doc registry |
| **Output** | `.claude/commands/*.md` files in target project |
| **Workers** | ln-161 creates commands, ln-162 reviews them |
| **Source policy** | Docs-first extraction; `AGENTS.md` and `CLAUDE.md` are routing-only |

---

## Workflow

```
Phase 1: Discovery (route docs, build inventory)
    |
Phase 2: Classification (procedural vs declarative scoring)
    |
Phase 3: Extraction Plan (user approval)
    |
Phase 4: Delegate -> ln-161 (create commands)
    |
Phase 5: Delegate -> ln-162 (review commands)
    |
Phase 6: Report (aggregate results)
```

---

## Phase 1: Discovery

**MANDATORY READ:** Load `shared/references/procedural_extraction_rules.md`, `shared/references/markdown_read_protocol.md`, and `shared/references/docs_quality_contract.md`

Build a docs-first inventory before extracting anything.

### Routing Sources

Use these files only to route discovery and prioritize reading:
- `AGENTS.md`
- `CLAUDE.md`
- `docs/project/.context/doc_registry.json` if present

Do **not** extract commands from routing sources.

### Extraction Sources

Scan only these sources for procedural content:
- `docs/**/*.md`
- `tests/README.md`
- `tests/manual/**/*`
- `README.md`
- `CONTRIBUTING.md`

Also scan:
- `.claude/commands/*.md` to avoid duplicate command creation

### Discovery Rules

1. If `docs/project/.context/doc_registry.json` exists, prioritize:
   - canonical docs first
   - `DOC_KIND=how-to` before `reference`
   - `reference` before `index` and `explanation`
2. Read markdown with the shared section-first protocol:
   - use outline first for large or unfamiliar files
   - read header markers and top sections first
   - expand only sections that might contain procedures
3. Ignore standard doc shell sections as extraction candidates:
   - `Quick Navigation`
   - `Agent Entry`
   - `Maintenance`
   - header markers such as `SCOPE`, `DOC_KIND`, `DOC_ROLE`, `READ_WHEN`, `SKIP_WHEN`, `PRIMARY_SOURCES`

### Build `contextStore`

```yaml
contextStore:
  project_root: {CWD}
  routing_sources:
    agents_md: true
    claude_md: true
    doc_registry: true
  existing_commands: [list of .claude/commands/*.md filenames]
  doc_inventory:
    - file: docs/project/runbook.md
      doc_kind: how-to
      doc_role: canonical
      sections:
        - header: "Deployment"
          line_range: [45, 92]
          signals: { code_blocks: 3, numbered_steps: 5, imperative_verbs: 8 }
```

---

## Phase 2: Classification

Score each candidate section with the shared procedural extraction rules.

| Classification | Condition | Action |
|---------------|-----------|--------|
| PROCEDURAL | `proc >= 4` and `proc > decl * 2` | Extract to command |
| DECLARATIVE | `decl >= 4` and `decl > proc * 2` | Keep as documentation |
| MIXED | Both >= 3 | Extract procedural subsection only |
| THIN | Both < 3 | Skip |

Filter:
- drop sections already covered by an existing `.claude/commands/*.md`
- drop standard doc shell sections
- prefer `DOC_KIND=how-to` when multiple sections overlap semantically

---

## Phase 3: Extraction Plan (User Approval Gate)

Present the classified result set to the user before creating files.

```
Found {N} procedural sections in {M} files:

| # | Source | DOC_KIND | Section | Score | Proposed Command |
|---|--------|----------|---------|-------|------------------|
| 1 | runbook.md | how-to | Deployment | P:8/D:1 | deploy.md |
| 2 | tests/README.md | index | Running Tests | P:7/D:2 | run-tests.md |

Existing .claude/commands/ (will skip): refresh_context.md, build-and-test.md

Include? (e.g., "1,2" or "all" or "all skip 2")
```

If the user approves nothing, stop with `No skills to create.`

---

## Phase 4: Delegate to ln-161 (Skill Creation)

Pass only approved sections to `ln-161-skill-creator`.

```text
Agent(
  description: "Create commands from procedural docs",
  prompt: "Execute skill creator.\nStep 1: Invoke:\n  Skill(skill: \"ln-161-skill-creator\")\nCONTEXT:\n{approved_sections}",
  subagent_type: "general-purpose"
)
```

Normalized payload:

```json
{
  "approved_sections": [
    {
      "source_file": "docs/project/runbook.md",
      "section_header": "Deployment",
      "line_range": [45, 92],
      "command_name": "deploy.md",
      "doc_kind": "how-to",
      "doc_role": "canonical"
    }
  ]
}
```

Collect:
- created file paths
- source-to-command mapping
- per-command summary

---

## Phase 5: Delegate to ln-162 (Skill Review)

Pass created command paths to `ln-162-skill-reviewer` in COMMAND mode.

```text
Agent(
  description: "Review created commands",
  prompt: "Execute skill reviewer in COMMAND mode.\nStep 1: Invoke:\n  Skill(skill: \"ln-162-skill-reviewer\", args: \"commands\")\nFILES: {list of created paths}",
  subagent_type: "general-purpose"
)
```

Collect:
- verdict per file
- aggregate pass/fix/warn counts

---

## Phase 6: Report

Aggregate the create and review results.

```text
## Docs Skill Extractor -- Complete

| Metric | Count |
|--------|-------|
| Documents scanned | {N} |
| Sections analyzed | {N} |
| Procedural found | {N} |
| Commands created | {N} |
| Commands skipped (existing) | {N} |
| Review PASS | {N} |
| Review FIXED | {N} |
| Review WARN | {N} |

Created commands:
- .claude/commands/deploy.md (from runbook.md#Deployment)
- .claude/commands/run-tests.md (from tests/README.md#Running Tests)
```

---

## Critical Rules

- **Docs-first extraction:** Extract only from docs sources. `AGENTS.md` and `CLAUDE.md` route discovery but never become command sources.
- **Section-first reading:** Use the shared markdown read protocol before full-file reads.
- **Detect before extract:** Only extract sections classified as procedural.
- **No duplicates:** Skip sections already covered by existing `.claude/commands/*.md`.
- **User approval required:** Never create commands without Phase 3 confirmation.
- **Delegate creation:** All command file writing goes through ln-161.
- **Delegate review:** All command validation goes through ln-162.
- **Preserve docs:** Source documentation stays intact.

---

**TodoWrite format (mandatory):**
```text
- Build docs inventory (in_progress)
- Invoke ln-161-skill-creator (pending)
- Invoke ln-162-skill-reviewer (pending)
- Aggregate report (pending)
```

## Worker Invocation (MANDATORY)

| Phase | Worker | Context |
|-------|--------|---------|
| 4 | ln-161-skill-creator | Approved procedural sections with source metadata |
| 5 | ln-162-skill-reviewer | Created command file paths in COMMAND mode |

**All workers:** Invoke via Skill tool. Workers consume only the context they need.

## Definition of Done

- [ ] Routing sources checked (`AGENTS.md`, `CLAUDE.md`, doc registry if present)
- [ ] Extraction inventory built from docs-first sources
- [ ] Every candidate section classified
- [ ] User approved extraction plan
- [ ] ln-161 created all approved commands
- [ ] ln-162 reviewed all created commands
- [ ] Final report aggregated with scan, create, and review metrics

---

## Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after Phase 6 completes. Output to chat using the `planning-coordinator` format.

---

**Version:** 1.0.0
**Last Updated:** 2026-03-26
