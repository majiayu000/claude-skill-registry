# html-anything

> **The agent skill that turns anything into a beautiful, shareable HTML page.**
> Rich answers, files, folders, URLs, and messy service exports become verified
> single-file `.html` artifacts with source-aware parsing, automatic style
> routing, **60 source prompts**, and **17 concrete style systems**. Short chats
> stay short; page-worthy answers become pages.

<p align="center">
  <a href="https://skills.sh/clockless-org/html-anything"><img alt="skills.sh" src="https://skills.sh/b/clockless-org/html-anything"></a>
  <a href="https://github.com/clockless-org/html-anything/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/clockless-org/html-anything?style=flat-square"></a>
  <a href="https://github.com/clockless-org/html-anything/blob/main/LICENSE"><img alt="License" src="https://img.shields.io/github/license/clockless-org/html-anything?style=flat-square"></a>
  <a href="./prompts/sources"><img alt="60 source prompts" src="https://img.shields.io/badge/sources-60%20prompts-7b40e0?style=flat-square"></a>
  <a href="./prompts/styles"><img alt="17 style systems" src="https://img.shields.io/badge/styles-17%20systems-a03b00?style=flat-square"></a>
  <a href="https://clockless-org.github.io/html-anything/examples/"><img alt="11 demos" src="https://img.shields.io/badge/examples-11%20demos-0f766e?style=flat-square"></a>
</p>

<p align="center">
  <a href="https://clockless-org.github.io/html-anything/examples/"><strong>→ Open the live demo gallery</strong></a>
</p>

`html-anything` works inside Codex and Claude Code. Ask for a teaching site,
drop in a PDF, upload a CSV, point it at a folder, or hand it an export like
Amazon orders, Kindle highlights, Spotify history, WeChat / iMessage,
Google Photos Takeout, logs, GPX, and more. The skill figures out the source,
chooses the right use case and style, builds the page, checks it in a browser,
and hands back a live HTML artifact instead of a long Markdown reply.

## Why this exists

AI agents are outgrowing plain Markdown. Inspired by Claude Code team member
Thariq Shihipar's viral
[“The Unreasonable Effectiveness of HTML”](https://x.com/trq212/status/2052809885763747935),
`html-anything` treats HTML as the richer response format: denser, more visual,
more interactive, and easier to share when the answer is really a page.

<table>
<tr>
<td width="100%" valign="top">
<h3>Before: plain response</h3>
<p>A long scroll of text for “Teach me solar system”. Useful, but hard to explore.</p>
<img src="./docs/plain-response-before.jpg" alt="Plain AI response about the solar system" width="100%">
</td>
</tr>
<tr>
<td align="center">
<strong>↓</strong><br>
<sub>Same intent, richer response format</sub>
</td>
</tr>
<tr>
<td width="100%" valign="top">
<h3>After: live HTML artifact</h3>
<p>The same teaching goal becomes a visual, interactive learning page.</p>
<a href="https://clockless-org.github.io/html-anything/examples/solar-system-studio/output.html"><img src="./docs/example-demos/solar-system-studio.gif" alt="html-anything solar system teaching studio (animated demo)" width="100%"></a>
</td>
</tr>
</table>

## Preview

<sub>Each card shows the kind of question a user would naturally ask. The skill detects intent, picks the right design system, and ships a polished HTML page — without anyone mentioning HTML. Open the [live demo gallery](https://clockless-org.github.io/html-anything/examples/) to see the rendered outputs.</sub>

### Teaching Studios

<table>
<tr>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/solar-system-studio/output.html"><img src="./docs/example-demos/solar-system-studio.gif" alt="Teach a concept demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/solar-system-studio/output.html">Teach a concept →</a></strong><br>
<sub>Source: teaching brief · Style: <code>teaching</code></sub><br>
<sub><strong>Ask:</strong> <code>Teach me the solar system.</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/markdown/output.html"><img src="./docs/example-demos/markdown.gif" alt="Learn from long-form text demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/markdown/output.html">Learn from long-form text →</a></strong><br>
<sub>Source: Markdown file · Style: <code>architectural-spread</code></sub><br>
<sub><strong>Ask:</strong> <code>Help me understand this essay.</code> (with a markdown file attached)</sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/docx/output.html"><img src="./docs/example-demos/docx.gif" alt="Learn from a document demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/docx/output.html">Learn from a document →</a></strong><br>
<sub>Source: DOCX file · Style: <code>kami-reading</code></sub><br>
<sub><strong>Ask:</strong> <code>Make this memo easier to read.</code> (with a docx file attached)</sub>
</td>
<td width="50%" valign="top"></td>
</tr>
</table>


### Files & Work Data

<table>
<tr>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/editorial-carousel/output.html"><img src="./docs/example-demos/editorial-carousel.gif" alt="Argument as sequence demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/editorial-carousel/output.html">Argument as sequence →</a></strong><br>
<sub>Source: strategy essay · Style: <code>editorial-carousel</code></sub><br>
<sub><strong>Ask:</strong> <code>Help me share this strategy essay with my team.</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/pdf/output.html"><img src="./docs/example-demos/pdf.gif" alt="Guide from dense document demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/pdf/output.html">Guide from dense document →</a></strong><br>
<sub>Source: PDF report · Style: <code>digital-eguide</code></sub><br>
<sub><strong>Ask:</strong> <code>Summarize this report and let me browse it section by section.</code></sub>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/email/output.html"><img src="./docs/example-demos/email.gif" alt="Inbox or workstream audit demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/email/output.html">Inbox or workstream audit →</a></strong><br>
<sub>Source: Mbox archive · Style: <code>soft-saas</code></sub><br>
<sub><strong>Ask:</strong> <code>What's happening in my inbox? Show me the open loops.</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/ci-log/output.html"><img src="./docs/example-demos/ci-log.gif" alt="Debugging evidence demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/ci-log/output.html">Debugging evidence →</a></strong><br>
<sub>Source: CI log · Style: <code>terminal-cli</code></sub><br>
<sub><strong>Ask:</strong> <code>Why did this build fail? Walk me through it.</code></sub>
</td>
</tr>
</table>


### Conversation Analysis

<table>
<tr>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/wechat-couple/output.html"><img src="./docs/example-demos/wechat-couple.gif" alt="Private chat recap demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/wechat-couple/output.html">Private chat recap →</a></strong><br>
<sub>Source: 1:1 chat export · Style: <code>love-romance-3d</code></sub><br>
<sub><strong>Ask:</strong> <code>Recap our 1:1 chat history. Keep it private — mask names.</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/slack/output.html"><img src="./docs/example-demos/slack.gif" alt="Group contribution analysis demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/slack/output.html">Group contribution analysis →</a></strong><br>
<sub>Source: team chat export · Style: <code>kinetic-scoreboard</code></sub><br>
<sub><strong>Ask:</strong> <code>Who's driving the conversation in this Slack channel?</code></sub>
</td>
</tr>
</table>


### Personal Data & Places

<table>
<tr>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/kindle-highlights/output.html"><img src="./docs/example-demos/kindle-highlights.gif" alt="Reflective reading archive demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/kindle-highlights/output.html">Reflective reading archive →</a></strong><br>
<sub>Source: My Clippings.txt · Style: <code>living-essay</code></sub><br>
<sub><strong>Ask:</strong> <code>What have I been reading and thinking about?</code></sub>
</td>
<td width="50%" valign="top">
<a href="https://clockless-org.github.io/html-anything/examples/travel-history/output.html"><img src="./docs/example-demos/travel-history.gif" alt="Mobility recap demo" width="100%"></a><br>
<strong><a href="https://clockless-org.github.io/html-anything/examples/travel-history/output.html">Mobility recap →</a></strong><br>
<sub>Source: Uber/Lyft CSV · Style: <code>global-travel</code></sub><br>
<sub><strong>Ask:</strong> <code>Where have I been this year? Show me on a map.</code></sub>
</td>
</tr>
</table>

## Install

Pick the path for your agent:
[Claude Code](#claude-code) ·
[Codex](#codex) ·
[claude.ai](#claudeai-web) ·
[Claude API](#claude-api) ·
[Cursor / Cline / Windsurf / OpenCode / Goose / Letta / …](#one-command-for-most-cli-and-editor-agents) ·
[ClawHub](#clawhub-publish)

### One command for most CLI and editor agents

```bash
npx skills add clockless-org/html-anything
```

Works with **Claude Code**, **Codex**, **Cursor**, **Cline**, **Windsurf**,
**OpenCode**, **Goose**, **Letta**, **Roo Code**, **Kiro**, and any other
agent following the [open agent-skills spec](https://agentskills.io).
The CLI also pings [skills.sh](https://skills.sh/clockless-org/html-anything)
so installs feed the public leaderboard.

### Claude Code

```bash
git clone https://github.com/clockless-org/html-anything ~/.claude/skills/html-anything
```

Restart Claude Code so it loads `SKILL.md`. To update later:
`git -C ~/.claude/skills/html-anything pull`.

### Codex

```bash
git clone https://github.com/clockless-org/html-anything "${CODEX_HOME:-$HOME/.codex}/skills/html-anything"
```

Restart Codex.

### claude.ai (web)

1. Download [`html-anything-skill.zip`](https://github.com/clockless-org/html-anything/releases/latest/download/html-anything-skill.zip) (`SKILL.md` + `prompts/`, including style references).
2. In claude.ai: **Settings → Features → Skills → Upload a Skill** → drop the zip.

Requires **Pro / Max / Team / Enterprise** with code execution enabled.
Custom skills on claude.ai are per-user; each teammate uploads their own copy.

### Claude API

```bash
curl https://api.anthropic.com/v1/skills \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-beta: skills-2025-10-02,code-execution-2025-08-25,files-api-2025-04-14" \
  -F file=@html-anything-skill.zip
```

Then reference the returned `skill_id` in the `container` of any message.
See the [Skills API guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide).
Uploaded skills are workspace-wide.

### ClawHub (publish)

This repo carries `.clawhubignore` so only `SKILL.md` + `prompts/` ship,
including canonical style references used by installed agents:

```bash
npm i -g clawhub && clawhub login
clawhub publish . --slug html-anything --version 0.1.1 --tags latest
```

### Where it does not work

| Surface | Status |
|---|---|
| ChatGPT / chatgpt.com | ❌ Custom GPTs are a different format. Use **OpenAI Codex CLI** instead (above). |
| Gemini web / Google Gems | ❌ Different format. Use **Gemini CLI** (`npx skills add`) instead. |
| Anthropic / Claude Desktop | ✅ Reads `~/.claude/skills/` — same as Claude Code. |

> ℹ Custom Skills do not sync across surfaces. The same skill uploaded to claude.ai is **not** automatically available on Claude Code or the API — each surface keeps its own copy.

## Use

Just ask your real question. You do not need to mention HTML, pages, dashboards,
reports, atlases, or any of the design vocabulary — the skill decides when an
answer should be a page and ships one.

```text
Teach me the solar system.
What does my Amazon order history say about me?
Help me understand this CSV.
What did I read in 2025?
Walk me through this GitHub repo.
How did last quarter go?
Make sense of this messy log file.
Recap our 1:1 chat from this year.
```

Each of these triggers a polished, single-file HTML page in the right design
system. Short conversational asks stay short.

If you name a data source but have no file yet (*"my Spotify history"*,
*"my WhatsApp chat"*, *"my Google Photos Takeout"*), the skill walks you
through the export first.

## Input And Output

| Input | What you give | What you get |
|---|---|---|
| Rich answer | A topic, analysis request, comparison, recap, brief, or teaching goal | A readable, styled HTML artifact instead of a long written answer |
| Idea | A short brief, e.g. "make a solar system teaching site" | A generated educational / interactive HTML page |
| File | CSV, JSON, Markdown, PDF, DOCX, chat export, log, transcript, statement | A live page designed for that file |
| Folder | Notes vault, Google Photos Takeout, Notion export, repo, exported archive | A browsable atlas / dashboard / audit page |
| URL | Article, GitHub repo, public webpage | A shareable HTML reading or exploration page |
| Export request | "My Amazon orders", "my Spotify history", "my relationship chat" | Export instructions first, then a live HTML page |

The output is a browser page, not a chat reply. Most outputs are a single
`output.html`. When the page needs generated images or other local
assets, the skill returns `output.html + assets/`. Ask for "single-file"
if you need everything in one HTML file.

## Automatic Usage Routing

You do not need to choose a style. The default is `auto`.

Routing has three layers:

| Layer | Meaning |
|---|---|
| Use case | The user's job: teaching, files/work data, conversation analysis, or personal data/places |
| Source | The input shape: prompt, CSV, PDF, DOCX, chat export, log, repo, folder, URL |
| Style | The design system + layout system used to make the HTML readable |

Styles are not CSS skins. The skill picks the system from the content, then
builds the page inside that system. Every non-fallback style has a checked-in
live example and screenshot preview.

Style fidelity is part of the contract: when a style is based on a reference
HTML or screenshot, the generated page should reproduce the reference's first
viewport, component vocabulary, interaction model, motion grammar, and visual
absence rules. Source modules are translated into the style instead of forcing
every output into the same dashboard/report shape.

Canonical style references can live under `prompts/styles/references/<style>/`,
so the published skill can use the same structural target as the demo gallery
without bundling every example. Style-specific assets stay beside their own
reference pack and are copied only when that style needs them.

| Usage pattern | Style |
|---|---|
| Unknown or mixed inputs | `default` (Insight Brief) |
| Tutorials, lessons, explainers, "teach me" prompts | `teaching` (Lesson Lab) |
| 1:1 chats and intimate message exports | `love-romance-3d` (Keepsake 3D Rhythm) |
| Reflective essays, Kindle highlights, idea notes, concept-heavy reading archives | `living-essay` (Mycelium Writing Environment) |
| Multi-participant activity streams, team chats, ranked contributors, owner/reps/players by workload | `kinetic-scoreboard` (Kinetic Championship) |
| Personal histories — chronological (orders, history, listening, health) **and** topical (Notion / Obsidian vaults) | `timeline-story` (Timeline Story) |
| Travel history, Uber/Lyft exports, and personal mobility recaps | `global-travel` (Global Travel Map) |
| Places, trips, routes, geotagged photos | `map-atlas` (Map Atlas) |
| Contacts, communities, social payments | `network-map` (Network Map) |
| Support mailboxes, email campaigns, onboarding, customer-success queues | `soft-saas` (Soft SaaS Console) |
| Finance, spreadsheets, logs, backlog, operational data | `dashboard` (Ops Console) |
| Essays, articles, reading lists, bookmarks, PDFs, DOCX, legal/medical/lab records | `document` (Document Review) |
| Long prose, DOCX memos, articles, essays, and manuscripts meant for sustained reading | `kami-reading` (Kami Longform Reader) |
| Long-form visual explainers, object-focused articles, architectural split-screen editorial requests | `architectural-spread` (Architectural Editorial Spread) |
| E-guides, PDF guides, creator guides, playbooks, lead magnets | `digital-eguide` (Digital E-Guide Spread) |
| Brand strategy essays, founder letters, article takeaways, lightweight reports meant to be shared as a sequence | `editorial-carousel` (Editorial Carousel) |
| Explicit terminal, CLI, shell, mainframe, hacker-console requests | `terminal-cli` (Terminal CLI, explicit override) |
| Logs, PR patches, stack traces, CI failures, repos | `developer` (Terminal Evidence Workbench) |

You can still steer it naturally: "make it more tutorial-like", "more
app-like", "less academic", "make it a carousel", "more dashboard-like",
or "more playful".

Reusable style prompts live in [`prompts/styles/`](./prompts/styles/).
The shared structural contract is
[`prompts/styles/_system.md`](./prompts/styles/_system.md). The internal
style catalog lives in [`prompts/styles/catalog.json`](./prompts/styles/catalog.json):
it records the four use cases plus each style's triggers, best sources,
example, preview, required primitives, and avoid rules so generation can stay
style-faithful without asking users to pick options. There is a fallback
`default` style plus 17 concrete style systems, each with a live example and
preview asset.

Example explicit style override:

```bash
npx tsx src/cli.ts examples/pdf/input.pdf \
  --style digital-eguide \
  --out /tmp/battery-storage-guide.html \
  --title "Mid-Market Battery Storage Field Guide"
```

## Use Cases And Sources

Sources can be endless, but the skill routes them into four stable use cases.
Each use case can use one or more style systems.

| Use case | Example sources | Likely styles |
|---|---|---|
| Teaching Studios | A short teaching brief, article, lesson outline, concept note, URL, Markdown, DOCX, or PDF/document simplification request | `teaching`, `architectural-spread`, `kami-reading` |
| Files & Work Data | CSV / TSV, spreadsheet-style exports, JSON, JSONL, logs, CI output, PR patches, stack traces, repos, email/support archives, bank transactions, invoices, QuickBooks, calendars, issue trackers, Markdown, PDF, DOCX, bookmarks, URL lists, bibliographies, research records, slide-style carousel outputs | `dashboard`, `soft-saas`, `document`, `kami-reading`, `architectural-spread`, `digital-eguide`, `editorial-carousel`, `developer`, `terminal-cli` |
| Conversation Analysis | WeChat, iMessage-style CSV, Slack, Discord, Telegram, email-style threads | `love-romance-3d`, `kinetic-scoreboard`, `network-map` |
| Personal Data & Places | Amazon orders, Apple Health, browser history, YouTube, Spotify, Twitch, Kindle highlights, Venmo / PayPal, AI chat exports, notes vaults, Google Maps saved places, travel history, GPX, KML, itinerary CSV, location history | `timeline-story`, `global-travel`, `living-essay`, `network-map`, `map-atlas` |

Use case is user-facing; style is internal. The user never has to name a
style — natural asks like *"help me understand this CSV"* or *"teach me the
solar system"* are enough; the skill picks the right system automatically.

The detailed source-specific instructions live in [`prompts/sources/`](./prompts/sources/).

## Defaults

- The skill chooses the style automatically.
- The skill samples large sources, but renders the full data where practical.
- The skill checks the page in a browser before handing it back.
- Generated pages are local-first and static. They can be opened directly or hosted anywhere static HTML works.
- Generated HTML can embed private source data client-side. Treat the output as sensitive as the original export.
- Sensitive-record outputs are for organization and review only, not medical, legal, tax, accounting, immigration, insurance, or investment advice.

## Developer Note

This repo also contains a standalone parser / CLI framework used by some
examples, but the primary product surface is the agent skill. Users should
not need to understand the internal implementation to use html-anything.

```bash
git clone https://github.com/clockless-org/html-anything
cd html-anything
npm install
export ANTHROPIC_API_KEY=sk-ant-...   # or OPENAI_API_KEY=sk-...
npx tsx src/cli.ts examples/csv/input.csv --out /tmp/customers.html
```

## License

[MIT-0](./LICENSE)
