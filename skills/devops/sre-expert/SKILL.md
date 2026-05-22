---
name: sre-expert
version: 1.0.0
description: Expert-level site reliability engineering, SLOs, incident management, and operational excellence
category: devops
tags: [sre, reliability, monitoring, incident-management, slo, observability]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(*)
---

# Site Reliability Engineering Expert

Expert guidance for SRE practices, reliability engineering, SLOs/SLIs, incident management, and operational excellence.

## Core Concepts

### SRE Fundamentals
- Service Level Objectives (SLOs)
- Service Level Indicators (SLIs)
- Error budgets
- Toil reduction
- Monitoring and alerting
- Capacity planning

### Reliability Practices
- Incident management
- Post-incident reviews (PIRs)
- On-call rotations
- Chaos engineering
- Disaster recovery
- Change management

### Automation
- Infrastructure as Code
- Configuration management
- Deployment automation
- Self-healing systems
- Runbook automation
- Automated remediation

## SLO/SLI Management

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict
import numpy as np

@dataclass
class SLI:
    """Service Level Indicator"""
    name: str
    description: str
    query: str
    unit: str  # 'percentage', 'milliseconds', etc.

@dataclass
class SLO:
    """Service Level Objective"""
    name: str
    sli: SLI
    target: float
    window_days: int

class SLOTracker:
    """Track and manage SLOs"""

    def __init__(self):
        self.slos: Dict[str, SLO] = {}
        self.measurements: Dict[str, List[Dict]] = {}

    def define_slo(self, slo: SLO):
        """Define a new SLO"""
        self.slos[slo.name] = slo
        self.measurements[slo.name] = []

    def record_measurement(self, slo_name: str, value: float, timestamp: datetime):
        """Record SLI measurement"""
        if slo_name in self.slos:
            self.measurements[slo_name].append({
                'value': value,
                'timestamp': timestamp
            })

    def calculate_slo_compliance(self, slo_name: str) -> Dict:
        """Calculate SLO compliance"""
        slo = self.slos.get(slo_name)
        if not slo:
            return {}

        measurements = self.measurements.get(slo_name, [])
        window_start = datetime.now() - timedelta(days=slo.window_days)

        recent_measurements = [
            m for m in measurements
            if m['timestamp'] > window_start
        ]

        if not recent_measurements:
            return {'status': 'no_data'}

        values = [m['value'] for m in recent_measurements]
        actual = np.mean(values)

        return {
            'slo_name': slo_name,
            'target': slo.target,
            'actual': actual,
            'compliant': actual >= slo.target,
            'window_days': slo.window_days,
            'sample_count': len(recent_measurements)
        }

    def calculate_error_budget(self, slo_name: str) -> Dict:
        """Calculate remaining error budget"""
        compliance = self.calculate_slo_compliance(slo_name)

        if compliance.get('status') == 'no_data':
            return {'status': 'no_data'}

        target = compliance['target']
        actual = compliance['actual']

        error_budget_target = 100 - target
        errors_actual = 100 - actual

        remaining = error_budget_target - errors_actual
        remaining_pct = (remaining / error_budget_target) * 100 if error_budget_target > 0 else 100

        return {
            'slo_name': slo_name,
            'error_budget_target': error_budget_target,
            'errors_actual': errors_actual,
            'remaining': remaining,
            'remaining_percentage': remaining_pct,
            'exhausted': remaining < 0
        }

# Example SLOs
def define_standard_slos() -> List[SLO]:
    """Define standard SLOs for a web service"""
    return [
        SLO(
            name="api_availability",
            sli=SLI(
                name="availability",
                description="Percentage of successful requests",
                query="sum(rate(http_requests_total{code!~'5..'}[5m])) / sum(rate(http_requests_total[5m])) * 100",
                unit="percentage"
            ),
            target=99.9,
            window_days=30
        ),
        SLO(
            name="api_latency",
            sli=SLI(
                name="latency_p95",
                description="95th percentile latency",
                query="histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))",
                unit="seconds"
            ),
            target=0.5,  # 500ms
            window_days=30
        )
    ]
```

## Incident Management

```python
from enum import Enum
from datetime import datetime
from typing import List, Optional

class Severity(Enum):
    SEV1 = "sev1"  # Critical
    SEV2 = "sev2"  # High
    SEV3 = "sev3"  # Medium
    SEV4 = "sev4"  # Low

class IncidentStatus(Enum):
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"

@dataclass
class Incident:
    incident_id: str
    title: str
    severity: Severity
    status: IncidentStatus
    started_at: datetime
    detected_at: datetime
    resolved_at: Optional[datetime]
    incident_commander: str
    responders: List[str]
    affected_services: List[str]
    timeline: List[Dict]
    root_cause: Optional[str] = None

class IncidentManager:
    """Manage incidents following SRE best practices"""

    def __init__(self):
        self.incidents: Dict[str, Incident] = {}

    def create_incident(self, incident: Incident) -> str:
        """Create new incident"""
        self.incidents[incident.incident_id] = incident

        # Notify on-call
        self.notify_oncall(incident)

        # Start incident timeline
        self.add_timeline_event(
            incident.incident_id,
            "Incident created",
            datetime.now()
        )

        return incident.incident_id

    def update_status(self, incident_id: str, new_status: IncidentStatus,
                     note: str):
        """Update incident status"""
        if incident_id in self.incidents:
            incident = self.incidents[incident_id]
            incident.status = new_status

            self.add_timeline_event(
                incident_id,
                f"Status changed to {new_status.value}: {note}",
                datetime.now()
            )

            if new_status == IncidentStatus.RESOLVED:
                incident.resolved_at = datetime.now()

    def add_timeline_event(self, incident_id: str, event: str,
                          timestamp: datetime):
        """Add event to incident timeline"""
        if incident_id in self.incidents:
            self.incidents[incident_id].timeline.append({
                'timestamp': timestamp,
                'event': event
            })

    def calculate_mttr(self, incident_id: str) -> Optional[float]:
        """Calculate Mean Time To Resolution"""
        incident = self.incidents.get(incident_id)

        if incident and incident.resolved_at:
            duration = incident.resolved_at - incident.detected_at
            return duration.total_seconds() / 60  # minutes

        return None

    def generate_incident_report(self, incident_id: str) -> Dict:
        """Generate incident report"""
        incident = self.incidents.get(incident_id)

        if not incident:
            return {}

        return {
            'incident_id': incident.incident_id,
            'title': incident.title,
            'severity': incident.severity.value,
            'status': incident.status.value,
            'duration_minutes': self.calculate_mttr(incident_id),
            'affected_services': incident.affected_services,
            'incident_commander': incident.incident_commander,
            'responders': incident.responders,
            'timeline': incident.timeline,
            'root_cause': incident.root_cause
        }

    def notify_oncall(self, incident: Incident):
        """Notify on-call engineer (integrate with PagerDuty, etc.)"""
        # Implementation would integrate with alerting system
        pass
```

## Monitoring and Alerting

```python
from prometheus_client import Counter, Histogram, Gauge
import time

# Metrics
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration')
active_connections = Gauge('active_connections', 'Number of active connections')

class MonitoringSystem:
    """Implement monitoring best practices"""

    def __init__(self):
        self.alerts = []

    def record_request(self, method: str, endpoint: str, status: int, duration: float):
        """Record HTTP request metrics"""
        request_count.labels(method=method, endpoint=endpoint, status=status).inc()
        request_duration.observe(duration)

    def define_alert(self, name: str, expression: str, threshold: float,
                    duration: str, severity: str) -> Dict:
        """Define alerting rule"""
        alert = {
            'name': name,
            'expression': expression,
            'threshold': threshold,
            'duration': duration,
            'severity': severity,
            'annotations': {
                'summary': f'{name} alert triggered',
                'runbook_url': f'https://runbooks.example.com/{name}'
            }
        }

        self.alerts.append(alert)
        return alert

    def check_golden_signals(self, metrics: Dict) -> Dict:
        """Check the four golden signals"""
        return {
            'latency': self._check_latency(metrics.get('latency', [])),
            'traffic': self._check_traffic(metrics.get('traffic', 0)),
            'errors': self._check_errors(metrics.get('error_rate', 0)),
            'saturation': self._check_saturation(metrics.get('cpu_usage', 0))
        }

    def _check_latency(self, latencies: List[float]) -> Dict:
        if not latencies:
            return {'status': 'unknown'}

        p95 = np.percentile(latencies, 95)
        return {
            'status': 'critical' if p95 > 1000 else 'ok',
            'p95_ms': p95
        }

    def _check_traffic(self, requests_per_second: float) -> Dict:
        return {
            'status': 'ok',
            'rps': requests_per_second
        }

    def _check_errors(self, error_rate: float) -> Dict:
        return {
            'status': 'critical' if error_rate > 1.0 else 'ok',
            'error_rate': error_rate
        }

    def _check_saturation(self, cpu_usage: float) -> Dict:
        return {
            'status': 'warning' if cpu_usage > 80 else 'ok',
            'cpu_usage': cpu_usage
        }
```

## Chaos Engineering

```python
import random
from typing import Callable

class ChaosExperiment:
    """Run chaos engineering experiments"""

    def __init__(self, name: str, hypothesis: str):
        self.name = name
        self.hypothesis = hypothesis
        self.results = []

    def inject_latency(self, service_call: Callable, delay_ms: int):
        """Inject latency into service call"""
        time.sleep(delay_ms / 1000)
        return service_call()

    def inject_failure(self, service_call: Callable, failure_rate: float):
        """Randomly fail service calls"""
        if random.random() < failure_rate:
            raise Exception("Chaos: Simulated failure")
        return service_call()

    def kill_random_instance(self, instances: List[str]) -> str:
        """Kill random instance"""
        victim = random.choice(instances)
        # Implementation would actually kill the instance
        return victim

    def run_experiment(self, experiment_func: Callable) -> Dict:
        """Run chaos experiment"""
        start_time = datetime.now()

        try:
            result = experiment_func()
            status = "success"
            error = None
        except Exception as e:
            result = None
            status = "failed"
            error = str(e)

        end_time = datetime.now()

        experiment_result = {
            'name': self.name,
            'hypothesis': self.hypothesis,
            'status': status,
            'result': result,
            'error': error,
            'duration': (end_time - start_time).total_seconds(),
            'timestamp': start_time
        }

        self.results.append(experiment_result)
        return experiment_result
```

## Best Practices

### SRE Principles
- Embrace risk management
- Set SLOs based on user experience
- Use error budgets for decision making
- Automate toil away
- Monitor the four golden signals
- Practice blameless post-mortems
- Gradual rollouts and canary deployments

### Incident Management
- Clear incident severity definitions
- Defined incident commander role
- Communicate proactively
- Document timeline during incident
- Conduct post-incident reviews
- Track action items to completion
- Share learnings across teams

### On-Call
- Reasonable on-call rotations
- Comprehensive runbooks
- Alert on symptoms, not causes
- Actionable alerts only
- Escalation policies
- Support on-call engineers
- Measure and reduce alert fatigue

## Anti-Patterns

❌ No SLOs defined
❌ Alerts without runbooks
❌ Blame culture for incidents
❌ No post-incident reviews
❌ 100% uptime expectations
❌ Toil not tracked or reduced
❌ Manual processes for common tasks

## Resources

- Google SRE Book: https://sre.google/sre-book/table-of-contents/
- Site Reliability Engineering: https://sre.google/
- SLO Workshop: https://github.com/google/slo-workshop
- Chaos Engineering: https://principlesofchaos.org/
- Prometheus: https://prometheus.io/
