---
name: premortem
description: "Identify failure modes before they occur. Use when reviewing plans, designs, or PRs to catch risks early. Not for post-incident analysis or debugging active issues."
user-invocable: true
---

# Pre-Mortem

<mission_control>
<objective>Identify failure modes before they occur by systematically questioning plans, designs, and implementations with verified evidence requirements</objective>
<success_criteria>Risks categorized (Tiger/Paper/Elephant) with specific verification evidence, HIGH severity risks addressed before proceeding</success_criteria>
</mission_control>

<trigger>When reviewing plans, designs, or PRs to catch risks early. Not for: Post-incident analysis or debugging active issues.</trigger>

<interaction_schema>
DETECT_CONTEXT → RUN_CHECKLIST → VERIFY_FINDINGS → PRESENT_RISKS → UPDATE_PLAN
</interaction_schema>

Identify failure modes before they occur by systematically questioning plans, designs, and implementations. Based on Gary Klein's technique, popularized by Shreyas Doshi (Stripe).

## Core Concept

> "Imagine it's 3 months from now and this project has failed spectacularly. Why did it fail?"

## Risk Categories

| Category        | Symbol       | Meaning                                         |
| --------------- | ------------ | ----------------------------------------------- |
| **Tiger**       | `[TIGER]`    | Clear threat that will hurt us if not addressed |
| **Paper Tiger** | `[PAPER]`    | Looks threatening but probably fine             |
| **Elephant**    | `[ELEPHANT]` | Thing nobody wants to talk about                |

## CRITICAL: Verify Before Flagging

**Do NOT flag risks based on pattern-matching alone.** Every potential tiger MUST go through verification.

### The False Positive Problem

Common mistakes that create false tigers:

- Seeing a hardcoded path without checking for `if exists():` fallback
- Finding missing feature X without asking "is X in scope?"
- Flagging code at line N without reading lines N±20 for context
- Assuming error case isn't handled without tracing the code

### Verification Checklist (REQUIRED)

Before flagging ANY tiger, verify:

1. **Context read**: Did I read ±20 lines around the finding?
2. **Fallback check**: Is there try/except, if exists(), or else branch?
3. **Scope check**: Is this even in scope for this code?
4. **Dev-only check**: Is this in **main**, tests/, or dev-only code?

**If ANY verification check is "no" or "unknown", DO NOT flag as tiger.**

### Required Evidence Format

Every tiger MUST include:

```yaml
risk: "<description>"
location: "file.py:42"
severity: high|medium
mitigation_checked: "<what was checked and NOT found>" # REQUIRED
```

If you cannot fill in `mitigation_checked` with specific evidence, it's not a verified tiger.

## Workflow

### Step 1: Detect Context & Depth

Auto-detect based on context:

- **Plan creation** → Quick (localized scope)
- **Before implementation** → Deep (global scope)
- **PR review** → Quick (localized scope)
- **Otherwise** → Ask user

### Step 2: Run Appropriate Checklist

#### Quick Checklist (Plans, PRs)

Run through these mentally, note any that apply:

**Core Questions:**

1. What's the single biggest thing that could go wrong?
2. Any external dependencies that could fail?
3. Is rollback possible if this breaks?
4. Edge cases not covered in tests?
5. Unclear requirements that could cause rework?

**Output Format:**

```yaml
mode: quick
context: "<plan/PR being analyzed>"

potential_risks: # Pass 1: Pattern-matching findings
  - "hardcoded path at line 42"
  - "missing error handling for X"

tigers: # Pass 2: After verification
  - risk: "<description>"
    location: "file.py:42"
    severity: high|medium
    category: dependency|integration|requirements|testing
    mitigation_checked: "<what was NOT found>"

elephants:
  - risk: "<unspoken concern>"
    severity: medium

paper_tigers:
  - risk: "<looks scary but ok>"
    reason: "<why it's fine - what mitigation EXISTS>"
```

#### Deep Checklist (Before Implementation)

Work through each category systematically:

**Technical Risks:**

- [ ] Scalability: Works at 10x/100x current load?
- [ ] Dependencies: External services + fallbacks defined?
- [ ] Data: Availability, consistency, migrations clear?
- [ ] Latency: SLA requirements will be met?
- [ ] Security: Auth, injection, OWASP considered?
- [ ] Error handling: All failure modes covered?

**Integration Risks:**

- [ ] Breaking changes identified?
- [ ] Migration path defined?
- [ ] Rollback strategy exists?
- [ ] Feature flags needed?

**Process Risks:**

- [ ] Requirements clear and complete?
- [ ] All stakeholder input gathered?
- [ ] Tech debt being tracked?
- [ ] Maintenance burden understood?

**Testing Risks:**

- [ ] Coverage gaps identified?
- [ ] Integration test plan exists?
- [ ] Load testing needed?
- [ ] Manual testing plan defined?

### Step 3: Present Risks via AskUserQuestion

**BLOCKING:** Present findings and require user decision on HIGH severity tigers.

Build the question with these options:

1. **Accept risks and proceed** - Acknowledged but not blocking
2. **Add mitigations to plan** - Update plan with risk mitigations before proceeding
3. **Research mitigation options** - Help find solutions for unknown mitigations
4. **Discuss specific risks** - Talk through particular concerns

### Step 4: Handle User Response

#### If "Accept risks and proceed"

Log acceptance for audit trail and continue to next workflow step.

#### If "Add mitigations to plan"

Update plan file with mitigations section, then re-run quick premortem to verify mitigations address risks.

#### If "Research mitigation options"

For each HIGH severity tiger:

1. Internal: Use Read/Grep to find how codebase handled this before
2. External: Use WebSearch for best practices
3. Synthesize 2-4 options
4. Present via AskUserQuestion

#### If "Discuss specific risks"

Ask which risk to discuss, then have conversation about that specific risk.

### Step 5: Update Plan (if mitigations added)

Append to the plan:

```markdown
## Risk Mitigations (Pre-Mortem)

### Tigers Addressed:

1. **{risk}** (severity: {severity})
   - Mitigation: {mitigation}
   - Added to phase: {phase_number}

### Accepted Risks:

1. **{risk}** - Accepted because: {reason}

### Pre-Mortem Run:

- Date: {timestamp}
- Mode: {quick|deep}
- Tigers: {count}
- Elephants: {count}
```

## Severity Thresholds

| Severity | Blocking? | Action Required                   |
| -------- | --------- | --------------------------------- |
| HIGH     | Yes       | Must address or explicitly accept |
| MEDIUM   | No        | Inform user, recommend addressing |
| LOW      | No        | Note for awareness                |

## Example Session

```
Running deep pre-mortem on API rate limiting plan...

Pre-mortem complete. Found 2 tigers, 1 elephant:

TIGERS:
1. [HIGH] No circuit breaker for external payment API
   - Category: dependency
   - If payment API is slow/down, requests will pile up
   - mitigation_checked: "No timeout, no retries, no circuit breaker pattern"

2. [HIGH] No rollback strategy defined
   - Category: integration
   - If rate limiting breaks auth flow, no quick fix path

ELEPHANTS:
1. [MEDIUM] Team hasn't used Redis before
   - We're introducing Redis for rate limit counters

PAPER TIGERS:
1. Database migration size - Only adds one index, <1s migration
```

## Integration Points

### In Planning Workflows

After plan structure is approved:

1. Run quick premortem
2. If HIGH risks found, block until addressed
3. If only MEDIUM/LOW, inform and proceed

### Before Implementation

Run deep premortem on full plan:

1. Block until all HIGH tigers addressed
2. Update plan with mitigations

### In Code Review

Run quick premortem on diff scope:

1. Inform of any risks found
2. Suggest mitigations if applicable

## References

- [Pre-Mortems by Shreyas Doshi](https://coda.io/@shreyas/pre-mortems)
- [Gary Klein's Original Research](https://hbr.org/2007/09/performing-a-project-premortem)

---

<critical_constraint>
MANDATORY: Verify every tiger with specific evidence before flagging
MANDATORY: Use required YAML format with mitigation_checked field
MANDATORY: Read ±20 lines around any finding for context
MANDATORY: Block on HIGH severity risks until user addresses them
MANDATORY: Never flag risks based on pattern-matching alone
No exceptions. Unverified tigers waste time and undermine credibility.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
