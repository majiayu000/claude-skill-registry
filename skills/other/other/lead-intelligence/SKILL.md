---
name: lead-intelligence
description: Advanced lead qualification and analysis using the EnterpriseHub GHL integration and predictive intelligence tools.
---

# Lead Intelligence Skill

Use this skill to perform deep lead qualification, property research, and predictive analysis for Jorge Salas' real estate business.

## Core Capabilities

1. **Public Records Research**: Use `get_public_records` to fetch property details.
2. **Predictive Analytics**: Use `detect_life_event_triggers` and `predict_propensity_to_sell` to identify high-intent leads.
3. **Lead Scoring Framework**: Apply the 28-feature pipeline logic to categorize leads.

## Lead Scoring Guidelines (28-Feature Pipeline)

When analyzing a lead, evaluate these core factors:

### 1. Budget Qualification (25%)
- Stated budget vs. market reality.
- Pre-approval status.
- Down payment availability.

### 2. Timeline Urgency (20%)
- Stated timeline to purchase/sell.
- Current housing situation.
- Market timing awareness.

### 3. Engagement Level (20%)
- Response rate to communications.
- Website interaction patterns (if available via CRM).
- Property viewing requests.

### 4. Geographic Focus (15%)
- Preferred area specificity.
- Realistic area expectations.

### 5. Behavioral Indicators (20%)
- Communication style and tone.
- Question quality and specificity.

## Scoring Grades

- **A-Grade (9-10)**: Hot leads ready to transact.
- **B-Grade (7-8)**: Warm leads needing nurturing.
- **C-Grade (5-6)**: Qualified prospects with longer timeline.
- **D-Grade (3-4)**: Requires significant qualification.
- **F-Grade (1-2)**: Not qualified or likely unviable.

## Workflow Integration

- Use the `enterprise-hub` MCP tools to fetch live data.
- Store results in the `PostgreSQL` database for long-term tracking.
- Update the `active-session.md` when a significant lead milestone is reached.
