---
name: quality-gate-manager
description: Manages quality gates and checkpoints to ensure work meets standards before proceeding to next phases. Use when you need to verify work quality, set quality standards, or decide if work is ready to proceed. Defines quality criteria, checks work against criteria, and makes go/no-go decisions.
---

# Quality Gate Manager Skill

## Instructions

1. Define quality criteria for the gate
2. Review work against criteria
3. Check if criteria are met
4. Identify any gaps or issues
5. Make go/no-go decision
6. Document gate results
7. Provide feedback for improvements if needed

## Quality Gate Process

### Step 1: Define Quality Criteria
- Identify what "ready" means for this gate
- Set specific, measurable criteria
- Define acceptance standards
- Note any exceptions or waivers

### Step 2: Review Work
- Examine work deliverables
- Check against criteria
- Verify completeness
- Assess quality

### Step 3: Evaluate Against Criteria
- Check each criterion
- Note which criteria are met
- Identify gaps
- Assess severity of gaps

### Step 4: Make Decision
- **Approve**: Work meets criteria, can proceed
- **Request Changes**: Work needs improvements before proceeding
- **Block**: Work does not meet standards, must fix

### Step 5: Document Results
- Record gate results
- Note any issues
- Provide feedback
- Track resolution

## Quality Gate Types

### Gate 1: Specification Gate
**When**: After specification is created
**Criteria**:
- Specification is complete
- Requirements are clear
- Technical approach is defined
- Dependencies identified

### Gate 2: Task Breakdown Gate
**When**: After tasks are broken down
**Criteria**:
- All requirements covered by tasks
- Tasks are atomic and modular
- Dependencies identified
- Tasks are actionable

### Gate 3: Design Gate
**When**: After design specifications are created
**Criteria**:
- Design specs are complete
- Accessibility considered
- Responsive design planned
- Design is implementable

### Gate 4: Implementation Gate
**When**: After code is implemented
**Criteria**:
- Code implements requirements
- Tests are written and passing
- Code follows standards
- Documentation is complete

### Gate 5: Review Gate
**When**: After code review
**Criteria**:
- Code review is complete
- All critical issues resolved
- Code is approved
- Ready for commit

### Gate 6: Deployment Gate
**When**: Before deployment
**Criteria**:
- All tests passing
- Code is reviewed and approved
- Documentation is complete
- Deployment plan is ready

## Quality Criteria Examples

### Specification Gate Criteria
- [ ] All requirements documented
- [ ] Technical approach defined
- [ ] Dependencies identified
- [ ] Acceptance criteria clear
- [ ] No ambiguous requirements

### Design Gate Criteria
- [ ] Design specs complete
- [ ] Accessibility requirements met
- [ ] Responsive design specified
- [ ] Design tokens defined
- [ ] Implementation-ready

### Implementation Gate Criteria
- [ ] Code implements requirements
- [ ] Unit tests written and passing
- [ ] Integration tests passing
- [ ] Code follows style guide
- [ ] Documentation complete

### Review Gate Criteria
- [ ] Code review completed
- [ ] All Must-Fix issues resolved
- [ ] All Should-Fix issues resolved (or waived)
- [ ] Code approved by reviewer
- [ ] Ready for commit

## Quality Gate Output Format

```markdown
## Quality Gate: [Gate Name]

### Gate Type
[Specification / Task Breakdown / Design / Implementation / Review / Deployment]

### Work Reviewed
[What work was reviewed]

### Quality Criteria

#### Criterion 1: [Description]
- **Status**: [Met / Not Met / Partial]
- **Notes**: [Notes on criterion]

#### Criterion 2: [Description]
- **Status**: [Met / Not Met / Partial]
- **Notes**: [Notes on criterion]

### Overall Assessment
**Status**: [Approved / Changes Requested / Blocked]

### Issues Found
- [Issue 1]: [Description and severity]
- [Issue 2]: [Description and severity]

### Feedback
[Feedback for improvements]

### Decision
**Can Proceed**: [Yes / No / After Changes]
**Required Changes**: [List of required changes]
**Next Steps**: [What needs to happen next]
```

## Examples

### Example 1: Specification Gate - Approved

**Input**: Review specification for user dashboard

**Output**:
```markdown
## Quality Gate: Specification Gate

### Gate Type
Specification

### Work Reviewed
specification-user-dashboard.md

### Quality Criteria

#### Criterion 1: All requirements documented
- **Status**: Met
- **Notes**: All functional and non-functional requirements are documented

#### Criterion 2: Technical approach defined
- **Status**: Met
- **Notes**: Technology stack, architecture, and implementation approach are clearly defined

#### Criterion 3: Dependencies identified
- **Status**: Met
- **Notes**: Dependencies on authentication, database, and API are identified

#### Criterion 4: Acceptance criteria clear
- **Status**: Met
- **Notes**: Clear acceptance criteria for each requirement

#### Criterion 5: No ambiguous requirements
- **Status**: Met
- **Notes**: All requirements are clear and unambiguous

### Overall Assessment
**Status**: Approved

### Issues Found
None

### Feedback
Specification is complete and ready for task breakdown. All criteria are met.

### Decision
**Can Proceed**: Yes
**Required Changes**: None
**Next Steps**: Proceed to scrum-master for task breakdown
```

### Example 2: Design Gate - Changes Requested

**Input**: Review design specifications for login page

**Output**:
```markdown
## Quality Gate: Design Gate

### Gate Type
Design

### Work Reviewed
Design specifications for login page (TASK-010-DESIGN)

### Quality Criteria

#### Criterion 1: Design specs complete
- **Status**: Met
- **Notes**: Layout, components, colors, and typography are specified

#### Criterion 2: Accessibility requirements met
- **Status**: Partial
- **Notes**: Most accessibility requirements met, but missing focus indicators specification

#### Criterion 3: Responsive design specified
- **Status**: Met
- **Notes**: Breakpoints and responsive behavior are defined

#### Criterion 4: Design tokens defined
- **Status**: Met
- **Notes**: Colors, spacing, and typography tokens are defined

#### Criterion 5: Implementation-ready
- **Status**: Partial
- **Notes**: Mostly ready, but missing focus indicator specs needed for implementation

### Overall Assessment
**Status**: Changes Requested

### Issues Found
- **Missing Focus Indicators**: Design specs don't specify focus indicator styles for form inputs and buttons. This is required for accessibility and implementation.

### Feedback
Design is mostly complete but needs focus indicator specifications added. Once added, design will be ready for implementation.

### Decision
**Can Proceed**: After Changes
**Required Changes**: 
- Add focus indicator specifications for form inputs
- Add focus indicator specifications for buttons
- Ensure focus indicators meet WCAG contrast requirements

**Next Steps**: Update design specs with focus indicators, then re-review
```

### Example 3: Implementation Gate - Blocked

**Input**: Review implementation of user authentication

**Output**:
```markdown
## Quality Gate: Implementation Gate

### Gate Type
Implementation

### Work Reviewed
User authentication implementation (TASK-015)

### Quality Criteria

#### Criterion 1: Code implements requirements
- **Status**: Met
- **Notes**: Code implements login and registration as specified

#### Criterion 2: Unit tests written and passing
- **Status**: Not Met
- **Notes**: Unit tests are written but 3 tests are failing

#### Criterion 3: Integration tests passing
- **Status**: Not Met
- **Notes**: Integration tests not written

#### Criterion 4: Code follows style guide
- **Status**: Met
- **Notes**: Code follows project style guide

#### Criterion 5: Documentation complete
- **Status**: Partial
- **Notes**: Code comments present but API documentation is missing

### Overall Assessment
**Status**: Blocked

### Issues Found
- **Failing Tests**: 3 unit tests are failing, indicating bugs in implementation
- **Missing Integration Tests**: Integration tests are required but not written
- **Missing API Documentation**: API documentation is required but missing

### Feedback
Implementation has several quality issues that must be resolved before proceeding:
1. Fix failing unit tests
2. Write and pass integration tests
3. Add API documentation

### Decision
**Can Proceed**: No
**Required Changes**: 
1. Fix failing unit tests (identify and fix bugs)
2. Write integration tests for authentication flow
3. Add API documentation for authentication endpoints

**Next Steps**: Fix issues and resubmit for gate review
```

## Quality Gate Workflow

### Gate Check Process
1. **Define Criteria**: Set quality criteria for gate
2. **Review Work**: Examine work deliverables
3. **Check Criteria**: Evaluate against each criterion
4. **Make Decision**: Approve, request changes, or block
5. **Document Results**: Record gate results
6. **Follow Up**: Track resolution of requested changes

### Gate Approval Levels
- **Approved**: All criteria met, can proceed
- **Changes Requested**: Minor issues, can proceed after fixes
- **Blocked**: Significant issues, must fix before proceeding

## Best Practices

- **Set Clear Criteria**: Define specific, measurable criteria
- **Be Thorough**: Check all criteria carefully
- **Be Fair**: Evaluate objectively against criteria
- **Provide Feedback**: Give clear feedback for improvements
- **Track Resolution**: Follow up on requested changes
- **Be Consistent**: Apply criteria consistently across gates
