---
name: cursor-rules-review
description: Audit Cursor IDE rules (.mdc files) against quality standards using a 5-gate review process. Validates frontmatter (YAML syntax, required fields, description quality, triggering configuration), glob patterns (specificity, performance, correctness), content quality (focus, organization, examples, cross-references), file length (under 500 lines recommended), and functionality (triggering, cross-references, maintainability). Use when reviewing pull requests with Cursor rule changes, conducting periodic rule quality audits, validating new rules before committing, identifying improvement opportunities, preparing rules for team sharing, or debugging why rules aren't working as expected.
version: 1.0.0
---

# Cursor Rules Review

## Quick Start

**5-Gate Review Process:**

```
Rule File (.mdc)
    ↓
Gate 1: Frontmatter Review
    ↓ PASS
Gate 2: Glob Patterns Review
    ↓ PASS
Gate 3: Content Quality Review
    ↓ PASS
Gate 4: File Length Review
    ↓ PASS
Gate 5: Functionality Review
    ↓ PASS
✅ APPROVED
```

**Severity Levels:**

- **BLOCKER** - Must fix before merge (prevents rule from working)
- **CRITICAL** - Must fix before production (causes issues)
- **MAJOR** - Should fix (impacts quality significantly)
- **MINOR** - Nice to have (improvements)

---

## When to Load Additional References

The 5-gate review process below provides core checks. Load these references for detailed examples and checklists:

**For detailed examples of good and bad patterns:**

```
Read `~/.claude/skills/cursor-rules-review/references/EXAMPLES.md`
```

Use when: You need concrete examples of violations, want to see before/after comparisons, or need reference patterns

**For copy-paste review checklist:**

```
Read `~/.claude/skills/cursor-rules-review/references/CHECKLIST.md`
```

Use when: Performing systematic review, want a comprehensive checklist, or need to document findings

**For test scenarios and edge cases:**

```
Read `~/.claude/skills/cursor-rules-review/references/test-scenarios.md`
```

Use when: Testing rules, validating fixes, or handling complex edge cases

---

## 5-Gate Review Process (Quick Summary)

### Gate 1: Frontmatter Review

- **YAML Syntax**: Valid YAML with proper `---` delimiters (BLOCKER if invalid)
- **Required Fields**: `description` field present and under 1024 chars (BLOCKER if missing)
- **Description Quality**: Specific, third-person, explains WHAT and WHEN (MAJOR if vague)
- **Triggering Config**: Appropriate use of `alwaysApply`, `globs`, or manual-only (CRITICAL if incorrect)

### Gate 2: Glob Patterns Review

- **Specificity**: Patterns match intended files only, not overly broad (CRITICAL if too broad)
- **Performance**: Efficient patterns, not excessive count (MAJOR if >10 patterns)
- **Correctness**: Patterns work with `find` command, correct syntax (BLOCKER if broken)

### Gate 3: Content Quality Review

- **Single Responsibility**: Focused on one concern, split if multiple topics (MAJOR if mixed)
- **Organization**: Clear structure, logical flow, no redundancy (MAJOR if poor)
- **Examples**: Realistic good/bad patterns with explanations (MAJOR if missing)
- **Cross-References**: Valid `@` syntax, referenced rules exist (CRITICAL if broken)

### Gate 4: File Length Review

- **Recommended**: <300 lines optimal, 300-500 good, 500-750 acceptable
- **Action Required**: Split if >750 lines into base/advanced/examples (MAJOR if >1000)

### Gate 5: Functionality Review

- **Triggering Test**: Create test files, verify correct triggering (BLOCKER if doesn't trigger)
- **Cross-Reference Validation**: Verify referenced files exist (CRITICAL if broken)
- **Maintainability**: Clear, follows conventions, documented (MINOR if poor)

**For detailed checks, examples, and criteria for each gate:**

```
Read `~/.claude/skills/cursor-rules-review/references/GATE-REVIEWS.md`
```

Use when: Performing comprehensive review, need detailed validation criteria, or checking specific gate requirements

---

## Review Output Format

**Report Structure**: Summary table with gate-by-gate status, issues grouped by severity (BLOCKER → CRITICAL → MAJOR → MINOR), specific fixes with line numbers, and prioritized recommendations.

**For complete report template with examples:**

```
Read `~/.claude/skills/cursor-rules-review/references/REPORT-FORMAT.md`
```

Use when: Documenting review findings, creating comprehensive reports, or presenting results to team

---

## Best Practices

### 1. Start with Frontmatter

Always validate frontmatter first - if it's broken, nothing else matters.

### 2. Test Triggering Early

Create test files and verify the rule triggers as expected.

### 3. Use Consistent Severity

Apply severity levels consistently across reviews.

### 4. Provide Actionable Fixes

Every issue should have a clear fix recommendation.

### 5. Re-Review After Fixes

Always run review again after fixes to confirm resolution.

---

## Common Issues (Quick Reference)

### Rule Not Triggering

- **Symptoms**: Rule doesn't appear when expected, glob patterns look correct
- **Fix**: Test glob with `find`, verify YAML syntax, check file location, restart Cursor

### Context Bloat

- **Symptoms**: Too much context loaded, slow performance, irrelevant info in responses
- **Fix**: Make globs more specific, minimize `alwaysApply: true`, split large rules

### Broken Cross-References

- **Symptoms**: `@referenced-rule` doesn't load, errors in Cursor logs
- **Fix**: Verify filename case-sensitivity, ensure file exists, use correct `@filename` syntax

**For detailed troubleshooting with debug commands and comprehensive solutions:**

```
Read `~/.claude/skills/cursor-rules-review/references/TROUBLESHOOTING.md`
```

Use when: Debugging specific issues, need detailed diagnostic steps, or handling complex problems

---

## Quick Validation Commands

```bash
# Check frontmatter
head -n 10 .cursor/rules/rule-name.mdc

# Check file length
wc -l .cursor/rules/rule-name.mdc

# Test glob patterns
find . -path "**/Chart.yaml"

# Verify cross-references
grep "@" .cursor/rules/rule-name.mdc
ls .cursor/rules/referenced-rule.mdc

# For complete checklist, read references/CHECKLIST.md
```

---

## Related Skills

- **cursor-rules-writing**: Create new Cursor rules following best practices
- **skill-review**: Review Claude Code skills (different from Cursor rules)

---

**This skill should be reviewed quarterly for updates to align with latest Cursor IDE features.**
