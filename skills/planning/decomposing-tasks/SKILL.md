---
name: decomposing-tasks
description: Break down large tasks into smaller, actionable items. Use when planning sprints, estimating work, or creating implementation plans. Covers task breakdown strategies.
allowed-tools: Read, Write, Glob, Grep
---

# Decomposing Tasks

## Workflows

- [ ] **Understand Scope**: What is the full scope of work?
- [ ] **Identify Components**: What are the major pieces?
- [ ] **Break Down**: Split into 1-2 day tasks
- [ ] **Order**: Define dependencies and sequence
- [ ] **Validate**: Can each task be demo'd/tested?

## Task Size Guidelines

### Too Big
- "Build the authentication system"
- Cannot be completed in 1-2 days
- Cannot be tested independently

### Just Right
- "Create login API endpoint"
- "Add password validation"
- "Implement JWT token generation"

### Too Small
- "Add semicolon"
- "Rename variable"
- Not worth tracking separately

## Decomposition Strategies

### Vertical Slicing
Cut through all layers for one feature.

```
Feature: User Login
├── API endpoint (POST /login)
├── Input validation
├── Database query
├── JWT generation
├── Error handling
└── Integration test
```

### Horizontal Slicing
Complete one layer at a time.

```
Database Layer
├── Users table
├── Sessions table
└── Indexes

API Layer
├── Login endpoint
├── Logout endpoint
└── Refresh endpoint
```

### SPIDR Method

- **Spike**: Research/investigation task
- **Path**: Main flow implementation
- **Interface**: API/UI contract
- **Data**: Storage and schemas
- **Rules**: Business logic and validation

## Task Template

```markdown
## Task: [Title]

**Description**: [What needs to be done]

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Dependencies**: [What must be done first]

**Estimate**: [X hours/points]
```

## Definition of Done

Every task should have:
- [ ] Code complete and reviewed
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Deployed to staging
