---
name: refiner
description: Quality assurance orchestrator that refines outputs from other skills using standards-based evaluation and iterative improvement.
version: 1.0.0
---

# GabeDA Refiner Skill

## Purpose

This skill acts as a **quality assurance orchestrator** that ensures outputs from other skills meet production standards through systematic evaluation and iterative refinement.

**Core Functions:**
1. **Detect Skill** - Identify which skill should handle the task
2. **Load Standard** - Retrieve applicable quality standard from `ai/standards/`
3. **Execute Task** - Delegate to appropriate skill for initial work
4. **Evaluate Output** - Score work against standard (1-10 scale)
5. **Refine Iteratively** - Re-run skill with improvements until score >8 (max 3 iterations)
6. **Document Results** - Generate refinement report in `ai/refiner/`

## When to Use This Skill

Invoke this skill when:
- Work requires quality assurance against a defined standard
- Initial output quality is uncertain or needs validation
- Task requires iterative refinement until meeting threshold
- Need documented evaluation of work quality
- Producing customer-facing deliverables (landing pages, reports, dashboards)
- Creating production-ready artifacts (code, documentation, designs)

**NOT for:**
- Tasks without defined standards
- Quick prototypes or MVPs (where 8/10 quality not required)
- Tasks that don't involve other skills
- Exploratory research (no clear quality metrics)

## Core Workflow

### Step 1: Analyze Task and Detect Skill

**Process:**
1. Parse user request to understand deliverable type
2. Map deliverable to responsible skill
3. Identify applicable standard from `ai/standards/`

**Skill Mapping:**

| Deliverable Type | Primary Skill | Standard |
|------------------|---------------|----------|
| Webpage design, mockup, wireframe | ux-design | UX_DESIGN_STANDARD.md |
| Marketing copy, landing page, campaign | marketing | MARKETING_STANDARD.md |
| Business case, user research, ROI analysis | business | BUSINESS_STANDARD.md |
| Implementation plan, architecture, code | architect | ARCHITECT_STANDARD.md |
| Strategic plan, requirements, decision | executive | EXECUTIVE_STANDARD.md |
| Notebook, dashboard, visualization | insights | INSIGHTS_STANDARD.md |

**For detailed skill detection logic:** See [references/skill_detection_rules.md](references/skill_detection_rules.md)

---

### Step 2: Load Quality Standard

**Process:**
1. Read standard file from `ai/standards/[SKILL]_STANDARD.md`
2. Extract evaluation metrics and scoring rubric
3. Identify minimum passing score (typically 8.0/10)
4. Note any constraints (e.g., "no metric below 6/10")

**Standard Structure:**
All standards follow consistent format:
- **Metrics:** 6-8 measurable dimensions with 0-10 scoring
- **Passing Score:** Typically 8.0/10 average
- **Evaluation Template:** Structured scoring format
- **Refinement Guidance:** Common issues and fixes

**For standard interpretation guide:** See [references/standard_interpretation.md](references/standard_interpretation.md)

---

### Step 3: Execute Task with Skill

**Process:**
1. Invoke detected skill with user's original request
2. Allow skill to complete initial work
3. Capture output (file paths, content, deliverables)
4. Prepare output for evaluation

**Invocation Format:**
```
Skill([skill-name])

[User's original request - pass through verbatim]

[Additional context if needed]
```

**Notes:**
- Pass user request verbatim to skill (don't modify or interpret)
- Skills may create files, generate content, or produce artifacts
- Track all outputs for evaluation

---

### Step 4: Evaluate Against Standard

**Process:**
1. Apply standard's evaluation template to output
2. Score each metric individually (0-10)
3. Calculate overall score (average of metrics)
4. Document rationale for each score
5. Identify lowest-scoring metrics for improvement

**Evaluation Structure:**

```markdown
## Iteration [N] Evaluation

**Output:** [What was produced]
**Standard:** [Which standard applied]
**Date:** [YYYY-MM-DD]

### Scores

| Metric | Score | Rationale |
|--------|-------|-----------|
| [Metric 1] | X/10 | [Why this score] |
| [Metric 2] | X/10 | [Why this score] |
| ... | ... | ... |

**Overall Score:** XX/10

**Status:** [✅ PASS (>8.0) / 🟡 REFINE (≤8.0) / ❌ FAIL (<6.0)]
```

**For detailed evaluation guide:** See [references/evaluation_methodology.md](references/evaluation_methodology.md)

---

### Step 5: Refine Until Quality Threshold Met

**Decision Logic:**

**If Score > 8.0:** ✅ **PASS** → Proceed to Step 6 (document results)

**If Score ≤ 8.0:** 🟡 **REFINE** → Iterate:
1. Identify 2-3 lowest-scoring metrics
2. Generate specific improvement instructions
3. Re-invoke skill with refinement guidance
4. Re-evaluate improved output
5. Repeat up to **max 3 total iterations**

**If Score < 6.0 after 3 iterations:** ❌ **ESCALATE** → Invoke executive skill for guidance

**Refinement Format:**
```
Skill([skill-name])

**Refinement Request - Iteration [N+1]**

**Previous Output:** [Link/description]
**Current Score:** X.X/10 (needs >8.0)

**Areas Needing Improvement:**
1. [Metric Name] (scored X/10) - [Specific issue]
   - **Fix:** [Concrete action to take]
2. [Metric Name] (scored X/10) - [Specific issue]
   - **Fix:** [Concrete action to take]

**Standard Reference:** ai/standards/[STANDARD].md

Please refine the output focusing on these areas.
```

**Iteration Limits:**
- **Max 3 iterations total** (initial + 2 refinements)
- After 3 iterations:
  - If score >8.0: Document success
  - If score ≤8.0: Escalate to executive, document partial success with recommendations

**For refinement strategies:** See [references/refinement_strategies.md](references/refinement_strategies.md)

---

### Step 6: Generate Refinement Report

**Process:**
1. Create timestamped report in `ai/refiner/refinement_[task]_[YYYYMMDD_HHMM].md`
2. Document all iterations with scores
3. Include final deliverable location/content
4. Note any unresolved issues or escalations
5. Provide recommendations for future improvements

**Report Structure:**

```markdown
# Refinement Report: [Task Name]

**Date:** [YYYY-MM-DD HH:MM]
**Skill Used:** [skill-name]
**Standard Applied:** [STANDARD_NAME]
**Iterations:** [N] of 3

---

## Summary

**Task:** [User's original request]
**Final Score:** X.X/10 [✅ PASS / 🟡 PARTIAL / ❌ ESCALATED]
**Output Location:** [File path or description]

---

## Iteration History

### Iteration 1: Initial Output
- **Score:** X.X/10
- **Status:** [PASS/REFINE]
- **Metrics:** [Breakdown]
- **Issues:** [What needed improvement]

### Iteration 2: First Refinement (if needed)
- **Score:** X.X/10
- **Status:** [PASS/REFINE]
- **Improvements:** [What changed]
- **Remaining Issues:** [If any]

### Iteration 3: Second Refinement (if needed)
- **Score:** X.X/10
- **Status:** [PASS/REFINE/ESCALATED]
- **Improvements:** [What changed]
- **Final Issues:** [If any]

---

## Final Evaluation

[Complete scoring breakdown from final iteration]

---

## Deliverable

**Location:** [File path or link]
**Quality Level:** [Production-ready / Needs minor fixes / Requires major revision]

---

## Recommendations

**For This Task:**
- [Any remaining improvements for user to consider]

**For Future Similar Tasks:**
- [Patterns noticed that could improve first-iteration quality]

---

**Report Status:** [Complete / Escalated to Executive]
```

**Template:** [assets/templates/refinement_report_template.md](assets/templates/refinement_report_template.md)

---

## Skill Integration

### From Executive Skill
- **Receives:** Strategic tasks requiring quality assurance
- **Returns:** Quality-assured deliverables with evaluation reports

### To All Skills
- **Provides:** Task delegation with quality requirements
- **Requests:** Initial work and refinements
- **Monitors:** Quality progression through iterations

### To Executive Skill (Escalation)
- **Triggers:** Score <6.0 after 3 iterations
- **Provides:** Refinement history, blockers, recommendations
- **Requests:** Strategic guidance or requirement adjustment

---

## Common Patterns

### Pattern 1: Landing Page Design (ux-design)

**Task:** "Create landing page for Chilean SMB market"

**Process:**
1. Detect skill: ux-design
2. Load standard: UX_DESIGN_STANDARD.md (8 metrics)
3. Invoke ux-design skill with task
4. Evaluate: Likely needs 1-2 refinements (responsiveness, content clarity common issues)
5. Refine: Focus on mobile layout, Spanish content, Chilean context
6. Document: Report in ai/refiner/refinement_landing_page_chile_[timestamp].md

**Expected Iterations:** 2 (first draft 7.5/10, refined 8.5/10)

---

### Pattern 2: Marketing Campaign Copy (marketing)

**Task:** "Write launch email for new retention feature"

**Process:**
1. Detect skill: marketing
2. Load standard: MARKETING_STANDARD.md
3. Invoke marketing skill with task
4. Evaluate: Check positioning, value prop clarity, CTA strength
5. Refine: Sharpen messaging, add ROI stats, improve CTA
6. Document: Report in ai/refiner/refinement_launch_email_[timestamp].md

**Expected Iterations:** 1-2 (first draft typically 7.5-8.5/10)

---

### Pattern 3: Business Case Analysis (business)

**Task:** "Analyze ROI for Chilean market expansion"

**Process:**
1. Detect skill: business
2. Load standard: BUSINESS_STANDARD.md
3. Invoke business skill with task
4. Evaluate: Check data rigor, assumptions, risk analysis
5. Refine: Add sensitivity analysis, validate assumptions
6. Document: Report in ai/refiner/refinement_chile_roi_[timestamp].md

**Expected Iterations:** 1 (business skill typically produces 8.5+/10 on first pass)

---

## Working Directory

**Refiner Workspace:** `.claude/skills/refiner/`

**Bundled Resources:**
- `references/skill_detection_rules.md` - Mapping deliverables to skills
- `references/standard_interpretation.md` - How to read and apply standards
- `references/evaluation_methodology.md` - Scoring guidelines and calibration
- `references/refinement_strategies.md` - Common issues and fixes per skill
- `assets/templates/refinement_report_template.md` - Standard report format
- `assets/examples/` - Complete refinement examples (3 patterns)

**Quality Standards (Reference):**
- `/ai/standards/UX_DESIGN_STANDARD.md` - 8 metrics for UX work
- `/ai/standards/MARKETING_STANDARD.md` - Marketing quality metrics
- `/ai/standards/BUSINESS_STANDARD.md` - Business rigor metrics
- `/ai/standards/ARCHITECT_STANDARD.md` - Code quality metrics
- `/ai/standards/EXECUTIVE_STANDARD.md` - Strategic work metrics
- `/ai/standards/INSIGHTS_STANDARD.md` - Analysis quality metrics

**Output Reports (Create Here):**
- `/ai/refiner/refinement_[task]_[YYYYMMDD_HHMM].md` - Timestamped reports

**Living Documents (Append Only):**
- `/ai/SKILLS_MANAGEMENT.md` - Track refinement patterns and skill quality trends

---

## Quality Assurance Principles

### 1. Standards-Based Evaluation

**Principle:** All evaluation uses objective, documented standards (not subjective opinion).

**Application:**
- Every score must reference specific standard criteria
- Rationale must cite standard examples or checklists
- No "I think" or "feels like" - only "standard requires" or "checklist shows"

---

### 2. Constructive Refinement

**Principle:** Refinement requests provide actionable guidance (not vague criticism).

**Bad Example:** ❌ "Typography needs improvement"
**Good Example:** ✅ "Typography scored 7/10. Issues: Body text is 14px (standard requires 16px+). Fix: Increase body text to 16px."

---

### 3. Iteration Efficiency

**Principle:** Each refinement focuses on 2-3 highest-impact improvements (not everything at once).

**Strategy:**
- Iteration 1 → Fix lowest-scoring metric
- Iteration 2 → Fix next 2 lowest metrics
- Iteration 3 → Polish and edge cases

---

### 4. Escalation Discipline

**Principle:** Escalate when blocked, not when impatient.

**Escalate when:**
- Score <6.0 after 3 iterations (quality floor not met)
- Standard unclear or contradictory (need guidance)
- Task requirements conflict with standard (strategic decision needed)

**Don't escalate when:**
- Just need one more iteration (but already at max 3)
- Want to try different skill (refiner chooses skill, not user)

---

## Examples

### Example 1: UX Design Refinement

**Task:** "Design landing page for GabeDA Chilean market"

**Iteration 1:**
- ux-design creates initial design
- Score: 7.8/10 (mobile responsiveness 7/10, content clarity 7/10)
- Refine: Increase touch targets to 44px, translate to Spanish, add Chilean currency examples

**Iteration 2:**
- ux-design refines with improvements
- Score: 8.6/10 (all metrics 8+)
- ✅ PASS - Report generated

**Full Example:** [assets/examples/example_ux_refinement.md](assets/examples/example_ux_refinement.md)

---

### Example 2: Marketing Copy Refinement

**Task:** "Write email announcing customer retention feature"

**Iteration 1:**
- marketing creates initial email
- Score: 7.5/10 (value prop 7/10, CTA 7/10)
- Refine: Add specific ROI stat ("250:1 ROI for Chilean SMBs"), strengthen CTA ("Start Free Trial" vs "Learn More")

**Iteration 2:**
- marketing refines with improvements
- Score: 8.4/10 (all metrics 8+)
- ✅ PASS - Report generated

**Full Example:** [assets/examples/example_marketing_refinement.md](assets/examples/example_marketing_refinement.md)

---

### Example 3: Escalation Scenario

**Task:** "Create real-time anomaly detection dashboard"

**Iteration 1:**
- insights creates initial dashboard
- Score: 5.2/10 (technical complexity too high for target audience)

**Iteration 2:**
- insights simplifies dashboard
- Score: 6.8/10 (still too technical)

**Iteration 3:**
- insights further simplifies
- Score: 7.2/10 (can't reach 8+ without changing requirements)

**Escalation:**
- Invoke executive skill: "Target audience (small business owners) conflicts with feature complexity (real-time ML). Recommend: Simplify to daily anomaly alerts (not real-time)."

**Full Example:** [assets/examples/example_escalation.md](assets/examples/example_escalation.md)

---

## Version History

**v1.0.0** (2025-10-30)
- Initial version with 6-step refinement workflow
- Skill detection, standard loading, iterative evaluation
- Max 3 iterations, escalation to executive if needed
- Timestamped reports in ai/refiner/

---

**Last Updated:** 2025-10-30
**Core Principles:**
1. **Objective evaluation** - Standards-based, not opinion-based
2. **Actionable refinement** - Specific fixes, not vague feedback
3. **Iteration efficiency** - Focus on highest-impact improvements
4. **Quality floor** - 8.0/10 minimum for production work
5. **Escalation discipline** - Escalate blockers, not impatience
