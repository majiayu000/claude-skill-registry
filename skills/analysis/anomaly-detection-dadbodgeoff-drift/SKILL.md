---
name: anomaly-detection
description: Rule-based anomaly detection for production systems with configurable thresholds, cooldown periods to prevent alert storms, and error pattern tracking for repeated failures.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: observability
  time: 5h
  source: drift-masterguide
---

# Anomaly Detection

Rule-based anomaly detection with cooldowns and error pattern tracking.

## When to Use This Skill

- Detecting slow job degradation before failures
- Tracking error rate creep over time
- Identifying repeated error patterns
- Preventing alert fatigue with cooldowns

## Core Concepts

Production systems fail in subtle ways - jobs getting slower, error rates creeping up, same errors repeating. The solution:

1. **Configurable rules** with severity levels
2. **Cooldown periods** to prevent alert storms
3. **Error pattern tracking** for repeated failures
4. **Violation decay** to reward recovery

## Implementation

### TypeScript

```typescript
enum AnomalyType {
  SLOW_JOB = 'slow_job',
  HIGH_FAILURE_RATE = 'high_failure_rate',
  WORKER_UNHEALTHY = 'worker_unhealthy',
  QUEUE_BACKLOG = 'queue_backlog',
  TIMEOUT_SPIKE = 'timeout_spike',
  REPEATED_ERROR = 'repeated_error',
  MEMORY_SPIKE = 'memory_spike',
  CPU_SPIKE = 'cpu_spike',
}

enum AnomalySeverity {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

interface AnomalyAlert {
  id: string;
  anomalyType: AnomalyType;
  severity: AnomalySeverity;
  workerName: string;
  jobId?: string;
  message: string;
  details: Record<string, unknown>;
  detectedAt: Date;
  resolvedAt?: Date;
  resolution?: string;
}

interface RuleContext {
  workerName: string;
  status: string;
  failureRate: number;
  queueDepth: number;
  durationMs: number;
  expectedDurationMs: number;
  timeoutCount: number;
  errorRepeatCount: number;
  errorMessage: string;
  memoryMb: number;
  cpuPercent: number;
}

interface AnomalyRule {
  anomalyType: AnomalyType;
  severity: AnomalySeverity;
  description: string;
  checkFn: (ctx: RuleContext) => boolean;
  messageTemplate: string;
  cooldownSeconds: number;
}

const ANOMALY_RULES: AnomalyRule[] = [
  {
    anomalyType: AnomalyType.SLOW_JOB,
    severity: AnomalySeverity.MEDIUM,
    description: 'Job execution time exceeds expected duration',
    checkFn: (ctx) => ctx.durationMs > ctx.expectedDurationMs * 2,
    messageTemplate: 'Job took {durationMs}ms, expected {expectedDurationMs}ms',
    cooldownSeconds: 300,
  },
  {
    anomalyType: AnomalyType.HIGH_FAILURE_RATE,
    severity: AnomalySeverity.HIGH,
    description: 'Worker failure rate exceeds threshold',
    checkFn: (ctx) => ctx.failureRate > 15,
    messageTemplate: 'Failure rate {failureRate}% exceeds 15% threshold',
    cooldownSeconds: 600,
  },
  {
    anomalyType: AnomalyType.WORKER_UNHEALTHY,
    severity: AnomalySeverity.CRITICAL,
    description: 'Worker health status is unhealthy',
    checkFn: (ctx) => ctx.status === 'unhealthy',
    messageTemplate: 'Worker {workerName} is unhealthy',
    cooldownSeconds: 300,
  },
  {
    anomalyType: AnomalyType.QUEUE_BACKLOG,
    severity: AnomalySeverity.MEDIUM,
    description: 'Queue depth exceeds threshold',
    checkFn: (ctx) => ctx.queueDepth > 50,
    messageTemplate: 'Queue depth {queueDepth} exceeds threshold',
    cooldownSeconds: 300,
  },
  {
    anomalyType: AnomalyType.REPEATED_ERROR,
    severity: AnomalySeverity.HIGH,
    description: 'Same error repeated multiple times',
    checkFn: (ctx) => ctx.errorRepeatCount > 5,
    messageTemplate: 'Error "{errorMessage}" repeated {errorRepeatCount} times',
    cooldownSeconds: 900,
  },
  {
    anomalyType: AnomalyType.MEMORY_SPIKE,
    severity: AnomalySeverity.HIGH,
    description: 'Memory usage exceeds threshold',
    checkFn: (ctx) => ctx.memoryMb > 1024,
    messageTemplate: 'Memory usage {memoryMb}MB exceeds 1GB threshold',
    cooldownSeconds: 300,
  },
];

class AnomalyDetector {
  private alerts = new Map<string, AnomalyAlert>();
  private cooldowns = new Map<string, Date>();
  private errorCounts = new Map<string, Map<string, number>>();
  private timeoutCounts = new Map<string, number>();
  private alertIdCounter = 0;

  checkWorkerHealth(
    workerName: string,
    health: {
      status: string;
      jobsProcessed: number;
      jobsFailed: number;
      queueDepth: number;
      lastDurationMs: number;
      expectedDurationMs: number;
      memoryMb: number;
      cpuPercent: number;
    }
  ): AnomalyAlert[] {
    const detected: AnomalyAlert[] = [];
    
    const failureRate = health.jobsProcessed > 0
      ? (health.jobsFailed / health.jobsProcessed) * 100
      : 0;

    const ctx: RuleContext = {
      workerName,
      status: health.status,
      failureRate,
      queueDepth: health.queueDepth,
      durationMs: health.lastDurationMs,
      expectedDurationMs: health.expectedDurationMs,
      timeoutCount: this.timeoutCounts.get(workerName) || 0,
      errorRepeatCount: 0,
      errorMessage: '',
      memoryMb: health.memoryMb,
      cpuPercent: health.cpuPercent,
    };

    for (const rule of ANOMALY_RULES) {
      if (this.isOnCooldown(workerName, rule.anomalyType)) continue;

      if (rule.checkFn(ctx)) {
        const alert = this.createAlert(workerName, rule, ctx);
        detected.push(alert);
        this.setCooldown(workerName, rule.anomalyType, rule.cooldownSeconds);
      }
    }

    return detected;
  }

  checkJobExecution(
    workerName: string,
    jobId: string,
    durationMs: number,
    expectedDurationMs: number,
    success: boolean,
    error?: string
  ): AnomalyAlert[] {
    const detected: AnomalyAlert[] = [];

    if (!success && error) {
      this.trackError(workerName, error);
    }

    // Check slow job
    if (durationMs > expectedDurationMs * 2) {
      if (!this.isOnCooldown(workerName, AnomalyType.SLOW_JOB)) {
        const rule = ANOMALY_RULES[0];
        const alert = this.createAlert(workerName, rule, {
          durationMs,
          expectedDurationMs,
        } as RuleContext);
        alert.jobId = jobId;
        detected.push(alert);
        this.setCooldown(workerName, AnomalyType.SLOW_JOB, 300);
      }
    }

    // Check repeated errors
    if (error) {
      const errorCounts = this.errorCounts.get(workerName);
      const count = errorCounts?.get(error.slice(0, 200)) || 0;
      
      if (count > 5 && !this.isOnCooldown(workerName, AnomalyType.REPEATED_ERROR)) {
        const rule = ANOMALY_RULES.find(r => r.anomalyType === AnomalyType.REPEATED_ERROR)!;
        const alert = this.createAlert(workerName, rule, {
          errorMessage: error.slice(0, 100),
          errorRepeatCount: count,
        } as RuleContext);
        detected.push(alert);
        this.setCooldown(workerName, AnomalyType.REPEATED_ERROR, 900);
      }
    }

    return detected;
  }

  resolveAnomaly(alertId: string, resolution: string): boolean {
    const alert = this.alerts.get(alertId);
    if (!alert || alert.resolvedAt) return false;

    alert.resolvedAt = new Date();
    alert.resolution = resolution;
    return true;
  }

  getActiveAnomalies(): AnomalyAlert[] {
    return Array.from(this.alerts.values())
      .filter(a => !a.resolvedAt)
      .sort((a, b) => {
        const order = { critical: 0, high: 1, medium: 2, low: 3 };
        return order[a.severity] - order[b.severity];
      });
  }

  private trackError(workerName: string, error: string): void {
    if (!this.errorCounts.has(workerName)) {
      this.errorCounts.set(workerName, new Map());
    }
    const counts = this.errorCounts.get(workerName)!;
    const key = error.slice(0, 200);
    counts.set(key, (counts.get(key) || 0) + 1);
  }

  private createAlert(workerName: string, rule: AnomalyRule, ctx: Partial<RuleContext>): AnomalyAlert {
    const id = `anomaly_${++this.alertIdCounter}_${Date.now()}`;
    
    let message = rule.messageTemplate;
    for (const [key, value] of Object.entries(ctx)) {
      message = message.replace(`{${key}}`, String(value));
    }

    const alert: AnomalyAlert = {
      id,
      anomalyType: rule.anomalyType,
      severity: rule.severity,
      workerName,
      message,
      details: ctx as Record<string, unknown>,
      detectedAt: new Date(),
    };

    this.alerts.set(id, alert);
    return alert;
  }

  private isOnCooldown(workerName: string, anomalyType: AnomalyType): boolean {
    const key = `${workerName}:${anomalyType}`;
    const cooldownEnd = this.cooldowns.get(key);
    return cooldownEnd !== undefined && cooldownEnd > new Date();
  }

  private setCooldown(workerName: string, anomalyType: AnomalyType, seconds: number): void {
    const key = `${workerName}:${anomalyType}`;
    this.cooldowns.set(key, new Date(Date.now() + seconds * 1000));
  }
}

// Singleton
let detector: AnomalyDetector | null = null;

export function getAnomalyDetector(): AnomalyDetector {
  if (!detector) {
    detector = new AnomalyDetector();
  }
  return detector;
}
```

### Python

```python
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Callable
from enum import Enum


class AnomalyType(str, Enum):
    SLOW_JOB = "slow_job"
    HIGH_FAILURE_RATE = "high_failure_rate"
    WORKER_UNHEALTHY = "worker_unhealthy"
    QUEUE_BACKLOG = "queue_backlog"
    TIMEOUT_SPIKE = "timeout_spike"
    REPEATED_ERROR = "repeated_error"
    MEMORY_SPIKE = "memory_spike"


class AnomalySeverity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class AnomalyAlert:
    id: str
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    worker_name: str
    message: str
    details: Dict
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    job_id: Optional[str] = None
    resolved_at: Optional[datetime] = None
    resolution: Optional[str] = None


@dataclass
class RuleContext:
    worker_name: str
    status: str = "healthy"
    failure_rate: float = 0.0
    queue_depth: int = 0
    duration_ms: float = 0.0
    expected_duration_ms: float = 0.0
    timeout_count: int = 0
    error_repeat_count: int = 0
    error_message: str = ""
    memory_mb: float = 0.0
    cpu_percent: float = 0.0


@dataclass
class AnomalyRule:
    anomaly_type: AnomalyType
    severity: AnomalySeverity
    description: str
    check_fn: Callable[[RuleContext], bool]
    message_template: str
    cooldown_seconds: int


ANOMALY_RULES: List[AnomalyRule] = [
    AnomalyRule(
        anomaly_type=AnomalyType.SLOW_JOB,
        severity=AnomalySeverity.MEDIUM,
        description="Job execution time exceeds expected duration",
        check_fn=lambda ctx: ctx.duration_ms > ctx.expected_duration_ms * 2,
        message_template="Job took {duration_ms}ms, expected {expected_duration_ms}ms",
        cooldown_seconds=300,
    ),
    AnomalyRule(
        anomaly_type=AnomalyType.HIGH_FAILURE_RATE,
        severity=AnomalySeverity.HIGH,
        description="Worker failure rate exceeds threshold",
        check_fn=lambda ctx: ctx.failure_rate > 15,
        message_template="Failure rate {failure_rate}% exceeds 15% threshold",
        cooldown_seconds=600,
    ),
    AnomalyRule(
        anomaly_type=AnomalyType.WORKER_UNHEALTHY,
        severity=AnomalySeverity.CRITICAL,
        description="Worker health status is unhealthy",
        check_fn=lambda ctx: ctx.status == "unhealthy",
        message_template="Worker {worker_name} is unhealthy",
        cooldown_seconds=300,
    ),
    AnomalyRule(
        anomaly_type=AnomalyType.REPEATED_ERROR,
        severity=AnomalySeverity.HIGH,
        description="Same error repeated multiple times",
        check_fn=lambda ctx: ctx.error_repeat_count > 5,
        message_template='Error "{error_message}" repeated {error_repeat_count} times',
        cooldown_seconds=900,
    ),
]


class AnomalyDetector:
    def __init__(self):
        self._alerts: Dict[str, AnomalyAlert] = {}
        self._cooldowns: Dict[str, datetime] = {}
        self._error_counts: Dict[str, Dict[str, int]] = {}
        self._timeout_counts: Dict[str, int] = {}
        self._alert_counter = 0
    
    def check_worker_health(
        self,
        worker_name: str,
        status: str,
        jobs_processed: int,
        jobs_failed: int,
        queue_depth: int,
        last_duration_ms: float,
        expected_duration_ms: float,
        memory_mb: float = 0,
        cpu_percent: float = 0,
    ) -> List[AnomalyAlert]:
        detected: List[AnomalyAlert] = []
        
        failure_rate = (jobs_failed / jobs_processed * 100) if jobs_processed > 0 else 0
        
        ctx = RuleContext(
            worker_name=worker_name,
            status=status,
            failure_rate=failure_rate,
            queue_depth=queue_depth,
            duration_ms=last_duration_ms,
            expected_duration_ms=expected_duration_ms,
            timeout_count=self._timeout_counts.get(worker_name, 0),
            memory_mb=memory_mb,
            cpu_percent=cpu_percent,
        )
        
        for rule in ANOMALY_RULES:
            if self._is_on_cooldown(worker_name, rule.anomaly_type):
                continue
            
            if rule.check_fn(ctx):
                alert = self._create_alert(worker_name, rule, ctx)
                detected.append(alert)
                self._set_cooldown(worker_name, rule.anomaly_type, rule.cooldown_seconds)
        
        return detected
    
    def check_job_execution(
        self,
        worker_name: str,
        job_id: str,
        duration_ms: float,
        expected_duration_ms: float,
        success: bool,
        error: Optional[str] = None,
    ) -> List[AnomalyAlert]:
        detected: List[AnomalyAlert] = []
        
        if not success and error:
            self._track_error(worker_name, error)
        
        # Check slow job
        if duration_ms > expected_duration_ms * 2:
            if not self._is_on_cooldown(worker_name, AnomalyType.SLOW_JOB):
                rule = ANOMALY_RULES[0]
                ctx = RuleContext(
                    worker_name=worker_name,
                    duration_ms=duration_ms,
                    expected_duration_ms=expected_duration_ms,
                )
                alert = self._create_alert(worker_name, rule, ctx)
                alert.job_id = job_id
                detected.append(alert)
                self._set_cooldown(worker_name, AnomalyType.SLOW_JOB, 300)
        
        # Check repeated errors
        if error:
            error_counts = self._error_counts.get(worker_name, {})
            count = error_counts.get(error[:200], 0)
            
            if count > 5 and not self._is_on_cooldown(worker_name, AnomalyType.REPEATED_ERROR):
                rule = next(r for r in ANOMALY_RULES if r.anomaly_type == AnomalyType.REPEATED_ERROR)
                ctx = RuleContext(
                    worker_name=worker_name,
                    error_message=error[:100],
                    error_repeat_count=count,
                )
                alert = self._create_alert(worker_name, rule, ctx)
                detected.append(alert)
                self._set_cooldown(worker_name, AnomalyType.REPEATED_ERROR, 900)
        
        return detected
    
    def resolve_anomaly(self, alert_id: str, resolution: str) -> bool:
        alert = self._alerts.get(alert_id)
        if not alert or alert.resolved_at:
            return False
        
        alert.resolved_at = datetime.now(timezone.utc)
        alert.resolution = resolution
        return True
    
    def get_active_anomalies(self) -> List[AnomalyAlert]:
        severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        return sorted(
            [a for a in self._alerts.values() if not a.resolved_at],
            key=lambda a: severity_order[a.severity.value]
        )
    
    def _track_error(self, worker_name: str, error: str) -> None:
        if worker_name not in self._error_counts:
            self._error_counts[worker_name] = {}
        key = error[:200]
        self._error_counts[worker_name][key] = self._error_counts[worker_name].get(key, 0) + 1
    
    def _create_alert(self, worker_name: str, rule: AnomalyRule, ctx: RuleContext) -> AnomalyAlert:
        self._alert_counter += 1
        alert_id = f"anomaly_{self._alert_counter}_{int(datetime.now().timestamp() * 1000)}"
        
        message = rule.message_template
        for key, value in ctx.__dict__.items():
            message = message.replace(f"{{{key}}}", str(value))
        
        alert = AnomalyAlert(
            id=alert_id,
            anomaly_type=rule.anomaly_type,
            severity=rule.severity,
            worker_name=worker_name,
            message=message,
            details=ctx.__dict__,
        )
        
        self._alerts[alert_id] = alert
        return alert
    
    def _is_on_cooldown(self, worker_name: str, anomaly_type: AnomalyType) -> bool:
        key = f"{worker_name}:{anomaly_type.value}"
        cooldown_end = self._cooldowns.get(key)
        return cooldown_end is not None and cooldown_end > datetime.now(timezone.utc)
    
    def _set_cooldown(self, worker_name: str, anomaly_type: AnomalyType, seconds: int) -> None:
        from datetime import timedelta
        key = f"{worker_name}:{anomaly_type.value}"
        self._cooldowns[key] = datetime.now(timezone.utc) + timedelta(seconds=seconds)


# Singleton
_detector: Optional[AnomalyDetector] = None

def get_anomaly_detector() -> AnomalyDetector:
    global _detector
    if _detector is None:
        _detector = AnomalyDetector()
    return _detector
```

## Usage Examples

### Worker Job Monitoring

```typescript
const detector = getAnomalyDetector();

async function executeJob(job: Job) {
  const startTime = Date.now();
  
  try {
    await processJob(job);
    const duration = Date.now() - startTime;
    
    const alerts = detector.checkJobExecution(
      'data-processor',
      job.id,
      duration,
      30000, // Expected 30s
      true
    );
    
    for (const alert of alerts) {
      await notifyOps(alert);
    }
  } catch (error) {
    const duration = Date.now() - startTime;
    
    const alerts = detector.checkJobExecution(
      'data-processor',
      job.id,
      duration,
      30000,
      false,
      error.message
    );
    
    for (const alert of alerts) {
      await notifyOps(alert);
    }
    throw error;
  }
}
```

### Periodic Health Checks

```typescript
setInterval(async () => {
  const health = await getWorkerHealth('data-processor');
  const alerts = detector.checkWorkerHealth('data-processor', health);
  
  for (const alert of alerts) {
    if (alert.severity === 'critical') {
      await pageOnCall(alert);
    } else {
      await notifySlack(alert);
    }
  }
}, 30000);
```

## Best Practices

1. Set cooldowns long enough to prevent alert storms
2. Use severity levels to route alerts appropriately
3. Track error patterns to catch repeated failures
4. Clean up old resolved alerts periodically
5. Tune thresholds based on your baseline metrics

## Common Mistakes

- Cooldowns too short (alert fatigue)
- No error pattern tracking (miss repeated failures)
- Same severity for all alerts (everything becomes noise)
- Not resolving alerts (dashboard becomes useless)
- Thresholds too sensitive (false positives)

## Related Patterns

- health-checks - Source of health data for anomaly detection
- logging-observability - Structured logging for alert context
- graceful-degradation - Response to detected anomalies
