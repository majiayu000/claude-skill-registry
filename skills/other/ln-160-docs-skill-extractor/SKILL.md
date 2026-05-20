---
name: ln-160-docs-skill-extractor
description: "Extracts procedural content from project docs into .claude/commands skills. Use when docs contain deploy, test, or troubleshoot procedures."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# ln-160-docs-skill-extractor

**Type:** L2 Coordinator
**Category:** 1XX Documentation Pipeline
**Workers:** ln-161-skill-creator, ln-162-skill-reviewer

Scans project documentation, identifies procedural content (deploy, test, SSH, troubleshoot), and extracts it into executable `.claude/commands/*.md` skills. Declarative content (architecture, requirements, API specs) remains as documentation.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Project docs (`docs/`, `tests/`, `README.md`) |
| **Output** | `.claude/commands/*.md` files in target project |
| **Workers** | ln-161 (create commands), ln-162 (review commands) |

---

## Workflow

```
Phase 1: Discovery (scan docs, build inventory)
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

Scan target project documentation to build content inventory.

**Scan targets:**
- `docs/` (all .md recursively)
- `tests/README.md`, `tests/manual/`
- `.claude/commands/` (existing -- to avoid duplicates)
- `README.md`, `CONTRIBUTING.md`

**Per file:** Extract H2/H3 sections with metadata.

**Build contextStore:**
```yaml
contextStore:
  project_root: {CWD}
  existing_commands: [list of .claude/commands/*.md filenames]
  doc_inventory:
    - file: docs/project/runbook.md
      sections:
        - header: "Deployment"
          line_range: [45, 92]
          signals: { code_blocks: 3, numbered_steps: 5, imperative_verbs: 8 }
```

---

## Phase 2: Classification

**MANDATORY READ:** Load `references/classification_rules.md`

Score each section as PROCEDURAL vs DECLARATIVE via weighted signals. Apply thresholds to classify:

| Classification | Condition | Action |
|---------------|-----------|--------|
| PROCEDURAL | proc >= 4 AND proc > decl * 2 | Extract to command |
| DECLARATIVE | decl >= 4 AND decl > proc * 2 | Skip (keep as doc) |
| MIXED | Both >= 3 | Partial extraction |
| THIN | Both < 3 | Skip |

Filter: remove sections already covered by existing `.claude/commands/`.

---

## Phase 3: Extraction Plan (User Approval Gate)

Present classified results via AskUserQuestion:

```
Found {N} procedural sections in {M} files:

| # | Source | Section | Score | Proposed Command |
|---|--------|---------|-------|------------------|
| 1 | runbook.md | Deployment | P:8/D:1 | deploy.md |
| 2 | runbook.md | Troubleshooting | P:6/D:0 | troubleshoot.md |
| 3 | tests/README.md | Running Tests | P:7/D:2 | run-tests.md |

Existing .claude/commands/ (will skip): refresh_context.md, build-and-test.md

Include? (e.g., "1,2,3" or "all" or "all skip 3")
```

If user approves none, end with "No skills to create."

---

## Phase 4: Delegate to ln-161 (Skill Creation)

Pass approved sections from contextStore to ln-161-skill-creator:

```
Agent(
  description: "Create commands from docs",
  prompt: "Execute skill creator.\nStep 1: Invoke:\n  Skill(skill: \"ln-161-skill-creator\")\nCONTEXT:\n{contextStore with approved sections}",
  subagent_type: "general-purpose"
)
```

Collect: list of created file paths + per-file summary.

---

## Phase 5: Delegate to ln-162 (Skill Review)

Pass created command file paths to ln-162-skill-reviewer:

```
Agent(
  description: "Review created commands",
  prompt: "Execute skill reviewer in COMMAND mode.\nStep 1: Invoke:\n  Skill(skill: \"ln-162-skill-reviewer\", args: \"commands\")\nFILES: {list of created paths}",
  subagent_type: "general-purpose"
)
```

Collect: review verdicts per file + aggregate pass rate.

---

## Phase 6: Report

Aggregate results from ln-161 (created files) + ln-162 (review verdicts):

```
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

Next steps:
- Test each command by invoking /{command-name}
- Customize generated commands for project-specific needs
```

---

## Critical Rules

- **Detect before extract:** Only extract sections scoring PROCEDURAL -- never force extraction on declarative content
- **No duplicates:** Skip sections already covered by existing `.claude/commands/` files
- **User approval required:** Never create commands without Phase 3 confirmation
- **Delegate creation:** All command file writing goes through ln-161 (SRP)
- **Delegate review:** All command validation goes through ln-162 (SRP)
- **Preserve docs:** Source documentation stays intact -- commands are extracted, not moved

---

## Definition of Done

- [ ] Doc inventory built (all scan targets discovered)
- [ ] Classification scored for every section (PROCEDURAL/DECLARATIVE/MIXED/THIN)
- [ ] User approved extraction plan (Phase 3 gate passed)
- [ ] ln-161 created all approved commands
- [ ] ln-162 reviewed all created commands
- [ ] Report aggregated with scan/create/review metrics

---

## Phase 7: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after Phase 6 completes. Output to chat using the `planning-coordinator` format.

---

**Version:** 1.0.0
**Last Updated:** 2026-03-13
