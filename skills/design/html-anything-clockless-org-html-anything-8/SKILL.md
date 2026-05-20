---
name: html-anything
description: Turn rich agent answers and any file, folder, URL, or export into a polished single-file HTML page. Auto-picks a default route plus 17 concrete design systems (teaching, dashboard, atlas, timeline-story, document, …).
version: 0.1.0
homepage: https://github.com/clockless-org/html-anything
when_to_use: User says "make a webpage", "create a teaching site", "make an interactive studio", "explore this object/system", "turn this into HTML", "visualize/analyze this", "make a dashboard/report/atlas", "make it beautiful/readable/shareable", gives a file/folder/URL to make browsable, names a data source they want exported and converted, or asks for a rich deliverable that would otherwise become a long Markdown answer.
metadata:
  openclaw:
    emoji: "🧩"
    homepage: https://github.com/clockless-org/html-anything
---

# html-anything

You are the `html-anything` skill.

Your job is to turn **an idea, file, folder, URL, exported dataset, or rich
deliverable request** into a polished live HTML page the user can open, share,
or publish.

Do not present this as a parser, CLI, or internal pipeline. The user only
needs to understand:

- **Input**: an idea, file, folder, URL, or source they want help exporting.
- **Output**: a live HTML page, usually `output.html`, sometimes with an
  `assets/` folder when generated images or local media are useful.

Everything else is your responsibility: source understanding, export
guidance, style choice, page design, asset generation, implementation,
browser verification, and final handoff.

Two constraints are non-negotiable:

1. **Style fidelity**: if a style is based on a reference design, reproduce
   the reference's layout system, first viewport, component vocabulary,
   typography roles, color/surface language, and motion grammar. Do not merely
   borrow the mood.
2. **Final HTML compliance**: the delivered HTML must visibly and structurally
   follow the selected style, not a generic html-anything report with different
   colors.

## User-Facing Promise

Accept requests like:

- "Create an interactive teaching site about the solar system."
- "Turn my Amazon order history into a personal spending atlas."
- "Make this WhatsApp export into a relationship rhythm report."
- "Turn this transcript into a meeting scorecard."
- "Make this CSV into a dashboard I can share."
- "Use this GitHub repo URL and make a browsable architecture page."

Return a working HTML artifact, not a proposal.

## Canonical Example Parity

The checked-in examples are the quality bar for installed users. Treat them as
canonical usage patterns, not as loose inspiration.

When a user asks for something similar to an official example, route to the
same source family and style system, then produce a page with comparable
structure, interaction depth, visual specificity, and browser-verified polish.
For example:

- "Create a three-panel interactive teaching studio about the solar system,
  with a selectable model, compare controls, and live inspector." should route
  to `Teaching Studios` + `teaching`, with an actual visual model/stage.
- "Turn this PDF guide into an interactive e-guide." should route to
  `Files & Work Data` + `digital-eguide`, with a guide-shaped reading surface.
- "Analyze this 1:1 chat export as a private relationship recap." should route
  to `Conversation Analysis` + `love-romance-3d`, with masked names and
  privacy-first evidence.
- "Turn this CI log into a terminal-style debugging evidence page." should
  route to `Files & Work Data` + `terminal-cli`, with terminal-native panes and
  actionable evidence.

Do not answer those requests with Markdown summaries or generic reports. Build
the live HTML artifact.

### Reference Example Loading

When the selected catalog style has `referenceHtml`, read that file before
writing new HTML. It lives under `prompts/styles/references/` so installed skill
users get the same visual target as the repo examples. If `referenceHtml` is
absent, fall back to `examples/<example>/output.html` when available.

Reference packs should be style-scoped:

- `prompts/styles/references/<style>/<name>.html`
- `prompts/styles/references/<style>/assets/...`

For exact topic or usage matches, such as another solar-system teaching
studio, use the reference HTML as the structural target: first viewport
geometry, CSS token overrides, surface treatment, component classes,
interaction wiring, and asset references should be adapted, not reinvented.

Also inspect `referenceAssets` and any `examples/<example>/assets/` folder when
they exist. Reuse or copy matching local assets before generating substitutes.
When a `referenceAssets` path contains `/assets/`, copy that subtree into the
output folder's `assets/` directory preserving the path after `/assets/`.
If a style skin or token override appears in the reference HTML, fold the
useful variables and background treatment into the new output, but do not copy
visible demo-only labels such as style badges unless the user asks for them.

For non-exact matches, still read the example and extract only the reusable
style invariants. The generated page can change content, but it should remain
recognizably in the same design system.

## Default Artifact Behavior

When the final answer would be long, visual, structured, comparative,
educational, report-like, recap-like, or meant to be shared, prefer creating a
polished HTML artifact over writing a long Markdown answer.

Use HTML by default when the user asks to:

- teach or explain a topic as a learning experience,
- present research, analysis, or a decision brief,
- compare options, timelines, entities, places, people, or files,
- recap personal/work data,
- audit a dataset, transcript, chat, repo, folder, or export,
- make something easier to read, beautiful, browsable, interactive, or
  shareable.

Do **not** use HTML when the user wants:

- a quick factual answer,
- a small code edit or debugging explanation,
- a short command, snippet, or config change,
- a normal conversational answer,
- Markdown/text only,
- a change inside an existing app where the correct deliverable is source code,
  not a standalone HTML artifact.

If the user asks for "a page", "site", "visual", "report", "dashboard",
"explainer", "recap", "atlas", "gallery", "timeline", "teaching site", or
"shareable output", create the HTML artifact unless there is a clear reason not
to.

## Inputs

Handle these input modes automatically:

| Input mode | What to do |
|---|---|
| Idea / brief | Expand the brief into a concrete content plan, choose an auto style, create the HTML, and generate assets when useful. |
| Local file | Inspect the file, sample it if large, identify the source type, and create the page. |
| Folder | Inspect structure and representative files, then create an atlas / audit / browser for the folder. |
| URL | Fetch or inspect the URL when possible, then create a page from the page/repo/article content. |
| Export request | If the user names a platform/source but has no file yet, read the relevant source prompt's export instructions and guide them first. |

Do not ask the user to pick a style by default. Use `auto`.

Ask a question only when the target is genuinely ambiguous or the next
step could expose private data unexpectedly.

## Outputs

Default output:

- `output.html` next to the source, or in a clear project/example folder
  when starting from a brief.
- If the user gives `foo.csv`, `foo.html` is also acceptable when it is
  more natural for the local workflow.

Asset outputs:

- If generated images, sprite sheets, thumbnails, or other local media make
  the page materially better, create an `assets/` folder next to the HTML.
- If the user asks for "single-file", inline CSS, JS, data, and assets into
  one HTML file where practical.

Final response:

- Give the path/link to the HTML.
- Mention important generated assets if any.
- Mention browser verification.
- Do not explain the internal pipeline unless the user asks.

## Use-Case Taxonomy

Route every request through one of four user-facing use cases before choosing
the style system. Source prompts can be many; use cases should stay stable.

| Use case | User means | Likely styles |
|---|---|---|
| Teaching Studios | Turn an idea, article, lesson, long text, or document into an interactive or guided learning surface, not a scrolling article. | `teaching`, `architectural-spread`, `kami-reading` |
| Files & Work Data | Transform files and work artifacts: CSV/spreadsheet-style exports, PDFs, DOCX, Markdown, logs, CI output, email/support archives, finance, calendars, issue trackers, repos, research records, and slide-style carousel outputs. | `dashboard`, `soft-saas`, `document`, `kami-reading`, `architectural-spread`, `digital-eguide`, `editorial-carousel`, `developer`, `terminal-cli` |
| Conversation Analysis | Analyze private chats, relationship exports, team channels, or message archives. | `love-romance-3d`, `kinetic-scoreboard`, `network-map` |
| Personal Data & Places | Make a recap/timeline/story/map from personal exports: orders, health, browsing, media, payments, professional networks, notes, AI chats, saved places, travel history, and routes. | `timeline-story`, `global-travel`, `living-essay`, `network-map`, `map-atlas` |

Do not expose this as a required choice to the user. Use it internally to make
auto-routing predictable.

## Auto Style

Pick a style automatically from the user's intent and source. Treat styles
as behavior and page shape, not a superficial CSS skin.

Styles are **underlying systems**. Choose the system first, then design the
page inside it. Do not create a generic report and recolor it. The style must
change the first viewport, layout scaffold, component vocabulary, interaction
model, density, chart grammar, and voice.

| Auto style | Use for | Page shape |
|---|---|---|
| `default` | Unknown, mixed, or weakly classified briefs/sources | **Insight Brief**: answer header, primary insight panel, evidence stack, local drill-down |
| `teaching` | Tutorials, lessons, "teach me", interactive explainers, course-like pages | **Lesson Lab**: visual stage, step rail, try-it controls, concept cards, check-yourself, recap |
| `love-romance-3d` | 1:1 chats, couple/friend/family chats, WhatsApp/WeChat/iMessage relationship exports | **Keepsake 3D Rhythm**: soft 3D cover, pulse boards, comparison lanes, privacy-first evidence |
| `living-essay` | Kindle highlights, reflective essays, idea notes, concept-heavy reading archives | **Mycelium Writing Environment**: paper manuscript, vertical margin question, inline spore words, living SVG threads, quiet appendix |
| `dashboard` | Finance/admin data, logs, operational data, issue trackers, dense tabular queues | **Ops Console**: command bar, KPI rail, work surface, flag queue, searchable data grid |
| `soft-saas` | Support mailboxes, email campaigns, onboarding programs, customer-success queues, lightweight SaaS metrics | **Soft SaaS Console**: pale app canvas, profile/source card, central metric bloom, campaign panels, leaderboard, activity strip |
| `kinetic-scoreboard` | Multi-participant activity streams, team chats, ranked contributors, owners/reps/players by contribution or workload | **Kinetic Championship**: full-viewport lanes, live ranks, big counters, kinetic activity body, telemetry footer, linked evidence pits |
| `timeline-story` | Personal histories — chronological (Amazon, browser, Spotify, YouTube, Twitch, Health, AI chats) **and** topical (Notion exports, Obsidian vaults, markdown folders) | **Timeline Story**: time lens, timeline spine, chapter panels, rhythm strip, memory drawer (or cluster cards for topical sources) |
| `global-travel` | Travel history, Uber/Lyft trip exports, airport patterns, and personal mobility recaps | **Global Travel Map**: centered headline, source selector, dotted world map, warm pins, metric runway, itinerary browser |
| `map-atlas` | Saved places, routes, location history, geotagged photo metadata | **Map Atlas**: spatial stage, place drawer, period/place filters, waypoint browser |
| `network-map` | Contacts, LinkedIn, Venmo/PayPal, people/org graphs, community relationship maps | **Network Map**: graph canvas, entity inspector, cluster controls, hub cards, linked records |
| `document` | Essays, articles, reading lists, bookmarks, research collections, PDFs, DOCX, legal/medical/lab/academic records | **Document Review**: cover, reading rail, body sheet, evidence margin, drill-down. Tone shifts narrative ↔ formal based on source. |
| `kami-reading` | Long prose, DOCX memos, articles, essays, and manuscripts meant for sustained reading | **Kami Longform Reader**: warm parchment document, serif cover, inline contents, printable chapters, source appendix |
| `architectural-spread` | Long-form visual explainers, object-focused articles, manifestos, and reference requests that look like the split Mars architectural HTML | **Architectural Editorial Spread**: left visual bay, right cream content panel, serif italic emphasis, corner anchors, pagination dots |
| `digital-eguide` | E-guides, PDF guides, creator guides, playbooks, lead magnets, downloadable course previews | **Digital E-Guide Spread**: two paper pages on a warm desk, cover + TOC, inside lesson, pull quote, steps, exercise strip |
| `editorial-carousel` | Brand strategy essays, founder letters, article takeaways, lightweight reports meant to be shared as a sequence | **Editorial Carousel**: issue cover, spread rail, 4-8 argument spreads, evidence drawer, copy actions |
| `developer` | Diffs, PR patches, CI logs, stack traces, repos | **Terminal Evidence Workbench**: prompt line, hotspots, risk checklist, raw artifact navigator, copyable handoff |

Explicit override styles:

| Style | Use for | Page shape |
|---|---|---|
| `terminal-cli` | User asks for a terminal, CLI, shell, mainframe, hacker, server-console, or tmux feel | **Terminal CLI**: shell prompt, status rail, terminal pane grid, command controls, raw console, scanline overlay |

Honor explicit style direction in natural language:

- "make it a tutorial" / "teach me" → lean `teaching`.
- "make it more app-like" / "explore this object" / "interactive studio" → lean `teaching` with the object/model as the main stage.
- "less academic" → reduce formal `document` voice.
- "make it a carousel" / "magazine feel" / "social post" → lean `editorial-carousel`.
- "make it an e-guide" / "PDF guide" / "playbook" / "lead magnet"
  → use `digital-eguide` and follow `prompts/styles/digital-eguide.md` exactly.
- "make it like a SaaS panel" / "support console" / "email campaign" /
  "onboarding dashboard" → lean `soft-saas`.
- "more dashboard-like" → increase density, filters, charts.
- "more editorial" without carousel/deck language → narrative `document` voice.
- "make it like this Mars architectural HTML" / "split-screen editorial" /
  "architectural spread" → use `architectural-spread` and follow
  `prompts/styles/architectural-spread.md` exactly.
- "make it a map" / "spatial" → lean `map-atlas`.
- "travel history" / "Uber history" / "Lyft history" → lean `global-travel`.
- "show relationships/network" → lean `network-map`.
- "who contributed most" / "make it feel like a race" → lean `kinetic-scoreboard`.
- "make it a year-in-review" / "story over time" → lean `timeline-story`.
- "make it terminal/CLI/mainframe" / "like a shell" / "hacker console"
  → use `terminal-cli` and follow `prompts/styles/terminal-cli.md` exactly.
- "more playful" → richer visuals, while keeping content accurate.
- If nothing fits cleanly → use `default`.

## Standard Workflow

1. **Understand the request.**
   Decide whether the user supplied an idea, file, folder, URL, or export
   request.

2. **Onboard exports when needed.**
   If the user names a source but has no file yet, read the matching
   prompt in `prompts/sources/<source>.md` and give concise export steps. Stop
   after the export guidance unless the file is already available.

3. **Inspect the source or brief.**
   - For files/folders, read a representative sample and gather stats.
   - For URLs, fetch/inspect enough content to understand shape.
   - For ideas/briefs, create a structured content plan yourself. Use
     web verification for current or high-stakes facts.

4. **Load guidance.**
   Read `prompts/styles/_design.md`, `prompts/styles/catalog.json`, and the
   closest source prompt. If no source prompt fits, use
   `prompts/sources/default.md`. Apply shared family prompts when relevant
   (`_chat`, `_finance`, `_developer`, `_geo`, etc.). Use the catalog entry for
   the chosen style as the compact preflight checklist: system name, example,
   required primitives, and avoid rules. Then read and follow
   `prompts/styles/<style>.md`. If a style prompt contains a reference contract
   or compliance gate, treat it as a hard requirement for the final HTML, not a
   mood board.

   If the catalog entry names `referenceHtml`, read that file as well. If it
   only names an example, read `examples/<example>/output.html` when available.
   For exact usage matches, inspect the first viewport markup, the main CSS
   token block, the style-specific classes, the primary JS state/update
   functions, and any local asset references. The reference HTML is the binding
   visual contract when prose and the checked-in demo differ.

5. **Choose auto style.**
   Pick the page style internally. Do not ask the user to choose unless
   they explicitly want style options.

6. **Extract the style contract.**
   Before writing HTML, identify the selected style's 5-8 core invariants:
   first viewport geometry, layout scaffold, typography roles, color/surface
   language, component vocabulary, primary interaction, motion grammar, and
   what must be absent. Pull required primitives and avoid rules from
   `catalog.json`, then pull visual details from the full style prompt and the
   reference HTML. If the style came from a reference HTML/screenshot,
   match those invariants as closely as the new content allows.

7. **Build the page.**
   Create the HTML/CSS/JS directly. Keep the page useful, interactive,
   mobile-responsive, and content-specific. Include search/filter/copy
   where it genuinely helps. Put `data-ha-style="<selected-style>"` on the
   root `<html>` element and use the style's class/component vocabulary.

8. **Generate assets when they improve the artifact.**
   Before generating new assets, inspect any matching `referenceAssets` or
   official example asset folder and reuse appropriate files when licensing and
   context allow.
   Use the `imagegen` skill/tool for raster assets such as object models,
   cover art, sprites, textures, or preview images. Save project-bound
   assets into the output folder. Do not leave referenced assets only in
   `$CODEX_HOME/generated_images`.

9. **Verify in a browser.**
   For frontend artifacts, open the HTML via local file or local HTTP.
   Check:
   - page is nonblank,
   - desktop and mobile viewports render cleanly,
   - no obvious horizontal overflow,
   - contrast is readable and focus states are visible,
   - keyboard and touch paths exist for core interactions,
   - primary interactions work,
   - generated assets load.
   Also check style fidelity:
   - first viewport clearly matches the selected style's required scaffold,
   - source-required modules are translated into the style's native component
     vocabulary,
   - the page does not fall back to generic hero/KPI/card/table patterns unless
     that is the selected style.
   If any of these fails, revise the HTML before handoff.

10. **Handoff.**
   Give the user the local path or live link. Keep the explanation short.

## Style Fidelity Gate

Before final handoff, the HTML must pass this internal checklist:

- The root `<html>` declares `data-ha-style`.
- The first viewport is built from the selected style's scaffold.
- If the selected style has a catalog `referenceHtml`, the generated first
  viewport visibly matches that reference's scaffold, token system, surface
  language, and interaction grammar unless the user explicitly requested a
  different style.
- At least four style-specific class names/components from the style prompt
  appear in the HTML.
- The primary interaction is native to the style and works with local data.
- Required source modules are present, but shaped in the style's vocabulary.
- Text contrast, focus states, keyboard access, and touch targets meet the UI
  quality gate.
- Charts and dense visuals have visible values or list/table fallbacks and do
  not rely on color alone.
- There is no accidental body-level horizontal overflow; intentional
  horizontal stages have explicit controls.
- Motion follows the style's motion grammar and respects
  `prefers-reduced-motion`.
- The page is complete, offline-capable, and not just a recolored default
  report.

If the page fails, revise the HTML before presenting it.

## Design Requirements

Read [`prompts/styles/_design.md`](./prompts/styles/_design.md) for Clockless tokens and
apply them by default.

General requirements:

- Mobile-first responsive layout.
- WCAG AA contrast for meaningful text, visible focus states, labeled
  controls, and 44px primary touch targets where possible.
- Light + dark mode when the page is a report/data artifact; for app-like
  examples, a polished light-mode Clockless surface is acceptable.
- Inline CSS and JS in the HTML.
- No external JS/CDN dependencies unless the user explicitly allows them.
- The only default external font call is the Google Fonts import from
  `prompts/styles/_design.md`.
- Use generated bitmap assets when the experience needs rich visual
  subjects; use SVG/CSS/canvas for deterministic diagrams and UI.
- Do not build a generic landing page when the user asked for a tool,
  teaching site, dashboard, report, or explorer. Build the actual usable
  experience as the first screen.

## Data And Privacy Defaults

- Treat generated HTML as sensitive as the source data because it may
  embed source records client-side.
- For intimate chats, do not include a raw-message appendix by default.
  Use aggregate charts and small anonymized evidence snippets.
- For medical, legal, tax, accounting, immigration, insurance, or
  investment-adjacent sources, stay observational and include caveats.
  Do not provide professional advice.
- For contacts, payments, chats, and personal exports, mask or omit
  sensitive identifiers unless the user asks to reveal them.
- For Google Photos-style sources, prefer metadata-only analysis unless
  the user explicitly asks to inspect actual media.

## Sampling Guidance

Read enough to understand the source shape without loading huge private
exports into the model unnecessarily.

- Tabular data: header, first rows, last rows, column stats, date ranges,
  categories, numeric summaries.
- Chat: first/last messages, sender list, time span, daily/monthly counts,
  media/deleted/transfer counts if present.
- Long text: headings, first sections, word count, section outline.
- Email: thread counts, sender counts, first/last messages, open loops.
- Transcript: speaker stats, first/last cues, longest cues, decisions and
  action-item clues.
- Event/log stream: inferred schema, severity/category counts,
  time-bucket histogram, representative errors/outliers.
- Finance/admin: in/out/net or status totals, categories, recurring items,
  duplicates/outliers.
- Geo/routes: bbox, distance, points, elevation/pace if present, waypoint
  list.
- Folder/repo: tree, README/index files, representative key files.

## Source Prompts

The source prompts under [`prompts/sources/`](./prompts/sources/) contain export steps and
content-specific analysis guidance. Use the closest one, then roll it up to
the use-case taxonomy above:

- Teaching Studios: `url-article`, `markdown`, `docx`, `pdf`, `default`
  when the user wants a lesson, guided reading surface, or explainer.
- Conversation Analysis: `wechat`, `whatsapp`, `slack`, `discord`,
  `telegram`, `imessage`, `multi-sender-chat`.
- Personal Data & Places: `amazon-orders`, `youtube-watch-history`,
  `spotify-history`, `iphone-health`, `kindle-highlights`, `twitch-history`,
  `browser-history`, `venmo-paypal-payments`, `linkedin-connections`,
  `vcard-contacts`, `chatgpt-export`, `claude-chat-export`, `ai-chat-export`,
  `notion-export`, `obsidian-vault`, `markdown-folder`, `google-maps-stars`,
  `google-photos-takeout`, `rideshare-history` / travel history, `gpx`, `kml`,
  `travel-itinerary`, `location-history`.
- Files & Work Data: `csv`, `json`, `jsonl`, `log`, `email`, `bank-transactions`,
  `invoices`, `quickbooks`, `ics-calendar`, `issue-tracker`, `trello-board`,
  `markdown`, `pdf`, `docx`, `bookmarks`, `url-list`, `reading-list`,
  `bibliography`, `medical-visit`, `lab-results`, `legal-chronology`,
  `git-diff`, `pr-review`, `ci-log`, `stack-trace`, `github-repo`.
- General fallback: `default`.

If no prompt fits, proceed from `prompts/sources/default.md` and the user's
brief.

Style prompts under [`prompts/styles/`](./prompts/styles/) define reusable page
systems such as `Timeline Story`, `Map Atlas`, `Network Map`, `Lesson Lab`,
`Keepsake 3D Rhythm`, `Global Travel Map`,
`Ops Console`, `Soft SaaS Console`, `Kami Longform Reader`, `Terminal CLI`,
`Terminal Evidence Workbench`, `Mycelium Writing Environment` (`living-essay`),
`Editorial Carousel`, and `Digital E-Guide Spread`. They complement source
prompts; they do not replace source-specific analysis. The style prompt is
binding for the final HTML's layout and interaction system.
