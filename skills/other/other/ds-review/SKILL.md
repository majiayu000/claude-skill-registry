---
name: ds-review
description: "This skill should be used when running Phase 4 of the /ds workflow or reviewing data analysis methodology."
user-invocable: false
disable-model-invocation: true
hooks:
  PostToolUse:
    - matcher: "Agent"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-post-subagent-guard.py"
  PreToolUse:
    - matcher: "Agent"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-pre-subagent-clear.py"
    - matcher: "Read"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Grep"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Glob"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-read-after-subagent-guard.py"
    - matcher: "Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-no-main-chat-code-guard.py"
    - matcher: "Edit"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-no-main-chat-code-guard.py"
    - matcher: "Bash"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/ds-no-main-chat-code-guard.py"
---

Announce: "Using ds-review (Phase 4) to check methodology and quality."

## Context Monitoring

| Level | Remaining Context | Action |
|-------|------------------|--------|
| Normal | >35% | Proceed normally |
| Warning | 25-35% | Complete current review cycle, then trigger ds-handoff |
| Critical | ≤25% | Immediately trigger ds-handoff — do not start new review cycles |

## Review Strategy Choice

After announcing phase, choose review strategy.

**Skip this choice when:**
- Exploratory analysis (one-off, not for publication)
- Trivial changes (formatting, documentation)
- Internal reporting (low-stakes, quick turnaround)
- Single notebook with < 100 LOC

**Otherwise, ask the user:**

```python
AskUserQuestion(questions=[{
  "question": "How should we review this analysis?",
  "header": "Review Strategy",
  "options": [
    {"label": "Single reviewer (Default)", "description": "Combined review covering methodology, data quality, and reproducibility. Faster, lower overhead."},
    {"label": "Parallel review (Research-grade)", "description": "Spawn 3 specialized reviewers (Methodology, Reproducibility, Code quality). Use for publications, high-stakes decisions, or research-grade work. Requires reconciliation."}
  ],
  "multiSelect": false
}])
```

**If Single reviewer:** Proceed to [The Iron Law of DS Review](#the-iron-law-of-ds-review) below (current behavior).

**If Parallel review:** Skip to [Parallel Review (Research-Grade)](#parallel-review-research-grade).

---

## Parallel Review (Research-Grade)

Use this section when user chose "Parallel review (Research-grade)" above.

> **Prerequisite:** Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` enabled. If unavailable, fall back to single reviewer.

### 1. Prerequisites Check

Before spawning reviewers, verify:

1. **`.planning/SPEC.md` exists** - reviewers verify against spec, not assumptions
2. **`.planning/PLAN.md` exists** - reviewers check tasks were completed
3. **`.planning/LEARNINGS.md` exists** - reviewers verify data quality pipeline documented
4. **Analysis files identified** - notebooks/scripts in scope for review

If any prerequisite fails, STOP and return to /ds-implement.

### 2. When to Use Parallel Review

**Use parallel review when:**
- Publication-bound work (papers, reports, external sharing)
- High-stakes decisions (business strategy, funding, policy)
- Research-grade analysis (academic standards, peer review)
- Regulatory compliance (audit trail required)
- Complex methodology (multiple statistical methods, model comparisons)
- Large codebases (4+ notebooks, multiple scripts)

**Do NOT use when:**
- Exploratory analysis (one-off, not for publication)
- Internal reporting (low-stakes, quick answers)
- Simple descriptive stats (counts, means, basic visualizations)
- Overhead exceeds benefit (single notebook, < 100 LOC)

### 3. Create Team and Spawn Reviewers

#### Team Creation

```
TeamCreate(name="Analysis Review", task_description="Parallel analysis review with 3 specialized reviewers")
```

Press **Shift+Tab** to enter delegate mode. The lead coordinates reviews, does NOT review analysis directly.

#### Spawn 3 Reviewers

Each reviewer receives a self-contained prompt from a reference file. **Reviewers start with a blank conversation and do NOT auto-load skills.** Read the prompt, substitute variables, and paste it in full.

**Tool Restrictions:** All reviewers (Methodology, Reproducibility, Code Quality) are READ-ONLY with `allowed_tools=["Read", "Glob", "Grep", "Bash(read-only)"]`. Reviewers read code and data, run verification checks, and return verdicts. They MUST NOT use Write or Edit.

**Before spawning, substitute these variables in each prompt:**
- `ANALYSIS_FILES` → list of notebooks/scripts in scope (paste actual list)
- `SPEC_CONTEXT` → relevant sections of .planning/SPEC.md (paste inline, do NOT reference file)
- `PLAN_TASKS` → task list from .planning/PLAN.md (paste inline, verify completed)
- `LEARNINGS_PIPELINE` → data quality chain from .planning/LEARNINGS.md (paste inline)
- `PLUGIN_ROOT` → resolved base directory for skill paths (relative to this skill's base directory)

**Reviewer prompts (read, substitute variables, send as message):**

| Reviewer | Focus | Prompt Source |
|----------|-------|---------------|
| 1. Methodology | Statistical soundness, assumptions, bias | `references/methodology-reviewer.md` |
| 2. Reproducibility | Seeds, versions, data traceability | `references/reproducibility-reviewer.md` |
| 3. Code Quality | Data quality handling, bugs, efficiency | `references/code-quality-reviewer.md` |

---

### 4. Lead Monitoring

While reviewers work, the lead:

- **Watches for completion messages** from all 3 reviewers
- **Does NOT review analysis directly** - your job is coordination and reconciliation
- **If a reviewer asks a question:** Answer it, then broadcast to other reviewers if relevant
- **If a reviewer is taking significantly longer than others:** Message them for status
- **When all 3 reviewers complete:** Proceed to reconciliation

### 5. Reconciliation Protocol (3 Passes)

After ALL reviewers message completion, the lead performs three passes:

<EXTREMELY-IMPORTANT>
**Pass 1 — Deduplication:**

Multiple reviewers may find the same issue (e.g., missing seed found by both Reproducibility and Code Quality reviewers).

1. Read all reviewer findings
2. Group by file and location
3. Identify duplicates:
   - Same file:location
   - Same root cause (even if described differently)
4. Merge duplicates:
   - Keep the highest confidence score
   - Combine descriptions if both add value
   - Attribute to both reviewers

**Example:**
```
Reproducibility found: "notebook.ipynb cell 5 - Random seed not set (Confidence: 85)"
Code Quality found: "notebook.ipynb cell 5 - Stochastic operation unseeded (Confidence: 80)"

→ Merge: "notebook.ipynb cell 5 - Random seed missing for train_test_split (Confidence: 85, found by Reproducibility + Code Quality)"
```

**Pass 2 — Prioritization:**

Not all issues are equally important. Rank by:

1. **Severity × Confidence:**
   - Critical (90-100 confidence) > Important (80-89)
   - Methodology > Reproducibility > Code Quality (when confidence is equal)
2. **Impact on conclusions:**
   - Invalidates results > Affects interpretation > Inconvenient
   - Correctness > Reproducibility > Style
3. **Fix effort:**
   - Quick wins (< 30 min) should be fixed now
   - Large refactors (> 2 hours) should be documented as limitations

Create final prioritized list:
```
1. [CRITICAL] Methodology: Selection bias invalidates results (Confidence: 95)
2. [CRITICAL] Code Quality: Join explosion duplicates rows (Confidence: 90)
3. [IMPORTANT] Reproducibility: Random seed missing (Confidence: 85)
4. [IMPORTANT] Code Quality: High-null column in final data (Confidence: 80)
```

**Pass 3 — Integration Check:**

Proposed fixes may conflict with each other or create new problems.

1. Read each reviewer's suggested fixes
2. Check for conflicts:
   - Do two fixes modify the same code?
   - Does one fix introduce a problem another reviewer would flag?
   - Do fixes require contradictory approaches?
3. If conflicts exist:
   - Design a unified fix addressing all concerns
   - OR: Flag the conflict and ask reviewers for input

**Example conflict:**
```
Methodology: "Use stratified sampling to control for confounder"
Code Quality: "Simplify sampling code for readability"

→ Unified: "Use stratified sampling (methodology) with clear variable names and comments (code quality)"
```

**If ANY pass finds conflicts → resolve before reporting final verdict.**
</EXTREMELY-IMPORTANT>

### 6. Final Verdict

After reconciliation, the lead reports:

```markdown
## Parallel Analysis Review: [Analysis Name]

Reviewed by: Methodology, Reproducibility, Code Quality

### Reconciliation Summary

**Issues found:** X total (Y critical, Z important)
**Duplicates merged:** N
**Conflicts resolved:** M

### Critical Issues (Must Fix)

[Deduplicated, prioritized list from Pass 1 + 2]

### Important Issues (Should Fix)

[Deduplicated, prioritized list from Pass 1 + 2]

### Verdict: APPROVED | CHANGES REQUIRED

[If APPROVED]
All 3 reviewers approved with no issues >= 80 confidence. The analysis meets research-grade standards.

[If CHANGES REQUIRED]
X critical and Y important issues must be addressed. Return to /ds-implement.
```

After parallel review completes:

**If APPROVED:** Immediately discover and load the ds-verify skill:
Read `${CLAUDE_SKILL_DIR}/../../skills/ds-verify/SKILL.md` and follow its instructions.

**If CHANGES REQUIRED:** Return to `/ds-implement` to fix reported issues.

**Maximum 3 review cycles.** If issues persist after 3 rounds of review → implement → re-review, escalate to the user with a summary of unresolved issues. Do not loop indefinitely.

---

# Analysis Review

Single-pass review combining methodology correctness, data quality handling, and reproducibility checks. Uses confidence-based filtering.

<EXTREMELY-IMPORTANT>
## The Iron Law of DS Review

**You MUST only report issues with >= 80% confidence. This is not negotiable.**

Before reporting ANY issue, you MUST:
1. Verify it's not a false positive
2. Verify it impacts results or reproducibility
3. Assign a confidence score
4. Only report if score >= 80

This applies even when:
- "This methodology looks suspicious"
- "I think this might introduce bias"
- "The approach seems unusual"
- "I would have done it differently"

**STOP - If you catch yourself about to report a low-confidence issue, DISCARD IT. You're about to compromise the review's integrity.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## The Iron Law of Re-Review

**NO "FIXED" CLAIMS WITHOUT FRESH RE-REVIEW. This is not negotiable.**

When review returns CHANGES REQUIRED and the analyst applies fixes, you MUST:
1. Re-run the SAME review criteria (methodology, data quality, reproducibility)
2. Verify issues are actually resolved (not assumed)
3. Check for new issues introduced by fixes (data changes, methodology shifts)
4. Only THEN return APPROVED

"I fixed it" without re-reviewing is NOT HELPFUL — unverified fixes ship wrong results to the user.

### The Audit-Fix Loop (Max 3 Iterations)

```
Iteration 1: Review → CHANGES REQUIRED → Fix → Re-Review
              ↓
Iteration 2: Re-Review → CHANGES REQUIRED → Fix → Re-Review
              ↓
Iteration 3: Re-Review → CHANGES REQUIRED → Fix → Re-Review
              ↓
         Still issues? → ESCALATE to user
         All clean? → APPROVED
```

**Track iterations in `.planning/REVIEW_STATE.md`:**

```yaml
---
iteration: 1
max_iterations: 3
last_review_date: 2026-03-09
issues_found_count: 5
---
```

**Exit criteria:**
- **APPROVED**: Zero issues >= 80 confidence
- **ESCALATE**: iteration >= 3 AND issues remain
- **CONTINUE**: iteration < 3 AND issues remain → loop back

**Before returning any verdict, check iteration count:**
1. READ `.planning/REVIEW_STATE.md` (create if missing with iteration: 1)
2. If iteration >= 3 and issues remain: ESCALATE (don't return CHANGES REQUIRED)
3. If iteration < 3 and issues remain: INCREMENT iteration, return CHANGES REQUIRED
4. If no issues: APPROVED

**Claiming APPROVED without re-review after fixes is NOT HELPFUL — the user acts on an approval that has no verification behind it.**

### Rationalization Prevention (Re-Review)

| Thought | Reality | Do Instead |
|---------|---------|------------|
| "Analyst said they fixed it" | Their claim needs YOUR verification | Re-run review fresh |
| "Just spot-check the fixed analysis" | Spot-checks miss downstream impacts | Full re-review, same criteria |
| "We're on iteration 3, approve it" | Max iterations means ESCALATE, not approve | Return ESCALATE verdict |
| "The fixes are minor tweaks" | Minor analysis changes break conclusions | Re-review anyway |
| "We already spent too much time" | Publishing wrong results wastes more time | Re-review or escalate |
| "Results look reasonable now" | Reasonable-looking != methodologically sound | Re-run full review |

### Why Skipping Re-Review Hurts the Thing You Care About Most

You skip re-review because you think it's helpful, efficient, or competent. Here's what actually happens:

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|--------------|----------------------|---------------------|
| **Helpfulness** | "Approving fast delivers results" | Wrong results ship. User makes decisions on flawed analysis. The 20-minute re-review would have caught it. Your speed caused harm. | **Anti-helpful** |
| **Competence** | "I trust the methodology now" | Trust without re-checking is negligence. The selection bias remained. Reviewers catch it. Your approval was incompetent. | **Incompetent** |
| **Efficiency** | "Re-review wastes time on fixed issues" | The re-review takes 20 minutes. The retracted paper costs 20 weeks. Your "efficiency" destroyed months of work. | **Anti-efficient** |
| **Approval** | "User wants results now" | User retracts the paper when flaws surface. They now require external review for all analysis. You lost their trust. | **Lost approval** |
| **Honesty** | "The analyst said they fixed it" | You didn't verify — you rubber-stamped. You claimed "analysis is sound" based on trust, not evidence. Unverified approval wastes the user's time. | **Anti-helpful** |

**The protocol is not overhead you pay. It is the service you provide.**

Publishing wrong results is worse than slow results. The user experiences your conclusions, not your review process. Speed without correctness is malpractice.
</EXTREMELY-IMPORTANT>

## Red Flags - STOP Immediately If You Think:

| Thought | Why It's Wrong | Do Instead |
|---------|----------------|------------|
| "This looks wrong" | Your vague suspicion isn't evidence | Find concrete proof or discard |
| "I would do it differently" | Your style preference isn't a methodology error | Check if the approach is valid |
| "This might cause problems" | Your "might" means < 80% confidence | Find proof or discard |
| "Unusual approach" | Unusual isn't wrong—your bias toward familiar methods is clouding judgment | Verify the methodology is sound |

## Shared Enforcement

**Load shared ds constraints before reviewing.** Read `${CLAUDE_SKILL_DIR}/../../references/ds-common-constraints.md` for the full constraint index.

For review phase, load these specific constraints:
Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-data-quality-checks.md`
Read `${CLAUDE_SKILL_DIR}/../../references/constraints/ds-post-subagent-boundary.md`

Load conventions for review phase:
Read `${CLAUDE_SKILL_DIR}/../../references/ds-common-conventions.md` for the full convention index.
Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-assumption-over-evidence.md`
Read `${CLAUDE_SKILL_DIR}/../../references/conventions/ds-deferred-verification.md`

## Review Focus Areas

### Spec Compliance
- [ ] Verify all objectives from .planning/SPEC.md are addressed
- [ ] Confirm success criteria can be verified
- [ ] Check constraints were respected (especially replication requirements)
- [ ] Verify analysis answers the original question

### Data Quality Handling
- [ ] Confirm missing values handled appropriately (not ignored)
- [ ] Verify duplicates addressed (documented if kept)
- [ ] Check outliers considered (handled or justified)
- [ ] Verify data types correct (dates parsed, numerics not strings)
- [ ] Confirm filtering logic documented with counts

#### Independent Verification (MANDATORY)

<EXTREMELY-IMPORTANT>
**Do NOT trust the analyst's claims about data quality. Run these checks yourself.**

The analyst may have reported "no duplicates" without actually checking, or "handled missing values" by silently dropping rows. You MUST run independent verification.

**Load shared check definitions first.** Read `${CLAUDE_SKILL_DIR}/../../skills/ds-implement/references/ds-checks.md` and follow its instructions.

Run checks DQ1-DQ5, M1 from the shared definitions. This ensures ds-review and ds-fix use identical checks.
</EXTREMELY-IMPORTANT>

**Post-subagent boundary (C5):** After any review Task agent returns, do NOT read project source code or data files to "double-check." Read the agent's report only. If issues found, re-dispatch.

Dispatch a Task agent to run these checks on the final analysis data:

```python
# 1. Empty/constant columns (useless data kept in analysis)
for col in df.columns:
    if df[col].nunique() <= 1:
        print(f"WARNING: {col} is constant or empty ({df[col].nunique()} unique values)")

# 2. High-null columns still in analysis
null_pct = df.isnull().mean()
high_null = null_pct[null_pct > 0.5]
if len(high_null) > 0:
    print(f"WARNING: Columns >50% null still in data:\n{high_null}")

# 3. Duplicate rows on key columns
key_cols = [...]  # from PLAN.md
dupes = df.duplicated(subset=key_cols, keep=False)
if dupes.sum() > 0:
    print(f"WARNING: {dupes.sum()} duplicate rows on {key_cols}")
    print(df[dupes].head())

# 4. Row count traceability
# Compare: raw input rows → after cleaning → after joins → final
# Each step should be documented in LEARNINGS.md
print(f"Final row count: {len(df)}")
# Verify this matches the chain documented in LEARNINGS.md

# 5. Cardinality check on categorical columns
for col in df.select_dtypes(include='object').columns:
    n_unique = df[col].nunique()
    if n_unique > 0.9 * len(df):
        print(f"WARNING: {col} has near-unique cardinality ({n_unique}/{len(df)}) — likely an ID, not a category")
    if n_unique == len(df):
        print(f"INFO: {col} is fully unique — confirm this is a key, not a category used in groupby")
```

**If ANY check produces a WARNING, this is a high-confidence issue (>=80). Report it.**

### Methodology Appropriateness
- [ ] Verify statistical methods appropriate for data type
- [ ] Check assumptions documented and verified (normality, independence, etc.)
- [ ] Confirm sample sizes adequate for conclusions
- [ ] Check multiple comparisons addressed if applicable
- [ ] Verify causality claims justified (or appropriately limited)

### Reproducibility
- [ ] Verify random seeds set where needed
- [ ] Check package versions documented
- [ ] Verify data source/version documented
- [ ] Confirm all transformations traceable
- [ ] Verify results can be regenerated

### Output Quality
- [ ] Verify visualizations labeled (title, axes, legend)
- [ ] Check numbers formatted appropriately (sig figs, units)
- [ ] Verify conclusions supported by evidence shown
- [ ] Confirm limitations acknowledged

## Confidence Scoring

Rate each potential issue from 0-100:

| Score | Meaning |
|-------|---------|
| 0 | False positive or style preference |
| 25 | Might be real, methodology is unusual but valid |
| 50 | Real issue but minor impact on conclusions |
| 75 | Verified issue, impacts result interpretation |
| 100 | Certain error that invalidates conclusions |

**CRITICAL: You MUST only report issues with confidence >= 80. If you report below this threshold, you're misrepresenting your certainty.**

## Common DS Issues to Check

### Data Leakage
- Training data contains information from future
- Test data used in feature engineering
- Target variable used directly or indirectly in features

### Selection Bias
- Filtering introduced systematic bias
- Survivorship bias in longitudinal data (analyzing only surviving entities — e.g., only companies that didn't delist)
- Non-random sampling not addressed

### Join Explosion
- Many-to-many joins silently multiplying rows
- Detection: compare `COUNT(*)` before and after join — any increase signals duplication
```sql
SELECT 'before' AS stage, COUNT(*) FROM a
UNION ALL
SELECT 'after', COUNT(*) FROM a JOIN b ON a.key = b.key;
```
- Always check join key uniqueness: `SELECT key, COUNT(*) FROM b GROUP BY key HAVING COUNT(*) > 1`

### Incomplete Period Comparison
- Comparing a partial current period (e.g., this month so far) to a full prior period
- Metrics will always look lower for the incomplete period — normalize by days elapsed or filter to complete periods only

### Denominator Shifting
- Rate or ratio denominators change between periods, making rates incomparable
- Example: "conversion rate dropped" but actually the denominator (total visitors) grew while numerator stayed flat
- Always report both numerator and denominator, not just the ratio

### Average of Averages
- Averaging pre-computed group averages produces incorrect results when group sizes differ
- Must compute weighted average or aggregate from raw data
- Example: avg(store_avg_price) ≠ avg(price) across all items

### Timezone Mismatches
- Different data sources using different timezones (UTC vs local vs server time)
- Symptoms: off-by-one day counts, missing hours around DST transitions, events appearing at impossible times
- Always document timezone assumptions per source and convert to a single timezone early in the pipeline

### Simpson's Paradox
- Aggregate trend reverses when data is segmented by a confounding variable
- Example: treatment appears better overall but worse in every subgroup because of unequal group sizes
- When reporting aggregate results, always check if the trend holds within key segments

### Statistical Errors
- Multiple testing without correction
- p-hacking or selective reporting
- Correlation interpreted as causation
- Inadequate sample size for claimed precision

### Reproducibility Failures
- Random operations without seeds
- Undocumented data preprocessing
- Hard-coded paths or environment dependencies
- Missing package versions

## Required Output Structure

```markdown
## Analysis Review: [Analysis Name]
Reviewing: [files/notebooks being reviewed]

### Critical Issues (Confidence >= 90)

#### [Issue Title] (Confidence: XX)

**Location:** `file/path.py:line` or `notebook.ipynb cell N`

**Problem:** Clear description of the issue

**Impact:** How this affects results/conclusions

**Requirement:** [REQ-ID from SPEC.md if this issue relates to a specific requirement, or "general"]

**Fix:**
```python
# Specific fix
```

### Important Issues (Confidence 80-89)

[Same format as Critical Issues]

### Data Quality Checklist

| Check | Status | Notes |
|-------|--------|-------|
| Missing values | PASS/FAIL | [details] |
| Duplicates | PASS/FAIL | [details] |
| Outliers | PASS/FAIL | [details] |
| Type correctness | PASS/FAIL | [details] |

### Methodology Checklist

| Check | Status | Notes |
|-------|--------|-------|
| Appropriate for data | PASS/FAIL | [details] |
| Assumptions checked | PASS/FAIL | [details] |
| Sample size adequate | PASS/FAIL | [details] |

### Reproducibility Checklist

| Check | Status | Notes |
|-------|--------|-------|
| Seeds set | PASS/FAIL | [details] |
| Versions documented | PASS/FAIL | [details] |
| Data versioned | PASS/FAIL | [details] |

### Summary

**Verdict:** APPROVED | CHANGES REQUIRED

[If APPROVED]
The analysis meets quality standards. No methodology issues with confidence >= 80 detected.

[If CHANGES REQUIRED]
X critical issues and Y important issues must be addressed before proceeding.
```

## Agent Invocation

Spawn a Task agent to review the analysis:

```
Task(subagent_type="general-purpose",
  allowed_tools=["Read", "Glob", "Grep", "Bash(read-only)"],
  prompt="""
Review analysis against .planning/SPEC.md.

Execute TWO-PASS review:

PASS 1 - Independent Data Quality Verification (RUN CODE):
1. Load the final analysis data
2. Check for empty/constant columns (nunique <= 1)
3. Check for high-null columns (>50% null)
4. Check for duplicate rows on key columns
5. Verify row count matches LEARNINGS.md chain
6. Check cardinality of categorical columns
Report any WARNING as confidence >= 80.

PASS 2 - Methodology and Compliance Review (READ CODE):
1. Spec compliance - verify all SPEC.md objectives addressed
2. Data quality handling - confirm issues from PLAN.md were resolved
3. Methodology - verify appropriate methods, assumptions checked
4. Reproducibility - confirm seeds, versions, documentation

Confidence score each issue (0-100).
Report only issues with >= 80 confidence.
Return structured output per /ds-review format.
""")
```

### Drive-Aligned Framing

**Approving analysis without running independent verification code is NOT HELPFUL — the user acts on results no one actually checked.** Reading the analyst's notebook and thinking "looks reasonable" is not verification. If you did not execute code that independently checks the results, you did not review — you rubber-stamped.

| Drive | Shortcut | Consequence |
|-------|----------|-------------|
| **Helpfulness** | Trusting analyst claims | You trusted 'data is clean' without checking. The results are wrong — your trust caused the user to publish flawed analysis. Anti-helpful. |
| **Competence** | Reporting low-confidence issues | You flagged issues below 80% confidence to appear thorough. Noise drowns signal — the real issues get lost. Incompetent review. |
| **Efficiency** | Not running verification code | You read the notebook instead of executing checks. The 30-second verification would have caught the join explosion that took 3 days to debug. Anti-efficient. |
| **Approval** | Rubber-stamping to avoid conflict | You approved to keep things moving. The user retracts when flaws surface. They now require external review. You lost their trust. |
| **Honesty** | Skipping independent verification | You reported 'methodology sound' without running anything. The user publishes wrong results — your unverified approval wasted their time. |

## Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "Analyst said data was clean" | Their claim is not evidence. They may have skipped checks. | Run independent verification yourself |
| "I already read LEARNINGS.md, quality looks fine" | Reading a report is not verification | Execute the verification code patterns on actual data |
| "Running checks would take too long" | Your unverified approval costs days of rework downstream | Run the checks. They take seconds. |
| "The output-first protocol already caught issues" | Output-first catches per-step issues, not cumulative ones | Check final state independently |
| "No point re-checking, I trust the methodology" | Trust is not verification. Your job is adversarial review. | Verify, then trust |
| "Minor data issues won't affect conclusions" | You don't know that without checking the magnitude | Quantify the impact, then decide |

## Delete & Restart: Fundamental Methodology Failures

<EXTREMELY-IMPORTANT>
**If methodology is fundamentally flawed, DELETE the implementation and return to ds-plan. No patching.**

A methodology is fundamentally flawed when:
- **Wrong statistical approach** (e.g., linear regression on non-linear data, parametric test on non-normal data without justification)
- **Wrong data source** (e.g., using quarterly data when daily is required, wrong table entirely)
- **Missing critical variable** (e.g., no control for a known confounder, omitted variable bias)
- **Wrong unit of analysis** (e.g., analyzing at firm-level when the question is about transactions)

| Thought | Action |
|---------|--------|
| "The approach is mostly right, just needs tweaking" | If the statistical method is wrong, tweaking parameters is p-hacking. DELETE and replan. |
| "We can add the missing variable as a robustness check" | If the variable is a known confounder, the main analysis is invalid. DELETE and replan with it included. |
| "Let's patch the methodology and re-review" | Patching a flawed foundation produces a patched flawed analysis. DELETE and replan from scratch. |

**When you identify a fundamental flaw:**
1. Document the flaw in LEARNINGS.md (what's wrong and why it can't be patched)
2. Report to user: "Methodology is fundamentally flawed: [specific reason]. Returning to ds-plan."
3. Return to ds-plan (not ds-implement) — the plan itself needs rethinking

**Patching a broken methodology to avoid rework is NOT HELPFUL — the user deserves correct analysis, not fast wrong analysis.**
</EXTREMELY-IMPORTANT>

## Quality Standards

- **You must NOT report methodology preferences not backed by statistical principles.** Your opinion about how code should be written is not a review issue.
- **You must treat alternative valid approaches as non-issues (confidence = 0).** If the approach works correctly, don't report it.
- Ensure each reported issue is immediately actionable
- **If you're unsure, rate it below 80 confidence.** Uncertainty is not a reason to report—it's a reason to investigate more.
- Focus on what affects conclusions, not style. **STOP if you catch yourself criticizing coding style—that's not your role here.**

## Gate: Exit Review Loop

**Checkpoint type:** human-verify (review scores are machine-verifiable)

Before claiming review is complete (APPROVED or ESCALATE):

```
1. IDENTIFY → What proves the review verdict is valid?
             - APPROVED: Zero issues >= 80 confidence
             - ESCALATE: iteration >= 3 AND issues remain

2. RUN     → Check `.planning/REVIEW_STATE.md` for iteration count
             Read review output for issue count

3. READ    → Examine both:
             - Review output (issues list)
             - REVIEW_STATE.md (iteration number)

4. VERIFY  → Verdict matches state:
             - APPROVED only if 0 issues
             - ESCALATE only if iteration >= 3
             - CHANGES REQUIRED only if iteration < 3

5. CLAIM   → Only after steps 1-4 pass, return verdict
```

**If iteration >= 3 and you're returning CHANGES REQUIRED instead of ESCALATE, you're being anti-helpful — the user needs to know when the loop isn't converging.**

## Phase Complete

After review completes, handle verdict-specific transitions:

### If APPROVED (no issues >= 80 confidence)

Mark review complete in `.planning/REVIEW_STATE.md`:

```yaml
---
iteration: [N]
max_iterations: 3
last_review_date: [date]
issues_found_count: 0
verdict: APPROVED
---
```

Immediately discover and load ds-verify:
Read `${CLAUDE_SKILL_DIR}/../../skills/ds-verify/SKILL.md` and follow its instructions.

### If CHANGES REQUIRED (issues >= 80 confidence found, iteration < 3)

Update `.planning/REVIEW_STATE.md`:

```yaml
---
iteration: [N+1]
max_iterations: 3
last_review_date: [date]
issues_found_count: [count]
verdict: CHANGES_REQUIRED
---
```

Return to `/ds-implement` with specific issues. **Analyst MUST re-invoke /ds-review after fixes.**

**Critical:** When analyst returns claiming "fixed", you MUST re-run the FULL review. No shortcuts.

### If ESCALATE (iteration >= 3, issues remain)

Update `.planning/REVIEW_STATE.md`:

```yaml
---
iteration: 3
max_iterations: 3
last_review_date: [date]
issues_found_count: [count]
verdict: ESCALATE
---
```

Report to user:

```
Review Loop Escalation (3 iterations completed)

After 3 fix-review cycles, [N] issues remain:

[List issues]

Options:
1. Accept current state and document limitations
2. Extend review (manual approval for iteration 4+)
3. Rethink methodology (return to /ds-plan)

Which option do you prefer?
```

## Workflow Continuity After Review

| Verdict | Next Action | Iteration Counter |
|---------|-------------|-------------------|
| APPROVED | Invoke /ds-verify immediately | Reset to 1 for next analysis |
| CHANGES REQUIRED | Return to /ds-implement, analyst fixes then re-invokes /ds-review | Increment |
| ESCALATE | Ask user for direction | Keep at max |

**Do NOT pause between review completion and next action.** The workflow is sequential.
