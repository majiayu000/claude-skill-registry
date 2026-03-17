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

## Automated Invocation (from evolve_loop)

The evolution loop automatically invokes this skill at **8am UTC daily** when there's highlight-worthy work from today's successful tasks. It passes task context via `--from-task`.

### When invoked with `--from-task`

Parse the task info and compose an appropriate highlight:

1. **Parse the context** (e.g., `expand-topic: concepts/qualia.md`)
2. **Read the relevant file** to understand what was created/changed
3. **Compose an engaging highlight**:
   - **Title**: 5-10 words, engaging, makes people want to click
   - **Description**: 1-2 sentences, max 280 chars
   - **Type**: new-article, insight, research, or refinement
   - **Link**: wikilink to the content
4. **Call the CLI** with `--tweet` flag

### Example

Input: `--from-task 'expand-topic: concepts/quantum-timing.md' --tweet`

Steps:
1. Read `obsidian/concepts/quantum-timing.md`
2. Understand the article's thesis
3. Compose highlight and run:

```bash
uv run python scripts/highlights.py add \
  "Quantum Timing: When Mind Meets Matter" \
  "New article maps timescales from femtosecond decoherence to 300ms decisions, showing how quantum effects must operate within neural constraints." \
  --type new-article \
  --link "[[quantum-timing]]" \
  --tweet
```

The `--tweet` flag triggers the full chain: **add → commit → push → wait for deployment → tweet**.

### Task type to highlight type mapping

| Task Type | Highlight Type |
|-----------|---------------|
| expand-topic | new-article |
| research-topic | research |
| research-voids | research |
| deep-review | insight |
| coalesce | new-article |
| apex-evolve | new-article |
| backlog | (infer from content - see below) |

### Handling backlog content

When invoked with `--from-task 'backlog: obsidian/path/to/file.md'`, this means we're highlighting existing content that hasn't been featured in the last 90 days. This is NOT necessarily new work—it's content worth sharing that hasn't had recent attention.

1. **Read the file** at the given path
2. **Determine highlight type** from the file's directory:
   - `obsidian/topics/` → new-article (even if old, it's an article)
   - `obsidian/concepts/` → new-article
   - `obsidian/apex/` → new-article
   - `obsidian/voids/` → insight (these explore cognitive limits)
3. **Compose an engaging highlight**:
   - The title and description should present the content as interesting/worth reading
   - Don't frame it as "new" if it's older content—just make it sound appealing
   - Focus on the most compelling aspect of the article
4. **Call the CLI** with appropriate flags

## Important

- **Max 280 characters** for descriptions (Twitter-ready for future integration)
- **Max 1 highlight per day** (enforced by the manager)
- **Always use wikilinks** for the link field
- **Skip routine maintenance** - only highlight interesting work
- The highlights page auto-trims to 20 items