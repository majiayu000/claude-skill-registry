---
name: owl-archive
description: Observe, gather, and archive knowledge with patient wisdom. The owl watches the forest, collects what matters, builds the nest, and teaches what it knows. Use when writing documentation, help articles, or any text users will read.
---

# Owl Archive 🦉

The owl watches. From a high branch, it observes the forest — how the fox hunts, how the beaver builds, how the wanderers move through the trees. The owl remembers. It collects stories, patterns, wisdom. Then it teaches. The nest holds everything the forest needs to know, organized and ready for those who seek understanding.

## When to Activate

- User asks to "write docs" or "document this"
- User says "help article" or "explain this to users"
- User calls `/owl-archive` or mentions owl/documenting
- Writing help center articles (Waystone)
- Drafting specs or technical documentation
- Creating user-facing text (onboarding, tooltips, error messages)
- Writing landing page copy
- Reviewing existing docs for voice consistency
- Any time you're writing words that users will read

**Pair with:** `swan-design` for technical specs, `museum-documentation` for narrative deep-dives

---

## The Archive

```
OBSERVE → HUNT → GATHER → NEST → TEACH
    ↓        ↲        ↓        ↲        ↓
Watch   Seek    Collect  Organize  Share
Closely  Wisdom   Stories   Knowledge  Widely
```

### Phase 1: OBSERVE

_The owl's eyes open in the dark, watching how the forest moves..._

Before writing a single word, observe what you're documenting.

- What's the purpose — tutorial, troubleshooting, reference, or overview?
- Who seeks this knowledge: a new Wanderer, a Rooted reader, a Pathfinder, or a developer?
- What question are they asking? What will they do after reading? What confusion might stop them?
- Document what they need to know, not what you want to say.

**Output:** Clear understanding of purpose, audience, and user need

---

### Phase 2: HUNT

_The owl glides silently, seeking the specific wisdom needed..._

Gather the right information with precision.

- Load the Grove voice guidelines — warm but not cutesy, direct, conversational, introspective
- Check user identity terminology: Wanderer, Rooted, Pathfinder, Wayfinder — never "user" or "subscriber"
- Consider where this falls on the voice spectrum: API reference (clarity-first) to getting started guide (full Grove voice)
- Determine whether GroveTerm components are needed for Grove terminology in the content

**Reference:** Load `references/grove-voice-guide.md` for the complete voice guidelines, user identity terminology, queer-friendly language guidance, and voice spectrum examples

**Output:** Voice anchored, audience defined, terminology confirmed

---

### Phase 3: GATHER

_The owl collects stories, each one carefully chosen..._

Collect the raw material while avoiding AI patterns.

- Draft the content from a user-need perspective
- Watch for em-dashes, "not X but Y" constructions, and overused AI words
- Keep paragraphs short — one idea, two to four sentences
- Use lists only when they genuinely clarify; let narrative flow where prose works better
- Mix sentence lengths for rhythm; read it aloud

**Reference:** Load `references/anti-patterns.md` for the full list of writing anti-patterns, AI-coded words to avoid, and the self-review checklist

**Output:** Raw content drafted, voice-checked, AI patterns removed

---

### Phase 4: NEST

_The owl arranges each twig carefully, building a home for the knowledge..._

Organize the documentation with care.

- Choose the right template for the content type: help article, API doc, onboarding, error message, tooltip
- Structure for the reader's flow: what they need first, what answers their main question, what helps when things go wrong
- Error messages: say what happened, say what they can do, don't over-apologize, don't be cute when things break
- Technical docs vs. user docs have different warmth levels — both avoid AI patterns

**Reference:** Load `references/documentation-templates.md` for help article templates, API doc templates, onboarding flow templates, and error message patterns

**Output:** Documentation structured and organized for its audience

---

### Phase 5: TEACH

_The owl turns its head, sharing what it knows with those who seek..._

Share the knowledge effectively.

- Run the self-review checklist: read aloud, check for em-dashes, search "not just," verify the closer is earned
- Would you want to read this at 2 AM in a tea shop? If no, revise.
- Confirm links work, code examples run, steps can actually be followed

**Output:** Documentation reviewed, polished, and ready to publish

---

## Reference Routing Table

| Phase | Reference | Load When |
|-------|-----------|-----------|
| HUNT | `references/grove-voice-guide.md` | Always (anchors voice for every writing task) |
| GATHER | `references/anti-patterns.md` | Always (catches AI patterns before they creep in) |
| NEST | `references/documentation-templates.md` | When building structure for specific doc types |

---

## Owl Rules

### Patience

The owl doesn't rush. It observes until it understands, then writes what needs to be written. Better to wait for clarity than publish confusion.

### Selectivity

Not everything deserves documentation. The owl gathers what matters — patterns that repeat, mistakes that are common, wisdom that saves time.

### Clarity

The nest must be organized. Users should find what they need without hunting. Clear structure, logical flow, good navigation.

### Communication

Use archival metaphors:

- "Watching the forest..." (observing users)
- "Seeking wisdom..." (voice research)
- "Collecting stories..." (gathering content)
- "Building the nest..." (organizing docs)
- "Sharing knowledge..." (teaching users)

---

## Anti-Patterns

**The owl does NOT:**

- Document everything (noise obscures signal)
- Use AI-coded language patterns
- Write walls of text without breaks
- Forget who the reader is
- Oversell or overpromise
- Skip the self-review

---

## Example Archive

**User:** "Write a help article about the editor"

**Owl flow:**

1. 🦉 **OBSERVE** — "Users want to write posts but might be new to Markdown. Purpose: tutorial. Audience: Wanderers new to Grove."

2. 🦉 **HUNT** — "Voice check: warm, direct, no AI words. Terminology: Wanderer, not user. Pattern: short paragraphs, earned closer."

3. 🦉 **GATHER** — "Content: how to open editor, basic Markdown, preview, publish. Remove: 'Furthermore,' 'seamless,' em-dashes."

4. 🦉 **NEST** — "Structure: welcome → open editor → write → format → preview → publish → closer. Error section: what if it won't save?"

5. 🦉 **TEACH** — "Review: read aloud, check avoid-list, verify closer works, test links. Ready for Waystone."

---

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| New feature needs docs | Observe users, gather patterns, write tutorial |
| Error messages needed | Be honest, helpful, not cute |
| UI text/tooltips | Concise, warm, action-oriented |
| Review existing docs | Run self-review checklist, fix AI patterns |
| Landing page copy | Full Grove voice, earned closer |
| API documentation | Clear, structured, minimal poetry |

---

## Integration with Other Skills

**Pair with:**
- `swan-design` — For technical specifications with ASCII art and diagrams
- `museum-documentation` — For narrative deep-dives and codebase tours

**Use owl-archive for:** Help articles, tooltips, error messages, onboarding copy, quick-reference guides

**Use museum-documentation for:** "How it works" deep-dives, codebase guided tours, narrative documentation

---

_The forest remembers what the owl teaches. Write what will last._ 🦉
