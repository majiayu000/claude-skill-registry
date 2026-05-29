---
name: truth-finder
category: verification
version: 1.0.0
description: Fact verification, source validation, confidence scoring
priority: 2
data_source: .claude/data/trusted-sources.yaml
---

# Truth Finder Skill

Procedures for verifying factual claims before publication.

## Claim Extraction Types

- **Numerical**: Statistics, percentages, costs
- **Temporal**: Timeframes, dates, frequencies
- **Causal**: X causes Y
- **Comparative**: Better than, more than
- **Regulatory**: Required by law
- **Attribution**: According to experts
- **Absolute**: Always, never, all, none

## Source Tier Reference

**Tier 1 (95-100%)**: .gov.au, courts, standards, peer-reviewed
**Tier 2 (80-94%)**: .edu.au, industry bodies
**Tier 3 (60-79%)**: TED Talks (verified), industry pubs
**Tier 4 (40-59%)**: News media, Wikipedia (leads only)
**NEVER USE**: AI-generated without verification

## Confidence Scoring Formula

```
Base = Source Tier Score
+ Multiple sources: +10% each (max +30%)
+ Primary source: +15%
+ Recent (<1 year): +10%
+ Peer-reviewed: +15%
- Single source: -20%
- Outdated (>3 years): -15% to -30%
- Known bias: -25%
```

## Publishing Thresholds

- 95%+: Publish with "Verified" badge
- 80-94%: Publish with citations
- 60-79%: Publish with disclaimer
- 40-59%: Human review required
- <40%: **DO NOT PUBLISH**

## Citation Formats

- **Marketing**: Hover reveal
- **Blog**: "According to [Source], [claim]"
- **Technical**: Footnotes¹
- **Legal**: Full academic citation
