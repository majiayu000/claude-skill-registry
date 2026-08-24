---
name: purpose-properties
description: "Derive the binding properties your why/how/what impose on everything below them, so no solution can silently contradict your own product definition. Retrofit entry point for projects that started before v0.120.0; also the re-derive path when why/how/what change and every stance below them goes stale."
metadata:
  instruction_budget: "21"
  framework_dependency: "mycelium"
  framework_dependency_note: "This skill is designed to run within the Mycelium framework (https://github.com/haabe/mycelium). Standalone use will skip the canvas state, theory gates, and harness behavior the skill assumes. Install: /plugin install mycelium@haabe-mycelium."
---

# Purpose Properties Skill

Retrofit and re-derive entry point for `purpose.yml#purpose_properties`. **For new projects this runs
inside `/mycelium:start` Step 3b.** Use this skill when:

- The project existed before **v0.120.0** and has no `purpose_properties` (the retrofit case — every
  project created before that release, since `/mycelium:start` Step 4 exits for already-initialized
  projects and never reaches the extraction).
- `why`, `how` or `what` changed, so `derived_from_hash` no longer matches and **every stance below
  it is superseded** (the drift case — this is the one that matters most and the easiest to skip).
- A property list exists but the user wants to revisit which properties are `binding`.

Full contract: `${CLAUDE_PLUGIN_ROOT}/../../docs/purpose-stance.md`.

## Step 1: Read the current state and say which case this is

Read `purpose.yml`. Then say plainly which of these you are in, because the three have different
consequences and the user should not have to infer it:

- **No `purpose_properties`** → retrofit. Nothing below has ever been checked against the purpose.
- **Hash mismatch** → drift. Report it as *"your purpose changed after these were derived, so every
  `purpose_stance` below them was reasoned under a definition you have since changed."* This is the
  state that quietly invalidates work; name it in those terms.
- **Hash matches** → nothing to do. Report the property count and stop. Do not re-derive for tidiness.

## Step 2: Attempt extraction, and classify what fails

For every element of `why`, `how` and `what`, ask: **can I name a specific solution that would
CONTRADICT this?**

- **Yes** → candidate property. Record `property`, `verbatim` (their words, not yours), `source`, and
  the contradicting solution in `contradicted_by`.
- **No** → **do not force one.** Quality adjectives — *secure, accessible, fast, simple, delightful,
  robust* — yield nothing checkable, because every candidate solution claims to satisfy them.

**Measured 2026-08-23, blind:** *"accessible and secure"* produced **no** checkable property, while
five abstract framework principles produced clean ones. **The axis is not abstract vs concrete — it
is quality adjective vs structural claim.** Do not treat concrete-sounding words as safe.

## Step 2a: Screen for quality adjectives BEFORE trusting your own refusal

**DO NOT RELY ON NOTICING.** Step 2 says a quality adjective yields nothing checkable and asks you to
decline. The evidence that an extractor actually declines is **one blind run, one model family** — the
2026-08-23 test, where the extractor returned NONE for *"accessible and secure"* unprompted. That
result is real and it is thin, and this skill runs under model families that test never touched, in
runtimes where no hook fires to catch the difference. **A model that does not refuse produces a
confident property, marks it binding, and creates a stance field that every solution answers
`preserves` forever — populated, green, and meaningless.** The mechanism's own failure mode, at its
entry point.

So the screen is a rule, not a judgement:

**TRIGGER LIST — if an element contains any of these words, it routes to Step 3 REGARDLESS of whether
you extracted something from it:**

> secure · safe · private · accessible · usable · intuitive · simple · easy · fast · performant ·
> scalable · reliable · robust · flexible · modern · seamless · delightful · high-quality ·
> best-in-class · efficient · powerful · lightweight

**Extracting a property from one of these words is not evidence the word was checkable.** It is the
predicted failure. Route it, let the builder supply the standard, and record what they say.

**AND THE GENERAL TEST, for words the list does not carry** (it cannot be complete, and treating it
as complete is the next version of this bug):

> **Would every plausible competing solution ALSO claim to satisfy this?**
> If yes, it is a quality adjective, whatever it sounds like. Route it.

*"Secure"* fails that test — nobody proposes an insecure login. *"Anonymous"* passes it — a solution
requiring an account plainly does not claim anonymity. **Note that the concrete-sounding word is the
one that fails.** The axis is never how technical the word looks.

**WHAT IS STILL UNTESTED, stated so nobody reads the list as coverage:** whether a builder actually
answers the Step 3 prompt. The 2026-08-23 run exercised extraction only — no builder was asked
anything — so the recovery path has evidence for its necessity and none for its effectiveness.

## Step 2b: Check the ALTITUDE of every candidate before you record it

**A property must sit at the altitude where violation is meaningful.** Ask, of each candidate:

> **What would have to be true for this to be violated — a single move, or a design choice?**

- **A design choice** → it is a property of the product. Record it.
- **A single move** → **you have extracted a rule about BEHAVIOUR, not a property of the product.
  Do not record it.** A property that can be violated by one sentence turns the stance field into a
  footnote requirement, and a check people must satisfy per action is one they mute.

**WORKED EXAMPLE, and it is why this step exists.** From *"Theory-guided decisions: every significant
decision is grounded in established frameworks"*, two independent blind extractions BOTH produced
*"a significant decision must name the framework it rests on"* — per decision. The words invite it.
But the founder's reading is the right one: **not everything needs to be grounded for the overall to
be grounded.** The principle is about how the SYSTEM is built — its gates, skills and structure derive
from theory — not about an audit trail on each move. Pitched per-decision it is micromanagement; the
same project's `(per: <source>)` convention, injected into every session, sits at **4 citations
across 197 decision-log entries**.

**AND CHECK WHETHER IT IS ALREADY MECHANISED BEFORE MINTING A PROPERTY.** That same principle is
already enforced at the right altitude by `check_theory_fidelity.py` on every push. **Point at the
existing check; do not mint a property that duplicates it** — two mechanisms for one claim means one
of them drifts unnoticed.

**`binding` and altitude guard different failures.** `binding: true` limits HOW MANY properties are
checked. Altitude limits how GRANULAR each one is. **Both end the same way if you get them wrong — a
check nobody reads — and only one of them is visible in the field.**

## Step 3: Interview the builder on what failed — with candidates, not an open question

> You said **"secure"**. Which of these would you call a violation?
> (a) passwords stored in plaintext (b) no transport encryption (c) sessions that never expire (d) something else

**Recognition is cheap; generation is not.** Offer three plausible violations drawn from the domain,
and expect (d) to be where the real answer lives.

- **They answer** → you have a property; record the violation in `contradicted_by`.
- **They cannot, or decline** → record `aspiration_reason` and say the consequence out loud:
  *"'secure' stays undefined, so no solution will ever be checked against it."* **A skip is a
  recorded choice, never a blank.**

**This is NOT `/mycelium:user-interview`.** That skill asks about specific past behaviour, which is
right for discovering user needs and wrong here — this elicits a definition from the builder about
their own intent, where the question is hypothetical by design.

## Step 4: The user marks `binding`, and only they can

Present the candidates and ask which ones, if violated, would **break the product** rather than merely
disappoint. Only those get `binding: true`, and only those are ever checked.

**Do not set these yourself.** A why/how/what yields many adjectives; an agent marking them all
binding turns the check into noise, and noise gets muted. Set `confirmed_by: human` only after they
have actually answered.

## Step 5: Write, then say what changed downstream

Write `purpose_properties` to `purpose.yml` (Read before Write, per the canonical rule). Set
`derived_from_hash` by running:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/check_purpose_stance.py" --canvas-dir .claude/canvas
```

**On a re-derive, tell them what it invalidated**: every existing `purpose_stance` was reasoned under
the old definition and now needs re-reading. Do not silently leave stale stances looking current.

## What this skill does NOT do

- **It does not judge whether a solution serves the purpose.** Nothing in Mycelium does; that
  judgement is unreliable and a checker that unreliable is a second opinion wearing a gate's clothes.
- **It does not write a stance on any solution.** That belongs to `/mycelium:ost-builder`.
- **It does not clear a `contradicts`.** Only a human can, and the check enforces it.

## Theory grounding

Sinek (*Start With Why*) — the why/how/what ordering, and the reason the innermost ring governs the
others. **Used as an ordering, never for the book's neuroscience claims, which do not survive
checking.** The mechanism itself is this project's own: a declaration that can be checked, rather
than an alignment that cannot.
