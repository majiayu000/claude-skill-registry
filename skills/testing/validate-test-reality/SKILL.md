---
name: validate-test-reality
description: Meta-validation skill that generates edge cases, production scenarios, and reality gaps not covered by original specifications. Identifies specification-reality mismatches by analyzing what tests claim versus what production data reveals. Creates test deficiency reports showing coverage gaps for Quinn review. Use before quality gate approval to ensure tests reflect production reality, not just specification compliance.
version: 1.0
category: Quality
acceptance:
  edge_cases_generated: "50+ edge cases, error conditions, and production scenarios generated beyond original specification scope"
  test_coverage_analyzed: "All existing tests analyzed for coverage of generated edge cases and production scenarios"
  reality_gaps_identified: "Specification-reality gaps identified where spec says X should work but production patterns show Y fails"
  deficiency_report_created: "Test deficiency report created with specific recommendations for additional tests needed"
inputs:
  story_id:
    type: string
    required: true
    description: "Story/task identifier for reality validation (e.g., 'task-007' or 'story-1.2')"
  story_file:
    type: string
    required: true
    description: "Path to story/task specification file"
  test_design_file:
    type: string
    required: false
    description: "Path to test design file (if already created)"
  production_traffic_file:
    type: string
    required: false
    description: "Path to production traffic patterns file (if available)"
  include_vibe_check:
    type: boolean
    required: false
    description: "Include vibe-check MCP validation (default: true)"
    default: true
outputs:
  total_edge_cases_generated:
    type: number
    description: "Total number of edge cases and production scenarios generated"
  test_coverage_percentage:
    type: number
    description: "Percentage of generated scenarios covered by existing tests"
  critical_gaps_count:
    type: number
    description: "Number of critical gaps where specification-reality mismatch exists"
  high_gaps_count:
    type: number
    description: "Number of high-priority gaps in test coverage"
  medium_gaps_count:
    type: number
    description: "Number of medium-priority gaps in test coverage"
  recommended_tests_count:
    type: number
    description: "Number of additional tests recommended"
  deficiency_report_path:
    type: string
    description: "Path to test deficiency report"
  ready_for_qa:
    type: boolean
    description: "Whether tests are ready for Quinn quality gate review"
telemetry:
  emit: "skill.validate-test-reality.completed"
  track:
    - story_id
    - total_edge_cases_generated
    - test_coverage_percentage
    - critical_gaps_count
    - high_gaps_count
    - medium_gaps_count
    - recommended_tests_count
    - ready_for_qa
    - vibe_check_used
    - production_traffic_available
---

# Test Reality Validation

The **validate-test-reality** skill is a meta-validation layer that bridges the specification-reality gap by generating scenarios beyond what specifications explicitly mention, then validating whether existing tests cover production reality.

## The Specification-Reality Problem

**The Core Challenge:** Specifications describe perfect scenarios. Tests validate specifications. Production provides imperfect reality. The gap between "spec says this should work" and "production shows this fails" is the reliability gap.

**Example:**
- **Specification says:** "User can register with email + password"
- **Tests validate:** User with "test@example.com" and "password123" can register ✓
- **Production reveals:** Emails with "+" (Gmail aliasing), Unicode characters, or simultaneous registrations cause failures ✗

Traditional testing validates specification compliance. Reality validation validates production resilience.

## Purpose

This skill performs three critical functions:

1. **Edge Case Generation:** Generate 50+ scenarios the specification didn't explicitly mention but production will encounter
2. **Test Coverage Analysis:** Verify existing tests cover these real-world scenarios
3. **Reality Gap Identification:** Find mismatches where specifications claim behavior but implementation/tests don't handle reality
4. **Deficiency Reporting:** Create actionable recommendations for Quinn quality gate review

## When to Use This Skill

**This skill should be used:**
- After test-design skill completes (validates test design reality)
- Before quality-gate skill runs (ensures tests reflect reality before approval)
- After initial test implementation (validates tests aren't overfitted to specs)
- When production incidents reveal spec-reality gaps (retrospective validation)
- For high-risk features requiring production-grade validation

**This skill is particularly valuable:**
- For user-facing features with unpredictable inputs
- For features handling external data (APIs, uploads, user content)
- For features with concurrency or race condition risks
- For features with security implications (auth, payments, data access)
- For brownfield codebases where production patterns are known

**This skill should NOT be used when:**
- Tests haven't been designed yet (run test-design first)
- Feature is trivial with no production exposure (internal tooling)
- Specification already includes comprehensive edge cases (rare)

## Reality Gap Categories

### Category 1: Data Reality Gaps
**What specifications miss:** Real data is messy, specifications assume clean data

**Edge Cases to Generate:**
- Unicode characters in text fields (emoji, RTL, special chars)
- Email edge cases (+aliasing, subdomain dots, long domains)
- Null, undefined, empty string variations
- Extremely long inputs (buffer overflow, truncation)
- Special SQL/HTML/JavaScript characters (injection vectors)
- Timezone-specific data (daylight savings, leap seconds)
- Floating point precision issues

**Example Gap:**
- Spec: "Password minimum 8 characters"
- Reality: What about passwords with null bytes? Unicode length vs byte length? Emoji counting?

### Category 2: Concurrency Reality Gaps
**What specifications miss:** Real systems have concurrent users, specifications describe sequential actions

**Edge Cases to Generate:**
- Simultaneous registration with same email
- Race conditions in resource allocation
- Database connection pool exhaustion
- Optimistic locking failures
- Distributed transaction consistency
- Cache invalidation timing

**Example Gap:**
- Spec: "User can create account"
- Reality: 10,000 users register simultaneously during marketing campaign launch

### Category 3: System Reality Gaps
**What specifications miss:** Real systems have failures, specifications assume perfect infrastructure

**Edge Cases to Generate:**
- Database connection failures mid-transaction
- Third-party API timeouts/rate limits
- Disk space exhaustion during file uploads
- Memory pressure during batch operations
- Network partitions and split-brain scenarios
- Graceful degradation requirements

**Example Gap:**
- Spec: "Send welcome email after registration"
- Reality: Email service is down, what happens to user account?

### Category 4: Performance Reality Gaps
**What specifications miss:** Real systems have load, specifications describe single-user scenarios

**Edge Cases to Generate:**
- Response time under 10x expected load
- Memory usage with 100x dataset size
- Database query performance with millions of records
- Connection pool sizing under load spikes
- Cache hit rates with production traffic patterns

**Example Gap:**
- Spec: "Retrieve user profile"
- Reality: Query takes 30s when user has 100K followers

### Category 5: Security Reality Gaps
**What specifications miss:** Real users are malicious, specifications assume honest actors

**Edge Cases to Generate:**
- SQL injection variants (time-based, boolean, union)
- XSS payloads (DOM-based, stored, reflected)
- Authentication bypass attempts
- Authorization boundary violations
- CSRF token manipulation
- Rate limiting bypass techniques
- Session fixation attacks

**Example Gap:**
- Spec: "User can update their profile"
- Reality: Can user update *other* users' profiles via ID manipulation?

### Category 6: Integration Reality Gaps
**What specifications miss:** Real systems integrate with changing dependencies, specifications assume stable interfaces

**Edge Cases to Generate:**
- API version mismatches
- Schema evolution (added/removed fields)
- Response format changes (XML→JSON)
- Authentication credential rotation
- Certificate expiration
- Backwards compatibility breaks

**Example Gap:**
- Spec: "Integrate with payment API"
- Reality: Payment API adds mandatory field in v2, breaks existing integration

## Sequential Skill Execution

**CRITICAL:** Each step must complete before proceeding. This skill uses vibe-check MCP to validate assumptions.

### Step 0: Load Context and Configuration

**Purpose:** Load story specification, test design, production traffic patterns, and configuration

**Actions:**

1. **Load story/task specification:**
   - Read story file (objective, acceptance criteria, context)
   - Extract key functionality claims ("user can X", "system validates Y")
   - Identify data types, external dependencies, security requirements

2. **Load test design (if available):**
   - Read test design file from test-design skill
   - Extract existing test scenarios (Given-When-Then)
   - Count coverage by category (happy path, error, edge, security)

3. **Load production traffic patterns (if available):**
   - Read production traffic logs/patterns file
   - Extract real data patterns (actual emails, inputs, edge cases observed)
   - Identify production failure patterns

4. **Load configuration:**
   - Read `.claude/config.yaml` for reality validation settings
   - Extract edge case generation limits
   - Extract criticality thresholds

5. **Check vibe-check MCP availability:**
   - Verify vibe-check MCP server is available
   - Prepare for assumption validation checkpoints

**Output:** Story context loaded (objective, ACs, claims), test design loaded (existing scenarios, coverage), production patterns loaded (if available), configuration loaded, vibe-check available

**Halt If:** Story file missing | Story too vague to analyze

**See:** `references/templates.md#step-0-context-loading` for complete format

---

### Step 1: Generate Edge Cases Beyond Specification

**Purpose:** Generate 50+ edge cases, error conditions, and production scenarios not explicitly mentioned in specification

**Actions:**

1. **For each acceptance criterion, generate edge cases in 6 categories:**

   **Data Reality:**
   - What if input contains Unicode/emoji?
   - What if input is null/undefined/empty?
   - What if input exceeds max length (10x, 100x)?
   - What if input contains SQL/HTML/JS special characters?
   - What if input has timezone/encoding issues?

   **Concurrency Reality:**
   - What if 10/100/1000 users do this simultaneously?
   - What if race condition on shared resource?
   - What if optimistic locking fails?
   - What if database connection pool exhausted?

   **System Reality:**
   - What if database connection fails mid-operation?
   - What if third-party API times out?
   - What if disk space runs out?
   - What if memory pressure occurs?
   - What if network partition happens?

   **Performance Reality:**
   - What if 10x expected load?
   - What if dataset is 100x larger?
   - What if query scans millions of records?
   - What if cache is cold?

   **Security Reality:**
   - What if SQL injection attempt?
   - What if XSS payload?
   - What if auth bypass attempt?
   - What if authorization boundary violation?
   - What if CSRF attack?

   **Integration Reality:**
   - What if API version changes?
   - What if schema evolves (new/removed fields)?
   - What if authentication fails?
   - What if certificate expires?

2. **Prioritize edge cases:**
   - **Critical:** Security vulnerabilities, data corruption, auth bypass
   - **High:** Data loss, concurrency failures, production outages
   - **Medium:** Performance degradation, edge case errors

3. **Use vibe-check for assumption validation (if enabled):**
   - After generating edge cases, use vibe-check MCP tool
   - Ask: "Are these edge cases realistic for production?"
   - Ask: "What edge cases am I missing?"
   - Refine based on feedback

**Output:** 50+ edge cases generated across 6 categories, each categorized by priority (critical/high/medium), vibe-check validation performed (if enabled)

**Halt If:** Cannot generate meaningful edge cases (spec too trivial)

**See:** `references/templates.md#step-1-edge-case-generation` for complete examples per category

---

### Step 2: Analyze Test Coverage of Reality Scenarios

**Purpose:** Verify existing tests cover generated edge cases and production scenarios

**Actions:**

1. **For each generated edge case, check test coverage:**
   - Does any existing test validate this scenario?
   - If yes: Mark as covered, note which test
   - If no: Mark as gap, note severity

2. **Analyze coverage by category:**
   - Data Reality: X% covered
   - Concurrency Reality: Y% covered
   - System Reality: Z% covered
   - Performance Reality: A% covered
   - Security Reality: B% covered
   - Integration Reality: C% covered

3. **Calculate overall reality coverage:**
   - Formula: (Covered Edge Cases / Total Edge Cases) × 100%
   - Target: ≥80% for production-ready code

4. **Identify critical gaps:**
   - Security scenarios not tested (injection, XSS, auth bypass)
   - Data corruption scenarios not tested
   - Concurrency scenarios not tested (race conditions)
   - System failure scenarios not tested (database down, API timeout)

**Output:** Coverage analysis by category, overall reality coverage percentage, critical gaps identified (security/data/concurrency/system), test-scenario mapping (which tests cover which scenarios)

**Halt If:** Test design file missing (cannot analyze coverage)

**See:** `references/templates.md#step-2-coverage-analysis` for complete format

---

### Step 3: Identify Specification-Reality Gaps

**Purpose:** Find mismatches where specification claims behavior but tests/implementation don't handle reality

**Actions:**

1. **Compare specification claims with reality coverage:**
   - Spec says: "User can register with email + password"
   - Reality check: Do tests cover email edge cases (Unicode, +, dots)?
   - Gap: Spec claims it works, but tests don't verify edge cases

2. **Analyze production traffic patterns (if available):**
   - What actual inputs occur in production?
   - What failures have been observed?
   - What edge cases exist in real data?
   - Compare against test coverage

3. **Identify specification incompleteness:**
   - What did spec fail to mention? (concurrency, failures, edge cases)
   - What assumptions did spec make? (clean data, perfect systems)
   - What constraints did spec omit? (performance, scalability)

4. **Use vibe-check for gap validation (if enabled):**
   - After identifying gaps, use vibe-check MCP tool
   - Ask: "Are these real gaps or theoretical concerns?"
   - Ask: "Which gaps are most likely to cause production issues?"
   - Prioritize based on feedback

5. **Categorize gaps by impact:**
   - **Critical:** Likely to cause production outages, security breaches, data loss
   - **High:** Likely to cause user-facing errors, degraded experience
   - **Medium:** Edge cases that may occur but have limited impact

**Output:** Specification-reality gaps identified with examples, production pattern comparison (if data available), gap severity (critical/high/medium), vibe-check validation performed

**Halt If:** None (can always identify potential gaps)

**See:** `references/templates.md#step-3-gap-identification` for complete examples

---

### Step 4: Generate Test Deficiency Report

**Purpose:** Create actionable recommendations for additional tests needed to close reality gaps

**Actions:**

1. **For each identified gap, recommend specific tests:**
   - **Gap:** Email with "+" character not tested
   - **Recommendation:** Add test case: "User registers with email containing + (Gmail aliasing)"
   - **Test Level:** Unit test for email validation
   - **Priority:** P1 (High)

2. **Structure recommendations by priority:**
   - **Critical gaps (must fix before QA approval):**
     - Security tests (injection, XSS, auth bypass)
     - Data corruption tests
     - Concurrency tests for critical resources

   - **High gaps (should fix before QA approval):**
     - Edge case tests for user inputs
     - System failure tests (API timeout, DB connection loss)
     - Performance tests under load

   - **Medium gaps (can defer if time-constrained):**
     - Rare edge cases
     - Integration version compatibility
     - Extreme load scenarios

3. **Calculate deficiency metrics:**
   - Total gaps: X
   - Critical: A (must fix)
   - High: B (should fix)
   - Medium: C (nice to have)
   - Recommended additional tests: A + B minimum

4. **Determine QA readiness:**
   - If critical gaps > 0: NOT ready for QA
   - If high gaps > 10: NOT ready for QA (too many important gaps)
   - If critical + high gaps = 0 and medium < 5: READY for QA
   - Otherwise: NEEDS IMPROVEMENT (fix high-priority gaps first)

**Output:** Test deficiency report with specific recommendations, gaps categorized by priority, recommended test count, QA readiness status (READY/NOT READY/NEEDS IMPROVEMENT)

**Halt If:** None (can always generate recommendations)

**See:** `references/templates.md#step-4-deficiency-report` for complete format

---

### Step 5: Generate Report and Present Summary

**Purpose:** Generate detailed test deficiency report and present concise summary to user

**Actions:**

1. **Generate report file path:**
   - Format: `.claude/quality/assessments/{story-id}-test-reality-{YYYYMMDD}.md`
   - Example: `.claude/quality/assessments/task-006-test-reality-20251111.md`

2. **Populate report template:**
   - Executive summary (overall coverage, critical gaps, QA readiness)
   - Edge cases generated (by category)
   - Coverage analysis (by category)
   - Specification-reality gaps (with examples)
   - Recommended tests (by priority)
   - QA readiness decision

3. **Write report file**

4. **Present concise summary to user:**
   - Overall reality coverage: X%
   - Edge cases generated: Y
   - Critical gaps: A (examples)
   - High gaps: B (examples)
   - Medium gaps: C
   - Recommended tests: X minimum
   - QA readiness: READY/NOT READY/NEEDS IMPROVEMENT
   - Next steps: Fix critical/high gaps, then proceed to quality-gate

**Output:** Test deficiency report written to file, concise summary presented with coverage/gaps/recommendations, clear QA readiness decision, actionable next steps

**Halt If:** File write fails

**See:** `references/templates.md#step-5-report-output` for complete summary and report template

---

## Integration with Other Skills

### Before quality-gate
**Sequential workflow:**
```
test-design → implement tests → validate-test-reality → quality-gate
```

**Data flow:**
- test-design creates test scenarios
- Implementation writes tests following scenarios
- **validate-test-reality checks:** Do tests cover production reality beyond specs?
- If gaps found: Add recommended tests, re-run validate-test-reality
- If ready: Proceed to quality-gate
- quality-gate uses reality validation as additional dimension

### With test-design
**Complementary relationship:**
- test-design: Creates tests from specification requirements
- validate-test-reality: Validates tests cover reality beyond requirements
- **Together:** Ensures tests validate both specification compliance AND production resilience

### With trace-requirements
**Validation layer:**
- trace-requirements: Verifies all ACs have tests
- validate-test-reality: Verifies all reality scenarios have tests
- **Gap:** AC may have tests but tests don't cover edge cases

### With production monitoring
**Feedback loop:**
- Production incidents reveal reality gaps
- validate-test-reality uses production traffic patterns to generate realistic edge cases
- Tests improve based on actual failures
- **Continuous improvement:** Tests evolve with production learnings

## Best Practices

1. **Run before quality gate:** Always validate test reality before final QA approval
2. **Use production data:** If available, use real traffic patterns for realistic edge cases
3. **Enable vibe-check:** Use MCP server to validate assumptions and avoid tunnel vision
4. **Prioritize security:** Always generate and test security edge cases (injection, XSS, auth)
5. **Test concurrency:** Real systems have concurrent users, generate race condition scenarios
6. **Test failures:** Systems fail, generate failure scenarios (DB down, API timeout)
7. **Fix critical gaps:** Never proceed to QA with critical security/data gaps
8. **Iterate:** Re-run after adding tests to verify gaps closed

## Common Pitfalls

**Pitfall 1: Assuming specification is complete**
- Specifications describe ideal scenarios, not production reality
- **Solution:** Always generate edge cases beyond specification scope

**Pitfall 2: Over-testing trivia, under-testing reality**
- 100% coverage of specification scenarios ≠ production-ready
- **Solution:** Focus on realistic edge cases (production data, concurrency, failures)

**Pitfall 3: Ignoring production patterns**
- Synthetic test data doesn't reveal real edge cases
- **Solution:** Use production traffic patterns if available

**Pitfall 4: Skipping security scenarios**
- Specifications rarely mention security edge cases
- **Solution:** Always generate injection, XSS, auth bypass tests

**Pitfall 5: Testing implementation details**
- Tests that pass with mocks fail with real systems
- **Solution:** Generate system failure scenarios (DB down, API timeout)

## Configuration

Configure in `.claude/config.yaml`:

```yaml
quality:
  reality_validation:
    edge_case_limit: 50  # Minimum edge cases to generate
    enable_vibe_check: true  # Use vibe-check MCP for validation
    production_traffic_path: ".claude/production/traffic.json"  # Optional
    critical_gap_threshold: 0  # Max critical gaps before blocking QA
    high_gap_threshold: 10  # Max high gaps before blocking QA
```

## Reference Files

Detailed documentation in `references/`:

- **templates.md**: All output formats (Steps 0-5), edge case generation examples, coverage analysis format, gap identification examples, deficiency report template, integration examples

- **edge-cases.md**: Comprehensive edge case catalog by category (data/concurrency/system/performance/security/integration)

- **reality-gaps.md**: Common specification-reality gap patterns with examples

- **production-patterns.md**: How to use production traffic patterns for realistic testing

- **vibe-check-integration.md**: How to use vibe-check MCP for assumption validation

---

**Version:** 1.0 (Initial release based on production reality validation research)
**Category:** Quality
**Depends On:** test-design (requires test scenarios to validate), vibe-check MCP (optional but recommended)
**Used By:** quality-gate (uses reality validation as additional quality dimension)
**Innovation:** First skill to bridge specification-reality gap through systematic edge case generation and production pattern analysis
