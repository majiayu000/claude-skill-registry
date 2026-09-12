---
name: brainstorm
description: |
  Structured marketing brainstorming when direction is unclear. Use when the agent doesn't know which skill to run, the user is vague about what they need, there are multiple valid marketing paths, or someone says 'I don't know where to start', 'what should we market', 'explore approaches', 'help me think through this', 'marketing ideas', 'what campaign should I run', 'where do I start with marketing', 'what's our marketing plan', or 'I have no idea how to promote this'. Explores 2-3 approaches and recommends the best path forward with a specific next-skill handoff. Even vague frustration like 'nobody knows about my product' or 'how do I get users' should trigger this when no specific channel or tactic is mentioned.
allowed-tools: []
---

# /brainstorm — Marketing Brainstorm

Structured exploration when marketing direction is unclear. You produce a brief that tells /cmo where to route next.

For brand memory protocol, see /cmo [rules/brand-memory.md](../cmo/rules/brand-memory.md).

## On Activation

1. Read `brand/` files if they exist (voice-profile.md, audience.md, positioning.md, learnings.md). They enhance but never gate.
2. Assess the user's request clarity level.

## Phase 0: Assess Clarity

Gate check. If the request is already specific, skip brainstorming:

| Signal | Action |
|--------|--------|
| "Write a landing page for X" | Skip. Route to `direct-response-copy`. |
| "Do SEO for my blog" | Skip. Route to `keyword-research`. |
| "I want to market my app" | Proceed. Multiple valid paths. |
| "What should I do next?" | Proceed. No clear direction. |
| "Help me think through our launch" | Proceed. Needs exploration. |

If skipping: "Your request is specific enough to execute directly. Routing to `/<skill>` instead of brainstorming."

## Phase 1: Understand the Challenge

Ask ONE question at a time. Prefer multiple choice when natural options exist. Skip questions already answered by brand/ context.

**Questions to cover (in order, stop when clear):**

1. **Goal** — What are you trying to achieve? (awareness / leads / revenue / retention / launch)
2. **Product** — What are you marketing? (Brief description if not obvious from project context)
3. **Audience** — Who buys this? (Skip if `brand/audience.md` exists and is current — confirm briefly instead: "Your audience profile says X. Still accurate?")
4. **Channels** — Where does your audience hang out? (search / social / email / communities / paid)
5. **Constraints** — Budget, timeline, team size, tools available?
6. **Competition** — Who else does this? What makes you different? (Skip if `brand/competitors.md` exists — reference it instead)

Stop as soon as you have enough to propose approaches. 3-4 questions is usually enough.

## Phase 2: Explore Approaches

Present 2-3 concrete strategic directions. For each:

```
### Approach [N]: [Name]

**Core angle:** [One sentence positioning]
**Channels:** [Primary → Secondary]
**Audience fit:** [Why this resonates with the target]
**Timeline:** [Quick win vs. long play]
**Pros:** [2-3 bullet points]
**Cons:** [1-2 bullet points]
**Best when:** [Conditions that make this the right choice]
```

Ask the user to pick one, combine elements, or explore further.

**Handling responses:**

| User says | Action |
|-----------|--------|
| Picks an approach | Move to Phase 3 with that approach |
| Wants to combine | Merge the relevant elements into a hybrid approach, confirm the blend, then move to Phase 3 |
| Rejects all approaches | Ask what felt wrong. Probe for the constraint or preference you missed. Generate 1-2 new approaches informed by their feedback |
| "I want to do all of them" | Recommend a sequence: "Start with [approach] because [reason]. If that works, layer in [approach 2] in week 3." Prioritize, don't parallelize |
| Wants to explore further | Ask one targeted follow-up question, then generate 1-2 additional approaches |

## Phase 3: Capture Marketing Brief

Write a structured brief to `marketing/brainstorms/YYYY-MM-DD-<topic>-brainstorm.md`:

```markdown
---
type: marketing-brainstorm
date: YYYY-MM-DD
topic: [kebab-case topic]
goal: [awareness|leads|revenue|retention|launch]
chosen-approach: [N]
---

# Marketing Brief: [Topic]

## Context
[What we're marketing and why now]

## Chosen Approach
[Selected direction with rationale]

## Target Audience
[Who we're reaching]

## Channels
[Primary and secondary channels]

## Key Messages
[3-5 core messages]

## Constraints
[Budget, timeline, tools]

## Success Metrics
[How we'll measure impact]

## Structured Handoff
next-skill: [skill-name]
confidence: [high|medium|low]
context-summary: "[One line summary for /cmo routing]"
```

The `next-skill` field is critical — it tells /cmo where to route after brainstorming.

## Phase 4: Route Back to /cmo

After writing the brief:

"The brainstorm is complete. Brief saved to `marketing/brainstorms/[filename]`. Run `/cmo` to execute the next step (`/[next-skill]`), or invoke `/<next-skill>` directly."

Do not list all 50 skills. Recommend the ONE next skill based on the brief.

## Worked Example

**User request:** 'I just built a verified meal delivery app, what should I do for marketing?'

**Approach 1: Community-Led Growth**
Build presence in health-focused community spaces (neighborhood Slack groups, campus food subreddits, verified-source food Instagram). Create shareable content that spreads through existing trust networks.
→ next-skill: audience-research

**Approach 2: SEO + Content**
Capture 'verified meal delivery' search traffic with city-specific landing pages. Write comparison content ('Is DoorDash organic?') to redirect competitor traffic.
→ next-skill: keyword-research

**Recommended:** Approach 1 — community trust is the moat for verification-driven products. SEO is Phase 2 after you have testimonials to feature.

---

## Output Format

Follow the output formatting rules from /cmo [rules/output-format.md](../cmo/rules/output-format.md). Key requirements:
- Header with "MARKETING BRAINSTORM" and date
- Each approach as a clearly separated section
- FILES SAVED section showing the brief path
- WHAT'S NEXT section with the recommended next-skill

## Anti-Patterns

| Anti-pattern | Instead | Why |
|-------------|---------|-----|
| Asking 5+ questions at once | One question at a time, multiple choice | Builders get overwhelmed by question walls. Each answer should shape the next question. |
| Jumping straight to tactics | Explore the strategic direction first | Tactics without strategy leads to scattered effort. "Post on TikTok" isn't a plan. |
| Proposing 5+ approaches | 2-3 focused options, not a menu | More options = more decision paralysis. The builder came here because they were stuck — don't make it worse. |
| Generic advice ("build an audience") | Specific to their product and context | Anyone can say "build an audience." The value is knowing WHICH audience, WHERE, with WHAT message. |
| Brainstorming when direction is clear | Skip to the execution skill | Brainstorming is exploration, not procrastination. If they know what they want, execute. |
| Leaving the user without a next step | Always include `next-skill` in the brief | A brainstorm that doesn't lead to action is just a meeting. The handoff is the whole point. |

## YAGNI Principles

- Resist adding channels you can't actually execute on
- One campaign well-executed beats three half-started
- If the user has no audience data, start with `audience-research`, not guessing
- Don't brainstorm pricing, launches, or SEO strategy — those have dedicated skills
- The brief is a compass, not a bible. It should fit on one page.
