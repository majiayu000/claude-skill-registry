---
name: "change-order-analysis"
description: "Analyze and predict construction change orders using ML. Classify change order types, predict costs and schedule impacts, identify patterns, and optimize approval workflows."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🚀", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Change Order Analysis

## Overview

This skill implements machine learning-based change order analysis for construction projects. Predict change order costs, classify types, identify patterns in historical data, and streamline approval processes.

**Capabilities:**
- Change order classification
- Cost impact prediction
- Schedule impact analysis
- Pattern identification
- Root cause analysis
- Approval workflow optimization

## Quick Start

```python
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Dict, Optional
from enum import Enum

class ChangeOrderType(Enum):
    DESIGN_CHANGE = "design_change"
    OWNER_REQUEST = "owner_request"
    FIELD_CONDITION = "field_condition"
    CODE_COMPLIANCE = "code_compliance"
    VALUE_ENGINEERING = "value_engineering"
    ERROR_OMISSION = "error_omission"
    SCOPE_CHANGE = "scope_change"

class ChangeOrderStatus(Enum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"

@dataclass
class ChangeOrder:
    co_number: str
    title: str
    description: str
    co_type: ChangeOrderType
    status: ChangeOrderStatus
    submitted_date: date
    requested_by: str
    cost_impact: float
    schedule_impact_days: int
    affected_elements: List[str] = field(default_factory=list)

def classify_change_order(description: str) -> ChangeOrderType:
    """Simple rule-based classification"""
    description_lower = description.lower()

    if any(word in description_lower for word in ['design', 'drawing', 'specification']):
        return ChangeOrderType.DESIGN_CHANGE
    elif any(word in description_lower for word in ['owner', 'client', 'request']):
        return ChangeOrderType.OWNER_REQUEST
    elif any(word in description_lower for word in ['site', 'field', 'condition', 'unforeseen']):
        return ChangeOrderType.FIELD_CONDITION
    elif any(word in description_lower for word in ['code', 'regulation', 'compliance']):
        return ChangeOrderType.CODE_COMPLIANCE
    elif any(word in description_lower for word in ['value', 'alternative', 'savings']):
        return ChangeOrderType.VALUE_ENGINEERING
    elif any(word in description_lower for word in ['error', 'omission', 'mistake']):
        return ChangeOrderType.ERROR_OMISSION
    else:
        return ChangeOrderType.SCOPE_CHANGE

# Example
co = ChangeOrder(
    co_number="CO-001",
    title="Additional structural reinforcement",
    description="Site conditions revealed weaker soil requiring additional foundation reinforcement",
    co_type=classify_change_order("Site conditions revealed weaker soil"),
    status=ChangeOrderStatus.SUBMITTED,
    submitted_date=date.today(),
    requested_by="Site Engineer",
    cost_impact=50000,
    schedule_impact_days=5
)
print(f"CO Type: {co.co_type.value}")
```

## Comprehensive Change Order System

### Change Order Management

```python
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Dict, Optional, Tuple
from enum import Enum
import pandas as pd
import numpy as np

class ImpactSeverity(Enum):
    MINOR = "minor"  # < 1% cost, < 1 week schedule
    MODERATE = "moderate"  # 1-5% cost, 1-4 weeks schedule
    MAJOR = "major"  # 5-10% cost, 1-3 months schedule
    CRITICAL = "critical"  # > 10% cost, > 3 months schedule

@dataclass
class CostBreakdown:
    labor: float = 0
    materials: float = 0
    equipment: float = 0
    subcontractor: float = 0
    overhead: float = 0
    profit: float = 0

    @property
    def total(self) -> float:
        return self.labor + self.materials + self.equipment + self.subcontractor + self.overhead + self.profit

@dataclass
class ScheduleImpact:
    direct_days: int
    ripple_days: int
    critical_path_affected: bool
    affected_activities: List[str] = field(default_factory=list)

    @property
    def total_days(self) -> int:
        return self.direct_days + self.ripple_days

@dataclass
class ChangeOrderDetail:
    co_id: str
    co_number: str
    title: str
    description: str
    justification: str

    # Classification
    co_type: ChangeOrderType
    initiated_by: str  # owner, contractor, designer, etc.
    responsibility: str  # who pays

    # Status
    status: ChangeOrderStatus
    submitted_date: date
    approved_date: Optional[date] = None
    implemented_date: Optional[date] = None

    # Impact
    cost_breakdown: CostBreakdown = field(default_factory=CostBreakdown)
    schedule_impact: ScheduleImpact = None
    severity: ImpactSeverity = ImpactSeverity.MINOR

    # Affected scope
    affected_elements: List[str] = field(default_factory=list)
    affected_drawings: List[str] = field(default_factory=list)
    affected_specs: List[str] = field(default_factory=list)

    # Supporting documents
    attachments: List[str] = field(default_factory=list)
    related_rfis: List[str] = field(default_factory=list)
    related_cos: List[str] = field(default_factory=list)

    # Approval
    approvals: List[Dict] = field(default_factory=list)
    comments: List[Dict] = field(default_factory=list)

class ChangeOrderManager:
    """Manage project change orders"""

    def __init__(self, project_id: str, contract_value: float):
        self.project_id = project_id
        self.contract_value = contract_value
        self.change_orders: Dict[str, ChangeOrderDetail] = {}
        self.co_counter = 0

    def create_change_order(self, title: str, description: str,
                           co_type: ChangeOrderType,
                           initiated_by: str) -> ChangeOrderDetail:
        """Create new change order"""
        self.co_counter += 1
        co_id = f"CO-{self.project_id}-{self.co_counter:04d}"

        co = ChangeOrderDetail(
            co_id=co_id,
            co_number=f"CO-{self.co_counter:04d}",
            title=title,
            description=description,
            justification="",
            co_type=co_type,
            initiated_by=initiated_by,
            responsibility="TBD",
            status=ChangeOrderStatus.DRAFT,
            submitted_date=date.today()
        )

        self.change_orders[co_id] = co
        return co

    def update_cost(self, co_id: str, cost_breakdown: CostBreakdown):
        """Update change order cost"""
        co = self.change_orders.get(co_id)
        if co:
            co.cost_breakdown = cost_breakdown
            co.severity = self._calculate_severity(co)

    def update_schedule_impact(self, co_id: str, impact: ScheduleImpact):
        """Update schedule impact"""
        co = self.change_orders.get(co_id)
        if co:
            co.schedule_impact = impact
            co.severity = self._calculate_severity(co)

    def _calculate_severity(self, co: ChangeOrderDetail) -> ImpactSeverity:
        """Calculate change order severity"""
        cost_pct = co.cost_breakdown.total / self.contract_value * 100
        schedule_days = co.schedule_impact.total_days if co.schedule_impact else 0

        if cost_pct > 10 or schedule_days > 90:
            return ImpactSeverity.CRITICAL
        elif cost_pct > 5 or schedule_days > 30:
            return ImpactSeverity.MAJOR
        elif cost_pct > 1 or schedule_days > 7:
            return ImpactSeverity.MODERATE
        else:
            return ImpactSeverity.MINOR

    def submit_for_approval(self, co_id: str):
        """Submit change order for approval"""
        co = self.change_orders.get(co_id)
        if co and co.status == ChangeOrderStatus.DRAFT:
            co.status = ChangeOrderStatus.SUBMITTED
            co.submitted_date = date.today()

    def approve(self, co_id: str, approver: str, comments: str = ""):
        """Approve change order"""
        co = self.change_orders.get(co_id)
        if co:
            co.approvals.append({
                'approver': approver,
                'action': 'approved',
                'date': date.today().isoformat(),
                'comments': comments
            })
            co.status = ChangeOrderStatus.APPROVED
            co.approved_date = date.today()

    def get_summary(self) -> Dict:
        """Get change order summary"""
        if not self.change_orders:
            return {'message': 'No change orders'}

        total_cost = sum(co.cost_breakdown.total for co in self.change_orders.values())
        total_schedule = sum(
            co.schedule_impact.total_days if co.schedule_impact else 0
            for co in self.change_orders.values()
        )

        by_type = {}
        by_status = {}
        by_severity = {}

        for co in self.change_orders.values():
            t = co.co_type.value
            by_type[t] = by_type.get(t, 0) + co.cost_breakdown.total

            s = co.status.value
            by_status[s] = by_status.get(s, 0) + 1

            sev = co.severity.value
            by_severity[sev] = by_severity.get(sev, 0) + 1

        return {
            'total_change_orders': len(self.change_orders),
            'total_cost_impact': total_cost,
            'cost_impact_pct': total_cost / self.contract_value * 100,
            'total_schedule_impact_days': total_schedule,
            'by_type': by_type,
            'by_status': by_status,
            'by_severity': by_severity
        }
```

### ML Classification and Prediction

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
import joblib

class ChangeOrderPredictor:
    """ML-based change order classification and cost prediction"""

    def __init__(self):
        self.type_classifier = None
        self.cost_predictor = None
        self.schedule_predictor = None
        self.vectorizer = TfidfVectorizer(max_features=500, ngram_range=(1, 2))
        self.type_encoder = LabelEncoder()
        self.is_trained = False

    def train(self, historical_data: pd.DataFrame):
        """Train models on historical change order data

        Expected columns:
        - description: text description
        - co_type: change order type
        - cost_impact: cost in dollars
        - schedule_impact: days of delay
        - contract_value: original contract value
        - project_phase: phase when CO was raised
        - affected_elements_count: number of affected elements
        """
        # Prepare text features
        text_features = self.vectorizer.fit_transform(historical_data['description'])

        # Prepare numeric features
        numeric_features = historical_data[[
            'contract_value', 'affected_elements_count'
        ]].values

        # Combine features
        X = np.hstack([text_features.toarray(), numeric_features])

        # Train type classifier
        y_type = self.type_encoder.fit_transform(historical_data['co_type'])
        X_train, X_test, y_train, y_test = train_test_split(X, y_type, test_size=0.2)

        self.type_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.type_classifier.fit(X_train, y_train)

        type_accuracy = self.type_classifier.score(X_test, y_test)

        # Train cost predictor
        y_cost = historical_data['cost_impact'].values
        self.cost_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.cost_predictor.fit(X, y_cost)

        # Train schedule predictor
        y_schedule = historical_data['schedule_impact'].values
        self.schedule_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.schedule_predictor.fit(X, y_schedule)

        self.is_trained = True

        return {
            'type_classifier_accuracy': type_accuracy,
            'models_trained': True
        }

    def predict(self, description: str, contract_value: float,
               affected_elements_count: int = 1) -> Dict:
        """Predict change order type and impacts"""
        if not self.is_trained:
            return {'error': 'Models not trained'}

        # Prepare features
        text_features = self.vectorizer.transform([description])
        numeric_features = np.array([[contract_value, affected_elements_count]])
        X = np.hstack([text_features.toarray(), numeric_features])

        # Predict type
        type_probs = self.type_classifier.predict_proba(X)[0]
        type_idx = np.argmax(type_probs)
        predicted_type = self.type_encoder.inverse_transform([type_idx])[0]

        # Predict cost
        predicted_cost = self.cost_predictor.predict(X)[0]

        # Predict schedule
        predicted_schedule = self.schedule_predictor.predict(X)[0]

        return {
            'predicted_type': predicted_type,
            'type_confidence': float(type_probs[type_idx]),
            'type_probabilities': {
                self.type_encoder.inverse_transform([i])[0]: float(p)
                for i, p in enumerate(type_probs)
            },
            'predicted_cost': float(max(0, predicted_cost)),
            'predicted_schedule_days': int(max(0, predicted_schedule)),
            'cost_as_pct_contract': float(predicted_cost / contract_value * 100)
        }

    def save_models(self, path: str):
        """Save trained models"""
        joblib.dump({
            'type_classifier': self.type_classifier,
            'cost_predictor': self.cost_predictor,
            'schedule_predictor': self.schedule_predictor,
            'vectorizer': self.vectorizer,
            'type_encoder': self.type_encoder
        }, path)

    def load_models(self, path: str):
        """Load trained models"""
        data = joblib.load(path)
        self.type_classifier = data['type_classifier']
        self.cost_predictor = data['cost_predictor']
        self.schedule_predictor = data['schedule_predictor']
        self.vectorizer = data['vectorizer']
        self.type_encoder = data['type_encoder']
        self.is_trained = True
```

### Pattern Analysis

```python
from collections import defaultdict
from typing import List, Dict
import pandas as pd

class ChangeOrderAnalyzer:
    """Analyze patterns in change orders"""

    def __init__(self, change_orders: List[ChangeOrderDetail]):
        self.cos = change_orders
        self.df = self._to_dataframe()

    def _to_dataframe(self) -> pd.DataFrame:
        """Convert change orders to DataFrame"""
        data = []
        for co in self.cos:
            data.append({
                'co_id': co.co_id,
                'co_type': co.co_type.value,
                'initiated_by': co.initiated_by,
                'cost': co.cost_breakdown.total,
                'schedule_days': co.schedule_impact.total_days if co.schedule_impact else 0,
                'submitted_date': co.submitted_date,
                'affected_elements': len(co.affected_elements),
                'severity': co.severity.value
            })
        return pd.DataFrame(data)

    def analyze_by_type(self) -> Dict:
        """Analyze change orders by type"""
        if self.df.empty:
            return {}

        analysis = {}
        for co_type in self.df['co_type'].unique():
            type_df = self.df[self.df['co_type'] == co_type]
            analysis[co_type] = {
                'count': len(type_df),
                'total_cost': type_df['cost'].sum(),
                'avg_cost': type_df['cost'].mean(),
                'total_schedule_days': type_df['schedule_days'].sum(),
                'avg_schedule_days': type_df['schedule_days'].mean()
            }

        return analysis

    def analyze_trends(self) -> Dict:
        """Analyze trends over time"""
        if self.df.empty:
            return {}

        self.df['month'] = pd.to_datetime(self.df['submitted_date']).dt.to_period('M')

        monthly = self.df.groupby('month').agg({
            'co_id': 'count',
            'cost': 'sum',
            'schedule_days': 'sum'
        }).rename(columns={'co_id': 'count'})

        return {
            'monthly_trend': monthly.to_dict(),
            'peak_month': monthly['count'].idxmax().strftime('%Y-%m'),
            'total_cost_trend': 'increasing' if monthly['cost'].is_monotonic_increasing else
                               'decreasing' if monthly['cost'].is_monotonic_decreasing else 'variable'
        }

    def identify_root_causes(self) -> List[Dict]:
        """Identify common root causes"""
        if self.df.empty:
            return []

        # Analyze by initiator and type combination
        causes = self.df.groupby(['initiated_by', 'co_type']).agg({
            'co_id': 'count',
            'cost': 'sum'
        }).reset_index()

        causes = causes.sort_values('cost', ascending=False)

        return [
            {
                'initiator': row['initiated_by'],
                'type': row['co_type'],
                'frequency': row['co_id'],
                'total_cost': row['cost'],
                'recommendation': self._get_recommendation(row['initiated_by'], row['co_type'])
            }
            for _, row in causes.head(10).iterrows()
        ]

    def _get_recommendation(self, initiator: str, co_type: str) -> str:
        """Generate recommendation based on pattern"""
        recommendations = {
            ('designer', 'design_change'): 'Improve design review process and BIM coordination',
            ('designer', 'error_omission'): 'Implement design quality checks and clash detection',
            ('owner', 'owner_request'): 'Define scope more clearly during planning phase',
            ('owner', 'scope_change'): 'Conduct thorough requirements gathering',
            ('contractor', 'field_condition'): 'Enhance site investigation before construction',
            ('contractor', 'value_engineering'): 'Include VE sessions earlier in project'
        }

        return recommendations.get(
            (initiator.lower(), co_type),
            'Review process and implement preventive measures'
        )

    def calculate_risk_score(self) -> float:
        """Calculate overall change order risk score"""
        if self.df.empty:
            return 0

        # Factors:
        # - Frequency of COs
        # - Cost impact severity
        # - Schedule impact severity
        # - Trend direction

        co_rate = len(self.df) / 12  # COs per month (assuming 12 month project)
        avg_cost_impact = self.df['cost'].mean()
        avg_schedule_impact = self.df['schedule_days'].mean()

        # Normalize and weight
        freq_score = min(1, co_rate / 10) * 30  # Up to 30 points
        cost_score = min(1, avg_cost_impact / 50000) * 40  # Up to 40 points
        schedule_score = min(1, avg_schedule_impact / 30) * 30  # Up to 30 points

        return freq_score + cost_score + schedule_score

    def generate_report(self, output_path: str) -> str:
        """Generate comprehensive analysis report"""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary = pd.DataFrame([{
                'Total COs': len(self.cos),
                'Total Cost Impact': self.df['cost'].sum(),
                'Total Schedule Impact (days)': self.df['schedule_days'].sum(),
                'Risk Score': self.calculate_risk_score()
            }])
            summary.to_excel(writer, sheet_name='Summary', index=False)

            # By type
            pd.DataFrame(self.analyze_by_type()).T.to_excel(
                writer, sheet_name='By_Type'
            )

            # Root causes
            pd.DataFrame(self.identify_root_causes()).to_excel(
                writer, sheet_name='Root_Causes', index=False
            )

            # All COs
            self.df.to_excel(writer, sheet_name='All_COs', index=False)

        return output_path
```

## Quick Reference

| CO Type | Typical Cause | Prevention Strategy |
|---------|--------------|---------------------|
| Design Change | Incomplete design | BIM coordination, design reviews |
| Owner Request | Changing requirements | Clear scope definition |
| Field Condition | Unforeseen site issues | Thorough site investigation |
| Code Compliance | Regulation changes | Early code review |
| Value Engineering | Cost savings opportunity | VE workshops |
| Error/Omission | Design mistakes | QA/QC processes |

## Resources

- **AIA A201**: General Conditions of the Contract
- **AGC ConsensusDocs**: Change order management
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `document-classification-nlp` for CO document processing
- See `risk-assessment-ml` for project risk analysis
- See `cost-prediction` for cost estimation
