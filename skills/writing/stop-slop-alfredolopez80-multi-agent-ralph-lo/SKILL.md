---
# VERSION: 2.43.0
name: stop-slop
description: "A skill for removing AI-generated writing patterns ('slop') from prose. Eliminates telltale signs of AI writing like filler phrases, excessive hedging, overly formal language, and mechanical sentence structures. Use when: writing content that should sound human and natural, editing AI-generated drafts, cleaning up prose for publication, or any content that needs to sound authentic rather than AI-generated. Triggers: 'stop-slop', 'remove AI tells', 'clean up prose', 'make it sound human', 'edit AI writing'."
allowed-tools: Read,Edit,Write,Bash,Glob
---

# Stop Slop

A skill for removing AI tells from prose. AI writing has patterns—predictable phrases, structures, and rhythms. Once you notice them, you see them everywhere.

## What It Catches

### Banned Phrases

**Throat-clearing openers** — Generic openings that delay the actual content:
- "Certainly!"
- "It is important to note that..."
- "It should be noted that..."
- "It is worth noting that..."
- "In today's fast-paced world..."
- "In the ever-evolving landscape of..."

**Emphasis crutches** — Overused emphasis patterns:
- "plays a crucial role"
- "is absolutely essential"
- "cannot be overstated"
- "is particularly important"

**Business jargon** — Empty corporate speak:
- "leverage the power of"
- "dive right in"
- "moving on to"
- "at the end of the day"

### Structural Clichés

**Binary contrasts** — Forced either/or framings:
- "This isn't just X, it's Y"
- "On one hand... on the other hand..."

**Dramatic fragmentation** — Unnecessary line breaks for emphasis:
- Short sentences after long ones just for effect

**Rhetorical setups** — Predictable question-answer patterns:
- "So what does this mean?"
- "The answer is..."

### Stylistic Habits

**Tripling** — Lists of three as a pattern:
- Examples, evidence, and expertise
- Fast, flexible, and affordable

**Metronomic endings** — Sentences that all end the same way

**Immediate question-answers** — Ask and answer in same paragraph

## Scoring

Rate 1-10 on each dimension:

| Dimension | Question |
|-----------|----------|
| **Directness** | Statements or announcements? |
| **Rhythm** | Varied or metronomic? |
| **Trust** | Respects reader intelligence? |
| **Authenticity** | Sounds human? |
| **Density** | Anything cuttable? |

**Below 35/50:** Revise the content.

## Process

When editing content:

1. **Scan for banned phrases** — Remove throat-clearing openers
2. **Fix structural clichés** — Break binary contrasts, reduce tripling
3. **Check rhythm** — Vary sentence length and structure
4. **Respect trust** — Don't over-explain, don't state obvious
5. **Verify authenticity** — Does it sound like a human wrote it?
6. **Trim density** — Cut anything that doesn't add value

## What to Remove

- Filler phrases and hedging
- Overused transitions (Furthermore, Moreover, Additionally)
- Artificial formality (due to the fact that, in order to)
- Redundant expressions (each and every, various different)
- Meta-commentary (As mentioned above, This demonstrates...)
- Generic openings (Certainly!, In today's fast-paced world...)

## What to Preserve

While removing slop, keep:
- Genuine technical explanations
- Actual insights and analysis
- Meaningful examples and evidence
- The author's authentic voice
- Facts and accurate information

## Anti-Goals

This skill does NOT:
- Dumb down the writing
- Remove all complexity
- Change your personal style
- Eliminate necessary explanations
- Make everything short

## Quick Reference

| AI Pattern | Fix |
|------------|-----|
| "It is important to note that" | Delete or state directly |
| "In conclusion" (as transition) | Just end or summarize |
| "Furthermore/Moreover" | Delete or use specific transition |
| "plays a crucial role" | "is important" or describe role |
| "manner in which" | "how" |
| "due to the fact that" | "because" |
| "each and every" | "each" or "every" |
| "a wide array of" | "many" |
| "As mentioned above" | Just continue |
| "This demonstrates that" | Just state what it demonstrates |

## Transformation Examples

### Example 1

**BEFORE (AI Slop):**
> "It is important to note that consistent practice plays a crucial role in skill development. Furthermore, one must consider that motivation is a key factor in maintaining this consistency. Moreover, this highlights the importance of setting realistic goals."

**AFTER (Human):**
> "Consistent practice develops skills. Motivation keeps you going, so set realistic goals."

### Example 2

**BEFORE (AI Slop):**
> "It should be noted that there are various different approaches to solving this problem. Each approach offers a unique set of advantages and disadvantages. In conclusion, the best choice depends on the specific context."

**AFTER (Human):**
> "Several approaches can solve this problem. Each has pros and cons. Pick what fits your situation."

### Example 3

**BEFORE (AI Slop):**
> "Certainly! Let's dive right in. In today's fast-paced digital landscape, businesses must leverage the power of technology to stay competitive. It's crucial to understand that digital transformation is not just a buzzword."

**AFTER (Human):**
> "Let's dive in. To stay competitive, businesses need technology. Digital transformation matters."

## Usage

**Claude Code:** This folder is a skill. Invoke `@stop-slop` when editing prose.

**Claude Projects:** Upload SKILL.md to project knowledge.

**API calls:** Include SKILL.md in your system prompt.

## Reference Files

For complete lists, see:
- `references/phrases.md` — Full banned phrases list
- `references/structures.md` — Structural patterns to avoid
- `references/examples.md` — More before/after transformations

---

Based on work by [Hardik Pandya](https://hvpandya.com/stop-slop)
