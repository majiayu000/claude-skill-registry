---
name: mktg-setup
description: >
  First-run conversational setup wizard for marketing-cli. Use when /cmo
  detects no populated brand files and no cmo-preferences.md, when the user
  just installed marketing-cli for the first time, or when they say things
  like "set up marketing", "start marketing", "marketing wizard", "I just
  installed marketing-cli", "onboard me", "first time", "initial setup".
  Asks 3 sharp questions (identity, posture, distribution preferences),
  records the answers to brand/cmo-preferences.md, then hands off to /cmo's
  foundation flow which spawns 3 research agents in parallel. The user never
  has to type /mktg-setup directly — /cmo auto-routes here on first run.
allowed-tools:
  - Bash(mktg *)
  - Bash(mkdir *)
  - Bash(test *)
  - Bash(cat *)
---

# /mktg-setup — First-Run Conversational Setup

## When This Runs

`/cmo` invokes this skill automatically when both conditions are true:

1. `brand/cmo-preferences.md` does not exist (or is template content), AND
2. `mktg status --json` reports `brandSummary.populated < 3`.

The user typically never types `/mktg-setup`. They install marketing-cli (`npm i -g marketing-cli`), open Claude Code in any project directory, type `/cmo` (or just say "help me with marketing"), and `/cmo`'s activation routes here. The wizard is a conversational on-ramp, not a slash command users have to memorize.

## What This Skill Does

Three AskUserQuestion calls. That is the entire wizard. No batched questions, no progress bars, no long forms.

Each answer becomes a persistent decision in `brand/cmo-preferences.md`. After question 3, hand off to `/cmo`'s foundation flow (3 research agents in parallel — see `cmo/rules/sub-agents.md`).

The wizard's job is to record the small set of decisions Claude cannot make for the user. Filling out the 10 brand files is `/cmo`'s job, not the wizard's.

## On Activation

1. Run `mktg status --json --fields project,brand,brandSummary` from the project root.
2. If `brandSummary.populated >= 3` AND `cmo-preferences.md` doesn't exist: a returning user got upgraded to a version that introduced preferences. Tell them: "I see you have a populated brand but no preferences file yet. I'll write one based on what's already here." Skip directly to step 3 (write preferences) using inferred defaults from existing brand files.
3. If `cmo-preferences.md` already exists and is non-template: skip the wizard entirely. Hand back to `/cmo` immediately. Tell the user: "Looks like you've already onboarded. Hand off to /cmo for your next move."
4. Otherwise (genuine first run): proceed to Step 1.

---

## Step 1 — Ask: Identity

Step 1 is a single-select question (1a) plus exactly one free-text follow-up (1b or 1c). Don't merge them and don't add extra prompts in between.

### Step 1a — Setup mode

Use AskUserQuestion. Single-select.

**Question text:** "How should we set up your brand?"

**Options:**
- "From a URL — I'll scrape your site to seed brand files (recommended if you have a website)"
- "Local conversational setup — I'll ask a few questions instead"
- "Pre-launch / open source / personal brand — describe in 1 sentence"

The user's choice determines the follow-up:
- **"From a URL"** → go to **Step 1b** (URL capture).
- **"Local conversational setup"** OR **"Pre-launch / open source / personal brand"** → go to **Step 1c** (sentence capture).

### Step 1b — URL capture (only if Step 1a = "From a URL")

Use AskUserQuestion. Single-select with the "Other" free-text path (so the user can paste the URL inline).

**Question text:** "Paste your URL"

**Options:**
- "I'll paste the URL in the next message" — the user types the URL in their next chat message.
- (Use the built-in "Other" free-text option for inline URL entry — paste-and-go.)

Capture the URL exactly as the user provides it. **Do NOT validate it inside the wizard** — no regex, no protocol check, no normalization. Pass the raw string straight to the CLI:

```bash
mktg init --from <url>
```

`mktg init --from` is the single source of truth for URL handling. If the URL is malformed, unreachable, or scrape-blocked, the CLI surfaces the error; the wizard relays that error to the user and falls back to the local sentence path (offer "I'll describe it in one sentence instead" without re-asking Step 1a).

On success, the scrape seeds `brand/voice-profile.md`, `brand/positioning.md`, `brand/audience.md`, and `brand/competitors.md`. Hold the captured URL and the "scrape ran" status (yes/no) for Step 5.

### Step 1c — Sentence capture (only if Step 1a = "Local conversational setup" OR "Pre-launch / open source / personal brand")

No URL here — this is the deliberate no-URL path. Ask a single short follow-up:

> "Got it — describe what we're marketing in one sentence."

Capture the response verbatim. Hold it as the seed for `brand/voice-profile.md` (it lands in the "What we are" section during Step 5 / foundation flow). Don't run `mktg init --from`; the foundation research agents fill the gaps.

---

## Step 2 — Ask: Posture

Use AskUserQuestion. Single-select.

**Question text:** "What's the marketing posture you want?"

**Options:**
- "Aggressive launch" — Product Hunt + Hacker News + X campaign blitz. Best for new product launches with momentum to capture.
- "Steady authority build" — SEO + newsletter + slow-burn thought leadership. Best for long-game category ownership.
- "Founder-led / personal brand" — voice-driven content, personality forward. Best when the founder IS the differentiator.
- "Product-led growth" — free tier hooks, referrals, viral mechanics. Best when the product itself drives acquisition.

This is the single most important answer. It shapes which skills `/cmo` prioritizes downstream:

| Posture | Skills /cmo prioritizes |
|---|---|
| aggressive-launch | `launch-strategy`, `startup-launcher`, `social-campaign`, `direct-response-copy` |
| steady-authority | `seo-content`, `keyword-research`, `newsletter`, `ai-seo` |
| founder-led | `brand-voice`, `voice-extraction`, `content-atomizer`, `mktg-x` |
| product-led-growth | `free-tool-strategy`, `referral-program`, `lead-magnet`, `conversion-flow-cro` |

---

## Step 3 — Ask: Distribution

Use AskUserQuestion. multiSelect = true.

**Question text:** "Which distribution channels should we wire up first?"

**Options:**
- "Typefully" — X/Twitter and threads. Best for short-form and thread-first audiences.
- "Postiz" — LinkedIn, Reddit, Bluesky, Mastodon, Threads, Instagram, TikTok, etc. (30+ providers via the postiz catalog).
- "Resend" — transactional email and newsletter delivery.
- "Skip for now — I'll connect later" — `/cmo` will use `--adapter file` for export until the user wires something up.

Multiple selections are fine. If the user picks "Skip", record that explicitly — a deliberate skip is signal, not absence of data.

---

## Step 4 — Ask: Studio (beta)

Use AskUserQuestion. Single-select.

**Question text:** "Want to use the Studio dashboard? (beta)"

**Options:**
- "Yes — auto-open the Studio at the end of setup (recommended)" — `/cmo` will run `mktg studio` automatically at the end of foundation flow and on subsequent activations when the user says "show me the dashboard."
- "No — keep me in the CLI only" — `/cmo` will not auto-launch Studio. The user can still run `mktg studio` manually any time.

Why this question: Studio is in beta. Some users prefer pure CLI workflows (especially headless/agent-only environments). Recording the choice once means /cmo never nags later.

If the user picks "No", `/cmo` reads `studio_enabled: no` from preferences and skips the studio launch step in its foundation flow. If they later change their mind, they can edit `brand/cmo-preferences.md` directly or just say "let's open studio" and /cmo will respect the explicit ask.

---

## Step 5 — Write Preferences

Create `brand/cmo-preferences.md` with this shape:

```markdown
# CMO Preferences

> Recorded by /mktg-setup on {ISO 8601 date}. Edit this file to change /cmo's runtime behavior.
> /cmo reads this file on every activation and uses it to shape skill prioritization and distribution routing.

## Identity

- **What we're marketing**: {URL or one-sentence description from Step 1}
- **Setup mode**: {from-url | local | pre-launch}
- **URL**: {captured URL if Setup mode is from-url, otherwise omit this line}
- **Scrape ran**: {yes if mktg init --from succeeded, no if from-url failed or mode is local/pre-launch}

## Posture

- **Mode**: {aggressive-launch | steady-authority | founder-led | product-led-growth}
- **Why this mode**: {one-line rationale based on the user's choice — pull from the option description in Step 2}
- **Skill priority shortlist**: {comma-separated list from the posture-to-skills mapping}

## Distribution

- **Selected**: {comma-separated list of selected platforms, or "none" if skipped}
- **Skipped**: {whichever options weren't selected}
- **Default adapter**: {typefully if X selected and only X | postiz if multi-platform | file if skipped}

## Studio

- **studio_enabled**: {yes | no}
- **Beta**: yes (Studio is in beta — record the user's preference; /cmo respects this on every activation)
- **Auto-open at end of setup**: {yes if studio_enabled is yes, no otherwise}

## Notes

- This file is the persistent contract. /cmo reads it on every activation.
- To change preferences, edit this file directly OR ask Claude to "re-run mktg setup" (it will overwrite this file).
```

Make sure the directory exists before writing:

```bash
test -d brand || mkdir -p brand
```

---

## Step 6 — Hand Off to /cmo

**SEO backend handoff (before spawning agents):** run `mktg seo status --json --fields readiness,catalog.endpointError,project`. OpenSEO is the default SEO data plane (measured KD, volume, SERP, backlinks, GSC).

- Any `*_ready` state → tell the user: "OpenSEO is configured. After foundation, I'll verify it with the free `whoami` tool and link a project (`mktg seo link-project`) so keyword research can use measured metrics." After the foundation chain, if `.seo/openseo.json` is still missing, recommend `/openseo-project-setup` as the first SEO move.
- `not_configured` → one line only, no blocking: "OpenSEO isn't set up — keyword metrics will be `unknown` until it is. Setup takes a minute: openseo.so → connect the hosted MCP with OAuth, or set OPENSEO_API_KEY for headless use." Never install anything or ask for keys inside the wizard.

Tell the user clearly what's happening next. Tailor the closing line to their Studio choice:

- **studio_enabled = yes** → "Recorded your preferences. Now I'm spawning 3 research agents in parallel — brand voice, audience, and competitors — to fill out your foundation. ~5 minutes. Then I'll auto-open the Studio dashboard."
- **studio_enabled = no** → "Recorded your preferences. Now I'm spawning 3 research agents in parallel — brand voice, audience, and competitors — to fill out your foundation. ~5 minutes. Studio stays off per your choice; I'll surface results in the CLI."

Then invoke the foundation flow per `cmo/rules/sub-agents.md`:

1. Spawn `mktg-brand-researcher` with the identity context from Step 1
2. Spawn `mktg-audience-researcher` with the posture context from Step 2
3. Spawn `mktg-competitive-scanner` with both

Wait for all 3, then chain:
- `/landscape-scan` for ecosystem grounding
- `/positioning-angles` to lock the angle
- **If `studio_enabled` is `yes`**: run `mktg studio` to auto-open the dashboard with the populated state.
- **If `studio_enabled` is `no`**: skip the Studio launch. Print a one-line summary of what was populated and the next recommended skill in the CLI. Tell the user: "Studio's off per your preference. If you change your mind, edit `brand/cmo-preferences.md` or just say 'open studio'."

---

## Anti-Patterns

| Anti-pattern | Instead | Why |
|---|---|---|
| Asking more than 3 questions in the wizard | Stop at 3 — hand off to /cmo for the rest | More questions = abandonment. /cmo's research agents fill the rest in 5 minutes via real research. |
| Asking for a URL before letting the user pick a setup mode | Always ask Step 1a (setup mode) first, then branch to Step 1b (URL) or Step 1c (sentence) | URL is just one of three paths. Pre-launch / open-source / personal-brand users don't have a URL yet, and the local conversational path bypasses the scrape entirely. Forcing a URL up front blocks them. |
| Validating the URL inside the wizard (regex, http vs https, "is this real?") | Pass the raw string straight to `mktg init --from <url>` and let the CLI handle malformed inputs | The CLI already returns structured errors for bad URLs. Re-validating in the wizard duplicates logic, drifts from the CLI, and frustrates users who paste valid-but-unusual URLs. |
| Silently routing to brand-voice / audience-research before recording preferences | Always record `cmo-preferences.md` FIRST | Without it, every future `/cmo` activation re-runs the wizard. The preferences file is the contract that prevents that. |
| Skipping the wizard if voice-profile.md exists but cmo-preferences.md doesn't | Run the wizard regardless of other brand files (use the migration path in step 2) | `cmo-preferences.md` is the persistent contract — separate from brand content. A user who upgraded from pre-mktg-setup needs to record their posture explicitly. |
| Treating "Skip distribution" as missing data | Record the skip explicitly as `selected: none` and `default_adapter: file` | A deliberate skip is signal. The user told us not to wire anything yet — respect that. |
| Spawning research agents BEFORE writing cmo-preferences.md | Always write the file first | If the user kills the conversation mid-research, we lose the preferences. The file write is the savepoint. |
| Letting the user re-run the wizard accidentally | After writing the file, /cmo on the next activation will see it and skip the wizard | This is the whole point of the persistent contract. /cmo only re-routes here when the file is missing. |

---

## Iteration / Re-Running

The user can change their preferences three ways:

1. **Edit `brand/cmo-preferences.md` directly** — it's just markdown.
2. **Ask Claude**: "I want to change my marketing posture" — `/cmo` will re-route here, overwriting the file.
3. **Future**: `mktg setup --force` (CLI flag, not yet implemented at v0.5.0; tracked for a future release).

---

## Dependencies

- Reads: `mktg status --json`, optionally URL via `mktg init --from <url>`.
- Writes: `brand/cmo-preferences.md` (new). Optionally seeds `brand/voice-profile.md` if the user provided a sentence in Step 1.
- Hands off to: `/cmo` foundation flow (which spawns the 3 research agents and chains `/landscape-scan` → `/positioning-angles` → `mktg studio`).
