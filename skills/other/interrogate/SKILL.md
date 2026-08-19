---
name: interrogate
description: Make the user defend a proposal they committed to. Use when a proposal is committed but its decisions are undefended.
---

## Extract

From the conversation/context/user:

- The **proposal** as committed — locked, chosen, or declared.
- Its **decisions** — the choices inside it the user has not defended.

## Gate

Proceed only when: the proposal is committed, its decisions need the user to defend them, and a decision falling under questioning would change what gets built.

Anything else, say which in one plain line — never interrogate anyway:

- The user hasn't committed, and holds what they cannot yet say → use **elicit** skill — there is nothing to defend, something to draw out.
- The user hasn't committed and is still weighing — nothing locked, chosen, or declared → there is nothing to defend yet.
- The user wants a verdict — the proposal exists and they're asking whether it is right, not standing behind it → use **judge** skill.
- Every question the proposal raises is answerable from the repo or the record — nothing needs the user → this is a review, not a questioning: run it yourself, answer each question from what is there, and proceed with what the review finds.
- No decision inside it would change what gets built, whatever the answers → skip the questioning and proceed with the work.

## Steelman

State the strongest case for the proposal as committed — the best reasons it is right — before any attack. Then assume it is wrong somewhere and go find where.

## Press

1. Attack one decision at a time: what breaks if this is wrong, what it traded away, why this over the nearest alternative.
2. Only ask what the user alone can answer. Anything answerable from the repo or the record, answer yourself and move on.
3. Do not accept a vague answer — "fast" gets "fast how, what number?".
4. Sort each answer before moving on:
   - it stands → keep it as the decision's defence
   - it changes the proposal → record it as an amendment
   - it exposes another decision the user has not defended → add that decision and press it next.
5. Continue until every surfaced decision carries a defence or an amendment in the user's own words. Stopping earlier is allowed only by naming the decisions left undefended.

## Output

The amended proposal is the result. Hand it back whole: each surfaced decision with its defence or its amendment, in the user's own words; any decision left undefended, named as such.

Then check whether the proposal is settled enough to return to the work it interrupted: would anything still unresolved change what gets built?

- Nothing would — or what would is a decision the user named undefended → proceed with the proposal as it now stands; the named decisions ride with it as the user's accepted risk.
- The user holds something they could not say under questioning → use **elicit** skill.
- An answer's words admit two readings that would build different things → use **clarify** skill.
- A claim about something that exists needs a verdict → use **judge** skill.
- The user is missing something already settled → use **explain** skill.

The questioning is spent once the loop ends — anything further runs under the branch picked here, never as another round of questioning.
