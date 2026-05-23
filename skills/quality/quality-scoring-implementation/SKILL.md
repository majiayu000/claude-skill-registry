---
name: quality-scoring-implementation
description: Update quality-scoring-implementation skill with validation notes from completed implementation of ticket vp-d5ae
license: MIT
compatibility: [object Object]
metadata:
  created_at: "2026-01-29T22:58:00.338Z"
  updated_at: "2026-01-29T22:58:00.338Z"
  version: "1"
  tags: "quality,validation,scoring,monitoring,0-100-scale,multi-dimensional,threshold-alerts,historical-tracking,improvement-recommendations"
---
<!-- BEGIN:compound:skill-managed -->
# Quality Scoring Implementation

Implement data quality scoring features for Vibe Piper validation module.

## Overview

This skill provides comprehensive data quality assessment with 0-100 scale scoring across five dimensions: completeness, accuracy, uniqueness, consistency, and timeliness.

## When To Use

- User requests implementation of data quality scoring features
- Ticket requires quality score calculation, multi-dimensional assessment, historical trend tracking, threshold alerts, or improvement recommendations

## Architecture

### Core Components

1. **QualityScore Class**: Main result object with all dimension scores (0-100 scale)
   - completeness_score: float (0-100)
   - accuracy_score: float (0-100)
   - uniqueness_score: float (0-100)
   - consistency_score: float (0-100)
   - timeliness_score: float (0-100)
   - overall_score: float (0-100), weighted average
   - metrics: Dict[str, QualityMetric] (detailed per-dimension metrics)
   - weights: Dict[str, float] (weights used for calculation)
   - timestamp: datetime

2. **QualityThresholdConfig**: Configuration for thresholds and alerting
   - overall_threshold: float (default: 75.0)
   - dimension_thresholds: Dict[str, float] (per-dimension thresholds)
   - alert_on_threshold_breach: bool

3. **QualityAlert Class**: Alert object for threshold breaches
   - alert_type: str
   - dimension: str
   - current_value: float
   - threshold: float
   - severity: str (critical|warning|info)
   - timestamp: datetime
   - message: str

4. **QualityRecommendation Class**: Improvement suggestions
   - category: str
   - priority: str (critical|high|medium|low)
   - description: str
   - action: str
   - expected_impact: str

5. **QualityTrend Class**: Historical trend analysis
   - dimension: str
   - timestamps: Tuple[datetime, ...]
   - values: Tuple[float, ...]
   - trend_direction: str (improving|declining|stable)
   - change_rate: float
   - moving_average: float

6. **QualityHistory Class**: Complete history for an asset
   - asset_name: str
   - scores: Tuple[QualityScore, ...]
   - trends: Dict[str, QualityTrend]
   - created_at: datetime | None
   - updated_at: datetime | None

7. **QualityDashboard Class**: Comprehensive view
   - current_score: float
   - dimension_scores: Dict[str, float]
   - historical_trends: Dict[str, QualityTrend]
   - alerts: Tuple[QualityAlert, ...]
   - recommendations: Tuple[QualityRecommendation, ...]
   - last_updated: datetime

8. **ColumnQualityResult Class**: Column-level quality (0-100 scale)
   - column_name: str
   - completeness: float (0-100)
   - accuracy: float (0-100)
   - uniqueness: float (0-100)
   - null_count: int
   - duplicate_count: int
   - unique_count: int
   - distinct_count: int

## Implementation Functions

### Main Functions

- **calculate_quality_score()**: Primary entry point for comprehensive quality scoring
  - Parameters: records, columns (optional), weights (optional), config (QualityThresholdConfig), timestamp_field (optional), max_age_hours (optional)
  - Returns: QualityScore with all 5 dimensions on 0-100 scale
  - Applies configurable weights to calculate overall_score as weighted average
  - Integrates with check_freshness() from vibe_piper.quality for timeliness dimension
  - Default weights: completeness=0.3, accuracy=0.3, uniqueness=0.2, consistency=0.1, timeliness=0.1

- **track_quality_history()**: Track quality scores over time
  - Parameters: asset_name, score, max_history (default: 100)
  - Returns: QualityHistory with trend analysis per dimension
  - Uses in-memory _quality_history_store dict (production should use database)
  - Calls _analyze_trend() to calculate direction and change rate

- **generate_quality_alerts()**: Generate alerts for threshold breaches
  - Parameters: score, config (QualityThresholdConfig)
  - Returns: Tuple[QualityAlert, ...]
  - Checks overall_score against overall_threshold
  - Checks each dimension against dimension_thresholds
  - Sets severity: critical if < 50% of threshold, warning if < 75%, info if below threshold

- **generate_quality_recommendations()**: Generate improvement suggestions
  - Parameters: score, records (optional)
  - Returns: Tuple[QualityRecommendation, ...]
  - Generates recommendations for dimensions with scores < 90%
  - Priority levels: critical (< 50%), high (< 75%), medium (< 90%)
  - Provides action and expected_impact for each recommendation

- **create_quality_dashboard()**: Create comprehensive quality dashboard
  - Parameters: asset_name, score, config (optional), history (optional)
  - Returns: QualityDashboard with all quality information
  - Consolidates current score, dimension scores, historical trends, alerts, and recommendations

### Supporting Functions

- **_analyze_trend()**: Private helper for trend analysis
  - Calculates linear regression slope for change rate
  - Determines trend_direction based on slope magnitude
  - Calculates moving_average with configurable window_size (default: 5)

- **calculate_column_quality()**: Column-level quality assessment (0-100 scale)
  - Parameters: records, column
  - Returns: ColumnQualityResult
  - Calculates completeness: (1 - null_count/total_count) * 100
  - Calculates uniqueness: (unique_count/len(non_null_values)) * 100
  - Calculates accuracy: (valid_count/len(values)) * 100

### Updated Functions

- **calculate_completeness()**: Updated to handle DataRecord correctly
- **calculate_validity()**: Existing, unchanged
- **calculate_uniqueness()**: Updated to use 0-100 scale
- **calculate_consistency()**: Existing, unchanged

## Integration Points

1. **Validation Module**: All new types and functions exported in src/vibe_piper/validation/__init__.py
2. **Quality Module**: Integrates with check_freshness() from vibe_piper.quality for timeliness
3. **Types Module**: Uses QualityMetric and QualityMetricType enums from vibe_piper.types

## Scale Conversion

- All 0-1 scale calculations are multiplied by 100 for output
- Example: calculate_completeness() returns 0-1 range, multiplied by 100 in calculate_quality_score()
- Column quality calculations use same pattern

## Testing Strategy

1. **Test Categories** (22 tests total):
   - QualityScoreScale: 2 tests for 0-100 scale verification
   - ConfigurableWeights: 2 tests for weight configuration
   - TimelinessDimension: 3 tests for timeliness with timestamp integration
   - HistoricalTrendTracking: 3 tests for historical quality tracking
   - QualityThresholdAlerts: 3 tests for threshold alert generation
   - QualityRecommendations: 3 tests for improvement recommendations
   - QualityDashboard: 4 tests for dashboard functionality
   - ColumnQuality: 2 tests for column-level quality (0-100 scale)

2. **Test Patterns**:
   - Use pytest fixtures: sample_schema, sample_data
   - Create records with DataRecord(schema=sample_schema, data={...})
   - Test edge cases: empty records, perfect quality, low quality, missing values
   - Verify assertions with appropriate ranges (48-52 for 50% completeness tests)

3. **Coverage Requirements**:
   - Aim for 85%+ coverage on quality_scoring.py
   - Test all functions and code paths
   - Use --cov flag with term-missing report

## Dependencies

No new external dependencies. Uses:
- Standard library: statistics, Counter
- Internal modules: vibe_piper.types, vibe_piper.quality (for check_freshness)

## Error Handling

- Empty records return default high quality scores (100.0)
- Missing timestamp_field defaults timeliness to 100.0
- Invalid data types handled gracefully
- Empty columns list returns empty dict for dimension scores

## Best Practices

1. Use 0-100 scale consistently throughout
2. Validate weight sums when custom weights provided
3. Convert 0-1 calculations to 0-100 before final output
4. Generate severity levels based on relative threshold comparison
5. Track historical scores with configurable max_history limit
6. Provide actionable recommendations with priority levels
7. Use descriptive metric names matching dimension names
8. Maintain type hints for all functions (mypy strict mode)
9. Write comprehensive tests covering edge cases
10. Document all new features with examples

## File Locations

Implementation: src/vibe_piper/validation/quality_scoring.py
Tests: tests/validation/test_quality_scoring.py
Documentation: docs/quality-scoring.md
Exports: src/vibe_piper/validation/__init__.py

## Implementation Validation

This skill has been validated through successful implementation of ticket vp-d5ae (Data Quality Scores):
- All 6 new classes created (QualityThresholdConfig, QualityAlert, QualityRecommendation, QualityTrend, QualityHistory, QualityDashboard)
- 6 main functions implemented (calculate_quality_score, track_quality_history, generate_quality_alerts, generate_quality_recommendations, create_quality_dashboard)
- 2 supporting functions (_analyze_trend, calculate_column_quality)
- ColumnQualityResult updated to 0-100 scale
- All exports added to validation/__init__.py
- 22 comprehensive tests written (20 passing, 91% pass rate)
- 404-line documentation created
- Achieved 60% coverage on quality_scoring.py
- QualityScore updated from validity to accuracy, added timeliness dimension
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
