---
name: dag-orchestrator
description: >
  The intelligence layer of WinDAGs. Decomposes natural language tasks into
  Hierarchical Task DAGs (HTDAGs), matches subtasks to skills, executes waves
  in parallel, and dynamically expands nodes when complexity exceeds executor
  capability. Use for 'orchestrate', 'execute DAG', 'parallel agents',
  'decompose task', 'coordinate skills'. NOT for single-skill tasks or
  simple linear workflows.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - TodoWrite
  - Grep
  - Glob
category: DAG Orchestration
tags: [dag, orchestration, task-decomposition, parallel-execution, htdag, adaptive-planning]
---

# DAG Orchestrator

The beating heart of WinDAGs. Transforms arbitrary natural language tasks into parallelized agent graphs that execute in waves, adapting dynamically to task complexity and executor capabilities.

## Activation Triggers

Responds to: orchestrate, execute DAG, parallel agents, decompose task, coordinate skills, multi-agent, complex task, wave execution, DAG framework, HTDAG

## Core Intelligence: HTDAG (Hierarchical Task DAG)

Based on state-of-the-art research in adaptive task decomposition:

- **Deep Agent (2025)**: Hierarchical Task DAGs with just-in-time planning
- **ADaPT (2024)**: As-needed decomposition when executor fails
- **TDAG (2024)**: Dynamic task recalibration based on preceding results

### The Three Laws of HTDAG

1. **Just-In-Time Planning**: Don't pre-plan everything. Decompose only when necessary.
2. **Adaptive Depth**: Nodes expand to sub-DAGs when complexity exceeds executor capability.
3. **Failure Cascading**: Unresolved failures propagate to parent nodes for re-planning.

## Architecture: Two-Stage Planner-Executor

```
┌─────────────────────────────────────────────────────────────────┐
│                      DAG ORCHESTRATOR                           │
├─────────────────────────────────────────────────────────────────┤
│  PLANNER STAGE                    │   EXECUTOR STAGE            │
│  ─────────────────                │   ──────────────            │
│  • Decompose task → subtasks      │   • Match subtasks → skills │
│  • Predict file conflicts         │   • Execute in parallel     │
│  • Compute wave topology          │   • Track confidence        │
│  • Determine AND/OR composition   │   • Handle failures         │
│                                   │                             │
│  When to plan:                    │   When to execute:          │
│  • Initial task received          │   • Subtask is atomic       │
│  • Executor fails on subtask      │   • Skill match found       │
│  • Node needs expansion           │   • Dependencies satisfied  │
└─────────────────────────────────────────────────────────────────┘
```

## The ADAPT Algorithm (As-Needed Decomposition)

```
ADAPT(task, depth, max_depth):
    1. TRY DIRECT EXECUTION
       result = executor.attempt(task)
       if result.success:
           return result

    2. DECOMPOSE (only if executor failed)
       if depth >= max_depth:
           return FAILURE  # Can't decompose further

       subtasks, logic = planner.decompose(task)
       # logic = AND (sequential) or OR (exploration)

    3. RECURSIVE EXECUTION
       for subtask in subtasks:
           subtask_result = ADAPT(subtask, depth + 1, max_depth)

           if logic == AND:
               if subtask_result.failed:
                   return FAILURE  # All must succeed
           elif logic == OR:
               if subtask_result.success:
                   return SUCCESS  # Any can succeed

       return combine_results(subtask_results, logic)
```

**Key insight**: This is recursive. A node that fails direct execution becomes its own sub-DAG.

## Node Types

### Atomic Nodes (Leaf)
```typescript
{
  type: "atomic",
  skill: "api-architect",
  prompt: "Design REST endpoints for user auth",
  // Cannot be further decomposed
}
```

### Composite Nodes (Can Expand)
```typescript
{
  type: "composite",
  description: "Build complete authentication system",
  expandable: true,
  // Will become sub-DAG if executor fails
}
```

### Phase Nodes (Deferred Planning)
```typescript
{
  type: "phase",
  phase: "BUILD",
  dependsOn: ["RESEARCH", "PLAN"],
  // DAG structure TBD based on earlier phase outputs
}
```

## Composition Logic

### AND Composition (Sequential Dependencies)
All subtasks must succeed. Execute in dependency order.

```
Task: "Build and deploy API"
  ├── [AND] Write API code
  ├── [AND] Write tests
  ├── [AND] Run tests (depends on above)
  └── [AND] Deploy (depends on tests passing)
```

### OR Composition (Exploration/Alternatives)
Any subtask succeeding = overall success. Try alternatives.

```
Task: "Find documentation for library X"
  ├── [OR] Check official docs site
  ├── [OR] Search GitHub README
  └── [OR] Query StackOverflow
```

### Complex Composition
```
Task: "Implement feature with fallback"
  ├── [AND] Research approaches
  │     ├── [OR] Check existing implementations
  │     └── [OR] Read academic papers
  ├── [AND] Implement primary approach
  └── [OR] Implement fallback if primary fails
```

## Wave Execution

DAGs execute in topological waves. Nodes in the same wave run in parallel:

```
Wave 0: [research-node]                    ← 1 agent
Wave 1: [analyze-node, summarize-node]     ← 2 agents in parallel
Wave 2: [synthesize-node]                  ← 1 agent (uses Wave 1 outputs)
Wave 3: [review-node, test-node]           ← 2 agents in parallel
Wave 4: [deploy-node]                      ← 1 agent (depends on all above)
```

**Parallel execution rule**: Make ALL Task calls for a wave in a SINGLE message.

```typescript
// Wave 1 - BOTH calls in one message
Task({
  subagent_type: "analyze-expert",
  prompt: "Analyze the research findings..."
});

Task({
  subagent_type: "summarize-expert",
  prompt: "Summarize the key points..."
});
```

## Dynamic Node Expansion

When an executor fails on a composite node, it expands into a sub-DAG:

```
BEFORE (single node):
┌─────────────────────────┐
│ Build Auth System       │  ← Executor fails (too complex)
└─────────────────────────┘

AFTER (expanded sub-DAG):
┌─────────────────────────────────────────────────┐
│ Build Auth System (expanded)                    │
│ ┌─────────┐   ┌─────────┐   ┌─────────┐        │
│ │ Design  │ → │ Implement│ → │  Test   │        │
│ │ Schema  │   │  Logic   │   │  Auth   │        │
│ └─────────┘   └─────────┘   └─────────┘        │
└─────────────────────────────────────────────────┘
```

## File Conflict Detection

Before parallel execution, predict file modifications:

```typescript
Wave 2: [brand-identity, wireframe-structure]
  Parallelizable: Yes
  Conflicts: None
  Predicted Files:
    brand-identity → ["src/styles/colors.css", "src/styles/typography.css"]
    wireframe-structure → ["src/components/Layout.tsx", "src/pages/Home.tsx"]
```

**Conflict Resolution**:
- No file overlap → Safe to parallelize
- File overlap detected → Force sequential (add dependency edge)
- Singleton task (build/lint/test) → Must run alone

## Self-Generated Success Heuristic

The executor LLM determines its own success (not waiting for gold rewards):

```typescript
// Executor prompt includes:
"After completing actions, output:
 - 'TASK_COMPLETED' if you believe you succeeded
 - 'TASK_FAILED: <reason>' if you cannot proceed
 - 'TASK_BLOCKED: <what_you_need>' if waiting on dependencies"
```

This enables as-needed decomposition without environment rewards.

## Confidence Self-Assessment

Every executor reports confidence (injected by SkillNodeExecutor):

```
After completing your task, rate your confidence:
- HIGH (90%+): Clear success, verified output
- MEDIUM (60-89%): Likely correct, some uncertainty
- LOW (<60%): Significant uncertainty, may need review
```

Low confidence triggers:
1. Potential re-execution with different approach
2. Human review gate insertion
3. Downstream task warnings

## Phase Orchestration

For tasks too complex for single-DAG planning, use phases:

```
RESEARCH → PLAN → BUILD → TEST → DEPLOY
```

**Phase properties**:
- Each phase has its own DAG (constructed just-in-time)
- Phase N output informs Phase N+1 DAG structure
- Can run `PhaseOrchestrator` for multi-phase execution

```typescript
// Phase 1: RESEARCH - DAG is known
const researchDAG = dag()
  .skillNode("research-1", "design-archivist", "Analyze competitors...")
  .skillNode("research-2", "search-specialist", "Find best practices...")
  .done();

// Phase 2: PLAN - DAG depends on research output
const planDAG = buildPlanDAG(researchResults); // Dynamic!

// Phase 3: BUILD - DAG depends on plan
const buildDAG = buildBuildDAG(planResults); // Dynamic!
```

## Skill Gap Detection

When no skill matches a subtask, the orchestrator can:

1. **Flag for human**: "No skill found for: quantum cryptography implementation"
2. **Use general agent**: Fall back to `general-purpose` subagent
3. **Create skill on-the-fly**: Invoke skill-architect to create missing capability

```typescript
if (!skillMatch) {
  // Option 1: Human review
  insertApprovalGate("No skill for: " + subtask.description);

  // Option 2: General fallback
  subtask.skill = "general-purpose";

  // Option 3: Create skill (advanced)
  Task({
    subagent_type: "skill-architect",
    prompt: `Create a skill for: ${subtask.description}
             Needed because: ${subtask.context}
             Should integrate with: ${relatedSkills.join(", ")}`
  });
}
```

## Practical Workflow

### Step 1: Receive Task
```
User: "Build me a landing page for my SaaS product"
```

### Step 2: Initial Decomposition
```bash
# Use TaskDecomposer
npx tsx packages/core/src/demos/decompose-and-execute.ts "Build me a landing page..."
```

Output:
```
Subtasks:
  1. Research competitor landing pages [design-archivist]
  2. Create brand identity [web-design-expert]
  3. Design page structure [ui-ux-designer]
  4. Write copy [copywriter]
  5. Build components [frontend-developer]
  6. Deploy [deployment-engineer]

Waves:
  Wave 0: [1] (research)
  Wave 1: [2, 3, 4] (parallel creative work)
  Wave 2: [5] (depends on 2,3,4)
  Wave 3: [6] (depends on 5)
```

### Step 3: Execute Wave-by-Wave
```typescript
// Wave 0 - Research
const researchResult = await Task({
  subagent_type: "design-archivist",
  prompt: "Research 20 SaaS landing pages..."
});

// Wave 1 - Parallel creative (ALL in one message!)
await Promise.all([
  Task({ subagent_type: "web-design-expert", prompt: "Create brand identity..." }),
  Task({ subagent_type: "ui-ux-designer", prompt: "Design page structure..." }),
  Task({ subagent_type: "copywriter", prompt: "Write compelling copy..." })
]);

// Continue through waves...
```

### Step 4: Handle Failures
If Wave 1's brand-identity fails:
```typescript
// Expand node into sub-DAG
const brandSubDAG = await planner.decompose("Create brand identity");
// Returns: [research-colors, define-typography, create-logo]
// Execute sub-DAG, then continue
```

## Error Handling

```typescript
if (taskResult.failed) {
  if (depth < maxDepth) {
    // Try decomposition
    return ADAPT(task, depth + 1, maxDepth);
  } else {
    // Max depth reached
    // 1. Mark dependent tasks as skipped
    markDependentsSkipped(task);
    // 2. Continue with independent tasks
    // 3. Report failures at end
    failures.push(task);
  }
}
```

## Performance Tips

1. **Use haiku for simple tasks**: Saves tokens and cost
2. **Maximize parallelism**: All independent tasks in one message
3. **Pass minimal context**: Don't overwhelm agents with data
4. **Set appropriate max_depth**: Usually 3-4 is sufficient
5. **Monitor confidence**: Low confidence = potential re-execution

## Integration with WinDAGs Core

Key files in `packages/core/src/`:

| File | Purpose |
|------|---------|
| `core/task-decomposer.ts` | Natural language → subtasks |
| `core/skill-matcher.ts` | Match subtasks to 143+ skills |
| `core/topology.ts` | Compute wave-based execution order |
| `core/executor.ts` | Execute DAGs with `executeDAG()` |
| `executors/skill-node-executor.ts` | Bridge nodes to ProcessExecutor |
| `core/phase-orchestrator.ts` | Multi-phase dynamic execution |

## Limitations

- Max ~5-10 parallel tasks per wave (Claude Code limit)
- Each task is isolated (no shared memory between agents)
- Context must be explicitly passed between waves
- Total execution time limited by longest critical path
- File prediction accuracy depends on decomposer

---

## Sources

Research foundations for this skill:

- [Deep Agent - HTDAG Architecture (2025)](https://arxiv.org/html/2502.07056)
- [ADaPT - As-Needed Decomposition (2024)](https://aclanthology.org/2024.findings-naacl.264/)
- [TDAG - Dynamic Task Decomposition (2024)](https://arxiv.org/html/2402.10178v2)
- [HTN Planning Overview](https://en.wikipedia.org/wiki/Hierarchical_task_network)

---

**The missing intelligence layer is now operational. DAGs win.**
