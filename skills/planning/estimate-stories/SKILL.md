---
name: estimate-stories
description: Calculate story point estimates for user stories using structured formula (Complexity × Effort + Risk). Analyzes acceptance criteria, assesses complexity (1-5), effort (1-5), and risk (0-3), then documents estimation rationale. Use during backlog grooming or sprint planning when stories need sizing.
acceptance:
  - story_loaded: "Story file successfully loaded with acceptance criteria"
  - complexity_assessed: "Complexity score (1-5) calculated with detailed rationale based on technical difficulty"
  - effort_assessed: "Effort score (1-5) calculated with rationale based on work volume"
  - risk_assessed: "Risk adjustment (0-3) calculated with rationale based on unknowns"
  - story_points_calculated: "Story points calculated using formula: (Complexity × Effort) + Risk"
  - estimation_documented: "Estimation block added to story file with formula, breakdown, and assumptions"
inputs:
  story_id:
    type: string
    required: true
    description: "Story identifier (e.g., 'story-auth-001')"
    validation: "Must match pattern: story-{component}-{number}-{slug}"
  story_file:
    type: string
    required: true
    description: "Path to story markdown file"
  batch_mode:
    type: boolean
    required: false
    description: "Whether estimating multiple stories (for consistency checks)"
    default: false
  config_file:
    type: string
    required: false
    description: "Path to config with velocity baseline (defaults to .claude/config.yaml)"
outputs:
  story_points:
    type: number
    description: "Calculated story points using formula"
  complexity_score:
    type: number
    description: "Complexity assessment (1-5 scale)"
  effort_score:
    type: number
    description: "Effort assessment (1-5 scale)"
  risk_score:
    type: number
    description: "Risk adjustment (0-3 scale)"
  confidence_level:
    type: string
    description: "Estimation confidence (high/medium/low based on clarity and familiarity)"
  estimation_added:
    type: boolean
    description: "Whether estimation block was added to story file"
  split_recommended:
    type: boolean
    description: "Whether story should be split (true if >13 points)"
telemetry:
  emit: "skill.estimate-stories.completed"
  track:
    - story_id
    - story_points
    - complexity_score
    - effort_score
    - risk_score
    - confidence_level
    - split_recommended
    - batch_mode
    - duration_ms
---

# Estimate Stories Skill

## Purpose

Estimate story points for user stories using a structured, evidence-based formula: **Story Points = (Complexity × Effort) + Risk**

This provides consistent estimations that help with sprint planning, velocity tracking, and story comparison.

**Core Principle:** Estimation is not guessing—it's structured analysis of complexity, effort, and risk based on acceptance criteria and technical context.

## Prerequisites

- Story file exists in `.claude/stories/` directory
- Story has clear acceptance criteria
- Understanding of project tech stack
- Access to historical velocity data (optional)

---

## Workflow

### 1. Load Story Context

**Read story file** to understand:
- User story narrative (As a... I want... So that...)
- Acceptance criteria (what needs to be implemented)
- Dependencies and technical notes
- Current priority level

**Load project context:**
- Team velocity baseline (from `.claude/config.yaml`)
- Tech stack and known patterns
- Historical estimation data (if available)

**Example story:**
```markdown
**User Story:** As a new user, I want to create an account with email/password

**Acceptance Criteria:**
- AC-1: User can enter email and password on signup form
- AC-2: Email validated with Zod
- AC-3: Password hashed with bcrypt
- AC-4: Duplicate emails rejected with 409
- AC-5: Success returns JWT token
- AC-6: User record saved to PostgreSQL
```

---

### 2. Analyze Complexity (1-5 Scale)

**Complexity** measures technical difficulty and cognitive load (NOT time/effort).

**Quick Guide:**
- **1 (Trivial):** Single file, copy-paste from existing, no edge cases
- **2 (Simple):** 2-3 files, existing patterns, minimal edge cases
- **3 (Moderate):** 4-6 files, may need new library, multiple edge cases
- **4 (Complex):** 7-12 files, multiple patterns, many error paths
- **5 (Very Complex):** 12+ files, new architecture, extensive edge cases

**Consider:**
- Number of integration points (APIs, databases, services)
- Error handling paths required
- State management complexity
- Data transformation complexity

**For example story:**
```
Complexity: 3 (Moderate)
- 6 files affected (form, validation, controller, service, model, tests)
- Multiple integration points (DB, JWT, bcrypt)
- Several error paths (validation, duplicates, DB errors)
- Moderate state management
```

**See:** `references/complexity-scale.md` for detailed scale with examples

---

### 3. Analyze Effort (1-5 Scale)

**Effort** measures the volume of work regardless of difficulty.

**Quick Guide:**
- **1 (Minimal):** <1 hour, <50 LOC, 2-3 tests
- **2 (Small):** 1-2 hours, 50-150 LOC, 4-6 tests
- **3 (Medium):** 3-4 hours, 150-300 LOC, 7-10 tests
- **4 (Large):** 5-6 hours, 300-500 LOC, 11-15 tests
- **5 (Very Large):** >6 hours, >500 LOC, 15+ tests

**Consider:**
- Number of acceptance criteria (more AC = more work)
- Lines of code to write
- Number of tests required
- Documentation needs

**For example story:**
```
Effort: 3 (Medium)
- 6 acceptance criteria
- ~250 LOC (controller, service, validation, model)
- ~10 tests (unit + integration)
- 3-4 hours estimated work
```

**See:** `references/effort-scale.md` for detailed scale with examples

---

### 4. Analyze Risk (0-3 Adjustment)

**Risk** is an adjustment factor for unknowns and potential issues.

**Quick Guide:**
- **0:** No significant risks
- **+1:** Minor risks (unfamiliar library, some unknowns)
- **+2:** Moderate risks (new pattern, integration uncertainty)
- **+3:** High risks (new architecture, external dependencies, R&D needed)

**Consider:**
- Team familiarity with required tech
- External dependencies (third-party APIs)
- Requirements clarity (vague requirements = higher risk)
- Performance/security concerns

**For example story:**
```
Risk: +1
- Team familiar with all tech (Zod, bcrypt, JWT, PostgreSQL)
- Requirements clear and testable
- Minor risk: ensuring proper bcrypt cost and JWT security
```

**See:** `references/risk-factors.md` for detailed risk analysis

---

### 5. Calculate Story Points

**Formula:** `Story Points = (Complexity × Effort) + Risk`

**For example story:**
```
Complexity: 3
Effort: 3
Risk: +1

Story Points = (3 × 3) + 1 = 10 points
```

**Story Point Scale Interpretation:**
- **1-2 points:** Trivial, can complete in < 1 hour
- **3-5 points:** Small, can complete in 1-3 hours
- **6-10 points:** Medium, can complete in half day
- **11-15 points:** Large, can complete in 1 day
- **16-20 points:** Very large, consider splitting
- **21+ points:** Too large, MUST split into smaller stories

**If story > 13 points:** Consider splitting into smaller stories.

**See:** `references/calculation-guide.md` for examples and edge cases

---

### 6. Provide Estimation Rationale

**Document WHY this estimate:**

```markdown
## Estimation Rationale

**Story Points:** 10

**Complexity (3/5):** Moderate
- 6 files to modify/create
- Multiple integration points (validation, hashing, DB, JWT)
- Multiple error paths to handle

**Effort (3/5):** Medium
- 6 acceptance criteria
- ~250 lines of code
- ~10 tests required
- Estimated 3-4 hours

**Risk (+1/3):** Minor
- Team familiar with tech stack
- Requirements clear and testable
- Minor security considerations for bcrypt/JWT

**Confidence:** High (80%)
- Clear requirements
- Standard patterns
- No unknowns
```

---

### 7. Update Story File

Add estimation block to story file:

```markdown
## Estimation

**Story Points:** 10
**Estimated By:** Alex (Planner)
**Date:** 2025-01-15
**Confidence:** High (80%)

**Breakdown:**
- Complexity: 3/5 (Moderate - 6 files, multiple integrations)
- Effort: 3/5 (Medium - 6 AC, ~250 LOC, ~10 tests, 3-4 hours)
- Risk: +1/3 (Minor - familiar tech, clear requirements)

**Formula:** (3 × 3) + 1 = 10 points

**Assumptions:**
- Team familiar with Zod, bcrypt, JWT, PostgreSQL
- Clear acceptance criteria remain stable
- No major architectural changes needed
```

---

### 8. Generate Estimation Report (Optional)

For formal estimation reviews or audits, generate comprehensive report:

```markdown
# Story Estimation Report

## Executive Summary
- **Story:** User Signup with Email/Password
- **Story Points:** 10
- **Confidence:** High (80%)
- **Recommendation:** Ready for sprint planning

## Detailed Analysis
[Complexity, Effort, Risk breakdown]

## Comparable Stories
- story-auth-002-login: 8 points (similar complexity, slightly less effort)
- story-auth-003-password-reset: 13 points (more complex flow)

## Assumptions & Risks
[List key assumptions]

## Sprint Planning Notes
- Can be completed in 1 sprint (assuming 2-week sprint)
- No blocking dependencies
- Suitable for mid-level developer
```

**See:** `references/report-templates.md` for full report format

---

## Batch Estimation

For multiple stories:

1. Load all stories
2. Estimate each using same process
3. Compare estimates for consistency
4. Adjust if similar stories have very different estimates
5. Generate summary report

**Tips for consistency:**
- Use same reference points
- Compare with recently estimated similar stories
- Document rationale for each estimate
- Flag outliers for review

---

## Calibration and Adjustment

**After sprint completes:**

1. Compare estimated vs actual story points
2. Identify patterns in over/under-estimation
3. Adjust future estimates based on learnings
4. Update complexity/effort/risk scales if needed

**Example:**
```
Story estimated: 10 points
Actual velocity: 13 points (30% under-estimated)

Reason: Underestimated integration complexity

Learning: Increase complexity score for multi-API integrations
```

---

## Common Scenarios

### Story Seems Too Large (>13 points)

**Approach:**
1. Identify if complexity, effort, or both are high
2. Look for natural split points in acceptance criteria
3. Split into multiple smaller stories
4. Re-estimate each smaller story

**Example:**
```
Original: User Profile (21 points)
Split into:
- User Profile - Basic Info (8 points)
- User Profile - Avatar Upload (8 points)
- User Profile - Preferences (5 points)
```

### Uncertainty in Estimation

**If confidence < 60%:**
1. Identify sources of uncertainty
2. Add risk adjustment
3. Consider spike story for research
4. Document assumptions clearly

### Team Disagreement on Estimate

**Approach:**
1. Each person explains their reasoning
2. Identify where views differ (complexity/effort/risk)
3. Discuss until consensus or average estimates
4. Document the final rationale

**See:** `references/estimation-scenarios.md` for complex cases

---

## Best Practices

1. **Be consistent** - Use same criteria for all stories
2. **Compare similar stories** - Check recent similar estimates
3. **Document rationale** - Explain WHY, not just WHAT
4. **Calibrate regularly** - Adjust based on actual velocity
5. **Split large stories** - > 13 points should be split
6. **Include the team** - Discuss estimates with implementers
7. **Track confidence** - Low confidence = higher risk adjustment

---

## Reference Files

- `references/complexity-scale.md` - Detailed 1-5 complexity scale with examples
- `references/effort-scale.md` - Detailed 1-5 effort scale with examples
- `references/risk-factors.md` - Risk analysis framework (0-3)
- `references/calculation-guide.md` - Formula examples and edge cases
- `references/report-templates.md` - Comprehensive report formats
- `references/estimation-scenarios.md` - Complex scenarios and solutions

---

## When to Escalate

- Story is very large (>20 points) and can't be split
- High uncertainty even after analysis (confidence < 40%)
- Team has no experience with required technology
- Requires significant architectural changes
- Story depends on many external factors

---

*Part of BMAD Enhanced Planning Suite*
