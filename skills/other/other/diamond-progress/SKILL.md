---
name: diamond-progress
description: "Progress a diamond from one phase to the next. Runs all required theory gate checks, validates evidence, and at Deliver->Complete runs the executable Definition of Done checklist."
---

# Diamond Progress Skill

Progress a diamond through phases with full theory gate validation. At delivery completion, runs an executable checklist that GATES progression.

## Workflow

1. **Identify transition**: From [current phase] to [next phase] at [scale].

2. **Run all required theory gates** (per theory-gates.md transition matrix):
   - For each gate:
     a. State the gate name and source theory.
     b. **Surface the suggested skill**: "Run `/skill-name` to satisfy this gate."
     c. Evaluate pass criteria against available evidence.
     d. Record Pass / Fail / Insufficient Evidence.
     e. If Fail: document what is missing, recommend the skill to run, and do NOT proceed.

   **CRITICAL — Perspective conflict check (do this BEFORE evaluating any other gate)**:
   Before checking any gate status, read `canvas/opportunities.yml` and inspect the Four Risks risk LEVELS for the active solution. Do NOT rely on `theory_gates_status.four_risks` in active.yml — that only records whether risks are documented, not whether they conflict. You must read the actual `value.level`, `usability.level`, `feasibility.level`, `viability.level` values.

   If TWO OR MORE risk dimensions are rated HIGH, or if perspectives directly contradict each other (e.g., value says "build it" but usability/feasibility say "don't"), this is a **perspective conflict** — not a simple gate failure. STOP evaluating other gates and jump to step 2b immediately. This takes priority over all other gate checks.

2b. **Resolve perspective conflict** (if detected in step 2):
   Do NOT continue to steps 3-6. A perspective conflict must be resolved before any other gate evaluation matters. Follow this procedure:

   1. **Name the conflict explicitly** in the decision log: "Perspective conflict: [type]" — use the vocabulary from `engine/perspective-resolution.md` (value-vs-feasibility, usability-vs-feasibility, value-vs-viability, usability-vs-viability, three-way).
   2. **Classify the conflict type** per the resolution framework.
   3. **State each perspective's position**:
      - Product perspective: what does the value evidence say?
      - Design perspective: what does the usability evidence say?
      - Engineering perspective: what does the feasibility evidence say?
   4. **Apply the resolution methods in order of preference**:
      - Constraint-based: Can all three perspectives be satisfied within acceptable thresholds?
      - Phased: Can we deliver in stages? (Phase 1 = MVP addressing highest risk, Phase 2 = polish)
      - Evidence-based: Can we test the disputed dimension? (Run `/assumption-test` on the riskiest assumption)
      - Scope reduction: Can we remove features until all perspectives align?
   5. **Log the resolution** in decision-log.md with: the conflict type, each perspective's position, the resolution method chosen, and why.
   6. **Block progression**: Report "Progression blocked: perspective conflict ([type]). Recommended resolution: [method]."
   7. Do NOT proceed to step 3 or beyond. The conflict must be resolved first.

   The perspective resolution framework (`engine/perspective-resolution.md`) is the authoritative reference. The anti-pattern to avoid is Perspective Suppression — resolving a conflict by ignoring one perspective.

3. **Calculate confidence**:
   - Apply scoring rules from confidence-thresholds.yml.
   - Look up `project_type` and `dogfood` from `diamonds/active.yml`.
   - Apply `project_type_adaptations` from confidence-thresholds.yml:
     - `effective_threshold = base_threshold * threshold_multiplier`
     - If `dogfood: true`: `effective_threshold *= dogfood_modifier.additional_threshold_multiplier`
     - `effective_min_sources = ceil(base_min_sources * min_sources_multiplier)`
   - Compare confidence to the **effective** threshold (not the base).
   - Report both: "Confidence: 0.55. Effective threshold: 0.57 (base 0.85, adapted for solo_product). Needs: one more evidence source to cross."

4. **Check human approval requirement**:
   - Per confidence-thresholds.yml, is human approval required/recommended/optional?
   - If required: present assessment and wait for approval.

5. **Run bias check**: Execute bias-check for the current stage.

6. **Run corrections check**: Review corrections.md for relevant entries.

6b. **Check trio perspective coverage** (Torres Product Trio):
   - For each gate evaluated in step 2, verify all three perspectives (product/design/engineering) are documented.
   - Each perspective must have evidence or an explicit "N/A: [reason]" justification.
   - Missing perspectives without justification = **GATE FAILED** (Perspective Skip anti-pattern).
   - See `engine/theory-gates.md` §Trio Perspective Requirement for per-scale guidance.
   - Note: Perspective CONFLICTS (2+ HIGH risk dimensions) are caught in step 2b, not here. This step checks for missing perspectives, not conflicting ones.

7. **If transition is Deliver -> Complete: RUN EXECUTABLE DoD CHECKLIST** (see below)

8. **Decision**:
   - All gates pass + confidence met + approval (if needed) + DoD pass (if delivery) = **PROGRESS**
   - Any REVIEW item fails = **blocked** (list specific blockers with suggested skills)
   - Confidence below threshold = **NEEDS EVIDENCE** (list what would help)

9. **If progressing**:
   - Update diamond state in active.yml.
   - Log transition in decision-log.md. If threshold was adapted, include: "Threshold adapted from [base] to [effective] because project_type=[type]. Would increase with [action]."
   - Update product-journal.md.
   - Identify if child diamonds should be spawned.
   - **Capture learnings** (see Learning Capture section below)

10. **If blocked or needs evidence**:
    - Report in plain language: "Can't mark this done yet because [reason]."
    - List each failed item with its suggested skill
    - Do not progress. Stay in current phase.

11. **Always communicate in plain language**:
    - Use status-translations.md for all state descriptions
    - Include contextual confidence explanation
    - Suggest specific skills for any gaps

---

## Executable Definition of Done (Deliver -> Complete ONLY)

When transitioning from Deliver to Complete, run this checklist. Items marked `REVIEW` block progression. Items marked `PROMPTED` are asked but don't block.

### Auto-Checked (Machine Verifiable)

Check `product_type` from `diamonds/active.yml` to determine which auto-checks apply.

**For software and ai_tool (code components):**

**Testing (G-V7 REVIEW)**:
- Check: Do test files exist? (glob for *.test.*, *.spec.*, Tests/*, __tests__/*)
- If no tests AND project has source files: **GATE FAILED**
- Message: "No tests found. Tests must exist before marking delivery complete. Run /reflexion to add tests."
- If tests exist: run them and verify they pass

**Type Safety (REVIEW for typed languages)**:
- Check: If tsconfig.json, *.swift, *.cs, go.mod, Cargo.toml detected: run type checker
- If type errors: **GATE FAILED**

**Linting (REVIEW if linter detected)**:
- Check: If linter config exists (.eslintrc, biome.json, .swiftlint.yml, ruff.toml): run it
- If lint errors: **GATE FAILED**

**For content products (content_course, content_publication, content_media):**

**Content Quality (REVIEW)**:
- Check: Are `content-metrics.yml#quality_review` flags all true? (sme_reviewed, accessibility_checked, fact_checked, style_consistent, learning_objectives_met)
- If any flag is false: **GATE FAILED** -- "Content quality review incomplete. Set the relevant flags in content-metrics.yml after completing review."
- Fallback: If content-metrics.yml doesn't exist yet, ask: "Has content been reviewed? Create content-metrics.yml and mark quality_review flags."

**For ai_tool:**

**Eval & Safety (REVIEW)**:
- Check: Are `ai-tool-metrics.yml#prompt_quality` fields populated (not null)? Specifically: accuracy_score, consistency_score, safety_score.
- If any are null: **GATE FAILED** -- "Prompt/model must be evaluated. Populate accuracy_score, consistency_score, and safety_score in ai-tool-metrics.yml."
- Check: Is `ai-tool-metrics.yml#prompt_quality.last_evaluated` set?
- If null: **GATE FAILED** -- "No evaluation timestamp. Run eval and record the date."

**For all product types:**

**Secrets (G-S1 BLOCK)**:
- Check: Scan all project files for secret patterns (same as gate.sh)
- If secrets found: **GATE FAILED**

### Delivery-Type Dependent (from canvas-guidance.yml)

**For user_facing work (G-V2, G-V8, G-V9 REVIEW)**:
- Check: Has services.yml been assessed? (count of "not-assessed" < 15)
- If all 15 are "not-assessed": **GATE FAILED** -- "Run /service-check before completing."
- Check: Has accessibility been considered? (any evidence of a11y work)
- If no evidence: **GATE FAILED** -- "Run /a11y-check for user-facing work."
- Check: Has usability been evaluated? (Nielsen's 10 heuristics via /usability-check)
- If no evidence: **GATE FAILED** -- "Run /usability-check for user-facing interfaces." (G-V10)

**For api_service or permission_requiring work (G-S2 REVIEW)**:
- Check: Does threat-model.yml have components listed?
- If empty: **GATE FAILED** -- "Run /threat-model for work that handles data or requires permissions."

**For data-handling work (G-S3 REVIEW)**:
- Check: Does privacy-assessment.yml have principles assessed?
- If all "not-assessed" and product handles user data: **GATE FAILED** -- "Run /privacy-check."

### Always Required (REVIEW)

**Decision log (G-P4)**:
- Check: Does decision-log.md have an entry for this delivery?
- If no entry since diamond was created: **GATE FAILED** -- "Log the delivery decision."

**BVSSH Quick-Check (Smart -- Fix 6)**:
- Prompt the user/agent with product-type-appropriate questions:

  **Software:**
  - "Better: Did code quality improve or degrade?"
  - "Value: Did we deliver measurable user value?"
  - "Sooner: Was deployment flow efficient? Any unnecessary delays?"
  - "Safer: Did we maintain security, reliability, and trust?"
  - "Happier: How is developer/team satisfaction?"

  **Content (course, publication, media):**
  - "Better: Did content quality and learning outcomes improve?"
  - "Value: Will this content help the audience accomplish their goal?"
  - "Sooner: Was production cadence maintained? Any bottlenecks?"
  - "Safer: Is the content accurate, accessible, and free from harm?"
  - "Happier: How is creator satisfaction? Audience sentiment?"

  **AI tool:**
  - "Better: Did eval scores improve? Is output quality higher?"
  - "Value: Does the tool reliably help users accomplish their task?"
  - "Sooner: Was the prompt/model iteration cycle efficient?"
  - "Safer: Are safety scores acceptable? Bias assessed? Regulatory status current?"
  - "Happier: How is the builder's satisfaction? User feedback positive?"

  **Service offering:**
  - "Better: Did delivery quality improve? Client satisfaction up?"
  - "Value: Did the client get measurable value from the engagement?"
  - "Sooner: Was delivery lead time acceptable? Any waiting waste?"
  - "Safer: Were commitments met? Trust maintained? No scope creep harm?"
  - "Happier: How is your satisfaction as a service provider? Client sentiment?"
- Record in bvssh-health.yml assessment_history
- **REVIEW**: Must answer all 5 (even briefly) before completing

### Prompted (Not Blocking)

**Delivery journal (PROMPTED)**:
- "What was built? What technical decisions were made? What surprised you?"
- Auto-draft entry from canvas diff if possible
- Present to user for confirmation

**Patterns (PROMPTED)**:
- "Did you discover any reusable patterns? I'll draft for patterns.md."
- Check corrections.md for entries logged during this diamond -- suggest generalizing any

**Retrospective (PROMPTED)**:
- "What went well? What didn't? What to change next time?"
- Suggest /retrospective for deeper review

---

## Non-Progression Paths: Pivot, Park, Kill

Not every diamond makes forward progress. Sometimes the right move is to reframe, pause, or abandon. `/diamond-progress` handles these paths too, via subcommands:

- `/diamond-progress pivot` — reframe the diamond's scope, audience, or JTBD with new evidence
- `/diamond-progress park` — mark the diamond as inactive-pending-conditions
- `/diamond-progress kill` — abandon with a documented reason

All three are **sanctioned exits** from a stuck diamond. They are not failure modes — they are the system working correctly when evidence tells you the current direction is wrong.

Addresses dogfood report finding T5: "Stop-the-diamond pattern has no escape valve."

### Pivot (reframe with new evidence)

Use when evidence invalidates the current framing but the underlying need is still valid. Example: macos-fileviewer pivoted from "replace QuickLook for all devs" to "serve terminal-resistant devs specifically" after mocked-persona findings.

**Workflow**:
1. State the invalidating evidence (what did we learn that broke the old framing?)
2. Propose the new framing (scope change, audience change, JTBD refinement)
3. Log decision in decision-log.md with:
   - Original framing
   - Invalidating evidence
   - New framing
   - Theory: which framework informed the pivot (Torres "evidence-guided", Cagan "value risk", etc.)
   - Confidence delta (the pivot should REDUCE confidence initially — you have less evidence for the new framing)
4. Update `diamonds/active.yml`:
   - Phase often regresses (e.g., Define → Discover) to gather evidence on the new framing
   - Confidence resets to match the new framing's evidence level
   - Add `pivot_history` entry listing old and new framings
5. Update relevant canvas files (purpose.yml, jobs-to-be-done.yml, opportunities.yml)
6. Do NOT archive the old framing — keep it as a pivot_history entry so future agents can see the learning

### Park (inactive-pending-conditions)

Use when the diamond cannot progress right now but may be revisitable later. Example: "park until I have time to do real user interviews" or "park until upstream dependency X ships."

**Workflow**:
1. State the blocking condition(s) — what would un-park this?
2. Log decision in decision-log.md with:
   - Reason for parking
   - Conditions for resuming
   - Expected timeline (best guess)
   - Theory: Goldratt ToC (constraint waiting on resolution) or Torres (evidence insufficient, acceptable to pause)
3. Update `diamonds/active.yml`:
   - State → `parked`
   - Add `parked_reason`, `parked_at`, `resume_conditions` fields
4. Parked diamonds remain in active.yml but do not count against WIP limits
5. `/feedback-review` and `/diamond-assess` surface parked diamonds with their resume conditions at session start

### Kill (abandon with documented reason)

Use when the diamond cannot be rescued via pivot or park. Example: the opportunity turned out to be imaginary (no real users, no demand), or the solution space has been exhausted, or the project direction has fundamentally changed.

**Workflow**:
1. State the reason for killing — what evidence makes this diamond dead?
2. Confirm with user (kill is destructive) — present the reason, ask for explicit confirmation
3. Log decision in decision-log.md with:
   - Final state of the diamond
   - Reason for kill
   - Alternatives considered (why not pivot, why not park?)
   - Theory: Kahneman (sunk cost fallacy — kill is correct when evidence says continuing is worse than stopping)
   - What we learned (the learning is the deliverable for a killed diamond)
4. Update `diamonds/active.yml`:
   - Move to `killed_diamonds` section (NOT deleted — canvas data is preserved)
   - Add `killed_at`, `killed_reason`, `learnings` fields
5. Do NOT delete canvas artifacts associated with the killed diamond — they are learning for future work
6. Capture the learning in `memory/patterns.md` and `memory/corrections.md` as appropriate
7. **Record cycle in `canvas/cycle-history.yml`**: Killed diamonds are terminal states. Record predicted ICE/effort, actual outcome as "killed", reason, and phase at kill. This feeds adaptive thresholds and pattern detection.

### Dogfood Mode Modifier (from canvas-guidance.yml)

When the project has `dogfood: true` set, stop conditions become Mycelium learnings rather than project deaths. In dogfood mode, a killed diamond generates a dogfood report entry in `.claude/evals/dogfood-reports/` instead of only being logged as a project kill. The framework gap caught is the real deliverable.

---

## Learning Capture (After Every Phase Transition)

After EVERY successful transition (not just Deliver->Complete):

1. **Corrections**: "Were any mistakes made during this phase? I'll draft a corrections.md entry."
2. **Patterns**: "Did anything work particularly well that's worth reusing?"
3. **Delivery journal** (delivery phases only): "What implementation decisions and learnings should be recorded?"
4. **Product journal** (discovery phases only): "What insights changed our understanding?"

Draft entries for the user. Present for confirmation before saving. This captures learning at the moment of discovery, not retrospectively.

---

## Theory Citations
- Torres: Evidence requirements
- Cagan: Four risks
- Christensen: JTBD validation
- Snowden: Cynefin classification
- Shotton/Kahneman: Bias mitigation
- OWASP/STRIDE: Security gates
- GDPR/PbD: Privacy gates
- Smart: BVSSH (now at completion, not just monthly)
- Downe: Service quality (gated for user-facing work)
- Forsgren: DORA metrics + testing requirements
- EU AI Act: Regulatory classification (L3-L5)
