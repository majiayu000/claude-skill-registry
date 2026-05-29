---
name: audit-comprehensive
description: Run all 6 domain audits in parallel and aggregate results
---

# Comprehensive Multi-Domain Audit Orchestrator

**Time Savings:** 77% faster than sequential (150min → 35min)

**What This Does:** Spawns all 6 specialized audit agents in parallel, then
aggregates their findings into a single comprehensive report with cross-domain
insights and priority ranking.

---

## Overview

This skill orchestrates a complete codebase audit across all 6 domains:

1. **Code Quality** (`audit-code`) - Code hygiene, types, framework patterns
2. **Security** (`audit-security`) - Auth, input validation, OWASP compliance
3. **Performance** (`audit-performance`) - Load times, queries, caching
4. **Documentation** (`audit-documentation`) - README, API docs, architecture
5. **Refactoring** (`audit-refactoring`) - Technical debt, complexity, DRY
6. **Process/Automation** (`audit-process`) - CI/CD, testing, workflows

**Output:** Single unified report in
`docs/audits/comprehensive/COMPREHENSIVE_AUDIT_REPORT.md`

---

## Pre-Flight Validation

**Step 1: Verify Skills Exist**

Check that all 6 audit skills are available:

```bash
ls -1 .claude/skills/audit-*/SKILL.md | wc -l
# Should return 6
```

If not all present, notify user which audits are missing and ask whether to
proceed with available audits only.

**Step 2: Create Output Directory**

```bash
mkdir -p docs/audits/comprehensive
```

**Step 3: Run Baseline Checks**

Gather current metrics to provide to all audits:

```bash
# Test count
npm test 2>&1 | grep -E "Tests:|passing|failed" | head -5

# Lint status
npm run lint 2>&1 | tail -10

# Pattern compliance
npm run patterns:check 2>&1 | head -20
```

Store results in `docs/audits/comprehensive/baseline.txt` for reference.

**Step 4: Load False Positives**

Read `docs/audits/FALSE_POSITIVES.jsonl` to pass to aggregator (prevents
duplicate flagging of known false positives).

---

## Parallel Audit Execution

**CRITICAL: Use Task tool to spawn all 6 audits in parallel**

Launch all audits using the Task tool with `run_in_background: true`:

```javascript
// Pseudo-code showing the pattern (you'll use actual Task tool calls)

const audits = [
  { name: "audit-code", description: "Code quality audit" },
  { name: "audit-security", description: "Security audit" },
  { name: "audit-performance", description: "Performance audit" },
  { name: "audit-documentation", description: "Documentation audit" },
  { name: "audit-refactoring", description: "Refactoring audit" },
  { name: "audit-process", description: "Process/automation audit" },
];

// Launch all in parallel
for (const audit of audits) {
  Task({
    subagent_type: audit.name,
    description: audit.description,
    prompt: `Run ${audit.name} and output to docs/audits/comprehensive/${audit.name}-report.md`,
    run_in_background: true,
  });
}
```

**Expected Outputs:**

- `docs/audits/comprehensive/audit-code-report.md`
- `docs/audits/comprehensive/audit-security-report.md`
- `docs/audits/comprehensive/audit-performance-report.md`
- `docs/audits/comprehensive/audit-documentation-report.md`
- `docs/audits/comprehensive/audit-refactoring-report.md`
- `docs/audits/comprehensive/audit-process-report.md`

---

## Progress Monitoring

**Step 1: Display Initial Status**

Show user:

```
🚀 Comprehensive Audit Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Running 6 audits in parallel:
  ⏳ Code Quality
  ⏳ Security
  ⏳ Performance
  ⏳ Documentation
  ⏳ Refactoring
  ⏳ Process/Automation

Estimated time: 30-35 minutes
(vs 150 minutes if run sequentially - 77% faster!)

You can continue working while audits run.
I'll notify when complete.
```

**Step 2: Poll for Completion**

Check TaskOutput for each agent every 60 seconds:

- Update status display (⏳ → ✅ as each completes)
- Detect failures (⏳ → ❌ if agent errors)
- Continue until all 6 complete or timeout (45 min)

**Step 3: Notify User**

When all complete:

```
✅ All Audits Complete!
━━━━━━━━━━━━━━━━━━━━━

  ✅ Code Quality    (32 findings)
  ✅ Security        (18 findings)
  ✅ Performance     (24 findings)
  ✅ Documentation   (15 findings)
  ✅ Refactoring     (41 findings)
  ✅ Process/Auto    (12 findings)

Total raw findings: 142
Now aggregating and deduplicating...
```

---

## Aggregation Phase

**Launch Aggregator Agent**

Use Task tool to spawn `audit-aggregator` agent:

```javascript
Task({
  subagent_type: "audit-aggregator",
  description: "Aggregate and deduplicate audit results",
  prompt: `
Read all 6 audit reports from docs/audits/comprehensive/

Perform:
1. Deduplicate findings (same file:line across multiple audits → merge)
2. Identify cross-cutting patterns (files appearing in 3+ audits)
3. Priority ranking (severity × cross-domain count × effort)
4. Generate executive summary with top 20 findings

Output to: docs/audits/comprehensive/COMPREHENSIVE_AUDIT_REPORT.md
  `,
});
```

**Expected Output:**

- `docs/audits/comprehensive/COMPREHENSIVE_AUDIT_REPORT.md` (unified report)

**Wait for aggregator to complete** (typically 3-5 minutes)

---

## Final Report Structure

The `COMPREHENSIVE_AUDIT_REPORT.md` should contain:

### Executive Summary

- Total unique findings (after deduplication)
- Severity breakdown (S0: X, S1: Y, S2: Z, S3: W)
- Top 3 cross-domain insights
- Recommended fix order
- Effort estimate (total hours)

### Priority-Ranked Findings (Top 20)

Table format:

| Rank | ID       | Severity | Domains | File:Line  | Description        | Effort |
| ---- | -------- | -------: | ------: | ---------- | ------------------ | -----: |
| 1    | COMP-001 |       S0 |       3 | auth.ts:45 | Missing auth check |     E1 |
| ...  | ...      |      ... |     ... | ...        | ...                |    ... |

### Cross-Domain Insights

Examples:

- "Files X, Y, Z appear in 4+ audits → Comprehensive refactor needed"
- "Security + Performance overlap: 12 findings where fixing one helps both"
- "Documentation gaps align with code complexity hotspots"

### Full Findings (Deduplicated)

Complete table of all findings grouped by severity, with links to original audit
reports.

### Appendix

- Links to individual audit reports
- Baseline metrics snapshot
- False positives excluded (count)

---

## Post-Audit (MANDATORY)

**After aggregation completes, you MUST update tracking:**

### 1. Update AUDIT_TRACKER.md

Add an entry to **each of the 6 category tables** in `docs/AUDIT_TRACKER.md`:

| Date    | Session       | Commits Covered | Files Covered | Findings                     | Reset Threshold |
| ------- | ------------- | --------------- | ------------- | ---------------------------- | --------------- |
| {TODAY} | Comprehensive | Full codebase   | All           | Session #{N} - [report link] | ✅ (all)        |

### 2. Update Threshold Summary Table

In the "Current Thresholds" section, update all 6 categories:

- Set "Last Audit" to today's date with "(Comprehensive)"
- Reset "Commits Since" to 0
- Reset "Files Since" to 0

### 3. Update Multi-AI Thresholds

In the "Multi-AI Audit Thresholds" section:

- Update "Total commits" reset date to today
- Update "Time elapsed" to "0 days (comprehensive audit {TODAY})"

**This step ensures `npm run review:check` correctly shows no triggers after the
audit.**

---

## Completion

**Display Final Summary:**

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 COMPREHENSIVE AUDIT COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Results Summary:
   • 142 raw findings → 97 unique (45 merged)
   • S0 Critical: 3
   • S1 High: 24
   • S2 Medium: 42
   • S3 Low: 28

🔍 Cross-Domain Insights:
   • 8 files need comprehensive refactor (4+ audits)
   • 12 security/performance overlaps
   • 5 documentation gaps in complex areas

📄 Full Report:
   docs/audits/comprehensive/COMPREHENSIVE_AUDIT_REPORT.md

⏱️  Total Time: 34 minutes
   (vs 150 minutes sequential - saved 116 minutes!)

🎯 Recommended Next Steps:
   1. Review top 20 priority findings
   2. Create GitHub issues for S0/S1
   3. Plan refactor for hotspot files
```

---

## Error Handling

**If Individual Audit Fails:**

- Continue with remaining audits
- Mark failed audit in status display (❌)
- Note failure in final report
- Suggest running failed audit individually for debugging

**If Aggregator Fails:**

- All individual reports still available
- User can manually review 6 separate reports
- Suggest creating GitHub issue for aggregator failure

**If All Audits Fail:**

- Check baseline environment (tests passing, lint working)
- Check for system issues (disk space, memory)
- Suggest running single audit first to isolate issue

---

## Usage Examples

**Quarterly Health Check:**

```
/audit-comprehensive
```

**Pre-Release Audit:**

```
/audit-comprehensive
```

**After Major Refactor:**

```
/audit-comprehensive
```

**Focused Audit (Not Comprehensive):**

Use individual skills instead:

```
/audit-security   (25 min - when you only need security review)
/audit-code       (30 min - when you only need code quality)
```

---

## Notes

- **Parallelization:** Uses Task tool with `run_in_background: true` for all 6
  audits
- **Time Savings:** 77% faster than sequential execution (150min → 35min)
- **Output Consistency:** All audits use same severity (S0-S3) and effort
  (E0-E3) scales
- **Cross-Cutting Value:** Aggregator finds patterns individual audits miss
- **Deduplication:** Prevents same issue flagged by multiple audits from
  appearing multiple times

---

## Future Enhancements

- [ ] **Incremental Audits:** Only re-run audits for changed domains
- [ ] **Custom Audit Subset:** `--audits code,security` to run subset
- [ ] **Confidence Scoring:** Weight findings by audit confidence levels
- [ ] **Trend Analysis:** Compare against previous comprehensive audits
- [ ] **Auto-Issue Creation:** Create GitHub issues for S0/S1 findings
      automatically

---

## Related Skills

- `/audit-code` - Individual code quality audit
- `/audit-security` - Individual security audit
- `/audit-performance` - Individual performance audit
- `/audit-documentation` - Individual documentation audit
- `/audit-refactoring` - Individual refactoring audit
- `/audit-process` - Individual process/automation audit
- `/audit-aggregator` - Standalone aggregation (if you have existing reports)
