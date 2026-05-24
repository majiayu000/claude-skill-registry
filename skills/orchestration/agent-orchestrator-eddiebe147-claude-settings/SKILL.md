---
name: Agent Orchestrator
slug: agent-orchestrator
description: Coordinate multiple AI agents and skills for complex workflows
category: meta
complexity: multi-agent
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "orchestrate agents"
  - "coordinate agents"
  - "multi-agent workflow"
  - "agent orchestrator"
  - "delegate to agents"
tags:
  - multi-agent
  - orchestration
  - coordination
  - delegation
---

# Agent Orchestrator

The Agent Orchestrator skill coordinates multiple specialized AI agents, skills, and tools to accomplish complex tasks that benefit from distributed expertise. It acts as a conductor, delegating subtasks to appropriate agents, managing dependencies, integrating results, and ensuring coherent final outputs.

This skill understands the capabilities of available agents (general-purpose, operations-manager, specialized skills), determines optimal task decomposition, manages inter-agent communication, handles failures, and synthesizes diverse outputs into unified results. It's the meta-layer that makes multi-agent collaboration effective.

Use this skill for complex projects requiring diverse expertise, tasks that benefit from parallel execution, or workflows where specialized agents outperform general-purpose approaches.

## Core Workflows

### Workflow 1: Decompose Task & Delegate
1. **Analyze** the complex task:
   - What's the end goal?
   - What are the components?
   - What expertise is needed?
2. **Map** to available agents/skills:
   - Which agents have relevant capabilities?
   - What's each agent's specialty?
   - What tools/MCPs do they access?
3. **Decompose** into subtasks:
   - Break along expertise boundaries
   - Identify dependencies
   - Determine execution order
4. **Delegate** to appropriate agents:
   - Assign subtasks with clear instructions
   - Provide necessary context
   - Set success criteria
   - Specify output format
5. **Monitor** execution:
   - Track progress
   - Identify blockers
   - Handle failures
6. **Integrate** results:
   - Collect agent outputs
   - Resolve conflicts
   - Synthesize into coherent whole
7. **Validate** final result

### Workflow 2: Parallel Agent Execution
1. **Identify** parallelizable subtasks:
   - Which tasks are independent?
   - Which share no dependencies?
   - Which can run concurrently?
2. **Prepare** parallel execution:
   - Assign subtasks to agents
   - Provide isolated contexts
   - Set timeout limits
3. **Launch** agents in parallel:
   - Initiate all at once
   - Maintain separate contexts
   - Monitor all executions
4. **Coordinate** completion:
   - Wait for all to finish
   - Handle stragglers
   - Manage timeout failures
5. **Aggregate** results:
   - Collect all outputs
   - Merge related findings
   - Resolve inconsistencies
6. **Synthesize** final output

### Workflow 3: Sequential Agent Pipeline
1. **Design** pipeline flow:
   - Order agents by dependencies
   - Define handoff points
   - Specify data transformations
2. **Execute** pipeline sequentially:
   - Agent 1: Process initial input → Output A
   - Validate Output A
   - Agent 2: Process Output A → Output B
   - Validate Output B
   - Agent N: Process Output (N-1) → Final Output
3. **Manage** state between agents:
   - Pass relevant data forward
   - Maintain context where needed
   - Discard temporary artifacts
4. **Handle** pipeline failures:
   - Identify failed stage
   - Retry or use fallback
   - Don't propagate bad data
5. **Validate** end-to-end result

### Workflow 4: Adaptive Agent Selection
1. **Assess** task requirements dynamically:
   - What capabilities are needed?
   - What's the complexity level?
   - What constraints exist?
2. **Select** best-fit agent:
   - Match capabilities to requirements
   - Consider agent availability
   - Factor in performance history
   - Choose specialist over generalist when appropriate
3. **Delegate** with context:
   - Provide task-specific instructions
   - Include relevant background
   - Set clear expectations
4. **Evaluate** agent performance:
   - Did it meet criteria?
   - Was quality sufficient?
   - Was time acceptable?
5. **Learn** for future selection:
   - Track which agents excel at what
   - Note failure patterns
   - Refine selection logic

### Workflow 5: Error Recovery & Fallback
1. **Detect** agent failure:
   - Task not completed
   - Output quality insufficient
   - Timeout exceeded
   - Error thrown
2. **Diagnose** failure cause:
   - Was task unclear?
   - Was agent wrong choice?
   - Was input malformed?
   - Was dependency unavailable?
3. **Attempt** recovery:
   - **Retry** with same agent (if transient error)
   - **Retry** with different agent (if capability mismatch)
   - **Simplify** task and retry (if too complex)
   - **Escalate** to human (if unrecoverable)
4. **Log** failure and recovery
5. **Continue** workflow if recovered

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Delegate complex task | "Orchestrate agents for [task]" |
| Run agents in parallel | "Run these tasks in parallel: [tasks]" |
| Create agent pipeline | "Create pipeline: [agent1] → [agent2] → [agent3]" |
| Select best agent | "Which agent should handle [task]?" |
| Coordinate workflow | "Coordinate [workflow] across agents" |
| Handle agent failure | "Agent [X] failed on [task], recover" |
| Integrate agent outputs | "Synthesize outputs from [agents]" |

## Best Practices

- **Match Expertise to Task**: Use specialized agents for specialized work
  - Operations Manager for project coordination
  - UI Builder for component design
  - Database Designer for schema work
  - Don't use general-purpose for everything

- **Provide Clear Context**: Each agent needs to understand its role
  - What's the larger goal?
  - What's this agent's specific responsibility?
  - What's the expected output?
  - How does it fit in the workflow?

- **Manage Dependencies**: Make execution order explicit
  - Agent B needs Agent A's output
  - Agent C can run parallel to A and B
  - Agent D waits for B and C

- **Validate Handoffs**: Don't pass bad data between agents
  - Check output format
  - Verify completeness
  - Validate against schema
  - Fail fast if something's wrong

- **Handle Failures Gracefully**: Agents will fail sometimes
  - Have fallback agents
  - Implement retry logic
  - Don't cascade failures
  - Log for post-mortem

- **Optimize Communication**: Minimize inter-agent chatter
  - Pass only necessary data
  - Use structured formats
  - Avoid redundant information
  - Compress when appropriate

- **Monitor Progress**: Know what's happening
  - Track which agents are active
  - Identify bottlenecks
  - Detect failures early
  - Provide status updates

- **Synthesize Thoughtfully**: Integrate diverse outputs coherently
  - Resolve conflicts
  - Maintain consistency
  - Preserve important details
  - Create unified narrative

## Agent Capabilities Map

### Available Agents/Skills

| Agent/Skill | Specialty | Best For | Avoid For |
|-------------|-----------|----------|-----------|
| **General-Purpose** | Broad tasks | Quick tasks, general coding | Complex orchestration |
| **Operations Manager** | Project coordination | Workflows, timelines, resources | Writing code |
| **UI Builder** | Frontend design | Components, layouts, styling | Backend logic |
| **Database Designer** | Schema design | Tables, relationships, RLS | Frontend work |
| **API Designer** | Endpoint design | RESTful APIs, validation | UI/UX |
| **Testing QA** | Test creation | E2E tests, test plans | Feature development |
| **Performance Optimizer** | Speed optimization | Metrics, caching, lazy loading | Initial development |
| **Deployment Automation** | CI/CD | Vercel, environments, pipelines | Coding features |
| **Prompt Engineer** | AI optimization | Improving prompts, AI workflows | Non-AI tasks |
| **Skill Creator** | Skill development | Building new skills | Daily tasks |
| **Workflow Designer** | Process design | Complex workflows | Simple tasks |
| **Chain Builder** | Prompt sequences | Multi-step AI tasks | Single prompts |

### MCP/Tool Access

| Agent | Available MCPs/Tools |
|-------|---------------------|
| **General-Purpose** | All (Playwright, Supabase, GitHub, Firecrawl, Memory) |
| **Operations Manager** | GitHub (PRs, issues), Memory (tracking) |
| **UI Builder** | Playwright (testing), Memory (design decisions) |
| **Database Designer** | Supabase (migrations, queries), Memory (schema) |
| **Testing QA** | Playwright (E2E), GitHub (test runs) |

## Orchestration Patterns

### Pattern 1: Expert Panel
```
Task → [Expert A, Expert B, Expert C] → Synthesize → Decision
```
**Use when**: Need diverse perspectives on same problem
**Example**: Architecture decision → [Performance expert, Security expert, Maintainability expert] → Recommendation

### Pattern 2: Assembly Line
```
Task → Agent A → Agent B → Agent C → Output
```
**Use when**: Sequential transformations needed
**Example**: Design → Implement → Test → Deploy

### Pattern 3: Divide & Conquer
```
Task → Split → [Agent 1: Part A, Agent 2: Part B, Agent N: Part N] → Merge → Output
```
**Use when**: Large task divisible into independent parts
**Example**: Multi-page app → [Agent per page] → Integrate

### Pattern 4: Supervisor-Worker
```
Supervisor analyzes → Delegates to Workers → Workers execute → Supervisor integrates
```
**Use when**: Central coordination needed
**Example**: Project manager → [Feature developers] → Integration

### Pattern 5: Collaborative Refinement
```
Agent A: Draft → Agent B: Critique → Agent A: Revise → Validate → Output
```
**Use when**: Quality improves through iteration
**Example**: Writer → Reviewer → Writer → Final

### Pattern 6: Specialist Routing
```
Analyze task → Route to appropriate specialist → Specialist executes → Return
```
**Use when**: Different task types need different agents
**Example**: Issue triage → [Bug to QA | Feature to Developer | Ops to DevOps]

## Delegation Templates

### Standard Delegation
```markdown
**Agent**: [Agent name]
**Task**: [Clear, specific task description]
**Context**: [Relevant background information]
**Inputs**: [Provided data/resources]
**Expected Output**: [Format and content requirements]
**Success Criteria**: [How to know it's done well]
**Constraints**: [Limitations or requirements]
**Deadline**: [If time-sensitive]
```

### Parallel Delegation
```markdown
**Parallel Execution**: [N agents]

**Agent 1**: [Agent name]
- Task: [Task 1]
- Output: [Output 1]

**Agent 2**: [Agent name]
- Task: [Task 2]
- Output: [Output 2]

**Integration**: [How to combine outputs]
```

### Pipeline Delegation
```markdown
**Pipeline**: [Agent A] → [Agent B] → [Agent C]

**Stage 1**: [Agent A]
- Input: [Initial data]
- Task: [Transform 1]
- Output: [Intermediate 1]

**Stage 2**: [Agent B]
- Input: [Intermediate 1]
- Task: [Transform 2]
- Output: [Intermediate 2]

**Stage 3**: [Agent C]
- Input: [Intermediate 2]
- Task: [Transform 3]
- Output: [Final output]
```

## Coordination Strategies

### Real-Time Coordination
- **When**: Agents need to interact during execution
- **How**: Shared context, message passing, state updates
- **Trade-off**: More complex but more flexible

### Batch Coordination
- **When**: Agents work independently, integrate at end
- **How**: Collect all outputs, then merge
- **Trade-off**: Simpler but less adaptive

### Hierarchical Coordination
- **When**: Clear authority structure
- **How**: Supervisor delegates, workers report back
- **Trade-off**: Clear but potentially bottlenecked

### Peer-to-Peer Coordination
- **When**: Agents are equals collaborating
- **How**: Shared workspace, mutual awareness
- **Trade-off**: Flexible but needs clear protocols

## Conflict Resolution

When agents produce conflicting outputs:

1. **Identify** the conflict:
   - What's inconsistent?
   - Which agents disagree?
   - What's the nature of disagreement?

2. **Evaluate** sources:
   - Which agent is more authoritative for this?
   - What's the confidence level?
   - What's the reasoning?

3. **Resolve** using strategy:
   - **Authority**: Trust the specialist
   - **Voting**: Majority wins (if multiple agents)
   - **Synthesis**: Combine best of both
   - **Escalate**: Ask human to decide

4. **Document** resolution:
   - What was the conflict?
   - How was it resolved?
   - Why this choice?

## Performance Optimization

### Reduce Overhead
- Don't orchestrate when single agent suffices
- Minimize handoffs and data passing
- Use parallel execution for independent tasks
- Cache repeated computations

### Load Balancing
- Distribute work evenly across agents
- Avoid bottlenecks at single agent
- Consider agent capacity and speed
- Use queuing for burst workloads

### Failure Isolation
- Don't let one agent failure crash workflow
- Use circuit breakers for unreliable agents
- Have fallback options
- Implement timeout limits

## Monitoring & Observability

Track these metrics:

- **Agent utilization**: How busy is each agent?
- **Task completion time**: How long per agent?
- **Success rate**: Which agents succeed/fail?
- **Handoff efficiency**: How smooth are transitions?
- **Integration quality**: How well do outputs combine?
- **Error rate**: Where do failures occur?
- **Cost**: Token usage per agent

## Example Orchestrations

### Feature Development Workflow
```markdown
**Orchestrator**: Coordinate feature development

1. **Requirements Analysis** (Operations Manager)
   - Clarify requirements
   - Define scope
   - Identify constraints

2. **Parallel Design Phase**
   - **UI Builder**: Design components
   - **Database Designer**: Design schema
   - **API Designer**: Design endpoints

3. **Integration Review** (Orchestrator)
   - Ensure designs are compatible
   - Resolve conflicts
   - Approve for implementation

4. **Implementation** (General-Purpose)
   - Build based on approved designs

5. **Quality Assurance** (Testing QA)
   - Generate E2E tests
   - Run test suite
   - Report issues

6. **Fix Issues** (General-Purpose)
   - Address failing tests

7. **Deployment** (Deployment Automation)
   - Deploy to staging
   - Verify deployment
   - Deploy to production
```

### Content Creation Pipeline
```markdown
**Orchestrator**: Create technical blog post

1. **Research** (General-Purpose + Firecrawl)
   - Gather sources
   - Extract key information

2. **Parallel Analysis**
   - **Prompt Engineer**: Analyze for clarity
   - **Workflow Designer**: Identify structure
   - **Output Formatter**: Determine format

3. **Draft** (General-Purpose)
   - Write based on research and analysis

4. **Review & Edit** (Prompt Engineer)
   - Review for quality
   - Suggest improvements

5. **Revise** (General-Purpose)
   - Apply feedback

6. **Format** (Output Formatter)
   - Format for target platform

7. **Generate Metadata** (General-Purpose)
   - SEO metadata
   - Social snippets
```
