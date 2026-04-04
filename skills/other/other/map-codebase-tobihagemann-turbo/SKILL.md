---
name: map-codebase
description: "Deep architecture report that fans out parallel inspections across different aspects of the codebase (structure, tech stack, APIs, patterns, data flow, dependencies, testing) and synthesizes findings into a comprehensive document at .turbo/codebase-map.md and .turbo/codebase-map.html. Use when the user asks to \"map the codebase\", \"map codebase\", \"architecture report\", \"codebase overview\", \"architecture overview\", \"what am I looking at\", or \"onboard me\"."
---

# Map Codebase

Deep architecture report. Fans out parallel inspections across different aspects of the codebase, synthesizes their findings, and writes `.turbo/codebase-map.md` and `.turbo/codebase-map.html`. Analysis-only.

## Task Tracking

At the start, use `TaskCreate` to create a task for each phase:

1. Scope
2. Launch inspection agents
3. Synthesize and generate markdown report
4. Generate HTML report

## Step 1: Scope

If `$ARGUMENTS` specifies paths, use those directly (skip the question).

Otherwise, use `AskUserQuestion` to confirm scope:

- **Entire codebase** — inspect everything
- **Specific paths** — user provides directories or file patterns

Once scope is determined, glob for source files in the selected scope. Exclude generated and vendored directories (`node_modules/`, `dist/`, `build/`, `vendor/`, `__pycache__/`, `.build/`, `DerivedData/`, `target/`, `.tox/`, and others appropriate to the project).

Build a file manifest grouped by top-level source directory. This manifest is shared with all agents as a starting point. Agents may explore beyond it based on what they discover.

## Step 2: Launch Inspection Agents

Launch all Agent tool calls in parallel (`model: "opus"`, do not set `run_in_background`). Each agent receives the scoped file manifest and its exploration brief. Batch across multiple messages if the total exceeds what can be launched at once.

### Dimensions

Launch one agent per dimension. Each agent's prompt provides the file manifest and the exploration brief below. Agents explore adaptively: go deeper where complexity warrants it, stay high-level where things are straightforward. Findings should be concrete (reference specific files and directories) rather than generic.

| # | Dimension | Exploration Brief |
|---|---|---|
| 1 | Project Structure | Map directory layout, module organization, naming conventions, and file roles. Identify the organizing principle (feature-based, layer-based, hybrid). Note generated or build output directories. |
| 2 | Tech Stack and Build System | Identify languages, frameworks, package managers, build tools, and runtime requirements. Note version constraints and compatibility targets. |
| 3 | Entry Points and Public API | Find how the system is invoked: CLI commands, HTTP endpoints, event handlers, exported modules, main functions. Map the public surface area. |
| 4 | Core Abstractions and Patterns | Identify key types, classes, interfaces, and design patterns. Note architectural patterns (MVC, plugin system, pipeline, etc.) and how they shape the code. |
| 5 | Data Flow and State | Trace how data enters, transforms, persists, and exits the system. Identify state management approaches, storage layers, and data boundaries. |
| 6 | External Dependencies and Integrations | Map third-party services, APIs, databases, and system boundaries. Note how external dependencies are abstracted or coupled. |
| 7 | Testing and Quality Infrastructure | Describe the test strategy: frameworks, coverage approach, test organization, CI/CD pipeline. Note gaps or unusual patterns. |

Each agent writes its findings as structured markdown with sections and subsections.

## Step 3: Synthesize and Generate Markdown Report

After all agents complete:

1. Read all agent reports.
2. Identify cross-cutting themes, connections between dimensions, and architectural trade-offs.
3. Write a brief executive summary (3-5 sentences) capturing the system's essential character.
4. Resolve contradictions or overlaps between dimension reports.
5. Write `.turbo/codebase-map.md` using the report template. Output the executive summary as text before writing the file.

### Report Template

```markdown
# Codebase Map

**Date:** <date>
**Scope:** <what was inspected>

## Executive Summary

<3-5 sentences: what the system is, how it's organized, what architectural choices define it>

## Project Structure

<from dimension 1>

## Tech Stack

<from dimension 2>

## Entry Points and API

<from dimension 3>

## Core Abstractions

<from dimension 4>

## Data Flow

<from dimension 5>

## External Dependencies

<from dimension 6>

## Testing and Quality

<from dimension 7>

## Cross-Cutting Observations

<themes, trade-offs, and connections identified during synthesis>
```

## Step 4: Generate HTML Report

Convert the markdown report into a styled, interactive HTML page.

1. Run the `/frontend-design` skill to load design principles.
2. Read `.turbo/codebase-map.md` for the full report content.
3. Write a self-contained `.turbo/codebase-map.html` (single file, no external dependencies beyond Google Fonts) that presents the architecture report with:
   - Executive summary card
   - Sticky navigation between sections
   - Collapsible dimension sections
   - File and directory references as styled inline code
   - Entrance animations and hover states
   - Print-friendly styles via `@media print`
   - Responsive layout for mobile

## Rules

- If any agent fails, proceed with findings from the remaining agents and note the failure in the report.
- Each dimension agent operates independently. Overlapping observations from different angles are expected. The synthesis step resolves overlaps.
- Does not modify source code, stage files, or commit.
