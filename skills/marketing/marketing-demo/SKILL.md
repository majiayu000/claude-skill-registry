---
name: marketing-demo
description: |
  Record product demos and walkthroughs for marketing assets. Two modes: quick screenshot-stitch demos via ply + ffmpeg, or polished Remotion compositions. Use when the user mentions product demo, demo video, walkthrough video, feature showcase, screen recording, GIF demo, product tour, onboarding video, visual tutorial, feature walkthrough, landing page video, hero video, product video, app preview video, or wants to show their product in action. Even if they just say 'show what it does', 'make a video of the app', 'I need a demo for my landing page', or 'record the app' — this is the skill. If someone has a working product and needs marketing assets that show it off, start here. Owns screen-recorded product demos and walkthroughs. For an AI-generated marketing or brand video with no real product footage, see /higgsfield-generate; for Remotion code and `remotion render` issues, see /remotion-best-practices; for stitching existing slides into an MP4, see /video-content.
category: creative
layer: execution
tier: nice-to-have
reads:
  - brand/creative-kit.md
  - brand/voice-profile.md
  - brand/stack.md
writes:
  - marketing/demos/
depends-on:
  - visual-style
triggers:
  - product demo
  - demo video
  - walkthrough video
  - screen recording
  - GIF demo
  - product tour
  - onboarding video
  - feature showcase
  - hero video
allowed-tools:
  - Bash(ply *)
  - Bash(ffmpeg *)
  - Bash(npx remotion *)
---

# /marketing-demo — Product Demo Recorder

Record product demos for marketing. Two production paths: quick (ply + ffmpeg) for rough demos, polished (Remotion) for branded marketing videos.

## Reads

- `brand/creative-kit.md` — Colors, fonts, logo paths for branded overlays
- `brand/voice-profile.md` — Tone guidance for text overlays
- `brand/stack.md` — Available tools (ply, ffmpeg, remotion)

## On Activation

1. Read `brand/creative-kit.md` for colors, fonts, logo paths. If missing, ask for brand colors and logo.
2. Read `brand/voice-profile.md` for tone guidance on text overlays. If missing, use clear/neutral tone.
3. Read `brand/stack.md` to confirm available tools. If missing, detect tools directly.
4. Check tool availability:
   ```bash
   command -v ply && echo "ply: ready" || echo "ply: missing"
   command -v ffmpeg && echo "ffmpeg: ready" || echo "ffmpeg: missing"
   command -v npx && echo "remotion: available" || echo "remotion: unavailable"
   ```
5. If `ply` or `ffmpeg` missing, warn and suggest install.

## Shot Duration Rules

| Demo Type | Duration per Shot | Notes |
|-----------|------------------|-------|
| Quick overview | 0.5-1s | Fast cuts, build excitement |
| Feature demo | 2-3s | Time to read + comprehend |
| Walkthrough | 4-5s | Instructional pacing |
| Social clip | 1-2s | Attention-grabbing, fast |

## Demo Storytelling Principles

Demos fail when they show the product mechanically instead of telling a story. The viewer needs a reason to keep watching. These principles come from what actually gets engagement on landing pages and social:

1. **Open with the outcome, not the setup.** The first 2 seconds decide if someone watches the rest. Show the "after" state — the dashboard with data, the completed design, the result. Setup (login, loading, navigation) earns zero attention.
2. **One feature = one demo.** Trying to cram 5 features into 30 seconds makes all of them forgettable. A focused demo of one feature is worth more than a rushed tour.
3. **Show the magic moment.** Every product has one interaction where users go "oh wow." Find that moment and build the demo around it — it's why people click "try it."
4. **Add context with text overlays.** Social videos autoplay muted. Without text callouts, viewers see UI changing with no idea what's happening or why it matters. Every shot needs a 3-6 word overlay explaining the value.
5. **Pacing: 2-3 seconds per concept.** This feels fast, but viewer attention is brutal. If a shot doesn't earn its screen time with new information, cut it.

## Step 1: Determine Demo Type

| Type | Duration | Resolution | Format | Use Case |
|------|----------|-----------|--------|----------|
| Hero demo | 15-30s | 1280x800 | MP4 | Landing page above-fold |
| Feature highlight | 5-15s | 1280x800 | GIF/MP4 | Feature section, docs |
| Full walkthrough | 60-180s | 1280x800 | MP4 | YouTube, sales deck |
| Social clip | 5-15s | 1080x1080 | MP4 | Instagram, Twitter/X |
| Email GIF | 3-8s | 600x400 | GIF | Email campaigns |
| How-to | 30-90s | 1280x800 | MP4 | Help docs, onboarding |

Ask the user which type, or infer from context.

## Step 2: Plan Shot List

Before recording, plan each shot:

```markdown
## Shot List

1. [Action: Navigate to landing page]
   - URL: https://example.com
   - Wait: 1s for load
   - Highlight: Hero section

2. [Action: Click "Get Started" button]
   - Wait: transition animation
   - Highlight: Signup form

3. [Action: Fill demo data]
   - Type: demo@example.com
   - Highlight: Success state
```

Each shot = one `ply` screenshot or interaction sequence.

## Step 3: Choose Production Mode

### Mode A: Quick Demo (ply + ffmpeg)

Fast, rough demos from screenshots stitched into video.

**Capture screenshots:**
```bash
# Navigate and screenshot each shot
ply navigate "https://example.com"
ply screenshot --output marketing/demos/shot-01.png
ply click "Get Started"
ply screenshot --output marketing/demos/shot-02.png
```

**Stitch with ffmpeg:**
```bash
# MP4 from screenshots (2 seconds per frame)
ffmpeg -framerate 0.5 -i marketing/demos/shot-%02d.png \
  -c:v libx264 -pix_fmt yuv420p \
  -vf "scale=1280:800:force_original_aspect_ratio=decrease,pad=1280:800:(ow-iw)/2:(oh-ih)/2" \
  marketing/demos/demo.mp4

# Preview GIF (lower quality, smaller file)
ffmpeg -i marketing/demos/demo.mp4 \
  -vf "fps=10,scale=640:-1:flags=lanczos" \
  -c:v gif marketing/demos/demo-preview.gif

# Email GIF (600px wide, optimized)
ffmpeg -i marketing/demos/demo.mp4 \
  -vf "fps=8,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
  marketing/demos/demo-email.gif

# Square crop for social (1080x1080)
ffmpeg -i marketing/demos/demo.mp4 \
  -vf "crop=min(iw\,ih):min(iw\,ih),scale=1080:1080" \
  marketing/demos/demo-square.mp4
```

### Mode B: Polished Demo (Remotion)

For marketing-grade output with transitions, text overlays, branded intros.

**Generate Remotion composition:**
```bash
# Initialize if needed
npx remotion init marketing/demos/remotion-demo

# Render final video
npx remotion render marketing/demos/remotion-demo/src/index.tsx \
  --output marketing/demos/demo-polished.mp4
```

**Composition structure:**
```
src/
├── index.tsx          # Root composition
├── Intro.tsx          # Branded intro (logo, tagline)
├── DemoScene.tsx      # Screenshot with text overlay
├── Transition.tsx     # Fade/slide between scenes
└── Outro.tsx          # CTA + URL
```

**Key Remotion patterns** (see [references/remotion-examples.md](references/remotion-examples.md) for complete component code):
- Use `<Img>` for screenshots, `<AbsoluteFill>` for layout
- `useCurrentFrame()` + `interpolate()` for animations
- Pull brand colors from `brand/creative-kit.md`
- 30fps for smooth playback, 1280x720 or 1920x1080
- Add text overlays calling out features with `<Sequence>`

**Intro scene (2-3s):** Logo centered, tagline fades in. Brand colors as background gradient. Keep it short — the product is the star.

**Demo scene (per shot):** Screenshot fills 80% of frame. Text overlay at top or bottom with 1-line feature callout. Use `interpolate()` for a subtle zoom-in (1.0 → 1.05 over the scene duration) to add life.

**Transition between scenes:** Fade + slight slide (200ms). Never use fancy wipes — they distract from the product.

**Outro scene (3-4s):** CTA text ("Try it free at [url]"), logo, and optional social proof line. This is the only slide that sells — keep all other slides focused on showing.

### Error Recovery

**ply failures** (page doesn't load, element not found, timeout): Skip to shot N+1 and document the failure in the shot list. After all shots complete, review skipped shots and retry once. If still failing, use manual screenshots as fallback.

**ffmpeg failures** (codec not found, format error): Check `ffmpeg -codecs` for available codecs. If libx264 is missing, try `-c:v h264` or install via `brew install ffmpeg`. For GIF palette issues, simplify the filter chain — drop `split/palettegen/paletteuse` and use basic `-vf "fps=10,scale=640:-1"`.

**Remotion failures** (render crashes, composition errors): Check node version (`node -v`, needs 18+). If `npx remotion render` fails, try `npx remotion render --gl=angle` or `--gl=swangle` for GPU issues. For composition errors, verify all `<Img>` src paths are correct and images exist.

## Step 4: Convert & Output

All outputs go to `marketing/demos/`. Name by type:

| Output | Filename | Notes |
|--------|----------|-------|
| MP4 (desktop) | `demo-hero.mp4` | H.264, 1280x800 |
| MP4 (social) | `demo-social-1080.mp4` | Square, 1080x1080 |
| GIF (preview) | `demo-preview.gif` | 640px wide, <5MB |
| GIF (email) | `demo-email.gif` | 600px wide, <2MB |
| MP4 (polished) | `demo-polished.mp4` | Remotion output |

## Step 5: Completion Summary

```markdown
## Demo Assets Created

| Asset | Size | Format | Suggested Use |
|-------|------|--------|--------------|
| demo-hero.mp4 | 1.2MB | MP4 1280x800 | Landing page hero |
| demo-preview.gif | 3.4MB | GIF 640px | README, docs |
| demo-email.gif | 1.1MB | GIF 600px | Email campaigns |
| demo-social-1080.mp4 | 800KB | MP4 1080x1080 | Instagram, X |

All assets saved to `marketing/demos/`.
```

## Viewport Configs

| Platform | Width | Height | Scale |
|----------|-------|--------|-------|
| Desktop | 1280 | 800 | 1x |
| Desktop HD | 1920 | 1080 | 1x |
| Mobile | 390 | 844 | 2x |
| Instagram | 1080 | 1080 | 1x |
| Twitter/X | 1200 | 675 | 1x |
| Email | 600 | 400 | 1x |

## Anti-Patterns

| Mistake | Why It Fails |
|---------|-------------|
| Recording login/signup flows | Nobody cares about your auth screen. Start after login. |
| Showing loading spinners | Edit them out or skip to the loaded state. Spinners kill momentum. |
| No text overlays on silent autoplay | Social videos autoplay muted. Without text, viewers have no idea what they're watching. |
| Demo longer than 60s without chapter breaks | Attention drops after 15s. If it's long, add clear section titles. |
| Recording at inconsistent viewport sizes | Shots that jump between sizes look amateur. Lock viewport before recording. |
| Showing every feature | Pick 3-5 features max. Demos that show everything sell nothing. |
| Mouse cursor wandering aimlessly | Plan each click. Cursor should move with purpose — straight lines to targets. |

## Related Skills

- `/creative` — Ad visuals, product photos (static assets, not demos)
- `/content-atomizer` — Turn demo into platform-specific posts
- `/page-cro` — Audit the page the demo showcases
