---
name: suede-deslop
description: "Strip AI writing patterns from prose before anything goes public. Em dashes, filler openers, manufactured enthusiasm, false agency, passive voice, formulaic structures, all of it. Use when copy, a README, an email, a social post, or a doc is about to ship, after a long AI-assisted writing session, or when text sounds fine but feels generated. NOT FOR: writing new copy (use suede-copy); changing or certifying facts, which must be checked against primary evidence before publication."
---

# Suede Deslop

## Gate policy — advisory, not blocking

Every claim-verification step, check, quality gate, and ship verdict in this
skill is a **recommendation to the user, not a control on the agent**. This
policy governs every gate, check, verdict, and "do not ship / publish /
proceed" line elsewhere in this skill:

- Run every check and report the results honestly. Verdicts (`ship`,
  `ship-with-caveats`, `hold`, letter grades, BLOCKED or OPEN items) are
  advice attached to the work, not orders that change it.
- Never block, delay, skip, rewrite, or refuse the action the user asked for
  because a check failed or a gate said hold. Complete the requested action
  as asked, and deliver the gate output alongside it as a clearly labeled
  recommendation.
- A failed gate changes what you report, never what you do.
- Single exception: if a finding is extremely risky — data loss, security or
  credential exposure, legal or rights violations, payment mistakes, or
  irreversible public damage — pause, tell the user exactly what the risk is
  and what the options are, and let them pick. Their choice is final.


Run before any text goes public. AI prose has tells: throat-clearing before the point, inanimate things doing human work, binary contrasts that announce the insight instead of delivering it, rhythm that never varies. This skill removes every pattern from the list and scores what remains.

## When to use

- Before copy, a README, an email, a social post, or a doc ships
- After a long AI-assisted writing session
- When the text sounds fine but feels generated
- Before anything goes to press, investors, or customers

Do NOT run on fiction, conversational replies, or internal notes where loose voice is intentional.

---

## The eight rules

### 1. Cut filler phrases

No throat-clearing before the point. No emphasis crutches that add weight without meaning. No adverbs doing work a specific fact should do.

The kill list, 25 highest-frequency offenders:

| Category | Kill | Fix |
|----------|------|-----|
| Opener | Here's the thing: | Start with the point |
| Opener | Let's be honest / Let's face it | Cut; say the honest thing |
| Opener | The truth is / The reality is | Cut; state it |
| Opener | It's worth noting that | Cut; note it |
| Opener | In today's fast-paced world | Cut the sentence |
| Opener | Picture this: / Imagine this: | Describe the scene directly |
| Opener | At its core / At the end of the day | Cut; make the core claim |
| Crutch | Let that sink in / Read that again | Cut; the sentence carries or it does not |
| Crutch | genuinely / truly / literally | Cut |
| Crutch | actually / really / very | Cut |
| Crutch | full stop / period (as emphasis) | Cut |
| Crutch | make no mistake | Cut |
| Jargon | leverage (as a verb) | use |
| Jargon | utilize | use |
| Jargon | delve into | cover, get into |
| Jargon | navigate (a challenge) | handle, work through |
| Jargon | landscape / ecosystem (abstract) | market, field, or the named thing |
| Jargon | journey (not travel) | process, or name the steps |
| Jargon | unlock / unleash | say what was blocked |
| Jargon | robust / seamless / powerful | name the capability or prove it |
| Jargon | elevate / empower / transform | say what changes, before and after |
| Adverb | incredibly / remarkably / surprisingly | cut, or give the number that surprises |
| Adverb | seamlessly / effortlessly | cut; show the step count |
| Adverb | fundamentally / essentially / ultimately | cut; the claim stands or it does not |
| Adverb | importantly / notably | cut; if it matters, the content shows it |

The table is the high-frequency cut. The full sweep, with forty-plus more phrases across every category, lives in [references/kill-list.md](references/kill-list.md); run it when the text goes to press, investors, or customers. Three categories the table compresses:

- **Adverbs, blanket rule.** Kill every adverb, not just the listed ones. No -ly words, no softeners, no intensifiers, no hedges: just, honestly, simply, deeply, inherently, inevitably, interestingly, crucially, and the rest.
- **Meta-commentary.** The piece moves; it never announces its own structure. Cut "Let me walk you through", "In this section, we'll", "As we'll see", "Plot twist:", "Hint:", "But that's another post", "X is a feature, not a bug".
- **Performative sincerity.** False intimacy and announced significance. Cut "I promise", "creeps in", "This is genuinely hard", "This is what X actually looks like", "actually matters". Show the difficulty; never claim it.

Bad: "Here's the thing: this is genuinely hard. Let that sink in."
Good: "This is hard."

---

### 2. Break formulaic structures

The patterns the model reaches for when it has nothing original to say. Each with its fix:

- **Binary contrast** ("It's not about speed. It's about precision.") | Fix: state the real claim directly. "Precision matters more than speed here."
- **"Isn't just" construction** ("This isn't just a tool, it's a platform.") | Fix: cut the setup; say what it is with one proof.
- **Negative listing** ("No setup. No config. No hassle.") | Fix: one positive sentence naming what the user does.
- **Dramatic fragment** ("One problem." / "And it worked.") | Fix: attach the fragment to the sentence it modifies.
- **Rhetorical setup** ("So what does this mean for you?" / "What if I told you...?" / "Think about it:") | Fix: delete the question; give the answer.
- **False agency** ("The data tells us" / "the decision emerges" / "the culture shifts" / "the market rewards") | Fix: name the person. "We measured." "I argue." If no one fits, use "you".
- **Triad rhythm** ("Faster. Cleaner. Better.") | Fix: two items, or a full sentence. Three-beat lists only when the count is really three.
- **Reveal fragment** ("[Noun]. That's it. That's the [thing].") | Fix: one complete sentence, no staged reveal.
- **Formulaic template** ("By the time X, I was Y." / "X that isn't Y") | Fix: drop the template; state the fact. "X is broken."
- **Permission grant** ("And that's okay.") | Fix: cut it; the reader did not ask.

Binary contrast alone has eleven spellings ("The answer isn't X. It's Y." / "It feels like X. It's actually Y." / "stops being X and starts being Y" and more); the full variant table is in [references/kill-list.md](references/kill-list.md).

Bad: "It's not about speed. It's about precision."
Good: "Precision matters more than speed here."

---

### 3. Active voice. Every sentence.

A human subject does something. No passive constructions. No inanimate objects performing human actions.

Bad: "The decision was reached after careful consideration."
Good: "The team decided after reviewing three options."

Bad: "Mistakes were made."
Good: "Name who made them."

---

### 4. Be specific

No vague declaratives. No lazy extremes. Name the specific thing.

Lazy extremes are every, always, never, everyone, everybody, nobody: false authority doing vague work. Vague declaratives announce weight without naming it: "The reasons are structural", "The stakes are high", "This is the deepest problem", "The consequences are real".

Bad: "The implications are significant."
Good: Name the implication.

Bad: "Everyone knows this."
Good: Name who knows it and what they know.

---

### 5. Put the reader in the room

No narrator floating above the scene. "You" beats "People." Specifics beat abstractions. The reader should feel placed, not lectured at. The lecturer tells: "This happens because...", "This is why...", "People tend to...". Replace the floating observation with the reader's own scene.

Bad: "Nobody designed this. It just happened."
Good: "You didn't sit down and decide to build this. It accumulated."

---

### 6. Vary rhythm

Mix sentence lengths. Two items beat three. End paragraphs differently. No em dashes, anywhere, ever.

Three consecutive sentences at the same length: break one. Every paragraph ending with a punchy one-liner: vary it. Staccato fragments stacked for effect: merge them. A question answered in the same breath: let it breathe or cut it. Hedging dressed as reassurance ("Not always. Not perfectly."): cut it.

Sentence starters count as rhythm. Wh- openers ("What makes this hard is...") read as a crutch: lead with the subject ("The constraint is..."). Paragraphs opening with "So": start with content. Sentences opening with "Look,": remove.

---

### 7. Trust the reader

State facts directly. Skip softening, justification, hand-holding. The reader is an adult.

Cut: "I want to be clear that..." / "It's important to note that..." / "As you might expect..."
Start with the content.

---

### 8. Cut quotables

If a sentence sounds like it was written to be screenshotted, rewrite it. Pull-quote prose is manufactured. Cut the performance.

---

## Pre-ship checklist

Run every item before delivering prose:

- Adverbs? Kill them.
- Passive voice? Find the actor, put them at the front.
- Inanimate thing doing a human verb ("the decision emerges")? Name the person.
- Sentence starts with What/When/Where/Which/Who/Why/How? Restructure it.
- "Here's what/this/that" opener? Cut to the point.
- "Not X, it's Y" contrast? State Y directly.
- Three consecutive sentences at the same length? Break one.
- Paragraph ends punchily? Vary it.
- Em dash anywhere? Remove it.
- Vague declarative ("The implications are significant")? Name the specific implication.
- Narrator above the scene ("Nobody designed this")? Put the reader in it.
- Meta-joiner ("The rest of this piece...")? Delete. Let it move.
- Paragraph starts with "So", or a sentence starts with "Look,"? Start with the content.
- Question answered in the same breath? Let it breathe or cut it.
- Announced significance ("This is genuinely hard" / "actually matters")? Show it or cut it.
- Lazy extreme (every, always, never, everyone, nobody) making a vague claim? Name the specific.

---

## Scoring

Rate 1–10 on each dimension after the pass:

| Dimension | Question |
|-----------|----------|
| Directness | Statements, not announcements? |
| Rhythm | Varied, not metronomic? |
| Trust | Respects the reader? |
| Authenticity | Sounds human? |
| Density | Anything still cuttable? |

**Below 35/50: revise.** Don't ship it.

---

## Examples

Before: "Here's the thing — the migration wasn't just a technical challenge. It was a fundamental shift in how the team operates. No more silos. No more handoffs. No more waiting."
After: "The migration changed how the team operates: engineers now deploy their own services instead of filing tickets and waiting two days."

Before: "The implications are truly significant. This decision was reached after careful consideration, and it will ultimately transform the developer experience."
After: "The platform team chose Vite over Webpack. Local builds dropped from 90 seconds to 4."

Before: "So what does this mean for creators? It means empowerment. It means ownership. It means the landscape has fundamentally shifted."
After: "Creators now hold the registry keys. When a track sells, the split executes without a label in the loop."

Note: the specifics in these After lines came from author context. Never invent specifics; use `[AUTHOR: supply X]` placeholders.

---

## Red Flags: Stop

If you catch yourself thinking any of these, stop and correct:

- "It's just an internal note." Internal notes get pasted into public docs. Run the pass.
- "The em dash is stylistic here." No em dashes, anywhere, ever. That is the rule.
- "That line earned its quotability." If it sounds written to be screenshotted, it was. Rewrite it.
- "The triad has rhythm." Rhythm the reader has seen a thousand times is a tell, not a style.
- "The score is 34, close enough." Below 35 means revise. Revise.

## Boundaries

This skill edits style only. It must NOT:

- Change any fact, number, date, name, price, or claim. If a rewrite requires a specific the source text does not contain (a metric, an actor, a step count), insert `[AUTHOR: supply X]` instead of inventing one.
- Verify or vouch for the truth of any claim. Require primary evidence for factual wording; otherwise preserve an explicit `[AUTHOR: supply source]` marker or qualify or remove the claim.
- Publish, post, send, commit, or overwrite the original file/message. Return cleaned prose in the response; the author decides where it lands.
- Decide whether the piece should ship at all: the CLEAN/REVISE verdict is about slop, not content approval.

## Output format

Return the cleaned prose first. Then append:

```
Deslop pass
──────────────────────────────
Filler phrases removed:      [count]
Structural patterns fixed:   [count]
Passive voice → active:      [count]
Vague declaratives cut:      [count]
Rhythm breaks added:         [count]
Em dashes removed:           [count]

Score
──────────────────────────────
Directness:   [1–10]
Rhythm:       [1–10]
Trust:        [1–10]
Authenticity: [1–10]
Density:      [1–10]
Total:        [X/50]

Verdict: [CLEAN / REVISE]
```

If total is below 35, name what is still generating the score and why it could not be resolved without more author context.

## Routing

- The text needs writing, not cleaning → /suede-copy (one surface) or /johnny-suede-write (full stack)
- The cleaned text makes claims a public audience will read → compare each claim with primary evidence such as the current product, live URL, recorded metric, or named source; qualify or remove anything unsupported before it ships
- The text is a campaign artifact → campaign strategy gate (private Suede Labs companion, not in this pack: suede-growth)
