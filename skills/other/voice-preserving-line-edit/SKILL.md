---
name: voice-preserving-line-edit
description: "Context-aware line edit that strips generic AI writing patterns without flattening the author's voice, plus a findings-only audit mode that names issues instead of rewriting. Applies contextual rules rather than blanket bans on adverbs, passive voice, and punctuation, and locks facts, numbers, quotes, code, links, and the supplied house style before it touches a sentence. Use before copy, a README, an email, a social post, or a doc ships; after a long assisted-writing session; when the text sounds fine but feels generated; or when the user asks for a findings-only slop audit. NOT FOR: writing new copy from scratch; deciding whether a person or a model wrote text; changing or certifying facts, which must be checked against primary evidence before publication."
---

# Voice-Preserving Line Edit

A finishing pass for prose that is already written. It hunts throat-clearing
before the point, inanimate things doing human work, binary contrasts that
announce an insight instead of delivering it, and rhythm that never varies.

Two things separate this from a generic anti-slop rule sheet:

1. **Every rule is contextual.** Adverbs, passive voice, third-person register,
   and em dashes are not banned outright. Each is cut only when it weakens
   this piece, in this genre, under this house style. A technical adverb, a
   conventional passive, an academic register, and a house-approved em dash all
   survive the pass.
2. **There is an audit mode.** Ask for findings and you get quoted issues,
   reasons, and minimum corrections, with your text returned unchanged. The
   rewrite mode is opt-in, not the only setting.

These are writing-quality signals. They are not evidence of who or what wrote
the text, and this skill never claims otherwise.

---

## What This Skill Does

- Finds and, on request, removes filler phrases, business jargon, empty
  intensifiers, formulaic structures, false agency, vague declaratives, and
  metronomic rhythm in finished prose.
- Preserves the author's voice: deliberate fragments, dry humor, technical
  vocabulary, chosen formality, and useful rough edges.
- Preserves the record: facts, numbers, dates, names, prices, claims,
  qualifiers, quotations, code, commands, links, citations, and paths pass
  through untouched.
- Runs in either of two modes, findings-only audit or cleaning pass, each with
  its own fixed output contract.
- Scores the result on five dimensions out of 50 and returns a CLEAN or REVISE
  verdict about the prose quality.

What it does not do: write new copy, restructure an argument, fact-check,
guess at authorship, or publish anything. See Boundaries.

---

## When to Use This Skill

- Before copy, a README, an email, a social post, or a doc ships
- After a long AI-assisted writing session
- When the text sounds fine but feels generated
- Before anything goes to press, to investors, or to customers
- When someone wants the issues identified without a rewrite
- When a draft has to keep a specific author's voice and a generic cleanup
  would erase it

Do not run it on fiction, conversational replies, or internal notes where a
loose voice is intentional. When the request is findings only, report the
issues and leave the supplied text unchanged.

---

## How to Use

### Basic

Hand the skill a block of prose and ask for a cleanup:

    Run a voice-preserving line edit on this README intro.
    <paste text>

You get the cleaned prose first, then a change report and a 50-point score.

### Advanced

**Findings-only audit.** Use the words detect, flag, review, diagnose, audit,
or do not rewrite:

    Audit this launch email for slop. Findings only, do not rewrite it.

You get quoted issues split into Clear issues and Judgment calls, with a
minimum correction for each. Your text comes back unchanged.

**Supply a house style.** A company or author style brief overrides the
defaults in this skill, including punctuation and register:

    Line-edit this page. House style: em dashes are fine, we write in
    third person, and "platform" is our term, never "ecosystem".

**Supply author context.** The example rewrites below only get specific because
the source supplied the specifics. If real numbers, names, or before/after
figures exist, paste them alongside the draft. Without them the skill marks the
gap rather than inventing a filler.

**Run the deep sweep.** The 25-row table below is the high-frequency cut. For
press, investor, or customer-facing text, or when the table comes back clean and
the prose still reads generated, run the full list in
[references/kill-list.md](references/kill-list.md).

**Scope the pass.** Ask for a subset when only part of the problem matters, for
example "structural patterns only, leave word choice alone."

---

## Advisory, not blocking

Every check, gate, score, and verdict in this skill is a recommendation to the
user, not a control on the agent.

- Run every check and report the results honestly. Verdicts (CLEAN, REVISE,
  a score below threshold) are advice attached to the work, not orders that
  change it.
- Never block, delay, skip, or refuse the action the user asked for because a
  check failed. Complete the request as asked and deliver the check output
  alongside it, clearly labeled as a recommendation.
- A failed check changes what you report, never what you do.
- Single exception: if a finding is extremely risky, such as legal or rights
  exposure, a claim that could mislead a customer or investor, or irreversible
  public damage, pause, state the risk and the options, and let the user pick.
  Their choice is final.

---

## Before the pass

1. **Choose the deliverable.** Default to cleaned prose. Use a findings-only
   audit when the user says detect, flag, review, diagnose, audit, or do not
   rewrite.
2. **Lock the source.** Preserve facts, numbers, dates, names, prices, claims,
   quotations, qualifiers, code, commands, links, citations, and paths.
3. **Lock the voice.** Preserve deliberate fragments, dry humor, technical
   vocabulary, formality, and useful rough edges. Remove a pattern only when it
   weakens this piece in this context.
4. **Read the house style.** A supplied company or author brief overrides the
   punctuation and register defaults in this skill.

Make the minimum effective edit. Never add anecdotes, customers, metrics,
quotes, first-person experience, or specificity that the source did not supply.

---

## The eight rules

### 1. Cut filler phrases

No throat-clearing before the point. No emphasis crutches that add weight
without meaning. No adverbs doing work a specific fact should do.

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

The table is the high-frequency cut. The full sweep, with forty-plus more
phrases across every category, lives in
[references/kill-list.md](references/kill-list.md); run it when the text goes
to press, to investors, or to customers. Three categories the table compresses:

- **Adverbs, contextual rule.** Cut adverbs that merely intensify, soften, or
  announce importance. Keep an adverb when it carries factual, technical,
  legal, quoted, or voice-specific meaning.
- **Meta-commentary.** The piece moves; it never announces its own structure.
  Cut "Let me walk you through", "In this section, we'll", "As we'll see",
  "Plot twist:", "Hint:", "But that's another post", "X is a feature, not a
  bug".
- **Performative sincerity.** False intimacy and announced significance. Cut
  "I promise", "creeps in", "This is genuinely hard", "This is what X actually
  looks like", "actually matters". Show the difficulty; never claim it.

Bad: "Here's the thing: this is genuinely hard. Let that sink in."
Good: "This is hard."

---

### 2. Break formulaic structures

The patterns a model reaches for when it has nothing original to say. Each with
its fix:

- **Binary contrast** ("It's not about speed. It's about precision.") | Fix:
  state the real claim directly. "Precision matters more than speed here."
- **"Isn't just" construction** ("This isn't just a tool, it's a platform.") |
  Fix: cut the setup; say what it is with one proof.
- **Negative listing** ("No setup. No config. No hassle.") | Fix: one positive
  sentence naming what the user does.
- **Dramatic fragment** ("One problem." / "And it worked.") | Fix: attach the
  fragment to the sentence it modifies.
- **Rhetorical setup** ("So what does this mean for you?" / "What if I told
  you...?" / "Think about it:") | Fix: delete the question; give the answer.
- **False agency** ("The data tells us" / "the decision emerges" / "the culture
  shifts" / "the market rewards") | Fix: name the person. "We measured." "I
  argue." If no one fits, use "you".
- **Triad rhythm** ("Faster. Cleaner. Better.") | Fix: two items, or a full
  sentence. Three-beat lists only when the count is really three.
- **Reveal fragment** ("[Noun]. That's it. That's the [thing].") | Fix: one
  complete sentence, no staged reveal.
- **Formulaic template** ("By the time X, I was Y." / "X that isn't Y") | Fix:
  drop the template; state the fact. "X is broken."
- **Permission grant** ("And that's okay.") | Fix: cut it; the reader did not
  ask.

Binary contrast alone has eleven spellings ("The answer isn't X. It's Y." /
"It feels like X. It's actually Y." / "stops being X and starts being Y" and
more); the full variant table is in
[references/kill-list.md](references/kill-list.md).

Bad: "It's not about speed. It's about precision."
Good: "Precision matters more than speed here."

---

### 3. Prefer active voice when the actor matters

Name the actor when responsibility or causality matters. Keep passive voice
when the actor is unknown, immaterial, deliberately withheld, or conventional
in the technical context. Do not force a human subject into a sentence that
does not need one.

Bad: "The decision was reached after careful consideration."
Good: "The team decided after reviewing three options."

Bad: "Mistakes were made."
Good: Name who made them.

---

### 4. Be specific

No vague declaratives. No lazy extremes. Name the specific thing.

Lazy extremes are every, always, never, everyone, everybody, nobody: false
authority doing vague work. Vague declaratives announce weight without naming
it: "The reasons are structural", "The stakes are high", "This is the deepest
problem", "The consequences are real".

Bad: "The implications are significant."
Good: Name the implication.

Bad: "Everyone knows this."
Good: Name who knows it and what they know.

---

### 5. Put the reader in the room when the genre supports it

Specifics beat abstractions. In direct guidance, "you" often beats a vague
"people." Preserve third-person, academic, legal, or documentary register when
the source calls for it.

Bad: "Nobody designed this. It just happened."
Good: "You didn't sit down and decide to build this. It accumulated."

---

### 6. Vary rhythm

Mix sentence lengths. Two items often beat three. End paragraphs differently.
Follow the supplied house style for em dashes; with no house style given,
replace them with commas, parentheses, colons, or periods. Never treat
punctuation as evidence of authorship.

Three consecutive sentences at the same length: break one. Every paragraph
ending with a punchy one-liner: vary it. Staccato fragments stacked for effect:
merge them. A question answered in the same breath: let it breathe or cut it.
Hedging dressed as reassurance ("Not always. Not perfectly."): cut it.

Sentence starters count as rhythm. Wh- openers ("What makes this hard is...")
read as a crutch: lead with the subject ("The constraint is..."). Paragraphs
opening with "So": start with content. Sentences opening with "Look,": remove.

---

### 7. Trust the reader

State facts directly. Skip softening, justification, hand-holding. The reader
is an adult.

Cut: "I want to be clear that..." / "It's important to note that..." / "As you
might expect..." Start with the content.

---

### 8. Cut quotables

If a sentence sounds like it was written to be screenshotted, rewrite it.
Pull-quote prose is manufactured. Cut the performance.

---

## Pre-ship checklist

Run every item before delivering prose:

- Empty intensifiers or hedges? Cut them; preserve meaning-bearing adverbs.
- Passive voice hiding responsibility? Name the actor; preserve useful
  technical passive voice.
- Inanimate thing doing a human verb ("the decision emerges")? Name the person.
- Sentence starts with What/When/Where/Which/Who/Why/How? Restructure it.
- "Here's what/this/that" opener? Cut to the point.
- "Not X, it's Y" contrast? State Y directly.
- Three consecutive sentences at the same length? Break one.
- Paragraph ends punchily? Vary it.
- Em dash conflicts with the active house style? Replace it; otherwise preserve
  the author's punctuation.
- Vague declarative ("The implications are significant")? Name the specific
  implication.
- Narrator above the scene ("Nobody designed this")? Put the reader in it.
- Meta-joiner ("The rest of this piece...")? Delete. Let it move.
- Paragraph starts with "So", or a sentence starts with "Look,"? Start with the
  content.
- Question answered in the same breath? Let it breathe or cut it.
- Announced significance ("This is genuinely hard" / "actually matters")? Show
  it or cut it.
- Lazy extreme (every, always, never, everyone, nobody) making a vague claim?
  Name the specific.

---

## Scoring

Rate 1-10 on each dimension after the pass:

| Dimension | Question |
|-----------|----------|
| Directness | Statements, not announcements? |
| Rhythm | Varied, not metronomic? |
| Trust | Respects the reader? |
| Authenticity | Sounds human? |
| Density | Anything still cuttable? |

**Below 35/50: revise.** Do not ship it.

---

## Example

A README intro, run through both modes. The source paragraph carries real
facts, so the rewrite has something to surface. Nothing below is invented.

### Source

> Here's the thing: developer onboarding isn't just a process problem. It's a
> cultural one. In today's fast-paced landscape, teams need to leverage robust
> tooling to seamlessly navigate the challenges of scale. The implications are
> significant. Our new CLI fundamentally transforms setup. No manual config. No
> YAML wrangling. No waiting on ops. It turns out that the setup that used to be
> handled by a dedicated engineer over two days now takes one command. Let that
> sink in.

### Mode 1: findings-only audit

```text
Clear issues
- "Here's the thing:" - throat-clearing before the point - delete; open on the CLI claim.
- "isn't just a process problem. It's a cultural one." - binary contrast announces an
  insight the paragraph never delivers; nothing that follows supports "cultural" - state
  the actual claim or cut the sentence.
- "In today's fast-paced landscape" - dated filler, and "landscape" names nothing - cut.
- "leverage robust tooling to seamlessly navigate the challenges of scale" - jargon stack
  (leverage, robust, seamlessly, navigate) with no capability named - replace with the
  capability the paragraph already has: one command.
- "The implications are significant." - vague declarative; the implication appears two
  sentences later - cut.
- "fundamentally transforms" - announced significance instead of the before and after,
  which the source supplies - use the two-days-to-one-command figures.
- "No manual config. No YAML wrangling. No waiting on ops." - negative listing; runway
  before the point - one positive sentence naming what the user does.
- "the setup that used to be handled by a dedicated engineer" - passive hides an actor
  who matters to the claim - name the engineer's role as the subject.
- "It turns out that" - throat-clearing - cut.
- "Let that sink in." - emphasis crutch - cut; the numbers carry it.

Judgment calls
- "Our new CLI" - "new" expires within a release cycle - drop "new" unless this README is
  a launch announcement.
- "developer onboarding" - reads as house vocabulary; if the rest of the docs say
  "onboarding" alone, match that. Left as supplied.

Boundary: writing-quality signals do not establish authorship.
```

The source text is returned unchanged in this mode.

### Mode 2: cleaning pass

> A dedicated engineer used to spend two days setting up each new developer.
> Our CLI does it in one command.

```
Line edit pass
------------------------------
Filler phrases removed:      9
Structural patterns fixed:   2
Passive voice to active:     1
Vague declaratives cut:      1
Rhythm breaks added:         1
Em dashes removed:           0

Score
------------------------------
Directness:   9
Rhythm:       8
Trust:        9
Authenticity: 8
Density:      9
Total:        43/50

Verdict: CLEAN
```

Note what did not happen. No metric was invented, no customer was named, and
the "cultural" claim was cut rather than expanded, because the source offered
no support for it. The two days and the one command were already there.

### More before and after pairs

Before: "Here's the thing - the migration wasn't just a technical challenge. It
was a fundamental shift in how the team operates. No more silos. No more
handoffs. No more waiting."
After: "The migration changed how the team operates: engineers now deploy their
own services instead of filing tickets and waiting two days."

Before: "The implications are truly significant. This decision was reached
after careful consideration, and it will ultimately transform the developer
experience."
After: "The platform team chose Vite over Webpack. Local builds dropped from 90
seconds to 4."

Before: "So what does this mean for creators? It means empowerment. It means
ownership. It means the landscape has fundamentally shifted."
After: "Creators now hold the registry keys. When a track sells, the split
executes without a label in the loop."

The specifics in these After lines came from author context. Never invent
specifics. Ask for missing material when interaction is possible; otherwise
mark the unresolved gap without manufacturing an answer.

---

## Tips

- **Audit first on anything you did not write.** Findings mode shows you the
  cost of each edit before a single word moves, which matters when the author
  is a client, a colleague, or your own past self.
- **Give it the numbers.** The largest quality jump comes from pasting the real
  figures next to the draft. Vague prose usually hides missing facts, and a
  line edit cannot conjure them.
- **State your house style up front.** One sentence ("we use em dashes, we
  write in third person") prevents the most common bad edit, which is a
  correctly applied rule that is wrong for your publication.
- **Read the Judgment calls section, not just Clear issues.** The judgment calls
  are where the author's voice actually lives.
- **A score of 34 means revise.** The threshold is not a suggestion, and
  rounding up to "close enough" is how slop ships.
- **Run the pass on your own edit.** The second pass usually finds two or three
  filler phrases the first one introduced.
- **Do not run it on a rough draft.** This is a finishing pass. Cleaning prose
  you are about to restructure wastes the work.
- **Keep the source.** The skill returns cleaned prose in the response and
  never overwrites a file, so keep the original until you have compared them.

---

## Common Use Cases

- **README and docs polish** before a repository goes public.
- **Landing page and product copy** review before launch.
- **Investor updates, board memos, and press releases**, where the deep sweep
  in the reference file is worth running.
- **Newsletters, blog posts, and essays** after an assisted drafting session.
- **Social posts and launch threads**, where quotable-sounding lines multiply.
- **Editing someone else's draft** without imposing your voice on it: audit
  mode gives them findings they can accept or reject one at a time.
- **Ghostwriting and client work**, where the deliverable has to sound like the
  named author rather than like a style guide.
- **Grant applications, proposals, and academic abstracts**, where the
  third-person register must survive the cleanup.
- **Style QA on a team**, using the 50-point score as a shared, repeatable
  quality bar.

---

## Red Flags: Stop

If you catch yourself thinking any of these, stop and correct:

- "It's just an internal note." Internal notes get pasted into public docs. Run
  the pass.
- "An em dash proves this was generated." Punctuation cannot establish
  authorship. Follow the active house style.
- "That line earned its quotability." If it sounds written to be screenshotted,
  it was. Rewrite it.
- "The triad has rhythm." Rhythm the reader has seen a thousand times is a
  tell, not a style.
- "The score is 34, close enough." Below 35 means revise. Revise.
- "This adverb is technically an adverb." Check whether it carries factual,
  technical, legal, or quoted meaning before cutting it.

---

## Boundaries

This skill edits style only. It must NOT:

- Change any fact, number, date, name, price, claim, qualifier, quotation,
  code, command, link, citation, or path.
- Infer or report whether a human or a model wrote the text. Findings describe
  the prose and its effect only.
- Flatten deliberate voice traits merely because they resemble a common
  pattern.
- Invent a metric, actor, anecdote, customer, quote, or first-person
  experience.
- Verify or vouch for the truth of any claim. Flag missing support separately;
  never qualify, remove, or otherwise alter supplied factual wording during
  this style pass.
- Publish, post, send, commit, or overwrite the original file or message.
  Return cleaned prose in the response; the author decides where it lands.
- Decide whether the piece should ship at all: the CLEAN or REVISE verdict is
  about slop, not content approval.

---

## Output format

For a findings-only audit, return:

```text
Clear issues
- [exact quote] - [why it weakens this piece] - [minimum correction]

Judgment calls
- [exact quote] - [context or voice trade-off] - [optional correction]

Boundary: writing-quality signals do not establish authorship.
```

Do not include cleaned prose in a findings-only audit.

For a cleaning pass, return the cleaned prose first. Then append:

```
Line edit pass
------------------------------
Filler phrases removed:      [count]
Structural patterns fixed:   [count]
Passive voice to active:     [count]
Vague declaratives cut:      [count]
Rhythm breaks added:         [count]
Em dashes removed:           [count]

Score
------------------------------
Directness:   [1-10]
Rhythm:       [1-10]
Trust:        [1-10]
Authenticity: [1-10]
Density:      [1-10]
Total:        [X/50]

Verdict: [CLEAN / REVISE]
```

If the total is below 35, name what is still generating the score and why it
could not be resolved without more author context.

---

## Handoffs

- The text needs writing, not cleaning. Use a copywriting or drafting skill;
  this one only edits prose that already exists.
- The cleaned text makes claims a public audience will read. Route factual
  verification to primary evidence such as the current product, a live URL, a
  recorded metric, or a named source. Report unsupported claims separately
  without changing their wording.
- The text needs its argument restructured. That is a developmental edit, not a
  line edit. Do that first, then run this pass.

---

## Credit

Adapted from the suede-creator-skills collection:
<https://github.com/JasonColapietro/suede-creator-skills>

## License

MIT. See [LICENSE](LICENSE).
