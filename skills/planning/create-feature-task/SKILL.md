---
name: create-feature-task
description: 'This skill should be used when the user asks to "create a feature task", "set up development tracking", "plan a feature implementation", or needs to structure a new feature development with proper tracking and phases.'
version: "1.0.0"
last_updated: "2026-01-25"
python_compatibility: "3.11+"
user-invocable: true
argument-hint: "<feature_name_and_description>"
---

# Create Feature Development Task

Set up a comprehensive feature development task with proper tracking, phases, and documentation.

## Execution Steps

### 1. Parse Feature Requirements

- Extract feature name and description from arguments
- Identify key requirements and constraints
- Determine complexity and scope

### 2. Generate Task Structure

- Customize phases based on feature type
- Add specific acceptance criteria
- Include relevant technical considerations

### 3. Create Task Documentation

Create task file at `.claude/tasks/{feature-name}.md` with:

```markdown
# Feature: {Feature Name}

## Overview
{Brief description}

## Requirements
- [ ] Requirement 1
- [ ] Requirement 2

## Technical Approach
{High-level design}

## Phases

### Phase 1: Design
- [ ] Review existing patterns
- [ ] Create interface definitions
- [ ] Document edge cases

### Phase 2: Implementation
- [ ] Core functionality
- [ ] Error handling
- [ ] Integration points

### Phase 3: Testing
- [ ] Unit tests (80% minimum coverage)
- [ ] Integration tests
- [ ] Edge case coverage

### Phase 4: Documentation
- [ ] Code documentation
- [ ] Usage examples
- [ ] API documentation (if applicable)

## Acceptance Criteria
- [ ] All tests pass
- [ ] Coverage meets minimum
- [ ] Documentation complete
- [ ] Code review approved

## Context Preservation
- Initial requirements: {captured}
- Key decisions: {recorded}
- Dependencies: {identified}
- Risks: {noted}
```

### 4. Set Up Tracking

- Add task to TODO list using TaskCreate tool
- Create initial checkpoints
- Set up progress markers

## Context Preservation

When creating tasks, preserve:

- Initial requirements from user
- Key technical decisions made
- File locations involved
- Dependencies identified
- Risk factors noted

## Integration

| Step          | Command/Action                                         |
| ------------- | ------------------------------------------------------ |
| Prerequisites | Clear feature requirements                             |
| Follow-up     | Use `python-cli-architect` agent for implementation    |
| Related       | `comprehensive-test-review`, `python-pytest-architect` |

## Example Usage

```text
/create-feature-task Add user authentication with OAuth2 support
/create-feature-task Implement rate limiting for API endpoints
/create-feature-task Create CLI command for database migrations
```
