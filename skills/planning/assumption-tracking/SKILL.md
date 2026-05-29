---
name: assumption-tracking
description: Explicit tracking, validation, and failure planning for project assumptions. Reference for managing assumptions throughout project lifecycle.
---

# Assumption Tracking Skill

// Project Autopilot - Assumption Management
// Copyright (c) 2026 Jeremy McSpadden <jeremy@fluxlabs.net>

**Purpose:** Explicitly track assumptions, define validation methods, and create failure plans to handle invalidated assumptions.

---

## Why Assumptions Matter

Assumptions are beliefs about the project that haven't been verified:
- **Valid assumptions** enable confident planning
- **Invalid assumptions** cause cascading failures
- **Untracked assumptions** become silent risks

This skill ensures assumptions are:
1. **Explicitly stated** - No hidden assumptions
2. **Categorized** - Technical, business, or external
3. **Validated** - With clear criteria
4. **Planned for failure** - With mitigation and fallback

---

## Assumption Categories

### Technical Assumptions
Beliefs about technical capabilities:
- API availability and behavior
- Library/framework compatibility
- Performance characteristics
- Infrastructure capabilities
- Data format and structure

### Business Assumptions
Beliefs about requirements and priorities:
- User behavior expectations
- Requirement interpretations
- Priority orderings
- Scope boundaries
- Timeline expectations

### External Assumptions
Beliefs about external factors:
- Third-party service SLAs
- Integration partner readiness
- Timeline dependencies
- Resource availability
- Regulatory compliance

---

## Assumption Template

### YAML Format

```yaml
assumptions:
  - id: A001
    statement: "Supabase rate limits won't affect normal usage"
    category: external
    criticality: high       # high | medium | low
    phase: 3               # Phase where assumption matters
    validation:
      method: "load_test"   # load_test | api_check | manual | code_review
      command: "npm run test:load"
      criteria: "< 10% failures at 100 concurrent users"
      when: "before_phase_3"  # when to validate
    failure_plan:
      impact: "Authentication delays during peak usage"
      mitigation: "Implement request queuing with exponential backoff"
      fallback: "Switch to self-hosted auth service"
      effort: "medium"      # low | medium | high
    status: untested        # untested | validated | invalidated
    validated_at: null
    notes: ""

  - id: A002
    statement: "Next.js 14 App Router supports all required features"
    category: technical
    criticality: medium
    phase: 1
    validation:
      method: "code_review"
      command: null
      criteria: "All planned features have documentation"
      when: "before_planning"
    failure_plan:
      impact: "May need to use Pages Router for some features"
      mitigation: "Identify feature gaps early, plan workarounds"
      fallback: "Fall back to Pages Router or hybrid approach"
      effort: "high"
    status: validated
    validated_at: "2026-01-29"
    notes: "Verified against Next.js 14 docs"

  - id: A003
    statement: "User data model matches existing schema"
    category: business
    criticality: high
    phase: 2
    validation:
      method: "api_check"
      command: "curl -X GET https://api.example.com/users/schema"
      criteria: "Schema includes: id, email, name, created_at"
      when: "before_phase_2"
    failure_plan:
      impact: "Database migration complexity increases"
      mitigation: "Add migration step to transform data"
      fallback: "Create new user entity, migrate data async"
      effort: "high"
    status: untested
    validated_at: null
    notes: ""
```

### Markdown Format

```markdown
## Assumptions

### Phase Assumptions
| ID | Assumption | Category | Criticality | Status |
|----|------------|----------|-------------|--------|
| A001 | Supabase rate limits won't affect normal usage | external | High | Untested |
| A002 | Next.js 14 App Router supports all required features | technical | Medium | Validated |
| A003 | User data model matches existing schema | business | High | Untested |

### Validation Tasks
| Assumption | Method | When | Criteria |
|------------|--------|------|----------|
| A001 | load_test | Before Phase 3 | < 10% failures at 100 users |
| A002 | code_review | Before planning | All features documented |
| A003 | api_check | Before Phase 2 | Schema includes required fields |

### Failure Plans
| Assumption | If Fails | Mitigation | Fallback |
|------------|----------|------------|----------|
| A001 | Auth delays | Request queuing | Self-hosted auth |
| A002 | Feature gaps | Plan workarounds | Pages Router hybrid |
| A003 | Schema mismatch | Migration step | New entity + async migrate |
```

---

## Validation Protocol

### Validation Methods

```
FUNCTION validateAssumption(assumption):
    result = {
        assumption_id: assumption.id,
        passed: false,
        evidence: null,
        error: null,
        validated_at: null
    }

    SWITCH assumption.validation.method:
        CASE "load_test":
            # Run load test
            output = runCommand(assumption.validation.command)
            result.passed = evaluateCriteria(output, assumption.validation.criteria)
            result.evidence = {
                type: "load_test",
                output: output,
                metrics: parseLoadTestMetrics(output)
            }

        CASE "api_check":
            # Check API endpoint
            IF assumption.validation.command:
                output = runCommand(assumption.validation.command)
            ELSE:
                output = fetchAPI(assumption.validation.endpoint)
            result.passed = evaluateCriteria(output, assumption.validation.criteria)
            result.evidence = {
                type: "api_check",
                response: output
            }

        CASE "manual":
            # Request manual verification
            LOG "Manual verification required for: {assumption.statement}"
            user_response = requestManualVerification(assumption)
            result.passed = user_response.confirmed
            result.evidence = {
                type: "manual",
                verified_by: user_response.user,
                notes: user_response.notes
            }

        CASE "code_review":
            # Analyze code or documentation
            LOG "Code review required for: {assumption.statement}"
            review_result = performCodeReview(assumption.validation.criteria)
            result.passed = review_result.meets_criteria
            result.evidence = {
                type: "code_review",
                findings: review_result.findings
            }

    IF result.passed:
        assumption.status = "validated"
        assumption.validated_at = now()
        LOG "✅ Assumption {assumption.id} VALIDATED"
    ELSE:
        assumption.status = "invalidated"
        LOG "❌ Assumption {assumption.id} INVALIDATED"
        activateFailurePlan(assumption.failure_plan)

    RETURN result
```

### Automatic Validation Triggers

```yaml
validation_triggers:
  - when: "before_planning"
    validate:
      - assumptions WHERE criticality == "high" AND phase == null

  - when: "before_phase"
    validate:
      - assumptions WHERE phase == current_phase AND status == "untested"

  - when: "phase_complete"
    validate:
      - assumptions WHERE phase == current_phase AND status == "untested"

  - when: "on_demand"
    validate:
      - assumption specified by user
```

---

## Failure Plan Activation

### When Assumption Invalidated

```
FUNCTION activateFailurePlan(failure_plan):
    LOG "⚠️ Activating failure plan"
    LOG "Impact: {failure_plan.impact}"
    LOG "Mitigation: {failure_plan.mitigation}"

    # Create mitigation task
    task = {
        type: "assumption_failure",
        title: "Mitigate invalidated assumption",
        description: failure_plan.mitigation,
        priority: "high",
        effort: failure_plan.effort,
        blocks: getAffectedPhases(assumption)
    }

    addTask(task)

    # If mitigation fails, fallback
    IF mitigationFails():
        LOG "⚠️ Mitigation failed, activating fallback"
        LOG "Fallback: {failure_plan.fallback}"

        fallback_task = {
            type: "assumption_fallback",
            title: "Implement fallback for assumption failure",
            description: failure_plan.fallback,
            priority: "critical"
        }

        addTask(fallback_task)
```

### Failure Plan Impact Assessment

```
FUNCTION assessFailurePlanImpact(assumption):
    impact = {
        affected_phases: [],
        affected_tasks: [],
        scope_change: false,
        timeline_impact: "unknown"
    }

    # Find affected phases
    FOR each phase IN project.phases:
        IF phase.depends_on_assumption(assumption.id):
            impact.affected_phases.add(phase.number)
            impact.affected_tasks.extend(phase.tasks)

    # Determine if scope change needed
    IF assumption.failure_plan.effort == "high":
        impact.scope_change = true
        impact.timeline_impact = "significant"
    ELSE IF assumption.failure_plan.effort == "medium":
        impact.timeline_impact = "moderate"
    ELSE:
        impact.timeline_impact = "minimal"

    RETURN impact
```

---

## Assumption Tracking in Phases

### Phase Template Addition

Add to each phase file:

```markdown
## Assumptions

### Phase Assumptions
| ID | Assumption | Criticality | Status |
|----|------------|-------------|--------|
| A001 | {statement} | High | Untested |
| A002 | {statement} | Medium | Validated |

### Validation Schedule
| Assumption | Method | When | Criteria |
|------------|--------|------|----------|
| A001 | load_test | Before Phase 3 | < 10% failures |
| A002 | api_check | Phase start | Schema match |

### Failure Plans
| Assumption | If Fails | Mitigation | Fallback |
|------------|----------|------------|----------|
| A001 | Auth delays | Request queuing | Self-hosted |
| A002 | Schema mismatch | Migration step | New entity |
```

### Assumption Status Tracking

```yaml
# In phase file or .autopilot/assumptions.yaml
assumptions_status:
  - id: A001
    status: validated
    validated_at: "2026-01-29T10:30:00Z"
    evidence: "Load test passed with 3% failure rate"

  - id: A002
    status: invalidated
    validated_at: "2026-01-29T11:00:00Z"
    evidence: "Schema missing required fields"
    mitigation_status: in_progress
```

---

## Integration Points

### With /autopilot:plan

```
plan.md reads:
    - assumptions WHERE phase == current_phase
    - Creates validation tasks
    - Adds assumption checks to phase quality gate
```

### With /autopilot:takeoff

```
build.md executes:
    - IF untested assumptions for current phase:
        FIRST validate assumptions
        IF any invalidated:
            Pause and show failure plan
            Wait for user decision
```

### With /autopilot:scan

```
scan.md includes:
    - List all assumptions
    - Show validation status
    - Flag invalidated assumptions
    - Suggest validation schedule
```

### With /autopilot:cockpit

```
resume.md loads:
    - Assumption status from previous session
    - Continues with validation state preserved
```

---

## Commands

### List Assumptions

```bash
/autopilot:assumptions list
/autopilot:assumptions list --phase=3
/autopilot:assumptions list --status=untested
```

### Validate Assumption

```bash
/autopilot:assumptions validate A001
/autopilot:assumptions validate --phase=3
/autopilot:assumptions validate --all
```

### Update Assumption Status

```bash
/autopilot:assumptions mark A001 --status=validated
/autopilot:assumptions mark A001 --status=invalidated
```

---

## Output Format

### Assumption Validation Report

```markdown
## Assumption Validation Report

**Phase:** 3 - User Dashboard
**Validated:** 2026-01-29

### Summary
| Status | Count |
|--------|-------|
| Validated | 2 |
| Invalidated | 1 |
| Untested | 1 |

### Results

#### ✅ A001: Supabase rate limits
**Status:** Validated
**Method:** load_test
**Evidence:** 3% failure rate at 100 concurrent users (criteria: <10%)

#### ✅ A002: Next.js 14 features
**Status:** Validated
**Method:** code_review
**Evidence:** All required features documented

#### ❌ A003: User schema match
**Status:** Invalidated
**Method:** api_check
**Evidence:** Schema missing `avatar` field

**Failure Plan Activated:**
- Impact: Database migration complexity increases
- Mitigation: Add migration step to transform data
- Fallback: Create new user entity, migrate data async

#### ⏳ A004: Payment gateway latency
**Status:** Untested
**When:** Before Phase 5
```

---

## Best Practices

### Writing Good Assumptions

**DO:**
- Be specific and testable
- Include clear validation criteria
- Define realistic failure plans
- Categorize by type (technical, business, external)
- Assign criticality based on impact

**DON'T:**
- Leave assumptions implicit
- Assume without evidence
- Skip failure planning for critical assumptions
- Wait until failure to consider alternatives

### Validation Timing

| Criticality | When to Validate |
|-------------|------------------|
| High | Before dependent phase starts |
| Medium | During phase planning |
| Low | During phase execution |

### Failure Plan Quality

Good failure plans have:
- Clear impact description
- Specific mitigation steps
- Fallback option that doesn't require the assumption
- Effort estimate
