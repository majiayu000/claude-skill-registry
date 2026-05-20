---
name: content-idea-generator
description: Generate content ideas rooted in positioning. Use when someone needs "content ideas," "what should I post," "blog topics," "LinkedIn ideas," or is stuck on what to create.
---

# Content Idea Generator

Content without positioning is noise. Before generating ideas, confirm positioning is clear. If not, run `positioning-basics` first.

---

## Mode

Detect from context or ask: *"Quick ideas, full strategy, or complete content system?"*

| Mode | What you get | Best for |
|------|-------------|----------|
| `quick` | 5 ideas, immediate output, no deep research | Breaking a block, starter brainstorm |
| `standard` | 10–15 positioned ideas with formats and rationale | Regular content planning |
| `deep` | Full content calendar system: pillars, formats, cadence, 30-day plan | Launching or overhauling content strategy |

**Default: `standard`** — use `quick` if they just need to start. Use `deep` if they want a repeatable system, not just today's ideas.

---

## Context Loading Gates

**Before generating any ideas, collect:**

- [ ] **Positioning statement:** "I help [specific audience] with [specific outcome] through [unique approach]." Must be specific — not "I help businesses grow."
- [ ] **ICP specifics:** What are the top 3 frustrations or questions the ideal customer has right now?
- [ ] **Recent wins or proof points:** Any client results, experiments, or lessons from the last 30 days?
- [ ] **Content formats available:** LinkedIn? Twitter/X? Newsletter? Short video? All?
- [ ] **Prior content strategy:** Any existing pillars from `linkedin-authority-builder`? Don't generate outside those pillars if they exist.

**Positioning gate:** If the user cannot complete the positioning sentence with specifics, stop:
> "Content without positioning produces random posts. Complete this first: 'I help [specific audience] achieve [specific outcome] through [unique approach].' If you need help, run `positioning-basics` first."

---

## Phase 1: Context Analysis

Before generating ideas, reason through:

1. **Positioning strength:** Is the one-liner specific enough to anchor content ideas? A vague positioning produces vague ideas.
2. **Proof point audit:** What real results, experiments, or opinions does the user have? Generic ideas come from generic inputs — specific proof points produce specific content.
3. **Platform match:** Different platforms need different idea formats. LinkedIn rewards frameworks and stories; Twitter rewards brevity and contrarian takes; newsletters reward depth and curation.
4. **Content gap:** What has the user NOT covered yet that their ICP is actively asking about?

Output a brief analysis:
> "You're creating content for [audience] as a [role]. Your strongest proof point is [X]. I'll generate ideas anchored to that — the biggest content gap I see is [specific gap]."

---

## Phase 2: Freshness Check (Tool Call)

Run a search before generating the batch:

```
web_search('[Topic] trending [Month Year]')
web_search('[ICP role] biggest challenges [Year]')
```

Use results to:
- Identify timely angles on evergreen topics
- Spot what competitors aren't covering (your opportunity)
- Include at least 1 current-moment hook in the batch

---

## Phase 3: Idea Generation with Quality Filter

Generate ideas using these 6 frameworks:

### 1. The Problem Call-Out
Name the pain your audience won't admit publicly.
**Template:** "The #1 mistake [audience] makes with [topic]"

### 2. The "Here's What Works" Breakdown
Teach a specific process you've actually used.
**Template:** "How to [achieve outcome] without [common obstacle]"

### 3. The Contrarian Take
Challenge something everyone assumes is true.
**Template:** "Stop [common advice]. Here's what actually works."

### 4. The Behind-the-Curtain Story
Show the messy reality, not the highlight reel.
**Template:** "I [tried thing]. Here's what actually happened."

### 5. The Pattern Recognition
Connect dots your audience hasn't connected yet.
**Template:** "What [experience A] taught me about [topic B]"

### 6. The Resource Stack
Curate genuinely useful tools.
**Template:** "[Number] tools I actually use for [outcome]"

---

## Phase 4: Quality Filter (Run Every Idea Through This)

Each idea must pass all 3 tests before being included in the output:

1. **Specific?** — Does it have a concrete angle? ("How to use LinkedIn" → fails. "How to get DMs from framework posts with <500 followers" → passes.)
2. **Has a hook angle?** — Can you write a specific first line that stops the scroll?
3. **Connects to ICP pain?** — Does it address a real, named frustration of the target customer?

Reject and replace any idea that fails 2 or more tests.

---

## Phase 5: Self-Critique Pass (REQUIRED)

After generating the full batch, evaluate:

- [ ] Are all ideas anchored to the stated positioning, or did any drift outside the lane?
- [ ] Does each idea have a specific enough hook that I could write the first line right now?
- [ ] Are the Quick Wins genuinely low-effort to produce, or are they actually complex pieces?
- [ ] Is at least one idea tied to a real proof point or story the user mentioned?
- [ ] Did the freshness search produce anything useful, or were results too generic?

Flag and replace any ideas that don't pass: "Idea 3 ('thoughts on AI in marketing') is too broad for your positioning as a [specific role]. Replaced with: [specific angle]."

---

## Fluff Filter: Do Not Include

❌ "Grateful for the journey" posts — show the work instead
❌ Generic motivational quotes without a specific take
❌ Vague "thought leadership" with no actual opinion
❌ Engagement bait with no value ("Agree? Comment below")
❌ Topics outside the stated positioning

**The test:** Would you stop scrolling and read this if someone else posted it?

---

## Output Structure

```markdown
## Content Ideas: [Name] — [Date]
**Positioning used:** [one-liner]
**Freshness search:** [query + key finding]

---

### Quick Wins (Post This Week)
*5 ideas ready to create now*

**1. [Title/Angle]**
- Hook: "[First line that stops the scroll]"
- Core insight: [The one thing they'll remember]
- Platform fit: [LinkedIn / Twitter / Newsletter]
- ICP pain: [What frustration this addresses]
- Quality check: [Specific ✅ | Hook ✅ | ICP ✅]

[Repeat for ideas 2–5]

---

### Authority Builders (This Month)
*3 ideas worth the investment*

**1. [Title/Angle]**
- Hook: "[First line]"
- Core insight: [Key takeaway]
- Platform fit: [Platform]
- Research needed: [What to find first]
- Estimated production time: [X hours]

[Repeat for ideas 2–3]

---

### Self-Critique Notes
[Any ideas replaced, gaps noted, or freshness findings]

### Multi-Agent Handoff
For each approved idea → pass to Scribe with format:
[Idea title] | [Platform] | [Hook] | [Framework type] | [ICP pain addressed]
```

---

*Skill by Brian Wagner | AI Marketing Architect | brianrwagner.com*
