---
name: ln-161-skill-creator
description: "Creates .claude/commands from procedural doc sections. Use when transforming documentation prose into executable skill files."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/{path}`.

# ln-161-skill-creator

**Type:** L3 Worker (standalone-capable)
**Category:** 1XX Documentation Pipeline
**Coordinator:** ln-160-docs-skill-extractor (optional)

Creates `.claude/commands/*.md` files from procedural documentation sections. Transforms declarative prose into imperative executable instructions.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Procedural doc sections (from ln-160 contextStore or standalone scan) |
| **Output** | `.claude/commands/*.md` files in target project |
| **Template** | `references/command_template.md` |

---

## Input Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Worker** | Invoked by ln-160 with contextStore | Use provided sections directly |
| **Standalone** | Invoked directly with `$ARGUMENTS` | Self-discover + classify docs |

### Standalone Discovery

When invoked directly (not via ln-160):
1. If `$ARGUMENTS` = file paths -> read those docs, extract procedural sections
2. If `$ARGUMENTS` = "all" or empty -> scan `docs/` recursively
3. Classify sections using same rules as ln-160 Phase 2

**MANDATORY READ:** Load `../ln-160-docs-skill-extractor/references/classification_rules.md` (standalone mode only)

4. Present extraction plan to user via AskUserQuestion
5. Create approved commands
6. Recommend user to run ln-162-skill-reviewer for quality review

---

## Workflow (Worker Mode)

### Phase 1: Prepare

Receive contextStore with approved procedural sections:
```yaml
approved_sections:
  - source_file: docs/project/runbook.md
    section_header: "Deployment"
    line_range: [45, 92]
    command_name: deploy.md
  - source_file: tests/README.md
    section_header: "Running Tests"
    line_range: [15, 48]
    command_name: run-tests.md
```

**MANDATORY READ:** Load `references/command_template.md`

### Phase 2: Transform and Create

For each approved section:

1. **Read source** -- extract section content from source file at specified line range

2. **Detect allowed-tools** -- infer from content:

| Content Pattern | Tool |
|----------------|------|
| bash/sh code blocks, shell commands | Bash |
| File read/load references | Read |
| File modify/update instructions | Edit |
| Search/find in files | Grep, Glob |
| Skill invocations | Skill |
| User confirmation steps | AskUserQuestion |

3. **Transform content** using rules below

4. **Write file** to `.claude/commands/{command_name}`

### Transformation Rules

| Rule | From | To |
|------|------|----|
| Voice | Declarative ("The system uses X") | Imperative ("Run X") |
| Code blocks | Preserve as-is | Keep unchanged |
| Numbered lists | Description-style | Ordered workflow steps with ### headers |
| Verification | Implicit ("should work") | Explicit verification commands |
| Doc metadata | SCOPE tags, Maintenance sections | Remove |
| Troubleshooting | Prose | Table format (Issue / Solution) |
| Prerequisites | Mentioned inline | Dedicated Prerequisites table |
| Related docs | Inline references | Related Documentation section with relative links |
| Trigger phrases | Missing in source | Append "Use when {inferred from section context}" to description |

### Phase 3: Report

Return to coordinator (or display to user in standalone mode):

```yaml
created:
  - file: .claude/commands/deploy.md
    source: docs/project/runbook.md#Deployment
    lines: 85
    tools: [Bash, Read]
  - file: .claude/commands/run-tests.md
    source: tests/README.md#Running Tests
    lines: 62
    tools: [Bash]
summary: "Created 2 commands from 2 procedural sections"
```

---

## Critical Rules

- **Template-driven:** All output follows `references/command_template.md` structure
- **Preserve source:** Never modify or delete source documentation files
- **No invention:** Only extract content that exists in source docs. Do NOT add commands, steps, or paths not found in the original
- **Imperative voice:** Every instruction must be actionable -- no passive descriptions
- **Relative paths:** All file references in created commands use paths relative to project root
- **Idempotent:** If command file already exists, skip (do not overwrite)

---

## Definition of Done

- [ ] Source sections read at specified line ranges
- [ ] Allowed-tools detected per content patterns
- [ ] Content transformed to imperative voice (all transformation rules applied)
- [ ] Files written to `.claude/commands/{command_name}`
- [ ] Existing command files not overwritten (idempotent)
- [ ] Report returned with created file list and summary

---

**Version:** 1.0.0
**Last Updated:** 2026-03-13
