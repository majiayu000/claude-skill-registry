---
name: moderation-guidelines
description: Community moderation, code of conduct enforcement, and conflict resolution
sasmp_version: "1.4.0"
version: "2.0.0"
updated: "2025-01"
bonded_agent: 02-community-builder
bond_type: SECONDARY_BOND
---

# Community Moderation

Implement **fair, consistent moderation** that keeps communities healthy and inclusive.

## Skill Contract

### Parameters
```yaml
parameters:
  required:
    - action_type: enum[review, warn, remove, ban, appeal]
    - incident_context: string
  optional:
    - severity: enum[minor, moderate, serious, severe]
    - prior_violations: integer
```

### Output
```yaml
output:
  moderation_action:
    decision: enum[no_action, warning, removal, ban]
    rationale: string
    communication: string
```

## Code of Conduct

### Core Principles
```
1. Be respectful and inclusive
2. No harassment, discrimination, or hate speech
3. Keep discussions constructive
4. Respect privacy and confidentiality
5. Follow platform rules
```

### Enforcement Ladder

| Level | Violation | Action | Record |
|-------|-----------|--------|--------|
| 1 | Minor (off-topic) | Friendly reminder | 30 days |
| 2 | Moderate (rude) | Warning + delete | 90 days |
| 3 | Serious (harassment) | Temp ban (1-7d) | 1 year |
| 4 | Severe (threats) | Permanent ban | Forever |

## Moderation Workflow

```
Report → Review → Decide → Act → Document → Follow-up
   ↓        ↓        ↓       ↓        ↓          ↓
 Flag    Context  Policy   Remove   Log      Appeal
 System  Check    Apply    Warn     Event    Process
```

## Conflict Resolution

### De-escalation Steps
1. **Acknowledge**: "I understand you're frustrated"
2. **Separate**: Move to private channel if needed
3. **Listen**: Let both parties share
4. **Find Common Ground**: Focus on shared goals
5. **Resolve**: Propose fair solution

### Difficult Situations

| Situation | Approach | Escalation |
|-----------|----------|------------|
| Heated debate | Cool off period | Community manager |
| Repeated offender | Clear warning | Ban review |
| Doxxing/threats | Immediate ban | Legal team |
| Gray area | Team discussion | Policy update |

## Moderation Team Roles

- **Community Manager**: Strategy, escalations
- **Senior Moderators**: Complex cases
- **Moderators**: Day-to-day enforcement
- **Champions**: Limited powers

## Retry Logic

```yaml
retry_patterns:
  unclear_violation:
    strategy: "Consult with another moderator"
    escalation: "Team vote on action"

  member_dispute:
    strategy: "Private mediation session"
    fallback: "Both parties warned"

  appeal_received:
    strategy: "Different moderator reviews"
```

## Failure Modes & Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| Inconsistent enforcement | Complaints | Audit, recalibrate |
| False positive ban | Appeal success | Apologize, restore |
| Mod burnout | Slow responses | Rotate, recruit |

## Debug Checklist

```
□ Violation matches CoC section?
□ Context fully understood?
□ Prior history reviewed?
□ Consistent with past cases?
□ Action proportionate?
□ Communication respectful?
□ Documentation complete?
□ Appeal path explained?
```

## Test Template

```yaml
test_moderation:
  unit_tests:
    - test_violation_classification:
        assert: "Correct severity level"
    - test_response_time:
        assert: "Reviewed within 4 hours"

  integration_tests:
    - test_appeal_process:
        assert: "Different reviewer, 72h decision"
```

## Observability

```yaml
metrics:
  - reports_per_week: integer
  - resolution_time_avg: duration
  - appeal_rate: float
  - overturn_rate: float
```

See `assets/` for code of conduct templates.
