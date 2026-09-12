---
name: postiz
description: >-
  Schedule social posts to any of 30+ providers via a running postiz instance
  (hosted at api.postiz.com or self-hosted). Use this skill whenever someone
  wants to post, schedule, or publish a draft to LinkedIn, Reddit, Bluesky,
  Mastodon, Threads, Instagram, TikTok, YouTube, Pinterest, Discord, Slack, or
  any non-Twitter social channel. ALWAYS chain content-atomizer first for
  platform-specific copy — this skill is a distribution layer only, it does
  not rewrite copy. For Twitter/X threads, use typefully instead (better
  thread UX). Triggers: "post to linkedin", "post to reddit", "post to
  bluesky", "post to mastodon", "post to threads", "schedule via postiz".
category: distribution
tier: must-have
layer: distribution
reads:
  - brand/voice-profile.md
depends-on:
  - content-atomizer
env_vars:
  - POSTIZ_API_KEY
  - POSTIZ_API_BASE
triggers:
  - post to linkedin
  - post to reddit
  - post to bluesky
  - post to mastodon
  - post to threads
  - schedule via postiz
allowed-tools:
  - Bash(mktg publish *)
  - Bash(mktg catalog *)
  - Bash(mktg doctor *)
---

# Postiz — Social Distribution Layer

You schedule pre-written social posts to LinkedIn, Reddit, Bluesky, Mastodon, Threads, Instagram, TikTok, YouTube, Pinterest, Discord, Slack, and any other provider a running postiz instance supports. You do NOT write copy. You do NOT tailor per platform. Upstream skills (content-atomizer, social-campaign) deliver platform-specific text; you turn it into drafts in postiz.

For Twitter/X threads, defer to `typefully` — its thread UX is canonical. You handle everything else.

## North Star

Postiz is a distribution execution layer in the mktg playbook:

1. You never generate or rewrite copy.
2. You never choose the platform mix — that's the user's ask or social-campaign's plan.
3. You never retry a failed post without first consulting the sent-marker file at `.mktg/publish/{campaign}-postiz.json` — postiz has no idempotency key, and retries duplicate.
4. You always use `mktg publish --adapter postiz` — never call the postiz API directly from the skill. The adapter owns rate-limit handling, 401/429 envelopes, and the two-step integration.id resolution.

## On Activation

Run these 4 steps before anything else. Each step has a fallback that keeps the skill useful even when postiz is absent.

### Step 1 — Verify the catalog is registered and configured

```bash
mktg catalog info postiz --json --fields configured,missing_envs,auth.credential_envs,resolved_base
```

`catalog info <name>` returns the full `CatalogEntry` plus computed `configured`/`missing_envs`/`resolved_base` fields. The command errors with exit code 1 (NOT_FOUND) if the catalog is not in `catalogs-manifest.json` — that's the "not registered" signal.

- Exit code 1 → postiz catalog is not registered. Tell the user: `mktg catalog add postiz --confirm`. Stop.
- `configured: false` → env vars are missing. Build the fix string from `missing_envs` rather than hardcoding. Canonical expectation: `POSTIZ_API_KEY` (required) and `POSTIZ_API_BASE` (defaults to `https://api.postiz.com` if unset; the catalog loader returns `resolved_base: null` in that case and the skill applies the default). Stop.
- `configured: true` → proceed to Step 2.

### Step 2 — Resolve connected provider identifiers (cached)

```bash
mktg publish --adapter postiz --list-integrations --json
```

Returns `{ adapter, integrations: [{ id, identifier, name, profile, disabled, picture, customer }, ...] }` from `GET /public/v1/integrations`. Cache in `.mktg/cache/postiz-integrations.json` (TTL 15 minutes). Use this to validate the user's requested providers before publish — fail fast if they ask for `"pinterest"` and it isn't connected.

**Critical: `identifier` is a postiz-native provider-module key, NOT a platform display name.** Single-variant providers collapse to the expected string (`"reddit"`, `"bluesky"`, `"mastodon"`, `"threads"`), but some platforms ship multiple identifiers:

| Platform | Possible postiz `identifier` values |
|---|---|
| LinkedIn | `linkedin` (personal profile), `linkedin-page` (company page) — distinct integrations |
| YouTube | may vary by postiz version (channel vs shorts flavors) |
| Other | any string postiz's provider module exports |

The adapter does **exact-match** on `identifier` (no alias layer) — if the user says *"post to LinkedIn"* and the instance only has `linkedin-page` connected, the adapter will refuse `"linkedin"`. Alias handling is your job in Step 2b.

### Step 2b — Handle user friendly-name aliasing (skill-layer only)

When the agent hears *"post to LinkedIn"* (a platform name, not a postiz identifier), map the friendly name to the right postiz identifier(s):

1. Look up the cached integrations from Step 2.
2. Find all identifiers whose display name or known-alias matches the user's phrase. For LinkedIn, both `linkedin` and `linkedin-page` match.
3. If exactly one matches → use it.
4. If multiple match → present the options via AskUserQuestion. *"You have both `linkedin` (personal) and `linkedin-page` (company) connected. Which?"* Let the user pick; cache their choice in `.mktg/cache/postiz-aliases.json` for future sessions.
5. If zero match → error: *"'LinkedIn' is not connected in this postiz instance. Connected: {enumeration}. Connect it in the postiz UI first."*

**Alias resolution lives here and NEVER in the adapter** — the adapter takes whatever you pass as `metadata.providers` and resolves against the live integrations verbatim.

### Step 3 — Chain to content-atomizer FIRST if content is raw

If the user's input is a blog post, article, or long-form source (length > 500 chars or file extension `.md` in `marketing/content/`), you MUST chain `/content-atomizer` first to produce platform-native copy. Feed the atomizer's output files (`linkedin-posts.md`, `reddit-posts.md`, etc.) into this skill.

If the user's input is already platform-tailored (short-form text targeting one platform), skip atomization and proceed.

### Step 4 — Tone-check against voice-profile (sanity guard only)

Read `brand/voice-profile.md` if it exists. Before building the publish manifest, verify each post:
- Does the tone spectrum match (not wildly off-brand)?
- Is the length within the platform's character limit **and** within the voice profile's stated sentence-rhythm range?

If a check fails, surface a warning to the user and ask before proceeding. **Never rewrite.** That's content-atomizer's job — bounce back there.

## How to Use

This skill runs in one of two modes. Pick by looking at the input.

### Mode A — Single post to one or more platforms

User says: *"Post this to LinkedIn and Bluesky"* + paste text.

1. Run the On Activation steps above. Step 2b resolves any user-said platform names ("LinkedIn") to postiz identifiers (`linkedin` or `linkedin-page` or both).
2. Build a single-item `publish.json`. The manifest's top-level `name` is the campaign identifier (the adapter threads this into sent-marker keys — do NOT also put `campaign` in `metadata`; the adapter ignores it):
   ```json
   {
     "name": "ad-hoc-{timestamp}",
     "items": [{
       "type": "social",
       "adapter": "postiz",
       "content": "<the user's text verbatim>",
       "metadata": { "providers": ["linkedin", "bluesky"] }
     }]
   }
   ```
3. `mktg publish --adapter postiz --dry-run --input '<manifest>' --json` — preview.
4. On user confirm: `mktg publish --adapter postiz --confirm --input '<manifest>' --json`.
5. Report per-provider status from the adapter's response envelope.

### Mode B — Campaign from content-atomizer output

User says: *"Schedule my atomized blog post to LinkedIn, Reddit, and Threads"*.

1. Run On Activation.
2. Read `marketing/social/{source-slug}/linkedin-posts.md`, `reddit-posts.md`, `threads-posts.md`. Each file contains one or more posts with YAML frontmatter matching the atomizer's contract.
3. Build a multi-item `publish.json` with one item per (file × post). Each item's `metadata.providers` is a single-element array matching the file's platform.
4. Same dry-run → confirm → report flow as Mode A.

### Example 1 — LinkedIn-only draft

```bash
mktg publish --adapter postiz --confirm --input '{
  "name": "linkedin-announcement",
  "items": [{
    "type": "social",
    "adapter": "postiz",
    "content": "We shipped v2.0 today. Here is what changed...",
    "metadata": { "providers": ["linkedin"] }
  }]
}' --json
```

### Example 2 — Cross-platform (atomizer output + postiz distribution)

```bash
/content-atomizer marketing/content/blog/v2-announcement.md
# Atomizer writes marketing/social/v2-announcement/{linkedin,reddit,threads}-posts.md

# Build a publish.json with one item per atomized post, then:
mktg publish --adapter postiz --dry-run --json < <tmp_publish_manifest.json>
# Review → confirm:
mktg publish --adapter postiz --confirm --json < <tmp_publish_manifest.json>
```

### Example 3 — Mixed batch (postiz + typefully)

This is the social-campaign Phase 5 path. You do NOT handle this standalone — the orchestrator in social-campaign routes per-post per the Phase 5 routing table.

## Inputs

| Input | Required | Shape | Notes |
|---|---|---|---|
| `content` | yes | string | Platform-tailored post text. Must fit the target platform's character limit (LinkedIn 3000, Reddit no limit, Bluesky 300, Mastodon 500, Threads 500). Failing this → Step 4 tone-check surfaces a warning. |
| `metadata.providers` | yes | string[] | **Postiz identifiers, not platform display names.** Canonical examples: `"linkedin"` (personal), `"linkedin-page"` (company page), `"reddit"`, `"bluesky"`, `"mastodon"`, `"threads"`, `"instagram"`, `"tiktok"`, `"youtube"`, `"pinterest"`, `"discord"`, `"slack"`. Must match `identifier` exactly from `GET /public/v1/integrations`. Unknown identifiers fail fast per-item with the connected list in the error. Alias resolution (user says "LinkedIn" → you pick `linkedin` vs `linkedin-page`) happens in Step 2b, never in the adapter. |
| `metadata.mediaPaths` | no | string[] | v2 stub — **ignored in v1** (draft-only, images hardcoded to `[]` in the adapter). Don't populate this field in v1 manifests; it has no effect. |

**Campaign identifier does NOT live in `metadata`.** The adapter reads it from the publish manifest's top-level `name` field. If you set `metadata.campaign`, the adapter silently ignores it. Never emit `metadata.campaign`.

**Validation performed at publish-time, before the network:**
- Control chars in `content` are rejected via the base pipeline's `rejectControlChars`.
- For each item, any identifier in `providers` that isn't in the cached `/public/v1/integrations` result produces a per-item `failed` result with `detail: "Unconnected provider(s): X. Connected: {list}. Connect in the postiz UI first."`. The adapter does NOT short-circuit the whole batch — items with fully-connected providers still publish.
- Missing `metadata.providers` fails per-item with `detail: "Missing item.metadata.providers[] — add at least one postiz identifier"`.

## Outputs

The adapter returns the standard `AdapterResult` envelope:

```json
{
  "adapter": "postiz",
  "items": 3,
  "published": 3,
  "failed": 0,
  "errors": [],
  "results": [
    { "item": 0, "status": "published", "detail": "draft id=abc123 provider=linkedin" },
    { "item": 0, "status": "published", "detail": "draft id=abc124 provider=reddit" },
    { "item": 0, "status": "skipped",   "detail": "dedupe: sent-marker match" }
  ]
}
```

**Per-provider fan-out:** one input item with N providers becomes N entries in `results[]`, each with its own status. A partial failure (Reddit rate-limited, LinkedIn succeeded) does NOT fail the whole item.

**Exit-code aggregation:** the top-level `publish` command exits **0** whenever at least one item succeeds. Top-level non-zero exit only when ZERO items succeed. This matches how `typefully` and `resend` adapters already behave. Inspect `results[]` for per-item outcomes — a successful publish run can still have failed providers inside it.

**Sent-marker side-effect:** successful publishes append to `.mktg/publish/<campaign>-postiz.json` with a stable hash key. Re-running the same campaign is a no-op for already-sent items.

**Platform coverage table (UI hint):** after a run, render a small confirmation table showing per-provider status, draft ID, and notes.

## Anti-Patterns

| Anti-Pattern | Why it fails | Instead |
|---|---|---|
| Generate copy in this skill | Voice drift — each skill that rewrites copy diverges from `voice-profile.md`. We have one generation path (content-atomizer) for a reason: platform-specific copy rules live there. If you inline paraphrasing here, the voice profile's guardrails don't fire. | Chain `/content-atomizer` first. Feed its file output into this skill. |
| Retry a failed post without checking the sent-marker | Postiz has no idempotency key and no webhooks. A retry without checking `.mktg/publish/<campaign>-postiz.json` duplicates the draft — if the user accepted the first one before the adapter crashed, you just ship the post twice. | Always call the adapter. The adapter consults the sent-marker *before* POSTing. Never construct your own HTTP request. |
| Call the postiz API from within this skill | Every HTTP caller reinvents error handling. The adapter owns 401 (bad key), 429 (rate limit with Retry-After), 400 (bad provider), and network timeouts — each with structured `fix` fields. Skipping the adapter loses these. | `mktg publish --adapter postiz ...`. Always. |
| Pass postiz `integration.id` DB primary keys in `metadata.providers` | `integration.id` values are database rows — they change between environments (hosted vs self-host vs fresh install). A hardcoded `"42"` breaks the moment the user rotates their instance. | Pass postiz **identifiers** (`"linkedin"`, `"linkedin-page"`, `"bluesky"`) verbatim — these are provider-module keys that are stable across instances. The adapter does the identifier → id lookup. |
| Translate user-said platform names to identifiers in the adapter | Alias drift: the moment postiz ships a new provider module, any in-adapter alias layer becomes wrong. The adapter does exact-match on `identifier`; aliasing is a SKILL-layer concern. | Handle alias resolution in Step 2b of On Activation (this skill). Pass exact postiz identifiers to the adapter. |
| Populate `metadata.campaign` in publish items | Redundant: the adapter threads `manifest.name` into sent-marker keys. If you also set `metadata.campaign`, the adapter ignores it — confusion for the agent about which wins. | Use the top-level `manifest.name` field as the campaign identifier. Don't duplicate into `metadata`. |
| Populate `metadata.mediaPaths` in v1 | v1 is draft-only; the adapter hardcodes images to `[]`. Setting `mediaPaths` silently no-ops and wastes tokens. | Leave `mediaPaths` out of v1 manifests. Image support lands in v2 alongside `schedule` / `now` post types. |
| Skip dry-run and go straight to `--confirm` | 30 drafts/hour is a tight rate limit; burning quota on broken manifests is wasteful. Dry-run validates providers and env vars without touching the network. | Always dry-run first. |
| Use this skill for X threads | Typefully owns threads — better UX, per-tweet character validation, and thread-unroll view. Postiz can post to X but thread authoring is weak. | Twitter/X single post OR thread → `typefully`. Everything else → this skill. |

## Progressive Enhancement

| Level | State | Experience |
|---|---|---|
| L0 | No brand files, no postiz configured | Activation step 1 fails with `configured: false` and emits a clean fix: set `POSTIZ_API_KEY` and optionally `POSTIZ_API_BASE`. No network calls, no partial state, no crash. Exit code 3 (dependency missing). |
| L1 | `POSTIZ_API_KEY` set, `POSTIZ_API_BASE` defaulted to `https://api.postiz.com` | The skill works for every platform the hosted instance supports. `voice-profile.md` absent → tone-check is a no-op. User feeds raw copy → warning suggests chaining content-atomizer but doesn't block. |
| L2 | + `voice-profile.md` | Tone-check fires. Posts that violate length or tone spectrum surface warnings before the publish confirm prompt. Still functional without atomization. |
| L3 | + `content-atomizer` has run and written `marketing/social/{slug}/` | Mode B is available. Batch-publish N atomized posts across M platforms with one confirm. |
| L4 | + full brand + postiz configured + content-atomizer chain | End-to-end: user says "launch my blog post on LinkedIn/Reddit/Bluesky", orchestrator routes, atomizer writes, postiz publishes. Voice honored; sent-markers prevent dupes; partial failures roll forward. |

This skill never fails silently. At every level, the user either gets structured output (publish succeeded/failed) or a structured error with a `fix` field. Absent postiz, the skill errors cleanly — no half-finished drafts.

## Related Skills

- **content-atomizer** — generates platform-specific copy. MUST run before this skill for long-form source content.
- **typefully** — X/Twitter thread handling. Complements this skill (X threads → typefully; everything else → this skill).
- **social-campaign** — orchestrator that chains strategy/write/review/design/schedule. In Phase 5, it picks the scheduling backend per platform.
- **brand-voice** — writes `voice-profile.md`, which this skill reads as a sanity guard in Step 4.
