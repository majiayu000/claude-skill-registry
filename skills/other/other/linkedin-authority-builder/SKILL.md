---
name: linkedin-authority-builder
description: Build a LinkedIn content system for thought leadership. Use when someone needs to establish authority, attract inbound leads, or build a consistent content presence. Covers positioning, content pillars, formats, and posting rhythm.
---

# LinkedIn Authority Builder

Here's what most people get wrong about LinkedIn: they're trying to go viral.

Viral doesn't pay your bills. Being remembered by the right 500 people when they need what you do — that pays your bills.

This skill builds a content system around consistent positioning and clear pillars — not hacks.

---

## Mode

Detect from context or ask: *"Starter plan, full content system, or 90-day build?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | 3 content pillars + 1-week posting starter plan | Getting unstuck, first week of consistency |
| `standard` | Full content system: pillars, formats, posting rhythm + first week written | Building a repeatable presence |
| `deep` | Full system + 90-day calendar + 10 posts written + engagement playbook | Serious authority-building campaign |

**Default: `standard`** — use `quick` if they just need to start posting. Use `deep` if they're committing to LinkedIn as a growth channel.

---

## Context Loading Gates

**Before generating any strategy, load:**

- [ ] **Current positioning:** One-liner, ICP, key differentiator (load from `positioning-basics` output if available)
- [ ] **Target audience on LinkedIn:** Specific titles, company stages, industries
- [ ] **Posting history:** What have they tried? What worked? What didn't?
- [ ] **Content goals:** Leads / job offers / speaking / partnerships / audience growth
- [ ] **Available time per week:** Hours they can realistically commit

**Sequencing gate:**
If positioning isn't clear yet, stop and ask:
> "Before building a content strategy, I need your one-liner: 'I help [specific audience] with [specific outcome] through [unique approach].' Do you have this locked, or should we nail positioning first with `positioning-basics`?"

Do not build a content system for an unclear position — the content will be unfocused.

**Also suggest:**
> "Run `linkedin-profile-optimizer` if you haven't — the content we build needs a profile that converts the traffic."

---

## Phase 1: Positioning Alignment Analysis

Before recommending any content, reason through:

1. **Positioning check:** Is the one-liner specific enough to anchor content pillars? If it's "I help businesses grow," that's too vague — push for specificity before proceeding.
2. **Audience clarity:** Are we targeting a specific title + company stage, or a demographic? Specific is better.
3. **Time-to-output match:** If they have 2 hours/week, don't recommend 5 posts/week. Sustainability matters more than ambition.
4. **Goal alignment:** Content for lead generation looks different from content for speaking gigs. Confirm goal before building pillars.

Output a brief strategy assessment:
> "You're a [role] targeting [audience] with [X hours/week] and a goal of [outcome]. I'll build a [3/5 post/week] strategy anchored to [X] pillars. The main gap in your current approach: [specific gap]."

---

## Phase 2: Content Pillars (3–5 Required)

Each pillar must pass all 4 tests:
1. You have genuine expertise (not just interest)
2. Your target audience actively cares about it
3. You can produce content on it consistently for 6+ months
4. It connects to what you sell or want to be known for

**Pillar ratio:**
- 70% core expertise → builds authority
- 20% adjacent insights → makes you interesting
- 10% personal → makes you relatable

**Output format per pillar:**
```
Pillar: [Name]
Ratio: [%]
Content types: [frameworks / stories / case studies]
Example hook: "[First line of a real post]"
Connection to goal: [how this drives the stated outcome]
```

---

## Phase 3: Format Selection & Post Templates

### Format-to-Goal Mapping

| Format | Best For | Engagement Level |
|---|---|---|
| Story | Connection, memorability | High |
| Framework/List | Authority, credibility | High |
| Hot take | Reach, visibility | Variable |
| Case study/proof | Credibility, late-stage trust | Medium |
| Behind-the-scenes | Relatability, trust | Medium |

**Recommended weekly mix:**
- 2–3 frameworks (authority)
- 1–2 stories (connection)
- 1 proof point (credibility)

### Post Templates

**Story Post:**
```
[Hook — the moment or realization]
[Setup — quick context]
[Tension — what was hard or went wrong]
[Turn — the insight]
[Lesson — the takeaway]
[Question — drives engagement]
```

**Framework Post:**
```
[Hook — bold claim or problem statement]
[Why this matters — 1-2 sentences]
[The X-step framework:]
1. [Step + brief explanation]
2. [Step + brief explanation]
3. [Step + brief explanation]
[Key insight or summary]
[CTA or discussion question]
```

**Hot Take:**
```
[Controversial statement]
[Your reasoning — 2-3 sentences]
[The nuance people miss]
[What to do instead]
[Question to drive comments]
```

---

## Phase 4: Content Calendar with Real Dates

Generate a 4-week calendar with actual dates (not generic day names):

| Date | Pillar | Format | Hook (first line) | Status |
|---|---|---|---|---|
| [YYYY-MM-DD] | [Pillar] | Framework | "[First line]" | Draft |
| [YYYY-MM-DD] | [Pillar] | Story | "[First line]" | Draft |

Fill 4 full weeks. Generic "Week 1, Monday" output is not sufficient.

Also output **5 starter post hooks** ready to write immediately — these break the blank-page problem:
```
1. [Hook]
2. [Hook]
3. [Hook]
4. [Hook]
5. [Hook]
```

---

## Phase 5: Self-Critique Pass (REQUIRED)

After generating the strategy, evaluate:

- [ ] Is the positioning one-liner specific enough to anchor the pillars?
- [ ] Are the 5 starter hooks actually strong — would they stop the scroll?
- [ ] Does the time commitment match the user's stated available hours?
- [ ] Is at least one pillar directly tied to the revenue/goal outcome?
- [ ] Does the calendar have actual dates, or just generic "Day 1/Day 3" placeholders?
- [ ] Would this content system still work in 6 months if the user stays consistent?

Flag issues: "Pillar 3 ('general business tips') doesn't connect to your stated goal of attracting SaaS founders. Replace with something more specific."

---

## Phase 6: 30-Day Iteration Protocol

After 30 days, review with these questions:
- Which posts got the most comments? What pillar did they fall under?
- Which posts drove DMs or profile views?
- Which posts got the most impressions regardless of engagement?

**Adjust based on data:**
- If case study posts outperform frameworks → increase case study ratio
- If stories drive DMs but frameworks drive impressions → use both intentionally

---

## Output Structure

```markdown
## LinkedIn Strategy: [Name] — [Date]

### Positioning Alignment
[One-liner + assessment of clarity]

### Content Pillars
[3-5 pillars with ratio, examples, connection to goal]

### Weekly Rhythm
- Posts/week: [X]
- Best times: [e.g., Tue/Thu 8am EST]
- Active commenting: [X min/day]

### Format Mix
[Breakdown with rationale]

### 4-Week Content Calendar
[Table with real dates + hooks]

### 5 Starter Posts (Write These First)
[Hooks with format labels]

### Engagement Plan
[Who to engage with, how much time, what to say]

### Self-Critique Notes
[Issues flagged + recommended fixes]

### 30-Day Review Triggers
[What to measure and when to adjust]

### Cross-References
- linkedin-profile-optimizer (run before publishing)
- content-idea-generator (for ongoing idea generation)
- voice-extractor (to ensure posts sound authentic)
```

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
