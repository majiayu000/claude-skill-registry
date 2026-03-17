---
name: tasker-to-beads
description: Transform Tasker task definitions into rich, self-contained Beads issues. Bridges ephemeral execution units with persistent planning artifacts.
tools:
  - bash
  - file_read
  - file_write
  - ask_user
---

# Tasker to Beads Transformer

Converts Tasker task definitions into enriched Beads issues that are **self-contained** and **human-readable**. This skill performs the "neural" work of understanding spec context, synthesizing narratives, and creating issues that stand alone.

## When to Use

- After completing Tasker `/plan` phase (state is "ready")
- When you want to track implementation progress in Beads
- When multiple people/agents will work on tasks and need persistent context

## Prerequisites

1. Tasker planning complete (`.tasker/state.json` exists, phase is "ready")
2. A target directory for development (beads will be initialized there if needed)

## Target Directory Concept

The **source project** (where tasker planning lives) may be different from the **target project** (where development happens). For example:

- **Source**: `~/projects/tasker/` - contains spec, planning artifacts, task definitions
- **Target**: `~/projects/fathom/` - where the actual Elixir project will be built

When invoked, this skill will:
1. **Ask for the target directory** if not provided
2. **Initialize beads** in the target directory if not already done
3. **Create issues** in the target project's beads system

---

## Workflow

### Step 0: Determine Target Directory

**IMPORTANT:** Before proceeding, ask the user where development will happen:

> "Where would you like to create the Beads issues? This should be the directory where the actual development will take place (e.g., the project repository being built)."

Common scenarios:
- **Same directory**: Use current project (e.g., adding features to existing codebase)
- **New directory**: Create issues in a separate project (e.g., building a new project from a spec)

### Step 1: Initialize Target (if needed)

```bash
# Check status and see if target needs initialization
tasker transform status -t /path/to/target

# Initialize beads in target directory with custom prefix
# This runs: bd init <PREFIX> && bd onboard
tasker transform init-target /path/to/target FATHOM
```

The `init-target` command runs two steps:
1. `bd init <PREFIX>` - Creates the `.beads` directory structure
2. `bd onboard` - Sets up project configuration and initial state

### Step 2: Prepare Context

```bash
tasker transform context --all -t /path/to/target
```

This extracts structural data from task files and saves context bundles to `.tasker/beads-export/`.

### Step 3: Enrich Each Task (LLM Work)

For each task, read the context file and generate an enriched issue description.

**Read the context:**
```bash
cat .tasker/beads-export/{TASK_ID}-context.json
```

**Generate enriched content using the template below**, then save:
```bash
# Save to .tasker/beads-export/{TASK_ID}-enriched.json
```

### Step 4: Create Beads Issues

After enrichment, create issues in the target directory:
```bash
tasker transform create {TASK_ID} .tasker/beads-export/{TASK_ID}-enriched.json -t /path/to/target
```

Or batch create from manifest:
```bash
tasker transform batch-create .tasker/beads-export/manifest.json -t /path/to/target
```

---

## Enrichment Template

When generating enriched issue content, produce JSON with this structure:

```json
{
  "task_id": "T001",
  "title": "Initialize Mix project with OTP dependencies",
  "priority": "critical",
  "labels": ["domain:infrastructure", "phase:1", "steel-thread"],
  "dependencies": [],
  "description": "... rich markdown description ..."
}
```

### Description Format

The description should be **self-contained** markdown with these sections:

```markdown
## Overview

[1-2 sentences explaining WHAT this task accomplishes and WHY it matters to the project]

## Spec Context

[Relevant excerpts from the specification that drive this task. Include enough context that someone can understand the requirement without reading the full spec.]

> "Direct quote from spec if available"

[Your synthesis of what the spec requires]

## Architecture Context

**Domain:** [domain name]
**Capability:** [capability name]

[Explain how this fits into the system architecture. What role does it play? What does it enable?]

## Implementation Approach

[Narrative description of how to implement this. Not just file paths, but the approach and key decisions.]

### Files to Create/Modify

| File | Purpose |
|------|---------|
| `path/to/file.ex` | Brief purpose |

## Dependencies

[If this task depends on others, explain WHAT it needs from them, not just the ID]

- **T003 (Core data schemas):** Provides the `Session` and `Message` structs used here
- **T005 (Tool behaviour):** Defines the `Tool` behaviour this implements

## Acceptance Criteria

Human-readable checklist (not raw verification commands):

- [ ] Project compiles without warnings
- [ ] All required dependencies are declared in mix.exs
- [ ] Basic module structure is in place
- [ ] Tests pass (if applicable)

## Notes

[Any additional context, gotchas, or considerations]
```

---

## Enrichment Prompts

When processing each task context, use this reasoning approach:

### 1. Understand the Task's Purpose

Read the task name, context, and behaviors. Ask:
- What problem does this solve?
- Why does this exist in the system?
- What would be missing without it?

### 2. Extract Spec Relevance

From `relevant_spec_sections` in the context:
- Find the most relevant 1-2 sections
- Extract key quotes that define the requirement
- Synthesize the requirement in your own words

### 3. Explain Architecture Fit

From `capability_context`:
- Describe the domain and capability this belongs to
- Explain how the behaviors contribute to the capability
- Connect to the broader system design

### 4. Narrate Dependencies

From `dependency_context`:
- For each dependency, explain what this task USES from it
- Make the dependency relationship meaningful, not just structural

### 5. Humanize Acceptance Criteria

From `task.acceptance_criteria`:
- Convert verification commands to human-readable checks
- Add implicit criteria (code quality, tests, documentation)
- Make them checkable by a human reviewer

---

## Single-Task Mode

To transform a single task:

```bash
# 1. Prepare context
tasker transform context T001

# 2. Read and understand
cat .tasker/beads-export/T001-context.json

# 3. Generate enriched content (you do this)
# ... apply the enrichment template ...
# Save to .tasker/beads-export/T001-enriched.json

# 4. Create the issue in target directory
tasker transform create T001 .tasker/beads-export/T001-enriched.json -t /path/to/target
```

---

## Batch Mode

To transform all tasks:

```bash
# 1. Check status and determine target
tasker transform status -t /path/to/target

# 2. Prepare all contexts
tasker transform context --all

# 3. For each context file, generate enriched content
# This is the neural loop - process each T*-context.json

# 4. Create manifest with all enriched issues
# Save to .tasker/beads-export/manifest.json with structure:
# { "issues": [ {...enriched issue 1...}, {...enriched issue 2...}, ... ] }

# 5. Batch create in target directory
tasker transform batch-create .tasker/beads-export/manifest.json -t /path/to/target
```

---

## Manifest Format

For batch creation, the manifest should be:

```json
{
  "created_at": "2025-01-15T10:00:00Z",
  "source": "tasker",
  "task_count": 47,
  "issues": [
    {
      "task_id": "T001",
      "title": "Initialize Mix project with OTP dependencies",
      "priority": "critical",
      "labels": ["domain:infrastructure", "phase:1", "steel-thread"],
      "dependencies": [],
      "description": "## Overview\n\n..."
    },
    {
      "task_id": "T002",
      "title": "...",
      ...
    }
  ]
}
```

---

## Quality Checklist

Before creating an issue, verify:

- [ ] Title is concise but descriptive (not just the task name)
- [ ] Overview explains WHY, not just WHAT
- [ ] Spec context includes actual quotes/references
- [ ] Architecture context explains the system role
- [ ] Dependencies are explained narratively
- [ ] Acceptance criteria are human-checkable
- [ ] Description stands alone (no external context needed)

---

## Example: T001 Enrichment

**Input context (abbreviated):**
```json
{
  "task_id": "T001",
  "task": {
    "name": "Mix project initialization",
    "phase": 1,
    "context": {
      "domain": "Infrastructure",
      "capability": "Project Setup",
      "steel_thread": true
    },
    "files": [{"path": "mix.exs", "action": "create"}],
    "acceptance_criteria": [
      {"criterion": "mix compile succeeds", "verification": "mix compile"}
    ]
  },
  "relevant_spec_sections": [
    "## Tech Stack\n\nThe agent framework uses Elixir with OTP patterns..."
  ]
}
```

**Output enriched (abbreviated):**
```json
{
  "task_id": "T001",
  "title": "Initialize Elixir/OTP project foundation",
  "priority": "critical",
  "labels": ["domain:infrastructure", "phase:1", "steel-thread"],
  "dependencies": [],
  "description": "## Overview\n\nEstablish the foundational Mix project structure for the Fathom agent framework. This is the critical first step that all other tasks depend on, providing the build system, dependency management, and basic project layout.\n\n## Spec Context\n\n> \"The agent framework uses Elixir with OTP patterns for fault-tolerant, distributed agent coordination.\"\n\nThe specification mandates Elixir/OTP as the implementation technology, leveraging its supervision trees, GenServers, and distribution capabilities for building resilient agent systems.\n\n## Architecture Context\n\n**Domain:** Infrastructure\n**Capability:** Project Setup\n\nThis task creates the skeleton that all other infrastructure and application code builds upon. It establishes:\n- Dependency versions (ecto, phoenix_pubsub, telemetry, etc.)\n- Compilation settings and warnings configuration\n- Project metadata and structure\n\n## Implementation Approach\n\nCreate a standard Mix project with umbrella-ready structure. Key dependencies include:\n- `ecto` + `postgrex` for persistence\n- `phoenix_pubsub` for inter-process messaging\n- `telemetry` + `opentelemetry` for observability\n- `libcluster` for node discovery\n\n### Files to Create/Modify\n\n| File | Purpose |\n|------|---------|\n| `mix.exs` | Project definition, dependencies, compilation settings |\n| `.formatter.exs` | Code formatting rules |\n| `.gitignore` | Standard Elixir ignores |\n| `README.md` | Project documentation |\n\n## Dependencies\n\nNone - this is the foundation task.\n\n## Acceptance Criteria\n\n- [ ] `mix deps.get` fetches all dependencies successfully\n- [ ] `mix compile --warnings-as-errors` passes\n- [ ] `mix format --check-formatted` passes\n- [ ] All required dependencies declared (ecto, postgrex, phoenix_pubsub, telemetry, libcluster, etc.)\n\n## Notes\n\nThis is on the **steel thread** path - it must complete before any other work can proceed. Keep the initial setup minimal but complete; don't add optional dependencies that aren't immediately needed."
}
```
