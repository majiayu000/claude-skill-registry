---
name: resource-optimizer
description: Optimizes resource usage and makes decisions about when to optimize existing resources vs. add new resources. Use when you need to improve efficiency, balance resource usage, or decide between optimization and expansion. Analyzes current resource usage and recommends optimization strategies.
---

# Resource Optimizer Skill

## Instructions

1. Analyze current resource usage
2. Identify inefficiencies and bottlenecks
3. Evaluate optimization options
4. Compare optimization vs. adding resources
5. Recommend optimization strategy
6. Plan optimization implementation
7. Monitor optimization results

## Resource Optimization Process

### Step 1: Assess Current State
- Review resource usage
- Identify current allocation
- Note workload distribution
- Assess efficiency

### Step 2: Identify Issues
- Find bottlenecks
- Identify inefficiencies
- Note resource waste
- Spot optimization opportunities

### Step 3: Evaluate Options
- **Optimize Existing**: Improve efficiency of current resources
- **Add Resources**: Hire new agents or add capabilities
- **Reallocate**: Move resources between tasks
- **Reduce**: Remove unnecessary resources

### Step 4: Compare Trade-offs
- Cost of optimization vs. adding resources
- Time to optimize vs. time to add
- Long-term vs. short-term benefits
- Risk and impact

### Step 5: Make Recommendation
- Choose optimization approach
- Justify decision
- Plan implementation
- Set success metrics

## Optimization Strategies

### Strategy 1: Improve Efficiency
**When**: Resources are underutilized or inefficient
**Approach**: Optimize workflows, reduce waste, improve processes
**Example**: Improve agent workflows to reduce time per task

### Strategy 2: Reallocate Resources
**When**: Resources are misallocated
**Approach**: Move resources to where they're needed
**Example**: Move agent from low-priority to high-priority tasks

### Strategy 3: Add Specialized Resources
**When**: Need specialized capabilities
**Approach**: Hire specialized agents for specific tasks
**Example**: Hire ML-engineer for machine learning tasks

### Strategy 4: Reduce Resources
**When**: Resources are over-allocated or unnecessary
**Approach**: Remove or reduce unnecessary resources
**Example**: Remove duplicate agents or consolidate work

## Optimization Decision Framework

### When to Optimize Existing Resources
- **Underutilization**: Resources not fully utilized
- **Inefficiency**: Processes can be improved
- **Waste**: Resources wasted on unnecessary work
- **Quick Wins**: Easy optimizations available
- **Cost Constraint**: Budget limits adding resources

### When to Add New Resources
- **Capacity Limit**: Current resources at capacity
- **Specialization Needed**: Need specialized capabilities
- **Time Constraint**: Optimization takes too long
- **Scale Required**: Need more resources for scale
- **Quality Issues**: Need more resources for quality

### When to Reallocate Resources
- **Misallocation**: Resources in wrong places
- **Priority Shift**: Priorities changed
- **Bottleneck**: Resources needed elsewhere
- **Balance**: Need to balance workload

### When to Reduce Resources
- **Over-allocation**: Too many resources
- **Duplication**: Duplicate capabilities
- **Low Value**: Resources on low-value work
- **Cost Reduction**: Need to reduce costs

## Resource Optimization Output Format

```markdown
## Resource Optimization Analysis

### Current State
[Description of current resource usage]

### Issues Identified
- [Issue 1]: [Description and impact]
- [Issue 2]: [Description and impact]

### Optimization Options

#### Option 1: [Optimization Strategy]
- **Approach**: [How to optimize]
- **Benefits**: [Benefits of this approach]
- **Costs**: [Costs or trade-offs]
- **Time**: [Time to implement]
- **Risk**: [Risk level]

#### Option 2: [Alternative Strategy]
[Similar format]

### Recommendation
**Strategy**: [Chosen strategy]
**Rationale**: [Why this strategy]
**Implementation**: [How to implement]
**Expected Results**: [Expected outcomes]

### Success Metrics
- [Metric 1]: [Target value]
- [Metric 2]: [Target value]
```

## Examples

### Example 1: Optimize Existing Resources

**Input**: implementation-engineer is taking too long on tasks

**Output**:
```markdown
## Resource Optimization Analysis

### Current State
implementation-engineer is handling 5 tasks but taking longer than expected. Average task completion time is 3 days, but should be 1-2 days. Agent is working on both frontend and backend tasks, switching context frequently.

### Issues Identified
- **Context Switching**: Agent switches between frontend and backend, causing inefficiency
- **Workload**: 5 tasks may be too many for optimal performance
- **Lack of Specialization**: Agent handles diverse tasks without specialization

### Optimization Options

#### Option 1: Reduce Context Switching
- **Approach**: Group similar tasks together, reduce task switching
- **Benefits**: 
  - Faster task completion
  - Better focus
  - Reduced overhead
- **Costs**: 
  - May delay some tasks
  - Requires better task planning
- **Time**: Immediate (just reorder tasks)
- **Risk**: Low

#### Option 2: Hire Specialized Agents
- **Approach**: Hire frontend-engineer and backend-engineer separately
- **Benefits**:
  - Specialization improves efficiency
  - Can work in parallel
  - Better expertise
- **Costs**:
  - Time to create new agents
  - More agents to manage
- **Time**: 1-2 days to create agents
- **Risk**: Medium

#### Option 3: Reduce Workload
- **Approach**: Reduce to 3 tasks at a time
- **Benefits**:
  - Faster completion per task
  - Better quality
  - Less stress
- **Costs**:
  - Slower overall throughput
  - May need more agents
- **Time**: Immediate
- **Risk**: Low

### Recommendation
**Strategy**: Option 1 (Reduce Context Switching) + Option 3 (Reduce Workload)
**Rationale**: 
- Grouping similar tasks reduces context switching overhead
- Reducing workload to 3 tasks improves focus and speed
- This is a quick win that doesn't require new agents
- Can evaluate Option 2 later if needed

**Implementation**: 
1. Group tasks by type (frontend vs backend)
2. Assign 3 tasks at a time, grouped by type
3. Complete one group before starting next
4. Monitor completion times

**Expected Results**: 
- Task completion time: 3 days → 1.5 days
- Better focus and quality
- Improved throughput

### Success Metrics
- Average task completion time: < 2 days
- Context switches per day: < 2
- Task quality: Maintained or improved
```

### Example 2: Add New Resources

**Input**: Need machine learning capabilities but no ML agent exists

**Output**:
```markdown
## Resource Optimization Analysis

### Current State
Project has 3 ML tasks but no agent with ML capabilities. Current agents (implementation-engineer, infrastructure-engineer) don't have ML expertise. Tasks are blocked.

### Issues Identified
- **Capability Gap**: No agent can handle ML tasks
- **Blocked Work**: 3 tasks cannot proceed
- **Quality Risk**: Attempting ML with non-specialized agents risks poor quality

### Optimization Options

#### Option 1: Hire ML Engineer Agent
- **Approach**: Create ml-engineer agent with ML capabilities
- **Benefits**:
  - Specialized ML expertise
  - Can handle all ML tasks
  - Better quality results
  - Enables ML work to proceed
- **Costs**:
  - Time to create agent (1 day)
  - Additional agent to manage
- **Time**: 1 day to create agent
- **Risk**: Low

#### Option 2: Train Existing Agent
- **Approach**: Add ML skills to implementation-engineer
- **Benefits**:
  - No new agent needed
  - Uses existing agent
- **Costs**:
  - May not achieve same quality
  - Agent may be less efficient
  - Time to add skills
- **Time**: 1-2 days to add skills
- **Risk**: Medium (quality concerns)

#### Option 3: Outsource ML Tasks
- **Approach**: Handle ML tasks externally or defer
- **Benefits**:
  - No agent creation needed
- **Costs**:
  - Tasks remain blocked
  - Project delays
  - May not be feasible
- **Time**: N/A (tasks blocked)
- **Risk**: High (project impact)

### Recommendation
**Strategy**: Option 1 (Hire ML Engineer Agent)
**Rationale**: 
- ML tasks require specialized expertise
- Creating specialized agent ensures quality
- Time investment (1 day) is small compared to project impact
- Enables all ML work to proceed
- Better long-term solution

**Implementation**: 
1. Use agent-creator to create ml-engineer agent
2. Add ML-specific skills
3. Assign ML tasks to new agent
4. Monitor performance

**Expected Results**: 
- ML tasks can proceed
- High-quality ML implementation
- Project unblocked
- Specialized expertise available

### Success Metrics
- ML tasks completed: 3/3
- ML task quality: High
- Agent creation time: < 1 day
- Project unblocked: Yes
```

### Example 3: Reallocate Resources

**Input**: High-priority tasks blocked while low-priority tasks have resources

**Output**:
```markdown
## Resource Optimization Analysis

### Current State
3 high-priority (P0) tasks are blocked waiting for implementation-engineer, while implementation-engineer is working on 2 low-priority (P3) tasks. Resource allocation doesn't match priorities.

### Issues Identified
- **Priority Mismatch**: High-priority tasks blocked by low-priority work
- **Resource Misallocation**: Resources on wrong tasks
- **Project Impact**: Critical work delayed

### Optimization Options

#### Option 1: Reallocate to High-Priority Tasks
- **Approach**: Move implementation-engineer from P3 tasks to P0 tasks
- **Benefits**:
  - Unblocks critical work
  - Aligns resources with priorities
  - Immediate impact
- **Costs**:
  - P3 tasks delayed
  - Context switching overhead
- **Time**: Immediate
- **Risk**: Low

#### Option 2: Hire Additional Agent
- **Approach**: Hire another implementation-engineer for P0 tasks
- **Benefits**:
  - Both P0 and P3 tasks can proceed
  - No task delays
- **Costs**:
  - Time to create agent
  - Additional agent to manage
- **Time**: 1 day to create agent
- **Risk**: Low

#### Option 3: Defer P3 Tasks
- **Approach**: Pause P3 tasks, focus on P0
- **Benefits**:
  - Focus on critical work
  - Immediate reallocation
- **Costs**:
  - P3 tasks delayed
  - May need to resume later
- **Time**: Immediate
- **Risk**: Low

### Recommendation
**Strategy**: Option 1 (Reallocate to High-Priority Tasks)
**Rationale**: 
- High-priority tasks should take precedence
- Quick reallocation unblocks critical work
- P3 tasks can wait (they're low priority)
- No need for additional agents yet
- Can evaluate Option 2 if P3 tasks become urgent

**Implementation**: 
1. Pause current P3 tasks
2. Assign P0 tasks to implementation-engineer
3. Resume P3 tasks after P0 complete
4. Monitor progress

**Expected Results**: 
- P0 tasks unblocked
- Critical work proceeds
- P3 tasks delayed (acceptable for low priority)
- Resources aligned with priorities

### Success Metrics
- P0 tasks unblocked: 3/3
- P0 task completion: On schedule
- Resource alignment: Improved
- Project impact: Positive
```

## Best Practices

- **Analyze Thoroughly**: Understand current state before optimizing
- **Consider Trade-offs**: Evaluate costs and benefits
- **Think Long-term**: Consider long-term implications
- **Start Simple**: Try simple optimizations first
- **Monitor Results**: Track optimization effectiveness
- **Be Flexible**: Adjust strategy as needed
