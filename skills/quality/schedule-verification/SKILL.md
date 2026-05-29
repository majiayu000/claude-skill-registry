---
name: schedule-verification
description: Human verification checklist for generated schedules. Use when reviewing Block 10 or any generated schedule to ensure it makes operational sense. Covers FMIT, call, Night Float, clinic days, and absence handling.
model_tier: sonnet
parallel_hints:
  can_parallel_with: [acgme-compliance, schedule-validator]
  must_serialize_with: [safe-schedule-generation]
  preferred_batch_size: 1
context_hints:
  max_file_context: 60
  compression_level: 1
  requires_git_context: false
  requires_db_context: true
escalation_triggers:
  - pattern: "FAIL|violation|conflict"
    reason: "Verification failures require human review before deployment"
  - pattern: "red flag|stop"
    reason: "Critical issues need immediate investigation"
  - keyword: ["0% coverage", "back-to-back"]
    reason: "Severe constraint violations need escalation"
---

# Schedule Verification Skill

Systematic checklist for human verification of generated schedules. Ensures the schedule makes operational sense before deployment.

## Two Truths: What You're Verifying

| Truth Type | Tables | Your Focus |
|------------|--------|------------|
| **Prescriptive** | `rotation_templates`, `weekly_patterns` | Rules the schedule SHOULD follow |
| **Descriptive** | `half_day_assignments` | What ACTUALLY got scheduled |

**You verify the descriptive truth (`half_day_assignments`)** - that's what gets deployed. But check that divergence from prescriptive truth (templates) is intentional.

### Source Column Audit (CRITICAL)

The `source` column explains WHY each slot has its value:

| Source | Meaning | Verification |
|--------|---------|--------------|
| `preload` | Fixed before solver (absences, FMIT, call) | Should match absences table, FMIT schedule |
| `solver` | Computed by optimizer | Should follow rotation patterns |
| `manual` | Human override | Intentional - don't question |
| `template` | Default from weekly pattern | Lowest priority, filled gaps |

**Spot Check Protocol:**
1. Pick 3 slots that diverge from template expectation
2. Check `source` column - does it explain the divergence?
3. If `source='solver'` but slot doesn't match template → investigate bug

## MANDATORY: Generate Visible Report

**CRITICAL:** Every time this skill runs, you MUST:

1. **Print a header** with block number and date range
2. **Run each check** and print PASS/FAIL for each item
3. **Show actual data** - not just "checked", but the values found
4. **Generate summary table** at the end with all results
5. **Save report** to `docs/reports/schedule-verification-{block}-{date}.md`

```
╔══════════════════════════════════════════════════════════════════╗
║  SCHEDULE VERIFICATION REPORT                                    ║
║  Block: 10  |  Date Range: 2026-03-12 to 2026-04-08              ║
║  Generated: 2025-12-26                                           ║
╠══════════════════════════════════════════════════════════════════╣
║  CHECK                                    │ STATUS │ DETAILS     ║
╠═══════════════════════════════════════════╪════════╪═════════════╣
║  FMIT faculty rotation pattern            │ ✅ PASS │ No b2b     ║
║  FMIT mandatory Fri+Sat call              │ ✅ PASS │ 4/4 weeks  ║
║  Post-FMIT Sunday blocking                │ ✅ PASS │ 0 conflicts║
║  Night Float headcount = 1                │ ❌ FAIL │ Found 3    ║
║  ...                                      │        │             ║
╚══════════════════════════════════════════════════════════════════╝
```

**DO NOT** silently run checks. Every check must produce visible output.

## When This Skill Activates

- After schedule generation completes
- Before deploying a new schedule to production
- When reviewing Block 10 or any academic block schedule
- When a human asks "does this schedule make sense?"
- After constraint changes to verify behavior

---

## Verification Checklist

### 1. Faculty FMIT Schedule

| Check | What to Verify | How to Check |
|-------|----------------|--------------|
| [ ] FMIT rotation pattern | No faculty has back-to-back FMIT weeks | Query: faculty with FMIT in consecutive weeks |
| [ ] FMIT mandatory call | FMIT faculty has Fri+Sat call during their week | Check call assignments for FMIT weeks |
| [ ] Post-FMIT Sunday block | No Sunday call within 3 days of FMIT end | Check Sunday call vs FMIT end dates |
| [ ] FMIT coverage | Every week has FMIT faculty assigned | No gaps in FMIT weekly coverage |

**Expected Pattern (Block 10 example):**
```
Week 1: FAC-CORE-01 (FMIT) → Fri/Sat call → Sun blocked
Week 2: FAC-CORE-02 (FMIT) → Fri/Sat call → Sun blocked
Week 3: FAC-CORE-01 (FMIT) → Fri/Sat call → Sun blocked
Week 4: FAC-CORE-03 (FMIT) → Fri/Sat call → Sun blocked
```

### 2. Resident Inpatient Assignments

| Check | What to Verify | Expected |
|-------|----------------|----------|
| [ ] FMIT headcount | 1 resident per PGY level on FMIT | 3 total per block |
| [ ] Night Float headcount | Exactly 1 resident on NF at a time | Never 0, never 2+ |
| [ ] NICU coverage | NICU resident has Friday PM clinic | Always |
| [ ] Post-Call | Thursday after NF ends is Post-Call | No assignments that day |

**PGY-Specific Clinic Days (FMIT residents):**
| PGY Level | Required Clinic Day |
|-----------|---------------------|
| PGY-1 | Wednesday AM |
| PGY-2 | Tuesday PM |
| PGY-3 | Monday PM |

### 3. Call Schedule Equity

| Check | What to Verify | Acceptable Range |
|-------|----------------|------------------|
| [ ] Sunday call distribution | Evenly distributed across faculty | Max variance: 1-2 |
| [ ] Weekday call distribution | Mon-Thu evenly distributed | Max variance: 2-3 |
| [ ] Call spacing | No back-to-back call weeks | Same faculty not in adjacent weeks |
| [ ] PD/APD Tuesday | Program Directors avoid Tuesday call | Preference, not hard |

### 4. Absence Handling

| Check | What to Verify | Expected |
|-------|----------------|----------|
| [ ] Leave respected | No assignments during approved leave | 0 conflicts |
| [ ] TDY respected | No assignments during TDY | 0 conflicts |
| [ ] Weekend assignments | Weekend blocks show appropriate coverage | Inpatient only |
| [ ] Holiday handling | Federal holidays have inpatient coverage | FMIT defaults |

### 5. Source Column Audit (NEW)

| Check | What to Verify | Expected |
|-------|----------------|----------|
| [ ] Preloads preserved | `source='preload'` rows match absences/FMIT tables | 100% match |
| [ ] Manual overrides | `source='manual'` rows are intentional edits | Should have audit trail |
| [ ] Solver decisions | `source='solver'` rows follow rotation patterns | Template-aligned |
| [ ] Template gaps | `source='template'` only for truly empty slots | Minimal usage |

**Query to audit source distribution:**
```sql
SELECT source, COUNT(*) as count
FROM half_day_assignments
WHERE date BETWEEN '2026-03-12' AND '2026-04-08'
GROUP BY source;
```

**Expected distribution (Block 10):**
```
preload   ~400  (absences, FMIT, call, conferences)
solver    ~800  (computed clinic, rotation activities)
manual    ~10   (human overrides, if any)
template  ~100  (gap-fill for empty slots)
```

### 6. Coverage Metrics

| Metric | Target | Warning | Violation |
|--------|--------|---------|-----------|
| Overall coverage | > 80% | 70-80% | < 70% |
| Weekday coverage | > 95% | 85-95% | < 85% |
| Weekend coverage | > 50% | 30-50% | < 30% |
| ACGME violations | 0 | 1-2 | > 2 |

---

## Spot Check Protocol

For any generated schedule, spot check **at least 3 people** of each type:

### Faculty Spot Check
1. Pick random faculty member
2. View their entire month
3. Verify:
   - FMIT weeks are not consecutive
   - Call weeks are spaced
   - Post-FMIT recovery days exist
   - No assignments during absences

### Resident Spot Check
1. Pick one resident from each PGY level
2. View their entire month
3. Verify:
   - Clinic days match PGY requirements
   - Night Float followed by Post-Call
   - No double-booking (AM+PM same day = OK, but not 2 rotations same slot)
   - Absences respected

---

## Query Templates

### Check FMIT Faculty Schedule
```sql
SELECT p.last_name, b.date, rt.name
FROM assignments a
JOIN blocks b ON a.block_id = b.id
JOIN people p ON a.person_id = p.id
JOIN rotation_templates rt ON a.rotation_template_id = rt.id
WHERE p.type = 'faculty'
  AND rt.activity_type = 'inpatient'
  AND b.date BETWEEN '2026-03-12' AND '2026-04-08'
ORDER BY p.last_name, b.date;
```

### Check Night Float Headcount
```sql
SELECT b.date, b.time_of_day, COUNT(*) as nf_count
FROM assignments a
JOIN blocks b ON a.block_id = b.id
JOIN rotation_templates rt ON a.rotation_template_id = rt.id
WHERE rt.name LIKE '%Night Float%'
  AND b.date BETWEEN '2026-03-12' AND '2026-04-08'
GROUP BY b.date, b.time_of_day
HAVING COUNT(*) != 1;
```

### Check for Absence Conflicts
```sql
SELECT p.last_name, b.date, rt.name as rotation, 'CONFLICT' as status
FROM assignments a
JOIN blocks b ON a.block_id = b.id
JOIN people p ON a.person_id = p.id
JOIN rotation_templates rt ON a.rotation_template_id = rt.id
WHERE EXISTS (
  SELECT 1 FROM absences ab
  WHERE ab.person_id = p.id
    AND b.date BETWEEN ab.start_date AND ab.end_date
)
AND rt.activity_type != 'absence';
```

---

## Red Flags (Stop and Investigate)

| Red Flag | Possible Cause | Action |
|----------|----------------|--------|
| 0% weekend coverage | Inpatient rotations not loading | Check `preserve_resident_inpatient` |
| All residents on Night Float | Missing headcount constraint | Check `ResidentInpatientHeadcountConstraint` |
| Faculty with 3+ FMIT weeks | Constraint not registered | Check `ConstraintManager.create_default()` |
| Assignments during leave | Absence preservation failing | Check `preserve_absence` |
| Back-to-back call weeks | CallSpacingConstraint weight too low | Increase weight from 8.0 |

---

## Sign-Off

After verification, update this section:

```
Schedule Verified: [ ] Yes  [ ] No
Block: ___
Verified By: ___
Date: ___
Issues Found: ___
Resolution: ___
```

---

## Examples

### Example 1: Clean Schedule Verification

**User Request:** "Verify the Block 10 schedule looks correct"

**Claude Response:**

```
╔══════════════════════════════════════════════════════════════════╗
║  SCHEDULE VERIFICATION REPORT                                    ║
║  Block: 10  |  Date Range: 2026-03-12 to 2026-04-08              ║
║  Generated: 2026-03-12 10:15:00                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  CHECK                                    │ STATUS │ DETAILS     ║
╠═══════════════════════════════════════════╪════════╪═════════════╣
║  FMIT faculty rotation pattern            │ ✅ PASS │ No b2b     ║
║  FMIT mandatory Fri+Sat call              │ ✅ PASS │ 4/4 weeks  ║
║  Post-FMIT Sunday blocking                │ ✅ PASS │ 0 conflicts║
║  Night Float headcount = 1                │ ✅ PASS │ Verified   ║
║  FMIT headcount (3 residents)             │ ✅ PASS │ 1 per PGY  ║
║  NICU Friday PM clinic                    │ ✅ PASS │ All weeks  ║
║  Post-Call after Night Float              │ ✅ PASS │ Thursdays  ║
║  PGY-1 Wednesday AM clinic                │ ✅ PASS │ 4/4 weeks  ║
║  PGY-2 Tuesday PM clinic                  │ ✅ PASS │ 4/4 weeks  ║
║  PGY-3 Monday PM clinic                   │ ✅ PASS │ 4/4 weeks  ║
║  Sunday call distribution                 │ ✅ PASS │ Variance: 1║
║  Absence conflicts                        │ ✅ PASS │ 0 conflicts║
║  Overall coverage                         │ ✅ PASS │ 97.9%      ║
║  ACGME violations                         │ ✅ PASS │ 0 found    ║
╚══════════════════════════════════════════════════════════════════╝

**Spot Check Results:**

Faculty: FAC-CORE-01
- Week 1: FMIT (Fri/Sat call) → Sun blocked ✅
- Week 3: FMIT (Fri/Sat call) → Sun blocked ✅
- No consecutive FMIT weeks ✅

Resident: RES-PGY1-02
- Night Float: Mar 17-23 → Post-Call Thu Mar 24 ✅
- Wednesday AM clinic: 4/4 weeks ✅
- Approved leave Mar 30-31: No assignments ✅

**VERDICT: ✅ Schedule approved for deployment**
```

Saved report to: `docs/reports/schedule-verification-block10-20260312.md`

### Example 2: Schedule with Issues Requiring Fix

**User Request:** "Check the newly generated schedule"

**Claude Response:**

```
╔══════════════════════════════════════════════════════════════════╗
║  SCHEDULE VERIFICATION REPORT                                    ║
║  Block: 10  |  Date Range: 2026-03-12 to 2026-04-08              ║
║  Generated: 2026-03-12 14:30:00                                  ║
╠══════════════════════════════════════════════════════════════════╣
║  CHECK                                    │ STATUS │ DETAILS     ║
╠═══════════════════════════════════════════╪════════╪═════════════╣
║  FMIT faculty rotation pattern            │ ✅ PASS │ No b2b     ║
║  FMIT mandatory Fri+Sat call              │ ❌ FAIL │ 2/4 weeks  ║
║  Post-FMIT Sunday blocking                │ ⚠️  WARN │ 1 conflict ║
║  Night Float headcount = 1                │ ❌ FAIL │ Found 0 NF ║
║  FMIT headcount (3 residents)             │ ✅ PASS │ 1 per PGY  ║
║  PGY-1 Wednesday AM clinic                │ ❌ FAIL │ 1/4 weeks  ║
║  Absence conflicts                        │ ❌ FAIL │ 3 conflicts║
║  Overall coverage                         │ ⚠️  WARN │ 78.5%      ║
║  ACGME violations                         │ ❌ FAIL │ 2 found    ║
╚══════════════════════════════════════════════════════════════════╝

**Critical Issues Found:**

🚨 **Night Float Coverage Missing**
- Mar 17-23: 0 residents assigned to Night Float
- Mar 24-30: 0 residents assigned to Night Float
- **Action:** Manually assign or regenerate with NF constraint

🚨 **Absence Conflicts Detected**
- RES-PGY2-01: Assigned to FMIT during approved leave (Mar 20-22)
- FAC-CORE-03: Sunday call on Mar 27 (TDY Mar 25-28)
- RES-PGY1-04: Clinic on Mar 31 (conference leave)
- **Action:** Remove these assignments immediately

🚨 **FMIT Call Pattern Broken**
- Week 2 FMIT (FAC-CORE-02): Missing Fri/Sat call
- Week 4 FMIT (FAC-CORE-01): Missing Saturday call
- **Action:** Add missing call assignments

**ACGME Violations:**
1. RES-PGY1-03: 82.5 hours week of Mar 17 (exceeds 80hr limit)
2. Mar 22 PM: 3 PGY-1 residents, 1 faculty (ratio violation)

**VERDICT: ❌ Schedule NOT approved - requires fixes before deployment**

Recommended next step: Restore from backup and regenerate with corrected constraints.
```

### Example 3: Quick Spot Check

**User Request:** "Just spot check a few residents to make sure the schedule makes sense"

**Claude Response:**

**Running quick spot check on 3 random residents...**

**RES-PGY1-02 (PGY-1):**
```
Mar 12-16: FMIT week
  - Wed Mar 16 AM: Clinic ✅ (correct day for PGY-1)
Mar 17-23: Night Float
  - Thu Mar 24: Post-Call ✅ (day after NF ends)
Mar 25-30: Outpatient
  - Wed Mar 30 AM: Clinic ✅
Mar 31: Conference leave → No assignments ✅
```

**RES-PGY2-05 (PGY-2):**
```
Mar 12-18: NICU rotation
  - Fri Mar 18 PM: Clinic ✅ (NICU Friday requirement)
  - Tue Mar 15 PM: Clinic ✅ (correct day for PGY-2)
Mar 19-25: Outpatient
  - Tue Mar 22 PM: Clinic ✅
Mar 26-Apr 1: FMIT week
  - Tue Mar 29 PM: Clinic ✅
```

**RES-PGY3-01 (PGY-3):**
```
Mar 12-18: Procedures
  - Mon Mar 13 PM: Clinic ✅ (correct day for PGY-3)
Mar 19-25: Night Float
  - Thu Mar 26: Post-Call ✅
Mar 27-Apr 2: FMIT week
  - Mon Mar 27 PM: Clinic ✅
```

**Spot Check Summary:**
- Clinic days match PGY requirements: ✅
- Post-Call days after Night Float: ✅
- No double-booking detected: ✅
- Absences respected: ✅

> "Spot check passed. Schedule appears operationally sound for these residents."
