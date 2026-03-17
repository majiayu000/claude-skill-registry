---
name: parallel-executor
version: 1.0.0
author: claude-command-and-control
created: 2025-11-29
last_updated: 2025-11-29
status: active
complexity: high
category: orchestration
tags: [parallel-execution, multi-agent, coordination, progress-tracking, result-aggregation]
---

# Parallel Executor Skill

## Description
Orchestrates concurrent task execution across multiple Claude agents with intelligent work distribution, real-time progress synchronization, automated result collection and validation, and comprehensive error handling. This skill transforms MULTI_AGENT_PLAN.md parallel groups into actual concurrent agent execution with coordination, monitoring, and rollback capabilities.

## When to Use This Skill
- "Execute these authentication tasks in parallel across 3 builder agents working in separate worktrees"
- "Run agents concurrently on API endpoint implementation, frontend components, and database migrations"
- "Start parallel development for microservices extraction with isolated agent environments"
- "Distribute work across agents to refactor payment processing module in 4 parallel streams"
- "Launch multi-agent execution of data pipeline components with progress monitoring"

## When NOT to Use This Skill
- Single agent sequential work → Use standard agent workflow instead
- Highly interdependent tasks with complex sequencing → Use sequential execution with handoffs
- Exploratory work without clear task definitions → Use research/planning skills first
- Critical sections requiring exclusive access → Use sequential execution with locks

## Prerequisites
- MULTI_AGENT_PLAN.md file with defined parallel groups and task assignments
- Agent configuration files for all participating agents (.claude/agents/*.md)
- Git repository with clean working directory
- Worktree manager skill for isolated workspace creation
- Agent communication skill for inter-agent messaging

## Workflow

### Phase 1: Pre-Execution Validation and Preparation
**Purpose**: Verify plan is executable, resources available, and environment ready for parallel work

#### Step 1.1: Validate MULTI_AGENT_PLAN.md
Parse and validate the plan structure:

```bash
# Check plan file exists and is well-formed
if [ ! -f "MULTI_AGENT_PLAN.md" ]; then
  echo "ERROR: MULTI_AGENT_PLAN.md not found"
  exit 1
fi

# Validate required sections present
grep -q "## Parallel Group" MULTI_AGENT_PLAN.md || {
  echo "ERROR: No parallel groups defined"
  exit 1
}
```

**Validation Checklist**:
- [ ] Plan file exists and is readable
- [ ] All parallel groups have defined tasks
- [ ] Each task has agent assignment
- [ ] Dependencies are clearly marked
- [ ] No circular dependencies in current group
- [ ] Success criteria defined for each task

**Expected Output**: Validated plan structure with extracted parallel groups

#### Step 1.2: Check Agent Availability
Verify all assigned agents are configured and ready:

```bash
# Check agent configuration files exist
for agent in $(grep -oP 'Agent: \K[A-Za-z0-9-]+' MULTI_AGENT_PLAN.md | sort -u); do
  if [ ! -f ".claude/agents/${agent}.md" ]; then
    echo "ERROR: Agent ${agent} not configured"
    exit 1
  fi
done
```

**Expected Output**: List of available agents with role assignments

#### Step 1.3: Verify Resource Availability
Check system resources for parallel execution:

**Resource Checks**:
- **Disk Space**: Minimum 10GB available for worktrees
- **Git State**: No uncommitted changes, clean working directory
- **Port Availability**: Development servers won't conflict
- **Environment Variables**: All required env vars set

**Decision Point**:
- IF resources insufficient → Reduce parallel groups or wait for cleanup
- ELSE IF git state dirty → Require commit or stash before proceeding
- ELSE → Proceed to workspace creation

**Expected Output**: Resource availability report with go/no-go decision

### Phase 2: Workspace Isolation and Agent Initialization
**Purpose**: Create isolated environments for each agent to prevent conflicts

#### Step 2.1: Create Git Worktrees
Use worktree-manager skill to create isolated workspaces:

```bash
# For each agent in parallel group
for task in parallel_group_tasks; do
  agent_name=$(extract_agent_name "$task")
  branch_name="agent/${agent_name}/$(generate_task_slug "$task")"

  # Create worktree
  git worktree add "../worktrees/${agent_name}" -b "${branch_name}"

  # Copy environment configuration
  cp .env "../worktrees/${agent_name}/.env"
  cp -r .claude "../worktrees/${agent_name}/.claude"
done
```

**Worktree Structure**:
```
project-root/
├── .git/
├── main-workspace/
└── worktrees/
    ├── builder-1/      # Isolated workspace for builder-1
    ├── builder-2/      # Isolated workspace for builder-2
    └── validator-1/    # Isolated workspace for validator-1
```

**Expected Output**: Isolated worktree for each parallel agent with replicated configuration

#### Step 2.2: Initialize Agent Contexts
Provision each agent with task-specific context:

**Context Bundle Per Agent**:
```markdown
# Agent Context: Builder-1

## Assigned Task
Implement JWT service with sign, verify, and refresh methods

## Task ID
parallel-group-2-task-1

## Dependencies Met
- JWT token structure designed (Architect-1 complete)
- User model created (database schema ready)

## Expected Output
- services/jwt.service.ts with full implementation
- services/jwt.service.spec.ts with unit tests
- Updated API documentation

## Success Criteria
- [ ] JWT tokens can be signed with user payload
- [ ] Tokens can be verified and decoded
- [ ] Refresh token flow implemented
- [ ] Unit tests passing with >80% coverage
- [ ] No security vulnerabilities (checked with npm audit)

## Related Context
- Architecture Decision: Using RS256 algorithm
- Token expiration: Access 15min, Refresh 7days
- See: docs/architecture/auth-design.md
```

**Expected Output**: Context file for each agent in their worktree

#### Step 2.3: Set Up Progress Tracking Infrastructure
Create shared progress tracking system:

**Progress Tracking File** (`PARALLEL_EXECUTION_STATUS.json`):
```json
{
  "execution_id": "exec_20251129_143052",
  "parallel_group": "Group 2: Core Auth",
  "started_at": "2025-11-29T14:30:52Z",
  "status": "in_progress",
  "agents": {
    "builder-1": {
      "task_id": "pg2-task-1",
      "task": "Implement JWT service",
      "status": "in_progress",
      "started_at": "2025-11-29T14:31:15Z",
      "progress_percent": 0,
      "worktree": "../worktrees/builder-1",
      "branch": "agent/builder-1/jwt-service"
    },
    "builder-2": {
      "task_id": "pg2-task-2",
      "task": "Create User model and repository",
      "status": "in_progress",
      "started_at": "2025-11-29T14:31:18Z",
      "progress_percent": 0,
      "worktree": "../worktrees/builder-2",
      "branch": "agent/builder-2/user-model"
    }
  },
  "completed_tasks": [],
  "failed_tasks": []
}
```

**Expected Output**: Initialized progress tracking with all agents in pending state

### Phase 3: Parallel Agent Execution with Monitoring
**Purpose**: Launch agents concurrently and monitor progress in real-time

#### Step 3.1: Distribute Work to Agents
Launch each agent in its isolated worktree:

**Agent Launch Script** (pseudo-code):
```bash
#!/bin/bash

function launch_agent() {
  local agent_name=$1
  local worktree_path=$2
  local task_description=$3
  local context_file=$4

  cd "$worktree_path"

  # Launch agent with task context
  claude-code-agent \
    --agent ".claude/agents/${agent_name}.md" \
    --task "$task_description" \
    --context "$context_file" \
    --output-log "logs/${agent_name}.log" \
    --status-file "status/${agent_name}.status" \
    &

  local agent_pid=$!
  echo "${agent_name}:${agent_pid}" >> ../agent_pids.txt
}

# Launch all agents in parallel
for agent_task in "${parallel_group[@]}"; do
  launch_agent "${agent_task.agent}" "${agent_task.worktree}" \
               "${agent_task.description}" "${agent_task.context}"
done

echo "Launched ${#parallel_group[@]} agents in parallel"
```

**Expected Output**: N background agent processes running concurrently, PIDs tracked

#### Step 3.2: Monitor Progress and Health
Poll agent status and update central tracking:

**Monitoring Loop**:
```bash
while [ $(count_active_agents) -gt 0 ]; do
  for agent in active_agents; do
    # Read agent status file
    status=$(cat "worktrees/${agent}/status/${agent}.status")

    # Parse progress
    progress=$(echo "$status" | jq -r '.progress_percent')
    current_step=$(echo "$status" | jq -r '.current_step')

    # Update central tracking
    update_execution_status "$agent" "$progress" "$current_step"

    # Check for errors
    if [ $(echo "$status" | jq -r '.has_error') == "true" ]; then
      handle_agent_error "$agent" "$status"
    fi
  done

  # Display progress dashboard
  display_progress_dashboard

  sleep 10  # Poll every 10 seconds
done
```

**Progress Dashboard Output**:
```
Parallel Execution: Group 2 - Core Auth (Started: 14:30:52)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Agent: builder-1 (JWT Service)
Status: IN_PROGRESS | Progress: ████████░░░░░░░░ 45%
Current: Writing unit tests for token verification

Agent: builder-2 (User Model)
Status: IN_PROGRESS | Progress: ████████████░░░░ 72%
Current: Creating repository integration tests

Agent: validator-1 (Auth Flow Tests)
Status: IN_PROGRESS | Progress: ██████░░░░░░░░░░ 28%
Current: Setting up test fixtures

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Completed: 0/3 | Failed: 0/3 | Runtime: 00:23:15
```

**Expected Output**: Real-time progress updates with agent status

#### Step 3.3: Handle Inter-Agent Communication
Process and route messages between agents:

**Message Bus Implementation**:
```json
{
  "message_id": "msg_001",
  "timestamp": "2025-11-29T14:45:30Z",
  "from_agent": "builder-1",
  "to_agent": "builder-2",
  "message_type": "interface_contract",
  "payload": {
    "interface": "IUserService",
    "methods": ["findById", "create", "updateRefreshToken"],
    "purpose": "JWT service needs to lookup users by ID"
  }
}
```

**Message Routing**:
- Agent publishes message to `messages/${to_agent}/inbox/`
- Receiving agent polls inbox every 30 seconds
- Messages acknowledged when processed
- Unacknowledged messages escalated after 5 minutes

**Expected Output**: Message queue with delivery tracking

### Phase 4: Result Collection and Validation
**Purpose**: Gather completed work, validate quality, and aggregate results

#### Step 4.1: Collect Agent Outputs
When agent completes, gather all artifacts:

**Collection Checklist per Agent**:
```bash
function collect_agent_output() {
  local agent_name=$1
  local worktree=$2

  # Create output bundle
  mkdir -p "outputs/${agent_name}"

  # Collect code changes
  cd "$worktree"
  git diff main > "../outputs/${agent_name}/changes.diff"
  git diff --name-only main > "../outputs/${agent_name}/files_changed.txt"

  # Collect test results
  cp test-results.json "../outputs/${agent_name}/"

  # Collect logs
  cp "logs/${agent_name}.log" "../outputs/${agent_name}/"

  # Collect agent summary
  cp "TASK_SUMMARY.md" "../outputs/${agent_name}/"

  # Collect metrics
  cat > "../outputs/${agent_name}/metrics.json" <<EOF
{
  "lines_added": $(git diff --stat main | tail -1 | grep -oP '\d+ insertions'),
  "lines_removed": $(git diff --stat main | tail -1 | grep -oP '\d+ deletions'),
  "files_modified": $(git diff --name-only main | wc -l),
  "test_coverage": $(jq -r '.coverage_percent' test-results.json),
  "execution_time": "$(($(date +%s) - start_time)) seconds"
}
EOF
}
```

**Expected Output**: Structured output bundle for each agent with code, tests, logs, metrics

#### Step 4.2: Validate Agent Results
Run quality checks on each agent's output:

**Validation Pipeline**:
```bash
function validate_agent_output() {
  local agent_name=$1
  local worktree=$2

  cd "$worktree"

  # Run linting
  npm run lint > "../outputs/${agent_name}/lint_results.txt" 2>&1
  lint_exit_code=$?

  # Run tests
  npm test > "../outputs/${agent_name}/test_output.txt" 2>&1
  test_exit_code=$?

  # Check test coverage
  coverage=$(jq -r '.coverage_percent' coverage/coverage-summary.json)

  # Security scan
  npm audit --json > "../outputs/${agent_name}/security_audit.json"
  critical_vulns=$(jq '.metadata.vulnerabilities.critical' "../outputs/${agent_name}/security_audit.json")

  # Build validation (if applicable)
  npm run build > "../outputs/${agent_name}/build_output.txt" 2>&1
  build_exit_code=$?

  # Generate validation report
  cat > "../outputs/${agent_name}/validation_report.json" <<EOF
{
  "agent": "$agent_name",
  "validations": {
    "lint": {
      "passed": $([ $lint_exit_code -eq 0 ] && echo "true" || echo "false"),
      "exit_code": $lint_exit_code
    },
    "tests": {
      "passed": $([ $test_exit_code -eq 0 ] && echo "true" || echo "false"),
      "exit_code": $test_exit_code,
      "coverage": $coverage
    },
    "security": {
      "passed": $([ $critical_vulns -eq 0 ] && echo "true" || echo "false"),
      "critical_vulnerabilities": $critical_vulns
    },
    "build": {
      "passed": $([ $build_exit_code -eq 0 ] && echo "true" || echo "false"),
      "exit_code": $build_exit_code
    }
  },
  "overall_passed": $(validate_all_checks)
}
EOF
}
```

**Decision Point**:
- IF all validations pass → Mark agent task as COMPLETE_VALIDATED
- ELSE IF only non-critical failures → Mark as COMPLETE_WITH_WARNINGS
- ELSE → Mark as FAILED, trigger error handling

**Expected Output**: Validation report for each agent with pass/fail status

#### Step 4.3: Aggregate Results
Combine outputs from all agents:

**Aggregation Process**:
```bash
# Merge all changes into integration branch
git checkout -b integration/parallel-group-2

for agent in completed_agents; do
  worktree="worktrees/${agent}"

  # Merge agent's branch
  git merge --no-ff "${agent_branch}" -m "Integrate ${agent} work"

  # Run integration tests after each merge
  npm test

  if [ $? -ne 0 ]; then
    echo "ERROR: Integration tests failed after merging ${agent}"
    # Rollback and investigate
    git merge --abort
    handle_integration_failure "${agent}"
  fi
done
```

**Integration Validation**:
- [ ] All agent branches merge without conflicts
- [ ] Combined code passes linting
- [ ] All tests pass (including new tests from agents)
- [ ] Test coverage maintained or improved
- [ ] No new security vulnerabilities
- [ ] Application builds successfully
- [ ] Integration tests pass

**Expected Output**: Single integration branch with all agent work combined and validated

### Phase 5: Cleanup and Reporting
**Purpose**: Clean up resources, generate execution report, prepare for next phase

#### Step 5.1: Generate Execution Report
Create comprehensive report of parallel execution:

**Execution Report Template**:
```markdown
# Parallel Execution Report: Group 2 - Core Auth

## Execution Summary
- **Execution ID**: exec_20251129_143052
- **Started**: 2025-11-29 14:30:52
- **Completed**: 2025-11-29 16:15:30
- **Duration**: 1 hour 44 minutes
- **Status**: SUCCESS

## Agent Performance

### builder-1: JWT Service Implementation
- **Status**: ✅ COMPLETE
- **Duration**: 1h 32min
- **Files Modified**: 3 (jwt.service.ts, jwt.service.spec.ts, jwt.types.ts)
- **Lines Added/Removed**: +387 / -12
- **Test Coverage**: 92%
- **Tests Passing**: 24/24
- **Validation**: All checks passed

### builder-2: User Model and Repository
- **Status**: ✅ COMPLETE
- **Duration**: 1h 18min
- **Files Modified**: 5
- **Lines Added/Removed**: +245 / -8
- **Test Coverage**: 88%
- **Tests Passing**: 18/18
- **Validation**: All checks passed

### validator-1: Auth Flow Integration Tests
- **Status**: ⚠️  COMPLETE WITH WARNINGS
- **Duration**: 1h 41min
- **Files Modified**: 2
- **Lines Added/Removed**: +156 / -3
- **Test Coverage**: 95%
- **Tests Passing**: 12/12
- **Validation**: Lint warnings (non-blocking)

## Integration Results
- **Integration Branch**: integration/parallel-group-2
- **Merge Conflicts**: 0
- **Integration Tests**: 54/54 passing
- **Combined Coverage**: 91%
- **Build Status**: ✅ SUCCESS

## Metrics
- **Total Lines Changed**: +788 / -23
- **Total Files Modified**: 10
- **Total Tests Added**: 54
- **Parallel Efficiency**: 62% (vs sequential estimate)
  - Sequential estimate: 4h 30min
  - Parallel actual: 1h 44min
  - Time saved: 2h 46min

## Issues Encountered
1. **Minor**: builder-2 needed IUserService interface from builder-1
   - Resolved via inter-agent messaging at 15:05
   - Delay: 8 minutes
2. **Warning**: validator-1 had ESLint warnings for test helpers
   - Non-blocking, documented for cleanup

## Next Steps
- [ ] Code review integration branch
- [ ] Merge integration branch to main
- [ ] Clean up worktrees
- [ ] Start Parallel Group 3 (OAuth2 Integration)
```

**Expected Output**: Detailed execution report with metrics and next steps

#### Step 5.2: Clean Up Worktrees
Remove temporary workspaces:

```bash
function cleanup_worktrees() {
  # Only clean up if integration successful
  if [ "$integration_status" == "SUCCESS" ]; then
    for agent in agents; do
      worktree="worktrees/${agent}"

      # Archive worktree logs before deletion
      tar -czf "archives/${agent}_${execution_id}.tar.gz" \
          "${worktree}/logs" \
          "${worktree}/outputs"

      # Remove worktree
      git worktree remove "$worktree"

      # Delete branch if merged
      git branch -d "${agent_branch}"
    done

    echo "Cleaned up ${#agents[@]} worktrees"
  else
    echo "Integration failed - preserving worktrees for debugging"
  fi
}
```

**Expected Output**: Cleaned filesystem with worktrees removed, logs archived

#### Step 5.3: Update Plan Status
Mark completed parallel group in MULTI_AGENT_PLAN.md:

```markdown
### Parallel Group 2: Core Auth ✅ COMPLETED
**Duration**: 3 days → **Actual**: 1h 44min
**Dependencies**: Group 1 complete

- [x] 2.1: Implement JWT service (Builder-1, 6h) ✅ 1h 32min
- [x] 2.2: Create User model and repository (Builder-1, 4h) ✅ 1h 18min
- [x] 2.3: Build registration endpoint (Builder-1, 5h) ⏭️ Moved to Group 3
- [x] 2.4: Write auth flow integration tests (Validator-1, 6h) ⚠️ 1h 41min (warnings)

**Execution Report**: reports/exec_20251129_143052.md
```

**Expected Output**: Updated plan with actual completion status

## Examples

### Example 1: Parallel API Endpoint Development
**Context**: Building 5 REST API endpoints concurrently with 3 builder agents and 2 validator agents

**Input:**
```markdown
## Parallel Group 3: API Endpoints
- Task 3.1: Build /auth/login endpoint (Builder-1)
- Task 3.2: Build /auth/register endpoint (Builder-2)
- Task 3.3: Build /auth/refresh endpoint (Builder-1)
- Task 3.4: Write endpoint integration tests (Validator-1)
- Task 3.5: Write endpoint security tests (Validator-2)
```

**Execution Flow:**
1. Phase 1: Validated plan, checked 5 agents configured, verified git clean
2. Phase 2: Created 5 worktrees (builder-1, builder-2, validator-1, validator-2)
3. Phase 3: Launched 5 agents in parallel at 10:15:30
4. Phase 3: Monitored progress, builder-1 completed first at 11:42, others by 12:05
5. Phase 4: Collected outputs, all validations passed
6. Phase 4: Merged to integration branch, all tests passing
7. Phase 5: Generated report, cleaned worktrees

**Expected Output:**
```markdown
# Execution Report

## Summary
- Duration: 1h 50min (vs 8h sequential)
- All 5 tasks completed successfully
- 0 merge conflicts
- 67 tests passing
- 89% combined coverage

## Agent Performance
- builder-1: 2 tasks in 1h 47min (endpoints + tests)
- builder-2: 1 task in 1h 23min
- validator-1: 1 task in 1h 38min
- validator-2: 1 task in 1h 42min

## Integration
- Branch: integration/parallel-group-3
- Files modified: 12
- Lines added: 892
- All integration tests passing
```

**Rationale**: Demonstrates efficient parallel execution of similar tasks with different agents, showing significant time savings

### Example 2: Microservices Parallel Extraction
**Context**: Extracting 3 microservices from monolith simultaneously

**Input:**
```markdown
## Parallel Group 2: Service Extraction
- Task 2.1: Extract Product Catalog service (Builder-1, Builder-2)
- Task 2.2: Extract Order Management service (Builder-3, Builder-4)
- Task 2.3: Extract Inventory service (Builder-5, Builder-6)
- Task 2.4: Set up service mesh (DevOps-1)
- Task 2.5: Create integration tests (Validator-1)
```

**Execution Flow:**
1. Created 7 worktrees for 7 agents
2. Builders worked in pairs on each service
3. DevOps-1 configured Istio while builders worked
4. Validator-1 wrote tests as services completed
5. Used inter-agent messaging for API contract coordination

**Expected Output:**
```markdown
# Execution Report

## Summary
- Duration: 3 days 6 hours (vs 10 days sequential)
- 3 services extracted successfully
- Service mesh configured
- 156 integration tests passing

## Challenges
- Merge conflict in shared utilities (resolved in 45min)
- API contract mismatch between Order and Inventory (resolved via messaging)

## Inter-Agent Messages
- 23 messages exchanged
- Average response time: 12 minutes
- 2 contract changes negotiated
```

**Rationale**: Shows complex parallel work with pair programming (2 agents per service) and coordination challenges

### Example 3: Parallel Test Suite Execution
**Context**: Running comprehensive test suite across multiple test types in parallel

**Input:**
```markdown
## Parallel Group: Comprehensive Testing
- Task: Unit tests (Validator-1)
- Task: Integration tests (Validator-2)
- Task: E2E tests (Validator-3)
- Task: Performance benchmarks (Validator-4)
- Task: Security audit (Validator-5)
```

**Expected Output:**
```markdown
# Test Execution Report

## Summary
- Total Duration: 42 minutes (vs 3h 15min sequential)
- Time Saved: 2h 33min (78% reduction)

## Results by Type
- Unit: 1,247 tests passing (12min)
- Integration: 234 tests passing (28min)
- E2E: 45 tests passing (35min)
- Performance: All benchmarks met (18min)
- Security: 0 critical vulnerabilities (42min)

## Resource Usage
- Peak CPU: 87% (5 parallel test runners)
- Peak Memory: 12.3 GB
- Disk I/O: Moderate
```

**Rationale**: Demonstrates parallel test execution with resource monitoring and significant time savings

## Quality Standards

### Output Requirements
- All agent tasks must complete with validation reports (lint, test, security)
- Integration branch must pass all tests before considering execution successful
- Execution report must include actual vs estimated time for each task
- Zero merge conflicts or documented resolution for any conflicts
- All inter-agent messages must be logged and archived

### Performance Requirements
- Execution time: Parallel group should complete in ≤50% of sequential estimate
- Progress updates: Status dashboard refreshed every ≤10 seconds
- Agent launch time: All agents launched within 2 minutes of execution start
- Resource overhead: Monitoring overhead ≤5% of total execution time

### Integration Requirements
- Integrates with worktree-manager-skill for workspace isolation
- Uses agent-communication-skill for inter-agent messaging
- Consumes MULTI_AGENT_PLAN.md from multi-agent-planner-skill
- Reports progress to orchestrator agent or user dashboard
- Updates plan status in real-time for visibility

## Common Pitfalls

### Pitfall 1: Resource Contention and Bottlenecks
**Issue**: Multiple agents trying to access same database, API, or service causing failures
**Why it happens**: Insufficient resource isolation, shared development database
**Solution**:
- Use containerized databases per worktree (Docker Compose)
- Mock external APIs for parallel development
- Use different ports for each agent's dev server
- Implement resource locking for shared resources

### Pitfall 2: Merge Conflicts from Parallel Work
**Issue**: Agents modify same files causing complex merge conflicts
**Why it happens**: Poor task decomposition, overlapping responsibilities
**Solution**:
- Better task decomposition to minimize file overlap
- Establish file ownership boundaries
- Use interface contracts to coordinate shared code
- Merge agents serially if conflicts detected, don't auto-merge

### Pitfall 3: Test Pollution and Flaky Tests
**Issue**: Tests passing in isolation but failing when run in parallel
**Why it happens**: Shared test state, database fixtures, race conditions
**Solution**:
- Use isolated test databases per agent
- Implement proper test cleanup (beforeEach/afterEach)
- Run tests with random order to detect dependencies
- Use condition-based-waiting for async operations

### Pitfall 4: Cascading Failures from Blocked Agent
**Issue**: One agent failure blocks all dependent agents, wasting parallel capacity
**Why it happens**: Tight coupling, synchronous handoffs
**Solution**:
- Design tasks with minimal dependencies
- Implement timeout-based failure detection
- Have backup tasks agents can work on if blocked
- Use circuit breaker pattern for dependent tasks

### Pitfall 5: Lost Context in Parallel Execution
**Issue**: Agents duplicate work or make conflicting decisions
**Why it happens**: Poor inter-agent communication, stale context
**Solution**:
- Use agent-communication-skill for real-time coordination
- Maintain shared decision log updated by all agents
- Broadcast architectural decisions to all agents
- Implement distributed locking for critical decisions

## Integration with Command & Control

### Related Agents
- **Orchestrator Agent**: Invokes parallel-executor skill to run MULTI_AGENT_PLAN.md parallel groups
- **Worker Agents (Builder/Validator/etc)**: Executed by this skill in isolated worktrees
- **Integration Manager**: Receives aggregated results for final integration

### Related Commands
- `/start-session`: May invoke parallel-executor for executing initial parallel work
- `/test-all`: Can leverage parallel executor to run test suites concurrently
- `/pr`: Uses results from parallel execution for PR creation

### Related Skills
- **multi-agent-planner-skill**: Produces MULTI_AGENT_PLAN.md consumed by this skill
- **worktree-manager-skill**: Creates and manages isolated workspaces (dependency)
- **agent-communication-skill**: Enables inter-agent messaging during execution (dependency)
- **verification-before-completion**: Validates agent outputs before marking complete

### MCP Dependencies
- **Git MCP**: Worktree creation, branch management, merging
- **IDE MCP**: Running tests, linting, building in each worktree
- **Process MCP**: Launching and monitoring background agent processes
- **Filesystem MCP**: Creating output directories, archiving logs

### Orchestration Notes
- **Invoked by**: Orchestrator agent, `/start-session` command with multi-agent plan
- **Invokes**: worktree-manager-skill (workspace setup), agent-communication-skill (messaging)
- **Chained with**: multi-agent-planner-skill (plan → execute), verification-before-completion (execute → validate)

## Troubleshooting

### Issue: Agent Process Crashes or Hangs
**Symptoms**: Agent status file not updating, no progress for >30 minutes
**Diagnosis**:
```bash
# Check if agent process still running
ps aux | grep -i "claude-code-agent.*${agent_name}"

# Check agent logs for errors
tail -f "worktrees/${agent_name}/logs/${agent_name}.log"
```
**Solution**:
1. If crashed: Review logs for error, fix issue, restart agent
2. If hung: Send SIGTERM to agent process, analyze state, restart
3. If repeated failures: Remove task from parallel group, run sequentially
4. Update progress tracking to mark agent as FAILED

### Issue: Integration Tests Fail After Merging Agent Work
**Symptoms**: Individual agent tests pass, but integration fails
**Diagnosis**:
```bash
# Identify which agent merge caused failure
git bisect start integration/parallel-group HEAD~N
git bisect run npm test
```
**Solution**:
1. Identify the agent whose merge broke tests
2. Review that agent's changes for integration issues
3. Check for interface mismatches or contract violations
4. Fix issue and re-run integration tests
5. Consider requiring integration test run before agent completion

### Issue: Parallel Execution Slower Than Sequential
**Symptoms**: Parallel completion time ≥ sequential estimate
**Diagnosis**: Check for serialization points and resource contention
**Solution**:
1. Identify if tasks actually have hidden dependencies
2. Check for resource bottlenecks (CPU, memory, disk, network)
3. Reduce number of parallel agents to match available resources
4. Consider if tasks are too small (overhead dominates)
5. Profile agent execution to find bottlenecks

### Issue: Worktree Configuration Drift
**Symptoms**: Agents getting different results due to config differences
**Diagnosis**:
```bash
# Compare configurations across worktrees
diff -r worktrees/builder-1/.env worktrees/builder-2/.env
diff -r worktrees/builder-1/.claude worktrees/builder-2/.claude
```
**Solution**:
1. Ensure worktree creation copies all config files
2. Use symlinks for shared config where possible
3. Implement config validation before agent launch
4. Periodically sync configs during long-running execution

## Version History
- 1.0.0 (2025-11-29): Initial release
  - Concurrent agent execution orchestration
  - Work distribution algorithms
  - Real-time progress tracking and monitoring
  - Result collection and validation pipeline
  - Integration branch creation and testing
  - Resource management and cleanup
  - Comprehensive execution reporting
  - Error handling and recovery mechanisms
