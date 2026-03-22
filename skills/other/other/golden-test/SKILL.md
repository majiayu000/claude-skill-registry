---
name: golden-test
description: Write or update low-noise golden prompt tests in puppeteer/tests, including minimal decks, replay scripts, and golden regeneration.
---

# Golden Test Workflow

Use this when adding a new gameplay golden or tightening an existing one.

Read only what you need:

- `doc/golden-prompts.md` for the full model
- `puppeteer/tests/golden_helpers.py` for deck constants and `run_golden_scenario`
- One or two nearby examples such as `test_golden_bolt_on_stack.py`, `test_golden_clone_copies_memnite.py`, or `test_golden_dark_depths_combo.py`

## Goal

Capture the smallest realistic game history that still exercises the mechanic under test.

Golden tests get noisy fast. Prefer:

- Fast mana (`Black Lotus`, `Lotus Petal`, cheap rocks) over waiting extra turns for lands
- Zero-mana permanents over filler turns when you just need board presence
- `pass_priority(until=...)` yields to jump over irrelevant phases
- Opening-hand setup over draw-step setup when the draw itself is not the mechanic

Avoid:

- Spending turns just to make mana if fast mana can do it
- Extra land plays or combat skips after the interesting state already exists
- Long scripts that only exist because the deck was not designed tightly enough

If the mechanic fundamentally requires time to pass, keep the script short anyway and make each turn do real work.

## Deck Design

Golden decks are deterministic. The first 7 cards are the opening hand because shuffling is disabled.

Rules:

- Exactly 60 cards
- Put every setup piece needed for the scenario in the first 7 cards unless the draw itself matters
- Put reveal targets, later draws, or pile-split cards immediately after the opening hand
- Pad the rest with basics unless a later specific draw is required
- Use real set codes and collector numbers from existing decks or `Mage.Sets`

If you know the mechanic but not the exact cards, use `card-finder` before
inventing a deck from memory. Start with
`.claude/skills/card-finder/references/golden-test-cards.md`, then use
`uv run python scripts/find_test_cards.py --list-recipes` or a targeted
`--query` search. Prefer reusable utility cards from that reference first, then
use the helper to find narrower one-off cards when the scenario really needs
them.

Predict short IDs in comments and replay scripts. IDs are assigned alphabetically by card name starting at `p3` (`p1`/`p2` are players).

Prompt and export goldens now keep literal MCP short IDs and literal stripped bridge output. Embedded JSON key order is normalized, but raw XMage HTML handle noise (`object_id='UUID'`, `</font> [abc]`) should be removed at the source boundary instead of redacted in goldens.

## Script Design

Use the standard mulligan preamble:

```python
{"name": "pass_priority", "arguments": {}},
{"name": "choose_action", "arguments": {"choice": "0"}},
{"name": "pass_priority", "arguments": {}},
{"name": "choose_action", "arguments": {"choice": "no"}},
```

Prefer `choice="pN"` for stable card/permanent selection when you know the ID.

Use `pass_priority` for phase advancement and `choose_action` for the decision itself.

Important patterns:

- After a land drop, the next `pass_priority` auto-passes once before stopping again
- `choose_action` can chain through pending follow-up actions without running the auto-pass loop
- Use chained `choose_action` calls when you need the stack to stay intact
- Use `pass_priority(until="declare_attackers")`, `until="postcombat_main"`, `until="my_turn"`, etc. to skip irrelevant prompts cleanly

Low-noise heuristics:

- If a test takes multiple turns only to hit a mana threshold, redesign the deck
- If the script ends with an unrelated land play, remove it and yield to the phase you actually need
- If you need `Fact or Fiction`, put the split cards at positions 8-12 instead of drawing for several turns
- If combat is not the mechanic, avoid creating creatures that force extra attacker prompts

## File Changes

Touch the minimum set of files:

- Deck: `puppeteer/tests/decks/<name>.dck`
- Test: `puppeteer/tests/test_golden_<name>.py`
- Golden helper constant if adding a new deck path
- Generated files under `puppeteer/tests/golden/`

Mark gameplay goldens with `@pytest.mark.golden`.

If you are adding a helper/unit test around golden infrastructure rather than a
real golden integration, do **not** name it `test_golden_*.py` unless it is
actually marked `@pytest.mark.golden`; the golden naming convention tests
enforce that contract.

## Regeneration And Validation

Use the make targets only. Direct `pytest -m golden` is blocked.

For focused iteration:

```bash
make regen-golden K=<name>
```

Then inspect the generated prompt/export and confirm:

- The intended board or stack state is present
- There are no `invalid_choice` or similar tool errors
- The script did not take irrelevant actions after the scenario was already established

After the targeted goldens are right, run:

```bash
make test
```

`make check` also covers golden tests in CI, but for Python changes in `puppeteer/`, at minimum run `make test` locally.

## Failure Triage

If regeneration fails:

- Wrong IDs or choice indexes: re-check alphabetical ordering and the exact prompt you stopped on
- Unexpected extra prompts: use `until=` yields or remove cards causing irrelevant actions
- Needing too many turns: redesign the deck around faster mana instead of scripting around the slowness

Do not paper over nondeterminism. If a golden is flaky, use the `investigate-golden-flake` skill and fix the root cause.
