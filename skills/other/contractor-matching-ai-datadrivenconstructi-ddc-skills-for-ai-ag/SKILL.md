---
slug: "contractor-matching-ai"
display_name: "Contractor Matching AI"
description: "AI-powered contractor matching and selection for construction projects. Analyze contractor capabilities, past performance, certifications, and project requirements to recommend optimal matches."
---

# AI Contractor Matching

## Overview

This skill implements AI-powered contractor matching for construction projects. Analyze project requirements against contractor capabilities, track historical performance, and generate recommendations based on multiple criteria.

**Matching Criteria:**
- Technical capabilities & expertise
- Past performance scores
- Certifications & licenses
- Geographic availability
- Capacity & current workload
- Pricing competitiveness
- Safety records

## Quick Start

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import date
import numpy as np

@dataclass
class Contractor:
    contractor_id: str
    name: str
    specializations: List[str]
    certifications: List[str]
    performance_score: float  # 0-100
    safety_score: float  # 0-100
    regions: List[str]
    capacity_available: float  # 0-100 percentage
    avg_bid_variance: float  # % above/below average

@dataclass
class ProjectRequirement:
    project_id: str
    work_types: List[str]
    required_certs: List[str]
    region: str
    estimated_value: float
    priority: str  # cost, quality, speed, safety

def match_contractors(project: ProjectRequirement,
                     contractors: List[Contractor],
                     top_n: int = 5) -> List[Dict]:
    """Simple contractor matching"""
    scores = []

    for c in contractors:
        # Check basic eligibility
        if project.region not in c.regions:
            continue

        work_match = len(set(project.work_types) & set(c.specializations))
        if work_match == 0:
            continue

        cert_match = len(set(project.required_certs) & set(c.certifications))
        if cert_match < len(project.required_certs):
            continue

        # Calculate score based on priority
        if project.priority == 'quality':
            score = c.performance_score * 0.6 + (100 - abs(c.avg_bid_variance)) * 0.2 + c.capacity_available * 0.2
        elif project.priority == 'cost':
            score = (100 - c.avg_bid_variance) * 0.5 + c.performance_score * 0.3 + c.capacity_available * 0.2
        elif project.priority == 'safety':
            score = c.safety_score * 0.6 + c.performance_score * 0.3 + c.capacity_available * 0.1
        else:  # speed
            score = c.capacity_available * 0.5 + c.performance_score * 0.3 + c.safety_score * 0.2

        scores.append({
            'contractor': c,
            'score': score,
            'work_match': work_match / len(project.work_types),
            'cert_match': cert_match / len(project.required_certs) if project.required_certs else 1.0
        })

    # Sort and return top matches
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores[:top_n]

# Example
contractors = [
    Contractor("C001", "ABC Builders", ["concrete", "structural"], ["ISO9001", "OHSAS18001"],
              85, 90, ["Moscow", "SPB"], 60, -5),
    Contractor("C002", "XYZ Construction", ["concrete", "finishing"], ["ISO9001"],
              78, 85, ["Moscow"], 80, 10),
]

project = ProjectRequirement("P001", ["concrete"], ["ISO9001"], "Moscow", 1000000, "quality")
matches = match_contractors(project, contractors)
for m in matches:
    print(f"{m['contractor'].name}: Score {m['score']:.1f}")
```

## Comprehensive Matching System

### Contractor Profile Management

```python
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from datetime import date, datetime
from enum import Enum
import numpy as np
from sklearn.preprocessing import MinMaxScaler

class ContractorSize(Enum):
    MICRO = "micro"  # < 10 employees
    SMALL = "small"  # 10-50 employees
    MEDIUM = "medium"  # 50-250 employees
    LARGE = "large"  # > 250 employees

class WorkCategory(Enum):
    GENERAL = "general_contractor"
    CONCRETE = "concrete"
    STRUCTURAL_STEEL = "structural_steel"
    MEP = "mep"
    ELECTRICAL = "electrical"
    PLUMBING = "plumbing"
    HVAC = "hvac"
    FINISHING = "finishing"
    FACADE = "facade"
    ROOFING = "roofing"
    EXCAVATION = "excavation"
    FOUNDATION = "foundation"
    LANDSCAPING = "landscaping"
    DEMOLITION = "demolition"

@dataclass
class ProjectReference:
    project_name: str
    client: str
    value: float
    completion_date: date
    work_type: str
    performance_rating: float  # 1-5
    on_time: bool
    on_budget: bool
    client_reference_available: bool

@dataclass
class ContractorProfile:
    contractor_id: str
    company_name: str
    legal_name: str
    registration_number: str
    size: ContractorSize
    founded_year: int
    employees_count: int

    # Capabilities
    specializations: List[WorkCategory]
    equipment_owned: List[str]
    max_project_value: float
    min_project_value: float

    # Certifications
    certifications: List[Dict]  # {name, issuer, valid_until}
    licenses: List[Dict]  # {type, number, region, valid_until}

    # Performance
    completed_projects: int
    active_projects: int
    references: List[ProjectReference] = field(default_factory=list)

    # Safety
    safety_certifications: List[str] = field(default_factory=list)
    incident_rate: float = 0.0  # incidents per 1000 work hours
    fatality_count: int = 0
    lost_time_incidents: int = 0

    # Financial
    annual_revenue: float = 0
    credit_rating: str = ""
    insurance_coverage: float = 0
    bonding_capacity: float = 0

    # Geographic
    headquarters_region: str = ""
    operating_regions: List[str] = field(default_factory=list)
    willing_to_travel: bool = False

    # Current status
    current_workload_pct: float = 0  # 0-100
    earliest_availability: Optional[date] = None

    # Pricing
    historical_bid_data: List[Dict] = field(default_factory=list)

    def calculate_performance_score(self) -> float:
        """Calculate overall performance score"""
        if not self.references:
            return 50.0  # Default for new contractors

        ratings = [r.performance_rating for r in self.references]
        on_time_rate = sum(1 for r in self.references if r.on_time) / len(self.references)
        on_budget_rate = sum(1 for r in self.references if r.on_budget) / len(self.references)

        # Weighted average
        avg_rating = sum(ratings) / len(ratings) / 5 * 100  # Normalize to 0-100
        on_time_score = on_time_rate * 100
        on_budget_score = on_budget_rate * 100

        return avg_rating * 0.5 + on_time_score * 0.3 + on_budget_score * 0.2

    def calculate_safety_score(self) -> float:
        """Calculate safety score"""
        base_score = 100

        # Deductions
        if self.incident_rate > 0:
            base_score -= min(30, self.incident_rate * 10)
        if self.fatality_count > 0:
            base_score -= 50  # Major deduction for fatalities
        if self.lost_time_incidents > 0:
            base_score -= min(20, self.lost_time_incidents * 2)

        # Bonuses for certifications
        if 'ISO45001' in self.safety_certifications or 'OHSAS18001' in self.safety_certifications:
            base_score += 10

        return max(0, min(100, base_score))

    def get_capacity_score(self) -> float:
        """Calculate available capacity score"""
        return 100 - self.current_workload_pct
```

### AI Matching Engine

```python
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

@dataclass
class ProjectRequirements:
    project_id: str
    project_name: str
    work_categories: List[WorkCategory]
    required_certifications: List[str]
    required_licenses: List[str]
    region: str
    estimated_value: float
    start_date: date
    duration_months: int
    priority_weights: Dict[str, float] = field(default_factory=dict)
    special_requirements: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.priority_weights:
            self.priority_weights = {
                'performance': 0.25,
                'safety': 0.20,
                'price': 0.20,
                'capacity': 0.15,
                'experience': 0.10,
                'financial': 0.10
            }

class ContractorMatchingEngine:
    """AI-powered contractor matching system"""

    def __init__(self):
        self.contractors: Dict[str, ContractorProfile] = {}
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.scaler = MinMaxScaler()

    def register_contractor(self, profile: ContractorProfile):
        """Register contractor in the system"""
        self.contractors[profile.contractor_id] = profile

    def find_matches(self, requirements: ProjectRequirements,
                    top_n: int = 10) -> List[Dict]:
        """Find best matching contractors for project"""
        eligible = self._filter_eligible(requirements)

        if not eligible:
            return []

        scored = []
        for contractor in eligible:
            score, breakdown = self._calculate_match_score(contractor, requirements)
            scored.append({
                'contractor_id': contractor.contractor_id,
                'company_name': contractor.company_name,
                'total_score': score,
                'score_breakdown': breakdown,
                'profile': contractor
            })

        # Sort by score
        scored.sort(key=lambda x: x['total_score'], reverse=True)

        return scored[:top_n]

    def _filter_eligible(self, req: ProjectRequirements) -> List[ContractorProfile]:
        """Filter contractors by basic eligibility"""
        eligible = []

        for contractor in self.contractors.values():
            # Check region
            if req.region not in contractor.operating_regions:
                if not contractor.willing_to_travel:
                    continue

            # Check work categories
            contractor_cats = set(contractor.specializations)
            required_cats = set(req.work_categories)
            if not required_cats.intersection(contractor_cats):
                continue

            # Check project size
            if req.estimated_value > contractor.max_project_value:
                continue
            if req.estimated_value < contractor.min_project_value:
                continue

            # Check certifications
            contractor_certs = set(c['name'] for c in contractor.certifications
                                  if c.get('valid_until', date.max) >= date.today())
            if not set(req.required_certifications).issubset(contractor_certs):
                continue

            # Check licenses
            contractor_licenses = set(l['type'] for l in contractor.licenses
                                     if l.get('valid_until', date.max) >= date.today())
            if not set(req.required_licenses).issubset(contractor_licenses):
                continue

            # Check capacity
            if contractor.current_workload_pct >= 95:  # Too busy
                continue

            # Check availability
            if contractor.earliest_availability and contractor.earliest_availability > req.start_date:
                continue

            eligible.append(contractor)

        return eligible

    def _calculate_match_score(self, contractor: ContractorProfile,
                              req: ProjectRequirements) -> Tuple[float, Dict]:
        """Calculate weighted match score"""
        weights = req.priority_weights
        breakdown = {}

        # Performance score
        breakdown['performance'] = contractor.calculate_performance_score()

        # Safety score
        breakdown['safety'] = contractor.calculate_safety_score()

        # Price competitiveness (from historical data)
        breakdown['price'] = self._calculate_price_score(contractor, req)

        # Capacity score
        breakdown['capacity'] = contractor.get_capacity_score()

        # Experience score (similar projects)
        breakdown['experience'] = self._calculate_experience_score(contractor, req)

        # Financial stability score
        breakdown['financial'] = self._calculate_financial_score(contractor, req)

        # Calculate weighted total
        total = sum(
            breakdown[key] * weights.get(key, 0)
            for key in breakdown
        )

        return total, breakdown

    def _calculate_price_score(self, contractor: ContractorProfile,
                              req: ProjectRequirements) -> float:
        """Calculate price competitiveness score"""
        if not contractor.historical_bid_data:
            return 50.0  # Neutral score

        # Find similar projects
        similar_bids = [
            bid for bid in contractor.historical_bid_data
            if bid.get('project_value', 0) * 0.5 <= req.estimated_value <= bid.get('project_value', 0) * 2
        ]

        if not similar_bids:
            return 50.0

        # Calculate average variance from winning bids
        variances = [bid.get('variance_pct', 0) for bid in similar_bids]
        avg_variance = sum(variances) / len(variances)

        # Lower variance = higher score
        # -10% to +10% is normal range
        if avg_variance <= -10:
            return 90  # Very competitive
        elif avg_variance <= 0:
            return 80 - avg_variance  # Competitive
        elif avg_variance <= 10:
            return 70 - avg_variance  # Average
        else:
            return max(30, 60 - avg_variance)  # Expensive

    def _calculate_experience_score(self, contractor: ContractorProfile,
                                   req: ProjectRequirements) -> float:
        """Calculate relevant experience score"""
        if not contractor.references:
            return 30.0  # Low score for no experience

        relevant_projects = []
        for ref in contractor.references:
            # Check work type match
            try:
                work_cat = WorkCategory(ref.work_type)
                if work_cat in req.work_categories:
                    relevant_projects.append(ref)
            except ValueError:
                continue

        if not relevant_projects:
            return 40.0

        # Score based on number and recency of relevant projects
        recent_relevant = [
            p for p in relevant_projects
            if (date.today() - p.completion_date).days <= 365 * 3  # Last 3 years
        ]

        count_score = min(50, len(relevant_projects) * 10)
        recency_score = min(30, len(recent_relevant) * 15)

        # Value similarity
        values = [p.value for p in relevant_projects]
        avg_value = sum(values) / len(values)
        value_ratio = min(req.estimated_value, avg_value) / max(req.estimated_value, avg_value)
        value_score = value_ratio * 20

        return count_score + recency_score + value_score

    def _calculate_financial_score(self, contractor: ContractorProfile,
                                  req: ProjectRequirements) -> float:
        """Calculate financial stability score"""
        score = 50.0  # Base score

        # Check bonding capacity
        if contractor.bonding_capacity >= req.estimated_value:
            score += 20
        elif contractor.bonding_capacity >= req.estimated_value * 0.5:
            score += 10

        # Check insurance
        if contractor.insurance_coverage >= req.estimated_value:
            score += 15
        elif contractor.insurance_coverage >= req.estimated_value * 0.5:
            score += 7

        # Credit rating
        credit_scores = {'AAA': 15, 'AA': 12, 'A': 10, 'BBB': 5, 'BB': 0, 'B': -10}
        score += credit_scores.get(contractor.credit_rating, 0)

        return min(100, max(0, score))

    def compare_contractors(self, contractor_ids: List[str],
                           req: ProjectRequirements) -> pd.DataFrame:
        """Compare specific contractors"""
        data = []

        for cid in contractor_ids:
            contractor = self.contractors.get(cid)
            if not contractor:
                continue

            score, breakdown = self._calculate_match_score(contractor, req)

            row = {
                'Contractor': contractor.company_name,
                'Total Score': f"{score:.1f}",
                'Performance': f"{breakdown['performance']:.1f}",
                'Safety': f"{breakdown['safety']:.1f}",
                'Price': f"{breakdown['price']:.1f}",
                'Capacity': f"{breakdown['capacity']:.1f}",
                'Experience': f"{breakdown['experience']:.1f}",
                'Financial': f"{breakdown['financial']:.1f}",
                'Active Projects': contractor.active_projects,
                'Workload': f"{contractor.current_workload_pct:.0f}%"
            }
            data.append(row)

        return pd.DataFrame(data)
```

### Bid Analysis and Prediction

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import numpy as np

class BidPredictor:
    """Predict contractor bid prices"""

    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False

    def train(self, historical_bids: pd.DataFrame):
        """Train bid prediction model

        Expected columns:
        - contractor_size, work_type, region, project_value
        - contractor_performance, contractor_workload
        - winning_bid, contractor_bid
        """
        features = ['project_value', 'contractor_performance',
                   'contractor_workload', 'duration_months']

        # One-hot encode categorical
        df = pd.get_dummies(historical_bids,
                           columns=['contractor_size', 'work_type', 'region'])

        # Features that exist
        X_cols = [c for c in df.columns if c not in ['winning_bid', 'contractor_bid']]
        X = df[X_cols]
        y = df['contractor_bid']

        self.feature_columns = X_cols
        self.model.fit(X, y)
        self.is_trained = True

    def predict_bid(self, contractor: ContractorProfile,
                   project: ProjectRequirements) -> Dict:
        """Predict expected bid from contractor"""
        if not self.is_trained:
            # Simple estimation if not trained
            base = project.estimated_value
            variance = np.random.uniform(-0.1, 0.15)
            return {
                'predicted_bid': base * (1 + variance),
                'confidence': 'low',
                'variance_range': (-15, 20)
            }

        # Build feature vector
        features = {
            'project_value': project.estimated_value,
            'contractor_performance': contractor.calculate_performance_score(),
            'contractor_workload': contractor.current_workload_pct,
            'duration_months': project.duration_months,
            f'contractor_size_{contractor.size.value}': 1,
            f'region_{project.region}': 1
        }

        # Add work type
        for cat in project.work_categories:
            features[f'work_type_{cat.value}'] = 1

        # Create feature vector
        X = pd.DataFrame([features]).reindex(columns=self.feature_columns, fill_value=0)

        prediction = self.model.predict(X)[0]

        # Calculate confidence based on similar historical data
        return {
            'predicted_bid': prediction,
            'confidence': 'medium',
            'variance_range': (-10, 15),
            'estimated_value': project.estimated_value,
            'predicted_variance_pct': (prediction - project.estimated_value) / project.estimated_value * 100
        }


class BidEvaluator:
    """Evaluate and score contractor bids"""

    def __init__(self, matching_engine: ContractorMatchingEngine):
        self.engine = matching_engine
        self.predictor = BidPredictor()

    def evaluate_bids(self, project: ProjectRequirements,
                     bids: List[Dict]) -> pd.DataFrame:
        """Evaluate received bids

        bids: List of {contractor_id, bid_amount, bid_breakdown, proposal}
        """
        results = []

        for bid in bids:
            contractor = self.engine.contractors.get(bid['contractor_id'])
            if not contractor:
                continue

            # Get match score
            match_score, breakdown = self.engine._calculate_match_score(
                contractor, project
            )

            # Price score (compared to other bids)
            avg_bid = sum(b['bid_amount'] for b in bids) / len(bids)
            price_deviation = (bid['bid_amount'] - avg_bid) / avg_bid * 100

            if price_deviation <= -10:
                price_score = 95  # Very competitive
            elif price_deviation <= 0:
                price_score = 85 - price_deviation
            elif price_deviation <= 10:
                price_score = 75 - price_deviation
            else:
                price_score = max(40, 65 - price_deviation)

            # Overall evaluation score (weighted)
            eval_score = match_score * 0.6 + price_score * 0.4

            results.append({
                'contractor_id': bid['contractor_id'],
                'company_name': contractor.company_name,
                'bid_amount': bid['bid_amount'],
                'price_vs_avg': f"{price_deviation:+.1f}%",
                'match_score': match_score,
                'price_score': price_score,
                'evaluation_score': eval_score,
                'performance': breakdown['performance'],
                'safety': breakdown['safety'],
                'recommendation': self._get_recommendation(eval_score, price_deviation)
            })

        df = pd.DataFrame(results)
        df = df.sort_values('evaluation_score', ascending=False)

        return df

    def _get_recommendation(self, eval_score: float, price_dev: float) -> str:
        """Generate recommendation"""
        if eval_score >= 80 and price_dev <= 5:
            return "Strongly Recommended"
        elif eval_score >= 70:
            return "Recommended"
        elif eval_score >= 60:
            return "Acceptable"
        elif price_dev > 20:
            return "Price Concerns"
        else:
            return "Review Required"
```

### Contractor Recommendation Report

```python
def generate_recommendation_report(engine: ContractorMatchingEngine,
                                   project: ProjectRequirements,
                                   output_path: str) -> str:
    """Generate contractor recommendation report"""
    matches = engine.find_matches(project, top_n=10)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary
        summary_data = [{
            'Project': project.project_name,
            'Estimated Value': project.estimated_value,
            'Work Categories': ', '.join(c.value for c in project.work_categories),
            'Region': project.region,
            'Start Date': project.start_date.isoformat(),
            'Duration': f"{project.duration_months} months",
            'Contractors Found': len(matches)
        }]
        pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)

        # Rankings
        ranking_data = []
        for i, match in enumerate(matches, 1):
            ranking_data.append({
                'Rank': i,
                'Contractor': match['company_name'],
                'Total Score': f"{match['total_score']:.1f}",
                'Performance': f"{match['score_breakdown']['performance']:.1f}",
                'Safety': f"{match['score_breakdown']['safety']:.1f}",
                'Price': f"{match['score_breakdown']['price']:.1f}",
                'Capacity': f"{match['score_breakdown']['capacity']:.1f}",
                'Experience': f"{match['score_breakdown']['experience']:.1f}",
                'Financial': f"{match['score_breakdown']['financial']:.1f}"
            })
        pd.DataFrame(ranking_data).to_excel(writer, sheet_name='Rankings', index=False)

        # Detailed profiles for top 5
        for i, match in enumerate(matches[:5], 1):
            profile = match['profile']
            profile_data = [{
                'Field': 'Company Name', 'Value': profile.company_name
            }, {
                'Field': 'Size', 'Value': profile.size.value
            }, {
                'Field': 'Employees', 'Value': profile.employees_count
            }, {
                'Field': 'Completed Projects', 'Value': profile.completed_projects
            }, {
                'Field': 'Active Projects', 'Value': profile.active_projects
            }, {
                'Field': 'Current Workload', 'Value': f"{profile.current_workload_pct}%"
            }, {
                'Field': 'Bonding Capacity', 'Value': f"${profile.bonding_capacity:,.0f}"
            }, {
                'Field': 'Safety Incidents', 'Value': profile.lost_time_incidents
            }]
            pd.DataFrame(profile_data).to_excel(
                writer, sheet_name=f'Contractor_{i}', index=False
            )

    return output_path
```

## Quick Reference

| Criterion | Weight Range | Data Sources |
|-----------|--------------|--------------|
| Performance | 20-30% | Project references, ratings |
| Safety | 15-25% | OSHA records, certifications |
| Price | 15-25% | Historical bids |
| Capacity | 10-20% | Current workload |
| Experience | 10-15% | Similar projects |
| Financial | 10-15% | Credit rating, bonding |

## Resources

- **DDC Website**: https://datadrivenconstruction.io
- **Construction contractor databases**: BuildingConnected, PlanHub

## Next Steps

- See `risk-assessment-ml` for contractor risk analysis
- See `document-classification-nlp` for proposal analysis
- See `open-construction-estimate` for bid validation
