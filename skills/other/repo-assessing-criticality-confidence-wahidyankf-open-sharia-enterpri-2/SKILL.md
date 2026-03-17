---
name: repo-assessing-criticality-confidence
description: Universal classification system for checker and fixer agents using orthogonal criticality (CRITICAL/HIGH/MEDIUM/LOW importance) and confidence (HIGH/MEDIUM/FALSE_POSITIVE certainty) dimensions. Covers priority matrix (P0-P4), execution order, dual-label pattern for verification status, standardized report format, and domain-specific examples. Essential for implementing checker/fixer agents and processing audit reports
---

# Criticality-Confidence System Skill

## Purpose

This Skill provides comprehensive guidance on the **criticality-confidence classification system** used by all checker and fixer agents in the repository.

**When to use this Skill:**

- Implementing checker agents (categorizing findings)
- Implementing fixer agents (assessing confidence, determining priority)
- Processing audit reports
- Understanding priority execution order (P0-P4)
- Working with dual-label patterns (verification + criticality)
- Writing standardized audit reports

## Core Concepts

### Two Orthogonal Dimensions

The system uses TWO independent dimensions:

**Criticality** (CRITICAL/HIGH/MEDIUM/LOW):

- Measures **importance and urgency**
- Answers: "How soon must this be fixed?"
- Set by **checker agents** during validation
- Objective criteria based on impact

**Confidence** (HIGH/MEDIUM/FALSE_POSITIVE):

- Measures **certainty and fixability**
- Answers: "How certain are we this needs fixing?"
- Assessed by **fixer agents** during re-validation
- Based on re-validation results

**Key Insight**: These dimensions are ORTHOGONAL - they measure different things and combine to determine priority.

### Four Criticality Levels

**🔴 CRITICAL** - Breaks functionality, blocks users, violates mandatory requirements

- Missing required fields (build breaks)
- Broken internal links (404 errors)
- Security vulnerabilities
- Syntax errors preventing execution
- MUST requirement violations

**🟠 HIGH** - Significant quality degradation, convention violations

- Wrong format (system functions but non-compliant)
- Accessibility violations (WCAG AA failures)
- SHOULD requirement violations
- Incorrect link format (works but violates convention)

**🟡 MEDIUM** - Minor quality issues, style inconsistencies

- Missing optional fields (minimal impact)
- Formatting inconsistencies
- Suboptimal structure (still functional)
- MAY/OPTIONAL requirement deviations

**🟢 LOW** - Suggestions, optimizations, enhancements

- Performance optimizations
- Alternative implementation suggestions
- Future-proofing recommendations
- Best practice suggestions (not requirements)

### Three Confidence Levels

**HIGH** - Objectively correct, safe to auto-fix

- Re-validation confirms issue exists
- Issue is objective and verifiable
- Fix is straightforward and safe
- No ambiguity, low risk

**MEDIUM** - Uncertain, requires manual review

- Re-validation is unclear or ambiguous
- Issue is subjective (human judgment needed)
- Multiple valid interpretations
- Context-dependent decision

**FALSE_POSITIVE** - Checker was wrong

- Re-validation clearly disproves issue
- Content is actually compliant
- Checker's detection logic flawed
- Report to improve checker

## Criticality × Confidence Priority Matrix

### Decision Matrix

| Criticality     | HIGH Confidence                                  | MEDIUM Confidence               | FALSE_POSITIVE                                    |
| --------------- | ------------------------------------------------ | ------------------------------- | ------------------------------------------------- |
| 🔴 **CRITICAL** | **P0** - Auto-fix immediately (block deployment) | **P1** - URGENT manual review   | Report with CRITICAL context (fix urgently)       |
| 🟠 **HIGH**     | **P1** - Auto-fix after P0                       | **P2** - Standard manual review | Report with HIGH context (fix soon)               |
| 🟡 **MEDIUM**   | **P2** - Auto-fix after P1 (user approval)       | **P3** - Optional review        | Report with MEDIUM context (note for improvement) |
| 🟢 **LOW**      | **P3** - Batch fixes (user decides when)         | **P4** - Suggestions only       | Report with LOW context (informational)           |

### Priority Levels Explained

- **P0** (Blocker): MUST fix before any publication/deployment
- **P1** (Urgent): SHOULD fix before publication, can proceed with approval
- **P2** (Normal): Fix in current cycle when convenient
- **P3** (Low): Fix in future cycle or batch operation
- **P4** (Optional): Suggestion only, no action required

### Execution Order for Fixers

Fixer agents MUST process findings in strict priority order:

```
1. P0 fixes (CRITICAL + HIGH) → Auto-fix, block if fails
2. P1 fixes (HIGH + HIGH OR CRITICAL + MEDIUM) → Auto-fix HIGH+HIGH, flag CRITICAL+MEDIUM
3. P2 fixes (MEDIUM + HIGH OR HIGH + MEDIUM) → Auto-fix MEDIUM+HIGH if approved, flag HIGH+MEDIUM
4. P3-P4 fixes (LOW priority) → Include in summary only
```

## Checker Agent Responsibilities

### Categorizing Findings by Criticality

**Decision tree**:

```
1. Does it BREAK functionality or BLOCK users?
   YES → CRITICAL
   NO → Continue

2. Does it cause SIGNIFICANT quality degradation or violate DOCUMENTED conventions?
   YES → HIGH
   NO → Continue

3. Is it a MINOR quality issue or style inconsistency?
   YES → MEDIUM
   NO → Continue

4. Is it a suggestion, optimization, or future consideration?
   YES → LOW
```

### Standardized Report Format

**Report header**:

```markdown
# [Agent Name] Audit Report

**Audit ID**: {uuid-chain}\_\_{timestamp}
**Scope**: {scope-description}
**Files Checked**: N files
**Audit Start**: YYYY-MM-DDTHH:MM:SS+07:00
**Audit End**: YYYY-MM-DDTHH:MM:SS+07:00

---

## Executive Summary

- 🔴 **CRITICAL Issues**: X (must fix before publication)
- 🟠 **HIGH Issues**: Y (should fix before publication)
- 🟡 **MEDIUM Issues**: Z (improve when time permits)
- 🟢 **LOW Issues**: W (optional enhancements)

**Total Issues**: X + Y + Z + W = TOTAL

**Overall Status**: [PASS | PASS WITH WARNINGS | FAIL]

---
```

**Issue sections**:

````markdown
## 🔴 CRITICAL Issues (Must Fix)

**Count**: X issues found

---

### 1. [Issue Title]

**File**: `path/to/file.md:line`
**Criticality**: CRITICAL - [Why critical]
**Category**: [Category name]

**Finding**: [What's wrong]
**Impact**: [What breaks if not fixed]
**Recommendation**: [How to fix]

**Example**:

```yaml
# Current (broken)
[show broken state]

# Expected (fixed)
[show fixed state]
```
````

**Confidence**: [Will be assessed by fixer]

---

````

### Dual-Label Pattern

**Five agents require BOTH verification/status AND criticality**:

- `docs__checker` - [Verified]/[Error]/[Outdated]/[Unverified] + criticality
- `docs__tutorial-checker` - Verification labels + criticality
- `apps__ayokoding-web__facts-checker` - Verification labels + criticality
- `docs-link-general-checker` - [OK]/[BROKEN]/[REDIRECT] + criticality
- `apps__ayokoding-web__link-checker` - Status labels + criticality

**Format**:

```markdown
### 1. [Verification] - Issue Title

**File**: `path/to/file.md:line`
**Verification**: [Error] - [Reason for verification status]
**Criticality**: CRITICAL - [Reason for criticality level]
**Category**: [Category name]

**Finding**: [Description]
**Impact**: [Consequences]
**Recommendation**: [Fix]
**Verification Source**: [URL]

**Confidence**: [Will be assessed by fixer]
````

**Why dual labels?**

- **Verification** describes FACTUAL STATE ([Verified], [Error], etc.)
- **Criticality** describes URGENCY/IMPORTANCE (CRITICAL, HIGH, etc.)
- Both provide complementary information

## Fixer Agent Responsibilities

### Re-Validation Process

**CRITICAL**: Fixer agents MUST re-validate all findings before applying fixes.

**Never trust checker findings blindly.**

**Process**:

```
Checker Report → Read Finding → Re-execute Validation → Assess Confidence → Apply/Skip/Report
```

**Re-validation methods**:

- Extract frontmatter using same AWK pattern
- Check file existence for broken links
- Count objective metrics (lines, headings)
- Verify patterns (date format, naming)
- Analyze context (content type, directory)

### Confidence Assessment

**Step 1: Classify issue type**

- **Objective** (missing field, wrong format) → Potentially HIGH confidence
- **Subjective** (narrative flow, tone) → MEDIUM confidence

**Step 2: Re-validate finding**

- **Confirms issue** → Continue to Step 3
- **Disproves issue** → FALSE_POSITIVE

**Step 3: Assess fix safety**

- **Safe and unambiguous** → HIGH confidence (auto-fix)
- **Unsafe or ambiguous** → MEDIUM confidence (manual review)

### Priority-Based Execution

**P0 fixes first** (CRITICAL + HIGH confidence):

```python
for finding in critical_high_confidence:
    apply_fix(finding)  # Auto-fix immediately
    if fix_failed:
        block_deployment()  # Stop if P0 fails
```

**P1 fixes second**:

```python
# AUTO: HIGH criticality + HIGH confidence
for finding in high_high_confidence:
    apply_fix(finding)

# FLAG: CRITICAL + MEDIUM confidence (urgent review)
for finding in critical_medium_confidence:
    flag_for_urgent_review(finding)
```

**P2 fixes third**:

```python
# AUTO if approved: MEDIUM + HIGH
if user_approved_batch_mode:
    for finding in medium_high_confidence:
        apply_fix(finding)

# FLAG: HIGH + MEDIUM (standard review)
for finding in high_medium_confidence:
    flag_for_standard_review(finding)
```

**P3-P4 last**:

```python
# Include in summary only
for finding in low_priority:
    include_in_summary(finding)
```

### Fix Report Format

````markdown
# [Agent Name] Fix Report

**Source Audit**: {agent-family}**{uuid}**{timestamp}\_\_audit.md
**Fix Date**: YYYY-MM-DDTHH:MM:SS+07:00

---

## Execution Summary

- **P0 Fixes Applied**: X (CRITICAL + HIGH confidence)
- **P1 Fixes Applied**: Y (HIGH + HIGH confidence)
- **P1 Flagged for Urgent Review**: Z (CRITICAL + MEDIUM confidence)
- **P2 Fixes Applied**: W (MEDIUM + HIGH confidence)
- **P2 Flagged for Standard Review**: V (HIGH + MEDIUM confidence)
- **P3-P4 Suggestions**: U (LOW priority)
- **False Positives Detected**: T

---

## P0 Fixes Applied (CRITICAL + HIGH Confidence)

### 1. [Issue Title]

**File**: `path/to/file.md`
**Criticality**: CRITICAL - [Why critical]
**Confidence**: HIGH - [Why confident]
**Fix Applied**: [What was changed]

**Before**:

```yaml
[broken state]
```

**After**:

```yaml
[fixed state]
```
````

---

[... P1, P2, P3-P4 sections ...]

---

## False Positives Detected

### 1. [Issue Title]

**File**: `path/to/file.md`
**Checker Finding**: [What checker reported]
**Re-validation**: [What fixer found]
**Conclusion**: FALSE_POSITIVE
**Reason**: [Why checker was wrong]

**Recommendation for Checker**:
[How to improve checker logic]

---

````

## Domain-Specific Examples

### Repository Governance (wow__rules-checker)

**CRITICAL**:
- Missing `subcategory` field in convention (breaks organization)
- Agent `name` doesn't match filename (discovery fails)
- YAML comment in agent frontmatter (parsing error)

**HIGH**:
- Missing "Principles Respected" section (traceability violation)
- Wrong file naming prefix (convention violation)

**MEDIUM**:
- Missing optional cross-reference
- Suboptimal section ordering

**LOW**:
- Suggest adding related links
- Consider alternative organization

### Hugo Content (ayokoding-web)

**CRITICAL**:
- Missing required `title` field (build fails)
- Invalid YAML syntax (parsing error)
- Broken internal link without language prefix (404)

**HIGH**:
- Missing `weight` field (navigation undefined)
- Wrong internal link format (relative vs absolute)
- Incorrect heading hierarchy (H3 before H2)

**MEDIUM**:
- Missing optional `description` field
- Suboptimal weight spacing

**LOW**:
- Suggest adding optional tags
- Consider alternative structure

### Documentation (docs__checker)

**CRITICAL**:
- [Error] Command syntax incorrect (verified via WebSearch)
- [BROKEN] Internal link to non-existent file
- Security vulnerability in code example

**HIGH**:
- [Outdated] Major version with breaking changes
- Passive voice in step-by-step instructions
- Wrong heading nesting (H1 → H3)

**MEDIUM**:
- [Unverified] External claim needs verification
- Missing optional code fence language tag

**LOW**:
- Suggest additional examples
- Consider adding diagram

## Common Patterns

### Pattern 1: Checker categorizing finding

```markdown
### 1. Missing Required Frontmatter Field

**File**: `apps/ayokoding-web/content/en/programming/python/_index.md:3`
**Criticality**: CRITICAL - Breaks Hugo build process
**Category**: Missing Required Field

**Finding**: Required `draft` field missing from frontmatter
**Impact**: Hugo build fails with "required field missing" error
**Recommendation**: Add `draft: false` to frontmatter
````

### Pattern 2: Fixer assessing confidence

```python
# Read checker finding
finding = "Missing `draft` field"

# Re-validate
frontmatter = extract_frontmatter(file)
draft_exists = "draft" in frontmatter  # Result: False (confirmed)

# Assess confidence
issue_type = "objective"  # Field either exists or doesn't
re_validation = "confirmed"  # Field is indeed missing
fix_safety = "safe"  # Adding missing field is straightforward

confidence = "HIGH"  # Objective, confirmed, safe → HIGH
priority = determine_priority("CRITICAL", "HIGH")  # → P0

# Apply fix
apply_fix(finding)
```

### Pattern 3: Dual-label finding

```markdown
### 1. [Error] - Command Syntax Incorrect

**File**: `docs/tutorials/tu__quick-start.md:42`
**Verification**: [Error] - Command syntax verified incorrect via WebSearch
**Criticality**: CRITICAL - Breaks user quick start experience
**Category**: Factual Error - Command Syntax

**Finding**: Installation command uses incorrect npm flag `--save-deps`
**Impact**: Users get command error, cannot complete setup
**Recommendation**: Change to `--save-dev`
**Verification Source**: https://docs.npmjs.com/cli/v9/commands/npm-install

**Confidence**: HIGH (verified via official docs)
```

## Best Practices

### For Checker Agents

**DO**:

- Use decision tree for consistent criticality assessment
- Document specific impact for each finding
- Provide clear, actionable recommendations
- Include examples showing broken vs fixed state
- Write findings progressively during execution

**DON'T**:

- Mix criticality levels in same report section
- Skip impact description
- Provide vague recommendations
- Forget to document verification source (for dual-label)

### For Fixer Agents

**DO**:

- ALWAYS re-validate before applying fixes
- Process findings in strict priority order (P0 → P1 → P2 → P3)
- Document confidence assessment reasoning
- Report false positives with improvement suggestions
- Group fixes by priority in report

**DON'T**:

- Trust checker findings without re-validation
- Apply fixes in discovery order (ignore priority)
- Skip MEDIUM confidence manual review flagging
- Apply P2 fixes without user approval

## Common Mistakes

### ❌ Mistake 1: Conflating verification with criticality

**Wrong**: [Error] is CRITICAL, [Verified] is LOW

**Right**: Verification describes WHAT (factual state), criticality describes HOW URGENT

### ❌ Mistake 2: File-level confidence instead of per-finding

**Wrong**: Overall file confidence HIGH

**Right**: Each finding assessed independently

### ❌ Mistake 3: Skipping re-validation

**Wrong**: Trust checker, apply fix directly

**Right**: Re-validate finding first, then assess confidence

### ❌ Mistake 4: Ignoring priority order

**Wrong**: Fix findings in discovery order

**Right**: Fix P0 first, then P1, then P2, then P3-P4

## Creating Domain-Specific Confidence Examples

Fixer agents should include domain-specific examples of HIGH/MEDIUM/FALSE_POSITIVE confidence assessments to guide re-validation decisions.

### Purpose of Domain Examples

**Why include domain-specific examples?**

- Provide concrete guidance for re-validation decisions
- Clarify what constitutes HIGH vs MEDIUM confidence in specific domain
- Help fixer agents make consistent confidence assessments
- Reduce ambiguity in edge cases
- Document domain conventions and patterns

**Where to include**: In fixer agent files (not in this Skill - keep examples domain-specific)

### Example Structure Template

```markdown
### Domain-Specific Confidence Examples

**HIGH Confidence** (Apply automatically):

- [Objective error type 1] verified by [verification method]
- [Objective error type 2] verified by [verification method]
- [Pattern-based error] verified by [pattern check]
- [File-based error] verified by [file check]

**MEDIUM Confidence** (Manual review):

- [Subjective issue 1] that may be [context-dependent reason]
- [Ambiguous issue] where [ambiguity explanation]
- [Quality judgment] requiring [human judgment reason]
- [Context-dependent issue] that could be [valid reason]

**FALSE_POSITIVE** (Report to checker):

- Checker flagged [correct thing] as incorrect ([reason for false positive])
- Checker reported [missing thing] that actually exists ([reason])
- Checker [misunderstood] [context explanation]
```

### Domain Examples by Agent Family

**docs-fixer** (Factual accuracy domain):

```markdown
**HIGH Confidence**:

- Broken command syntax verified by checker's cited sources
- Incorrect version number verified by checker's registry findings
- Wrong API method verified by checker's documentation review
- Broken internal link verified by file existence check

**MEDIUM Confidence**:

- Contradiction that may be context-dependent
- Outdated information where "outdated" is subjective
- Content duplication where duplication may be intentional

**FALSE_POSITIVE**:

- Checker flagged correct LaTeX as incorrect
- Checker flagged valid command as broken
```

**readme-fixer** (README quality domain):

```markdown
**HIGH Confidence**:

- Paragraph exceeding 5 lines (count is objective)
- Specific jargon patterns without context
- Acronym without expansion
- Passive voice patterns (pattern match)

**MEDIUM Confidence**:

- Overall tone assessment (subjective)
- Engagement quality (context-dependent)
- Sentence length appropriateness (judgment call)

**FALSE_POSITIVE**:

- Checker flagged technical term as jargon (domain-appropriate)
- Checker flagged intentional passive voice (style choice)
```

**docs-tutorial-fixer** (Tutorial quality domain):

```markdown
**HIGH Confidence**:

- Missing hands-on element verified by structure check
- Wrong tutorial type verified by content analysis
- Missing visual aid in complex section (objective criteria met)

**MEDIUM Confidence**:

- Narrative flow issues (subjective assessment)
- Pedagogical effectiveness (requires teaching expertise)
- Example clarity (reader-dependent)

**FALSE_POSITIVE**:

- Checker flagged advanced tutorial as beginner (correct level)
- Checker reported missing visual where text is sufficient
```

### Guidelines for Creating Examples

**Be Specific**:

- Use concrete error types from your domain
- Reference actual verification methods
- Include pattern examples
- Show real scenarios

**Cover Common Cases**:

- Include the 3-5 most common HIGH confidence scenarios
- Include 2-3 common MEDIUM confidence scenarios
- Include 2-3 common FALSE_POSITIVE scenarios
- Don't try to be exhaustive (guidelines, not rules)

**Keep It Actionable**:

- Focus on verification methods: "verified by [method]"
- Explain ambiguity: "where [reason for uncertainty]"
- Show reasoning: "that may be [valid reason]"

**Domain-Appropriate**:

- docs-fixer: Command syntax, versions, APIs, links
- readme-fixer: Jargon, paragraphs, tone, engagement
- tutorial-fixer: Hands-on elements, flow, visuals
- link-fixer: Path format, target existence, redirects
- structure-fixer: Folder patterns, weights, organization

### Placement in Agent Files

Add "Domain-Specific Confidence Examples" section:

- After confidence level definitions
- Before re-validation guidelines
- In fixer agent files (not checker files)

### Benefits

✅ Reduces ambiguity in confidence assessment
✅ Provides concrete guidance for edge cases
✅ Improves consistency across similar fixers
✅ Documents domain conventions
✅ Helps new fixer implementations

### Anti-Patterns

❌ **Too Generic**: Examples that could apply to any domain
❌ **Too Exhaustive**: Trying to cover every possible scenario
❌ **No Verification Method**: Not explaining how to verify
❌ **Missing Context**: Not explaining why something is MEDIUM
❌ **In Skill**: Domain examples belong in agents, not Skills

### Key Takeaways

- Include domain-specific examples in fixer agents
- Cover HIGH/MEDIUM/FALSE_POSITIVE confidence cases
- Use concrete scenarios from your domain
- Explain verification methods
- Keep examples actionable and specific
- Place in fixer agents, not in this Skill

## References

**Primary Conventions**:

- [Criticality Levels Convention](../../../governance/development/quality/criticality-levels.md) - Complete criticality system
- [Fixer Confidence Levels Convention](../../../governance/development/quality/fixer-confidence-levels.md) - Complete confidence system

**Related Conventions**:

- [Repository Validation Methodology](../../../governance/development/quality/repository-validation.md) - Standard validation patterns
- [Maker-Checker-Fixer Pattern](../../../governance/development/pattern/maker-checker-fixer.md) - Three-stage workflow

**Related Skills**:

- `wow__applying-maker-checker-fixer` - Understanding three-stage workflow
- `docs__validating-factual-accuracy` - Verification label system

**Related Agents**:

All 14 checker agents and 11 fixer agents use this system.

---

This Skill packages the critical criticality-confidence classification system for maintaining consistent quality validation and automated fixing. For comprehensive details, consult the primary convention documents.
