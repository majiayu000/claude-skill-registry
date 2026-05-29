---
name: format-design
description: "How to design formats that succeed — simplicity, community, timing"
license: MIT
tier: 1
protocol: FORMAT-DESIGN
allowed-tools:
  - read_file
  - write_file
origin: "Anil Dash — 'How Markdown Took Over the World' (2025)"
lineage:
  - "Richard Gabriel — 'Worse is Better' (1989)"
  - "Jon Postel — Robustness Principle (1980)"
  - "John Gruber — Markdown (2004)"
  - "Anil Dash — 'How Markdown Took Over the World' (2025)"
related: [markdown, yaml-jazz, plain-text, postel]
tags: [moollm, philosophy, design, standards, worse-is-better]
---

# Format Design

> *"Smart people think of good things that are crazy enough that they just might work, and then they give them away, over and over, until they slowly take over the world."*
> — Anil Dash

---

## What Is It?

**Format Design** is the art of creating data formats, protocols, and conventions that actually get adopted. It's not about technical superiority — it's about fit, timing, and community.

Markdown beat Textile. JSON beat XML. RSS survived. Why?

---

## The 10 Reasons Markdown Won

From Anil Dash's "[How Markdown Took Over the World](https://anildash.com/2025/01/09/how-markdown-took-over-the-world/)" (January 2025):

### 1. Had a Great Brand

> *"'Markdown' as a name is clever as hell. Get it — it's not markup, it's markdown."*

- **Memorable** — Sticks in the mind
- **Self-explanatory** — Name implies purpose
- **Clever** — Rewards understanding

**MOOLLM parallel:** YAML Jazz, SOUL-CHAT, K-lines — memorable names that reward understanding.

### 2. Solved a Real Problem

> *"Millions of people were encountering the idea that it was too difficult or inconvenient to write out full HTML by hand."*

Not abstract improvement. A specific, felt problem.

**Test:** Can you describe the pain point in one sentence? Can users?

### 3. Built on Existing Behaviors

> *"The format is based on the ways people had been adding emphasis and formatting to their text for years or even decades."*

People already used `*asterisks*` for emphasis in email. Markdown just formalized it.

**Principle:** Don't invent new behaviors. Codify existing ones.

### 4. Mirrored RSS in Its Origin

> *"Both were spearheaded by a smart technologist who was also more than a little stubborn."*

A champion who believed, advocated, and refined. Community built around a person.

**Requirement:** Someone must care deeply enough to keep pushing.

### 5. Community Ready to Help

> *"Markdown was part of a community that could build on it right from the start."*

Prior art (Textile), beta testers (Aaron Swartz), early adopters (bloggers).

**Principle:** No format succeeds alone. Build with others.

### 6. Had the Right Flavor for Every Context

> *"Various communities that were implementing Markdown could add their own 'flavors' as they needed."*

CommonMark for standardization. GitHub-Flavored for tables. Obsidian for wikilinks.

**Principle:** Core should be simple. Extensions should be possible.

### 7. Released at a Time of Behavior Change

> *"You can get people to change their behaviors when they're using a new tool."*

Blogging was new in 2004. People were already learning new habits.

**Timing matters:** Launch during transitions (new platforms, new tools, new eras).

### 8. Came at the Cusp of the "Build Tool Era"

> *"Markdown is a raw material that has to be transformed into HTML, it perfectly fit this new workflow."*

Build pipelines became standard. Markdown fit the compile-to-output model.

**Principle:** Align with emerging workflows, not legacy ones.

### 9. Worked with "View Source"

> *"It only takes one glimpse of a source Markdown file for anyone to understand how they might make a similar file of their own."*

Inspectable. Learnable by example. No teaching required.

**Test:** Can someone learn your format by looking at one example?

### 10. Not Encumbered by IP

> *"There are no legal restrictions around Markdown. Nobody's been afraid to use the format."*

No patents. No licenses. No approval needed.

**Principle:** Generosity enables adoption. Give it away.

---

## The "Worse is Better" Principle

Richard Gabriel (1989):

> *"Simplicity is the most important consideration in a design."*

### The Two Philosophies

| MIT/Stanford ("The Right Thing") | New Jersey ("Worse is Better") |
|----------------------------------|--------------------------------|
| Correctness is paramount | Simplicity is paramount |
| Consistency matters | Interface should be simple |
| Completeness required | 80% solution acceptable |
| May sacrifice simplicity | May sacrifice correctness |

### Why "Worse" Wins

The simpler thing:
- Gets implemented faster
- Gets adopted more easily
- Gets modified more readily
- Survives longer

**Examples:**
- Markdown beat Textile (simpler, less precise)
- JSON beat XML (simpler, less expressive)
- JavaScript beat Java in browsers (simpler, less typed)
- Unix beat Multics (simpler, less secure)

### The Lesson

> *"If you're using ALL of C++ in your projects you're 'doing it wrong.' It is not a well-designed language."*
> — @calmbonsai, Hacker News

Complex formats that aren't fully used are worse than simple formats fully used.

---

## Postel's Law in Format Design

> *"Be liberal in what you accept, and conservative in what you send."*

### For Parsers

Accept:
- Variant spellings
- Missing optional fields
- Extra whitespace
- Unknown extensions

### For Generators

Output:
- Canonical form
- Complete required fields
- Minimal complexity
- Maximum compatibility

---

## The Superset Pattern

From HN:

> *"CommonMark Markdown is a rough superset of HTML, like how YAML is a superset of JSON."*

Successful formats often nest:
- Markdown ⊃ HTML
- YAML ⊃ JSON
- JSX ⊃ JavaScript

**Benefit:** Easy migration path from simpler format.

---

## Case Studies

### Markdown (2004) — Won

| Factor | Score |
|--------|-------|
| Brand | ✅ Clever name |
| Problem | ✅ HTML too verbose |
| Existing behavior | ✅ Email conventions |
| Champion | ✅ John Gruber |
| Community | ✅ Bloggers |
| Timing | ✅ Blog era |
| Simple | ✅ 10 minute learning curve |
| Inspectable | ✅ Raw = readable |
| Free | ✅ No restrictions |

### Textile (2003) — Lost

| Factor | Score |
|--------|-------|
| Brand | ❌ Obscure name |
| Problem | ✅ Same as Markdown |
| Existing behavior | ⚠️ Some |
| Champion | ⚠️ Dean Allen (less visible) |
| Community | ⚠️ Smaller |
| Timing | ✅ Same era |
| Simple | ⚠️ Slightly more complex |
| Inspectable | ✅ Yes |
| Free | ✅ Yes |

### XML (1998) → JSON (2002)

| | XML | JSON |
|--|-----|------|
| Verbosity | High | Low |
| Types | Complex | Simple |
| Parsing | Hard | Easy |
| Learning | Weeks | Hours |
| Adoption | Declined | Dominant |

---

## Designing for MOOLLM

When creating new formats (skill cards, room files, etc.):

### Checklist

- [ ] **Name** — Memorable? Self-explanatory?
- [ ] **Problem** — Clear, specific pain point?
- [ ] **Existing behavior** — Building on something familiar?
- [ ] **Community** — Who will help?
- [ ] **Simplicity** — Can you remove more?
- [ ] **Inspectable** — Learnable by example?
- [ ] **Free** — No restrictions?

### Format Smell Tests

**Red Flags:**
- Requires documentation to understand examples
- Has more than 5 required fields
- Uses abbreviations or codes
- Needs special tools to view
- Includes binary components

**Green Flags:**
- One example teaches the format
- Readable without rendering
- Extensible without breaking
- Works with standard tools

---

## The Community Point

From Anil:

> *"The people who make the real Internet and the real innovations also don't look for ways to hurt the world around them, or the people around them."*

Formats succeed when:
- Created to solve the creator's own problem
- Shared freely for others' benefit
- Refined through feedback
- Not used to extract rent

**Generosity scales. Greed doesn't.**

---

## Dovetails With

- [markdown/](../markdown/) — Case study in success
- [yaml-jazz/](../yaml-jazz/) — MOOLLM's data format
- [plain-text/](../plain-text/) — The substrate
- [postel/](../postel/) — Liberal parsing
- [k-lines/](../k-lines/) — K-lines (symbolic activators)

---

## Protocol Symbol

```
FORMAT-DESIGN
```

Invoke when: Designing new formats, evaluating existing ones, choosing between options.

---

## The Bottom Line

> *"Nearly every bit of the high-tech world, from the most cutting-edge AI systems at the biggest companies, to the casual scraps of code cobbled together by college students, is annotated and described by the same, simple plain text format."*

That format wasn't designed by a committee. It was created by one person to solve their own problem, tested by a teenager, and given away for free.

**Design like that.**
