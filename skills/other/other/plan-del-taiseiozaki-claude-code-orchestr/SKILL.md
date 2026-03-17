---
name: plan
description: Create a detailed implementation plan for a feature or task. Use when user wants to plan before coding.
disable-model-invocation: true
---

# Create Implementation Plan

Create an implementation plan for $ARGUMENTS.

## Planning Process

### 1. Requirements Analysis

First clarify:

- **Purpose**: What to achieve
- **Scope**: What to include, what to exclude
- **Constraints**: Technical, time, dependencies

### 2. Current State Investigation

Investigate the codebase:

```
- Related existing code
- Files affected
- Libraries/patterns to use
- Existing tests
```

### 3. Break Down Implementation Steps

Break into small steps:

1. Each step is independently testable
2. Consider dependency order
3. High-risk steps first

### 4. Output Format

```markdown
## Implementation Plan: {Title}

### Purpose
{1-2 sentences}

### Scope
- New files: {list}
- Modified files: {list}
- Dependencies: {list}

### Implementation Steps

#### Step 1: {Title}
- [ ] {Specific task}
- [ ] {Specific task}
**Verification**: {Completion criteria for this step}

#### Step 2: {Title}
...

### Risks & Considerations
- {Potential issues and mitigations}

### Open Questions
- {Items to clarify before implementation}
```

## Notes

- Plans should be at actionable granularity
- Include verification method for each step
- Ask questions at planning stage for unclear points
- Don't over-detail (adjust during implementation)
