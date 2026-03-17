---
name: messaging-audit
description: Review positioning and messaging across content
role_groups: [marketing, product, leadership]
jtbd: |
  Your messaging drifts over time as different people write content. This scans 
  05-Areas/Content/, checks consistency across materials, identifies conflicts or gaps, 
  and suggests refinements so your positioning stays tight and consistent.
time_investment: "15-20 minutes per audit"
---

## Purpose

Ensure messaging consistency across all content and identify where positioning needs tightening.

## Usage

- `/messaging-audit` - Full messaging review
- `/messaging-audit [topic]` - Focus on specific product/feature messaging

---

## Steps

1. **Scan 05-Areas/Content/** for published content
2. **Extract messaging elements:**
   - Value propositions mentioned
   - Key benefits highlighted
   - Target audience descriptions
   - Problem statements
   - Competitive positioning

3. **Check consistency:**
   - Same value props across content?
   - Consistent problem framing?
   - Aligned audience descriptions?
   - Unified competitive positioning?

4. **Identify issues:**
   - Conflicting messages
   - Outdated positioning
   - Missing key messages
   - Inconsistent terminology

5. **Generate audit report with:**
   - Consistency analysis
   - Conflicts found
   - Missing messages
   - Recommendations for alignment

---

## Output Format

```markdown
# 🎯 Messaging Audit

**Date:** [Today]
**Content reviewed:** [Count]

## Current Messaging Patterns

### Value Propositions
- "[Value prop 1]" - Used in [X] pieces
- "[Value prop 2]" - Used in [X] pieces

### Problem Statements
- "[Problem 1]" - [X] mentions
- "[Problem 2]" - [X] mentions

## Consistency Issues

### Conflicts Found
1. [Content A] says "[X]" but [Content B] says "[Y]"
2. [Inconsistency description]

### Missing Key Messages
- [Message] not mentioned in [content type]

## Recommendations
1. [Recommendation for alignment]
2. [Recommendation for improvement]
```
