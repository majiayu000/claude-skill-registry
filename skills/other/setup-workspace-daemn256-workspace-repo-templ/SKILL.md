---
name: setup-workspace
description: Configure workspace context and project settings
---

# Setup Workspace

Uses **Planner** (primary) with **Orchestrator** support. Guide the creation or update of workspace-specific context. Detects project characteristics and gathers information needed for the agentic kernel to work effectively.

**Prerequisites:** Access to project root, project files exist (at minimum a README or package manifest)

---

## Modes

### Quick Start (Minimum Viable)

For fast setup, only needs:

1. Project name and purpose
2. Stack confirmation (auto-detected)
3. Key documentation pointers

### Comprehensive

For full setup, covers all sections in the workspace context schema.

---

## Phase 1: Detection

### Scan for Project Markers

1. Look for `README.md`
2. Check for package manifests (`package.json`, `*.csproj`, `pom.xml`)
3. Look for `docs/` or `docs/adr/` directories
4. Scan for configuration files
5. Report findings

### Output

```markdown
## Context Anchors

- **Phase:** 1 — Detection

## Detected Markers

| Marker              | Found  | Details         |
| ------------------- | ------ | --------------- |
| README.md           | Yes/No | <path>          |
| Package manifest    | Yes/No | <type and path> |
| docs/ directory     | Yes/No | <structure>     |
| Configuration files | Yes/No | <list>          |

## Next Step

Confirm detection findings are correct.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human explicitly approves:

- Detection findings are correct
- No important markers were missed

---

## Phase 2: Stack Inference

### Classify Technology

1. Classify backend technology
2. Classify frontend technology
3. Identify documentation structure
4. Report inference

### Stack Categories

| Layer    | Options                            |
| -------- | ---------------------------------- |
| Backend  | .NET / Node / Java / Python / None |
| Frontend | Angular / React / Vue / None       |
| Docs     | ADR structure / Custom / None      |

### Output

```markdown
## Context Anchors

- **Phase:** 2 — Stack Inference

## Inferred Stack

| Layer    | Detection    | Confidence        |
| -------- | ------------ | ----------------- |
| Backend  | <technology> | <High/Medium/Low> |
| Frontend | <technology> | <High/Medium/Low> |
| Docs     | <structure>  | <High/Medium/Low> |

## Next Step

Confirm stack inference is correct.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human explicitly approves:

- Stack classification is correct
- Technology choices are accurately detected

---

## Phase 3: Project Identity

### Gather Project Information

1. Ask project name
2. Ask one-line purpose
3. Ask about domain terminology
4. Ask about project-specific conventions

### Output

```markdown
## Context Anchors

- **Phase:** 3 — Project Identity

## Project Identity

- **Name:** <name>
- **Purpose:** <one-line purpose>
- **Domain terms:** <key terms>
- **Conventions:** <project-specific conventions>

## Next Step

Continue to preview.

**Approval Required:** No
```

---

## Phase 4: Preview and Confirm

### Generate and Present

1. Generate workspace context from gathered information
2. Present preview of the full context file
3. Apply after approval

### Workspace Context Schema

The workspace context file contains:

- Project identity (name, purpose)
- Domain terminology
- Architecture (pattern, backend, frontend)
- Convention amendments (project-specific overrides)
- Key documentation pointers

### Output

```markdown
## Context Anchors

- **Phase:** 4 — Preview and Confirm

## Generated Workspace Context

<full preview of docs/workspace/context.md content>

## Next Step

Awaiting approval to write workspace context file.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not write the workspace context file until human explicitly approves:

- Content is accurate
- No sections are missing
- Terminology is correct

---

## Error Handling

| Error                      | Recovery                                    |
| -------------------------- | ------------------------------------------- |
| Empty project (no markers) | Ask user to describe project manually       |
| Conflicting markers        | Present all detected, ask for clarification |
| Existing context file      | Offer to update vs replace                  |
