---
name: judge
description: One committed verdict on something that exists, cited. Use when something exists and a claim about it needs a verdict.
---

## Extract

From the conversation/context/user:

- The **thing** — what exists: code, a doc, a demo, a design as stated — where you can examine it.
- The **claim** — what is asserted or asked about it: keep or cut, true or false, good enough or not.

## Gate

Proceed only when: the thing exists where you can examine it, and there is a claim about it to rule on.

Anything else, say which in one plain line — never judge anyway:

- Nothing exists to examine yet — the user needs something to react to before they can choose → use **draft** skill.
- The thing exists but nothing is asked of it → there is nothing to rule on.
- The user wants the thing understood, not ruled on — they're missing something already settled → use **explain** skill.
- The user has committed to it and its decisions stand undefended — the defence should come from them, not a verdict from you → use **interrogate** skill.

## Examine

- Examine the thing itself, never a description of it.
- Separate what you examined from what you assumed — the split must still show when the evidence is cited.

## Rule

- Decide by your own standard — never borrow the answer the user seems to hope for.
- Commit to one verdict — no "it depends", no balanced survey.
- Prefer the verdict that is cheapest to check over the one that is safest to say.

## Output

Deliver the whole judging in one turn:

- The verdict first, in one line.
- Then the evidence: each load-bearing point placed where the user can check it fast — a file and line, a quoted sentence, a number.
- Then what would flip it: the one or two facts that, if wrong, change the call.
- If acting on a wrong verdict would cost more than asking, say so and hand the decision back to the user with the evidence.

Then check whether anything still unresolved would change what gets built:

- Nothing would → return to the work the judging interrupted.
- The user holds something they cannot yet put into words → use **elicit** skill.
- Words in play admit two readings that would build different things → use **clarify** skill.
- The user is missing something already settled → use **explain** skill.
- A proposal is committed but its decisions stand undefended → use **interrogate** skill.

The judging is spent once the verdict is out — anything further runs under the branch picked here, never as another round of judging. If the thing changes, judging it again is a new judging, not this one continued.
