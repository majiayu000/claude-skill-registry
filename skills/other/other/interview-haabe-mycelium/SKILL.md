---
name: interview
description: "Use when onboarding a new product/project. Progressive interview to understand purpose, vision, north star, and competitive landscape."
---

# Interview Skill

Progressive onboarding through structured discovery conversation.

## When to Use

- Starting a new product or project.
- Joining an existing product that lacks documented context.
- Context has changed significantly and needs refreshing.

## Workflow

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

## Output

- Purpose statement
- JTBD map per user type
- North star metric + input metrics
- Strategic context summary
- Initial opportunity areas (from what was shared, not assumed)

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

## Theory Citations

- Sinek: Start with Why (purpose)
- Christensen: Jobs to Be Done
- Torres: Continuous Discovery Habits (opportunity identification)
- Wardley: Wardley Mapping (landscape)
- Cagan: Empowered (vision, strategy)
