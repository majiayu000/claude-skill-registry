---
name: interview
description: "Use when onboarding a new product/project. Progressive interview to understand purpose, vision, north star, and competitive landscape."
instruction_budget: 110
---

# Interview Skill

Progressive onboarding through structured discovery conversation.

## When to Use

- Starting a new product or project.
- Joining an existing product that lacks documented context.
- Context has changed significantly and needs refreshing.

## Workflow

### Phase 0: Time Budget (ALWAYS FIRST)

Before any interview questions, ask:

> "How much time do you have for this project right now — today's session specifically?"

Based on the answer, select a path:

| Time Budget | Path | What Happens |
|-------------|------|-------------|
| **< 8 hours** | **Inline discovery** | Skip /interview entirely. Go straight to delivery. Weave 3 discovery questions into the first task: (1) What problem? (2) Who's the user? (3) What does done look like? Create a minimal L0 diamond with `confidence: 0.1`. |
| **8-48 hours** | **Sprint interview** | Run Phases 1 + 2 only (Purpose + Users). Skip Phases 3-5c. Jump to Phase 6 (Classification) with defaults. Parallelize all canvas writes. Total: ~15 minutes of questions. |
| **48+ hours** | **Full interview** | Run all phases as documented below. |

**Sprint interview specifics** (8-48h path):
- Phase 1: Compress to 2 questions: "What problem do you solve and for whom?" + "What does success look like?"
- Phase 2: Compress to 2 questions: "Describe a specific user and their job-to-be-done" + "What do they use today?"
- Skip Phases 3, 4, 5, 5b, 5c — these populate with stubs marked `source_class: internal_stakeholder, validated: false, confidence: 0.1`
- Phase 6: Ask product type only. Default project scope to `solo_product`. Skip dogfood question.
- Canvas writing: all files in parallel, one batch
- End with: "We skipped landscape, north star, and constraints to save time. Run `/interview` again when you have time to fill those in."

*Source: Hoskins friction log (2026-04-25) — full interview consumed an entire session before any delivery work started. Horthy (instruction budget overflow). Corrections.md: "Interview ceremony too long for sprints."*

### Phase 1: Purpose & Vision
1. Ask: "What problem does this product/organization solve? Who suffers without it?"
2. Ask: "What does success look like in 3 years? What would change in the world?"
3. Ask: "What will you never do, even if it would be profitable?" (ethical boundaries)
4. Synthesize into a purpose statement. Validate with the user.

### Phase 2: Users & Jobs
5. Ask: "Who are your primary users? Describe a specific person."
6. Ask: "What are they trying to accomplish? What job are they hiring your product to do?"
7. Map JTBD (functional, emotional, social) per user type.
8. Ask: "What workarounds do they currently use?"

### Phase 3: North Star & Metrics
9. Ask: "What is the single metric that best indicates you're fulfilling your purpose?"
10. Ask: "What leading indicators predict movement in that metric?"
11. Construct a north star framework: metric + input metrics.

### Phase 4: Landscape & Strategy
12. Ask: "Who else solves this problem? How are you different?"
13. Ask: "What are you betting on strategically right now?"
14. Ask: "What is your biggest uncertainty or risk?"
15. Sketch initial Wardley map positioning if sufficient context exists.

### Phase 5: Current State
16. Ask: "What has been tried and failed? What did you learn?"
17. Ask: "What's the team structure? How do decisions get made?"
18. Ask: "What are the immediate priorities?"

### Phase 5b: Constraints (Brown)

Surface the constraints that will shape solution space. These are often the most critical missing context during handovers.

19. Ask: "What can't change? Any legacy systems, platform limitations, or technical choices that are locked in?"
20. Ask: "Who has to approve what? What are the decision-making boundaries and political dynamics?"
21. Ask: "What rules apply? Regulatory requirements, compliance obligations, SLAs, data handling restrictions?"

Store constraints in `purpose.yml` under a `constraints` section:

```yaml
constraints:
  technical:
    - description: "..."
      source_class: internal_stakeholder
  political:
    - description: "..."
      source_class: internal_stakeholder
  regulatory:
    - description: "..."
      source_class: internal_stakeholder
```

These feed directly into Cagan's feasibility and viability risk assessments at L3. Tag all constraint entries as `internal_stakeholder` — they are the stakeholder's understanding of constraints, which may be incomplete or outdated.

*Source: Brown (three lines of questioning: domain/audience/constraints), Cagan (feasibility/viability risks).*

### Phase 5c: Closing

22. Ask: "Is there anything important that I didn't ask about?"

This catch-all question surfaces what the stakeholder considers most important but wasn't covered by the structured phases. Log the answer with high priority for follow-up — unprompted disclosures tend to be the most revealing.

*Source: Brown (EightShapes), NNGroup (stakeholder interview best practices).*

## Evidence Classification

**All `/interview` outputs are stakeholder beliefs, not validated evidence.** This is a stakeholder interview — the founder/PM is sharing their mental model of the product, users, and market.

When writing canvas entries from interview answers:
- Tag evidence as `source_class: internal_stakeholder`
- Claims about users (Phase 2) are **organizational mythology** (Brown) — what the stakeholder believes about users, not observed behavior. These count toward L0 confidence but do NOT satisfy L2's `external_human` requirement.
- Mark user-related claims with `validated: false` to create natural pressure for real user research.
- The wayfinding map after interview should note: "Based on stakeholder perspective. Confidence increases with external validation."

This classification ensures the evidence gate correctly distinguishes between "the founder told us" and "we observed users doing this."

*Source: Brown (organizational mythology), Torres (assumptions are beliefs that may or may not be true), Spool (secondhand research fails to produce the same benefits as firsthand observation).*

## Output

- Purpose statement
- JTBD map per user type
- North star metric + input metrics
- Strategic context summary
- Constraints map (technical, political, regulatory)
- Initial opportunity areas (from what was shared, not assumed)
- All outputs tagged `source_class: internal_stakeholder`

## Phase 6: Project Classification (NEW in v0.2)

At the end of the interview, classify the project to determine which canvas files are required:

Ask: "Let me understand the project scope to tailor the framework:"

**Product type** (v0.11.0 -- ask first, determines delivery profile):
- "What type of product are you building?"
  - Software (app, API, tool, library)
  - Online course or educational content
  - Written publication (ebook, newsletter, docs)
  - Media content (video, podcast, audio)
  - AI tool or agent (prompts, fine-tuned models, AI workflows)
  - Service offering (consulting, coaching, agency)
  - Other (describe)

Store as `product_type` on the L0 diamond entry in `diamonds/active.yml` (per-diamond field, not root-level). Child diamonds inherit product_type from their parent unless overridden. Load delivery profile from `canvas-guidance.yml#product_types`.

**Project scope**:
- Is this a solo or team project?
- Is this a hobby/learning project, a real product, or enterprise?
- Will it have external users?
- Will it handle user data?

Classify into one of:
- **solo_hobby**: Personal project, no commercial intent
- **solo_product**: Solo developer, real product with users
- **team_startup**: Small team (2-10), product with users/revenue
- **team_enterprise**: Larger team, regulatory/compliance needs

Load canvas guidance from `.claude/engine/canvas-guidance.yml` for the classified type.

**Also ask the dogfood question**:

> "Is this primarily a real product that you intend to ship, or are you using this project mostly as a vehicle to test and learn Mycelium itself?"

If the user says it's primarily about learning Mycelium:
- Set `dogfood: true` in `diamonds/active.yml` (in addition to `project_type`)
- Explain what this enables: mocked personas via `/mocked-persona-interview`, honest stop conditions, dogfood reports as the real deliverable
- Reference `.claude/evals/dogfood-reports/README.md` for the pattern
- Note that theory gates will accept "documented Mycelium learning" as evidence in place of user research

See `.claude/engine/canvas-guidance.yml#dogfood_modifier` for the full effect list.

Report to user: "Based on this being a [type] project [+ dogfood modifier if applicable], here's what we'll focus on:"
- **Required canvas files**: [list] -- "These will be populated as we work."
- **Recommended**: [list] -- "Worth doing if time allows."
- **Optional**: [list] -- "You can skip these for this project type."
- **If dogfood**: "Mocked personas are acceptable via `/mocked-persona-interview`. The real deliverable is a dogfood report at session end."

Store classification in `diamonds/active.yml` as `project_type`. If dogfood, also store `dogfood: true`.

### Threshold Implications (v0.11.0)

After classifying project_type (and dogfood status), inform the user of threshold adaptations from `confidence-thresholds.yml#project_type_adaptations`:

"Based on your project type, confidence thresholds are adapted:
- L0 Purpose: [base] -> [effective] (base [base] x [project_type multiplier] [x dogfood multiplier if applicable])
- L1 Strategy: [base] -> [effective]
- ... (list all scales)
- [If dogfood: 'Dogfood mode stacks an additional 0.8x multiplier. Example: solo_product (0.85) x dogfood (0.8) = 0.68 effective multiplier. L0: 0.9 x 0.68 = 0.612.']
- This means you need [plain language: 'less formal evidence' / 'the same rigor as a full team'] to progress diamonds.
- Note: evidence quality and external evidence requirements are NOT reduced -- you still need at least one real human conversation before shipping purpose or opportunity diamonds."

**Canvas setup**: Based on the product_type, create the appropriate delivery metrics canvas:
- software -> `canvas/dora-metrics.yml` (already exists as template)
- content_course/content_publication/content_media -> `canvas/content-metrics.yml`
- ai_tool -> `canvas/ai-tool-metrics.yml`
- service_offering -> `canvas/service-metrics.yml`

Tell the user: "I've set up [canvas name] for tracking your delivery metrics. When you reach L4, run `/dora-check` to assess delivery health."

**Metric source detection** (v0.14): After the tech-stack conversation and canvas setup, detect which **external metric sources** apply to this product — GitHub, Plausible, Stripe, app stores, support channels, etc. These feed L0/L1/L2/L5 evidence loops (replacing manual "I checked the dashboard" reports).

Follow `.claude/jit-tooling/metrics-detector.md`:
1. Scan for signals (git remote, SDK installs, env vars).
2. Ask the user about things the repo can't reveal: deployed product URL, payment processor, app stores, support channels.
3. Confirm each candidate source. For novel sources with no adapter, follow `metrics-adapters/GENERATING.md`.
4. Write `.claude/jit-tooling/active-metrics.yml`.

Tell the user: "I've configured N metric source(s) in `active-metrics.yml`. Run `/metrics-pull` whenever you want a fresh snapshot — I'll also remind you before `/diamond-assess` at L0/L1/L2/L5 if the latest is >7 days old."

If the user prefers to defer this: skip, note in the interview summary, and suggest `/metrics-detect` later.

## After the Interview: What Happens Next

The interview creates an **L0 Purpose diamond** in Discover phase. Here's the bridge to ongoing work:

### Decision Log Entry (v0.11.1)

Write a decision-log entry for the interview itself. The interview shapes all downstream work — it is the most foundational decision in the project lifecycle. Log entry must include:
- **Decision**: "Conducted initial product interview. Established purpose, JTBD, north star, landscape, and classification."
- **Theory**: Sinek (purpose), Christensen (JTBD), Torres (opportunity identification), Wardley (landscape)
- **Evidence**: Summary of key inputs from the user (problem statement, target users, strategic bets)
- **Confidence**: The initial diamond confidence (typically 0.2-0.35 for a first interview)
- **Alternatives considered**: N/A for initial interview (but note if the user considered alternative framings)
- **Classification rationale**: Why this project_type and dogfood status were chosen

### Theory Gates Initialization (v0.11.1)

When creating the L0 diamond in `active.yml`, initialize `theory_gates_status` with ALL applicable gates for the diamond's scale. Use the Quick Reference table in `theory-gates.md#quick-reference-gates-per-scale-for-theory_gates_status-initialization`:

| Scale | Gates to Initialize |
|-------|-------------------|
| L0 | evidence, cynefin, bias, bvssh, corrections |
| L1 | evidence, four_risks, jtbd, cynefin, bias, bvssh, corrections |
| L2 | evidence, four_risks, jtbd, cynefin, bias, privacy, bvssh, service_quality, corrections |
| L3 | All 12 gates |
| L4 | All except jtbd (11 gates) |
| L5 | evidence, cynefin, bias, security, bvssh, delivery_metrics, corrections, regulatory |

Set each to `pending`. Example for L0:
```yaml
theory_gates_status:
  evidence: pending
  cynefin: pending
  bias: pending
  bvssh: pending
  corrections: pending
```

1. **Tell the user**: "Interview complete. I've created your L0 Purpose diamond and populated the initial canvas files."
2. **Render the journey map**: Follow `.claude/engine/wayfinding.md` to render the "You Are Here" map. Use the post-interview intro: "Welcome to your product journey. Here's the map:" This is the user's first view of the full L0→L5 structure — it builds the mental model they'll carry forward.
3. **Suggest next step**: "Run `/diamond-assess` to see your starting state and what to work on next."
4. **The typical flow from here**:
   - `/diamond-progress` to advance L0 through its phases
   - L0 spawns L1 (Strategy) when purpose is solid -- unless project type is solo_hobby (skip L1, go to L2)
   - L1 spawns L2 (Opportunity) when landscape is mapped
   - Each progression runs theory gates automatically

**Do NOT leave the user without a clear next action.** Always end the interview with a specific recommendation.

### Handoff to Delivery (Preventing the Process Cliff)

**CRITICAL**: After the interview, Mycelium must stay present — but lightweight. The process cliff (corrections.md, 2026-04-30) happens when the agent drops all framework structure after /interview and becomes a raw implementation co-pilot.

If the user immediately wants to build something after the interview:

1. **Create an L3 diamond** for the first delivery task. Don't ask — just do it. Set phase to Discover, confidence to 0.15.
2. **State the next checkpoint plainly**: "I'll run a quick service check and security scan before we call this done — you won't need to do anything extra."
3. **Run gates inline**, not as separate skill invocations. Instead of "/service-check" as a formal step, weave the Downe principles check into the delivery review naturally.
4. **Keep canvas updated silently**. As delivery decisions are made, update `gist.yml` and `opportunities.yml` without ceremony.
5. **At delivery completion**, run the DoD checklist from `/diamond-progress` — but present results conversationally, not as a bureaucratic gate.

The goal: the user shouldn't notice the framework is running, but the decision log should show it was.

*Source: Hoskins transcript (2026-04-25) — process abandoned for 75% of session after /interview. Böckeler (inferential guidance that's too heavy gets ignored). Smart (BVSSH Sooner — process overhead that slows delivery without adding value is waste). Corrections.md: "Process cliff after onboarding."*

## Theory Citations

- Sinek: Start with Why (purpose)
- Christensen: Jobs to Be Done
- Torres: Continuous Discovery Habits (opportunity identification, assumption mapping)
- Wardley: Wardley Mapping (landscape)
- Cagan: Empowered (vision, strategy, four risks)
- Brown: The Delicate Art of Interviewing Stakeholders (three mindsets, three lines of questioning, organizational mythology)
- Hall: Just Enough Research (stakeholder interviews as dual-agenda conversations)
- Spool: User Exposure Hours (secondhand research vs firsthand observation)
- NNGroup: Stakeholder interview best practices (closing question)
