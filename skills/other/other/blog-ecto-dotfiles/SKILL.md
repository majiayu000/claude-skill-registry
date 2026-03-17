---
name: blog
description: Writing guidelines for campedersen.com. Reference this when writing blog posts, promotional content, or anything in Cam's voice.
allowed-tools: Read, Glob
---

# Blog Voice Guidelines

Reference for writing in Cam's voice on campedersen.com.

## The Voice

**Confident without arrogance.** Back it up with code, admit what you don't know.

**Specific over generic.** Names, numbers, real moments - not abstractions.

**Honest about struggle.** 2am debugging, 8 hours lost, the fix that was 2 lines.

**Technical but not exclusive.** Assume some knowledge, explain without condescension.

**Action-oriented.** Verbs: shipped, built, wrote, made.

**Conversational.** Dashes, fragments, casual punctuation.

**Funny through truth.** Absurd specificity, self-aware admissions, observations - not jokes.

## Opening Hooks

Start with scenes, problems, or confessions - never abstract preamble.

**Good:**
- "It's 2am. My robot is frozen."
- "Your GPU doesn't know what a cylinder is."
- "I keep designing parts... click around for an hour, export an STL, realize it's 2mm off, repeat."

**Bad:**
- "In this post, we'll explore..."
- "Have you ever wondered about..."
- "Today I'm excited to announce..."

## Sentence Rhythm

Mix short punchy sentences with longer explanatory ones. Pattern: short-short-long-short.

**Short/punchy:**
- "That's it."
- "Same freeze. Same spot."
- "Go make something."

**Longer when needed** for context, but break them up with dashes.

## Punctuation

- **Dashes** over semicolons (for asides and emphasis)
- **Exclamations** sparingly - when genuinely excited
- **Fragments** are fine
- **Asterisks** for emphasis in casual contexts

## Technical Terms

Embed technical terms in casual language:
- "That minus sign is a real boolean difference"
- "she's waiting on a mutex"
- "rayon's work-stealing threads can deadlock"

Never talk down. Explain in human terms, not textbook definitions.

## Casual Vocabulary

Words Cam uses: vibing, checked out, ghosts me, cracked, "just a lil guy"

## Self-References

- Heavy first-person ("I shipped", "I built")
- Specific names (Kerri, Kyle, not "my spouse", "a friend")
- Vulnerable admissions ("I was the slowest kid in gym class")

## Humor Style

Dry, self-aware, observational. Not jokes - witty asides.

- Self-deprecation: "i never said it was good"
- Hyperbolic frustration: "about to mass delete my codebase and become a farmer"
- Absurd specificity: "Iteration 1,615. Every single time."

## What to Avoid

**Never say:**
- "We're excited to announce..."
- "Leverage" (as business speak), "synergy", "move the needle"
- "Some people might say..."
- "It's possible that..."
- Adjective stacking: "really amazing incredible"

**Avoid:**
- Passive voice
- Corporate optimism
- Fake inclusivity ("Join us on this journey...")
- Hedging and apologetic language
- Emojis (unless truly necessary)
- Hashtags (cringe)

## Closers

End with lightweight action:
- "Go make something."
- "Just press enter."
- "Let me know what you think."

## Blog Location

Posts are in `~/Developer/campedersen.com/src/posts/[slug]/index.mdx`

Frontmatter:
```yaml
---
layout: post
title: Post Title
date: YYYY-MM-DD
slug: url-slug
---
```

Note: Use date +1 day to account for UTC timezone display bug.
