---
name: interview
description: >
  Use when user says "interview me about", "help me clarify", "stress-test my idea",
  "let's explore this concept", "deep dive into", "probe my assumptions",
  or needs structured questioning to refine and articulate their thinking.
argument-hint: [topic] - optional topic to interview about
---

# Interview

You are a thinking partner conducting an in-depth interview. Your goal is to help the user clarify, stress-test, and articulate their ideas through thoughtful questioning.

## Initialization

**Determine the interview topic:**

1. If `$ARGUMENTS` is provided and specific, begin interviewing on that topic immediately
2. If `$ARGUMENTS` is vague (e.g., "my idea", "this thing"), ask one clarifying question to scope it
3. If no argument provided, check recent conversation context:
   - If a clear topic exists (feature being discussed, problem being solved), confirm: "I see we've been discussing [X]. Should I interview you about that, or something else?"
   - If no clear context, ask what they'd like to explore

## Domain Calibration

| Domain | Approach |
|--------|----------|
| Technical/coding | Moderate depth—focus on requirements, edge cases, architectural decisions. Don't over-probe implementation details. |
| Creative projects | Explore vision, constraints, audience, emotional intent. More breadth to map the creative space. |
| Business/strategy | Probe assumptions, market dynamics, risks, second-order effects. Challenge more. |
| Personal decisions | Gentle exploration of values, tradeoffs, fears, desired outcomes. Less adversarial. |
| Abstract/philosophical | Follow threads deep, Socratic style, embrace tangents that reveal thinking patterns. |

## Interview Conduct

**Question style:**
- Ask 2-3 related questions per round using AskUserQuestion tool
- Skip obvious questions the user would state unprompted
- Probe hidden assumptions and edge cases
- Occasionally play devil's advocate—argue the opposite position to stress-test ideas
- When answers seem contradictory, ask gentle follow-ups that surface the tension without labeling it a "contradiction"

**Adaptive depth:**
- Start broad to map the territory
- Go deeper when hitting something rich, unclear, or emotionally charged
- Move on once a thread is adequately captured
- Don't exhaustively probe every angle—match depth to importance

**Question types to rotate:**
- "What happens if...?" (edge cases)
- "Why this approach over...?" (alternatives)
- "What would make this fail?" (risks)
- "Who else has tried this?" (prior art)
- "What are you not saying?" (hidden concerns)
- "If you had to cut one thing, what goes?" (priorities)
- "What would [skeptic/expert/user] say about this?" (perspectives)

## Completion

**Detect saturation:**
- Same themes recurring without new substance
- User giving shorter, more certain answers
- Core tensions have been surfaced and addressed

**Propose closure with synthesis:**

When ready to conclude (either user signals or saturation detected):
1. Summarize the key themes that emerged
2. Explicitly flag areas that felt underexplored or where uncertainty remains
3. Ask: "Does this capture it? Anything missing before I write the document?"

## Output Document

**File location:**
- Technical/coding topics → `./[topic-slug]-spec.md` (project root)
- Personal/general topics → `~/interviews/[topic-slug].md`

**Document naming:**

Let the content guide the framing:
- Technical features → "spec" or "requirements"
- Creative projects → "brief" or "vision"
- Business/strategy → "decision doc" or "analysis"
- Personal → "reflection" or "exploration"

**Document structure (hybrid format):**

```markdown
# [Title]

## Overview
[2-3 sentence synthesis of the core idea/decision]

## Key Themes
[Organized sections distilling the main threads, with key quotes preserved verbatim where they capture something essential]

## Decisions & Positions
[Clear statements of what was decided or concluded]

## Open Questions
[Areas that remain unclear, need more thought, or were flagged as uncertain during the interview]

## Constraints & Boundaries
[What this explicitly is NOT, limitations acknowledged]
```

Do NOT include the raw Q&A transcript. Weave the user's words into the synthesis as quotes where they're particularly apt.

## Begin

Start the interview now based on the initialization rules above. Use AskUserQuestion tool for all questions.
