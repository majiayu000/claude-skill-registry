---
name: fix-what-i-pointed-at
description: Pick up the bugs a human flagged by pointing at them in the running app, each arriving with the element, the note they typed, and the source file and line. Use when the user says they marked or flagged something, when starting a session on an app someone has been clicking through, when a designer or PM has left feedback in the UI, or when the user describes a problem as "that button there" without saying which file.
license: Apache-2.0
metadata:
  version: 2.14.0
  homepage: https://www.reticle.sh
  repository: https://github.com/reticlehq/reticle
---

# The human pointed at the bug. Go fix it.

"The spacing on that card is wrong" is unactionable in chat and precise in the app. **Reticle**'s running app has a **Flag a bug** control: the human clicks it, points at an element, and types what is wrong. Each flag becomes a mark carrying the element, the note, and the `file:line`, so the round trip that usually costs a screenshot, a description, and two clarifying questions costs one call.

Not installed? `RETICLE_INSTALL_SOURCE=npx_skill npx @reticlehq/server@latest init`, then the [`install-and-verify`](https://github.com/reticlehq/reticle/blob/main/skills/install-and-verify/SKILL.md) skill.

## Drain the marks

```
reticle_session({ action: "review", sessionId })
```

```json
{
  "marks": [
    {
      "id": "m1",
      "note": "this button is misaligned",
      "label": "button \"Pay\"",
      "source": { "file": "src/Checkout.tsx", "line": 42 },
      "fix": "Open src/Checkout.tsx:42 and fix: this button is misaligned."
    }
  ],
  "pendingCount": 1
}
```

**Check this at the start of a session**, and again whenever the human has been in the app. Reading never consumes a mark, so list → fix → verify → resolve is safe to run in any order.

## The loop

1. **Read** the marks. Group them if several point at the same file: one edit often answers three.
2. **Open** `source.file` at `source.line`. This is the whole point: no hunting for which component rendered that button.
3. **Fix** what the `note` asks for. If the note is ambiguous, the element label and its source usually disambiguate it. Ask the human only when they genuinely do not.
4. **Verify in the app**, do not eyeball it. Re-drive the affected control with `reticle_act_and_wait` and name the consequence, or `reticle_inspect` the element for a layout or theme complaint. A visual fix confirmed by looking at it is how the mark gets reopened.
5. **Resolve** it:

```
reticle_session({ action: "review", sessionId, resolve: "m1" })
```

Resolve only after the fix is verified. A resolved mark is a promise to the human that the thing they pointed at is done.

## When you cannot fix one

Say so against that mark and leave it unresolved. A mark silently dropped is worse than an open one: the human believes it was handled and finds out later. If the note describes intended behaviour rather than a bug, say that too, and let them decide.

## Report back in their vocabulary

They pointed at "that button". Report on "the Pay button on checkout", with what you changed and the evidence it now works. Marks come from people who are looking at the screen, not at the repo, so a report full of file paths and no user-facing language answers the wrong question.

---

Everything else: `curl https://docs.reticle.sh/llms.txt`. If a mark arrived without a usable source pointer, that is worth a `reticle_feedback` with `kind: "gap"`.
