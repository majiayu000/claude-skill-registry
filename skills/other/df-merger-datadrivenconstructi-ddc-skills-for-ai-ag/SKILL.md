---
name: "df-merger"
description: "Merge pandas DataFrames from multiple construction sources. Handle different schemas, keys, and data quality issues."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🐼", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# DataFrame Merger for Construction Data

## Overview
Construction projects combine data from BIM, schedules, costs, and sensors. This skill merges DataFrames from disparate sources with intelligent key matching and schema reconciliation.

## Python Implementation

```python
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from difflib import SequenceMatcher


class MergeStrategy(Enum):
    """DataFrame merge strategies."""
    INNER = "inner"       # Only matching rows
    LEFT = "left"         # All left, matching right
    RIGHT = "right"       # Matching left, all right
    OUTER = "outer"       # All rows from both
    CROSS = "cross"       # Cartesian product


@dataclass
class MergeResult:
    """Result of merge operation."""
    merged_df: pd.DataFrame
    matched_rows: int
    left_only: int
    right_only: int
    merge_quality: float  # 0-1 score


class ConstructionDFMerger:
    """Merge DataFrames from construction sources."""

    # Common construction column name mappings
    COLUMN_MAPPINGS = {
        'element_id': ['elementid', 'elem_id', 'id', 'guid', 'globalid'],
        'type_name': ['typename', 'type', 'element_type', 'category'],
        'level': ['level', 'floor', 'storey', 'building_storey'],
        'material': ['material', 'mat', 'material_name'],
        'volume': ['volume', 'vol', 'volume_m3', 'qty_volume'],
        'area': ['area', 'surface_area', 'qty_area', 'area_m2'],
        'cost': ['cost', 'price', 'total_cost', 'amount'],
        'task_id': ['task_id', 'activity_id', 'wbs', 'activity'],
        'start_date': ['start', 'start_date', 'planned_start', 'begin'],
        'end_date': ['end', 'end_date', 'planned_finish', 'finish']
    }

    def __init__(self):
        self.column_cache: Dict[str, str] = {}

    def find_common_key(self, df1: pd.DataFrame,
                        df2: pd.DataFrame) -> Optional[str]:
        """Find common key column between DataFrames."""

        # Check exact matches first
        common = set(df1.columns) & set(df2.columns)
        if common:
            # Prefer ID-like columns
            for col in common:
                if 'id' in col.lower() or 'code' in col.lower():
                    return col
            return list(common)[0]

        # Try semantic matching
        for col1 in df1.columns:
            for col2 in df2.columns:
                if self._columns_match(col1, col2):
                    return col1

        return None

    def _columns_match(self, col1: str, col2: str) -> bool:
        """Check if column names are semantically similar."""
        col1_lower = col1.lower().replace('_', '').replace('-', '')
        col2_lower = col2.lower().replace('_', '').replace('-', '')

        # Exact match after normalization
        if col1_lower == col2_lower:
            return True

        # Check against mappings
        for standard, variants in self.COLUMN_MAPPINGS.items():
            if col1_lower in variants and col2_lower in variants:
                return True

        # Similarity check
        similarity = SequenceMatcher(None, col1_lower, col2_lower).ratio()
        return similarity > 0.8

    def harmonize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Standardize column names."""
        df = df.copy()
        rename_map = {}

        for col in df.columns:
            col_lower = col.lower().replace('_', '').replace('-', '')

            for standard, variants in self.COLUMN_MAPPINGS.items():
                if col_lower in variants:
                    rename_map[col] = standard
                    break

        return df.rename(columns=rename_map)

    def merge(self, left: pd.DataFrame,
              right: pd.DataFrame,
              on: Optional[str] = None,
              left_on: Optional[str] = None,
              right_on: Optional[str] = None,
              how: MergeStrategy = MergeStrategy.LEFT,
              harmonize: bool = True) -> MergeResult:
        """Merge two DataFrames."""

        if harmonize:
            left = self.harmonize_columns(left)
            right = self.harmonize_columns(right)

        # Determine merge keys
        if on is None and left_on is None and right_on is None:
            common_key = self.find_common_key(left, right)
            if common_key is None:
                raise ValueError("No common key found. Specify merge key manually.")
            on = common_key

        # Perform merge
        merged = pd.merge(
            left, right,
            on=on,
            left_on=left_on,
            right_on=right_on,
            how=how.value,
            indicator=True,
            suffixes=('_left', '_right')
        )

        # Calculate statistics
        matched = len(merged[merged['_merge'] == 'both'])
        left_only = len(merged[merged['_merge'] == 'left_only'])
        right_only = len(merged[merged['_merge'] == 'right_only'])

        # Quality score
        total = len(left) + len(right)
        quality = (matched * 2) / total if total > 0 else 0

        # Clean up
        merged = merged.drop('_merge', axis=1)

        return MergeResult(
            merged_df=merged,
            matched_rows=matched,
            left_only=left_only,
            right_only=right_only,
            merge_quality=round(quality, 2)
        )

    def merge_multiple(self, dfs: List[pd.DataFrame],
                       on: Optional[str] = None,
                       how: MergeStrategy = MergeStrategy.OUTER) -> pd.DataFrame:
        """Merge multiple DataFrames sequentially."""

        if not dfs:
            return pd.DataFrame()

        result = dfs[0].copy()

        for i, df in enumerate(dfs[1:], 1):
            result_obj = self.merge(result, df, on=on, how=how)
            result = result_obj.merged_df

        return result

    def fuzzy_merge(self, left: pd.DataFrame,
                    right: pd.DataFrame,
                    left_on: str,
                    right_on: str,
                    threshold: float = 0.8) -> pd.DataFrame:
        """Merge using fuzzy string matching."""

        matches = []

        left_values = left[left_on].dropna().unique()
        right_values = right[right_on].dropna().unique()

        for lval in left_values:
            best_match = None
            best_score = 0

            for rval in right_values:
                score = SequenceMatcher(None, str(lval).lower(),
                                        str(rval).lower()).ratio()
                if score > best_score and score >= threshold:
                    best_score = score
                    best_match = rval

            if best_match:
                matches.append({
                    'left_key': lval,
                    'right_key': best_match,
                    'match_score': best_score
                })

        match_df = pd.DataFrame(matches)

        # Join using match mapping
        left_with_key = left.merge(match_df, left_on=left_on, right_on='left_key', how='left')
        result = left_with_key.merge(right, left_on='right_key', right_on=right_on, how='left')

        return result


class BIMScheduleMerger(ConstructionDFMerger):
    """Specialized merger for BIM and schedule data."""

    def merge_bim_schedule(self, bim_df: pd.DataFrame,
                           schedule_df: pd.DataFrame,
                           bim_type_col: str = 'Type Name',
                           schedule_wbs_col: str = 'WBS') -> pd.DataFrame:
        """Merge BIM elements with schedule activities."""

        # This typically requires a mapping table
        # For now, use fuzzy matching on descriptions

        bim_df = self.harmonize_columns(bim_df)
        schedule_df = self.harmonize_columns(schedule_df)

        # Try to match type names to WBS descriptions
        result = self.fuzzy_merge(
            bim_df, schedule_df,
            left_on=bim_type_col,
            right_on=schedule_wbs_col,
            threshold=0.6
        )

        return result


class CostQTOMerger(ConstructionDFMerger):
    """Merge cost data with quantity takeoffs."""

    def merge_cost_qto(self, cost_df: pd.DataFrame,
                       qto_df: pd.DataFrame) -> pd.DataFrame:
        """Merge cost rates with QTO quantities."""

        cost_df = self.harmonize_columns(cost_df)
        qto_df = self.harmonize_columns(qto_df)

        # Try common merge keys
        for key in ['work_item_code', 'type_name', 'material', 'element_id']:
            if key in cost_df.columns and key in qto_df.columns:
                result = self.merge(cost_df, qto_df, on=key)

                # Calculate extended costs
                result.merged_df['extended_cost'] = (
                    result.merged_df.get('quantity', 0) *
                    result.merged_df.get('unit_price', 0)
                )

                return result.merged_df

        # Fallback to fuzzy merge
        return self.fuzzy_merge(
            qto_df, cost_df,
            left_on='type_name' if 'type_name' in qto_df.columns else qto_df.columns[0],
            right_on='description' if 'description' in cost_df.columns else cost_df.columns[0]
        )
```

## Quick Start

```python
merger = ConstructionDFMerger()

# Merge two DataFrames
result = merger.merge(bim_df, schedule_df)
print(f"Matched: {result.matched_rows}, Quality: {result.merge_quality}")

# Access merged data
merged = result.merged_df
```

## Common Use Cases

### 1. BIM + Schedule Integration
```python
bim_schedule = BIMScheduleMerger()
integrated = bim_schedule.merge_bim_schedule(bim_elements, schedule_activities)
```

### 2. Cost + QTO
```python
cost_merger = CostQTOMerger()
priced_qto = cost_merger.merge_cost_qto(cost_database, quantities)
print(f"Total: ${priced_qto['extended_cost'].sum():,.2f}")
```

### 3. Multiple Sources
```python
all_data = merger.merge_multiple(
    [bim_df, schedule_df, cost_df, resource_df],
    on='element_id'
)
```

## Resources
- **DDC Book**: Chapter 2.3 - Pandas DataFrame
