---
name: spec-verification
description: Verify generated specification documents for context preservation and quality issues. Automatically triggered after document generation. Checks that upstream requirements are preserved and identifies common specification problems.
---

# Spec Verification Skill

Verify specification documents for context preservation (nothing important lost from upstream docs) and quality issues (vague language, missing rationale, untestable criteria, etc.).

## When This Skill Runs

This skill runs automatically after generating:
- `TECHNICAL_SPEC.md` (verifies against `PRODUCT_SPEC.md`)
- `EXECUTION_PLAN.md` (verifies against `TECHNICAL_SPEC.md`)
- `FEATURE_TECHNICAL_SPEC.md` (verifies against `FEATURE_SPEC.md`)
- Feature `EXECUTION_PLAN.md` (verifies against `FEATURE_TECHNICAL_SPEC.md`)

Can also be invoked manually via `/verify-spec <document-type>`.

## Workflow Overview

```
1. Identify document type and locate upstream document(s)
2. Context Preservation Check: Extract key items from upstream, verify in current
3. Quality Check: Scan for common specification anti-patterns
4. Present issues inline with resolution options
5. Collect user choices for each CRITICAL issue
6. Apply fixes to document(s)
7. Re-verify (max 2 iterations, then escalate)
```

Copy this checklist and track progress:

```
Spec Verification Progress:
- [ ] Step 1: Detect document type
- [ ] Step 2: Context preservation check
- [ ] Step 3: Quality check
- [ ] Step 4: Present issues
- [ ] Step 5: Collect user choices
- [ ] Step 6: Apply fixes
- [ ] Step 7: Re-verify
```

## Step 1: Document Type Detection

Determine what's being verified and its upstream dependencies:

| Document Being Verified | Upstream Document(s) | Generation Prompt |
|------------------------|---------------------|-------------------|
| `TECHNICAL_SPEC.md` | `PRODUCT_SPEC.md` | `TECHNICAL_SPEC_PROMPT.md` |
| `EXECUTION_PLAN.md` (greenfield) | `TECHNICAL_SPEC.md`, `PRODUCT_SPEC.md` | `GENERATOR_PROMPT.md` |
| `FEATURE_TECHNICAL_SPEC.md` | `FEATURE_SPEC.md` | `FEATURE_TECHNICAL_SPEC_PROMPT.md` |
| `EXECUTION_PLAN.md` (feature) | `FEATURE_TECHNICAL_SPEC.md`, `FEATURE_SPEC.md` | `FEATURE_EXECUTION_PLAN_GENERATOR_PROMPT.md` |
| `PRODUCT_SPEC.md` | None (quality check only) | `PRODUCT_SPEC_PROMPT.md` |
| `FEATURE_SPEC.md` | None (quality check only) | `FEATURE_SPEC_PROMPT.md` |

## Step 2: Context Preservation Check

### 2a: Extract Key Items from Upstream Document

Read the upstream document and extract:

**From PRODUCT_SPEC.md / FEATURE_SPEC.md:**
- [ ] Core features (each listed feature)
- [ ] User flows (each step-by-step flow)
- [ ] Constraints (security, performance, accessibility, etc.)
- [ ] Edge cases explicitly mentioned
- [ ] Non-functional requirements
- [ ] Integration points (feature only)
- [ ] Backwards compatibility concerns (feature only)

**From TECHNICAL_SPEC.md / FEATURE_TECHNICAL_SPEC.md:**
- [ ] Architecture decisions
- [ ] Data model entities and relationships
- [ ] API endpoints/contracts
- [ ] Technical constraints
- [ ] Implementation sequence items
- [ ] Edge cases and boundary conditions

Create a checklist of extracted items with unique IDs (e.g., `CTX-001`, `CTX-002`).

### 2b: Verify Each Item in Downstream Document

For each extracted item, check if it appears in the downstream document:

| Status | Meaning |
|--------|---------|
| **PRESENT** | Item found with clear reference |
| **CONSOLIDATED** | Item merged into broader item (acceptable) |
| **DEFERRED** | Explicitly marked as future/out-of-scope (acceptable) |
| **MISSING** | Not found, not deferred - **FLAG AS CRITICAL** |

### 2c: Context Preservation Output

```
CONTEXT PRESERVATION CHECK
==========================
Upstream: PRODUCT_SPEC.md
Downstream: TECHNICAL_SPEC.md

Extracted Items: 12
Present: 9
Consolidated: 2
Deferred: 0
Missing: 1 <- CRITICAL

MISSING ITEMS
-------------
[CTX-007] "Rate limiting for API endpoints"
  - Source: PRODUCT_SPEC.md, Section "Security Requirements"
  - Not found in TECHNICAL_SPEC.md
  - Not marked as deferred
```

## Step 3: Quality Check

Scan the document for common anti-patterns. Be **conservative** - only flag obvious, clear problems.

### Universal Quality Checks (All Documents)

| ID | Check | Pattern to Detect | Severity |
|----|-------|-------------------|----------|
| Q-001 | Vague/Unmeasurable Language | "fast", "user-friendly", "intuitive", "simple", "easy", "quickly", "responsive" without metrics | CRITICAL |
| Q-002 | Subjective Terms | "better", "improved", "enhanced" without baseline | CRITICAL |
| Q-003 | Missing Rationale | Architecture/tech decisions without "because" or "to enable" | MAJOR |
| Q-004 | Scope Creep | Items in downstream not traceable to upstream | CRITICAL |
| Q-005 | Implicit Assumptions | Decisions that assume unstated context | MAJOR |
| Q-006 | Conflicting Requirements | Two statements that cannot both be true | CRITICAL |

### PRODUCT_SPEC.md / FEATURE_SPEC.md Quality Checks

| ID | Check | Pattern to Detect | Severity |
|----|-------|-------------------|----------|
| Q-PS-001 | Missing User Flow | Feature mentioned without step-by-step interaction | MAJOR |
| Q-PS-002 | Undefined Edge Cases | Only happy path described | MAJOR |
| Q-PS-003 | Unbounded Scope | "all", "any", "every" without limits | CRITICAL |
| Q-PS-004 | Missing Non-Functional | No mention of performance, security, or accessibility | MAJOR |

### TECHNICAL_SPEC.md / FEATURE_TECHNICAL_SPEC.md Quality Checks

| ID | Check | Pattern to Detect | Severity |
|----|-------|-------------------|----------|
| Q-TS-001 | Architecture Without Justification | Pattern chosen without tradeoff discussion | MAJOR |
| Q-TS-002 | Incomplete Data Model | Entity without fields, types, or constraints | CRITICAL |
| Q-TS-003 | Undefined API Contract | Endpoint without request/response shape | CRITICAL |
| Q-TS-004 | Orphaned Dependency | External service mentioned but never integrated | MAJOR |
| Q-TS-005 | Implementation Detail | Code snippets or specific implementation in spec | MINOR |

### EXECUTION_PLAN.md Quality Checks

| ID | Check | Pattern to Detect | Severity |
|----|-------|-------------------|----------|
| Q-EP-001 | Untestable Acceptance Criteria | Criterion that can't be verified programmatically | CRITICAL |
| Q-EP-002 | Missing Task Dependency | Task references another task's output without declared dependency | CRITICAL |
| Q-EP-003 | Circular Dependency | A depends on B depends on C depends on A | CRITICAL |
| Q-EP-004 | Orphaned Spec Reference | Task references spec section that doesn't exist | CRITICAL |
| Q-EP-005 | Insufficient Criteria | Task has fewer than 3 acceptance criteria | MAJOR |
| Q-EP-006 | Oversized Task | Task description suggests >1 day of work | MAJOR |
| Q-EP-007 | Vague Acceptance Criterion | Uses "should", "properly", "correctly" without specifics | CRITICAL |
| Q-EP-008 | Missing Verification Metadata | Acceptance criterion missing verification type or method | CRITICAL |

### Quality Check Output

```
QUALITY CHECK
=============
Document: TECHNICAL_SPEC.md

Issues Found: 3

[Q-001] CRITICAL: Vague Language
  Location: Section "Performance Requirements"
  Text: "API responses should be fast"
  Problem: "fast" is unmeasurable

[Q-TS-003] CRITICAL: Undefined API Contract
  Location: Section "API Endpoints", /api/users
  Text: "POST /api/users - Creates a new user"
  Problem: No request body or response shape defined

[Q-003] MAJOR: Missing Rationale
  Location: Section "Architecture"
  Text: "Use Redis for caching"
  Problem: No explanation of why Redis vs alternatives
```

## Step 4: Issue Presentation

Present all CRITICAL issues inline. Do NOT present MAJOR issues unless there are no CRITICAL issues.

### Issue Presentation Format

For each CRITICAL issue, present:

```
────────────────────────────────────────────────────────────
ISSUE 1 of N: [Issue ID] - [Issue Type]
────────────────────────────────────────────────────────────
Location: [Document], [Section/Line]
Problem: [Clear description]
Text: "[The problematic text]"

How would you like to resolve this?
```

Then use AskUserQuestion with appropriate options based on issue type.

### Resolution Options by Issue Type

**Vague/Unmeasurable Language (Q-001, Q-EP-007):**
- Option 1: Use suggested specific wording (provide suggestion)
- Option 2: Specify your own measurable target
- Option 3: Mark as intentionally vague (adds TODO for later)
- Option 4: Remove this requirement

**Missing from Upstream / Scope Creep (CTX-*, Q-004):**
- Option 1: Add to upstream document (expands scope)
- Option 2: Remove from current document
- Option 3: Mark as explicitly deferred

**Missing Rationale (Q-003):**
- Option 1: Add suggested rationale (provide suggestion)
- Option 2: Provide your own rationale
- Option 3: Remove this decision

**Undefined Contract/Model (Q-TS-002, Q-TS-003):**
- Option 1: Define now (will prompt for details)
- Option 2: Mark as TBD with TODO

**Untestable Criteria (Q-EP-001):**
- Option 1: Use suggested testable version (provide suggestion)
- Option 2: Rewrite criterion
- Option 3: Remove criterion

**Missing Verification Metadata (Q-EP-008):**
- Option 1: Add suggested verification type + method (recommended)
- Option 2: Mark as MANUAL with a reason
- Option 3: Remove criterion

**Conflicting Requirements (Q-006):**
- Option 1: Keep first, remove second
- Option 2: Keep second, remove first
- Option 3: Clarify intent (will prompt for resolution)

## Step 5: Collect User Choices

Use AskUserQuestion to collect resolution for each CRITICAL issue.

Example:
```
questions:
  - question: "API responses should be fast' is unmeasurable. How should we fix this?"
    header: "Vague term"
    options:
      - label: "API responses return within 200ms p95 (Recommended)"
        description: "Sets a specific, measurable latency target"
      - label: "Specify custom target"
        description: "You'll provide your own performance number"
      - label: "Remove requirement"
        description: "Delete this requirement entirely"
```

If user selects "Other" or a custom option, prompt for their input.

## Step 6: Apply Fixes

For each collected resolution:

1. **Read the target document**
2. **Locate the problematic text** (use exact match from issue)
3. **Apply the fix** using Edit tool
4. **Verify the edit** — Re-read the edited section to confirm the change was applied correctly. If the Edit tool reported no match or the content is unchanged, retry with corrected `old_string`.
5. **For upstream document changes**: Require explicit confirmation before editing

### Fix Application Rules

- Make minimal edits - only change what's necessary
- Preserve document formatting and structure
- For additions, place in appropriate section
- For removals, ensure no orphaned references remain

### Upstream Document Edits

When a fix requires editing an upstream document (e.g., adding a requirement to PRODUCT_SPEC.md):

```
This fix requires editing the upstream document.

Document: PRODUCT_SPEC.md
Change: Add "Rate limiting: 100 requests/minute per user" to Security Requirements section

Confirm this upstream change? (This expands project scope)
```

Only proceed with explicit confirmation.

## Step 7: Re-Verification

After applying fixes:

1. **Run context preservation check again** on modified documents
2. **Run quality check again** on modified documents
3. **If new CRITICAL issues**: Present them (max 2 total iterations)
4. **If still issues after 2 iterations**: Escalate to user

### Escalation Format

```
VERIFICATION INCOMPLETE
=======================
After 2 fix iterations, these issues remain:

[Q-001] Vague Language in Section X
  - Attempted fixes: [list]
  - Recommendation: Manual review needed

Proceeding with current state. Review flagged sections before execution.
```

## Step 8: Final Report

```
SPECIFICATION VERIFICATION COMPLETE
===================================
Document: TECHNICAL_SPEC.md
Status: PASSED | PASSED WITH NOTES | NEEDS REVIEW

Context Preservation:
  - Items checked: 12
  - All present or explicitly deferred: Yes/No

Quality Check:
  - Critical issues found: 2
  - Critical issues resolved: 2
  - Major issues noted: 1 (non-blocking)

Fixes Applied:
  - TECHNICAL_SPEC.md: 2 edits
  - PRODUCT_SPEC.md: 0 edits

Notes:
  - [Q-003] Missing rationale for Redis - marked for future documentation

Ready to proceed: Yes/No
```

## Conservative Flagging Principles

To avoid noisy reports:

1. **Only flag obvious problems** - If it requires interpretation, skip it
2. **Prefer false negatives** - Missing a minor issue is better than crying wolf
3. **Context matters** - "Fast" in a performance section is vague; in casual description, maybe not
4. **Trust consolidation** - If upstream item seems covered by broader downstream item, mark as CONSOLIDATED
5. **Limit output** - Maximum 5 CRITICAL issues per verification. If more exist, show top 5 by severity

## Severity Definitions

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Will cause implementation problems or lost requirements | BLOCKS - must resolve |
| MAJOR | Should be addressed but won't break implementation | Note for user, continue |
| MINOR | Style/preference issue | Ignore unless no other issues |

## Manual Invocation

The skill can be invoked manually:

```
/verify-spec technical-spec     # Verify TECHNICAL_SPEC.md
/verify-spec execution-plan     # Verify EXECUTION_PLAN.md
/verify-spec feature-technical  # Verify FEATURE_TECHNICAL_SPEC.md
/verify-spec feature-plan       # Verify feature EXECUTION_PLAN.md
/verify-spec product-spec       # Quality check only (no upstream)
/verify-spec feature-spec       # Quality check only (no upstream)
```

## Example Workflow

**Input:** Just generated `TECHNICAL_SPEC.md` from `PRODUCT_SPEC.md`

**Step 1:** Detect document type = TECHNICAL_SPEC, upstream = PRODUCT_SPEC

**Step 2:** Extract 8 key items from PRODUCT_SPEC:
- CTX-001: User authentication
- CTX-002: Data export feature
- CTX-003: Rate limiting
- ... (5 more)

Verify in TECHNICAL_SPEC:
- CTX-001: PRESENT (Section "Authentication")
- CTX-002: PRESENT (Section "Export API")
- CTX-003: MISSING <- Flag

**Step 3:** Quality check finds:
- Q-001: "API should respond quickly" <- CRITICAL
- Q-TS-003: POST /users has no request shape <- CRITICAL

**Step 4-5:** Present 3 issues, collect resolutions:
- CTX-003: User chooses "Add to TECHNICAL_SPEC.md"
- Q-001: User chooses "200ms p95"
- Q-TS-003: User provides request/response shape

**Step 6:** Apply 3 edits to TECHNICAL_SPEC.md

**Step 7:** Re-verify - all clear

**Step 8:** Report PASSED, ready to proceed

## When Verification Cannot Complete

**If issues persist after 2 fix iterations:**
- Stop attempting automatic fixes
- Report: "Verification loop limit reached (2 iterations)"
- List all remaining issues with their current state
- Recommend: "Manual review required for these {N} issues"
- Ask user: "Continue with known issues or pause for manual resolution?"

**If upstream document is missing or unreadable:**
- Skip context preservation check
- Proceed with quality checks only
- Report: "Context preservation skipped (upstream document unavailable)"
- Note which checks were limited

**If user declines to resolve CRITICAL issues:**
- Do NOT silently proceed
- Report: "Proceeding with {N} unresolved CRITICAL issues"
- List the specific items that remain unresolved
- Warn about potential downstream impacts

**If document format prevents parsing:**
- Report: "Unable to parse document structure"
- List what could not be extracted
- Suggest: "Check document follows expected markdown format"
- Provide manual verification steps as fallback
