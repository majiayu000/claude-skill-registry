---
name: risk-profile
description: Assess implementation risks using Probability × Impact (P×I) scoring methodology across 6 categories (Technical, Security, Performance, Data, Business, Operational). Scores risks (P×I: 1-9), develops mitigations for high-risk items (score ≥6), and prioritizes test scenarios (P0/P1/P2). Use before implementation or during quality review to identify and mitigate potential issues.
version: 2.0
category: Quality
acceptance:
  risks_identified: "All potential risks identified across 6 categories (Technical, Security, Performance, Data, Business, Operational) with 10-20 risks typical"
  risks_scored: "All risks scored using P×I methodology (Probability 1-3, Impact 1-3, Score 1-9) with reasoning documented"
  mitigations_developed: "Mitigation strategies developed for all high-risk items (score ≥6) with concrete actions and effort estimates"
  tests_prioritized: "Test scenarios prioritized by risk level (P0 for score ≥7, P1 for score 5-6, P2 for score 3-4)"
inputs:
  task_id:
    required: true
    description: "Task identifier for risk assessment (e.g., 'task-006')"
  task_file:
    required: true
    description: "Path to task specification file"
  assessment_mode:
    required: false
    description: "Assessment timing (pre-implementation/during-development/post-implementation, auto-detected from task status)"
outputs:
  total_risks:
    description: "Total number of risks identified"
  critical_risks_count:
    description: "Number of critical risks (score ≥7)"
  high_risks_count:
    description: "Number of high risks (score 6)"
  risk_profile_path:
    description: "Path to generated risk profile report"
  quality_gate_impact:
    description: "Predicted quality gate status (PASS/CONCERNS/FAIL)"
  p0_tests_count:
    description: "Number of P0 (critical) tests required"
telemetry:
  emit: "skill.risk-profile.completed"
  track:
    - task_id
    - assessment_mode
    - total_risks
    - critical_risks_count
    - high_risks_count
    - medium_risks_count
    - low_risks_count
    - highest_risk_score
    - quality_gate_impact
    - p0_tests_count
    - p1_tests_count
    - assessment_duration_ms
---

# Risk Profile Assessment

The **risk-profile** skill assesses implementation risks before or during development using the Probability × Impact (P×I) scoring methodology. This skill identifies potential issues early, enables risk-based test prioritization, and informs quality gate decisions. By systematically evaluating risks across 6 categories (Technical, Security, Performance, Data, Business, Operational), the skill produces a risk matrix with mitigation strategies and test priorities.

The P×I methodology scores each risk on a 1-9 scale (Probability 1-3 × Impact 1-3), enabling objective risk measurement and comparison. Critical risks (score ≥7) require immediate mitigation, high risks (score 6) require testing validation, medium risks (3-5) need monitoring, and low risks (1-2) require standard precautions. This scoring directly integrates with the quality gate: risks ≥9 trigger FAIL, risks ≥6 trigger CONCERNS, providing clear quality thresholds.

The skill is most powerful when used pre-implementation (after task spec creation, before coding begins), allowing developers to design mitigations into the implementation rather than retrofitting fixes later. The risk profile generates test priorities (P0/P1/P2) based on risk scores, ensuring the highest-risk areas receive comprehensive testing. The output integrates with test-design and quality-gate skills for comprehensive quality assessment.

## When to Use This Skill

**This skill should be used when:**
- Risks need to be assessed before starting implementation (recommended timing)
- Potential issues need identification early in development cycle
- Test scenarios need to be prioritized by risk level
- Quality gate decisions need to be informed with risk data
- Mitigation strategies need to be developed for high-risk areas

**This skill is particularly valuable:**
- After task spec creation, before implementation begins (optimal timing)
- For complex or high-risk features (external APIs, security, data migrations)
- When planning comprehensive test strategy
- During quality review to validate risk mitigation

**This skill should NOT be used when:**
- Task is simple CRUD with no external dependencies (low value)
- Bug fix has clear root cause and straightforward solution
- Well-established patterns with no unknowns (minimal risk)

## Prerequisites

Before running risk-profile, ensure you have:

1. **Task specification file** with clear objective, acceptance criteria, and context
2. **Project configuration** (.claude/config.yaml) with risk threshold setting
3. **Understanding of implementation approach** (what will be built, how, with what technologies)

**Optimal timing:**
- **Pre-implementation:** Task status "Draft" or "Approved" (best time for risk assessment)
- **During development:** Task status "InProgress" (validate mitigation effectiveness)
- **Post-implementation:** Task status "Review" (inform quality gate)

## Sequential Risk Assessment Process

This skill executes through 7 sequential steps (Step 0-6). Each step must complete successfully before proceeding. The process systematically identifies risks, scores them with P×I methodology, develops mitigations, prioritizes tests, and generates a comprehensive risk profile report.

### Step 0: Load Configuration and Task Context

**Purpose:** Load project configuration and task specification to understand what will be implemented and establish the risk assessment context.

**Actions:**
1. Load project configuration from `.claude/config.yaml`:
   - Extract `quality.riskScoreThreshold` (default: 6)
   - Extract `quality.qualityLocation` (default: .claude/quality)
2. Read task specification file:
   - Load objective and acceptance criteria
   - Load context (data models, APIs, components, constraints)
   - Load task breakdown (implementation steps)
3. Determine assessment mode from task status:
   - Pre-implementation: Status "Draft" or "Approved"
   - During development: Status "InProgress"
   - Post-implementation: Status "Review"
4. Understand implementation scope and complexity

**Halt If:**
- Configuration file missing or invalid
- Task file not found or unreadable
- Task too vague to assess risks

**Output:** Configuration loaded with risk threshold, task spec loaded with ID/title, assessment mode determined, implementation scope analyzed (tasks/systems/patterns)

**See:** `references/templates.md#step-0-output` for complete format

---

### Step 1: Identify Risk Areas

**Purpose:** Brainstorm potential risks across all 6 risk categories by analyzing task complexity, technical context, acceptance criteria, and known issues.

**Actions:**
1. Analyze task complexity:
   - Count tasks/subtasks (>10 = higher complexity)
   - Count systems involved (>3 = higher integration risk)
   - Identify new patterns vs. established patterns
   - Identify unknown vs. familiar technologies
2. Review technical context:
   - Data models involved
   - External APIs/services
   - Authentication/authorization requirements
   - Database operations (migrations, complex queries)
   - UI components (if applicable)
3. Check acceptance criteria for risk signals:
   - Security requirements mentioned?
   - Performance targets specified?
   - Data migration needed?
   - Complex business logic?
   - User-facing changes (impact scope)?
4. Brainstorm potential risks in each category:
   - **Technical:** Integration challenges, unknown APIs, complexity
   - **Security:** Auth vulnerabilities, injection risks, data exposure
   - **Performance:** Response time, scalability, N+1 queries, resource usage
   - **Data:** Integrity issues, migration complexity, data loss potential
   - **Business:** User impact scope, revenue implications, compliance
   - **Operational:** Deployment complexity, monitoring gaps, rollback difficulty
5. Document 10-20 potential risks with initial categorization

**Output:** Risk areas identified with count per category (Technical/Security/Performance/Data/Business/Operational), complexity indicators (task count, system count, pattern type)

**See:** `references/templates.md#step-1-output` for complete format with examples

---

### Step 2: Score Each Risk (P×I)

**Purpose:** Systematically score each identified risk using Probability × Impact methodology to enable objective risk comparison and prioritization.

**Actions:**
For each identified risk:
1. Assess Probability (P: 1-3):
   - **1 (Low):** Unlikely to occur (<20% chance) - good patterns, known approaches
   - **2 (Medium):** May occur (20-60% chance) - some unknowns, moderate complexity
   - **3 (High):** Likely to occur (>60% chance) - complex, many unknowns, new territory
2. Assess Impact (I: 1-3):
   - **1 (Low):** Minor inconvenience, easy fix, low impact
   - **2 (Medium):** Significant issue, moderate effort to fix, notable impact
   - **3 (High):** Critical failure, major effort to fix, security/data loss/business impact
3. Calculate Risk Score:
   - Risk Score = P × I (1-9 scale)
4. Document reasoning:
   - Why this probability? (evidence, similar experiences, complexity factors)
   - Why this impact? (user impact, business impact, fix difficulty)
5. Sort risks by score (highest first for reporting)

**Output:** Risks scored with P×I methodology, score distribution (critical/high/medium/low counts), highest score, quality gate impact prediction

**See:** `references/templates.md#step-2-output` for complete format and scoring examples

---

### Step 3: Develop Mitigation Strategies

**Purpose:** Create actionable mitigation strategies for all high-risk items (score ≥6) with concrete prevention, detection, and recovery actions.

**Actions:**
For each high-risk item (prioritize critical risks first):
1. Identify mitigation approach:
   - **Prevention:** How to prevent risk from occurring? (design, patterns, validation)
   - **Detection:** How to detect if risk occurs? (tests, monitoring, logging)
   - **Recovery:** How to recover if risk occurs? (rollback, fallback, manual fix)
2. Specify concrete actions:
   - What specific code/design changes?
   - What tests to write? (test files, scenarios)
   - What monitoring to add? (metrics, alerts)
   - What documentation needed?
3. Assign to appropriate phase:
   - **During Implementation:** Handle when coding (architectural decisions, validation)
   - **Testing:** Validate through tests (unit, integration, E2E)
   - **Deployment:** Address in deployment process (migrations, feature flags)
   - **Monitoring:** Detect in production (alerts, dashboards)
4. Estimate effort:
   - Minimal (<1 hour)
   - Moderate (1-4 hours)
   - Significant (>4 hours)

**Output:** Mitigation strategies developed for all high-risk items, critical/high risks mitigation counts, total effort estimate, phase breakdown (implementation/testing/deployment/monitoring)

**See:** `references/templates.md#step-3-output` for complete format and mitigation examples

---

### Step 4: Prioritize Test Scenarios

**Purpose:** Map risks to test priorities (P0/P1/P2) and identify must-have test scenarios for high-risk areas to ensure comprehensive validation.

**Actions:**
1. Map risks to test priorities:
   - **P0 (Critical):** Risks with score ≥7 (must have before merge)
   - **P1 (High):** Risks with score 5-6 (should have before merge)
   - **P2 (Medium):** Risks with score 3-4 (nice to have)
   - **P3 (Low):** Risks with score 1-2 (standard testing)
2. Identify must-have tests for high-risk areas:
   - Security risks → Security test scenarios (injection, auth bypass, data exposure)
   - Performance risks → Performance test scenarios (load tests, query analysis)
   - Data risks → Data integrity test scenarios (race conditions, migrations)
   - Integration risks → Integration test scenarios (external API failures)
3. Specify test scenarios for each P0/P1 risk:
   - Describe test scenario (what to test, how to test)
   - Specify test level (unit/integration/E2E)
   - Assign priority (P0/P1/P2)
   - Define expected outcome
4. Document risk-test mapping:
   - Which tests validate which risks?
   - What test coverage is needed?
   - What scenarios would expose the risk?

**Output:** Test scenarios prioritized by risk level, P0/P1/P2 test counts, risk-test mapping complete

**See:** `references/templates.md#step-4-output` for complete format and test examples

---

### Step 5: Generate Risk Profile Report

**Purpose:** Create comprehensive risk profile report documenting all risks, scores, mitigations, and test priorities for reference during implementation and quality review.

**Actions:**
1. Load risk profile template from `.claude/templates/risk-profile.md`
2. Populate risk matrix:
   - List all risks sorted by score (highest first)
   - Include: #, Category, Risk, P, I, Score, Mitigation summary
3. Create high-risk summary section:
   - Risks with score ≥6 with detailed mitigations
   - Concrete actions, phase assignment, effort estimates
4. Document test prioritization:
   - P0/P1/P2 test scenarios with risk mapping
   - Test files, scenarios, expected outcomes
5. Add quality gate impact prediction:
   - Will any risks trigger FAIL (score ≥9)?
   - Will any risks trigger CONCERNS (score ≥6)?
   - What's needed for PASS? (mitigation + testing)
6. Generate file path: `{qualityLocation}/assessments/{taskId}-risk-{YYYYMMDD}.md`
7. Write risk profile file with all sections

**Output:** Risk profile report generated at path, total risks documented, critical/high risks detailed, test priorities documented (P0/P1/P2 counts), quality gate impact prediction

**See:** `references/templates.md#step-5-output` and `#complete-risk-profile-report-template` for complete format

---

### Step 6: Present Summary to User

**Purpose:** Provide concise summary with key risk metrics, critical risks highlighted, mitigation strategies, test priorities, and clear next steps.

**Actions:**
1. Display formatted summary:
   - Task metadata (ID, title, assessment date)
   - Risk summary (total, critical, high, medium, low counts)
   - Critical risk(s) highlighted with mitigation (if any)
   - High-risk areas with mitigation summaries
   - Test priorities (P0/P1 scenarios)
   - Quality gate impact prediction
   - Recommendation for next steps
2. Highlight critical risks (score ≥7) requiring immediate attention
3. Provide implementation guidance:
   - Address critical risks first
   - Implement high-risk mitigations during development
   - Write P0/P1 tests to validate
4. Emit telemetry event with all metrics

**Output:** Formatted summary with task metadata, risk counts by severity, critical risks highlighted with mitigations, high-risk areas summarized, P0/P1 test priorities, quality gate impact prediction, path to PASS recommendations, next steps

**See:** `references/templates.md#step-6-user-facing-summary` for complete formatted output examples

**Execution Complete.**

---

## Risk Scoring Methodology

**Probability (P):** 1-3 scale measuring likelihood (1=<20% unlikely, 2=20-60% may occur, 3=>60% likely)

**Impact (I):** 1-3 scale measuring severity (1=minor/easy fix, 2=significant issue/moderate fix, 3=critical failure/major fix)

**Risk Score:** P × I (1-9 scale) | 9=critical immediate mitigation, 6-8=high mitigation+testing, 3-5=medium monitor, 1-2=low standard precautions

**Quality Gate Rules:** Score ≥9 → FAIL | Score ≥6 → CONCERNS | Score <6 → No auto-impact

**See:** `references/templates.md#probability-assessment-guidelines` and `#impact-assessment-guidelines` for detailed scoring criteria and examples

---

## Integration with Other Skills

**Before:** Planning skills (create-task-spec, breakdown-epic) create task spec → Task approved → Ready for risk assessment

**After - Pre-implementation:** Developer aware of risks, mitigations inform implementation approach, test priorities guide test writing

**Handoff to test-design:** Risk profile with P0/P1/P2 priorities → test-design creates detailed scenarios for high-risk areas

**Handoff to quality-gate:** Risk profile informs gate decision | Critical risks (≥7) checked for mitigation | High risks (≥6) checked for test coverage

**See:** `references/templates.md#integration-examples` for complete workflows with data flow

---

## Best Practices

Assess early (after spec, before code) | Be honest about probability (consider team experience) | Consider real impact (data loss, security, business) | Actionable mitigations (specific, phase-assigned, effort-estimated) | Risk-driven testing (high risk = high priority tests) | Continuous reassessment (if requirements change or new risks discovered)

---

## Reference Files

Detailed documentation in `references/`:

- **templates.md**: All output formats (Step 0-6), risk scoring examples, complete risk profile report template, risk category details, probability/impact guidelines, mitigation strategies, test prioritization examples, integration workflows, JSON output format

- **risk-categories.md**: Risk category definitions and examples (currently placeholder - see templates.md)

- **risk-scoring.md**: P×I methodology details (currently placeholder - see templates.md)

- **mitigation-strategies.md**: Mitigation patterns (currently placeholder - see templates.md)

- **risk-examples.md**: Risk profile examples (currently placeholder - see templates.md)

---

*Risk Profile Assessment skill - Version 2.0 - Minimal V2 Architecture*
