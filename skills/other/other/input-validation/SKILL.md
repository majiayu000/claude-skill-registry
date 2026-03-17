---
slug: "input-validation"
display_name: "Input Validation"
description: "Validate construction data inputs before processing: cost estimates, schedules, BIM data, field reports. Catch errors early with domain-specific rules."
---

# Input Validation for Construction Data

## Overview

Validate incoming construction data before processing to catch errors early. Domain-specific validation rules for estimates, schedules, BIM exports, and field data.

## Validation Framework

### Core Validator Class

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Callable, Optional
from enum import Enum
import re
from datetime import datetime

class ValidationSeverity(Enum):
    ERROR = "error"      # Must fix, blocks processing
    WARNING = "warning"  # Should review, allows processing
    INFO = "info"        # FYI, no action needed

@dataclass
class ValidationIssue:
    field: str
    message: str
    severity: ValidationSeverity
    value: Any = None
    suggestion: str = None

@dataclass
class ValidationResult:
    is_valid: bool
    issues: List[ValidationIssue] = field(default_factory=list)

    def add_error(self, field: str, message: str, value: Any = None, suggestion: str = None):
        self.issues.append(ValidationIssue(field, message, ValidationSeverity.ERROR, value, suggestion))
        self.is_valid = False

    def add_warning(self, field: str, message: str, value: Any = None, suggestion: str = None):
        self.issues.append(ValidationIssue(field, message, ValidationSeverity.WARNING, value, suggestion))

    def add_info(self, field: str, message: str, value: Any = None):
        self.issues.append(ValidationIssue(field, message, ValidationSeverity.INFO, value))

    @property
    def errors(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == ValidationSeverity.ERROR]

    @property
    def warnings(self) -> List[ValidationIssue]:
        return [i for i in self.issues if i.severity == ValidationSeverity.WARNING]

    def to_report(self) -> str:
        lines = ["VALIDATION REPORT", "=" * 50]
        lines.append(f"Status: {'PASSED' if self.is_valid else 'FAILED'}")
        lines.append(f"Errors: {len(self.errors)}, Warnings: {len(self.warnings)}")
        lines.append("")

        for issue in self.issues:
            icon = "❌" if issue.severity == ValidationSeverity.ERROR else "⚠️" if issue.severity == ValidationSeverity.WARNING else "ℹ️"
            lines.append(f"{icon} [{issue.field}] {issue.message}")
            if issue.suggestion:
                lines.append(f"   Suggestion: {issue.suggestion}")

        return "\n".join(lines)
```

### Cost Estimate Validation

```python
class CostEstimateValidator:
    """Validate cost estimate inputs."""

    # Typical cost ranges per CSI division ($/SF)
    TYPICAL_RANGES = {
        '03': (15, 45),    # Concrete
        '04': (8, 25),     # Masonry
        '05': (12, 35),    # Metals
        '06': (5, 20),     # Wood/Plastics
        '07': (8, 30),     # Thermal/Moisture
        '08': (15, 50),    # Openings
        '09': (10, 40),    # Finishes
        '22': (8, 25),     # Plumbing
        '23': (12, 40),    # HVAC
        '26': (10, 35),    # Electrical
    }

    def validate(self, estimate_data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(is_valid=True)

        # Required fields
        self._validate_required_fields(estimate_data, result)

        # Line item validation
        if 'line_items' in estimate_data:
            self._validate_line_items(estimate_data['line_items'], result)

        # Total validation
        self._validate_totals(estimate_data, result)

        # Cost range validation
        if 'gross_area' in estimate_data:
            self._validate_cost_ranges(estimate_data, result)

        return result

    def _validate_required_fields(self, data: dict, result: ValidationResult):
        required = ['project_name', 'estimate_date', 'line_items', 'total']
        for field in required:
            if field not in data or data[field] is None:
                result.add_error(field, f"Required field '{field}' is missing")

    def _validate_line_items(self, items: list, result: ValidationResult):
        for i, item in enumerate(items):
            # Check for negative values
            if item.get('quantity', 0) < 0:
                result.add_error(f"line_items[{i}].quantity", "Quantity cannot be negative", item.get('quantity'))

            if item.get('unit_cost', 0) < 0:
                result.add_error(f"line_items[{i}].unit_cost", "Unit cost cannot be negative", item.get('unit_cost'))

            # Check for missing descriptions
            if not item.get('description'):
                result.add_warning(f"line_items[{i}].description", "Line item missing description")

            # Check for valid CSI code
            if item.get('csi_code'):
                if not re.match(r'^\d{2}\s?\d{2}\s?\d{2}$', item['csi_code']):
                    result.add_warning(f"line_items[{i}].csi_code", f"Invalid CSI code format: {item['csi_code']}", suggestion="Use format: XX XX XX")

            # Check for zero amounts
            amount = item.get('quantity', 0) * item.get('unit_cost', 0)
            if amount == 0:
                result.add_warning(f"line_items[{i}]", "Line item has zero amount")

    def _validate_totals(self, data: dict, result: ValidationResult):
        if 'line_items' not in data or 'total' not in data:
            return

        calculated = sum(
            item.get('quantity', 0) * item.get('unit_cost', 0)
            for item in data['line_items']
        )

        declared = data['total']
        variance = abs(calculated - declared)

        if variance > 0.01:
            result.add_error("total", f"Total mismatch: calculated {calculated:.2f}, declared {declared:.2f}", variance)

    def _validate_cost_ranges(self, data: dict, result: ValidationResult):
        gross_area = data['gross_area']

        for item in data.get('line_items', []):
            csi_div = item.get('csi_code', '')[:2]
            if csi_div in self.TYPICAL_RANGES:
                amount = item.get('quantity', 0) * item.get('unit_cost', 0)
                cost_per_sf = amount / gross_area if gross_area > 0 else 0

                low, high = self.TYPICAL_RANGES[csi_div]
                if cost_per_sf < low * 0.5 or cost_per_sf > high * 2:
                    result.add_warning(
                        f"line_items[{item.get('description', 'Unknown')}]",
                        f"Cost ${cost_per_sf:.2f}/SF outside typical range ${low}-${high}/SF for Division {csi_div}",
                        cost_per_sf,
                        "Review unit costs and quantities"
                    )
```

### Schedule Validation

```python
class ScheduleValidator:
    """Validate schedule/planning inputs."""

    def validate(self, schedule_data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(is_valid=True)

        # Required fields
        self._validate_required_fields(schedule_data, result)

        # Task validation
        if 'tasks' in schedule_data:
            self._validate_tasks(schedule_data['tasks'], result)
            self._validate_dependencies(schedule_data['tasks'], result)
            self._validate_resources(schedule_data['tasks'], result)

        return result

    def _validate_required_fields(self, data: dict, result: ValidationResult):
        required = ['project_name', 'start_date', 'tasks']
        for field in required:
            if field not in data:
                result.add_error(field, f"Required field '{field}' is missing")

    def _validate_tasks(self, tasks: list, result: ValidationResult):
        task_ids = set()

        for i, task in enumerate(tasks):
            # Check for duplicate IDs
            task_id = task.get('id')
            if task_id in task_ids:
                result.add_error(f"tasks[{i}].id", f"Duplicate task ID: {task_id}")
            task_ids.add(task_id)

            # Check dates
            start = task.get('start_date')
            end = task.get('end_date')

            if start and end:
                try:
                    start_dt = datetime.fromisoformat(start) if isinstance(start, str) else start
                    end_dt = datetime.fromisoformat(end) if isinstance(end, str) else end

                    if end_dt < start_dt:
                        result.add_error(f"tasks[{i}]", f"End date before start date", f"{start} -> {end}")

                    # Check for unrealistic durations
                    duration = (end_dt - start_dt).days
                    if duration > 365:
                        result.add_warning(f"tasks[{i}]", f"Task duration exceeds 1 year ({duration} days)")
                    if duration == 0 and task.get('type') != 'milestone':
                        result.add_warning(f"tasks[{i}]", "Task has zero duration but is not marked as milestone")

                except ValueError as e:
                    result.add_error(f"tasks[{i}]", f"Invalid date format: {e}")

            # Check for missing duration
            if not task.get('duration') and not (start and end):
                result.add_error(f"tasks[{i}]", "Task missing duration or start/end dates")

    def _validate_dependencies(self, tasks: list, result: ValidationResult):
        task_ids = {t.get('id') for t in tasks}
        task_dict = {t.get('id'): t for t in tasks}

        for task in tasks:
            predecessors = task.get('predecessors', [])
            for pred_id in predecessors:
                # Check predecessor exists
                if pred_id not in task_ids:
                    result.add_error(f"tasks[{task.get('id')}].predecessors", f"Predecessor '{pred_id}' does not exist")
                    continue

                # Check for logical sequence (if dates available)
                pred = task_dict.get(pred_id)
                if pred and pred.get('end_date') and task.get('start_date'):
                    pred_end = datetime.fromisoformat(pred['end_date']) if isinstance(pred['end_date'], str) else pred['end_date']
                    task_start = datetime.fromisoformat(task['start_date']) if isinstance(task['start_date'], str) else task['start_date']

                    if task_start < pred_end:
                        result.add_error(
                            f"tasks[{task.get('id')}]",
                            f"Task starts before predecessor '{pred_id}' ends",
                            f"Pred ends: {pred_end}, Task starts: {task_start}"
                        )

    def _validate_resources(self, tasks: list, result: ValidationResult):
        # Check for resource over-allocation by date
        resource_usage = {}

        for task in tasks:
            resources = task.get('resources', [])
            start = task.get('start_date')
            end = task.get('end_date')

            if not (resources and start and end):
                continue

            # Simplified: just check if any resource assigned to multiple tasks
            for resource in resources:
                res_id = resource.get('id') or resource.get('name')
                if res_id not in resource_usage:
                    resource_usage[res_id] = []
                resource_usage[res_id].append({
                    'task': task.get('id'),
                    'start': start,
                    'end': end,
                    'allocation': resource.get('allocation', 100)
                })

        # Check allocations
        for res_id, assignments in resource_usage.items():
            if len(assignments) > 1:
                # Simple overlap check
                total_allocation = sum(a['allocation'] for a in assignments)
                if total_allocation > 100:
                    result.add_warning(
                        f"resource[{res_id}]",
                        f"Resource may be over-allocated ({total_allocation}%)",
                        suggestion="Check for overlapping assignments"
                    )
```

### BIM Data Validation

```python
class BIMDataValidator:
    """Validate BIM export data (IFC, COBie, etc.)."""

    def validate(self, bim_data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(is_valid=True)

        # Check element data
        if 'elements' in bim_data:
            self._validate_elements(bim_data['elements'], result)

        # Check property sets
        if 'property_sets' in bim_data:
            self._validate_properties(bim_data['property_sets'], result)

        # Check spatial structure
        if 'spatial_structure' in bim_data:
            self._validate_spatial(bim_data['spatial_structure'], result)

        return result

    def _validate_elements(self, elements: list, result: ValidationResult):
        guids = set()

        for i, elem in enumerate(elements):
            # Check for unique GUIDs
            guid = elem.get('guid')
            if guid in guids:
                result.add_error(f"elements[{i}].guid", f"Duplicate GUID: {guid}")
            guids.add(guid)

            # Check for required properties
            if not elem.get('ifc_type'):
                result.add_warning(f"elements[{i}]", "Element missing IFC type")

            if not elem.get('name'):
                result.add_warning(f"elements[{i}]", "Element missing name")

            # Check geometry
            if not elem.get('geometry') and not elem.get('location'):
                result.add_warning(f"elements[{i}]", "Element has no geometry or location")

            # Check for valid quantities
            for qty_name in ['area', 'volume', 'length']:
                if qty_name in elem and elem[qty_name] < 0:
                    result.add_error(f"elements[{i}].{qty_name}", f"Negative {qty_name} value", elem[qty_name])

    def _validate_properties(self, property_sets: list, result: ValidationResult):
        for pset in property_sets:
            pset_name = pset.get('name', 'Unknown')

            # Check for empty property sets
            if not pset.get('properties'):
                result.add_warning(f"property_set[{pset_name}]", "Property set has no properties")

            # Check property values
            for prop in pset.get('properties', []):
                if prop.get('value') is None:
                    result.add_info(f"property_set[{pset_name}].{prop.get('name')}", "Property has null value")

    def _validate_spatial(self, spatial: dict, result: ValidationResult):
        # Check for proper hierarchy
        if not spatial.get('site'):
            result.add_warning("spatial_structure", "No site defined")
        if not spatial.get('building'):
            result.add_warning("spatial_structure", "No building defined")
        if not spatial.get('levels') or len(spatial.get('levels', [])) == 0:
            result.add_warning("spatial_structure", "No levels/floors defined")
```

### Field Data Validation

```python
class FieldDataValidator:
    """Validate field/site data inputs."""

    def validate(self, field_data: Dict[str, Any]) -> ValidationResult:
        result = ValidationResult(is_valid=True)

        # Daily report validation
        if field_data.get('type') == 'daily_report':
            self._validate_daily_report(field_data, result)

        # Inspection data
        if field_data.get('type') == 'inspection':
            self._validate_inspection(field_data, result)

        # Progress data
        if field_data.get('type') == 'progress':
            self._validate_progress(field_data, result)

        return result

    def _validate_daily_report(self, data: dict, result: ValidationResult):
        required = ['date', 'weather', 'workforce']
        for field in required:
            if field not in data:
                result.add_error(field, f"Daily report missing '{field}'")

        # Validate workforce
        if 'workforce' in data:
            total = sum(w.get('count', 0) for w in data['workforce'])
            if total == 0:
                result.add_warning("workforce", "No workers reported on-site")
            if total > 500:
                result.add_warning("workforce", f"Unusually high workforce count: {total}")

        # Validate date
        if 'date' in data:
            try:
                report_date = datetime.fromisoformat(data['date']) if isinstance(data['date'], str) else data['date']
                if report_date > datetime.now():
                    result.add_error("date", "Report date is in the future")
            except ValueError:
                result.add_error("date", "Invalid date format")

    def _validate_inspection(self, data: dict, result: ValidationResult):
        required = ['inspection_type', 'date', 'inspector', 'result']
        for field in required:
            if field not in data:
                result.add_error(field, f"Inspection missing '{field}'")

        # Check result value
        valid_results = ['pass', 'fail', 'conditional', 'not_applicable']
        if data.get('result') and data['result'].lower() not in valid_results:
            result.add_warning("result", f"Non-standard inspection result: {data['result']}")

    def _validate_progress(self, data: dict, result: ValidationResult):
        # Check percentage values
        if 'percent_complete' in data:
            pct = data['percent_complete']
            if pct < 0 or pct > 100:
                result.add_error("percent_complete", f"Invalid percentage: {pct}", suggestion="Must be 0-100")

        # Check for regression (if previous value available)
        if 'previous_percent' in data and 'percent_complete' in data:
            if data['percent_complete'] < data['previous_percent']:
                result.add_warning("percent_complete", "Progress decreased from previous report",
                                  f"{data['previous_percent']}% -> {data['percent_complete']}%")
```

## Usage Examples

```python
# Validate a cost estimate
estimate = {
    'project_name': 'Office Building',
    'estimate_date': '2026-01-15',
    'gross_area': 50000,
    'line_items': [
        {'description': 'Concrete', 'csi_code': '03 30 00', 'quantity': 5000, 'unit_cost': 150},
        {'description': 'Steel', 'csi_code': '05 12 00', 'quantity': 200, 'unit_cost': 2500},
    ],
    'total': 1250000
}

validator = CostEstimateValidator()
result = validator.validate(estimate)
print(result.to_report())

# Validate before processing
if result.is_valid:
    process_estimate(estimate)
else:
    print("Fix errors before processing")
    for error in result.errors:
        print(f"  - {error.field}: {error.message}")
```

## Integration with DDC Pipeline

```python
# Validate all inputs before pipeline execution
def validate_pipeline_inputs(inputs: dict) -> bool:
    validators = {
        'estimate': CostEstimateValidator(),
        'schedule': ScheduleValidator(),
        'bim_data': BIMDataValidator(),
        'field_data': FieldDataValidator()
    }

    all_valid = True
    for input_type, data in inputs.items():
        if input_type in validators:
            result = validators[input_type].validate(data)
            if not result.is_valid:
                print(f"\n{input_type.upper()} VALIDATION FAILED:")
                print(result.to_report())
                all_valid = False

    return all_valid
```

## Resources

- **Data Quality Best Practices**: Validate early, validate often
- **Construction Data Standards**: CSI, IFC, COBie specifications
- **Error Handling**: Always provide actionable suggestions
