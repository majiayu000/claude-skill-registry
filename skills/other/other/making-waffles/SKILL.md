---
name: making-waffles
description: Generates WAFFLES Declarations for social media posts — preemptive lists of what a post does NOT say. Use when users mention WAFFLES, ask for clarifications on their post, want to prevent misinterpretation, or request disclaimers for controversial/nuanced takes.
metadata:
  version: 0.1.0
---

# WAFFLES Declaration Generator

Generate preemptive clarifications listing what a post explicitly does NOT say, helping low-context readers avoid misinterpretation.

## Background

"WAFFLES" originated from Bluesky's October 2025 controversy. A meme satirized how users read hostile implications into innocuous posts: "(bluesky user bursts into Waffle House) OH SO YOU HATE PANCAKES??" CEO Jay Graber's reply of "WAFFLES!" to an off-topic comment sparked platform-wide debate. The term evolved into a declaration format pioneered by @gracekind.net — a preemptive list of things a post does NOT claim.

## When Triggered

Generate a WAFFLES Declaration when user:
- Explicitly requests WAFFLES or "waffle declaration"
- Asks "what might people misread into this?"
- Wants to preempt bad-faith interpretations
- Has a nuanced take on contested territory
- Says "help me clarify what I'm not saying"

## Generation Process

Given post text, produce 12-20 declarations across these dimensions:

| Category | What to identify |
|----------|------------------|
| Emotional scope | Extremes, permanence, or intensity not claimed |
| Universality | Generalizations the author isn't making |
| Policy/advocacy | Positions not being endorsed |
| Judgments | Evaluations not being rendered |
| Temporal claims | Timelines or permanence not asserted |
| Adjacent hot-takes | Related controversial positions not implied |
| Inverses | Opposite claims also not being made |
| Meta-claims | Authority or expertise not asserted |

## Output Format

```
🧇 WAFFLES DECLARATION 🦋
aka things this post doesn't say:

— [declaration 1]
— [declaration 2]
...
```

Use varied phrasing:
- "This post does not claim..."
- "The author is not saying..."
- "This is not an argument that..."
- "Nothing here suggests..."

## Quality Criteria

Declarations should be:
- **Plausible**: Things a reasonable but uncharitable reader might actually misread
- **Balanced**: Include both "sides" when touching contested territory
- **Concise**: One line each, clear and direct
- **Useful**: Genuinely clarifying, not padding

Prioritize likely misinterpretations over implausible ones. A good declaration makes the reader think "oh, I might have assumed that."
