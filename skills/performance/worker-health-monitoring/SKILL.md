---
name: worker-health-monitoring
description: Heartbeat-based health monitoring for background workers with configurable thresholds, rolling duration windows, failure rate calculation, and stuck job detection.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: observability
  time: 5h
  source: drift-masterguide
---

# Worker Health Monitoring

Heartbeat-based health monitoring for background workers.

## When to Use This Skill

- Monitoring background job workers
- Detecting offline or stuck workers
- Tracking worker performance degradation
- Calculating failure rates and latency percentiles

## Core Concepts

Workers can fail in subtle ways:
- **Offline** - No heartbeat received
- **Degraded** - Slow or occasionally failing
- **Unhealthy** - High failure rate
- **Stuck** - Started but never completed

The solution uses heartbeats, rolling windows, and configurable thresholds.

## Implementation

### TypeScript

```typescript
enum HealthStatus {
  HEALTHY = 'healthy',
  DEGRADED = 'degraded',
  UNHEALTHY = 'unhealthy',
  OFFLINE = 'offline',
  UNKNOWN = 'unknown',
}

interface HealthThresholds {
  heartbeatTimeoutSeconds: number;
  degradedFailureRate: number;
  unhealthyFailureRate: number;
  degradedLatencyMultiplier: number;
  unhealthyLatencyMultiplier: number;
  maxQueueDepth: number;
}

interface WorkerHealthState {
  workerName: string;
  status: HealthStatus;
  lastHeartbeat?: Date;
  heartbeatCount: number;
  jobsProcessed: number;
  jobsFailed: number;
  avgDurationMs: number;
  lastDurationMs: number;
  expectedDurationMs: number;
  queueDepth: number;
  memoryMb: number;
  cpuPercent: number;
}

interface HealthSummary {
  totalWorkers: number;
  byStatus: Record<HealthStatus, number>;
  healthyCount: number;
  unhealthyCount: number;
  totalJobsProcessed: number;
  totalJobsFailed: number;
  overallFailureRate: number;
  systemStatus: 'healthy' | 'degraded' | 'unhealthy';
}

const DEFAULT_THRESHOLDS: HealthThresholds = {
  heartbeatTimeoutSeconds: 60,
  degradedFailureRate: 0.05,
  unhealthyFailureRate: 0.15,
  degradedLatencyMultiplier: 1.5,
  unhealthyLatencyMultiplier: 3.0,
  maxQueueDepth: 100,
};

class HealthMonitor {
  private workers = new Map<string, WorkerHealthState>();
  private thresholds: HealthThresholds;
  private durations = new Map<string, number[]>();

  constructor(thresholds: Partial<HealthThresholds> = {}) {
    this.thresholds = { ...DEFAULT_THRESHOLDS, ...thresholds };
  }

  registerWorker(workerName: string, expectedDurationMs: number): void {
    if (!this.workers.has(workerName)) {
      this.workers.set(workerName, {
        workerName,
        status: HealthStatus.UNKNOWN,
        heartbeatCount: 0,
        jobsProcessed: 0,
        jobsFailed: 0,
        avgDurationMs: 0,
        lastDurationMs: 0,
        expectedDurationMs,
        queueDepth: 0,
        memoryMb: 0,
        cpuPercent: 0,
      });
      this.durations.set(workerName, []);
    }
  }

  recordHeartbeat(
    workerName: string,
    metrics: { memoryMb?: number; cpuPercent?: number; queueDepth?: number } = {}
  ): void {
    const state = this.workers.get(workerName);
    if (!state) return;

    state.lastHeartbeat = new Date();
    state.heartbeatCount++;
    state.memoryMb = metrics.memoryMb ?? state.memoryMb;
    state.cpuPercent = metrics.cpuPercent ?? state.cpuPercent;
    state.queueDepth = metrics.queueDepth ?? state.queueDepth;
    state.status = this.determineStatus(state);
  }

  recordExecutionComplete(
    workerName: string,
    success: boolean,
    durationMs: number
  ): void {
    const state = this.workers.get(workerName);
    if (!state) return;

    state.jobsProcessed++;
    if (!success) state.jobsFailed++;
    state.lastDurationMs = durationMs;
    state.lastHeartbeat = new Date();

    // Update rolling duration window (keep last 100)
    const durations = this.durations.get(workerName) || [];
    durations.push(durationMs);
    if (durations.length > 100) durations.shift();
    this.durations.set(workerName, durations);

    state.avgDurationMs = durations.reduce((a, b) => a + b, 0) / durations.length;
    state.status = this.determineStatus(state);
  }

  private determineStatus(state: WorkerHealthState): HealthStatus {
    const now = new Date();

    // Check heartbeat
    if (!state.lastHeartbeat) return HealthStatus.OFFLINE;
    
    const heartbeatAge = (now.getTime() - state.lastHeartbeat.getTime()) / 1000;
    if (heartbeatAge > this.thresholds.heartbeatTimeoutSeconds) {
      return HealthStatus.OFFLINE;
    }

    // Check failure rate
    const failureRate = state.jobsProcessed > 0
      ? state.jobsFailed / state.jobsProcessed
      : 0;

    if (failureRate >= this.thresholds.unhealthyFailureRate) {
      return HealthStatus.UNHEALTHY;
    }
    if (failureRate >= this.thresholds.degradedFailureRate) {
      return HealthStatus.DEGRADED;
    }

    // Check latency
    if (state.avgDurationMs > state.expectedDurationMs * this.thresholds.unhealthyLatencyMultiplier) {
      return HealthStatus.UNHEALTHY;
    }
    if (state.avgDurationMs > state.expectedDurationMs * this.thresholds.degradedLatencyMultiplier) {
      return HealthStatus.DEGRADED;
    }

    // Check queue depth
    if (state.queueDepth > this.thresholds.maxQueueDepth) {
      return HealthStatus.DEGRADED;
    }

    return HealthStatus.HEALTHY;
  }

  getHealthSummary(): HealthSummary {
    const byStatus: Record<HealthStatus, number> = {
      healthy: 0, degraded: 0, unhealthy: 0, offline: 0, unknown: 0,
    };

    let totalJobs = 0, totalFailed = 0;

    for (const state of this.workers.values()) {
      state.status = this.determineStatus(state);
      byStatus[state.status]++;
      totalJobs += state.jobsProcessed;
      totalFailed += state.jobsFailed;
    }

    const unhealthyCount = byStatus.unhealthy + byStatus.offline;
    let systemStatus: 'healthy' | 'degraded' | 'unhealthy' = 'healthy';
    if (unhealthyCount > 0) systemStatus = 'unhealthy';
    else if (byStatus.degraded > 0) systemStatus = 'degraded';

    return {
      totalWorkers: this.workers.size,
      byStatus,
      healthyCount: byStatus.healthy,
      unhealthyCount,
      totalJobsProcessed: totalJobs,
      totalJobsFailed: totalFailed,
      overallFailureRate: totalJobs > 0 ? totalFailed / totalJobs : 0,
      systemStatus,
    };
  }

  getPercentileDuration(workerName: string, percentile: number): number {
    const durations = this.durations.get(workerName);
    if (!durations || durations.length === 0) return 0;

    const sorted = [...durations].sort((a, b) => a - b);
    const index = Math.ceil((percentile / 100) * sorted.length) - 1;
    return sorted[Math.max(0, index)];
  }

  checkStuckJobs(maxAgeSeconds = 300): string[] {
    const stuck: string[] = [];
    const now = new Date();

    for (const [name, state] of this.workers) {
      if (state.lastHeartbeat) {
        const age = (now.getTime() - state.lastHeartbeat.getTime()) / 1000;
        if (age > maxAgeSeconds && state.status !== HealthStatus.OFFLINE) {
          stuck.push(name);
        }
      }
    }
    return stuck;
  }
}

// Singleton
let monitor: HealthMonitor | null = null;
export function getHealthMonitor(): HealthMonitor {
  if (!monitor) monitor = new HealthMonitor();
  return monitor;
}
```

### Python

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional
from enum import Enum


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    OFFLINE = "offline"
    UNKNOWN = "unknown"


@dataclass
class HealthThresholds:
    heartbeat_timeout_seconds: int = 60
    degraded_failure_rate: float = 0.05
    unhealthy_failure_rate: float = 0.15
    degraded_latency_multiplier: float = 1.5
    unhealthy_latency_multiplier: float = 3.0
    max_queue_depth: int = 100


@dataclass
class WorkerHealthState:
    worker_name: str
    expected_duration_ms: float
    status: HealthStatus = HealthStatus.UNKNOWN
    last_heartbeat: Optional[datetime] = None
    heartbeat_count: int = 0
    jobs_processed: int = 0
    jobs_failed: int = 0
    avg_duration_ms: float = 0
    last_duration_ms: float = 0
    queue_depth: int = 0
    memory_mb: float = 0
    cpu_percent: float = 0


class HealthMonitor:
    def __init__(self, thresholds: Optional[HealthThresholds] = None):
        self._thresholds = thresholds or HealthThresholds()
        self._workers: Dict[str, WorkerHealthState] = {}
        self._durations: Dict[str, List[float]] = {}
    
    def register_worker(self, worker_name: str, expected_duration_ms: float) -> None:
        if worker_name not in self._workers:
            self._workers[worker_name] = WorkerHealthState(
                worker_name=worker_name,
                expected_duration_ms=expected_duration_ms,
            )
            self._durations[worker_name] = []
    
    def record_heartbeat(
        self,
        worker_name: str,
        memory_mb: float = 0,
        cpu_percent: float = 0,
        queue_depth: int = 0,
    ) -> None:
        state = self._workers.get(worker_name)
        if not state:
            return
        
        state.last_heartbeat = datetime.now(timezone.utc)
        state.heartbeat_count += 1
        state.memory_mb = memory_mb
        state.cpu_percent = cpu_percent
        state.queue_depth = queue_depth
        state.status = self._determine_status(state)
    
    def record_execution_complete(
        self,
        worker_name: str,
        success: bool,
        duration_ms: float,
    ) -> None:
        state = self._workers.get(worker_name)
        if not state:
            return
        
        state.jobs_processed += 1
        if not success:
            state.jobs_failed += 1
        state.last_duration_ms = duration_ms
        state.last_heartbeat = datetime.now(timezone.utc)
        
        # Update rolling window
        durations = self._durations.get(worker_name, [])
        durations.append(duration_ms)
        if len(durations) > 100:
            durations.pop(0)
        self._durations[worker_name] = durations
        
        state.avg_duration_ms = sum(durations) / len(durations) if durations else 0
        state.status = self._determine_status(state)
    
    def _determine_status(self, state: WorkerHealthState) -> HealthStatus:
        now = datetime.now(timezone.utc)
        
        if not state.last_heartbeat:
            return HealthStatus.OFFLINE
        
        heartbeat_age = (now - state.last_heartbeat).total_seconds()
        if heartbeat_age > self._thresholds.heartbeat_timeout_seconds:
            return HealthStatus.OFFLINE
        
        failure_rate = state.jobs_failed / state.jobs_processed if state.jobs_processed > 0 else 0
        
        if failure_rate >= self._thresholds.unhealthy_failure_rate:
            return HealthStatus.UNHEALTHY
        if failure_rate >= self._thresholds.degraded_failure_rate:
            return HealthStatus.DEGRADED
        
        if state.avg_duration_ms > state.expected_duration_ms * self._thresholds.unhealthy_latency_multiplier:
            return HealthStatus.UNHEALTHY
        if state.avg_duration_ms > state.expected_duration_ms * self._thresholds.degraded_latency_multiplier:
            return HealthStatus.DEGRADED
        
        if state.queue_depth > self._thresholds.max_queue_depth:
            return HealthStatus.DEGRADED
        
        return HealthStatus.HEALTHY
    
    def get_health_summary(self) -> dict:
        by_status = {s.value: 0 for s in HealthStatus}
        total_jobs = 0
        total_failed = 0
        
        for state in self._workers.values():
            state.status = self._determine_status(state)
            by_status[state.status.value] += 1
            total_jobs += state.jobs_processed
            total_failed += state.jobs_failed
        
        unhealthy_count = by_status["unhealthy"] + by_status["offline"]
        
        if unhealthy_count > 0:
            system_status = "unhealthy"
        elif by_status["degraded"] > 0:
            system_status = "degraded"
        else:
            system_status = "healthy"
        
        return {
            "total_workers": len(self._workers),
            "by_status": by_status,
            "healthy_count": by_status["healthy"],
            "unhealthy_count": unhealthy_count,
            "total_jobs_processed": total_jobs,
            "total_jobs_failed": total_failed,
            "overall_failure_rate": total_failed / total_jobs if total_jobs > 0 else 0,
            "system_status": system_status,
        }
    
    def get_percentile_duration(self, worker_name: str, percentile: float) -> float:
        durations = self._durations.get(worker_name, [])
        if not durations:
            return 0
        
        sorted_durations = sorted(durations)
        index = int((percentile / 100) * len(sorted_durations)) - 1
        return sorted_durations[max(0, index)]


# Singleton
_monitor: Optional[HealthMonitor] = None

def get_health_monitor() -> HealthMonitor:
    global _monitor
    if _monitor is None:
        _monitor = HealthMonitor()
    return _monitor
```

## Usage Examples

### Worker Registration

```typescript
const monitor = getHealthMonitor();

// Register workers with expected durations
monitor.registerWorker('email-sender', 5000);     // 5s expected
monitor.registerWorker('data-processor', 30000);  // 30s expected
monitor.registerWorker('report-generator', 60000); // 60s expected
```

### Job Execution Tracking

```typescript
async function processJob(job: Job) {
  const startTime = Date.now();

  try {
    await doWork(job);
    monitor.recordExecutionComplete('data-processor', true, Date.now() - startTime);
  } catch (error) {
    monitor.recordExecutionComplete('data-processor', false, Date.now() - startTime);
    throw error;
  }
}
```

### Heartbeat Loop

```typescript
setInterval(() => {
  const memUsage = process.memoryUsage();
  
  monitor.recordHeartbeat('data-processor', {
    memoryMb: Math.round(memUsage.heapUsed / 1024 / 1024),
    cpuPercent: getCpuUsage(),
    queueDepth: getQueueDepth(),
  });
}, 30000);
```

### Health API Endpoint

```typescript
app.get('/health/workers', async (req, res) => {
  const summary = monitor.getHealthSummary();
  const statusCode = summary.systemStatus === 'unhealthy' ? 503 : 200;
  
  res.status(statusCode).json({
    status: summary.systemStatus,
    summary,
    percentiles: {
      'data-processor': {
        p50: monitor.getPercentileDuration('data-processor', 50),
        p95: monitor.getPercentileDuration('data-processor', 95),
        p99: monitor.getPercentileDuration('data-processor', 99),
      },
    },
  });
});
```

## Best Practices

1. Set expected durations based on actual baseline measurements
2. Use rolling windows to smooth out outliers
3. Configure thresholds based on your SLOs
4. Send heartbeats even when idle
5. Include resource metrics (memory, CPU) in heartbeats

## Common Mistakes

- Heartbeat timeout too short (false offline detection)
- Not tracking job durations (miss degradation)
- Failure rate thresholds too strict (alert fatigue)
- No percentile tracking (miss tail latency issues)
- Missing heartbeats during long jobs

## Related Patterns

- health-checks - HTTP health endpoints
- anomaly-detection - Alert on health changes
- graceful-shutdown - Drain workers cleanly
