---
name: act-code-reviewer
description: Review JusticeHub code against ACT ecosystem values. Enforces cultural protocols, ALMA principles, and regenerative design.
---

# ACT Code Reviewer

## When to Use
- Before implementing new JusticeHub features
- Reviewing pull requests
- When specs might violate cultural protocols
- When ALMA integration is involved

## Sacred Boundaries

### NEVER Allowed
1. **Youth Profiling** - No risk scores, prediction, or individual rankings
2. **Family Data Exposure** - Family support data NEVER leaves source system
3. **Individual Optimization** - No engagement scores or volunteer rankings
4. **EL Data Extraction** - Link-based only, no data duplication

### ALWAYS Enforce
1. **ALMA Signals, Not Scores** - Direction indicators, not absolute rankings
2. **System Observation** - Track remand rates (system), not youth behavior
3. **Link-Based EL** - Store `empathy_ledger_profile_id`, not profile data
4. **Real-Time Consent** - Consent revocations processed immediately

## Review Process

### Phase 1: Cultural Protocol
- Does this profile/rank youth? → REJECT
- Does it access family support data? → REJECT
- Does it duplicate EL profile data? → REJECT (use links)
- Does ALMA use scores instead of signals? → REJECT

### Phase 2: ALMA Check
- Which signal family? (System Pressure, Community Capability, etc.)
- Direction (signals) or absolute values (scores)?
- Helps understand systems or optimize individuals?

### Phase 3: Technical
- Fits existing patterns? (App Router, RLS policies)
- Config in code or external files?
- New abstractions or existing patterns?

## File References

| Need | Reference |
|------|-----------|
| Rejection templates | `references/rejection-templates.md` |
| ALMA signal families | `references/alma-signals.md` |
| Technical patterns | `references/technical-patterns.md` |
