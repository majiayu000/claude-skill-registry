---
name: suede-ship-copy
description: "Suede Labs copy-only orchestration DAG: intake with a verbatim capture of the published text, five blind research lenses, an audit of agent-generated facts that closes the set of assertable claims, three angles, a section map with one message per section, disjoint section writers, four-lens review, adversarial refutation, a deslop pass, and a publish-readiness gate. Use for one high-stakes piece strangers will read that has to be true: a landing page, launch post, blog post, email, X thread, docs page, README, ad, or store listing. The audit targets what the agents invent, never what the requester supplied: their own statements are given, and no phase may verify, hedge, or gate on them. Reads the live surface; never publishes. NOT FOR: multi-surface campaign writing (use johnny-suede-write); changing code (use suede-ship); one surface in one pass with no research (use suede-copy); stripping AI patterns from existing text (use suede-deslop); bulk generation (use suede-codex-fleet)."
---

# Suede Ship Copy

The copy side of the canonical Suede DAG. One brief in, one publishable draft out,
with about thirty agents in between arranged as a graph rather than a chain.

`suede-ship` decomposes work by **file ownership**: two lanes may never write the
same file. This decomposes by **message ownership**: two sections may never make
the same point, and no section may assert a fact an agent invented. Same graph,
different collision rule.

## Whose claims get audited

**The audit exists to catch agents inventing things. It never runs on the
requester.**

A research lens that reports "cold start drops to 40ms" is a machine asserting a
number, and it gets opened against its source. The requester saying the same
thing in the brief is the person who owns the product telling you a fact about
it. Those are not the same input and this workflow never treats them as the same
input.

Anything the requester supplies — the brief, the `given` list, `mustSay` strings —
enters the permitted claim set marked `origin: "user"` and is **exempt at every
stage**:

- Intake transcribes it. It does not verify, source, soften, or flag it.
- The audit never sees it. A research fact that merely restates a given is
  removed before the audit rather than checked — the given itself already carries
  that content into the permitted set, so nothing is lost. The run log and the
  evidence record both say "removed", not "passed through".
- **Protected strings are not claims.** A `mustSay` product name or legal line is
  a string to preserve byte-exact, not an assertion to exempt from review. Letting
  a product name count as a given would exempt half the draft from review, so the
  exemption corpus excludes them.
- Research lenses are told it is established and are forbidden from returning a
  constraint that contradicts it.
- Writers assert it plainly. No "reportedly", no "according to", no hedge.
- A review finding aimed at one is **discarded by a pure function** before a
  verifier is spent on it, so a persuasive lens cannot argue its way back in.
  It runs a second time after refutation, so a verifier that sustained one anyway
  still cannot hand it to the reviser.
- The match is **proportional**, not a character floor: the shorter of the given
  and the quoted text must be contained in the longer *and* be at least 60% of it,
  with a 6-character minimum. A lens quoting most of a given is out of scope; a
  lens quoting two words that happen to appear inside one is not. That matters in
  both directions — a flat floor would let a compound sentence (something you said
  **and** something an agent invented) launder the invented half behind the true
  half.
- The refute prompt says out-of-scope **at every severity**, not only for blockers.
- The publish-readiness gate skips it: no spot-check, no drift verdict, no risk
  entry, and no escalation when a live page disagrees. A stale page losing to the
  requester is the correct outcome, not a finding.
- The evidence record lists it as given, with no "unverified" label.

The exemption errs toward dropping. A legitimate finding lost because it brushed
a given is a cost worth paying; a given rewritten by the reviser because a filter
was too clever is the thing this workflow promises cannot happen.

The only hazard that can stop this run is an output path pointing at published
copy, which is a fact about a file path rather than a judgement about anything
the requester said. If an intake agent tries to mark anything else blocking, the
script downgrades it to advisory and logs the overreach.

Invoke the workflow bundled at `skills/suede-ship-copy/workflows/suede-ship-copy.js`.
If you keep a personal copy, `~/.claude/workflows/suede-ship-copy.js` works the same way.

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

**That exception never applies to a claim the requester supplied.** A
user-supplied earnings, health, or compliance statement reads as "legal or rights
violations" to a model scanning the list above, and pausing on it would be
exactly the behavior the next section forbids. The exception covers findings
about agent-generated content and about the live environment. A given is not a
finding.

## Choose this, the single pass, or the fleet

| The job | The tool |
|---|---|
| One piece, read by strangers, where a wrong number is a real cost | `suede-ship-copy` |
| One surface, written in one pass, facts already known | `suede-copy` |
| Text that exists and needs the AI patterns stripped | `suede-deslop` |
| Forty product descriptions from a spec | `suede-codex-fleet` (bills to OpenAI) |
| The change is code, not copy | `suede-ship` |

This is the expensive instrument: about thirty agents (26 floor, ~31 typical,
42 ceiling), research-heavy and front-loaded, billed to the Claude limit. Brute
force beats surgery when the work is genuinely parallel and shallow.

## Parse the invocation

The argument is free-form. Extract:

- **piece** — required. What to write, in the user's own words, kept verbatim.
  Do not compress it into a slogan; the planner decomposes it into sections and
  the detail is what makes sections separable.
- **surface** — required. Where it goes: landing page, email, email sequence, X
  thread, blog post, README, docs page, ad, app store listing, press note. The
  surface sets hard character limits, so a wrong guess is a rewrite.
- **sources** — paths and URLs that ground the facts: the repo, the pricing
  config, the changelog, the live site, transcripts, support threads. Optional,
  and the intake agent finds them otherwise, but a supplied source list is the
  difference between a claim audit that has something to check and one that
  deletes half the draft.
- **given** — facts the user states themselves, as an array of plain strings (an
  object with a `claim` key also works). These are established:
  they go straight into the permitted set, skip the audit, and no phase may
  question them. Use this whenever the user tells you something about the product
  that no file will confirm — a launch date, a customer result, a decision not yet
  written down.
- **audience** — who reads it. Optional; intake infers it and says what it inferred.
- **liveUrl** — the published surface, if one exists. The baseline capture and the
  drift check both use it.
- **outDir** — where the draft lands. Defaults to a `.suede-copy/<slug>/`
  directory. Must be a draft location: an output path pointing at already
  published copy is a halt.
- **mustSay** — strings that must survive byte-exact: legal product name,
  trademark forms, price strings, disclaimer sentences.
- **wordBudget** — total words. Optional; the surface law supplies limits per field.

If **piece** or **surface** is missing, ask. Do not invent a brief for something
a public audience will read.

## State the cost before launching

This is Claude-model fan-out against the weekly limit. Say so in one line before
the call, so the spend is a decision rather than a surprise. One line, this shape:

> Running suede-ship-copy on the Agent Studio landing page: about 30 agents
> (26-42 depending on section count and findings), billed to the Claude weekly
> limit. Starting now.

## Launch

```
Workflow({
  scriptPath: "skills/suede-ship-copy/workflows/suede-ship-copy.js",
  args: { piece, surface, sources, given, audience, liveUrl, outDir, mustSay, wordBudget }
})
```

Pass `args` as a real object. If the harness stringifies it the script recovers,
but an object is correct.

## The graph

Twelve phases, parallel wherever the edges are not real. This is the logical DAG;
the script's twelve `phase()` labels fold **Claim audit** into `Gaps` and **Collision
check** into `Outline`, and split **Review and refute** and **Gate and handoff** into
two each. When narrating live progress use the script's labels — there is no phase
called "Claim audit" in `/workflows`.

1. **Intake** — sources, the requester's own statements transcribed into the
   permitted set untouched, the currently published text captured verbatim, voice
   references drawn from shipped copy, protected strings, the surface's hard
   limits, hazards. Manifest only.
2. **Research** — five blind lenses: product truth, audience, market, voice,
   surface law. Each searches a different way because one angle never finds
   everything. Every fact carries a `file:line`, URL, sha, or timestamp.
3. **Gaps** — a completeness critic names what went unread, then one bounded fill
   round (first 2 gaps; the rest ride to the handoff as unread).
4. **Claim audit** — the load-bearing skeptic, pointed only at agent output. Every
   agent-generated fact is opened against its source and returns `holds`,
   `overstated`, `unsourceable`, or `stale`. Dropped claims leave the set;
   overstated ones are narrowed to what the source supports. The requester's
   givens are not in this list and a verdict returned against one is discarded
   unread. **Nothing downstream may assert a claim outside the permitted set:
   surviving agent claims plus every given.**
5. **Angles** — three postures generated blind to each other: problem-first,
   outcome-first, wedge. Each declares whether a competitor could publish its
   headline verbatim, which is a failing grade rather than a formatting field.
6. **Outline** — the planner judges the three angles, grafts the best of the
   runners-up, and writes a section map: one message per section, citations drawn
   only from the surviving claims, an observable acceptance question per section.
   High effort by design. Then a red team. One revision round follows **only** if the
   red team returned a fatal objection or two serious ones; otherwise the map stands
   and the objections ride to the handoff. Do not narrate a revision that did not run.
7. **Collision check** — a pure function, no agent. Duplicate message ownership,
   a citation outside the claim set, a protected string assigned zero or twice, or
   budgets over the ceiling all halt the run.
8. **Draft** — one writer per section, in parallel. Each sees its neighbours' jobs
   so transitions are possible, and never their text. A fact outside its citation
   list becomes `[AUTHOR: supply X]`, never an invention.
9. **Assemble** — a barrier. Transitions written, repetition cut, one voice,
   budget enforced, placeholders and protected strings preserved byte-exact.
10. **Review and refute** — four lenses on the whole piece (cold read, assertion
    audit, conversion, slop). Findings aimed at a given are dropped by a pure
    function first, then two independent verifiers take each surviving blocker or
    major, refute by default. **Both must fail to refute** for a finding to
    survive; unanimity, not majority, because rewriting a line that was fine has a
    real cost in a short piece.
11. **Polish** — one reviser for confirmed blockers (prose has no file-level
    disjointness, so parallel editors of one string produce a conflict with no
    merge tool), then the deslop pass scored out of 50, then the graphic spec and
    the channel package in parallel.
12. **Gate and handoff** — deterministic checks (open placeholders, missing
    protected strings, em dashes, word count, fields over limit) run in the script
    where no agent can argue with them, then a read-only publish-readiness verifier
    for drift, truth at the source, rights, and reversibility. Drift and truth-at-the-source
    are scoped to agent-generated claims; the rights check is scoped to third-party material,
    so a customer result you supplied cannot come back as a permissions risk wearing a
    rights label. Then the evidence record.

## Thresholds

Every gate in this workflow resolves to a number or a command:

| Check | Threshold |
|---|---|
| Requester's own claims audited | Never. 0 reach the audit. They reach the refute and gate prompts only as named out-of-scope context, never as a target |
| Claim may be asserted | Present in the permitted set (surviving agent claims + every given). Anything else is `[AUTHOR: supply X]` |
| Finding survives review | 2 of 2 verifiers fail to refute it |
| Findings refuted per run | First 4 blockers/majors; the remainder are logged, never silently dropped |
| Gap fills | First 2; the rest are reported as unread |
| Sections | 3-5 preferred, 7 ceiling |
| Deslop score | 35/50 or the piece is `REVISE` |
| Channel field | `chars <= limit` per field, counted and reported individually |
| Word count | `<= wordBudget × 1.1` when a budget was supplied; unenforced when it was not |
| Em dashes | 0 |
| Open placeholders | 0, or Status is "ready for author", never "reviewed" |
| Placeholders vanished since draft | 0. A placeholder the assembler or deslop pass resolved away is a fabrication |
| Stalled sections | 0. A writer returning `blocked`, `needs-context`, or nothing leaves a hole in the piece |

The last seven rows are **hard gates**: any one of them fails and `hardMechanical`
forces `copyVerdict: hold`. Two more hard gates have no row because they are
liveness rather than quality — a channel-package agent or a deslop agent that
returned nothing also forces `hold`.

The first five rows are **not** hard gates. They bound how the run behaves, and the
deslop score in particular only moves the verdict to `ship-with-caveats`, never to
`hold`. Do not report a 22/50 deslop score as a hold.

## What halts it, and what to do

Two conditions stop the run. Neither is a judgement about anything the user said:

**`halted: true, reason: "output path points at published copy"`** — the requested
`outDir` points at a live page source, a shipped README, or a sent template rather
than a draft location. Name the path, then offer: write to a draft path beside it,
write to `.suede-copy/<slug>/`, or confirm the user wants to place it themselves.

**`halted: true, reason: "section map collision"`** — two sections own the same
message, a section cites a claim that failed the audit, a protected string is
unassigned or double-assigned, or the section budgets total more than
`wordBudget × 1.1`. Report the collisions. The fix is a re-plan, not a retry:
merge the duplicate sections, supply a source for the missing claim, add the
missing fact to `given`, or relax the budget.

Three failures throw instead of returning, because each one leaves nothing to
carry forward: intake returned no manifest, the planner returned no section map,
or assembly returned no text. Report which one, name the agents already spent,
and offer: re-run with `resumeFromRunId` so the completed phases replay from
cache, re-run with better `sources` or `given`, or stop. Do not silently retry
the whole workflow — that pays for every completed phase twice.

## While it runs

Do not predict results or narrate progress you cannot see. The workflow returns a
notification when it completes; `/workflows` shows live progress.

## When it returns

Report faithfully, in this order:

1. `copyVerdict` and the deliverable path.
2. `stalled` — any section whose writer returned nothing usable. The assembled
   piece has a hole where that section's message should be. This is the loudest
   failure in the run and the easiest to miss, because the draft still reads.
3. `openPlaceholders` — the copy is not publishable until a human fills these.
   Lead with them; they are the honest measure of what nobody could source.
4. `droppedClaims` and `narrowedClaims` — what the **research agents** asserted and
   the audit refused. Anyone editing this copy later must not put them back. Report
   `givenClaims` as established fact; never present a given as unverified.
5. `findingsDiscardedAsOutOfScope` — findings dropped for targeting a given.
   Report the count. These were not verified either way, so a large number means a
   large part of the review was scoped out, not that the copy came back clean.
6. `confirmedFindings`, then `mechanical`, then the deslop score.
7. `unread` — naming what went unread is most of the honesty.

## Verdict is advisory

`copyVerdict` changes what you report, never what the run produced. The single
exception is a problem in **already published** copy that the verifier observed
independent of this draft — one live page contradicting another, a claim that has
gone stale on the site. That goes to the user immediately.

This exception is about two published surfaces disagreeing with each other. It is
never a route to escalate a **given**: if a live page disagrees with something the
requester stated, the page is what is stale. Do not report that as an exposure.

**Do not claim `published`, `posted`, `sent`, `live`, or `shipped`.** This
workflow writes a draft file and reads the live surface. Those states require an
action nobody has taken here.

## Boundaries

This workflow must NOT:

- **Publish anything.** It writes exactly two files into `outDir`: the draft and
  the evidence record. It does not post, send, commit, deploy, or edit a live
  surface, and an `outDir` pointing at published copy is a halt.
- **Invent a specific.** No number, date, price, customer name, or result that no
  source supports. The `[AUTHOR: supply X]` placeholder is the only permitted
  answer, and the deslop pass and the assembler are both forbidden from smoothing
  one away.
- **Audit, hedge, gate on, or argue with the requester's own claims.** Not at
  intake, not in research, not at review, not at the gate, and not in the evidence
  record. The audit is aimed at machine output.
- **Assert outside the permitted set.** An agent claim that failed the audit cannot
  return as an implication, a headline, on-image text, or a meta description.
- **Change a fact during a style pass.** Deslop edits style only.
- **Redraw the Suede S.** The only permitted mark is the approved asset at
  `docs/assets/suede-ai-logo-transparent.png` (sha256
  `83a7ee0317e4debe2e7b076c20ba067feb76a587f9e829dc6310ae4be4b44dfa`). Never
  trace, typeset, recolor, distort, or generate a replacement. If the approved
  file is unavailable, the graphic spec omits the mark and says so.
- **Generate images.** The graphic builder writes the spec and the words on the
  image; generation routes elsewhere.
- **Decide whether the piece should exist.** The verdict is about evidence and
  slop, not content approval.

## Iterating

Edit the script and re-invoke with the same `scriptPath`. Add
`resumeFromRunId: "<run id>"` to replay unchanged agents from cache. Changing an
agent's prompt or schema re-runs that agent and everything downstream of it — so
a tweak to the deslop prompt is cheap, and a tweak to the intake prompt is a full
re-run.

## Routing

- The change is code rather than copy -> use `suede-ship`, the same graph with
  file ownership as its collision rule.
- One surface, one pass, facts already established -> use `suede-copy`.
- Text already written that only needs AI patterns stripped -> use `suede-deslop`.
- The house voice needs defining rather than extracting from shipped copy ->
  private Suede Labs companion, not in this pack: suede-brand-voice. Without it,
  put a few pieces of already-shipped copy in `sources` and let the voice lens
  measure the voice from those.
- The graphic spec needs executing -> use `suede-image`.
- The piece needs search and answer-engine treatment after it is written -> use
  `suede-seo-audit`, then `suede-visibility-grader` for the A-F page score.
- Many independent pieces from one spec -> use `suede-codex-fleet`.
- Writing a completion or done-state claim about this run ->
  private Suede Labs companion, not in this pack: suede-verification-law. The rule
  it enforces is stated inline above: this workflow writes a draft and reads the
  live surface, so `published`, `posted`, `sent`, `live`, and `shipped` are not
  states it can claim.
- From `johnny-suede-write`: route a single high-stakes piece that must survive a
  fact audit here; keep multi-surface campaign writing there.
