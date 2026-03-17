---
name: "labor-productivity-analyzer"
description: "Analyze labor productivity by trade, activity, and location. Track efficiency and identify improvement opportunities."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "👷", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Labor Productivity Analyzer

## Technical Implementation

```python
import pandas as pd
from datetime import date
from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


class ProductivityStatus(Enum):
    EXCEEDING = "exceeding"
    ON_TARGET = "on_target"
    BELOW_TARGET = "below_target"
    CRITICAL = "critical"


@dataclass
class ProductivityEntry:
    entry_id: str
    date: date
    trade: str
    activity_code: str
    activity_description: str
    location: str
    crew_size: int
    hours_worked: float
    quantity_installed: float
    unit: str
    target_productivity: float  # units per hour

    @property
    def actual_productivity(self) -> float:
        if self.hours_worked == 0:
            return 0
        return self.quantity_installed / self.hours_worked

    @property
    def productivity_factor(self) -> float:
        if self.target_productivity == 0:
            return 0
        return self.actual_productivity / self.target_productivity

    @property
    def status(self) -> ProductivityStatus:
        pf = self.productivity_factor
        if pf >= 1.1:
            return ProductivityStatus.EXCEEDING
        elif pf >= 0.9:
            return ProductivityStatus.ON_TARGET
        elif pf >= 0.7:
            return ProductivityStatus.BELOW_TARGET
        return ProductivityStatus.CRITICAL


class LaborProductivityAnalyzer:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.entries: List[ProductivityEntry] = []
        self.targets: Dict[str, float] = {}  # activity_code: target_productivity
        self._counter = 0

    def set_target(self, activity_code: str, target_productivity: float):
        self.targets[activity_code] = target_productivity

    def add_entry(self, entry_date: date, trade: str, activity_code: str,
                 activity_description: str, location: str, crew_size: int,
                 hours_worked: float, quantity_installed: float,
                 unit: str) -> ProductivityEntry:
        self._counter += 1
        entry_id = f"PROD-{self._counter:05d}"

        target = self.targets.get(activity_code, 1.0)

        entry = ProductivityEntry(
            entry_id=entry_id,
            date=entry_date,
            trade=trade,
            activity_code=activity_code,
            activity_description=activity_description,
            location=location,
            crew_size=crew_size,
            hours_worked=hours_worked,
            quantity_installed=quantity_installed,
            unit=unit,
            target_productivity=target
        )
        self.entries.append(entry)
        return entry

    def get_productivity_by_trade(self) -> Dict[str, Dict[str, Any]]:
        by_trade = {}
        for entry in self.entries:
            if entry.trade not in by_trade:
                by_trade[entry.trade] = {'hours': 0, 'quantity': 0, 'entries': 0}
            by_trade[entry.trade]['hours'] += entry.hours_worked
            by_trade[entry.trade]['quantity'] += entry.quantity_installed
            by_trade[entry.trade]['entries'] += 1

        for trade in by_trade:
            hours = by_trade[trade]['hours']
            qty = by_trade[trade]['quantity']
            by_trade[trade]['avg_productivity'] = qty / hours if hours > 0 else 0

        return by_trade

    def get_productivity_by_activity(self) -> Dict[str, Dict[str, Any]]:
        by_activity = {}
        for entry in self.entries:
            code = entry.activity_code
            if code not in by_activity:
                by_activity[code] = {
                    'description': entry.activity_description,
                    'hours': 0, 'quantity': 0, 'target': entry.target_productivity
                }
            by_activity[code]['hours'] += entry.hours_worked
            by_activity[code]['quantity'] += entry.quantity_installed

        for code in by_activity:
            hours = by_activity[code]['hours']
            qty = by_activity[code]['quantity']
            by_activity[code]['actual'] = qty / hours if hours > 0 else 0
            by_activity[code]['factor'] = (
                by_activity[code]['actual'] / by_activity[code]['target']
                if by_activity[code]['target'] > 0 else 0
            )

        return by_activity

    def get_low_performers(self) -> List[ProductivityEntry]:
        return [e for e in self.entries
                if e.status in [ProductivityStatus.BELOW_TARGET, ProductivityStatus.CRITICAL]]

    def get_summary(self) -> Dict[str, Any]:
        if not self.entries:
            return {'total_entries': 0}

        total_hours = sum(e.hours_worked for e in self.entries)
        factors = [e.productivity_factor for e in self.entries]
        avg_factor = sum(factors) / len(factors)

        return {
            'total_entries': len(self.entries),
            'total_hours': total_hours,
            'average_productivity_factor': round(avg_factor, 2),
            'exceeding': sum(1 for e in self.entries if e.status == ProductivityStatus.EXCEEDING),
            'on_target': sum(1 for e in self.entries if e.status == ProductivityStatus.ON_TARGET),
            'below_target': sum(1 for e in self.entries if e.status == ProductivityStatus.BELOW_TARGET),
            'critical': sum(1 for e in self.entries if e.status == ProductivityStatus.CRITICAL)
        }

    def export_report(self, output_path: str):
        data = [{
            'Date': e.date,
            'Trade': e.trade,
            'Activity': e.activity_code,
            'Location': e.location,
            'Crew': e.crew_size,
            'Hours': e.hours_worked,
            'Quantity': e.quantity_installed,
            'Unit': e.unit,
            'Target': e.target_productivity,
            'Actual': round(e.actual_productivity, 2),
            'Factor': round(e.productivity_factor, 2),
            'Status': e.status.value
        } for e in self.entries]
        pd.DataFrame(data).to_excel(output_path, index=False)
```

## Quick Start

```python
analyzer = LaborProductivityAnalyzer("Office Tower")

# Set targets
analyzer.set_target("CONC-001", 2.5)  # m3 per hour

# Add entry
entry = analyzer.add_entry(
    entry_date=date.today(),
    trade="Concrete",
    activity_code="CONC-001",
    activity_description="Pour concrete slab",
    location="Level 3",
    crew_size=8,
    hours_worked=80,
    quantity_installed=180,
    unit="m3"
)

print(f"Productivity factor: {entry.productivity_factor:.2f}")
print(f"Status: {entry.status.value}")
```

## Resources
- **DDC Book**: Chapter 3.2 - Resource Management
