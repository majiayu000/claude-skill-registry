---
slug: "cwicr-comparison-tool"
display_name: "CWICR Comparison Tool"
description: "Compare cost estimates across projects, versions, and scenarios. Identify variances, benchmark against standards, and generate comparison reports."
---

# CWICR Comparison Tool

## Business Case

### Problem Statement
Project stakeholders need to compare:
- Alternative design options
- Estimate versions over time
- Projects against benchmarks
- Actual vs estimated costs

### Solution
Structured comparison of CWICR-based estimates with variance analysis, benchmarking, and visual reporting.

### Business Value
- **Decision support** - Compare alternatives objectively
- **Version control** - Track estimate evolution
- **Benchmarking** - Compare against standards
- **Audit** - Document estimate changes

## Technical Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class ComparisonType(Enum):
    """Types of comparisons."""
    VERSION = "version"          # Same project, different versions
    ALTERNATIVE = "alternative"  # Same project, design alternatives
    BENCHMARK = "benchmark"      # Project vs standard/benchmark
    ACTUAL = "actual"            # Estimate vs actual costs
    PROJECT = "project"          # Different projects


class VarianceSignificance(Enum):
    """Significance level of variance."""
    CRITICAL = "critical"    # >20% variance
    HIGH = "high"            # 10-20%
    MEDIUM = "medium"        # 5-10%
    LOW = "low"              # <5%
    NONE = "none"            # No variance


@dataclass
class ComparisonItem:
    """Single item comparison."""
    work_item_code: str
    description: str
    base_quantity: float
    base_cost: float
    compare_quantity: float
    compare_cost: float
    quantity_variance: float
    quantity_variance_pct: float
    cost_variance: float
    cost_variance_pct: float
    significance: VarianceSignificance


@dataclass
class ComparisonResult:
    """Complete comparison result."""
    comparison_type: ComparisonType
    base_name: str
    compare_name: str
    base_total: float
    compare_total: float
    total_variance: float
    total_variance_pct: float
    items: List[ComparisonItem]
    summary_by_category: Dict[str, Dict[str, float]]
    created_at: datetime


class CWICRComparisonTool:
    """Compare CWICR-based estimates."""

    SIGNIFICANCE_THRESHOLDS = {
        VarianceSignificance.CRITICAL: 0.20,
        VarianceSignificance.HIGH: 0.10,
        VarianceSignificance.MEDIUM: 0.05,
        VarianceSignificance.LOW: 0.01
    }

    def __init__(self):
        pass

    def _get_significance(self, variance_pct: float) -> VarianceSignificance:
        """Determine variance significance."""
        abs_var = abs(variance_pct) / 100

        if abs_var >= self.SIGNIFICANCE_THRESHOLDS[VarianceSignificance.CRITICAL]:
            return VarianceSignificance.CRITICAL
        elif abs_var >= self.SIGNIFICANCE_THRESHOLDS[VarianceSignificance.HIGH]:
            return VarianceSignificance.HIGH
        elif abs_var >= self.SIGNIFICANCE_THRESHOLDS[VarianceSignificance.MEDIUM]:
            return VarianceSignificance.MEDIUM
        elif abs_var >= self.SIGNIFICANCE_THRESHOLDS[VarianceSignificance.LOW]:
            return VarianceSignificance.LOW
        else:
            return VarianceSignificance.NONE

    def compare_estimates(self,
                          base_df: pd.DataFrame,
                          compare_df: pd.DataFrame,
                          base_name: str = "Base",
                          compare_name: str = "Compare",
                          comparison_type: ComparisonType = ComparisonType.VERSION,
                          code_column: str = 'work_item_code',
                          quantity_column: str = 'quantity',
                          cost_column: str = 'total_cost') -> ComparisonResult:
        """Compare two estimates."""

        # Merge on code
        merged = base_df.merge(
            compare_df,
            on=code_column,
            how='outer',
            suffixes=('_base', '_compare')
        )

        items = []
        for _, row in merged.iterrows():
            base_qty = float(row.get(f'{quantity_column}_base', 0) or 0)
            base_cost = float(row.get(f'{cost_column}_base', 0) or 0)
            compare_qty = float(row.get(f'{quantity_column}_compare', 0) or 0)
            compare_cost = float(row.get(f'{cost_column}_compare', 0) or 0)

            qty_variance = compare_qty - base_qty
            qty_variance_pct = (qty_variance / base_qty * 100) if base_qty > 0 else (100 if compare_qty > 0 else 0)

            cost_variance = compare_cost - base_cost
            cost_variance_pct = (cost_variance / base_cost * 100) if base_cost > 0 else (100 if compare_cost > 0 else 0)

            items.append(ComparisonItem(
                work_item_code=str(row.get(code_column, '')),
                description=str(row.get('description_base', row.get('description_compare', ''))),
                base_quantity=base_qty,
                base_cost=base_cost,
                compare_quantity=compare_qty,
                compare_cost=compare_cost,
                quantity_variance=round(qty_variance, 2),
                quantity_variance_pct=round(qty_variance_pct, 1),
                cost_variance=round(cost_variance, 2),
                cost_variance_pct=round(cost_variance_pct, 1),
                significance=self._get_significance(cost_variance_pct)
            ))

        # Totals
        base_total = sum(i.base_cost for i in items)
        compare_total = sum(i.compare_cost for i in items)
        total_variance = compare_total - base_total
        total_variance_pct = (total_variance / base_total * 100) if base_total > 0 else 0

        # Summary by category
        summary_by_category = self._summarize_by_category(items, merged)

        return ComparisonResult(
            comparison_type=comparison_type,
            base_name=base_name,
            compare_name=compare_name,
            base_total=round(base_total, 2),
            compare_total=round(compare_total, 2),
            total_variance=round(total_variance, 2),
            total_variance_pct=round(total_variance_pct, 1),
            items=items,
            summary_by_category=summary_by_category,
            created_at=datetime.now()
        )

    def _summarize_by_category(self,
                                items: List[ComparisonItem],
                                merged_df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
        """Summarize comparison by category."""

        summary = {}

        # Try to extract category from work item code prefix
        for item in items:
            code = item.work_item_code
            category = code.split('-')[0] if '-' in code else 'Other'

            if category not in summary:
                summary[category] = {
                    'base_cost': 0,
                    'compare_cost': 0,
                    'variance': 0,
                    'variance_pct': 0,
                    'item_count': 0
                }

            summary[category]['base_cost'] += item.base_cost
            summary[category]['compare_cost'] += item.compare_cost
            summary[category]['variance'] += item.cost_variance
            summary[category]['item_count'] += 1

        # Calculate percentages
        for category in summary:
            base = summary[category]['base_cost']
            if base > 0:
                summary[category]['variance_pct'] = round(
                    summary[category]['variance'] / base * 100, 1
                )

        return summary

    def get_significant_variances(self,
                                   result: ComparisonResult,
                                   min_significance: VarianceSignificance = VarianceSignificance.MEDIUM) -> List[ComparisonItem]:
        """Get items with significant variances."""

        significance_order = [
            VarianceSignificance.CRITICAL,
            VarianceSignificance.HIGH,
            VarianceSignificance.MEDIUM,
            VarianceSignificance.LOW,
            VarianceSignificance.NONE
        ]

        min_index = significance_order.index(min_significance)
        significant = [
            item for item in result.items
            if significance_order.index(item.significance) <= min_index
        ]

        return sorted(significant, key=lambda x: abs(x.cost_variance), reverse=True)

    def compare_multiple(self,
                          estimates: List[Tuple[str, pd.DataFrame]],
                          base_index: int = 0) -> Dict[str, ComparisonResult]:
        """Compare multiple estimates against base."""

        base_name, base_df = estimates[base_index]
        results = {}

        for i, (name, df) in enumerate(estimates):
            if i == base_index:
                continue

            result = self.compare_estimates(
                base_df=base_df,
                compare_df=df,
                base_name=base_name,
                compare_name=name,
                comparison_type=ComparisonType.ALTERNATIVE
            )
            results[name] = result

        return results

    def benchmark_comparison(self,
                              project_df: pd.DataFrame,
                              benchmark_df: pd.DataFrame,
                              project_name: str,
                              benchmark_name: str = "Industry Benchmark") -> ComparisonResult:
        """Compare project against benchmark."""

        return self.compare_estimates(
            base_df=benchmark_df,
            compare_df=project_df,
            base_name=benchmark_name,
            compare_name=project_name,
            comparison_type=ComparisonType.BENCHMARK
        )

    def version_comparison(self,
                           versions: List[Tuple[str, pd.DataFrame]]) -> List[ComparisonResult]:
        """Compare sequential versions."""

        results = []

        for i in range(1, len(versions)):
            prev_name, prev_df = versions[i-1]
            curr_name, curr_df = versions[i]

            result = self.compare_estimates(
                base_df=prev_df,
                compare_df=curr_df,
                base_name=prev_name,
                compare_name=curr_name,
                comparison_type=ComparisonType.VERSION
            )
            results.append(result)

        return results

    def export_comparison(self,
                          result: ComparisonResult,
                          output_path: str) -> str:
        """Export comparison to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary_df = pd.DataFrame([{
                'Comparison Type': result.comparison_type.value,
                'Base': result.base_name,
                'Compare': result.compare_name,
                'Base Total': result.base_total,
                'Compare Total': result.compare_total,
                'Variance': result.total_variance,
                'Variance %': result.total_variance_pct,
                'Generated': result.created_at.strftime('%Y-%m-%d %H:%M')
            }])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Details
            details_df = pd.DataFrame([
                {
                    'Work Item': i.work_item_code,
                    'Description': i.description,
                    f'{result.base_name} Qty': i.base_quantity,
                    f'{result.base_name} Cost': i.base_cost,
                    f'{result.compare_name} Qty': i.compare_quantity,
                    f'{result.compare_name} Cost': i.compare_cost,
                    'Qty Variance': i.quantity_variance,
                    'Qty Variance %': i.quantity_variance_pct,
                    'Cost Variance': i.cost_variance,
                    'Cost Variance %': i.cost_variance_pct,
                    'Significance': i.significance.value
                }
                for i in result.items
            ])
            details_df.to_excel(writer, sheet_name='Details', index=False)

            # By Category
            cat_df = pd.DataFrame([
                {
                    'Category': cat,
                    'Base Cost': data['base_cost'],
                    'Compare Cost': data['compare_cost'],
                    'Variance': data['variance'],
                    'Variance %': data['variance_pct'],
                    'Items': data['item_count']
                }
                for cat, data in result.summary_by_category.items()
            ])
            cat_df.to_excel(writer, sheet_name='By Category', index=False)

            # Significant Variances
            significant = self.get_significant_variances(result)
            sig_df = pd.DataFrame([
                {
                    'Work Item': i.work_item_code,
                    'Description': i.description,
                    'Cost Variance': i.cost_variance,
                    'Variance %': i.cost_variance_pct,
                    'Significance': i.significance.value
                }
                for i in significant
            ])
            sig_df.to_excel(writer, sheet_name='Significant', index=False)

        return output_path


class ComparisonAnalytics:
    """Analytics for comparison results."""

    def __init__(self, comparison_tool: CWICRComparisonTool):
        self.tool = comparison_tool

    def variance_distribution(self, result: ComparisonResult) -> Dict[str, int]:
        """Get distribution of variance significance."""

        distribution = {s.value: 0 for s in VarianceSignificance}

        for item in result.items:
            distribution[item.significance.value] += 1

        return distribution

    def top_variances(self,
                      result: ComparisonResult,
                      n: int = 10,
                      positive: bool = True) -> List[ComparisonItem]:
        """Get top N variances (positive or negative)."""

        if positive:
            sorted_items = sorted(result.items, key=lambda x: x.cost_variance, reverse=True)
        else:
            sorted_items = sorted(result.items, key=lambda x: x.cost_variance)

        return sorted_items[:n]

    def category_impact(self, result: ComparisonResult) -> pd.DataFrame:
        """Analyze which categories contribute most to variance."""

        data = []
        for cat, values in result.summary_by_category.items():
            contribution_pct = (values['variance'] / result.total_variance * 100) if result.total_variance != 0 else 0
            data.append({
                'Category': cat,
                'Variance': values['variance'],
                'Contribution %': round(contribution_pct, 1)
            })

        return pd.DataFrame(data).sort_values('Contribution %', ascending=False)

    def trend_analysis(self,
                        version_results: List[ComparisonResult]) -> pd.DataFrame:
        """Analyze cost trend across versions."""

        data = []
        cumulative = 0

        for result in version_results:
            cumulative += result.total_variance
            data.append({
                'From': result.base_name,
                'To': result.compare_name,
                'Variance': result.total_variance,
                'Variance %': result.total_variance_pct,
                'Cumulative Variance': cumulative
            })

        return pd.DataFrame(data)
```

## Quick Start

```python
# Initialize comparison tool
tool = CWICRComparisonTool()

# Compare two estimate versions
result = tool.compare_estimates(
    base_df=estimate_v1,
    compare_df=estimate_v2,
    base_name="Estimate v1.0",
    compare_name="Estimate v2.0"
)

print(f"Total Variance: ${result.total_variance:,.2f} ({result.total_variance_pct}%)")
```

## Common Use Cases

### 1. Significant Variances
```python
significant = tool.get_significant_variances(result)
for item in significant[:5]:
    print(f"{item.work_item_code}: ${item.cost_variance:,.2f} ({item.significance.value})")
```

### 2. Version History
```python
versions = [
    ("v1.0", estimate_v1),
    ("v2.0", estimate_v2),
    ("v3.0", estimate_v3)
]
version_results = tool.version_comparison(versions)

analytics = ComparisonAnalytics(tool)
trend = analytics.trend_analysis(version_results)
```

### 3. Design Alternatives
```python
alternatives = [
    ("Option A - Steel", option_a),
    ("Option B - Concrete", option_b),
    ("Option C - Hybrid", option_c)
]
comparisons = tool.compare_multiple(alternatives, base_index=0)
```

### 4. Export Report
```python
tool.export_comparison(result, "estimate_comparison.xlsx")
```

## Resources
- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **DDC Book**: Chapter 3.1 - Estimate Management
