---
name: monitoring-alerting
description: Automatically applies when implementing monitoring and alerting. Ensures proper metric instrumentation, alerts, SLO/SLI definition, dashboards, and observability patterns.
category: observability
---

# Monitoring and Alerting Patterns

When implementing monitoring and alerting, follow these patterns for reliable observability.

**Trigger Keywords**: monitoring, alerting, metrics, SLO, SLI, SLA, dashboard, observability, instrumentation, Prometheus, Grafana, alert, threshold

**Agent Integration**: Used by `backend-architect`, `devops-engineer`, `sre-engineer`, `performance-engineer`

## ✅ Correct Pattern: Metric Instrumentation

```python
from prometheus_client import Counter, Histogram, Gauge, Summary
from typing import Callable
from functools import wraps
import time


# Define metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
)

active_connections = Gauge(
    'active_connections',
    'Number of active connections'
)

database_query_duration = Summary(
    'database_query_duration_seconds',
    'Database query duration',
    ['query_type']
)


def track_request_metrics(endpoint: str):
    """Decorator to track request metrics."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()

            try:
                # Execute request
                result = await func(*args, **kwargs)

                # Track success
                http_requests_total.labels(
                    method='GET',
                    endpoint=endpoint,
                    status='200'
                ).inc()

                # Track duration
                duration = time.time() - start_time
                http_request_duration_seconds.labels(
                    method='GET',
                    endpoint=endpoint
                ).observe(duration)

                return result

            except Exception as e:
                # Track error
                http_requests_total.labels(
                    method='GET',
                    endpoint=endpoint,
                    status='500'
                ).inc()
                raise

        return wrapper
    return decorator


# Usage
@track_request_metrics('/api/users')
async def get_users():
    """Get users with metrics tracking."""
    return await db.query(User).all()
```

## FastAPI Middleware for Metrics

```python
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
import time


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to track HTTP metrics."""

    async def dispatch(self, request: Request, call_next):
        """Track request metrics."""
        start_time = time.time()

        # Increment active connections
        active_connections.inc()

        try:
            response = await call_next(request)

            # Track metrics
            duration = time.time() - start_time

            http_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status=response.status_code
            ).inc()

            http_request_duration_seconds.labels(
                method=request.method,
                endpoint=request.url.path
            ).observe(duration)

            return response

        except Exception as e:
            # Track errors
            http_requests_total.labels(
                method=request.method,
                endpoint=request.url.path,
                status='500'
            ).inc()
            raise

        finally:
            # Decrement active connections
            active_connections.dec()


# Add middleware
app = FastAPI()
app.add_middleware(MetricsMiddleware)


# Metrics endpoint
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST

@app.get("/metrics")
async def metrics():
    """Expose Prometheus metrics."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )
```

## SLO/SLI Definition

```python
from dataclasses import dataclass
from typing import List, Dict
from datetime import datetime, timedelta


@dataclass
class SLI:
    """Service Level Indicator."""

    name: str
    description: str
    metric_query: str  # Prometheus query
    target: float      # Target percentage (0-100)
    window: timedelta  # Time window


@dataclass
class SLO:
    """Service Level Objective."""

    name: str
    description: str
    slis: List[SLI]
    error_budget: float  # Percentage (0-100)


# Define SLOs
api_availability_slo = SLO(
    name="API Availability",
    description="API should be available 99.9% of the time",
    slis=[
        SLI(
            name="Request Success Rate",
            description="Percentage of successful requests",
            metric_query="""
                sum(rate(http_requests_total{status=~"2.."}[5m]))
                /
                sum(rate(http_requests_total[5m]))
            """,
            target=99.9,
            window=timedelta(days=30)
        )
    ],
    error_budget=0.1  # 0.1% error budget
)

api_latency_slo = SLO(
    name="API Latency",
    description="95th percentile latency should be under 500ms",
    slis=[
        SLI(
            name="P95 Latency",
            description="95th percentile request duration",
            metric_query="""
                histogram_quantile(0.95,
                    sum(rate(http_request_duration_seconds_bucket[5m]))
                    by (le)
                )
            """,
            target=0.5,  # 500ms
            window=timedelta(days=30)
        )
    ],
    error_budget=5.0  # 5% can be over threshold
)


class SLOTracker:
    """Track SLO compliance."""

    def __init__(self, prometheus_url: str):
        self.prometheus_url = prometheus_url

    async def check_sli(self, sli: SLI) -> Dict[str, any]:
        """
        Check SLI against target.

        Returns:
            Dict with current value, target, and compliance
        """
        # Query Prometheus
        current_value = await self._query_prometheus(sli.metric_query)

        is_compliant = current_value >= sli.target

        return {
            "name": sli.name,
            "current": current_value,
            "target": sli.target,
            "compliant": is_compliant,
            "margin": current_value - sli.target
        }

    async def check_slo(self, slo: SLO) -> Dict[str, any]:
        """Check all SLIs for SLO."""
        sli_results = []

        for sli in slo.slis:
            result = await self.check_sli(sli)
            sli_results.append(result)

        all_compliant = all(r["compliant"] for r in sli_results)

        return {
            "name": slo.name,
            "slis": sli_results,
            "compliant": all_compliant,
            "error_budget_remaining": self._calculate_error_budget(slo, sli_results)
        }
```

## Alert Rules

```python
from typing import Dict, List, Callable
from pydantic import BaseModel


class AlertRule(BaseModel):
    """Alert rule definition."""

    name: str
    description: str
    query: str          # Prometheus query
    threshold: float
    duration: str       # e.g., "5m"
    severity: str       # critical, warning, info
    annotations: Dict[str, str] = {}
    labels: Dict[str, str] = {}


# Define alert rules
high_error_rate_alert = AlertRule(
    name="HighErrorRate",
    description="Error rate exceeds 1%",
    query="""
        sum(rate(http_requests_total{status=~"5.."}[5m]))
        /
        sum(rate(http_requests_total[5m]))
        > 0.01
    """,
    threshold=0.01,
    duration="5m",
    severity="critical",
    annotations={
        "summary": "High error rate detected",
        "description": "Error rate is {{ $value | humanizePercentage }}"
    },
    labels={
        "team": "backend",
        "component": "api"
    }
)

high_latency_alert = AlertRule(
    name="HighLatency",
    description="P95 latency exceeds 1 second",
    query="""
        histogram_quantile(0.95,
            sum(rate(http_request_duration_seconds_bucket[5m]))
            by (le)
        ) > 1.0
    """,
    threshold=1.0,
    duration="10m",
    severity="warning",
    annotations={
        "summary": "High API latency",
        "description": "P95 latency is {{ $value }}s"
    }
)

error_budget_exhausted_alert = AlertRule(
    name="ErrorBudgetExhausted",
    description="Error budget for availability SLO exhausted",
    query="""
        (1 - sum(rate(http_requests_total{status=~"2.."}[30d]))
        /
        sum(rate(http_requests_total[30d])))
        > 0.001
    """,
    threshold=0.001,
    duration="1h",
    severity="critical",
    annotations={
        "summary": "Error budget exhausted",
        "description": "SLO violation: error rate {{ $value | humanizePercentage }}"
    }
)


# Export to Prometheus alert format
def export_prometheus_alert(rule: AlertRule) -> str:
    """Export alert rule to Prometheus format."""
    return f"""
- alert: {rule.name}
  expr: {rule.query}
  for: {rule.duration}
  labels:
    severity: {rule.severity}
    {' '.join(f'{k}: {v}' for k, v in rule.labels.items())}
  annotations:
    {' '.join(f'{k}: {v}' for k, v in rule.annotations.items())}
"""
```

## Alert Notification

```python
import httpx
from typing import Dict


class AlertNotifier:
    """Send alert notifications."""

    def __init__(
        self,
        slack_webhook_url: str,
        pagerduty_key: str = None
    ):
        self.slack_webhook_url = slack_webhook_url
        self.pagerduty_key = pagerduty_key

    async def notify_slack(
        self,
        alert_name: str,
        severity: str,
        description: str,
        details: Dict[str, any] = None
    ):
        """Send Slack notification."""
        color = {
            "critical": "#FF0000",
            "warning": "#FFA500",
            "info": "#00FF00"
        }.get(severity, "#808080")

        message = {
            "attachments": [{
                "color": color,
                "title": f"🚨 {alert_name}",
                "text": description,
                "fields": [
                    {
                        "title": "Severity",
                        "value": severity.upper(),
                        "short": True
                    },
                    {
                        "title": "Time",
                        "value": datetime.utcnow().isoformat(),
                        "short": True
                    }
                ],
                "footer": "Monitoring System"
            }]
        }

        if details:
            message["attachments"][0]["fields"].extend([
                {
                    "title": k,
                    "value": str(v),
                    "short": True
                }
                for k, v in details.items()
            ])

        async with httpx.AsyncClient() as client:
            await client.post(
                self.slack_webhook_url,
                json=message
            )

    async def notify_pagerduty(
        self,
        alert_name: str,
        severity: str,
        description: str
    ):
        """Trigger PagerDuty incident."""
        if not self.pagerduty_key:
            return

        event = {
            "routing_key": self.pagerduty_key,
            "event_action": "trigger",
            "payload": {
                "summary": f"{alert_name}: {description}",
                "severity": severity,
                "source": "monitoring-system",
                "timestamp": datetime.utcnow().isoformat()
            }
        }

        async with httpx.AsyncClient() as client:
            await client.post(
                "https://events.pagerduty.com/v2/enqueue",
                json=event
            )


# Usage
notifier = AlertNotifier(
    slack_webhook_url="https://hooks.slack.com/services/...",
    pagerduty_key="..."
)

await notifier.notify_slack(
    alert_name="High Error Rate",
    severity="critical",
    description="Error rate exceeded 1%",
    details={
        "current_rate": "1.5%",
        "threshold": "1.0%"
    }
)
```

## Dashboard Configuration

```python
from typing import List


@dataclass
class DashboardPanel:
    """Grafana dashboard panel."""

    title: str
    query: str
    visualization: str  # graph, gauge, table
    unit: str = "short"
    thresholds: List[float] = None


@dataclass
class Dashboard:
    """Complete dashboard definition."""

    title: str
    panels: List[DashboardPanel]
    refresh: str = "30s"


# Define dashboard
api_dashboard = Dashboard(
    title="API Monitoring",
    panels=[
        DashboardPanel(
            title="Request Rate",
            query="sum(rate(http_requests_total[5m]))",
            visualization="graph",
            unit="reqps"
        ),
        DashboardPanel(
            title="Error Rate",
            query="""
                sum(rate(http_requests_total{status=~"5.."}[5m]))
                /
                sum(rate(http_requests_total[5m]))
            """,
            visualization="gauge",
            unit="percentunit",
            thresholds=[0.01, 0.05]
        ),
        DashboardPanel(
            title="P95 Latency",
            query="""
                histogram_quantile(0.95,
                    sum(rate(http_request_duration_seconds_bucket[5m]))
                    by (le)
                )
            """,
            visualization="graph",
            unit="s",
            thresholds=[0.5, 1.0]
        ),
        DashboardPanel(
            title="Active Connections",
            query="active_connections",
            visualization="gauge",
            unit="short"
        )
    ]
)
```

## ❌ Anti-Patterns

```python
# ❌ No metric labels
requests_total = Counter('requests_total', 'Total requests')
# Can't filter by endpoint or status!

# ✅ Better: Use labels
requests_total = Counter(
    'requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)


# ❌ Too many metric labels
requests = Counter(
    'requests',
    'Requests',
    ['method', 'endpoint', 'status', 'user_id', 'request_id']
)  # Cardinality explosion!

# ✅ Better: Reasonable labels
requests = Counter(
    'requests',
    'Requests',
    ['method', 'endpoint', 'status']
)


# ❌ No alert threshold
# Just logging errors without alerts

# ✅ Better: Define alert rules
if error_rate > 0.01:
    trigger_alert("High error rate")


# ❌ Vague alert messages
"Something is wrong"

# ✅ Better: Specific with context
f"Error rate {error_rate:.2%} exceeds threshold 1% for endpoint /api/users"
```

## Best Practices Checklist

- ✅ Instrument critical paths with metrics
- ✅ Use appropriate metric types (Counter, Gauge, Histogram)
- ✅ Add meaningful labels to metrics
- ✅ Define SLOs/SLIs for key services
- ✅ Create alert rules with thresholds
- ✅ Set up alert notifications (Slack, PagerDuty)
- ✅ Build dashboards for visualization
- ✅ Track error budgets
- ✅ Monitor latency percentiles (P50, P95, P99)
- ✅ Track request rates and error rates
- ✅ Monitor resource usage (CPU, memory)
- ✅ Set up on-call rotation

## Auto-Apply

When implementing monitoring:
1. Add Prometheus metrics to key endpoints
2. Define SLOs/SLIs for service
3. Create alert rules with thresholds
4. Set up alert notifications
5. Build Grafana dashboards
6. Track error budgets
7. Monitor latency and error rates

## Related Skills

- `observability-logging` - For logging patterns
- `performance-profiling` - For performance analysis
- `fastapi-patterns` - For API instrumentation
- `structured-errors` - For error tracking
