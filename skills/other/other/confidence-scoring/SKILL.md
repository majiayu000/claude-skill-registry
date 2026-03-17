---
name: confidence-scoring
description: "Assess research quality with systematic confidence scoring, source validation, and uncertainty quantification."
---

# Research Confidence Scoring

## Overview

Apply systematic confidence scoring to research findings. Quantify uncertainty, validate sources, detect contradictions, and provide calibrated assessments of information reliability.

## The Process

### 1. Source Assessment

Rate each source on a 0.0-1.0 scale:

| Score | Source Quality |
|-------|---------------|
| 0.9-1.0 | Primary source, official docs, peer-reviewed |
| 0.7-0.8 | Reputable secondary source, established experts |
| 0.5-0.6 | Community content, blog posts, forums |
| 0.3-0.4 | Unverified claims, single source only |
| 0.0-0.2 | Contradicted by better sources, outdated |

**Source Quality Factors:**
- Authority: Is the source authoritative on this topic?
- Recency: How current is the information?
- Corroboration: Do multiple sources agree?
- Methodology: Is reasoning/evidence provided?
- Bias: Does the source have obvious bias?

### 2. Claim Validation

For each research finding:

```
Claim: [Statement being assessed]
Sources: [List of sources]
Source Confidence: [0.0-1.0 per source]
Corroboration: [Number of independent sources agreeing]
Contradictions: [Sources that disagree]
Final Confidence: [Weighted score]
```

**Confidence Calculation:**
- Single source: Cap at 0.6 regardless of source quality
- Two agreeing sources: Up to 0.8
- Three+ agreeing sources: Up to 0.95
- Any contradiction: Reduce by 0.2, flag for review

### 3. Uncertainty Quantification

Express findings with explicit uncertainty:

**High Confidence (0.8-1.0):**
> "X is documented behavior" / "X is confirmed by multiple sources"

**Medium Confidence (0.5-0.7):**
> "X appears to be the case based on..." / "Evidence suggests X"

**Low Confidence (0.2-0.4):**
> "X may be true, but verification needed" / "Limited evidence for X"

**Uncertain (0.0-0.2):**
> "Cannot confirm X" / "Conflicting information about X"

### 4. Contradiction Detection

When sources disagree:

1. **Identify the contradiction**: State both positions clearly
2. **Assess source quality**: Which sources are more authoritative?
3. **Check recency**: Is one source outdated?
4. **Look for context**: Could both be true in different contexts?
5. **Flag unresolved**: If contradiction persists, report both positions

### 5. Confidence Reporting

Structure research output with confidence metadata:

```markdown
## Finding: [Topic]

**Confidence: 0.75** (Medium-High)

**Summary:** [Key finding in 1-2 sentences]

**Evidence:**
- Source A (0.9): [What it says]
- Source B (0.7): [What it says]
- Source C (0.5): [What it says]

**Limitations:**
- [What we couldn't verify]
- [Areas of uncertainty]

**Contradictions:**
- [If any sources disagreed]
```

## Confidence Calibration

### Red Flags (Lower confidence)
- Only one source found
- Source is promotional/marketing content
- Information is > 2 years old for fast-moving topics
- Source has obvious bias or conflict of interest
- Claim seems extraordinary without extraordinary evidence

### Green Flags (Higher confidence)
- Multiple independent sources agree
- Official documentation confirms
- Peer-reviewed or expert-validated
- Includes methodology or reasoning
- Matches observed behavior/testing

## Key Principles

- **Explicit uncertainty**: Always state confidence level
- **Source transparency**: Cite sources with quality ratings
- **Contradiction awareness**: Flag disagreements, don't hide them
- **Calibration**: Track accuracy to improve future scoring
- **Epistemic humility**: "I don't know" is a valid answer
- **Recency weighting**: Recent sources > older for evolving topics
