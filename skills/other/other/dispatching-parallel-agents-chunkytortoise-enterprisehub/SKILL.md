---
name: Dispatching Parallel Agents
description: This skill should be used when managing "concurrent agent execution", "parallel task processing", "load balancing across agents", "resource optimization", "high-throughput workflows", or when orchestrating multiple agents working simultaneously on different aspects of complex projects.
version: 1.0.0
---

# Dispatching Parallel Agents: Concurrent Workflow Management

## Overview

This skill provides sophisticated patterns for dispatching and managing multiple agents working in parallel, optimizing resource utilization, balancing workloads, and ensuring efficient coordination of concurrent workflows.

## When to Use This Skill

Use this skill when implementing:
- **High-throughput parallel processing** with multiple agents
- **Load balancing and resource optimization** across agent pools
- **Concurrent task execution** with dependency management
- **Dynamic agent scaling** based on workload
- **Priority-based task dispatching** with queue management
- **Fault-tolerant parallel workflows** with failover mechanisms
- **Performance optimization** through parallel execution

## Core Parallel Orchestration System

### 1. Agent Pool Management

```python
"""
Advanced agent pool management with load balancing and scaling
"""

import asyncio
import heapq
import time
from typing import Dict, List, Optional, Set, Callable, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import logging
import threading
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import psutil
import queue
import statistics


class LoadBalancingStrategy(Enum):
    """Strategies for load balancing tasks across agents."""
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    WEIGHTED_ROUND_ROBIN = "weighted_round_robin"
    CAPABILITY_BASED = "capability_based"
    PERFORMANCE_BASED = "performance_based"
    PRIORITY_BASED = "priority_based"
    GEOGRAPHIC = "geographic"
    RESOURCE_AWARE = "resource_aware"


class ScalingPolicy(Enum):
    """Policies for scaling agent pools."""
    STATIC = "static"                    # Fixed pool size
    REACTIVE = "reactive"                # Scale based on queue length
    PREDICTIVE = "predictive"            # Scale based on predicted load
    TIME_BASED = "time_based"           # Scale based on time patterns
    RESOURCE_BASED = "resource_based"   # Scale based on resource usage
    HYBRID = "hybrid"                   # Combination of strategies


class AgentHealthStatus(Enum):
    """Health status of agents."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    RECOVERING = "recovering"
    OFFLINE = "offline"


@dataclass
class AgentMetrics:
    """Performance metrics for an agent."""
    agent_id: str
    tasks_completed: int = 0
    tasks_failed: int = 0
    total_execution_time: float = 0.0
    average_execution_time: float = 0.0
    current_load: float = 0.0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    error_rate: float = 0.0
    last_activity: Optional[float] = None
    health_score: float = 1.0
    throughput: float = 0.0  # tasks per second
    availability: float = 1.0

    def calculate_efficiency_score(self) -> float:
        """Calculate overall efficiency score for the agent."""
        if self.tasks_completed == 0:
            return 0.5  # Neutral score for new agents

        success_rate = 1.0 - self.error_rate
        load_factor = max(0.1, 1.0 - self.current_load)  # Lower load is better
        health_factor = self.health_score
        availability_factor = self.availability

        return (success_rate * 0.3 +
                load_factor * 0.25 +
                health_factor * 0.25 +
                availability_factor * 0.2)

    def update_metrics(self, execution_time: float, success: bool):
        """Update metrics after task completion."""
        self.tasks_completed += 1 if success else 0
        self.tasks_failed += 0 if success else 1

        self.total_execution_time += execution_time
        self.average_execution_time = self.total_execution_time / max(1, self.tasks_completed + self.tasks_failed)

        total_tasks = self.tasks_completed + self.tasks_failed
        self.error_rate = self.tasks_failed / max(1, total_tasks)

        self.last_activity = time.time()

        # Calculate throughput (tasks per minute)
        if self.last_activity and total_tasks > 0:
            time_since_start = self.last_activity - (self.last_activity - self.total_execution_time)
            self.throughput = total_tasks / max(1, time_since_start / 60)


@dataclass
class TaskPriority:
    """Enhanced priority system for tasks."""
    level: int  # 1-10 scale
    deadline: Optional[float] = None
    business_value: float = 1.0
    urgency_multiplier: float = 1.0

    def calculate_priority_score(self, current_time: float) -> float:
        """Calculate dynamic priority score based on current conditions."""
        base_score = self.level * self.business_value

        # Urgency factor based on deadline
        if self.deadline:
            time_remaining = self.deadline - current_time
            if time_remaining <= 0:
                urgency_factor = 10.0  # Overdue tasks get highest urgency
            else:
                # Urgency increases as deadline approaches
                urgency_factor = max(1.0, 5.0 / max(1.0, time_remaining / 3600))  # Scale by hours
        else:
            urgency_factor = 1.0

        return base_score * urgency_factor * self.urgency_multiplier


@dataclass
class PriorityTask:
    """Task with priority information for queue management."""
    id: str
    priority: TaskPriority
    payload: Any
    created_at: float = field(default_factory=time.time)
    assigned_at: Optional[float] = None
    started_at: Optional[float] = None
    dependencies: Set[str] = field(default_factory=set)
    required_capabilities: Set[str] = field(default_factory=set)
    estimated_duration: float = 3600.0  # seconds
    retry_count: int = 0
    max_retries: int = 3

    def __lt__(self, other) -> bool:
        """Priority comparison for heap queue (lower score = higher priority)."""
        current_time = time.time()
        self_score = -self.priority.calculate_priority_score(current_time)  # Negative for max-heap behavior
        other_score = -other.priority.calculate_priority_score(current_time)
        return self_score < other_score

    def can_execute(self, completed_tasks: Set[str]) -> bool:
        """Check if task dependencies are satisfied."""
        return self.dependencies.issubset(completed_tasks)

    def matches_capabilities(self, agent_capabilities: Set[str]) -> bool:
        """Check if agent has required capabilities."""
        return self.required_capabilities.issubset(agent_capabilities)


class WorkloadPredictor:
    """Predicts future workload patterns for proactive scaling."""

    def __init__(self, history_window: int = 168):  # 1 week in hours
        self.history_window = history_window
        self.task_history: deque = deque(maxlen=history_window)
        self.hourly_patterns: Dict[int, List[float]] = defaultdict(list)
        self.daily_patterns: Dict[int, List[float]] = defaultdict(list)

    def record_workload(self, timestamp: float, task_count: int):
        """Record workload data point."""
        self.task_history.append((timestamp, task_count))

        # Extract hour and day patterns
        import datetime
        dt = datetime.datetime.fromtimestamp(timestamp)
        hour_of_day = dt.hour
        day_of_week = dt.weekday()

        self.hourly_patterns[hour_of_day].append(task_count)
        self.daily_patterns[day_of_week].append(task_count)

        # Keep only recent data for patterns
        max_pattern_history = 30
        if len(self.hourly_patterns[hour_of_day]) > max_pattern_history:
            self.hourly_patterns[hour_of_day] = self.hourly_patterns[hour_of_day][-max_pattern_history:]
        if len(self.daily_patterns[day_of_week]) > max_pattern_history:
            self.daily_patterns[day_of_week] = self.daily_patterns[day_of_week][-max_pattern_history:]

    def predict_workload(self, future_timestamp: float) -> float:
        """Predict workload for a future timestamp."""
        if not self.task_history:
            return 1.0  # Default prediction

        import datetime
        dt = datetime.datetime.fromtimestamp(future_timestamp)
        hour_of_day = dt.hour
        day_of_week = dt.weekday()

        # Get historical averages
        hourly_avg = statistics.mean(self.hourly_patterns[hour_of_day]) if self.hourly_patterns[hour_of_day] else 1.0
        daily_avg = statistics.mean(self.daily_patterns[day_of_week]) if self.daily_patterns[day_of_week] else 1.0
        overall_avg = statistics.mean([count for _, count in self.task_history])

        # Weight the predictions
        return (hourly_avg * 0.4 + daily_avg * 0.4 + overall_avg * 0.2)

    def get_scaling_recommendation(self, current_agents: int, queue_length: int) -> int:
        """Get scaling recommendation based on predictions."""
        current_time = time.time()

        # Predict workload for next hour
        future_workload = self.predict_workload(current_time + 3600)

        # Calculate required agents
        avg_task_duration = 300  # 5 minutes average
        tasks_per_hour_per_agent = 3600 / avg_task_duration

        required_agents = max(1, int((future_workload + queue_length) / tasks_per_hour_per_agent))

        # Add buffer for spikes
        buffer_factor = 1.2
        recommended_agents = int(required_agents * buffer_factor)

        return max(1, min(recommended_agents, current_agents * 3))  # Cap scaling


class AgentPool:
    """Manages a pool of agents with load balancing and health monitoring."""

    def __init__(self,
                 pool_id: str,
                 initial_size: int = 3,
                 max_size: int = 10,
                 min_size: int = 1,
                 load_balancing_strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
                 scaling_policy: ScalingPolicy = ScalingPolicy.REACTIVE):

        self.pool_id = pool_id
        self.max_size = max_size
        self.min_size = min_size
        self.load_balancing_strategy = load_balancing_strategy
        self.scaling_policy = scaling_policy

        self.agents: Dict[str, Any] = {}  # agent_id -> agent instance
        self.agent_metrics: Dict[str, AgentMetrics] = {}
        self.agent_capabilities: Dict[str, Set[str]] = {}
        self.agent_health: Dict[str, AgentHealthStatus] = {}

        self.task_queue: List[PriorityTask] = []  # Priority queue
        self.running_tasks: Dict[str, PriorityTask] = {}  # task_id -> task
        self.completed_tasks: Set[str] = set()
        self.failed_tasks: Set[str] = set()

        self.workload_predictor = WorkloadPredictor()
        self.logger = logging.getLogger(f"AgentPool_{pool_id}")

        # Round robin counter
        self._round_robin_index = 0

        # Initialize with specified size
        for i in range(initial_size):
            self._create_agent(f"{pool_id}_agent_{i}")

    def add_agent(self, agent_id: str, agent_instance: Any, capabilities: Set[str]):
        """Add an agent to the pool."""
        if len(self.agents) >= self.max_size:
            raise ValueError(f"Pool at maximum size ({self.max_size})")

        self.agents[agent_id] = agent_instance
        self.agent_metrics[agent_id] = AgentMetrics(agent_id=agent_id)
        self.agent_capabilities[agent_id] = capabilities
        self.agent_health[agent_id] = AgentHealthStatus.HEALTHY

        self.logger.info(f"Added agent {agent_id} to pool {self.pool_id}")

    def remove_agent(self, agent_id: str):
        """Remove an agent from the pool."""
        if len(self.agents) <= self.min_size:
            raise ValueError(f"Pool at minimum size ({self.min_size})")

        if agent_id in self.agents:
            del self.agents[agent_id]
            del self.agent_metrics[agent_id]
            del self.agent_capabilities[agent_id]
            del self.agent_health[agent_id]

            self.logger.info(f"Removed agent {agent_id} from pool {self.pool_id}")

    def submit_task(self, task: PriorityTask):
        """Submit a task to the pool's priority queue."""
        heapq.heappush(self.task_queue, task)

        # Record workload for prediction
        self.workload_predictor.record_workload(time.time(), len(self.task_queue))

        self.logger.debug(f"Submitted task {task.id} with priority {task.priority.level}")

    def get_available_agents(self, required_capabilities: Set[str] = None) -> List[str]:
        """Get list of available agents that can handle the requirements."""
        available = []

        for agent_id, health in self.agent_health.items():
            # Check health and availability
            if health not in [AgentHealthStatus.HEALTHY, AgentHealthStatus.DEGRADED]:
                continue

            # Check if agent is not currently running tasks (simplified)
            metrics = self.agent_metrics[agent_id]
            if metrics.current_load >= 1.0:  # Assuming load 1.0 means fully occupied
                continue

            # Check capabilities
            if required_capabilities:
                if not required_capabilities.issubset(self.agent_capabilities[agent_id]):
                    continue

            available.append(agent_id)

        return available

    def select_agent(self, task: PriorityTask) -> Optional[str]:
        """Select the best agent for a task based on load balancing strategy."""
        available_agents = self.get_available_agents(task.required_capabilities)

        if not available_agents:
            return None

        if self.load_balancing_strategy == LoadBalancingStrategy.ROUND_ROBIN:
            agent_id = available_agents[self._round_robin_index % len(available_agents)]
            self._round_robin_index += 1
            return agent_id

        elif self.load_balancing_strategy == LoadBalancingStrategy.LEAST_LOADED:
            return min(available_agents,
                      key=lambda aid: self.agent_metrics[aid].current_load)

        elif self.load_balancing_strategy == LoadBalancingStrategy.PERFORMANCE_BASED:
            return max(available_agents,
                      key=lambda aid: self.agent_metrics[aid].calculate_efficiency_score())

        elif self.load_balancing_strategy == LoadBalancingStrategy.CAPABILITY_BASED:
            # Prefer agents with exact capability match
            exact_matches = [aid for aid in available_agents
                           if self.agent_capabilities[aid] == task.required_capabilities]
            if exact_matches:
                return min(exact_matches,
                          key=lambda aid: self.agent_metrics[aid].current_load)
            else:
                return min(available_agents,
                          key=lambda aid: self.agent_metrics[aid].current_load)

        elif self.load_balancing_strategy == LoadBalancingStrategy.RESOURCE_AWARE:
            def resource_score(agent_id: str) -> float:
                metrics = self.agent_metrics[agent_id]
                # Lower CPU and memory usage is better
                return -(metrics.cpu_usage + metrics.memory_usage) / 2

            return max(available_agents, key=resource_score)

        else:
            # Default to least loaded
            return min(available_agents,
                      key=lambda aid: self.agent_metrics[aid].current_load)

    async def dispatch_next_task(self) -> Optional[Tuple[str, PriorityTask]]:
        """Dispatch the next highest priority task to an available agent."""
        if not self.task_queue:
            return None

        # Find tasks that can be executed (dependencies satisfied)
        executable_tasks = []
        for task in self.task_queue:
            if task.can_execute(self.completed_tasks):
                executable_tasks.append(task)

        if not executable_tasks:
            return None

        # Get highest priority executable task
        task = min(executable_tasks, key=lambda t: t)

        # Remove from queue
        self.task_queue.remove(task)
        heapq.heapify(self.task_queue)  # Re-heapify after removal

        # Select agent
        agent_id = self.select_agent(task)
        if not agent_id:
            # No available agents, put task back in queue
            heapq.heappush(self.task_queue, task)
            return None

        # Assign task
        task.assigned_at = time.time()
        task.started_at = time.time()
        self.running_tasks[task.id] = task

        # Update agent load
        self.agent_metrics[agent_id].current_load += 0.5  # Simplified load calculation

        self.logger.info(f"Dispatched task {task.id} to agent {agent_id}")
        return agent_id, task

    async def complete_task(self, task_id: str, agent_id: str, success: bool, execution_time: float):
        """Mark a task as completed and update metrics."""
        if task_id not in self.running_tasks:
            self.logger.warning(f"Task {task_id} not found in running tasks")
            return

        task = self.running_tasks[task_id]
        del self.running_tasks[task_id]

        # Update completion tracking
        if success:
            self.completed_tasks.add(task_id)
        else:
            self.failed_tasks.add(task_id)

        # Update agent metrics
        if agent_id in self.agent_metrics:
            self.agent_metrics[agent_id].update_metrics(execution_time, success)
            self.agent_metrics[agent_id].current_load = max(0,
                self.agent_metrics[agent_id].current_load - 0.5)

        self.logger.info(f"Completed task {task_id} ({'success' if success else 'failure'}) in {execution_time:.2f}s")

    def get_pool_status(self) -> Dict[str, Any]:
        """Get comprehensive status of the agent pool."""
        healthy_agents = sum(1 for status in self.agent_health.values()
                           if status == AgentHealthStatus.HEALTHY)
        total_load = sum(metrics.current_load for metrics in self.agent_metrics.values())
        avg_load = total_load / max(1, len(self.agent_metrics))

        return {
            'pool_id': self.pool_id,
            'agent_count': len(self.agents),
            'healthy_agents': healthy_agents,
            'queue_length': len(self.task_queue),
            'running_tasks': len(self.running_tasks),
            'completed_tasks': len(self.completed_tasks),
            'failed_tasks': len(self.failed_tasks),
            'average_load': avg_load,
            'total_throughput': sum(metrics.throughput for metrics in self.agent_metrics.values()),
            'agents_by_status': {
                status.value: sum(1 for s in self.agent_health.values() if s == status)
                for status in AgentHealthStatus
            }
        }

    async def auto_scale(self):
        """Automatically scale the pool based on current conditions and predictions."""
        if self.scaling_policy == ScalingPolicy.STATIC:
            return

        current_size = len(self.agents)
        queue_length = len(self.task_queue)

        if self.scaling_policy == ScalingPolicy.REACTIVE:
            # Scale based on queue length
            if queue_length > current_size * 2 and current_size < self.max_size:
                # Scale up
                new_agent_id = f"{self.pool_id}_agent_{int(time.time())}"
                self._create_agent(new_agent_id)
                self.logger.info(f"Scaled up: added agent {new_agent_id}")

            elif queue_length == 0 and current_size > self.min_size:
                # Consider scaling down if load is consistently low
                avg_load = sum(m.current_load for m in self.agent_metrics.values()) / current_size
                if avg_load < 0.2:
                    # Find least active agent to remove
                    least_active = min(self.agent_metrics.keys(),
                                     key=lambda aid: self.agent_metrics[aid].current_load)
                    if self.agent_metrics[least_active].current_load < 0.1:
                        self.remove_agent(least_active)
                        self.logger.info(f"Scaled down: removed agent {least_active}")

        elif self.scaling_policy == ScalingPolicy.PREDICTIVE:
            # Use workload predictor
            recommended = self.workload_predictor.get_scaling_recommendation(current_size, queue_length)

            if recommended > current_size and current_size < self.max_size:
                needed = min(recommended - current_size, self.max_size - current_size)
                for i in range(needed):
                    new_agent_id = f"{self.pool_id}_agent_pred_{int(time.time())}_{i}"
                    self._create_agent(new_agent_id)

            elif recommended < current_size and current_size > self.min_size:
                excess = min(current_size - recommended, current_size - self.min_size)
                # Remove excess agents (simplified - would need more sophisticated selection)
                agents_to_remove = list(self.agents.keys())[:excess]
                for agent_id in agents_to_remove:
                    if self.agent_metrics[agent_id].current_load < 0.1:
                        self.remove_agent(agent_id)

    def _create_agent(self, agent_id: str):
        """Create a new agent and add to pool (simplified)."""
        # This would be implemented based on your specific agent creation logic
        # For now, we'll simulate with a placeholder
        mock_agent = type('MockAgent', (), {
            'agent_id': agent_id,
            'execute_task': lambda self, task: None
        })()

        # Default capabilities (would be determined by agent type)
        default_capabilities = {'general_processing', 'basic_analysis'}

        self.add_agent(agent_id, mock_agent, default_capabilities)


class ParallelDispatcher:
    """Main dispatcher for managing multiple agent pools and orchestrating parallel execution."""

    def __init__(self):
        self.pools: Dict[str, AgentPool] = {}
        self.global_task_queue: List[PriorityTask] = []
        self.cross_pool_dependencies: Dict[str, Set[str]] = {}
        self.execution_policies: Dict[str, Dict[str, Any]] = {}

        self.logger = logging.getLogger("ParallelDispatcher")

        # Performance monitoring
        self.metrics_collection_interval = 60  # seconds
        self.last_metrics_collection = time.time()

        # Task routing rules
        self.routing_rules: Dict[str, Callable[[PriorityTask], str]] = {}

    def create_pool(self,
                   pool_id: str,
                   initial_size: int = 3,
                   max_size: int = 10,
                   load_balancing_strategy: LoadBalancingStrategy = LoadBalancingStrategy.LEAST_LOADED,
                   scaling_policy: ScalingPolicy = ScalingPolicy.REACTIVE) -> AgentPool:
        """Create a new agent pool."""

        pool = AgentPool(
            pool_id=pool_id,
            initial_size=initial_size,
            max_size=max_size,
            load_balancing_strategy=load_balancing_strategy,
            scaling_policy=scaling_policy
        )

        self.pools[pool_id] = pool
        self.logger.info(f"Created agent pool: {pool_id}")
        return pool

    def add_routing_rule(self, rule_name: str, rule_function: Callable[[PriorityTask], str]):
        """Add a routing rule for directing tasks to specific pools."""
        self.routing_rules[rule_name] = rule_function

    def route_task(self, task: PriorityTask) -> str:
        """Route a task to the appropriate pool."""
        # Apply routing rules in order
        for rule_name, rule_function in self.routing_rules.items():
            try:
                pool_id = rule_function(task)
                if pool_id and pool_id in self.pools:
                    return pool_id
            except Exception as e:
                self.logger.warning(f"Routing rule {rule_name} failed: {e}")

        # Default routing: least loaded pool
        if not self.pools:
            raise ValueError("No pools available")

        return min(self.pools.keys(),
                  key=lambda pid: len(self.pools[pid].task_queue))

    async def submit_task(self, task: PriorityTask, target_pool: Optional[str] = None):
        """Submit a task for parallel processing."""
        if target_pool and target_pool not in self.pools:
            raise ValueError(f"Pool {target_pool} not found")

        # Route task to appropriate pool
        pool_id = target_pool or self.route_task(task)
        pool = self.pools[pool_id]

        # Submit to pool
        pool.submit_task(task)

        # Track cross-pool dependencies if needed
        if task.dependencies:
            self.cross_pool_dependencies[task.id] = task.dependencies

        self.logger.debug(f"Submitted task {task.id} to pool {pool_id}")

    async def dispatch_all_tasks(self, max_concurrent: Optional[int] = None):
        """Dispatch all pending tasks across all pools."""
        dispatching_tasks = []

        for pool_id, pool in self.pools.items():
            # Auto-scale pools if needed
            await pool.auto_scale()

            # Dispatch tasks from this pool
            task = self._create_dispatch_task(pool)
            dispatching_tasks.append(task)

        # Limit concurrency if specified
        if max_concurrent:
            semaphore = asyncio.Semaphore(max_concurrent)

            async def limited_dispatch(task):
                async with semaphore:
                    return await task

            dispatching_tasks = [limited_dispatch(task) for task in dispatching_tasks]

        # Execute all dispatching tasks
        results = await asyncio.gather(*dispatching_tasks, return_exceptions=True)

        # Log any exceptions
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                pool_id = list(self.pools.keys())[i]
                self.logger.error(f"Dispatching failed for pool {pool_id}: {result}")

    async def _create_dispatch_task(self, pool: AgentPool):
        """Create an async task for dispatching from a specific pool."""
        async def dispatch_from_pool():
            try:
                dispatch_result = await pool.dispatch_next_task()
                if dispatch_result:
                    agent_id, task = dispatch_result

                    # Simulate task execution (in real implementation, this would
                    # involve actual agent execution)
                    execution_time = await self._simulate_task_execution(task)

                    # Complete the task
                    await pool.complete_task(task.id, agent_id, True, execution_time)

                    return {'pool_id': pool.pool_id, 'task_id': task.id, 'agent_id': agent_id}
                return None

            except Exception as e:
                self.logger.error(f"Error dispatching from pool {pool.pool_id}: {e}")
                raise

        return asyncio.create_task(dispatch_from_pool())

    async def _simulate_task_execution(self, task: PriorityTask) -> float:
        """Simulate task execution time."""
        # Simulate variable execution time based on task characteristics
        base_time = task.estimated_duration / 10  # Scale down for simulation
        variance = base_time * 0.2  # 20% variance

        import random
        execution_time = base_time + random.uniform(-variance, variance)

        # Simulate actual work
        await asyncio.sleep(max(0.1, execution_time))

        return execution_time

    def get_global_status(self) -> Dict[str, Any]:
        """Get comprehensive status across all pools."""
        total_agents = sum(len(pool.agents) for pool in self.pools.values())
        total_queue_length = sum(len(pool.task_queue) for pool in self.pools.values())
        total_running = sum(len(pool.running_tasks) for pool in self.pools.values())
        total_completed = sum(len(pool.completed_tasks) for pool in self.pools.values())
        total_failed = sum(len(pool.failed_tasks) for pool in self.pools.values())

        pool_statuses = {pool_id: pool.get_pool_status()
                        for pool_id, pool in self.pools.items()}

        return {
            'dispatcher_id': id(self),
            'pool_count': len(self.pools),
            'total_agents': total_agents,
            'total_queue_length': total_queue_length,
            'total_running_tasks': total_running,
            'total_completed_tasks': total_completed,
            'total_failed_tasks': total_failed,
            'pool_details': pool_statuses,
            'system_load': self._get_system_load()
        }

    def _get_system_load(self) -> Dict[str, float]:
        """Get current system resource usage."""
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=1),
                'memory_percent': psutil.virtual_memory().percent,
                'disk_percent': psutil.disk_usage('/').percent
            }
        except Exception:
            return {'cpu_percent': 0.0, 'memory_percent': 0.0, 'disk_percent': 0.0}

    async def optimize_performance(self):
        """Optimize performance across all pools."""
        current_time = time.time()

        # Collect metrics periodically
        if current_time - self.last_metrics_collection > self.metrics_collection_interval:
            await self._collect_performance_metrics()
            self.last_metrics_collection = current_time

        # Balance load across pools
        await self._balance_inter_pool_load()

        # Optimize individual pools
        for pool in self.pools.values():
            await self._optimize_pool(pool)

    async def _collect_performance_metrics(self):
        """Collect detailed performance metrics."""
        for pool_id, pool in self.pools.items():
            pool_metrics = pool.get_pool_status()

            # Log performance data
            self.logger.info(f"Pool {pool_id} metrics: "
                           f"agents={pool_metrics['agent_count']}, "
                           f"queue={pool_metrics['queue_length']}, "
                           f"throughput={pool_metrics['total_throughput']:.2f}")

    async def _balance_inter_pool_load(self):
        """Balance load across different pools."""
        if len(self.pools) < 2:
            return

        # Find overloaded and underloaded pools
        pool_loads = {}
        for pool_id, pool in self.pools.items():
            status = pool.get_pool_status()
            load_ratio = status['queue_length'] / max(1, status['agent_count'])
            pool_loads[pool_id] = load_ratio

        max_load_pool = max(pool_loads.keys(), key=lambda p: pool_loads[p])
        min_load_pool = min(pool_loads.keys(), key=lambda p: pool_loads[p])

        # Move tasks if there's significant imbalance
        load_difference = pool_loads[max_load_pool] - pool_loads[min_load_pool]
        if load_difference > 2.0:  # Threshold for rebalancing
            await self._move_tasks_between_pools(max_load_pool, min_load_pool)

    async def _move_tasks_between_pools(self, source_pool_id: str, target_pool_id: str):
        """Move tasks from overloaded pool to underloaded pool."""
        source_pool = self.pools[source_pool_id]
        target_pool = self.pools[target_pool_id]

        # Move up to 25% of tasks
        tasks_to_move = len(source_pool.task_queue) // 4

        moved_tasks = []
        for _ in range(min(tasks_to_move, len(source_pool.task_queue))):
            if source_pool.task_queue:
                task = heapq.heappop(source_pool.task_queue)

                # Check if target pool can handle the task capabilities
                available_agents = target_pool.get_available_agents(task.required_capabilities)
                if available_agents:
                    target_pool.submit_task(task)
                    moved_tasks.append(task.id)
                else:
                    # Put task back if target pool can't handle it
                    heapq.heappush(source_pool.task_queue, task)

        if moved_tasks:
            self.logger.info(f"Moved {len(moved_tasks)} tasks from {source_pool_id} to {target_pool_id}")

    async def _optimize_pool(self, pool: AgentPool):
        """Optimize individual pool performance."""
        # Auto-scaling
        await pool.auto_scale()

        # Health monitoring
        await self._check_agent_health(pool)

    async def _check_agent_health(self, pool: AgentPool):
        """Monitor and update agent health status."""
        current_time = time.time()

        for agent_id, metrics in pool.agent_metrics.items():
            # Check if agent is responsive
            if metrics.last_activity and (current_time - metrics.last_activity) > 300:  # 5 minutes
                pool.agent_health[agent_id] = AgentHealthStatus.UNHEALTHY
            elif metrics.error_rate > 0.3:  # More than 30% error rate
                pool.agent_health[agent_id] = AgentHealthStatus.DEGRADED
            else:
                pool.agent_health[agent_id] = AgentHealthStatus.HEALTHY
```

## Usage Examples

### Real Estate AI Parallel Processing

```python
"""
Example: Parallel processing for real estate AI workflows
"""

async def create_real_estate_parallel_workflow():
    """Create parallel processing workflow for real estate tasks."""

    # Initialize dispatcher
    dispatcher = ParallelDispatcher()

    # Create specialized pools
    data_processing_pool = dispatcher.create_pool(
        pool_id="data_processing",
        initial_size=5,
        max_size=15,
        load_balancing_strategy=LoadBalancingStrategy.PERFORMANCE_BASED,
        scaling_policy=ScalingPolicy.PREDICTIVE
    )

    ai_analysis_pool = dispatcher.create_pool(
        pool_id="ai_analysis",
        initial_size=3,
        max_size=8,
        load_balancing_strategy=LoadBalancingStrategy.RESOURCE_AWARE,
        scaling_policy=ScalingPolicy.REACTIVE
    )

    notification_pool = dispatcher.create_pool(
        pool_id="notifications",
        initial_size=2,
        max_size=6,
        load_balancing_strategy=LoadBalancingStrategy.ROUND_ROBIN,
        scaling_policy=ScalingPolicy.STATIC
    )

    # Add routing rules
    def data_task_router(task: PriorityTask) -> str:
        if 'data_processing' in task.required_capabilities:
            return 'data_processing'
        elif 'ai_analysis' in task.required_capabilities:
            return 'ai_analysis'
        elif 'notification' in task.required_capabilities:
            return 'notifications'
        return 'data_processing'  # default

    dispatcher.add_routing_rule("capability_based", data_task_router)

    # Create sample tasks
    tasks = []

    # Property data processing tasks
    for i in range(10):
        task = PriorityTask(
            id=f"process_property_data_{i}",
            priority=TaskPriority(level=5, business_value=1.0),
            payload={
                'property_id': f'prop_{i}',
                'data_source': 'MLS',
                'processing_type': 'normalization'
            },
            required_capabilities={'data_processing'},
            estimated_duration=300  # 5 minutes
        )
        tasks.append(task)

    # AI analysis tasks
    for i in range(5):
        task = PriorityTask(
            id=f"ai_property_analysis_{i}",
            priority=TaskPriority(level=8, business_value=2.0),
            payload={
                'property_batch': [f'prop_{j}' for j in range(i*5, (i+1)*5)],
                'analysis_type': 'market_valuation',
                'model_version': 'v2.1'
            },
            required_capabilities={'ai_analysis'},
            dependencies={f'process_property_data_{j}' for j in range(i*5, (i+1)*5)},
            estimated_duration=600  # 10 minutes
        )
        tasks.append(task)

    # Lead notification tasks
    for i in range(3):
        task = PriorityTask(
            id=f"send_notifications_{i}",
            priority=TaskPriority(level=3, business_value=0.5),
            payload={
                'notification_type': 'new_matches',
                'user_segment': f'segment_{i}',
                'channel': 'email_sms'
            },
            required_capabilities={'notification'},
            estimated_duration=120  # 2 minutes
        )
        tasks.append(task)

    # Submit all tasks
    for task in tasks:
        await dispatcher.submit_task(task)

    # Execute parallel processing
    print("🚀 Starting parallel processing...")

    # Run processing loop
    processing_rounds = 10
    for round_num in range(processing_rounds):
        print(f"\n📊 Processing Round {round_num + 1}/{processing_rounds}")

        # Dispatch tasks
        await dispatcher.dispatch_all_tasks(max_concurrent=20)

        # Get status
        status = dispatcher.get_global_status()
        print(f"Active tasks: {status['total_running_tasks']}")
        print(f"Queue length: {status['total_queue_length']}")
        print(f"Completed: {status['total_completed_tasks']}")

        # Optimize performance
        await dispatcher.optimize_performance()

        # Break if no more tasks
        if status['total_queue_length'] == 0 and status['total_running_tasks'] == 0:
            break

        await asyncio.sleep(2)  # Wait between rounds

    # Final status
    final_status = dispatcher.get_global_status()
    print(f"\n✅ Processing Complete!")
    print(f"Total completed: {final_status['total_completed_tasks']}")
    print(f"Total failed: {final_status['total_failed_tasks']}")

    return final_status


async def demonstrate_load_balancing():
    """Demonstrate different load balancing strategies."""

    print("🔄 Load Balancing Strategy Comparison")

    strategies = [
        LoadBalancingStrategy.ROUND_ROBIN,
        LoadBalancingStrategy.LEAST_LOADED,
        LoadBalancingStrategy.PERFORMANCE_BASED,
        LoadBalancingStrategy.RESOURCE_AWARE
    ]

    results = {}

    for strategy in strategies:
        print(f"\n🎯 Testing {strategy.value}")

        # Create dispatcher with specific strategy
        dispatcher = ParallelDispatcher()
        pool = dispatcher.create_pool(
            pool_id=f"test_{strategy.value}",
            initial_size=4,
            max_size=8,
            load_balancing_strategy=strategy
        )

        # Create test tasks
        test_tasks = []
        for i in range(20):
            task = PriorityTask(
                id=f"test_task_{i}",
                priority=TaskPriority(level=random.randint(1, 10)),
                payload={'test_data': f'data_{i}'},
                required_capabilities={'general_processing'},
                estimated_duration=random.uniform(60, 300)
            )
            test_tasks.append(task)

        # Submit and process
        start_time = time.time()

        for task in test_tasks:
            await dispatcher.submit_task(task)

        # Process until completion
        while True:
            await dispatcher.dispatch_all_tasks()
            status = dispatcher.get_global_status()
            if status['total_queue_length'] == 0 and status['total_running_tasks'] == 0:
                break
            await asyncio.sleep(0.5)

        end_time = time.time()

        # Collect results
        final_status = dispatcher.get_global_status()
        pool_status = final_status['pool_details'][f"test_{strategy.value}"]

        results[strategy.value] = {
            'total_time': end_time - start_time,
            'throughput': pool_status['total_throughput'],
            'average_load': pool_status['average_load'],
            'completed_tasks': pool_status['completed_tasks']
        }

        print(f"  Completed in {end_time - start_time:.2f}s")
        print(f"  Throughput: {pool_status['total_throughput']:.2f} tasks/min")

    # Compare results
    print(f"\n📈 Strategy Comparison:")
    for strategy, metrics in results.items():
        print(f"  {strategy}: {metrics['total_time']:.2f}s, "
              f"throughput: {metrics['throughput']:.2f}")


# Streamlit Integration
def create_parallel_processing_dashboard():
    """Create Streamlit dashboard for monitoring parallel processing."""

    import streamlit as st

    st.title("🔄 Parallel Agent Processing Dashboard")

    # Initialize dispatcher
    if 'dispatcher' not in st.session_state:
        st.session_state.dispatcher = ParallelDispatcher()

        # Create default pools
        st.session_state.dispatcher.create_pool("processing", initial_size=3)
        st.session_state.dispatcher.create_pool("analysis", initial_size=2)

    dispatcher = st.session_state.dispatcher

    # Control Panel
    st.header("Control Panel")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Add Processing Tasks"):
            for i in range(5):
                task = PriorityTask(
                    id=f"proc_task_{int(time.time())}_{i}",
                    priority=TaskPriority(level=random.randint(1, 10)),
                    payload={'data': f'batch_{i}'},
                    required_capabilities={'data_processing'},
                    estimated_duration=random.uniform(60, 300)
                )
                asyncio.run(dispatcher.submit_task(task, 'processing'))
            st.success("Added 5 processing tasks")

    with col2:
        if st.button("Add Analysis Tasks"):
            for i in range(3):
                task = PriorityTask(
                    id=f"analysis_task_{int(time.time())}_{i}",
                    priority=TaskPriority(level=random.randint(5, 10)),
                    payload={'analysis_type': f'type_{i}'},
                    required_capabilities={'ai_analysis'},
                    estimated_duration=random.uniform(120, 600)
                )
                asyncio.run(dispatcher.submit_task(task, 'analysis'))
            st.success("Added 3 analysis tasks")

    with col3:
        if st.button("Process Tasks"):
            with st.spinner("Processing..."):
                # Run one round of processing
                asyncio.run(dispatcher.dispatch_all_tasks())
            st.success("Processing round completed")

    # Status Overview
    st.header("System Status")

    status = dispatcher.get_global_status()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Agents", status['total_agents'])
    with col2:
        st.metric("Queue Length", status['total_queue_length'])
    with col3:
        st.metric("Running Tasks", status['total_running_tasks'])
    with col4:
        st.metric("Completed", status['total_completed_tasks'])

    # Pool Details
    st.header("Pool Status")

    for pool_id, pool_status in status['pool_details'].items():
        with st.expander(f"Pool: {pool_id}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Agent Count:** {pool_status['agent_count']}")
                st.write(f"**Healthy Agents:** {pool_status['healthy_agents']}")
                st.write(f"**Queue Length:** {pool_status['queue_length']}")
                st.write(f"**Running Tasks:** {pool_status['running_tasks']}")

            with col2:
                st.write(f"**Completed:** {pool_status['completed_tasks']}")
                st.write(f"**Failed:** {pool_status['failed_tasks']}")
                st.write(f"**Average Load:** {pool_status['average_load']:.2f}")
                st.write(f"**Throughput:** {pool_status['total_throughput']:.2f} tasks/min")

            # Progress bar
            if pool_status['agent_count'] > 0:
                load_percentage = min(100, pool_status['average_load'] * 100)
                st.progress(load_percentage / 100)

    # System Resources
    st.header("System Resources")
    system_load = status['system_load']

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CPU Usage", f"{system_load['cpu_percent']:.1f}%")
    with col2:
        st.metric("Memory Usage", f"{system_load['memory_percent']:.1f}%")
    with col3:
        st.metric("Disk Usage", f"{system_load['disk_percent']:.1f}%")

    # Auto-refresh
    if st.checkbox("Auto-refresh (5s)"):
        time.sleep(5)
        st.rerun()


# Example usage
async def main():
    """Main demonstration function."""
    print("🔄 Parallel Agent Dispatching Demo")

    # Run real estate workflow
    await create_real_estate_parallel_workflow()

    print("\n" + "="*50)

    # Demonstrate load balancing
    await demonstrate_load_balancing()


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
```

## Best Practices

1. **Resource Management**: Monitor and optimize resource usage across agent pools
2. **Load Balancing**: Choose appropriate load balancing strategies based on workload characteristics
3. **Fault Tolerance**: Implement robust error handling and recovery mechanisms
4. **Monitoring**: Comprehensive monitoring of agent health and performance
5. **Scaling Policies**: Implement intelligent scaling based on workload patterns
6. **Queue Management**: Proper priority queue management with dependency handling
7. **Performance Optimization**: Regular optimization based on collected metrics

This dispatching parallel agents skill provides a comprehensive framework for managing high-throughput, concurrent agent workflows with sophisticated load balancing, scaling, and optimization capabilities specifically designed for the complex requirements of the EnterpriseHub GHL Real Estate AI project.