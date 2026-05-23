---
name: "subcontractor-prequalification"
description: "Prequalify subcontractors based on safety, financial, and performance criteria."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🛒", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Subcontractor Prequalification

## Technical Implementation

```python
import pandas as pd
from datetime import date
from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


class QualificationStatus(Enum):
    PENDING = "pending"
    QUALIFIED = "qualified"
    CONDITIONALLY_QUALIFIED = "conditionally_qualified"
    NOT_QUALIFIED = "not_qualified"


@dataclass
class PrequalificationCriteria:
    name: str
    weight: float
    min_score: int
    max_score: int = 10


@dataclass
class SubcontractorApplication:
    app_id: str
    company_name: str
    trade: str
    contact_email: str
    years_in_business: int
    annual_revenue: float
    bonding_capacity: float
    emr_rate: float  # Experience Modification Rate
    status: QualificationStatus
    scores: Dict[str, int] = field(default_factory=dict)
    documents_received: List[str] = field(default_factory=list)
    notes: str = ""

    @property
    def total_score(self) -> float:
        return sum(self.scores.values())


class SubcontractorPrequalification:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.applications: Dict[str, SubcontractorApplication] = {}
        self.criteria = self._default_criteria()
        self._counter = 0

    def _default_criteria(self) -> List[PrequalificationCriteria]:
        return [
            PrequalificationCriteria("Safety Record", 0.25, 6),
            PrequalificationCriteria("Financial Stability", 0.20, 5),
            PrequalificationCriteria("Experience", 0.20, 6),
            PrequalificationCriteria("References", 0.15, 5),
            PrequalificationCriteria("Capacity", 0.10, 5),
            PrequalificationCriteria("Insurance/Bonding", 0.10, 7)
        ]

    def add_application(self, company_name: str, trade: str, contact_email: str,
                       years_in_business: int, annual_revenue: float,
                       bonding_capacity: float, emr_rate: float) -> SubcontractorApplication:
        self._counter += 1
        app_id = f"PQ-{self._counter:03d}"

        app = SubcontractorApplication(
            app_id=app_id,
            company_name=company_name,
            trade=trade,
            contact_email=contact_email,
            years_in_business=years_in_business,
            annual_revenue=annual_revenue,
            bonding_capacity=bonding_capacity,
            emr_rate=emr_rate,
            status=QualificationStatus.PENDING
        )
        self.applications[app_id] = app
        return app

    def score_application(self, app_id: str, scores: Dict[str, int]):
        if app_id not in self.applications:
            return
        app = self.applications[app_id]
        app.scores = scores
        self._evaluate_qualification(app)

    def _evaluate_qualification(self, app: SubcontractorApplication):
        passed = True
        for criteria in self.criteria:
            score = app.scores.get(criteria.name, 0)
            if score < criteria.min_score:
                passed = False
                break

        if passed and app.total_score >= 60:
            app.status = QualificationStatus.QUALIFIED
        elif app.total_score >= 50:
            app.status = QualificationStatus.CONDITIONALLY_QUALIFIED
        else:
            app.status = QualificationStatus.NOT_QUALIFIED

    def get_qualified(self, trade: str = None) -> List[SubcontractorApplication]:
        qualified = [a for a in self.applications.values()
                    if a.status in [QualificationStatus.QUALIFIED,
                                   QualificationStatus.CONDITIONALLY_QUALIFIED]]
        if trade:
            qualified = [a for a in qualified if a.trade.lower() == trade.lower()]
        return qualified

    def export_register(self, output_path: str):
        data = [{
            'ID': a.app_id,
            'Company': a.company_name,
            'Trade': a.trade,
            'Years': a.years_in_business,
            'Revenue': a.annual_revenue,
            'EMR': a.emr_rate,
            'Status': a.status.value,
            'Score': a.total_score
        } for a in self.applications.values()]
        pd.DataFrame(data).to_excel(output_path, index=False)
```

## Quick Start

```python
prequal = SubcontractorPrequalification("Office Tower")

app = prequal.add_application("ABC Electric", "Electrical", "info@abc.com",
                              years_in_business=15, annual_revenue=10000000,
                              bonding_capacity=5000000, emr_rate=0.85)

prequal.score_application(app.app_id, {
    "Safety Record": 8, "Financial Stability": 7, "Experience": 8,
    "References": 7, "Capacity": 8, "Insurance/Bonding": 9
})

qualified = prequal.get_qualified("Electrical")
```

## Resources
- **DDC Book**: Chapter 3.4 - Procurement
