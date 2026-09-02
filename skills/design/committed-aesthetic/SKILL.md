---
name: committed-aesthetic
description: "How to write — and how to use — a skill that IS one aesthetic rather than a catalogue of them. A catalogue lets an agent pick, and it picks the modal option; a committed aesthetic makes it execute one thing precisely, against rules you can check. Use when a design keeps coming out competent and forgettable, when starting a new brand surface with no reference, or when authoring a house style you want executed the same way twice."
when_to_use: |
  Apply when:
  - design-advisor is starting a UI-bearing surface with NO existing system to match
  - output from ui-ux-pro-max keeps landing on "clean modern minimal"
  - you are writing a house style meant to be executed by an agent, not read by a human
  Do NOT apply when:
  - an existing product's design already governs (match it — that is anydesign's job)
  - the surface is one screen inside a system that already has a vocabulary
effort: low
allowed-tools: Read, Write, Grep, Glob
---

# A committed aesthetic beats a catalogue

## The problem this exists for

`ui-ux-pro-max` ships 84 styles, 161 palettes and 57 font pairings, and
`design-advisor` is wired to all of it. The catalogue is not the bottleneck.

The bottleneck is that **a catalogue lets a model pick, and an unconstrained pick
is the modal one.** Asked for a landing page with no brand, any model reaches for
the same safe centre: a soft gradient, a large sans heading, three rounded cards
with a left accent border, generous neutral grey. Every input in the training
distribution votes for it. Nothing in a catalogue entry saying *"Swiss minimalism
— clean, grid-based, generous whitespace"* is specific enough to override that,
because that sentence describes the safe centre too.

Compare a rule from a committed aesthetic:

> every dimension is `calc(fraction * 100vw)` against a baseline width, so one
> page at 1024px reads as a perfect scaled-down of the same page at 1920px

You can **check** that. A design either obeys it or does not. That is the whole
difference: a catalogue entry is a *label*, a committed aesthetic is a *constraint*.

## The form

A committed-aesthetic skill has five parts. The first is the one that does the work.

### 1. Transferable DNA — numbered, specific, falsifiable

Between 8 and 14 rules. Each must be checkable by someone who was not in the
room. Test every rule against this: **could two designers disagree about whether
a page obeys it?** If yes, it is a vibe, rewrite it.

| Vibe (useless) | Constraint (usable) |
|---|---|
| "thin, elegant type" | "weights 100 or 300 only, never 400+" |
| "lots of whitespace" | "~60% of any above-the-fold area is empty" |
| "restrained motion" | "no shadows, no gradients, no bounce; one shadow exists in the system, on toasts" |
| "technical feel" | "product codes use en-dash U+2013, never hyphen" |
| "dark and dense" | "five surface steps, each ~5% apart; depth is a surface step, never a shadow" |

### 2. What this does NOT do — the IP boundary, as a table

An aesthetic is *inspired-by, not cloned*. Name the specific assets that belong to
whoever you are borrowing from — wordmark, icon set, information architecture,
product names, copy — and for each give the reason and what to do instead. This
is not a legal disclaimer at the bottom; it is a working table an agent reads
while building, and it is the difference between an homage and a trademark
problem. Where the source is a real company, default to inspired-but-distinct and
ask before taking the clone path.

### 3. A component library that runs

One HTML file the agent can open, with every component rendered and its own CSS
inline, copy-pasteable. A token table in prose is read and paraphrased; a
rendered gallery is copied exactly. This is why the form works at all.

### 4. Templates for the signature patterns

The two or three moves nobody would reconstruct from the DNA list alone — the
navigation shape, the section header, the hero. With `swap these for your own
brand` marked in comments.

### 5. Reference captures, marked "study, do not pixel-copy"

Screenshots are for understanding the patterns. Building FROM a screenshot rather
than from the rules produces a bad tracing of one page instead of a design in the
family.

## The banned list, and why we needed one

`ui-ux-pro-max`'s anti-pattern tables are about accessibility, touch targets and
performance. They are good and they are not about taste. Nothing in this repository
told an agent what *cliché* looks like, so the only defence against slop was one
sentence in `design-advisor`: "no generic clean modern minimal filler".

Banned by default on any surface without an existing system that calls for them:

- **A gradient as the page ground.** Especially purple-to-blue, especially at 135°.
- **The card triplet**: three equal cards, rounded corners, a coloured left border,
  an icon in a tinted circle.
- **Inter, Roboto, Arial, Open Sans, Fraunces, Poppins** as the display face. Not
  because they are bad — because they are the default vote.
- **Emoji as iconography.** Draw the icon. (Emoji are fine if the brand uses them.)
- **The hero that describes a category rather than taking a position.** "The modern
  platform for X" is the sentence a model writes when it has not been told what to
  believe.
- **Glassmorphism, neumorphism, and a mesh-gradient blob** unless the brief names
  one of them.
- **Symmetric three-column feature grids** as the default second section.

A banned list is not a style. It removes the centre so a choice has to be made.

## Using one

1. If a system already governs, this skill does not apply — match what exists.
2. If nothing governs and **you can ask**: offer 2–4 genuinely different
   directions, each an axis you can name, before building. Not five shades of one
   aesthetic — that is not a choice.
3. If nothing governs and **you cannot ask**: commit to ONE, state the assumption
   in a line at handover, and put 1–2 low-fi alternates beside the deliverable,
   never instead of it.
4. Once a direction is chosen, load its committed-aesthetic skill and execute the
   DNA rules literally. Cite the rule number for each choice, the way
   `design-advisor` already cites a ui-ux-pro-max rule.

## Instances in this repository

- [`skills/aesthetic-instrument/SKILL.md`](../aesthetic-instrument/SKILL.md) —
  great_cto's own, measured from the board and greatcto.systems rather than
  designed for this document.

Related: [`skills/ui-ux-pro-max/SKILL.md`](../ui-ux-pro-max/SKILL.md) is the
catalogue this stands beside, not a replacement for it — the catalogue is where
you look when you need to KNOW something; this is what you load once you have
DECIDED something.
