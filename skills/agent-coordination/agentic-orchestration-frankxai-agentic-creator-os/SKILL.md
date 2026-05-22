---
name: agentic-orchestration
description: Patterns for multi-agent coordination, task decomposition, handoffs, and workflow orchestration. Best practices for building and managing agent systems.
version: 1.0.0
last_updated: 2025-12-19
external_version: "Claude Agent SDK 2025"
changelog: |
  - 1.0.0: Initial skill with orchestration patterns from Claude Agent SDK and FrankX system
---

# Agentic Orchestration Patterns

This skill covers patterns for coordinating multiple AI agents, decomposing complex tasks, managing handoffs, and building robust agent workflows.

---

## Orchestration Fundamentals

### Agent Hierarchy Model
```
┌─────────────────────────────────────────────────────┐
│              ORCHESTRATOR AGENT                      │
│  (Strategic coordination, task routing, synthesis)   │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  Specialist  │  │  Specialist  │  │ Specialist │ │
│  │   Agent A    │  │   Agent B    │  │  Agent C   │ │
│  │  (Domain 1)  │  │  (Domain 2)  │  │ (Domain 3) │ │
│  └──────────────┘  └──────────────┘  └────────────┘ │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### Core Principles

1. **Single Responsibility**: Each agent has one clear domain
2. **Explicit Handoffs**: Clear protocols for transferring work
3. **Context Preservation**: State travels with the task
4. **Graceful Degradation**: System works if agents fail
5. **Observable Execution**: Can see what each agent is doing

---

## Task Decomposition Patterns

### Pattern 1: Hierarchical Decomposition
```
Complex Task: "Build a feature for user authentication"

Decomposed:
├── Research Phase (Research Agent)
│   ├── Analyze existing auth patterns in codebase
│   ├── Identify dependencies and constraints
│   └── Document findings
│
├── Design Phase (Architect Agent)
│   ├── Design auth flow
│   ├── Define API contracts
│   └── Create component structure
│
├── Implementation Phase (Developer Agent)
│   ├── Implement backend auth logic
│   ├── Build frontend components
│   └── Add error handling
│
├── Testing Phase (QA Agent)
│   ├── Write unit tests
│   ├── Integration tests
│   └── Security review
│
└── Documentation Phase (Docs Agent)
    ├── API documentation
    ├── User guide
    └── Developer notes
```

### Pattern 2: Parallel Decomposition
```
Task: "Analyze codebase and suggest improvements"

Parallel Execution:
┌─────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                      │
│                Spawns parallel agents                │
└───────────┬─────────────┬─────────────┬────────────┘
            │             │             │
            ▼             ▼             ▼
    ┌───────────┐  ┌───────────┐  ┌───────────┐
    │ Security  │  │Performance│  │   Code    │
    │  Analyst  │  │  Analyst  │  │  Quality  │
    └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
          │              │              │
          ▼              ▼              ▼
    [Security     [Performance   [Quality
     Report]       Report]        Report]
          │              │              │
          └──────────────┼──────────────┘
                         │
                         ▼
              ┌─────────────────┐
              │   ORCHESTRATOR  │
              │    Synthesizes  │
              └─────────────────┘
```

### Pattern 3: Iterative Refinement
```
Task: "Write a technical blog post"

Iteration Loop:
1. Researcher → Gathers information
2. Writer → Creates draft
3. Editor → Reviews and critiques
4. Writer → Revises based on feedback
5. Editor → Approves or requests more changes
6. Repeat 4-5 until quality threshold met
7. Publisher → Formats and publishes
```

---

## Handoff Patterns

### Pattern 1: Explicit Handoff Protocol
```typescript
interface TaskHandoff {
  from_agent: string;
  to_agent: string;
  task_id: string;
  context: {
    original_request: string;
    work_completed: string[];
    current_state: any;
    next_steps: string[];
  };
  artifacts: {
    files_created: string[];
    files_modified: string[];
    decisions_made: Decision[];
  };
}

// Example handoff
const handoff: TaskHandoff = {
  from_agent: "ArchitectAgent",
  to_agent: "DeveloperAgent",
  task_id: "auth-feature-123",
  context: {
    original_request: "Implement user authentication",
    work_completed: [
      "Analyzed existing patterns",
      "Designed auth flow",
      "Created API contracts"
    ],
    current_state: {
      design_doc: "/docs/auth-design.md",
      api_spec: "/specs/auth-api.yaml"
    },
    next_steps: [
      "Implement AuthService class",
      "Create login/logout endpoints",
      "Build session management"
    ]
  },
  artifacts: {
    files_created: ["/docs/auth-design.md", "/specs/auth-api.yaml"],
    files_modified: [],
    decisions_made: [
      { decision: "Use JWT for tokens", rationale: "Stateless, scalable" },
      { decision: "Redis for session store", rationale: "Fast, supports TTL" }
    ]
  }
};
```

### Pattern 2: Capability-Based Routing
```typescript
const agentCapabilities = {
  ResearchAgent: ["search", "analyze", "summarize", "compare"],
  ArchitectAgent: ["design", "plan", "structure", "evaluate"],
  DeveloperAgent: ["implement", "refactor", "debug", "optimize"],
  ReviewerAgent: ["review", "critique", "validate", "approve"],
  DocsAgent: ["document", "explain", "format", "publish"]
};

function routeTask(task: string): string {
  const taskVerb = extractVerb(task);

  for (const [agent, capabilities] of Object.entries(agentCapabilities)) {
    if (capabilities.includes(taskVerb)) {
      return agent;
    }
  }

  return "GeneralAgent"; // Fallback
}
```

### Pattern 3: Context Window Management
```typescript
// Problem: Context grows as agents work
// Solution: Summarize and compress at handoffs

interface CompressedContext {
  essential: {
    task_goal: string;
    key_decisions: string[];
    current_blockers: string[];
  };
  reference: {
    file_paths: string[];      // Can be re-read if needed
    doc_links: string[];       // External references
  };
  discarded: {
    exploration_notes: string; // Summarized, not full content
    rejected_approaches: string[];
  };
}

function compressForHandoff(fullContext: any): CompressedContext {
  return {
    essential: extractEssentials(fullContext),
    reference: extractReferences(fullContext),
    discarded: summarizeDiscarded(fullContext)
  };
}
```

---

## Coordination Patterns

### Pattern 1: Conductor Model
```
One orchestrator coordinates all activity:

┌─────────────────────────────────────────────┐
│             CONDUCTOR AGENT                  │
│  - Receives initial request                  │
│  - Decomposes into subtasks                  │
│  - Assigns to specialist agents              │
│  - Monitors progress                         │
│  - Synthesizes results                       │
│  - Handles failures and retries              │
└─────────────────────────────────────────────┘

Best for: Complex projects with many dependencies
Example: FrankX Starlight Orchestrator
```

### Pattern 2: Pipeline Model
```
Sequential processing through specialized stages:

Request → [Agent A] → [Agent B] → [Agent C] → Result
             │            │            │
           Stage 1     Stage 2      Stage 3
          Research     Design      Execute

Best for: Well-defined workflows with clear stages
Example: Content creation pipeline
```

### Pattern 3: Swarm Model
```
Multiple agents work in parallel, coordinating peer-to-peer:

     ┌────────┐
     │Agent A │←──────────────────┐
     └───┬────┘                   │
         │                        │
    ┌────▼────┐              ┌────┴───┐
    │ Agent B │◄────────────►│Agent D │
    └────┬────┘              └────┬───┘
         │                        │
     ┌───▼────┐                   │
     │Agent C │◄──────────────────┘
     └────────┘

Best for: Exploratory tasks, parallel research
Example: Codebase analysis from multiple angles
```

### Pattern 4: Blackboard Model
```
Shared workspace that all agents read/write:

┌─────────────────────────────────────────┐
│             BLACKBOARD                   │
│  ┌─────────────────────────────────┐    │
│  │ Current State: { ... }          │    │
│  │ Hypotheses: [ ... ]             │    │
│  │ Evidence: [ ... ]               │    │
│  │ Conclusions: [ ... ]            │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
        │           │           │
   ┌────▼───┐  ┌────▼───┐  ┌────▼───┐
   │Agent A │  │Agent B │  │Agent C │
   │ reads  │  │ reads  │  │ reads  │
   │ writes │  │ writes │  │ writes │
   └────────┘  └────────┘  └────────┘

Best for: Complex problem-solving with evolving understanding
Example: Debugging a complex system issue
```

---

## Error Handling & Recovery

### Pattern 1: Retry with Backoff
```typescript
async function executeWithRetry(agent, task, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await agent.execute(task);
    } catch (error) {
      if (attempt === maxRetries) throw error;

      const delay = Math.pow(2, attempt) * 1000; // Exponential backoff
      console.log(`Attempt ${attempt} failed, retrying in ${delay}ms`);
      await sleep(delay);
    }
  }
}
```

### Pattern 2: Fallback Agents
```typescript
const agentFallbacks = {
  "SpecialistCodeReviewer": ["GeneralCodeReviewer", "SeniorDeveloper"],
  "SecurityAnalyst": ["GeneralAnalyst", "SeniorDeveloper"],
  "PerformanceExpert": ["GeneralAnalyst", "SeniorDeveloper"]
};

async function executeWithFallback(primaryAgent, task) {
  try {
    return await primaryAgent.execute(task);
  } catch (error) {
    const fallbacks = agentFallbacks[primaryAgent.name] || [];

    for (const fallbackName of fallbacks) {
      try {
        console.log(`Primary failed, trying ${fallbackName}`);
        return await getAgent(fallbackName).execute(task);
      } catch (fallbackError) {
        continue;
      }
    }

    throw new Error(`All agents failed for task: ${task.id}`);
  }
}
```

### Pattern 3: Checkpoint & Resume
```typescript
interface Checkpoint {
  task_id: string;
  completed_steps: string[];
  current_step: string;
  state: any;
  timestamp: Date;
}

async function executeWithCheckpoints(task, steps) {
  const checkpoint = await loadCheckpoint(task.id);
  const startIndex = checkpoint
    ? steps.indexOf(checkpoint.current_step)
    : 0;

  for (let i = startIndex; i < steps.length; i++) {
    const step = steps[i];

    try {
      await executeStep(step, task);
      await saveCheckpoint({
        task_id: task.id,
        completed_steps: steps.slice(0, i + 1),
        current_step: steps[i + 1] || "complete",
        state: task.state,
        timestamp: new Date()
      });
    } catch (error) {
      // Checkpoint is saved, can resume from here
      throw error;
    }
  }
}
```

---

## Observability Patterns

### Pattern 1: Structured Logging
```typescript
function agentLog(agent, event, details) {
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    agent: agent.name,
    task_id: agent.currentTask?.id,
    event: event,
    details: details,
    duration_ms: details.duration,
    tokens_used: details.tokens
  }));
}

// Usage
agentLog(agent, "TASK_START", { task: task.description });
agentLog(agent, "TOOL_CALL", { tool: "read_file", path: "/src/index.ts" });
agentLog(agent, "TASK_COMPLETE", { result: "success", duration: 5230 });
```

### Pattern 2: Progress Tracking
```typescript
interface TaskProgress {
  task_id: string;
  total_steps: number;
  completed_steps: number;
  current_step: string;
  estimated_remaining: number; // seconds
  agents_involved: string[];
}

// Expose progress for UI/monitoring
function getProgress(task): TaskProgress {
  return {
    task_id: task.id,
    total_steps: task.steps.length,
    completed_steps: task.completedSteps.length,
    current_step: task.currentStep?.description || "idle",
    estimated_remaining: estimateRemaining(task),
    agents_involved: task.agentHistory
  };
}
```

### Pattern 3: Decision Audit Trail
```typescript
interface Decision {
  timestamp: Date;
  agent: string;
  decision: string;
  options_considered: string[];
  rationale: string;
  confidence: number; // 0-1
  reversible: boolean;
}

// Track all significant decisions
const decisionLog: Decision[] = [];

function recordDecision(agent, decision, options, rationale, confidence) {
  decisionLog.push({
    timestamp: new Date(),
    agent: agent.name,
    decision,
    options_considered: options,
    rationale,
    confidence,
    reversible: true
  });
}
```

---

## FrankX System Application

### Starlight Orchestrator Pattern
```
The FrankX system uses weighted synthesis:

┌────────────────────────────────────────────────────┐
│              STARLIGHT ORCHESTRATOR                 │
│        (Meta-intelligence coordinator)              │
├────────────────────────────────────────────────────┤
│                                                     │
│  Weight Distribution for Strategic Decisions:       │
│  ├── Starlight Architect: 30%  (Systems design)    │
│  ├── Creation Engine: 25%      (Content/product)   │
│  ├── Luminor Oracle: 25%       (Future strategy)   │
│  └── Frequency Alchemist: 20%  (Consciousness)     │
│                                                     │
│  Synthesis Process:                                 │
│  1. Each agent provides perspective                 │
│  2. Orchestrator weights by domain relevance       │
│  3. Conflicts are explicitly surfaced              │
│  4. Final recommendation synthesizes all views     │
│                                                     │
└────────────────────────────────────────────────────┘
```

### Agent Team Patterns in FrankX

**Book Writing Team:**
- Master Story Architect → Design
- Genre Writer → Draft
- Editor → Review cycles
- Sensitivity Reader → Final check
- Continuity Guardian → Consistency

**Arcanea Development Team:**
- Architect → Design
- Frontend Specialist → UI
- Backend Specialist → API
- AI Specialist → Luminor integration
- DevOps → Deployment

---

## Anti-Patterns to Avoid

### ❌ God Agent
One agent that does everything - no specialization, no delegation.

### ❌ Agent Explosion
Too many tiny agents with overlapping responsibilities.

### ❌ Lost Context
Handoffs that don't preserve essential information.

### ❌ Infinite Loops
Agents that keep handing work back and forth.

### ❌ Silent Failures
Agents that fail without proper error reporting.

### ❌ Unobservable Execution
Can't see what agents are doing or why.

---

*Good orchestration is invisible - the system should feel like one coherent intelligence, not a committee of bickering agents.*
