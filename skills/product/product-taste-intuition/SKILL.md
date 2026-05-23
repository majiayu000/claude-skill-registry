---
name: "product-taste-intuition"
description: "Build stronger product taste + intuition as a PM by running a Taste Calibration Sprint (benchmark set, product critique notes, intuition→hypothesis log, validation plan, practice loop). Use for “product taste”, “product sense”, “intuition”, “calibrate taste”."
---

# Product Taste & Intuition

## Scope

**Covers**
- Developing **product taste** (what “good” looks like) through deliberate exposure, observation, and critique
- Using intuition as a **hypothesis generator** (turning “gut feel” into testable hypotheses)
- Building a repeatable **practice loop** (exposure hours → analysis → validation → updated taste rules)

**When to use**
- “Help me improve my product taste / product sense.”
- “Calibrate what ‘good onboarding’ looks like for our product category.”
- “Turn my intuition about this flow into testable hypotheses.”
- “Create a structured way to study great products and extract patterns.”

**When NOT to use**
- You need to decide *what to build* (use `problem-definition`, `prioritizing-roadmap`, or `defining-product-vision`).
- You need user evidence first (use `conducting-user-interviews` or `usability-testing`).
- You want aesthetic critique only (this is product experience: value, UX, clarity, trust, speed—not just visuals).
- You can’t name any target user, use case, or the “taste domain” you want to improve (we’ll narrow first).

## Inputs

**Minimum required**
- Taste domain to improve (pick 1): onboarding, activation, navigation/IA, editor/workflow, pricing/packaging UX, notifications, retention loops, trust/safety, performance/latency feel, copy/voice
- Target user + top job-to-be-done for that domain
- 3–10 benchmark products/experiences to study (or “unknown—please propose”)
- Time box (e.g., 60–120 min sprint; or a 2–4 week practice plan)
- Constraints (platform, geography, accessibility, compliance, brand voice, etc.)

**Missing-info strategy**
- Ask up to 5 questions from [references/INTAKE.md](references/INTAKE.md).
- If inputs remain missing, proceed with explicit assumptions and provide 2 scope options (narrow vs broad).

## Outputs (deliverables)

Produce a **Taste Calibration Pack** (in-chat Markdown; or as files if requested):

1) **Taste Calibration Brief** (domain, target user/job, what “good” means, constraints)
2) **Benchmark Set** (5–10 products) + “why these” + what to study
3) **Product Study Notes** (1 page per benchmark) using a consistent critique template
4) **Taste Rules + Anti-Patterns** (do/don’t rules derived from evidence)
5) **Intuition → Hypothesis Log** (testable hypotheses + predicted signals)
6) **Validation Plan** (qual + quant checks; smallest viable tests)
7) **Practice Plan** (2–4 weeks: exposure hours + weekly synthesis cadence)
8) **Risks / Open questions / Next steps** (always included)

Templates: [references/TEMPLATES.md](references/TEMPLATES.md)

## Workflow (8 steps)

### 1) Intake + pick the taste domain (narrow the problem)
- **Inputs:** User context; [references/INTAKE.md](references/INTAKE.md).
- **Actions:** Choose 1 taste domain and 1 “moment” (e.g., first-run onboarding). Define target user + job + constraints. Set time box.
- **Outputs:** Taste Calibration Brief (draft).
- **Checks:** A stakeholder can answer: “What specific experience are we calibrating taste for?”

### 2) Define “good taste” as decision criteria (not vibes)
- **Inputs:** Domain + user/job.
- **Actions:** Draft 6–10 criteria (e.g., clarity, time-to-value, trust, agency, error recovery, perceived speed, cognitive load). Add explicit tradeoffs (what you’ll sacrifice).
- **Outputs:** Criteria list + tradeoffs section in the brief.
- **Checks:** Criteria are observable in-product (you can point to UI/behavior), not generic adjectives.

### 3) Build the benchmark set (exposure hours, curated)
- **Inputs:** Known benchmarks (or none).
- **Actions:** Select 5–10 exemplars (direct, adjacent, and at least 1 “gold standard”). For each: what you’re studying and why it’s relevant.
- **Outputs:** Benchmark Set table.
- **Checks:** Set includes at least 2 “outside the category” references to avoid local maxima.

### 4) Study like a voracious user (structured observation)
- **Inputs:** Benchmarks; critique template.
- **Actions:** Use each product as the target user. Capture micro-moments: friction, delight, confusion, trust breaks. Record “what happened” before “why it’s good/bad”.
- **Outputs:** Product Study Notes (draft).
- **Checks:** Each benchmark note includes at least 3 concrete moments with screenshots/quotes if available (or precise descriptions).

### 5) Synthesize: turn observations into taste rules + anti-patterns
- **Inputs:** Study notes across benchmarks.
- **Actions:** Cluster patterns. Convert into rules: **DO/DO NOT**, plus rationale and where it applies. Add anti-patterns that create “AI slop” (generic, incoherent, misaligned experiences).
- **Outputs:** Taste Rules + Anti-Patterns.
- **Checks:** Each rule is backed by ≥ 2 observations from different benchmarks (or explicitly marked “hypothesis”).

### 6) Intuition as hypothesis generator (make it testable)
- **Inputs:** Rules + your gut reactions.
- **Actions:** Write intuition statements (“It feels off because…”) and convert into testable hypotheses with predicted signals and counter-signals.
- **Outputs:** Intuition → Hypothesis Log.
- **Checks:** Each hypothesis has a clear falsification condition (“If X doesn’t change after Y, we were wrong.”).

### 7) Validate with smallest viable checks (qual + quant)
- **Inputs:** Hypothesis log; available data/research access.
- **Actions:** Choose the lightest validation per hypothesis: usability task, intercept prompt, session replay review, funnel slice, A/B smoke test, copy test, etc. Define success metrics and sample.
- **Outputs:** Validation Plan with owners/cadence if known.
- **Checks:** Validation steps are feasible within the stated time box and don’t require sensitive data.

### 8) Create a practice loop + quality gate + finalize
- **Inputs:** Draft pack.
- **Actions:** Build a 2–4 week practice plan (exposure hours schedule + weekly synthesis). Run [references/CHECKLISTS.md](references/CHECKLISTS.md) and score with [references/RUBRIC.md](references/RUBRIC.md). Add Risks/Open questions/Next steps.
- **Outputs:** Final Taste Calibration Pack.
- **Checks:** A reader can follow the practice plan without additional context; assumptions are explicit.

## Quality gate (required)
- Use [references/CHECKLISTS.md](references/CHECKLISTS.md) and [references/RUBRIC.md](references/RUBRIC.md).
- Always include: **Risks**, **Open questions**, **Next steps**.

## Examples

**Example 1 (Onboarding):** “Calibrate our onboarding taste vs best-in-class. Target users are first-time PMs. Time box: 90 minutes. Output a Taste Calibration Pack.”  
Expected: benchmark set, critique notes, taste rules, hypotheses, and a lightweight validation plan.

**Example 2 (B2B workflow UX):** “My gut says our ‘create project’ flow feels slow and confusing. Turn that into testable hypotheses and a validation plan.”  
Expected: intuition→hypothesis log with falsification conditions and smallest viable checks.

**Boundary example:** “Tell me what good taste is in general.”  
Response: require a specific domain + target user/job; otherwise produce a menu of domain options and propose a narrow starting point.

