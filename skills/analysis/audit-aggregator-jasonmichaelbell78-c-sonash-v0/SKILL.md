---
name: audit-aggregator
description: Aggregate and deduplicate findings from multiple audit reports
---

# Audit Aggregator Agent

**Purpose:** Merge findings from 6+ domain-specific audit reports into a single
comprehensive, priority-ranked report with cross-domain insights and
deduplication.

**Input:** Multiple audit report files (markdown format) **Output:**
`COMPREHENSIVE_AUDIT_REPORT.md` with executive summary, priority rankings, and
cross-cutting analysis

---

## Input Requirements

**Expected Files:**

- `docs/audits/comprehensive/audit-code-report.md`
- `docs/audits/comprehensive/audit-security-report.md`
- `docs/audits/comprehensive/audit-performance-report.md`
- `docs/audits/comprehensive/audit-documentation-report.md`
- `docs/audits/comprehensive/audit-refactoring-report.md`
- `docs/audits/comprehensive/audit-process-report.md`

**Required Format (in each report):**

Each individual audit report should contain findings in this structure:

```markdown
## Findings

### [ID] [Title] (Severity: S0-S3, Effort: E0-E3, Confidence: High/Medium/Low)

**File:** `path/to/file.ts:123` **Category:** [Category Name] **Description:**
[Detailed description] **Evidence:** [Code snippets, metrics, etc.]
**Recommendation:** [How to fix]
```

---

## Processing Steps

### Step 1: Parse All Reports

Read all 6 audit reports and extract findings into structured format:

```javascript
{
  id: "CODE-001",
  title: "Missing error handling",
  severity: "S1",
  effort: "E1",
  confidence: "High",
  file: "src/auth.ts",
  line: 45,
  category: "Code Quality",
  domain: "code",
  description: "...",
  evidence: "...",
  recommendation: "..."
}
```

**Parsing Rules:**

- **ID Format:** `{DOMAIN}-{NUMBER}` (e.g., CODE-001, SEC-012, PERF-003)
- **Severity:** S0 (Critical) > S1 (High) > S2 (Medium) > S3 (Low)
- **Effort:** E0 (Trivial) < E1 (Hours) < E2 (Day) < E3 (Major)
- **Confidence:** High > Medium > Low (affects priority weighting)
- **File:Line:** Extract from "File: \`path/to/file.ts:123\`" format

**Handle Missing Fields:**

- If severity missing → assume S2 (Medium)
- If effort missing → assume E1 (Hours)
- If confidence missing → assume Medium
- If file:line missing → categorize as "General" finding

---

### Step 2: Deduplicate Findings

**Deduplication Logic:**

Group findings by `(file, line)` pair:

```javascript
// Pseudo-code
const groups = groupBy(findings, (f) => `${f.file}:${f.line}`);

for (const group of groups) {
  if (group.length > 1) {
    // Multiple audits flagged same location
    merged = {
      id: `COMP-${nextId++}`, // New composite ID
      domains: group.map((f) => f.domain), // ["code", "security"]
      severity: maxSeverity(group), // Take worst severity
      effort: maxEffort(group), // Take highest effort estimate
      confidence: maxConfidence(group), // Take highest confidence
      title: mergeTitles(group), // Combine titles
      description: mergeDescriptions(group), // Combine contexts
      category: "Cross-Domain", // Flag as spanning multiple domains
      ...
    };
  }
}
```

**Merge Rules:**

- **Severity:** Take worst (S0 > S1 > S2 > S3)
- **Effort:** Take highest (E3 > E2 > E1 > E0)
- **Confidence:** Take highest (High > Medium > Low)
- **Title:** Combine unique titles (e.g., "Missing error handling + Exception
  vulnerability")
- **Description:** Concatenate all descriptions with domain labels
- **Category:** Change to "Cross-Domain" if 2+ domains

**Example Deduplication:**

```
Before:
  CODE-001: Missing error handling (S1, E1) at auth.ts:45
  SEC-012: Exception vulnerability (S0, E1) at auth.ts:45

After:
  COMP-001: Missing error handling + Exception vulnerability (S0, E1, Domains: 2)
    Category: Cross-Domain (Code + Security)
```

---

### Step 3: Identify Cross-Cutting Patterns

**Pattern Detection:**

**A. Hotspot Files** (appear in 3+ audits):

```javascript
// Count how many audits mention each file
const fileCounts = {};
for (const finding of findings) {
  fileCounts[finding.file] = (fileCounts[finding.file] || 0) + 1;
}

// Files with 3+ mentions
const hotspots = Object.entries(fileCounts)
  .filter(([file, count]) => count >= 3)
  .sort((a, b) => b[1] - a[1]);
```

**B. Related Findings** (fixing one helps another):

Look for pairs where:

- Same file, different concerns (e.g., performance + security in same function)
- Dependency chain (e.g., missing docs for complex code)
- Contradiction patterns (e.g., over-engineered simple function)

**C. Domain Overlaps:**

Count overlaps between domain pairs:

```
Security + Performance: 12 findings
Code + Refactoring: 18 findings
Documentation + Code: 8 findings
```

**D. Category Patterns:**

Group by category across domains:

```
Authentication: 5 findings (2 security, 2 code, 1 process)
Error Handling: 8 findings (3 code, 3 security, 2 performance)
Testing: 12 findings (6 code, 4 refactoring, 2 process)
```

---

### Step 4: Priority Ranking

**Priority Score Formula:**

```javascript
priority = severityWeight × crossDomainMultiplier × confidenceWeight / effortWeight;

// Weights
severityWeight = { S0: 100, S1: 50, S2: 20, S3: 5 };
crossDomainMultiplier = 1 + (domains.length - 1) * 0.5; // 1.0, 1.5, 2.0, 2.5...
confidenceWeight = { High: 1.0, Medium: 0.8, Low: 0.5 };
effortWeight = { E0: 0.5, E1: 1.0, E2: 2.0, E3: 4.0 };
```

**Ranking Rules:**

1. **S0 Critical** always rank first (regardless of other factors)
2. **Cross-domain findings** bubble up (multiplier effect)
3. **High confidence** preferred over low confidence
4. **Low effort** (quick wins) preferred when severity equal

**Example Scores:**

```
Finding A: S0 Critical, 1 domain, High confidence, E1 effort
  → 100 × 1.0 × 1.0 / 1.0 = 100 (Rank #1)

Finding B: S1 High, 3 domains, High confidence, E1 effort
  → 50 × 2.0 × 1.0 / 1.0 = 100 (Rank #2 - tie, resolved by severity S0 > S1)

Finding C: S2 Medium, 2 domains, High confidence, E0 trivial
  → 20 × 1.5 × 1.0 / 0.5 = 60 (Rank #3 - quick win)

Finding D: S1 High, 1 domain, Medium confidence, E2 day
  → 50 × 1.0 × 0.8 / 2.0 = 20 (Rank #4 - high effort lowers priority)
```

---

### Step 5: Generate Executive Summary

**Summary Components:**

**A. Statistics:**

```markdown
## Executive Summary

### Audit Overview

- **Raw Findings:** 142 (across 6 audits)
- **Unique Findings:** 97 (after deduplication)
- **Merged Findings:** 45 (appeared in 2+ audits)
- **Cross-Domain Findings:** 18 (3+ audits)

### Severity Breakdown

- **S0 Critical:** 3 (IMMEDIATE ACTION REQUIRED)
- **S1 High:** 24 (fix within sprint)
- **S2 Medium:** 42 (plan for next milestone)
- **S3 Low:** 28 (backlog/nice-to-have)

### Effort Estimate

- **Total estimated effort:** 127 hours
- **Quick wins (E0):** 15 findings (12 hours)
- **Short fixes (E1):** 42 findings (42 hours)
- **Medium tasks (E2):** 28 findings (56 hours)
- **Major refactors (E3):** 12 findings (96 hours)
```

**B. Top Insights:**

List 3-5 highest-impact insights:

```markdown
### Key Insights

1. **Authentication Layer Needs Comprehensive Refactor**
   - 8 files appear in 4+ audits (security, code, performance, documentation)
   - High complexity with poor error handling and missing tests
   - Recommended: Dedicated sprint to harden auth module

2. **Security + Performance Overlap**
   - 12 findings where fixing security also improves performance
   - Example: Rate limiting prevents DoS (security) + reduces server load
     (performance)
   - Recommended: Bundle these fixes together

3. **Documentation Gaps Align with Code Complexity**
   - 5 files with S1 complexity issues also have missing/outdated docs
   - Difficult to maintain or extend without documentation
   - Recommended: Document complex areas first (highest ROI)
```

**C. Recommended Fix Order:**

```markdown
### Recommended Action Plan

**Phase 1: Critical Fixes (Week 1)**

1. FIX S0 findings (3 items - 8 hours)
2. Address top 5 quick wins (E0 - 4 hours)

**Phase 2: High-Priority Fixes (Week 2-3)**

1. Cross-domain findings (18 items - 32 hours)
2. Hotspot files refactor (8 files - 48 hours)

**Phase 3: Systematic Improvements (Month 2)**

1. Remaining S1 findings (21 items - 36 hours)
2. S2 medium-effort fixes (28 items - 56 hours)

**Phase 4: Backlog (Ongoing)**

1. S3 low-priority (28 items - 24 hours)
2. Major refactors (E3 - 96 hours, spread over quarters)
```

---

### Step 6: Generate Full Report

**Output File:** `docs/audits/comprehensive/COMPREHENSIVE_AUDIT_REPORT.md`

**Structure:**

```markdown
# Comprehensive Audit Report

**Generated:** [Date] **Audits Included:** Code, Security, Performance,
Documentation, Refactoring, Process **Total Findings:** 97 unique (142 raw)

---

## Executive Summary

[Generated in Step 5]

---

## Priority-Ranked Findings (Top 20)

| Rank | ID       | Severity | Domains | File:Line           | Description                             | Effort | Score |
| ---- | -------- | -------: | ------: | ------------------- | --------------------------------------- | -----: | ----: |
| 1    | COMP-001 |       S0 |       3 | src/auth.ts:45      | Missing error handling + Exception vuln |     E1 |   100 |
| 2    | SEC-012  |       S0 |       1 | firestore.rules:102 | Missing auth check on delete            |     E0 |    95 |
| ...  | ...      |      ... |     ... | ...                 | ...                                     |    ... |   ... |

---

## Cross-Domain Insights

### Hotspot Files (3+ audits)

1. **src/auth.ts** (5 audits: code, security, performance, documentation,
   refactoring)
   - Complexity: 45 (high)
   - Missing tests: 8 functions
   - Security issues: 3 (auth bypass, exception handling, rate limiting)
   - Performance: N+1 queries
   - Documentation: Outdated

[Continue with other hotspots...]

### Domain Overlaps

- **Security + Performance:** 12 findings (bundling opportunity)
- **Code + Refactoring:** 18 findings (quality improvements)
- **Documentation + Code:** 8 findings (complex code needs docs)

### Category Patterns

- **Authentication:** 5 findings → Need dedicated hardening sprint
- **Error Handling:** 8 findings → Systematic improvement needed
- **Testing:** 12 findings → Coverage gaps in critical areas

---

## Full Findings (Deduplicated)

### S0 Critical (3 findings)

#### COMP-001: Missing error handling + Exception vulnerability

**Domains:** Code (CODE-001), Security (SEC-012), Performance (PERF-005)
**File:** `src/auth.ts:45` **Severity:** S0 (Critical) **Effort:** E1 (Hours)
**Confidence:** High

**Description:** [Merged description from all 3 audits...]

**Evidence:** [Merged evidence from all 3 audits...]

**Recommendation:** [Merged recommendations from all 3 audits...]

---

[Continue with all findings grouped by severity...]

---

## Appendix

### Individual Audit Reports

- [Code Quality Report](./audit-code-report.md) - 32 findings
- [Security Report](./audit-security-report.md) - 18 findings
- [Performance Report](./audit-performance-report.md) - 24 findings
- [Documentation Report](./audit-documentation-report.md) - 15 findings
- [Refactoring Report](./audit-refactoring-report.md) - 41 findings
- [Process/Automation Report](./audit-process-report.md) - 12 findings

### Baseline Metrics

- **Tests:** 287 passing
- **Lint:** 0 errors, 12 warnings
- **Pattern Compliance:** 4 violations
- **Stack:** Next.js 16.1.1, React 19.2.3, Firebase 12.6.0

### False Positives Excluded

- **Total excluded:** 8 findings
- **Reason:** Documented false positives in FALSE_POSITIVES.jsonl
- **Categories:** code (3), security (2), performance (2), documentation (1)
```

---

## Output Validation

**Before Finalizing Report:**

1. **Verify deduplication worked:**
   - Count unique findings vs raw findings
   - Ensure merged findings have correct domain lists
   - No duplicate file:line pairs

2. **Verify priority ranking:**
   - Top 20 should have highest scores
   - S0 Critical should all be in top 20
   - Cross-domain findings should rank higher than single-domain

3. **Verify cross-cutting insights:**
   - Hotspot files should have 3+ mentions
   - Domain overlaps should be accurate counts
   - Category patterns should group related findings

4. **Verify completeness:**
   - All raw findings accounted for (unique + duplicates = raw total)
   - All severity levels represented
   - All 6 audit reports linked in appendix

---

## Error Handling

**If Audit Report Missing:**

- Note in report: "X audit not available"
- Continue with available audits
- Adjust statistics (e.g., "5 audits analyzed")

**If Parsing Fails:**

- Log which report/finding failed to parse
- Skip malformed finding
- Note in report: "X findings skipped due to format issues"

**If Deduplication Produces Empty Result:**

- Verify input reports aren't empty
- Check parsing logic
- Fall back to showing all findings without deduplication

---

## Usage

**Standalone Usage (you have existing audit reports):**

```
/audit-aggregator
```

**Integrated Usage (called by audit-comprehensive):**

Automatically invoked after all 6 parallel audits complete.

---

## Notes

- **Deduplication Benefits:** Prevents same issue from appearing 6 times
- **Cross-Domain Value:** Finds patterns individual audits miss
- **Priority Ranking:** Helps focus on high-impact fixes first
- **Effort Estimation:** Helps plan sprint capacity

---

## Future Enhancements

- [ ] **Trend Analysis:** Compare against previous comprehensive audits
- [ ] **Auto-Issue Creation:** Create GitHub issues for top 20 findings
- [ ] **Confidence Calibration:** Track how often Low confidence findings are
      false positives
- [ ] **Fix Chains:** Automatically detect dependencies between findings
- [ ] **ROI Scoring:** Prioritize fixes by impact/effort ratio

---

## Related Skills

- `/audit-comprehensive` - Orchestrator that calls this aggregator
- Individual audit skills - Generate the input reports this aggregator processes
