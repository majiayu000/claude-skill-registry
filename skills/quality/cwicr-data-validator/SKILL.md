---
name: cwicr-data-validator
description: "Validate CWICR data quality and estimate inputs. Check for errors, inconsistencies, outliers, and missing data."
---

# CWICR Data Validator

## Business Case

### Problem Statement
Data quality issues cause:
- Incorrect estimates
- Budget overruns
- Delayed projects
- Rework costs

### Solution
Systematic validation of CWICR data and estimate inputs to catch errors, outliers, and inconsistencies before they impact projects.

### Business Value
- **Error prevention** - Catch issues early
- **Data quality** - Ensure reliable estimates
- **Consistency** - Standard validation rules
- **Audit trail** - Document data issues

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime


class ValidationSeverity(Enum):
    """Validation issue severity."""
    ERROR = "error"          # Must fix
    WARNING = "warning"      # Should review
    INFO = "info"            # For awareness


class ValidationCategory(Enum):
    """Validation categories."""
    MISSING_DATA = "missing_data"
    INVALID_VALUE = "invalid_value"
    OUTLIER = "outlier"
    DUPLICATE = "duplicate"
    INCONSISTENT = "inconsistent"
    FORMAT = "format"


@dataclass
class ValidationIssue:
    """Single validation issue."""
    field: str
    record_id: str
    category: ValidationCategory
    severity: ValidationSeverity
    message: str
    current_value: Any
    expected: str


@dataclass
class ValidationResult:
    """Complete validation result."""
    total_records: int
    valid_records: int
    issues: List[ValidationIssue]
    error_count: int
    warning_count: int
    info_count: int
    validation_date: datetime
    passed: bool


class CWICRDataValidator:
    """Validate CWICR data and estimates."""

    # Standard validation rules
    REQUIRED_FIELDS = ['work_item_code', 'description', 'unit']
    NUMERIC_FIELDS = ['labor_cost', 'material_cost', 'equipment_cost', 'labor_norm']
    POSITIVE_FIELDS = ['labor_cost', 'material_cost', 'equipment_cost', 'quantity']

    # Outlier detection thresholds (IQR multiplier)
    OUTLIER_THRESHOLD = 3.0

    def __init__(self, cwicr_reference: pd.DataFrame = None):
        self.reference = cwicr_reference
        if cwicr_reference is not None:
            self._build_reference_stats()

    def _build_reference_stats(self):
        """Build reference statistics for outlier detection."""
        self._stats = {}

        for col in self.NUMERIC_FIELDS:
            if col in self.reference.columns:
                values = pd.to_numeric(self.reference[col], errors='coerce').dropna()
                if len(values) > 0:
                    self._stats[col] = {
                        'mean': values.mean(),
                        'std': values.std(),
                        'q1': values.quantile(0.25),
                        'q3': values.quantile(0.75),
                        'iqr': values.quantile(0.75) - values.quantile(0.25)
                    }

    def validate_dataframe(self, df: pd.DataFrame) -> ValidationResult:
        """Validate entire dataframe."""

        issues = []
        valid_count = 0

        for idx, row in df.iterrows():
            row_issues = self._validate_row(row, str(idx))
            issues.extend(row_issues)

            if not any(i.severity == ValidationSeverity.ERROR for i in row_issues):
                valid_count += 1

        # Check for duplicates
        if 'work_item_code' in df.columns:
            duplicates = df[df.duplicated(subset=['work_item_code'], keep=False)]
            for idx, row in duplicates.iterrows():
                issues.append(ValidationIssue(
                    field='work_item_code',
                    record_id=str(idx),
                    category=ValidationCategory.DUPLICATE,
                    severity=ValidationSeverity.WARNING,
                    message=f"Duplicate work item code: {row['work_item_code']}",
                    current_value=row['work_item_code'],
                    expected="Unique codes"
                ))

        error_count = sum(1 for i in issues if i.severity == ValidationSeverity.ERROR)
        warning_count = sum(1 for i in issues if i.severity == ValidationSeverity.WARNING)
        info_count = sum(1 for i in issues if i.severity == ValidationSeverity.INFO)

        return ValidationResult(
            total_records=len(df),
            valid_records=valid_count,
            issues=issues,
            error_count=error_count,
            warning_count=warning_count,
            info_count=info_count,
            validation_date=datetime.now(),
            passed=error_count == 0
        )

    def _validate_row(self, row: pd.Series, record_id: str) -> List[ValidationIssue]:
        """Validate single row."""

        issues = []

        # Check required fields
        for field in self.REQUIRED_FIELDS:
            if field in row.index:
                value = row[field]
                if pd.isna(value) or str(value).strip() == '':
                    issues.append(ValidationIssue(
                        field=field,
                        record_id=record_id,
                        category=ValidationCategory.MISSING_DATA,
                        severity=ValidationSeverity.ERROR,
                        message=f"Required field '{field}' is missing",
                        current_value=value,
                        expected="Non-empty value"
                    ))

        # Check numeric fields
        for field in self.NUMERIC_FIELDS:
            if field in row.index:
                value = row[field]
                if pd.notna(value):
                    try:
                        num_val = float(value)
                        # Check for negative where positive expected
                        if field in self.POSITIVE_FIELDS and num_val < 0:
                            issues.append(ValidationIssue(
                                field=field,
                                record_id=record_id,
                                category=ValidationCategory.INVALID_VALUE,
                                severity=ValidationSeverity.ERROR,
                                message=f"Negative value in '{field}'",
                                current_value=value,
                                expected="Positive number"
                            ))

                        # Check for outliers
                        if self._stats and field in self._stats:
                            stats = self._stats[field]
                            lower = stats['q1'] - self.OUTLIER_THRESHOLD * stats['iqr']
                            upper = stats['q3'] + self.OUTLIER_THRESHOLD * stats['iqr']

                            if num_val < lower or num_val > upper:
                                issues.append(ValidationIssue(
                                    field=field,
                                    record_id=record_id,
                                    category=ValidationCategory.OUTLIER,
                                    severity=ValidationSeverity.WARNING,
                                    message=f"Outlier value in '{field}'",
                                    current_value=value,
                                    expected=f"Between {lower:.2f} and {upper:.2f}"
                                ))

                    except (ValueError, TypeError):
                        issues.append(ValidationIssue(
                            field=field,
                            record_id=record_id,
                            category=ValidationCategory.INVALID_VALUE,
                            severity=ValidationSeverity.ERROR,
                            message=f"Non-numeric value in '{field}'",
                            current_value=value,
                            expected="Numeric value"
                        ))

        # Check work item code format
        if 'work_item_code' in row.index:
            code = row['work_item_code']
            if pd.notna(code) and not self._valid_code_format(str(code)):
                issues.append(ValidationIssue(
                    field='work_item_code',
                    record_id=record_id,
                    category=ValidationCategory.FORMAT,
                    severity=ValidationSeverity.INFO,
                    message="Non-standard code format",
                    current_value=code,
                    expected="CATEGORY-NUMBER format"
                ))

        return issues

    def _valid_code_format(self, code: str) -> bool:
        """Check if code follows expected format."""
        # Expect format like "CONC-001" or "EXCV-DEEP-002"
        parts = code.split('-')
        return len(parts) >= 2 and parts[0].isalpha()

    def validate_estimate(self,
                          items: List[Dict[str, Any]],
                          check_against_cwicr: bool = True) -> ValidationResult:
        """Validate estimate items."""

        issues = []
        valid_count = 0

        for i, item in enumerate(items):
            record_id = str(i)
            item_issues = []

            # Check required fields
            code = item.get('work_item_code', item.get('code'))
            if not code:
                item_issues.append(ValidationIssue(
                    field='work_item_code',
                    record_id=record_id,
                    category=ValidationCategory.MISSING_DATA,
                    severity=ValidationSeverity.ERROR,
                    message="Missing work item code",
                    current_value=None,
                    expected="Valid work item code"
                ))

            # Check quantity
            qty = item.get('quantity', 0)
            if qty <= 0:
                item_issues.append(ValidationIssue(
                    field='quantity',
                    record_id=record_id,
                    category=ValidationCategory.INVALID_VALUE,
                    severity=ValidationSeverity.ERROR,
                    message="Invalid quantity",
                    current_value=qty,
                    expected="Positive number"
                ))

            # Check against CWICR reference
            if check_against_cwicr and self.reference is not None and code:
                if 'work_item_code' in self.reference.columns:
                    if code not in self.reference['work_item_code'].values:
                        item_issues.append(ValidationIssue(
                            field='work_item_code',
                            record_id=record_id,
                            category=ValidationCategory.INVALID_VALUE,
                            severity=ValidationSeverity.WARNING,
                            message=f"Work item code not found in CWICR: {code}",
                            current_value=code,
                            expected="Valid CWICR code"
                        ))

            issues.extend(item_issues)

            if not any(i.severity == ValidationSeverity.ERROR for i in item_issues):
                valid_count += 1

        return ValidationResult(
            total_records=len(items),
            valid_records=valid_count,
            issues=issues,
            error_count=sum(1 for i in issues if i.severity == ValidationSeverity.ERROR),
            warning_count=sum(1 for i in issues if i.severity == ValidationSeverity.WARNING),
            info_count=sum(1 for i in issues if i.severity == ValidationSeverity.INFO),
            validation_date=datetime.now(),
            passed=all(i.severity != ValidationSeverity.ERROR for i in issues)
        )

    def get_data_quality_score(self, result: ValidationResult) -> Dict[str, Any]:
        """Calculate data quality score."""

        if result.total_records == 0:
            return {'score': 0, 'grade': 'N/A'}

        # Weighted scoring
        error_weight = 10
        warning_weight = 3
        info_weight = 1

        total_deductions = (
            result.error_count * error_weight +
            result.warning_count * warning_weight +
            result.info_count * info_weight
        )

        max_deductions = result.total_records * error_weight
        score = max(0, 100 - (total_deductions / max_deductions * 100)) if max_deductions > 0 else 100

        # Assign grade
        if score >= 95:
            grade = 'A'
        elif score >= 85:
            grade = 'B'
        elif score >= 75:
            grade = 'C'
        elif score >= 60:
            grade = 'D'
        else:
            grade = 'F'

        return {
            'score': round(score, 1),
            'grade': grade,
            'total_records': result.total_records,
            'valid_records': result.valid_records,
            'error_count': result.error_count,
            'warning_count': result.warning_count
        }

    def export_validation_report(self,
                                  result: ValidationResult,
                                  output_path: str) -> str:
        """Export validation report to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            quality = self.get_data_quality_score(result)
            summary_df = pd.DataFrame([{
                'Total Records': result.total_records,
                'Valid Records': result.valid_records,
                'Errors': result.error_count,
                'Warnings': result.warning_count,
                'Info': result.info_count,
                'Quality Score': quality['score'],
                'Grade': quality['grade'],
                'Validation Date': result.validation_date,
                'Passed': result.passed
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Issues
            if result.issues:
                issues_df = pd.DataFrame([
                    {
                        'Record': i.record_id,
                        'Field': i.field,
                        'Category': i.category.value,
                        'Severity': i.severity.value,
                        'Message': i.message,
                        'Current Value': str(i.current_value),
                        'Expected': i.expected
                    }
                    for i in result.issues
                ])
                issues_df.to_excel(writer, sheet_name='Issues', index=False)

        return output_path
```

## Quick Start

```python
# Load CWICR reference
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize validator
validator = CWICRDataValidator(cwicr)

# Validate estimate
items = [
    {'work_item_code': 'CONC-001', 'quantity': 100},
    {'work_item_code': 'INVALID-CODE', 'quantity': -5}
]

result = validator.validate_estimate(items)
print(f"Passed: {result.passed}")
print(f"Errors: {result.error_count}")
```

## Common Use Cases

### 1. Data Quality Score
```python
quality = validator.get_data_quality_score(result)
print(f"Score: {quality['score']} ({quality['grade']})")
```

### 2. Validate DataFrame
```python
import_df = pd.read_excel("estimate_import.xlsx")
result = validator.validate_dataframe(import_df)

for issue in result.issues:
    if issue.severity == ValidationSeverity.ERROR:
        print(f"ERROR: {issue.message}")
```

### 3. Export Report
```python
validator.export_validation_report(result, "validation_report.xlsx")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 2.1 - Data Quality Management
