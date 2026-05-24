---
name: maintainer-decline
description: "Guide for drafting issue closure and decline responses as an open-source package maintainer. Use when helping compose a reply that says \"no\" to a feature request, closes an issue as won't-fix, redirects a user to a different package, explains why a design choice is intentional, or otherwise declines or closes a community contribution. Also use when the maintainer needs to explain a deprecation, point out a user misunderstanding, or communicate an effort/scope tradeoff to a contributor."
---

# Maintainer Decline

Help an open-source maintainer compose responses that close, decline, or redirect issues while leaving the contributor informed and respected.

## Core Philosophy

Closure is not dismissal. A well-crafted decline educates, unblocks, or redirects the contributor productively. The goal is that someone reading your response walks away understanding *why* — even if they didn't get what they asked for.

## Principles

**Explain the why, not the what.** Contributors understand they're being told "no." What they need is the reasoning: strategic direction, design philosophy, effort/benefit tradeoff, or the actual technical root cause.

**Validate before declining.** Acknowledge the contributor's point before the redirect. Phrases like "Yeah," "This is a reasonable idea," or "I think..." signal that you heard them before delivering the decision.

**Offer a path forward when possible.** Even a "no" can come with "but you could..." or "use X instead." Leave the contributor unblocked or pointed in the right direction.

**Use "we" for design decisions.** "We believe," "we've decided," "we experimented with..." positions decisions as team choices, not personal gatekeeping.

**One decision per response.** No hedging, no "maybe later" unless you mean it. Clear closure — even if that closure is "this will happen after X."

**Brevity signals respect.** Most declines land in 1–3 sentences. Go longer only when the misunderstanding is significant or teaching is genuinely needed.

**Acknowledge effort.** If the contributor did real work (wrote a reprex, drafted code, did research), name it. "Thanks for the detailed report" costs nothing and signals you value their time.

## Response Patterns

Choose the pattern that fits the situation. These are not templates — they're structural moves you can adapt.

### Duplicate

One line. Link the original issue. No elaboration needed.

> Duplicate of #7651

### Fixed / Resolved

Link the fix. Nothing else required.

> Fixed in #1430

### Won't Fix — Superseded or Deprecated

Explain the strategic direction, reference the replacement, thank the user.

> gather() is no longer under active development because it's been superseded by pivot_longer(). Sorry we can't help more and thanks for using tidyr!

> Given that we're moving away from this warning (in favour of using .by), I think unfortunately it's more effort than it's worth.

**Structure:** [What's happening strategically] + [migration path or replacement] + [brief thanks or acknowledgment]

### Design Philosophy

When something looks like a bug but is working as intended. Frame as a principle, explain the consequence chain.

> In general, we believe this liberal type casting is a net negative because it can mean that data quality problems are silently propagated, eventually causing uninformative errors.

> We experimented with this in the past but because many tidyr functions produce list columns and the data.frame method for print() doesn't do a great job with them, we've decided to stick with tibbles everywhere.

**Structure:** [The principle: "we believe..." / "we've decided..."] + [What goes wrong if you allow it] + [Optionally: past exploration that led here]

### Workaround / Unblocking Alternative

The request isn't happening, but there's a path forward. Lead with validation, offer the concrete alternative. Position the workaround as the *best* approach, not a consolation prize.

> Yeah, I think you're best off creating the formulas outside of expand_grid().

> You could make your code a bit simpler by using coalesce(): [code example]. We don't have many functions that work across columns because of the challenge of what to do if they're incompatible types.

**Structure:** [Validation: "Yeah," / "I think..."] + [Concrete alternative, possibly with code] + [Optionally: why the feature doesn't exist]

### Clarification / Teaching Root Cause

The contributor misunderstands the behavior. Show what's actually happening — with a reprex, a documentation quote, or a one-sentence explanation of the mechanic they missed.

> The problem is that your pattern doesn't match, and the expected behaviour in that case is that you get an NA at the output. Unfortunately there's no way for us to fill in the result from some of the match groups, because none of them get populated by the regexp engine.

> It's not showing up because instead of one long map() call, you're creating many short ones.

> I think this is pretty clearly documented: [quotes docs]. It's pretty hard to change this sort of behaviour without affecting a lot of existing code and given the seeming rarity of it being a problem, I unfortunately don't think it's worth the effort.

**Structure:** [What's actually happening] + [Why it works this way] + [Optionally: why it can't easily change]

### Effort Assessment

The request is valid but the effort/benefit doesn't justify it. Acknowledge the idea, explain the barrier, optionally leave the door open for external solutions.

> This seems like a reasonable optimisation, but it's not clear to me where it should live. Unfortunately I think there are just too many unknowns for us to get traction on this problem, but it would be great to have a tidyverse-wide solution.

**Structure:** [Acknowledge validity] + [Name the real barrier] + [Optionally: where it could live instead]

### Scope / "Not Here Yet"

The idea has merit but doesn't belong in this package or isn't ready.

> Closing this for the above reasons; I think it's an interesting idea, but doesn't feel right for tidyr yet.

**Structure:** [Acknowledge merit] + [Question fit: "doesn't feel right for X yet" / "is Y the right place?"]

### Redirect Diagnosis

The contributor is looking at the wrong layer or package. Gently suggest a different direction.

> This looks more like a stringr issue?

**Structure:** [Suggest alternative diagnosis, often as a question]

## Choosing the Right Pattern

Use these heuristics to identify which pattern fits:

| Signal in the issue | Pattern to use |
|---|---|
| Reporter hit a bug in a deprecated/superseded function | **Won't Fix — Superseded** |
| Request is reasonable but the function/feature is intentionally designed this way | **Design Philosophy** |
| Reporter's code has a fixable mistake or there's an existing alternative | **Workaround** |
| Reporter has a wrong mental model of how the function works | **Clarification** |
| Request is valid but implementation cost is too high or architecture is unclear | **Effort Assessment** |
| Idea is interesting but belongs in a different package or isn't ready | **Scope** |
| The bug or behavior originates in a dependency, not this package | **Redirect Diagnosis** |

**When multiple patterns apply:** Lead with the most helpful one. If someone misunderstands behavior AND there's a workaround, teach the root cause first, then offer the alternative. If something is superseded AND there's a migration path, the superseded pattern already includes the path forward.

**When the issue is just a duplicate or already fixed:** Use the mechanical one-liner. No need for explanation or empathy scaffolding — brevity *is* the respectful response.

## What to Avoid

- **Lengthy justifications for simple decisions.** If it's "no," explain briefly.
- **Defensive tone.** Never "that's how it works because..." without explaining the principle.
- **Dismissive language.** No "obviously," "as we've said before," "this doesn't make sense."
- **Over-apologizing.** One "sorry" or "unfortunately" is enough.
- **False promises.** Don't say "we'll look into it" when you won't.
- **Hedging.** "Maybe later," "we'll think about it" — be clear about the decision.
- **Passive aggression.** No "As we've said before..." or implications the contributor should have known.
- **Condescension.** Even when closing something obvious, stay matter-of-fact.

## Tone Calibration

- **Honesty about constraints:** "Unfortunately," "it's not clear to me," "there are unknowns" — be genuine about what you don't know.
- **Owned opinions:** "I don't think...", "we believe...", "I guess that was done..." — not deflection.
- **Gratitude where warranted:** "Thanks for the report," "thanks for using X" — acknowledge that the person took time.
- **Humor sparingly:** Only as genuine personality, never to soften a blow or at the contributor's expense.

## Applying This Skill

When asked to draft a response:

1. **Identify the pattern.** Which closure archetype fits? (Duplicate, won't-fix, design philosophy, workaround, clarification, effort assessment, scope, redirect)
2. **Draft the response** following the relevant structure.
3. **Check:** Does it explain *why*? Does it validate before declining? Is there a path forward? Is it as short as it can be while still being clear?
4. **Present the draft** for the maintainer to review and adjust to their voice.
