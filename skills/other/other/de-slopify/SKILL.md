---
name: de-slopify
description: "Remove telltale signs of AI-generated 'slop' writing from README files and documentation. Make your docs sound authentically human."
---

# De-Slopify — Remove AI Writing Artifacts

> **Purpose:** Make your documentation sound like it was written by a human, not an LLM.
>
> **Key Insight:** You can't do this with regex or a script—it requires manual, systematic review of each line.

---

## What is "AI Slop"?

AI slop refers to writing patterns that LLMs produce disproportionately more commonly than human writers. These patterns make text sound inauthentic and "cringe."

### Common Tells

| Pattern | Problem |
|---------|---------|
| **Emdash overuse** | LLMs love emdashes—they use them constantly—even when other punctuation works better |
| **"It's not X, it's Y"** | Formulaic contrast structure |
| **"Here's why"** | Clickbait-style lead-in |
| **"Here's why it matters:"** | Same energy |
| **"Let's dive in"** | Forced enthusiasm |
| **"In this guide, we'll..."** | Overly formal setup |
| **"It's worth noting that..."** | Unnecessary hedge |
| **"At its core..."** | Pseudo-profound opener |

---

## THE EXACT PROMPT — De-Slopify Documentation

```
I want you to read through the complete text carefully and look for any telltale signs of "AI slop" style writing; one big tell is the use of emdash. You should try to replace this with a semicolon, a comma, or just recast the sentence accordingly so it sounds good while avoiding emdash.

Also, you want to avoid certain telltale writing tropes, like sentences of the form "It's not [just] XYZ, it's ABC" or "Here's why" or "Here's why it matters:".  Basically, anything that sounds like the kind of thing an LLM would write disproportionately more commonly that a human writer and which sounds inauthentic/cringe.

And you can't do this sort of thing using regex or a script, you MUST manually read each line of the text and revise it manually in a systematic, methodical, diligent way. Use ultrathink.
```

---

## Why Manual Review is Required

The prompt explicitly states:

> "And you can't do this sort of thing using regex or a script, you MUST manually read each line of the text and revise it manually in a systematic, methodical, diligent way."

Reasons:
1. **Context matters** — Sometimes an emdash is actually the right choice
2. **Recasting sentences** — Often the fix isn't substitution but rewriting
3. **Tone consistency** — Need to maintain voice throughout
4. **Judgment calls** — Some patterns are fine in moderation

---

## Emdash Alternatives

When you encounter an emdash (—), consider:

| Original | Alternative |
|----------|-------------|
| `X—Y—Z` | `X; Y; Z` or `X, Y, Z` |
| `The tool—which is powerful—works well` | `The tool, which is powerful, works well` |
| `We built this—and it works` | `We built this, and it works` |
| `Here's the thing—it matters` | `Here's the thing: it matters` or recast entirely |

Sometimes the best fix is to split into two sentences or restructure entirely.

---

## Phrases to Eliminate or Rewrite

### "Here's why" family
- "Here's why" → Just explain why directly
- "Here's why it matters" → Explain the importance inline
- "Here's the thing" → Usually can be deleted entirely

### Contrast formulas
- "It's not X, it's Y" → "This is Y" or explain the distinction differently
- "It's not just X, it's also Y" → "This does X and Y" or similar

### Forced enthusiasm
- "Let's dive in!" → Just start
- "Let's get started!" → Just start
- "Excited to share..." → Just share it

### Pseudo-profound openers
- "At its core..." → Usually can be deleted
- "Fundamentally..." → Often unnecessary
- "In essence..." → Just say the essence

### Unnecessary hedges
- "It's worth noting that..." → Just note it
- "It's important to remember..." → Just state the fact
- "Keep in mind that..." → Often deletable

---

## Before and After Examples

### Example 1: Emdash Overuse

**Before (sloppy):**
```
This tool—which we built from scratch—handles everything automatically—from parsing to output.
```

**After (clean):**
```
This tool handles everything automatically, from parsing to output. We built it from scratch.
```

### Example 2: "Here's why" Pattern

**Before (sloppy):**
```
We chose Rust for this component. Here's why: performance matters, and Rust delivers.
```

**After (clean):**
```
We chose Rust for this component because performance matters.
```

### Example 3: Contrast Formula

**Before (sloppy):**
```
It's not just a linter—it's a complete code quality system.
```

**After (clean):**
```
This is a complete code quality system, not just a linter.
```

Or even better:
```
This complete code quality system goes beyond basic linting.
```

### Example 4: Forced Enthusiasm

**Before (sloppy):**
```
# Getting Started

Let's dive in! We're excited to help you get up and running with our amazing tool.
```

**After (clean):**
```
# Getting Started

Install the tool and run your first command in under a minute.
```

---

## When to De-Slopify

### Best Times
- Before publishing a README
- Before releasing documentation
- After AI-assisted writing sessions
- During documentation reviews

### Files to Check
- README.md
- CONTRIBUTING.md
- API documentation
- Blog posts
- Any public-facing text

---

## Integration with Workflow

### As Part of Bead Workflow

```bash
bd create "De-slopify README.md" -t docs -p 3
bd create "De-slopify API documentation" -t docs -p 3
```

### As Final Pass Before Commit

```
Now, before we commit, please read through README.md and look for any telltale signs of "AI slop" style writing...
```

---

## What NOT to Fix

Some things are fine even if they seem "AI-like":

- **Technical accuracy** — Don't sacrifice correctness for style
- **Necessary structure** — Headers, lists, etc. are fine
- **Clear explanations** — Being thorough isn't slop
- **Code examples** — Focus on prose, not code

---

## Complete Prompt Reference

### Main De-Slopify Prompt
```
I want you to read through the complete text carefully and look for any telltale signs of "AI slop" style writing; one big tell is the use of emdash. You should try to replace this with a semicolon, a comma, or just recast the sentence accordingly so it sounds good while avoiding emdash.

Also, you want to avoid certain telltale writing tropes, like sentences of the form "It's not [just] XYZ, it's ABC" or "Here's why" or "Here's why it matters:".  Basically, anything that sounds like the kind of thing an LLM would write disproportionately more commonly that a human writer and which sounds inauthentic/cringe.

And you can't do this sort of thing using regex or a script, you MUST manually read each line of the text and revise it manually in a systematic, methodical, diligent way. Use ultrathink.
```

### Quick Version (for minor touch-ups)
```
Review this text and remove any AI slop patterns: excessive emdashes, "Here's why" constructions, "It's not X, it's Y" formulas, and other LLM writing tells. Recast sentences to sound more naturally human. Use ultrathink.
```
