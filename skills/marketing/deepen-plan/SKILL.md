---
name: deepen-plan
description: |
  Enhance an existing marketing plan with parallel research. Use when the agent has a draft plan (brand strategy, campaign brief, content calendar, launch plan) that needs strengthening with real data. Triggers on 'deepen this plan', 'strengthen this strategy', 'research gaps in my plan', 'make this plan better', 'this plan is too surface level', 'add research to this', 'validate this plan', 'back this up with data', or when a plan exists but lacks audience data, competitive positioning, or keyword strategy. Make sure to use this whenever someone has an EXISTING plan that feels thin or unresearched — even if they just say 'is this plan good enough?' or 'what's missing here?', they likely need deepening. This skill ENHANCES existing plans — it does not create new ones. If no plan exists, route to /brainstorm or /launch-strategy first.
---

# /deepen-plan — Plan Enhancement with Parallel Research

The second pass. Takes an existing marketing plan and strengthens it with targeted research — audience data, competitive intel, keyword gaps — then merges findings back in.

For brand memory protocol, see /cmo [rules/brand-memory.md](../cmo/rules/brand-memory.md).

## On Activation

1. Read `brand/` files if they exist (voice-profile.md, audience.md, competitors.md, positioning.md, keyword-plan.md). They enhance but never gate.
2. Identify the plan to deepen — the user will either point to a file or have one in context.

## Phase 0: Assess the Plan

Read the existing plan and classify it:

| Plan Type | Signals | Common Gaps |
|-----------|---------|-------------|
| Brand strategy | Voice, positioning, values | Missing audience data, no competitive differentiation |
| Campaign brief | Timeline, channels, messages | Vague audience, no keyword backing, weak positioning |
| Content calendar | Topics, dates, channels | No keyword research, missing distribution strategy |
| Launch plan | Timeline, milestones, channels | No competitive landscape, missing pricing context |
| Brainstorm output | Approaches, recommendations | Everything — brainstorms are directional, not researched |

If no plan is found or provided:
"I need an existing plan to deepen. Either point me to a file or run `/brainstorm` or `/launch-strategy` first to create one."

If the plan is embedded in conversation context (not a file): extract the key sections and work with them inline. Note in the handoff that the deepened plan should be saved to a file.

## Phase 1: Gap Analysis

Score the plan across 5 dimensions. For each, rate as **strong**, **weak**, or **missing**:

```
### Plan Gap Analysis

| Dimension | Status | Evidence |
|-----------|--------|----------|
| Audience clarity | [strong/weak/missing] | [What the plan says or doesn't] |
| Competitive positioning | [strong/weak/missing] | [What the plan says or doesn't] |
| Keyword/search strategy | [strong/weak/missing] | [What the plan says or doesn't] |
| Distribution plan | [strong/weak/missing] | [What the plan says or doesn't] |
| Success metrics | [strong/weak/missing] | [What the plan says or doesn't] |
```

Show this table to the user. Explain which gaps you'll fill and why they matter:
"Your campaign brief has strong messaging but no audience data backing it. The competitive section is a single sentence. I'm going to research both in parallel — this will take a few minutes but will make the plan 3x more actionable."

If all dimensions are **strong**: "This plan is solid. I don't see gaps worth researching. If you want me to dig deeper on a specific section, tell me which one."

### Quality Gate

A dimension is **strong** when it contains:
- Specific data points (numbers, names, quotes) rather than vague statements
- Actionable details an agent or human could execute on
- Evidence of research, not just assumptions

A dimension is **weak** when it:
- States the obvious without specifics ("target tech-savvy users")
- Has the right structure but lacks data backing
- Makes claims without evidence

A dimension is **missing** when:
- The section doesn't exist at all
- It's a single vague sentence

## Phase 2: Parallel Research

Spawn research agents based on the gaps found. Use the Agent tool to run up to 3 agents **simultaneously in a single message**:

### When audience is weak or missing:
Spawn `mktg-audience-researcher`:
- Provide: the product/project name, what it does, who the plan currently targets (if stated)
- Agent writes to `brand/audience.md`
- Tell it: "Research the target audience for [product]. The current plan says [quote relevant section]. Find buyer personas, where they hang out online, what language they use, and what objections they have. Write findings to brand/audience.md."

### When competitive positioning is weak or missing:
Spawn `mktg-competitive-scanner`:
- Provide: the product/project name, market space, any competitors mentioned in the plan
- Agent writes to `brand/competitors.md`
- Tell it: "Research competitors for [product] in the [space] market. The current plan mentions [competitors if any]. Find 3-5 competitors, their positioning, pricing, strengths, and weaknesses. Write findings to brand/competitors.md."

### When keyword/search strategy is weak or missing:
Do NOT spawn an agent. Instead, note that keyword research should be run after deepening:
- Add to the synthesis: "Keyword strategy gap identified. After this deepening pass, run `/keyword-research` to fill this with real search data."

### When distribution is weak or missing:
Do NOT spawn an agent. Distribution gaps are filled during synthesis by cross-referencing audience data (where they hang out) with the plan's channel strategy.

### When success metrics are weak or missing:
Do NOT spawn an agent. Metrics are filled during synthesis based on the plan type and channels.

**Minimum research:** At least 1 agent must be spawned. If no gaps warrant an agent, skip to Phase 3 with a note.

**Fallback:** If agents are not installed (`mktg doctor` shows agents missing), read the corresponding skill files and execute the research inline — first audience, then competitive. This is slower but works everywhere.

## Phase 3: Synthesize

After all research agents complete, merge findings into the plan. Follow these rules:

1. **Read the research outputs** — `brand/audience.md`, `brand/competitors.md`, or any other files the agents wrote.
2. **Do not rewrite the plan.** Add to it. The user's original thinking is preserved.
3. **For each gap that was researched, add a new subsection** within the relevant part of the plan:

```markdown
### Audience Research (Added [YYYY-MM-DD])
[Synthesized findings from audience-researcher, tailored to this plan's context]

### Competitive Landscape (Added [YYYY-MM-DD])
[Synthesized findings from competitive-scanner, tailored to this plan's context]
```

4. **Strengthen existing sections** — If the plan had a weak audience section, enhance it with specifics from the research. Add quotes, data points, persona details. Don't replace the original text; build on it.
5. **Fill distribution gaps** using audience data — "Your audience is active in [communities/platforms]. Add these to your distribution plan: [specific channels]."
6. **Fill metrics gaps** based on plan type:
   - Brand strategy -> awareness metrics (search volume, social mentions, brand recall)
   - Campaign brief -> campaign metrics (CTR, conversion rate, CAC)
   - Content calendar -> content metrics (organic traffic, time on page, email signups)
   - Launch plan -> launch metrics (day-1 signups, activation rate, press mentions)

## Phase 4: Handoff

1. **Write the updated plan** back to its original file location. If the plan was provided inline (not from a file), write to `marketing/plans/YYYY-MM-DD-<topic>-deepened.md`.

2. **Append a deepening log** at the bottom of the plan:

```markdown
---

## Deepened on [YYYY-MM-DD]

**Gaps addressed:**
- [List each gap and what was added]

**Research agents used:**
- [agent-name]: [one-line summary of findings]

**Remaining gaps:**
- [Any gaps not addressed and recommended next skill]

**Suggested next step:** /[skill-name] — [why]
```

3. **Append to `brand/learnings.md`** (if it exists):
```
- [YYYY-MM-DD] [/deepen-plan] Deepened [plan-type] for [project]. Key finding: [most surprising or actionable insight from research].
```

4. **Tell the user what changed:**
"Plan deepened. Here's what I added: [2-3 sentence summary]. The biggest insight from research was [highlight]. Your plan now has [strong count]/5 dimensions covered. Suggested next step: `/[skill]` to [reason]."

---

## Anti-Patterns

| Anti-pattern | Why it fails | Instead |
|-------------|-------------|---------|
| Rewriting the user's plan from scratch | The user's original thinking contains context and decisions you don't have — overwriting it loses institutional knowledge | Add to existing sections, preserve original thinking |
| Running all 5 research types regardless | Researching what's already strong wastes time and may contradict validated decisions the user already made | Only research actual gaps — strong sections don't need more data |
| Spawning agents for keyword or distribution gaps | Keyword research is a complex methodology that deserves its own skill run — a quick agent pass produces shallow results that mislead | Keywords need `/keyword-research` skill. Distribution is synthesized from audience data |
| Deepening a plan that doesn't exist yet | You can't enhance nothing — the agent will hallucinate a plan and then deepen its own hallucination | Route to `/brainstorm` or `/launch-strategy` first |
| Running without showing the gap analysis | The user should see and approve what you're about to research — surprise research wastes cycles if they already know the answers | Always show the gap table and explain what you'll research |
| Silently updating brand files | Brand files persist across sessions — silent updates may overwrite previous research the user relied on | Agents write to brand/. That's fine. But tell the user what was updated |
| Deepening the same plan twice without new context | Double-deepening without new information just adds redundant research and makes the plan harder to read | Flag it: "This plan was already deepened on [date]. Want me to research something specific, or has the situation changed?" |

## YAGNI Principles

- Don't research what's already strong. A solid audience section doesn't need more audience research.
- Don't add sections the plan doesn't need. A content calendar doesn't need a pricing analysis.
- Don't create a new plan. This skill enhances, it doesn't generate.
- Don't run keyword research inline. That's a dedicated skill with its own methodology.
- The gap analysis table is the decision framework. If it shows all strong, you're done.

---

## Related Skills

- **brainstorm**: When no plan exists yet and the user needs direction
- **launch-strategy**: When the plan to deepen is a launch plan, or when no plan exists
- **keyword-research**: For filling keyword/search strategy gaps identified in gap analysis
- **audience-research**: For deep-dive audience work beyond what the researcher agent provides
- **competitive-intel**: For deep competitive analysis beyond the scanner agent
