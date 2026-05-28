# Instruction-Type Skill Template

**Purpose**: Execute tasks when user invokes via `/command` or direct skill call.

**Frontmatter Requirements**:
```yaml
---
name: example-workflow
description: Execute this when user requests workflow automation
user-invocable: true
allowed-tools: ["Read", "Glob", "Bash(git:*)", "Task"]
---
```

**Writing Style Requirements**:
- Use imperative voice: "Load...", "Create...", "Analyze...", "Execute..."
- Never use declarative descriptions: avoid "is", "are", "provides"

**Structure Requirements**:
- Phase-based workflow: "## Phase 1:", "## Phase 2:"
- Each phase has "**Goal**:" and "**Actions**:" sections
- Actions as numbered lists with clear steps
- Include linear process flow from start to completion

**Complete Template**:
```markdown
---
name: example-workflow
description: Execute this when user requests workflow automation
user-invocable: true
allowed-tools: ["Read", "Glob", "Bash(git:*)", "Task"]
---

# Workflow Execution

Execute automated workflow for $ARGUMENTS.

## Phase 1: Preparation
**Goal**: Gather inputs and validate preconditions.

**Actions**:
1. Load required knowledge skills using Skill tool
2. Gather user input and context
3. Validate all prerequisites are met
4. Proceed to execution phase

## Phase 2: Execution
**Goal**: Process inputs and generate outputs.

**Actions**:
1. Process gathered inputs according to workflow logic
2. Apply transformations or execute operations
3. Handle errors and edge cases
4. Collect results for final reporting
```
