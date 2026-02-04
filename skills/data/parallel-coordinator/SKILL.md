---
name: parallel-coordinator
version: 1.0
last_updated: 2026-01-29
description: Orchestrate multiple independent agents running simultaneously, leveraging Claude Sonnet 4.5's parallel tool execution capabilities to maximize throughput on multi-task requests.
success_criteria:
  - Independent tasks correctly identified and parallelized
  - All parallel tasks completed successfully
  - Results consolidated and presented coherently
  - No task dependencies violated
  - Throughput improvement achieved vs sequential execution
  - Error handling preserves partial results when tasks fail
---

# Parallel Coordinator

## Purpose

The Parallel Coordinator skill enables orchestration of multiple independent agents executing simultaneously. By leveraging Claude Sonnet 4.5's native capability to execute multiple tool calls in a single message, this skill maximizes throughput when users present requests containing multiple independent tasks.

This skill transforms sequential bottlenecks into parallel workflows, reducing overall completion time and improving user experience when handling complex, multi-faceted requests.

## When to Use This Skill

Invoke the Parallel Coordinator when:

1. **Multiple Independent Tasks**: The user's request contains 2 or more tasks that can be completed without interdependencies
2. **Parallelizable Operations**: Tasks involve I/O-bound operations (file reading, web searches, API calls) that benefit from concurrent execution
3. **Multi-Domain Requests**: The request spans different domains or contexts (e.g., "analyze this dataset AND review that codebase AND research this topic")
4. **Batch Operations**: The user needs the same operation performed on multiple independent targets

### Clear Indicators for Use

- User employs conjunctions suggesting independence: "and also", "separately", "in parallel"
- Request contains numbered or bulleted lists of distinct tasks
- Tasks operate on different files, datasets, or domains
- No shared mutable state between tasks
- Results can be aggregated after completion without cross-dependencies

### When NOT to Use

Do not use this skill when:

- Tasks have sequential dependencies (Task B requires output from Task A)
- Tasks modify shared resources that could create race conditions
- A single cohesive task that happens to involve multiple steps
- User explicitly requests sequential execution
- Tasks are trivial and parallelization overhead exceeds benefits

## Core Workflow

The Parallel Coordinator follows a structured four-phase approach:

### Phase 1: Task Decomposition and Analysis

**Objective**: Break down the user's request into discrete, analyzable units.

1. **Parse the Request**: Identify all distinct tasks within the user's message
2. **Extract Requirements**: For each task, determine:
   - Inputs required
   - Expected outputs
   - Resources needed (files, APIs, tools)
   - Estimated complexity
3. **Document Task Boundaries**: Clearly define where one task ends and another begins

### Phase 2: Dependency Verification

**Objective**: Ensure tasks are truly independent and can safely execute in parallel.

1. **Check Data Dependencies**: Verify no task requires output from another
2. **Identify Shared Resources**: Flag any files, databases, or APIs used by multiple tasks
3. **Assess Resource Conflicts**: Determine if shared resources are read-only (safe) or mutable (unsafe)
4. **Validate Independence**: Confirm each task can complete successfully without waiting for others

**Decision Point**: If dependencies exist, either:
- Restructure into independent phases (Phase 1 tasks run parallel, then Phase 2 tasks run parallel)
- Abort parallelization and execute sequentially

### Phase 3: Parallel Execution

**Objective**: Launch all independent tasks simultaneously using Claude Sonnet 4.5's parallel tool execution.

1. **Create Task Definitions**: Use TaskCreate to define each independent task with:
   - Clear, actionable subject in imperative form
   - Detailed description including context and acceptance criteria
   - Present continuous activeForm for progress tracking

2. **Execute in Single Message**: Make all TaskCreate calls within one function_calls block to ensure true parallel execution

3. **Monitor Progress**: Track task completion status without blocking

**Technical Implementation**: Execute multiple tool calls simultaneously in a single function_calls block. This is Claude Sonnet 4.5's key strength - the ability to fire off multiple independent operations at once.

### Phase 4: Result Integration

**Objective**: Aggregate outputs from parallel tasks into a cohesive response.

1. **Collect Results**: Gather outputs from all completed tasks
2. **Identify Cross-Task Insights**: Look for patterns, contradictions, or synergies across results
3. **Synthesize Response**: Combine individual results into a unified, coherent answer
4. **Validate Completeness**: Ensure all original user requirements are addressed

## Parallel Execution Patterns

### Pattern 1: Homogeneous Batch Processing

**Use Case**: Apply the same operation to multiple independent targets.

**Example**: "Analyze code quality in files A.py, B.py, and C.py"

**Approach**:
- Create identical task templates
- Parameterize by target (file, dataset, etc.)
- Execute all instances simultaneously
- Compare results in aggregation phase

**Benefits**:
- Reduces total time from 3T to T (where T is single task duration)
- Enables comparative analysis across targets

### Pattern 2: Heterogeneous Multi-Domain

**Use Case**: Perform different operations across unrelated domains.

**Example**: "Research quantum computing papers, analyze sales data, and review frontend code"

**Approach**:
- Define domain-specific tasks with unique requirements
- Ensure no shared resources between domains
- Execute all tasks simultaneously
- Present results in structured, domain-separated format

**Benefits**:
- Maximizes throughput on diverse requests
- Reduces context switching for user

### Pattern 3: Fork-Join with Independent Forks

**Use Case**: Parallel exploration followed by synthesis.

**Example**: "Search for solutions in documentation, Stack Overflow, and GitHub issues, then summarize"

**Approach**:
- **Fork Phase**: Launch parallel search tasks
- **Join Phase**: After all complete, synthesize findings
- Ensure fork tasks are truly independent

**Benefits**:
- Comprehensive exploration in minimal time
- Enables better synthesis from multiple sources

### Pattern 4: Pipeline Parallelism

**Use Case**: Multiple independent pipelines executing simultaneously.

**Example**: "Process Dataset A (load, clean, analyze) AND Dataset B (load, clean, analyze) AND Dataset C (load, clean, analyze)"

**Approach**:
- Each pipeline is a sequential chain within itself
- Pipelines are independent of each other
- Execute all pipelines simultaneously
- Each pipeline maintains internal order while running parallel to others

**Benefits**:
- Parallelizes at pipeline level, not step level
- Maintains data integrity within each pipeline

## Handling Shared Resources

### Read-Only Resources (Safe for Parallel Access)

When multiple tasks read from the same resource without modification:

**Acceptable Scenarios**:
- Multiple tasks reading the same configuration file
- Parallel web searches using the same search API
- Multiple analyses of the same immutable dataset

**Best Practices**:
- Document shared read dependencies
- Verify resource won't change during execution
- Consider caching if resource access is expensive

### Mutable Resources (Unsafe - Requires Coordination)

When tasks might modify shared state:

**Problematic Scenarios**:
- Multiple tasks editing the same file
- Parallel writes to the same database
- Concurrent modifications to shared data structures

**Mitigation Strategies**:
- **Partition Resources**: Divide mutable resource into independent sections
- **Sequence Critical Sections**: Parallelize non-conflicting parts, sequence conflicting parts
- **Abort Parallelization**: Execute sequentially if conflicts are unavoidable

## Examples of Effective Parallelization

### Example 1: Multi-Modal Research Task

**User Request**: "Research recent advances in transformer architectures, analyze sentiment in customer reviews dataset, and create a visualization of our Q4 sales data"

**Parallelization Strategy**:

**Task 1 - Research Agent**:
- Subject: "Research transformer architecture advances"
- Actions: Web search, documentation review, summarization
- Resources: Web search API (read-only, shared safe)

**Task 2 - Analysis Agent**:
- Subject: "Analyze sentiment in customer reviews"
- Actions: Load dataset, apply sentiment analysis, generate statistics
- Resources: reviews.csv (read-only)

**Task 3 - Visualization Agent**:
- Subject: "Create Q4 sales visualization"
- Actions: Load sales data, generate charts, export images
- Resources: sales_q4.csv (read-only)

**Independence Verification**:
- No data dependencies between tasks
- All resources are read-only
- Results can be aggregated independently

**Expected Outcome**: Completion in time T (single task duration) vs. 3T (sequential)

### Example 2: Parallel Literature Review

**User Request**: "Find papers on: neural architecture search, federated learning, and explainable AI"

**Parallelization Strategy**:

**Three Parallel Search Agents**:
- Each conducts independent literature search on one topic
- No shared mutable state
- Results aggregated for comparative analysis

**Benefits**:
- Comprehensive coverage in 1/3 the time
- Enables cross-topic insights during synthesis

### Example 3: Multi-Codebase Analysis

**User Request**: "Review code quality in our auth service, payment service, and notification service"

**Parallelization Strategy**:

**Three Parallel Review Agents**:
- Each analyzes one service codebase
- Independent file systems (no conflicts)
- Consistent evaluation criteria across all agents

**Synthesis Phase**:
- Compare quality metrics across services
- Identify common patterns and anti-patterns
- Prioritize remediation efforts

## Anti-Patterns and Common Pitfalls

### Anti-Pattern 1: Premature Parallelization

**Problem**: Attempting to parallelize tasks with hidden dependencies.

**Example**: "Analyze file A, then use those insights to process file B" - These tasks appear independent but have implicit data dependency.

**Solution**: Always perform explicit dependency analysis before parallelizing.

### Anti-Pattern 2: Over-Granular Parallelization

**Problem**: Creating too many tiny parallel tasks with high coordination overhead.

**Example**: Parallelizing 20 tasks that each take 2 seconds - coordination overhead exceeds benefits.

**Solution**: Aim for 2-5 substantial tasks. Batch small operations into larger tasks.

### Anti-Pattern 3: Ignoring Shared Mutable State

**Problem**: Multiple tasks modifying the same resource concurrently.

**Example**: Three tasks appending to the same output file without coordination.

**Solution**: Either partition the resource or sequence the conflicting operations.

### Anti-Pattern 4: False Independence

**Problem**: Tasks appear independent but share implicit coupling.

**Example**: Two tasks analyzing the same dataset where first performs cleaning that second assumes - if second runs before first, results are incorrect.

**Solution**: Make all dependencies explicit. If implicit coupling exists, tasks are not independent.

## Integration and Result Synthesis

### Collecting Results

After all parallel tasks complete:

1. **Verify Completion**: Confirm all tasks reached completion state
2. **Check for Errors**: Identify any failures or partial completions
3. **Gather Outputs**: Collect all results, maintaining task identity

### Synthesis Strategies

**Aggregation**: When results are similar in nature:
- Combine into unified list or table
- Calculate summary statistics
- Identify outliers or anomalies

**Comparison**: When results should be evaluated against each other:
- Highlight similarities and differences
- Rank or prioritize based on criteria
- Identify best practices or concerns

**Integration**: When results form parts of a larger whole:
- Identify connections between findings
- Construct comprehensive narrative
- Address user's original intent holistically

### Presenting Results

Structure the final response to:
1. **Summarize Overall Findings**: High-level overview addressing user's request
2. **Detail Individual Results**: Present each task's output with clear attribution
3. **Highlight Cross-Task Insights**: Note patterns, contradictions, or synergies discovered
4. **Provide Actionable Recommendations**: Based on complete picture from all tasks

## Technical Considerations

### Claude Sonnet 4.5 Parallel Execution

Claude Sonnet 4.5 has native support for executing multiple tool calls in a single message. Key characteristics:

- **True Parallelism**: When multiple independent tool calls are provided in one function_calls block, they execute concurrently
- **I/O Optimization**: Particularly effective for I/O-bound operations (file reads, web requests)
- **No Explicit Threading**: Parallelism is handled automatically by the execution environment
- **Result Ordering**: Results return in completion order, not call order

### Best Practices for Tool Calls

1. **Batch Independent Calls**: Group all independent tool calls in one function_calls block
2. **Avoid Sequential Calls**: Don't make a call, wait for result, then make another if they could be parallel
3. **Use TaskCreate for Complex Work**: For substantial tasks that may involve multiple steps, use Task tools to maintain coordination
4. **Monitor, Don't Block**: Check task status without waiting synchronously

### Performance Expectations

**Ideal Scenarios** (near-linear speedup):
- File reading operations (Read tool)
- Web searches (WebSearch tool)
- Independent code analysis tasks
- Parallel API calls

**Limited Speedup Scenarios**:
- CPU-bound operations (computation)
- Tasks with hidden dependencies
- Very short tasks (coordination overhead dominates)

## Skill Invocation Contract

When this skill is invoked:

**Input Requirements**:
- User request containing 2+ potentially independent tasks
- Clear specification of what each task should accomplish
- Sufficient context to identify dependencies

**Skill Responsibilities**:
1. Analyze request for parallelization opportunities
2. Verify task independence through dependency analysis
3. Create and launch parallel tasks using appropriate tools
4. Monitor execution progress
5. Integrate results into cohesive response
6. Present findings in structured, actionable format

**Output Guarantees**:
- All independent tasks executed in parallel
- Results from all tasks included in final response
- Dependencies respected (no race conditions)
- Clear attribution of results to tasks
- Synthesis that addresses original user intent

**Failure Modes**:
- If dependencies detected: Restructure or abort parallelization
- If task fails: Report failure, continue with successful tasks
- If resources conflict: Sequence conflicting operations

## Conclusion

The Parallel Coordinator skill unlocks Claude Sonnet 4.5's ability to execute multiple independent operations simultaneously. By carefully analyzing task dependencies, structuring parallel execution, and synthesizing results, this skill dramatically reduces completion time for multi-faceted requests.

Use this skill when independence is clear, dependencies are absent, and the user's request naturally decomposes into concurrent operations. The result is faster, more efficient responses that maintain quality while maximizing throughput.
