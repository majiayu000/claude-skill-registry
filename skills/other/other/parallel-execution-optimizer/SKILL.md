---
name: parallel-execution-optimizer
description: Identify and execute independent operations in parallel for 3-5x speedup. Auto-analyzes task dependencies, groups into batches, launches parallel Task() calls. Applies to /optimize (5 checks), /ship pre-flight (5 checks), /implement (task batching), /prototype (N screens). Auto-triggers when detecting multiple independent operations in a phase.
---

<objective>
The parallel-execution-optimizer skill transforms sequential workflows into concurrent execution patterns, dramatically reducing wall-clock time for phases with multiple independent operations.

Traditional sequential execution wastes time:

- /optimize runs 5 quality checks sequentially (10-15 minutes)
- /ship runs 5 pre-flight checks sequentially (8-12 minutes)
- /implement processes tasks one-by-one despite no dependencies
- Prototype screens generated sequentially when all could run in parallel

This skill analyzes operation dependencies, groups independent work into batches, and orchestrates parallel execution using multiple Task() agent calls in a single message. The result: 3-5x faster phase completion with zero compromise on quality or correctness.
</objective>

<quick_start>
<basic_pattern>
When you detect multiple independent operations, send **a single message** with multiple tool calls:

**Sequential (slow)**:

- Send message with Task call for security-sentry
- Wait for response
- Send message with Task call for performance-profiler
- Wait for response
- Send message with Task call for accessibility-auditor
- Total: 15 minutes

**Parallel (fast)**:

- Send ONE message with 3 Task calls (security-sentry, performance-profiler, accessibility-auditor)
- All three run concurrently
- Total: 5 minutes
  </basic_pattern>

<immediate_use_cases>

1. **/optimize phase**: Run 5 quality checks in parallel (security, performance, accessibility, code-review, type-safety)
2. **/ship pre-flight**: Run 5 deployment checks in parallel (env-vars, build, docker, CI-config, dependency-audit)
3. **/implement**: Process independent task batches in parallel layers
4. **Design variations**: Generate multiple mockup variations concurrently
5. **Research phase**: Fetch multiple documentation sources concurrently
   </immediate_use_cases>
   </quick_start>

<workflow>
<step number="1">
**Identify independent operations**

Scan the current phase for operations that:

- Read different files/data sources
- Don't modify shared state
- Have no sequential dependencies
- Can produce results independently

Examples:

- Quality checks (security scan + performance test + accessibility audit)
- File reads (spec.md + plan.md + tasks.md)
- API documentation fetches (Stripe docs + Twilio docs + SendGrid docs)
- Test suite runs (unit tests + integration tests + E2E tests)
  </step>

<step number="2">
**Analyze dependencies**

Build a dependency graph:

- **Layer 0**: Operations with no dependencies (can run immediately)
- **Layer 1**: Operations depending only on Layer 0 outputs
- **Layer 2**: Operations depending on Layer 1 outputs
- etc.

Example (/optimize):

```
Layer 0 (parallel):
  - security-sentry (reads codebase)
  - performance-profiler (reads codebase + runs benchmarks)
  - accessibility-auditor (reads UI components)
  - type-enforcer (reads TypeScript files)
  - dependency-curator (reads package.json)

Layer 1 (after Layer 0):
  - Generate optimization-report.md (combines all Layer 0 results)
```

</step>

<step number="3">
**Group into batches**

Create batches for each layer:

- All Layer 0 operations in single message (parallel execution)
- Wait for Layer 0 completion
- All Layer 1 operations in single message
- Continue through layers

Batch size considerations:

- **Optimal**: 3-5 operations per batch (balanced parallelism)
- **Maximum**: 8 operations (avoid overwhelming system)
- **Minimum**: 2 operations (below 2, parallelism has no benefit)
  </step>

<step number="4">
**Execute parallel batches**

Send a single message with multiple tool calls for each batch.

Critical requirements:

- Must be a **single message** with multiple tool use blocks
- Each tool call must be complete and independent
- Do not use placeholders or forward references
- Each agent must have all required context in its prompt

See [references/execution-patterns.md](references/execution-patterns.md) for detailed examples.
</step>

<step number="5">
**Aggregate results**

After each batch completes:

- Collect results from all parallel operations
- Check for failures or blocking issues
- Decide whether to proceed to next layer
- Aggregate findings into unified report

Failure handling:

- If any operation blocks (critical security issue), halt pipeline
- If operations have warnings (minor performance issue), continue but log
- If operations fail (agent error), retry individually or escalate
  </step>
  </workflow>

<phase_specific_patterns>
<optimize_phase>
**Operation**: Run 5 quality gates in parallel

**Dependency graph**:

```
Layer 0 (parallel - 5 operations):
  1. security-sentry → Scan for vulnerabilities, secrets, auth issues
  2. performance-profiler → Benchmark API endpoints, detect N+1 queries
  3. accessibility-auditor → WCAG 2.1 AA compliance (if UI feature)
  4. type-enforcer → TypeScript strict mode compliance
  5. dependency-curator → npm audit, outdated packages

Layer 1 (sequential - 1 operation):
  6. Generate optimization-report.md (aggregates Layer 0 findings)
```

**Time savings**:

- Sequential: ~15 minutes (3 min per check)
- Parallel: ~5 minutes (longest check + aggregation)
- **Speedup**: 3x

See [references/optimize-phase-parallelization.md](references/optimize-phase-parallelization.md) for implementation details.
</optimize_phase>

<ship_preflight>
**Operation**: Run 5 pre-flight checks in parallel

**Dependency graph**:

```
Layer 0 (parallel - 5 operations):
  1. Check environment variables (read .env.example vs .env)
  2. Validate production build (npm run build)
  3. Check Docker configuration (docker-compose.yml, Dockerfile)
  4. Validate CI configuration (.github/workflows/*.yml)
  5. Run dependency audit (npm audit --production)

Layer 1 (sequential - 1 operation):
  6. Update state.yaml with pre-flight results
```

**Time savings**:

- Sequential: ~12 minutes
- Parallel: ~4 minutes (build is longest operation)
- **Speedup**: 3x

See [references/ship-preflight-parallelization.md](references/ship-preflight-parallelization.md).
</ship_preflight>

<implement_phase>
**Operation**: Execute independent task batches in parallel

**Dependency analysis**:

1. Read tasks.md
2. Build dependency graph from task relationships
3. Identify tasks with no dependencies (Layer 0)
4. Group tasks by layer

**Example** (15 tasks):

```
Layer 0 (4 tasks - parallel):
  T001: Create User model
  T002: Create Product model
  T005: Setup test framework
  T008: Create API client utility

Layer 1 (3 tasks - parallel, depend on Layer 0):
  T003: User CRUD endpoints (needs T001)
  T004: Product CRUD endpoints (needs T002)
  T009: Write User model tests (needs T001, T005)

Layer 2 (2 tasks - parallel):
  T006: User-Product relationship (needs T001, T002)
  T010: Write Product model tests (needs T002, T005)

Layer 3 (sequential):
  T007: Integration tests (needs all above)
```

**Execution**:

- Batch 1: Launch 4 agents for Layer 0 tasks (parallel)
- Batch 2: Launch 3 agents for Layer 1 tasks (parallel)
- Batch 3: Launch 2 agents for Layer 2 tasks (parallel)
- Batch 4: Single agent for Layer 3

**Time savings**:

- Sequential: 15 tasks × 20 min = 300 minutes (5 hours)
- Parallel: 4 batches × 30 min = 120 minutes (2 hours)
- **Speedup**: 2.5x

See [references/implement-phase-parallelization.md](references/implement-phase-parallelization.md).
</implement_phase>

<prototype_screens>
**Operation**: Generate multiple prototype screens in parallel

**Use case**: User wants to create 3 different screens (login, dashboard, settings)

**Sequential approach** (slow):

1. Generate login screen
2. Generate dashboard screen
3. Generate settings screen
   Total: 15 minutes

**Parallel approach** (fast):

1. Launch 3 screen agents in single message (login, dashboard, settings)
   Total: 5 minutes (all generate concurrently)

**Speedup**: 3x

Note: All screens share theme.yaml for consistency.
</prototype_screens>
</phase_specific_patterns>

<dependency_analysis>
<determining_independence>
Two operations are independent if:

1. **Read-only access to shared resources**: Both only read the same files (safe to parallelize)
2. **Disjoint file access**: They read/write completely different files
3. **No temporal dependencies**: Neither requires the other's output
4. **Idempotent operations**: Running them in any order produces same result

Two operations are **dependent** if:

1. **Write-after-read**: Operation B reads file that Operation A writes
2. **Write-after-write**: Both write to same file (race condition)
3. **Data dependency**: Operation B needs Operation A's output as input
4. **Order-dependent side effects**: Operations modify shared state
   </determining_independence>

<common_patterns>
**Independent** (safe to parallelize):

- Multiple quality checks reading codebase
- Multiple file reads (spec.md, plan.md, tasks.md)
- Multiple API documentation fetches
- Multiple test suite runs (if isolated)
- Multiple lint checks on different file types

**Dependent** (must sequence):

- Generate code → Run tests on generated code
- Fetch API docs → Generate client based on docs
- Write file → Read file back for validation
- Create database schema → Run migrations
- Build project → Deploy built artifacts
  </common_patterns>

<edge_cases>
**Shared mutable state**: If operations modify the same git branch, database, or filesystem location, they CANNOT run in parallel safely.

**Resource contention**: Even if logically independent, operations competing for same resource (CPU, memory, network) may not see speedup. Monitor system resources.

**Cascading failures**: If one parallel operation fails and others depend on it indirectly, you may need to cancel or retry the batch.
</edge_cases>
</dependency_analysis>

<auto_trigger_conditions>
<when_to_apply>
Automatically apply parallel execution when you detect:

1. **Multiple quality checks**: ≥3 independent checks in /optimize or /ship
2. **Multiple file reads**: ≥3 files to read that don't depend on each other
3. **Multiple API calls**: ≥2 external API documentation fetches
4. **Batch task processing**: ≥5 tasks in /implement with identifiable layers
5. **Multiple test suites**: Unit, integration, E2E running independently
6. **Multiple design variations**: ≥2 mockup/prototype variants requested
7. **Multiple research queries**: ≥3 web searches or documentation lookups
   </when_to_apply>

<when_not_to_apply>
Do NOT parallelize when:

1. **Sequential dependencies exist**: Operation B needs Operation A's output
2. **Shared state modification**: Operations write to same files/database
3. **Small operation count**: <2 independent operations (no benefit)
4. **Complex coordination needed**: Results must be merged in specific order
5. **User explicitly requests sequential**: "Do X, then Y, then Z"
   </when_not_to_apply>

<proactive_detection>
Scan for these phrases in phase workflows:

- "Run these checks: A, B, C, D, E" → Parallel candidate
- "Generate variations: X, Y, Z" → Parallel candidate
- "Fetch documentation for: Service1, Service2, Service3" → Parallel candidate
- "Execute tasks: T001, T002, T003 (no dependencies)" → Parallel candidate

When detected, immediately analyze dependencies and propose parallel execution strategy.
</proactive_detection>
</auto_trigger_conditions>

<examples>
<example name="/optimize-phase-parallelization">
**Context**: Running /optimize on a feature with UI components

**Sequential execution** (15 minutes):

```
1. Launch security-sentry (3 min)
2. Wait for completion
3. Launch performance-profiler (4 min)
4. Wait for completion
5. Launch accessibility-auditor (3 min)
6. Wait for completion
7. Launch type-enforcer (2 min)
8. Wait for completion
9. Launch dependency-curator (2 min)
10. Wait for completion
11. Aggregate results (1 min)
Total: 15 minutes
```

**Parallel execution** (5 minutes):

```
1. Launch 5 agents in SINGLE message:
   - security-sentry
   - performance-profiler
   - accessibility-auditor
   - type-enforcer
   - dependency-curator
2. All run concurrently (longest is 4 min)
3. Aggregate results (1 min)
Total: 5 minutes
```

**Implementation**: See [examples/optimize-phase-parallel.md](examples/optimize-phase-parallel.md)
</example>

<example name="/ship-preflight-parallelization">
**Context**: Running pre-flight checks before deployment

**Sequential execution** (12 minutes):

```
1. Check env vars (1 min)
2. Run build (5 min)
3. Check Docker config (2 min)
4. Validate CI config (2 min)
5. Dependency audit (2 min)
Total: 12 minutes
```

**Parallel execution** (6 minutes):

```
1. Launch 5 checks in SINGLE message (all concurrent)
2. Longest operation is build (5 min)
3. Update workflow state (1 min)
Total: 6 minutes
```

**Implementation**: See [examples/ship-preflight-parallel.md](examples/ship-preflight-parallel.md)
</example>

<example name="/implement-task-batching">
**Context**: 12 tasks with dependency graph in /implement phase

**Task dependencies**:

```
T001 (User model) → no deps
T002 (Product model) → no deps
T003 (User endpoints) → depends on T001
T004 (Product endpoints) → depends on T002
T005 (User tests) → depends on T001, T003
T006 (Product tests) → depends on T002, T004
T007 (Integration tests) → depends on T003, T004
```

**Parallel execution plan**:

```
Batch 1 (Layer 0): T001, T002 (parallel - 2 tasks)
Batch 2 (Layer 1): T003, T004 (parallel - 2 tasks, wait for Batch 1)
Batch 3 (Layer 2): T005, T006 (parallel - 2 tasks, wait for Batch 2)
Batch 4 (Layer 3): T007 (sequential - 1 task, wait for Batch 3)
```

**Time savings**:

- Sequential: 7 tasks × 20 min = 140 minutes
- Parallel: 4 batches × 25 min = 100 minutes
- **Speedup**: 1.4x

**Implementation**: See [examples/implement-batching-parallel.md](examples/implement-batching-parallel.md)
</example>
</examples>

<anti_patterns>
<anti_pattern name="fake-parallelism">
**Problem**: Sending multiple messages rapidly, thinking they'll run in parallel

**Wrong approach**:

```
Send message 1: Launch agent A
Send message 2: Launch agent B
Send message 3: Launch agent C
```

These execute **sequentially** because each message waits for the previous to complete.

**Correct approach**:

```
Send ONE message with 3 tool calls (A, B, C)
```

**Rule**: Multiple tool calls in a SINGLE message = parallel. Multiple messages = sequential.
</anti_pattern>

<anti_pattern name="ignoring-dependencies">
**Problem**: Parallelizing dependent operations causing race conditions

**Wrong approach**:

```
Parallel batch:
- Generate User model code
- Write tests for User model (needs generated code)
```

Second operation will fail because code doesn't exist yet.

**Correct approach**:

```
Batch 1 (sequential): Generate User model code
Batch 2 (sequential): Write tests for User model
```

**Rule**: Always build dependency graph first. Never parallelize dependent operations.
</anti_pattern>

<anti_pattern name="over-parallelization">
**Problem**: Launching 20 agents in parallel, overwhelming system

**Wrong approach**:

```
Launch 20 agents in single message (all tasks at once)
```

System resources exhausted, agents may fail or slow down dramatically.

**Correct approach**:

```
Batch 1: Launch 5 agents (Layer 0)
Batch 2: Launch 5 agents (Layer 1)
Batch 3: Launch 5 agents (Layer 2)
Batch 4: Launch 5 agents (Layer 3)
```

**Rule**: Keep batches to 3-8 operations. More layers is better than huge batches.
</anti_pattern>

<anti_pattern name="parallelizing-trivial-operations">
**Problem**: Using parallel execution for operations taking <30 seconds each

**Wrong approach**:

```
Parallel batch:
- Read spec.md (5 seconds)
- Read plan.md (5 seconds)
```

Overhead of parallel coordination exceeds time savings.

**Correct approach**:

```
Sequential:
- Read spec.md
- Read plan.md
```

**Rule**: Only parallelize operations taking ≥1 minute each. Below that, sequential is fine.
</anti_pattern>
</anti_patterns>

<validation>
<success_indicators>
After applying parallel execution optimization:

1. **Wall-clock time reduced**: Phase completes 2-5x faster than sequential baseline
2. **All operations successful**: No failures due to race conditions or dependencies
3. **Results identical**: Parallel execution produces same output as sequential
4. **No resource exhaustion**: System handles parallel load without failures
5. **Clear dependency graph**: Can explain why operations were grouped into specific batches
   </success_indicators>

<testing_approach>
**Before parallelization**:

1. Run phase sequentially
2. Record total time
3. Record all outputs (files, reports, state changes)

**After parallelization**:

1. Run phase with parallel batches
2. Record total time
3. Record all outputs

**Validate**:

- Time reduced by expected factor (2-5x)
- Outputs identical (diff files, compare checksums)
- No errors or warnings introduced
- Workflow state updated correctly

**Rollback if**:

- Parallel version produces different outputs
- Failures or race conditions occur
- Time savings <20% (not worth complexity)
  </testing_approach>
  </validation>

<reference_guides>
For deeper topics, see reference files:

**Execution patterns**: [references/execution-patterns.md](references/execution-patterns.md)

- Correct vs incorrect parallel execution patterns
- Message structure for parallel tool calls
- Handling tool call failures

**Phase-specific guides**:

- [references/optimize-phase-parallelization.md](references/optimize-phase-parallelization.md)
- [references/ship-preflight-parallelization.md](references/ship-preflight-parallelization.md)
- [references/implement-phase-parallelization.md](references/implement-phase-parallelization.md)

**Dependency analysis**: [references/dependency-analysis-guide.md](references/dependency-analysis-guide.md)

- Building dependency graphs
- Detecting hidden dependencies
- Handling edge cases

**Troubleshooting**: [references/troubleshooting.md](references/troubleshooting.md)

- Common failures and fixes
- Performance not improving
- Race condition debugging
  </reference_guides>

<success_criteria>
The parallel-execution-optimizer skill is successfully applied when:

1. **Dependency graph created**: All operations analyzed for dependencies before execution
2. **Batches identified**: Independent operations grouped into parallel execution batches
3. **Single message per batch**: Each batch executed via ONE message with multiple tool calls
4. **Time savings achieved**: 2-5x speedup compared to sequential execution
5. **Correctness maintained**: Parallel execution produces identical results to sequential
6. **No race conditions**: No failures due to shared state or missing dependencies
7. **Appropriate scope**: Only applied when ≥2 operations taking ≥1 minute each
8. **Clear documentation**: Execution plan explained (layers, batches, expected speedup)
   </success_criteria>
