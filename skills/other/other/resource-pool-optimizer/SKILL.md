---
slug: "resource-pool-optimizer"
display_name: "Resource Pool Optimizer"
description: "Optimize shared resource pools across multiple construction projects. Balance resource allocation, minimize conflicts, and maximize utilization across the portfolio."
---

# Resource Pool Optimizer

## Overview

Manage and optimize shared resources (equipment, specialized labor, materials) across multiple construction projects. Identify conflicts, balance allocations, and maximize resource utilization while minimizing idle time and project delays.

## Resource Pool Concept

```
┌─────────────────────────────────────────────────────────────────┐
│                  RESOURCE POOL OPTIMIZATION                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  RESOURCE POOL                    PROJECTS                      │
│  ─────────────                    ────────                      │
│  🏗️ Tower Crane A    ───────────→  Project 1 (Weeks 1-8)       │
│  🏗️ Tower Crane B    ───────────→  Project 2 (Weeks 3-12)      │
│  🔧 Excavator Fleet  ─────┬─────→  Project 1 (Weeks 1-4)       │
│                           └─────→  Project 3 (Weeks 5-10)       │
│  👷 Steel Crew A     ───────────→  Project 2 (Weeks 6-15)      │
│  👷 Steel Crew B     ─────┬─────→  Project 1 (Weeks 8-14)      │
│                           └─────→  Project 3 (Weeks 15-20)      │
│                                                                  │
│  OPTIMIZATION GOALS:                                            │
│  • Minimize idle time between projects                          │
│  • Avoid double-booking conflicts                               │
│  • Prioritize critical path activities                          │
│  • Balance utilization across resources                         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Set
from datetime import datetime, timedelta
from enum import Enum
import heapq

class ResourceType(Enum):
    EQUIPMENT = "equipment"
    LABOR_CREW = "labor_crew"
    MATERIAL = "material"
    SPECIALTY = "specialty"

class AllocationStatus(Enum):
    AVAILABLE = "available"
    ALLOCATED = "allocated"
    MAINTENANCE = "maintenance"
    CONFLICT = "conflict"

class Priority(Enum):
    CRITICAL = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4

@dataclass
class Resource:
    id: str
    name: str
    resource_type: ResourceType
    capacity: float = 1.0  # Can be split (e.g., crew size)
    daily_cost: float = 0.0
    home_location: str = ""
    mobilization_days: int = 1
    skills: List[str] = field(default_factory=list)

@dataclass
class ResourceRequest:
    id: str
    project_id: str
    project_name: str
    resource_type: ResourceType
    required_skills: List[str]
    start_date: datetime
    end_date: datetime
    quantity_needed: float = 1.0
    priority: Priority = Priority.NORMAL
    is_critical_path: bool = False
    flexibility_days: int = 0  # Can shift by this many days
    notes: str = ""

@dataclass
class Allocation:
    id: str
    resource_id: str
    request_id: str
    project_id: str
    start_date: datetime
    end_date: datetime
    quantity: float
    status: AllocationStatus = AllocationStatus.ALLOCATED

@dataclass
class Conflict:
    resource_id: str
    resource_name: str
    date: datetime
    requests: List[ResourceRequest]
    total_demand: float
    available: float
    resolution_options: List[str]

@dataclass
class UtilizationReport:
    resource_id: str
    resource_name: str
    period_start: datetime
    period_end: datetime
    total_days: int
    allocated_days: int
    utilization_pct: float
    idle_periods: List[Tuple[datetime, datetime]]
    cost: float

class ResourcePoolOptimizer:
    """Optimize shared resources across projects."""

    def __init__(self, pool_name: str):
        self.pool_name = pool_name
        self.resources: Dict[str, Resource] = {}
        self.requests: Dict[str, ResourceRequest] = {}
        self.allocations: Dict[str, Allocation] = {}

    def add_resource(self, id: str, name: str, resource_type: ResourceType,
                    capacity: float = 1.0, daily_cost: float = 0.0,
                    skills: List[str] = None) -> Resource:
        """Add resource to pool."""
        resource = Resource(
            id=id,
            name=name,
            resource_type=resource_type,
            capacity=capacity,
            daily_cost=daily_cost,
            skills=skills or []
        )
        self.resources[id] = resource
        return resource

    def add_request(self, project_id: str, project_name: str,
                   resource_type: ResourceType, start_date: datetime,
                   end_date: datetime, quantity: float = 1.0,
                   priority: Priority = Priority.NORMAL,
                   required_skills: List[str] = None,
                   is_critical_path: bool = False,
                   flexibility_days: int = 0) -> ResourceRequest:
        """Add resource request from project."""
        request_id = f"REQ-{project_id}-{len(self.requests)+1:03d}"

        request = ResourceRequest(
            id=request_id,
            project_id=project_id,
            project_name=project_name,
            resource_type=resource_type,
            required_skills=required_skills or [],
            start_date=start_date,
            end_date=end_date,
            quantity_needed=quantity,
            priority=priority,
            is_critical_path=is_critical_path,
            flexibility_days=flexibility_days
        )
        self.requests[request_id] = request
        return request

    def find_available_resources(self, request: ResourceRequest) -> List[Tuple[Resource, float]]:
        """Find resources that can fulfill request."""
        available = []

        for resource in self.resources.values():
            # Check type match
            if resource.resource_type != request.resource_type:
                continue

            # Check skills match
            if request.required_skills:
                if not all(skill in resource.skills for skill in request.required_skills):
                    continue

            # Check availability
            available_qty = self._get_availability(
                resource.id, request.start_date, request.end_date
            )

            if available_qty > 0:
                available.append((resource, available_qty))

        return sorted(available, key=lambda x: -x[1])

    def _get_availability(self, resource_id: str, start: datetime, end: datetime) -> float:
        """Get available capacity for resource in period."""
        resource = self.resources.get(resource_id)
        if not resource:
            return 0

        # Find overlapping allocations
        allocated = 0
        for alloc in self.allocations.values():
            if alloc.resource_id != resource_id:
                continue

            # Check overlap
            if alloc.start_date < end and alloc.end_date > start:
                allocated = max(allocated, alloc.quantity)

        return resource.capacity - allocated

    def allocate(self, request_id: str, resource_id: str,
                quantity: float = None) -> Allocation:
        """Allocate resource to request."""
        if request_id not in self.requests:
            raise ValueError(f"Request {request_id} not found")
        if resource_id not in self.resources:
            raise ValueError(f"Resource {resource_id} not found")

        request = self.requests[request_id]
        resource = self.resources[resource_id]

        if quantity is None:
            quantity = min(request.quantity_needed, resource.capacity)

        # Check availability
        available = self._get_availability(
            resource_id, request.start_date, request.end_date
        )

        if available < quantity:
            raise ValueError(f"Insufficient capacity. Available: {available}, Requested: {quantity}")

        alloc_id = f"ALLOC-{len(self.allocations)+1:04d}"

        allocation = Allocation(
            id=alloc_id,
            resource_id=resource_id,
            request_id=request_id,
            project_id=request.project_id,
            start_date=request.start_date,
            end_date=request.end_date,
            quantity=quantity
        )

        self.allocations[alloc_id] = allocation
        return allocation

    def auto_allocate(self) -> Dict[str, List[Allocation]]:
        """Automatically allocate resources using priority-based algorithm."""
        results = {"allocated": [], "unallocated": [], "conflicts": []}

        # Sort requests by priority and critical path
        sorted_requests = sorted(
            self.requests.values(),
            key=lambda r: (r.priority.value, not r.is_critical_path, r.start_date)
        )

        for request in sorted_requests:
            # Check if already allocated
            existing = [a for a in self.allocations.values()
                       if a.request_id == request.id]
            if existing:
                continue

            # Find available resources
            available = self.find_available_resources(request)

            if not available:
                results["unallocated"].append(request)
                continue

            # Allocate best match
            resource, qty = available[0]

            try:
                allocation = self.allocate(request.id, resource.id,
                                          min(request.quantity_needed, qty))
                results["allocated"].append(allocation)
            except ValueError:
                results["conflicts"].append(request)

        return results

    def detect_conflicts(self) -> List[Conflict]:
        """Detect resource conflicts across all requests."""
        conflicts = []

        # Group requests by resource type
        by_type: Dict[ResourceType, List[ResourceRequest]] = {}
        for req in self.requests.values():
            if req.resource_type not in by_type:
                by_type[req.resource_type] = []
            by_type[req.resource_type].append(req)

        # Check each resource type
        for resource_type, requests in by_type.items():
            # Get all resources of this type
            resources = [r for r in self.resources.values()
                        if r.resource_type == resource_type]
            total_capacity = sum(r.capacity for r in resources)

            # Check each day for conflicts
            all_dates = set()
            for req in requests:
                current = req.start_date
                while current <= req.end_date:
                    all_dates.add(current)
                    current += timedelta(days=1)

            for date in sorted(all_dates):
                # Sum demand for this date
                day_requests = [r for r in requests
                               if r.start_date <= date <= r.end_date]
                total_demand = sum(r.quantity_needed for r in day_requests)

                if total_demand > total_capacity:
                    # Generate resolution options
                    options = []
                    for req in sorted(day_requests, key=lambda x: x.priority.value, reverse=True):
                        if req.flexibility_days > 0:
                            options.append(f"Shift {req.project_name} by {req.flexibility_days} days")
                    options.append("Add additional resource")
                    options.append("Extend work hours")

                    conflict = Conflict(
                        resource_id=resource_type.value,
                        resource_name=resource_type.value,
                        date=date,
                        requests=day_requests,
                        total_demand=total_demand,
                        available=total_capacity,
                        resolution_options=options
                    )
                    conflicts.append(conflict)

        return conflicts

    def calculate_utilization(self, start_date: datetime,
                             end_date: datetime) -> List[UtilizationReport]:
        """Calculate utilization for all resources."""
        reports = []
        total_days = (end_date - start_date).days

        for resource in self.resources.values():
            # Find allocations in period
            allocs = [a for a in self.allocations.values()
                     if a.resource_id == resource.id
                     and a.start_date < end_date
                     and a.end_date > start_date]

            # Calculate allocated days
            allocated_dates = set()
            for alloc in allocs:
                current = max(alloc.start_date, start_date)
                while current < min(alloc.end_date, end_date):
                    allocated_dates.add(current)
                    current += timedelta(days=1)

            allocated_days = len(allocated_dates)
            utilization = (allocated_days / total_days * 100) if total_days > 0 else 0

            # Find idle periods
            idle_periods = []
            all_dates = set()
            current = start_date
            while current < end_date:
                all_dates.add(current)
                current += timedelta(days=1)

            idle_dates = sorted(all_dates - allocated_dates)
            if idle_dates:
                # Group consecutive idle dates
                period_start = idle_dates[0]
                for i, date in enumerate(idle_dates[1:], 1):
                    if (date - idle_dates[i-1]).days > 1:
                        idle_periods.append((period_start, idle_dates[i-1]))
                        period_start = date
                idle_periods.append((period_start, idle_dates[-1]))

            cost = allocated_days * resource.daily_cost

            reports.append(UtilizationReport(
                resource_id=resource.id,
                resource_name=resource.name,
                period_start=start_date,
                period_end=end_date,
                total_days=total_days,
                allocated_days=allocated_days,
                utilization_pct=utilization,
                idle_periods=idle_periods,
                cost=cost
            ))

        return sorted(reports, key=lambda x: -x.utilization_pct)

    def suggest_optimization(self) -> List[Dict]:
        """Suggest optimizations for resource allocation."""
        suggestions = []

        # Find underutilized resources
        util = self.calculate_utilization(
            datetime.now(),
            datetime.now() + timedelta(days=90)
        )

        for report in util:
            if report.utilization_pct < 50:
                suggestions.append({
                    "type": "underutilization",
                    "resource": report.resource_name,
                    "utilization": report.utilization_pct,
                    "suggestion": f"Consider reassigning or releasing {report.resource_name}"
                })

        # Find conflicts
        conflicts = self.detect_conflicts()
        for conflict in conflicts[:5]:
            suggestions.append({
                "type": "conflict",
                "date": conflict.date,
                "demand": conflict.total_demand,
                "available": conflict.available,
                "suggestion": conflict.resolution_options[0] if conflict.resolution_options else "Review allocation"
            })

        return suggestions

    def generate_report(self) -> str:
        """Generate resource pool report."""
        lines = [
            "# Resource Pool Optimization Report",
            "",
            f"**Pool:** {self.pool_name}",
            f"**Date:** {datetime.now().strftime('%Y-%m-%d')}",
            "",
            "## Resource Inventory",
            "",
            "| Resource | Type | Capacity | Daily Cost |",
            "|----------|------|----------|------------|"
        ]

        for r in self.resources.values():
            lines.append(
                f"| {r.name} | {r.resource_type.value} | {r.capacity} | ${r.daily_cost:,.0f} |"
            )

        lines.extend([
            "",
            "## Current Allocations",
            "",
            "| Resource | Project | Start | End | Qty |",
            "|----------|---------|-------|-----|-----|"
        ])

        for alloc in sorted(self.allocations.values(), key=lambda x: x.start_date):
            resource = self.resources.get(alloc.resource_id)
            lines.append(
                f"| {resource.name if resource else alloc.resource_id} | "
                f"{alloc.project_id} | {alloc.start_date.strftime('%Y-%m-%d')} | "
                f"{alloc.end_date.strftime('%Y-%m-%d')} | {alloc.quantity} |"
            )

        # Utilization
        util = self.calculate_utilization(
            datetime.now(),
            datetime.now() + timedelta(days=90)
        )

        lines.extend([
            "",
            "## 90-Day Utilization Forecast",
            "",
            "| Resource | Utilization | Idle Periods |",
            "|----------|-------------|--------------|"
        ])

        for report in util:
            idle_str = f"{len(report.idle_periods)} gaps" if report.idle_periods else "None"
            lines.append(
                f"| {report.resource_name} | {report.utilization_pct:.0f}% | {idle_str} |"
            )

        # Conflicts
        conflicts = self.detect_conflicts()
        if conflicts:
            lines.extend([
                "",
                f"## Conflicts Detected ({len(conflicts)})",
                "",
                "| Date | Resource | Demand | Available |",
                "|------|----------|--------|-----------|"
            ])
            for c in conflicts[:10]:
                lines.append(
                    f"| {c.date.strftime('%Y-%m-%d')} | {c.resource_name} | "
                    f"{c.total_demand} | {c.available} |"
                )

        return "\n".join(lines)
```

## Quick Start

```python
from datetime import datetime, timedelta

# Initialize optimizer
optimizer = ResourcePoolOptimizer("Regional Equipment Pool")

# Add resources
optimizer.add_resource("CR-001", "Tower Crane Alpha", ResourceType.EQUIPMENT,
                       capacity=1, daily_cost=2500)
optimizer.add_resource("CR-002", "Tower Crane Beta", ResourceType.EQUIPMENT,
                       capacity=1, daily_cost=2500)
optimizer.add_resource("EX-001", "Excavator Fleet", ResourceType.EQUIPMENT,
                       capacity=3, daily_cost=1500)
optimizer.add_resource("SC-001", "Steel Crew A", ResourceType.LABOR_CREW,
                       capacity=1, daily_cost=8000, skills=["structural", "welding"])

# Add requests from projects
optimizer.add_request(
    "PRJ-001", "Downtown Tower",
    ResourceType.EQUIPMENT,
    start_date=datetime(2025, 2, 1),
    end_date=datetime(2025, 6, 30),
    quantity=1,
    priority=Priority.HIGH,
    is_critical_path=True
)

optimizer.add_request(
    "PRJ-002", "Hospital Wing",
    ResourceType.EQUIPMENT,
    start_date=datetime(2025, 3, 1),
    end_date=datetime(2025, 8, 31),
    quantity=1,
    priority=Priority.NORMAL,
    flexibility_days=14
)

# Auto-allocate resources
results = optimizer.auto_allocate()
print(f"Allocated: {len(results['allocated'])}")
print(f"Unallocated: {len(results['unallocated'])}")

# Detect conflicts
conflicts = optimizer.detect_conflicts()
print(f"Conflicts: {len(conflicts)}")

# Get optimization suggestions
suggestions = optimizer.suggest_optimization()
for s in suggestions[:5]:
    print(f"{s['type']}: {s['suggestion']}")

# Generate report
print(optimizer.generate_report())
```

## Requirements

```bash
pip install (no external dependencies)
```
