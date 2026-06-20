---
name: reflect-outcome
user-invocable: false
description: |
  Detects when a stated outcome names a specific instance — a mechanism-as-means or a single named product — where a category was meant, and returns a neutral fork for the lead to show the user, or nothing. Invoked by launch commands at outcome capture, in place of the verbatim echo.
---

The user stated an outcome in their own words. Read it for ONE structural pattern — **a specific instance named as the way to reach a broader end the user's outcome also states** — which can silently collapse the team onto that one point and orphan the alternatives. Fire ONLY when BOTH are present: (1) a named mechanism, product, or instance, AND (2) a wider goal **stated anywhere in the user's outcome** — not necessarily in the same sentence as the named instance — that the named thing is merely one way to serve. The named thing being *narrower than that stated wider goal* is the discriminator. **Infer nothing:** if no wider end is stated, do not fire (a category you could infer from the name is not a stated end), and never predict that foreclosure will happen — detect only the divergence the user's own words make plain. A bare concrete noun, mechanism or product, with no stated wider end does NOT fire; that over-firing is the alarm-fatigue failure this exists to avoid. The cheap, incumbent-first dismiss is what makes firing on a real signal safe.

- **Mechanism-as-means:** "force a resume *so it can nudge* a forgotten prospect" → "nudge" is one way to reach the wider stated goal "resurface a forgotten prospect" → FIRE. Contrast "add a retry queue for failed webhooks" → "retry queue" IS the whole ask, no wider goal it under-serves → **stay SILENT**.
- **Proper-noun-specific-instance:** "integrate with Salesforce *so sales can see deals*" → the wider end "sales can see deals" is stated and Salesforce is one way to reach it → FIRE. Contrast bare "store it in S3," "send a Slack notification," "cache it in Redis," "deploy on Vercel" → the product IS the ask, no wider end stated → **stay SILENT**. Do NOT fire on the class you could infer from the product name — that inference is the alarm-fatigue over-fire; an existing-integration collision with no stated end drops to the Research-phase repo check instead.

Scan the whole input, not a single clause: if more than one pin is present, fork on the single most consequential one; if it is genuinely ambiguous which matters most, return `NO FORK`.

The same *infer nothing* applies to the LINK across sentences: couple a goal and an instance only when the serve-relationship is plain in the user's own words; a link you would have to infer is `NO FORK`. When the outcome names more than one instance, pair each only with the end it plainly serves — never fire an instance against an end that belongs to a different named thing.

Read the WORDING only. Do not read the codebase. Do not grade quality. Do not hunt for missing detail — over-specification is the failure here, not under-specification.

**Common case — nothing pinned:** return exactly `NO FORK`. The lead shows the user nothing and carries the outcome forward as-is. Do not hedge, apologize, or manufacture a concern; a clean pass is a first-class result. Fire only on a citable pinning word that is actually in the user's text — no citable word, no fork.

**A pinned instance is present (either shape):** return a ready-to-render AskUserQuestion object the lead shows verbatim and does not author. Build it to this grammar:
- **Subject** is the team or the reading, never the user — "the team would read this as…", never "you didn't specify…".
- **Forward-looking:** name the consequence the user can veto, not a deficiency they must defend.
- **Pivot on the user's OWN word**, quoted, as a means/ends substitution — introduce no noun they didn't write.
- **Only remedy is to pick a reading** — never to add more detail.

Shape (draft NO goal anywhere — not in the stem, not in either label; the open pole asserts only that other ways exist, naming none):
- `question`: *"'\<their word>' reads as the way to do this — the team builds only what the wording pins. Did you mean \<their word> specifically, or are you open to other ways to do this?"*
- `header`: "Outcome"
- `options` (exactly two — incumbent first, both first-person in the user's own voice):
  - *"Yes — \<their word> specifically is what I want."* — that specific one, exactly as worded
  - *"I'm open to other ways to do this — \<their word> was just how I put it."* — \<their word> was one example, not the requirement

**Neutrality bar — all four must hold, or return `NO FORK` instead:** (1) introduce no noun the user didn't write; (2) assert no quality grade; (3) the user's verbatim still briefs the team without your words leaking in; (4) the user keeps an unforced choice to leave the wording exactly as-is.

**Resolving the choice (the lead handles the answer — the skill stores nothing):**
- **Option A — keep the named instance:** nothing to record. The verbatim already contains the word and flows to the briefs unchanged.
- **Option B — open to other ways:** ask the user to restate the outcome in their own words with an OPEN prompt ("tell me what you'd like to happen") — never a drafted "did you mean X?", which would re-introduce the assembled-goal the fork exists to avoid. The restatement re-enters this reflection (a fresh outcome, usually `NO FORK`) and BECOMES the verbatim of record, flowing to the briefs unchanged. Store no separate supplement — the user's own revised words carry the signal that the original word was incidental.
- **If a re-authored outcome forks again,** give it the same two-option treatment — each pass is a fresh user-authored outcome, so the incumbent option (A) is the terminator; there is no separate loop counter.
