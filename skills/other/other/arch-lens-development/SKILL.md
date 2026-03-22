---
name: arch-lens-development
categories: [arch-lens]
description: Create Development architecture diagram showing project structure, build tools, and quality gates. Development lens answering "How is it built and tested?"
hooks:
  PreToolUse:
    - matcher: "*"
      hooks:
        - type: command
          command: "echo 'Development Lens - Analyzing build and test tooling...'"
          once: true
---

# Development Architecture Lens

**Cognitive Mode:** Development
**Primary Question:** "How is it built and tested?"
**Focus:** Project Structure, Build Tools, Quality Gates, Test Framework

## When to Use

- Need to understand developer experience
- Documenting build and test infrastructure
- Analyzing code quality gates
- User invokes `/autoskillit:arch-lens-development` or `/autoskillit:make-arch-diag development`

## Critical Constraints

**NEVER:**
- Modify any source code files
- Include runtime architecture details
- Show business logic

**ALWAYS:**
- Focus on BUILD and TEST infrastructure
- Show quality gate pipeline
- Document test framework setup
- Include entry points
- BEFORE creating any diagram, LOAD the `/autoskillit:mermaid` skill using the Skill tool - this is MANDATORY

---

## Analysis Workflow

### Step 1: Launch Parallel Exploration Subagents

Spawn Explore subagents to investigate:

**Project Structure**
- Find top-level directory organization
- Identify module/package boundaries
- Look for: build configs, package definitions, project layout

**Build Tooling**
- Find build configuration
- Identify package manager and build backend
- Look for: build config files, makefiles, task runners, package managers

**Linting & Formatting**
- Find code quality tools
- Identify pre-commit hooks
- Look for: linter configs, formatter configs, pre-commit hooks, code quality tools

**Type Checking**
- Find type checking configuration
- Identify strictness level
- Look for: type checker configs, static analysis tools

**Test Framework**
- Find test configuration
- Identify test patterns and fixtures
- Look for: test configs, test directories, test runners, test fixtures

**CI/CD (if present)**
- Find CI configuration
- Identify workflow stages
- Look for: CI/CD configs, workflow definitions, pipeline configs

**Entry Points**
- Find CLI entry points
- Identify console scripts
- Look for: entry point definitions, command definitions, binary files

### Step 2: Map Quality Pipeline

Document the code quality pipeline:
```
Code -> Format -> Lint -> Type Check -> Test -> Commit
```

**CRITICAL - Analyze Read/Write Direction:**
For EVERY build/test component:
- **Inputs (reads)**: What files/config does this tool READ?
- **Outputs (writes)**: What does this tool WRITE (reports, modified files)?
- **Side effects**: Does it modify source files or just report?

Distinguish:
- Tools that READ and MODIFY code (formatters)
- Tools that READ and REPORT only (linters, type checkers)
- Tools that READ code and WRITE artifacts (test output files)
- Config files (READ by tools, not written by build process)

### Step 3: Count Project Metrics

| Metric | Value |
|--------|-------|
| Source Files | N |
| Test Files | N |
| Dependencies | N |
| Entry Points | N |

### Step 4: Create the Diagram

Use flowchart with:

**Direction:** `TB` for pipeline flow

**Subgraphs:**
- Project Structure (directories)
- Build Tools (packaging)
- Quality Gates (linting, types)
- Test Framework (test runner, etc)
- Entry Points (CLI commands)

**Node Styling:**
- `cli` class: Project structure, directories
- `phase` class: Build configuration
- `detector` class: Quality gates (linting, typing)
- `handler` class: Test framework
- `output` class: Entry points, outputs

**Show Pipeline Flow:**
- Code through quality gates
- Build to entry points

### Step 5: Write Output

Write the diagram to: `temp/arch-lens-development/arch_diag_development_{YYYY-MM-DD_HHMMSS}.md` (relative to the current working directory)

After writing the diagram file, emit a structured output line:

```
diagram_path = {absolute_path_to_diagram_file}
```

---

## Output Template

```markdown
# Development Diagram: {Project Name}

**Lens:** Development (Build & Test)
**Question:** How is it built and tested?
**Date:** {YYYY-MM-DD}
**Scope:** {What was analyzed}

## Project Metrics

| Metric | Value |
|--------|-------|
| Source Directories | {count} |
| Test Files | {count} |
| Dependencies | {count} |
| Entry Points | {count} |

## Development Diagram

```mermaid
%%{init: {'flowchart': {'nodeSpacing': 50, 'rankSpacing': 60, 'curve': 'basis'}}}%%
flowchart TB
    %% CLASS DEFINITIONS %%
    classDef cli fill:#1a237e,stroke:#7986cb,stroke-width:2px,color:#fff;
    classDef stateNode fill:#004d40,stroke:#4db6ac,stroke-width:2px,color:#fff;
    classDef handler fill:#e65100,stroke:#ffb74d,stroke-width:2px,color:#fff;
    classDef phase fill:#6a1b9a,stroke:#ba68c8,stroke-width:2px,color:#fff;
    classDef output fill:#00695c,stroke:#4db6ac,stroke-width:2px,color:#fff;
    classDef detector fill:#b71c1c,stroke:#ef5350,stroke-width:2px,color:#fff;

    subgraph Structure ["PROJECT STRUCTURE"]
        direction TB
        SRC["src/<br/>━━━━━━━━━━<br/>Source code"]
        TESTS["tests/<br/>━━━━━━━━━━<br/>Test suite"]
    end

    subgraph Build ["BUILD TOOLING"]
        direction TB
        CONFIG["Build Config<br/>━━━━━━━━━━<br/>Build system"]
        TASKFILE["Task Runner<br/>━━━━━━━━━━<br/>Task automation"]
    end

    subgraph Quality ["CODE QUALITY GATES"]
        direction TB
        FORMAT["Formatter<br/>━━━━━━━━━━<br/>Code style"]
        LINT["Linter<br/>━━━━━━━━━━<br/>Code quality"]
        TYPES["Type Checker<br/>━━━━━━━━━━<br/>Static analysis"]
    end

    subgraph Testing ["TEST FRAMEWORK"]
        direction TB
        TESTRUN["Test Runner<br/>━━━━━━━━━━<br/>Test execution"]
        FIXTURES["Fixtures<br/>━━━━━━━━━━<br/>Test setup"]
    end

    subgraph EntryPoints ["ENTRY POINTS"]
        direction LR
        EP1["cli-command"]
    end

    %% FLOW %%
    SRC --> CONFIG
    TESTS --> CONFIG
    CONFIG --> TASKFILE

    CONFIG --> FORMAT
    FORMAT --> LINT
    LINT --> TYPES

    TYPES --> TESTRUN
    TESTRUN --> FIXTURES

    CONFIG --> EP1

    %% CLASS ASSIGNMENTS %%
    class SRC,TESTS cli;
    class CONFIG,TASKFILE phase;
    class FORMAT,LINT,TYPES detector;
    class TESTRUN,FIXTURES handler;
    class EP1 output;
```

**Color Legend:**
| Color | Category | Description |
|-------|----------|-------------|
| Dark Blue | Structure | Project directories |
| Purple | Build | Configuration and automation |
| Red | Quality | Linters and type checkers |
| Orange | Testing | Test framework and fixtures |
| Dark Teal | Entry Points | CLI commands |

## Development Workflow

```
Code -> format -> lint -> type-check -> test -> commit
```

## Pre-commit Hooks

| Hook | Purpose |
|------|---------|
| {hook} | {purpose} |

## Entry Points

| Command | Module | Purpose |
|---------|--------|---------|
| {command} | {module} | {purpose} |
```

---

## Pre-Diagram Checklist

Before creating the diagram, verify:

- [ ] LOADED `/autoskillit:mermaid` skill using the Skill tool
- [ ] Using ONLY classDef styles from the mermaid skill (no invented colors)
- [ ] Diagram will include a color legend table

---

## Related Skills

- `/autoskillit:make-arch-diag` - Parent skill for lens selection
- `/autoskillit:mermaid` - MUST BE LOADED before creating diagram