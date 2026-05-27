---
name: diamond-assess
description: "Use to evaluate the current state of a diamond. Checks theory gates, confidence levels, and recommends next action."
metadata:
  instruction_budget: "82"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe/mycelium."
---

# Diamond Assess Skill

Evaluate current diamond state and recommend next action.

## Workflow

0. **Cognitive Forcing (ALWAYS FIRST — before any analysis)**:

   Before presenting any assessment, ask the human for their unprimed judgment:

   > "Before I run the gates — where do you think this diamond stands right now? What feels solid and what feels shaky?"

   Wait for the human's response. Record it. Then proceed with the full assessment below. After presenting the assessment (step 10), compare:

   > "You said [X]. The gates say [Y]. Where do we differ?"

   This prevents the agent's analysis from anchoring the human's judgment. The human's pre-assessment often catches things the gates miss (Hoskins consistently outperformed the agent on product judgment calls).

   *Source: Buçinca, Malaya & Gajos (Cognitive Forcing Functions, Harvard CHI/CSCW 2021) — forcing initial human judgment before AI output significantly reduces automation bias and over-reliance on incorrect AI recommendations.*

1. **Identify the diamond**: Which diamond (ID, scale, phase) is being assessed?

2. **Gather current state**:
   - Current phase (Discover/Define/Develop/Deliver)
   - Evidence collected so far
   - Confidence score with breakdown
   - Blockers or risks

3. **Check theory gates for next transition**:
   - Reference ${CLAUDE_PLUGIN_ROOT}/engine/theory-gates.md for the current transition
   - Check `product_type` from `.claude/diamonds/active.yml` -- gates conditioned on product_type include:
     - **Security Gate**: full OWASP for software/ai_tool; platform-only for content; infra-only for service
     - **Delivery Metrics Gate**: routes to product-type-appropriate metrics canvas
     - **Service Quality Gate**: Downe applies to consumption experience for all product types; Nielsen only for digital interfaces
   - Evaluate each applicable gate: Pass / Fail / Insufficient Evidence / N/A (if gate doesn't apply to this product_type)
   - **Read-before-claim (HARD RULE; anti-pattern #7 instance #4, 2026-05-09):** Before claiming a required-evidence bucket is *missing* or *partial* (e.g., "Wardley Map | Missing", "user_research_synthesis | Insufficient"), the agent MUST use the **Read tool** on the canvas file that bucket maps to (e.g., `landscape.yml`, `user-needs.yml`, `opportunities.yml`, `gist.yml`). Spawn-note text, theory-gates.md references, and prior conversation context do NOT count as evidence of the bucket's actual state — only reading the file does. Treating consistency between spawn-note phrasing and an absence-claim as causal evidence is anti-pattern #7 (Consistency-as-Evidence). The graduation case for instance #4 was the agent recommending "build the Wardley map now" when the map was substantially complete — the agent had not opened landscape.yml.
   - Document what is missing for failed gates, naming the specific canvas file read and the specific field that is empty/incomplete (not the inference that it should be empty).

4. **Check confidence threshold**:
   - Reference ${CLAUDE_PLUGIN_ROOT}/engine/confidence-thresholds.yml for the current scale
   - Apply `project_type_adaptations` to compute effective threshold (see ${CLAUDE_PLUGIN_ROOT}/engine/confidence-thresholds.yml)
   - Compare current confidence to the **effective** threshold
   - Identify what would increase confidence

5. **Check for anti-patterns**:
   - Reference ${CLAUDE_PLUGIN_ROOT}/harness/anti-patterns.md
   - Flag any detected failure modes
   - For L1/L2 diamonds: also check for **system archetypes** (Senge) — Fixes That Fail, Shifting the Burden, Limits to Growth, Eroding Goals
   - At L3->L4 transitions: also run the **Design Completeness Check** (quality/CLAUDE.md) to verify all layers of the product design stack have evidence. Source: Mill, building on Garrett.

6. **Check canvas health**:
   - Run the `/mycelium:canvas-health` checks inline: missing required files, stale confidence, inconsistent evidence types
   - Report any critical or warning-level findings
   - This catches silent canvas degradation before it affects progression decisions

6b. **Check metric snapshot freshness** (v0.14; L0/L1/L2/L5 only):
   - If the current diamond scale is L0, L1, L2, or L5 AND `.claude/jit-tooling/active-metrics.yml` exists:
     - For each `status: active` source, find the newest file in `.claude/evals/metrics/<source>/`.
     - If the newest snapshot is >7 days old (or missing entirely), flag as a warning and recommend `/mycelium:metrics-pull`.
     - If `.claude/jit-tooling/active-metrics.yml` is missing, recommend `/mycelium:metrics-detect` (softer — info-level, not a gate).
   - Rationale: evidence loops for Purpose/Strategy/Opportunity/Market depend on external signal freshness. A stale snapshot silently anchors confidence.
   - Do NOT block progression on stale snapshots — this is a NUDGE, not a gate.

7. **Check corrections.md**:
   - Any relevant past mistakes to avoid?

7b. **Check trio perspective coverage** (Torres Product Trio):
   - For the current diamond phase, verify all three perspectives (product/design/engineering) have been applied.
   - Reference `${CLAUDE_PLUGIN_ROOT}/engine/theory-gates.md` §Trio Perspective Requirement for the per-scale coverage matrix.
   - Flag any missing perspectives as a gap: "Design perspective not yet applied at L[X]. Consider running `/mycelium:usability-check` or `/mycelium:service-check`."
   - If perspectives are in conflict, recommend `${CLAUDE_PLUGIN_ROOT}/engine/perspective-resolution.md`.

8. **Coaching check** (Rother's Coaching Kata):
   Surface these five questions in the output to prompt the human's thinking:
   1. What is the **target condition** for this diamond? (What does "done" look like?)
   2. What is the **actual condition** right now? (Summarize from steps 2-7 above)
   3. What **obstacles** are preventing progress? Which one are you addressing now?
   4. What is your **next step**? What do you **expect** will happen? (Force a prediction before acting)
   5. When can we **check what we learned** from that step? (Commit to a review point)
   The coach (human) should answer these, not the agent. The agent surfaces them.
   *Source: Rother (Toyota Kata) — the 5 questions install scientific thinking as a daily habit.*

9. **Log assessment in .claude/harness/decision-log.md** (MANDATORY):
   - APPEND a `### Diamond Assessment` entry to `.claude/harness/decision-log.md`
   - Include: diamond ID and scale, gates passed/failed, current confidence with rationale, evidence gaps
   - This log entry is essential for auditability — every assessment should be documented

10. **Recommend next action**:
   - If all gates pass and confidence meets threshold: recommend transition to next phase
   - If gates fail: recommend specific actions to address failures
   - If confidence is low: recommend evidence-gathering activities
   - If anti-patterns detected: recommend corrective actions
   - If regression needed: recommend which phase to return to and why

11. **Play devil's advocate**: Before recommending progression, ask:
    - What are we most likely wrong about?
    - What evidence have we dismissed?
    - Is there a simpler path we're overlooking?

12. **Report harness thickness** (informational):
    - Count: total skills, active guardrails, mandatory reads, hooks, theory gates
    - Current: 44 skills, 37 guardrails, 4 mandatory reads, 5 hook layers, 12 gates
    - If thickness has increased since last assess, note it
    - This is observability, not a gate — purely informational
    - *Source: Trivedy (Anatomy of an Agent Harness, LangChain blog — "scaffolding should decrease as models improve," but harnesses remain valuable as they engineer systems around model intelligence)*

## Output Format

**ALWAYS output in plain language first, then technical details.**
Use `${CLAUDE_PLUGIN_ROOT}/engine/status-translations.md` for translations.

**ALWAYS render the journey map first.** Follow `${CLAUDE_PLUGIN_ROOT}/engine/wayfinding.md` to render the "You Are Here" map before any other output. This orients the user to where they are in the full L0→L5 progression before diving into gate details.

**Phase-index narration discipline** (per ht-012 cohort-log f9, shipped v0.23.21): when surfacing routing decisions or flagging empty canvas fields, **do NOT narrate internal phase numbers ("Phase 6 questions", "Phase 4 Landscape") to the user**. Reference the outcome instead: "the project-type question", "the landscape mapping step". L0–L5 diamond scales are framework-external vocabulary and ARE narratable (they appear in user-facing docs); Phase-N indices are internal skill structure and are NOT.

```
[Journey map from ${CLAUDE_PLUGIN_ROOT}/engine/wayfinding.md — rendered first]

## Where We Are

Current focus: [plain-language description from ${CLAUDE_PLUGIN_ROOT}/engine/status-translations.md]
  [1-2 sentences of context]
  Confidence: [plain word] ([number], [Gilad level]) -- [why this level, what would increase it]

## Progress

[N] of [M] diamonds complete:
  [Name]: [STATUS] -- [plain-language one-liner]
  [Name]: [STATUS] -- [plain-language one-liner]

## Theory Gate Check (for next transition)

| Gate | Status | Suggested Skill |
|------|--------|----------------|
| Evidence | Pass/Fail | /mycelium:user-interview or /mycelium:assumption-test |
| Four Risks | Pass/Fail | /mycelium:assumption-test |
| ... | ... | ... |

## What I'd Challenge (Devil's Advocate)
- [Key assumption to question]
- [Evidence gap to flag]

## Coaching Check (for the human)
1. What does "done" look like for this diamond?
2. Given what we know now, what's the biggest obstacle?
3. What's your next step -- and what do you expect will happen?
4. When should we check what we learned?

## Recommended Next Step
[Plain-language recommendation with theory justification]

Suggested actions:
  - /skill-name -- [why this is relevant now]
  - /skill-name -- [why this is relevant now]
```

## Theory Citations
- Buçinca, Malaya & Gajos: Cognitive Forcing Functions (human judges first, then AI presents — reduces automation bias)
- Torres: Evidence-based progression
- Gilad: Confidence scoring with contextual explanation
- Cagan: Four risks assessment
- Snowden: Cynefin classification
- Shotton/Kahneman: Devil's advocate bias check
- Rother: Coaching Kata (5 questions for scientific thinking)
