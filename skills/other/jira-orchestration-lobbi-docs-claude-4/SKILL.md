---
name: Jira Orchestration Workflow
description: This skill should be used when the user asks to "orchestrate jira", "work on issue", "complete jira ticket", "development workflow", "jira automation", "issue lifecycle", "work on story", "fix bug ticket", or needs guidance on coordinating development work through Jira with multi-agent orchestration patterns.
version: 1.0.0
---

# Jira Orchestration Workflow

Coordinate development work through Jira tickets using the 6-phase orchestration protocol with intelligent agent selection and progress tracking.

## When to Use This Skill

Activate this skill when:
- Starting work on a Jira issue (Bug, Story, Task, Epic)
- Automating development workflows through Jira
- Need to track progress and link commits/PRs to issues
- Coordinating multi-agent work on complex tickets
- Managing issue lifecycle from assignment to completion

## The 6-Phase Development Workflow

Execute all Jira-related development work through this mandatory protocol:

```
EXPLORE → PLAN → CODE → TEST → FIX → COMMIT
```

### Phase 1: EXPLORE (2+ agents)

**Objective:** Understand the issue, gather context, identify dependencies.

**Activities:**
1. Fetch issue details from Jira (summary, description, acceptance criteria)
2. Review linked issues, sub-tasks, and parent epics
3. Analyze recent comments and attachments
4. Identify codebase areas affected
5. Check for similar resolved issues
6. Review relevant documentation

**Agent Selection:**
- `code-analyst` - Analyze affected codebase areas
- `requirements-analyzer` - Parse acceptance criteria and requirements
- `dependency-mapper` - Identify dependencies and blockers

**Outputs:**
- Issue analysis document
- Affected files list
- Dependency map
- Risk assessment

**Jira Updates:**
- Transition to "In Progress"
- Add comment: "Analysis phase started by AI orchestration"
- Log estimated effort (update story points if needed)

### Phase 2: PLAN (1-2 agents)

**Objective:** Create implementation strategy and task breakdown.

**Activities:**
1. Design solution approach
2. Break down work into subtasks
3. Identify test scenarios
4. Plan file changes and new files
5. Define success criteria
6. Create DAG for parallel execution

**Agent Selection (based on issue type):**
- **Bug:** `critical-bug-analyzer`, `root-cause-investigator`
- **Story:** `feature-architect`, `code-architect`
- **Task:** `technical-planner`, `implementation-strategist`
- **Epic:** `epic-decomposer`, `strategic-planner`

**Outputs:**
- Implementation plan
- Task breakdown (DAG)
- Test plan
- Rollback strategy

**Jira Updates:**
- Create sub-tasks if needed
- Add plan as comment
- Update time estimate
- Tag relevant stakeholders

### Phase 3: CODE (2-4 agents)

**Objective:** Implement the planned solution with parallel execution.

**Activities:**
1. Execute DAG tasks in parallel where possible
2. Implement changes to existing files
3. Create new files as needed
4. Follow coding standards and best practices
5. Add inline documentation
6. Implement error handling

**Agent Selection (based on technology):**
- **Backend:** `backend-developer`, `api-specialist`, `database-expert`
- **Frontend:** `frontend-developer`, `ui-specialist`, `component-builder`
- **DevOps:** `infra-engineer`, `deployment-specialist`, `config-manager`
- **Full-stack:** Combination of above

**Outputs:**
- Implemented code changes
- New files created
- Updated configurations
- Migration scripts (if needed)

**Jira Updates:**
- Add progress comments with % completion
- Update work log with time spent
- Flag blockers immediately if encountered

### Phase 4: TEST (2-3 agents)

**Objective:** Validate implementation meets acceptance criteria.

**Activities:**
1. Run unit tests (existing + new)
2. Run integration tests
3. Execute E2E tests for affected flows
4. Manual testing against acceptance criteria
5. Performance testing (if relevant)
6. Security scanning (if relevant)

**Agent Selection:**
- `test-engineer` - Write and execute tests
- `qa-specialist` - Validate acceptance criteria
- `integration-tester` - Test cross-system interactions

**Outputs:**
- Test results
- Coverage report
- Performance metrics
- Security scan results

**Jira Updates:**
- Add test results as comment
- Attach test reports/screenshots
- Update "Testing Done" checklist

**Failure Handling:**
- If tests fail, return to FIX phase
- Do NOT mark issue complete
- Log failure details in Jira

### Phase 5: FIX (1-2 agents)

**Objective:** Address test failures and code review feedback.

**Activities:**
1. Analyze test failures
2. Debug and fix issues
3. Address code review comments
4. Refactor as needed
5. Re-run tests until passing
6. Update documentation

**Agent Selection:**
- `debugger` - Fix test failures
- `code-reviewer` - Self-review changes
- `refactoring-specialist` - Improve code quality

**Outputs:**
- Fixed code
- Updated tests
- Refactored implementations

**Jira Updates:**
- Log fixes in comments
- Update work log
- Re-run test phase

**Loop Condition:**
- Return to TEST phase after fixes
- Maximum 3 FIX iterations before escalation

### Phase 6: COMMIT (1-2 agents)

**Objective:** Create PR, link to Jira, prepare for review.

**Activities:**
1. Create feature branch (if not exists)
2. Commit changes with Jira issue key
3. Push to remote repository
4. Create pull request
5. Link PR to Jira issue
6. Request human review
7. Update documentation

**Agent Selection:**
- `git-specialist` - Handle git operations
- `pr-creator` - Create well-formatted PRs
- `documentation-writer` - Update docs

**Outputs:**
- Git commits with issue key
- Pull request
- Updated documentation
- Jira issue linked to PR

**Commit Message Format:**
```
[ISSUE-KEY] Brief description of change

Detailed explanation of what was changed and why.

Changes:
- Change 1
- Change 2

Resolves: ISSUE-KEY
```

**PR Description Format:**
```markdown
## Summary
Brief summary of changes

## Related Jira Issue
[ISSUE-KEY](link-to-jira-issue)

## Changes Made
- Change 1
- Change 2

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing complete

## Screenshots (if applicable)
Add screenshots

## Checklist
- [ ] Code follows project standards
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
```

**Jira Updates:**
- Add PR link as comment
- Transition to "In Review"
- Assign to reviewer
- Set "Fix Version" if applicable

## Agent Selection Strategy

Choose agents based on issue characteristics:

### By Issue Type

| Issue Type | Primary Agents | Secondary Agents |
|------------|----------------|------------------|
| **Bug** | `critical-bug-analyzer`, `debugger` | `root-cause-investigator`, `test-engineer` |
| **Story** | `feature-architect`, `code-architect` | `frontend-developer`, `backend-developer` |
| **Task** | `technical-planner`, `implementation-strategist` | Technology-specific agents |
| **Epic** | `epic-decomposer`, `strategic-planner` | Break into Stories first |
| **Spike** | `research-specialist`, `poc-developer` | Domain experts |

### By Technology Stack

| Stack | Agent Categories |
|-------|------------------|
| **Frontend** | `react-specialist`, `ui-developer`, `component-builder` |
| **Backend** | `api-specialist`, `database-expert`, `service-developer` |
| **DevOps** | `infra-engineer`, `k8s-specialist`, `cicd-expert` |
| **Full-stack** | Combination of above |
| **Mobile** | `mobile-developer`, `native-specialist` |

### By Priority Level

| Priority | Considerations |
|----------|----------------|
| **Blocker** | Use `critical-bug-analyzer`, escalate quickly, involve humans early |
| **Critical** | Use senior agents, enable extended thinking, parallel execution |
| **High** | Standard agent selection, follow all phases |
| **Medium** | Standard workflow, optimize for efficiency |
| **Low** | Simpler agents, batch with similar work |

## Handling Blockers and Escalation

### Blocker Identification

Mark as blocker when:
- Missing requirements or unclear acceptance criteria
- Dependency on another team/issue
- Technical limitation discovered
- Security/compliance concern
- Breaking change required

### Blocker Response

1. **Immediate Actions:**
   - Update Jira issue status
   - Add "Blocked" label
   - Create detailed blocker comment
   - Link blocking issue (if exists)
   - Notify relevant stakeholders

2. **Create Blocker Report:**
```markdown
## Blocker Identified

**Type:** [Missing Requirement | Dependency | Technical | Security]

**Description:**
Detailed description of blocker

**Impact:**
How this blocks progress

**Proposed Resolution:**
Suggested way to unblock

**Requires Action From:**
@stakeholder-name

**Estimated Unblock Time:**
X hours/days
```

3. **Checkpoint Current Progress:**
   - Save all work completed so far
   - Document what remains
   - Create recovery plan

### Escalation Triggers

Escalate to humans when:
- Blocker persists > 4 hours
- Technical decision beyond agent authority
- Security vulnerability discovered
- Breaking change affects multiple teams
- Customer impact identified
- Legal/compliance question
- Budget/resource constraint

### Escalation Process

1. Pause orchestration
2. Document all context
3. Create escalation comment in Jira
4. Tag appropriate humans
5. Transition issue to "Waiting for Support"
6. Set reminder to check status

## Human Review and Collaboration

### When to Involve Humans

**Always involve humans for:**
- Security-related changes
- Breaking API changes
- Database migrations
- Infrastructure changes
- Customer-facing features
- Regulatory/compliance work

**Optional human involvement:**
- Standard bug fixes (post-review)
- Documentation updates (post-review)
- Test additions (post-review)
- Refactoring (post-review)

### Review Request Format

```markdown
## Review Request: [ISSUE-KEY]

**Issue Type:** Bug/Story/Task
**Priority:** High/Medium/Low
**Complexity:** High/Medium/Low

**Summary:**
Brief description of changes

**Changes Made:**
- List of changes

**Testing:**
- Test results
- Coverage: X%

**Review Focus Areas:**
- Area 1 to review carefully
- Area 2 to review carefully

**Timeline:**
Needs review by: [date]

**AI Confidence:**
High/Medium/Low confidence in solution
```

## Progress Tracking and Reporting

### Real-time Updates

Update Jira automatically at:
- Phase transitions
- Blocker identification
- Test failures
- PR creation
- Each hour of active work

### Progress Indicators

Track metrics:
- **Velocity:** Story points completed per sprint
- **Cycle Time:** Time from "In Progress" to "Done"
- **Lead Time:** Time from creation to completion
- **Work Log:** Actual time spent per phase

### Status Comments

Add structured comments:

```markdown
## Progress Update - Phase: CODE

**Completed:**
- ✅ Task 1
- ✅ Task 2

**In Progress:**
- 🔄 Task 3 (60% complete)

**Blocked:**
- ❌ Task 4 (waiting on API access)

**Next Steps:**
- Continue Task 3
- Start Task 5 after Task 3

**Time Spent:** 2h 30m
**Estimated Remaining:** 1h 30m
```

## PR Creation and Jira Linking

### PR Title Format

```
[ISSUE-KEY] Brief description

Examples:
[PROJ-123] Fix authentication bug in login flow
[PROJ-456] Add user profile management feature
[PROJ-789] Update documentation for API endpoints
```

### Automatic Jira Linking

**In Commit Messages:**
```
[PROJ-123] Implement user authentication

- Add JWT token generation
- Implement login endpoint
- Add password hashing

Resolves: PROJ-123
```

**In PR Description:**
- Include issue key in title
- Link to Jira issue
- Reference issue in description
- Use Jira smart commits

### Smart Commits

Use Jira smart commits for automation:

```
[PROJ-123] #comment Added authentication tests
[PROJ-123] #time 2h 30m Work on authentication
[PROJ-123] #transition In Review
```

### Branch Naming

```
[type]/[issue-key]-[short-description]

Examples:
feature/PROJ-123-user-authentication
bugfix/PROJ-456-login-timeout
hotfix/PROJ-789-security-patch
```

## Best Practices

### Phase Execution

1. **Never skip phases** - Each phase has critical validations
2. **Checkpoint between phases** - Save state for recovery
3. **Parallel execution** - Run independent tasks concurrently
4. **Context preservation** - Maintain full context across phases
5. **Validation gates** - Verify outputs before phase transition

### Agent Coordination

1. **Minimum 3-5 agents** - Complex work requires specialization
2. **Maximum 13 agents** - Avoid coordination overhead
3. **Clear ownership** - Each agent owns specific outputs
4. **Communication protocol** - Agents share via structured artifacts
5. **Conflict resolution** - Master orchestrator resolves conflicts

### Jira Hygiene

1. **Frequent updates** - Update Jira throughout workflow
2. **Work logging** - Track actual time spent
3. **Linking** - Link all related issues, PRs, commits
4. **Labels** - Use consistent labels for categorization
5. **Components** - Tag appropriate components
6. **Sprint management** - Update sprint progress

### Quality Gates

Pass all gates before completion:

- [ ] All tests passing (unit, integration, E2E)
- [ ] Code coverage meets threshold (>80%)
- [ ] No security vulnerabilities
- [ ] No breaking changes (or documented)
- [ ] Documentation updated
- [ ] PR created and linked
- [ ] Human review requested
- [ ] Acceptance criteria met

## Issue Type Workflows

### Bug Workflow

```
1. EXPLORE: Reproduce bug, identify root cause
2. PLAN: Design fix, avoid regressions
3. CODE: Implement fix
4. TEST: Verify fix, add regression test
5. FIX: Address edge cases
6. COMMIT: Create hotfix PR
```

**Special Considerations:**
- Add regression tests
- Check for similar bugs
- Update error messages
- Document resolution

### Story Workflow

```
1. EXPLORE: Understand requirements, review designs
2. PLAN: Break into subtasks, design architecture
3. CODE: Implement feature components
4. TEST: Validate all acceptance criteria
5. FIX: Refine based on feedback
6. COMMIT: Create feature PR with docs
```

**Special Considerations:**
- Create comprehensive tests
- Update user documentation
- Consider UX implications
- Plan for future iterations

### Epic Workflow

```
1. EXPLORE: Decompose into Stories
2. Create Stories: Break epic into manageable stories
3. For each Story: Run standard Story workflow
4. Integration: Ensure stories work together
5. COMMIT: Create integration PR
```

**Special Considerations:**
- Don't implement epics directly
- Create sub-stories first
- Track epic-level progress
- Coordinate across stories

## Examples

### Example 1: Bug Fix

```bash
# Issue: PROJ-123 "Login timeout after 5 minutes"

# Phase 1: EXPLORE
Agents: [code-analyst, security-specialist]
- Analyzed authentication code
- Identified JWT token expiry issue
- Found session cleanup bug

# Phase 2: PLAN
Agent: [critical-bug-analyzer]
- Extend token expiry to 60 minutes
- Fix session cleanup logic
- Add token refresh mechanism

# Phase 3: CODE
Agents: [backend-developer, security-specialist]
- Updated JWT config
- Fixed session cleanup
- Implemented token refresh

# Phase 4: TEST
Agents: [test-engineer, qa-specialist]
- Unit tests: ✅ Pass
- Integration tests: ✅ Pass
- Manual testing: ✅ Pass

# Phase 5: FIX
- No fixes needed

# Phase 6: COMMIT
Agent: [git-specialist]
- Created PR: "Fix login timeout issue"
- Linked to PROJ-123
- Requested review
```

### Example 2: Feature Story

```bash
# Issue: PROJ-456 "Add user profile editing"

# Phase 1: EXPLORE
Agents: [requirements-analyzer, ui-specialist]
- Reviewed designs
- Identified API changes needed
- Analyzed existing profile code

# Phase 2: PLAN
Agents: [feature-architect, code-architect]
- Design profile update API
- Plan frontend form components
- Define validation rules

# Phase 3: CODE
Agents: [backend-developer, frontend-developer, test-engineer]
- Created profile update endpoint (parallel)
- Built profile edit form (parallel)
- Added validation (parallel)

# Phase 4: TEST
Agents: [test-engineer, qa-specialist]
- Unit tests: ✅ Pass
- E2E tests: ✅ Pass
- Accessibility: ✅ Pass

# Phase 5: FIX
Agent: [refactoring-specialist]
- Improved form validation UX
- Added loading states

# Phase 6: COMMIT
Agents: [git-specialist, documentation-writer]
- Created feature PR
- Updated API documentation
- Added user guide section
```

## Reference Documentation

For deeper implementation details, see:
- `references/phase-guides/` - Detailed guides for each phase
- `references/agent-selection.md` - Comprehensive agent selection criteria
- `references/jira-api.md` - Jira API integration patterns
- `references/escalation-playbook.md` - Detailed escalation procedures

## Integration with Other Skills

This skill works best when combined with:
- **jira** - Jira API operations and queries
- **git-workflows** - Branch management and PR creation
- **orchestration-patterns** - Multi-agent coordination strategies
- **testing** - Test execution and validation
- **debugging** - Issue investigation and root cause analysis
