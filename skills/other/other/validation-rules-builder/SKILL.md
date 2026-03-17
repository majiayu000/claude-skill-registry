---
name: "validation-rules-builder"
description: "Build validation rules for construction data. Create RegEx and logic-based validation for BIM elements, cost codes, and schedule data."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "✔️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Validation Rules Builder

## Business Case

### Problem Statement
Construction data quality challenges:
- Inconsistent naming conventions
- Invalid cost codes and WBS
- Missing or malformed data
- Non-compliant BIM elements

### Solution
Rule-based validation engine using RegEx and logic rules to ensure data quality across construction systems.

## Technical Implementation

```python
import re
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum
from datetime import date


class RuleType(Enum):
    REGEX = "regex"
    RANGE = "range"
    ENUM = "enum"
    CUSTOM = "custom"
    REQUIRED = "required"
    DATE = "date"
    REFERENCE = "reference"


class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationResult:
    field: str
    is_valid: bool
    message: str
    severity: Severity
    value: Any = None


@dataclass
class ValidationRule:
    name: str
    field: str
    rule_type: RuleType
    pattern: str = ""
    min_value: float = None
    max_value: float = None
    allowed_values: List[Any] = field(default_factory=list)
    custom_func: Callable = None
    severity: Severity = Severity.ERROR
    message: str = ""
    enabled: bool = True


class ValidationRulesBuilder:
    """Build and execute validation rules for construction data."""

    # Pre-defined patterns for construction data
    PATTERNS = {
        'wbs_code': r'^[0-9]{2}\.[0-9]{2}\.[0-9]{2}(\.[0-9]{2})?$',
        'cost_code': r'^[A-Z]{1,3}-[0-9]{3,6}$',
        'activity_id': r'^[A-Z]{1,3}[0-9]{4,6}$',
        'drawing_number': r'^[A-Z]{1,2}-[0-9]{3}-[A-Z0-9]{2,4}$',
        'specification_section': r'^[0-9]{2}\s?[0-9]{2}\s?[0-9]{2}(\.[0-9]{2})?$',
        'level_name': r'^(Level|L|FL)\s?[-_]?\s?([0-9]{1,3}|B[0-9]|R|G|M)$',
        'grid_line': r'^[A-Z]\.?[0-9]?$|^[0-9]{1,2}\.?[A-Z]?$',
        'revision': r'^[A-Z]$|^[0-9]{1,2}$|^Rev\.?\s?[A-Z0-9]+$',
        'date_iso': r'^\d{4}-\d{2}-\d{2}$',
        'email': r'^[\w\.-]+@[\w\.-]+\.\w+$',
        'phone': r'^\+?[0-9]{1,3}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{4}$',
    }

    def __init__(self):
        self.rules: List[ValidationRule] = []
        self.custom_patterns: Dict[str, str] = {}

    def add_regex_rule(self,
                       name: str,
                       field: str,
                       pattern: str,
                       message: str = "",
                       severity: Severity = Severity.ERROR) -> 'ValidationRulesBuilder':
        """Add regex validation rule."""

        self.rules.append(ValidationRule(
            name=name,
            field=field,
            rule_type=RuleType.REGEX,
            pattern=pattern,
            message=message or f"Field '{field}' does not match pattern",
            severity=severity
        ))
        return self

    def add_range_rule(self,
                       name: str,
                       field: str,
                       min_value: float = None,
                       max_value: float = None,
                       message: str = "",
                       severity: Severity = Severity.ERROR) -> 'ValidationRulesBuilder':
        """Add numeric range validation rule."""

        self.rules.append(ValidationRule(
            name=name,
            field=field,
            rule_type=RuleType.RANGE,
            min_value=min_value,
            max_value=max_value,
            message=message or f"Field '{field}' out of range [{min_value}, {max_value}]",
            severity=severity
        ))
        return self

    def add_enum_rule(self,
                      name: str,
                      field: str,
                      allowed_values: List[Any],
                      message: str = "",
                      severity: Severity = Severity.ERROR) -> 'ValidationRulesBuilder':
        """Add enumeration validation rule."""

        self.rules.append(ValidationRule(
            name=name,
            field=field,
            rule_type=RuleType.ENUM,
            allowed_values=allowed_values,
            message=message or f"Field '{field}' must be one of: {allowed_values}",
            severity=severity
        ))
        return self

    def add_required_rule(self,
                          name: str,
                          field: str,
                          message: str = "",
                          severity: Severity = Severity.ERROR) -> 'ValidationRulesBuilder':
        """Add required field validation rule."""

        self.rules.append(ValidationRule(
            name=name,
            field=field,
            rule_type=RuleType.REQUIRED,
            message=message or f"Field '{field}' is required",
            severity=severity
        ))
        return self

    def add_custom_rule(self,
                        name: str,
                        field: str,
                        func: Callable[[Any], bool],
                        message: str = "",
                        severity: Severity = Severity.ERROR) -> 'ValidationRulesBuilder':
        """Add custom validation function."""

        self.rules.append(ValidationRule(
            name=name,
            field=field,
            rule_type=RuleType.CUSTOM,
            custom_func=func,
            message=message or f"Field '{field}' failed custom validation",
            severity=severity
        ))
        return self

    def add_pattern(self, name: str, pattern: str):
        """Add custom pattern for reuse."""
        self.custom_patterns[name] = pattern

    def use_pattern(self,
                    rule_name: str,
                    field: str,
                    pattern_name: str,
                    message: str = "",
                    severity: Severity = Severity.ERROR) -> 'ValidationRulesBuilder':
        """Use pre-defined or custom pattern."""

        pattern = self.custom_patterns.get(pattern_name) or self.PATTERNS.get(pattern_name)
        if not pattern:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        return self.add_regex_rule(rule_name, field, pattern, message, severity)

    def validate_record(self, record: Dict[str, Any]) -> List[ValidationResult]:
        """Validate a single record against all rules."""

        results = []

        for rule in self.rules:
            if not rule.enabled:
                continue

            value = record.get(rule.field)
            result = self._apply_rule(rule, value)
            results.append(result)

        return results

    def validate_records(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate multiple records and return summary."""

        all_results = []
        error_count = 0
        warning_count = 0

        for i, record in enumerate(records):
            record_results = self.validate_record(record)
            for result in record_results:
                if not result.is_valid:
                    result_dict = {
                        'record_index': i,
                        'field': result.field,
                        'message': result.message,
                        'severity': result.severity.value,
                        'value': result.value
                    }
                    all_results.append(result_dict)

                    if result.severity == Severity.ERROR:
                        error_count += 1
                    elif result.severity == Severity.WARNING:
                        warning_count += 1

        return {
            'total_records': len(records),
            'valid_records': len(records) - len(set(r['record_index'] for r in all_results if r['severity'] == 'error')),
            'error_count': error_count,
            'warning_count': warning_count,
            'issues': all_results
        }

    def _apply_rule(self, rule: ValidationRule, value: Any) -> ValidationResult:
        """Apply single validation rule."""

        if rule.rule_type == RuleType.REQUIRED:
            is_valid = value is not None and value != "" and value != []
            return ValidationResult(
                field=rule.field,
                is_valid=is_valid,
                message="" if is_valid else rule.message,
                severity=rule.severity,
                value=value
            )

        # Skip other validations if value is None/empty
        if value is None or value == "":
            return ValidationResult(
                field=rule.field,
                is_valid=True,
                message="",
                severity=rule.severity,
                value=value
            )

        if rule.rule_type == RuleType.REGEX:
            is_valid = bool(re.match(rule.pattern, str(value)))

        elif rule.rule_type == RuleType.RANGE:
            try:
                num_value = float(value)
                is_valid = True
                if rule.min_value is not None and num_value < rule.min_value:
                    is_valid = False
                if rule.max_value is not None and num_value > rule.max_value:
                    is_valid = False
            except (ValueError, TypeError):
                is_valid = False

        elif rule.rule_type == RuleType.ENUM:
            is_valid = value in rule.allowed_values

        elif rule.rule_type == RuleType.CUSTOM:
            try:
                is_valid = rule.custom_func(value)
            except Exception:
                is_valid = False

        else:
            is_valid = True

        return ValidationResult(
            field=rule.field,
            is_valid=is_valid,
            message="" if is_valid else rule.message,
            severity=rule.severity,
            value=value
        )

    def get_rules_summary(self) -> List[Dict]:
        """Get summary of all rules."""

        return [{
            'name': r.name,
            'field': r.field,
            'type': r.rule_type.value,
            'severity': r.severity.value,
            'enabled': r.enabled
        } for r in self.rules]


# Construction-specific validators
class ConstructionValidators:
    """Pre-built validators for construction data."""

    @staticmethod
    def wbs_validator() -> ValidationRulesBuilder:
        """Validator for WBS codes."""

        return (ValidationRulesBuilder()
            .add_required_rule("wbs_required", "wbs_code")
            .use_pattern("wbs_format", "wbs_code", "wbs_code", "Invalid WBS format (expected: XX.XX.XX)")
        )

    @staticmethod
    def cost_item_validator() -> ValidationRulesBuilder:
        """Validator for cost items."""

        return (ValidationRulesBuilder()
            .add_required_rule("code_required", "cost_code")
            .add_required_rule("desc_required", "description")
            .use_pattern("code_format", "cost_code", "cost_code")
            .add_range_rule("quantity_positive", "quantity", min_value=0)
            .add_range_rule("unit_cost_positive", "unit_cost", min_value=0)
            .add_enum_rule("unit_valid", "unit", ["EA", "LF", "SF", "CY", "TON", "HR", "LS"])
        )

    @staticmethod
    def schedule_activity_validator() -> ValidationRulesBuilder:
        """Validator for schedule activities."""

        def dates_valid(record):
            start = record.get('start_date')
            end = record.get('end_date')
            if start and end:
                return start <= end
            return True

        return (ValidationRulesBuilder()
            .add_required_rule("id_required", "activity_id")
            .add_required_rule("name_required", "activity_name")
            .use_pattern("id_format", "activity_id", "activity_id")
            .add_range_rule("duration_positive", "duration", min_value=0)
            .add_range_rule("progress_range", "percent_complete", min_value=0, max_value=100)
        )

    @staticmethod
    def bim_element_validator() -> ValidationRulesBuilder:
        """Validator for BIM elements."""

        return (ValidationRulesBuilder()
            .add_required_rule("guid_required", "element_guid")
            .add_required_rule("type_required", "element_type")
            .add_required_rule("level_required", "level")
            .use_pattern("level_format", "level", "level_name", severity=Severity.WARNING)
            .add_enum_rule("status_valid", "status",
                          ["New", "Existing", "Demolished", "Temporary"])
        )
```

## Quick Start

```python
# Create validator
validator = ValidationRulesBuilder()

# Add rules
validator.add_required_rule("id_required", "item_id")
validator.use_pattern("wbs_valid", "wbs_code", "wbs_code")
validator.add_range_rule("cost_range", "total_cost", min_value=0, max_value=10000000)
validator.add_enum_rule("status_valid", "status", ["Active", "Completed", "Cancelled"])

# Validate records
records = [
    {"item_id": "001", "wbs_code": "01.02.03", "total_cost": 50000, "status": "Active"},
    {"item_id": "", "wbs_code": "invalid", "total_cost": -100, "status": "Unknown"}
]

results = validator.validate_records(records)
print(f"Valid: {results['valid_records']}/{results['total_records']}")
print(f"Errors: {results['error_count']}, Warnings: {results['warning_count']}")
```

## Common Use Cases

### 1. Cost Data Validation
```python
cost_validator = ConstructionValidators.cost_item_validator()
results = cost_validator.validate_records(cost_items)
```

### 2. Schedule Validation
```python
schedule_validator = ConstructionValidators.schedule_activity_validator()
results = schedule_validator.validate_records(activities)
```

### 3. BIM Element Validation
```python
bim_validator = ConstructionValidators.bim_element_validator()
results = bim_validator.validate_records(elements)
```

## Resources
- **DDC Book**: Chapter 2.6 - Data Quality Requirements
- **Website**: https://datadrivenconstruction.io
