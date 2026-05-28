---
name: workflow-completion
description: Workflow completion standards and success criteria
---

# Workflow Execution Rules

## Phase Execution

1. **Sequential Processing**: Execute phases in order
2. **Context Passing**: Read previous phase outputs
3. **Progress Tracking**: Write phase outputs
4. **Gate Validation**: Check before proceeding
5. **Completion**: Create final artifacts

## Task Execution Rules

### Single Task Execution
- Execute ONLY the requested task
- Stop and return control after completion
- Do NOT auto-continue to next tasks
- Wait for explicit instruction

### Failure Handling
- Stop immediately on failure
- Report issue clearly
- Do NOT attempt to fix without permission
- Return control to user

## Gate Validation

Required gates in order:
1. **API Specification**: Valid OpenAPI spec
2. **Type Generation**: Types compile
3. **Implementation**: Code complete
4. **Test Creation**: Tests written
5. **Test Execution**: Tests pass
6. **Build**: Project builds

## Breaking Changes Policy

### Update Workflows
- NO breaking changes allowed
- Preserve ALL existing functionality
- Fail fast on regressions
- Maintain backward compatibility

### Fix Workflows
- Breaking changes permitted
- May modify functionality
- Document all changes
- Version bump required
