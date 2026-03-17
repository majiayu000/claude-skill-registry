---
name: "bim-consistency-checker"
description: "Check BIM model consistency: naming conventions, parameter completeness, spatial relationships, and data integrity across model elements."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🔎", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# BIM Consistency Checker for Construction

## Overview

Validate BIM model consistency including naming conventions, parameter completeness, spatial relationships, classification compliance, and cross-reference integrity.

## Business Case

BIM consistency checking ensures:
- **Data Quality**: Complete and accurate model data
- **Interoperability**: Models work across platforms
- **Coordination**: Consistent information for all trades
- **Deliverable Compliance**: Meet BIM execution plan requirements

## Technical Implementation

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Set
from enum import Enum
import re

class CheckSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class CheckCategory(Enum):
    NAMING = "naming"
    PARAMETERS = "parameters"
    SPATIAL = "spatial"
    CLASSIFICATION = "classification"
    GEOMETRY = "geometry"
    RELATIONSHIPS = "relationships"

@dataclass
class ConsistencyIssue:
    element_id: str
    element_name: str
    category: CheckCategory
    severity: CheckSeverity
    rule: str
    message: str
    suggestion: str = ""

@dataclass
class ConsistencyReport:
    model_name: str
    total_elements: int
    elements_checked: int
    issues: List[ConsistencyIssue]
    issues_by_category: Dict[str, int]
    issues_by_severity: Dict[str, int]
    pass_rate: float

@dataclass
class NamingConvention:
    element_type: str
    pattern: str
    description: str
    examples: List[str]

class BIMConsistencyChecker:
    """Check BIM model consistency and data quality."""

    # Default naming conventions
    DEFAULT_NAMING_RULES = [
        NamingConvention(
            element_type='Level',
            pattern=r'^(L|Level)\s*\d{1,2}$|^(B|Basement)\s*\d?$|^(R|Roof)$',
            description='Levels should follow L01, Level 1, B1, Roof pattern',
            examples=['L01', 'Level 1', 'B1', 'Roof']
        ),
        NamingConvention(
            element_type='Grid',
            pattern=r'^[A-Z]$|^\d{1,2}$|^[A-Z]\.\d$',
            description='Grids should be single letters (A-Z) or numbers',
            examples=['A', '1', 'A.1']
        ),
        NamingConvention(
            element_type='Room',
            pattern=r'^\d{3,4}[A-Z]?\s*-?\s*.+',
            description='Rooms should have number and name (101 - Office)',
            examples=['101 - Office', '201A Conference']
        ),
        NamingConvention(
            element_type='Wall',
            pattern=r'^(INT|EXT|CW|CMU|GYP)[-_].+',
            description='Walls should have type prefix',
            examples=['INT-GYP-1HR', 'EXT-CMU-8IN']
        ),
        NamingConvention(
            element_type='Door',
            pattern=r'^[A-Z]?\d{2,3}[A-Z]?$',
            description='Doors should follow type numbering',
            examples=['101', 'A101', '101A']
        ),
    ]

    # Required parameters by element type
    REQUIRED_PARAMETERS = {
        'Wall': ['Fire Rating', 'Function', 'Structural'],
        'Door': ['Fire Rating', 'Width', 'Height', 'Frame Material'],
        'Room': ['Name', 'Number', 'Area', 'Department'],
        'Window': ['Width', 'Height', 'Glass Type'],
        'Floor': ['Structural', 'Fire Rating'],
        'Ceiling': ['Height', 'Type'],
        'Column': ['Structural Material', 'Shape'],
        'Beam': ['Structural Material', 'Size'],
    }

    def __init__(self):
        self.naming_rules: List[NamingConvention] = list(self.DEFAULT_NAMING_RULES)
        self.required_params: Dict[str, List[str]] = dict(self.REQUIRED_PARAMETERS)
        self.issues: List[ConsistencyIssue] = []

    def add_naming_rule(self, rule: NamingConvention):
        """Add custom naming convention rule."""
        self.naming_rules.append(rule)

    def set_required_parameters(self, element_type: str, parameters: List[str]):
        """Set required parameters for an element type."""
        self.required_params[element_type] = parameters

    def check_model(self, elements: List[Dict]) -> ConsistencyReport:
        """Run all consistency checks on model elements."""
        self.issues = []

        for element in elements:
            self._check_naming(element)
            self._check_parameters(element)
            self._check_spatial(element)
            self._check_classification(element)
            self._check_geometry(element)

        # Cross-element checks
        self._check_relationships(elements)
        self._check_duplicates(elements)

        # Calculate statistics
        issues_by_category = {}
        issues_by_severity = {}

        for issue in self.issues:
            cat = issue.category.value
            sev = issue.severity.value
            issues_by_category[cat] = issues_by_category.get(cat, 0) + 1
            issues_by_severity[sev] = issues_by_severity.get(sev, 0) + 1

        elements_with_issues = len(set(i.element_id for i in self.issues))
        pass_rate = (len(elements) - elements_with_issues) / len(elements) * 100 if elements else 100

        return ConsistencyReport(
            model_name='Model',
            total_elements=len(elements),
            elements_checked=len(elements),
            issues=self.issues,
            issues_by_category=issues_by_category,
            issues_by_severity=issues_by_severity,
            pass_rate=pass_rate
        )

    def _check_naming(self, element: Dict):
        """Check element naming conventions."""
        element_type = element.get('type', '')
        name = element.get('name', '')
        element_id = element.get('id', '')

        if not name:
            self.issues.append(ConsistencyIssue(
                element_id=element_id,
                element_name='(no name)',
                category=CheckCategory.NAMING,
                severity=CheckSeverity.ERROR,
                rule='Name Required',
                message='Element has no name',
                suggestion='Assign a descriptive name following conventions'
            ))
            return

        # Check against naming rules
        for rule in self.naming_rules:
            if rule.element_type.lower() in element_type.lower():
                if not re.match(rule.pattern, name, re.IGNORECASE):
                    self.issues.append(ConsistencyIssue(
                        element_id=element_id,
                        element_name=name,
                        category=CheckCategory.NAMING,
                        severity=CheckSeverity.WARNING,
                        rule=f'{rule.element_type} Naming',
                        message=f'Name "{name}" does not follow convention',
                        suggestion=f'{rule.description}. Examples: {", ".join(rule.examples)}'
                    ))

        # Check for special characters
        if re.search(r'[<>:"/\\|?*]', name):
            self.issues.append(ConsistencyIssue(
                element_id=element_id,
                element_name=name,
                category=CheckCategory.NAMING,
                severity=CheckSeverity.ERROR,
                rule='Invalid Characters',
                message='Name contains invalid characters',
                suggestion='Remove special characters: < > : " / \\ | ? *'
            ))

    def _check_parameters(self, element: Dict):
        """Check parameter completeness."""
        element_type = element.get('type', '')
        element_id = element.get('id', '')
        name = element.get('name', '')
        params = element.get('parameters', {})

        # Check required parameters
        required = self.required_params.get(element_type, [])
        for param in required:
            if param not in params or params[param] in [None, '', 'None']:
                self.issues.append(ConsistencyIssue(
                    element_id=element_id,
                    element_name=name,
                    category=CheckCategory.PARAMETERS,
                    severity=CheckSeverity.WARNING,
                    rule='Required Parameter',
                    message=f'Missing required parameter: {param}',
                    suggestion=f'Set value for {param}'
                ))

        # Check for default/placeholder values
        placeholder_values = ['TBD', 'XXX', 'TODO', 'CHANGE', '<default>']
        for param, value in params.items():
            if str(value).upper() in placeholder_values:
                self.issues.append(ConsistencyIssue(
                    element_id=element_id,
                    element_name=name,
                    category=CheckCategory.PARAMETERS,
                    severity=CheckSeverity.WARNING,
                    rule='Placeholder Value',
                    message=f'Parameter "{param}" has placeholder value: {value}',
                    suggestion='Replace with actual value'
                ))

    def _check_spatial(self, element: Dict):
        """Check spatial consistency."""
        element_id = element.get('id', '')
        name = element.get('name', '')
        element_type = element.get('type', '')

        # Check level assignment
        level = element.get('level')
        requires_level = element_type in ['Wall', 'Door', 'Window', 'Room', 'Floor', 'Ceiling']

        if requires_level and not level:
            self.issues.append(ConsistencyIssue(
                element_id=element_id,
                element_name=name,
                category=CheckCategory.SPATIAL,
                severity=CheckSeverity.ERROR,
                rule='Level Assignment',
                message='Element not assigned to a level',
                suggestion='Assign element to appropriate level'
            ))

        # Check room bounding
        if element_type == 'Wall':
            room_bounding = element.get('room_bounding', True)
            if not room_bounding:
                self.issues.append(ConsistencyIssue(
                    element_id=element_id,
                    element_name=name,
                    category=CheckCategory.SPATIAL,
                    severity=CheckSeverity.INFO,
                    rule='Room Bounding',
                    message='Wall is not room bounding',
                    suggestion='Verify this is intentional'
                ))

    def _check_classification(self, element: Dict):
        """Check classification codes."""
        element_id = element.get('id', '')
        name = element.get('name', '')
        params = element.get('parameters', {})

        # Check for classification
        classification = params.get('Classification') or params.get('OmniClass') or params.get('UniFormat')

        if not classification:
            self.issues.append(ConsistencyIssue(
                element_id=element_id,
                element_name=name,
                category=CheckCategory.CLASSIFICATION,
                severity=CheckSeverity.INFO,
                rule='Classification Required',
                message='Element has no classification code',
                suggestion='Assign OmniClass, UniFormat, or other classification'
            ))
        else:
            # Validate format
            if not re.match(r'^\d{2}[-\s]?\d{2}[-\s]?\d{2}', str(classification)):
                self.issues.append(ConsistencyIssue(
                    element_id=element_id,
                    element_name=name,
                    category=CheckCategory.CLASSIFICATION,
                    severity=CheckSeverity.WARNING,
                    rule='Classification Format',
                    message=f'Invalid classification format: {classification}',
                    suggestion='Use standard format (XX XX XX)'
                ))

    def _check_geometry(self, element: Dict):
        """Check geometry validity."""
        element_id = element.get('id', '')
        name = element.get('name', '')
        geometry = element.get('geometry', {})

        # Check for zero area/volume
        area = geometry.get('area', 0)
        volume = geometry.get('volume', 0)

        if area == 0 and volume == 0 and element.get('type') not in ['Grid', 'Level', 'ReferencePlane']:
            self.issues.append(ConsistencyIssue(
                element_id=element_id,
                element_name=name,
                category=CheckCategory.GEOMETRY,
                severity=CheckSeverity.ERROR,
                rule='Zero Geometry',
                message='Element has zero area and volume',
                suggestion='Check element geometry is valid'
            ))

        # Check for extremely small elements
        if 0 < area < 0.01:  # Less than 0.01 m² or ft²
            self.issues.append(ConsistencyIssue(
                element_id=element_id,
                element_name=name,
                category=CheckCategory.GEOMETRY,
                severity=CheckSeverity.WARNING,
                rule='Tiny Element',
                message=f'Element has very small area: {area}',
                suggestion='Verify element is intentional and not a modeling error'
            ))

    def _check_relationships(self, elements: List[Dict]):
        """Check cross-element relationships."""
        # Build lookup
        elements_by_id = {e['id']: e for e in elements}
        elements_by_type = {}
        for e in elements:
            t = e.get('type', '')
            if t not in elements_by_type:
                elements_by_type[t] = []
            elements_by_type[t].append(e)

        # Check door-wall relationships
        for door in elements_by_type.get('Door', []):
            host_wall = door.get('host_id')
            if host_wall and host_wall not in elements_by_id:
                self.issues.append(ConsistencyIssue(
                    element_id=door['id'],
                    element_name=door.get('name', ''),
                    category=CheckCategory.RELATIONSHIPS,
                    severity=CheckSeverity.ERROR,
                    rule='Invalid Host',
                    message=f'Door references non-existent wall: {host_wall}',
                    suggestion='Rehost door to valid wall'
                ))

        # Check room enclosure
        for room in elements_by_type.get('Room', []):
            if not room.get('is_bounded', True):
                self.issues.append(ConsistencyIssue(
                    element_id=room['id'],
                    element_name=room.get('name', ''),
                    category=CheckCategory.RELATIONSHIPS,
                    severity=CheckSeverity.ERROR,
                    rule='Unbounded Room',
                    message='Room is not properly bounded',
                    suggestion='Check room boundary walls'
                ))

    def _check_duplicates(self, elements: List[Dict]):
        """Check for duplicate elements."""
        seen: Dict[str, List[Dict]] = {}

        for element in elements:
            # Create signature for duplicate detection
            sig_parts = [
                element.get('type', ''),
                str(element.get('geometry', {}).get('location', '')),
                element.get('name', '')
            ]
            signature = '|'.join(sig_parts)

            if signature in seen:
                for dup in seen[signature]:
                    self.issues.append(ConsistencyIssue(
                        element_id=element['id'],
                        element_name=element.get('name', ''),
                        category=CheckCategory.RELATIONSHIPS,
                        severity=CheckSeverity.WARNING,
                        rule='Duplicate Element',
                        message=f'Possible duplicate of element {dup["id"]}',
                        suggestion='Review and remove duplicate if confirmed'
                    ))

            if signature not in seen:
                seen[signature] = []
            seen[signature].append(element)

    def generate_report(self, report: ConsistencyReport) -> str:
        """Generate consistency check report."""
        lines = ["# BIM Consistency Check Report", ""]
        lines.append(f"**Model:** {report.model_name}")
        lines.append(f"**Elements Checked:** {report.elements_checked}")
        lines.append(f"**Pass Rate:** {report.pass_rate:.1f}%")
        lines.append("")

        # Summary
        lines.append("## Summary")
        lines.append(f"- **Total Issues:** {len(report.issues)}")
        lines.append(f"- Errors: {report.issues_by_severity.get('error', 0)}")
        lines.append(f"- Warnings: {report.issues_by_severity.get('warning', 0)}")
        lines.append(f"- Info: {report.issues_by_severity.get('info', 0)}")
        lines.append("")

        # By category
        lines.append("## Issues by Category")
        for cat, count in sorted(report.issues_by_category.items()):
            lines.append(f"- {cat}: {count}")
        lines.append("")

        # Critical issues
        errors = [i for i in report.issues if i.severity == CheckSeverity.ERROR]
        if errors:
            lines.append("## Critical Issues (Errors)")
            for issue in errors[:20]:
                lines.append(f"\n### {issue.element_name} ({issue.element_id})")
                lines.append(f"- **Rule:** {issue.rule}")
                lines.append(f"- **Issue:** {issue.message}")
                lines.append(f"- **Fix:** {issue.suggestion}")

        return "\n".join(lines)
```

## Quick Start

```python
# Initialize checker
checker = BIMConsistencyChecker()

# Sample model elements
elements = [
    {
        'id': 'wall-001',
        'type': 'Wall',
        'name': 'INT-GYP-1HR',
        'level': 'Level 1',
        'parameters': {'Fire Rating': '1 Hour', 'Function': 'Interior'},
        'geometry': {'area': 50.5}
    },
    {
        'id': 'door-001',
        'type': 'Door',
        'name': '101',
        'level': 'Level 1',
        'host_id': 'wall-001',
        'parameters': {'Width': 36, 'Height': 84}
    }
]

# Run checks
report = checker.check_model(elements)

print(f"Pass Rate: {report.pass_rate:.1f}%")
print(f"Issues Found: {len(report.issues)}")

# Generate report
print(checker.generate_report(report))
```

## Dependencies

```bash
pip install (no external dependencies)
```
