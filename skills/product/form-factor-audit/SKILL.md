---
name: form-factor-audit
description: "Evaluate which product form factors will create the most leverage: mobile app, Slack app, GitHub app, or browser extension. Use when deciding how an application should surface, notify, or automate work."
---

# Form Factor Audit

Choose the smallest form factor that maximizes user pull, workflow fit, and automation leverage.

## Purpose

Evaluate which form factors (mobile, Slack app, GitHub app, browser extension) would materially benefit an application, then recommend a prioritized path.

## Assessment Criteria by Form Factor

Score each criterion 0-3 using the rubric below.

### Mobile

- Offline needs: meaningful value without network.
- Push notifications: time-sensitive or habit loops.
- Device features: camera, GPS, biometrics, sensors.
- Gesture UI: fast capture, swipes, or mobile-first ergonomics.

### Slack App

- Team notifications: shared awareness beats email.
- Commands: slash commands or quick actions reduce context switching.
- Workflows: multi-step team flows run inside Slack.
- Approval flows: clear yes/no decisions in-channel.

### GitHub App

- PR automation: status checks, labeling, backports, or merges.
- Issue management: triage, routing, or synchronization with other systems.
- Code review: review assignment, summaries, or policy enforcement.

### Browser Extension

- Page augmentation: UI overlays, side panels, or inline helpers.
- Productivity: reduce copy/paste and tab churn.
- Data extraction: scrape, structure, or export on-page data.

## Scoring Rubric (0-3)

Use the same scale for every criterion.

- 0: Not relevant. No real user value.
- 1: Weak signal. Occasional value, not core.
- 2: Strong signal. Regular value in key flows.
- 3: Critical. Core to product success or differentiation.

## Output Format

Return prioritized recommendations with short rationale and complexity estimates.

Complexity scale:
- Low: narrow surface, few integrations, low risk.
- Medium: multiple surfaces or integrations, moderate risk.
- High: deep integrations, policy/compliance risk, or heavy UX lift.

Recommended structure:

```md
# Form Factor Audit — <App Name>

## Scores
- Mobile: <total>/12
- Slack: <total>/12
- GitHub: <total>/9
- Browser Extension: <total>/9

## Recommendations (Priority Order)
1. <Form Factor> — Complexity: <Low|Medium|High>
   Rationale: <2-3 short statements tied to high-scoring criteria>
   First slice: <smallest shippable surface>
2. ...

## Notes and Risks
- <key dependency, constraint, or open question>
```

## Example Audit Output

```md
# Form Factor Audit — PR Triage Assistant

## Scores
- Mobile: 2/12
- Slack: 10/12
- GitHub: 8/9
- Browser Extension: 3/9

## Recommendations (Priority Order)
1. GitHub App — Complexity: Medium
   Rationale:
   PR automation is core (3/3). Code review support is core (3/3). Issue management useful but secondary (2/3).
   First slice: status check + auto-label + reviewer suggestion bot.
2. Slack App — Complexity: Medium
   Rationale:
   Team notifications high leverage (3/3). Approval flows strong fit (3/3).
   First slice: daily digest + approve/deny buttons for risky PRs.

## Notes and Risks
- Needs GitHub App permissions design early.
- Slack notifications must be configurable to avoid spam.
```

## Decision Tree (Text Flowchart)

```text
Start
 |
 +-- Does value depend on code, PRs, or issues?
 |    |
 |    +-- Yes --> GitHub App likely primary.
 |    |
 |    +-- No --> continue
 |
 +-- Does value depend on team coordination or approvals?
 |    |
 |    +-- Yes --> Slack App likely primary.
 |    |
 |    +-- No --> continue
 |
 +-- Does value depend on web pages users already visit?
 |    |
 |    +-- Yes --> Browser Extension likely primary.
 |    |
 |    +-- No --> continue
 |
 +-- Does value depend on mobile context, push, offline, or sensors?
      |
      +-- Yes --> Mobile likely primary.
      |
      +-- No --> Prefer web app first; revisit after traction.
```
