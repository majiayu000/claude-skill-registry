---
name: task-dependency-resolver-skill
description: Implements Kahn's algorithm for topological sorting and cycle detection in task dependency graphs
version: 1.0.0
tags: [orchestration, dag, dependencies, topological-sort, cycle-detection]
---

# Task Dependency Resolver Skill

## Purpose

This skill provides algorithms for analyzing and resolving task dependencies in multi-agent workflows. It implements Kahn's algorithm for topological sorting, cycle detection using depth-first search, and dependency validation to ensure workflows can execute correctly.

## When to Use This Skill

**Use this skill when:**
- ✅ Executing workflows with complex task dependencies
- ✅ Need to determine optimal execution order
- ✅ Must validate workflow definitions before execution
- ✅ Building DAG-based orchestration systems
- ✅ Detecting circular dependencies

**Don't use this skill for:**
- ❌ Simple sequential workflows (no dependencies)
- ❌ Workflows already validated and sorted
- ❌ Real-time streaming tasks (DAGs are batch-oriented)

## Core Algorithms

### 1. Kahn's Algorithm (Topological Sort)

**Purpose**: Determine linear ordering of tasks respecting all dependencies

**Time Complexity**: O(V + E) where V = tasks, E = dependencies

**Algorithm**:
```python
def topological_sort_kahn(tasks: Dict[str, Task], dependencies: Dict[str, List[str]]) -> List[str]:
    """
    Kahn's algorithm for topological sorting.

    Args:
        tasks: Dictionary of task_id -> Task object
        dependencies: Dictionary of task_id -> list of dependency task_ids

    Returns:
        List of task_ids in topological order

    Raises:
        CycleDetectedError: If circular dependency exists
    """
    from collections import defaultdict, deque

    # Build graph and calculate in-degrees
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    # Initialize all tasks with in-degree 0
    for task_id in tasks:
        in_degree[task_id] = 0

    # Build adjacency list and in-degrees
    for task_id, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task_id)  # dep -> task_id edge
            in_degree[task_id] += 1

    # Queue all tasks with no dependencies
    queue = deque([task_id for task_id in tasks if in_degree[task_id] == 0])
    sorted_order = []

    # Process queue
    while queue:
        current = queue.popleft()
        sorted_order.append(current)

        # Reduce in-degree for all neighbors
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Check if all tasks were processed (no cycle)
    if len(sorted_order) != len(tasks):
        raise CycleDetectedError("Circular dependency detected")

    return sorted_order
```

**Example**:
```python
tasks = {
    "analyze": Task(...),
    "design": Task(...),
    "implement": Task(...),
    "test": Task(...)
}

dependencies = {
    "design": ["analyze"],
    "implement": ["design"],
    "test": ["implement"]
}

# Result: ["analyze", "design", "implement", "test"]
sorted_tasks = topological_sort_kahn(tasks, dependencies)
```

### 2. Cycle Detection (DFS)

**Purpose**: Detect circular dependencies before execution

**Time Complexity**: O(V + E)

**Algorithm**:
```python
def detect_cycle_dfs(tasks: Dict[str, Task], dependencies: Dict[str, List[str]]) -> Optional[List[str]]:
    """
    Detect cycles using depth-first search with coloring.

    Args:
        tasks: Dictionary of task_id -> Task object
        dependencies: Dictionary of task_id -> list of dependency task_ids

    Returns:
        List representing cycle path if found, None otherwise
    """
    from collections import defaultdict

    # Build graph
    graph = defaultdict(list)
    for task_id, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task_id)

    # Colors: WHITE (unvisited), GRAY (visiting), BLACK (visited)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {task_id: WHITE for task_id in tasks}
    parent = {task_id: None for task_id in tasks}

    def dfs(node: str, path: List[str]) -> Optional[List[str]]:
        """DFS with cycle detection."""
        color[node] = GRAY
        path.append(node)

        for neighbor in graph[node]:
            if color[neighbor] == GRAY:
                # Back edge found - cycle detected
                cycle_start = path.index(neighbor)
                return path[cycle_start:] + [neighbor]

            if color[neighbor] == WHITE:
                parent[neighbor] = node
                cycle = dfs(neighbor, path[:])
                if cycle:
                    return cycle

        color[node] = BLACK
        return None

    # Check each component
    for task_id in tasks:
        if color[task_id] == WHITE:
            cycle = dfs(task_id, [])
            if cycle:
                return cycle

    return None
```

**Example**:
```python
# Cycle: A -> B -> C -> A
dependencies = {
    "A": ["C"],
    "B": ["A"],
    "C": ["B"]
}

cycle = detect_cycle_dfs(tasks, dependencies)
# Result: ["A", "C", "B", "A"]
```

### 3. Dependency Validation

**Purpose**: Validate workflow definition before execution

**Algorithm**:
```python
def validate_dependencies(tasks: Dict[str, Task], dependencies: Dict[str, List[str]]) -> ValidationResult:
    """
    Validate task dependencies for common errors.

    Returns:
        ValidationResult with errors and warnings
    """
    errors = []
    warnings = []

    # 1. Check for missing task references
    all_task_ids = set(tasks.keys())
    for task_id, deps in dependencies.items():
        if task_id not in all_task_ids:
            errors.append(f"Task '{task_id}' not found in task list")

        for dep in deps:
            if dep not in all_task_ids:
                errors.append(f"Dependency '{dep}' of task '{task_id}' not found")

    # 2. Check for self-dependencies
    for task_id, deps in dependencies.items():
        if task_id in deps:
            errors.append(f"Task '{task_id}' depends on itself")

    # 3. Check for cycles
    try:
        cycle = detect_cycle_dfs(tasks, dependencies)
        if cycle:
            cycle_path = " → ".join(cycle)
            errors.append(f"Circular dependency detected: {cycle_path}")
    except Exception as e:
        errors.append(f"Cycle detection failed: {str(e)}")

    # 4. Check for unreachable tasks (tasks with no path from entry points)
    entry_points = [tid for tid in tasks if not dependencies.get(tid, [])]
    if not entry_points:
        errors.append("No entry points found (all tasks have dependencies)")

    # 5. Warn about deep dependency chains
    max_depth = calculate_max_depth(tasks, dependencies)
    if max_depth > 10:
        warnings.append(f"Deep dependency chain detected (depth: {max_depth}). Consider flattening.")

    return ValidationResult(errors=errors, warnings=warnings)
```

### 4. Batching for Parallel Execution

**Purpose**: Group independent tasks into execution batches

**Algorithm**:
```python
def create_execution_batches(tasks: Dict[str, Task], dependencies: Dict[str, List[str]]) -> List[List[str]]:
    """
    Group tasks into batches where each batch contains only independent tasks.

    Args:
        tasks: Dictionary of task_id -> Task object
        dependencies: Dictionary of task_id -> list of dependency task_ids

    Returns:
        List of batches, where each batch is a list of task_ids that can run in parallel
    """
    from collections import defaultdict, deque

    # Build graph and calculate in-degrees
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for task_id in tasks:
        in_degree[task_id] = 0

    for task_id, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task_id)
            in_degree[task_id] += 1

    # Process in batches
    batches = []
    current_batch = [tid for tid in tasks if in_degree[tid] == 0]

    while current_batch:
        batches.append(current_batch[:])
        next_batch = []

        for task_id in current_batch:
            for neighbor in graph[task_id]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    next_batch.append(neighbor)

        current_batch = next_batch

    return batches
```

**Example**:
```python
tasks = {"A": Task(), "B": Task(), "C": Task(), "D": Task(), "E": Task()}

dependencies = {
    "B": ["A"],
    "C": ["A"],
    "D": ["B", "C"],
    "E": ["D"]
}

batches = create_execution_batches(tasks, dependencies)
# Result:
# Batch 0: ["A"]           (no dependencies)
# Batch 1: ["B", "C"]      (both depend only on A)
# Batch 2: ["D"]           (depends on B and C)
# Batch 3: ["E"]           (depends on D)
```

## Workflow

### Step 1: Parse Workflow Definition

```python
def parse_workflow_yaml(yaml_content: str) -> Tuple[Dict, Dict]:
    """Parse YAML workflow into tasks and dependencies."""
    import yaml

    workflow = yaml.safe_load(yaml_content)

    tasks = {}
    dependencies = {}

    for task_def in workflow["tasks"]:
        task_id = task_def["id"]
        tasks[task_id] = Task(
            id=task_id,
            command=task_def["command"],
            args=task_def.get("args", [])
        )
        dependencies[task_id] = task_def.get("dependencies", [])

    return tasks, dependencies
```

### Step 2: Validate Dependencies

```python
validation_result = validate_dependencies(tasks, dependencies)

if validation_result.errors:
    print("❌ Workflow validation failed:")
    for error in validation_result.errors:
        print(f"  - {error}")
    exit(1)

if validation_result.warnings:
    print("⚠️ Warnings:")
    for warning in validation_result.warnings:
        print(f"  - {warning}")
```

### Step 3: Detect Cycles

```python
cycle = detect_cycle_dfs(tasks, dependencies)

if cycle:
    cycle_path = " → ".join(cycle)
    raise CycleDetectedError(f"Circular dependency: {cycle_path}")
```

### Step 4: Create Execution Plan

```python
# Option A: Linear execution order (topological sort)
sorted_tasks = topological_sort_kahn(tasks, dependencies)
print("Execution order:", " → ".join(sorted_tasks))

# Option B: Parallel execution batches
batches = create_execution_batches(tasks, dependencies)
for i, batch in enumerate(batches):
    print(f"Batch {i}: {', '.join(batch)} (can run in parallel)")
```

### Step 5: Calculate Critical Path

```python
def calculate_critical_path(tasks: Dict[str, Task], dependencies: Dict[str, List[str]]) -> Tuple[List[str], int]:
    """Calculate critical path (longest dependency chain)."""
    from collections import defaultdict

    # Build reverse graph for backward traversal
    graph = defaultdict(list)
    for task_id, deps in dependencies.items():
        for dep in deps:
            graph[dep].append(task_id)

    # Calculate longest path to each task
    longest_path = {}

    def dfs_longest_path(node: str) -> int:
        if node in longest_path:
            return longest_path[node]

        max_path = 0
        for neighbor in graph[node]:
            max_path = max(max_path, dfs_longest_path(neighbor))

        task_duration = tasks[node].estimated_duration or 1
        longest_path[node] = max_path + task_duration
        return longest_path[node]

    # Calculate for all tasks
    for task_id in tasks:
        dfs_longest_path(task_id)

    # Find critical path (task with longest path)
    critical_task = max(longest_path, key=longest_path.get)
    critical_duration = longest_path[critical_task]

    # Reconstruct path
    path = [critical_task]
    current = critical_task
    while dependencies.get(current):
        # Find dependency with longest path
        deps = dependencies[current]
        next_task = max(deps, key=lambda t: longest_path.get(t, 0))
        path.append(next_task)
        current = next_task

    return list(reversed(path)), critical_duration
```

## Error Handling

### Cycle Detection Error

```python
class CycleDetectedError(Exception):
    """Raised when circular dependency is detected."""

    def __init__(self, cycle_path: List[str]):
        self.cycle_path = cycle_path
        message = f"Circular dependency detected: {' → '.join(cycle_path)}"
        super().__init__(message)
```

**Resolution**:
```
1. Review workflow definition
2. Identify cycle: A → B → C → A
3. Remove or reorder dependencies:
   - Option 1: Remove A's dependency on C
   - Option 2: Merge circular tasks into single task
   - Option 3: Reorder workflow to break cycle
```

### Missing Task Reference

```python
class MissingTaskError(Exception):
    """Raised when task reference not found."""
    pass
```

**Resolution**:
```
1. Check task ID spelling
2. Verify task exists in workflow definition
3. Use autocomplete or validation tools
```

## Integration Patterns

### With DAG Orchestrator

```python
# In DAG Orchestrator Agent
from skills.orchestration.task_dependency_resolver import (
    topological_sort_kahn,
    detect_cycle_dfs,
    validate_dependencies,
    create_execution_batches
)

# Step 1: Validate
validation = validate_dependencies(tasks, dependencies)
if validation.errors:
    raise WorkflowValidationError(validation.errors)

# Step 2: Detect cycles
cycle = detect_cycle_dfs(tasks, dependencies)
if cycle:
    raise CycleDetectedError(cycle)

# Step 3: Create execution plan
batches = create_execution_batches(tasks, dependencies)

# Step 4: Execute batches in parallel
for batch_num, batch in enumerate(batches):
    print(f"Executing Batch {batch_num}: {batch}")
    execute_batch_in_parallel(batch)
```

### With State Manager

```python
# Store dependency graph in shared state
state_manager.put("workflow_graph", {
    "tasks": tasks,
    "dependencies": dependencies,
    "sorted_order": topological_sort_kahn(tasks, dependencies),
    "batches": create_execution_batches(tasks, dependencies)
})
```

## Examples

### Example 1: Simple Build Pipeline

```yaml
# workflow.yml
tasks:
  - id: install_deps
    command: npm install
    dependencies: []

  - id: lint
    command: npm run lint
    dependencies: [install_deps]

  - id: test
    command: npm test
    dependencies: [install_deps]

  - id: build
    command: npm run build
    dependencies: [lint, test]

  - id: deploy
    command: npm run deploy
    dependencies: [build]
```

**Analysis**:
```python
tasks, dependencies = parse_workflow_yaml(yaml_content)

# Validate
validation = validate_dependencies(tasks, dependencies)
# ✓ No errors

# Create batches
batches = create_execution_batches(tasks, dependencies)
# Batch 0: [install_deps]
# Batch 1: [lint, test]         # Can run in parallel!
# Batch 2: [build]
# Batch 3: [deploy]

# Critical path
path, duration = calculate_critical_path(tasks, dependencies)
# Path: install_deps → test → build → deploy
# Duration: 15 minutes (if test is slowest)
```

### Example 2: Circular Dependency (Error)

```yaml
tasks:
  - id: task_a
    dependencies: [task_c]

  - id: task_b
    dependencies: [task_a]

  - id: task_c
    dependencies: [task_b]
```

**Analysis**:
```python
cycle = detect_cycle_dfs(tasks, dependencies)
# Result: ["task_a", "task_c", "task_b", "task_a"]

# Error message:
# ❌ Circular dependency detected: task_a → task_c → task_b → task_a
```

### Example 3: Feature Development Workflow

```yaml
tasks:
  - id: analyze_requirements
    dependencies: []

  - id: design_frontend
    dependencies: [analyze_requirements]

  - id: design_backend
    dependencies: [analyze_requirements]

  - id: design_database
    dependencies: [analyze_requirements]

  - id: implement_frontend
    dependencies: [design_frontend, design_database]

  - id: implement_backend
    dependencies: [design_backend, design_database]

  - id: integration_tests
    dependencies: [implement_frontend, implement_backend]

  - id: deploy_staging
    dependencies: [integration_tests]
```

**Analysis**:
```python
batches = create_execution_batches(tasks, dependencies)

# Batch 0: [analyze_requirements]
# Batch 1: [design_frontend, design_backend, design_database]  # 3 parallel
# Batch 2: [implement_frontend, implement_backend]             # 2 parallel
# Batch 3: [integration_tests]
# Batch 4: [deploy_staging]

# Parallelization analysis:
total_tasks = 8
sequential_time = sum(task.duration for task in tasks)  # 60 minutes
parallel_time = max_batch_duration(batches)              # 28 minutes
speedup = sequential_time / parallel_time                 # 2.14x
efficiency = speedup / max_parallel_tasks                 # 71%
```

## Best Practices

1. **Always Validate Before Execution**
   ```python
   validation = validate_dependencies(tasks, dependencies)
   assert not validation.errors, "Fix errors before executing"
   ```

2. **Use Batching for Parallelization**
   ```python
   batches = create_execution_batches(tasks, dependencies)
   for batch in batches:
       execute_parallel(batch)  # Maximize throughput
   ```

3. **Calculate Critical Path Early**
   ```python
   path, duration = calculate_critical_path(tasks, dependencies)
   print(f"Critical path: {path}")
   print(f"Minimum duration: {duration} minutes")
   # Focus optimization efforts on critical path tasks
   ```

4. **Handle Cycles Gracefully**
   ```python
   cycle = detect_cycle_dfs(tasks, dependencies)
   if cycle:
       suggest_fix(cycle)  # Provide actionable resolution
   ```

5. **Monitor Depth**
   ```python
   max_depth = calculate_max_depth(tasks, dependencies)
   if max_depth > 10:
       warn("Consider flattening deep dependency chains")
   ```

## Related Skills

- `dag-orchestrator-skill`: Uses this skill for execution planning
- `observability-tracker-skill`: Tracks actual execution vs plan
- `performance-profiler-skill`: Analyzes critical path efficiency

## References

- [Kahn's Algorithm](https://en.wikipedia.org/wiki/Topological_sorting#Kahn's_algorithm)
- [Cycle Detection Algorithms](https://en.wikipedia.org/wiki/Cycle_detection)
- Document 15, Section 2: Complex Dependency Management

---

**Version**: 1.0.0
**Status**: Production Ready
**Complexity**: High (advanced algorithms)
**Token Cost**: Low (pure computation, minimal I/O)
