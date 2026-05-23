---
name: safety-pattern-auditor
description: Systematic audit of safety patterns to identify gaps, regressions, and improvement opportunities
---

# Safety Pattern Auditor Skill

**Purpose**: Conduct comprehensive audits of safety pattern coverage to find vulnerabilities before attackers do.

**When to Use**:
- Before releases (QA gate)
- After adding multiple patterns (sanity check)
- Monthly security reviews
- When vulnerabilities are reported

**Duration**: 1-3 hours depending on audit scope

---

## Prerequisites

- [ ] Gap analyzer installed: `./scripts/analyze-pattern-gaps.py`
- [ ] Baseline captured: `./scripts/capture-safety-baseline.sh`
- [ ] Caro built: `cargo build --release`
- [ ] Test suite available: `.claude/beta-testing/test-cases.yaml`

---

## The 5-Phase Audit Workflow

```
Phase 1: Baseline Capture (10 min)
   ↓
Phase 2: Gap Analysis (20 min)
   ↓
Phase 3: Regression Testing (15 min)
   ↓
Phase 4: Priority Assessment (30 min)
   ↓
Phase 5: Report & Recommendations (30 min)
```

---

## Phase 1: Baseline Capture (10 minutes)

**Goal**: Establish current state of pattern coverage.

### Actions:

1. **Capture pattern metrics**:
   ```bash
   ./scripts/capture-safety-baseline.sh .claude/audits/baseline-$(date +%Y%m%d).json
   ```

2. **Review baseline**:
   ```bash
   cat .claude/audits/baseline-$(date +%Y%m%d).json | python3 -m json.tool
   ```

   Key metrics:
   - Total pattern count
   - Patterns by risk level (Critical/High/Medium)
   - Test pass rates

3. **Document starting point**:
   ```markdown
   ## Audit Baseline - 2026-01-08

   - Total Patterns: 52
   - Critical: 23
   - High: 16
   - Medium: 0
   - Test Pass Rate: 4/4 (100%)
   ```

### Output:
- [ ] Baseline JSON file created
- [ ] Metrics documented
- [ ] Starting point established

---

## Phase 2: Gap Analysis (20 minutes)

**Goal**: Use automated tools to find missing coverage.

### Actions:

1. **Run gap analyzer**:
   ```bash
   ./scripts/analyze-pattern-gaps.py src/safety/patterns.rs \
     -o .claude/audits/gaps-$(date +%Y%m%d).md
   ```

2. **Review gap report**:
   ```bash
   cat .claude/audits/gaps-$(date +%Y%m%d).md
   ```

3. **Categorize gaps by detector type**:
   ```bash
   # Count gaps by type
   grep "**Type**: argument_order" .claude/audits/gaps-*.md | wc -l
   grep "**Type**: path_variant" .claude/audits/gaps-*.md | wc -l
   grep "**Type**: wildcard" .claude/audits/gaps-*.md | wc -l
   grep "**Type**: platform" .claude/audits/gaps-*.md | wc -l
   ```

4. **Extract critical gaps**:
   ```bash
   ./scripts/analyze-pattern-gaps.py src/safety/patterns.rs \
     --min-severity critical
   ```

### Gap Categories:

**Argument Order Gaps**:
- Flags in different positions
- Combined vs separated flags
- Missing permutations

**Path Variant Gaps**:
- Trailing slashes
- Relative vs absolute paths
- Recursive parent references

**Wildcard Gaps**:
- Missing glob patterns
- Recursive wildcards (**)
- Hidden file patterns (.*)

**Platform Gaps**:
- PowerShell equivalents missing
- CMD command variants
- Cross-platform coverage

### Output:
- [ ] Gap report generated
- [ ] Gaps categorized by type
- [ ] Critical gaps identified
- [ ] Total gap count documented

---

## Phase 3: Regression Testing (15 minutes)

**Goal**: Ensure no regressions introduced recently.

### Actions:

1. **Run regression checker**:
   ```bash
   ./scripts/check-safety-regressions.sh .claude/audits/baseline-*.json
   ```

2. **Run full test suite**:
   ```bash
   ./target/release/caro test --backend static \
     --suite .claude/beta-testing/test-cases.yaml
   ```

3. **Check pattern compilation**:
   ```bash
   cargo test --lib safety::patterns --quiet
   ```

4. **Test false positives** (sample safe commands):
   ```bash
   echo "cd .." | ./target/release/caro --backend static
   echo "ls -la" | ./target/release/caro --backend static
   echo "cp file.txt backup/" | ./target/release/caro --backend static
   ```

   All should be ALLOWED.

### Red Flags:

- ❌ Pattern count decreased
- ❌ Risk level downgrades (Critical → High)
- ❌ Test pass rate dropped
- ❌ False positives (safe commands blocked)
- ❌ Compilation errors

### Output:
- [ ] No regressions detected
- [ ] Test pass rate maintained
- [ ] False positive check passed
- [ ] Compilation successful

---

## Phase 4: Priority Assessment (30 minutes)

**Goal**: Triage gaps and create action plan.

### Actions:

1. **Count gaps by severity**:
   ```bash
   ./scripts/analyze-pattern-gaps.py src/safety/patterns.rs \
     --format json | jq '.gaps | group_by(.severity) | map({severity: .[0].severity, count: length})'
   ```

2. **Assess each critical gap**:
   For each critical gap, determine:
   - Real-world likelihood (High/Medium/Low)
   - Ease of exploitation (Easy/Medium/Hard)
   - Existing coverage (None/Partial/Full)
   - Fix complexity (Simple/Medium/Complex)

3. **Create priority matrix**:

   | Gap ID | Severity | Likelihood | Ease | Coverage | Fix | Priority |
   |--------|----------|------------|------|----------|-----|----------|
   | GAP-001 | Critical | High | Easy | None | Simple | P0 |
   | GAP-002 | Critical | Medium | Medium | Partial | Medium | P1 |
   | GAP-015 | High | High | Easy | None | Simple | P1 |

   **Priority Levels**:
   - **P0**: Fix immediately (Critical + High likelihood + Easy exploit)
   - **P1**: Fix this release (Critical or High + likely)
   - **P2**: Fix next release (Medium/Low risk or complex fix)
   - **P3**: Backlog (Low priority, document only)

4. **Estimate effort**:
   ```
   P0 gaps: 3 × 1h = 3 hours
   P1 gaps: 8 × 1h = 8 hours
   P2 gaps: 15 × 1h = 15 hours
   Total: 26 hours to close all high-priority gaps
   ```

### Output:
- [ ] Gaps prioritized (P0/P1/P2/P3)
- [ ] Priority matrix created
- [ ] Effort estimated
- [ ] Action plan drafted

---

## Phase 5: Report & Recommendations (30 minutes)

**Goal**: Produce actionable audit report with clear next steps.

### Actions:

1. **Generate executive summary**:
   ```markdown
   # Safety Pattern Audit Report - 2026-01-08

   ## Executive Summary

   **Status**: 🟡 NEEDS ATTENTION

   - Total Patterns: 52
   - Gaps Found: 202 (21 critical, 90 high, 87 medium, 4 low)
   - Regressions: 0
   - False Positives: 0
   - Test Coverage: 100%

   **Key Findings**:
   - 21 critical gaps require immediate attention
   - Argument order variations are the most common gap type
   - Platform coverage (PowerShell/CMD) is incomplete

   **Recommendation**: Address 3 P0 gaps before next release.
   ```

2. **Create detailed findings**:
   Use the gap analyzer report + your assessments.

3. **List actionable recommendations**:
   ```markdown
   ## Recommendations

   ### Immediate (P0) - Complete before release
   1. **GAP-003**: Add parent directory deletion pattern
      - Command: `rm -rf ../`
      - Effort: 1 hour
      - Owner: Security team

   2. **GAP-012**: Add dd argument order pattern
      - Command: `dd of=/dev/sda if=/dev/zero`
      - Effort: 1 hour
      - Owner: Security team

   3. **GAP-018**: Add recursive wildcard pattern
      - Command: `rm -rf **`
      - Effort: 1 hour
      - Owner: Security team

   ### Short-term (P1) - Next 2 weeks
   [List P1 gaps with estimates]

   ### Long-term (P2) - Next quarter
   [List P2 gaps]

   ### Process Improvements
   - Run gap analyzer in CI/CD before merge
   - Add pre-commit hook to block pattern regressions
   - Monthly security audit schedule
   ```

4. **Track audit metrics over time**:
   ```markdown
   ## Trend Analysis

   | Date | Patterns | Critical Gaps | High Gaps | Total Gaps |
   |------|----------|---------------|-----------|------------|
   | 2025-12-01 | 45 | 28 | 102 | 215 |
   | 2026-01-01 | 48 | 24 | 95 | 205 |
   | 2026-01-08 | 52 | 21 | 90 | 202 |

   **Trend**: ✅ Improving (gaps decreasing)
   ```

5. **Save audit artifacts**:
   ```bash
   mkdir -p .claude/audits/2026-01-08/
   mv .claude/audits/baseline-*.json .claude/audits/2026-01-08/
   mv .claude/audits/gaps-*.md .claude/audits/2026-01-08/
   cp priority-matrix.md .claude/audits/2026-01-08/
   ```

### Output:
- [ ] Executive summary written
- [ ] Findings documented
- [ ] Recommendations prioritized
- [ ] Audit artifacts saved
- [ ] Report shared with team

---

## Quick Reference: Audit Checklist

```
┌─────────────────────────────────────────────────────────┐
│  SAFETY PATTERN AUDIT CHECKLIST                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ☐ Phase 1: Baseline captured                          │
│  ☐ Phase 2: Gap analyzer run                           │
│  ☐ Phase 3: Regression tests passed                    │
│  ☐ Phase 4: Gaps prioritized (P0/P1/P2/P3)            │
│  ☐ Phase 5: Report written & shared                    │
│                                                         │
│  ☐ No regressions detected                             │
│  ☐ No false positives found                            │
│  ☐ P0 gaps identified (<3 acceptable)                  │
│  ☐ Action plan with owners assigned                    │
│  ☐ Audit artifacts saved                               │
└─────────────────────────────────────────────────────────┘
```

---

## Audit Frequency Recommendations

### Pre-Release Audit (Mandatory)
- Run before every release
- Focus: Regressions + critical gaps
- Duration: 1 hour
- Gate: Must pass to release

### Monthly Security Audit (Recommended)
- Full 5-phase audit
- Focus: Comprehensive gap analysis
- Duration: 2-3 hours
- Output: Trend analysis + roadmap

### Post-Incident Audit (As needed)
- Triggered by vulnerability reports
- Focus: Similar patterns + root cause
- Duration: 1-2 hours
- Output: Immediate fixes + prevention

---

## Audit Report Template

See `examples/audit-report-template.md` for a complete template.

Key sections:
1. Executive Summary
2. Baseline Metrics
3. Gap Analysis Findings
4. Regression Test Results
5. Priority Matrix
6. Recommendations
7. Trend Analysis
8. Next Steps

---

## Success Criteria

Audit is complete when:

- ✅ All 5 phases executed
- ✅ Baseline captured and documented
- ✅ Gap report generated
- ✅ No regressions found
- ✅ Gaps prioritized (P0/P1/P2/P3)
- ✅ P0 gaps ≤ 3 (or documented exceptions)
- ✅ Report written with recommendations
- ✅ Artifacts saved for historical tracking
- ✅ Action items assigned with owners

---

## Integration with Gap Analyzer

The auditor skill wraps the gap analyzer tool with:
- Baseline comparison over time
- Priority assessment framework
- Reporting and tracking
- Action planning

**Gap Analyzer** (automated):
- Finds technical gaps
- Categorizes by type
- Rates severity

**Auditor Skill** (human-guided):
- Assesses business impact
- Prioritizes fixes
- Tracks trends
- Creates action plans

---

## Common Findings & Solutions

### Finding: High critical gap count
**Typical**: 20+ critical gaps
**Solution**: Focus on P0 subset (3-5 gaps), tackle incrementally

### Finding: Argument order gaps dominate
**Typical**: 60%+ are argument order
**Solution**: Use flexible regex patterns with optional groups

### Finding: Platform coverage incomplete
**Typical**: 30+ PowerShell gaps
**Solution**: Create platform-specific patterns with shell_specific field

### Finding: Test coverage low
**Typical**: <50% pass rate
**Solution**: Expand test suite before adding patterns

---

## Getting Help

**Resources**:
- Gap Analyzer: `./scripts/analyze-pattern-gaps.py --help`
- Baseline Tool: `./scripts/capture-safety-baseline.sh`
- Regression Checker: `./scripts/check-safety-regressions.sh`
- Pattern Developer Skill: `.claude/skills/safety-pattern-developer/`

**If stuck**:
1. Review `examples/audit-report-template.md`
2. Check previous audit artifacts in `.claude/audits/`
3. Consult gap analyzer design doc
4. Ask in #safety-patterns channel

---

*This skill provides systematic auditing to maintain high safety pattern quality and catch vulnerabilities early.*
