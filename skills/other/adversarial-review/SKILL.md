---
name: adversarial-review
description: Adversarially review something just built — presume it is broken and find where. Use after implementing a feature, finishing a build, or before shipping, or whenever ATLAS or Boss wants a hostile second opinion on a diff, a running app, or a whole codebase. Spawns clean-context reviewers with opposing lenses (correctness, security, empty-world) and reproduces every finding by running the target before believing it. Distinct from /code-review, which statically reads a diff and never runs the app.
---

# Adversarial review — presume it broken, find where

A normal review reads code and looks for reasons to approve it. An adversarial review starts from the
opposite prior: **this was just built, it is presumed broken, and the job is to find where.** The
builder believes in their work — that belief is exactly the blind spot. So the reviewer must be
incentivized to find failure, not confirm success, and must work *without the builder's context* so it
cannot inherit the builder's assumptions.

This skill is the canonical adversarial-review protocol for ATLAS. Reach for it autonomously after
building anything non-trivial, before shipping, or when handed unfamiliar code to harden.

## When to use it — and which review

- **Use this** when you want the thing *attacked*: a feature you just finished, a build before
  delivery, a flow you suspect is fragile, an unfamiliar codebase you must trust.
- **Use `/code-review` instead** for a fast, conservative pass over a **diff or PR** — it statically
  reads the change for bugs and cleanups, scores confidence, and **never runs the app**. That is the
  right tool for routine change review.
- **The line between them:** `/code-review` reads; adversarial-review *runs*. This skill presumes
  breakage, fans out diverse hostile lenses in clean contexts, and **reproduces findings against the
  live target** before believing them. Heavier, empirical, used deliberately.
- **Scale down, don't skip:** for a small change one hostile reviewer is enough. Don't fan out a fleet
  to attack a typo fix — deliberating everything ships nothing.

## The four invariants (what makes a review adversarial)

1. **Presumed-broken mandate.** Every reviewer gets one instruction: *"this was just built and is
   presumed broken; find where."* Never "check if it looks ok."
2. **Context isolation.** Reviewers run in **clean contexts** (separate subagents) — they get the
   target and the mandate, not the build's rationalizations. A separate context window is the closest
   thing to a genuine second opinion.
3. **Empirical reproduction.** A finding is a hypothesis until reproduced against the real target.
   Run it. A finding that can't be reproduced is an opinion, not a bug.
4. **Senior triage.** Reproduce before fixing, fix what's real, re-verify the fix, and name the false
   alarms. The report is only trustworthy if it admits what wasn't real.

## How to run it

1. **Frame the target and scale.** Name what's under review (a diff, a feature, a running app, a whole
   codebase) and how to exercise it (commands to run, URLs/flows to walk, entry points). Pick reviewer
   count by stakes: 1 for a small change, 3–5 lenses for a feature or build.

2. **Fan out hostile reviewers in clean contexts.** Spawn subagents, each with the presumed-broken
   mandate and **one lens**, blind to each other. Choose lenses that fit the target — typically:
   - **Correctness** — edge cases, off-by-one, race conditions, broken flows, state that lies
   - **Security** — injection, authz/authn holes, secrets in code, unvalidated input, SSRF/path traversal
   - **The empty world** — first run, zero data, no config, expired token: does it still stand up?
   - **Data integrity** — partial writes, lost updates, migrations, constraints that don't hold
   - **Failure & limits** — network/dependency failure, timeouts, huge inputs, concurrent users
   - **UX seams** — error messages, loading/empty states, the run instructions a stranger needs
   (One-shot work dies at the seams and the empty world far more than the happy path — weight those.)

3. **Reproduce every finding.** Before fixing anything, run the target and confirm the failure
   actually happens. Capture the evidence (output, screenshot, failing command). Unreproducible →
   demote to "unconfirmed," don't fix on faith.

4. **Triage like a senior.** Fix what reproduced, re-run to confirm the fix closed it (and opened
   nothing new), and record what looked like a bug but wasn't. If a fix opens a real design fork,
   invoke `free-will`.

## Output — the report

One honest summary:

- **Confirmed & fixed** — what broke, the reproduction, the fix, the re-verification.
- **Confirmed & deferred** — real but consciously not fixed now, and why (goes on the gap list).
- **False alarms** — flagged then disproven. Listing these is what makes the rest credible.
- **Residual risk** — what this pass could not exercise, and what would attack it next.

Never report "no issues found" from a read alone — that claim requires having *run* the lenses and
reproduced nothing. Report what you actually exercised, not what you assume holds.
