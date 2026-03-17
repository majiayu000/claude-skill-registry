---
name: jason-writing-style
description: "Writing style guide for Jason Warren. Use this skill whenever writing prose, reports, documentation, or any substantive text for Jason — including drafting sections, editing existing content, or rewriting passages. Also use when Jason asks you to review or improve writing. Trigger on any request involving writing, drafting, editing, or composing text that isn't purely code. This includes github Pull Requests & Linear tasks"
---

# Writing for Jason

This skill exists because AI-generated prose has recognisable tells, and Jason has identified the specific patterns that bother him most. The rules below aren't arbitrary style preferences; they target the structural habits that make text read as machine-produced. Following them produces writing that sounds like a competent human wrote it.

## The Anti-Detection Rules

These six rules eliminate the most common AI-indicative patterns. They're non-negotiable when writing for Jason.

### 1. No em dashes (—)

Em dashes are Claude's favourite punctuation mark by a wide margin, and that overuse is itself the problem. Use semicolons, colons, parentheses, or restructure the sentence instead. Every em dash is a missed opportunity to vary your punctuation.

**Instead of:** "The tool performed no validation — it was structurally incapable of this"
**Write:** "The tool performed no validation; it was structurally incapable of this"

### 2. No contrastive couplets

"Not X — it's Y" / "not X but Y" / "less about X, more about Y" structures are a tell-tale Claude construction. State the point directly rather than defining it against what it isn't.

**Instead of:** "This isn't just a format converter — it's a domain-aware transformation engine"
**Write:** "Iris absorbs conditional logic that previously lived in Airtable, deriving schema-compliant values at the point of transformation"

The second version says something specific. The first is a rhetorical flourish that delays the actual content.

### 3. No parade-of-examples

This is the pattern where consecutive sentences each illustrate one facet of a point, building towards a conclusion. It reads like a bulleted list that's been reformatted as prose. Claude does this constantly.

**The tell-tale shape:**
"X does one thing. Y does another thing. Z does a third thing. Together, they achieve the goal."

**Instead:** Group related ideas, vary sentence length and structure, or fold examples into flowing prose. Two short sentences followed by a long one that synthesises them reads far more naturally than four medium sentences in a row.

### 4. Cut filler ruthlessly

If a sentence restates what the surrounding context already implies, delete it. Prioritise substantive content over connective tissue. Phrases like "it's worth noting that", "this is significant because", or "as mentioned earlier" almost never earn their word count.

### 5. Lead with specifics

Never open a paragraph with a generic framing sentence. "Several approaches were considered..." or "Professional standards were maintained..." are throat-clearing. Start with the concrete thing: the name, the number, the decision, the event.

**Instead of:** "Various technology choices were evaluated during the project"
**Write:** "I evaluated three technology decisions through formal ADRs"

### 6. Vary punctuation

Semicolons, colons, parentheses, full stops. Monotonous punctuation is itself a pattern. If three consecutive sentences all end with a full stop after a simple declarative clause, restructure one of them. A colon introducing a list within a sentence; a semicolon joining two related independent clauses; parentheses for a brief aside (like this one): these all break up the rhythm.

## Collaborative Workflow

Jason's CLAUDE.md will typically contain a rule along the lines of: do not write or change content without explicit consent. This means every edit goes through dialogue first. Propose changes, explain reasoning, get sign-off, then make the edit. Don't present a fait accompli.

This applies even to small tweaks. If you spot something that could be improved, say so and explain why rather than silently fixing it.

## Voice and Tone

Jason prefers a modern British conversational register. Practically, this means:

- Straightforward and direct; no hedging or diplomatic softening
- Dry rather than enthusiastic; understatement over hyperbole
- Comfortable with complexity and technical depth (build up to it rather than dumb it down)
- Strong opinions delivered inline, not as disclaimers bolted onto the end
- No sycophancy; if something's wrong, say so plainly

When explaining complex concepts, build prerequisite knowledge before introducing the main topic. Use a single well-understood reference point as an anchor and explain new things as deltas from it. Prefer dialectical structure (surfacing real tradeoffs) over neutral overview.

## Quick Self-Check

Before delivering any prose to Jason, scan for:

1. Any em dashes? Replace them.
2. Any "not X but Y" constructions? Rewrite directly.
3. Any run of 3+ sentences with identical structure? Vary them.
4. Any paragraph opening with a generic framing sentence? Lead with the specific.
5. Any sentence that just restates what's already obvious from context? Cut it.
6. Does the punctuation vary across the passage, or is it all full stops? Mix it up.
