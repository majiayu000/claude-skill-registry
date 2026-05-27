---
name: bid-analysis-comparator
description: "Compare and analyze contractor bids. Score proposals, identify scope gaps, and recommend selections."
---

# Bid Analysis Comparator

## Business Case

Bid evaluation requires systematic comparison across multiple criteria. This skill provides structured bid analysis and scoring.

## Technical Implementation

```python
import pandas as pd
from datetime import date
from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


class BidStatus(Enum):
    RECEIVED = "received"
    UNDER_REVIEW = "under_review"
    SHORTLISTED = "shortlisted"
    AWARDED = "awarded"
    REJECTED = "rejected"


@dataclass
class EvaluationCriteria:
    name: str
    weight: float  # 0-1
    max_score: int = 10


@dataclass
class BidScore:
    criteria: str
    score: int
    notes: str = ""


@dataclass
class Bid:
    bid_id: str
    bidder_name: str
    bid_package: str
    submitted_date: date
    base_bid: float
    alternates: Dict[str, float]
    status: BidStatus
    scores: List[BidScore] = field(default_factory=list)
    qualifications: List[str] = field(default_factory=list)
    exclusions: List[str] = field(default_factory=list)

    @property
    def total_weighted_score(self) -> float:
        return sum(s.score for s in self.scores)


class BidAnalysisComparator:
    def __init__(self, project_name: str, bid_package: str):
        self.project_name = project_name
        self.bid_package = bid_package
        self.bids: Dict[str, Bid] = {}
        self.criteria: List[EvaluationCriteria] = []
        self._setup_default_criteria()
        self._counter = 0

    def _setup_default_criteria(self):
        self.criteria = [
            EvaluationCriteria("Price", 0.35),
            EvaluationCriteria("Experience", 0.20),
            EvaluationCriteria("Schedule", 0.15),
            EvaluationCriteria("Safety Record", 0.10),
            EvaluationCriteria("References", 0.10),
            EvaluationCriteria("Capacity", 0.10)
        ]

    def add_bid(self, bidder_name: str, base_bid: float,
               submitted_date: date = None,
               alternates: Dict[str, float] = None) -> Bid:
        self._counter += 1
        bid_id = f"BID-{self._counter:03d}"

        bid = Bid(
            bid_id=bid_id,
            bidder_name=bidder_name,
            bid_package=self.bid_package,
            submitted_date=submitted_date or date.today(),
            base_bid=base_bid,
            alternates=alternates or {},
            status=BidStatus.RECEIVED
        )
        self.bids[bid_id] = bid
        return bid

    def score_bid(self, bid_id: str, scores: Dict[str, int]):
        """Score bid on criteria. scores = {'Price': 8, 'Experience': 7, ...}"""
        if bid_id not in self.bids:
            return
        bid = self.bids[bid_id]
        bid.scores = []
        for criteria, score in scores.items():
            bid.scores.append(BidScore(criteria, score))
        bid.status = BidStatus.UNDER_REVIEW

    def calculate_weighted_scores(self) -> pd.DataFrame:
        """Calculate weighted scores for all bids."""
        results = []
        criteria_weights = {c.name: c.weight for c in self.criteria}

        for bid in self.bids.values():
            row = {
                'Bidder': bid.bidder_name,
                'Base Bid': bid.base_bid,
                'Status': bid.status.value
            }
            total = 0
            for score in bid.scores:
                weight = criteria_weights.get(score.criteria, 0)
                weighted = score.score * weight * 10
                row[score.criteria] = score.score
                row[f'{score.criteria} (W)'] = round(weighted, 1)
                total += weighted
            row['Total Score'] = round(total, 1)
            results.append(row)

        return pd.DataFrame(results).sort_values('Total Score', ascending=False)

    def get_recommendation(self) -> Dict[str, Any]:
        """Get bid recommendation."""
        df = self.calculate_weighted_scores()
        if df.empty:
            return {'recommendation': 'No bids to evaluate'}

        top = df.iloc[0]
        lowest = df.sort_values('Base Bid').iloc[0]

        return {
            'highest_score': {
                'bidder': top['Bidder'],
                'score': top['Total Score'],
                'bid': top['Base Bid']
            },
            'lowest_price': {
                'bidder': lowest['Bidder'],
                'bid': lowest['Base Bid']
            },
            'total_bids': len(self.bids),
            'recommendation': top['Bidder']
        }

    def export_analysis(self, output_path: str):
        df = self.calculate_weighted_scores()
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Comparison', index=False)

            # Bid details
            details = [{
                'Bidder': b.bidder_name,
                'Bid': b.base_bid,
                'Exclusions': '; '.join(b.exclusions),
                'Qualifications': '; '.join(b.qualifications)
            } for b in self.bids.values()]
            pd.DataFrame(details).to_excel(writer, sheet_name='Details', index=False)
```

## Quick Start

```python
comparator = BidAnalysisComparator("Office Tower", "Electrical")

bid1 = comparator.add_bid("ABC Electric", 850000)
bid2 = comparator.add_bid("XYZ Electric", 920000)

comparator.score_bid(bid1.bid_id, {'Price': 9, 'Experience': 7, 'Schedule': 8,
                                   'Safety Record': 8, 'References': 7, 'Capacity': 8})
comparator.score_bid(bid2.bid_id, {'Price': 7, 'Experience': 9, 'Schedule': 7,
                                   'Safety Record': 9, 'References': 9, 'Capacity': 9})

recommendation = comparator.get_recommendation()
print(f"Recommended: {recommendation['recommendation']}")
```

## Resources
- **DDC Book**: Chapter 3.4 - Procurement
