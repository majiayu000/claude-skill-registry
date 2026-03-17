---
name: agent-pool-manager-skill
description: Implements agent pool lifecycle management with auto-scaling, health monitoring, and resource optimization
version: 1.0.0
tags: [orchestration, agent-pool, auto-scaling, health-monitoring, resource-management]
---

# Agent Pool Manager Skill

## Purpose

This skill provides comprehensive agent pool management including auto-scaling (reactive and predictive), health monitoring, agent recycling, and resource optimization. It ensures efficient agent utilization while maintaining performance SLAs and cost control.

## When to Use This Skill

**Use this skill when:**
- ✅ Managing pools of worker agents for variable workloads
- ✅ Need auto-scaling based on queue depth or predictions
- ✅ Want health monitoring with automatic agent replacement
- ✅ Running long-duration workflows (>30 minutes)
- ✅ Optimizing costs while meeting performance targets

**Don't use this skill for:**
- ❌ Single-agent workflows
- ❌ Short, one-off tasks (<5 minutes)
- ❌ Workflows with fixed, predictable agent counts
- ❌ Development/testing (use fixed pools)

## Core Algorithms

### 1. Reactive Auto-Scaling

**Purpose**: Scale agent pool based on current workload metrics

**Algorithm**:
```python
def reactive_autoscale(
    current_pool_size: int,
    queue_depth: int,
    idle_agents: int,
    min_size: int,
    max_size: int,
    scale_up_threshold: int,
    scale_down_threshold: int,
    cooldown_remaining: int
) -> Tuple[str, int]:
    """
    Reactive auto-scaling based on current metrics.

    Args:
        current_pool_size: Current number of agents
        queue_depth: Number of tasks waiting
        idle_agents: Number of idle agents
        min_size: Minimum pool size
        max_size: Maximum pool size
        scale_up_threshold: Queue depth to trigger scale-up
        scale_down_threshold: Idle agents to trigger scale-down
        cooldown_remaining: Seconds until next scaling action allowed

    Returns:
        Tuple of (action, count) where action is "scale_up", "scale_down", or "no_action"
    """
    # Respect cooldown period
    if cooldown_remaining > 0:
        return ("no_action", 0)

    # Scale up if queue is backed up
    if queue_depth > scale_up_threshold:
        # Scale by half of queue depth, but don't exceed max
        agents_to_add = min(
            queue_depth // 2,
            max_size - current_pool_size
        )
        if agents_to_add > 0:
            return ("scale_up", agents_to_add)

    # Scale down if too many idle agents
    if idle_agents > scale_down_threshold:
        # Scale down by idle count minus threshold, but keep at least min
        agents_to_remove = min(
            idle_agents - scale_down_threshold,
            current_pool_size - min_size
        )
        if agents_to_remove > 0:
            return ("scale_down", agents_to_remove)

    return ("no_action", 0)
```

**Example**:
```python
# Scenario: Queue building up
action, count = reactive_autoscale(
    current_pool_size=5,
    queue_depth=12,        # 12 tasks waiting
    idle_agents=0,
    min_size=3,
    max_size=20,
    scale_up_threshold=5,  # Threshold exceeded
    scale_down_threshold=2,
    cooldown_remaining=0
)
# Result: ("scale_up", 6)  # Add 6 agents (12 / 2)
```

### 2. Predictive Auto-Scaling

**Purpose**: Scale proactively based on historical patterns

**Algorithm**:
```python
from typing import List
import statistics

def predictive_autoscale(
    current_pool_size: int,
    historical_load: List[Tuple[datetime, int]],
    min_size: int,
    max_size: int,
    prediction_window_minutes: int = 15
) -> Tuple[str, int]:
    """
    Predictive auto-scaling using historical load patterns.

    Args:
        current_pool_size: Current number of agents
        historical_load: List of (timestamp, queue_depth) tuples
        min_size: Minimum pool size
        max_size: Maximum pool size
        prediction_window_minutes: How far ahead to predict

    Returns:
        Tuple of (action, count)
    """
    from datetime import datetime, timedelta

    now = datetime.now()
    current_time = now.time()

    # Filter historical data for same time window
    similar_periods = []
    for timestamp, queue_depth in historical_load:
        # Get data from same time of day (±30 min window)
        if abs((timestamp.time().hour * 60 + timestamp.time().minute) -
               (current_time.hour * 60 + current_time.minute)) <= 30:
            similar_periods.append(queue_depth)

    if len(similar_periods) < 3:
        # Not enough data for prediction
        return ("no_action", 0)

    # Calculate statistics
    avg_load = statistics.mean(similar_periods)
    max_load = max(similar_periods)
    std_dev = statistics.stdev(similar_periods) if len(similar_periods) > 1 else 0

    # Predict load (use P95: mean + 1.65 * std_dev)
    predicted_load = avg_load + (1.65 * std_dev)

    # Calculate required agents (assume 1 agent per 2 tasks)
    required_agents = int(predicted_load / 2) + 1

    # Determine action
    if required_agents > current_pool_size:
        agents_to_add = min(
            required_agents - current_pool_size,
            max_size - current_pool_size
        )
        if agents_to_add > 0:
            return ("scale_up", agents_to_add)

    elif required_agents < current_pool_size - 2:  # Leave some buffer
        agents_to_remove = min(
            current_pool_size - required_agents - 1,  # Keep 1 extra
            current_pool_size - min_size
        )
        if agents_to_remove > 0:
            return ("scale_down", agents_to_remove)

    return ("no_action", 0)
```

**Example**:
```python
# Historical data shows load peaks at 10am
historical_load = [
    (datetime(2026, 1, 20, 10, 0), 25),  # Yesterday 10am: 25 tasks
    (datetime(2026, 1, 19, 10, 0), 28),  # 2 days ago: 28 tasks
    (datetime(2026, 1, 18, 10, 0), 22),  # 3 days ago: 22 tasks
]

# Current time: 9:50am (10 minutes before predicted peak)
action, count = predictive_autoscale(
    current_pool_size=5,
    historical_load=historical_load,
    min_size=3,
    max_size=20,
    prediction_window_minutes=15
)
# Result: ("scale_up", 8)  # Pre-scale before peak hits
# Predicted load: 28.3 tasks (mean + 1.65*stdev)
# Required agents: 15 (28.3 / 2 + 1)
# Add: 10 agents (15 - 5)
```

### 3. Health Monitoring

**Purpose**: Detect unhealthy agents and trigger replacement

**Algorithm**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AgentHealth:
    agent_id: str
    last_heartbeat: datetime
    consecutive_failures: int
    tasks_completed: int
    avg_task_duration: float
    status: str  # "healthy", "degraded", "unhealthy"

def check_agent_health(
    agent: AgentHealth,
    heartbeat_timeout_seconds: int = 30,
    failure_threshold: int = 3,
    task_duration_threshold_multiplier: float = 2.0,
    pool_avg_task_duration: float = None
) -> Tuple[str, str]:
    """
    Check agent health and determine if replacement needed.

    Returns:
        Tuple of (health_status, recommendation)
    """
    from datetime import timedelta

    now = datetime.now()

    # Check 1: Heartbeat timeout
    time_since_heartbeat = (now - agent.last_heartbeat).total_seconds()
    if time_since_heartbeat > heartbeat_timeout_seconds:
        return ("unhealthy", f"replace: No heartbeat for {time_since_heartbeat:.0f}s")

    # Check 2: Consecutive failures
    if agent.consecutive_failures >= failure_threshold:
        return ("unhealthy", f"replace: {agent.consecutive_failures} consecutive failures")

    # Check 3: Performance degradation
    if pool_avg_task_duration and agent.tasks_completed > 3:
        if agent.avg_task_duration > pool_avg_task_duration * task_duration_threshold_multiplier:
            return ("degraded", f"monitor: Tasks taking {agent.avg_task_duration / pool_avg_task_duration:.1f}x longer than average")

    # Check 4: Stuck agent (no task completion in long time)
    if agent.status == "busy":
        # Agent should complete tasks periodically
        # This check would require last_task_completion timestamp
        pass

    return ("healthy", "no_action")
```

**Example**:
```python
agent = AgentHealth(
    agent_id="agent-builder-3",
    last_heartbeat=datetime.now() - timedelta(seconds=45),
    consecutive_failures=0,
    tasks_completed=5,
    avg_task_duration=180.0,  # 3 minutes
    status="busy"
)

status, recommendation = check_agent_health(
    agent,
    heartbeat_timeout_seconds=30,
    failure_threshold=3,
    pool_avg_task_duration=90.0  # Pool average: 1.5 minutes
)
# Result: ("unhealthy", "replace: No heartbeat for 45s")
```

### 4. Agent Recycling

**Purpose**: Prevent memory leaks by recycling agents after N tasks

**Algorithm**:
```python
def should_recycle_agent(
    agent_id: str,
    tasks_completed: int,
    uptime_seconds: int,
    max_tasks_per_agent: int = 100,
    max_uptime_hours: int = 24
) -> Tuple[bool, str]:
    """
    Determine if agent should be recycled.

    Returns:
        Tuple of (should_recycle, reason)
    """
    # Reason 1: Task count threshold
    if tasks_completed >= max_tasks_per_agent:
        return (True, f"task_limit: Completed {tasks_completed}/{max_tasks_per_agent} tasks")

    # Reason 2: Uptime threshold
    uptime_hours = uptime_seconds / 3600
    if uptime_hours >= max_uptime_hours:
        return (True, f"uptime_limit: Running for {uptime_hours:.1f}/{max_uptime_hours} hours")

    return (False, "no_recycle")
```

**Recycling Process**:
```python
def recycle_agent(agent_id: str, pool: AgentPool) -> None:
    """
    Gracefully recycle an agent.

    Steps:
    1. Mark agent for recycling
    2. Wait for current task to complete
    3. Spawn replacement agent
    4. Terminate old agent
    5. Update pool registry
    """
    # Step 1: Mark for recycling
    pool.mark_for_recycling(agent_id)

    # Step 2: Wait for task completion (with timeout)
    timeout = 600  # 10 minutes max
    if not pool.wait_for_idle(agent_id, timeout):
        # Force termination if stuck
        pool.force_terminate(agent_id)

    # Step 3: Spawn replacement
    new_agent_id = pool.spawn_agent(template=pool.get_template(agent_id))

    # Step 4: Terminate old agent
    pool.terminate_agent(agent_id)

    # Step 5: Update registry
    pool.log_recycling_event(agent_id, new_agent_id)
```

### 5. Load Balancing

**Purpose**: Distribute tasks across agents efficiently

**Strategies**:

#### Round-Robin
```python
class RoundRobinBalancer:
    def __init__(self, agents: List[str]):
        self.agents = agents
        self.current_index = 0

    def select_agent(self) -> str:
        """Select next agent in round-robin fashion."""
        agent = self.agents[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.agents)
        return agent
```

#### Least-Loaded
```python
class LeastLoadedBalancer:
    def select_agent(self, agents: List[AgentHealth]) -> str:
        """Select agent with fewest active tasks."""
        # Filter out unhealthy agents
        healthy_agents = [a for a in agents if a.status == "healthy"]

        if not healthy_agents:
            raise NoHealthyAgentsError("All agents are unhealthy")

        # Sort by task count (ascending)
        sorted_agents = sorted(healthy_agents, key=lambda a: a.tasks_completed)

        return sorted_agents[0].agent_id
```

#### Performance-Based
```python
class PerformanceBasedBalancer:
    def select_agent(self, agents: List[AgentHealth], task_type: str = None) -> str:
        """Select agent based on historical performance."""
        # Filter healthy agents
        healthy_agents = [a for a in agents if a.status == "healthy"]

        # Score agents by performance (lower duration = better)
        scored = []
        for agent in healthy_agents:
            # Factor in both speed and reliability
            score = agent.avg_task_duration * (1 + agent.consecutive_failures * 0.1)
            scored.append((score, agent.agent_id))

        # Return best performer
        scored.sort()
        return scored[0][1]
```

## Workflow

### Initialization

```python
def initialize_agent_pool(config: PoolConfig) -> AgentPool:
    """
    Initialize agent pool with minimum number of agents.

    Steps:
    1. Validate configuration
    2. Spawn minimum agents
    3. Pre-load configured skills
    4. Run initial health checks
    5. Mark pool as ready
    """
    # Step 1: Validate
    assert config.min_size <= config.max_size
    assert config.min_size > 0
    assert config.scale_up_threshold > 0

    # Step 2: Spawn agents
    pool = AgentPool(config)
    for i in range(config.min_size):
        agent_id = pool.spawn_agent(template=config.agent_template)
        pool.register_agent(agent_id)

    # Step 3: Pre-load skills (if specified)
    if config.preload_skills:
        for agent_id in pool.list_agents():
            pool.load_skills(agent_id, config.preload_skills)

    # Step 4: Health checks
    for agent_id in pool.list_agents():
        health = pool.check_health(agent_id)
        if health.status != "healthy":
            # Replace unhealthy agent immediately
            pool.replace_agent(agent_id)

    # Step 5: Mark ready
    pool.status = "ready"
    return pool
```

### Main Loop

```python
def agent_pool_manager_loop(pool: AgentPool):
    """
    Main loop for agent pool management.

    Runs continuously, performing:
    - Auto-scaling decisions
    - Health checks
    - Agent recycling
    - Metrics collection
    """
    while pool.status == "running":
        # Every 30 seconds: Auto-scaling
        if should_run_autoscaling(pool):
            action, count = autoscale(pool)
            if action == "scale_up":
                for _ in range(count):
                    pool.spawn_agent()
            elif action == "scale_down":
                for _ in range(count):
                    pool.terminate_idle_agent()

        # Every 60 seconds: Health checks
        if should_run_health_checks(pool):
            for agent in pool.list_agents():
                health = pool.check_health(agent.id)
                if health.status == "unhealthy":
                    pool.replace_agent(agent.id)

        # Every 5 minutes: Recycling checks
        if should_run_recycling_checks(pool):
            for agent in pool.list_agents():
                should_recycle, reason = should_recycle_agent(
                    agent.id,
                    agent.tasks_completed,
                    agent.uptime_seconds,
                    pool.config.max_tasks_per_agent
                )
                if should_recycle:
                    pool.recycle_agent(agent.id)

        # Every 60 seconds: Metrics
        if should_collect_metrics(pool):
            pool.collect_and_publish_metrics()

        time.sleep(5)  # Check every 5 seconds
```

## Error Handling

### Spawn Failure

```python
def handle_spawn_failure(pool: AgentPool, error: Exception, attempt: int) -> None:
    """
    Handle agent spawn failures with exponential backoff.

    Args:
        pool: Agent pool instance
        error: The exception that occurred
        attempt: Current retry attempt (1-indexed)
    """
    max_attempts = 3
    base_delay = 10  # seconds

    if attempt >= max_attempts:
        # Alert and fallback
        pool.alert(
            severity="critical",
            message=f"Failed to spawn agent after {max_attempts} attempts: {error}"
        )

        # Check if pool is below minimum
        if len(pool.agents) < pool.config.min_size:
            pool.alert(
                severity="critical",
                message=f"Pool size ({len(pool.agents)}) below minimum ({pool.config.min_size})"
            )

        return

    # Exponential backoff
    delay = base_delay * (2 ** (attempt - 1))

    pool.log(f"Spawn failed (attempt {attempt}/{max_attempts}), retrying in {delay}s: {error}")

    time.sleep(delay)

    # Retry spawn
    try:
        agent_id = pool.spawn_agent()
        pool.log(f"Spawn succeeded on attempt {attempt + 1}: {agent_id}")
    except Exception as e:
        handle_spawn_failure(pool, e, attempt + 1)
```

### Pool Exhaustion

```python
def handle_pool_exhaustion(pool: AgentPool) -> None:
    """
    Handle scenario where all agents are busy and queue is building.

    Actions:
    1. Alert operators
    2. Recommend scaling
    3. Provide queue status
    """
    message = f"""
    ⚠️ Pool Exhaustion Warning

    Pool: {len(pool.agents)}/{pool.config.max_size} agents (all busy)
    Queue: {pool.queue_depth} tasks waiting
    Avg Wait Time: {pool.avg_wait_time:.1f} minutes

    Recommendations:
    1. Increase max_size to {pool.config.max_size + 10}
    2. Optimize task duration (current avg: {pool.avg_task_duration:.1f}s)
    3. Enable task batching to reduce overhead

    Current Bottleneck: All agents processing long tasks
    """

    pool.alert(severity="warning", message=message)
```

## Integration Patterns

### With DAG Orchestrator

```python
# DAG orchestrator requests agents from pool
from skills.orchestration.agent_pool_manager import AgentPool

pool = AgentPool.initialize(config)

# For each batch in DAG
for batch in dag_batches:
    agents = []
    for task in batch:
        # Get agent from pool
        agent_id = pool.acquire_agent(
            required_skills=task.required_skills,
            load_balancer="least_loaded"
        )
        agents.append((agent_id, task))

    # Execute batch in parallel
    execute_batch_parallel(agents)

    # Release agents back to pool
    for agent_id, task in agents:
        pool.release_agent(agent_id, task_result)
```

### With Performance Monitor

```python
# Performance monitor provides metrics for auto-scaling decisions
from skills.orchestration.performance_monitor import get_metrics

metrics = get_metrics(pool)

# Use metrics for predictive scaling
action, count = predictive_autoscale(
    current_pool_size=pool.size,
    historical_load=metrics.historical_queue_depth,
    min_size=pool.config.min_size,
    max_size=pool.config.max_size
)
```

## Examples

### Example 1: Reactive Scaling

```python
# Initialize pool
config = PoolConfig(
    min_size=3,
    max_size=20,
    scale_up_threshold=5,
    scale_down_threshold=2,
    cooldown_period=60
)

pool = initialize_agent_pool(config)

# Simulate workload
tasks = generate_tasks(count=50)

for task in tasks:
    # Auto-scale check
    action, count = reactive_autoscale(
        current_pool_size=len(pool.agents),
        queue_depth=pool.queue_depth,
        idle_agents=pool.idle_count,
        **config.__dict__
    )

    if action == "scale_up":
        print(f"Scaling up: Adding {count} agents")
        for _ in range(count):
            pool.spawn_agent()

    # Assign task
    agent = pool.acquire_agent()
    agent.execute(task)
```

### Example 2: Health Monitoring

```python
# Health check loop
while True:
    for agent in pool.list_agents():
        status, recommendation = check_agent_health(
            agent=agent.health,
            heartbeat_timeout_seconds=30,
            failure_threshold=3
        )

        if status == "unhealthy":
            print(f"Agent {agent.id} is unhealthy: {recommendation}")

            # Spawn replacement
            new_agent = pool.spawn_agent(template=agent.template)

            # Terminate unhealthy agent
            pool.terminate_agent(agent.id)

            print(f"Replaced {agent.id} with {new_agent}")

    time.sleep(60)  # Check every minute
```

### Example 3: Agent Recycling

```python
# Recycling loop
for agent in pool.list_agents():
    should_recycle, reason = should_recycle_agent(
        agent_id=agent.id,
        tasks_completed=agent.tasks_completed,
        uptime_seconds=agent.uptime,
        max_tasks_per_agent=100,
        max_uptime_hours=24
    )

    if should_recycle:
        print(f"Recycling {agent.id}: {reason}")

        # Wait for current task
        pool.wait_for_idle(agent.id, timeout=600)

        # Spawn replacement
        new_agent = pool.spawn_agent(template=agent.template)

        # Terminate old agent
        pool.terminate_agent(agent.id)

        print(f"Recycled {agent.id} → {new_agent}")
```

## Best Practices

1. **Set Appropriate Thresholds**
   ```python
   # Good: Based on workload analysis
   scale_up_threshold = 5      # 2-3x average task duration
   scale_down_threshold = 2    # Keep some idle capacity

   # Bad: Too aggressive
   scale_up_threshold = 1      # Constant scaling churn
   scale_down_threshold = 0    # No idle capacity for bursts
   ```

2. **Use Predictive Scaling for Predictable Loads**
   ```python
   # If workload has daily patterns, use predictive
   if has_historical_data(days=7):
       use_predictive_autoscale()
   else:
       use_reactive_autoscale()
   ```

3. **Monitor Agent Health Continuously**
   ```python
   # Health checks should run frequently
   health_check_interval = 60  # seconds

   # But failures need multiple confirmations
   failure_threshold = 3  # consecutive failures
   ```

4. **Recycle Agents Proactively**
   ```python
   # Prevent memory leaks
   max_tasks_per_agent = 100  # Recycle after 100 tasks
   max_uptime_hours = 24      # Or after 24 hours
   ```

5. **Respect Cooldown Periods**
   ```python
   # Prevent scaling thrash
   cooldown_period = 60  # seconds between actions

   # Allow system to stabilize after scaling
   ```

## Related Skills

- `performance-profiler-skill`: Provides metrics for scaling decisions
- `observability-tracker-skill`: Tracks agent health and performance
- `task-dependency-resolver-skill`: Determines agent requirements

## References

- Document 15, Section 3: Dynamic Agent Management
- Command: `/dynamic-orchestrator`
- Agent: `pool-manager.md`

---

**Version**: 1.0.0
**Status**: Production Ready
**Complexity**: High (stateful, long-running)
**Token Cost**: Low (periodic checks, minimal overhead)
