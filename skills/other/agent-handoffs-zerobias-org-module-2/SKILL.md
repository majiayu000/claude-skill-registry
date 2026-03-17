---
name: agent-handoffs
description: Agent parameter passing, memory files, and data handoffs between agents
---

# Agent Parameter Passing Guidelines

## Core Principle

**Agents are workflow-agnostic.** They perform specific tasks regardless of which workflow invokes them.

Workflows pass parameters to agents to tell them:
- Which workflow is running
- What files to read (input)
- What files to write (output)
- Any workflow-specific context

## Standard Parameters

All agents that work with memory files MUST accept these parameters:

```typescript
interface AgentParameters {
  workflow: string;      // "create-module" | "add-operation" | "update-module"
  moduleId: string;      // "github-github" | "amazon-aws-s3"
  inputFile?: string;    // File to read from (optional if agent doesn't need input)
  outputFile: string;    // File to write to
}
```

## Memory Path Construction

**CRITICAL: Always use absolute paths for `.localmemory` to avoid issues when working from different directories.**

```bash
# Get project root (choose method based on context)
PROJECT_ROOT="$(git rev-parse --show-toplevel)"

# Standard pattern - ALWAYS use absolute paths
MEMORY_PATH="${PROJECT_ROOT}/.claude/.localmemory/${workflow}-${moduleId}"

# Examples (where PROJECT_ROOT is your project's absolute path):
# ${PROJECT_ROOT}/.claude/.localmemory/create-module-github-github/
# ${PROJECT_ROOT}/.claude/.localmemory/add-operation-github-github/
# ${PROJECT_ROOT}/.claude/.localmemory/update-module-amazon-aws-s3/
```

### For Bash Scripts

```bash
# Method 1: Using git (preferred if in git repo)
PROJECT_ROOT="$(git rev-parse --show-toplevel)"

# Method 2: Using script location (if you know the script depth)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Always construct absolute paths
MEMORY_PATH="${PROJECT_ROOT}/.claude/.localmemory/${workflow}-${moduleId}"
```

### For Agents (invoked by Claude)

Agents should always receive or construct absolute paths. When constructing paths in agent responses, use the working directory from the environment.

## Reading Input Files

```bash
# Agent receives parameters
WORKFLOW="create-module"
MODULE_ID="github-github"
INPUT_FILE="phase-01-discovery.json"

# Get project root and construct absolute paths
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
MEMORY_PATH="${PROJECT_ROOT}/.claude/.localmemory/${WORKFLOW}-${MODULE_ID}"
INPUT_PATH="${MEMORY_PATH}/${INPUT_FILE}"

# Read data
PRODUCT_PACKAGE=$(jq -r '.productPackage' "${INPUT_PATH}")
MODULE_PACKAGE=$(jq -r '.modulePackage' "${INPUT_PATH}")
```

## Writing Output Files

```bash
# Agent receives parameters
OUTPUT_FILE="phase-02-scaffolding.json"

# Get project root and construct absolute paths
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
MEMORY_PATH="${PROJECT_ROOT}/.claude/.localmemory/${WORKFLOW}-${MODULE_ID}"
OUTPUT_PATH="${MEMORY_PATH}/${OUTPUT_FILE}"

# Ensure directory exists
mkdir -p "${MEMORY_PATH}"

# Write data
cat > "${OUTPUT_PATH}" <<EOF
{
  "phase": 2,
  "name": "Module Scaffolding",
  "status": "completed",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  ...
}
EOF
```

## Agent Documentation Structure

### ❌ Wrong (Workflow-Specific)

```markdown
## Responsibilities
- Create module structure for new modules
- Read from phase-01-discovery.json
- Write to phase-02-scaffolding.json
```

### ✅ Correct (Workflow-Agnostic)

```markdown
## Responsibilities
- Create module directory structure
- Read parameters from input file
- Validate generated structure
- Write results to output file

## Required Parameters
- workflow: Workflow type
- moduleId: Module identifier
- inputFile: File containing parameters
- outputFile: File to write results

## Input File Structure
Expected fields in input file:
- productPackage: Product package name
- modulePackage: Module package name
- serviceName: Service name
```

## Invocation Examples

### From Workflow Documentation

```markdown
### Phase 2: Module Scaffolding

**Agent:** @module-scaffolder

**Invocation:**
```bash
@module-scaffolder
Parameters:
  workflow: create-module
  moduleId: github-github
  inputFile: phase-01-discovery.json
  outputFile: phase-02-scaffolding.json
```
```

### Multiple Workflows Using Same Agent

**Create Module Workflow:**
```bash
@api-architect
Parameters:
  workflow: create-module
  moduleId: github-github
  inputFile: phase-01-discovery.json
  outputFile: phase-03-api-spec.json
```

**Add Operation Workflow:**
```bash
@api-architect
Parameters:
  workflow: add-operation
  moduleId: github-github
  inputFile: operation-spec.json
  outputFile: updated-api-spec.json
```

Same agent, different parameters!

## File Naming in Workflows

Workflows specify exact file names based on their phase structure:

**Create Module:**
- Phase 1: `phase-01-discovery.json`
- Phase 2: `phase-02-scaffolding.json`
- Phase 3: `phase-03-api-spec.json`
- etc.

**Add Operation:**
- Step 1: `operation-definition.json`
- Step 2: `api-spec-update.json`
- Step 3: `implementation-plan.json`
- etc.

**Update Module:**
- Step 1: `operations-list.json`
- Step 2: `update-plan.json`
- etc.

## Agent Flexibility

Agents should be flexible about input structure:

```typescript
// Agent reads what it needs
const productPackage = input.productPackage;
const modulePackage = input.modulePackage;

// If field doesn't exist, agent reports error
if (!productPackage) {
  throw new Error("Required field 'productPackage' missing from input file");
}
```

## Workflow Responsibility

**Workflows are responsible for:**
1. Creating memory directories
2. Passing correct parameters to agents
3. Ensuring output from one phase matches input expected by next phase
4. Orchestrating agent sequence
5. Error handling and recovery

**Agents are responsible for:**
1. Accepting standard parameters
2. Reading from specified input file
3. Performing their specific task
4. Writing to specified output file
5. Reporting errors if parameters/input invalid

## Benefits

✅ **Reusability**: Same agent works across multiple workflows
✅ **Testability**: Agents can be tested independently with different parameters
✅ **Maintainability**: Agent changes don't affect workflow structure
✅ **Flexibility**: New workflows can use existing agents
✅ **Clarity**: Clear separation of concerns

## Anti-Patterns

### ❌ Hardcoding Workflow Type
```bash
# BAD
if [ "$WORKFLOW" == "create-module" ]; then
  # Special logic for create
fi
```

Agents should not have workflow-specific logic. If needed, workflows should pass different parameters.

### ❌ Hardcoding File Paths
```bash
# BAD - Relative path
INPUT=".claude/.localmemory/create-module-${MODULE_ID}/phase-01-discovery.json"

# BAD - Hardcoded workflow
INPUT="${PROJECT_ROOT}/.claude/.localmemory/create-module-${MODULE_ID}/phase-01-discovery.json"

# GOOD - Absolute path with parameters
PROJECT_ROOT="$(git rev-parse --show-toplevel)"
INPUT="${PROJECT_ROOT}/.claude/.localmemory/${WORKFLOW}-${MODULE_ID}/${INPUT_FILE}"
```

Always construct absolute paths from parameters.

### ❌ Hardcoding Phase Numbers
```bash
# BAD
echo '{"phase": 2, ...}'
```

Extract phase info from parameters or workflow context if needed.

## Migration Guide

### Old Style (Workflow-Specific)
```markdown
**File:** `.claude/.localmemory/create-{module-id}/phase-02-scaffolding.json`

Read from: `.claude/.localmemory/create-{module-id}/phase-01-discovery.json`
```

### New Style (Workflow-Agnostic)
```markdown
**Input File:** Specified by workflow (e.g., phase-01-discovery.json)
**Output File:** Specified by workflow (e.g., phase-02-scaffolding.json)

**Example Paths:**
- Input: `.claude/.localmemory/{workflow}-{moduleId}/{inputFile}`
- Output: `.claude/.localmemory/{workflow}-{moduleId}/{outputFile}`
```

## Summary

- Agents receive parameters, not hardcoded values
- Workflows control file naming and sequencing
- Agents work across any workflow that provides correct parameters
- Clear separation: workflows orchestrate, agents execute
