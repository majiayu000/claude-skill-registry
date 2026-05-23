---
name: cold-outreach-sequence
description: Build personalized cold outreach sequences for LinkedIn and email. Use when someone needs to reach prospects, warm up cold leads, or build a systematic outreach engine. Covers research, connection requests, follow-ups, and conversion.
---

# Cold Outreach Sequence

Here's what I've learned about cold outreach: the word "cold" is the problem.

Spray-and-pray templates don't work. 10 minutes of research + a specific reference = not cold anymore. This skill builds the second kind.

---

## Mode

Detect from context or ask: *"One message, full sequence, or full outreach system?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | 1 connection request + 1 follow-up for a single prospect | Testing an angle, one-off outreach |
| `standard` | Full 4-touch sequence for a single prospect | Active pipeline, individual targets |
| `deep` | Multi-prospect sequence system + A/B variants + tracking framework | Launching an outreach campaign |

**Default: `standard`** — use `quick` if they give you one name and say "draft something." Use `deep` if they're building a repeatable outreach engine.

---

## Context Loading Gates

**Before writing any message, collect:**

- [ ] **Prospect name and company** — full name, company, role/title
- [ ] **Research signals** — run tool calls first (see below); do not write without them
- [ ] **Sender positioning** — what does the sender do, for whom, with what result? (Use `positioning-basics` output if available)
- [ ] **Platform** — LinkedIn DM, email, or both?
- [ ] **Batch size** — how many prospects? (determines tier assignment)

**Research tool calls — run before writing:**

```
web_search('[Company] [Founder/Name] news 2026')
web_search('[Company] funding recent')
web_search('[Person name] [Company] LinkedIn')
```

**Personalization constraint:** Do not write a Tier 1 message without a named specific signal from research. If search yields 0 signals, default to Tier 3 and say so explicitly.

---

## Phase 1: Research & Signal Assessment

For each prospect, document findings before drafting:

**Signal types (ranked by message strength):**
1. Recent news event (funding, launch, hire, press) → strongest signal
2. Recent LinkedIn post activity → strong signal
3. Company stage/growth data → medium signal
4. Role + industry awareness only → weak signal (Tier 3)

**Personalization tier assignment:**

| Research Result | Tier | Approach |
|---|---|---|
| Named signal (news + post + context) | Tier 1 | Fully custom, reference signal in every message |
| Company info + role context | Tier 2 | Template + personalized opener |
| No signals found | Tier 3 | Volume template, minimal customization |

---

## Phase 2: Sequence Generation

### Connection Request (LinkedIn) — 300 chars max

**Formula:** `[Specific observation from research] + [Simple reason to connect]`

**Rules:**
- No pitching
- Prove you did research (name the signal)
- One sentence, conversational
- Never "I'd love to pick your brain"

**By signal type:**
```
Recent funding: "Congrats on the Series A — the [investor] backing is a smart signal. Would love to connect."

Recent post: "Your post on [specific topic] resonated — been thinking the same thing. Happy to connect."

News/launch: "Saw the [product] launch — [specific detail] is smart positioning. Would love to connect."
```

---

### First Message (After Accept — Wait 24-48 Hours)

**Formula:** `[Thanks] + [Bridge to relevance] + [Light value] + [Soft question]`

**Template:**
```
Thanks for connecting. I work with [ICP description] on [specific outcome].

Curious — is [relevant function] something you own directly at [Company], 
or is that still founder-led?

Happy to share what I'm seeing work at similar-stage companies either way.
```

---

### Follow-Up #1 (Day 7)

**Formula:** `[Light nudge] + [New signal or angle] + [Easy out]`

**Constraint:** Do NOT write "following up" with nothing new. Add one new piece:
- A relevant article or trend
- A related insight you recently had
- A connection to something they posted

**Template:**
```
Bumping this up — came across [specific article/trend/insight] and 
thought of your situation at [Company].

[One sentence on why it's relevant to them.]

Happy to share more if useful. If not, no worries.
```

---

### Follow-Up #2 (Day 14)

Shift to email if LinkedIn hasn't converted, or try a different angle.

**Subject line options:**
- "[Company]'s [function] as you scale"
- "Saw your [post/news] — quick thought"
- "Question about [specific thing they're doing]"

**Email structure:**
```
[1-line hook tied to their specific situation]

[2-3 sentences: why you're reaching out + one proof point]

[Soft CTA — 1 sentence]
```

---

### Break-Up Message (Day 21)

```
I'll assume timing isn't right — totally get it. 

If [relevant pain point] becomes a priority down the road, happy to reconnect. 
Best of luck with [specific thing they're working on based on research].
```

**Post-break-up action:** Add to 6-month re-engagement list with a resurface date.

---

## Phase 3: Self-Critique Pass (REQUIRED)

After generating the full sequence, evaluate:

- [ ] Does every message reference the specific signal from research, or are they generic?
- [ ] Is the connection request under 300 characters?
- [ ] Does the first message ask a question (invite dialogue) rather than pitch?
- [ ] Does follow-up #1 add something genuinely new, or is it just "following up"?
- [ ] Does the break-up message reference something specific about their situation?
- [ ] Did I correctly assign the personalization tier, or am I over-personalizing a Tier 3 prospect?

Flag any issue: "The first message doesn't include a soft question — it reads as a pitch. Revised to invite dialogue."

---

## Pipeline Tracking Table

Always output a tracking table for the batch:

```markdown
| Prospect | Company | Platform | Tier | Sent Date | Response | Stage | Next Action | Resurface Date |
|---|---|---|---|---|---|---|---|---|
| [Name] | [Co] | LinkedIn | 1 | [date] | — | Connection sent | Wait 24-48h | — |
| [Name] | [Co] | Email | 2 | [date] | — | First email sent | Follow-up Day 7 | — |
```

---

## Iteration Protocol

After each response (or non-response), ask:
- Did the connection request get accepted? If low acceptance rate → revise the observation line
- Did the first message get a reply? If no → was the question soft enough, or did it feel like a pitch?
- Did follow-ups get ignored? If yes → try a different angle or acknowledge the silence directly

---

## Output Structure

```markdown
## Outreach Sequence: [Prospect Name] — [Date]

### Research Summary
- Signal type: [news / post / company info / none]
- Signal found: "[Specific detail]"
- Personalization tier: [1/2/3]
- Source: [URL or platform]

### Sequence

**Connection Request (LinkedIn):**
[Text — max 300 chars]

**First Message (Day 1-2 after accept):**
[Text]

**Follow-Up #1 (Day 7):**
[Text]

**Follow-Up #2 (Day 14):**
Platform: [LinkedIn / Email]
Subject: [if email]
[Text]

**Break-Up (Day 21):**
[Text]

### Pipeline Entry
| Prospect | Company | Platform | Tier | Stage | Next Action | Resurface Date |
|---|---|---|---|---|---|---|
| [Name] | [Co] | [Platform] | [Tier] | Connection sent | Wait 24-48h | — |

### Self-Critique Notes
[Any issues flagged + revisions made]
```

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
