---
name: quality-assurance
description: Use when deciding test strategy, struggling with code reviews, shipping without tests, or conflating verification with validation
---

# Quality Assurance

## Overview

This skill implements the **Verification (VER)** and **Validation (VAL)** process areas from the CMMI-based SDLC prescription.

**Core principle**: Verification ≠ Validation. Tests prove you built it correctly (VER). Users prove you built the right thing (VAL). Both required at Level 3.

**Critical distinction**:
- **Verification**: "Did we build the product right?" (tests, reviews, inspections)
- **Validation**: "Did we build the right product?" (user acceptance, stakeholder approval)

**Reference**: See `docs/sdlc-prescription-cmmi-levels-2-4.md` Section 3.3 for complete VER/VAL policy.

---

## When to Use

Use this skill when:
- Deciding test strategy or coverage requirements
- Code reviews ineffective ("LGTM" rubber stamps)
- Pressure to skip tests ("we'll add them later")
- Tests pass but customers report bugs (VER without VAL)
- Same defects recurring (no root cause analysis)
- Manual testing taking days (ice cream cone anti-pattern)
- Unclear what "quality" means for your project level

**Do NOT use for**:
- Specific test framework details → Use domain skills (python-engineering, web-backend)
- E2E/performance/chaos engineering → Use ordis-quality-engineering
- Production monitoring → Use platform-integration

---

## Quick Reference

| Situation | Primary Reference Sheet | Key Decision |
|-----------|------------------------|--------------|
| "Skip tests to ship faster?" | Testing Practices | Level 3: Tests required before merge. Exception protocol for emergencies only. |
| "Reviews catching nothing" | Peer Reviews | Social dynamics issue, not technical. Psychological safety + reviewer accountability. |
| "Tests pass, customers unhappy" | Validation with Stakeholders | VER without VAL. Both required at Level 3. UAT process needed. |
| "Same bugs recurring" | Defect Management | Requires RCA (5 Whys, fishbone). Pattern = systemic issue needing process fix. |
| "Manual tests take 2 days" | Testing Practices | Ice cream cone anti-pattern. Migrate to test pyramid with economics. |

---

## Verification vs Validation: The Critical Distinction

### Verification (VER) - "Built Correctly"

**What**: Ensuring product meets specifications and requirements

**How**: Testing, code review, static analysis, inspections

**Who**: Development team (internal)

**When**: Throughout development, before release

**Level 3 Requirements**:
- Test coverage >70% for critical paths
- Peer review required for all changes
- Automated tests in CI pipeline

**Example**: Unit tests pass, integration tests pass, code reviewed

### Validation (VAL) - "Right Thing Built"

**What**: Ensuring product meets user needs and solves actual problems

**How**: User acceptance testing (UAT), stakeholder demos, beta testing

**Who**: End users, stakeholders (external to dev team)

**When**: End of iteration, before production release

**Level 3 Requirements**:
- Stakeholder sign-off on acceptance criteria
- UAT with representative users
- Demo to product owner for approval

**Example**: Users confirm feature solves their problem, stakeholders approve for release

### Why Both Matter

| Scenario | VER | VAL | Outcome |
|----------|-----|-----|---------|
| Tests pass, users happy | ✅ | ✅ | **SUCCESS** - Built correctly AND right thing |
| Tests pass, users unhappy | ✅ | ❌ | **FAILURE** - Wrong feature, wrong UX, wrong problem solved |
| Tests fail, users would have been happy | ❌ | ✅ | **FAILURE** - Right idea, poor execution, bugs prevent use |
| Tests fail, users would be unhappy | ❌ | ❌ | **DISASTER** - Wrong thing built poorly |

**Level 3 mandate**: Both VER and VAL required before production release.

---

## Level-Based QA Requirements

### Level 2: Managed

**VER Requirements**:
- Basic test coverage (>50% for critical paths)
- Peer review recommended (not enforced)
- Manual testing acceptable

**VAL Requirements**:
- Product owner approval
- Informal stakeholder feedback

**Work Products**:
- Test results (pass/fail)
- Review notes (PR comments)

**Quality Criteria**:
- Critical functionality tested
- Stakeholder aware of release

**Audit Trail**:
- Test runs logged
- Approval emails/messages

### Level 3: Defined

**VER Requirements**:
- **Required test coverage >70% for critical paths**
- **Mandatory peer review (2+ reviewers, platform-enforced)**
- Automated testing in CI
- Code review checklist used
- Test strategy documented

**VAL Requirements**:
- **UAT with representative users required**
- Formal stakeholder acceptance criteria
- Demo to product owner mandatory
- Validation documented (sign-off)

**Work Products**:
- Test strategy document
- Test coverage reports
- Review effectiveness metrics
- UAT plan and results
- Stakeholder acceptance sign-off

**Quality Criteria**:
- Coverage targets met (>70%)
- Review finding rate 20-40% (detects real issues)
- Stakeholder approval documented
- Defect escape rate tracked

**Audit Trail**:
- All tests tracked in CI
- Review approvals in platform
- UAT sign-off with dates
- Defect metrics dashboard

### Level 4: Quantitatively Managed

**Statistical Practices**:
- Defect prediction models (based on complexity, churn)
- Review effectiveness statistical control (control charts)
- Test coverage trends with baselines
- Defect escape rate within statistical limits

**Quantitative Work Products**:
- Statistical process control charts (defect injection, escape rates)
- Predictive models for quality
- Cp/Cpk analysis for test processes

**Quality Criteria**:
- Defect density <0.5 per KLOC (baseline established)
- Review finding rate within control limits (20-40%)
- Test coverage stable >80% with minimal variation

**Audit Trail**:
- Historical quality data with statistical analysis
- Prediction vs actual defect counts
- Process capability indices

---

## Exception Protocol: Shipping Without Tests

**CRITICAL**: "Tests later" = tests never (documented historical pattern)

### When Shipping Without Tests is NEVER Acceptable

**Level 3 projects - Absolute requirements**:
- Critical user-facing features
- Security-sensitive code (auth, payments, PII)
- Regulatory/compliance features
- Data migration or modification
- Core business logic

**Rationale**: Risk too high, rework too expensive, reputation damage too severe

### Emergency Exception Process (TEST-HOTFIX)

**When**: Production outage, immediate fix needed, no time for full test suite

**Level 3 Requirements**:
1. Fix the emergency (restore service)
2. Document in issue tracker with "TEST-HOTFIX" label
3. **Write tests within 48 hours** (retrospective testing mandatory)
4. Create ticket for proper fix if hotfix is hack
5. RCA for why hotfix needed (prevent future)

**Frequency Limit**: >5 TEST-HOTFIXes per month = systemic problem requiring process audit

**Violation**: Skipping retrospective tests = QA failure, escalate to engineering manager

### Risk-Based Minimal Testing (When Must Ship)

If absolutely must ship without full coverage:

1. **Critical path only**: Test happy path + 1-2 critical error cases
2. **Feature flag**: Deploy disabled, enable after testing
   - **Maximum duration flagged**: 7 days before full test suite required
   - Flagged features count toward TEST-HOTFIX frequency limit
   - Must have validation plan with timeline before deploying flagged
3. **Beta rollout**: Ship to 5-10% users, monitor, expand
4. **Demo ≠ Production**: Demo to stakeholders, don't enable for all users
   - **Maximum demo-only duration**: 2 sprints
   - After demo: either release to production (with UAT) or cancel feature
   - "Perpetual demo" is validation theater anti-pattern
5. **Manual acceptance test**: At minimum, stakeholder uses feature live

**Retrospective required**: Within 7 days, answer "Why no tests?" and address root cause

**Enforcement**: Violations escalate to engineering manager, process audit if patterns emerge

---

## Anti-Patterns and Red Flags

### Test Last

**Detection**: Tests written after code (or not at all), "We'll add tests later"

**Red Flags**:
- PR without tests for new functionality
- Test coverage declining sprint-over-sprint
- "Too busy to write tests"
- Tests added only when bugs found

**Why it fails**: "Later" never comes, test debt accumulates, bugs reach production, rework costs 10-100x more

**Counter**: TDD requirement (Level 3 can waive, but must justify). Tests = part of "done", not optional.

### Rubber Stamp Reviews

**Detection**: Code reviews <5 minutes, "LGTM" without specific feedback, defects escaping to production

**Red Flags**:
- Review approved within minutes of PR creation
- No comments or only style nitpicks
- Reviewer didn't pull code or run it
- Same bugs recurring that reviews should have caught

**Why it fails**: Social pressure not to block > quality, reviewers fear being "difficult", no accountability

**Counter**: Review metrics (finding rate should be 20-40%), reviewer accountability, psychological safety

### Ice Cream Cone (Inverted Test Pyramid)

**Detection**: Mostly manual E2E tests, few unit tests, regression testing takes days

**Red Flags**:
- >50% of testing time is manual
- Regression suite takes >4 hours
- Most tests are UI/E2E (slow, brittle)
- "Can't automate, need manual QA"

**Why it fails**: Doesn't scale, slow feedback, expensive to maintain, brittle tests

**Counter**: Test pyramid economics, migration to unit-heavy strategy, ROI calculation

### Defect Whack-a-Mole

**Detection**: Same bugs recurring in different places, no pattern analysis, firefighting constantly

**Red Flags**:
- Similar bugs in different modules (copy-paste errors)
- Defects closed without RCA
- "Fix it quick, no time to investigate"
- Bug fixes create new bugs (ripple effects)

**Why it fails**: Treats symptoms not causes, waste effort on recurring issues, no learning

**Counter**: RCA requirement (Level 3 mandatory for recurring defects), defect pattern analysis

### Validation Theater

**Detection**: Stakeholders "approve" without actually using system, checkbox exercise

**Red Flags**:
- UAT sign-off in <1 hour (didn't actually test)
- Stakeholders approve without touching the system
- Demo only (no hands-on validation)
- Rubber stamp "looks good" without criteria
- Product owner used as "representative user" instead of actual end users
- Feature in perpetual demo mode (>2 sprints without production release or cancellation)

**Why it fails**: False confidence, issues found in production, customer dissatisfaction

**Counter**:
- Hands-on UAT requirement
- **Level 3 requires at least 2 actual end users for UAT** (not proxies)
- Product owner is NOT a representative user (unless they use the product daily)
- Exception: Internal tools where team members are actual users
- Acceptance criteria verification
- Time requirement (min 1 day for meaningful validation)
- Demo-only maximum: 2 sprints before release or cancel decision

---

## Reference Sheets

The following reference sheets provide detailed guidance for specific QA domains. Load them on-demand when needed.

### 1. Testing Practices

**When to use**: Deciding test strategy, coverage requirements, test pyramid, TDD

→ See [testing-practices.md](./testing-practices.md)

**Covers**:
- Test pyramid (unit, integration, E2E) with economics
- Coverage criteria by project level
- Test-driven development (TDD) process
- Test types (smoke, regression, acceptance)
- Migration from manual to automated (ice cream cone → pyramid)
- Anti-patterns: Test Last, Over-Mocking, Flaky Tests

### 2. Peer Reviews

**When to use**: Code reviews ineffective, rubber-stamp approvals, unclear reviewer responsibilities

→ See [peer-reviews.md](./peer-reviews.md)

**Covers**:
- Review checklist (functionality, tests, design, security)
- Social dynamics playbook (giving critical feedback safely)
- Reviewer accountability and responsibilities
- Review metrics (effectiveness, turnaround time, finding rate)
- Review taxonomy (depth varies by change type: hotfix vs feature)
- Anti-patterns: Rubber Stamp, Bikeshedding, Review Backlog

### 3. Validation with Stakeholders

**When to use**: Planning UAT, stakeholder acceptance, beta testing, demo preparation

→ See [validation-with-stakeholders.md](./validation-with-stakeholders.md)

**Covers**:
- UAT process and planning
- Acceptance criteria definition (INVEST)
- Stakeholder identification and management
- Demo vs hands-on validation
- Beta rollout strategies
- Anti-patterns: Validation Theater, Demo-Only, Proxy Users

### 4. Defect Management

**When to use**: Bugs recurring, defect triage, root cause analysis, prevention

→ See [defect-management.md](./defect-management.md)

**Covers**:
- Defect classification (severity, recurrence, root cause)
- Root cause analysis (5 Whys, fishbone diagram, fault tree)
- Defect prevention over detection
- Level 3 requirement: RCA for recurring defects
- Defect metrics (escape rate, density, resolution time)
- Anti-patterns: Whack-a-Mole, Symptom Fixes, No RCA

### 5. QA Metrics

**When to use**: Measuring quality effectiveness, tracking improvement, justifying QA investment

→ See [qa-metrics.md](./qa-metrics.md)

**Covers**:
- Defect escape rate (bugs found post-release / total bugs)
- Review effectiveness (finding rate: bugs in review / total bugs)
- Test automation ROI
- Coverage trends and targets
- Level 4 statistical process control

### 6. Level 2→3→4 Scaling

**When to use**: Understanding appropriate QA rigor for project tier

→ See [level-scaling.md](./level-scaling.md)

**Covers**:
- Level 2 baseline QA practices
- Level 3 organizational QA standards
- Level 4 statistical quality control
- Escalation criteria (when to increase rigor)
- De-escalation criteria (when rigor is overkill)

---

## Common Mistakes

| Mistake | Why It Fails | Better Approach |
|---------|--------------|-----------------|
| "Tests later" | Later never comes, debt accumulates | Tests = part of "done". Level 3: required before merge. |
| "Tests pass = done" | Conflates VER with VAL, skips user acceptance | Both required at Level 3. Tests AND stakeholder approval. |
| "LGTM rubber stamps" | Social pressure > quality, reviewers fear blocking | Reviewer accountability, metrics (20-40% finding rate), psychological safety. |
| "Automate everything" | Automation has costs (setup, maintenance), not always ROI-positive | Test pyramid economics. Unit tests cheap, E2E expensive. Choose wisely. |
| "Manual testing is bad" | Some testing should be manual (exploratory, one-time, usability) | Strategic automation. Critical paths automated, exploratory manual. |
| "Skip RCA, fix it quick" | Same bugs recur, waste effort whack-a-mole | Level 3: RCA required for recurring defects. Fix root cause, not symptom. |
| "Stakeholder approved" (without using system) | Validation theater, issues found in production | Hands-on UAT required. Stakeholder must actually use feature, not just demo. |

---

## Integration with Other Skills

| When You're Doing | Also Use | For |
|-------------------|----------|-----|
| Writing tests for Python code | `axiom-python-engineering` | pytest-specific patterns and idioms |
| E2E/performance/chaos testing | `ordis-quality-engineering` | Specialized test strategies |
| Implementing code review process | `design-and-build` | Code review checklist, CI integration |
| Designing acceptance criteria | `requirements-lifecycle` | INVEST criteria, user story format |
| Setting up CI for testing | `design-and-build` | CI/CD pipeline configuration |

---

## Real-World Impact

**Without this skill**: Teams experience:
- VER without VAL (tests pass, customers unhappy)
- Test debt accumulating ("later" never comes)
- Rubber stamp reviews (LGTM without reading)
- Same defects recurring (no RCA)
- Ice cream cone (slow manual E2E tests)

**With this skill**: Teams achieve:
- Both VER and VAL (quality gate before production)
- Tests written alongside code (TDD culture)
- Effective reviews (20-40% finding rate)
- Defect prevention through RCA
- Test pyramid (fast feedback, low maintenance)

---

## Next Steps

1. **Determine project level**: Check CLAUDE.md or ask user for CMMI target level (default: Level 3)
2. **Identify situation**: Use Quick Reference table to find relevant reference sheet
3. **Load reference sheet**: Read detailed guidance for specific domain
4. **Enforce VER+VAL**: Level 3 requires both verification and validation - no exceptions
5. **Apply frameworks**: Use systematic evaluation (test pyramid economics, review metrics, RCA methods)
6. **Counter anti-patterns**: Watch for test-last, rubber stamps, ice cream cone, whack-a-mole
7. **Measure effectiveness**: Establish baselines, track defect escape rate and review finding rate

**Remember**: Verification proves you built it correctly. Validation proves you built the right thing. You need BOTH.
