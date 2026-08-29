---
name: filing-issues
description: Use when filing one or more GitHub issues for planned work — "file an issue for this", "turn this plan into issues", "open a tracking issue". Covers filing everything on skyf0xx/hedgehog regardless of which repo's code changes, whether to split a plan into a tracking issue plus sub-issues, which account files the issue, labels, and acceptance criteria. For how to word an issue, see the pr-writing skill.
---

# Filing issues

The mechanics of getting planned work into GitHub. `pr-writing` owns how
an issue is worded — title shape, the Why/What structure, `<details>`
folding, and style. This skill owns everything before and around that.

## Which repo

Every issue is filed on `skyf0xx/hedgehog`, never on a core's own repo
(e.g. the one shipping `full-stack-app` or `pwa-app`) — one issue queue
to track and review, regardless of which repo's code changes.

When the fix actually lands in a core repo, open the issue body with a
line naming that repo and linking it, so a contributor knows where the
PR belongs even though the issue itself doesn't live there.

## One issue or several

Split when the parts have different reviewers, different repos, different
risk, or can be worked in parallel. Keep one issue when the work is a
single reviewable change, even a large one.

A split gets a tracking issue plus sub-issues:

- The tracking issue carries the Why, the scope boundary, and a numbered
  list of sub-issues with a one-line description of each.
- Each sub-issue is self-contained — someone picking it up should not
  have to read the tracker to know what to do.
- State the dependency edges explicitly, including their absence:
  which can be picked up now, which blocks which, and which merely
  prefer an order without blocking.
- File the tracker first so sub-issues can reference its number, then
  patch the tracker with the real numbers once they exist.
- Comment `Part of #<tracker>` on each sub-issue.

## Which account files it

Issues go out as the user's own `gh` session by default.

Some projects have a bot identity for maintainer actions. Use it only
when the user asks for it by name. A bot voice tuned for short notes
does not apply to a planned-work issue — write the issue at full length
and say that is what you are doing.

## Labels

Read the target repo's labels before filing (`gh label list --repo
<owner/repo>`) — the engine repo and the core repos carry overlapping but
not identical sets.

Apply what is verifiable at filing time: a type label (`feature`, `bug`,
`documentation`) and any `risk:` label the change clearly earns.
`good-first-issue` fits an issue that is genuinely self-contained with an
obvious done state. Leave `size:` labels alone — they describe a diff
that does not exist yet.

## Acceptance criteria

End every issue with a checkbox list a contributor ticks off and a
reviewer checks against. Each line is one observable outcome, not a
restatement of the task list.

- Testable by inspection or a command, not by judgment. "`pnpm nx test
  mobile -- src/{module}/` passes on generated output" — not "the
  generator works well."
- Include the things that must *not* change: the existing behavior that
  still has to pass, the version that must not be bumped.
- Cover the whole change. A criterion nobody can check is noise; a
  missing one is a gap a reviewer has to find themselves.

On a tracking issue, the criteria are the sub-issues plus the end-to-end
outcome that proves the whole set landed.

## Before filing

Verify every claim the issue makes about existing behavior, and cite it
`file:line`. An issue is public and durable — a wrong claim in one sends
a contributor down a path that does not exist.

Confirm the split and the identity with the user before creating
anything — the repo is fixed, not a decision to make each time. Issue
creation is public and hard to reverse.
