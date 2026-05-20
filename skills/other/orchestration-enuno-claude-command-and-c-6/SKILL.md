---
name: performance-profiler-skill
description: Analyzes token usage, execution time, and workflow bottlenecks to optimize performance and reduce costs
version: 1.0.0
tags: [orchestration, performance, profiling, optimization, cost-analysis]
---

# Performance Profiler Skill

## Purpose

This skill provides comprehensive performance analysis for multi-agent workflows, including token usage tracking, execution time profiling, bottleneck detection, and cost optimization recommendations.

## When to Use This Skill

**Use this skill when:**
- ✅ Optimizing multi-agent workflow performance
- ✅ Reducing token usage and costs
- ✅ Identifying bottlenecks in execution
- ✅ Analyzing workflow efficiency
- ✅ Meeting performance SLAs

**Don't use this skill for:**
- ❌ Simple, one-off tasks
- ❌ Workflows already optimized
- ❌ Real-time critical operations (profiling adds overhead)
- ❌ Tasks where cost is not a concern

## Core Metrics

### 1. Token Usage Analysis

```python
from dataclasses import dataclass, field
from typing import Dict, List
import time

@dataclass
class TokenUsage:
    """Track token usage for a workflow or agent."""
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0

    @property
    def total_tokens(self) -> int:
        """Total tokens used."""
        return self.input_tokens + self.output_tokens

    @property
    def cost_usd(self) -> float:
        """Estimated cost in USD (Claude Sonnet 4 pricing)."""
        # Pricing as of 2026-01
        input_cost = (self.input_tokens / 1_000_000) * 3.00   # $3 per MTok
        output_cost = (self.output_tokens / 1_000_000) * 15.00  # $15 per MTok

        return input_cost + output_cost

    def merge(self, other: 'TokenUsage') -> 'TokenUsage':
        """Merge token usage from another source."""
        return TokenUsage(
            input_tokens=self.input_tokens + other.input_tokens,
            output_tokens=self.output_tokens + other.output_tokens,
            cached_tokens=self.cached_tokens + other.cached_tokens
        )

class TokenProfiler:
    """Profile token usage across workflow."""

    def __init__(self):
        self.usage_by_agent: Dict[str, TokenUsage] = {}
        self.usage_by_task: Dict[str, TokenUsage] = {}
        self.total_usage = TokenUsage()

    def record_agent_usage(self, agent_id: str, input_tokens: int, output_tokens: int) -> None:
        """Record token usage for an agent."""
        if agent_id not in self.usage_by_agent:
            self.usage_by_agent[agent_id] = TokenUsage()

        self.usage_by_agent[agent_id].input_tokens += input_tokens
        self.usage_by_agent[agent_id].output_tokens += output_tokens

        self.total_usage.input_tokens += input_tokens
        self.total_usage.output_tokens += output_tokens

    def record_task_usage(self, task_id: str, input_tokens: int, output_tokens: int) -> None:
        """Record token usage for a task."""
        if task_id not in self.usage_by_task:
            self.usage_by_task[task_id] = TokenUsage()

        self.usage_by_task[task_id].input_tokens += input_tokens
        self.usage_by_task[task_id].output_tokens += output_tokens

    def get_top_consumers(self, limit: int = 5) -> List[tuple]:
        """Get top token-consuming agents."""
        sorted_agents = sorted(
            self.usage_by_agent.items(),
            key=lambda x: x[1].total_tokens,
            reverse=True
        )
        return sorted_agents[:limit]

    def get_cost_breakdown(self) -> Dict:
        """Get detailed cost breakdown."""
        return {
            "total_cost": self.total_usage.cost_usd,
            "total_tokens": self.total_usage.total_tokens,
            "by_agent": {
                agent_id: {
                    "tokens": usage.total_tokens,
                    "cost": usage.cost_usd
                }
                for agent_id, usage in self.usage_by_agent.items()
            },
            "by_task": {
                task_id: {
                    "tokens": usage.total_tokens,
                    "cost": usage.cost_usd
                }
                for task_id, usage in self.usage_by_task.items()
            }
        }
```

### 2. Execution Time Profiling

```python
@dataclass
class ExecutionProfile:
    """Profile execution time for tasks."""
    task_id: str
    start_time: float
    end_time: Optional[float] = None
    duration: Optional[float] = None
    agent_id: Optional[str] = None
    status: str = "running"

    def complete(self) -> None:
        """Mark task as complete and calculate duration."""
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.status = "completed"

class TimeProfiler:
    """Profile execution time across workflow."""

    def __init__(self):
        self.profiles: Dict[str, ExecutionProfile] = {}
        self.workflow_start: float = time.time()
        self.workflow_end: Optional[float] = None

    def start_task(self, task_id: str, agent_id: str = None) -> None:
        """Start timing a task."""
        self.profiles[task_id] = ExecutionProfile(
            task_id=task_id,
            start_time=time.time(),
            agent_id=agent_id
        )

    def complete_task(self, task_id: str) -> None:
        """Complete task timing."""
        if task_id in self.profiles:
            self.profiles[task_id].complete()

    def complete_workflow(self) -> None:
        """Complete workflow timing."""
        self.workflow_end = time.time()

    def get_workflow_duration(self) -> float:
        """Get total workflow duration."""
        end = self.workflow_end or time.time()
        return end - self.workflow_start

    def get_slowest_tasks(self, limit: int = 5) -> List[ExecutionProfile]:
        """Get slowest tasks."""
        completed = [p for p in self.profiles.values() if p.duration is not None]
        sorted_tasks = sorted(completed, key=lambda p: p.duration, reverse=True)
        return sorted_tasks[:limit]

    def get_agent_total_time(self, agent_id: str) -> float:
        """Get total execution time for an agent."""
        agent_profiles = [
            p for p in self.profiles.values()
            if p.agent_id == agent_id and p.duration is not None
        ]
        return sum(p.duration for p in agent_profiles)

    def get_parallelization_efficiency(self) -> float:
        """
        Calculate parallelization efficiency.

        Efficiency = Sequential Time / (Parallel Time * Agent Count)
        """
        total_task_time = sum(
            p.duration for p in self.profiles.values()
            if p.duration is not None
        )
        workflow_time = self.get_workflow_duration()
        num_agents = len(set(p.agent_id for p in self.profiles.values() if p.agent_id))

        if workflow_time == 0 or num_agents == 0:
            return 0.0

        return total_task_time / (workflow_time * num_agents)
```

### 3. Bottleneck Detection

```python
@dataclass
class Bottleneck:
    """Represents a detected bottleneck."""
    type: str  # "slow_task", "blocked_task", "high_token_usage", "agent_idle"
    severity: str  # "critical", "warning", "info"
    description: str
    recommendation: str
    impact: str

class BottleneckDetector:
    """Detect performance bottlenecks in workflows."""

    def __init__(
        self,
        slow_task_threshold_multiplier: float = 2.0,
        idle_threshold_seconds: float = 60.0
    ):
        self.slow_task_threshold_multiplier = slow_task_threshold_multiplier
        self.idle_threshold_seconds = idle_threshold_seconds

    def detect_slow_tasks(
        self,
        time_profiler: TimeProfiler,
        avg_duration: float
    ) -> List[Bottleneck]:
        """Detect tasks taking significantly longer than average."""
        bottlenecks = []
        threshold = avg_duration * self.slow_task_threshold_multiplier

        for profile in time_profiler.profiles.values():
            if profile.duration and profile.duration > threshold:
                bottlenecks.append(Bottleneck(
                    type="slow_task",
                    severity="warning" if profile.duration < threshold * 1.5 else "critical",
                    description=f"Task {profile.task_id} took {profile.duration:.1f}s (avg: {avg_duration:.1f}s)",
                    recommendation=f"Investigate task {profile.task_id} for optimization opportunities",
                    impact=f"Adds {profile.duration - avg_duration:.1f}s to workflow"
                ))

        return bottlenecks

    def detect_high_token_tasks(
        self,
        token_profiler: TokenProfiler,
        avg_tokens: int
    ) -> List[Bottleneck]:
        """Detect tasks using significantly more tokens than average."""
        bottlenecks = []
        threshold = avg_tokens * 2.0

        for task_id, usage in token_profiler.usage_by_task.items():
            if usage.total_tokens > threshold:
                bottlenecks.append(Bottleneck(
                    type="high_token_usage",
                    severity="warning",
                    description=f"Task {task_id} used {usage.total_tokens:,} tokens (avg: {avg_tokens:,})",
                    recommendation="Consider caching, reducing context, or optimizing prompts",
                    impact=f"Extra cost: ${usage.cost_usd - (avg_tokens / 1_000_000 * 15):.2f}"
                ))

        return bottlenecks

    def detect_idle_agents(
        self,
        time_profiler: TimeProfiler,
        agent_ids: List[str]
    ) -> List[Bottleneck]:
        """Detect agents that are idle for significant time."""
        bottlenecks = []
        workflow_duration = time_profiler.get_workflow_duration()

        for agent_id in agent_ids:
            agent_active_time = time_profiler.get_agent_total_time(agent_id)
            idle_time = workflow_duration - agent_active_time

            if idle_time > self.idle_threshold_seconds:
                idle_percentage = (idle_time / workflow_duration) * 100

                bottlenecks.append(Bottleneck(
                    type="agent_idle",
                    severity="info" if idle_percentage < 50 else "warning",
                    description=f"Agent {agent_id} idle for {idle_time:.1f}s ({idle_percentage:.1f}%)",
                    recommendation="Consider scaling down agents or redistributing work",
                    impact=f"Wasted capacity: {idle_percentage:.1f}%"
                ))

        return bottlenecks
```

## Workflow

### Step 1: Initialize Profilers

```python
# Create profilers
token_profiler = TokenProfiler()
time_profiler = TimeProfiler()
bottleneck_detector = BottleneckDetector()
```

### Step 2: Instrument Workflow

```python
# Start workflow timing
time_profiler.workflow_start = time.time()

for task in tasks:
    # Start task timing
    time_profiler.start_task(task.id, agent_id=task.agent_id)

    # Execute task
    result = execute_task(task)

    # Record token usage
    token_profiler.record_task_usage(
        task.id,
        input_tokens=result.usage.input_tokens,
        output_tokens=result.usage.output_tokens
    )
    token_profiler.record_agent_usage(
        task.agent_id,
        input_tokens=result.usage.input_tokens,
        output_tokens=result.usage.output_tokens
    )

    # Complete task timing
    time_profiler.complete_task(task.id)

# Complete workflow timing
time_profiler.complete_workflow()
```

### Step 3: Analyze Performance

```python
# Calculate averages
avg_duration = sum(
    p.duration for p in time_profiler.profiles.values() if p.duration
) / len(time_profiler.profiles)

avg_tokens = token_profiler.total_usage.total_tokens / len(tasks)

# Detect bottlenecks
bottlenecks = []
bottlenecks.extend(bottleneck_detector.detect_slow_tasks(time_profiler, avg_duration))
bottlenecks.extend(bottleneck_detector.detect_high_token_tasks(token_profiler, avg_tokens))
bottlenecks.extend(bottleneck_detector.detect_idle_agents(time_profiler, agent_ids))
```

### Step 4: Generate Report

```python
def generate_performance_report(
    token_profiler: TokenProfiler,
    time_profiler: TimeProfiler,
    bottlenecks: List[Bottleneck]
) -> str:
    """Generate comprehensive performance report."""

    report = []
    report.append("Performance Analysis Report")
    report.append("=" * 60)

    # Workflow Summary
    report.append("\nWorkflow Summary:")
    report.append(f"  Total Duration: {time_profiler.get_workflow_duration():.1f}s")
    report.append(f"  Total Tasks: {len(time_profiler.profiles)}")
    report.append(f"  Total Tokens: {token_profiler.total_usage.total_tokens:,}")
    report.append(f"  Total Cost: ${token_profiler.total_usage.cost_usd:.2f}")

    # Token Usage Breakdown
    report.append("\nTop Token Consumers:")
    for agent_id, usage in token_profiler.get_top_consumers():
        report.append(f"  {agent_id}: {usage.total_tokens:,} tokens (${usage.cost_usd:.2f})")

    # Execution Time Breakdown
    report.append("\nSlowest Tasks:")
    for profile in time_profiler.get_slowest_tasks():
        report.append(f"  {profile.task_id}: {profile.duration:.1f}s")

    # Bottlenecks
    if bottlenecks:
        report.append("\nBottlenecks Detected:")
        for bottleneck in sorted(bottlenecks, key=lambda b: b.severity, reverse=True):
            severity_icon = "🔴" if bottleneck.severity == "critical" else "🟡" if bottleneck.severity == "warning" else "ℹ️"
            report.append(f"\n{severity_icon} {bottleneck.type.upper()}")
            report.append(f"  {bottleneck.description}")
            report.append(f"  Impact: {bottleneck.impact}")
            report.append(f"  Recommendation: {bottleneck.recommendation}")

    # Efficiency Metrics
    efficiency = time_profiler.get_parallelization_efficiency()
    report.append(f"\nParallelization Efficiency: {efficiency:.1%}")

    return "\n".join(report)
```

## Optimization Recommendations

### 1. Token Optimization

```python
class TokenOptimizer:
    """Analyze and recommend token optimizations."""

    @staticmethod
    def analyze_repetition(context_history: List[str]) -> dict:
        """Detect repeated context across tasks."""
        from collections import Counter

        # Count repeated phrases (simplified)
        all_text = " ".join(context_history)
        words = all_text.split()
        word_counts = Counter(words)

        # Find highly repeated content
        repeated = {word: count for word, count in word_counts.items() if count > 10}

        return {
            "repeated_words": len(repeated),
            "total_repetitions": sum(repeated.values()),
            "recommendation": "Consider caching repeated context" if repeated else "No significant repetition"
        }

    @staticmethod
    def suggest_caching(token_profiler: TokenProfiler) -> List[str]:
        """Suggest which contexts to cache."""
        suggestions = []

        # Tasks with high token usage
        for task_id, usage in token_profiler.usage_by_task.items():
            if usage.input_tokens > 50000:  # > 50K input tokens
                suggestions.append(
                    f"Cache context for {task_id} (input: {usage.input_tokens:,} tokens)"
                )

        return suggestions

    @staticmethod
    def suggest_model_downgrade(token_profiler: TokenProfiler) -> dict:
        """Suggest using smaller models for simple tasks."""
        suggestions = {}

        # Tasks with low output tokens may not need Opus/Sonnet
        for task_id, usage in token_profiler.usage_by_task.items():
            if usage.output_tokens < 500:  # Low output, possibly simple task
                # Estimate savings (Sonnet → Haiku)
                sonnet_cost = usage.cost_usd
                haiku_input_cost = (usage.input_tokens / 1_000_000) * 0.80  # $0.80 per MTok
                haiku_output_cost = (usage.output_tokens / 1_000_000) * 4.00  # $4 per MTok
                haiku_cost = haiku_input_cost + haiku_output_cost

                savings = sonnet_cost - haiku_cost

                if savings > 0.01:  # More than 1 cent savings
                    suggestions[task_id] = {
                        "current_cost": sonnet_cost,
                        "haiku_cost": haiku_cost,
                        "savings": savings
                    }

        return suggestions
```

### 2. Execution Optimization

```python
class ExecutionOptimizer:
    """Analyze and recommend execution optimizations."""

    @staticmethod
    def suggest_parallelization(
        time_profiler: TimeProfiler,
        task_dependencies: Dict[str, List[str]]
    ) -> List[str]:
        """Suggest tasks that could be parallelized."""
        suggestions = []

        # Find tasks with no dependencies
        independent_tasks = [
            task_id for task_id in time_profiler.profiles.keys()
            if not task_dependencies.get(task_id, [])
        ]

        if len(independent_tasks) > 1:
            total_time = sum(
                time_profiler.profiles[tid].duration
                for tid in independent_tasks
                if time_profiler.profiles[tid].duration
            )
            parallel_time = max(
                time_profiler.profiles[tid].duration
                for tid in independent_tasks
                if time_profiler.profiles[tid].duration
            )
            savings = total_time - parallel_time

            suggestions.append(
                f"Parallelize {len(independent_tasks)} independent tasks "
                f"(estimated time savings: {savings:.1f}s)"
            )

        return suggestions

    @staticmethod
    def suggest_batching(time_profiler: TimeProfiler) -> List[str]:
        """Suggest batching small tasks."""
        suggestions = []

        # Find many small tasks (< 5 seconds each)
        small_tasks = [
            p for p in time_profiler.profiles.values()
            if p.duration and p.duration < 5.0
        ]

        if len(small_tasks) > 5:
            total_overhead = len(small_tasks) * 2.0  # Assume 2s overhead per task
            suggestions.append(
                f"Batch {len(small_tasks)} small tasks to reduce overhead "
                f"(estimated savings: {total_overhead:.1f}s)"
            )

        return suggestions
```

## Integration with Performance Monitor

```python
# Performance Monitor Agent uses this skill
from skills.orchestration.performance_profiler import (
    TokenProfiler,
    TimeProfiler,
    BottleneckDetector,
    TokenOptimizer,
    ExecutionOptimizer
)

class PerformanceMonitorAgent:
    def __init__(self):
        self.token_profiler = TokenProfiler()
        self.time_profiler = TimeProfiler()
        self.bottleneck_detector = BottleneckDetector()

    def analyze_workflow(self, workflow_results):
        """Analyze completed workflow."""

        # Detect bottlenecks
        avg_duration = calculate_avg_duration(workflow_results)
        avg_tokens = calculate_avg_tokens(workflow_results)

        bottlenecks = []
        bottlenecks.extend(
            self.bottleneck_detector.detect_slow_tasks(self.time_profiler, avg_duration)
        )
        bottlenecks.extend(
            self.bottleneck_detector.detect_high_token_tasks(self.token_profiler, avg_tokens)
        )

        # Generate optimization recommendations
        token_opts = TokenOptimizer.suggest_caching(self.token_profiler)
        exec_opts = ExecutionOptimizer.suggest_parallelization(
            self.time_profiler,
            workflow_results.dependencies
        )

        # Generate report
        report = generate_performance_report(
            self.token_profiler,
            self.time_profiler,
            bottlenecks
        )

        return {
            "report": report,
            "bottlenecks": bottlenecks,
            "optimizations": {
                "token": token_opts,
                "execution": exec_opts
            }
        }
```

## Best Practices

1. **Profile Continuously**
   ```python
   # Always profile workflows to track performance over time
   profiler = TokenProfiler()
   # ... record usage throughout workflow
   save_metrics_to_database(profiler.get_cost_breakdown())
   ```

2. **Set Budgets**
   ```python
   TOKEN_BUDGET = 1_000_000  # 1M tokens max
   COST_BUDGET = 10.00       # $10 max

   if token_profiler.total_usage.total_tokens > TOKEN_BUDGET:
       raise BudgetExceededError("Token budget exceeded")

   if token_profiler.total_usage.cost_usd > COST_BUDGET:
       raise BudgetExceededError("Cost budget exceeded")
   ```

3. **Monitor Trends**
   ```python
   # Track metrics over time
   metrics_history.append({
       "timestamp": time.time(),
       "total_tokens": token_profiler.total_usage.total_tokens,
       "total_cost": token_profiler.total_usage.cost_usd,
       "duration": time_profiler.get_workflow_duration()
   })

   # Detect regressions
   if metrics_history[-1]["total_tokens"] > metrics_history[-2]["total_tokens"] * 1.2:
       alert("Token usage increased by >20%")
   ```

4. **Optimize Based on Data**
   ```python
   # Don't guess - use profiling data
   bottlenecks = detect_bottlenecks(profiler)
   for bottleneck in sorted(bottlenecks, key=lambda b: b.impact):
       apply_optimization(bottleneck.recommendation)
   ```

## Related Skills

- `observability-tracker-skill`: Detailed tracing and metrics
- `agent-pool-manager-skill`: Uses profiling for scaling decisions
- `circuit-breaker-skill`: Performance degradation detection

## References

- Document 15, Section 6: Performance Optimization
- Command: `/performance-optimizer`
- Agent: `performance-monitor.md`

---

**Version**: 1.0.0
**Status**: Production Ready
**Complexity**: Medium (metric collection and analysis)
**Token Cost**: Minimal (lightweight instrumentation)
