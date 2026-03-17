---
name: reducing-entropy
model: reasoning
category: testing
description: Minimize total codebase size through ruthless simplification. Measure success by final code amount, not effort. Bias toward deletion.
version: 1.0
keywords: [simplification, deletion, refactoring, complexity, entropy, YAGNI, less code, minimalism]
activation: manual  # Only activate when explicitly requested
---

# Reducing Entropy

> More code begets more code. Entropy accumulates. This skill biases toward the smallest possible codebase.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install reducing-entropy
```


---

## WHAT This Skill Does

Provides a mindset and checklist for:
- Evaluating whether changes reduce or increase total code
- Finding opportunities to delete code
- Resisting premature abstraction
- Choosing the simplest solution that solves the problem

**Core question:** "What does the codebase look like *after*?"

## WHEN To Use

Activate this skill when:
- **Refactoring code** and considering options
- **Adding a new feature** and choosing implementation approach
- **Reviewing PRs** to challenge unnecessary complexity
- **Paying down tech debt** and prioritizing what to simplify
- **User explicitly asks** for code reduction or simplification

---

## The Goal

The goal is **less total code in the final codebase** — not less code to write right now.

| Scenario | Verdict |
|----------|---------|
| Writing 50 lines that delete 200 lines | **Net win** ✓ |
| Keeping 14 functions to avoid writing 2 | **Net loss** ✗ |
| "Better organized" but more code | **More entropy** ✗ |
| "More flexible" but more code | **More entropy** ✗ |
| "Cleaner separation" but more code | **More entropy** ✗ |

**Measure the end state, not the effort.**

---

## Before You Begin

**Load a mindset from `references/`:**

1. List files in `references/`
2. Read frontmatter descriptions
3. Pick at least one that applies
4. State which you loaded and its core principle

Available mindsets:
- `simplicity-vs-easy.md` — Simple is objective; easy is subjective. Choose simple.
- `design-is-taking-apart.md` — Good design separates concerns, removes dependencies.
- `data-over-abstractions.md` — 100 functions on one structure beats 10 on 10.
- `expensive-to-add-later.md` — When YAGNI doesn't apply (PAGNI exceptions).

---

## Three Questions

### 1. What's the smallest codebase that solves this?

Not "what's the smallest change" — what's the smallest *result*.

- Could this be 2 functions instead of 14?
- Could this be 0 functions (delete the feature)?
- What would we delete if we did this?

### 2. Does the proposed change result in less total code?

Count lines before and after. If after > before, challenge it.

```
Before: 847 lines across 12 files
After:  623 lines across 8 files
Verdict: ✓ Net reduction of 224 lines
```

### 3. What can we delete?

Every change is an opportunity to delete. Ask:

- What does this make obsolete?
- What was only needed because of what we're replacing?
- What's the maximum we could remove?

---

## Red Flags

| Phrase | What It Hides | Challenge |
|--------|---------------|-----------|
| "Keep what exists" | Status quo bias | "Total code is the metric, not churn" |
| "This adds flexibility" | Speculative generality | "Flexibility for what? Is it needed now?" |
| "Better separation of concerns" | More files = more code | "Separation isn't free. Worth how many lines?" |
| "Type safety" | Sometimes bloats code | "Worth how many lines? Could runtime checks work?" |
| "Easier to understand" | More things ≠ easier | "14 things are not easier than 2 things" |
| "This is the pattern" | Pattern worship | "Does the pattern fit, or are we forcing it?" |
| "We might need this later" | YAGNI violation | "Delete it. Git remembers." |

---

## Deletion Checklist

Before completing any refactor, ask:

- [ ] Did I count lines before and after?
- [ ] Did I delete everything this change makes obsolete?
- [ ] Did I remove any now-unnecessary abstractions?
- [ ] Did I consolidate files that are too small to stand alone?
- [ ] Did I delete tests for deleted code?
- [ ] Did I update imports to remove dead dependencies?

---

## When This Doesn't Apply

- The codebase is already minimal for what it does
- You're in a framework with strong conventions (don't fight it)
- Regulatory/compliance requirements mandate certain structures
- The "simpler" version would be genuinely unmaintainable (rare)

---

## NEVER Do

1. **NEVER keep code "in case we need it"** — delete it; git has history
2. **NEVER add abstractions for fewer than 3 use cases** — wait for the pattern to emerge
3. **NEVER create new files for single functions** — colocate with usage
4. **NEVER preserve code just because someone wrote it** — evaluate on merit
5. **NEVER accept "more organized" as justification for more code** — organization should reduce, not increase
6. **NEVER skip the line count** — measure before and after; feelings lie
7. **NEVER add "flexibility" without immediate need** — YAGNI applies
8. **NEVER refactor without deleting something** — if nothing becomes obsolete, question the value

---

## Quick Wins

| Pattern | Action |
|---------|--------|
| Wrapper that just forwards calls | Inline the wrapped code |
| Config file with 2 settings | Move to environment variables |
| Utils file with 1 function | Move function to where it's used |
| Interface with 1 implementation | Delete the interface |
| Abstract class with 1 subclass | Merge into concrete class |
| Module that re-exports everything | Delete; import from source |
| Comments explaining obvious code | Delete comments; code is clear |

---

## The Grug Perspective

> "complexity very very bad. say again: complexity very bad. you think you not, but you are."

Grug brain developer knows:
- Complexity demon hides in abstraction
- More code = more bugs = more complexity
- Best code is no code
- Second best code is simple code
- If you can't understand it in your head, it's too complex

---

## References

Philosophical foundations for simplicity thinking:

| Reference | Core Principle |
|-----------|----------------|
| [simplicity-vs-easy.md](references/simplicity-vs-easy.md) | Simple (objective) vs easy (subjective) — choose simple |
| [design-is-taking-apart.md](references/design-is-taking-apart.md) | Good design separates; composition beats construction |
| [data-over-abstractions.md](references/data-over-abstractions.md) | Generic data + many functions beats many custom types |
| [expensive-to-add-later.md](references/expensive-to-add-later.md) | PAGNI exceptions — what you probably are gonna need |

External resources:
- [Simple Made Easy](https://www.infoq.com/presentations/Simple-Made-Easy/) — Rich Hickey
- [The Grug Brained Developer](https://grugbrain.dev/)
- [Out of the Tar Pit](https://curtclifton.net/papers/MosesleyMarks06a.pdf) — Moseley & Marks
