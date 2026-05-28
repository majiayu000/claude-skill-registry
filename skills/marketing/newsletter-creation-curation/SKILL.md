---
name: newsletter-creation-curation
description: Industry-adaptive B2B newsletter creation with stage, role, and geography-aware workflows
---

# Newsletter Creation & Curation Skill

Use this skill to create B2B newsletters that match business context, not generic content templates.

Deep strategic guidance is in `PLAYBOOK.md`.
Use this file as the executable operating manual.

---

## Mode

Detect from context or ask: *"Outline only, full edition, or full edition + calendar?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | Edition outline + 3 lead story angles, no writing | Planning, editorial direction |
| `standard` | Full newsletter edition, all sections written | Publishing this week |
| `deep` | Full edition + 4-week content calendar + audience segmentation recommendations | Launching or systematizing a newsletter |

**Default: `standard`** — use `quick` if they're still deciding what to write. Use `deep` if they're building a newsletter from scratch or scaling.

---

## Context Loading Gates

**Before generating any newsletter content, collect:**

- [ ] **Company context:** What product/service? Who is the ICP?
- [ ] **Newsletter goal:** Lead gen / thought leadership / personal brand / category ownership
- [ ] **Industry vertical:** Sales Tech / HR Tech / Fintech / Operations Tech
- [ ] **Company stage:** Series A / Series B / Series C+
- [ ] **Role:** Founder / VP-Director / PMM-Content / Enterprise employee
- [ ] **Geography:** US-first / India-first
- [ ] **Prior issues:** Any existing issues to maintain consistency and voice?
- [ ] **Approval constraints:** Does this need legal/brand/manager review?

**Structured intake — answer all 5 dimensions before proceeding:**

```
Goal: [lead_gen | thought_leadership | personal_brand | category_ownership]
Industry: [sales_tech | hr_tech | fintech | ops_tech]
Stage: [series_a | series_b | series_c_plus]
Role: [founder | vp_director | pmm_content | enterprise_employee]
Geography: [us_first | india_first]
```

---

## Phase 1: Context Analysis

Before drafting, reason through:

1. **Template match:** Which industry template best fits? (Sales Tech = data-heavy; HR Tech = research-led; Fintech = compliance-aware; Ops Tech = practical)
2. **Cadence match:** Series A = weekly/bi-weekly for simplicity; Series B = weekly with process; Series C+ = media-grade weekly with pillars
3. **Role constraints:** Founder = direct POV allowed; Employee = approval checkpoint required before final draft
4. **Geography adjustments:** India-first = IST timing + local examples; US-first = EST/PST + US benchmarks
5. **Goal-content alignment:** Lead gen needs a clear conversion CTA; thought leadership needs original insight, not general content

Output one-line strategy statement:
> `For [ICP], we publish [cadence] to achieve [goal] with [format].`

---

## Phase 2: Issue Blueprint

Before writing full draft, produce an issue blueprint:

```markdown
## Issue Blueprint

**Strategy:** For [ICP], [cadence] to achieve [goal].
**Industry tone:** [tactical/research-led/compliance-aware/practical]
**Approval required:** [yes/no — who]

**Sections:**
1. Subject lines (3 options) — [~words each]
2. Hook — [target ~75 words]
3. Core insight — [target ~200 words]
4. Actionable playbook — [target ~150 words, 3-5 steps]
5. CTA — [1 sentence, singular action]
```

Get confirmation or proceed to draft.

---

## Phase 3: Full Issue Draft

Generate complete publish-ready draft. Required structure — every issue:

### Subject Line Options (3 required)
Produce 3 distinct angles:
- A: Curiosity/open loop ("The metric most [ICP] ignore")
- B: Specific + benefit ("How [Company type] achieves [X] in [timeframe]")  
- C: Contrarian/bold ("Stop [common behavior]. Do this instead.")

### Hook
- First 2 sentences must earn the read
- Lead with the problem + stakes
- Target: busy reader can extract the point in 60 seconds

### Core Insight
- One primary takeaway per issue — not three
- Support with: data, framework, or named pattern
- Include specific numbers or named examples wherever possible

### Actionable Playbook
- 3-5 steps or checklist items
- Each step must be implementable, not just conceptual
- Series A = simpler steps; Series C+ = more sophisticated process

### CTA
- ONE measurable action only
- Options: reply with [X], click [link], share [asset], book [demo]
- Never use vague CTAs ("Learn more")

---

## Phase 4: Refinement Checklist

Run before delivering:

- [ ] `Clarity`: Can a busy reader extract value in 60 seconds?
- [ ] `Specificity`: Does each section include concrete guidance or evidence?
- [ ] `Relevance`: Does tone match industry and role constraints?
- [ ] `Compliance`: For fintech/employee-led, is a legal/manager review step included?
- [ ] `Consistency`: Does voice align with prior issues (if any were provided)?
- [ ] `CTA`: Is there exactly ONE measurable CTA — not two, not zero?

---

## Phase 5: Self-Critique Pass (REQUIRED)

After completing the draft, evaluate:

- [ ] Does the subject line A option create genuine curiosity without being clickbait?
- [ ] Does the hook deliver a problem + stakes in the first 2 sentences?
- [ ] Is the core insight something subscribers couldn't get from a generic AI prompt?
- [ ] Does the playbook have steps that are specific to this audience, not generic "tips"?
- [ ] Is the CTA actually measurable — i.e., can they track whether it worked?
- [ ] For fintech/employee contexts: is there an explicit approval checkpoint?

Flag any issue: "The playbook steps are too generic for a Series B SaaS audience — they read as beginner content. Revised to assume existing process maturity."

---

## Iteration Protocol

After delivering the draft:
1. Ask: "Does the hook earn the read? Does the playbook feel actionable for your audience?"
2. If hook is weak → rewrite using a different angle (data-led, story-led, or contrarian)
3. If playbook is too generic → ask for a specific example from their own experience to ground it
4. For next issue: "Want me to save these content themes so the next issue builds on this one?"

---

## Output Structure

```markdown
## Newsletter Issue: [Name] — Issue #[X] — [Date]
**Strategy:** For [ICP], [cadence] to achieve [goal].

---

### Subject Line Options
A) [Curiosity/open loop]
B) [Specific + benefit]  
C) [Contrarian/bold]
**Recommended:** [A/B/C] — [reason]

---

### Hook
[2-3 sentences — problem + stakes]

---

### Core Insight
[200-300 words — data, framework, or named pattern]

---

### Actionable Playbook
1. [Step]
2. [Step]
3. [Step]

---

### CTA
[Single measurable action]

---

### Distribution Plan
- **Send time:** [Day, Time, Timezone]
- **LinkedIn amplification:** [Post angle / hook]
- **Secondary channel:** [Platform + angle]

### KPI Targets
- Open rate goal: [%]
- CTR goal: [%]
- Primary metric: [SQLs / subscribers / replies]

### Approval Required
[Yes — [who] | No]

### Self-Critique Notes
[Issues flagged + revisions made]
```

---

## Playbook Map (Deep Dives in `PLAYBOOK.md`)

- Sales Tech strategy: `SECTION A`
- HR Tech strategy: `SECTION B`
- Fintech strategy: `SECTION C`
- Operations Tech strategy: `SECTION D`
- Role approvals and geography tactics: `CROSS-CUTTING: UNIVERSAL FRAMEWORKS`

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
