---
name: Phase Management
description: This skill should be used when the user asks about "phase management", "6-phase protocol", "explore phase", "plan phase", "code phase", "test phase", "fix phase", "document phase", "phase transitions", "phase enforcement", or needs guidance on managing the mandatory orchestration phases.
version: 1.0.0
---

# Phase Management

Establish systematic progression through the mandatory 6-phase protocol for all complex tasks, ensuring quality gates and proper transitions.

## The 6-Phase Protocol

Every complex task MUST progress through these phases in order:

```
EXPLORE → PLAN → CODE → TEST → FIX → DOCUMENT
```

### Phase Overview

| Phase | Purpose | Min Agents | Outputs |
|-------|---------|------------|---------|
| **EXPLORE** | Understanding & Research | 2+ | Context, requirements, constraints |
| **PLAN** | Strategy & Design | 1-2 | Architecture, task breakdown, DAG |
| **CODE** | Implementation | 2-4 | Working code, initial tests |
| **TEST** | Validation | 2-3 | Test results, coverage reports |
| **FIX** | Refinement | 1-2 | Bug fixes, improvements |
| **DOCUMENT** | Knowledge Transfer | 1-2 | Docs, ADRs, vault updates |

## Phase 1: EXPLORE

**Purpose**: Gather comprehensive understanding before planning.

### Activities
- Analyze requirements and constraints
- Research existing codebase
- Identify dependencies and risks
- Gather library documentation (Context7)
- Understand domain context

### Agents
- `code-explorer` - Codebase analysis
- `research-agent` - Documentation gathering
- `requirements-analyst` - Requirement extraction

### Exit Criteria
- [ ] Requirements documented
- [ ] Codebase context understood
- [ ] Risks identified
- [ ] Dependencies mapped

### Outputs
```yaml
explore_output:
  requirements: "Detailed requirement specification"
  codebase_context: "Relevant files and patterns"
  risks: "Identified risks and mitigations"
  dependencies: "External and internal dependencies"
```

## Phase 2: PLAN

**Purpose**: Design solution and create execution plan.

### Activities
- Design architecture/approach
- Break down into tasks
- Create dependency graph (DAG)
- Allocate resources
- Estimate complexity

### Agents
- `master-strategist` - Overall planning
- `architect-supreme` - Technical design

### Exit Criteria
- [ ] Architecture defined
- [ ] Tasks broken down
- [ ] DAG created
- [ ] Resources allocated

### Outputs
```yaml
plan_output:
  architecture: "Technical design document"
  task_dag: "Directed acyclic graph of tasks"
  resource_allocation: "Agent assignments"
  checkpoints: "Phase boundary markers"
```

## Phase 3: CODE

**Purpose**: Implement the planned solution.

### Activities
- Execute tasks per DAG
- Write production code
- Write unit tests
- Handle edge cases
- Integrate components

### Agents
- `coder` - Implementation (2-4 agents)
- `unit-tester` - Test writing
- `integrator` - Component integration

### Exit Criteria
- [ ] All tasks completed
- [ ] Unit tests passing
- [ ] Code compiles/runs
- [ ] Integration successful

### Outputs
```yaml
code_output:
  files_created: ["list of new files"]
  files_modified: ["list of changed files"]
  tests_written: ["list of test files"]
  integration_status: "success|partial|failed"
```

## Phase 4: TEST

**Purpose**: Validate implementation quality.

### Activities
- Run full test suite
- Perform integration testing
- Execute E2E tests (if applicable)
- Measure coverage
- Security scanning

### Agents
- `test-runner` - Test execution
- `coverage-analyst` - Coverage analysis
- `security-scanner` - Security validation

### Exit Criteria
- [ ] All tests pass
- [ ] Coverage meets threshold
- [ ] No security issues
- [ ] Performance acceptable

### Outputs
```yaml
test_output:
  test_results: "pass|fail with details"
  coverage_report: "Coverage percentage by file"
  security_findings: "Any vulnerabilities found"
  performance_metrics: "Key performance indicators"
```

## Phase 5: FIX

**Purpose**: Address issues found during testing.

### Activities
- Fix failing tests
- Address security findings
- Improve coverage
- Optimize performance
- Refactor as needed

### Agents
- `debugger` - Issue diagnosis
- `fixer` - Bug resolution

### Exit Criteria
- [ ] All tests passing
- [ ] Security issues resolved
- [ ] Coverage improved
- [ ] Performance optimized

### Outputs
```yaml
fix_output:
  issues_resolved: ["list of fixed issues"]
  regressions_avoided: "Verification status"
  final_test_status: "All tests passing confirmation"
```

## Phase 6: DOCUMENT

**Purpose**: Create knowledge transfer artifacts.

### Activities
- Update README/docs
- Create ADRs for decisions
- Sync to Obsidian vault
- Update API documentation
- Log learnings

### Agents
- `documentation-expert` - Doc writing
- `vault-syncer` - Obsidian sync

### Exit Criteria
- [ ] Docs updated
- [ ] ADRs created
- [ ] Vault synced
- [ ] Knowledge captured

### Outputs
```yaml
document_output:
  docs_updated: ["list of documentation files"]
  adrs_created: ["architectural decision records"]
  vault_entries: ["Obsidian vault updates"]
  commit_ready: "Ready for final commit"
```

## Phase Transitions

### Transition Protocol

1. **Verify Exit Criteria**: All criteria must be met
2. **Create Checkpoint**: Save phase state
3. **Package Outputs**: Prepare for next phase
4. **Notify Transition**: Log phase completion
5. **Initialize Next Phase**: Load context, spawn agents

### Checkpoint Structure

```yaml
checkpoint:
  phase: "EXPLORE|PLAN|CODE|TEST|FIX|DOCUMENT"
  timestamp: "ISO 8601 timestamp"
  status: "completed|partial|blocked"
  outputs: "Phase output package"
  next_phase: "Next phase to execute"
  context: "Preserved context for continuation"
```

### Recovery from Checkpoint

If interrupted, resume from last checkpoint:
1. Load checkpoint state
2. Verify outputs still valid
3. Continue from current phase
4. Don't repeat completed work

## Enforcement

The 6-phase protocol is **MANDATORY** and enforced via hooks:

- **Pre-task**: Verify phase compliance plan
- **Post-task**: Validate all phases completed
- **Phase-transition**: Enforce exit criteria

### Skip Prevention

Phases cannot be skipped:
- TEST phase: Required even for "simple" changes
- DOCUMENT phase: Required for all work
- FIX phase: Can be minimal if no issues

## Additional Resources

### Reference Files
- **`references/phase-details.md`** - Extended phase specifications
- **`references/checkpoint-format.md`** - Checkpoint data structures

### Examples
- **`examples/phase-outputs.json`** - Sample outputs by phase
- **`examples/checkpoint.json`** - Sample checkpoint structure
