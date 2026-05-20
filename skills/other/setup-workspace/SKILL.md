---
name: setup-workspace
description: Configure workspace context and project settings.
---

# Setup Workspace

The Planner drives this workflow with Orchestrator support for process setup. Guide the creation or update of workspace-specific context by detecting project characteristics and gathering information.

**Prerequisites:** Access to project root, project files exist (at minimum a README or package manifest).

---

## Modes

- **Quick Start (Minimum Viable):** Project name, purpose, stack confirmation, key documentation pointers
- **Comprehensive:** All sections in the workspace context schema

---

## Phase 1: Detection

Scan for project markers and report findings.

### Steps

1. Look for README.md
2. Check for package manifests (package.json, \*.csproj, pom.xml)
3. Look for docs/ or docs/adr/ directories
4. Scan for configuration files
5. Report findings

### Output

```markdown
## Context Anchors

- **Phase:** Detection

## Detection Results

| Marker           | Found  | Details       |
| ---------------- | ------ | ------------- |
| README.md        | Yes/No | <details>     |
| Package manifest | Yes/No | <type>        |
| Documentation    | Yes/No | <structure>   |
| Configuration    | Yes/No | <files found> |

## Next Step

Confirm detection findings are correct.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human confirms detection findings.

---

## Phase 2: Stack Inference

Infer technology stack from detected files.

### Steps

1. Classify backend technology
2. Classify frontend technology
3. Identify documentation structure
4. Report inference

### Stack Categories

- Backend: .NET / Node / Java / Python / None
- Frontend: Angular / React / Vue / None
- Docs: ADR structure / Custom / None

### ⛔ CHECKPOINT

**STOP.** Do not proceed until human confirms stack inference.

---

## Phase 3: Project Identity

Gather project-specific information.

### Steps

1. Ask project name
2. Ask one-line purpose
3. Ask about domain terminology
4. Ask about project-specific conventions

---

## Phase 4: Preview and Confirm

Generate workspace context and get approval.

### Steps

1. Generate workspace context from gathered information
2. Present preview
3. Apply after approval

### Output

```markdown
## Context Anchors

- **Phase:** Preview and Confirm

## Generated Context

<preview summary>

## Next Step

Approve to write workspace context.

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Approve workspace context before writing.

---

## Workspace Context Schema

The workspace context file contains:

- Project identity (name, purpose)
- Domain terminology
- Architecture (pattern, backend, frontend)
- Convention amendments (project-specific overrides)
- Key documentation pointers

---

## Error Handling

| Error                      | Recovery                                    |
| -------------------------- | ------------------------------------------- |
| Empty project (no markers) | Ask user to describe project manually       |
| Conflicting markers        | Present all detected, ask for clarification |
| Existing context file      | Offer to update vs replace                  |
