---
name: promote
description: Generate X/Twitter release promotion posts with ASCII tables and CodeSnap rendering. Use when writing release posts, promotion tweets, plugin announcements, or preparing social media content for new versions.
effort: medium
---

# /promote — Release Promotion Post Generator

Generate data-driven X/Twitter posts for plugin releases with ASCII cards ready for CodeSnap screenshots.

## When to use

Run `/promote vX.Y.Z` after tagging a release. Optionally add a title: `/promote v2.8.0 "LiveView Streams Overhaul"`.

## Output

All files go to `scratchpad/x-posts/{version}-release.md` (create directory if needed).

The output file contains three sections:
1. **ASCII Card** — box-drawing table for CodeSnap screenshot
2. **Tweet Thread** — 3-5 tweets in proven format
3. **CodeSnap Command** — exact CLI command to render the card
4. **Fact-Check** — every claim with verifiable data source

## Execution Flow

### Step 1: Gather Data

Collect these metrics (all are verifiable commands — run them, don't estimate):

| Metric | How to get it |
|--------|---------------|
| File count + insertions/deletions | `git diff --stat {prev-tag}..{tag}` |
| Skill count | `ls plugins/elixir-phoenix/skills/ \| wc -l` |
| Agent count | `ls plugins/elixir-phoenix/agents/*.md \| wc -l` |
| Iron Law count | Grep for numbered Iron Laws in CLAUDE.md |
| Eval scores | `make eval-all` (run it, report actual numbers) |
| Changelog entries | Read CHANGELOG.md for this version's section |
| Before/after metrics | Depends on release — look for quantifiable changes |

The strongest posts have **before/after comparisons**. Look for changes in CHANGELOG.md that have measurable deltas (line counts, counts of affected files, error rates, coverage numbers).

### Step 2: Write the ASCII Card

The card is the visual centerpiece — it gets screenshotted via CodeSnap and attached to tweet 1.

Rules:
- **Exactly 72 characters wide** (including borders) — consistent with past posts
- Use Unicode box-drawing: `┌─┐│└┘╞═╡╤╪╧` for borders and separators
- Include: version + title, headline stats, before/after table, repo URL
- The table content comes from Step 1 data — pick the 3-5 most impressive changes
- **VERIFY ALIGNMENT**: After writing the table, run a Python script to check every line has the same visual width. Off-by-one errors are the most common problem — em dashes (`—`) and arrows (`→`) are single-width but easy to miscount. Every line between the top `┌` and bottom `└` borders must be exactly 72 visual characters

Also save the ASCII card as a separate `.txt` file at `scratchpad/x-posts/{version}-table.txt` for CodeSnap input.

See `${CLAUDE_SKILL_DIR}/references/templates.md` for the proven card format and past examples.

### Step 3: Write the Tweet Thread

Follow the **hook → findings → details → CTA** structure. Read `${CLAUDE_SKILL_DIR}/references/templates.md` for proven tweet patterns.

**Thread rules (from analytics on 7 posts, 6.9K-9.9K views):**

- **Tweet 1 (Hook)**: Version + one compelling sentence about what changed. Include headline stats (files changed, skills, agents). Repo link here — not in a reply. Add `#ElixirLang #ClaudeCode` hashtags.
- **Tweet 2-3 (Findings)**: The specific changes with numbers. Use numbered lists. Before/after metrics are the highest-performing content type.
- **Tweet 4-5 (Details/CTA)**: Additional changes + soft CTA ("Try it and let me know how it feels"). Link to release page.
- **Max 5 tweets** — casual readers drop off after 4-6. If you have more content, cut the least impactful items.

**Voice and tone:**
- Data-heavy, transparent, no-hype — this is the proven #1 strength
- Write like a builder sharing real numbers, not a marketer
- Concrete numbers over adjectives ("32/40 descriptions rewritten" not "improved many descriptions")
- Never mention API costs or token prices — subscription user, cost per call is irrelevant

### Step 4: CodeSnap Command

Output the exact command to render the ASCII card as an image. The card `.txt` file from Step 2 is the input.

Use the config file at `scratchpad/x-posts/codesnap-claude-dark.json` (dark gradient, tight margins, no watermark):

```
codesnap -f scratchpad/x-posts/{version}-table.txt \
  -o scratchpad/x-posts/{version}-card.png \
  --config scratchpad/x-posts/codesnap-claude-dark.json \
  --title "claude-elixir-phoenix {version}" \
  -l text
```

Then render and verify the image looks correct by reading the output PNG.

### Step 5: Fact-Check

Every claim in the tweets must have a corresponding entry in the fact-check section:

```markdown
## Fact-Check

- File stats: `git diff --stat {prev}..{tag}` (output: N files, +X/-Y)
- Eval scores: `make eval-all` output — N skills avg X.XXX, N agents X.XXX
- [claim]: [exact command or file:line that proves it]
```

If a claim can't be verified with a command or file reference, flag it as **UNVERIFIED** and suggest rewording.

## Bundling Strategy

When deciding whether a release warrants its own post:

- **Standalone post**: Major features, impressive before/after metrics, new capabilities
- **Bundle with next release**: Bug fixes, description tweaks, minor config changes
- **Skip entirely**: Patch releases with <5 files changed and no user-facing changes

The v2.6.1 post (37 likes, 1.4K views) vs v2.6.0 (150 likes, 5.5K views) demonstrates this — back-to-back releases dilute signal. When in doubt, wait and bundle.
