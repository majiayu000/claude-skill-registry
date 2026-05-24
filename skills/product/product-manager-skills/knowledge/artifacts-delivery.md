# PM Artifacts & Delivery

Compressed reference for the full PM artifact lifecycle: from proto-personas and problem framing through PRDs, user stories, epics, story maps, and end-of-life communications.

## PRD Development

10-section document, built over 2-4 days.

**Template structure (10 sections):**
1. Executive Summary -- "We're building [solution] for [persona] to solve [problem], resulting in [impact]."
2. Problem Statement -- Who, what, why, evidence (quotes, analytics, tickets)
3. Target Users & Personas -- Primary + secondary proto-personas
4. Strategic Context -- OKRs, TAM/SAM/SOM, competitive landscape, "why now?"
5. Solution Overview -- High-level description + user flows (not pixel specs)
6. Success Metrics -- Primary metric (optimize), secondary (monitor), guardrail (don't regress)
7. User Stories & Requirements -- Epic hypothesis + broken-down stories with acceptance criteria
8. Out of Scope -- Explicit exclusions with rationale
9. Dependencies & Risks -- Technical, external, team; risks + mitigations
10. Open Questions -- Unresolved decisions needing discovery

**Metrics structure:** Always define current baseline, target, and measurement timeline. Format: "Metric: Current X -> Target Y, measure Z days post-launch."

**Phase sequence:**
- Day 1: Exec summary (30m) + Problem (60m) + Personas (30m) + Strategy (45m)
- Day 2: Solution (60m) + Metrics (30m) + Stories (90-120m)
- Day 3: Scope/Dependencies (30m) + Review (60m)

## User Stories

**Format (Mike Cohn + Gherkin):**
```
As a [specific persona], I want to [action], so that [outcome/motivation].

Scenario: [description]
Given: [preconditions -- multiple Givens OK]
When: [single trigger event -- aligns with "I want to"]
Then: [single outcome -- aligns with "so that"]
```

**Quality gates:**
- "As a" uses specific persona, not generic "user"
- "So that" states motivation, not restatement of action
- One When, one Then per story. Multiple = split signal.
- Acceptance criteria are testable by QA -- no "better experience" or "faster"
- Summary is value-centric: "Enable Google login for trial users" not "Add login button"

### Splitting Stories

8 patterns applied in order (Richard Lawrence / Humanizing Work). Stop at first match:

| # | Pattern | Signal | Split strategy |
|---|---------|--------|----------------|
| 1 | Workflow steps | Multi-step sequence | Thin end-to-end slices (full workflow, increasing sophistication) |
| 2 | Business rules | Different rules per scenario | One story per rule variation |
| 3 | Data variations | Different data types/formats | One story per data type, simplest first |
| 4 | AC complexity | Multiple When/Then | One story per When/Then pair |
| 5 | Major effort | Hard first build, easy additions | "Implement one + add remaining" |
| 6 | External deps | Multiple APIs/third parties | One story per dependency boundary |
| 7 | DevOps steps | Infrastructure/deployment work | Split by operational complexity |
| 8 | Tiny Acts of Discovery | High uncertainty, none above apply | Time-boxed experiments, not stories |

**Validation after split:** Each piece must (a) deliver user value independently, (b) be testable independently, (c) fit in a sprint (1-5 days), (d) all pieces combined equal the original.

**Critical rule:** Always split vertically (front-end + back-end = user value). Never horizontally ("Build API" / "Build UI").

## Story Mapping

**Jeff Patton framework -- 2D map:**
- Horizontal (left-right): Activities in narrative/workflow order = backbone
- Vertical (top-down): Priority within each activity

**Hierarchy:** Segment -> Persona -> Narrative (goal) -> Activities (3-5) -> Steps (3-5 per activity) -> Tasks (5-7 per step)

**Building the map:**
1. Define segment + persona + narrative (one-sentence JTBD goal)
2. Identify 3-5 backbone activities in sequential workflow order
3. Break each activity into steps (user actions, observable, logical sequence)
4. Break steps into tasks (granular, prioritizable)
5. Prioritize vertically: top = MVP, middle = R2, bottom = future
6. Draw horizontal release lines

**Walking skeleton:** Top-priority task from EVERY activity = minimal end-to-end functionality. Build across all activities incrementally, not one activity fully before starting the next.

**Release slicing:**
- R1 (Walking skeleton): Simplest version across all activities
- R2 (Enhanced): Second-priority tasks improving core workflow
- R3 (Polish): Nice-to-haves, edge cases, optimizations

## Epics

### Epic Hypothesis

**Template (Tim Herbig / Lean UX):**
```
If we [specific action/solution]
for [specific persona]
Then we will [measurable outcome]
```

**Tiny Acts of Discovery:** 2-3 lightweight experiments before full build.
- Types: prototype + user test, concierge test, landing page test, Wizard of Oz, A/B test
- Constraint: days/weeks not months; cheap; falsifiable

**Validation measures:**
```
We know our hypothesis is valid if within [2-4 weeks]
we observe:
- [Quantitative: "20% increase in activation rate"]
- [Qualitative: "8/10 users say it saved time"]
```

**Decision gate:** Validated -> write user stories. Invalidated -> kill or pivot. Inconclusive -> more experiments.

### Epic Breakdown (9 Patterns)

Pre-split: INVEST check (Independent, Negotiable, Valuable, Estimable, Small, Testable). If not Valuable, STOP -- combine with other work, don't split.

**9 patterns applied sequentially** (superset of story splitting):
1. **Workflow steps** -- thin end-to-end, NOT step-by-step
2. **Operations (CRUD)** -- "manage" = Create + Read + Update + Delete
3. **Business rule variations** -- each rule = separate story
4. **Data variations** -- add data types just-in-time
5. **Data entry methods** -- basic input first, fancy UI later
6. **Major effort** -- implement one + add remaining
7. **Simple/Complex** -- simplest core first, variations later
8. **Defer performance** -- "make it work" then "make it fast"
9. **Break out a spike** -- time-box investigation when uncertainty blocks splitting

**Meta-pattern across all:** Identify core complexity -> list variations -> reduce to one complete slice -> make other variations separate stories.

**Evaluate splits:** (a) Does it reveal low-value work you can kill? (b) Are resulting stories roughly equal-sized?

**Cynefin adjustment:** Low uncertainty = find all stories, prioritize by value. High uncertainty = identify 1-2 learning stories only. Chaos = defer splitting, stabilize first.

## Proto-Personas

**Hypothesis-driven persona, not validated research.** Created in hours from available data.

**Template sections:**
1. **Name** -- alliterative, memorable ("Manager Mike")
2. **Bio & Demographics** -- behavioral, not just age/location. Include career, online presence, tech habits.
3. **Quotes** -- real or representative; revealing mindset, not facts
4. **Pains** -- specific and product-relevant ("3 hrs/week copying data between tools")
5. **What they're trying to accomplish** -- observable behaviors and outcomes
6. **Goals** -- short-term + long-term, personal + professional
7. **Attitudes & Influences** -- decision authority, influencers, beliefs affecting adoption

**Mark uncertainty:** Tag unvalidated items with [ASSUMPTION--VALIDATE]. Plan research to fill gaps. Limit to 1-2 personas initially.

## Press Release / PRFAQ

**Amazon Working Backwards format.** Written BEFORE building. Planning tool, not launch copy.

**Structure:**
1. **Headline** -- benefit-focused, specific ("Cut Invoice Processing by 60%")
2. **Dateline** -- city, date
3. **Introduction** -- what launched, for whom, key benefit (2-3 sentences)
4. **Problem paragraph** -- specific customer problem with data
5. **Solution paragraph** -- outcome-focused, not feature list
6. **Executive quote** -- customer-empathetic, visionary (not "excited to innovate")
7. **Supporting details** -- additional benefits with data
8. **Boilerplate** -- company background
9. **CTA + media contact**

**Litmus tests:** Would a customer care? Is the problem clear? Are benefits measurable? Is it jargon-free? Does it survive "so what?"

## Storyboards

**6-frame narrative arc** for pitching, alignment, and emotional validation.

| Frame | Name | Content |
|-------|------|---------|
| 1 | Main character | Persona + context (specific, not "busy professional") |
| 2 | Problem emerges | Challenge + how it affects life |
| 3 | "Oh crap" moment | Escalation creating urgency |
| 4 | Solution appears | Realistic discovery of product |
| 5 | "Aha" moment | Breakthrough experience (outcome, not feature demo) |
| 6 | Life after | Improved state with specifics |

**Visual style default:** Fat-marker sharpie sketches, minimal, monochrome. Low-fidelity is fine.

**7 input questions:** Who is the character? What problem? What's the escalation? How is solution introduced? What's the breakthrough? What's life after? Visual style preferences?

## Recommendation Canvas

**11-section strategic proposal** for AI/high-uncertainty product decisions. Executive-friendly.

1. **Business Outcome** -- [Direction] [Metric] [Outcome] [Context] [Criteria]
2. **Product Outcome** -- same format, customer perspective
3. **Problem Statement** -- persona-centric narrative
4. **Solution Hypothesis** -- If/Then + Tiny Acts of Discovery + Proof-of-Life measures
5. **Positioning Statement** -- For/That need/Is a/That + Unlike/Provides differentiation
6. **Assumptions & Unknowns** -- explicit, testable
7. **PESTEL Risks (Investigate)** -- Political, Economic, Social, Tech, Environmental, Legal (specific, not generic)
8. **PESTEL Risks (Monitor)** -- lower priority watch list
9. **Value Justification** -- data-backed case for C-level ("addresses #1 pain point, $500k ARR impact")
10. **Success Metrics** -- SMART format
11. **What's Next** -- ordered action steps

## End-of-Life Communication

**9-section empathy-first EOL message.** Never send without a complete transition plan.

**Structure:**
1. **Company context** -- who you are, customer commitment
2. **Announcement** -- single clear sentence: what's ending, what's replacing it, when
3. **Rationale** -- framed as customer benefit, not cost savings
4. **Current product context** -- acknowledge what's being lost and who it served
5. **Customer impact** -- explicitly name disruptions (migration time, learning curve, integration updates)
6. **Transition solution** -- positioning format: For/That currently use/Is a/That + continuity + improvements
7. **Support measures** -- 1:1 assistance, auto-migration, discounts, training
8. **Timeline** -- specific dates: migration tool available, read-only date, full shutdown, data export deadline. 6-12 months lead time.
9. **Call to action** -- next steps + contact info

**Tone rules:** Empathetic, not defensive. Forward-looking, not apologetic. Specific, not vague. Never blame customers for low usage.

## Quality Gates

### Cross-cutting anti-patterns

| Anti-pattern | Appears in | Fix |
|---|---|---|
| Written in isolation | PRD, story map | Collaborate with design + eng on stories/map |
| No evidence in problem statement | PRD, press release, canvas | Include quotes, analytics, tickets |
| Solution too prescriptive | PRD | Keep solution high-level; let design own UI |
| Feature list instead of benefits | Press release, canvas | Translate features to outcomes |
| Generic "As a user" | User stories | Use specific persona names/roles |
| "So that" restates "I want to" | User stories | Dig into real motivation |
| Multiple When/Then | User stories | Split the story |
| Horizontal slicing | Story splitting, epic breakdown | Always vertical: each story delivers end-to-end user value |
| Skipping experiments | Epic hypothesis, canvas | Define lightweight validation before build |
| Vague validation measures | Epic hypothesis, canvas | Specific metrics + timeframe (2-4 weeks) |
| Treating hypotheses as commitments | Epic hypothesis | Frame as bets; allow invalidation |
| Activities are features, not behaviors | Story map | Map user actions, not product capabilities |
| Technical backbone | Story map | Backbone follows user workflow, not system layers |
| Feature-complete waterfall releases | Story map | Walking skeleton = thin slice across ALL activities |
| Demographics without behavior | Proto-persona | Add behavioral context, not just age/location |
| Too many personas | Proto-persona | Start with 1-2; expand as validated |
| Business-centric EOL rationale | EOL message | Frame as customer benefit |
| Vague EOL timeline | EOL message | Specific dates with milestones |
| No transition support plan | EOL message | Migration assistance, tools, discounts |

---

## Interaction Rules (Coaching Mode)

When coaching is active for artifacts and delivery topics, use these rules.

| Trigger | Action | Stop When |
|---------|--------|-----------|
| PRD has no problem statement or it contains a solution | Push: "This PRD starts with the solution. What's the user problem it solves?" | User writes a problem-first statement |
| User story lacks acceptance criteria or uses vague language | Challenge: "When would an engineer know this story is done? Write the Given/When/Then." | User provides testable acceptance criteria |
| Epic has no hypothesis or success metric | Push: "What would have to be true for this epic to be worth building? How would you measure it?" | User states a falsifiable hypothesis with metric |
| Story is too large (multiple outcomes in one story) | Challenge: "This story has 3 outcomes. Which one ships first as a thin vertical slice?" | User identifies one outcome as the first slice |
| PRFAQ press release buries the user benefit | Push: "Your first paragraph is about the company. Rewrite it starting with the customer's life change." | User leads with customer outcome |
| User has answered 2 follow-ups on the same point | Stop pushing. Summarize what's still weak and give best-guess output. | -- |
