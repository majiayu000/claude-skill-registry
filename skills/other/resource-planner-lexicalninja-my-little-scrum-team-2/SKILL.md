---
name: resource-planner
description: Plans resource allocation and agent assignments to tasks. Use when you need to allocate agents to tasks, balance workload, or plan resource usage. Considers task dependencies, agent capabilities, and workload distribution.
---

# Resource Planner Skill

## Instructions

1. Review all tasks and their requirements
2. Review available agents and their capabilities
3. Consider task dependencies and priorities
4. Allocate agents to tasks optimally
5. Balance workload across agents
6. Plan resource usage efficiently
7. Create resource allocation plan

## Resource Planning Process

### Step 1: Inventory Resources
- List all available agents
- Assess agent capabilities and capacity
- Note agent specializations
- Identify agent availability

### Step 2: Analyze Tasks
- List all tasks to be assigned
- Identify task requirements
- Note task dependencies
- Determine task priorities

### Step 3: Match Tasks to Agents
- Use task-to-agent-matcher for each task
- Consider agent capabilities
- Consider agent workload
- Consider task dependencies

### Step 4: Optimize Allocation
- Balance workload across agents
- Minimize context switching
- Group related tasks
- Consider dependencies

### Step 5: Create Allocation Plan
- Document agent assignments
- Note workload distribution
- Identify any resource constraints
- Plan execution order

## Allocation Principles

### Capability Match
- Assign tasks to agents with matching capabilities
- Prefer specialized agents for specialized tasks
- Ensure agent can handle task effectively

### Workload Balance
- Distribute tasks evenly across agents
- Avoid overloading single agents
- Consider agent capacity
- Plan for parallel execution

### Dependency Management
- Respect task dependencies
- Assign dependent tasks after dependencies complete
- Plan sequential execution when needed
- Enable parallel execution when possible

### Efficiency
- Group related tasks for same agent
- Minimize agent switching
- Optimize for throughput
- Consider resource constraints

## Resource Allocation Output Format

```markdown
## Resource Allocation Plan

### Available Agents
- [agent-name]: [capacity/status]
- [agent-name]: [capacity/status]

### Task Assignments

#### [Agent Name]
- TASK-001: [task description] - [priority]
- TASK-002: [task description] - [priority]
- **Workload**: [X tasks, Y complexity]

#### [Agent Name]
- TASK-003: [task description] - [priority]
- **Workload**: [X tasks, Y complexity]

### Execution Order
1. [Phase/Group]: [tasks]
2. [Phase/Group]: [tasks]

### Workload Distribution
- [agent-name]: [X] tasks ([Y]% of total)
- [agent-name]: [X] tasks ([Y]% of total)

### Resource Constraints
- [Constraint 1]
- [Constraint 2]

### Recommendations
[Any recommendations for optimization]
```

## Examples

### Example 1: Simple Allocation

**Input**: Allocate 5 tasks to available agents

**Output**:
```markdown
## Resource Allocation Plan

### Available Agents
- ui-ux-designer: Available
- implementation-engineer: Available
- infrastructure-engineer: Available

### Task Assignments

#### ui-ux-designer
- TASK-001: Design login page layout - High priority
- TASK-002: Design button component styles - Medium priority
- **Workload**: 2 tasks, Medium complexity

#### implementation-engineer
- TASK-003: Implement login API endpoint - High priority (depends on TASK-001)
- TASK-004: Implement button component - Medium priority (depends on TASK-002)
- **Workload**: 2 tasks, Medium complexity

#### infrastructure-engineer
- TASK-005: Set up database schema - High priority
- **Workload**: 1 task, Medium complexity

### Execution Order
1. **Phase 1 (Parallel)**:
   - ui-ux-designer: TASK-001, TASK-002
   - infrastructure-engineer: TASK-005

2. **Phase 2 (After Phase 1)**:
   - implementation-engineer: TASK-003, TASK-004

### Workload Distribution
- ui-ux-designer: 2 tasks (40% of total)
- implementation-engineer: 2 tasks (40% of total)
- infrastructure-engineer: 1 task (20% of total)

### Resource Constraints
- TASK-003 and TASK-004 depend on design tasks
- All tasks can be completed with available agents

### Recommendations
- Start with Phase 1 tasks in parallel
- Begin Phase 2 after Phase 1 completes
- Workload is well-balanced
```

### Example 2: Complex Allocation with Dependencies

**Input**: Allocate 10 tasks with complex dependencies

**Output**:
```markdown
## Resource Allocation Plan

### Available Agents
- specification-writer: Available
- scrum-master: Available
- ui-ux-designer: Available
- implementation-engineer: Available
- infrastructure-engineer: Available
- test-runner: Available

### Task Assignments

#### specification-writer
- TASK-001: Create user dashboard specification - High priority
- **Workload**: 1 task, High complexity

#### scrum-master
- TASK-002: Break down specification into tasks - High priority (depends on TASK-001)
- **Workload**: 1 task, Medium complexity

#### ui-ux-designer
- TASK-003: Design dashboard layout - High priority (depends on TASK-002)
- TASK-004: Design user profile component - Medium priority (depends on TASK-002)
- **Workload**: 2 tasks, Medium complexity

#### infrastructure-engineer
- TASK-005: Set up database - High priority
- TASK-006: Configure API server - High priority
- **Workload**: 2 tasks, Medium complexity

#### implementation-engineer
- TASK-007: Implement dashboard API - High priority (depends on TASK-003, TASK-005, TASK-006)
- TASK-008: Implement user profile API - Medium priority (depends on TASK-004, TASK-005)
- TASK-009: Implement frontend dashboard - High priority (depends on TASK-003, TASK-007)
- **Workload**: 3 tasks, High complexity

#### test-runner
- TASK-010: Run test suite - High priority (depends on TASK-007, TASK-008, TASK-009)
- **Workload**: 1 task, Medium complexity

### Execution Order
1. **Phase 1**: 
   - specification-writer: TASK-001

2. **Phase 2** (depends on Phase 1):
   - scrum-master: TASK-002

3. **Phase 3** (depends on Phase 2, can run in parallel):
   - ui-ux-designer: TASK-003, TASK-004
   - infrastructure-engineer: TASK-005, TASK-006

4. **Phase 4** (depends on Phase 3):
   - implementation-engineer: TASK-007, TASK-008, TASK-009

5. **Phase 5** (depends on Phase 4):
   - test-runner: TASK-010

### Workload Distribution
- specification-writer: 1 task (10%)
- scrum-master: 1 task (10%)
- ui-ux-designer: 2 tasks (20%)
- infrastructure-engineer: 2 tasks (20%)
- implementation-engineer: 3 tasks (30%)
- test-runner: 1 task (10%)

### Resource Constraints
- Sequential phases due to dependencies
- implementation-engineer has highest workload (3 tasks)
- Some parallel execution possible in Phase 3

### Recommendations
- Consider splitting implementation-engineer tasks if possible
- Phase 3 can run in parallel to save time
- Monitor implementation-engineer workload
```

## Workload Balancing

### Balancing Strategies

1. **Equal Distribution**: Distribute tasks evenly
2. **Complexity-Based**: Consider task complexity, not just count
3. **Capability-Based**: Match tasks to agent strengths
4. **Dependency-Aware**: Consider dependencies when balancing

### Workload Metrics

- **Task Count**: Number of tasks per agent
- **Complexity Score**: Sum of task complexities
- **Estimated Time**: Estimated time per agent
- **Dependency Depth**: How many dependencies agent must wait for

## Best Practices

- **Balance Workload**: Distribute tasks evenly
- **Respect Dependencies**: Don't assign tasks before dependencies complete
- **Enable Parallelism**: Assign independent tasks to different agents
- **Group Related Tasks**: Assign related tasks to same agent when possible
- **Consider Capacity**: Don't overload agents
- **Plan Ahead**: Consider future workload when allocating
