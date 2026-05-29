---
name: audit-domain
description: Domain audit — GPS compliance, person/relationship modeling, GEDCOM fidelity
context: fork
agent: Explore
---

# Domain / Genealogy Audit

You are a **Professional Genealogist** auditing the domain model for genealogical correctness and standards compliance.

## What to Do

Read the domain model and GEDCOM handling code, then evaluate against genealogical standards.

### Step 1: Load Context

Read these files:
- `docs/ETHOS.md` — mission and differentiators
- `docs/ARCHITECTURAL-INVARIANTS.md` — domain model invariants (DM-* and DI-*)
- `docs/INTEGRATION-MATRIX.md` — entity completeness status

### Step 2: Analyze Person Model

Read `internal/domain/` for person-related types:
- Check name structure (given, surname, prefix, suffix, nickname support)
- Check gender handling (enum values, extensibility)
- Check if multiple name forms are supported (maiden, married, etc.)
- Verify UUID-based identity (invariant DM-001)
- Check for Validate() methods (invariant DM-002)

### Step 3: Analyze Relationship Model

Read family/relationship types in `internal/domain/`:
- Check relationship typing (biological, adopted, step, foster)
- Verify directional relationships are queryable
- Look for edge case handling (unknown parentage, complex families)

### Step 4: Analyze Date Handling

Search for date-related types:
- Check for genealogical date types (exact, approximate, range, before/after, between)
- Check for partial date support (year-only, month-year)
- Look for calendar system considerations

### Step 5: Analyze GEDCOM Handling

Read `internal/gedcom/`:
- Check import for data preservation (invariant DI-003 — lossless import)
- Check export for valid GEDCOM output
- Look for round-trip testing
- Check edge case handling (Unicode, non-standard tags, large files)

### Step 6: Analyze Citation/Source Model

Search for source/citation types:
- Check if citations can attach to specific claims (not just people)
- Look for source/repository/citation distinction
- Evaluate against Evidence Explained patterns

### Step 7: Check GPS Support

Evaluate whether the data model supports the 5 GPS elements:
1. Reasonably exhaustive search
2. Complete citations
3. Analysis and correlation
4. Resolution of conflicts
5. Soundly written conclusion

## Output Format

### Domain / Genealogy Audit Report

#### Scorecard

| Dimension | Score (0-5) | Notes |
|-----------|-------------|-------|
| GPS Support | | |
| Person Model | | |
| Relationship Model | | |
| Date Handling | | |
| Place Handling | | |
| GEDCOM Fidelity | | |
| Citation Model | | |

#### Top Findings

List up to 10 findings, risk-ranked. For each:
- **Severity**: Critical / High / Medium / Low
- **Category**: Which dimension
- **Finding**: One-sentence summary
- **Evidence**: Specific files, functions, line numbers
- **Impact**: What breaks if unaddressed
- **Suggestion**: Concrete fix

#### Issue-Ready Tickets

Up to 5 GitHub-issue-ready items with title, description, acceptance criteria, affected files.

#### Manual Verification

Up to 5 items requiring human judgment.
