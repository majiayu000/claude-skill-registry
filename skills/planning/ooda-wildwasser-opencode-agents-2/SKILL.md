---
name: ooda
description: OODA loop decision framework (Observe, Orient, Decide, Act). Use for complex decisions, problem-solving, unclear situations, or when someone is jumping to solutions without analysis.
user-invocable: true
---

# OODA Loop Analysis

Run a complete OODA loop (Observe, Orient, Decide, Execute) on the problem or decision provided.

## Instructions

Work through each phase sequentially. Be thorough but concise.

### Phase 1: OBSERVE
Gather facts before analyzing. Ask: "What is actually happening?"

Output:
- **Current State**: Facts only, no interpretation
- **Signals**: What prompted this inquiry
- **Scope**: Boundaries of the situation
- **Constraints**: Resources, time, rules, dependencies
- **Unknowns**: Information gaps to acknowledge

### Phase 2: ORIENT
Analyze and build understanding. Ask: "Why is this happening?"

Output:
- **Root Cause Analysis**: Underlying drivers, not just symptoms
- **Mental Models**: Frameworks that apply (first principles, inversion, second-order effects, etc.)
- **Patterns**: Similar situations and their outcomes
- **Stakeholder Views**: How different parties see this
- **Assumptions**: What we're taking for granted
- **Biases**: Cognitive traps to watch for

### Phase 3: DECIDE
Choose from viable options. Ask: "What's the best approach?"

Output:
- **Options** (minimum 3):
  - Option A — Pros / Cons / Risk level
  - Option B — Pros / Cons / Risk level
  - Option C — Pros / Cons / Risk level
- **Recommendation**: Selected approach with rationale
- **Success Criteria**: How we'll know it worked
- **Contingency**: Fallback if primary approach fails

### Phase 4: EXECUTE
Plan implementation with verification. Ask: "How do we act and confirm?"

Output:
- **Action Steps**: Ordered, concrete steps
- **Verification Points**: How to check progress at each stage
- **Timeline**: Realistic schedule
- **First Action**: The immediate next step

### Feedback Loop
End with:
- **Key Risks**: What could derail this
- **Review Trigger**: When to reassess (time or event based)

## Format

Use clear headers for each phase. Be direct and actionable. Avoid fluff.

## Examples

### Business: Product Launch Timing

**Context**: Feature 85% complete, competitor launching similar feature next month.

**OBSERVE**: Core functionality works; edge cases unhandled. Competitor announced similar launch. 3 engineers available; Q4 revenue targets looming.

**ORIENT**: Root tension is first-mover advantage vs. quality reputation. Last rushed launch caused 3-month support burden. Sales wants it now; Support worried; Engineering wants 2 more weeks.

**DECIDE**: Options evaluated—Launch now (high risk), Delay 4 weeks (medium), Soft launch to 10 customers (low risk). Selected: Soft launch → gather feedback → full launch in 3 weeks.

**EXECUTE**: Identify 10 beta customers (2 days) → Deploy with feature flag (1 day) → Monitor 2 weeks → Full launch with case studies.

### Personal: Job Offer Decision

**Context**: 3 years at current company, plateaued. Offer is 30% raise, bigger scope, requires travel.

**OBSERVE**: Current role comfortable but stagnant. New role offers growth but spouse's job isn't portable; young child at home.

**ORIENT**: Root feeling is being undervalued + seeking growth. Models: Regret minimization; total compensation (salary + learning + relationships).

**DECIDE**: Selected transparent conversation with current manager + gather more info on new role before deciding.

**EXECUTE**: List non-negotiables → Career conversation with manager → Talk to future team → 48-hour reflection before final decision.

$ARGUMENTS
