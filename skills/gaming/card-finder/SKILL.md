---
name: card-finder
description: Find Magic cards for compact golden-test scenarios using existing repo goldens, curated references, and Scryfall search recipes.
---

# Card Finder

Use this when the task is "find the right Magic cards for a test" rather than
"write the golden itself."

Read only what you need:

- `references/golden-test-cards.md` for repo-proven cards and query patterns

## Workflow

1. Start with the curated reference. It is intentionally biased toward reusable,
   general-purpose test cards, not every niche card that happens to appear in a
   current golden.
2. If the mechanic is not covered there, run the helper script:

   ```bash
   uv run python scripts/find_test_cards.py --list-recipes
   uv run python scripts/find_test_cards.py --recipe zero-mana-body
   uv run python scripts/find_test_cards.py --recipe trigger-prompt --filter 't:white'
   uv run python scripts/find_test_cards.py --query 'game:paper unique:cards function:clone is:spell mv<=4 order:cmc direction:asc'
   ```

3. Bias toward cards that reduce turns, prompts, and unrelated board text:
   fast mana, zero-mana bodies, single-card setup, and deterministic triggers.
4. When giving recommendations, return a short list with "why this is useful in
   a golden" and "what noise it adds." Use existing repo goldens as evidence for
   what works, but do not turn the curated list into an index of one-off
   scenario cards.

## Query Patterns

- Start most searches with `game:paper unique:cards` so results match paper
  XMage coverage and collapse duplicate printings.
- Use `order:cmc direction:asc` when you want the cheapest setup pieces first.
- Use `function:` tags for broad roles such as `function:clone`,
  `function:removal`, or `function:counterspell`.
- Use `o:` for Oracle text fragments, `fo:` when reminder text matters, and
  `o:/.../` regex when you care about text shape such as `o:/^When/`.
- Use `is:` flags for UI-heavy cards: `is:mdfc`, `is:split`, `is:transform`.
- Use `!"Exact Name"` when you already suspect a card and want all printings or
  details for that exact card.

If the user is also writing a golden, hand off to `golden-test` after the card
selection is narrowed down.
