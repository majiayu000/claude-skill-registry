---
name: google-sre
description: Apply Google's Site Reliability Engineering methodology. Emphasizes error budgets, SLO-driven operations, toil elimination, and blameless postmortems. Use when building and operating reliable services at scale.
---

# Google Site Reliability Engineering (SRE)

## Overview

Site Reliability Engineering (SRE) is Google's approach to running production systems. It applies software engineering principles to operations, treating reliability as a feature that can be measured, budgeted, and engineered.

## References

- **Book**: "Site Reliability Engineering: How Google Runs Production Systems" (O'Reilly, 2016)
- **Workbook**: "The Site Reliability Workbook" (O'Reilly, 2018)
- **Online**: https://sre.google/

## Core Philosophy

> "Hope is not a strategy."

> "SRE is what happens when you ask a software engineer to design an operations function."

> "Reliability is the most important feature."

SRE balances the tension between development velocity and system reliability using measurable objectives and error budgets.

## Key Concepts

### The Service Level Hierarchy

```
SLI (Service Level Indicator)
    ↓ Quantitative measure of service
    ↓ Example: "Request latency < 100ms"

SLO (Service Level Objective)  
    ↓ Target value for SLI
    ↓ Example: "99.9% of requests < 100ms"

SLA (Service Level Agreement)
    ↓ Contract with consequences
    ↓ Example: "If SLO missed, credits issued"

Error Budget = 100% - SLO
    Example: 99.9% SLO = 0.1% error budget = 43 minutes/month downtime
```

### Error Budget Philosophy

```
Error Budget Remaining?
        │
    ┌───┴───┐
    │       │
   YES      NO
    │       │
    ↓       ↓
 Ship new   Focus on
 features   reliability
```

## Design Principles

1. **Embrace Risk**: 100% reliability is wrong target; it's too expensive.

2. **Error Budgets**: Explicit budget for unreliability enables velocity.

3. **Eliminate Toil**: Automate repetitive operational work.

4. **Simplicity**: Simple systems are more reliable.

## When Implementing

### Always

- Define SLIs before launching a service
- Set SLOs based on user needs, not engineering pride
- Track error budget consumption
- Measure and reduce toil
- Conduct blameless postmortems
- Automate incident response where possible

### Never

- Set SLOs at 100% (it's impossible and wrong)
- Ignore SLO violations
- Blame individuals for outages
- Accept toil as "just how things are"
- Skip postmortems for "small" incidents

### Prefer

- Automation over manual processes
- Gradual rollouts over big-bang deploys
- Monitoring over hoping
- Documentation over tribal knowledge
- Proactive work over reactive firefighting

## Implementation Patterns

### Defining SLIs and SLOs

```python
# slo_definitions.py
# Define service level indicators and objectives

from dataclasses import dataclass
from enum import Enum
from typing import Optional

class SLIType(Enum):
    AVAILABILITY = "availability"
    LATENCY = "latency"
    THROUGHPUT = "throughput"
    ERROR_RATE = "error_rate"
    FRESHNESS = "freshness"

@dataclass
class SLI:
    """Service Level Indicator - what we measure"""
    name: str
    type: SLIType
    description: str
    good_event_query: str      # Events that are "good"
    total_event_query: str     # All events
    
    def calculate(self, good_count: int, total_count: int) -> float:
        if total_count == 0:
            return 1.0
        return good_count / total_count

@dataclass
class SLO:
    """Service Level Objective - our target"""
    sli: SLI
    target: float              # e.g., 0.999 for 99.9%
    window_days: int           # Rolling window
    
    @property
    def error_budget(self) -> float:
        """How much unreliability we can tolerate"""
        return 1.0 - self.target
    
    def budget_remaining(self, current_sli: float) -> float:
        """What percentage of error budget remains"""
        errors_used = 1.0 - current_sli
        if self.error_budget == 0:
            return 0.0
        return max(0, 1.0 - (errors_used / self.error_budget))


# Example SLO definitions
availability_sli = SLI(
    name="api_availability",
    type=SLIType.AVAILABILITY,
    description="Proportion of successful API requests",
    good_event_query="http_status < 500",
    total_event_query="all requests"
)

availability_slo = SLO(
    sli=availability_sli,
    target=0.999,        # 99.9% availability
    window_days=30       # Rolling 30-day window
)

# 99.9% over 30 days = 43 minutes of allowed downtime
```

### Error Budget Tracking

```python
# error_budget.py
# Track and alert on error budget consumption

import time
from dataclasses import dataclass
from typing import List
from datetime import datetime, timedelta

@dataclass
class ErrorBudgetTracker:
    slo: 'SLO'
    window_seconds: int
    
    def __init__(self, slo: 'SLO'):
        self.slo = slo
        self.window_seconds = slo.window_days * 24 * 60 * 60
        self.events: List[tuple] = []  # (timestamp, is_good)
    
    def record_event(self, is_good: bool):
        """Record an event"""
        now = time.time()
        self.events.append((now, is_good))
        self._prune_old_events(now)
    
    def _prune_old_events(self, now: float):
        """Remove events outside window"""
        cutoff = now - self.window_seconds
        self.events = [(t, g) for t, g in self.events if t > cutoff]
    
    def current_sli(self) -> float:
        """Calculate current SLI value"""
        if not self.events:
            return 1.0
        good = sum(1 for _, is_good in self.events if is_good)
        return good / len(self.events)
    
    def budget_remaining_percent(self) -> float:
        """Percentage of error budget remaining"""
        return self.slo.budget_remaining(self.current_sli()) * 100
    
    def time_until_budget_exhausted(self) -> Optional[timedelta]:
        """Estimate when budget will be exhausted at current burn rate"""
        remaining = self.budget_remaining_percent()
        if remaining <= 0:
            return timedelta(0)
        
        # Calculate burn rate (budget consumed per hour)
        # This is simplified - real implementation needs more data
        return None  # Requires historical burn rate
    
    def should_freeze_deployments(self) -> bool:
        """Should we stop deploying new features?"""
        return self.budget_remaining_percent() < 10  # Less than 10% remaining


# Alert policies based on error budget
def create_error_budget_alerts(tracker: ErrorBudgetTracker):
    """Create tiered alerts for error budget consumption"""
    remaining = tracker.budget_remaining_percent()
    
    if remaining < 0:
        return "CRITICAL: Error budget exhausted! Focus 100% on reliability."
    elif remaining < 10:
        return "WARNING: Error budget nearly exhausted. Freeze deployments."
    elif remaining < 25:
        return "CAUTION: Error budget below 25%. Review recent changes."
    elif remaining < 50:
        return "INFO: Error budget at 50%. Monitor closely."
    else:
        return "OK: Error budget healthy. Safe to ship features."
```

### Toil Measurement and Elimination

```python
# toil_tracker.py
# Measure and track operational toil

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict
from datetime import datetime, timedelta

class ToilCategory(Enum):
    MANUAL = "manual"           # Could be automated
    REPETITIVE = "repetitive"   # Done frequently
    TACTICAL = "tactical"       # Reactive, not strategic
    NO_VALUE = "no_value"       # Doesn't improve service
    SCALES_LINEARLY = "scales"  # Grows with service size

@dataclass
class ToilTask:
    name: str
    categories: List[ToilCategory]
    time_spent_minutes: int
    frequency_per_week: float
    automation_possible: bool
    automation_effort_days: float
    
    @property
    def weekly_toil_hours(self) -> float:
        return (self.time_spent_minutes * self.frequency_per_week) / 60
    
    @property
    def automation_roi_weeks(self) -> float:
        """Weeks until automation pays off"""
        if not self.automation_possible:
            return float('inf')
        
        effort_hours = self.automation_effort_days * 8
        return effort_hours / self.weekly_toil_hours

@dataclass 
class ToilBudget:
    """SRE teams should spend <50% time on toil"""
    team_size: int
    hours_per_week: int = 40
    max_toil_percent: float = 0.50
    
    @property
    def max_toil_hours_per_week(self) -> float:
        return self.team_size * self.hours_per_week * self.max_toil_percent
    
    def is_over_budget(self, current_toil_hours: float) -> bool:
        return current_toil_hours > self.max_toil_hours_per_week


class ToilTracker:
    def __init__(self, budget: ToilBudget):
        self.budget = budget
        self.tasks: Dict[str, ToilTask] = {}
    
    def add_task(self, task: ToilTask):
        self.tasks[task.name] = task
    
    def total_weekly_toil(self) -> float:
        return sum(t.weekly_toil_hours for t in self.tasks.values())
    
    def toil_percent(self) -> float:
        max_hours = self.budget.team_size * self.budget.hours_per_week
        return (self.total_weekly_toil() / max_hours) * 100
    
    def automation_priorities(self) -> List[ToilTask]:
        """Rank tasks by automation ROI"""
        automatable = [t for t in self.tasks.values() if t.automation_possible]
        return sorted(automatable, key=lambda t: t.automation_roi_weeks)
    
    def report(self) -> str:
        report = []
        report.append(f"Total weekly toil: {self.total_weekly_toil():.1f} hours")
        report.append(f"Toil percentage: {self.toil_percent():.1f}%")
        report.append(f"Budget: {self.budget.max_toil_percent * 100}%")
        report.append(f"Status: {'OVER' if self.toil_percent() > 50 else 'OK'}")
        report.append("\nTop automation targets:")
        for task in self.automation_priorities()[:5]:
            report.append(f"  - {task.name}: {task.automation_roi_weeks:.1f} weeks to ROI")
        return "\n".join(report)
```

### Blameless Postmortem Template

```markdown
# Postmortem: [Incident Title]

**Date**: YYYY-MM-DD
**Authors**: [Names]
**Status**: Draft | In Review | Complete
**Severity**: P0 | P1 | P2 | P3

## Summary

[2-3 sentences describing what happened, impact, and resolution]

## Impact

- **Duration**: X hours Y minutes
- **Users affected**: N users / X% of traffic
- **Revenue impact**: $X (if applicable)
- **Error budget consumed**: X%

## Timeline (all times UTC)

| Time | Event |
|------|-------|
| HH:MM | First alert fired |
| HH:MM | On-call engaged |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Service fully recovered |

## Root Cause

[Technical explanation of what caused the incident]

## Resolution

[What was done to resolve the incident]

## Detection

- How was the incident detected?
- Could we have detected it sooner?
- What monitoring would have helped?

## Lessons Learned

### What went well

- [Things that worked]

### What went wrong

- [Things that didn't work]

### Where we got lucky

- [Things that could have made it worse]

## Action Items

| Action | Type | Owner | Due Date | Status |
|--------|------|-------|----------|--------|
| Add monitoring for X | Detect | @name | YYYY-MM-DD | TODO |
| Implement circuit breaker | Mitigate | @name | YYYY-MM-DD | TODO |
| Update runbook | Process | @name | YYYY-MM-DD | TODO |

## Supporting Information

- Relevant logs, graphs, or documentation
- Links to related incidents
```

### On-Call Rotation Best Practices

```python
# oncall.py
# On-call rotation management

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

@dataclass
class OnCallShift:
    engineer: str
    start: datetime
    end: datetime
    
    @property
    def duration_hours(self) -> float:
        return (self.end - self.start).total_seconds() / 3600

@dataclass
class OnCallPolicy:
    """Google SRE on-call best practices"""
    
    # Shift structure
    max_shift_hours: int = 12          # No more than 12 hours
    min_time_between_shifts: int = 12  # At least 12 hours rest
    max_incidents_per_shift: int = 2   # Escalate if exceeded
    
    # Team structure
    min_team_size: int = 8             # For sustainable rotation
    secondary_oncall: bool = True      # Always have backup
    
    # Compensation
    time_off_per_incident: float = 0.5 # Hours of comp time
    
    def validate_shift(self, shift: OnCallShift, 
                       previous_shifts: List[OnCallShift]) -> List[str]:
        """Check shift against policy"""
        violations = []
        
        if shift.duration_hours > self.max_shift_hours:
            violations.append(
                f"Shift too long: {shift.duration_hours}h > {self.max_shift_hours}h"
            )
        
        # Check rest time
        for prev in previous_shifts:
            if prev.engineer == shift.engineer:
                gap = (shift.start - prev.end).total_seconds() / 3600
                if gap < self.min_time_between_shifts:
                    violations.append(
                        f"Insufficient rest: {gap}h < {self.min_time_between_shifts}h"
                    )
        
        return violations

    def calculate_comp_time(self, incidents_handled: int) -> float:
        """Calculate compensation time for incidents"""
        return incidents_handled * self.time_off_per_incident
```

## Mental Model

Google SRE asks:

1. **What's the SLO?** Reliability target based on user needs
2. **What's the error budget?** How much unreliability can we afford?
3. **Is this toil?** Manual, repetitive, automatable, no lasting value?
4. **What does the postmortem say?** Learn from failures, don't blame
5. **Can we ship this safely?** Gradual rollout with monitoring

## Signature SRE Moves

- Error budgets to balance reliability and velocity
- SLI/SLO/SLA hierarchy for clear targets
- Toil tracking and elimination
- Blameless postmortems
- On-call that doesn't burn out engineers
- Automation as first response to toil
