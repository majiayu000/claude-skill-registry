---
name: cs-prep
description: Use when preparing customer success materials (QBR briefs) - synthesizes customer-specific meeting history, extracts signals, quotes, and pain points for strategic discussions
---

# CS Prep

## Purpose

Compile customer context for QBR or strategic CS meetings:
- Customer-specific meeting history
- Signal synthesis (asks, problems, wins)
- Key quotes and testimonials
- Pain points and friction areas
- Feature request timeline

## When to Use

Activate when:
- User invokes `/project:cs-prep`
- Preparing for QBR
- Customer check-in planning

## Workflow

### 1. Determine Customer and Time Window

**Inputs:**
- `customer`: Customer name (required)
- `days`: Lookback window (default: 90 for QBRs)

### 2. Synthesize Customer Meetings

**Invoke:** `meeting-synthesis` skill

**Inputs:**
- include_customers: {specified customer only}
- Time window: {days}
- No thresholds (include all signals for this customer)

**Outputs:**
- All signals from this customer
- Chronological meeting list
- Verbatim quotes

### 3. Organize by Category

**Group signals:**
- **Wins**: Positive feedback, success stories
- **Pain Points**: Friction, challenges, blockers
- **Feature Requests**: Asks for new capabilities
- **Onboarding/Setup**: Implementation challenges
- **Performance/Scale**: Technical concerns

### 4. Extract Key Quotes

**For each category:**
- Select 2-3 most impactful quotes
- Include speaker, date, context

### 5. Build Timeline

**Feature request timeline:**
```
2025-08-15: Requested Google Sheets export
2025-09-02: Asked about real-time sync
2025-10-10: Followed up on export feature
```

### 6. Generate CS Brief

**Output:** `datasets/product/customer-briefs/{Customer}_{YYYYMMDD}_qbr.md`

**Format:**
```markdown
# QBR Brief: {Customer}

**Date**: {YYYY-MM-DD}
**Time Window**: Last {N} days
**Meetings Reviewed**: {N}

## Wins
- {Quote/signal 1}
- {Quote/signal 2}

## Pain Points
- {Quote/signal 1}
- {Quote/signal 2}

## Feature Requests
- {Request 1} (mentioned {N} times)
- {Request 2} (mentioned {N} times)

## Timeline of Key Events
- {Date}: {Event}
- {Date}: {Event}

## Recommended Discussion Topics
1. {Topic 1}
2. {Topic 2}
```

## Success Criteria

- Customer-specific signals synthesized
- Quotes extracted and categorized
- Timeline of requests built
- CS brief written to customer-briefs/

## Related Skills

- `meeting-synthesis`: Extracts customer signals
- `product-planning`: Uses similar synthesis logic
