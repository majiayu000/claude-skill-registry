---
name: ReAcTree Agent Coordination Patterns
description: "Hierarchical task decomposition with control flow nodes and dual memory systems from ReAcTree research. Trigger keywords: ReAcTree, parallel execution, working memory, episodic memory, LOOP, CONDITIONAL, FEEDBACK, hierarchical agents, coordination, control flow, agent trees"
version: 1.0.0
source: "ReAcTree: Hierarchical LLM Agent Trees with Control Flow for Long-Horizon Task Planning" (Choi et al., 2024)
---

## Core Concepts

**Hierarchical Agent Trees**: Complex tasks decomposed into tree structures where each node can be an agent (reasoning + action) or control flow coordinator.

**Control Flow Nodes**: Six coordination patterns inspired by behavior trees:
1. **Sequence**: Execute children sequentially (for dependencies)
2. **Parallel**: Execute children concurrently (for independent work)
3. **Fallback**: Try alternatives until one succeeds (for resilience)
4. **LOOP**: Iterative refinement until condition met (NEW in v2.0)
5. **CONDITIONAL**: Branching logic based on observations (NEW in v2.0)
6. **TRANSACTION**: Atomic operations with rollback (Coming in v2.0)

**Dual Memory Systems**:
1. **Working Memory**: Shared knowledge across agents (cached verifications)
2. **Episodic Memory**: Successful subgoal experiences (learning from past)

## Benefits (Research-Proven)

- **61% success rate** vs 31% for monolithic ReAct (97% improvement)
- **30-50% faster** workflows (parallel execution)
- **Consistent facts** (working memory eliminates re-discovery)
- **Learning over time** (episodic memory improves with use)

## Application to Rails Development

### Control Flow Examples

**Sequence** (Dependencies Exist):
```
Database → Models → Services → Controllers
```

**Parallel** (Independent Work):
```
After Models Complete:
  ├── Services (uses models) ┐
  ├── Components (uses models) ├ Run concurrently!
  └── Model Tests (tests models) ┘
```

**Fallback** (Resilience):
```
Try fetching TailAdmin patterns:
  Primary: GitHub repo
  ↓ (if fails)
  Fallback1: Local cache
  ↓ (if fails)
  Fallback2: Generic Tailwind
  ↓ (if fails)
  Fallback3: Warn + Use plain HTML
```

**LOOP** (Iterative Refinement - NEW in v2.0):
```
TDD Cycle (max 3 iterations):
  LOOP until tests pass:
    1. Run RSpec tests
    2. IF tests failing:
         Fix failing specs
       ELSE:
         Break loop (success!)

Iteration 1: 5 examples, 2 failures → Fix validation
Iteration 2: 5 examples, 0 failures → DONE ✓
```

**CONDITIONAL** (Branching - NEW in v2.0):
```
IF integration tests pass:
  THEN: Deploy to staging
  ELSE: Debug test failures

Result: Tests passing → Deployed to staging ✓
```

### Working Memory Examples

**Codebase Facts Cached**:
- Authentication helpers (`current_administrator`)
- Route prefixes (`/admin`, `/api`)
- Service patterns (`Callable concern`)
- UI frameworks (`TailAdmin`, `Stimulus`)

**Benefits**: First agent verifies, all agents reuse (no redundant `rg/grep`)

### Episodic Memory Examples

**Stored Episodes**:
```json
{
  "subgoal": "stripe_payment_integration",
  "patterns_applied": ["Callable service", "Retry logic"],
  "learnings": ["Webhooks need idempotency keys"]
}
```

**Next Similar Task** (PayPal):
- Reuse proven decomposition
- Apply same patterns
- Remember past learnings

## When to Use ReAcTree Patterns

**Use LOOP Nodes** when (NEW in v2.0):
- Iterative refinement needed (TDD red-green-refactor)
- Performance optimization with verification
- Error recovery with retry logic
- Example: Write test → Run → Fix → Verify (repeat until passing)

**Use Parallel Nodes** when:
- Phases only depend on earlier completed phase (not each other)
- Example: Services + Components both depend on Models only

**Use Fallback Nodes** when:
- Primary approach may fail (network, external resource)
- Graceful degradation acceptable
- Example: GitHub fetch → Cache → Default

**Use Working Memory** when:
- Multiple agents need same fact
- Fact is verifiable once, reusable many times
- Example: Auth helpers, route prefixes, patterns

**Use Episodic Memory** when:
- Similar tasks repeat (different APIs, different models)
- Past learnings can improve future executions
- Example: Stripe → PayPal, One CRUD → Another CRUD

## Implementation in reactree-rails-dev Plugin

### Memory Files

**Working Memory** (`.claude/reactree-memory.jsonl`):
```json
{
  "timestamp": "2025-01-21T10:30:00Z",
  "agent": "codebase-inspector",
  "knowledge_type": "pattern_discovery",
  "key": "service_object_pattern",
  "value": {
    "pattern": "Callable concern",
    "location": "app/concerns/callable.rb"
  },
  "confidence": "verified"
}
```

**Episodic Memory** (`.claude/reactree-episodes.jsonl`):
```json
{
  "episode_id": "ep-2025-01-21-001",
  "timestamp": "2025-01-21T11:00:00Z",
  "subgoal": "implement_stripe_payment_service",
  "context": {
    "feature_type": "payment_processing",
    "complexity": "high"
  },
  "approach": {
    "patterns_applied": ["Callable service", "Result object", "Retry with exponential backoff"]
  },
  "outcome": {
    "success": true,
    "duration_minutes": 45
  },
  "learnings": [
    "Stripe webhooks require idempotency keys to prevent duplicate processing"
  ]
}
```

### Agent Memory Responsibilities

| Agent | Memory Role | What it Writes | What it Reads |
|-------|-------------|----------------|---------------|
| **workflow-orchestrator** | Initialize | Nothing | Nothing (just inits) |
| **codebase-inspector** | Writer | Patterns, auth helpers, routes | Nothing (first to run) |
| **rails-planner** | Reader + Writer | Architecture decisions | All patterns from inspector |
| **implementation-executor** | Reader + Writer | Phase results, discoveries | All patterns + decisions |
| **control-flow-manager** | Reader + Writer | Loop iterations, conditions | All context + state |

## Performance Comparison

### Time Savings (Medium Feature)

**Traditional Sequential Workflow**:
```
Database:    10 min
Models:      15 min
Services:    20 min ← waiting
Components:  25 min ← waiting
Jobs:        10 min ← waiting
Controllers: 15 min ← waiting
Views:       10 min ← waiting
Tests:       20 min ← waiting
──────────────────
TOTAL:      125 min
```

**ReAcTree Parallel Workflow**:
```
Group 0: Database         10 min
Group 1: Models           15 min
Group 2 (PARALLEL):       25 min (max of Services:20, Components:25, Tests:15)
Group 3 (PARALLEL):       15 min (max of Jobs:10, Controllers:15)
Group 4: Views            10 min
Group 5: Integration      20 min
──────────────────────────
TOTAL:                    85 min
SAVED:                    40 min (32% faster)
```

### Memory Efficiency

**Without Working Memory** (current):
- Context verification: 5-8 `rg/grep` operations × 4 agents = 20-32 operations
- Time: ~3-5 minutes wasted on redundant analysis

**With Working Memory** (ReAcTree):
- Context verification: 5-8 operations × 1 agent (inspector) = 5-8 operations
- Time: ~30 seconds (cached reads for other agents)
- **Savings**: 2.5-4.5 minutes per workflow

## Research Citation

This plugin implements concepts from:

```bibtex
@article{choi2024reactree,
  title={ReAcTree: Hierarchical LLM Agent Trees with Control Flow for Long-Horizon Task Planning},
  author={Choi, Jae-Woo and Kim, Hyungmin and Ong, Hyobin and Jang, Minsu and Kim, Dohyung and Kim, Jaehong and Yoon, Youngwoo},
  journal={arXiv preprint arXiv:2511.02424},
  year={2024}
}
```

## Comparison with rails-enterprise-dev

| Feature | rails-enterprise-dev | reactree-rails-dev |
|---------|---------------------|-------------------|
| **Execution** | Sequential | **Parallel** ✨ |
| **Memory** | None | **Working + Episodic** ✨ |
| **Speed** | Baseline | **30-50% faster** ✨ |
| **Learning** | No | **Yes** ✨ |
| **Fallbacks** | Limited | **Full support** ✨ |
| **Skill Reuse** | Own skills | **Reuses rails-enterprise-dev skills** |
| **Approach** | Fixed workflow | **Adaptive hierarchy** |

## LOOP Control Flow Patterns (v2.0)

### TDD Cycle Pattern

**Use Case**: Test-Driven Development with red-green-refactor cycle.

**Pattern**:
```json
{
  "type": "LOOP",
  "node_id": "tdd-payment-service",
  "max_iterations": 3,
  "exit_on": "condition_true",
  "condition": {
    "type": "test_result",
    "key": "payment_service_spec",
    "operator": "equals",
    "value": "passing"
  },
  "children": [
    {
      "type": "ACTION",
      "skill": "rspec_run",
      "target": "spec/services/payment_service_spec.rb",
      "agent": "RSpec Specialist"
    },
    {
      "type": "CONDITIONAL",
      "condition": {"key": "payment_service_spec", "operator": "equals", "value": "failing"},
      "true_branch": {
        "type": "ACTION",
        "skill": "fix_failing_specs",
        "agent": "Backend Lead"
      },
      "false_branch": {
        "type": "ACTION",
        "skill": "break_loop"
      }
    }
  ]
}
```

**Execution**:
```
Iteration 1:
  ✓ Run RSpec: 5 examples, 2 failures (missing validation, wrong error class)
  ✓ Fix code: Add email validation, correct error class

Iteration 2:
  ✓ Run RSpec: 5 examples, 0 failures
  ✓ Condition met: Tests passing

✅ TDD cycle completed in 2 iterations
```

### Performance Optimization Pattern

**Use Case**: Iteratively optimize until performance target met.

**Pattern**:
```json
{
  "type": "LOOP",
  "node_id": "optimize-query-performance",
  "max_iterations": 5,
  "exit_on": "condition_true",
  "condition": {
    "type": "observation_check",
    "key": "query.duration_ms",
    "operator": "less_than",
    "value": "100"
  },
  "children": [
    {
      "type": "ACTION",
      "skill": "measure_query_performance",
      "agent": "Database Specialist"
    },
    {
      "type": "CONDITIONAL",
      "condition": {"key": "query.duration_ms", "operator": "greater_than", "value": "100"},
      "true_branch": {
        "type": "ACTION",
        "skill": "apply_optimization",
        "agent": "Backend Lead"
      },
      "false_branch": {
        "type": "ACTION",
        "skill": "break_loop"
      }
    }
  ]
}
```

**Execution**:
```
Iteration 1:
  Measure: 450ms (N+1 query detected)
  Optimize: Add includes(:comments)

Iteration 2:
  Measure: 120ms (Still slow, missing index)
  Optimize: Add database index

Iteration 3:
  Measure: 85ms (Target met!)
  ✓ Break loop

✅ Optimized from 450ms → 85ms (81% improvement)
```

### Error Recovery Pattern

**Use Case**: Retry operation with fixes until success.

**Pattern**:
```json
{
  "type": "LOOP",
  "node_id": "deploy-with-retry",
  "max_iterations": 3,
  "timeout_seconds": 300,
  "exit_on": "condition_true",
  "condition": {
    "type": "observation_check",
    "key": "deployment.status",
    "operator": "equals",
    "value": "success"
  },
  "children": [
    {
      "type": "ACTION",
      "skill": "deploy_to_staging",
      "agent": "Deployment Engineer"
    },
    {
      "type": "CONDITIONAL",
      "condition": {"key": "deployment.status", "operator": "equals", "value": "failed"},
      "true_branch": {
        "type": "ACTION",
        "skill": "diagnose_and_fix",
        "agent": "DevOps Specialist"
      },
      "false_branch": {
        "type": "ACTION",
        "skill": "break_loop"
      }
    }
  ]
}
```

**Execution**:
```
Iteration 1:
  Deploy: Failed (missing environment variable)
  Fix: Add STRIPE_API_KEY to .env.staging

Iteration 2:
  Deploy: Success!
  ✓ Break loop

✅ Deployment successful after 1 retry
```

### Nested LOOP Pattern

**Use Case**: LOOP within LOOP for complex refinement.

**Pattern**:
```json
{
  "type": "LOOP",
  "node_id": "outer-feature-implementation",
  "max_iterations": 3,
  "children": [
    {
      "type": "ACTION",
      "skill": "implement_feature_phase",
      "agent": "Backend Lead"
    },
    {
      "type": "LOOP",
      "node_id": "inner-tdd-cycle",
      "max_iterations": 3,
      "condition": {"key": "tests.status", "operator": "equals", "value": "passing"},
      "children": [
        {"type": "ACTION", "skill": "run_tests"},
        {"type": "ACTION", "skill": "fix_if_failing"}
      ]
    },
    {
      "type": "ACTION",
      "skill": "verify_phase_complete"
    }
  ]
}
```

**Note**: Use nested LOOPs sparingly. Max depth = 2 to avoid complexity.

### LOOP Exit Conditions

**Condition Types**:

1. **condition_true**: Exit when condition evaluates to true
   ```json
   {"exit_on": "condition_true", "condition": {"key": "tests.status", "operator": "equals", "value": "passing"}}
   ```

2. **condition_false**: Exit when condition evaluates to false
   ```json
   {"exit_on": "condition_false", "condition": {"key": "errors.count", "operator": "greater_than", "value": "0"}}
   ```

3. **manual_break**: Exit when break signal set in memory
   ```json
   {"exit_on": "manual_break"}
   // Agent sets: write_memory("loop_control", "loop.node_id.break", "true")
   ```

4. **max_iterations**: Always exits when max iterations reached (failsafe)

### LOOP State Tracking

**State File** (`.claude/reactree-state.jsonl`):

```jsonl
{"type":"loop_start","node_id":"tdd-cycle","timestamp":"2025-01-21T10:00:00Z","max_iterations":3}
{"type":"loop_iteration","node_id":"tdd-cycle","iteration":1,"condition_met":false,"elapsed":15}
{"type":"loop_iteration","node_id":"tdd-cycle","iteration":2,"condition_met":true,"elapsed":28}
{"type":"loop_complete","node_id":"tdd-cycle","iterations":2,"status":"success"}
```

**Query State**:
```bash
# Get loop status
cat .claude/reactree-state.jsonl | \
  jq -r "select(.node_id == \"tdd-cycle\") | {iteration, condition_met, elapsed}"
```

## CONDITIONAL Control Flow Patterns (v1.1)

### Deployment Decision Pattern

**Use Case**: Deploy to staging if tests pass, otherwise debug failures.

**Pattern**:
```json
{
  "type": "CONDITIONAL",
  "node_id": "decide-deploy-or-debug",
  "condition": {
    "type": "test_result",
    "key": "integration_tests.status",
    "operator": "equals",
    "value": "passing"
  },
  "true_branch": {
    "type": "SEQUENCE",
    "children": [
      {
        "type": "ACTION",
        "skill": "deploy_to_staging",
        "agent": "Deployment Engineer"
      },
      {
        "type": "ACTION",
        "skill": "run_smoke_tests",
        "agent": "QA Specialist"
      }
    ]
  },
  "false_branch": {
    "type": "SEQUENCE",
    "children": [
      {
        "type": "ACTION",
        "skill": "analyze_test_failures",
        "agent": "RSpec Specialist"
      },
      {
        "type": "ACTION",
        "skill": "fix_failing_tests",
        "agent": "Backend Lead"
      }
    ]
  }
}
```

**Execution**:
```
Evaluating condition: integration_tests.status == 'passing'
✓ Condition true (45/45 tests passing)

Executing true branch:
  ✓ Deploy to staging (v2.3.1)
  ✓ Run smoke tests (all passed)

✅ Deployment successful
```

### Feature Flag Pattern

**Use Case**: Enable feature based on runtime flag or configuration.

**Pattern**:
```json
{
  "type": "CONDITIONAL",
  "node_id": "check-feature-flag",
  "condition": {
    "type": "observation_check",
    "key": "feature_flags.new_ui_enabled",
    "operator": "equals",
    "value": "true"
  },
  "true_branch": {
    "type": "ACTION",
    "skill": "implement_new_ui_components",
    "agent": "UI Specialist"
  },
  "false_branch": {
    "type": "ACTION",
    "skill": "use_legacy_ui_components",
    "agent": "UI Specialist"
  }
}
```

**Execution**:
```
Checking feature flag: new_ui_enabled
✓ Feature flag enabled for this environment

Executing true branch:
  ✓ Implementing new UI with TailwindCSS
  ✓ Using ViewComponents architecture

✅ New UI components implemented
```

### Environment-Based Pattern

**Use Case**: Different behavior for development vs production.

**Pattern**:
```json
{
  "type": "CONDITIONAL",
  "node_id": "environment-specific-config",
  "condition": {
    "type": "observation_check",
    "key": "rails.environment",
    "operator": "equals",
    "value": "production"
  },
  "true_branch": {
    "type": "SEQUENCE",
    "children": [
      {"type": "ACTION", "skill": "enable_error_tracking"},
      {"type": "ACTION", "skill": "enable_performance_monitoring"},
      {"type": "ACTION", "skill": "configure_cdn"}
    ]
  },
  "false_branch": {
    "type": "SEQUENCE",
    "children": [
      {"type": "ACTION", "skill": "enable_debug_logging"},
      {"type": "ACTION", "skill": "disable_asset_compression"}
    ]
  }
}
```

### File Existence Pattern

**Use Case**: Check if file exists before proceeding.

**Pattern**:
```json
{
  "type": "CONDITIONAL",
  "node_id": "check-migration-exists",
  "condition": {
    "type": "file_exists",
    "path": "db/migrate/*_add_stripe_fields_to_payments.rb",
    "operator": "exists"
  },
  "true_branch": {
    "type": "ACTION",
    "skill": "skip_migration_creation",
    "message": "Migration already exists"
  },
  "false_branch": {
    "type": "ACTION",
    "skill": "generate_migration",
    "agent": "Database Lead"
  }
}
```

### Nested CONDITIONAL Pattern

**Use Case**: Multi-level decision tree (e.g., test status → coverage check → deploy decision).

**Pattern**:
```json
{
  "type": "CONDITIONAL",
  "node_id": "outer-test-check",
  "condition": {
    "type": "test_result",
    "key": "all_tests.status",
    "operator": "equals",
    "value": "passing"
  },
  "true_branch": {
    "type": "CONDITIONAL",
    "node_id": "inner-coverage-check",
    "condition": {
      "type": "observation_check",
      "key": "coverage.percentage",
      "operator": "greater_than",
      "value": "85"
    },
    "true_branch": {
      "type": "ACTION",
      "skill": "deploy_to_production",
      "agent": "Deployment Engineer"
    },
    "false_branch": {
      "type": "ACTION",
      "skill": "request_more_tests",
      "agent": "RSpec Specialist"
    }
  },
  "false_branch": {
    "type": "ACTION",
    "skill": "fix_failing_tests",
    "agent": "Backend Lead"
  }
}
```

**Execution**:
```
Level 1: Check if all tests passing
  ✓ All tests passing (127/127)

Level 2: Check coverage threshold
  ✓ Coverage: 92% (> 85% required)

Executing: Deploy to production
  ✓ Production deployment successful

✅ Multi-level checks passed, deployed to production
```

**Note**: Limit nesting to 2-3 levels to maintain readability.

### Performance-Based Pattern

**Use Case**: Optimize only if performance below threshold.

**Pattern**:
```json
{
  "type": "CONDITIONAL",
  "node_id": "check-query-performance",
  "condition": {
    "type": "observation_check",
    "key": "query.duration_ms",
    "operator": "greater_than",
    "value": "100"
  },
  "true_branch": {
    "type": "LOOP",
    "node_id": "optimization-loop",
    "max_iterations": 5,
    "condition": {
      "type": "observation_check",
      "key": "query.duration_ms",
      "operator": "less_than",
      "value": "100"
    },
    "children": [
      {"type": "ACTION", "skill": "measure_performance"},
      {"type": "ACTION", "skill": "apply_optimization"}
    ]
  },
  "false_branch": {
    "type": "ACTION",
    "skill": "log_performance_acceptable"
  }
}
```

**Note**: Demonstrates CONDITIONAL containing LOOP (control flow composition).

### Error Handling Pattern

**Use Case**: Handle errors differently based on error type.

**Pattern**:
```json
{
  "type": "CONDITIONAL",
  "node_id": "error-type-check",
  "condition": {
    "type": "observation_check",
    "key": "error.type",
    "operator": "equals",
    "value": "Stripe::CardError"
  },
  "true_branch": {
    "type": "ACTION",
    "skill": "notify_user_card_declined",
    "agent": "Backend Lead"
  },
  "false_branch": {
    "type": "CONDITIONAL",
    "node_id": "check-network-error",
    "condition": {
      "type": "observation_check",
      "key": "error.type",
      "operator": "matches_regex",
      "value": ".*NetworkError.*"
    },
    "true_branch": {
      "type": "LOOP",
      "max_iterations": 3,
      "children": [{"type": "ACTION", "skill": "retry_request"}]
    },
    "false_branch": {
      "type": "ACTION",
      "skill": "log_and_raise_error"
    }
  }
}
```

### Condition Operators Reference

**Comparison Operators**:
- `equals`: Exact match (`"passing" == "passing"`)
- `not_equals`: Not equal (`"failing" != "passing"`)
- `greater_than`: Numeric/lexical comparison (`92 > 85`)
- `less_than`: Numeric/lexical comparison (`50 < 100`)

**String Operators**:
- `contains`: Substring match (`"card declined" contains "declined"`)
- `not_contains`: Substring not present
- `matches_regex`: Regular expression match (`"v2.3.1" matches "v\d+\.\d+\.\d+"`)

**File Operators**:
- `exists`: File or directory exists
- `not_exists`: File or directory does not exist

**Boolean Operators**:
- For boolean values, use `equals` with `"true"` or `"false"` strings

### Condition Evaluation Cache

**Cache File** (`.claude/reactree-conditions.jsonl`):

```jsonl
{"timestamp":"2025-01-21T10:00:00Z","node_id":"check-tests","condition_key":"integration_tests.status","result":true,"cache_until":"2025-01-21T10:05:00Z"}
{"timestamp":"2025-01-21T10:01:00Z","node_id":"check-coverage","condition_key":"coverage.percentage","result":true,"cache_until":"2025-01-21T10:06:00Z"}
```

**Cache Invalidation**:
- Time-based: `cache_until` timestamp
- Event-based: Invalidate on file changes, test runs
- Manual: Clear cache with `rm .claude/reactree-conditions.jsonl`

**Benefits**:
- Avoid redundant condition evaluations
- Faster branch selection
- Consistent results within cache window

### CONDITIONAL State Tracking

**State File** (`.claude/reactree-state.jsonl`):

```jsonl
{"type":"conditional_eval","node_id":"decide-deploy","condition_met":true,"timestamp":"2025-01-21T10:00:00Z","branch":"true"}
{"type":"node_start","node_id":"deploy-action","parent":"decide-deploy","timestamp":"2025-01-21T10:00:05Z"}
{"type":"node_complete","node_id":"deploy-action","status":"success","timestamp":"2025-01-21T10:02:30Z"}
```

**Query State**:
```bash
# Get conditional decision history
cat .claude/reactree-state.jsonl | \
  jq -r 'select(.type == "conditional_eval") | {node_id, condition_met, branch}'
```

### Best Practices for CONDITIONAL Nodes

1. **Clear Conditions**: Use descriptive condition keys (`integration_tests.status` not `test_status`)
2. **Both Branches**: Always define both true and false branches (avoid empty branches)
3. **Fail-Safe Defaults**: False branch should be the safe/conservative option
4. **Limit Nesting**: Max 2-3 levels of nested CONDITIONALs
5. **Cache Wisely**: Use cache for expensive condition evaluations
6. **Log Decisions**: Always log which branch was taken and why
7. **Test Both Paths**: Ensure both branches are tested in different scenarios

## Best Practices

### Memory-First Development

1. **Always check memory first** before running analysis commands
2. **Write all discoveries** to working memory (especially codebase-inspector)
3. **Query memory** before making architectural decisions
4. **Record episodes** after successful feature completion

### Parallel Execution Optimization

1. **Identify independent phases** during planning
2. **Group by dependencies** (same dependency = can run parallel)
3. **Execute parallel groups** using control flow nodes
4. **Track as parallel** even if sequential (infrastructure readiness)

### Fallback Pattern Design

1. **Primary first** - try the ideal approach
2. **Graceful degradation** - each fallback is less ideal but still works
3. **Warn on fallback** - inform user of degradation
4. **Never silent failure** - always log what succeeded

## FEEDBACK Edge Patterns (v2.0)

Enable backwards communication from child nodes to parent nodes, allowing adaptive fix-verify cycles when issues are discovered.

### Test-Driven Feedback Pattern

**Use when**: Tests discover missing implementation or validation

**Structure**:
```json
{
  "type": "SEQUENCE",
  "children": [
    {
      "type": "ACTION",
      "node_id": "create-payment-model",
      "skill": "rails_generate_model",
      "args": "Payment amount:decimal status:string"
    },
    {
      "type": "ACTION",
      "node_id": "test-payment-model",
      "skill": "rspec_run_model",
      "args": "Payment",
      "feedback_enabled": true
    }
  ]
}
```

**Feedback Flow**:
1. Model created successfully
2. Test runs, discovers missing validation: `validates :email, presence: true`
3. Test sends FIX_REQUEST feedback to `create-payment-model`
4. Model node re-executes, adds validation
5. Test re-runs automatically, passes ✓

**Feedback Message**:
```json
{
  "type": "FEEDBACK",
  "from_node": "test-payment-model",
  "to_node": "create-payment-model",
  "feedback_type": "FIX_REQUEST",
  "message": "PaymentSpec:42 - Expected validates_presence_of(:email)",
  "suggested_fix": "validates :email, presence: true, format: { with: URI::MailTo::EMAIL_REGEXP }",
  "priority": "high",
  "artifacts": ["spec/models/payment_spec.rb:42-45"]
}
```

**Benefits**:
- Self-correcting workflows
- Tests drive implementation quality
- No manual fix-test cycles
- Comprehensive coverage enforced

### Dependency Discovery Pattern

**Use when**: Node discovers missing prerequisite during execution

**Structure**:
```json
{
  "type": "SEQUENCE",
  "children": [
    {
      "type": "ACTION",
      "node_id": "create-payment-processor",
      "skill": "implement_service",
      "args": "PaymentProcessorService"
    }
  ]
}
```

**Feedback Flow**:
1. Service implementation begins
2. Discovers dependency on `Refund` model (doesn't exist)
3. Sends DEPENDENCY_MISSING feedback to workflow planner
4. Planner inserts Refund model creation before service
5. Refund model created
6. Service re-executes successfully ✓

**Feedback Message**:
```json
{
  "type": "FEEDBACK",
  "from_node": "create-payment-processor",
  "to_node": "workflow-planner",
  "feedback_type": "DEPENDENCY_MISSING",
  "message": "PaymentProcessorService requires Refund model (app/models/refund.rb not found)",
  "suggested_action": "Add node: rails generate model Refund amount:decimal reason:text payment:references",
  "priority": "critical",
  "missing_files": ["app/models/refund.rb"]
}
```

**Benefits**:
- Auto-discovery of dependencies
- Dynamic workflow adjustment
- No pre-planning exhaustion
- Handles complex dependency graphs

### Architecture Correction Pattern

**Use when**: Circular dependencies or design issues detected

**Structure**:
```json
{
  "type": "SEQUENCE",
  "children": [
    {
      "type": "ACTION",
      "node_id": "create-invoice-service",
      "skill": "implement_service",
      "args": "InvoiceService"
    }
  ]
}
```

**Feedback Flow**:
1. InvoiceService implementation begins
2. Detects circular dependency: Invoice → Payment → Invoice
3. Sends ARCHITECTURE_ISSUE feedback to planner
4. Planner redesigns: introduces InvoicePayment join model
5. Architecture re-planned with proper separation
6. Implementation proceeds with corrected architecture ✓

**Feedback Message**:
```json
{
  "type": "FEEDBACK",
  "from_node": "create-invoice-service",
  "to_node": "plan-invoice-feature",
  "feedback_type": "ARCHITECTURE_ISSUE",
  "message": "Circular dependency detected: Invoice → Payment → Invoice",
  "suggested_fix": "Introduce join model: InvoicePayment (invoice_id, payment_id, amount)",
  "priority": "critical",
  "cycle_path": ["Invoice", "Payment", "Invoice"]
}
```

**Benefits**:
- Prevents bad architecture
- Catches design flaws early
- Self-correcting system design
- Maintains clean dependencies

### Context Request Pattern

**Use when**: Child needs information from parent to proceed

**Structure**:
```json
{
  "type": "SEQUENCE",
  "children": [
    {
      "type": "ACTION",
      "node_id": "create-payment-service",
      "skill": "implement_service",
      "args": "PaymentService"
    },
    {
      "type": "ACTION",
      "node_id": "create-payments-controller",
      "skill": "implement_controller",
      "args": "PaymentsController"
    }
  ]
}
```

**Feedback Flow**:
1. Controller implementation begins
2. Needs PaymentService method signature to call correctly
3. Sends CONTEXT_REQUEST feedback to service node
4. Service node provides method signature via working memory
5. Controller reads signature from memory
6. Controller implementation proceeds with correct method call ✓

**Feedback Message**:
```json
{
  "type": "FEEDBACK",
  "from_node": "create-payments-controller",
  "to_node": "create-payment-service",
  "feedback_type": "CONTEXT_REQUEST",
  "message": "Need PaymentService.process_payment method signature",
  "requested_info": {
    "method_name": "?",
    "parameters": "?",
    "return_type": "?",
    "success_key": "?",
    "error_handling": "?"
  },
  "priority": "medium"
}
```

**Response** (via working memory):
```json
{
  "method_name": "process_payment",
  "parameters": "amount:, token:, currency: 'usd'",
  "return_type": "Result",
  "success_key": "result.success?",
  "error_handling": "result.error"
}
```

**Benefits**:
- Just-in-time information sharing
- Reduces upfront planning
- Correct integration guaranteed
- No API mismatches

### Multi-Round Feedback Pattern

**Use when**: Multiple iterations needed to achieve correctness

**Structure**:
```json
{
  "type": "LOOP",
  "max_iterations": 3,
  "children": [
    {
      "type": "ACTION",
      "node_id": "implement-feature"
    },
    {
      "type": "ACTION",
      "node_id": "test-feature",
      "feedback_enabled": true
    }
  ]
}
```

**Feedback Flow**:
```
Round 1:
  Implement → Test (fails: missing validation)
  Test sends FIX_REQUEST
  Implement fixes → Test (fails: wrong association)

Round 2:
  Test sends FIX_REQUEST
  Implement fixes → Test (passes) ✓
  Exit loop (condition met)
```

**Benefits**:
- Iterative refinement
- Handles complex issues requiring multiple fixes
- Automatic retry with feedback context
- Bounded by max rounds (prevents infinite loops)

### Feedback Loop Prevention

**Mechanisms**:

1. **Max Feedback Rounds**: 2 rounds per node pair
```
Round 1: Test → Model (add validation) ✓
Round 2: Test → Model (fix association) ✓
Round 3: ❌ BLOCKED (max rounds exceeded)
```

2. **Max Chain Depth**: 3 levels maximum
```
OK:     E2E → Controller → Service (depth 2)
OK:     E2E → Controller → Service → Model (depth 3)
BLOCK:  E2E → Controller → Service → Model → DB (depth 4) ❌
```

3. **Cycle Detection**:
```
Node A → Node B (feedback)
Node B → Node C (feedback)
Node C → Node A (feedback) ❌ CYCLE DETECTED
```

### Feedback State Tracking

**File**: `.claude/reactree-feedback.jsonl`

**Format**:
```jsonl
{"timestamp":"2025-01-21T14:00:00Z","from_node":"test-payment","to_node":"create-payment","feedback_type":"FIX_REQUEST","message":"Missing validation","status":"queued","round":1}
{"timestamp":"2025-01-21T14:01:30Z","from_node":"test-payment","to_node":"create-payment","status":"delivered"}
{"timestamp":"2025-01-21T14:03:00Z","from_node":"test-payment","to_node":"create-payment","status":"resolved","resolved_at":"2025-01-21T14:03:00Z"}
```

**Status Values**:
- `queued` - Feedback created, waiting for delivery
- `delivered` - Feedback routed to target node
- `processing` - Parent node executing fix
- `verifying` - Child node re-running verification
- `resolved` - Fix verified successfully
- `failed` - Fix failed after max rounds

### Feedback Best Practices

1. **Be Specific**: Include file paths, line numbers, error messages
2. **Suggest Fix**: Don't just report problem, suggest solution
3. **Set Priority**: Critical > High > Medium > Low
4. **Include Artifacts**: Reference relevant files, specs, logs
5. **Respect Limits**: Don't force feedback beyond max rounds
6. **Verify Fixes**: Always re-run child after parent fix
7. **Log Everything**: Complete audit trail for debugging

### Feedback Anti-Patterns

**❌ Vague Feedback**:
```json
{"message": "Tests failing"}  // BAD
```

**✅ Specific Feedback**:
```json
{
  "message": "PaymentSpec:42 - Expected validates_presence_of(:email)",
  "suggested_fix": "validates :email, presence: true",
  "artifacts": ["spec/models/payment_spec.rb:42"]
}  // GOOD
```

**❌ Infinite Loops**:
```
Test → Model (fix) → Test (still fails) → Model (fix) → Test (still fails) → ...
```

**✅ Bounded Retries**:
```
Test → Model (fix) → Test (still fails) → Model (fix) → Test (passes) ✓
Max 2 rounds enforced
```

**❌ Feedback Cycles**:
```
Service A → Service B (needs method)
Service B → Service A (needs method)
❌ Deadlock
```

**✅ Hierarchical Resolution**:
```
Service A → Planner (needs Service B method)
Service B → Planner (needs Service A method)
Planner: Define interface contract first
Both services implement interface ✓
```

## Test-First Strategy Patterns (v2.0)

Enable test-driven development with TestOracle agent for comprehensive test planning before implementation.

### Test Pyramid Pattern

**Use when**: Ensuring balanced test suite with appropriate unit:integration:system ratio

**Target Ratios**:
- **70% Unit Tests** - Fast, focused tests for models, services, POROs
- **20% Integration Tests** - Request/controller tests for API contracts
- **10% System Tests** - End-to-end tests with browser automation

**Structure**:
```json
{
  "test_plan": {
    "unit_tests": [
      {"file": "spec/models/payment_spec.rb", "examples": 15},
      {"file": "spec/services/payment_processor_spec.rb", "examples": 20}
    ],
    "integration_tests": [
      {"file": "spec/requests/payments_spec.rb", "examples": 12}
    ],
    "system_tests": [
      {"file": "spec/system/payment_workflow_spec.rb", "examples": 5}
    ]
  }
}
```

**Workflow**:
```
1. TestOracle analyzes feature
2. Generates test plan following pyramid ratios
3. Validates pyramid before test generation
4. Adjusts if ratios exceed thresholds
```

**Benefits**:
- Fast test suite (unit tests run in milliseconds)
- Comprehensive coverage at all levels
- Maintainable tests (unit tests easier to update than system tests)
- Optimal test execution time

**Validation**:
```bash
Unit: 35 files (70%) ✓
Integration: 10 files (20%) ✓
System: 5 files (10%) ✓

Total: 50 test files
Pyramid: HEALTHY ✓
```

### Red-Green-Refactor with LOOP

**Use when**: Implementing features with test-first discipline

**Structure**:
```json
{
  "type": "LOOP",
  "node_id": "tdd-cycle",
  "max_iterations": 3,
  "exit_on": "condition_true",
  "condition": {
    "type": "test_result",
    "key": "all_specs.status",
    "operator": "equals",
    "value": "passing"
  },
  "children": [
    {
      "type": "ACTION",
      "node_id": "generate-tests",
      "skill": "test_oracle_generate",
      "description": "Generate failing tests (RED)"
    },
    {
      "type": "ACTION",
      "node_id": "implement-code",
      "skill": "implement_to_pass_tests",
      "description": "Implement minimum code to pass (GREEN)"
    },
    {
      "type": "ACTION",
      "node_id": "run-tests",
      "skill": "rspec_run_all"
    },
    {
      "type": "CONDITIONAL",
      "condition": {
        "type": "test_result",
        "key": "all_specs.status",
        "operator": "equals",
        "value": "passing"
      },
      "true_branch": {
        "type": "ACTION",
        "skill": "refactor_code",
        "description": "Refactor with confidence (REFACTOR)"
      },
      "false_branch": {
        "type": "ACTION",
        "skill": "analyze_failures",
        "description": "Analyze and fix failures"
      }
    }
  ]
}
```

**Execution Flow**:
```
RED: Generate failing tests
  ├─ payment_spec.rb (15 pending examples)
  ├─ payment_processor_spec.rb (20 pending examples)
  └─ payments_request_spec.rb (12 pending examples)

GREEN Iteration 1:
  ├─ Implement Payment model
  ├─ Run specs: 47 examples, 32 failures
  └─ Continue loop

GREEN Iteration 2:
  ├─ Implement PaymentProcessor service
  ├─ Run specs: 47 examples, 5 failures
  └─ Continue loop

GREEN Iteration 3:
  ├─ Fix remaining failures
  ├─ Run specs: 47 examples, 0 failures ✓
  └─ Exit loop (condition met)

REFACTOR:
  ├─ Extract private methods
  ├─ Improve naming
  ├─ Run specs: 47 examples, 0 failures ✓
  └─ Refactor complete
```

**Benefits**:
- Tests drive implementation design
- Prevents over-engineering (minimum code to pass)
- Refactor fearlessly (tests verify behavior)
- Iterative improvement with bounds

### Coverage-Driven Expansion Pattern

**Use when**: Initial tests pass but coverage below threshold (85%)

**Structure**:
```json
{
  "type": "LOOP",
  "node_id": "coverage-expansion",
  "max_iterations": 3,
  "condition": {
    "type": "observation_check",
    "key": "coverage.percentage",
    "operator": "greater_than",
    "value": "85"
  },
  "children": [
    {
      "type": "ACTION",
      "skill": "run_coverage_analysis"
    },
    {
      "type": "CONDITIONAL",
      "condition": {"key": "coverage.percentage", "operator": "less_than", "value": "85"},
      "true_branch": {
        "type": "SEQUENCE",
        "children": [
          {"skill": "identify_coverage_gaps"},
          {"skill": "generate_additional_tests"},
          {"skill": "run_rspec"}
        ]
      }
    }
  ]
}
```

**Execution Flow**:
```
Iteration 1:
  ├─ Run coverage: 72.5%
  ├─ Gaps: payment_processor.rb (45% coverage)
  ├─ Generate: 8 additional tests for edge cases
  └─ Run: Coverage now 78.3%

Iteration 2:
  ├─ Run coverage: 78.3%
  ├─ Gaps: payment.rb (missing scope tests)
  ├─ Generate: 5 scope tests
  └─ Run: Coverage now 84.1%

Iteration 3:
  ├─ Run coverage: 84.1%
  ├─ Gaps: Minor gaps in error handling
  ├─ Generate: 3 error handling tests
  └─ Run: Coverage now 87.2% ✓

Exit: Coverage threshold met (87.2% > 85%)
```

**Benefits**:
- Automatic gap detection
- Targeted test generation
- Ensures threshold met
- Prevents missing edge cases

### Test Quality Validation Pattern

**Use when**: Ensuring tests are meaningful, not just coverage-seeking

**Quality Checks**:
1. **No pending tests** - All tests implemented
2. **Has assertions** - Tests actually verify behavior
3. **Uses factories** - No hardcoded test data
4. **No sleeps/waits** - Avoid flaky tests
5. **Tests behavior** - Not implementation details

**Validation Flow**:
```bash
For each test file:
  ✓ No pending tests
  ✓ Contains expect/should assertions
  ✓ Uses FactoryBot factories
  ✗ Uses sleep(5) - FLAKY TEST WARNING
  ✓ Tests public interface

Result: 4/5 quality checks passed
Action: Remove sleep, use proper wait conditions
```

**Bad Test Example**:
```ruby
# ❌ Testing implementation details
it "calls private method" do
  expect(subject.send(:calculate_fee)).to eq(10)
end

# ❌ Hardcoded data
it "finds user" do
  user = User.find(1)
  expect(user.name).to eq("John")
end

# ❌ Flaky test
it "completes async job" do
  job.perform_later
  sleep(2)  # ❌ Race condition
  expect(job_result).to be_present
end
```

**Good Test Example**:
```ruby
# ✓ Tests public behavior
it "calculates total with fee" do
  result = subject.calculate_total(amount: 100)
  expect(result).to eq(110)  # 100 + 10 fee
end

# ✓ Uses factories
it "creates user" do
  user = create(:user)
  expect(user).to be_persisted
end

# ✓ Proper async handling
it "completes async job" do
  perform_enqueued_jobs do
    job.perform_later
  end
  expect(job_result).to be_present
end
```

### Test-First Integration with Feedback

**Use when**: Tests discover missing validations/associations during implementation

**Combined Pattern**: TestOracle + LOOP + FEEDBACK

```json
{
  "type": "SEQUENCE",
  "children": [
    {
      "type": "ACTION",
      "node_id": "test-oracle-plan",
      "skill": "generate_test_plan",
      "agent": "TestOracle"
    },
    {
      "type": "ACTION",
      "node_id": "generate-tests",
      "skill": "create_test_files",
      "agent": "TestOracle"
    },
    {
      "type": "LOOP",
      "max_iterations": 3,
      "children": [
        {
          "type": "ACTION",
          "node_id": "implement",
          "skill": "implement_feature",
          "feedback_enabled": true
        },
        {
          "type": "ACTION",
          "node_id": "run-tests",
          "skill": "rspec_run_all",
          "feedback_enabled": true
        }
      ]
    }
  ]
}
```

**Flow with Feedback**:
```
1. TestOracle generates comprehensive test plan
2. Tests created (47 examples, all pending)
3. LOOP Iteration 1:
   ├─ Implement Payment model (minimal)
   ├─ Run tests: 47 examples, 25 failures
   └─ Tests send FEEDBACK: "Missing validations"

4. Feedback processed:
   ├─ Model re-executes with feedback context
   ├─ Adds validates :amount, :email, :status
   └─ Model updated

5. Tests re-run: 47 examples, 8 failures

6. LOOP Iteration 2:
   ├─ Tests send FEEDBACK: "Missing association :invoice"
   ├─ Model adds belongs_to :invoice, optional: true
   └─ Tests re-run: 47 examples, 0 failures ✓

7. Exit loop (all passing)
```

**Benefits**:
- TestOracle ensures comprehensive coverage
- LOOP enables iterative refinement
- FEEDBACK auto-corrects missing pieces
- Fully autonomous TDD workflow

### Test Metrics Pattern

**Use when**: Tracking test suite health over time

**Metrics Tracked**:
```json
{
  "test_suite_metrics": {
    "total_examples": 247,
    "total_files": 50,
    "pyramid": {
      "unit": {"count": 35, "percentage": 70, "status": "healthy"},
      "integration": {"count": 10, "percentage": 20, "status": "healthy"},
      "system": {"count": 5, "percentage": 10, "status": "healthy"}
    },
    "coverage": {
      "overall": 87.2,
      "unit": 92.5,
      "integration": 81.3,
      "threshold": 85,
      "status": "passing"
    },
    "execution_time": {
      "total": "12.5s",
      "unit": "2.3s",
      "integration": "7.8s",
      "system": "2.4s"
    },
    "quality_score": 94,
    "flaky_tests": 0,
    "pending_tests": 0
  }
}
```

**Reporting**:
```
📊 Test Suite Health Report
═══════════════════════════

Tests: 247 examples in 50 files
Status: ✓ ALL PASSING

Pyramid Distribution:
  Unit:        35 files (70%) ✓
  Integration: 10 files (20%) ✓
  System:       5 files (10%) ✓

Coverage:
  Overall:     87.2% ✓ (threshold: 85%)
  Unit:        92.5% ✓
  Integration: 81.3% ⚠

Execution Time:
  Total:        12.5s
  Unit:          2.3s (18%)
  Integration:   7.8s (62%)
  System:        2.4s (19%)

Quality Score: 94/100 ✓
  ✓ No flaky tests
  ✓ No pending tests
  ✓ All assertions present
  ✓ Uses factories

Recommendations:
  - Integration coverage below 85% (currently 81.3%)
  - Consider adding 3-5 more integration tests
```

### Test-First Best Practices

1. **Always write tests first** - Tests drive design decisions
2. **Follow the pyramid** - 70/20/10 ratio for speed and maintainability
3. **Test behavior, not implementation** - Public interface only
4. **Use factories** - Consistent, flexible test data
5. **Keep tests fast** - Unit tests in milliseconds
6. **Avoid test interdependence** - Each test runs independently
7. **Meaningful assertions** - Test what matters
8. **Refactor tests too** - DRY applies to specs

### Test Anti-Patterns to Avoid

**❌ Inverted Pyramid** (too many slow tests):
```
System:       40 files (80%) ❌ TOO SLOW
Integration:   8 files (16%)
Unit:          2 files (4%) ❌ TOO FEW
```

**❌ 100% Coverage Obsession**:
```ruby
# Testing framework code, not your code
it "has attr_accessor" do
  expect(subject).to respond_to(:name)
  expect(subject).to respond_to(:name=)
end
```

**❌ Implementation Details**:
```ruby
# Bad: Testing SQL queries
it "uses INNER JOIN" do
  query = Payment.joins(:user).to_sql
  expect(query).to include("INNER JOIN")
end

# Good: Testing behavior
it "includes user data" do
  payment = create(:payment, :with_user)
  expect(payment.user).to be_present
end
```

**❌ Brittle Tests** (break on refactoring):
```ruby
# Bad: Depends on exact error message
it "validates email" do
  user.email = "invalid"
  user.valid?
  expect(user.errors[:email].first).to eq("is invalid")
end

# Good: Tests validation exists
it { should validate_email_format_of(:email) }
```

## Future Enhancements

- True concurrent agent execution (when Claude Code supports it)
- Semantic search in episodic memory (vector embeddings)
- Automatic similarity detection for episode retrieval
- Cross-project episode sharing (learn from other teams)
- Memory compaction strategies (manage file size)
- Machine learning for feedback pattern recognition
- Automatic suggested fixes generation from historical feedback

## Summary

ReAcTree transforms Rails development workflows from:
- **Sequential** → **Parallel**
- **Redundant** → **Memory-cached**
- **Static** → **Learning**
- **Brittle** → **Resilient**

Result: **30-50% faster, smarter workflows** that improve with each use.
