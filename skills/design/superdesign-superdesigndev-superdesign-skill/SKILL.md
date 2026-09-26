---
name: superdesign
description: "Design or redesign frontend UI, presentations, and graphics on the Superdesign canvas with a choice of leading AI models. Use whenever the user wants to design a page, feature, flow, slide deck, or brand-new product; improve or reproduce existing UI; compare design results across top models; explore visual variants; set or extract a design system; build reusable components or multi-page flows; create presentations; or create posters and marketing graphics, even if they never say the word 'design tool'. Also supports generating supporting image or video assets when a design needs them."
---

Superdesign helps you find design inspiration and generate or iterate design drafts on an infinite canvas, with multiple leading models available for different design tasks and side-by-side exploration. When a design needs a new visual asset, it can also provide image and video generation.

---

# Core scenarios (what this skill handles)

1. **Analyze a codebase for design work** — `superdesign init` builds reusable UI context in `.superdesign/init/`; read [INIT.md](references/INIT.md).
2. **Design, reproduce, or improve UI** — create pages, features, flows, and new products on the canvas; read [SUPERDESIGN.md](references/SUPERDESIGN.md).
3. **Choose and compare leading design models** — run `list-models`, select a model suited to the task, or use different models to explore independent directions.
4. **Create design systems and reusable components** — establish visual foundations, extract patterns, and design connected multi-page experiences.
5. **Design from a live website or reference URL** — extract and apply its design language; read [WEBSITE.md](references/WEBSITE.md).
6. **Create or export presentations** — plan an editable slide outline, approve it in chat, generate a real presentation draft, make slide-safe edits, or reconstruct an editable PPTX when requested and supported; read [PRESENTATION.md](references/PRESENTATION.md).
7. **Create graphics** — posters, covers, social posts, thumbnails, flyers, and ads; read [GRAPHIC.md](references/GRAPHIC.md).
8. **Generate supporting images or video** — use native image generation when appropriate or choose from Superdesign's generation models; read [ASSET_GENERATION.md](references/ASSET_GENERATION.md).
9. **Continue or directly correct existing work** — resume saved targets through [RESUME.md](references/RESUME.md), or use [design-with-your-model.md](references/design-with-your-model.md) when direct authoring is the right path.

When continuing a draft, follow [SUPERDESIGN.md](references/SUPERDESIGN.md) **ITERATION MODE ROUTING**: replace refines the selected direction with version history; branch is only for alternatives the user wants to compare.

# Step 0 — Environment preflight (BEFORE any CLI step)

Superdesign runs entirely through its CLI, so you must be able to execute shell commands. Confirm that capability first, before any CLI verification.

If you have no way to run shell commands in this environment (no terminal/execution tool at all), OR your very first bare `npx --yes @superdesign/cli@latest` preflight attempt fails because command execution itself is unavailable (the harness reports it cannot run commands / there is no shell) then STOP. Do NOT keep retrying or improvise workarounds. Tell the user once, and pick the message that matches where you are running:

- **Standard ChatGPT chat without Work Mode tools** — this exact copy, because the Work tab is the fix:

  ```text
  Chat isn't supported by the Superdesign plugin. Please switch to the Work tab and paste this prompt in for the full experience.
  ```

- **Any other harness** (a coding agent whose shell is unavailable or disabled) — do NOT send the ChatGPT copy; there is no Work tab to switch to. Say plainly that Superdesign drives its CLI over the shell, that this session cannot run shell commands, and that they can re-run it in a session with shell access or design in the web app at https://superdesign.dev.

# Step 1 — Is there a codebase to analyze?

Two entry paths. Choose one with this cheap, deterministic check BEFORE any init or design work.

**No meaningful codebase** (empty workspace, scratch/sandbox dir, no frontend code) — treat the workspace as "no codebase" when ALL of these hold:

- No `.superdesign/init/` files already exist, AND
- No dependency manifest with frontend deps (no `package.json`, or a `package.json` whose deps include no frontend framework/UI library — react, vue, svelte, angular, next, nuxt, astro, etc.), AND
- No frontend source found (a quick scan for `.tsx`/`.jsx`/`.vue`/`.svelte` files, any `.html`/`.css` files such as a root `index.html` + `style.css`, or a `src/`/`app/`/`components/` dir with UI files, turns up nothing).

→ SKIP repo init entirely. Do NOT "analyze" an empty sandbox, and do NOT ask the user to point you at a repo they don't have. Instead, gather design context conversationally FIRST: ask what they want to build, the target audience/platform, style/brand preferences, and any reference designs or inspirations. Then design from that conversation via the **BRAND NEW PROJECT** path in [SUPERDESIGN.md](references/SUPERDESIGN.md).

**Real codebase present** (any frontend code, or an existing `.superdesign/init/`) — repo init must have completed at least once before designing. Reuse a valid initialized target through Step 1.5; run the full analysis only when init is incomplete or warm state cannot be used.

**Exception — standalone extraction:** if the task is ONLY to extract a site's design DNA or set/refresh `design-system.md` from a URL (`extract-website` → `design-system.md`, no design generation; read [WEBSITE.md](references/WEBSITE.md) for the recipes), run it WITHOUT repo init — extracting an external site's style doesn't require analyzing the user's codebase. Init is still required before generating designs FOR the existing codebase's UI (reproducing/redesigning an existing page).

**Exception — graphics:** posters/marketing assets (scenario 7) skip init even in a real codebase — the brief carries the style, and most of init's output (components, layouts, routes, pages) has no bearing on a fixed-canvas artwork. The graphic brief round asks whether the artwork should be on-brand with this repo's product ([GRAPHIC.md](references/GRAPHIC.md) Step 1); only an on-brand "yes" pulls in the design-system/brand context — running init first only if that context doesn't already exist.

**Exception — presentations:** slide decks (scenario 6) skip UI repo init by default because routes, components, and page dependency trees do not help deck creation. Follow [PRESENTATION.md](references/PRESENTATION.md). Use narrowly relevant product documents, design-system context, and Brand Assets when the user wants an on-brand product presentation; run init only when matching the codebase brand is required and no usable brand/theme context exists yet.

**Exception — image/video generation:** a standalone generated asset (scenario 8) skips init even in a real codebase. Read [ASSET_GENERATION.md](references/ASSET_GENERATION.md) and gather only the project, brand, reference, or destination context the requested asset actually needs. If the asset is one step inside a broader UI, presentation, or graphic-design task, follow that task's normal init/brief path and use asset generation only at the point where a new visual is needed.

# Step 1.5 — Resume before rediscovery (real-codebase UI path)

Before reading init artifacts or source files, check `.superdesign/resume.json` for the requested route/feature. A matching target defaults to [RESUME.md](references/RESUME.md) regardless of whether the user says "continue", "change", "redesign", or gives only a direct instruction such as "make the dashboard darker". Intent phrasing never decides warm versus cold routing.

Apply the saved target's trust/structural checks FIRST. A safe, structurally valid target reuses the saved project, draft, component records, design direction, and exact `--context-file` bundle: matching hashes go to warm resume, while mismatches go to incremental refresh without cold rediscovery. If a request needs code understanding not captured by the active draft metadata, use RESUME.md's targeted context-expansion rule; do not rerun full discovery merely to understand that request.

Use the cold path only when no saved entry covers the requested target, the user explicitly asks to start over from fresh ground truth, the state is unsafe/structurally invalid, or targeted repair determines it is stale beyond incremental repair. A new agent session, different wording, or a fingerprint mismatch alone never forces cold routing.

# Init: Repo Analysis (real-codebase path)

When a real codebase is present (per Step 1, and no Step 1 exception applies) and init is NOT complete, you MUST automatically:

1. Create the `.superdesign/init/` directory
2. Read [INIT.md](references/INIT.md)
3. Follow its instructions to analyze the repo and write context files

**Init-complete test (one decidable rule, used everywhere):** init is complete only if all six named files below exist AND are non-empty. A directory that is missing any of them, or holds an empty one (e.g. an interrupted init), is NOT complete — rerun the full init, which regenerates all six; overwriting existing files is expected and fine.

Do NOT ask the user to do this manually — just do it.

# Init Files (cold/stale context path)

For a first design of a target, or after [RESUME.md](references/RESUME.md) determines that saved context is stale/unusable, read all six files before collecting the target context:

- `components.md` — shared UI primitives with full source code
- `layouts.md` — shared layout components (nav, sidebar, header, footer)
- `routes.md` — page/route mapping
- `theme.md` — design tokens, CSS variables, Tailwind config
- `pages.md` — page component dependency trees (which files each page needs)
- `extractable-components.md` — components that can be extracted as reusable DraftComponents

On a valid warm resume, only check that all six files exist and are non-empty — do NOT read their contents. Reuse the target's saved context bundle; read only narrowly selected source files when [RESUME.md](references/RESUME.md) explicitly triggers targeted context expansion.

**When cold-designing an existing page**: First check `pages.md` for the page's dependency tree — the candidate set of `--context-file` files. Pass them under the PAYLOAD BUDGET rules in [SUPERDESIGN.md](references/SUPERDESIGN.md) so the payload does not 400. Then also add the globals.css tokens, tailwind.config, and design-system.md. Persist the final selection per [RESUME.md](references/RESUME.md).

# Superdesign CLI (MUST use before any command)

**IMPORTANT: Run the CLI on demand with `npx --yes @superdesign/cli@latest`. Start every session with the bare command — it IS the preflight.**

1. Preflight once:
   ```
   npx --yes @superdesign/cli@latest
   ```
   The bare command verifies everything in one shot: that the CLI runs at all, an `auth:` status line (`authenticated as team "…"` vs `not authenticated — run superdesign login`), and a list of recent projects. On a valid warm resume, use the saved `projectId`/`activeDraftId` directly. Otherwise read the recent-project list when deciding whether to reuse an existing project or `create-project`; `fetch-design-nodes --project-id <id>` is the fallback for recovering draft ids when durable resume state is unavailable or rejected.

2. If the `auth:` line says not authenticated, run login NOW, before any real command:
   ```
   npx --yes @superdesign/cli@latest login
   ```
   Wait for login to complete successfully before proceeding.

3. Run the intended commands with the same `npx --yes @superdesign/cli@latest` prefix. A session can still expire mid-flow — handle a later auth/login error per the failure block below.

> **Never assume the user is already logged in** — read the preflight's `auth:` line instead of guessing or probing with real commands.

## When a command fails

- **Auth/login error** (the CLI ran but rejected the session): run `login` (above), then retry the intended command ONCE. If login itself fails (headless/no-browser auth, expired flow, user declines), tell the user plainly and STOP — do not keep retrying or improvise.
- **`extract-website` fails or times out** (it can take ~60–120s): retry ONCE. If it still fails, offer to continue WITHOUT the extraction (design from the conversation / existing design system) rather than blocking.
- **General rule:** retry a failed command at most once. If `create-design-draft` or `iterate-design-draft` still fails, continue via [design-with-your-model.md](references/design-with-your-model.md); otherwise report the failure and stop.

## Command examples

Always use the full on-demand runner prefix, e.g.:

```bash
npx --yes @superdesign/cli@latest create-project --title "X"
```

Full invocations live at their use sites — the SOPs in [SUPERDESIGN.md](references/SUPERDESIGN.md) and the graphic steps in [GRAPHIC.md](references/GRAPHIC.md); flag sets come from `<command> --help`, and the COMMAND CONTRACT in [SUPERDESIGN.md](references/SUPERDESIGN.md) covers the traps help leaves out.

The CLI defaults to an agent-optimized output (compact TOON plus `help[]` next-step hints); add `--json` only when you need the full machine-readable payload.

# Surface the canvas URL

Every project/draft command's default output includes a `canvas:` link (the project canvas, `https://superdesign.dev/teams/<teamId>/projects/<projectId>`) and, for drafts, a `preview:` link (`https://superdesign.dev/preview/draft/<draftId>`). Read these from the command output — do NOT hand-construct them (the ids are server-generated).

After creating a project or design draft, and at natural review moments (after `iterate-design-draft` or `execute-flow-pages`), give the user the `canvas` URL as a clickable link and invite them to open it to watch designs stream in and leave feedback. Adding `?live=1` to the canvas URL opens the live view where drafts appear as they generate.

## Browser Choice

`create-project` auto-opens the canvas in user's browser by default. Leave it on, and tell the user the canvas was opened (with the `canvas` URL as a clickable link). Only pass `--no-open` when there's no user-facing browser (CI, headless).

# Images and local assets

Before generation, inventory only the images the user attached or the narrowly relevant local assets selected for this target. Follow [SUPERDESIGN.md](references/SUPERDESIGN.md) **ASSET PURPOSE ROUTING**: temporary screenshots/references go to canvas reference nodes; logos, fonts, and reusable identity imagery go to Brand Assets; final-content imagery stays project content. Pass returned node ids or Brand Asset keys with `--reference-id` so create, iterate, and flow generation receive the actual pixels. When any source component or requested design has a logo position, enforce SUPERDESIGN.md's **Logo invariant**: an available appropriate Brand Asset logo must visibly render there, including inside reusable components; never substitute initials, emoji, generic marks, invented SVGs, or text alone. For a pasted direct public image URL or a website reference, read [WEBSITE.md](references/WEBSITE.md) and materialize only the selected visual through the same upload flow. Never bulk-upload the repository and never put local filesystem paths into draft HTML.

# After generating: offer to go further

Always close with a short, warm follow-up that offers to go further (on every surface). Ask one question with 2 to 3 concrete options tailored to what you just made, not a generic list. For example: try a different hero image or key visual direction, try an alternate layout or composition, or generate a few more variations or asset ideas as surprises. Only generate after the user picks, since every generation spends credits.

(Graphics get a dedicated one-round visual self-review before this close — [GRAPHIC.md](references/GRAPHIC.md) Step 5. UI drafts are reviewed by the user on the canvas.)

# How it works

Read [SUPERDESIGN.md](references/SUPERDESIGN.md), then follow its instructions.

For an image or video generation request, read [ASSET_GENERATION.md](references/ASSET_GENERATION.md). Load the other scenario-specific references linked above when those scenarios apply.
