# Instruction-Type Skill Template

**Purpose**: Execute tasks when user invokes via `/command` or direct skill call.

**Frontmatter Requirements**:
```yaml
---
name: skill-name
description: Execute this when user requests [workflow/task description]
user-invocable: true
allowed-tools: ["Read", "Glob", "Bash(git:*)", "Task", ...]
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
name: skill-name
description: Execute this when user requests [workflow/task description]
user-invocable: true
allowed-tools: ["Read", "Glob", "Bash(git:*)", "Task", ...]
---

# [Workflow/Task Title]

Execute automated workflow for $ARGUMENTS.

## Initialization (Optional)

[Environment setup, prerequisites, or configuration steps needed before workflow execution.]

**Actions**:
1. [Setup step 1]
2. [Setup step 2]

## Background Knowledge (Optional)

[Domain knowledge, context, or reference information required to execute this workflow effectively.]

- **[Knowledge Item 1]**: [Brief explanation]
- **[Knowledge Item 2]**: [Brief explanation]

## Phase 1: [Phase Name]
**Goal**: [What this phase accomplishes].

**Actions**:
1. [Action step 1]
2. [Action step 2]
3. [Action step 3]
4. [Action step 4]

## Phase 2: [Phase Name]
**Goal**: [What this phase accomplishes].

**Actions**:
1. [Action step 1]
2. [Action step 2]
3. [Action step 3]
4. [Action step 4]

## Phase N: [Final Phase Name]
**Goal**: [What this phase accomplishes].

**Actions**:
1. [Action step 1]
2. [Action step 2]
3. [Action step 3]
```
