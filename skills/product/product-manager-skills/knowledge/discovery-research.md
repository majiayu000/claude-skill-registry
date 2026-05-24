# Discovery & Research

Compressed decision logic, frameworks, and quality gates for running product discovery end-to-end: framing problems, interviewing customers, mapping jobs and journeys, generating solutions, and validating hypotheses before committing to build.

## Problem Framing

### Problem Statement (Component)

**Template -- write from the user's perspective:**

```
I am:       [persona with 3-4 key characteristics]
Trying to:  [desired outcome -- measurable, not a task]
But:        [barriers preventing the outcome]
Because:    [root cause, not symptom]
Which makes me feel: [authentic emotion from research]
```

**Final statement formula:** `[Persona] needs a way to [outcome] because [root cause], which currently [impact].`

**Quality gates:**
- "I am" passes if you can picture a real person (not "busy professionals")
- "Trying to" is an outcome, not an activity
- "Because" survives 5-why interrogation
- "Makes me feel" uses verbatim customer language, not marketing copy
- Final statement fits one sentence and is measurable

**Top anti-patterns:**
1. **Solution smuggling** -- "The problem is we don't have X." Fix: reframe around user outcome.
2. **Business problem disguised as user problem** -- "Users want to reduce our churn." Fix: dig into why users leave from their perspective.
3. **Symptom instead of root cause** -- "Because the UI is confusing." Fix: keep asking "why" until you hit structural cause.

---

### Problem Framing Canvas (MITRE, Interactive)

**Three-phase bias-check before you write a problem statement.**

**Phase 1 -- Look Inward:**
- What is the problem? (symptoms only)
- Why haven't we solved it? (new / hard / low priority / lack of resources / authority / systemic inequity)
- How are we part of the problem? (confirmation bias / internal bias / survivorship bias / premature convergence)

**Phase 2 -- Look Outward:**
- Who experiences it? When, where, consequences?
- Who else has it? Who doesn't? (counter-examples reveal root cause)
- Who's been left out of the conversation?
- Who benefits from the problem existing? Who benefits from it being solved?

**Phase 3 -- Reframe:**
- Restate: "[Who] struggles to [what] because [root cause], leading to [consequence]. Affects [segments], overlooked because [bias]."
- HMW: "How might we [action] as we aim to [objective]?"

**Quality gates:**
- HMW is broad enough to permit multiple solutions, narrow enough to be actionable
- Canvas was completed cross-functionally, not solo
- "Who benefits from the status quo?" was explicitly answered

**Top anti-patterns:**
1. **Skipping Look Inward** -- groupthink persists. Fix: force explicit bias discussion.
2. **Generic reframe** -- "Improve user experience." Fix: include who, what, when, consequence, root cause.
3. **HMW too narrow** -- "How might we add a mobile app?" Fix: state the job, not the solution.

---

## Customer Discovery

### Discovery Process (Workflow, 6 phases / 3-4 weeks)

```
Phase 1: Frame (Day 1-2)
  -> Problem Framing Canvas (120 min) + Problem Statement (30 min)
  -> Optional: Proto-Persona, JTBD
  -> Output: problem hypothesis, 3-5 research questions, success criteria
  -> Gate: enough context to start research? If no, gather data first (+2-3 days)

Phase 2: Plan Research (Day 3)
  -> Discovery Interview Prep (90 min)
  -> Recruit 5-10 participants, schedule across 1-2 weeks
  -> Output: interview guide (5-7 Mom Test questions), participant roster

Phase 3: Conduct Research (Week 1-2)
  -> 5-10 interviews + support ticket analysis + analytics review
  -> Note template per interview: participant, context, actions, pain points, workarounds, verbatim quotes, insights
  -> Gate: saturation? Same pains across 3+ interviews = proceed. Still learning = +3-5 interviews.

Phase 4: Synthesize (End of Week 2)
  -> Affinity mapping: sticky notes -> themed clusters with frequency counts
  -> Optional: Customer Journey Map workshop
  -> Prioritize: score each pain on frequency x intensity x strategic fit (1-5 each)
  -> Output: top 3-5 pain points, 3-5 verbatim quotes per pain, validated problem statement

Phase 5: Generate & Validate Solutions (Week 3)
  -> Opportunity Solution Tree OR Lean UX Canvas
  -> Design experiments: concierge / prototype / landing page / A/B test
  -> Run experiments (1-2 weeks each)
  -> Gate: validated? If no, pivot to next solution (+1-2 weeks)

Phase 6: Decide & Document (Week 3-4)
  -> GO (roadmap + epics + PRD) / PIVOT (next solution) / KILL (deprioritize)
  -> 30-min stakeholder readout: problem validation, solution validation, recommendation
```

**Timeline ranges:** fast track 3 weeks (5 interviews, 1 experiment) | typical 4 weeks | thorough 6-8 weeks.

**Top anti-patterns:**
1. **Skipping interviews** -- relying only on analytics. Fix: always 5-10 qualitative interviews.
2. **Analysis paralysis** -- 6 weeks synthesizing. Fix: time-box to 3-4 weeks total.
3. **Discovery as one-time event** -- run continuous (Teresa Torres: 1 interview/week).

---

### Interview Prep (Interactive, 4 adaptive questions)

**Q1 -- Research Goal:** problem validation | JTBD discovery | retention/churn investigation | feature prioritization

**Q2 -- Target Segment:** people who experience problem regularly | people who tried to solve it | people in target segment regardless of awareness | people who recently experienced it

**Q3 -- Constraints:** limited access (5-10, 2 weeks) | existing base (100+ customers) | cold outreach required | internal stakeholders only (proxy)

**Q4 -- Methodology (context-aware on Q1-Q3):**
- **Mom Test (Rob Fitzpatrick — problem validation):** past behavior, not hypotheticals. "Tell me about the last time..."
- **JTBD interviews:** what customers hire/fire. "What were you trying to get done?"
- **Switch interviews:** push/pull of changing solutions. "What prompted you to look?"
- **Timeline/journey mapping:** chronological walkthrough of full experience

**Output: interview plan with opening (5 min), 5 core questions with follow-ups and anti-patterns, closing (5 min), bias checklist, success criteria, logistics.**

**5 biases to avoid in every interview:**
1. Confirmation bias -- don't ask "Don't you think X is a problem?"
2. Leading questions -- don't ask "Would you use this?"
3. Hypothetical questions -- don't ask "If we built Y, would you pay?"
4. Pitching disguised as research -- don't explain your solution
5. Yes/no questions -- don't ask "Is invoicing hard?"

**Interview success = specific stories (not generic complaints) + past behavior (not wishes) + patterns across 3+ interviews + at least one surprise.**

**Top anti-patterns:**
1. **Asking what customers want** -- gets feature requests, not problems. Fix: ask about past behavior.
2. **Pitching instead of listening** -- don't mention your solution until last 5 min (if at all).
3. **Stopping at 1-2 interviews** -- small sample = confirmation bias. Fix: 5-10 minimum.

---

## Jobs to Be Done

### JTBD Framework (Component)

**Three categories of customer jobs:**

| Type | Question | Examples |
|------|----------|----------|
| **Functional** | What tasks to complete? | "Reconcile monthly expenses for tax filing" |
| **Social** | How to be perceived? | "Be seen as strategic by exec team" |
| **Emotional** | What state to achieve/avoid? | "Feel confident I'm not missing details" |

**Four categories of pains:**
- **Challenges:** obstacles preventing job completion
- **Costliness:** excessive time, money, or effort
- **Common mistakes:** preventable errors
- **Unresolved problems:** gaps in current solutions

**Four categories of gains:**
- **Expectations:** what exceeds current solutions
- **Savings:** time/money/effort reductions
- **Adoption factors:** what triggers switching
- **Life improvement:** how life gets better

**Quality gates for jobs:**
- Verb-driven (actions, not nouns)
- Solution-agnostic ("communicate with team" not "use Slack")
- Specific ("track expenses for tax deductions" not "manage finances")

**Prioritization:** rank pains by intensity (acute vs. mild). Ask: "If we solved one pain, which has biggest impact?"

**Top anti-patterns:**
1. **Confusing jobs with solutions** -- "I need Slack." Fix: ask "Why?" 5 times.
2. **Ignoring social/emotional jobs** -- people buy on emotion, justify with logic. Fix: explicitly ask about perception and feelings.
3. **Fabricating JTBD without research** -- assumptions aren't insights. Fix: conduct switch interviews or contextual inquiries.

---

## Opportunity Mapping

### Opportunity Solution Tree (Teresa Torres — Interactive, 2 phases)

**Structure:**
```
Desired Outcome (1 measurable metric)
    |
    +-- Opportunity 1 (customer problem, not solution)
    |     +-- Solution A + experiment
    |     +-- Solution B + experiment
    |     +-- Solution C + experiment
    |
    +-- Opportunity 2
    |     +-- Solutions...
    |
    +-- Opportunity 3
          +-- Solutions...
```

**Phase 1 -- Generate tree:**
1. Extract desired outcome (revenue growth / retention / acquisition / efficiency)
2. Generate 3 opportunities per outcome (customer problems with evidence)
3. Generate 3 solutions per opportunity (with hypothesis + experiment for each)

**Phase 2 -- Select POC:**
- Score each solution: Feasibility (1-5) + Impact (1-5) + Market Fit (1-5)
- Feasibility: 1 = months, 5 = days. Impact: 1 = minimal, 5 = major. Market Fit: 1 = customers don't care, 5 = actively request.
- Pick highest total score as POC. Define experiment type: A/B test, prototype + usability, or concierge.

**Hypothesis template:** "If we [solution], then [metric] will [change] from [X] to [Y] because [rationale]."

**Top anti-patterns:**
1. **Opportunities disguised as solutions** -- "We need a mobile app." Fix: reframe as customer problem: "Mobile users can't access product on the go."
2. **Skipping divergence** -- "We know the solution." Fix: generate 3+ per opportunity. Force divergence before convergence.
3. **No experiments** -- picking solution and going to roadmap. Fix: every solution must map to an experiment.
4. **Vague outcomes** -- "Improve UX." Fix: make measurable: "Reduce drop-off from 60% to 40%."

---

## Customer Journey

### Journey Map (Component)

**Horizontal axis (stages):** Awareness -> Consideration -> Decision -> Service -> Loyalty

**Vertical axis (per stage):**
- Customer Actions (observable, specific)
- Touchpoints (digital + physical + human)
- Customer Experience (emotions with customer quotes)
- KPIs (measurable, stage-appropriate)
- Business Goals (outcome-focused, stage-aligned)
- Teams Involved (cross-functional with specific roles)

**Quality gates:**
- Emotions are specific ("relieved setup took 30 min, not 3 hours") not generic ("happy")
- Touchpoints include offline (conferences, calls), not just digital
- Map reflects what customers actually do, not what you want them to do
- KPIs and goals present for every stage

---

### Journey Mapping Workshop (Interactive, 5 questions)

**Q1 -- Actor:** select persona (primary / secondary / high-churn / newly discovered)
**Q2 -- Scenario + Goal:** first-time use / core workflow / problem resolution / upgrade-expansion
**Q3 -- Journey Phases:** generate 4-6 phases based on scenario (e.g., Discover -> Evaluate -> Try -> Activate -> Use -> Expand)
**Q4 -- Per-phase mapping:** 3-5 actions, thoughts, emotions, and pain points per phase
**Q5 -- Opportunities:** rank 5-7 pain points by impact (HIGH/MEDIUM/LOW) with evidence

**Output:** full journey map + prioritized opportunity list.

**Top anti-patterns:**
1. **Mapping internal process, not customer experience** -- "Lead generated -> Qualified -> Demo." Fix: map from customer POV.
2. **No emotions** -- actions only. Fix: add customer quotes and emotional states.
3. **Too many personas in one map** -- loses focus. Fix: one map per persona.

---

## Lean Validation

### Lean UX Canvas (v2, Interactive, 8 boxes)

**Fill order:**

| Box | Question | Content Type |
|-----|----------|-------------|
| 1. Business Problem | What changed that created a problem? | Context + trigger |
| 2. Business Outcomes | What behavior change = success? | Metrics (not emotions) |
| 3. Users | Which persona first? | Specific segment |
| 4. User Outcomes & Benefits | Why would users seek this? | Goals, emotions, empathy (not metrics) |
| 5. Solutions | What might solve it? | 3+ candidate features/initiatives |
| 6. Hypotheses | Testable if/then statements | "We believe [outcome] if [user] attains [benefit] with [solution]" |
| 7. Learn First | What's the riskiest assumption? | Value > usability > feasibility > viability risk |
| 8. Least Work | Smallest experiment to test it? | Must complete in <2 weeks |

**Box 2 vs Box 4 distinction:** Box 2 = behavior change metrics. Box 4 = human motivation and empathy.

**Top anti-patterns:**
1. **Starting with solutions** -- Box 1 says "build X." Fix: ask "What changed? Why is this a problem now?"
2. **Confusing Box 2 and Box 4** -- metrics in the empathy box. Fix: Box 2 = numbers, Box 4 = feelings.
3. **Only one solution in Box 5** -- no exploration. Fix: force 3+ candidates.
4. **Skipping experiments** -- "just build it." Fix: design smallest test first.

---

### PoL Probe (Component) -- Proof of Life

**A disposable, hypothesis-driven validation artifact. Not an MVP. Planned for deletion.**

**5 required characteristics:** Lightweight (hours/days) + Disposable (deletion date set) + Narrow Scope (one hypothesis) + Brutally Honest (surfaces harsh truth) + Tiny & Focused (reconnaissance, not product).

**Template fields:** hypothesis, risk being eliminated, probe type, target users, success criteria (pass/fail/learn thresholds), tools, timeline, disposal plan, owner, status.

**5 Probe Flavors:**

| Flavor | Core Question | Timeline | When to Use |
|--------|---------------|----------|-------------|
| Feasibility Check | Can we build this? | 1-2 days | Technical unknowns, API deps, data integrity |
| Task-Focused Test | Can users complete this job? | 2-5 days | Critical UI moments, navigation, drop-off zones |
| Narrative Prototype | Does this earn buy-in? | 1-3 days | Complex flow explanation, stakeholder alignment |
| Synthetic Data Simulation | Can we model without production risk? | 2-4 days | Edge cases, unknown-unknowns, load testing |
| Vibe-Coded Probe | Will this survive real user contact? | 2-3 days | Workflow/UX validation needing real interaction |

**Golden Rule:** Use the cheapest prototype that tells the harshest truth.

---

### PoL Probe Advisor (Interactive, decision logic)

**Selection flow:** hypothesis -> risk type -> core question -> recommended probe.

**Decision matrix:**
- Technical feasibility unknown -> **Feasibility Check** (spike-and-delete, API sniff tests)
- Critical UI friction -> **Task-Focused Test** (Optimal Workshop, UsabilityHub, Maze)
- Need stakeholder alignment -> **Narrative Prototype** (Loom walkthrough, slideware storyboard)
- Edge case exploration -> **Synthetic Data Simulation** (Monte Carlo, synthetic users, LangFlow)
- Need real user interaction -> **Vibe-Coded Probe** (ChatGPT Canvas + Replit + Airtable Frankensoft)

**Refinement questions when hypothesis is too broad:**
1. What's the smallest thing you could test first?
2. What would failure look like?
3. Is this testing user behavior, technical feasibility, or stakeholder alignment? Pick one.

**Top anti-patterns:**
1. **Choosing based on tooling comfort** -- "I know Figma, so I'll prototype." Fix: match method to hypothesis, not skillset.
2. **Defaulting to code** -- "Let's just build it." Fix: ask what's cheapest path to harsh truth.
3. **Confusing vibe-coded probes with MVPs** -- scope creep, refusal to dispose. Fix: set disposal date before building.
4. **Testing multiple things at once** -- ambiguous results. Fix: one probe, one hypothesis.
5. **No success criteria** -- "we'll know it when we see it." Fix: define pass/fail/learn before building.

---

## Quality Gates

### Consolidated Anti-Patterns Across All 11 Skills

**Problem framing failures:**
- Solution smuggling in problem statements
- Business metrics framed as user problems
- Generic personas ("busy professionals")
- Skipping bias examination (Look Inward)

**Research failures:**
- Leading / hypothetical / yes-no questions
- Pitching disguised as research
- Stopping at 1-2 interviews (need 5-10 minimum)
- Not recording insights immediately post-interview
- Never reaching saturation (same patterns in 3+ interviews)

**Synthesis failures:**
- Analysis paralysis (6+ weeks, no decisions)
- Opportunities disguised as solutions in OST
- Vague outcomes that can't be measured
- Journey maps reflecting internal wishful thinking, not customer reality
- Generic emotions ("happy") instead of specific states

**Validation failures:**
- Prototype theater (impressive demos that teach nothing)
- Choosing validation method by tooling comfort, not hypothesis
- Testing multiple variables in one experiment
- No pre-defined failure criteria
- Treating disposable probes as production code
- Discovery as one-time event instead of continuous practice

### Universal Quality Checks

Every discovery artifact should pass these:
1. **Falsifiable:** can you describe what failure looks like?
2. **Evidence-backed:** grounded in customer research, not assumptions?
3. **Specific:** can you picture the person, the problem, the metric?
4. **Actionable:** does it inform a concrete next step?
5. **Time-boxed:** is there a deadline that prevents indefinite exploration?

---

## Interaction Rules (Coaching Mode)

When coaching is active for discovery topics, use these rules to decide when to push, challenge, or stop.

| Trigger | Action | Stop When |
|---------|--------|-----------|
| Problem statement contains a solution ("We need X") | Push: "That's a solution. What's the user problem behind it?" | User restates as a user outcome |
| Success metric has no baseline or target | Push: "What's the current number, and what would success look like?" | User provides a specific number + timeframe |
| Persona is a category ("SMBs", "developers") | Challenge: "Name one specific person. What's their title, what gets them promoted?" | User names a role with context |
| No evidence of talking to users | Challenge: "Have you watched someone try to solve this? What surprised you?" | User describes a real observation or admits they haven't |
| User claims "everyone needs this" | Challenge: "Everyone means no one. Who would be upset if this disappeared tomorrow?" | User names a specific segment or person |
| Hypothesis has no failure criteria | Push: "What result would prove this idea wrong?" | User defines a measurable failure condition |
| User has answered 2 follow-ups on the same point | Stop pushing. Summarize what's still weak and give best-guess output. | -- |
| User provides specific evidence (quotes, data, behaviors) | Acknowledge and move forward. Don't push on points that already have evidence. | -- |
