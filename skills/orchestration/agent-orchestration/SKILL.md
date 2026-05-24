---
name: Agent Orchestration Patterns
description: Multi-agent coordination patterns for building effective AI teams
version: 1.0.0
license: MIT
tier: community
---

# Agent Orchestration Patterns

> **Build coordinated AI teams that work together seamlessly**

This skill provides battle-tested patterns for orchestrating multiple AI agents to solve complex problems collaboratively.

## Core Principles

### 1. Single Responsibility Agents
Each agent should have one clear purpose. Generalists create confusion; specialists create excellence.

```yaml
Bad:
  GeneralAgent: "Does everything - UI, backend, writing, testing"

Good:
  FrontendAgent: "React components, styling, accessibility"
  BackendAgent: "APIs, database, business logic"
  TestAgent: "Unit tests, integration tests, E2E"
```

### 2. Clear Communication Protocols
Define how agents share information, hand off work, and resolve conflicts.

```yaml
Handoff Protocol:
  From: BackendAgent
  To: FrontendAgent
  Includes:
    - API contract (types, endpoints)
    - Example payloads
    - Error scenarios
    - Authentication requirements
```

### 3. Orchestrator Pattern
One agent coordinates; others execute. Prevents chaos and conflicting directions.

```
                    ┌─────────────────┐
                    │   ORCHESTRATOR  │
                    │  (Coordinates)  │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│   Agent A     │   │   Agent B     │   │   Agent C     │
│  (Executes)   │   │  (Executes)   │   │  (Executes)   │
└───────────────┘   └───────────────┘   └───────────────┘
```

## Orchestration Patterns

### Pattern 1: Sequential Pipeline

Best for: Tasks with clear dependencies where each step requires the previous step's output.

```yaml
Pipeline:
  1. Research Agent → Gathers information
  2. Analysis Agent → Processes findings (needs step 1)
  3. Writing Agent → Creates content (needs step 2)
  4. Review Agent → Quality check (needs step 3)
```

**Implementation:**
```markdown
## Sequential Pipeline Protocol

### Step 1: Research Phase
**Agent:** Research Agent
**Input:** User query
**Output:** Structured research document
**Completion Signal:** "Research complete. Findings ready for analysis."

### Step 2: Analysis Phase
**Agent:** Analysis Agent
**Input:** Research document from Step 1
**Output:** Analyzed insights with recommendations
**Completion Signal:** "Analysis complete. Ready for content creation."

### Step 3: Writing Phase
**Agent:** Writing Agent
**Input:** Analysis from Step 2
**Output:** Draft content
**Completion Signal:** "Draft complete. Ready for review."

### Step 4: Review Phase
**Agent:** Review Agent
**Input:** Draft from Step 3
**Output:** Final content with quality assessment
**Completion Signal:** "Review complete. Content finalized."
```

### Pattern 2: Parallel Fan-Out

Best for: Independent tasks that can run simultaneously.

```yaml
Fan-Out:
  Orchestrator splits task into:
    - Agent A: Frontend components
    - Agent B: Backend APIs
    - Agent C: Database schema

  Fan-In:
    - Orchestrator collects results
    - Integrates into unified solution
```

**Implementation:**
```markdown
## Parallel Fan-Out Protocol

### Split Phase
**Orchestrator Action:** Divide task into independent workstreams
**Criteria for parallelization:**
- No shared state dependencies
- No sequential requirements
- Clear interface contracts defined

### Parallel Execution
**Agent A:** [Task description]
- Works independently
- Reports completion status

**Agent B:** [Task description]
- Works independently
- Reports completion status

**Agent C:** [Task description]
- Works independently
- Reports completion status

### Integration Phase
**Orchestrator Action:**
- Wait for all agents to complete
- Resolve any interface conflicts
- Integrate outputs into unified result
```

### Pattern 3: Specialist Consultation

Best for: Tasks requiring domain expertise at specific points.

```yaml
Consultation:
  Primary Agent working...
  → Hits domain-specific challenge
  → Consults Specialist Agent
  → Receives expert guidance
  → Continues with enhanced solution
```

**Implementation:**
```markdown
## Specialist Consultation Protocol

### Recognition Triggers
The primary agent should consult a specialist when:
- Task requires domain-specific knowledge
- Decision has significant architectural impact
- Quality standard requires expert validation
- Risk mitigation requires specialized review

### Consultation Format
**From:** [Primary Agent]
**To:** [Specialist Agent]
**Context:** [What we're building]
**Question:** [Specific question]
**Constraints:** [Relevant limitations]
**Expected Output:** [What we need back]

### Response Integration
Specialist provides:
- Direct answer to question
- Reasoning behind recommendation
- Potential alternatives considered
- Caveats or edge cases
```

### Pattern 4: Debate & Synthesis

Best for: Complex decisions where multiple perspectives improve outcomes.

```yaml
Debate:
  Agent A: Argues for Approach 1
  Agent B: Argues for Approach 2
  Agent C: Synthesizes best of both
  Orchestrator: Makes final decision
```

**Implementation:**
```markdown
## Debate & Synthesis Protocol

### Phase 1: Position Development
**Agent A:** Develops Position 1
- State the approach clearly
- List all advantages
- Acknowledge weaknesses
- Provide implementation path

**Agent B:** Develops Position 2
- State the approach clearly
- List all advantages
- Acknowledge weaknesses
- Provide implementation path

### Phase 2: Critique
Each agent critiques the other's position:
- What's missing?
- What's overestimated?
- What edge cases are unhandled?

### Phase 3: Synthesis
**Synthesis Agent:**
- Extract best elements from each position
- Resolve contradictions
- Propose hybrid solution if beneficial

### Phase 4: Decision
**Orchestrator:**
- Evaluate all positions and synthesis
- Make final decision with reasoning
- Document decision rationale
```

### Pattern 5: Hierarchical Delegation

Best for: Large projects requiring multiple levels of coordination.

```
                      ┌─────────────────┐
                      │  ORCHESTRATOR   │
                      │   (Strategic)   │
                      └────────┬────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
   │  Team Lead A  │   │  Team Lead B  │   │  Team Lead C  │
   │  (Tactical)   │   │  (Tactical)   │   │  (Tactical)   │
   └───────┬───────┘   └───────┬───────┘   └───────┬───────┘
           │                   │                   │
    ┌──────┴──────┐     ┌──────┴──────┐     ┌──────┴──────┐
    │             │     │             │     │             │
    ▼             ▼     ▼             ▼     ▼             ▼
┌───────┐   ┌───────┐   ...         ...   ...         ...
│Agent 1│   │Agent 2│
└───────┘   └───────┘
```

## Communication Contracts

### Agent-to-Agent Message Format

```yaml
Message:
  from: "agent_id"
  to: "agent_id"
  type: "request|response|status|handoff"
  priority: "low|normal|high|critical"
  content:
    summary: "Brief description"
    details: "Full content"
    artifacts: ["list of outputs"]
  context:
    conversation_id: "unique_id"
    parent_message: "optional_id"
    related_tasks: ["task_ids"]
```

### Status Reporting Protocol

```yaml
Status Update:
  agent: "agent_id"
  timestamp: "ISO 8601"
  status: "idle|working|blocked|complete|error"
  current_task: "description"
  progress: "0-100%"
  blockers: ["list of blockers"]
  next_steps: ["planned actions"]
  estimated_completion: "optional timestamp"
```

### Error Escalation Protocol

```yaml
Error Report:
  agent: "agent_id"
  severity: "warning|error|critical"
  error_type: "category"
  description: "what went wrong"
  attempted_solutions: ["what we tried"]
  suggested_actions: ["what might help"]
  requires_human: true|false
  blocks_progress: true|false
```

## Quality Gates

### Before Agent Assignment

- [ ] Task clearly defined
- [ ] Success criteria established
- [ ] Dependencies mapped
- [ ] Appropriate agent selected
- [ ] Resources available

### During Execution

- [ ] Progress being reported
- [ ] Blockers escalated promptly
- [ ] Quality standards maintained
- [ ] Timeline on track

### After Completion

- [ ] Deliverables meet criteria
- [ ] No known defects
- [ ] Documentation complete
- [ ] Handoff information ready

## Anti-Patterns to Avoid

### 1. The Generalist Trap
**Problem:** One agent tries to do everything
**Symptom:** Inconsistent quality, context overload
**Solution:** Split into specialized agents

### 2. The Circular Dependency
**Problem:** Agent A waits for B, B waits for C, C waits for A
**Symptom:** Deadlock, no progress
**Solution:** Identify and break cycles, define clear ordering

### 3. The Silent Agent
**Problem:** Agent works without status updates
**Symptom:** Orchestrator has no visibility, surprises at completion
**Solution:** Require regular status reports

### 4. The Micro-Manager
**Problem:** Orchestrator controls every small decision
**Symptom:** Bottleneck at orchestrator, slow progress
**Solution:** Delegate decisions within boundaries

### 5. The Scope Creeper
**Problem:** Agent expands task beyond assignment
**Symptom:** Delayed completion, unnecessary work
**Solution:** Clear scope definition, confirmation before expansion

## Team Templates

### Minimal Development Team (3 agents)

```yaml
Team:
  Architect:
    Role: Orchestrator + Technical decisions
    Responsibilities: Planning, coordination, architecture

  Builder:
    Role: Implementation
    Responsibilities: Frontend, backend, integrations

  Validator:
    Role: Quality assurance
    Responsibilities: Testing, review, documentation
```

### Standard Development Team (5 agents)

```yaml
Team:
  Architect:
    Role: Orchestrator

  Frontend:
    Role: UI specialist

  Backend:
    Role: API/data specialist

  DevOps:
    Role: Infrastructure

  QA:
    Role: Testing specialist
```

### Full Product Team (8+ agents)

```yaml
Team:
  Product:
    Strategist: Vision and roadmap
    Designer: UX/UI design

  Engineering:
    Architect: Technical leadership
    Frontend: UI implementation
    Backend: Services implementation
    DevOps: Infrastructure
    QA: Testing

  Content:
    Writer: Documentation, copy
```

## Integration with Claude Code

### Agent Definition Format

```yaml
# .claude/agents/example-agent.md

---
name: Example Agent
description: What this agent does
model: sonnet|opus
mcpServers:
  - server-name
workingDirectories:
  - /path/to/focus
---

# Agent Name

## Mission
What this agent aims to accomplish.

## Responsibilities
- Specific duty 1
- Specific duty 2

## Capabilities
- What tools/skills it can use

## Communication Protocol
How it reports status and coordinates.
```

### Skill Loading

```yaml
# Reference this skill in your session
Skills:
  - .claude/skills/community/agent-orchestration
```

---

*"A team of specialized agents, well-coordinated, will always outperform a single generalist."*
