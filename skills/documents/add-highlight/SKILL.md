---
name: add-highlight
description: Add an item to the highlights page. Max 1 per day.
---

# Add Highlight

Add a notable item to the public highlights (What's New) page.

## When to Use

- After writing a new article worth sharing
- When research reveals something interesting
- When a review finds a significant insight
- Any time something is worth publicising
- Manual invocation: `/add-highlight [topic]`

## Instructions

### 1. Check Rate Limit

Use the CLI to check if we can add today:

```bash
uv run python scripts/highlights.py check
```

Only 1 highlight per day is allowed. If already added today, skip silently and note in output that a highlight was already added.

### 2. Compose Highlight

Determine the content:

- **Title**: Short, engaging (5-10 words). Should make someone want to click.
- **Description**: 1-2 sentences explaining what's new or interesting. Max 280 characters (Twitter-ready).
- **Type**: One of:
  - `new-article` - A new piece of content was created
  - `insight` - An interesting finding from review or analysis
  - `research` - Research notes or discoveries
  - `refinement` - Significant improvement to existing content
- **Link**: Wikilink to the relevant content (e.g., `[[hard-problem-of-consciousness]]`)

### 3. Add via CLI

```bash
uv run python scripts/highlights.py add "Title Here" "Description of what's interesting, max 280 chars." --type new-article --link "[[article-name]]"
```

### 4. Post to Twitter (Optional)

If Twitter is configured (credentials in `.env`), add the `--tweet` flag:

```bash
uv run python scripts/highlights.py add "Title" "Description" --type new-article --link "[[article]]" --tweet
```

To test formatting without posting:

```bash
uv run python scripts/highlights.py add "Title" "Description" --type new-article --link "[[article]]" --tweet --dry-run
```

**Note:** Twitter posting is optional. If credentials aren't configured, the highlight is added and a warning is logged. Twitter failures never block highlight creation.

### 5. Verify Addition

The CLI will confirm success or report rate limiting.

## Content Guidelines

**Good highlights are:**
- Genuinely interesting to a general audience
- Understandable without deep context
- Engaging enough to click through
- Connected to The Unfinishable Map's philosophical mission

**Skip these (not highlight-worthy):**
- Routine maintenance (validate-all, check-links)
- Minor refinements with no new insight
- Failed or blocked tasks
- Internal workflow changes

## Examples

### New Article
```bash
uv run python scripts/highlights.py add \
  "Why Materialism Can't Explain Consciousness" \
  "New article argues that all forms of materialism fail to account for subjective experience. The hard problem isn't just unsolved—it may be unsolvable in principle." \
  --type new-article \
  --link "[[materialism]]"
```

### Research Insight
```bash
uv run python scripts/highlights.py add \
  "Buddhist Perspectives Challenge Western Assumptions" \
  "Research into Buddhist philosophy reveals that the self-consciousness problem looks different from a tradition that questions the self's existence entirely." \
  --type research \
  --link "[[buddhist-perspectives-meaning]]"
```

### Review Finding
```bash
uv run python scripts/highlights.py add \
  "Decoherence Timescales Present Real Challenge" \
  "Pessimistic review identified that quantum decoherence in warm brains happens in femtoseconds—nine orders of magnitude faster than neural processes." \
  --type insight \
  --link "[[consciousness-selecting-neural-patterns]]"
```

## Integration with /evolve

The `/evolve` skill automatically considers adding a highlight at the end of each session. You don't need to manually call `/add-highlight` after evolve—it handles this.

## Important

- **Max 280 characters** for descriptions (Twitter-ready for future integration)
- **Max 1 highlight per day** (enforced by the manager)
- **Always use wikilinks** for the link field
- **Skip routine maintenance** - only highlight interesting work
- The highlights page auto-trims to 20 items