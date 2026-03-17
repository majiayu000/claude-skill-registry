---
name: "payment-application-generator"
description: "Generate AIA-style payment applications. Track schedule of values, calculate retention, and produce payment documentation."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "💰", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Payment Application Generator

## Business Case

### Problem Statement
Payment applications are error-prone:
- Manual calculations cause mistakes
- Retention tracking is complex
- Inconsistent documentation
- Delayed submissions affect cash flow

### Solution
Automated payment application generation with schedule of values tracking, retention calculations, and standard format output.

### Business Value
- **Accuracy** - Eliminate calculation errors
- **Speed** - Faster billing cycle
- **Cash flow** - Timely payments
- **Compliance** - Standard documentation

## Technical Implementation

```python
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class SOVStatus(Enum):
    """Schedule of Values item status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    STORED_MATERIAL = "stored_material"


@dataclass
class SOVItem:
    """Schedule of Values line item."""
    item_number: str
    description: str
    scheduled_value: float
    work_completed_previous: float
    work_completed_current: float
    materials_stored_previous: float
    materials_stored_current: float
    total_completed_previous: float

    @property
    def total_completed_current(self) -> float:
        """Total completed and stored this period."""
        return (self.work_completed_previous + self.work_completed_current +
                self.materials_stored_previous + self.materials_stored_current)

    @property
    def percent_complete(self) -> float:
        """Percent of scheduled value complete."""
        if self.scheduled_value == 0:
            return 0
        return (self.total_completed_current / self.scheduled_value) * 100

    @property
    def balance_to_finish(self) -> float:
        """Remaining value."""
        return self.scheduled_value - self.total_completed_current


@dataclass
class PaymentApplication:
    """Payment application (AIA G702/G703 style)."""
    application_number: int
    period_from: date
    period_to: date
    project_name: str
    contractor: str
    owner: str
    contract_sum: float
    change_orders_amount: float
    retainage_percent: float

    items: List[SOVItem] = field(default_factory=list)
    approved_date: Optional[date] = None
    approved_by: str = ""

    @property
    def total_contract_sum(self) -> float:
        """Original contract plus approved changes."""
        return self.contract_sum + self.change_orders_amount

    @property
    def total_completed_this_period(self) -> float:
        """Work completed this billing period."""
        return sum(item.work_completed_current + item.materials_stored_current
                  for item in self.items)

    @property
    def total_completed_to_date(self) -> float:
        """Total completed and stored to date."""
        return sum(item.total_completed_current for item in self.items)

    @property
    def retainage_amount(self) -> float:
        """Total retainage held."""
        return self.total_completed_to_date * self.retainage_percent

    @property
    def total_earned_less_retainage(self) -> float:
        """Amount earned less retainage."""
        return self.total_completed_to_date - self.retainage_amount

    @property
    def balance_to_finish(self) -> float:
        """Remaining contract balance."""
        return self.total_contract_sum - self.total_completed_to_date


class PaymentApplicationGenerator:
    """Generate and manage payment applications."""

    DEFAULT_RETAINAGE = 0.10

    def __init__(self, project_name: str, contractor: str, owner: str,
                 original_contract: float, retainage: float = None):
        self.project_name = project_name
        self.contractor = contractor
        self.owner = owner
        self.original_contract = original_contract
        self.retainage_percent = retainage or self.DEFAULT_RETAINAGE
        self.sov_items: Dict[str, SOVItem] = {}
        self.applications: List[PaymentApplication] = []
        self.change_orders_total: float = 0

    def setup_sov(self, items: List[Dict[str, Any]]):
        """Initialize Schedule of Values."""
        for item in items:
            sov = SOVItem(
                item_number=item['number'],
                description=item['description'],
                scheduled_value=item['value'],
                work_completed_previous=0,
                work_completed_current=0,
                materials_stored_previous=0,
                materials_stored_current=0,
                total_completed_previous=0
            )
            self.sov_items[item['number']] = sov

    def add_change_order(self, amount: float, description: str, item_number: str = None):
        """Add approved change order to contract."""
        self.change_orders_total += amount

        if item_number:
            # Add to existing item
            if item_number in self.sov_items:
                self.sov_items[item_number].scheduled_value += amount
        else:
            # Create new line item
            new_number = f"CO-{len([i for i in self.sov_items if 'CO' in i]) + 1:02d}"
            self.sov_items[new_number] = SOVItem(
                item_number=new_number,
                description=f"Change Order: {description}",
                scheduled_value=amount,
                work_completed_previous=0,
                work_completed_current=0,
                materials_stored_previous=0,
                materials_stored_current=0,
                total_completed_previous=0
            )

    def create_application(self, period_from: date, period_to: date,
                          progress: Dict[str, Dict[str, float]]) -> PaymentApplication:
        """Create new payment application."""
        app_number = len(self.applications) + 1

        # Update progress for each item
        items_copy = []
        for item_num, sov in self.sov_items.items():
            # Carry forward previous values
            updated_sov = SOVItem(
                item_number=sov.item_number,
                description=sov.description,
                scheduled_value=sov.scheduled_value,
                work_completed_previous=sov.total_completed_current - sov.materials_stored_current,
                work_completed_current=0,
                materials_stored_previous=sov.materials_stored_current,
                materials_stored_current=0,
                total_completed_previous=sov.total_completed_current
            )

            # Apply current period progress
            if item_num in progress:
                prog = progress[item_num]
                if 'work' in prog:
                    updated_sov.work_completed_current = prog['work']
                if 'materials' in prog:
                    updated_sov.materials_stored_current = prog['materials']

            items_copy.append(updated_sov)

            # Update master SOV
            self.sov_items[item_num] = SOVItem(
                item_number=updated_sov.item_number,
                description=updated_sov.description,
                scheduled_value=updated_sov.scheduled_value,
                work_completed_previous=updated_sov.work_completed_previous + updated_sov.work_completed_current,
                work_completed_current=0,
                materials_stored_previous=updated_sov.materials_stored_previous + updated_sov.materials_stored_current,
                materials_stored_current=0,
                total_completed_previous=updated_sov.total_completed_current
            )

        application = PaymentApplication(
            application_number=app_number,
            period_from=period_from,
            period_to=period_to,
            project_name=self.project_name,
            contractor=self.contractor,
            owner=self.owner,
            contract_sum=self.original_contract,
            change_orders_amount=self.change_orders_total,
            retainage_percent=self.retainage_percent,
            items=items_copy
        )

        self.applications.append(application)
        return application

    def calculate_payment_due(self, application: PaymentApplication,
                             previous_payments: float = None) -> Dict[str, float]:
        """Calculate payment due for application."""
        if previous_payments is None:
            # Calculate from previous applications
            previous_payments = sum(
                app.total_earned_less_retainage
                for app in self.applications[:-1]
            )

        current_payment = application.total_earned_less_retainage - previous_payments

        return {
            'total_completed_to_date': application.total_completed_to_date,
            'retainage_held': application.retainage_amount,
            'total_earned_less_retainage': application.total_earned_less_retainage,
            'previous_payments': previous_payments,
            'current_payment_due': current_payment,
            'balance_to_finish': application.balance_to_finish,
            'percent_complete': round(
                application.total_completed_to_date / application.total_contract_sum * 100, 1
            ) if application.total_contract_sum > 0 else 0
        }

    def generate_g702(self, application: PaymentApplication) -> Dict[str, Any]:
        """Generate AIA G702 Application summary."""
        payment = self.calculate_payment_due(application)

        return {
            'document': 'AIA Document G702',
            'application_number': application.application_number,
            'period_to': application.period_to.isoformat(),
            'project': application.project_name,
            'contractor': application.contractor,
            'owner': application.owner,
            'original_contract_sum': application.contract_sum,
            'net_change_orders': application.change_orders_amount,
            'contract_sum_to_date': application.total_contract_sum,
            'total_completed_to_date': payment['total_completed_to_date'],
            'retainage': {
                'percent': application.retainage_percent * 100,
                'amount': payment['retainage_held']
            },
            'total_earned_less_retainage': payment['total_earned_less_retainage'],
            'previous_certificates': payment['previous_payments'],
            'current_payment_due': payment['current_payment_due'],
            'balance_to_finish': payment['balance_to_finish']
        }

    def generate_g703(self, application: PaymentApplication) -> pd.DataFrame:
        """Generate AIA G703 Continuation Sheet."""
        data = []
        for item in application.items:
            data.append({
                'Item No.': item.item_number,
                'Description': item.description,
                'Scheduled Value': item.scheduled_value,
                'Work Completed - Previous': item.work_completed_previous,
                'Work Completed - This Period': item.work_completed_current,
                'Materials Stored - Previous': item.materials_stored_previous,
                'Materials Stored - This Period': item.materials_stored_current,
                'Total Completed & Stored': item.total_completed_current,
                '% Complete': round(item.percent_complete, 1),
                'Balance to Finish': item.balance_to_finish,
                'Retainage': item.total_completed_current * application.retainage_percent
            })

        # Add totals row
        df = pd.DataFrame(data)
        totals = df.select_dtypes(include='number').sum()
        totals['Item No.'] = ''
        totals['Description'] = 'TOTALS'
        totals['% Complete'] = round(
            application.total_completed_to_date / application.total_contract_sum * 100, 1
        ) if application.total_contract_sum > 0 else 0

        df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)
        return df

    def export_application(self, application: PaymentApplication, output_path: str):
        """Export payment application to Excel."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # G702 Summary
            g702 = self.generate_g702(application)
            g702_df = pd.DataFrame([{'Field': k, 'Value': v} for k, v in g702.items()
                                   if not isinstance(v, dict)])
            g702_df.to_excel(writer, sheet_name='G702 Summary', index=False)

            # G703 Continuation
            g703 = self.generate_g703(application)
            g703.to_excel(writer, sheet_name='G703 Continuation', index=False)

        return output_path
```

## Quick Start

```python
from datetime import date

# Initialize generator
generator = PaymentApplicationGenerator(
    project_name="Office Tower",
    contractor="ABC Construction",
    owner="XYZ Development",
    original_contract=10000000,
    retainage=0.10
)

# Setup Schedule of Values
generator.setup_sov([
    {'number': '01', 'description': 'General Conditions', 'value': 500000},
    {'number': '02', 'description': 'Site Work', 'value': 800000},
    {'number': '03', 'description': 'Concrete', 'value': 2000000},
])

# Create application with progress
app = generator.create_application(
    period_from=date(2024, 1, 1),
    period_to=date(2024, 1, 31),
    progress={
        '01': {'work': 50000},
        '02': {'work': 200000, 'materials': 50000},
        '03': {'work': 100000}
    }
)

# Calculate payment
payment = generator.calculate_payment_due(app)
print(f"Current Payment Due: ${payment['current_payment_due']:,.2f}")
```

## Common Use Cases

### 1. Generate G702/G703
```python
g702 = generator.generate_g702(app)
g703 = generator.generate_g703(app)
```

### 2. Export Application
```python
generator.export_application(app, "pay_app_001.xlsx")
```

### 3. Add Change Order
```python
generator.add_change_order(150000, "Additional MEP work", item_number='03')
```

## Resources
- **DDC Book**: Chapter 3.1 - Cost Management
- **Reference**: AIA Documents G702, G703
