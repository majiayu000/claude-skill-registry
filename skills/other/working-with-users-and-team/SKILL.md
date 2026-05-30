---
name: working-with-users-and-team
description: Use when gathering or interpreting requirements, estimating effort, or communicating with stakeholders/customers about what to build
---

# Working With Users and Team

## Overview

Restate requests in *different* words and test reactions, separate estimates from targets from commitments, and start from yes when a request lands. Human-to-human collaboration material (pairing, rotation) lives in `principles.md` for attribution only.

## When to invoke

Invoke when you're about to:

- Write down or interpret a requirement from a customer, PM, designer, or stakeholder
- Give a number ("how long will this take?", "when can we ship?", "how many users can it handle?")
- Push back on, accept, or reshape a feature request
- Talk to a customer, demo a feature, or write a release note that frames the change to non-developers

### Non-triggers — do NOT invoke for

- Fixing an isolated bug whose reproducer is already in a failing test
- Renaming, formatting, or import-only changes
- Adding a unit test that pins down already-agreed-on behavior
- Internal refactor with no user-visible change (use `before-you-refactor`)
- Routine dependency bump or config tweak
- Reviewing code for technical quality — domain skills (`clean-code`, `security-and-trust-boundaries`, etc.) handle code review

## Checklist

Run the relevant items. If a request crosses areas (a UX call with an estimate attached), run each.

1. **Restate the request in different words, then ask one clarifying question that distinguishes two competing interpretations.** Do not parrot the user's words back — they did not mean what they told you. Example: user says "I want a customer dashboard." Restate: "So an at-a-glance view a salesperson opens once a day to spot accounts that need attention?" Then ask: "Is this for the salesperson, or for the customer themselves to log into?" *(Jackson, 97/97.)*
2. **Probe context with vocabulary swaps.** When the user says "client" or "user" or "customer," substitute the other terms in your reply and watch the reaction. A mismatch in the casual term shows where you and the user disagree on what a word means. *(Jackson, 97/97.)*
3. **Use a visual aid for layout, color, or workflow ordering.** Whiteboard, mockup, or prototype. Verbal descriptions are how the "I said black, I meant white" demo happens. *(Jackson, 97/97.)*
4. **You are not the user.** *(Colborne, 97/3.)* Users do not share your mental models or care how the software is built. Before adding a UI affordance, list two alternative paths a non-power-user might take and confirm both work. Place help at the point of action (inline hint, tooltip on the control), not in a sidebar a stuck user will not see.
5. **When surfacing a question or blocker, deliver context.** What you tried, what you expected, the smallest reproducer. Don't just state the problem. *(Brush, 97/36.)*
6. **Start from yes — ask "why?" before you object.** *(Miller, 97/77.)* Find the underlying need; often the request is achievable as stated, and sometimes voicing the reason makes the original objection look wrong. If after the why the request still cannot work, propose the closest thing that does, or escalate — never silently refuse.
7. **Before giving a number, name which of three things is being asked for** *(Asproni, 97/50)*: an **estimate** (approximate calculation from data, never spuriously precise), a **target** (a desired business outcome), or a **commitment** (a promise to deliver specified scope at specified quality by a specified date). These are independent. A target is not an estimate. A commitment should be *based on* an estimate, not negotiated against one.
8. **Refuse to compress an estimate by negotiation.** If you said three weeks and the PM says "I can give you two," that is a target, not a new estimate. Either reduce scope, change the team, or accept that the target will miss — do not relabel.

## Red Flags

| Thought | Reality |
|---|---|
| "The user said they want X — I'll just build X." | What users say and what they do diverge. Restate in *different* words and ask one question that distinguishes interpretations. (97/97) |
| "I'll restate the requirement word-for-word so they know I heard them." | Verbatim restatement confirms the words, not the meaning. Restate in different words to surface the gap. (97/97) |
| "I know how a user will use this — I designed it." | You are not the user. Walk the non-power-user path before shipping the affordance; place help at the point of action, not the sidebar. (97/3) |
| "Two weeks is fine — I'll just commit to it." | A target accepted under pressure is not an estimate. Name what's being asked for: estimate, target, or commitment. (97/50) |
| "I'll give a precise number so it sounds credible." | Spurious precision (4.2 days) signals a target dressed as an estimate. Give a range from data, or say you do not have data yet. (97/50) |
| "The request is dumb — I'll push back and explain why." | Start from yes. Ask why first. The reason often reveals a real constraint, and sometimes the objection collapses. (97/77) |
| "I'll just escalate — someone will know." | Without what-you-tried, what-you-expected, and a reproducer, you are asking for magic. Deliver context with the question. (97/36) |

## What "done" looks like

- [ ] You restated each interpreted requirement in *different* words and got confirmation, not just nods.
- [ ] Any number you gave is labeled as estimate, target, or commitment, and a precise number (e.g., 4.2 days) is replaced by a range or refused.
- [ ] You started from yes on the request, asked why, and either accepted, reshaped with the asker's agreement, or escalated — you did not silently refuse.
- [ ] If the change is user-facing, two alternative non-power-user paths through the new affordance have been walked.

## Principles in this skill

| # | Principle | Author |
|---|---|---|
| 97/3 | You Are Not the User | Giles Colborne |
| 97/36 | The Guru Myth | Ryan Brush |
| 97/50 | Learn to Estimate | Giovanni Asproni |
| 97/77 | Start from Yes | Alex Miller |
| 97/97 | Your Customers Do Not Mean What They Say | Nate Jackson |

See `principles.md` for the long-form distillations, citations, and source links.
