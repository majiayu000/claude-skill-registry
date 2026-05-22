---
name: safety-architecture
version: 1.0.0
description: |
  Framework for designing safeguards in autonomous systems including kill switches,
  resource limits, anomaly detection, and human-in-the-loop patterns.
author: QuantQuiver AI R&D
license: MIT

category: workflow
tags:
  - safety
  - autonomous-systems
  - kill-switch
  - monitoring
  - risk-management
  - circuit-breaker
  - failsafe

dependencies:
  skills: []
  python: ">=3.9"
  packages:
    - pyyaml
  tools:
    - code_execution
    - bash

triggers:
  - "safety architecture"
  - "kill switch"
  - "autonomous safeguards"
  - "circuit breaker"
  - "failsafe design"
  - "human in the loop"
  - "anomaly detection"
---

# Safety Architecture Framework

## Purpose

A framework for designing safeguards in autonomous systems including kill switches, resource limits, anomaly detection, and human-in-the-loop patterns. Ensures autonomous systems fail safely and maintain human oversight.

**Problem Space:**
- Autonomous systems can cause runaway damage if unchecked
- Default behavior during failures often unsafe
- Human oversight mechanisms afterthoughts
- Resource exhaustion can cascade to other systems

**Solution Approach:**
- Defense-in-depth safety layers
- Fail-safe defaults
- Mandatory human checkpoints
- Resource isolation and limits
- Comprehensive anomaly detection

## When to Use

- Designing any autonomous system
- Systems that control resources (money, compute, data)
- AI agents with tool access
- Automated trading/scheduling systems
- Any system requiring regulatory compliance
- Production systems with business-critical operations

## When NOT to Use

- Simple scripts with no autonomous decision-making
- Read-only analysis tools
- Systems with no resource impact
- Prototype/experimental code (but consider adding before production)

---

## Core Instructions

### Safety Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    SAFETY LAYER ARCHITECTURE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Layer 5: Human Oversight                                       │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Manual approval gates for critical actions              │ │
│  │  • Alert escalation with response requirements             │ │
│  │  • Audit logging with human review                        │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
│  Layer 4: Business Logic Guards                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Domain-specific validation rules                        │ │
│  │  • Value limits and thresholds                            │ │
│  │  • Timing and rate constraints                            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
│  Layer 3: Anomaly Detection                                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Statistical outlier detection                          │ │
│  │  • Behavioral drift monitoring                            │ │
│  │  • Pattern deviation alerts                               │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
│  Layer 2: Circuit Breakers                                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Error rate thresholds                                   │ │
│  │  • Consecutive failure limits                              │ │
│  │  • Automatic recovery with backoff                        │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
│  Layer 1: Resource Limits (Hard Stops)                          │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Memory limits                                           │ │
│  │  • CPU/time limits                                         │ │
│  │  • Cost/budget caps                                        │ │
│  │  • Action count limits                                     │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Standard Safety Components

#### 1. Kill Switch Patterns

```python
from datetime import datetime, timedelta
from enum import Enum
import threading
import signal
import sys

class KillSwitchState(Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    KILLED = "killed"

class KillSwitch:
    """
    Global kill switch for autonomous system.

    Features:
    - Manual activation (API/CLI)
    - Automatic activation on anomaly
    - Graceful shutdown with cleanup
    - State persistence for recovery
    """

    def __init__(self, cleanup_callback=None, timeout_seconds=30):
        self.state = KillSwitchState.ACTIVE
        self.cleanup_callback = cleanup_callback
        self.timeout_seconds = timeout_seconds
        self.activation_reason = None
        self.activation_time = None
        self._lock = threading.Lock()

        # Register signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle OS signals for graceful shutdown."""
        self.activate(f"Received signal {signum}")

    def activate(self, reason: str):
        """
        Activate kill switch - stops all autonomous operations.

        Args:
            reason: Why the kill switch was activated
        """
        with self._lock:
            if self.state == KillSwitchState.KILLED:
                return  # Already killed

            self.state = KillSwitchState.KILLED
            self.activation_reason = reason
            self.activation_time = datetime.now()

            print(f"[KILL SWITCH ACTIVATED] {reason}")

            # Run cleanup with timeout
            if self.cleanup_callback:
                cleanup_thread = threading.Thread(
                    target=self.cleanup_callback
                )
                cleanup_thread.start()
                cleanup_thread.join(timeout=self.timeout_seconds)

                if cleanup_thread.is_alive():
                    print("[KILL SWITCH] Cleanup timeout - forcing exit")

    def pause(self, reason: str):
        """Pause operations without full shutdown."""
        with self._lock:
            if self.state == KillSwitchState.ACTIVE:
                self.state = KillSwitchState.PAUSED
                self.activation_reason = reason
                print(f"[SYSTEM PAUSED] {reason}")

    def resume(self):
        """Resume from paused state."""
        with self._lock:
            if self.state == KillSwitchState.PAUSED:
                self.state = KillSwitchState.ACTIVE
                self.activation_reason = None
                print("[SYSTEM RESUMED]")

    def check(self) -> bool:
        """Check if operations should continue."""
        return self.state == KillSwitchState.ACTIVE

    @property
    def is_active(self) -> bool:
        return self.state == KillSwitchState.ACTIVE

    @property
    def is_paused(self) -> bool:
        return self.state == KillSwitchState.PAUSED

    @property
    def is_killed(self) -> bool:
        return self.state == KillSwitchState.KILLED
```

#### 2. Circuit Breaker Pattern

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import threading

class CircuitState(Enum):
    CLOSED = "closed"    # Normal operation
    OPEN = "open"        # Failing - reject calls
    HALF_OPEN = "half_open"  # Testing recovery

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout_seconds: int = 60
    half_open_max_calls: int = 3

class CircuitBreaker:
    """
    Circuit breaker for protecting against cascading failures.

    States:
    - CLOSED: Normal operation, tracking failures
    - OPEN: Failing, rejecting all calls
    - HALF_OPEN: Testing if service recovered
    """

    def __init__(self, name: str, config: CircuitBreakerConfig = None):
        self.name = name
        self.config = config or CircuitBreakerConfig()
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        self._lock = threading.Lock()

    def can_execute(self) -> bool:
        """Check if call should be allowed."""
        with self._lock:
            if self.state == CircuitState.CLOSED:
                return True

            if self.state == CircuitState.OPEN:
                # Check if timeout elapsed
                if self._timeout_elapsed():
                    self._transition_to_half_open()
                    return True
                return False

            if self.state == CircuitState.HALF_OPEN:
                if self.half_open_calls < self.config.half_open_max_calls:
                    self.half_open_calls += 1
                    return True
                return False

            return False

    def record_success(self):
        """Record successful call."""
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                if self.success_count >= self.config.success_threshold:
                    self._transition_to_closed()
            elif self.state == CircuitState.CLOSED:
                # Reset failure count on success
                self.failure_count = 0

    def record_failure(self):
        """Record failed call."""
        with self._lock:
            self.last_failure_time = datetime.now()

            if self.state == CircuitState.HALF_OPEN:
                self._transition_to_open()
            elif self.state == CircuitState.CLOSED:
                self.failure_count += 1
                if self.failure_count >= self.config.failure_threshold:
                    self._transition_to_open()

    def _timeout_elapsed(self) -> bool:
        if not self.last_failure_time:
            return True
        elapsed = datetime.now() - self.last_failure_time
        return elapsed.total_seconds() >= self.config.timeout_seconds

    def _transition_to_open(self):
        self.state = CircuitState.OPEN
        print(f"[CIRCUIT BREAKER] {self.name}: OPEN (failures: {self.failure_count})")

    def _transition_to_half_open(self):
        self.state = CircuitState.HALF_OPEN
        self.half_open_calls = 0
        self.success_count = 0
        print(f"[CIRCUIT BREAKER] {self.name}: HALF_OPEN (testing recovery)")

    def _transition_to_closed(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        print(f"[CIRCUIT BREAKER] {self.name}: CLOSED (recovered)")

    def __call__(self, func):
        """Decorator for wrapping functions with circuit breaker."""
        def wrapper(*args, **kwargs):
            if not self.can_execute():
                raise CircuitOpenError(f"Circuit {self.name} is open")
            try:
                result = func(*args, **kwargs)
                self.record_success()
                return result
            except Exception as e:
                self.record_failure()
                raise
        return wrapper

class CircuitOpenError(Exception):
    pass
```

#### 3. Resource Limiter

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import threading

@dataclass
class ResourceLimits:
    """Configuration for resource limits."""
    max_actions_per_hour: int = 1000
    max_value_per_action: float = 10000.0
    max_total_value_per_hour: float = 100000.0
    max_api_calls_per_minute: int = 60
    max_memory_mb: int = 1024
    max_execution_time_seconds: int = 300

class ResourceLimiter:
    """
    Tracks and enforces resource usage limits.

    Prevents runaway consumption of:
    - API calls
    - Financial value
    - Compute resources
    - Time
    """

    def __init__(self, limits: ResourceLimits = None):
        self.limits = limits or ResourceLimits()
        self.action_count = 0
        self.total_value = 0.0
        self.api_calls = []  # Timestamps
        self.start_time = datetime.now()
        self.hour_start = datetime.now()
        self._lock = threading.Lock()

    def check_action(self, value: float = 0.0) -> tuple[bool, str]:
        """
        Check if action is within limits.

        Returns:
            (allowed, reason) tuple
        """
        with self._lock:
            self._cleanup_old_records()

            # Check execution time
            elapsed = (datetime.now() - self.start_time).total_seconds()
            if elapsed > self.limits.max_execution_time_seconds:
                return False, f"Max execution time exceeded ({elapsed:.0f}s)"

            # Check action count
            if self.action_count >= self.limits.max_actions_per_hour:
                return False, f"Max actions per hour exceeded ({self.action_count})"

            # Check single value
            if value > self.limits.max_value_per_action:
                return False, f"Action value ${value:.2f} exceeds max ${self.limits.max_value_per_action:.2f}"

            # Check total value
            if self.total_value + value > self.limits.max_total_value_per_hour:
                return False, f"Total value would exceed limit (${self.total_value + value:.2f})"

            return True, "OK"

    def record_action(self, value: float = 0.0):
        """Record an action and its value."""
        with self._lock:
            self.action_count += 1
            self.total_value += value

    def check_api_call(self) -> tuple[bool, str]:
        """Check if API call is within rate limit."""
        with self._lock:
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)

            # Clean old calls
            self.api_calls = [t for t in self.api_calls if t > minute_ago]

            if len(self.api_calls) >= self.limits.max_api_calls_per_minute:
                return False, f"API rate limit exceeded ({len(self.api_calls)}/min)"

            return True, "OK"

    def record_api_call(self):
        """Record an API call."""
        with self._lock:
            self.api_calls.append(datetime.now())

    def _cleanup_old_records(self):
        """Reset hourly counters if hour elapsed."""
        now = datetime.now()
        if (now - self.hour_start).total_seconds() >= 3600:
            self.action_count = 0
            self.total_value = 0.0
            self.hour_start = now

    def get_usage_report(self) -> Dict[str, Any]:
        """Get current resource usage."""
        with self._lock:
            return {
                "actions_this_hour": self.action_count,
                "actions_limit": self.limits.max_actions_per_hour,
                "value_this_hour": self.total_value,
                "value_limit": self.limits.max_total_value_per_hour,
                "api_calls_last_minute": len(self.api_calls),
                "api_limit": self.limits.max_api_calls_per_minute,
                "execution_seconds": (datetime.now() - self.start_time).total_seconds(),
                "execution_limit": self.limits.max_execution_time_seconds,
            }
```

#### 4. Anomaly Detector

```python
from dataclasses import dataclass
from collections import deque
from typing import Optional, List
import statistics
import math

@dataclass
class AnomalyConfig:
    window_size: int = 100
    z_score_threshold: float = 3.0
    min_samples: int = 10
    consecutive_anomalies_alert: int = 3

class AnomalyDetector:
    """
    Statistical anomaly detection for continuous metrics.

    Uses Z-score method with rolling statistics.
    """

    def __init__(self, name: str, config: AnomalyConfig = None):
        self.name = name
        self.config = config or AnomalyConfig()
        self.values = deque(maxlen=self.config.window_size)
        self.consecutive_anomalies = 0

    def check(self, value: float) -> tuple[bool, Optional[str]]:
        """
        Check if value is anomalous.

        Returns:
            (is_anomaly, reason) tuple
        """
        if len(self.values) < self.config.min_samples:
            self.values.append(value)
            return False, None

        mean = statistics.mean(self.values)
        stdev = statistics.stdev(self.values)

        if stdev == 0:
            self.values.append(value)
            return False, None

        z_score = abs((value - mean) / stdev)

        self.values.append(value)

        if z_score > self.config.z_score_threshold:
            self.consecutive_anomalies += 1
            reason = f"Z-score {z_score:.2f} > threshold {self.config.z_score_threshold}"

            if self.consecutive_anomalies >= self.config.consecutive_anomalies_alert:
                reason += f" (ALERT: {self.consecutive_anomalies} consecutive anomalies)"

            return True, reason
        else:
            self.consecutive_anomalies = 0
            return False, None

    @property
    def should_alert(self) -> bool:
        """Check if anomaly pattern warrants alert."""
        return self.consecutive_anomalies >= self.config.consecutive_anomalies_alert
```

#### 5. Human-in-the-Loop Gate

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Callable
import uuid

class ApprovalStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"

@dataclass
class ApprovalRequest:
    id: str
    action_type: str
    description: str
    value: float
    context: dict
    created_at: datetime
    expires_at: datetime
    status: ApprovalStatus = ApprovalStatus.PENDING
    reviewer: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    review_notes: Optional[str] = None

class HumanApprovalGate:
    """
    Requires human approval for critical actions.

    Features:
    - Configurable approval thresholds
    - Timeout handling
    - Audit trail
    - Notification hooks
    """

    def __init__(
        self,
        approval_timeout_minutes: int = 60,
        notify_callback: Callable = None,
        auto_approve_below: float = 0.0  # Auto-approve small values
    ):
        self.timeout_minutes = approval_timeout_minutes
        self.notify_callback = notify_callback
        self.auto_approve_below = auto_approve_below
        self.pending_approvals: dict[str, ApprovalRequest] = {}

    def request_approval(
        self,
        action_type: str,
        description: str,
        value: float,
        context: dict = None
    ) -> ApprovalRequest:
        """
        Create approval request for critical action.

        Returns:
            ApprovalRequest object to track
        """
        # Auto-approve small values
        if value <= self.auto_approve_below:
            request = ApprovalRequest(
                id=str(uuid.uuid4()),
                action_type=action_type,
                description=description,
                value=value,
                context=context or {},
                created_at=datetime.now(),
                expires_at=datetime.now(),
                status=ApprovalStatus.APPROVED,
                reviewer="auto",
                reviewed_at=datetime.now(),
                review_notes="Auto-approved (below threshold)"
            )
            return request

        # Create pending request
        request = ApprovalRequest(
            id=str(uuid.uuid4()),
            action_type=action_type,
            description=description,
            value=value,
            context=context or {},
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(minutes=self.timeout_minutes)
        )

        self.pending_approvals[request.id] = request

        # Send notification
        if self.notify_callback:
            self.notify_callback(request)

        print(f"[APPROVAL REQUIRED] {request.id}: {description} (${value:.2f})")

        return request

    def approve(
        self,
        request_id: str,
        reviewer: str,
        notes: str = None
    ) -> bool:
        """Approve a pending request."""
        if request_id not in self.pending_approvals:
            return False

        request = self.pending_approvals[request_id]

        if request.status != ApprovalStatus.PENDING:
            return False

        if datetime.now() > request.expires_at:
            request.status = ApprovalStatus.EXPIRED
            return False

        request.status = ApprovalStatus.APPROVED
        request.reviewer = reviewer
        request.reviewed_at = datetime.now()
        request.review_notes = notes

        print(f"[APPROVED] {request_id} by {reviewer}")
        return True

    def reject(
        self,
        request_id: str,
        reviewer: str,
        notes: str = None
    ) -> bool:
        """Reject a pending request."""
        if request_id not in self.pending_approvals:
            return False

        request = self.pending_approvals[request_id]

        if request.status != ApprovalStatus.PENDING:
            return False

        request.status = ApprovalStatus.REJECTED
        request.reviewer = reviewer
        request.reviewed_at = datetime.now()
        request.review_notes = notes

        print(f"[REJECTED] {request_id} by {reviewer}: {notes}")
        return True

    def check_status(self, request_id: str) -> ApprovalStatus:
        """Check approval status."""
        if request_id not in self.pending_approvals:
            return None

        request = self.pending_approvals[request_id]

        # Check expiration
        if request.status == ApprovalStatus.PENDING:
            if datetime.now() > request.expires_at:
                request.status = ApprovalStatus.EXPIRED

        return request.status
```

### Decision Framework

**When to Require Human Approval:**
- Actions above value threshold
- First-time or unusual actions
- Actions affecting external systems
- Any irreversible action
- Actions during anomaly state

**Circuit Breaker vs Kill Switch:**
| Aspect | Circuit Breaker | Kill Switch |
|--------|-----------------|-------------|
| Scope | Single service/endpoint | Entire system |
| Trigger | Automatic (errors) | Manual or critical anomaly |
| Recovery | Automatic with backoff | Manual restart required |
| Use Case | Service resilience | Emergency stop |

---

## Templates

### Complete Safety-Wrapped System

```python
class SafeAutonomousSystem:
    """
    Template for autonomous system with full safety architecture.
    """

    def __init__(self, config: dict):
        # Layer 1: Resource limits
        self.resource_limiter = ResourceLimiter(ResourceLimits(
            max_actions_per_hour=config.get("max_actions", 1000),
            max_value_per_action=config.get("max_value", 10000),
            max_total_value_per_hour=config.get("max_total", 100000)
        ))

        # Layer 2: Circuit breakers
        self.circuit_breakers = {
            "api": CircuitBreaker("api", CircuitBreakerConfig(
                failure_threshold=5,
                timeout_seconds=60
            )),
            "database": CircuitBreaker("database", CircuitBreakerConfig(
                failure_threshold=3,
                timeout_seconds=120
            ))
        }

        # Layer 3: Anomaly detection
        self.anomaly_detectors = {
            "value": AnomalyDetector("value", AnomalyConfig(z_score_threshold=3.0)),
            "frequency": AnomalyDetector("frequency", AnomalyConfig(z_score_threshold=2.5))
        }

        # Layer 4: Human approval
        self.approval_gate = HumanApprovalGate(
            approval_timeout_minutes=60,
            auto_approve_below=100.0
        )

        # Layer 5: Kill switch
        self.kill_switch = KillSwitch(cleanup_callback=self._cleanup)

    def execute_action(self, action: dict) -> dict:
        """
        Execute action through all safety layers.
        """
        # Check kill switch
        if not self.kill_switch.check():
            return {"error": "System is stopped", "reason": self.kill_switch.activation_reason}

        value = action.get("value", 0)

        # Check resource limits
        allowed, reason = self.resource_limiter.check_action(value)
        if not allowed:
            return {"error": "Resource limit exceeded", "reason": reason}

        # Check anomaly
        is_anomaly, anomaly_reason = self.anomaly_detectors["value"].check(value)
        if is_anomaly and self.anomaly_detectors["value"].should_alert:
            self.kill_switch.pause(f"Anomaly detected: {anomaly_reason}")
            return {"error": "Anomaly detected - paused", "reason": anomaly_reason}

        # Check circuit breakers
        if not self.circuit_breakers["api"].can_execute():
            return {"error": "Circuit open", "service": "api"}

        # Human approval for high-value actions
        if value > 1000:
            request = self.approval_gate.request_approval(
                action_type=action.get("type", "unknown"),
                description=action.get("description", ""),
                value=value,
                context=action
            )
            if request.status != ApprovalStatus.APPROVED:
                return {"error": "Approval required", "request_id": request.id}

        # Execute the actual action
        try:
            result = self._do_action(action)
            self.resource_limiter.record_action(value)
            self.circuit_breakers["api"].record_success()
            return {"success": True, "result": result}
        except Exception as e:
            self.circuit_breakers["api"].record_failure()
            return {"error": str(e)}

    def _do_action(self, action: dict):
        """Actual action implementation."""
        pass

    def _cleanup(self):
        """Cleanup on kill switch activation."""
        print("Running cleanup...")
```

---

## Examples

### Example 1: Trading System Safety

**Input**: "Add safety controls to my automated trading system"

**Output**: Implementation with:
- Position size limits per trade
- Daily loss limits with auto-stop
- Anomaly detection on trade frequency
- Human approval for large trades
- Kill switch for market anomalies

### Example 2: AI Agent Safeguards

**Input**: "Add safeguards to my autonomous AI agent"

**Output**: Implementation with:
- API call rate limiting
- Cost accumulation limits
- Circuit breakers for external services
- Human approval for destructive actions
- Emergency stop capability

---

## Validation Checklist

Before deploying autonomous system:

- [ ] Kill switch tested and accessible
- [ ] Circuit breakers configured for all external calls
- [ ] Resource limits set appropriately
- [ ] Anomaly detection calibrated on historical data
- [ ] Human approval thresholds defined
- [ ] Alert notifications tested
- [ ] Cleanup procedures verified
- [ ] Recovery procedures documented
- [ ] Monitoring dashboards created

---

## Related Resources

- Skill: `repository-auditor` - Security review of safety code
- Skill: `cicd-pipeline-generator` - CI with safety tests
- Pattern: Circuit Breaker (Martin Fowler)
- Pattern: Bulkhead (Resilience patterns)

---

## Changelog

### 1.0.0 (January 2026)
- Initial release
- Kill switch implementation
- Circuit breaker pattern
- Resource limiter
- Anomaly detection
- Human-in-the-loop gates
