---
name: sec-compliance
description: SEC 2025 compliance validation for investment recommendations. Use when generating, reviewing, or auditing stock recommendations to ensure proper disclosures, audit trails, and regulatory requirements are met. Trigger on any recommendation generation or compliance review task.
metadata: {"clawdbot":{"emoji":"⚖️","project":"investment-analysis-platform"}}
---

# SEC Compliance Skill

Ensure all investment recommendations comply with SEC 2025 regulations for algorithmic investment advice.

## Quick Reference

### Required Disclosures for Every Recommendation

Every stock recommendation MUST include these SEC-required disclosures:

```python
class RecommendationDisclosure:
    # 1. Methodology Disclosure (REQUIRED)
    methodology_disclosure: str  # How the recommendation was generated

    # 2. Data Sources (REQUIRED)
    data_sources: list[str]      # All data sources with timestamps
    model_version: str           # ML model version used
    training_date: str           # Last model training date

    # 3. Risk Warnings (REQUIRED)
    risk_factors: list[str]      # Specific risks for this recommendation
    volatility_warning: bool     # If stock is high volatility
    liquidity_warning: bool      # If low trading volume

    # 4. Performance Disclaimer (REQUIRED)
    disclaimer: str = "Past performance does not guarantee future results."

    # 5. Confidence Level (REQUIRED)
    confidence_score: float      # 0.0 - 1.0
    uncertainty_disclosure: str  # What the model doesn't know
```

## Compliance Checklist

Before publishing ANY recommendation:

```markdown
□ Methodology Disclosure
  - [ ] Algorithm description is included
  - [ ] Data sources are listed with timestamps
  - [ ] Model version is documented

□ Risk Warnings
  - [ ] "Past performance" disclaimer present
  - [ ] Stock-specific risk factors listed
  - [ ] Volatility/liquidity warnings if applicable
  - [ ] Sector concentration alert if needed

□ Fair Presentation
  - [ ] Balanced view of risks AND opportunities
  - [ ] No misleading performance claims
  - [ ] Clear distinction between historical and projected

□ Audit Trail
  - [ ] Recommendation ID generated
  - [ ] All inputs logged
  - [ ] Timestamp recorded
  - [ ] User interaction tracked

□ Limitations Statement
  - [ ] Scope of analysis disclosed
  - [ ] Data freshness limitations noted
  - [ ] Model confidence levels shown
```

## Audit Logging Requirements

```python
# Every recommendation must be logged for SEC compliance
# Retention: 5+ years minimum

audit_log = {
    "event_id": str(uuid.uuid4()),
    "timestamp": datetime.utcnow().isoformat(),
    "event_type": "recommendation.generated",

    # Inputs
    "ticker": ticker,
    "input_data": {
        "fundamental_metrics": {...},
        "technical_indicators": {...},
        "sentiment_scores": {...},
        "data_timestamps": {...},
    },

    # Model Info
    "model_version": "v2.3.1",
    "model_training_date": "2025-01-15",

    # Output
    "recommendation": {
        "action": "BUY",
        "confidence": 0.78,
        "target_price": 155.00,
        "thesis": "...",
        "risk_factors": [...],
    },

    # Compliance
    "disclosures_included": True,
    "compliance_check_passed": True,
}
```

## Validation Commands

```bash
# Validate a recommendation object has all required disclosures
python -c "
from backend.services.compliance import SECComplianceValidator

validator = SECComplianceValidator()
result = validator.validate_recommendation(recommendation)

if not result.is_compliant:
    print('COMPLIANCE FAILURE:')
    for issue in result.issues:
        print(f'  - {issue}')
else:
    print('Recommendation is SEC compliant')
"

# Check audit trail completeness
python -c "
from backend.services.audit import AuditService

audit = AuditService()
gaps = audit.find_compliance_gaps(
    start_date='2025-01-01',
    end_date='2025-01-25'
)
print(f'Found {len(gaps)} audit trail gaps')
"
```

## Common Compliance Issues

| Issue | Fix |
|-------|-----|
| Missing methodology | Add `methodology_disclosure` field |
| No data timestamps | Include `data_source_timestamps` |
| Missing risk warning | Add standard disclaimer text |
| No confidence score | Calculate and include model confidence |
| Audit log missing | Ensure `AuditLogger.log()` called |

## Integration with Recommendation Engine

```python
# Always wrap recommendation generation with compliance check
from backend.services.compliance import ensure_sec_compliance

@ensure_sec_compliance
async def generate_recommendation(ticker: str) -> Recommendation:
    # ... analysis logic ...
    return recommendation  # Decorator validates before returning
```

## GDPR Considerations

When recommendations are personalized:
- Track consent for data processing
- Implement data export capability
- Support right to erasure (anonymization)
- Document lawful basis for processing
