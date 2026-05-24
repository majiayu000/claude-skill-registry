---
name: goap-agent
description: Invoke for complex multi-step tasks requiring intelligent planning and multi-agent coordination. Use when tasks need decomposition, dependency mapping, parallel/sequential/swarm/iterative execution strategies, or coordination of multiple specialized agents with quality gates and dynamic optimization.
---

# GOAP Agent Skill: Goal-Oriented Action Planning

Enable intelligent planning and execution of complex multi-step tasks through systematic decomposition, dependency mapping, and coordinated multi-agent execution.

Always use the plans/ folder for all files.

## Quick Reference

See the GOAP Agent documentation (`../agents/goap-agent.md`) for detailed execution patterns and examples.

## CRITICAL: Understanding Skills vs Task Agents

**There are TWO different types of workers you can coordinate in GOAP planning:**

### Skills (invoked via `Skill` tool)
Skills are **instruction sets** that guide Claude directly. They provide specialized knowledge and workflows.

**How to invoke**: `Skill(command="skill-name")`

**When to use**:
- Need specialized knowledge/workflow guidance
- Task requires deep domain expertise (Rust quality, architecture validation)
- Want to follow a proven methodology
- Examples: Code quality review, gap analysis, architecture validation

### Task Agents (invoked via `Task` tool)
Task Agents are **autonomous sub-processes** that execute tasks independently using tools.

**How to invoke**: `Task(subagent_type="agent-name", prompt="...", description="...")`

**When to use**:
- Need autonomous task execution
- Task requires tool usage (Read, Edit, Bash, etc.)
- Want parallel/independent execution
- Examples: Running tests, implementing features, debugging

### Common Error to Avoid

**WRONG**: `Task(subagent_type="rust-code-quality", ...)` → ERROR! rust-code-quality is a Skill!

**CORRECT**: `Skill(command="rust-code-quality")` → SUCCESS

**See the agent-coordination skill for the complete reference on Skills vs Agents.**

## When to Use This Skill

Use this skill when facing:

- **Complex Multi-Step Tasks**: Tasks requiring 5+ distinct steps or multiple specialized capabilities
- **Cross-Domain Problems**: Issues spanning multiple areas (storage, API, testing, documentation)
- **Optimization Opportunities**: Tasks that could benefit from parallel or hybrid execution
- **Quality-Critical Work**: Projects requiring validation checkpoints and quality gates
- **Resource-Intensive Operations**: Large refactors, migrations, or architectural changes
- **Ambiguous Requirements**: Tasks needing structured analysis before execution

## Available Skills by Category

### Quality & Validation Skills
- **rust-code-quality**: Comprehensive Rust code review against best practices
- **architecture-validation**: Validate implementation vs architecture plans
- **plan-gap-analysis**: Implementation gap analysis between plans and code
- **code-quality**: General code quality maintenance (formatting, linting)
- **quality-unit-testing**: High-quality test writing following best practices

### Build & Testing Skills
- **build-compile**: Build management and compilation with error handling
- **test-fix**: Systematic test debugging and fixing
- **test-runner**: Test execution and management

### Analysis & Decision-Making Skills
- **analysis-swarm**: Multi-perspective code analysis (RYAN, FLASH, SOCRATES)
- **codebase-consolidation**: Analyze, consolidate, document codebases
- **debug-troubleshoot**: Systematic async Rust debugging

### Research Skills
- **web-search-researcher**: Web research for modern information
- **context-retrieval**: Episodic memory retrieval from learning system

### Memory System Skills
- **episode-start**: Start learning episodes for task tracking
- **episode-log-steps**: Log execution steps during episodes
- **episode-complete**: Complete and score episodes
- **memory-mcp**: MCP server operations
- **memory-cli-ops**: CLI operations for memory system
- **storage-sync**: Storage synchronization between Turso and redb

### Workflow & Coordination Skills
- **task-decomposition**: Break down complex tasks into atomic goals
- **agent-coordination**: Coordinate multiple Skills and Agents
- **parallel-execution**: Execute independent tasks simultaneously
- **loop-agent**: Iterative refinement with convergence detection
- **github-workflows**: Diagnose and optimize CI/CD workflows

### Meta Skills
- **skill-creator**: Create new Claude Code skills
- **feature-implement**: Systematic feature implementation workflow

## Available Task Agents

### Execution Agents
- **feature-implementer**: Design, implement, test new features
- **refactorer**: Improve code quality, structure, maintainability
- **debugger**: Diagnose runtime issues, performance problems

### Validation Agents
- **code-reviewer**: Review code quality, correctness, standards
- **test-runner**: Execute tests, diagnose failures

### Meta Agents
- **agent-creator**: Create new Task Agents
- **goap-agent**: Complex multi-step task planning (recursive)
- **loop-agent**: Execute workflows iteratively
- **Explore**: Fast codebase exploration and search

## Core GOAP Methodology

### The GOAP Planning Cycle

```
1. ANALYZE → Understand goals, constraints, resources
2. DECOMPOSE → Break into atomic tasks with dependencies
3. STRATEGIZE → Choose execution pattern (parallel/sequential/swarm/hybrid/iterative)
4. COORDINATE → Assign tasks to specialized agents
5. EXECUTE → Run with monitoring and quality gates
6. SYNTHESIZE → Aggregate results and validate success
```

## Phase 1: Task Analysis

### Initial Assessment

```markdown
## Task Analysis

**Primary Goal**: [Clear statement of what success looks like]

**Constraints**:
- Time: [Urgent / Normal / Flexible]
- Resources: [Available agents, tools, data]
- Dependencies: [External systems, prerequisites]

**Complexity Level**:
- Simple: Single agent, <3 steps
- Medium: 2-3 agents, some dependencies
- Complex: 4+ agents, mixed execution modes
- Very Complex: Multiple phases, many dependencies

**Quality Requirements**:
- Testing: [Unit / Integration / E2E]
- Standards: [AGENTS.md compliance, formatting, linting]
- Documentation: [API docs, examples, guides]
- Performance: [Speed, memory, scalability]
```

### Context Gathering

1. **Codebase Understanding**: Use Explore agent to understand relevant code
2. **Past Patterns**: Check if similar tasks have been done before
3. **Available Resources**: Identify available agents and their capabilities
4. **Current State**: Understand starting conditions and existing implementations

## Phase 2: Task Decomposition

Use the **task-decomposition** skill to break down the goal:

```markdown
## Task Decomposition: [Task Name]

### Main Goal
[Clear statement of primary objective]

### Sub-Goals
1. [Component 1] - Priority: P0
   - Success Criteria: [How to verify]
   - Dependencies: [Prerequisites]
   - Complexity: [Low/Medium/High]

2. [Component 2] - Priority: P1
   - Success Criteria: [How to verify]
   - Dependencies: [Component 1]
   - Complexity: [Low/Medium/High]

### Atomic Tasks
**Component 1: [Name]**
- Task 1.1: [Action] (Agent: type, Deps: none)
- Task 1.2: [Action] (Agent: type, Deps: 1.1)

### Dependency Graph
```
Task 1.1 → Task 1.2 → Task 2.1
                  ↘
Task 1.3 (parallel) → Task 2.2
```
```

### Key Decomposition Principles
- **Atomic**: Each task is indivisible and clear
- **Testable**: Can verify completion
- **Independent where possible**: Minimize dependencies
- **Assigned**: Each task maps to an agent capability

## Phase 3: Strategy Selection

Choose execution strategy based on task characteristics. See the GOAP Agent documentation (`../agents/goap-agent.md`) for detailed execution patterns.

### Quick Strategy Guide

| Strategy | When to Use | Speed | Complexity |
|----------|-------------|-------|------------|
| **Parallel** | Independent tasks, time-critical | Nx | High |
| **Sequential** | Dependent tasks, order matters | 1x | Low |
| **Swarm** | Many similar tasks | ~Nx | Medium |
| **Hybrid** | Mixed requirements | 2-4x | Very High |
| **Iterative** | Progressive refinement, convergence | Varies | Medium |

### Decision Tree
```
Needs iterative refinement?
  ├─ Yes (until criteria met or converged) → ITERATIVE
  └─ No → Is time critical?
      ├─ Yes → Can tasks run in parallel?
      │   ├─ Yes → PARALLEL
      │   └─ No → SEQUENTIAL (prioritize critical path)
      └─ No → Are tasks similar?
          ├─ Yes (many similar) → SWARM
          ├─ No (mixed) → HYBRID
          └─ Simple linear → SEQUENTIAL
```

## Phase 4: Agent Assignment

### Agent Capability Matrix

| Agent Type | Capabilities | Tools Available | Best For |
|------------|--------------|-----------------|----------|
| **feature-implementer** | Design, implement, test, integrate features | Read, Write, Edit, Bash, Glob, Grep | New functionality, modules, APIs |
| **debugger** | Diagnose runtime issues, async problems | Read, Bash, Grep, Edit | Bug fixes, deadlocks, performance |
| **test-runner** | Execute tests, diagnose failures | Bash, Read, Grep, Edit | Test validation, debugging tests |
| **refactorer** | Improve structure, eliminate duplication | Read, Edit, Bash, Grep, Glob | Code quality, modernization |
| **code-reviewer** | Review quality, standards, security | Read, Glob, Grep, Bash | Quality assurance, pre-commit |
| **loop-agent** | Iterative refinement, convergence | Task, Read, TodoWrite, Glob, Grep | Progressive improvements, test-fix loops |
| **agent-creator** | Create new Task Agents | Write, Read, Glob, Grep, Edit | Building new autonomous capabilities |
| **Explore** | Fast codebase exploration | All tools | Finding files, understanding architecture |
| **memory-cli** | CLI development and testing | Read, Write, Edit, Bash, Glob, Grep | Memory CLI features and fixes |

### Assignment Principles
1. Match agent capabilities to task requirements
2. Balance workload across agents
3. Consider agent specialization
4. Plan for quality validation

### Phase-Specific Skill/Agent Recommendations

#### Phase 1: Research & Analysis
**Skills (Parallel)**:
- `web-search-researcher` - Research best practices, modern solutions
- `context-retrieval` - Find similar past implementations
- `codebase-consolidation` - Understand current architecture

**Agents (Parallel)**:
- `Explore` - Fast codebase exploration
- `code-reviewer` - Audit current code quality

**Use when**: Beginning new features, investigating issues, understanding requirements

#### Phase 2: Decision-Making & Planning
**Skills (Sequential)**:
- `task-decomposition` - Break down complex goals
- `analysis-swarm` - Multi-perspective architectural decisions (RYAN, FLASH, SOCRATES)

**Use when**: Multiple valid approaches, significant trade-offs, architectural decisions

#### Phase 3: Quality Validation (Pre-Implementation)
**Skills (Parallel)**:
- `rust-code-quality` - Rust best practices review
- `architecture-validation` - Validate vs architectural plans
- `plan-gap-analysis` - Verify all requirements covered

**Use when**: Before major implementation, validating design decisions

#### Phase 4: Implementation
**Agents (Parallel or Sequential)**:
- `feature-implementer` - Build new functionality
- `refactorer` - Improve existing code

**Skills (Guidance)**:
- `feature-implement` - Feature implementation workflow

**Use when**: Executing planned work, building features

#### Phase 5: Testing & Debugging
**Skills (Sequential)**:
- `test-fix` - Systematic test debugging
- `quality-unit-testing` - High-quality test writing

**Agents (Parallel or Sequential)**:
- `test-runner` - Execute test suites
- `debugger` - Diagnose runtime issues

**Use when**: Validating implementations, fixing test failures

#### Phase 6: Build & CI/CD
**Skills (Sequential)**:
- `build-compile` - Build verification and optimization
- `github-workflows` - CI/CD pipeline validation

**Use when**: Preparing for deployment, troubleshooting CI failures

#### Phase 7: Quality Assurance (Post-Implementation)
**Skills (Parallel)**:
- `rust-code-quality` - Final Rust review
- `architecture-validation` - Validate vs architecture
- `plan-gap-analysis` - Verify completeness

**Agents (Parallel)**:
- `code-reviewer` - Final quality check
- `test-runner` - Full test suite validation

**Use when**: Pre-commit, pre-merge, release preparation

## Phase 5: Execution Planning

### Create the Execution Plan

```markdown
## Execution Plan: [Task Name]

### Overview
- Strategy: [Parallel/Sequential/Swarm/Hybrid/Iterative]
- Total Tasks: [N]
- Estimated Duration: [Time]
- Quality Gates: [N checkpoints]

### Phase 1: [Phase Name]
**Tasks**:
- Task 1: [Description] (Agent: type)
- Task 2: [Description] (Agent: type)

**Quality Gate**: [Validation criteria]

### Phase 2: [Phase Name]
**Tasks**:
- Task 3: [Description] (Agent: type)

**Quality Gate**: [Validation criteria]

### Overall Success Criteria
- [ ] All tasks complete
- [ ] Quality gates passed
- [ ] Tests passing
- [ ] Documentation updated

### Contingency Plans
- If Phase 1 fails → [Recovery plan]
- If tests fail → [Diagnostic approach]
```

## Phase 6: Coordinated Execution

### Parallel Execution

```markdown
**Launching parallel agents:**
- Agent 1 (feature-implementer) → Task A
- Agent 2 (feature-implementer) → Task B
- Agent 3 (test-runner) → Task C

**Coordination**:
- All agents work simultaneously
- Monitor progress independently
- Aggregate results when all complete
```

### Sequential Execution

```markdown
**Launching sequential agents:**
Phase 1: Agent 1 (debugger) → Diagnose issue
  ↓ Quality Gate: Root cause identified
Phase 2: Agent 2 (refactorer) → Apply fix
  ↓ Quality Gate: Tests pass
Phase 3: Agent 3 (code-reviewer) → Validate
```

### Monitoring During Execution
- Track agent progress
- Monitor for failures
- Validate intermediate results
- Adjust plan if needed

### Atomic Git Commit Policy
After each successful todo completion, create an atomic git commit:
- **Commit only the changes** for that specific todo item
- Use descriptive commit messages following `[module] description` format
- Do NOT commit changes from incomplete todos
- This ensures incremental, reversible progress tracking
- Example: `feat(storage): add episode creation method`

## Phase 7: Result Synthesis

### Aggregate Results

```markdown
## Execution Summary: [Task Name]

### ✓ Completed Tasks
- [Task 1]: Success
- [Task 2]: Success

### 📦 Deliverables
- [File/Feature 1]
- [File/Feature 2]

### ✅ Quality Validation
- Tests: [Pass/Fail] ([coverage]%)
- Linting: [Pass/Fail]
- Standards: [Compliant]

### 📊 Performance Metrics
- Duration: [actual vs estimated]
- Efficiency: [parallel speedup if applicable]

### 💡 Recommendations
- [Improvement 1]
- [Improvement 2]

### 🎓 Lessons Learned
- [What worked well]
- [What to improve]
```

## Integration with Self-Learning Memory

GOAP coordination tasks can be tracked as learning episodes to improve future planning decisions.

### Starting a GOAP Episode

```markdown
**Use**: Skill(command="episode-start")

**TaskContext**:
- language: "coordination"
- domain: "goap"
- tags: ["multi-agent", "parallel", "sequential", etc.]

**Description**: "GOAP coordination for [task description]"
```

### Logging GOAP Steps

```markdown
**Use**: Skill(command="episode-log-steps")

**Log during**:
- Decomposition decisions (how goals were broken down)
- Agent assignments (which agents chosen for which tasks)
- Strategy selection (why parallel vs sequential vs swarm)
- Quality gate results (pass/fail and why)
- Recovery actions (how failures were handled)
```

### Completing a GOAP Episode

```markdown
**Use**: Skill(command="episode-complete")

**Score based on**:
- Goal achievement (all tasks completed?)
- Efficiency (parallel speedup, resource utilization)
- Quality (all quality gates passed?)
- Adaptability (how well recovered from failures?)

**Patterns extracted**:
- Successful decomposition strategies
- Effective agent assignments
- Optimal execution patterns
- Quality gate effectiveness
```

### Retrieving Past GOAP Context

```markdown
**Use**: Skill(command="context-retrieval")

**Query for**:
- Similar coordination tasks
- Past parallel/sequential decisions
- Agent assignment patterns
- Quality gate strategies

**Apply learnings**:
- Reuse successful decompositions
- Avoid past mistakes
- Apply proven strategies
- Optimize based on history
```

### Example: Learning-Enabled GOAP

```markdown
Task: Implement authentication system

Phase 0: Retrieve Context
└─ Skill(command="context-retrieval")
   Query: "authentication implementation coordination"
   → Found: 3 past auth implementations
   → Pattern: Parallel (model + middleware + endpoints) worked well
   → Lesson: Sequential integration after parallel build

Phase 1: Start Episode
└─ Skill(command="episode-start")
   Context: {domain: "goap", tags: ["auth", "parallel"]}

Phase 2-N: Execute with logging
└─ Skill(command="episode-log-steps")
   Log each: decomposition, assignment, quality gate

Phase Final: Complete Episode
└─ Skill(command="episode-complete")
   Score: High (reused successful pattern)
   Pattern: Confirmed parallel → sequential integration strategy
```

## Dynamic Capability Creation

When existing Skills and Agents are insufficient, create new capabilities dynamically.

### When to Create New Skills

**Create Skill when**:
- Recurring workflow pattern identified
- Deep domain knowledge needed
- Reusable methodology discovered
- No existing Skill covers the domain

**Examples**:
- Custom quality standards for your domain
- Specialized testing workflows
- Domain-specific architecture patterns
- Project-specific best practices

**How to create**:
```markdown
Use: Skill(command="skill-creator")

Provide:
- Skill name and description
- When to use this skill
- Step-by-step methodology
- Examples and patterns
- Integration points
```

### When to Create New Agents

**Create Agent when**:
- New autonomous execution capability needed
- Specialized tool usage pattern required
- Cross-cutting concern needs dedicated agent
- Complex multi-step execution to automate

**Examples**:
- Custom deployment agent
- Specialized migration agent
- Domain-specific analyzer agent
- Project-specific workflow agent

**How to create**:
```markdown
Use: Task(subagent_type="agent-creator", ...)

Or use: Skill(command="skill-creator") for agent definition

Provide:
- Agent purpose and capabilities
- Tools the agent needs
- Input/output specification
- Success criteria
```

### Update GOAP Knowledge

After creating new capabilities:

1. **Document in GOAP**:
   - Add to Skills or Agents list
   - Update capability matrix
   - Add to phase-specific recommendations

2. **Test the capability**:
   - Use in real scenario
   - Validate effectiveness
   - Refine as needed

3. **Share the pattern**:
   - Document in project
   - Add examples
   - Enable reuse

### Example: Creating Custom Capability

```markdown
Problem: Need specialized security audit for authentication code

Step 1: Identify gap
→ No existing Skill covers auth security audit specifically

Step 2: Create Skill
└─ Skill(command="skill-creator")
   Name: "auth-security-audit"
   Purpose: "Audit authentication code for security vulnerabilities"
   Methodology: [OWASP auth checklist, crypto review, token validation, ...]

Step 3: Integrate into GOAP
→ Add to Quality & Validation Skills
→ Add to Phase 3 and Phase 7 recommendations
→ Document in project CLAUDE.md

Step 4: Use in workflow
└─ Phase 3: Skill(command="auth-security-audit")
   → Validates auth design before implementation
```

## Common GOAP Patterns

### Pattern 1: Research → Decide → Implement → Validate (Full Stack)

```markdown
Task: Implement complex feature with architectural impact

Phase 0: Retrieve Context [Skills]
├─ Skill(command="context-retrieval")
│  Query: "similar feature implementations"
│  → Apply past learnings
└─ Skill(command="episode-start")
   → Start tracking this coordination

Phase 1: Research [Parallel Skills + Agents]
├─ Skill(command="web-search-researcher")
│  → Research modern best practices
├─ Skill(command="codebase-consolidation")
│  → Understand current architecture
└─ Task(subagent_type="Explore")
   → Fast codebase exploration
Quality Gate: Architecture and requirements clear

Phase 2: Decision [Skill]
└─ Skill(command="analysis-swarm")
   → Multi-perspective architectural decision (RYAN, FLASH, SOCRATES)
   → Evaluate trade-offs, choose approach
Quality Gate: Architecture approved

Phase 3: Pre-Implementation Validation [Parallel Skills]
├─ Skill(command="architecture-validation")
│  → Validate design vs plans
├─ Skill(command="plan-gap-analysis")
│  → Ensure complete requirements coverage
└─ Skill(command="rust-code-quality")
   → Review design for Rust best practices
Quality Gate: Design validated

Phase 4: Implementation [Parallel Agents]
├─ Task(subagent_type="feature-implementer")
│  Prompt: "Implement Module A"
├─ Task(subagent_type="feature-implementer")
│  Prompt: "Implement Module B"
└─ Task(subagent_type="feature-implementer")
   Prompt: "Implement Module C"
Quality Gate: All modules implemented

Phase 5: Testing [Skills + Agents]
├─ Task(subagent_type="test-runner")
│  → Execute all tests
├─ Skill(command="test-fix")
│  → Fix any failing tests systematically
└─ Skill(command="quality-unit-testing")
   → Ensure high-quality tests
Quality Gate: All tests passing

Phase 6: Quality Validation [Parallel Skills + Agents]
├─ Skill(command="rust-code-quality")
│  → Final Rust review
├─ Skill(command="architecture-validation")
│  → Validate vs architecture
├─ Skill(command="plan-gap-analysis")
│  → Verify completeness
└─ Task(subagent_type="code-reviewer")
   → Final quality check
Quality Gate: Quality standards met

Phase 7: Build & CI [Skills]
├─ Skill(command="build-compile")
│  → Build verification
└─ Skill(command="github-workflows")
   → CI validation
Quality Gate: Ready for merge

Phase 8: Learning [Skills]
└─ Skill(command="episode-complete")
   Score: High (all phases successful)
   Patterns: Document successful strategies
```

### Pattern 2: Investigate → Diagnose → Fix → Verify
```
Phase 1: Investigate
  - debugger → Reproduce issue
  - Quality Gate: Issue reproduced

Phase 2: Diagnose
  - debugger → Root cause analysis
  - Quality Gate: Root cause identified

Phase 3: Fix
  - refactorer → Apply fix
  - Quality Gate: Fix implemented

Phase 4: Verify
  - test-runner → Regression tests
  - Quality Gate: Tests pass
```

### Pattern 3: Audit → Improve → Validate
```
Phase 1: Audit
  - code-reviewer → Quality audit
  - Quality Gate: Issues identified

Phase 2 (Swarm): Improve
  - Multiple refactorer agents
  - Work queue: [issue list]
  - Quality Gate: All issues addressed

Phase 3: Validate
  - test-runner → Full test suite
  - code-reviewer → Final check
  - Quality Gate: Quality targets met
```

## Error Handling & Recovery

### Agent Failure Recovery
```markdown
**If agent fails:**
1. Log failure reason
2. Check quality gate status
3. Options:
   - Retry same agent (transient error)
   - Assign to different agent (agent issue)
   - Modify task (requirements issue)
   - Escalate to user (blocking issue)
```

### Quality Gate Failure
```markdown
**If quality gate fails:**
1. Identify failing criteria
2. Diagnose root cause
3. Options:
   - Re-run previous phase with fixes
   - Adjust quality criteria (if appropriate)
   - Change strategy (e.g., parallel → sequential for debugging)
```

### Blocked Dependencies
```markdown
**If dependency blocks progress:**
1. Identify blocking task
2. Prioritize unblocking
3. Options:
   - Execute dependency first (re-order)
   - Remove dependency (refactor plan)
   - Parallel work on independent tasks
```

## Best Practices

### DO:
✓ Break tasks into atomic, testable units
✓ Define clear quality gates between phases
✓ Match agent capabilities to task requirements
✓ Monitor progress and validate incrementally
✓ Document decisions and rationale
✓ Learn from execution for future planning
✓ Use parallel execution where safe
✓ Validate dependencies before execution
✓ Create plan to fix all pre-existing issues
✓ Never skip lint - always run and resolve
✓ Always implement changes and verify they work

### DON'T:
✗ Create monolithic tasks (break them down)
✗ Skip quality gates (leads to cascading failures)
✗ Assume tasks are independent (verify carefully)
✗ Ignore agent failures (address immediately)
✗ Over-complicate simple tasks (use sequential)
✗ Under-estimate coordination overhead
✗ Forget to aggregate and synthesize results
✗ Leave pre-existing issues unfixed
✗ Skip lint checks or warnings

## Integration with Other Skills

- **task-decomposition**: Use for Phase 2 (breaking down complex goals)
- **agent-coordination**: Use for Phase 6 (coordinating multiple agents)
- **parallel-execution**: Use for parallel strategy implementation
- **loop-agent**: Use for iterative refinement strategy implementation
- All specialized agents (feature-implementer, debugger, test-runner, etc.)

## Quick Example

```markdown
Task: Implement authentication system

## GOAP Plan

### Phase 1: Analysis (Sequential)
- goap-agent → Define requirements
- Quality Gate: Requirements clear

### Phase 2: Implementation (Parallel)
- Agent A → User model + database
- Agent B → Auth middleware
- Agent C → API endpoints
- Quality Gate: All components implemented

### Phase 3: Integration (Sequential)
- feature-implementer → Wire components together
- test-runner → Integration tests
- Quality Gate: Tests pass

### Phase 4: Validation (Sequential)
- code-reviewer → Security review
- Quality Gate: Approved for deployment
```

## Success Metrics

### Planning Quality
- Clear decomposition with measurable tasks
- Realistic time estimates
- Appropriate strategy selection
- Well-defined quality gates

### Execution Quality
- Tasks completed as planned
- Quality gates passed
- Minimal re-work required
- Efficient resource utilization

### Learning
- Document what worked well
- Identify improvement areas
- Update patterns for future use
- Share knowledge with team

## Advanced Topics

### Dynamic Re-Planning
If during execution:
- Dependencies change
- Requirements clarified
- Blockers discovered
- Performance issues found

Then:
1. Pause execution
2. Re-analyze with new information
3. Adjust plan (tasks, dependencies, strategy)
4. Resume with updated plan

### Optimization Techniques
- **Critical path optimization**: Parallelize non-critical-path tasks
- **Resource pooling**: Share agents across similar tasks
- **Incremental delivery**: Complete and validate phases incrementally
- **Adaptive strategy**: Switch strategies based on progress

## Summary

GOAP enables systematic planning and execution of complex tasks through:
1. **Structured Analysis**: Understand goals, constraints, and context
2. **Intelligent Decomposition**: Break into atomic, testable tasks
3. **Strategic Execution**: Choose optimal execution pattern
4. **Quality Assurance**: Validate at checkpoints
5. **Coordinated Agents**: Leverage specialized capabilities
6. **Continuous Learning**: Improve from each execution

Use GOAP when facing complex, multi-step challenges requiring coordination, optimization, and quality assurance.
