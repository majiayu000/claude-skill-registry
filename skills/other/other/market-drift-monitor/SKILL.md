---
name: market-drift-monitor
description: Monitors PostgreSQL data quality for lead intelligence, detecting market drift in lead source quality, conversion readiness, and ROI metrics. Use when auditing lead generation performance or validating data integrity across tenants.
---

# Market Drift Monitor Skill

This skill provides specialized procedures for auditing lead intelligence data quality and detecting market drift in real estate lead generation performance. It leverages the logic from the `EnhancedLeadScoringService` to identify shifts in lead behavior and source effectiveness.

## Core Audit Procedures

### 1. Source Quality Distribution Audit
Monitor the distribution of lead sources and their relative quality scores to detect if high-performing channels are degrading.

**Key Metrics:**
- **Source Mix**: Percentage distribution across `LeadSourceType` (REFERRAL, ORGANIC_SEARCH, PAID_SEARCH, etc.).
- **Quality Velocity**: Change in average `source_quality_score` over a 30-day window.
- **Attribution Gap**: Ratio of `UNKNOWN` sources vs. trackable sources.

**SQL Pattern:**
```sql
SELECT 
    source_type, 
    COUNT(*) as lead_count, 
    AVG(source_quality_score) as avg_quality,
    AVG(conversion_likelihood) as avg_conv_likelihood
FROM lead_intelligence_scores
WHERE location_id = :location_id 
  AND scoring_timestamp > NOW() - INTERVAL '30 days'
GROUP BY source_type
ORDER BY avg_quality DESC;
```

### 2. Conversion Readiness Trend Analysis
Detect "Market Drift" by analyzing the shift in `closing_probability` and `conversion_readiness_score`.

**Drift Indicators:**
- **Score Compression**: Increasing volume of leads in the "Lukewarm" (50-69) range with fewer in "Hot" (85+).
- **Signal Decay**: Decrease in the frequency of `positive_signals` (e.g., "High financial readiness") relative to `risk_factors`.

### 3. Behavioral Pattern Audit
Monitor the evolution of prospect engagement by auditing `BehavioralSignals`.

**Audit Targets:**
- **Urgency Frequency**: Count of `urgency_indicators` (asap, urgent, etc.) per 1000 messages.
- **Authority Signal Ratio**: Presence of `decision_authority_signals` in initial qualification turns.
- **Objection Density**: Growth in `objection_patterns` (too expensive, market uncertainty).

## Data Integrity Verification

Ensure the following integrity constraints are maintained across the PostgreSQL `lead_intelligence_v2` schema:

1. **Tenant Isolation**: Verify all queries include `location_id` filtering.
2. **Feature Completeness**: Audit records for missing `utm_source` or `utm_medium` which causes `attribution_confidence` to drop below 0.5.
3. **ML Feature Drift**: Monitor the `avg_message_length` and `question_count` used as features for the `closing_probability_model`.

## Recommended Actions on Drift Detection

- **Source Pivot**: If `PAID_SEARCH` quality drops >15%, recommend shifting budget to `REFERRAL` or `ORGANIC_SEARCH`.
- **Nurture Adjustment**: If `urgency_indicators` decline, suggest updating the "Warm-Lead" nurture sequences with more educational content.
- **Model Retraining**: If `ml_confidence` drops below 0.6 consistently, trigger a request for model retraining on recent 90-day data.

## Integration Points
- **Service**: `ghl_real_estate_ai.services.enhanced_lead_scoring.EnhancedLeadScoringService`
- **Model**: `ghl_real_estate_ai.ml.closing_probability_model`
- **Database**: PostgreSQL (pgvector enabled for behavioral similarity)
