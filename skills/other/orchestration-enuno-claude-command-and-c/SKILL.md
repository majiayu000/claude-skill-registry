---
name: circuit-breaker-skill
description: Implements circuit breaker pattern with 3-state FSM (CLOSED, OPEN, HALF_OPEN) to prevent cascading failures
version: 1.0.0
tags: [orchestration, circuit-breaker, resilience, fault-tolerance, failure-prevention]
---

# Circuit Breaker Skill

## Purpose

This skill implements the circuit breaker pattern to prevent cascading failures in distributed systems. It automatically detects failing services and stops sending requests (fail-fast) until the service recovers, implementing a 3-state finite state machine (CLOSED, OPEN, HALF_OPEN).

## When to Use This Skill

**Use this skill when:**
- ✅ Making calls to external services or APIs that may fail
- ✅ Want to prevent cascading failures across system
- ✅ Need automatic failure detection and recovery
- ✅ Implementing fault-tolerant multi-agent workflows
- ✅ Protecting slow or unresponsive dependencies

**Don't use this skill for:**
- ❌ Internal function calls (low failure risk)
- ❌ Database connections (use connection pooling instead)
- ❌ Operations that must always be attempted
- ❌ Services with no recovery mechanism

## Core Concepts

### Three States

```
CLOSED (Normal)         failures++        OPEN (Failing)
   ↓                    ----------→          ↓
   ↓                                         ↓ timeout
   ↓                                         ↓
   ↓                    ←----------      HALF_OPEN (Testing)
   ↓←----- success ----              failure →----+
   ↓                                               ↓
   +-----------------------------------------------+
```

**CLOSED**: Circuit is closed, requests flow normally
- Track success/failure rate
- Open circuit after threshold failures

**OPEN**: Circuit is open, fail-fast (don't call service)
- Reject all requests immediately
- Wait for timeout period
- Transition to HALF_OPEN after timeout

**HALF_OPEN**: Testing if service recovered
- Allow limited test requests
- If success → CLOSED (service recovered)
- If failure → OPEN (still failing)

## Implementation

### 1. Basic Circuit Breaker

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Any, Optional
import time
from collections import deque

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreaker:
    """
    Circuit breaker with 3-state FSM.

    Configuration:
        failure_threshold: Number of failures before opening circuit
        timeout: Seconds to wait before testing service again (OPEN → HALF_OPEN)
        half_open_max_calls: Maximum test calls in HALF_OPEN state
    """
    failure_threshold: int = 5
    timeout: float = 60.0  # seconds
    half_open_max_calls: int = 1

    # State
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    last_failure_time: Optional[float] = None
    half_open_calls: int = 0

    # Metrics
    total_calls: int = 0
    total_successes: int = 0
    total_failures: int = 0

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute function with circuit breaker protection.

        Raises:
            CircuitOpenError: If circuit is open
        """
        self.total_calls += 1

        # Check state
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._transition_to_half_open()
            else:
                self.total_failures += 1
                raise CircuitOpenError(
                    f"Circuit breaker is OPEN (service unavailable). "
                    f"Retry in {self._time_until_reset():.0f}s"
                )

        # Track HALF_OPEN calls
        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                # Exceeded test calls in HALF_OPEN
                self.total_failures += 1
                raise CircuitOpenError("Circuit breaker is testing recovery (HALF_OPEN). Try again soon.")

            self.half_open_calls += 1

        # Execute function
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure(e)
            raise

    def _on_success(self) -> None:
        """Handle successful call."""
        self.total_successes += 1
        self.failure_count = 0

        if self.state == CircuitState.HALF_OPEN:
            # Service recovered, close circuit
            self._transition_to_closed()

    def _on_failure(self, exception: Exception) -> None:
        """Handle failed call."""
        self.total_failures += 1
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            # Service still failing, reopen circuit
            self._transition_to_open()

        elif self.state == CircuitState.CLOSED:
            if self.failure_count >= self.failure_threshold:
                # Too many failures, open circuit
                self._transition_to_open()

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to test service."""
        if self.last_failure_time is None:
            return False

        return (time.time() - self.last_failure_time) >= self.timeout

    def _time_until_reset(self) -> float:
        """Calculate seconds until circuit can test recovery."""
        if self.last_failure_time is None:
            return 0.0

        elapsed = time.time() - self.last_failure_time
        return max(0, self.timeout - elapsed)

    def _transition_to_open(self) -> None:
        """Transition to OPEN state."""
        self.state = CircuitState.OPEN
        self.last_failure_time = time.time()
        print(f"⚠️ Circuit breaker OPEN (service failing)")

    def _transition_to_half_open(self) -> None:
        """Transition to HALF_OPEN state."""
        self.state = CircuitState.HALF_OPEN
        self.half_open_calls = 0
        print(f"🔄 Circuit breaker HALF_OPEN (testing recovery)")

    def _transition_to_closed(self) -> None:
        """Transition to CLOSED state."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        print(f"✓ Circuit breaker CLOSED (service recovered)")

    def reset(self) -> None:
        """Manually reset circuit breaker."""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        print("Circuit breaker manually reset to CLOSED")

class CircuitOpenError(Exception):
    """Raised when circuit breaker is OPEN."""
    pass
```

### 2. Advanced Circuit Breaker with Metrics

```python
@dataclass
class MetricsCircuitBreaker(CircuitBreaker):
    """Circuit breaker with detailed metrics tracking."""

    # Sliding window for failure rate calculation
    window_size: int = 100
    recent_calls: deque = field(default_factory=lambda: deque(maxlen=100))

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute with metrics tracking."""
        start_time = time.time()

        try:
            result = super().call(func, *args, **kwargs)
            duration = time.time() - start_time

            self.recent_calls.append({
                "success": True,
                "duration": duration,
                "timestamp": time.time()
            })

            return result

        except CircuitOpenError:
            # Circuit open, track as failure
            self.recent_calls.append({
                "success": False,
                "circuit_open": True,
                "timestamp": time.time()
            })
            raise

        except Exception as e:
            duration = time.time() - start_time

            self.recent_calls.append({
                "success": False,
                "duration": duration,
                "error": str(e),
                "timestamp": time.time()
            })
            raise

    def get_failure_rate(self) -> float:
        """Calculate failure rate over sliding window."""
        if not self.recent_calls:
            return 0.0

        failures = sum(1 for call in self.recent_calls if not call["success"])
        return failures / len(self.recent_calls)

    def get_avg_duration(self) -> float:
        """Calculate average call duration."""
        durations = [call["duration"] for call in self.recent_calls if "duration" in call]

        if not durations:
            return 0.0

        return sum(durations) / len(durations)

    def get_metrics(self) -> dict:
        """Get comprehensive metrics."""
        return {
            "state": self.state.value,
            "total_calls": self.total_calls,
            "total_successes": self.total_successes,
            "total_failures": self.total_failures,
            "success_rate": self.total_successes / max(1, self.total_calls),
            "failure_rate": self.get_failure_rate(),
            "avg_duration": self.get_avg_duration(),
            "time_until_reset": self._time_until_reset() if self.state == CircuitState.OPEN else 0
        }
```

### 3. Circuit Breaker Decorator

```python
def circuit_breaker(
    failure_threshold: int = 5,
    timeout: float = 60.0,
    half_open_max_calls: int = 1,
    name: Optional[str] = None
):
    """
    Decorator to add circuit breaker to function.

    Usage:
        @circuit_breaker(failure_threshold=3, timeout=30)
        def call_external_api():
            ...
    """
    cb = CircuitBreaker(
        failure_threshold=failure_threshold,
        timeout=timeout,
        half_open_max_calls=half_open_max_calls
    )

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            return cb.call(func, *args, **kwargs)

        wrapper.circuit_breaker = cb  # Expose CB for inspection
        wrapper.__name__ = name or func.__name__
        return wrapper

    return decorator
```

## Workflow

### Step 1: Create Circuit Breaker

```python
# Create circuit breaker for external service
api_circuit_breaker = CircuitBreaker(
    failure_threshold=5,    # Open after 5 failures
    timeout=60.0,           # Wait 60s before testing
    half_open_max_calls=1   # Allow 1 test call
)
```

### Step 2: Wrap Service Calls

```python
def call_external_api(endpoint: str, data: dict) -> dict:
    """Call external API with circuit breaker protection."""
    import requests

    def api_call():
        response = requests.post(endpoint, json=data, timeout=5)
        response.raise_for_status()
        return response.json()

    try:
        return api_circuit_breaker.call(api_call)

    except CircuitOpenError as e:
        # Circuit open - fail fast
        print(f"Service unavailable: {e}")
        # Return cached result or default value
        return {"status": "unavailable", "cached": True}

    except Exception as e:
        # Service failed
        print(f"API error: {e}")
        raise
```

### Step 3: Monitor Circuit State

```python
def monitor_circuit_breakers(breakers: dict):
    """Monitor all circuit breakers."""
    while True:
        for name, cb in breakers.items():
            metrics = cb.get_metrics() if hasattr(cb, 'get_metrics') else {}

            print(f"\nCircuit Breaker: {name}")
            print(f"  State: {cb.state.value}")
            print(f"  Failures: {cb.failure_count}/{cb.failure_threshold}")

            if cb.state == CircuitState.OPEN:
                print(f"  Retry in: {cb._time_until_reset():.0f}s")

        time.sleep(10)  # Check every 10 seconds
```

## Integration Patterns

### With Resilience Orchestrator

```python
# Resilience orchestrator uses circuit breakers for each service
from skills.orchestration.circuit_breaker import CircuitBreaker

class ResilientOrchestrator:
    def __init__(self):
        self.circuit_breakers = {
            "database": CircuitBreaker(failure_threshold=3, timeout=30),
            "external_api": CircuitBreaker(failure_threshold=5, timeout=60),
            "payment_gateway": CircuitBreaker(failure_threshold=2, timeout=120)
        }

    def call_service(self, service_name: str, func: Callable) -> Any:
        """Call service with circuit breaker protection."""
        cb = self.circuit_breakers[service_name]

        try:
            return cb.call(func)

        except CircuitOpenError:
            # Fail fast - circuit is open
            return self._get_fallback_result(service_name)
```

### With Retry Logic

```python
def call_with_retry_and_circuit_breaker(
    func: Callable,
    circuit_breaker: CircuitBreaker,
    max_retries: int = 3,
    backoff_seconds: float = 2.0
) -> Any:
    """
    Combine circuit breaker with retry logic.

    Note: Circuit breaker provides fail-fast protection.
    Retries only happen when circuit is CLOSED or HALF_OPEN.
    """
    for attempt in range(max_retries):
        try:
            return circuit_breaker.call(func)

        except CircuitOpenError:
            # Don't retry if circuit is open
            raise

        except Exception as e:
            if attempt == max_retries - 1:
                raise

            # Exponential backoff
            wait_time = backoff_seconds * (2 ** attempt)
            print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s")
            time.sleep(wait_time)
```

## Examples

### Example 1: Protecting External API

```python
# Create circuit breaker for API
api_breaker = CircuitBreaker(failure_threshold=5, timeout=60)

@circuit_breaker(failure_threshold=5, timeout=60)
def fetch_user_data(user_id: str) -> dict:
    """Fetch user data from external API."""
    import requests
    response = requests.get(f"https://api.example.com/users/{user_id}")
    response.raise_for_status()
    return response.json()

# Use protected function
for user_id in user_ids:
    try:
        user_data = fetch_user_data(user_id)
        process_user(user_data)

    except CircuitOpenError:
        # Circuit open - use cached data
        user_data = cache.get(f"user:{user_id}")
        if user_data:
            process_user(user_data)
        else:
            log_warning(f"User {user_id} unavailable")
```

### Example 2: Multi-Service Orchestration

```python
# Different circuit breakers for each service
class ServiceOrchestrator:
    def __init__(self):
        self.breakers = {
            "auth_service": CircuitBreaker(failure_threshold=3, timeout=30),
            "user_service": CircuitBreaker(failure_threshold=5, timeout=60),
            "payment_service": CircuitBreaker(failure_threshold=2, timeout=120)
        }

    def create_order(self, user_id: str, items: list) -> dict:
        """Create order using multiple services."""

        # 1. Authenticate user (critical)
        try:
            auth = self.breakers["auth_service"].call(
                lambda: auth_service.verify(user_id)
            )
        except CircuitOpenError:
            return {"error": "Authentication service unavailable"}

        # 2. Get user details (optional - can use cache)
        try:
            user = self.breakers["user_service"].call(
                lambda: user_service.get(user_id)
            )
        except CircuitOpenError:
            user = cache.get(f"user:{user_id}")  # Fallback to cache

        # 3. Process payment (critical)
        try:
            payment = self.breakers["payment_service"].call(
                lambda: payment_service.charge(user_id, items)
            )
        except CircuitOpenError:
            return {"error": "Payment service unavailable"}

        return {"order_id": "...", "status": "confirmed"}
```

### Example 3: Graceful Degradation

```python
class RecommendationService:
    def __init__(self):
        self.ml_breaker = CircuitBreaker(failure_threshold=5, timeout=60)

    def get_recommendations(self, user_id: str) -> list:
        """Get recommendations with graceful degradation."""

        # Try ML service first
        try:
            return self.ml_breaker.call(
                lambda: ml_service.get_personalized_recommendations(user_id)
            )

        except CircuitOpenError:
            # ML service down - use simple fallback
            return self._get_popular_items()

    def _get_popular_items(self) -> list:
        """Fallback: Return popular items (cached)."""
        return cache.get("popular_items") or []
```

## Advanced Features

### 1. Selective Circuit Breaking

```python
def should_open_circuit(exception: Exception) -> bool:
    """Determine if exception should count toward opening circuit."""

    # Don't open circuit for client errors (4xx)
    if isinstance(exception, HTTPError):
        if 400 <= exception.response.status_code < 500:
            return False  # Client error, not service failure

    # Don't open for validation errors
    if isinstance(exception, ValidationError):
        return False

    # Open for server errors, timeouts, connection errors
    return True

class SelectiveCircuitBreaker(CircuitBreaker):
    """Circuit breaker that only opens for specific error types."""

    def _on_failure(self, exception: Exception) -> None:
        """Only count failures that should open circuit."""
        if should_open_circuit(exception):
            super()._on_failure(exception)
```

### 2. Adaptive Timeout

```python
class AdaptiveCircuitBreaker(MetricsCircuitBreaker):
    """Circuit breaker with adaptive timeout based on recovery time."""

    base_timeout: float = 60.0
    max_timeout: float = 300.0

    def _transition_to_open(self) -> None:
        """Adjust timeout based on failure history."""
        super()._transition_to_open()

        # Increase timeout if circuit opens frequently
        recent_opens = sum(
            1 for call in self.recent_calls
            if call.get("circuit_open", False)
        )

        if recent_opens > 10:
            # Service is frequently failing, wait longer
            self.timeout = min(self.timeout * 1.5, self.max_timeout)
            print(f"Adaptive timeout increased to {self.timeout:.0f}s")
```

### 3. Circuit Breaker Pool

```python
class CircuitBreakerPool:
    """Manage multiple circuit breakers."""

    def __init__(self):
        self.breakers: Dict[str, CircuitBreaker] = {}

    def get_breaker(self, name: str, **config) -> CircuitBreaker:
        """Get or create circuit breaker."""
        if name not in self.breakers:
            self.breakers[name] = CircuitBreaker(**config)

        return self.breakers[name]

    def get_all_states(self) -> Dict[str, str]:
        """Get state of all circuit breakers."""
        return {
            name: breaker.state.value
            for name, breaker in self.breakers.items()
        }

    def reset_all(self) -> None:
        """Reset all circuit breakers."""
        for breaker in self.breakers.values():
            breaker.reset()
```

## Monitoring Dashboard

```python
def generate_circuit_breaker_dashboard(breakers: Dict[str, CircuitBreaker]) -> str:
    """Generate status dashboard for circuit breakers."""

    dashboard = []
    dashboard.append("Circuit Breaker Status")
    dashboard.append("=" * 60)

    for name, cb in breakers.items():
        # State indicator
        if cb.state == CircuitState.CLOSED:
            indicator = "✓"
        elif cb.state == CircuitState.OPEN:
            indicator = "✗"
        else:
            indicator = "⚠"

        dashboard.append(f"\n{indicator} {name}: {cb.state.value.upper()}")

        # Metrics
        if hasattr(cb, 'get_metrics'):
            metrics = cb.get_metrics()
            dashboard.append(f"  Success Rate: {metrics['success_rate']:.1%}")
            dashboard.append(f"  Avg Duration: {metrics['avg_duration']:.2f}s")

            if cb.state == CircuitState.OPEN:
                dashboard.append(f"  Retry in: {metrics['time_until_reset']:.0f}s")

        else:
            dashboard.append(f"  Failures: {cb.failure_count}/{cb.failure_threshold}")

    return "\n".join(dashboard)
```

## Best Practices

1. **Set Appropriate Thresholds**
   ```python
   # Critical services: Lower threshold
   auth_breaker = CircuitBreaker(failure_threshold=3, timeout=30)

   # Non-critical services: Higher threshold
   recommendations_breaker = CircuitBreaker(failure_threshold=10, timeout=60)
   ```

2. **Provide Fallbacks**
   ```python
   try:
       result = circuit_breaker.call(service_call)
   except CircuitOpenError:
       result = get_cached_result()  # Always have fallback
   ```

3. **Monitor Circuit State**
   ```python
   # Alert when circuit opens
   if circuit_breaker.state == CircuitState.OPEN:
       alert_operators(f"Circuit {name} is OPEN")
   ```

4. **Don't Catch CircuitOpenError Silently**
   ```python
   # Bad: Silent failure
   try:
       result = circuit_breaker.call(func)
   except CircuitOpenError:
       pass  # Bad! User has no feedback

   # Good: Handle explicitly
   try:
       result = circuit_breaker.call(func)
   except CircuitOpenError:
       log_warning("Service unavailable, using fallback")
       result = fallback_value
   ```

5. **Test Circuit Breaker Behavior**
   ```python
   def test_circuit_breaker():
       cb = CircuitBreaker(failure_threshold=2, timeout=1)

       # Force failures to open circuit
       for _ in range(2):
           try:
               cb.call(lambda: (_ for _ in ()).throw(Exception()))
           except:
               pass

       assert cb.state == CircuitState.OPEN

       # Wait for timeout
       time.sleep(1.1)

       # Should transition to HALF_OPEN
       try:
           cb.call(lambda: "success")
       except:
           pass

       assert cb.state == CircuitState.CLOSED
   ```

## Related Skills

- `retry-handler-skill`: Combine with circuit breaker for resilient calls
- `saga-pattern-skill`: Use circuit breaker in saga steps
- `resilience-orchestrator-skill`: Orchestrates multiple circuit breakers

## References

- [Circuit Breaker Pattern (Martin Fowler)](https://martinfowler.com/bliki/CircuitBreaker.html)
- Document 15, Section 5: Advanced Error Handling
- Command: `/fault-tolerant-orchestrator`

---

**Version**: 1.0.0
**Status**: Production Ready
**Complexity**: Medium (state machine logic)
**Token Cost**: Minimal (low overhead protection)
