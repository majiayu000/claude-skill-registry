# Whitespace Mapping — CompetitorNames Reference

How to identify and validate naming whitespace in a competitive landscape.

---

## The Whitespace Matrix

After classifying all competitor names, plot them on two axes:

**X-axis:** Style (Descriptive → Invented → Real word → Concept/Metaphor)
**Y-axis:** Phonetic energy (Soft/warm → Hard/technical)

Clusters = saturation. Empty quadrants = whitespace.

Example for a project management category:
```
                    HARD/TECHNICAL
                         │
    Invented             │        Modified real
    (saturated)          │        (moderate)
    Notion, Height,      │        Stripe-like,
    Coda                 │        Loom-like
                         │
─────────────────────────┼─────────────────────────
                         │
    Descriptive          │        Concept/Metaphor  ← WHITESPACE
    (very saturated)     │        (0-1 competitors)
    TaskFlow,            │        Basecamp is alone
    ProjectHub           │        here
                         │
                    SOFT/WARM
```

---

## Whitespace Validation Tests

Not all whitespace is good whitespace. Before recommending a pattern, run three tests:

**Test 1 — Category fit**
Would a name using this pattern be taken seriously in this category?
- Geographic names in B2B SaaS: questionable
- Latin roots in consumer wellness: works (Lumora, Forma)
- Hard technical names in consumer mental health: fails (wrong energy)

**Test 2 — Audience recognition**
Would the target audience recognize this as a legitimate brand in the space?
- Developer tools can use ultra-short cryptic names (Bun, Zed, Nx) — devs read these as deliberate
- Enterprise B2B cannot use ultra-short names — reads as unfinished
- Consumer apps need warm phonetics — hard consonant openers create friction

**Test 3 — Differentiation value**
How much does this whitespace actually differentiate?
- Style whitespace (nobody uses real-word-out-of-context): HIGH differentiation value
- Phonetic whitespace (nobody uses hard openers): MEDIUM value — subtle
- Length whitespace (nobody uses ultra-short): HIGH if category allows, LOW if it doesn't

---

## Saturation Thresholds

| Competitors using pattern | Saturation level | Action |
|--------------------------|-----------------|--------|
| 0 | Whitespace | Explore — but validate first |
| 1 | Low | Strong opportunity |
| 2-3 | Moderate | Viable with exceptional execution |
| 4-5 | High | Avoid unless execution is clearly superior |
| 6+ or majority | Dominant convention | Breaking it = risk + reward. Following it = invisible. |

---

## Breaking Dominant Convention

When the entire market uses one pattern, breaking it is both the riskiest and most differentiating move.

**When to break convention:**
- The dominant pattern is dated (everyone uses -ify, nobody has broken out yet)
- The brand has the budget to redefine the category's naming standard
- The target audience is sophisticated enough to recognize the deliberate break

**When to follow convention:**
- The convention exists for good reason (trust, category recognition)
- The brand is early-stage with limited marketing budget
- The break would create confusion rather than differentiation

**Real example:** In project management, most tools use clean invented words (Notion, Linear). Basecamp broke convention with a geographic/metaphor name. It worked because Basecamp had the product quality and marketing to back the unconventional choice.

---

## Cross-Category Whitespace

Sometimes the best naming inspiration comes from adjacent categories.

**Process:**
1. Identify what naming conventions are dominant in the user's category
2. Look at 3 adjacent categories for naming patterns that haven't crossed over
3. Ask: would that pattern work here? Why hasn't it been used?

**Example:**
- Fintech names (Stripe, Brex, Ramp, Fey) use hard, sharp, confident phonetics
- Project management hasn't borrowed this energy
- A project management tool with fintech-style naming (short, hard consonants, premium feel) would stand out

**Cross-category patterns to watch:**
| Source category | Dominant pattern | Potential targets |
|----------------|-----------------|-------------------|
| Fintech | Hard consonants, sharp, 4-6 chars | DevTools, B2B SaaS |
| Luxury fashion | Rare real words, French-adjacent | Premium consumer apps |
| CLI/DevTools | Ultra-short, lowercase, cryptic | Developer-adjacent B2B |
| Consumer AI | Warm, vowel-ending, approachable | HR tech, wellness, education |
| Open source | Clever references, wordplay | Indie SaaS, community tools |

---

## Naming Brief Template

Produced at the end of whitespace mapping. Fed directly to DomainForge.

```
COMPETITIVE NAMING BRIEF — [Category]

SATURATED (hard constraint — avoid):
- [Pattern]: used by [X/Y] competitors
- [Pattern]: used by [X/Y] competitors

MODERATE (avoid unless exceptional):
- [Pattern]: used by [X/Y] competitors

OPEN (explore first):
- [Pattern]: only 1 competitor — [name]
- [Pattern]: 0 competitors — pure whitespace

WHITESPACE OPPORTUNITY:
Primary: [pattern] — [why it works for this category]
Secondary: [pattern] — [validation notes]

PHONETIC TARGET:
[Hard/soft] consonants, [length range], ends in [X]
Reason: [how this differentiates from the competitive cluster]

DIFFERENTIATION REQUIREMENT:
Must not sound like: [specific competitors]
Must signal: [positioning/archetype]
Must avoid: [specific patterns/suffixes]
```
