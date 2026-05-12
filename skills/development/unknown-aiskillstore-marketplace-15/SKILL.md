---
name: wonda-cli
description: Using the Wonda CLI to generate images, videos, music, and audio from the terminal — plus LinkedIn, Reddit, and X/Twitter research and automation
---

# Wonda CLI

Wonda CLI is a content creation toolkit for terminal-based agents. Use it to generate images, videos, music, and audio; edit and compose media; publish to social platforms; and research/automate across LinkedIn, Reddit, and X/Twitter.

## Install

If `wonda` is not found on PATH, install it first:

```bash
# npm
npm i -g @degausai/wonda

# Homebrew
brew tap degausai/tap && brew install wonda
```

## Setup

- **Auth**: `wonda auth login` (opens browser, recommended) or set `WONDA_API_KEY` env var
- **Verify**: `wonda auth check`

### Access tiers

Not all commands are available to every account type:

| Tier                                        | Access                                                                                                                           |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| **Anonymous** (temporary account, no login) | Media upload/download, editing (`video/edit`, `image/edit`, `audio/edit`), transcription, social publishing, scraping, analytics |
| **Free** (logged in, Basic/Free plan)       | Everything above + **generation** (`image/generate`, `video/generate`, etc.), styles, recipes, brand                             |
| **Paid** (Plus, Pro, or Absolute plan)      | Everything above + **video analysis** (requires credits), **skill commands** (`wonda skill install/list/get`)                    |

If a command returns a `403` error, check your plan at https://app.wondercat.ai/settings/billing.

### Social signups (Instagram, TikTok, etc.)

Drive them with the `wonda device` primitives + a throwaway mailbox from `wonda email`. The screenshot → decide → tap/type/swipe loop is how these flows work — there's no shortcut command, and that's fine: social apps change their UI constantly and any canned flow would drift faster than you could maintain it.

Standard loop:

1. `wonda email account create --random` → save `{email, password}`. Persist the resulting platform login with `wonda credentials create --website instagram.com --username <handle> --email <email> --password-stdin <<< "<pw>"` (passwords are AES-256-GCM encrypted at rest; retrieve later with `wonda credentials get <id>`).
2. `wonda device create` → pick a `ready` device (poll `wonda device get <id> --fields status`).
3. `wonda device launch <device-id> com.instagram.android` (or `com.zhiliaoapp.musically` for TikTok). Fall back to `wonda device open-url` if you'd rather start in the web flow.
4. Loop: `wonda device screenshot <device-id> > s.json` → decode the base64 PNG → read → pick an action → `tap | type | swipe | key` → screenshot again. Use `--text "SomeButtonLabel"` on `tap` before guessing coordinates; fall back to `--x --y` read off the screenshot for elements without matching text (number pickers, date spinners, etc.).
5. When the app sends a verification email, `wonda email inbox wait <email> --timeout 120` — returns `{codes: ["483921"], links: [...]}` with the 6-digit code already extracted. `wonda device type <device-id> --text "<code>"` to feed it back. **Race-safety**: capture a timestamp _before_ triggering the signup (`SINCE=$(date -u +%FT%TZ)`) and pass `--since "$SINCE"` — otherwise a fast mail server can land the email before your wait call and the old snapshot filters it out.
6. For number/date spinners: tap on the highlighted cell, Android pops up a numeric or alphabetic keyboard, `wonda device type --text "<value>"` replaces the selected text. `wonda device key --code 4` dismisses the keyboard when done.

**Consent-like taps** — anything that accepts Terms/Privacy/Cookies, grants permissions, or publishes something. Before starting an automation that may hit these, ask the user once in chat whether to auto-accept them. If they say yes, tap through without pausing; if they say no, stop at each one and confirm. This does not apply to CAPTCHAs or "prove you're human" puzzles — always hand those off via `wonda device stream` (see next section).

**Rate-limit signals** — if the app shows you a visual puzzle ("we want to make sure you're a real person"), stop and hand off to the user with `wonda device stream <id>` (see next section). Don't click through puzzles yourself.

### Credentials vault

Persist logins created on external platforms (Instagram, TikTok, Twitter, etc.) so they can be reused on the next run. Passwords are AES-256-GCM encrypted with a server-side key and only decrypted on `get`.

```bash
# Create
wonda credentials create --website instagram.com --username myhandle \
  --email me@example.com --password-stdin <<< "hunter2" \
  --metadata '{"signup_source":"wonda-email"}'

# List (passwords omitted)
wonda credentials list --website instagram.com

# Get full record including decrypted password
wonda credentials get <id>

# Update any field (use --password-stdin to rotate; --username "" to clear)
wonda credentials update <id> --username newhandle

# Delete
wonda credentials delete <id>

# Fetch + record why you're using it in one call — POST, not GET, because
# it writes a 'used' event with the reason. Prefer this over `get` whenever
# you can articulate the reason.
wonda credentials use <id> --reason "instagram signup flow"

# See recent events (created / used / rotated / updated) for audit
wonda credentials events <id>
```

Fields: `website` (required — typed input like `insta` is canonicalized to `instagram.com`), `username`, `email`, `password` (required), `metadata` (arbitrary JSON). At least one of `username` / `email` must be present. Multiple records per `(website, username)` are allowed — dedupe on your side if you need to.

**Event log**: every `credentials get`/`use`, `create`, password rotate, and other updates are recorded as events on the credential (actor: `cli` | `web` | `system`). Use `credentials events <id>` or the web UI's history icon to audit. The event log is append-only and cascades on credential delete.

### Handing off to a human

If automation hits a screen that requires a human to take over (consent flow you shouldn't auto-accept, ambiguous UI, step where the user prefers to act themselves), use `wonda device stream <device-id>` — returns a `playerUrl` signed with a short-lived JWT (1h). Give that URL to the user, they act in their own browser, and automation can resume afterward.

```bash
wonda device stream <device-id>
# → { "streamUrl": "wss://…", "playerUrl": "https://…", "deviceType": "social" }
```

### Global output flags

All commands support these output control flags:

- `--json` — Force JSON output (auto-enabled when stdout is piped)
- `--quiet` — Only output the primary identifier (job ID, media ID, etc.) — ideal for scripting
- `-o <path>` — Download output to file (implies `--wait`)
- `--fields status,outputs` — Select specific JSON fields
- `--jq '.outputs[0].media.url'` — Filter JSON output with a jq expression

## How to think about content creation

You are a marketing director with access to a full production toolkit. Before touching any tool, think:

1. **What product category?** (beauty, food, tech, fashion, fitness, etc.)
2. **What format performs for this category?** (UGC memes for everyday products, cinematic for luxury, before/after for transformations, testimonial for services)
3. **What's the hook?** (relatable scenario, surprising twist, aspirational lifestyle, social proof)
4. **What specific scene?** (not "product on table" but "person discovering the product in a funny situation")

## Decision flow

When asked to create content, follow this order:

### Step 1: Gather context

```bash
wonda brand                                                    # Brand identity, colors, products, audience
wonda analytics instagram                                      # What content performs well
wonda scrape social --handle @competitor --platform instagram --wait  # Competitive research (if relevant)

# Cross-platform research (if relevant)
wonda x search "topic OR keyword"                              # Find conversations on X/Twitter
wonda x user-tweets @competitor                                # Competitor's recent tweets
wonda reddit search "topic" --sort top --time week             # Reddit discussions
wonda reddit feed marketing --sort hot                         # Subreddit trends
wonda linkedin search "topic" --type COMPANIES                 # LinkedIn company/people research
wonda linkedin profile competitor-vanity-name                  # LinkedIn profile intel
```

### Step 2: Check content skills

Content skills are step-by-step guides for common content types. Each skill tells you exactly which models, prompts, and editing operations to use — and in what order. ALWAYS check skills before building from scratch.

```bash
wonda skill list                                # Browse all content skills
wonda skill get <slug>                          # Full step-by-step guide for a skill
```

**Full skill index:**

| Slug                      | Description                                                                                                                           | Input                         |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| product-video             | Product/scene video — prompt library for all categories                                                                               | optional product image        |
| ugc-talking               | Talking-head UGC — single clip, two-angle PIP, or 20s+ with B-roll                                                                    | optional reference            |
| ugc-reaction-batch        | Batch TikTok-native UGC reactions with viral strategy                                                                                 | optional product image        |
| tiktok-ugc-pipeline       | Scrape viral reel → generate 5 UGC → post as drafts                                                                                   | reel or TikTok URL            |
| ugc-dance-motion          | Dance/motion transfer                                                                                                                 | image + video                 |
| marketing-brain           | Marketing strategy brain — hooks, visuals, ads                                                                                        | user brief                    |
| reddit-subreddit-intel    | Scrape top posts, analyze virality, generate ideas                                                                                    | subreddit + product           |
| twitter-influencer-search | Find X influencers and amplifiers                                                                                                     | competitor/niche keywords     |
| tiktok-slideshow-carousel | 3-slide TikTok carousel — hook, bridge, product reveal                                                                                | app screenshot + audience     |
| creative-static-ads       | Single-frame static ad images — 6 conversion pillars, 8 archetypes, 8 psychological hooks                                             | product + optional image      |
| ffmpeg                    | All local ffmpeg recipes — trim, audio swap, captions, social formats, scene split, silence cut, frame extraction, analysis artifacts | local video path or mediaId   |
| image-edit                | All image edit paths — img2img, background removal, crop, text overlay, vectorize                                                     | image mediaId or local path   |
| remotion-local-render     | Render editorPipeline blueprint steps locally via @remotion/renderer                                                                  | manifest JSON + editor job id |

**If a skill matches** → `wonda skill get <slug>`, read it, adapt to context, execute each step.

**If no skill matches** → build from scratch (Step 3).

### Step 2.5: Decide whether finishing should be local

Not every media task should go back through Wonda editing. Use this routing rule:

- Use `wonda` for AI generation, AI transcription/alignment, scraping, publishing, hosted transitions, and workflows that need media IDs or remote jobs.
- Use local `ffmpeg` for deterministic transforms on files you already have or can download: trim, crop/scale/pad, concat, replace audio, extract audio/frame, reverse, normalize for delivery, burn captions, split scenes, cut silence, and build analysis artifacts.

When a task starts from a Wonda media ID but the actual edit is deterministic, move it to local files first:

```bash
wonda media download <mediaId> -o ./input.mp4
```

Before any local ffmpeg work:

```bash
which ffmpeg
which ffprobe
ffmpeg -version
ffprobe -v error -show_format -show_streams -of json ./input.mp4
```

Font rule for local caption/text work:

- Prefer an explicit font file path over a family name.
- Never assume a font exists. Check first with `fc-match`, `fc-list`, `/System/Library/Fonts`, `/Library/Fonts`, `~/Library/Fonts`, or `/usr/share/fonts`.
- If the task is mainly local finishing/captions/formatting/splitting/artifact extraction, check the `ffmpeg` skill before inventing commands.
- `wonda edit video` renders locally by default for single-video ops (`trim`, `crop`, `speed`, `volume`, `textOverlay`, `animatedCaptions` with supplied captions, `editAudio`). The server returns a manifest; the CLI runs `@remotion/renderer` against a CloudFront-hosted bundle, uploads the output, and finalizes the editor_job. No flag needed. Pass `--render-server` only to force Lambda. Multi-video ops (`overlay`, `splitScreen`, `merge`, `splitScenes`, `motionDesign`) auto-reject with a 400 — the CLI will tell you to use `--render-server`. See the `remotion-local-render` content skill for the full recipe (including the STT-free TikTok-style caption flow via `wonda alignment extract-timestamps` → `--caption-segments`).

Default local export target unless the user asked otherwise:

```bash
-c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p -movflags +faststart -c:a aac -b:a 192k
```

Always pass `-y` as the first flag so the command auto-overwrites the output. `ffmpeg` prompts interactively when the output path exists and agent shells hang on that prompt until timeout.

### Step 3: Build from scratch (chain endpoints)

When no skill matches, chain individual CLI commands. Each step produces an output that feeds into the next.

**Single asset:**

```bash
wonda generate image --model gpt-image-2 --prompt "..." --aspect-ratio 9:16 --wait -o out.png
# --params '{"quality":"high"}' — auto/low/medium/high (default auto)
# --negative-prompt "..."       — override what to exclude (models like cookie have good defaults)
# --seed <number>               — pin the seed for reproducible results (model-dependent)
wonda generate video --model seedance-2 --prompt "..." --duration 5 --params '{"quality":"high"}' --wait -o out.mp4
wonda generate text --model <model> --prompt "..." --wait
wonda generate music --model suno-music --prompt "upbeat lo-fi" --wait -o music.mp3
```

**Audio (speech, transcription, dialogue):**

```bash
# Text-to-speech
wonda audio speech --model elevenlabs-tts --prompt "Your script here" \
  --params '{"voiceId":"21m00Tcm4TlvDq8ikWAM"}' --wait -o speech.mp3
# elevenlabs-tts always requires a voiceId param
# Common voice: Rachel (female) "21m00Tcm4TlvDq8ikWAM"

# Transcribe audio/video to text
wonda audio transcribe --model elevenlabs-stt --attach $MEDIA --wait

# Multi-speaker dialogue
wonda audio dialogue --model elevenlabs-dialogue --prompt "Speaker A: Hi! Speaker B: Hello!" \
  --wait -o dialogue.mp3
```

**Audio AI operations (direct-inference, NOT editor ops):**

```bash
# Denoise / dereverberate speech
wonda audio enhance --model replicate-resemble-enhance --attach $MEDIA \
  --params '{"denoise":true,"chunkSeconds":10}' --wait -o enhanced.wav

# Split a track into voice and instrumental stems
wonda audio extract-voice --model replicate-demucs --attach $MEDIA \
  --wait -o vocals.wav
```

DO NOT use `wonda edit video --operation enhanceAudio` or `--operation voiceExtractor` — those paths are deprecated. They still work but emit a warning, and they route through the heavier editor_job pipeline for no functional reason.

**Add animated captions to a video:**

The `animatedCaptions` operation handles everything in one step — it extracts audio, transcribes for word-level timing, and renders animated word-by-word captions onto the video.

```bash
# Generate a video with speech audio
VID_JOB=$(wonda generate video --model seedance-2 --prompt "..." --duration 5 --aspect-ratio 9:16 --params '{"quality":"high"}' --wait --quiet)
VID_MEDIA=$(wonda jobs get inference $VID_JOB --jq '.outputs[0].media.mediaId')

# Add animated captions (single step)
wonda edit video --operation animatedCaptions --media $VID_MEDIA \
  --params '{"fontFamily":"TikTok Sans SemiCondensed","position":"bottom-center","sizePercent":80,"strokeWidth":2.5,"fontSizeScale":0.8,"highlightColor":"rgb(252, 61, 61)"}' \
  --wait -o final.mp4
```

The video's original audio is preserved. Do NOT replace the audio with TTS — Sora already generated the speech.

**Transitions (effects pipelines on a single video):**

```bash
wonda transitions presets                            # List built-in presets (JSON)
wonda transitions operations                         # Grouped by category (analysis/effect/...)
wonda transitions operations --json                  # Full per-param metadata
wonda transitions llms                               # Full reference (presets + ops + dependencies)
wonda transitions run --media $VID --preset flash_glow --wait -o out.mp4
# Or build a custom pipeline of steps:
wonda transitions run --media $VID \
  --steps '[{"glow":{"spread":8}},{"scene_flash":{}}]' --wait -o out.mp4
# Or send an agent-generated timeline of clips (inline JSON):
wonda transitions run --media $VID \
  --clips '[{"layer_type":"video","start_frame":0,"end_frame":60}]' --wait -o out.mp4
# …or from a file (handy for long agent timelines):
wonda transitions run --media $VID --clips ./timeline.json --wait -o out.mp4
wonda transitions job <jobId>                        # Poll a transition job
```

Use exactly one of `--preset`, `--steps`, or `--clips`. Requires a full (logged-in) account. **Always read `wonda transitions llms` first when composing a custom pipeline or a clips timeline** — it documents the detect→segment→effect dependencies, which ops need masks, and the full clip-spec shape (layer types, tracks, effects, transforms).

**Preset variables (`variables` block).** Each preset declares the template variables it accepts under `variables` in `wonda transitions presets`. Each entry has `name`, `description`, and `required`. Required variables MUST be supplied or the job is rejected with a 400 — no more silent skipping. Pass them with `--var name=value` (repeatable) or, for the common `prompt` case, the `--prompt` shortcut:

```bash
# flash_glow_prompted requires { prompt }
wonda transitions run --media $VID --preset flash_glow_prompted \
  --prompt "woman in white dress" --wait -o out.mp4

# text_behind_person requires { prompt, text }
wonda transitions run --media $VID --preset text_behind_person \
  --var prompt="the person" --var text="HELLO WORLD" --wait -o out.mp4
```

The `prompt` variable is a **detection text query** (Grounding DINO target describing which subject to mask), not a content-generation prompt. For presets that don't declare a `prompt` variable but still list `sam2`/`clip` in `models`, detection auto-picks the most recurring subject via CLIP — no variable needed.

Building a custom `--steps` pipeline that uses `detect` + `segment`? Add a `detect` step with `method: grounding_dino` and put the subject description in that step's `prompt` param (or use `method: clip` for auto-detect).

**Multi-scene presets (`requiresMultiScene: true`).** Some presets use `scene_split` and expect a video with multiple cuts/scenes. Check `requiresMultiScene` in `wonda transitions presets` — if true, feeding a single continuous shot will produce only one scene and the effect may look underwhelming. Combine clips first or use a video with natural cuts.

**Per-step overrides (`--overrides`).** Tweak individual params of a preset's steps without rewriting the whole pipeline. Shape is **nested**: `{stepName: {paramName: value}}`. Step and param names come from `wonda transitions operations --json`.

```bash
wonda transitions run --media $VID --preset flash_glow \
  --overrides '{"glow":{"spread":12},"zoom":{"end":2.5}}' --wait -o out.mp4
```

**Output URL paths differ by job type:**

- Inference jobs (generate, audio): `.outputs[0].media.url` and `.outputs[0].media.mediaId`
- Editor jobs (edit): `.outputs[0].url` and `.outputs[0].mediaId`

## Model waterfall

### Image

Default: `gpt-image-2`. OpenAI's flagship — strongest prompt adherence, best text-in-image, high-fidelity edits via reference images. Handles 1-4 reference images. Quality tiers: `auto` (default), `low`, `medium`, `high` — pass via `--params '{"quality":"high"}'`. Caps at 1536px output.

For img2img editing specifically (change, add/remove, restyle, bg-remove, crop, text overlay, vectorize), use `wonda skill get image-edit` — it has the full edit-specific decision tree.

Pick something else only when one of these applies:

- User explicitly requests another model
- **More than 4 reference images** → `nano-banana-2` (gpt-image-2 caps at 4 refs; nano-banana-2 accepts up to 14). For 1-4 refs, stay on `gpt-image-2`.
- Need vector output → `runware-vectorize`
- Need background removal → `birefnet-bg-removal`
- Cheapest possible / fastest drafts → `z-image`
- Need >1536px / true 4K output → `nano-banana-pro` (1K/2K/4K) or `nano-banana-2` (1K/2K/4K). gpt-image-2 caps at 1536px.
- gpt-image-2 unavailable / OpenAI down → `nano-banana-2` or `seedream-4-5` or `grok-imagine-pro`
- Spicy content → `cookie` (SDXL-based, tag-based or natural language prompts) — **ONLY select when the user explicitly asks for spicy content. Never auto-select.**

**Cookie model (`cookie`):** SDXL with DMD acceleration and hires fix. **Restricted: only use when the user explicitly requests spicy content.** Accepts both danbooru-style tags (`1cat, portrait, soft lighting`) and natural language. Supports `--negative-prompt` (has sensible defaults; override only when needed) and `--seed` for reproducibility.

```bash
wonda generate image --model cookie --prompt "1cat, portrait, soft lighting" --wait -o out.png
wonda generate image --model cookie --prompt "a woman in a garden, golden hour" \
  --negative-prompt "ugly, blurry, watermark" --seed 42 --wait -o out.png
```

### Video

Default: `seedance-2` (duration 5/10/15s, default 5s, quality: high). Escalation:

- Quality complaint or different style → `sora2` or `sora2pro`
- Max single-clip duration is **15s** for Seedance 2, **20s** for Sora → for longer content, stitch multiple clips via merge
- Veo (`veo3_1`, `veo3_1-fast`) is available but NOT in the default waterfall. Only pick Veo when the user explicitly asks for Veo by name.

**Image-to-video routing (MANDATORY when attaching a reference image):**

- Person/face visible in the **reference image** → MUST use `kling_3_pro` (preserves identity better for faces)
- No person in reference image → use `seedance-2`
- **Text-to-video (no reference image):** Seedance 2 generates people fine. This rule ONLY applies when you `--attach` an image.

**Kling model family:**

- `kling_3_pro` — Text-to-video and image-to-video, supports start/end images, custom elements (@Element1, @Element2), 3-15s duration, 16:9/9:16/1:1
- `kling_2_6_pro` — General purpose, 5-10s, 16:9/9:16/1:1, text-to-video and image-to-video
- `kling_2_6_motion_control` — Motion transfer: requires both a reference image AND a reference video, recreates the video's motion with the image's appearance
- `kling2_5-pro` — Budget Kling option, 5-10s, supports first/last frame images

**Kling prompt rules (important):** Kling's prompt field caps at **2,500 characters** and Kling responds poorly to Sora-style structured briefs (`SCENE:` / `SUBJECT:` / `MOTION:` / `BANNED LOOK:` section headers). In that format Kling latches onto atmosphere nouns and silently drops the central subject (verified empirically: the same 2,842-char Sora-style prompt that rendered correctly on Sora 2 Pro and Seedance 2 produced no phone at all on Kling — even when trimmed to 2,250 chars). When escalating Seedance → Kling, or targeting Kling directly, **rewrite the prompt as short natural-language prose (~1,000–1,500 chars)** and **lead with the hero subject in the opening sentence** rather than burying it inside a `SUBJECT:` block. Do NOT pass a Sora-formatted prompt through to Kling unchanged.

**Other video models:**

- `grok-imagine-video` — xAI video generation, 5-15s, supports 7 aspect ratios including 4:3 and 3:2
- `topaz-video-upscale` — Upscale video resolution (1-4x factor, supports fps conversion)
- `sync-lipsync-v2-pro` — Legacy lipsync for user-supplied video + audio pairs. Inferior to native-audio generation and almost never the right choice for new content. See the "Lip sync" section for rules.

Seedance family (DEFAULT video model, watermarks automatically removed):

- `seedance-2` — Base Seedance 2.0 (T2V/I2V, 5-15s, high=standard/basic=fast)
- `seedance-2-omni` — Multi-reference generation (images, audio refs)
- `seedance-2-video-edit` — Edit existing video via text prompt

**Video durations:** Accepted `--duration` values vary by model. Check with `wonda capabilities` or `wonda models info <slug>`.

### Audio

- Music: `suno-music` (set `--params '{"instrumental":true}'` for no vocals)
- Text-to-speech: `elevenlabs-tts` — only for explicit narrator/voice-over asks over silent footage. Do NOT use to "make a UGC character talk" — Sora / Sora 2 Pro / Veo 3.1 / Kling 3 / Seedance 2 generate native synced speech in any language, which looks and sounds far better. Always set voiceId in params. Default female voice: `--params '{"voiceId":"21m00Tcm4TlvDq8ikWAM"}'` (Rachel).
- Transcription: `elevenlabs-stt`
- Multi-speaker dialogue: `elevenlabs-dialogue`
- Enhance audio (clean up noisy speech): `replicate-resemble-enhance` via `wonda audio enhance` — denoise + dereverberate. Use when a voice recording sounds muffled, echoey, or has background noise. NOT a general "sounds better" button; if the source is already clean this can soften it.
- Extract voice (isolate vocals / split stems): `replicate-demucs` via `wonda audio extract-voice` — splits into voice and instrumental tracks. Use to pull a speaker or singer off a track, or to isolate the music behind a vocal.

**Native synced speech (preferred over TTS + lipsync):** Sora, Sora 2 Pro, Veo 3.1, Kling 3, and Seedance 2 all generate dialogue in any language directly inside the video, with mouth movements baked in. Put the line (and language) in the video model's `--prompt`. Never chain `elevenlabs-tts` → `sync-lipsync-v2-pro` to fake speech over a silent generation.

## Prompt writing rules

Follow this waterfall top-to-bottom. Use the FIRST matching rule and stop.

1. **PASSTHROUGH** — If the user says "use my exact prompt" / "verbatim" / "no enhancements" → copy their words exactly. Zero modifications.

2. **IMAGE-TO-VIDEO** — When a source image feeds into a video model, describe MOTION ONLY. The model can see the image. Do NOT describe the image content.
   - Good: `"gentle breathing motion, camera slowly pushes in, atmospheric lighting shifts"`
   - Bad: `"Two cats on a lavender background breathing softly"` (describes the image)

3. **EMPTY PROMPT (from scratch)** — Use the user's exact request as the prompt. Do NOT add style descriptors, lighting, composition, or mood.
   - User says "create an image of a cat with sunglasses" → prompt: `"create an image of a cat with sunglasses"`
   - Do NOT enhance to `"A playful orange tabby wearing oversized reflective sunglasses, studio lighting, shallow depth of field"`

4. **NON-EMPTY PROMPT (adapting a template)** — Keep the structure and style, only swap content to match the user's request. Keep prompts literal and constraint-heavy.

## Aspect ratio rules

Three cases, no exceptions:

1. User specifies a ratio → use it: `--aspect-ratio 16:9`
2. User doesn't mention ratio → explicitly set `--aspect-ratio 9:16` for social content (UGC, TikTok, Reels, Stories). Portrait is the default for any social/marketing video.
3. Editing existing media → use `--aspect-ratio auto` to preserve source dimensions

**UGC and social content is ALWAYS portrait (9:16).** If someone asks for a TikTok, Reel, Story, or UGC video, always use `--aspect-ratio 9:16`. Landscape is only for YouTube, presentations, or when explicitly requested.

**Square (1:1)** is supported by all Kling models and some image models — use for Instagram feed posts when requested.

## Common chaining patterns

These patterns show how to compose multi-step pipelines by chaining CLI commands. Each step's output feeds into the next.

> **No need to download and re-upload between steps.** Every generation and edit
> produces a media ID in its output. Pass that ID directly to the next command
> via `--media` or `--audio-media`. Use `--jq '.outputs[0].media.mediaId'`
> for inference jobs and `--jq '.outputs[0].mediaId'` for editor jobs.
> Only use `-o <file>` on the FINAL step to download the finished output.

### Animate an image to video

```bash
MEDIA=$(wonda media upload ./product.jpg --quiet)
# No person in image → Seedance 2
wonda generate video --model seedance-2 --prompt "camera slowly pushes in, product rotates" \
  --attach $MEDIA --duration 5 --params '{"quality":"high"}' --wait -o animated.mp4
# Person in image → Kling (ONLY when attaching a reference image with a person)
wonda generate video --model kling_3_pro --prompt "the person turns and smiles" \
  --attach $MEDIA --duration 5 --wait -o person.mp4
```

### Replace audio on a video (TTS voiceover or music)

```bash
# Generate TTS
TTS_JOB=$(wonda audio speech --model elevenlabs-tts --prompt "The script" \
  --params '{"voiceId":"21m00Tcm4TlvDq8ikWAM"}' --wait --quiet)
TTS_MEDIA=$(wonda jobs get inference $TTS_JOB --jq '.outputs[0].media.mediaId')
# Mix onto video (mute original, full voiceover)
wonda edit video --operation editAudio --media $VID_MEDIA --audio-media $TTS_MEDIA \
  --params '{"videoVolume":0,"audioVolume":100}' --wait -o with-voice.mp4
```

Only use this when you need to REPLACE the video's audio. Sora, Sora 2 Pro, Veo 3.1, Kling 3, and Seedance 2 all generate native synced speech in any language — don't replace it with TTS unless the user explicitly asks for a different voiceover. Never reach for this step to "add speech" to a UGC/talking-head clip; put the dialogue in the video model's prompt instead.

### Add static text overlay

Static overlays (meme text, "chat did i cook", etc.) use smaller font sizes than captions. They're ambient, not meant to dominate the frame.

```bash
wonda edit video --operation textOverlay --media $VID_MEDIA \
  --prompt-text "chat, did i cook" \
  --params '{"fontFamily":"TikTok Sans SemiCondensed","position":"top-center","sizePercent":66,"fontSizeScale":0.5,"strokeWidth":4.5,"paddingTop":10}' \
  --wait -o with-text.mp4
```

**Featured textOverlay + animatedCaptions presets.** `wonda edit {video,image,audio}` accepts `--preset <name>` (scoped to `--operation`). `--params` fields override preset values on key collisions.

`textOverlay` (static, top-centered):

- `TikTok White Highlight` — black text on a slightly rounded white box.
- `TikTok Black Highlight` — white text on a slightly rounded black box.
- `TikTok Red Highlight` — white text on a slightly rounded red (`#E14135`) box.

`animatedCaptions` (STT-driven, bottom-centered):

- `TikTok White Captions` — black text, white highlight on the active word.
- `TikTok Black Captions` — white text, black highlight on the active word.
- `TikTok Red Captions` — white text, red (`#E14135`) highlight on the active word.

```bash
wonda edit video --operation textOverlay \
  --preset "TikTok Red Highlight" --media <id> \
  --params '{"text":"YOUR HEADLINE"}' --wait -o ./out.mp4
```

Image `textOverlay` requires `--render-server`; video renders locally by default.

**Font sizing guide:**

- Static overlays: `sizePercent: 66`, `fontSizeScale: 0.5`, `strokeWidth: 4.5`
- Animated captions: `sizePercent: 80`, `fontSizeScale: 0.8`, `strokeWidth: 2.5`, `highlightColor: rgb(252, 61, 61)`
- Font: `TikTok Sans SemiCondensed` for both

### Add animated captions (word-by-word with timing)

The `animatedCaptions` operation extracts audio, transcribes, and renders animated word-by-word captions — all in one step.

```bash
wonda edit video --operation animatedCaptions --media $VIDEO_MEDIA \
  --params '{"fontFamily":"TikTok Sans SemiCondensed","position":"bottom-center","sizePercent":80,"strokeWidth":2.5,"fontSizeScale":0.8,"highlightColor":"rgb(252, 61, 61)"}' \
  --wait -o with-captions.mp4
```

For quick static captions (no timing, just text on screen), use `textOverlay` with `--prompt-text`:

```bash
wonda edit video --operation textOverlay --media $VIDEO_MEDIA \
  --prompt-text "Summer Sale - 50% Off" \
  --params '{"fontFamily":"TikTok Sans SemiCondensed","position":"bottom-center","sizePercent":80}' \
  --wait -o captioned.mp4
```

### Add background music

```bash
MUSIC_JOB=$(wonda generate music --model suno-music \
  --prompt "upbeat lo-fi hip hop, warm vinyl crackle" --wait --quiet)
MUSIC_MEDIA=$(wonda jobs get inference $MUSIC_JOB --jq '.outputs[0].media.mediaId')
wonda edit video --operation editAudio --media $VID_MEDIA --audio-media $MUSIC_MEDIA \
  --params '{"videoVolume":100,"audioVolume":30}' --wait -o with-music.mp4
```

### Editor output chaining

When chaining multiple editor operations (e.g., editAudio → animatedCaptions → textOverlay), extract the media ID from each editor job output and pass it to the next step. Note the jq path differs from inference jobs:

```bash
# Inference jobs: .outputs[0].media.mediaId
# Editor jobs:    .outputs[0].mediaId

EDIT_JOB=$(wonda edit video --operation editAudio --media $VID --audio-media $AUDIO \
  --params '{"videoVolume":0,"audioVolume":100}' --wait --quiet)
STEP1_MEDIA=$(wonda jobs get editor $EDIT_JOB --jq '.outputs[0].mediaId')

CAP_JOB=$(wonda edit video --operation animatedCaptions --media $STEP1_MEDIA \
  --params '{"fontFamily":"TikTok Sans SemiCondensed","position":"bottom-center","sizePercent":80,"strokeWidth":2.5,"fontSizeScale":0.8,"highlightColor":"rgb(252, 61, 61)"}' --wait --quiet)
STEP2_MEDIA=$(wonda jobs get editor $CAP_JOB --jq '.outputs[0].mediaId')

wonda edit video --operation textOverlay --media $STEP2_MEDIA \
  --prompt-text "Hook text" --params '{"position":"top-center","fontFamily":"TikTok Sans SemiCondensed","sizePercent":66,"fontSizeScale":0.5,"strokeWidth":4.5}' --wait -o final.mp4
```

### Merge multiple clips

```bash
wonda edit video --operation merge --media $CLIP1,$CLIP2,$CLIP3 --wait -o merged.mp4
```

Media order = playback order. Up to 5 clips.

### Split scenes / keep a specific scene

Two modes — pick by intent:

```bash
# Keep a specific scene (split mode) — splits into scenes, auto-selects one
wonda edit video --operation splitScenes --media $VID_MEDIA \
  --params '{"mode":"split","threshold":0.5,"minClipDuration":2,"outputSelection":"last"}' \
  --wait -o last-scene.mp4
# outputSelection: "first", "last", or 1-indexed number (e.g. 2 for second scene)

# Remove a scene (omit mode) — removes one scene, merges the rest
wonda edit video --operation splitScenes --media $VID_MEDIA \
  --params '{"mode":"omit","threshold":0.5,"minClipDuration":2,"outputSelection":"first"}' \
  --wait -o without-first.mp4
# outputSelection: which scene to REMOVE
```

Use omit mode for "remove frozen first frame" (common with Sora videos). Use split mode for "keep just scene X".

### Image editing

Any image edit — img2img, background removal, crop, text overlay, vectorize — has its own skill with the full decision tree, aspect-ratio rules, and model waterfall for edits:

```bash
wonda skill get image-edit
```

One gotcha worth keeping here: image and video background removal use **different** models (`birefnet-bg-removal` vs `bria-video-background-removal`). Never swap them.

### Lip sync (last-resort fallback — prefer native-audio video models)

Sora, Sora 2 Pro, Veo 3.1, Kling 3, and Seedance 2 all generate speech in any language with correctly synced mouth movements as part of the video itself. That path produces dramatically better results than `sync-lipsync-v2-pro`: better lip physics, better lighting, better costs, and no second inference round-trip. For any talking UGC, ad, or spokesperson video, put the dialogue directly in the video model's prompt — do not chain TTS + lipsync.

Only reach for `sync-lipsync-v2-pro` when the user EXPLICITLY supplies both a pre-existing video and a pre-existing audio clip and asks you to align the mouth to that audio. If a user asks for lipsync as the default method of making a character speak, push back: the native-audio video models are the better tool and work in any language.

```bash
wonda generate video --model sync-lipsync-v2-pro --attach $VIDEO_MEDIA,$AUDIO_MEDIA --wait -o synced.mp4
```

### Video upscale

```bash
wonda generate video --model topaz-video-upscale --attach $VIDEO_MEDIA \
  --params '{"upscaleFactor":2}' --wait -o upscaled.mp4
```

## Editor operations reference

| Operation          | Inputs                      | Key Params                                                                    |
| ------------------ | --------------------------- | ----------------------------------------------------------------------------- |
| `animatedCaptions` | video_0                     | fontFamily, position, sizePercent, fontSizeScale, strokeWidth, highlightColor |
| `textOverlay`      | video_0 + prompt            | fontFamily, position, sizePercent, fontSizeScale, strokeWidth                 |
| `editAudio`        | video_0 + audio_0           | videoVolume (0-100), audioVolume (0-100)                                      |
| `merge`            | video_0..video_4            | Handle order = playback order                                                 |
| `overlay`          | video_0 (bg) + video_1 (fg) | position, resizePercent                                                       |
| `splitScreen`      | video_0 + video_1           | targetAspectRatio (16:9 or 9:16)                                              |
| `trim`             | video_0                     | trimStartMs, trimEndMs (milliseconds)                                         |
| `splitScenes`      | video_0                     | mode (split/omit), threshold, outputSelection                                 |
| `speed`            | video_0                     | speed (multiplier: 2 = 2x faster)                                             |
| `extractAudio`     | video_0                     | Extracts audio track                                                          |
| `reverseVideo`     | video_0                     | Plays backwards                                                               |
| `skipSilence`      | video_0                     | maxSilenceDuration (default 0.03)                                             |
| `imageCrop`        | video_0                     | aspectRatio                                                                   |
| `textOverlay`      | video_0 (image)             | Same as video textOverlay — works on images, outputs image (png/jpg)          |

Valid textOverlay fonts: Inter, Montserrat, Bebas Neue, Oswald, TikTok Sans, TikTok Sans Condensed, TikTok Sans SemiCondensed, TikTok Sans SemiExpanded, TikTok Sans Expanded, TikTok Sans ExtraExpanded, Nohemi, Poppins, Raleway, Anton, Comic Cat, Gavency
Valid positions: top-left, top-center, top-right, center-left, center, center-right, bottom-left, bottom-center, bottom-right

## Marketing & distribution

```bash
# Connected social accounts
wonda accounts instagram
wonda accounts tiktok

# Analytics
wonda analytics instagram
wonda analytics tiktok
wonda analytics meta-ads

# Scrape competitors
wonda scrape social --handle @nike --platform instagram --wait
wonda scrape social-status <taskId>                   # Get results of a social scrape
wonda scrape ads --query "sneakers" --country US --wait
wonda scrape ads --query "sneakers" --country US --search-type keyword \
  --active-status active --sort-by impressions_desc --period last30d \
  --media-type video --max-results 50 --wait
wonda scrape ads-status <taskId>                      # Get results of an ads search

# Download a single reel or TikTok video
SCRAPE=$(wonda scrape video --url "https://www.instagram.com/reel/ABC123/" --wait --quiet)
# → returns scrape result with mediaId in the media array

# Publish
wonda publish instagram --media <id> --account <accountId> --caption "New drop"
wonda publish instagram --media <id> --account <accountId> --caption "..." --alt-text "..." --product IMAGE --share-to-feed
wonda publish instagram-carousel --media <id1>,<id2>,<id3> --account <accountId> --caption "..."
wonda publish tiktok --media <id> --account <accountId> --caption "New drop"
wonda publish tiktok --media <id> --account <accountId> --caption "..." --privacy-level PUBLIC_TO_EVERYONE --aigc
wonda publish tiktok-carousel --media <id1>,<id2> --account <accountId> --caption "..." --cover-index 0

# History
wonda publish history instagram --limit 10
wonda publish history tiktok --limit 10

# Browse media library
wonda media list --kind image --limit 20
wonda media info <mediaId>
```

### X/Twitter

Supports reads, writes, and social graph.

```bash
# Auth setup (run `wonda x auth --help` for details)
wonda x auth set --auth-token <token> --ct0 <ct0>
wonda x auth set --account burner --auth-token <...> --ct0 <...>  # multi-account
wonda x auth check

# Read
wonda x search "sneakers" -n 20                     # Search tweets
wonda x user @nike                                   # User profile
wonda x user-tweets @nike -n 20                      # User's recent tweets
wonda x read <tweet-id-or-url>                       # Single tweet
wonda x replies <tweet-id-or-url>                    # Replies to a tweet
wonda x thread <tweet-id-or-url>                     # Full thread (author's self-replies)
wonda x home                                         # Home timeline (--following for Following tab)
wonda x bookmarks                                    # Your bookmarks
wonda x likes                                        # Your liked tweets
wonda x following @handle                            # Who a user follows
wonda x followers @handle                            # A user's followers
wonda x lists @handle                                # User's lists (--member-of for memberships)
wonda x list-timeline <list-id-or-url>               # Tweets from a list
wonda x news --tab trending                          # Trending topics (tabs: for_you, trending, news, sports, entertainment)

# Write (uses internal API — use on secondary accounts)
wonda x tweet "Hello world"                          # Post a tweet
wonda x tweet "Hello world" --browser                # Full stealth via real browser (Patchright)
wonda x tweet "Hello world" --attach ~/clip.mp4      # Attach image/gif/video (up to 4)
wonda x reply <tweet-id-or-url> "Great point"        # Reply
wonda x like <tweet-id-or-url>                       # Like
wonda x unlike <tweet-id-or-url>                     # Unlike
wonda x retweet <tweet-id-or-url>                    # Retweet
wonda x unretweet <tweet-id-or-url>                  # Unretweet
wonda x follow @handle                               # Follow
wonda x unfollow @handle                             # Unfollow

# Maintenance
wonda x refresh-ids                                  # Refresh cached GraphQL query IDs from X's JS bundles
```

All paginated commands support: `-n <count>`, `--cursor`, `--all`, `--max-pages`, `--delay <ms>`.

**Tweet modes:** The `tweet` command has two modes:

- **Default (API):** X's internal GraphQL (`CreateTweet` for ≤280 chars, `CreateNoteTweet` for long-form Premium). Fast (<1s), supports `--attach` for media. Occasionally fails with error 226 when X rotates query IDs or feature flags — when that happens, recapture via `twitter-tone-research/_artifacts/scripts/capture-ct-bw.mjs` and bump the three knobs in `xclient/`.
- **`--browser` (Patchright):** Launches a real undetected Chrome browser, opens x.com compose, types with human-style jitter, clicks Post. Supports `--attach` (image/gif/video, up to 4) — files are driven through the hidden compose input via Playwright's `setInputFiles`, no native picker dialog opens; the script waits for X's upload pipeline to finalize (up to 5 min for video) before submitting. Zero fingerprinting risk. Slower (~10s text, ~30-90s with video) but fully drift-proof — no queryIds, feature flags, or request shape to maintain. Requires: `npm i patchright && npx patchright install chromium`.

### LinkedIn

Supports search, profiles, companies, messaging, and engagement.

```bash
# Auth setup (run `wonda linkedin auth --help` for details)
wonda linkedin auth set --li-at-value <v> --jsessionid-value <v>
wonda linkedin auth set --account brand-A --li-at-value <...> --jsessionid-value <...>  # multi-account
wonda linkedin auth check

# Read
wonda linkedin me                                    # Your identity
wonda linkedin search "data engineer" --type PEOPLE  # Search (types: PEOPLE, COMPANIES, ALL)
wonda linkedin profile johndoe                       # View profile (vanity name or URL)
wonda linkedin company google                        # View company page
wonda linkedin conversations                         # List message threads
wonda linkedin messages <conversation-urn>           # Read messages in a thread
wonda linkedin notifications -n 20                   # Recent notifications
wonda linkedin connections                           # Your connections
wonda linkedin reactions <activity-id>               # Reactions with reactor profiles + type

# Write
wonda linkedin connect <vanity-name> --message "Hey!" # Send connection request with note
wonda linkedin connect <vanity-name> -m "Hey!" --browser  # Full stealth via real browser (Patchright)
wonda linkedin like <activity-urn>                   # Like a post
wonda linkedin unlike <activity-urn>                 # Remove a like
wonda linkedin send-message <conversation-urn> "Hi!" # Send a message
wonda linkedin post "Excited to announce..."         # Create a post
wonda linkedin delete-post <activity-id>             # Delete a post
```

Paginated commands support: `-n <count>`, `--start`, `--all`, `--max-pages`, `--delay <ms>`.

**Connection request modes:** The `connect` command has two modes:

- **Default (API):** Voyager REST API with fingerprint mitigations (profile visit → drawer warm-up → connect). Fast (~3s), supports notes via `customMessage`.
- **`--browser` (Patchright):** Launches a real undetected Chrome browser, navigates to the profile, and clicks through the UI. Zero fingerprinting risk. Slower (~10s) but fully safe. Use this as a fallback if you want full protection. Requires: `npm i patchright && npx patchright install chromium`.

### Reddit

Auth is optional — many reads work unauthenticated. Supports search, feeds, users, posts, trending, and chat/DMs.

```bash
# Auth setup (run `wonda reddit auth --help` for details)
wonda reddit auth set --session-value <jwt>
wonda reddit auth set --account burner-1 --session-value <jwt>  # multi-account
wonda reddit auth check

# Read (works without auth)
wonda reddit search "AI video" --sort top --time week   # Search posts (sort: relevance, hot, top, new, comments)
wonda reddit subreddit marketing                        # Subreddit info
wonda reddit feed marketing --sort hot                  # Subreddit posts (sort: hot, new, top, rising)
wonda reddit user spez                                  # User profile
wonda reddit user-posts spez --sort top                 # User's posts
wonda reddit user-comments spez                         # User's comments
wonda reddit post <id-or-url> -n 50                     # Post with comments
wonda reddit trending --sort hot                        # Popular/trending posts

# Read (requires auth)
wonda reddit home --sort best                           # Your home feed

# Write (requires auth)
wonda reddit submit marketing --title "Great tool" --text "Check this out..."  # Self post
wonda reddit submit marketing --title "Great tool" --url "https://..."         # Link post
wonda reddit comment <parent-fullname> --text "Nice post!"                     # Reply
wonda reddit vote <fullname> --up                       # Upvote (--down, --unvote)
wonda reddit subscribe marketing                        # Subscribe (--unsub to unsubscribe)
wonda reddit save <fullname>                            # Save a post or comment
wonda reddit unsave <fullname>                          # Unsave
wonda reddit delete <fullname>                          # Delete your post or comment
```

Paginated commands support: `-n <count>`, `--after <cursor>`, `--all`, `--max-pages`, `--delay <ms>`.

### Reddit chat / DMs

Direct messaging via the Matrix protocol. Requires a separate chat token.

```bash
# Auth setup (run `wonda reddit chat auth-set --help` for details)
wonda reddit chat auth-set

# Read
wonda reddit chat inbox                                  # List DM conversations with latest messages
wonda reddit chat messages <room-id> -n 50               # Fetch messages from a room
wonda reddit chat all-rooms                              # List ALL joined rooms (not limited to sync window)

# Write
wonda reddit chat send <room-id> --text "Hey!"           # Send a DM (mimics browser typing behavior)

# Management
wonda reddit chat accept-all                             # Accept all pending chat requests
wonda reddit chat refresh                                # Force-refresh the Matrix chat token
```

**Important**: The chat token expires every ~24h. The CLI auto-refreshes on use, but if it expires fully, re-run `auth-set`. Rate limit DM sends to 15-20/day with varied text to avoid detection. The `send` command includes a typing delay (1-5s) to mimic human behavior.

## Workflow & discovery

### Video analysis

Analyze a video to extract a composite frame grid (visual) and audio transcript (text). Useful for understanding video content before creating variations. Requires a **full account** (not anonymous) and costs credits based on video duration (ElevenLabs STT pricing).

If the video was just uploaded and is still normalizing, the CLI auto-retries until the media is ready.

```bash
# Analyze a video — returns composite grid image + transcript
ANALYSIS_JOB=$(wonda analyze video --media $VIDEO_MEDIA --wait --quiet)

# The job output contains:
# - compositeGrid: image showing 24 evenly-spaced frames
# - transcript: full text of any speech
# - wordTimestamps: word-level timing [{word, start, end}]
# - videoMetadata: {width, height, durationMs, fps, aspectRatio}

# Download the composite grid for visual inspection
wonda analyze video --media $VIDEO_MEDIA --wait -o /tmp/grid.jpg

# Get just the transcript
wonda analyze video --media $VIDEO_MEDIA --wait --jq '.outputs[] | select(.outputKey=="transcript") | .outputValue'
```

**Error handling**: 402 = insufficient credits, 409 = media still processing (CLI auto-retries).

### Chat (AI assistant)

Interactive chat sessions for content creation — the AI handles generation, editing, and iteration.

```bash
wonda chat create --title "Product launch"            # New session
wonda chat list                                       # List sessions (--limit, --offset)
wonda chat messages <chatId>                          # Get messages
wonda chat send <chatId> --message "Create a UGC reaction video"
wonda chat send <chatId> --message "Edit it" --media <id>
wonda chat send <chatId> --message "..." --aspect-ratio 9:16 --quality-tier max
wonda chat send <chatId> --message "..." --style <styleId>
wonda chat send <chatId> --message "..." --passthrough-prompt  # Use exact prompt, no AI enhancement
```

### Jobs & runs

```bash
wonda jobs get inference <id>                         # Inference job status
wonda jobs get editor <id>                            # Editor job status
wonda jobs get publish <id>                           # Publish job status
wonda jobs wait inference <id> --timeout 20m          # Wait for completion
wonda run get <runId>                                 # Run status
wonda run wait <runId> --timeout 30m                  # Wait for run completion
```

### Discovery

```bash
wonda models list                                     # All available models
wonda models info <slug>                              # Model details and params
wonda operations list                                 # All editor operations
wonda operations info <operation>                     # Operation details
wonda capabilities                                    # Full platform capabilities
wonda pricing list                                    # Pricing for all models
wonda pricing estimate --model seedance-2 --prompt "..." # Cost estimate
wonda style list                                      # Available visual styles
wonda topup                                            # Top up credits (opens Stripe checkout)
```

### Editing audio & images

```bash
# Edit audio
wonda edit audio --operation <op> --media <id> --wait -o out.mp3
```

For any image edit (crop, text overlay, img2img, background removal, vectorize) pull the dedicated skill: `wonda skill get image-edit`.

### Alignment (timestamp extraction)

```bash
wonda alignment extract-timestamps --model <model> --attach <mediaId> --wait
```

## Quality tiers

| Tier     | Image Model                                    | Resolution                              | Video Model              | When                                                                                                                                               |
| -------- | ---------------------------------------------- | --------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Standard | `gpt-image-2` (auto) — alt: `nano-banana-2` 1K | 1024×1024 / 1024×1536 (gpt) / 1K (nano) | `seedance-2` (high, 5s)  | Default. gpt-image-2 for strongest prompt adherence + text-in-image; nano-banana-2 for faster Gemini iteration with multi-reference support.       |
| High     | `gpt-image-2` (high) — alt: `nano-banana-2` 2K | 1024×1024 / 1024×1536 (gpt) / 2K (nano) | `seedance-2` (high, 15s) | Crisp output. Use `--params '{"quality":"high"}'` on gpt-image-2 or bump `--params '{"resolution":"2K"}'` on nano-banana-2. Also offer `sora2pro`. |
| Max      | `nano-banana-pro` 4K — alt: `nano-banana-2` 4K | 4K                                      | `seedance-2` (high, 15s) | True 4K (gpt-image-2 caps at 1536px). Use `--params '{"resolution":"4K"}'`. Also offer `sora2pro` (1080p) for video.                               |

## Troubleshooting

| Symptom                          | Likely Cause                                  | Fix                                                    |
| -------------------------------- | --------------------------------------------- | ------------------------------------------------------ |
| Sora rejected image              | Person in image                               | Switch to `kling_3_pro`                                |
| Video adds objects not in source | Motion prompt describes elements not in image | Simplify to camera movement and atmosphere only        |
| Text unreadable in video         | AI tried to render text in generation         | Remove text from video prompt, use textOverlay instead |
| Hands look wrong                 | Complex hand actions in prompt                | Simplify to passive positions or frame to exclude      |
| Style inconsistent across series | No shared anchor                              | Use same reference image via `--attach`                |
| Changes to step A not in step B  | Stale render                                  | Re-run all downstream steps                            |

## Timing expectations

- Image: 30s - 2min
- Video (Sora): 2 - 5min
- Video (Sora Pro): 5 - 10min
- Video (Veo 3.1): 1 - 3min
- Video (Kling): 3 - 8min
- Video (Grok): 2 - 5min
- Music (Suno): 1 - 3min
- TTS: 10 - 30s
- Editor operations: 30s - 2min
- Lip sync: 1 - 3min
- Video upscale: 2 - 5min

## Error recovery

- **Unknown model**: `wonda models list`
- **No API key**: `wonda auth login` or set `WONDA_API_KEY` env var
- **Job failed**: `wonda jobs get inference <id>` for error details
- **Bad params**: `wonda models info <slug>` for valid params
- **Timeout**: `wonda jobs wait inference <id> --timeout 20m`
- **Insufficient credits (402)**: `wonda topup` to add credits
