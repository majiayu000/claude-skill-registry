---
name: plan
description: PLANNING PHASE - Decompose specification into task DAG with dependencies and phases. DO NOT invoke execute skill.
tools:
  - agent
  - bash
  - file_read
  - file_write
---

# Plan Workflow

**CRITICAL: This is the PLAN skill. Do NOT call Skill(execute) or Skill(tasker:execute). Follow the instructions below directly.**

**IMPORTANT: All tasker working files go in `$TARGET_DIR/.tasker/`. Do NOT create any other directories like `project-planning/`, `planning/`, or `schemas/` at the target project root. The `.tasker/` directory is the ONLY location for tasker artifacts (including `.tasker/schemas/` for JSON schemas).**

Decompose a specification into an executable task DAG. This is Phase 2 of the tasker workflow:

```
/specify → /plan → /execute
```

## Input Requirements

- **Spec** from `/specify`: `{TARGET}/docs/specs/<slug>.md`
- **Capability Map**: `{TARGET}/docs/specs/<slug>.capabilities.json`
- **FSM Artifacts** (optional): `{TARGET}/docs/state-machines/<slug>/`

## Output

- **Task DAG**: `.tasker/tasks/T001.json`, `T002.json`, etc.
- **Physical Map**: `.tasker/artifacts/physical-map.json`
- **Validation Report**: `.tasker/reports/task-validation-report.md`

---

## MANDATORY FIRST STEP: Ask for Target Project Directory

**ALWAYS ask for target_dir FIRST before anything else.** No guessing, no inference from CWD.

### Step 1: Ask for Target Directory

Use AskUserQuestion to ask:
```
What is the target project directory?
```
Free-form text input. User must provide an absolute or relative path.

**Validation:**
```bash
TARGET_DIR="<user-provided-path>"
# Convert to absolute path
TARGET_DIR=$(cd "$TARGET_DIR" 2>/dev/null && pwd || echo "$TARGET_DIR")

if [ ! -d "$TARGET_DIR" ]; then
    # For new projects, check parent exists
    PARENT=$(dirname "$TARGET_DIR")
    if [ -d "$PARENT" ]; then
        echo "Directory will be created: $TARGET_DIR"
        mkdir -p "$TARGET_DIR"
    else
        echo "Error: Parent directory does not exist: $PARENT"
        # Re-ask for target_dir
    fi
fi
```

### Step 2: Check for Existing Session and Initialize

After target_dir is confirmed, check for existing `.tasker/` state:

```bash
TASKER_DIR="$TARGET_DIR/.tasker"
if [ -f "$TASKER_DIR/state.json" ]; then
    echo "Found existing tasker session at $TASKER_DIR"
    echo "Resuming from saved state..."
    # Read phase from state.json and resume
    tasker state status
else
    echo "No existing session. Initializing..."
    # Initialize directory structure
fi
```

### Step 3: Detect Specs (Automatic)

**Specs are REQUIRED for /plan to proceed.** Check `$TARGET_DIR/docs/specs/` for specs from /specify:

```bash
SPEC_DIR="$TARGET_DIR/docs/specs"

# Find spec files (from /specify workflow)
SPEC_FILES=$(find "$SPEC_DIR" -maxdepth 1 -name "*.md" 2>/dev/null)
CAP_MAPS=$(find "$SPEC_DIR" -maxdepth 1 -name "*.capabilities.json" 2>/dev/null)

if [ -n "$SPEC_FILES" ]; then
    echo "=== Specs found ==="
    echo "$SPEC_FILES"

    # Use the first spec (or only spec)
    SPEC_PATH=$(echo "$SPEC_FILES" | head -1)
    SPEC_SLUG=$(basename "$SPEC_PATH" .md)

    # Check for matching capability map
    CAP_MAP="$SPEC_DIR/${SPEC_SLUG}.capabilities.json"
    if [ -f "$CAP_MAP" ]; then
        echo "Capability map found: $CAP_MAP"
        echo "Can skip logic-architect phase"
    fi
else
    echo "No specs found in $SPEC_DIR"
    # BLOCK - see below
fi
```

### If spec found:

Proceed to Step 4. No user question needed.

### If NO spec found — BLOCK and offer /specify:

**/plan CANNOT proceed without specs.** Present this to the user:

```markdown
## Specs Required

Planning requires a specification to decompose into tasks. Without a spec, there's nothing to plan.

**Would you like to create a spec now using `/specify`?**

The `/specify` workflow will guide you through:
1. Defining goals and scope
2. Clarifying requirements through structured questions
3. Extracting capabilities and behaviors
4. Producing a spec ready for `/plan`
```

Ask using AskUserQuestion:
```
Would you like to run /specify to create a spec now?
```
Options:
- **Yes, start /specify** — Begin the specification workflow
- **No, I'll provide a spec later** — Exit /plan for now

### Step 4: Detect Project Type (Automatic)

**Do not ask the user** — infer project type from target directory:

```bash
# Check if target directory has source code
SOURCE_FILES=$(find "$TARGET_DIR" \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" -o -name "*.java" \) \
    -not -path "*node_modules*" -not -path "*__pycache__*" -not -path "*.venv*" -not -path "*/.git/*" 2>/dev/null | head -5)

if [ -n "$SOURCE_FILES" ]; then
    PROJECT_TYPE="existing"
    echo "Detected existing project with source files"
else
    PROJECT_TYPE="new"
    echo "New project (no existing source files)"
fi
```

- **Existing project** → Proceed to Step 5 (project analysis)
- **New project** → Skip to Step 6 (tech stack)

### Step 5: Existing Project Analysis (if PROJECT_TYPE=existing)

**If enhancing an existing project**, you MUST analyze the target directory **BEFORE proceeding to ingestion**. This analysis is CRITICAL - sub-agents cannot see the codebase, so you must extract and pass this context to them.

```bash
# Check directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Target directory does not exist"
    exit 1
fi

# Analyze structure (capture output for context)
echo "=== Project Structure ==="
tree -L 3 -I 'node_modules|__pycache__|.git|venv|.venv|dist|build|.pytest_cache' "$TARGET_DIR" 2>/dev/null || \
    find "$TARGET_DIR" -maxdepth 3 -type f | head -50

# Identify key configuration files
echo "=== Key Configuration Files ==="
for f in package.json pyproject.toml Cargo.toml go.mod Makefile requirements.txt setup.py tsconfig.json; do
    [ -f "$TARGET_DIR/$f" ] && echo "Found: $f"
done

# Detect source layout patterns
echo "=== Source Layout ==="
for d in src lib app pkg cmd internal; do
    [ -d "$TARGET_DIR/$d" ] && echo "Found directory: $d/"
done

# Detect test layout
echo "=== Test Layout ==="
for d in tests test spec __tests__; do
    [ -d "$TARGET_DIR/$d" ] && echo "Found test directory: $d/"
done

# Sample existing code files to understand patterns
echo "=== Code Samples ==="
find "$TARGET_DIR" \( -name "*.py" -o -name "*.ts" -o -name "*.js" -o -name "*.go" -o -name "*.rs" \) \
    -not -path "*node_modules*" -not -path "*__pycache__*" -not -path "*.venv*" | head -10
```

**Read key files to understand patterns:**
```bash
# Read config files to understand dependencies and structure
[ -f "$TARGET_DIR/pyproject.toml" ] && cat "$TARGET_DIR/pyproject.toml"
[ -f "$TARGET_DIR/package.json" ] && cat "$TARGET_DIR/package.json"

# Sample a few source files to understand coding patterns
# (naming conventions, import style, architecture patterns)
```

### Step 6: Store Discovery Context

**CRITICAL:** You must retain this analysis for passing to sub-agents. Store it as a structured context block:

```
PROJECT_CONTEXT = """
Directory: {TARGET_DIR}
Project Type: existing
Stack: {detected stack}
Source Layout: {layout pattern}
Test Layout: {test pattern}

Key Patterns:
- {pattern 1}
- {pattern 2}
- {pattern 3}

Integration Requirements:
- {requirement 1}
- {requirement 2}
"""
```

This `PROJECT_CONTEXT` MUST be included in every sub-agent spawn prompt (logic-architect, physical-architect, task-author). Without it, sub-agents will design solutions that conflict with existing code.

---

## Directory Initialization

**CRITICAL:** After obtaining target_dir, initialize the `.tasker/` directory structure. Sub-agents assume directories already exist.

```bash
TASKER_DIR="$TARGET_DIR/.tasker"
mkdir -p "$TASKER_DIR"/{artifacts,inputs,tasks,reports,bundles,logs}
```

This creates:
- `$TARGET_DIR/.tasker/artifacts/` - For capability-map.json, physical-map.json
- `$TARGET_DIR/.tasker/inputs/` - For spec.md
- `$TARGET_DIR/.tasker/tasks/` - For T001.json, T002.json, etc.
- `$TARGET_DIR/.tasker/reports/` - For task-validation-report.md
- `$TARGET_DIR/.tasker/bundles/` - For execution bundles
- `$TARGET_DIR/.tasker/logs/` - For activity logging

---

## Runtime Logging (MANDATORY)

All orchestrator activity and sub-agent activity MUST be logged using `./scripts/log-activity.sh`.

```bash
./scripts/log-activity.sh <LEVEL> <AGENT> <EVENT> "<MESSAGE>"
```

**Parameters:**
- `LEVEL`: INFO, WARN, ERROR
- `AGENT`: orchestrator, logic-architect, physical-architect, task-author, etc.
- `EVENT`: start, decision, tool, complete, spawn, spawn-complete, phase-transition, validation
- `MESSAGE`: Description of the activity

---

## Skip Phases for /specify-Generated Specs

If the spec came from `/specify` workflow, it has already been reviewed AND capabilities have been extracted. Check for artifacts:

```bash
# Derive capability map path from spec path
SPEC_DIR=$(dirname "$SPEC_PATH")
SPEC_SLUG=$(basename "$SPEC_PATH" .md)
CAPABILITY_MAP="${SPEC_DIR}/${SPEC_SLUG}.capabilities.json"

if [ -f "$CAPABILITY_MAP" ]; then
    echo "Capability map found from /specify workflow: $CAPABILITY_MAP"
    echo "Copying artifacts and skipping to physical phase..."

    # Copy artifacts to .tasker/ directory
    cp "$CAPABILITY_MAP" "$TASKER_DIR/artifacts/capability-map.json"

    # Check for FSM artifacts from /specify workflow
    FSM_DIR="${SPEC_DIR}/../state-machines/${SPEC_SLUG}"
    if [ -d "$FSM_DIR" ]; then
        echo "FSM artifacts found from /specify workflow: $FSM_DIR"
        mkdir -p "$TASKER_DIR/artifacts/fsm"
        cp -r "$FSM_DIR"/* "$TASKER_DIR/artifacts/fsm/"
    fi

    # Skip spec_review AND logical phases - advance directly to physical
    tasker state set-phase physical
fi
```

**Skip phases when `/specify` artifacts exist:**
- `spec_review` - Skipped (already done by `/specify` Phase 7)
- `logical` - Skipped (capability map already exists from `/specify` Phase 3)

---

## Plan Phase Dispatch

```bash
# Initialize if no state exists
if [ ! -f "$TASKER_DIR/state.json" ]; then
    tasker state init "$TARGET_DIR"
fi

# Check current phase
tasker state status
```

| Phase | Agent | Output | Validation | Skip if |
|-------|-------|--------|------------|---------|
| `ingestion` | (none) | `inputs/spec.md` (verbatim) | File exists | — |
| `spec_review` | **spec-reviewer** | `artifacts/spec-review.json` | All critical resolved | `/specify` artifacts exist |
| `logical` | **logic-architect** | `artifacts/capability-map.json` | `validate capability_map` | `/specify` artifacts exist |
| `physical` | **physical-architect** | `artifacts/physical-map.json` | `validate physical_map` | — |
| `definition` | **task-author** | `tasks/*.json` | `load-tasks` | — |
| `validation` | **task-plan-verifier** | Validation report | `validate-tasks <verdict>` | — |
| `sequencing` | **plan-auditor** | Updated task phases | DAG is valid | — |
| `ready` | (done) | Planning complete | — | — |

---

## Plan Loop

```python
while phase not in ["ready", "executing", "complete"]:
    1. Query current phase
    2. Spawn appropriate agent WITH FULL CONTEXT (see spawn templates below)
    3. Wait for agent to complete
    4. **VERIFY OUTPUT EXISTS** (critical - see below)
       - DO NOT log spawn-complete until file verified
       - DO NOT proceed to validation until file verified
    5. If file missing: RE-SPAWN agent immediately (see recovery below)
    6. Validate output:
       - For artifacts: tasker state validate <artifact>
       - For task validation: tasker state validate-tasks <verdict>
    7. If valid: tasker state advance
    8. If invalid: Tell agent to fix, re-validate
```

**CRITICAL: Never log "spawn-complete: SUCCESS" until the output file is verified to exist!**

---

## Output Verification Before Validation

**MANDATORY STEP:** After each agent completes, you MUST verify its output file exists before attempting validation.

```bash
# After logic-architect completes:
if [ ! -f $TASKER_DIR/artifacts/capability-map.json ]; then
    echo "ERROR: capability-map.json not written. Agent must retry."
fi

# After physical-architect completes:
if [ ! -f $TASKER_DIR/artifacts/physical-map.json ]; then
    echo "ERROR: physical-map.json not written. Agent must retry."
fi

# After task-author completes:
task_count=$(ls $TASKER_DIR/tasks/*.json 2>/dev/null | wc -l)
if [ "$task_count" -eq 0 ]; then
    echo "ERROR: No task files written. Agent must retry."
fi
```

**Recovery procedure:** If file doesn't exist:
1. Check if directory exists: `ls -la $TASKER_DIR/artifacts/`
2. Re-spawn the agent with explicit reminder to use Write tool

---

## Agent Spawn Templates

**CRITICAL:** Each sub-agent is context-isolated. They CANNOT see the orchestrator's conversation. You MUST pass ALL relevant context explicitly in the spawn prompt.

### Physical Phase: physical-architect

```
Map behaviors to concrete file paths.

## Logging (MANDATORY)

./scripts/log-activity.sh INFO physical-architect start "Mapping behaviors to file paths"

## Context

TASKER_DIR: {absolute path to .tasker directory}
Target Directory: {TARGET_DIR}
Project Type: {new | existing}
Tech Stack: {from spec or inferred}

## Project Context (CRITICAL for existing projects)

{INSERT FULL PROJECT_CONTEXT HERE}

## Your Task

1. Read {TASKER_DIR}/artifacts/capability-map.json
2. **For existing projects:** Map behaviors to paths that FIT the existing structure
3. For new projects: Establish clean, conventional structure
4. **CRITICAL: Use the Write tool** to save to {TASKER_DIR}/artifacts/physical-map.json
5. **Verify file exists**: `ls -la {TASKER_DIR}/artifacts/physical-map.json`
6. Validate with: `cd {TASKER_DIR}/.. && tasker state validate physical_map`
```

### Definition Phase: task-author

```
Create individual task files from the physical map.

## Logging (MANDATORY)

./scripts/log-activity.sh INFO task-author start "Creating task files"

## Context

TASKER_DIR: {absolute path to .tasker directory}
Target Directory: {TARGET_DIR}
Project Type: {new | existing}

## Project Context (for existing projects)

{INSERT FULL PROJECT_CONTEXT HERE}

## Your Task

1. Read {TASKER_DIR}/artifacts/physical-map.json
2. Read {TASKER_DIR}/artifacts/capability-map.json (for behavior details)
3. **Check for FSM artifacts**: If {TASKER_DIR}/artifacts/fsm/index.json exists, add FSM context to tasks
4. **CRITICAL: Use the Write tool** to save each task file to {TASKER_DIR}/tasks/T001.json, etc.
5. **Verify files exist**: `ls -la {TASKER_DIR}/tasks/`
6. Load tasks with: `cd {TASKER_DIR}/.. && tasker state load-tasks`
```

### Validation Phase: task-plan-verifier

```
Verify task definitions for planning

## Logging (MANDATORY)

./scripts/log-activity.sh INFO task-plan-verifier start "Verifying task definitions"

## Context

TASKER_DIR: {absolute path to .tasker directory}
Spec: {TASKER_DIR}/inputs/spec.md
Capability Map: {TASKER_DIR}/artifacts/capability-map.json
Tasks Directory: {TASKER_DIR}/tasks/

## Required Command

Register verdict using: tasker state validate-tasks <VERDICT> "<summary>"
```

### Sequencing Phase: plan-auditor

```
Assign phases to tasks and validate the dependency graph.

## Logging (MANDATORY)

./scripts/log-activity.sh INFO plan-auditor start "Assigning phases and validating DAG"

## Context

TASKER_DIR: {absolute path to .tasker directory}

## Your Task

1. Read {TASKER_DIR}/tasks/*.json
2. Read {TASKER_DIR}/artifacts/capability-map.json (for steel thread flows)
3. Build dependency graph
4. Assign phases (1: foundations, 2: steel thread, 3+: features)
5. **CRITICAL: Update task files** using Write tool
6. Validate DAG (no cycles, deps in earlier phases)
7. Run: cd {TASKER_DIR}/.. && tasker state load-tasks
```

---

## Plan Completion

When phase reaches "ready":
```markdown
## Planning Complete ✓

**Tasks:** 24
**Phases:** 4
**Steel Thread:** T001 → T003 → T007 → T012

Run `/execute` to begin implementation.
```

### Archive Planning Artifacts (Automatic)

After planning completes, archive the artifacts:

```bash
tasker archive planning {project_name}
```

---

## State Commands Reference

```bash
# General
tasker state status          # Current phase, task counts
tasker state advance         # Try to advance phase

# Planning
tasker state init <dir>      # Initialize new plan
tasker state validate <art>  # Validate artifact
tasker state validate-tasks <verdict> [summary]  # Register task validation result
tasker state load-tasks      # Reload from files
```

---

## Error Recovery

If agent produces invalid output:
1. Validation fails (`tasker state validate` returns non-zero)
2. Report errors to agent
3. Agent fixes and re-outputs
4. Re-validate
5. Only advance on success
