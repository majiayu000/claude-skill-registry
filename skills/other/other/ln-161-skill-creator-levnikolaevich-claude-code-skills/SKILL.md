---
name: ln-161-skill-creator
description: "Creates .claude/commands from procedural doc sections. Use when transforming documentation prose into executable skill files."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# ln-161-skill-creator

**Type:** L3 Worker (standalone-capable)
**Category:** 1XX Documentation Pipeline

Creates `.claude/commands/*.md` files from procedural documentation sections. It converts procedural prose into imperative command instructions without changing the source docs.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Approved procedural sections or standalone docs scan |
| **Output** | `.claude/commands/*.md` files in target project |
| **Template** | `references/command_template.md` |
| **Read mode** | Section-first markdown reading |

---

## Input Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Provided sections** | Context contains `approved_sections` | Use supplied sections directly |
| **Standalone** | Invoked directly with `$ARGUMENTS` | Self-discover, classify, and create commands |

### Standalone Discovery

When invoked without `approved_sections`:
1. Read `shared/references/procedural_extraction_rules.md`, `shared/references/markdown_read_protocol.md`, and `shared/references/docs_quality_contract.md`
2. Scan docs-first sources:
   - `docs/**/*.md`
   - `tests/README.md`
   - `tests/manual/**/*`
   - `README.md`
   - `CONTRIBUTING.md`
3. Use `AGENTS.md`, `CLAUDE.md`, and `docs/project/.context/doc_registry.json` only to route discovery
4. Classify candidate sections with the shared procedural extraction rules
5. Present the extraction plan to the user for approval
6. Create approved commands

---

## Workflow

### Phase 1: Prepare

Receive or build this normalized input:

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

**MANDATORY READ:** Load `references/command_template.md`

### Phase 2: Transform and Create

For each approved section:

1. Read the source section using the shared markdown read protocol
2. Ignore standardized doc shell content if it appears in the selected range:
   - header markers such as `DOC_KIND`, `DOC_ROLE`, `READ_WHEN`, `SKIP_WHEN`, `PRIMARY_SOURCES`
   - `Quick Navigation`
   - `Agent Entry`
   - `Maintenance`
3. Detect `allowed-tools`

| Content Pattern | Tool |
|----------------|------|
| shell commands or fenced `bash` / `sh` blocks | Bash |
| file reads or config inspection | Read |
| file updates | Edit |
| search steps | Grep, Glob |
| skill calls | Skill |
| approval gates | AskUserQuestion |

4. Transform the content with these rules:

| Rule | From | To |
|------|------|----|
| Voice | Declarative prose | Imperative instructions |
| Code blocks | Source shell blocks | Preserve when executable |
| Numbered lists | Doc prose | Ordered workflow steps |
| Verification | Implicit expectations | Explicit verification checks |
| Doc shell | Metadata and navigation | Remove |
| Source provenance | Implied only | Explicit `Source` section |
| Related docs | Inline refs | `Related Documentation` section |

5. Write `.claude/commands/{command_name}` if the file does not already exist

### Phase 3: Report

Return:

```yaml
created:
  - file: .claude/commands/deploy.md
    source: docs/project/runbook.md#Deployment
    lines: 85
    tools: [Bash, Read]
summary: "Created 1 command from 1 procedural section"
```

---

## Critical Rules

- **Template-driven:** All output follows `references/command_template.md`.
- **Preserve source:** Never modify or delete source docs.
- **No invention:** Do not add commands, steps, or paths absent from the source.
- **Imperative voice:** Every retained instruction must be actionable.
- **No copied doc shell:** Do not copy `DOC_KIND`, `DOC_ROLE`, `Quick Navigation`, `Agent Entry`, or `Maintenance` into commands.
- **Source provenance:** Every generated command must point back to its source doc and section.
- **Relative paths:** File references must stay relative to project root.
- **Idempotent:** Skip existing command files; do not overwrite them.

## Definition of Done

- [ ] Approved sections received or discovered
- [ ] Source sections read with section-first protocol
- [ ] Allowed-tools detected per command
- [ ] Content transformed into imperative workflow steps
- [ ] Standard doc shell content removed from command output
- [ ] Source provenance included in each created command
- [ ] Existing command files not overwritten
- [ ] Creation report returned

---

**Version:** 1.0.0
**Last Updated:** 2026-03-26
