---
name: spec
description: Spec document conventions for writing and reviewing specification documents. Apply when creating or modifying specifications, workflows, API docs, or terminology definitions.
---

# Spec Document Conventions

## Directory Structure

```
docs/spec/
├── terminology.md        # Canonical definitions (single source of truth)
├── storage.md            # .mdvs/, parquet schemas, mdvs.toml, mdvs.lock
├── shared.md             # Shared output structs (DiscoveredField, etc.)
├── commands/             # One file per CLI command
│   ├── init.md
│   ├── build.md
│   ├── search.md
│   ├── check.md
│   ├── update.md
│   ├── clean.md
│   └── info.md
├── workflows/            # Cross-cutting logic shared across commands
│   ├── inference.md
│   ├── model-loading.md
│   └── model-mismatch.md
└── archive/              # Old specs, do not reference
```

## Document Categories

- **Terminology** (`terminology.md`) — Canonical definitions, single source of truth for terms
- **Storage** (`storage.md`) — Parquet schemas, config file formats, directory layout
- **Shared types** (`shared.md`) — Output structs used by multiple commands
- **Command specs** (`commands/*.md`) — One per CLI command: inputs, behavior, output struct, errors
- **Workflows** (`workflows/*.md`) — Cross-cutting logic used by multiple commands

## Writing a Spec

### Header

Every spec starts with:

```markdown
# <Title>

**Status: DRAFT** (or TODO, REVIEW, FINAL)

**See also:** [link1](path), [link2](path)
```

### Command Spec Template

Command specs should include these sections:

```markdown
# `mdvs <command>`

**Status: DRAFT**

## Synopsis
<usage line and flags>

## Behavior
<what the command does, step by step>

## Output
<output struct definition — every command collects results in a struct before display>

## Errors
<error conditions and messages>

## Examples
<CLI usage examples>
```

### Workflow Spec Template

```markdown
# Workflow: <Name>

**Status: DRAFT**

## Overview
<what this workflow does and which commands use it>

## Algorithm
<step-by-step logic>

## Edge Cases
<boundary conditions>
```

## Rules

- **Single source of truth:** each term/struct/concept defined in ONE place only
- **Cross-references:** link, never duplicate definitions
- **Output structs:** every command must define its result as a struct, separate from display formatting
- **Mermaid for diagrams** — never ASCII art
- **No stale references:** do not link to anything in `archive/`
