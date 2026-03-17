---
slug: "cwicr-subcontractor"
display_name: "CWICR Subcontractor"
description: "Analyze and compare subcontractor bids against CWICR benchmarks. Evaluate pricing, identify outliers, and support negotiation."
---

# CWICR Subcontractor Analyzer

## Business Case

### Problem Statement
Evaluating subcontractor bids requires:
- Fair price benchmarks
- Bid comparison
- Outlier identification
- Negotiation support

### Solution
Compare subcontractor bids against CWICR cost data to identify fair pricing, outliers, and negotiation opportunities.

### Business Value
- **Fair evaluation** - Objective benchmarks
- **Cost savings** - Identify overpriced bids
- **Risk detection** - Flag unrealistic low bids
- **Negotiation support** - Data-driven discussions

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from statistics import mean, stdev


class BidStatus(Enum):
    """Bid evaluation status."""
    COMPETITIVE = "competitive"
    HIGH = "high"
    LOW = "low"
    OUTLIER_HIGH = "outlier_high"
    OUTLIER_LOW = "outlier_low"


@dataclass
class SubcontractorBid:
    """Subcontractor bid."""
    subcontractor_name: str
    trade: str
    bid_amount: float
    scope_items: List[Dict[str, Any]]
    includes_material: bool
    includes_labor: bool
    includes_equipment: bool
    duration_days: int
    notes: str = ""


@dataclass
class BidEvaluation:
    """Bid evaluation result."""
    subcontractor_name: str
    bid_amount: float
    benchmark_cost: float
    variance: float
    variance_percent: float
    status: BidStatus
    line_item_analysis: List[Dict[str, Any]]
    recommendation: str


class CWICRSubcontractor:
    """Analyze subcontractor bids using CWICR data."""

    OUTLIER_THRESHOLD = 0.30  # 30% from benchmark
    HIGH_THRESHOLD = 0.15    # 15% above benchmark
    LOW_THRESHOLD = -0.10    # 10% below benchmark

    def __init__(self,
                 cwicr_data: pd.DataFrame,
                 overhead_rate: float = 0.12,
                 profit_rate: float = 0.10):
        self.cost_data = cwicr_data
        self.overhead_rate = overhead_rate
        self.profit_rate = profit_rate
        self._index_data()

    def _index_data(self):
        """Index cost data."""
        if 'work_item_code' in self.cost_data.columns:
            self._code_index = self.cost_data.set_index('work_item_code')
        else:
            self._code_index = None

    def calculate_benchmark(self,
                            scope_items: List[Dict[str, Any]],
                            include_overhead: bool = True,
                            include_profit: bool = True) -> Dict[str, Any]:
        """Calculate benchmark cost for scope."""

        labor = 0
        material = 0
        equipment = 0

        line_items = []

        for item in scope_items:
            code = item.get('work_item_code', item.get('code'))
            qty = item.get('quantity', 0)

            if self._code_index is not None and code in self._code_index.index:
                wi = self._code_index.loc[code]
                item_labor = float(wi.get('labor_cost', 0) or 0) * qty
                item_material = float(wi.get('material_cost', 0) or 0) * qty
                item_equipment = float(wi.get('equipment_cost', 0) or 0) * qty

                labor += item_labor
                material += item_material
                equipment += item_equipment

                line_items.append({
                    'code': code,
                    'quantity': qty,
                    'labor': round(item_labor, 2),
                    'material': round(item_material, 2),
                    'equipment': round(item_equipment, 2),
                    'total': round(item_labor + item_material + item_equipment, 2)
                })

        direct_cost = labor + material + equipment

        overhead = direct_cost * self.overhead_rate if include_overhead else 0
        profit = (direct_cost + overhead) * self.profit_rate if include_profit else 0

        return {
            'labor': round(labor, 2),
            'material': round(material, 2),
            'equipment': round(equipment, 2),
            'direct_cost': round(direct_cost, 2),
            'overhead': round(overhead, 2),
            'profit': round(profit, 2),
            'total': round(direct_cost + overhead + profit, 2),
            'line_items': line_items
        }

    def evaluate_bid(self, bid: SubcontractorBid) -> BidEvaluation:
        """Evaluate single subcontractor bid."""

        benchmark = self.calculate_benchmark(bid.scope_items)
        benchmark_cost = benchmark['total']

        variance = bid.bid_amount - benchmark_cost
        variance_pct = (variance / benchmark_cost * 100) if benchmark_cost > 0 else 0

        # Determine status
        if variance_pct > self.OUTLIER_THRESHOLD * 100:
            status = BidStatus.OUTLIER_HIGH
            recommendation = "Bid significantly above benchmark. Request detailed breakdown or reject."
        elif variance_pct < -self.OUTLIER_THRESHOLD * 100:
            status = BidStatus.OUTLIER_LOW
            recommendation = "Bid significantly below benchmark. Verify scope understanding and capacity."
        elif variance_pct > self.HIGH_THRESHOLD * 100:
            status = BidStatus.HIGH
            recommendation = "Bid above benchmark. Consider negotiation or alternative bidders."
        elif variance_pct < self.LOW_THRESHOLD * 100:
            status = BidStatus.LOW
            recommendation = "Bid below benchmark. Verify completeness and quality approach."
        else:
            status = BidStatus.COMPETITIVE
            recommendation = "Bid within acceptable range. Proceed with standard evaluation."

        # Line item analysis
        line_analysis = []
        for i, item in enumerate(bid.scope_items):
            if i < len(benchmark['line_items']):
                bench_item = benchmark['line_items'][i]
                # Assume proportional pricing
                expected = bench_item['total'] / benchmark['direct_cost'] * bid.bid_amount if benchmark['direct_cost'] > 0 else 0
                line_analysis.append({
                    'code': item.get('work_item_code', item.get('code')),
                    'benchmark': bench_item['total'],
                    'expected_in_bid': round(expected, 2)
                })

        return BidEvaluation(
            subcontractor_name=bid.subcontractor_name,
            bid_amount=bid.bid_amount,
            benchmark_cost=benchmark_cost,
            variance=round(variance, 2),
            variance_percent=round(variance_pct, 1),
            status=status,
            line_item_analysis=line_analysis,
            recommendation=recommendation
        )

    def compare_bids(self,
                      bids: List[SubcontractorBid]) -> Dict[str, Any]:
        """Compare multiple bids."""

        if not bids:
            return {}

        evaluations = [self.evaluate_bid(bid) for bid in bids]

        # Statistics
        amounts = [e.bid_amount for e in evaluations]
        avg_bid = mean(amounts)
        std_bid = stdev(amounts) if len(amounts) > 1 else 0

        # Rank by variance from benchmark
        ranked = sorted(evaluations, key=lambda x: abs(x.variance_percent))

        # Find best value
        competitive = [e for e in evaluations if e.status == BidStatus.COMPETITIVE]
        if competitive:
            best_value = min(competitive, key=lambda x: x.bid_amount)
        else:
            best_value = ranked[0]

        # Identify outliers
        outliers = [e for e in evaluations if e.status in [BidStatus.OUTLIER_HIGH, BidStatus.OUTLIER_LOW]]

        return {
            'bid_count': len(bids),
            'average_bid': round(avg_bid, 2),
            'std_deviation': round(std_bid, 2),
            'spread': round(max(amounts) - min(amounts), 2),
            'spread_percent': round((max(amounts) - min(amounts)) / avg_bid * 100, 1) if avg_bid > 0 else 0,
            'benchmark': evaluations[0].benchmark_cost,
            'best_value': {
                'name': best_value.subcontractor_name,
                'amount': best_value.bid_amount,
                'variance_from_benchmark': best_value.variance_percent
            },
            'lowest_bid': {
                'name': min(evaluations, key=lambda x: x.bid_amount).subcontractor_name,
                'amount': min(amounts)
            },
            'outliers': [
                {'name': e.subcontractor_name, 'status': e.status.value, 'variance': e.variance_percent}
                for e in outliers
            ],
            'evaluations': evaluations
        }

    def generate_negotiation_points(self,
                                     evaluation: BidEvaluation) -> List[Dict[str, Any]]:
        """Generate negotiation points based on evaluation."""

        points = []

        if evaluation.status in [BidStatus.HIGH, BidStatus.OUTLIER_HIGH]:
            points.append({
                'topic': 'Overall Price',
                'benchmark': evaluation.benchmark_cost,
                'bid': evaluation.bid_amount,
                'target': round(evaluation.benchmark_cost * 1.05, 2),  # 5% above benchmark
                'potential_savings': round(evaluation.bid_amount - evaluation.benchmark_cost * 1.05, 2)
            })

            # Suggest line item discussions
            for item in evaluation.line_item_analysis:
                points.append({
                    'topic': f"Line Item: {item['code']}",
                    'benchmark': item['benchmark'],
                    'suggestion': 'Request detailed breakdown'
                })

        return points

    def export_bid_comparison(self,
                               comparison: Dict[str, Any],
                               output_path: str) -> str:
        """Export bid comparison to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Number of Bids': comparison['bid_count'],
                'Average Bid': comparison['average_bid'],
                'Spread': comparison['spread'],
                'Spread %': comparison['spread_percent'],
                'Benchmark': comparison['benchmark'],
                'Best Value Bidder': comparison['best_value']['name'],
                'Lowest Bidder': comparison['lowest_bid']['name']
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # All evaluations
            eval_df = pd.DataFrame([
                {
                    'Subcontractor': e.subcontractor_name,
                    'Bid Amount': e.bid_amount,
                    'Benchmark': e.benchmark_cost,
                    'Variance': e.variance,
                    'Variance %': e.variance_percent,
                    'Status': e.status.value,
                    'Recommendation': e.recommendation
                }
                for e in comparison['evaluations']
            ])
            eval_df.to_excel(writer, sheet_name='Evaluations', index=False)

        return output_path
```

## Quick Start

```python
# Load CWICR data
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize analyzer
analyzer = CWICRSubcontractor(cwicr)

# Define scope
scope = [
    {'work_item_code': 'ELEC-001', 'quantity': 100},
    {'work_item_code': 'ELEC-002', 'quantity': 50}
]

# Create bid
bid = SubcontractorBid(
    subcontractor_name="ABC Electric",
    trade="Electrical",
    bid_amount=75000,
    scope_items=scope,
    includes_material=True,
    includes_labor=True,
    includes_equipment=True,
    duration_days=30
)

# Evaluate
evaluation = analyzer.evaluate_bid(bid)
print(f"Status: {evaluation.status.value}")
print(f"Variance: {evaluation.variance_percent}%")
print(f"Recommendation: {evaluation.recommendation}")
```

## Common Use Cases

### 1. Compare Multiple Bids
```python
bids = [
    SubcontractorBid("ABC Electric", "Electrical", 75000, scope, True, True, True, 30),
    SubcontractorBid("XYZ Power", "Electrical", 68000, scope, True, True, True, 35),
    SubcontractorBid("Quick Elec", "Electrical", 82000, scope, True, True, True, 25)
]

comparison = analyzer.compare_bids(bids)
print(f"Best Value: {comparison['best_value']['name']}")
```

### 2. Negotiation Support
```python
points = analyzer.generate_negotiation_points(evaluation)
for point in points:
    print(f"{point['topic']}: Target ${point.get('target', 'N/A')}")
```

### 3. Export Report
```python
analyzer.export_bid_comparison(comparison, "bid_comparison.xlsx")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.2 - Subcontractor Management
