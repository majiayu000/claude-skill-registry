---
name: plan-reviewer
description: Review implementation plans, PR specifications, and feature documentation to ensure acceptance criteria are testable, validation is complete, and integration risks are surfaced before coding begins.
---

# Plan Reviewer


## Minimum required inputs from the plan (reviewer gate)

Before reviewing details, confirm the plan includes these minimum inputs. If any are missing, request edits to the plan rather than guessing.

- **Acceptance Criteria**: clear, user visible outcomes, written as observable conditions
- **Validation Plan**: at least one validation step per acceptance criterion
- **Automated Test Intent**: what will be covered by automated tests, and where they live
- **Manual Validation Steps**: concrete steps anyone on the team can follow
- **Integration Touchpoints**: systems, services, queues, APIs, data stores, or clients that will be affected


Review implementation plans, PR specifications, and feature documentation **before coding begins**.

This skill focuses on:
- Testable acceptance criteria
- Complete validation strategies (manual + automated)
- Integration awareness
- Clear open questions and risks

It is designed to produce **actionable deltas**, not a perfect plan.

---

## When to Use This Skill

Use this skill when reviewing:
- Implementation plans and execution checklists
- PR specifications
- Feature documentation and PRDs (where acceptance criteria exist)

**Do not use** this skill for:
- Reviewing actual code (use a code reviewer)
- Performance optimization reviews
- Security audits (use a dedicated security review)
- Architecture and design decisions (use an architecture review)

---

## Definition of Done (Stop Conditions)

A plan review is “done” when:

1. **Every acceptance criterion is testable**  
   Each acceptance criterion maps to at least one validation step.

2. **Validation is complete enough to start coding**  
   Manual validation covers key scenarios, and automated tests are specified or explicitly deferred.

3. **Integration points are explicit and validated**  
   Anything the change touches has a corresponding verification step.

4. **Open questions are documented**  
   Any ambiguity is called out as a decision, not silently assumed.

5. **Top risks are listed with mitigations**  
   At least the top 3 risks are identified and tied to validation.

Once these five conditions are met, **stop expanding**.

---

## Core Review Process (Always Run)

### Step 1: Acceptance Criteria Testability

For each acceptance criterion, check:

- ✅ Is it specific and measurable?
- ✅ Can it be validated manually?
- ✅ Can it be validated automatically (unit, integration, UI)?
- ❓ If not testable, what decision or rewrite is required?

**Common gaps to flag**
- Vague language: “works”, “handles gracefully”, “clearly”, “fast”
- Unbounded scope: “supports all formats”, “all edge cases”
- Missing constraints: timeouts, retries, limits, permissions

**Rule:** Do not invent new product requirements.  
Only make existing requirements testable, or flag them as ambiguous.

---

### Step 2: Manual Validation Completeness

Manual validation should cover:

- **Happy path**
- **At least one realistic failure path**
- **At least one integration touchpoint**
- **Expected results**, not just “verify it works”

Manual validation steps should include:
- Preconditions (environment, flags, account state, data)
- Step by step actions
- Expected outcome
- Observability (logs, metrics, UI state, API responses)

---

### Step 3: Automated Test Expectations (Actionable)

Convert vague testing statements into explicit expectations:

- **Where tests live** (file or suite)
- **What is covered** (scenario level)
- **What is mocked vs real** (dependency strategy)

Examples:
- “Unit tests cover X” → list concrete test cases
- “Integration tests exist” → describe workflow boundaries (POST → GET → UPDATE)
- “Error cases are tested” → specify which errors and expected responses

**Naming guidance**
Use descriptive names, consistent with existing patterns:
- `test_create_resource_when_valid_returns_201()`
- `test_create_resource_when_missing_field_returns_400()`
- `test_service_retries_on_timeout_then_fails()`

---

### Step 4: Integration Points and Required Validations

List the systems touched by this change, then for each one specify:
- What could break
- How we validate it

Examples of integration points:
- API endpoints and clients
- Persistent storage
- Configuration and flags
- UI surfaces
- External dependencies (third party APIs, framewors)

**Outcome:** a short “integration validation checklist” tied to the plan.

---

## Optional Modules (Only If Relevant)

Use these checklists when the plan includes the relevant domain.

### Module: Configuration and Precedence

Verify:
- Which sources exist (env, file json, DB, secret manager, etc.)
- Precedence rules are explicitly defined
- Behavior when a value is missing, invalid, or changed

Add validations:
- precedence tests
- unset / rollback behavior
- failure handling

---

### Module: Backward Compatibility and Safe Defaults

Verify:
- old clients or old data still function
- do we need to be backwards compatible, or is it OK to make breaking changes
  (KISS, SRP, DRY, YAGNI - prefer to keep logic simple)
- missing fields have defaults
- schema changes are safe or migrated

Add validations:
- old payloads accepted or rejected explicitly
- old reads remain stable
- compatibility expectations are documented

---

### Module: External Dependency Failure

Verify:
- timeouts and retries are specified
- errors are surfaced cleanly
- user experience is defined during partial outages

Add validations:
- simulate dependency outage
- verify error messages
- verify no infinite retry loops

---

### Module: UI Workflow (If Applicable)

Verify:
- loading state is defined
- error state is defined
- empty state is defined
- state consistency matches API behavior

Add validations:
- slow API simulation
- error responses
- empty dataset behavior

---

### Module: Security and Secrets Hygiene

Verify:
- no secrets are logged
- no secrets are returned in API responses
- sensitive values are masked consistently

Add validations:
- redaction tests
- response content checks
- log output checks

---

## Risk Scoring (PM + Principal Engineer Friendly)

For each major risk, record:

- **Impact:** Low / Medium / High
- **Likelihood:** Low / Medium / High
- **Mitigation:** what test or validation catches it

Example:

- Risk: “Old clients break due to response change”  
  Impact: High  
  Likelihood: Medium  
  Mitigation: integration test with old payload, contract tests

Keep this list short: top 3 to 5 risks.

---

## Default Review Output (Short)

Use this structure by default:

```markdown
# Plan Review: [Feature Name]

## 1. Readiness Verdict
- Verdict: ✅ Ready to implement / 🟡 Ready after fixes / 🔴 Not ready
- Why: [1 to 3 bullets]

## 2. Open Questions To Resolve Before Coding (Decisions needed)
- [ ] Item 1
- [ ] Item 2

## 3. Open Requirements
### Must resolve before coding (blocking)
- Items where the acceptance criterion itself is missing, ambiguous, or untestable

### Resolve during implementation (non-blocking)
- Items where the WHAT is clear from the acceptance criteria but the exact HOW is an implementation detail
- Example: "a test seam is needed for year injection" is non-blocking if the AC already says "rejects non-2026 year before writes"
- Example: "which exact mock library to use" is non-blocking

## 4. Validation Plan Summary
### Manual
- Scenario: ...
   - [ ] Item 1
   - [ ] Item 2
   ...
- Scenario: ...
   ...

### Automated
- Unit: ...
   - [ ] Item 1
   - [ ] Item 2
   ...
- Integration: ...
   - [ ] Item 1
   - [ ] Item 2
   ...
- UI (if applicable): ...
   - [ ] Item 1
   - [ ] Item 2
   ...

## 5. Top Risks and Mitigations
- Risk: ...
  - Impact: ...
  - Likelihood: ...
  - Mitigation: ...
```

---

## Expanded Output (Only When Requested)

If the reviewer requests a full deep dive, expand into:
- Acceptance criteria gaps
- Manual validation gaps
- Automated testing specifications
- Integration validation checklist
- Compatibility and migration notes
- Prioritized recommendations
- Unresolved question and for each one, iterate with reviewer/human until decision is made, which is then documented in the plan.

---

## Principles

1. **Testability first:** Every acceptance criterion must be testable
2. **Specificity over generality:** “Test X” is not enough, specify what and how
3. **Stop conditions matter:** Finish when the plan is shippable, not perfect
4. **Integration awareness:** Verify what could break outside the happy path
5. **Do not invent requirements:** Flag ambiguity, do not hallucinate scope
6. **Prefer actionable deltas:** Smallest set of changes that unblock coding


## Automated Test Expectations

**Requirement:** For each Acceptance Criterion, provide at least **one explicit example test case** when feasible. If a criterion cannot be reasonably automated, mark it as **Deferred** and include the reason and what manual validation will cover.

When a test approach requires codebase investigation to determine the mechanism (e.g., how to inject a test seam, which mock strategy to use), classify it as "resolve during implementation" rather than blocking — as long as the plan states the acceptance criterion the test must satisfy.
