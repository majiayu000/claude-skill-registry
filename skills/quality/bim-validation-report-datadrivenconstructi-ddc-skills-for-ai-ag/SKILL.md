---
slug: "bim-validation-report"
display_name: "BIM Validation Report"
description: "Generate comprehensive BIM model validation reports. Check data quality, completeness, and compliance with standards."
---

# BIM Validation Report Generator

## Business Case

### Problem Statement
BIM models often have quality issues:
- Missing required properties
- Invalid or inconsistent data
- Non-compliant with project standards
- Incomplete model information

### Solution
Automated BIM validation system that checks models against configurable rules and generates detailed compliance reports.

### Business Value
- **Quality assurance** - Catch issues early
- **Standards compliance** - Meet project requirements
- **Automation** - Reduce manual QC effort
- **Transparency** - Clear validation results

## Technical Implementation

```python
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum


class ValidationSeverity(Enum):
    """Validation issue severity."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationStatus(Enum):
    """Overall validation status."""
    PASSED = "passed"
    PASSED_WITH_WARNINGS = "passed_with_warnings"
    FAILED = "failed"


class RuleCategory(Enum):
    """Validation rule categories."""
    REQUIRED_PROPERTIES = "required_properties"
    DATA_FORMAT = "data_format"
    NAMING_CONVENTION = "naming_convention"
    GEOMETRIC = "geometric"
    CLASSIFICATION = "classification"
    RELATIONSHIPS = "relationships"


@dataclass
class ValidationRule:
    """Single validation rule."""
    rule_id: str
    name: str
    category: RuleCategory
    description: str
    severity: ValidationSeverity
    check_function: Callable
    applicable_categories: List[str] = field(default_factory=list)
    enabled: bool = True


@dataclass
class ValidationIssue:
    """Single validation issue."""
    issue_id: str
    rule_id: str
    rule_name: str
    element_id: str
    element_name: str
    element_category: str
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'issue_id': self.issue_id,
            'rule_id': self.rule_id,
            'rule_name': self.rule_name,
            'element_id': self.element_id,
            'element_name': self.element_name,
            'element_category': self.element_category,
            'severity': self.severity.value,
            'message': self.message
        }


@dataclass
class ValidationReport:
    """Complete validation report."""
    project_name: str
    model_name: str
    validated_at: datetime
    status: ValidationStatus
    total_elements: int
    elements_with_issues: int
    issues: List[ValidationIssue]
    rules_checked: int
    summary_by_severity: Dict[str, int]
    summary_by_category: Dict[str, int]


class BIMValidationEngine:
    """BIM model validation engine."""

    def __init__(self, project_name: str, model_name: str):
        self.project_name = project_name
        self.model_name = model_name
        self.rules: List[ValidationRule] = []
        self.issues: List[ValidationIssue] = []
        self._issue_counter = 0

        # Load default rules
        self._load_default_rules()

    def _load_default_rules(self):
        """Load standard validation rules."""

        # Required properties rules
        self.add_rule(ValidationRule(
            rule_id="REQ-001",
            name="Element Name Required",
            category=RuleCategory.REQUIRED_PROPERTIES,
            description="All elements must have a name",
            severity=ValidationSeverity.ERROR,
            check_function=lambda e: bool(e.get('name'))
        ))

        self.add_rule(ValidationRule(
            rule_id="REQ-002",
            name="Level Assignment Required",
            category=RuleCategory.REQUIRED_PROPERTIES,
            description="Elements must be assigned to a level",
            severity=ValidationSeverity.WARNING,
            check_function=lambda e: bool(e.get('level')),
            applicable_categories=["Walls", "Floors", "Doors", "Windows"]
        ))

        self.add_rule(ValidationRule(
            rule_id="REQ-003",
            name="Material Required",
            category=RuleCategory.REQUIRED_PROPERTIES,
            description="Structural elements must have material defined",
            severity=ValidationSeverity.ERROR,
            check_function=lambda e: bool(e.get('material')),
            applicable_categories=["Structural Columns", "Structural Framing", "Floors"]
        ))

        # Naming convention rules
        self.add_rule(ValidationRule(
            rule_id="NAM-001",
            name="No Special Characters",
            category=RuleCategory.NAMING_CONVENTION,
            description="Names should not contain special characters",
            severity=ValidationSeverity.WARNING,
            check_function=self._check_no_special_chars
        ))

        self.add_rule(ValidationRule(
            rule_id="NAM-002",
            name="Name Length Check",
            category=RuleCategory.NAMING_CONVENTION,
            description="Names should be between 3 and 100 characters",
            severity=ValidationSeverity.INFO,
            check_function=lambda e: 3 <= len(e.get('name', '')) <= 100
        ))

        # Classification rules
        self.add_rule(ValidationRule(
            rule_id="CLS-001",
            name="Classification Code Present",
            category=RuleCategory.CLASSIFICATION,
            description="Elements should have classification code",
            severity=ValidationSeverity.WARNING,
            check_function=lambda e: bool(e.get('classification_code') or e.get('uniformat'))
        ))

        # Geometric rules
        self.add_rule(ValidationRule(
            rule_id="GEO-001",
            name="Non-Zero Volume",
            category=RuleCategory.GEOMETRIC,
            description="3D elements must have non-zero volume",
            severity=ValidationSeverity.ERROR,
            check_function=lambda e: float(e.get('volume', 0)) > 0,
            applicable_categories=["Walls", "Floors", "Structural Columns", "Structural Framing"]
        ))

        self.add_rule(ValidationRule(
            rule_id="GEO-002",
            name="Valid Bounding Box",
            category=RuleCategory.GEOMETRIC,
            description="Elements must have valid bounding box",
            severity=ValidationSeverity.ERROR,
            check_function=self._check_valid_bbox
        ))

    def _check_no_special_chars(self, element: Dict[str, Any]) -> bool:
        """Check name for special characters."""
        import re
        name = element.get('name', '')
        return bool(re.match(r'^[\w\s\-\.]+$', name))

    def _check_valid_bbox(self, element: Dict[str, Any]) -> bool:
        """Check for valid bounding box."""
        try:
            min_x = float(element.get('min_x', 0))
            max_x = float(element.get('max_x', 0))
            min_y = float(element.get('min_y', 0))
            max_y = float(element.get('max_y', 0))
            min_z = float(element.get('min_z', 0))
            max_z = float(element.get('max_z', 0))
            return max_x > min_x and max_y > min_y and max_z > min_z
        except (ValueError, TypeError):
            return False

    def add_rule(self, rule: ValidationRule):
        """Add validation rule."""
        self.rules.append(rule)

    def add_custom_rule(self, rule_id: str, name: str, category: RuleCategory,
                       check_function: Callable, severity: ValidationSeverity = ValidationSeverity.WARNING,
                       description: str = "", categories: List[str] = None):
        """Add custom validation rule."""
        rule = ValidationRule(
            rule_id=rule_id,
            name=name,
            category=category,
            description=description,
            severity=severity,
            check_function=check_function,
            applicable_categories=categories or []
        )
        self.add_rule(rule)

    def validate_element(self, element: Dict[str, Any]) -> List[ValidationIssue]:
        """Validate single element against all rules."""
        issues = []
        element_category = element.get('category', '')

        for rule in self.rules:
            if not rule.enabled:
                continue

            # Check if rule applies to this category
            if rule.applicable_categories and element_category not in rule.applicable_categories:
                continue

            try:
                passed = rule.check_function(element)
                if not passed:
                    self._issue_counter += 1
                    issue = ValidationIssue(
                        issue_id=f"ISS-{self._issue_counter:05d}",
                        rule_id=rule.rule_id,
                        rule_name=rule.name,
                        element_id=str(element.get('element_id', '')),
                        element_name=str(element.get('name', '')),
                        element_category=element_category,
                        severity=rule.severity,
                        message=rule.description
                    )
                    issues.append(issue)
            except Exception as e:
                # Rule check failed
                self._issue_counter += 1
                issue = ValidationIssue(
                    issue_id=f"ISS-{self._issue_counter:05d}",
                    rule_id=rule.rule_id,
                    rule_name=rule.name,
                    element_id=str(element.get('element_id', '')),
                    element_name=str(element.get('name', '')),
                    element_category=element_category,
                    severity=ValidationSeverity.ERROR,
                    message=f"Rule check error: {str(e)}"
                )
                issues.append(issue)

        return issues

    def validate_model(self, elements_df: pd.DataFrame) -> ValidationReport:
        """Validate entire BIM model."""
        self.issues = []
        elements_with_issues = set()

        for _, row in elements_df.iterrows():
            element = row.to_dict()
            element_issues = self.validate_element(element)

            if element_issues:
                elements_with_issues.add(element.get('element_id'))
                self.issues.extend(element_issues)

        # Calculate summaries
        summary_by_severity = {
            'error': sum(1 for i in self.issues if i.severity == ValidationSeverity.ERROR),
            'warning': sum(1 for i in self.issues if i.severity == ValidationSeverity.WARNING),
            'info': sum(1 for i in self.issues if i.severity == ValidationSeverity.INFO)
        }

        summary_by_category = {}
        for issue in self.issues:
            cat = issue.element_category
            summary_by_category[cat] = summary_by_category.get(cat, 0) + 1

        # Determine overall status
        if summary_by_severity['error'] > 0:
            status = ValidationStatus.FAILED
        elif summary_by_severity['warning'] > 0:
            status = ValidationStatus.PASSED_WITH_WARNINGS
        else:
            status = ValidationStatus.PASSED

        return ValidationReport(
            project_name=self.project_name,
            model_name=self.model_name,
            validated_at=datetime.now(),
            status=status,
            total_elements=len(elements_df),
            elements_with_issues=len(elements_with_issues),
            issues=self.issues,
            rules_checked=len([r for r in self.rules if r.enabled]),
            summary_by_severity=summary_by_severity,
            summary_by_category=summary_by_category
        )

    def export_report(self, report: ValidationReport, output_path: str):
        """Export validation report to Excel."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = {
                'Metric': ['Project', 'Model', 'Validated At', 'Status',
                          'Total Elements', 'Elements with Issues', 'Rules Checked',
                          'Errors', 'Warnings', 'Info'],
                'Value': [report.project_name, report.model_name,
                         report.validated_at.isoformat(), report.status.value,
                         report.total_elements, report.elements_with_issues,
                         report.rules_checked, report.summary_by_severity['error'],
                         report.summary_by_severity['warning'], report.summary_by_severity['info']]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

            # Issues sheet
            issues_df = pd.DataFrame([i.to_dict() for i in report.issues])
            if not issues_df.empty:
                issues_df.to_excel(writer, sheet_name='Issues', index=False)

            # By Category sheet
            cat_df = pd.DataFrame([
                {'Category': k, 'Issue Count': v}
                for k, v in report.summary_by_category.items()
            ])
            if not cat_df.empty:
                cat_df.to_excel(writer, sheet_name='By Category', index=False)

        return output_path


def generate_validation_report(elements_df: pd.DataFrame,
                               project_name: str,
                               model_name: str,
                               output_path: str = None) -> ValidationReport:
    """Quick function to generate validation report."""
    engine = BIMValidationEngine(project_name, model_name)
    report = engine.validate_model(elements_df)

    if output_path:
        engine.export_report(report, output_path)

    return report
```

## Quick Start

```python
# Load BIM elements
elements = pd.read_excel("bim_elements.xlsx")

# Run validation
report = generate_validation_report(
    elements,
    project_name="Office Tower",
    model_name="Architectural Model v3.2",
    output_path="validation_report.xlsx"
)

print(f"Status: {report.status.value}")
print(f"Errors: {report.summary_by_severity['error']}")
print(f"Warnings: {report.summary_by_severity['warning']}")
```

## Common Use Cases

### 1. Custom Validation Rules
```python
engine = BIMValidationEngine("Project", "Model")

# Add custom rule
engine.add_custom_rule(
    rule_id="CUSTOM-001",
    name="Fire Rating Required",
    category=RuleCategory.REQUIRED_PROPERTIES,
    check_function=lambda e: bool(e.get('fire_rating')),
    severity=ValidationSeverity.ERROR,
    categories=["Walls", "Doors"]
)
```

### 2. Filter Issues
```python
# Get only errors
errors = [i for i in report.issues if i.severity == ValidationSeverity.ERROR]

# Get issues for specific category
wall_issues = [i for i in report.issues if i.element_category == "Walls"]
```

### 3. Automated QC Pipeline
```python
report = engine.validate_model(elements)
if report.status == ValidationStatus.FAILED:
    send_notification("BIM validation failed", report.summary_by_severity)
```

## Resources
- **DDC Book**: Chapter 4.3 - BIM Validation
- **Reference**: ISO 19650, buildingSMART IDS
