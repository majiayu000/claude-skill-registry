---
name: tiktok-psych-video
description: Produce a narrated, illustrated TikTok psychology explainer video for Clarido — from concept ideation through rendered mp4. Use when creating new TikTok content.
allowed-tools: Bash(pipenv *), Bash(cd videos *), Bash(npx remotion *), Bash(npm *), Bash(mkdir *), Bash(ls *), Bash(cp *), Bash(ffmpeg *), mcp__google-workspace__send_gmail_message
---

# TikTok Psychology Explainer Video

End-to-end workflow for producing a narrated, illustrated TikTok video that explains a psychology concept. Invoked by the user with `/tiktok-psych-video`.

The full method with all implementation details is documented in `docs/tiktok-psych-video-method.md`. **Read that file before starting** — it contains exact API calls, voice settings, style prompts, image sizes, Remotion component specs, and lessons learned.

## Workflow with Approval Gates

### Phase 1: Ideation (→ user approves concept)

The user may invoke this skill in two ways:
- **With a content gap target:** User passes a screenshot of TikTok's Creator Search Insights "Content gap" tab, or types specific keywords/topics they want to target. This is the preferred approach — it ensures every video fills validated demand.
- **Without a target:** Claude picks concepts based on keyword map and dedup check.

1. **Dedup Check** — Read ALL `content/tiktok/*/brief.md` files. Don't duplicate concepts, angles, or stories.
2. **Read keyword map** — Read `docs/tiktok-keyword-map.md` for validated search queries, content gaps, and the psych concept → search query mapping table.
3. **Ideation** — If the user provided a content gap or target keyword:
   - Identify which gap(s) Clarido can credibly fill
   - Pick the psych concept that best explains *why* that topic matters (e.g., "daily tracker journal" → Cognitive Offloading, "share your daily thoughts" → Expressive Writing)
   - The hook and script must use the exact search phrase people are typing

   If no target provided: Pick 2-3 psychology concepts with compelling origin stories that connect to Clarido's value prop, prioritizing concepts that map to high-demand search queries from the keyword map.
4. **Present concepts** to the user and wait for approval before proceeding.

### Phase 2: Script (→ user approves script)

4. **Write script** — Read `docs/writing-style-reference.md` first. **Target 30-45 seconds** (75-110 words at 1.25x speed; ~2.5 words/sec). Every sentence must earn its spot. Cut ruthlessly. Structure is **curiosity hook → factoid → personal → landing line**:
   - **Curiosity hook (0-3s)**: One sentence bridging something unexpected to a relatable problem. Pattern: "[Unexpected subject] [accidentally/proved] why [relatable problem]." E.g., "A waitress accidentally explained why your brain won't shut up at night." This creates a curiosity gap before the story starts.
   - **Factoid/story (3-15s)**: The actual study, told as compressed narrative. Concrete, visual, specific.
   - **Bridge to viewer (15-25s)**: Make it personal. "That's why you lie awake at 3am."
   - **Landing line (25-30s)**: Gut-punch reframe, NO CTA. Video ends on the punch so TikTok auto-loops seamlessly.

   **Tone is Style B**: dry, restrained, trust the viewer to feel the weight. Don't over-explain the emotion. Say search keywords ("overthinking," "brain dump," "journaling," "mental clarity") out loud where natural. Content territory includes psych studies, cognitive biases, and brain quirks — not limited to overthinking/brain dump. See the reference script in the method doc for the exact target format.
5. **Generate caption & hashtags** — 3-5 niche hashtags only. Never use #fyp, #viral, #science, #brainhacks. Use: #overthinking, #[concept], #mentalclarity, #braindump, #journaling, #anxietyrelief.
6. **Create content folder** (`content/tiktok/YYYY-MM-DD_HHMM_slug/`) and save `brief.md`.
7. **Present the full brief** to the user and wait for approval before proceeding.

### Phase 3: Asset Generation (automated)

After script approval, run these scripts in sequence:

8. **Voiceover**: `pipenv run python3 scripts/tiktok/voiceover.py <content-folder>`
   - Reads script from brief.md, calls ElevenLabs, speeds up 1.25x, saves to assets/
9. **Transcribe**: `pipenv run python3 scripts/tiktok/transcribe.py <content-folder>`
   - Calls Deepgram Nova-3, saves transcript.json, prints sentence-level and word-level timestamps
10. **Plan slides** — Use the transcript timestamps to plan **~10 slides at ~3s each** (for 30s video) or **~15 slides at ~3s each** (for 45s video). Every slide gets a unique illustration. No CTA slide at the end — final slide should be a simple closing image that loops cleanly back to slide 1. Add slide plan to brief.md.
11. **Write illustrations JSON** — Save illustration specs to `assets/illustrations.json`:
    ```json
    [{"name": "slug-name", "prompt": "Scene description (style prefix added automatically)"}]
    ```
12. **Generate illustrations**: `pipenv run python3 scripts/tiktok/illustrations.py <illustrations-json> <output-dir>`
    - Generates all illustrations with brand style references, portrait 1024x1536, transparent bg

### Phase 4: Composition & Render (automated)

13. **Prepare assets**: `pipenv run python3 scripts/tiktok/prepare_assets.py <content-folder>`
    - Copies illustrations + voiceover to `videos/public/` for Remotion
14. **Build Remotion composition** — Create `videos/src/{ConceptName}TikTok/` with config.ts, Slide.tsx, index.tsx. Register in Root.tsx under `<Folder name="TikTok">`.
15. **Render**: `cd videos && npx remotion render CompositionId out/output-name.mp4`
16. **Archive**: Copy mp4 back to content folder.

### Phase 5: Deliver (automated)

17. **Email**: Send the rendered video with caption and hashtags to both `abhinav@jabhi.ca` and `joieta@jabhi.ca` using the Google Workspace MCP. Send two separate emails (one per recipient). Format:
    - **To**: `abhinav@jabhi.ca` and `joieta@jabhi.ca` (use `abhinav@jabhi.ca` as `user_google_email` for both sends)
    - **Subject**: `{Concept Name} — TikTok Video`
    - **Body**: Caption text followed by hashtags, all on one line. No heading, no formatting — plain text ready to copy-paste into TikTok.
    - **Attachment**: The rendered mp4 file from the content folder (use `path` option)

## Helper Scripts

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `scripts/tiktok/voiceover.py` | ElevenLabs TTS + 1.25x speedup | Content folder (reads brief.md) | `assets/voiceover-raw.mp3`, `assets/voiceover.mp3` |
| `scripts/tiktok/transcribe.py` | Deepgram Nova-3 word timestamps | Content folder (reads voiceover.mp3) | `assets/transcript.json` + printed table |
| `scripts/tiktok/illustrations.py` | OpenAI gpt-image-1.5 with style refs | JSON config + output dir | Portrait PNGs in output dir |
| `scripts/tiktok/prepare_assets.py` | Copy assets to Remotion public/ | Content folder | Files in `videos/public/` |

## Folder Structure

```
content/tiktok/YYYY-MM-DD_HHMM_slug/
├── brief.md                    # Script, caption, hashtags, slide plan
├── assets/
│   ├── illustrations/          # PNGs (portrait, transparent bg)
│   ├── illustrations.json      # Illustration specs for regeneration
│   ├── voiceover-raw.mp3
│   ├── voiceover.mp3
│   └── transcript.json
└── slug.mp4                    # Final rendered video
```

## Critical Details (common mistakes)

- **Image size**: Must be `1024x1536` (portrait), NOT `1024x1024` — square images get cropped in vertical frame
- **Audio import**: Use `<Audio>` from `@remotion/media`, NOT from core remotion
- **ElevenLabs stability**: Only 0.0, 0.5, or 1.0 — no in-between values. Only pass stability, no other voice_settings.
- **Speed**: Apply via ffmpeg post-generation, not as an ElevenLabs parameter
- **Overflow**: Set `overflow: "visible"` on slide container to prevent zoom clipping
- **No text overlays**: TikTok captions + background music provide enough stimulation — don't add text to the video
- **Run end-to-end**: Generate all assets AND render the final video — don't stop at code

## Key Files

- Writing style reference: `docs/writing-style-reference.md` (Paul Graham essay + style guide)
- Method doc: `docs/tiktok-psych-video-method.md`
- Brand reference images: `assets/illustrations/overwhelmed-filing-cabinet.png`, `floating-yellow-balloon.png`, `planting-yellow-seedling.png`
- Example composition (new format, 30s): `videos/src/ParadoxOfChoiceTikTok/` (config.ts, Slide.tsx, index.tsx)
- Example brief (new format): `content/tiktok/2026-02-18_1430_paradox-of-choice/brief.md`
- Legacy composition (old format, 60s): `videos/src/ZeigarnikTikTok/`
