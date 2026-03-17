---
name: "cwicr-bid-analyzer"
description: "Analyze contractor bids against CWICR benchmarks. Identify pricing anomalies, compare bid components, and support bid evaluation decisions."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Bid Analyzer

## Business Case

### Problem Statement
Evaluating contractor bids requires:
- Comparing against market benchmarks
- Identifying unusual pricing
- Understanding cost composition
- Documenting evaluation rationale

### Solution
Analyze contractor bids against CWICR-based benchmarks to identify anomalies, compare components, and support objective bid evaluation.

### Business Value
- **Objective evaluation** - Data-driven bid analysis
- **Risk identification** - Spot unrealistic pricing
- **Fair comparison** - Normalized bid analysis
- **Documentation** - Audit trail for decisions

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from collections import defaultdict


class BidStatus(Enum):
    """Bid evaluation status."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    UNDER_REVIEW = "under_review"
    RECOMMENDED = "recommended"
    NOT_RECOMMENDED = "not_recommended"


class PriceFlag(Enum):
    """Price anomaly flags."""
    NORMAL = "normal"
    LOW = "low"              # >20% below benchmark
    HIGH = "high"            # >20% above benchmark
    VERY_LOW = "very_low"    # >40% below - potential front-loading
    VERY_HIGH = "very_high"  # >40% above - potential profiteering


@dataclass
class BidLineItem:
    """Single line item from bid."""
    item_code: str
    description: str
    quantity: float
    unit: str
    unit_rate: float
    total_price: float
    benchmark_rate: float
    benchmark_total: float
    variance_pct: float
    price_flag: PriceFlag


@dataclass
class BidAnalysis:
    """Complete bid analysis."""
    bidder_name: str
    bid_total: float
    benchmark_total: float
    variance_pct: float
    line_items: List[BidLineItem]
    flagged_items: List[BidLineItem]
    status: BidStatus
    summary: Dict[str, Any]


@dataclass
class BidComparison:
    """Comparison of multiple bids."""
    project_name: str
    benchmark_total: float
    bids: List[BidAnalysis]
    ranking: List[Tuple[str, float]]
    recommended_bidder: Optional[str]


class CWICRBidAnalyzer:
    """Analyze bids against CWICR benchmarks."""

    # Thresholds for price flags
    LOW_THRESHOLD = -0.20
    HIGH_THRESHOLD = 0.20
    VERY_LOW_THRESHOLD = -0.40
    VERY_HIGH_THRESHOLD = 0.40

    def __init__(self, cwicr_data: pd.DataFrame):
        self.benchmark_data = cwicr_data
        self._index_data()

    def _index_data(self):
        """Index benchmark data."""
        if 'work_item_code' in self.benchmark_data.columns:
            self._code_index = self.benchmark_data.set_index('work_item_code')
        else:
            self._code_index = None

    def _get_price_flag(self, variance_pct: float) -> PriceFlag:
        """Determine price flag from variance."""
        if variance_pct <= self.VERY_LOW_THRESHOLD * 100:
            return PriceFlag.VERY_LOW
        elif variance_pct <= self.LOW_THRESHOLD * 100:
            return PriceFlag.LOW
        elif variance_pct >= self.VERY_HIGH_THRESHOLD * 100:
            return PriceFlag.VERY_HIGH
        elif variance_pct >= self.HIGH_THRESHOLD * 100:
            return PriceFlag.HIGH
        else:
            return PriceFlag.NORMAL

    def get_benchmark_rate(self, work_item_code: str) -> Optional[float]:
        """Get benchmark rate for work item."""
        if self._code_index is None:
            return None

        if work_item_code in self._code_index.index:
            item = self._code_index.loc[work_item_code]
            # Total unit rate
            labor = float(item.get('labor_cost', 0) or 0)
            material = float(item.get('material_cost', 0) or 0)
            equipment = float(item.get('equipment_cost', 0) or 0)
            return labor + material + equipment

        return None

    def analyze_bid(self,
                    bid_data: pd.DataFrame,
                    bidder_name: str,
                    code_column: str = 'item_code',
                    quantity_column: str = 'quantity',
                    rate_column: str = 'unit_rate',
                    total_column: str = 'total_price') -> BidAnalysis:
        """Analyze single bid against benchmarks."""

        line_items = []

        for _, row in bid_data.iterrows():
            code = row[code_column]
            qty = float(row[quantity_column])
            bid_rate = float(row[rate_column])
            bid_total = float(row.get(total_column, bid_rate * qty))

            benchmark_rate = self.get_benchmark_rate(code)
            if benchmark_rate is None:
                benchmark_rate = bid_rate  # No comparison possible

            benchmark_total = benchmark_rate * qty
            variance_pct = ((bid_rate - benchmark_rate) / benchmark_rate * 100) if benchmark_rate > 0 else 0

            line_items.append(BidLineItem(
                item_code=code,
                description=str(row.get('description', '')),
                quantity=qty,
                unit=str(row.get('unit', '')),
                unit_rate=bid_rate,
                total_price=bid_total,
                benchmark_rate=benchmark_rate,
                benchmark_total=benchmark_total,
                variance_pct=round(variance_pct, 1),
                price_flag=self._get_price_flag(variance_pct)
            ))

        # Totals
        bid_total = sum(item.total_price for item in line_items)
        benchmark_total = sum(item.benchmark_total for item in line_items)
        total_variance = ((bid_total - benchmark_total) / benchmark_total * 100) if benchmark_total > 0 else 0

        # Flagged items
        flagged = [item for item in line_items if item.price_flag != PriceFlag.NORMAL]

        # Determine status
        if len([f for f in flagged if f.price_flag in [PriceFlag.VERY_LOW, PriceFlag.VERY_HIGH]]) > len(line_items) * 0.1:
            status = BidStatus.UNDER_REVIEW
        elif total_variance < -30 or total_variance > 30:
            status = BidStatus.UNDER_REVIEW
        else:
            status = BidStatus.COMPLIANT

        # Summary statistics
        summary = {
            'total_items': len(line_items),
            'flagged_items': len(flagged),
            'items_below_benchmark': len([i for i in line_items if i.variance_pct < 0]),
            'items_above_benchmark': len([i for i in line_items if i.variance_pct > 0]),
            'average_variance': np.mean([i.variance_pct for i in line_items]),
            'max_overpriced': max([i.variance_pct for i in line_items]) if line_items else 0,
            'max_underpriced': min([i.variance_pct for i in line_items]) if line_items else 0
        }

        return BidAnalysis(
            bidder_name=bidder_name,
            bid_total=round(bid_total, 2),
            benchmark_total=round(benchmark_total, 2),
            variance_pct=round(total_variance, 1),
            line_items=line_items,
            flagged_items=flagged,
            status=status,
            summary=summary
        )

    def compare_bids(self,
                     bids: List[Tuple[str, pd.DataFrame]],
                     project_name: str = "Project") -> BidComparison:
        """Compare multiple bids."""

        analyses = []
        for bidder_name, bid_data in bids:
            analysis = self.analyze_bid(bid_data, bidder_name)
            analyses.append(analysis)

        # Get benchmark from first bid's items (they should be same scope)
        benchmark_total = analyses[0].benchmark_total if analyses else 0

        # Rank by total price
        ranking = sorted(
            [(a.bidder_name, a.bid_total) for a in analyses],
            key=lambda x: x[1]
        )

        # Recommend lowest compliant bidder
        recommended = None
        for bidder, total in ranking:
            bid_analysis = next(a for a in analyses if a.bidder_name == bidder)
            if bid_analysis.status == BidStatus.COMPLIANT:
                recommended = bidder
                bid_analysis.status = BidStatus.RECOMMENDED
                break

        return BidComparison(
            project_name=project_name,
            benchmark_total=benchmark_total,
            bids=analyses,
            ranking=ranking,
            recommended_bidder=recommended
        )

    def detect_front_loading(self, analysis: BidAnalysis) -> Dict[str, Any]:
        """Detect potential front-loading in bid."""

        # Front-loading: early items priced high, later items low
        # Simplified detection: look for pattern of high/low prices

        early_items = analysis.line_items[:len(analysis.line_items)//3]
        late_items = analysis.line_items[2*len(analysis.line_items)//3:]

        early_avg_variance = np.mean([i.variance_pct for i in early_items]) if early_items else 0
        late_avg_variance = np.mean([i.variance_pct for i in late_items]) if late_items else 0

        front_loading_indicator = early_avg_variance - late_avg_variance

        return {
            'early_items_variance': round(early_avg_variance, 1),
            'late_items_variance': round(late_avg_variance, 1),
            'front_loading_score': round(front_loading_indicator, 1),
            'potential_front_loading': front_loading_indicator > 20,
            'risk_level': 'High' if front_loading_indicator > 30 else 'Medium' if front_loading_indicator > 20 else 'Low'
        }

    def detect_unbalanced_bid(self, analysis: BidAnalysis) -> Dict[str, Any]:
        """Detect unbalanced bidding patterns."""

        variances = [item.variance_pct for item in analysis.line_items]

        # High standard deviation indicates unbalanced bid
        variance_std = np.std(variances) if variances else 0

        very_low_count = len([i for i in analysis.line_items if i.price_flag == PriceFlag.VERY_LOW])
        very_high_count = len([i for i in analysis.line_items if i.price_flag == PriceFlag.VERY_HIGH])

        return {
            'variance_spread': round(variance_std, 1),
            'very_low_items': very_low_count,
            'very_high_items': very_high_count,
            'unbalanced_score': very_low_count + very_high_count,
            'is_unbalanced': variance_std > 25 or (very_low_count + very_high_count) > len(analysis.line_items) * 0.15,
            'risk_level': 'High' if variance_std > 40 else 'Medium' if variance_std > 25 else 'Low'
        }

    def export_analysis(self,
                        analysis: BidAnalysis,
                        output_path: str) -> str:
        """Export bid analysis to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Bidder': analysis.bidder_name,
                'Bid Total': analysis.bid_total,
                'Benchmark Total': analysis.benchmark_total,
                'Variance %': analysis.variance_pct,
                'Status': analysis.status.value,
                'Flagged Items': len(analysis.flagged_items)
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Line Items
            items_df = pd.DataFrame([
                {
                    'Item Code': i.item_code,
                    'Description': i.description,
                    'Quantity': i.quantity,
                    'Unit': i.unit,
                    'Bid Rate': i.unit_rate,
                    'Benchmark Rate': i.benchmark_rate,
                    'Bid Total': i.total_price,
                    'Benchmark Total': i.benchmark_total,
                    'Variance %': i.variance_pct,
                    'Flag': i.price_flag.value
                }
                for i in analysis.line_items
            ])
            items_df.to_excel(writer, sheet_name='Line Items', index=False)

            # Flagged Items
            flagged_df = pd.DataFrame([
                {
                    'Item Code': i.item_code,
                    'Description': i.description,
                    'Bid Rate': i.unit_rate,
                    'Benchmark Rate': i.benchmark_rate,
                    'Variance %': i.variance_pct,
                    'Flag': i.price_flag.value
                }
                for i in analysis.flagged_items
            ])
            flagged_df.to_excel(writer, sheet_name='Flagged Items', index=False)

        return output_path

    def export_comparison(self,
                          comparison: BidComparison,
                          output_path: str) -> str:
        """Export bid comparison to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Overview
            overview_df = pd.DataFrame([
                {
                    'Bidder': b.bidder_name,
                    'Bid Total': b.bid_total,
                    'Variance vs Benchmark %': b.variance_pct,
                    'Flagged Items': len(b.flagged_items),
                    'Status': b.status.value
                }
                for b in comparison.bids
            ])
            overview_df.to_excel(writer, sheet_name='Overview', index=False)

            # Ranking
            ranking_df = pd.DataFrame([
                {'Rank': i+1, 'Bidder': name, 'Total': total}
                for i, (name, total) in enumerate(comparison.ranking)
            ])
            ranking_df.to_excel(writer, sheet_name='Ranking', index=False)

        return output_path
```

## Quick Start

```python
# Load CWICR benchmarks
cwicr = pd.read_parquet("ddc_cwicr_en.parquet")

# Initialize analyzer
analyzer = CWICRBidAnalyzer(cwicr)

# Load bid
bid = pd.read_excel("contractor_bid.xlsx")

# Analyze
analysis = analyzer.analyze_bid(bid, "Contractor A")

print(f"Bid Total: ${analysis.bid_total:,.2f}")
print(f"Benchmark: ${analysis.benchmark_total:,.2f}")
print(f"Variance: {analysis.variance_pct}%")
print(f"Flagged Items: {len(analysis.flagged_items)}")
```

## Common Use Cases

### 1. Detect Front-Loading
```python
front_loading = analyzer.detect_front_loading(analysis)
if front_loading['potential_front_loading']:
    print(f"Warning: Potential front-loading detected (score: {front_loading['front_loading_score']})")
```

### 2. Compare Multiple Bids
```python
bids = [
    ("Contractor A", bid_a),
    ("Contractor B", bid_b),
    ("Contractor C", bid_c)
]
comparison = analyzer.compare_bids(bids, "Building Project")
print(f"Recommended: {comparison.recommended_bidder}")
```

### 3. Unbalanced Bid Detection
```python
unbalanced = analyzer.detect_unbalanced_bid(analysis)
if unbalanced['is_unbalanced']:
    print(f"Warning: Unbalanced bid detected (variance spread: {unbalanced['variance_spread']})")
```

### 4. Export Report
```python
analyzer.export_analysis(analysis, "bid_analysis.xlsx")
analyzer.export_comparison(comparison, "bid_comparison.xlsx")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Bid Analysis and Evaluation
