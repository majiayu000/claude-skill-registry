---
name: construction-expert
version: 1.0.0
description: Expert-level construction management, project planning, BIM, safety compliance, and construction technology
category: domains
tags: [construction, bim, project-management, safety, building]
allowed-tools:
  - Read
  - Write
  - Edit
---

# Construction Expert

Expert guidance for construction management, project planning, Building Information Modeling (BIM), safety compliance, and modern construction technology solutions.

## Core Concepts

### Construction Management
- Project planning and scheduling
- Cost estimation and control
- Resource management
- Quality assurance
- Contract management
- Risk management
- Change order management

### Technologies
- Building Information Modeling (BIM)
- Construction management software
- Drone surveying and inspection
- 3D printing and modular construction
- IoT sensors for monitoring
- Augmented reality for visualization
- Construction robotics

### Standards and Regulations
- OSHA safety regulations
- Building codes (IBC, IRC)
- AIA contracts and standards
- LEED certification
- ISO 19650 (BIM standards)
- CSI MasterFormat
- Environmental regulations

## Project Management System

```python
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from decimal import Decimal
from enum import Enum

class ProjectPhase(Enum):
    PRE_CONSTRUCTION = "pre_construction"
    SITE_PREPARATION = "site_preparation"
    FOUNDATION = "foundation"
    FRAMING = "framing"
    MEP = "mep"  # Mechanical, Electrical, Plumbing
    INTERIOR = "interior"
    EXTERIOR = "exterior"
    FINAL = "final"
    CLOSEOUT = "closeout"

class TaskStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    ON_HOLD = "on_hold"

@dataclass
class ConstructionProject:
    """Construction project information"""
    project_id: str
    project_name: str
    location: dict
    project_type: str  # 'residential', 'commercial', 'industrial'
    owner: str
    general_contractor: str
    start_date: datetime
    planned_end_date: datetime
    actual_end_date: Optional[datetime]
    budget: Decimal
    current_cost: Decimal
    square_footage: float
    current_phase: ProjectPhase

@dataclass
class Task:
    """Construction task/activity"""
    task_id: str
    project_id: str
    name: str
    description: str
    phase: ProjectPhase
    status: TaskStatus
    assigned_to: str  # Subcontractor or crew
    planned_start: datetime
    planned_end: datetime
    actual_start: Optional[datetime]
    actual_end: Optional[datetime]
    budget: Decimal
    actual_cost: Decimal
    predecessors: List[str]  # Task IDs that must complete first
    progress_percent: float

class ConstructionManagementSystem:
    """Construction project management system"""

    def __init__(self):
        self.projects = {}
        self.tasks = {}
        self.change_orders = []
        self.inspections = []

    def create_project_schedule(self, project_id: str, tasks_data: List[dict]) -> dict:
        """Create project schedule using Critical Path Method"""
        project = self.projects.get(project_id)
        if not project:
            return {'error': 'Project not found'}

        # Create tasks
        tasks = []
        for task_data in tasks_data:
            task = Task(
                task_id=self._generate_task_id(),
                project_id=project_id,
                name=task_data['name'],
                description=task_data.get('description', ''),
                phase=ProjectPhase(task_data['phase']),
                status=TaskStatus.NOT_STARTED,
                assigned_to=task_data['assigned_to'],
                planned_start=task_data['planned_start'],
                planned_end=task_data['planned_end'],
                actual_start=None,
                actual_end=None,
                budget=Decimal(str(task_data['budget'])),
                actual_cost=Decimal('0'),
                predecessors=task_data.get('predecessors', []),
                progress_percent=0.0
            )
            tasks.append(task)
            self.tasks[task.task_id] = task

        # Calculate critical path
        critical_path = self._calculate_critical_path(tasks)

        # Calculate project duration
        if tasks:
            project_end = max(t.planned_end for t in tasks)
            project_duration = (project_end - project.start_date).days
        else:
            project_duration = 0

        return {
            'project_id': project_id,
            'total_tasks': len(tasks),
            'project_duration_days': project_duration,
            'critical_path': [t.task_id for t in critical_path],
            'critical_path_duration': sum(
                (t.planned_end - t.planned_start).days for t in critical_path
            )
        }

    def _calculate_critical_path(self, tasks: List[Task]) -> List[Task]:
        """Calculate critical path through project network"""
        # Simplified critical path calculation
        # In production, would use proper CPM algorithm

        # Find tasks with no predecessors
        start_tasks = [t for t in tasks if not t.predecessors]

        # Find longest path through network
        critical_path = []
        current_tasks = start_tasks

        while current_tasks:
            # Find task with longest duration
            longest_task = max(current_tasks,
                             key=lambda t: (t.planned_end - t.planned_start).days)
            critical_path.append(longest_task)

            # Find successors
            current_tasks = [
                t for t in tasks
                if longest_task.task_id in t.predecessors
            ]

        return critical_path

    def track_progress(self, project_id: str) -> dict:
        """Track project progress and performance"""
        project = self.projects.get(project_id)
        if not project:
            return {'error': 'Project not found'}

        project_tasks = [t for t in self.tasks.values() if t.project_id == project_id]

        # Calculate overall progress
        if project_tasks:
            overall_progress = sum(t.progress_percent for t in project_tasks) / len(project_tasks)
        else:
            overall_progress = 0.0

        # Calculate schedule performance
        total_planned_days = (project.planned_end_date - project.start_date).days
        elapsed_days = (datetime.now() - project.start_date).days
        planned_progress = (elapsed_days / total_planned_days * 100) if total_planned_days > 0 else 0

        schedule_variance = overall_progress - planned_progress

        # Calculate cost performance
        cost_variance = project.budget - project.current_cost
        cost_performance_index = float(project.budget / project.current_cost) if project.current_cost > 0 else 1.0

        # Calculate estimated completion date
        if overall_progress > 0:
            estimated_total_days = elapsed_days / (overall_progress / 100)
            estimated_completion = project.start_date + timedelta(days=estimated_total_days)
        else:
            estimated_completion = project.planned_end_date

        return {
            'project_id': project_id,
            'overall_progress_percent': overall_progress,
            'schedule_variance_percent': schedule_variance,
            'schedule_status': 'ahead' if schedule_variance > 0 else 'behind' if schedule_variance < 0 else 'on_track',
            'cost_variance': float(cost_variance),
            'cost_performance_index': cost_performance_index,
            'budget_status': 'under' if cost_variance > 0 else 'over',
            'estimated_completion': estimated_completion.isoformat(),
            'days_variance': (estimated_completion - project.planned_end_date).days
        }

    def manage_change_order(self, project_id: str, change_data: dict) -> dict:
        """Manage construction change orders"""
        project = self.projects.get(project_id)
        if not project:
            return {'error': 'Project not found'}

        change_order = {
            'co_id': self._generate_co_id(),
            'project_id': project_id,
            'description': change_data['description'],
            'reason': change_data['reason'],
            'cost_impact': Decimal(str(change_data['cost_impact'])),
            'schedule_impact_days': change_data.get('schedule_impact_days', 0),
            'submitted_by': change_data['submitted_by'],
            'submitted_date': datetime.now(),
            'status': 'pending_approval',
            'approved': False
        }

        self.change_orders.append(change_order)

        return {
            'change_order_id': change_order['co_id'],
            'cost_impact': float(change_order['cost_impact']),
            'schedule_impact_days': change_order['schedule_impact_days'],
            'new_budget': float(project.budget + change_order['cost_impact']),
            'new_completion_date': (
                project.planned_end_date + timedelta(days=change_order['schedule_impact_days'])
            ).isoformat()
        }

    def estimate_costs(self, project_type: str, square_footage: float, specifications: dict) -> dict:
        """Estimate construction costs"""
        # Cost per square foot by project type
        base_costs = {
            'residential_basic': Decimal('150'),
            'residential_luxury': Decimal('300'),
            'commercial_office': Decimal('200'),
            'industrial_warehouse': Decimal('75')
        }

        base_cost_per_sf = base_costs.get(project_type, Decimal('150'))

        # Calculate base cost
        base_cost = base_cost_per_sf * Decimal(str(square_footage))

        # Add complexity factors
        complexity_factor = Decimal('1.0')

        if specifications.get('custom_design', False):
            complexity_factor += Decimal('0.15')

        if specifications.get('sustainable_materials', False):
            complexity_factor += Decimal('0.10')

        if specifications.get('complex_site', False):
            complexity_factor += Decimal('0.20')

        adjusted_cost = base_cost * complexity_factor

        # Add contingency (10%)
        contingency = adjusted_cost * Decimal('0.10')

        # Breakdown by category
        breakdown = {
            'site_work': float(adjusted_cost * Decimal('0.08')),
            'foundation': float(adjusted_cost * Decimal('0.12')),
            'structure': float(adjusted_cost * Decimal('0.25')),
            'exterior': float(adjusted_cost * Decimal('0.15')),
            'interior': float(adjusted_cost * Decimal('0.20')),
            'mep': float(adjusted_cost * Decimal('0.20'))
        }

        total_estimate = adjusted_cost + contingency

        return {
            'project_type': project_type,
            'square_footage': square_footage,
            'base_cost_per_sf': float(base_cost_per_sf),
            'complexity_factor': float(complexity_factor),
            'adjusted_cost': float(adjusted_cost),
            'contingency': float(contingency),
            'total_estimate': float(total_estimate),
            'cost_breakdown': breakdown
        }

    def _generate_task_id(self) -> str:
        import uuid
        return f"TASK-{uuid.uuid4().hex[:8].upper()}"

    def _generate_co_id(self) -> str:
        import uuid
        return f"CO-{uuid.uuid4().hex[:6].upper()}"
```

## Safety Management System

```python
@dataclass
class SafetyIncident:
    """Safety incident report"""
    incident_id: str
    project_id: str
    incident_type: str  # 'injury', 'near_miss', 'property_damage'
    severity: str  # 'minor', 'moderate', 'severe', 'fatal'
    description: str
    location: str
    occurred_at: datetime
    reported_by: str
    injured_person: Optional[str]
    root_cause: Optional[str]
    corrective_actions: List[str]

class SafetyManagementSystem:
    """Construction safety management"""

    def __init__(self):
        self.incidents = []
        self.safety_inspections = []
        self.training_records = []

    def conduct_safety_inspection(self, project_id: str, inspector: str) -> dict:
        """Conduct safety inspection"""
        inspection_items = [
            'Personal protective equipment (PPE)',
            'Fall protection systems',
            'Scaffolding integrity',
            'Electrical safety',
            'Equipment guarding',
            'Housekeeping',
            'Fire prevention',
            'First aid availability',
            'Emergency exits',
            'Signage and barriers'
        ]

        violations = []
        passed_items = []

        # Simulate inspection (in production, would be actual checklist)
        for item in inspection_items:
            # Random pass/fail for demonstration
            import random
            if random.random() < 0.85:  # 85% pass rate
                passed_items.append(item)
            else:
                violations.append({
                    'item': item,
                    'severity': random.choice(['minor', 'major']),
                    'action_required': 'Correct immediately' if random.random() < 0.3 else 'Correct within 24 hours'
                })

        inspection = {
            'inspection_id': self._generate_inspection_id(),
            'project_id': project_id,
            'inspector': inspector,
            'inspection_date': datetime.now(),
            'items_inspected': len(inspection_items),
            'items_passed': len(passed_items),
            'violations': violations,
            'overall_score': (len(passed_items) / len(inspection_items)) * 100,
            'status': 'pass' if len(violations) == 0 else 'fail'
        }

        self.safety_inspections.append(inspection)

        return inspection

    def report_incident(self, incident_data: dict) -> SafetyIncident:
        """Report safety incident"""
        incident = SafetyIncident(
            incident_id=self._generate_incident_id(),
            project_id=incident_data['project_id'],
            incident_type=incident_data['incident_type'],
            severity=incident_data['severity'],
            description=incident_data['description'],
            location=incident_data['location'],
            occurred_at=incident_data['occurred_at'],
            reported_by=incident_data['reported_by'],
            injured_person=incident_data.get('injured_person'),
            root_cause=None,
            corrective_actions=[]
        )

        self.incidents.append(incident)

        # Notify relevant parties
        self._notify_incident(incident)

        return incident

    def calculate_safety_metrics(self, project_id: str, hours_worked: float) -> dict:
        """Calculate safety performance metrics"""
        project_incidents = [
            i for i in self.incidents
            if i.project_id == project_id
        ]

        # Count recordable incidents
        recordable_incidents = [
            i for i in project_incidents
            if i.incident_type == 'injury' and i.severity in ['moderate', 'severe', 'fatal']
        ]

        # OSHA Incident Rate = (Number of incidents × 200,000) / Total hours worked
        if hours_worked > 0:
            incident_rate = (len(recordable_incidents) * 200000) / hours_worked
        else:
            incident_rate = 0

        # Days Away, Restricted, or Transferred (DART) Rate
        dart_incidents = [
            i for i in recordable_incidents
            if i.severity in ['severe', 'fatal']
        ]
        dart_rate = (len(dart_incidents) * 200000) / hours_worked if hours_worked > 0 else 0

        return {
            'project_id': project_id,
            'total_hours_worked': hours_worked,
            'total_incidents': len(project_incidents),
            'recordable_incidents': len(recordable_incidents),
            'incident_rate': incident_rate,
            'dart_rate': dart_rate,
            'safety_rating': 'Excellent' if incident_rate < 1.0 else
                           'Good' if incident_rate < 3.0 else
                           'Needs Improvement'
        }

    def _notify_incident(self, incident: SafetyIncident):
        """Notify stakeholders of incident"""
        # Implementation would send notifications
        pass

    def _generate_inspection_id(self) -> str:
        import uuid
        return f"INS-{uuid.uuid4().hex[:8].upper()}"

    def _generate_incident_id(self) -> str:
        import uuid
        return f"INC-{uuid.uuid4().hex[:8].upper()}"
```

## BIM Integration

```python
class BIMManagement:
    """Building Information Modeling management"""

    def __init__(self):
        self.models = {}
        self.clash_detections = []

    def perform_clash_detection(self, model_ids: List[str]) -> dict:
        """Detect clashes between BIM models"""
        # Simulate clash detection between disciplines
        # In production, would use BIM software APIs (Revit, Navisworks)

        clashes = [
            {
                'clash_id': 'CLASH-001',
                'type': 'hard',  # 'hard' or 'soft'
                'disciplines': ['structural', 'mep'],
                'description': 'Steel beam conflicts with HVAC duct',
                'location': 'Level 3, Grid B-4',
                'severity': 'high',
                'status': 'open'
            },
            {
                'clash_id': 'CLASH-002',
                'type': 'soft',
                'disciplines': ['architectural', 'mep'],
                'description': 'Insufficient clearance for plumbing access',
                'location': 'Level 2, Grid C-2',
                'severity': 'medium',
                'status': 'open'
            }
        ]

        return {
            'models_analyzed': model_ids,
            'total_clashes': len(clashes),
            'hard_clashes': len([c for c in clashes if c['type'] == 'hard']),
            'soft_clashes': len([c for c in clashes if c['type'] == 'soft']),
            'clashes': clashes
        }

    def extract_quantities(self, model_id: str) -> dict:
        """Extract material quantities from BIM model"""
        # Simulate quantity takeoff
        # In production, would extract from actual BIM model

        quantities = {
            'concrete': {
                'unit': 'cubic_yards',
                'quantity': 1250,
                'cost_per_unit': 150,
                'total_cost': 187500
            },
            'rebar': {
                'unit': 'tons',
                'quantity': 85,
                'cost_per_unit': 800,
                'total_cost': 68000
            },
            'structural_steel': {
                'unit': 'tons',
                'quantity': 120,
                'cost_per_unit': 1200,
                'total_cost': 144000
            }
        }

        total_cost = sum(item['total_cost'] for item in quantities.values())

        return {
            'model_id': model_id,
            'quantities': quantities,
            'total_estimated_cost': total_cost
        }
```

## Best Practices

### Project Management
- Use critical path method for scheduling
- Implement regular progress reviews
- Maintain detailed documentation
- Use integrated project delivery (IPD)
- Implement lean construction principles
- Track key performance indicators
- Conduct regular stakeholder meetings

### Cost Control
- Develop detailed estimates
- Track costs continuously
- Manage change orders effectively
- Use value engineering
- Implement cost coding systems
- Monitor cash flow
- Conduct regular audits

### Safety Management
- Implement comprehensive safety program
- Conduct regular toolbox talks
- Provide proper PPE
- Maintain OSHA compliance
- Investigate all incidents
- Track safety metrics
- Promote safety culture

### BIM Implementation
- Use BIM for clash detection
- Implement 4D scheduling
- Extract quantities from model
- Enable collaboration
- Maintain model coordination
- Use BIM for facility management
- Follow ISO 19650 standards

## Anti-Patterns

❌ Poor project planning
❌ Inadequate cost tracking
❌ No safety program
❌ Poor communication
❌ Ignoring change orders
❌ No quality control
❌ Inadequate documentation
❌ Poor subcontractor management
❌ No risk management

## Resources

- AIA (American Institute of Architects): https://www.aia.org/
- AGC (Associated General Contractors): https://www.agc.org/
- OSHA: https://www.osha.gov/construction
- International Building Code: https://www.iccsafe.org/
- buildingSMART (BIM): https://www.buildingsmart.org/
- PMI Construction Extension: https://www.pmi.org/
- LEED Certification: https://www.usgbc.org/leed
