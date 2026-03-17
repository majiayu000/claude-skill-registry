---
name: olympia-status
description: Get Project Olympia status update and M&A due diligence progress
user-invocable: true
---

You are helping executive leadership get a status update on Project Olympia (M&A due diligence).

Follow these steps:

### Step 1: Gather Context

Ask the user what aspect of Project Olympia they want to review:
- **Overall status** — where are we in the process?
- **Financial modeling** — forward model and valuation status
- **Due diligence** — data room, findings, open items
- **Timeline** — milestones and deadlines

### Step 2: Delegate to Managing Director

Use the `managing-director` agent to coordinate the status update. The managing-director will:
- Summarize current phase and progress
- Identify blockers or risks
- Report on workstream status (historical financials, forward model, growth drivers)

### Step 3: Financial Detail

If the user needs financial details, delegate to the `financial-modeler` agent for:
- Current state of the financial model
- Key assumptions and sensitivities
- Valuation ranges and methodology

### Step 4: Present Status

Format as an executive status update:
- **Phase**: Current phase of the M&A process
- **Progress**: % complete by workstream
- **Key Findings**: Top insights from due diligence
- **Risks**: Open items and risks requiring attention
- **Next Steps**: Upcoming milestones and actions
- **Timeline**: Target dates for key milestones

### Step 5: Follow-Up

Offer:
- **Deeper dive** into a specific workstream
- **Executive summary** — `/jf-executive-suite:executive-summary` for full business metrics
- **Scenario modeling** — `/jf-executive-suite:scenario-model`

### Error Handling

- If Project Olympia data is not available, note that this is an agent-driven skill and does not require Snowflake
- If specific workstream agents are not available, provide the best summary possible from available information
