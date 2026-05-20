---
name: "bim-validation-pipeline"
description: "Build automated BIM validation pipelines for IFC/Revit data. Continuous validation against IDS, LOD requirements, COBie, and project-specific BEP standards."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🔎", "os": ["win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"], "anyBins": ["ifcopenshell"]}}}
---
# BIM Validation Pipeline

## Overview

Based on DDC methodology (Chapter 4.3), this skill provides automated BIM data validation pipelines. Validate BIM models against Information Delivery Specification (IDS), Level of Development (LOD) requirements, and project standards.

**Book Reference:** "Автоматический ETL конвейер для валидации данных" / "Automated ETL Pipeline for Data Validation"

> "Автоматизированная валидация BIM-данных позволяет выявлять ошибки на ранних стадиях и обеспечивать соответствие требованиям BEP."
> — DDC Book, Chapter 4.3

## Quick Start

```python
import ifcopenshell
import pandas as pd

# Load IFC model
ifc_model = ifcopenshell.open("model.ifc")

# Quick validation checks
walls = ifc_model.by_type("IfcWall")
print(f"Total walls: {len(walls)}")

# Check for required properties
issues = []
for wall in walls:
    # Check if wall has material
    if not wall.HasAssociations:
        issues.append(f"Wall {wall.GlobalId}: No material assigned")

print(f"Issues found: {len(issues)}")
```

## BIM Validation Framework

### Core Validator Class

```python
import ifcopenshell
import ifcopenshell.util.element as element_util
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum

class Severity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationIssue:
    element_id: str
    element_type: str
    rule_id: str
    severity: Severity
    message: str
    location: Optional[str] = None

class BIMValidator:
    """Comprehensive BIM model validator"""

    def __init__(self, ifc_path: str):
        self.model = ifcopenshell.open(ifc_path)
        self.issues: List[ValidationIssue] = []
        self.stats = {}

    def validate_all(self):
        """Run all validation checks"""
        self.validate_geometry()
        self.validate_properties()
        self.validate_relationships()
        self.validate_naming()
        self.validate_classification()
        return self.get_report()

    def validate_geometry(self):
        """Check geometry validity"""
        elements_with_geometry = [
            e for e in self.model.by_type("IfcProduct")
            if e.Representation
        ]

        for element in elements_with_geometry:
            # Check for zero volume
            try:
                settings = ifcopenshell.geom.settings()
                shape = ifcopenshell.geom.create_shape(settings, element)
                # Volume check would go here
            except:
                self.issues.append(ValidationIssue(
                    element_id=element.GlobalId,
                    element_type=element.is_a(),
                    rule_id="GEO-001",
                    severity=Severity.ERROR,
                    message="Invalid or missing geometry"
                ))

        self.stats['elements_with_geometry'] = len(elements_with_geometry)

    def validate_properties(self, required_psets: Dict[str, List[str]] = None):
        """Check required property sets and properties"""
        if required_psets is None:
            required_psets = {
                'IfcWall': ['Pset_WallCommon', 'BaseQuantities'],
                'IfcSlab': ['Pset_SlabCommon', 'BaseQuantities'],
                'IfcColumn': ['Pset_ColumnCommon', 'BaseQuantities'],
                'IfcBeam': ['Pset_BeamCommon', 'BaseQuantities']
            }

        for ifc_type, psets in required_psets.items():
            elements = self.model.by_type(ifc_type)

            for element in elements:
                element_psets = element_util.get_psets(element)

                for required_pset in psets:
                    if required_pset not in element_psets:
                        self.issues.append(ValidationIssue(
                            element_id=element.GlobalId,
                            element_type=ifc_type,
                            rule_id="PROP-001",
                            severity=Severity.WARNING,
                            message=f"Missing PropertySet: {required_pset}"
                        ))

    def validate_relationships(self):
        """Check spatial containment and relationships"""
        products = self.model.by_type("IfcProduct")

        for product in products:
            # Check spatial containment
            if hasattr(product, 'ContainedInStructure'):
                if not product.ContainedInStructure:
                    self.issues.append(ValidationIssue(
                        element_id=product.GlobalId,
                        element_type=product.is_a(),
                        rule_id="REL-001",
                        severity=Severity.WARNING,
                        message="Element not assigned to building storey"
                    ))

            # Check material assignment
            if hasattr(product, 'HasAssociations'):
                has_material = any(
                    rel.is_a('IfcRelAssociatesMaterial')
                    for rel in (product.HasAssociations or [])
                )
                if not has_material and product.is_a() in ['IfcWall', 'IfcSlab', 'IfcColumn']:
                    self.issues.append(ValidationIssue(
                        element_id=product.GlobalId,
                        element_type=product.is_a(),
                        rule_id="MAT-001",
                        severity=Severity.WARNING,
                        message="No material assigned"
                    ))

    def validate_naming(self, patterns: Dict[str, str] = None):
        """Validate element naming conventions"""
        import re

        if patterns is None:
            patterns = {
                'IfcBuildingStorey': r'^(Level|L|Floor|Уровень)\s*[-]?\d+',
                'IfcWall': r'^W[-_]?\d{3,}|^Wall[-_]',
                'IfcColumn': r'^C[-_]?\d{3,}|^Column[-_]',
                'IfcSpace': r'^Room[-_]|^Space[-_]'
            }

        for ifc_type, pattern in patterns.items():
            elements = self.model.by_type(ifc_type)

            for element in elements:
                name = element.Name or ""
                if not re.match(pattern, name, re.IGNORECASE):
                    self.issues.append(ValidationIssue(
                        element_id=element.GlobalId,
                        element_type=ifc_type,
                        rule_id="NAME-001",
                        severity=Severity.INFO,
                        message=f"Name '{name}' doesn't match convention"
                    ))

    def validate_classification(self, required_systems: List[str] = None):
        """Check classification system assignments"""
        if required_systems is None:
            required_systems = ['Uniclass', 'OmniClass', 'Uniformat']

        elements = self.model.by_type("IfcProduct")

        for element in elements:
            if hasattr(element, 'HasAssociations'):
                has_classification = any(
                    rel.is_a('IfcRelAssociatesClassification')
                    for rel in (element.HasAssociations or [])
                )

                if not has_classification:
                    self.issues.append(ValidationIssue(
                        element_id=element.GlobalId,
                        element_type=element.is_a(),
                        rule_id="CLASS-001",
                        severity=Severity.INFO,
                        message="No classification assigned"
                    ))

    def get_report(self):
        """Generate validation report"""
        by_severity = {s: [] for s in Severity}
        by_type = {}
        by_rule = {}

        for issue in self.issues:
            by_severity[issue.severity].append(issue)

            if issue.element_type not in by_type:
                by_type[issue.element_type] = []
            by_type[issue.element_type].append(issue)

            if issue.rule_id not in by_rule:
                by_rule[issue.rule_id] = []
            by_rule[issue.rule_id].append(issue)

        return {
            'total_issues': len(self.issues),
            'errors': len(by_severity[Severity.ERROR]),
            'warnings': len(by_severity[Severity.WARNING]),
            'info': len(by_severity[Severity.INFO]),
            'by_type': {k: len(v) for k, v in by_type.items()},
            'by_rule': {k: len(v) for k, v in by_rule.items()},
            'issues': self.issues,
            'stats': self.stats
        }
```

## LOD Validation

### Level of Development Checker

```python
class LODValidator:
    """Validate Level of Development (LOD) requirements"""

    # LOD requirements by element type
    LOD_REQUIREMENTS = {
        'LOD100': {
            'geometry': False,
            'properties': [],
            'description': 'Conceptual'
        },
        'LOD200': {
            'geometry': True,
            'approximate_size': True,
            'properties': ['Category'],
            'description': 'Schematic Design'
        },
        'LOD300': {
            'geometry': True,
            'exact_size': True,
            'properties': ['Category', 'Material', 'Type'],
            'quantities': ['Length', 'Area', 'Volume'],
            'description': 'Design Development'
        },
        'LOD350': {
            'geometry': True,
            'exact_size': True,
            'properties': ['Category', 'Material', 'Type', 'Manufacturer'],
            'quantities': ['Length', 'Area', 'Volume', 'Weight'],
            'connections': True,
            'description': 'Construction Documentation'
        },
        'LOD400': {
            'geometry': True,
            'fabrication_ready': True,
            'properties': ['Category', 'Material', 'Type', 'Manufacturer',
                          'Model', 'Serial', 'InstallationDate'],
            'quantities': ['All'],
            'connections': True,
            'description': 'Fabrication & Assembly'
        }
    }

    def __init__(self, model, target_lod='LOD300'):
        self.model = model
        self.target_lod = target_lod
        self.requirements = self.LOD_REQUIREMENTS.get(target_lod, {})
        self.results = []

    def validate_element(self, element):
        """Validate single element against LOD requirements"""
        issues = []
        element_guid = element.GlobalId
        psets = element_util.get_psets(element)

        # Check geometry
        if self.requirements.get('geometry'):
            if not element.Representation:
                issues.append({
                    'element': element_guid,
                    'issue': 'Missing geometry',
                    'required_for': self.target_lod
                })

        # Check required properties
        required_props = self.requirements.get('properties', [])
        all_props = {}
        for pset_name, props in psets.items():
            all_props.update(props)

        for prop in required_props:
            if prop not in all_props or all_props[prop] is None:
                issues.append({
                    'element': element_guid,
                    'issue': f'Missing property: {prop}',
                    'required_for': self.target_lod
                })

        # Check quantities
        required_quantities = self.requirements.get('quantities', [])
        if required_quantities != ['All']:
            qsets = psets.get('BaseQuantities', {})
            for qty in required_quantities:
                if qty not in qsets:
                    issues.append({
                        'element': element_guid,
                        'issue': f'Missing quantity: {qty}',
                        'required_for': self.target_lod
                    })

        return issues

    def validate_model(self, element_types=None):
        """Validate entire model"""
        if element_types is None:
            element_types = ['IfcWall', 'IfcSlab', 'IfcColumn', 'IfcBeam',
                            'IfcDoor', 'IfcWindow', 'IfcStair']

        all_issues = []
        summary = {}

        for ifc_type in element_types:
            elements = self.model.by_type(ifc_type)
            type_issues = []

            for element in elements:
                issues = self.validate_element(element)
                type_issues.extend(issues)

            summary[ifc_type] = {
                'total': len(elements),
                'issues': len(type_issues),
                'compliance': ((len(elements) - len(type_issues)) /
                              len(elements) * 100) if elements else 100
            }
            all_issues.extend(type_issues)

        return {
            'target_lod': self.target_lod,
            'total_issues': len(all_issues),
            'summary': summary,
            'issues': all_issues
        }
```

## IDS Validation

### Information Delivery Specification

```python
import xml.etree.ElementTree as ET

class IDSValidator:
    """Validate against IDS (Information Delivery Specification)"""

    def __init__(self, ids_path: str):
        self.ids = self._parse_ids(ids_path)

    def _parse_ids(self, path):
        """Parse IDS XML file"""
        tree = ET.parse(path)
        root = tree.getroot()

        specifications = []
        for spec in root.findall('.//specification'):
            specifications.append({
                'name': spec.get('name'),
                'applicability': self._parse_facets(spec.find('applicability')),
                'requirements': self._parse_facets(spec.find('requirements'))
            })

        return specifications

    def _parse_facets(self, element):
        """Parse IDS facets"""
        if element is None:
            return []

        facets = []
        for child in element:
            facet = {
                'type': child.tag,
                'constraints': {}
            }
            for attr, value in child.attrib.items():
                facet['constraints'][attr] = value
            facets.append(facet)

        return facets

    def validate(self, model):
        """Validate IFC model against IDS"""
        results = []

        for spec in self.ids:
            applicable_elements = self._find_applicable_elements(
                model, spec['applicability']
            )

            for element in applicable_elements:
                issues = self._check_requirements(element, spec['requirements'])
                if issues:
                    results.append({
                        'specification': spec['name'],
                        'element': element.GlobalId,
                        'issues': issues
                    })

        return results

    def _find_applicable_elements(self, model, applicability):
        """Find elements matching applicability criteria"""
        elements = []

        for facet in applicability:
            if facet['type'] == 'entity':
                ifc_type = facet['constraints'].get('name')
                if ifc_type:
                    elements.extend(model.by_type(ifc_type))

        return elements

    def _check_requirements(self, element, requirements):
        """Check element against requirements"""
        issues = []
        psets = element_util.get_psets(element)

        for req in requirements:
            if req['type'] == 'property':
                pset_name = req['constraints'].get('propertySet')
                prop_name = req['constraints'].get('name')

                if pset_name and prop_name:
                    pset = psets.get(pset_name, {})
                    if prop_name not in pset:
                        issues.append(f"Missing property: {pset_name}.{prop_name}")

        return issues
```

## Pipeline Automation

### Automated Validation Pipeline

```python
import os
from datetime import datetime
import json

class BIMValidationPipeline:
    """Automated BIM validation pipeline"""

    def __init__(self, config_path=None):
        self.config = self._load_config(config_path)
        self.results_history = []

    def _load_config(self, path):
        if path and os.path.exists(path):
            with open(path) as f:
                return json.load(f)

        return {
            'lod_target': 'LOD300',
            'required_psets': {
                'IfcWall': ['Pset_WallCommon'],
                'IfcSlab': ['Pset_SlabCommon']
            },
            'naming_patterns': {},
            'fail_on_errors': True,
            'warn_threshold': 50
        }

    def run(self, ifc_path):
        """Run complete validation pipeline"""
        start_time = datetime.now()

        # Initialize validators
        validator = BIMValidator(ifc_path)
        lod_validator = LODValidator(
            validator.model,
            self.config['lod_target']
        )

        # Run validations
        bim_report = validator.validate_all()
        lod_report = lod_validator.validate_model()

        # Compile results
        result = {
            'file': ifc_path,
            'timestamp': start_time.isoformat(),
            'duration_seconds': (datetime.now() - start_time).total_seconds(),
            'bim_validation': bim_report,
            'lod_validation': lod_report,
            'passed': self._evaluate_pass(bim_report, lod_report)
        }

        self.results_history.append(result)
        return result

    def _evaluate_pass(self, bim_report, lod_report):
        """Determine if validation passed"""
        if self.config['fail_on_errors'] and bim_report['errors'] > 0:
            return False

        if bim_report['warnings'] > self.config['warn_threshold']:
            return False

        return True

    def run_batch(self, ifc_paths):
        """Run validation on multiple files"""
        results = []
        for path in ifc_paths:
            try:
                result = self.run(path)
                results.append(result)
            except Exception as e:
                results.append({
                    'file': path,
                    'error': str(e),
                    'passed': False
                })

        return {
            'total': len(results),
            'passed': sum(1 for r in results if r.get('passed', False)),
            'failed': sum(1 for r in results if not r.get('passed', True)),
            'results': results
        }

    def export_report(self, output_path):
        """Export validation results to Excel"""
        if not self.results_history:
            return None

        latest = self.results_history[-1]

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary = pd.DataFrame({
                'Metric': ['File', 'Timestamp', 'Passed', 'Errors', 'Warnings'],
                'Value': [
                    latest['file'],
                    latest['timestamp'],
                    latest['passed'],
                    latest['bim_validation']['errors'],
                    latest['bim_validation']['warnings']
                ]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)

            # Issues
            if latest['bim_validation']['issues']:
                issues_df = pd.DataFrame([
                    {
                        'Element': i.element_id,
                        'Type': i.element_type,
                        'Rule': i.rule_id,
                        'Severity': i.severity.value,
                        'Message': i.message
                    }
                    for i in latest['bim_validation']['issues']
                ])
                issues_df.to_excel(writer, sheet_name='Issues', index=False)

        return output_path
```

## Quick Reference

| Rule ID | Description | Severity |
|---------|-------------|----------|
| GEO-001 | Invalid/missing geometry | ERROR |
| PROP-001 | Missing PropertySet | WARNING |
| REL-001 | No spatial containment | WARNING |
| MAT-001 | No material assigned | WARNING |
| NAME-001 | Invalid naming convention | INFO |
| CLASS-001 | No classification | INFO |

## LOD Requirements Summary

| LOD | Geometry | Properties | Quantities |
|-----|----------|------------|------------|
| 100 | No | - | - |
| 200 | Approximate | Category | - |
| 300 | Exact | Material, Type | L, A, V |
| 350 | Exact + connections | Manufacturer | All |
| 400 | Fabrication-ready | All details | All |

## Resources

- **Book**: "Data-Driven Construction" by Artem Boiko, Chapter 4.3
- **Website**: https://datadrivenconstruction.io
- **IDS Standard**: https://technical.buildingsmart.org/projects/information-delivery-specification-ids/
- **IfcOpenShell**: https://ifcopenshell.org

## Next Steps

- See `ifc-data-extraction` for extracting data from IFC
- See `data-quality-check` for general data validation
- See `qto-report` for quantity take-off from validated models
