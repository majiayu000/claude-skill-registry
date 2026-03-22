---
name: news
description: Research and publish a daily AI news edition (The AI Dispatch)
argument-hint: [preview|publish|regenerate YYYY-MM-DD]
allow-model-invocation: true
---

# Publish The AI Dispatch

Generate and publish a daily edition of **The AI Dispatch** — an AI news broadsheet styled with the newspaper design system from `styles/newspaper.html`.

Arguments: `$ARGUMENTS`

- `publish` (default, or no args): Full pipeline — research, write, deploy
- `preview`: Research only — show what stories would be covered, don't write HTML
- `regenerate YYYY-MM-DD`: Redo a specific day's edition

## Phase 0 — Setup

1. Parse arguments to determine mode (`preview`, `publish`, or `regenerate`).
2. Set today's date: `YYYY-MM-DD` format (or the specified date for `regenerate`).
3. Read `styles/newspaper.html` to extract the full CSS design system.
4. Read `news/CLAUDE.md` for section conventions and template structure.
5. Check if `news/{date}/index.html` already exists (skip if publish, overwrite if regenerate).
6. Read up to 3 most recent editions from `news/*/index.html` for deduplication:
   - Extract headlines (`<h2>`, `<h3>` text)
   - Extract source URLs (`href="http..."`)
   - Build a dedup set of covered topics and links

## Phase 1 — Research (5 parallel sonnet subagents)

Launch 5 **sonnet** subagents in parallel, each using WebSearch:

### Agent 1: AI Industry News
Search for the latest from Claude/Anthropic, OpenAI, Google AI/DeepMind, Meta AI, xAI, Mistral, and general AI industry news. Focus on product launches, policy changes, funding rounds, partnerships.

### Agent 2: Open Source & Developer Tools
Search for new AI developer tools, open-source model releases, MCP servers, framework updates, and notable library releases.

### Agent 3: AI Research & Papers
Search for AI research breakthroughs, new benchmarks, notable papers (arXiv), safety research, and technical achievements.

### Agent 4: Community, Culture & Media
Search for AI community discussions, notable AI YouTube videos, podcast highlights, opinion pieces, regulatory developments, and cultural impact stories.

### Agent 5: GitHub Trending
Search for today's top trending GitHub repositories — not just AI/ML, but across all languages and topics. Use WebSearch to find GitHub trending pages, aggregator sites (e.g., trendshift.io, ossinsight.io), and dev community posts about trending repos. Return the top 5-8 repos with: repo name, author, language, stars/growth, and a 1-sentence description. Include the GitHub URL for each.

**Agents 1-4 return:** 5-8 ranked story summaries with:
- Headline
- 2-3 sentence summary
- Source URL(s)
- Significance rating (1-5)

**Agent 5 returns:** 5-8 trending repos with:
- Repo name and author
- Language and star count/growth
- 1-sentence description
- GitHub URL

## Phase 1.5 — Deduplicate

Compare all research results against the dedup set from Phase 0:
- Drop any story whose headline or URL matches recent coverage
- Flag stories that are follow-ups to recent coverage (can still run, but note the prior coverage)

**If mode is `preview`:** Stop here. Display the curated story list to the user and exit.

## Phase 2 — Editorial Planning

This is where Claude exercises editorial judgment. Instead of rigid required sections:

1. **Rank all stories** by significance, newsworthiness, and reader interest.
2. **Pick a lead story** — the single most important story of the day.
3. **Choose layout components** based on what the day's news warrants:
   - `.card-lead` — Lead/feature stories (1-2 per edition)
   - `.card-column` — Standard column stories (3-6 per edition)
   - `.card-brief` — Quick-hit briefs (2-5 per edition)
   - `.card-feature` — Boxed feature with label (0-2 per edition)
   - `.pull-quote` — Notable quotes from the day (0-2)
   - `.data-table` — Data/benchmark comparisons (0-1)
   - `.alert-breaking` — Only if genuinely breaking news
   - `.cols-2`, `.cols-3`, `.cols-2-1` — Column layouts as appropriate
4. **Plan page structure** — masthead, then sections in order of importance.
5. **GitHub Trending table** — Always include a `.data-table` near the end of the edition showing 5-8 trending repos with columns: Repo, Language, Stars/Growth, Description. Each repo name links to its GitHub URL.
6. **Only constants:** masthead with date, at least one lead story, source attribution on every story, GitHub Trending table, footer with archive link.

Output a structured editorial plan before building.

## Phase 3 — Build (2-3 sequential opus subagents)

### Agent 1: HTML Skeleton + Lead
- Create `news/{date}/index.html`
- Full inlined newspaper CSS (adapted from `styles/newspaper.html`)
- Google Fonts: Playfair Display, Libre Baskerville, PT Sans Narrow
- Masthead with "THE AI DISPATCH" nameplate, date, volume/issue number
- Volume = 1, Issue = count of existing editions + 1
- Lead story and first half of planned sections
- All external links: `target="_blank" rel="noopener"`
- Bylines with source attribution on every story

### Agent 2: Remaining Sections + Footer
- Read the file from Agent 1
- Add remaining sections per editorial plan
- Footer with:
  - Archive link: `<a href="../index.html">AI Dispatch Archive</a>`
  - Back to elevator: `<a href="../../index.html">Back to Lobby</a>`
  - Generated-by credit line
- Verify all links work, no broken references

### Agent 3: Polish (optional, if needed)
- Read complete file
- Verify responsive design (check `@media` rules)
- Ensure consistent newspaper styling throughout
- Check that every story has source attribution
- Verify no duplicate stories within the edition

**Target size:** 800-2000 lines per edition.

## Phase 4 — Index & Ship

1. Read `news/index.html` (the archive hub page).
2. Add new entry at top of the archive list with:
   - Date
   - Lead headline
   - Brief summary (1 sentence)
   - Link to `{date}/index.html`
3. Commit with message: `Publish AI Dispatch for {date}: {lead headline}`
4. Push using: `git config --global credential.helper store && echo "https://GGPrompts:$(gh auth token --user GGPrompts)@github.com" > ~/.git-credentials && git push origin main`

## Edition HTML Template Reference

Each daily edition follows this structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The AI Dispatch — {Month Day, Year}</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400;1,700&family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=PT+Sans+Narrow:wght@400;700&display=swap" rel="stylesheet">
    <style>
        /* Full newspaper CSS inlined from styles/newspaper.html */
        /* Adapted: masthead says "THE AI DISPATCH" */
    </style>
</head>
<body>
    <div class="container">
        <header class="masthead">
            <div class="masthead-top">
                <span>Volume 1, No. {issue}</span>
                <span>{date}</span>
                <span>AI News Daily</span>
            </div>
            <h1 class="masthead-nameplate">The AI Dispatch</h1>
            <p class="masthead-motto">"All the AI News That's Fit to Compile"</p>
            <nav class="masthead-nav">
                <a href="../index.html">Archive</a>
                <a href="../../index.html">Lobby</a>
            </nav>
        </header>

        <!-- Editorially chosen sections here -->
        <!-- Use newspaper components: .card-lead, .card-column, .card-brief, etc. -->
        <!-- Every story gets a .card-byline with source attribution -->

        <footer class="footer">
            <p><a href="../index.html">AI Dispatch Archive</a> · <a href="../../index.html">Back to Lobby</a></p>
            <p class="footer-credit">Generated by Claude · <a href="https://github.com/GGPrompts/htmlstyleguides">Source</a></p>
        </footer>
    </div>
</body>
</html>
```

## Key Rules

- **Self-contained HTML**: Each edition is a single file with all CSS inlined.
- **No JavaScript required**: Editions are pure static HTML/CSS.
- **Source attribution**: Every story must link to its source. Never fabricate URLs.
- **Editorial freedom**: Claude decides which sections/layout to use. No rigid template.
- **Deduplication**: Never repeat a story that ran in the last 3 editions.
- **External links**: Always `target="_blank" rel="noopener"`.
- **Responsive**: Include mobile breakpoints from the newspaper style guide.
