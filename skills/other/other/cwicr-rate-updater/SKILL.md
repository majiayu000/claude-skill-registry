---
slug: "cwicr-rate-updater"
display_name: "CWICR Rate Updater"
description: "Update CWICR resource rates with current market prices. Integrate external price data, apply inflation adjustments, and maintain rate history."
---

# CWICR Rate Updater

## Business Case

### Problem Statement
Resource rates become outdated:
- Material prices fluctuate with market
- Labor rates change annually
- Equipment costs vary by region
- Historical rates need adjustment

### Solution
Systematic rate updates integrating market data, inflation indices, and regional factors while maintaining audit trail.

### Business Value
- **Accuracy** - Current market pricing
- **Flexibility** - Update specific resources or categories
- **Audit trail** - Track rate changes over time
- **Automation** - Integrate with price APIs

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
import json


class RateType(Enum):
    """Types of rates."""
    LABOR = "labor"
    MATERIAL = "material"
    EQUIPMENT = "equipment"
    SUBCONTRACT = "subcontract"


class AdjustmentMethod(Enum):
    """Methods for rate adjustment."""
    FIXED_AMOUNT = "fixed_amount"
    PERCENTAGE = "percentage"
    MULTIPLIER = "multiplier"
    REPLACEMENT = "replacement"


@dataclass
class RateChange:
    """Record of rate change."""
    resource_code: str
    rate_type: RateType
    old_rate: float
    new_rate: float
    change_percent: float
    change_date: datetime
    reason: str
    source: str


@dataclass
class RateUpdateResult:
    """Result of rate update operation."""
    total_items: int
    updated: int
    unchanged: int
    errors: int
    changes: List[RateChange]
    summary: Dict[str, Any]


class CWICRRateUpdater:
    """Update resource rates in CWICR data."""

    def __init__(self, cwicr_data: pd.DataFrame):
        self.data = cwicr_data.copy()
        self.change_log: List[RateChange] = []
        self.original_data = cwicr_data.copy()

    def get_current_rates(self,
                          rate_type: RateType = None,
                          category: str = None) -> pd.DataFrame:
        """Get current rates, optionally filtered."""

        df = self.data.copy()

        # Filter by category if specified
        if category and 'category' in df.columns:
            df = df[df['category'].str.contains(category, case=False, na=False)]

        # Select relevant columns based on rate type
        rate_columns = {
            RateType.LABOR: ['work_item_code', 'description', 'labor_rate', 'labor_cost'],
            RateType.MATERIAL: ['work_item_code', 'description', 'material_cost'],
            RateType.EQUIPMENT: ['work_item_code', 'description', 'equipment_cost', 'equipment_rate']
        }

        if rate_type and rate_type in rate_columns:
            cols = [c for c in rate_columns[rate_type] if c in df.columns]
            return df[cols]

        return df

    def update_rate(self,
                    work_item_code: str,
                    rate_type: RateType,
                    new_rate: float,
                    reason: str = "Manual update",
                    source: str = "User") -> Optional[RateChange]:
        """Update single rate."""

        rate_column = self._get_rate_column(rate_type)
        if rate_column not in self.data.columns:
            return None

        mask = self.data['work_item_code'] == work_item_code
        if not mask.any():
            return None

        old_rate = float(self.data.loc[mask, rate_column].iloc[0])
        self.data.loc[mask, rate_column] = new_rate

        change_percent = ((new_rate - old_rate) / old_rate * 100) if old_rate > 0 else 0

        change = RateChange(
            resource_code=work_item_code,
            rate_type=rate_type,
            old_rate=old_rate,
            new_rate=new_rate,
            change_percent=round(change_percent, 2),
            change_date=datetime.now(),
            reason=reason,
            source=source
        )

        self.change_log.append(change)
        return change

    def _get_rate_column(self, rate_type: RateType) -> str:
        """Get column name for rate type."""
        mapping = {
            RateType.LABOR: 'labor_rate',
            RateType.MATERIAL: 'material_cost',
            RateType.EQUIPMENT: 'equipment_cost',
            RateType.SUBCONTRACT: 'subcontract_cost'
        }
        return mapping.get(rate_type, 'labor_rate')

    def apply_percentage_adjustment(self,
                                     rate_type: RateType,
                                     percentage: float,
                                     category: str = None,
                                     reason: str = "Percentage adjustment") -> RateUpdateResult:
        """Apply percentage adjustment to rates."""

        rate_column = self._get_rate_column(rate_type)
        if rate_column not in self.data.columns:
            return RateUpdateResult(0, 0, 0, 1, [], {})

        # Build mask
        mask = pd.Series([True] * len(self.data))
        if category and 'category' in self.data.columns:
            mask = self.data['category'].str.contains(category, case=False, na=False)

        # Store old values
        old_values = self.data.loc[mask, rate_column].copy()

        # Apply adjustment
        multiplier = 1 + (percentage / 100)
        self.data.loc[mask, rate_column] = old_values * multiplier

        # Record changes
        changes = []
        for idx in self.data[mask].index:
            old_rate = float(old_values.loc[idx])
            new_rate = float(self.data.loc[idx, rate_column])

            if old_rate != new_rate:
                change = RateChange(
                    resource_code=str(self.data.loc[idx, 'work_item_code']),
                    rate_type=rate_type,
                    old_rate=old_rate,
                    new_rate=new_rate,
                    change_percent=percentage,
                    change_date=datetime.now(),
                    reason=reason,
                    source=f"Bulk {percentage}%"
                )
                changes.append(change)
                self.change_log.append(change)

        return RateUpdateResult(
            total_items=len(self.data[mask]),
            updated=len(changes),
            unchanged=len(self.data[mask]) - len(changes),
            errors=0,
            changes=changes,
            summary={
                'rate_type': rate_type.value,
                'adjustment_percent': percentage,
                'category': category,
                'average_new_rate': self.data.loc[mask, rate_column].mean()
            }
        )

    def apply_inflation_index(self,
                               base_year: int,
                               current_year: int,
                               inflation_rates: Dict[int, float],
                               rate_types: List[RateType] = None) -> RateUpdateResult:
        """Apply inflation index from base year to current."""

        if rate_types is None:
            rate_types = [RateType.LABOR, RateType.MATERIAL, RateType.EQUIPMENT]

        # Calculate cumulative multiplier
        cumulative_multiplier = 1.0
        for year in range(base_year, current_year):
            rate = inflation_rates.get(year, 0.02)  # Default 2%
            cumulative_multiplier *= (1 + rate)

        total_changes = []

        for rate_type in rate_types:
            result = self.apply_percentage_adjustment(
                rate_type=rate_type,
                percentage=(cumulative_multiplier - 1) * 100,
                reason=f"Inflation {base_year}-{current_year}"
            )
            total_changes.extend(result.changes)

        return RateUpdateResult(
            total_items=len(self.data),
            updated=len(total_changes),
            unchanged=len(self.data) - len(total_changes),
            errors=0,
            changes=total_changes,
            summary={
                'base_year': base_year,
                'current_year': current_year,
                'cumulative_multiplier': round(cumulative_multiplier, 4),
                'total_adjustment_percent': round((cumulative_multiplier - 1) * 100, 2)
            }
        )

    def import_external_rates(self,
                               external_data: pd.DataFrame,
                               code_column: str,
                               rate_column: str,
                               rate_type: RateType,
                               match_on: str = 'work_item_code') -> RateUpdateResult:
        """Import rates from external data source."""

        changes = []
        errors = 0
        target_column = self._get_rate_column(rate_type)

        for _, row in external_data.iterrows():
            code = row[code_column]
            new_rate = row[rate_column]

            try:
                change = self.update_rate(
                    work_item_code=code,
                    rate_type=rate_type,
                    new_rate=new_rate,
                    reason="External import",
                    source="External data"
                )
                if change:
                    changes.append(change)
            except Exception:
                errors += 1

        return RateUpdateResult(
            total_items=len(external_data),
            updated=len(changes),
            unchanged=len(external_data) - len(changes) - errors,
            errors=errors,
            changes=changes,
            summary={
                'source': 'External import',
                'rate_type': rate_type.value
            }
        )

    def apply_regional_factors(self,
                                region_factors: Dict[str, float],
                                default_factor: float = 1.0) -> RateUpdateResult:
        """Apply regional adjustment factors."""

        # This assumes region column exists or applies uniformly
        factor = region_factors.get('default', default_factor)

        labor_result = self.apply_percentage_adjustment(
            RateType.LABOR,
            (region_factors.get('labor', factor) - 1) * 100,
            reason="Regional adjustment"
        )

        material_result = self.apply_percentage_adjustment(
            RateType.MATERIAL,
            (region_factors.get('material', factor) - 1) * 100,
            reason="Regional adjustment"
        )

        equipment_result = self.apply_percentage_adjustment(
            RateType.EQUIPMENT,
            (region_factors.get('equipment', factor) - 1) * 100,
            reason="Regional adjustment"
        )

        all_changes = (labor_result.changes + material_result.changes +
                       equipment_result.changes)

        return RateUpdateResult(
            total_items=len(self.data),
            updated=len(all_changes),
            unchanged=len(self.data) * 3 - len(all_changes),
            errors=0,
            changes=all_changes,
            summary={
                'region_factors': region_factors,
                'labor_adjusted': len(labor_result.changes),
                'material_adjusted': len(material_result.changes),
                'equipment_adjusted': len(equipment_result.changes)
            }
        )

    def get_change_log(self,
                        start_date: datetime = None,
                        rate_type: RateType = None) -> List[RateChange]:
        """Get change log, optionally filtered."""

        changes = self.change_log

        if start_date:
            changes = [c for c in changes if c.change_date >= start_date]

        if rate_type:
            changes = [c for c in changes if c.rate_type == rate_type]

        return changes

    def export_change_log(self, output_path: str) -> str:
        """Export change log to Excel."""

        df = pd.DataFrame([
            {
                'Resource Code': c.resource_code,
                'Rate Type': c.rate_type.value,
                'Old Rate': c.old_rate,
                'New Rate': c.new_rate,
                'Change %': c.change_percent,
                'Date': c.change_date.strftime('%Y-%m-%d %H:%M'),
                'Reason': c.reason,
                'Source': c.source
            }
            for c in self.change_log
        ])

        df.to_excel(output_path, index=False)
        return output_path

    def rollback_changes(self,
                          since: datetime = None) -> int:
        """Rollback changes since date (returns to original data)."""

        if since is None:
            # Full rollback
            self.data = self.original_data.copy()
            count = len(self.change_log)
            self.change_log = []
            return count

        # Partial rollback - more complex, would need versioning
        return 0

    def export_updated_data(self, output_path: str) -> str:
        """Export updated CWICR data."""

        if output_path.endswith('.parquet'):
            self.data.to_parquet(output_path)
        else:
            self.data.to_excel(output_path, index=False)

        return output_path


class RateScheduler:
    """Schedule automatic rate updates."""

    def __init__(self, updater: CWICRRateUpdater):
        self.updater = updater
        self.schedules: List[Dict[str, Any]] = []

    def add_annual_labor_increase(self,
                                   percentage: float,
                                   effective_date: date) -> Dict[str, Any]:
        """Schedule annual labor rate increase."""

        schedule = {
            'id': len(self.schedules) + 1,
            'type': 'annual_labor',
            'percentage': percentage,
            'effective_date': effective_date,
            'rate_type': RateType.LABOR,
            'status': 'scheduled'
        }
        self.schedules.append(schedule)
        return schedule

    def execute_due_updates(self, current_date: date = None) -> List[RateUpdateResult]:
        """Execute all updates that are due."""

        if current_date is None:
            current_date = date.today()

        results = []

        for schedule in self.schedules:
            if schedule['status'] == 'scheduled' and schedule['effective_date'] <= current_date:
                result = self.updater.apply_percentage_adjustment(
                    rate_type=schedule['rate_type'],
                    percentage=schedule['percentage'],
                    reason=f"Scheduled {schedule['type']}"
                )
                schedule['status'] = 'executed'
                schedule['executed_date'] = current_date
                results.append(result)

        return results
```

## Quick Start

```python
# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize updater
updater = CWICRRateUpdater(cwicr)

# Apply 5% labor rate increase
result = updater.apply_percentage_adjustment(
    rate_type=RateType.LABOR,
    percentage=5.0,
    reason="2024 Annual Increase"
)

print(f"Updated {result.updated} labor rates")
print(f"Average adjustment: {result.summary.get('adjustment_percent')}%")
```

## Common Use Cases

### 1. Inflation Adjustment
```python
inflation_rates = {
    2020: 0.012, 2021: 0.047, 2022: 0.065, 2023: 0.034
}
result = updater.apply_inflation_index(
    base_year=2020,
    current_year=2024,
    inflation_rates=inflation_rates
)
print(f"Cumulative adjustment: {result.summary['total_adjustment_percent']}%")
```

### 2. Regional Factors
```python
berlin_factors = {
    'labor': 1.15,
    'material': 0.95,
    'equipment': 1.05
}
result = updater.apply_regional_factors(berlin_factors)
```

### 3. Import External Prices
```python
market_prices = pd.read_excel("current_prices.xlsx")
result = updater.import_external_rates(
    external_data=market_prices,
    code_column='item_code',
    rate_column='price',
    rate_type=RateType.MATERIAL
)
```

### 4. Export Audit Trail
```python
updater.export_change_log("rate_changes_2024.xlsx")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Rate Management
