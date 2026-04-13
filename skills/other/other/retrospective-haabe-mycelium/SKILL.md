---
name: retrospective
description: "Structured retrospective after completing a delivery increment or diamond. Captures learning for continuous improvement."
---

# Retrospective

Run after every completed delivery diamond or significant milestone. Source: Forsgren (learning culture).

## Workflow

Run these steps IN ORDER. Do not skip any step. **Step 1 (cycle recording) MUST be completed FIRST — before any reflective analysis.**

### Step 1. Record Cycle in `canvas/cycle-history.yml` AND Decision Log (MANDATORY — DO THIS FIRST)

**This step is critical.** Without it, the learning metabolism has no data. You MUST do BOTH parts (5a and 5b).

#### Step 5a. Write cycle record to `canvas/cycle-history.yml`

Find the leaf_id and opportunity_id for the delivered solution (from `canvas/opportunities.yml` or `canvas/gist.yml`). Then write a cycle record:

```yaml
- cycle_id: cycle-NNN
  leaf_id: "opp-XXX-sol-X"         # From opportunities.yml
  opportunity_id: "opp-XXX"         # Parent opportunity
  diamond_id: "d-XXX"               # From diamonds/active.yml
  completed_at: "YYYY-MM-DDTHH:MM:SSZ"
  outcome: shipped | partial | failed | discarded
  predicted:
    ice_score: {i: X, c: X, e: X, total: XXX}  # ICE at time of scoring
    feasibility_risk: low | medium | high        # From four_risks
    effort_estimate: "X days/weeks"              # Original estimate
  actual:
    effort: "X days/weeks"                       # How long it actually took
    dora:                                        # From /dora-check or known metrics
      deploy_frequency: "..."
      lead_time: "..."
      change_failure_rate: "..."
      mttr: "..."
  calibration:
    ice_accuracy: "predicted XXX vs actual [outcome description]"
    effort_accuracy: "predicted X days vs actual X days (delta: +/-X)"
    risk_accuracy: "feasibility was [predicted] — actual was [description]"
  learnings: "Key learning from this cycle"
```

Update `calibration_summary.total_cycles` count. If total_cycles reaches a multiple of 5, prompt: "5 cycles since last review. Run `/framework-health` to check calibration?"

#### Step 5b. Log cycle calibration summary in decision-log.md

Write a decision log entry titled "Cycle calibration record" that includes ALL of the following (use these exact words):

- **cycle** number and diamond ID
- **predicted** ICE score and effort estimate (from the original canvas)
- **actual** outcome and effort (from what really happened)
- **calibration** assessment: was the prediction accurate?
- **effort** delta: if the estimate was an **underestimate** or overestimate, state the **accuracy** gap (e.g., "effort accuracy: predicted 5 days vs actual 7 days, 40% underestimate")
- Risk dimension accuracy (e.g., "feasibility was predicted medium — actual confirmed, analytics pipeline was indeed the hardest part")

This decision log entry ensures the calibration data is auditable alongside other decisions, not just buried in cycle-history.yml.

### Step 2. What Went Well?
- Which patterns from patterns.md were reused successfully?
- What new approaches worked?
- Where did the theory gates catch a real problem?

### Step 3. What Didn't Go Well?
- What mistakes were made? (Add to corrections.md)
- Where did we skip a guardrail and regret it?
- What took longer than expected and why?

### Step 4. What Should Change?
- New corrections to add
- New patterns to capture
- Process improvements
- Guardrail adjustments

### Step 5. BVSSH Dimension Check
- **Better**: Did quality improve or degrade?
- **Value**: Did we deliver actual user value?
- **Sooner**: Was our flow efficient?
- **Safer**: Did we maintain security and trust?
- **Happier**: How is team satisfaction?

## Root Cause Analysis (when "What Didn't Go Well" surfaces a significant problem)

Use these two complementary techniques. Fishbone gives breadth (all possible causes). 5 Whys gives depth (one cause traced to its root).

### Fishbone Diagram (Ishikawa)

Map all potential causes before investigating any. Structure:

```
                        ┌─ People (skills, handoffs, communication)
                        ├─ Process (gates, cadence, workflow)
Problem ◄───────────────├─ Product (canvas, evidence, assumptions)
(effect)                ├─ Platform (tools, infra, dependencies)
                        ├─ Principles (which theory/guardrail failed?)
                        └─ Pressures (deadlines, scope, external)
```

1. Write the specific problem at the head
2. Brainstorm causes in each category — add as branches
3. Drill into sub-causes until you reach actionable items
4. Vote/rank the most likely root causes for investigation

*Category set adapted for product development from Ishikawa's 6M manufacturing categories.*

### 5 Whys (Toyoda)

For the top-ranked cause from the fishbone, ask "why?" five times:

1. Why did this happen? → [first-level cause]
2. Why did that happen? → [second-level cause]
3. Why? → [deeper]
4. Why? → [deeper]
5. Why? → [root cause — usually systemic]

**Stop rule**: Stop when you reach something you can change systemically (a guardrail, a gate, a process step), not just a one-time fix.

**Anti-pattern**: Stopping at "human error" — that's never the root cause. Ask why the system allowed the error.

*Source: Ishikawa (cause-and-effect diagrams), Toyoda/Ohno (5 Whys), adapted for agentic product development.*

## Blameless Post-Mortem Format (SRE)

For incidents or significant failures, use the SRE blameless post-mortem:
1. **Timeline**: What happened, when, in what order
2. **Impact**: Who was affected, how severely, for how long
3. **Contributing factors**: What conditions led to this (NOT "who caused it")
4. **Root cause**: The systemic issue, not the human action (use fishbone + 5 Whys above)
5. **Action items**: Specific, assigned, time-bound improvements
6. **What went well**: What prevented it from being worse

Rule: No blame. Focus on the system, not the person. *Source: Beyer et al. (SRE)*

## Refactoring Prompt

After delivery retrospective, always ask:
- "Are there refactoring opportunities? Duplicated logic (DRY)? Unnecessary complexity (KISS)?"
*Source: Beck (XP), Fowler (Refactoring)*

## Output
1. Update `.claude/memory/corrections.md` with new corrections
2. Update `.claude/memory/patterns.md` with new patterns
3. Update `.claude/memory/delivery-journal.md` with retrospective entry
4. Update canvas/bvssh-health.yml if dimensions changed
5. Log in decision-log.md
6. Record cycle in `canvas/cycle-history.yml` (see Cycle History Recording above)
