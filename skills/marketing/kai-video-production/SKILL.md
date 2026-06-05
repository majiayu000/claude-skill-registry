---
name: kai-video-production
description: Full-stack video production from script to rendered video. Combines script generation (optimized for TikTok/YouTube/Reels) with AI-powered video rendering using Remotion, AI voiceovers (Qwen3-TTS/ElevenLabs), music generation (ACE-Step), and browser-based demo recording. Multi-session project tracking with automatic intent reconciliation. Use when "create video", "produce video", "demo video", "product video", or any request to generate AND render video content.
---

# Video Production Pipeline

Complete video production from concept to final MP4. Combines two capabilities:
1. **Script generation** - Platform-optimized scripts (TikTok, YouTube, Reels)
2. **Video production** - AI-powered rendering with voiceovers, music, transitions

## Prerequisites Check

**Required:**
- Node.js 18+ (for Remotion)
- FFmpeg (for video encoding)

**Recommended for AI features:**
- Modal account ($30/month free compute) OR
- RunPod account (pay-per-second)
- ElevenLabs API key (optional, for premium voices)

Run `/video-setup` for interactive configuration.

---

## Part 1: Script Generation (existing kai-video skill)

### Phase 0: Load Product Context

Check if `MARKETING.md` exists in the **project root** (same directory as CLAUDE.md, README.md, package.json).

**If it exists:** Read it — skip product discovery questions.

**If it does NOT exist:** Auto-explore the codebase to create it in the **project root** (next to CLAUDE.md). Do NOT ask the user what the product is. Read CLAUDE.md, README.md, PROJECT.md, package.json, landing pages, and any project files. Search for email/ad/analytics config. Then create `MARKETING.md` using the template from `/kai-email-system`. Present draft to user for confirmation.

### Phase 1: Video Discovery

Read from `MARKETING.md`. Only ask about things not covered there:

1. **Topic/product** — what's the video about?
2. **Platform(s)** — TikTok, YouTube Shorts, Reels, YouTube long-form?
3. **Format** — talking head, screen recording, b-roll, animation, slides?
4. **Length** — short-form (15-60s) or long-form (5-15min)?
5. **Goal** — awareness, education, conversion, engagement?
6. **Production** — script only, or full video render?

### Phase 2: Script Production

Load these before writing:
- `knowledge/playbooks/video-content-creation.md`
- `knowledge/channels/tiktok-algorithm.md` (if TikTok)
- `knowledge/channels/youtube.md` (if YouTube)
- `knowledge/channels/instagram.md` (if Reels)

Use hook formulas, quality gates from existing `kai-video` skill.

Output scripts to `workspace/video/scripts/`

---

## Part 2: Video Production (new capability)

### Production Options

1. **Script only** - Stop after Phase 2, user records manually
2. **Automated production** - Continue to render pipeline
3. **Hybrid** - Generate some assets (voiceover, slides), user provides demos

### Video Templates

**Available templates:**
- **product-demo** - Marketing videos (title, problem, solution, demo, CTA)
- **explainer** - Educational content (title, overview, sections, recap)
- **demo-walkthrough** - Screen recordings with narration
- **social-short** - 15-60s vertical video for TikTok/Reels/Shorts
- **testimonial** - Customer quotes + visuals
- **announcement** - Product launches, releases, news

**Template structure:**
```
projects/{name}/
├── project.json          # Project state, scenes, assets
├── VOICEOVER-SCRIPT.md   # Full narration script
├── src/
│   ├── Root.tsx          # Remotion composition
│   ├── scenes/           # Scene components
│   └── config/           # Timing, brand, assets
├── public/
│   ├── audio/            # Voiceovers, music, SFX
│   ├── demos/            # Screen recordings
│   ├── images/           # Screenshots, graphics
│   └── videos/           # External video clips
└── CLAUDE.md             # Auto-generated status
```

### Production Pipeline

### Preflight Variant Lab

Before asset creation or rendering, generate lightweight variants and score them as a dry run:

- **3 hook variants** with platform, expected first-frame visual, and viewer promise
- **2 structure variants** for scene order or pacing
- **2 CTA variants** matched to the campaign goal
- **1 risk note per variant** for unsupported claims, brand mismatch, or approval needs

Write results to `workspace/video/projects/{name}/PREFLIGHT-VARIANTS.md`.

Use this scoring table:

| Factor | Score | Question |
|--------|-------|----------|
| Hook strength | 1-5 | Does the opening create immediate attention? |
| Message clarity | 1-5 | Is the core idea obvious after one watch? |
| Proof density | 1-5 | Are claims supported by demo, quote, data, or source? |
| Production fit | 1-5 | Can this be made with available assets and timeline? |
| Brand safety | 1-5 | Does it avoid fake authority, risky claims, or unclear rights? |

Pick one winner for production and keep rejected variants in the same file as the kill list. User approval is required before moving from variant lab to full render.

#### Step 1: Scene Planning

**Decompose script into scenes:**
```json
{
  "scenes": [
    {
      "id": 1,
      "type": "title",
      "duration": 5,
      "visual": "slide",
      "narration": "Introducing KaiCalls...",
      "status": "ready"
    },
    {
      "id": 2,
      "type": "demo",
      "duration": 20,
      "visual": "demos/call-flow.mp4",
      "narration": "Watch how it handles incoming calls...",
      "status": "asset-needed"
    }
  ]
}
```

**Scene types:**
- **title** - Branded opening (slide)
- **overview** - Key points (slide with bullets)
- **demo** - Screen recording (Playwright or external)
- **split-demo** - Side-by-side comparison
- **problem** - Pain point visualization
- **solution** - How product solves it
- **feature** - Specific feature highlight
- **stats** - Numbers, metrics (animated)
- **testimonial** - Customer quote + photo
- **cta** - Call to action (slide)
- **credits** - Team, thank you

#### Step 2: Asset Creation

**For each scene requiring assets:**

**Slide assets (auto-generated):**
- Title cards with brand colors/fonts
- Bullet point slides
- Stat visualization
- CTA screens

**Demo assets (user/AI created):**
- **Option 1:** Browser recording with Playwright
  ```bash
  /record-demo
  # Opens browser, user performs actions, saves MP4
  ```
- **Option 2:** External screen recording
  - User provides MP4/MOV
  - Moved to `public/demos/`
- **Option 3:** AI-generated demo
  - Script actions → Playwright automation → recording
  ```bash
  /record-demo --script demo-script.md --auto
  ```

**Image assets:**
- **AI generation** - FLUX.2 Klein for backgrounds, graphics
  ```bash
  python tools/flux2.py --prompt "Tech background" --cloud modal
  ```
- **AI editing** - Style transfer, backgrounds, effects
  ```bash
  python tools/image_edit.py --input photo.jpg --style cyberpunk
  ```
- **Screenshots** - Playwright capture
- **External** - User-provided images

#### Step 3: Audio Production

**Voiceover generation:**

**Option 1: AI voiceover (Qwen3-TTS, free)**
```bash
python tools/voiceover.py --provider qwen3 \\
  --speaker Ryan --script VOICEOVER-SCRIPT.md \\
  --scene-dir public/audio/scenes --json
```

**9 speakers available:**
- Ryan, Brad, Ava, Lily (male/female, neutral/warm/energetic)
- Emily, Sam, Alex, Kevin, Zoe

**Option 2: ElevenLabs (premium)**
```bash
python tools/voiceover.py --provider elevenlabs \\
  --voice-id {ID} --script VOICEOVER-SCRIPT.md
```

**Option 3: Voice cloning (custom brand voice)**
```bash
/voice-clone
# Records sample, creates cloned voice, saves to brand
```

**Music generation:**

**Option 1: ACE-Step (free, precise control)**
```bash
python tools/music_gen.py --preset corporate-bg \\
  --duration 120 --bpm 90 --key "D Minor"
```

**8 scene presets:**
- corporate-bg, upbeat-intro, dramatic-reveal, ambient-subtle
- tension-build, inspirational-montage, tech-minimal, celebration-end

**Option 2: ElevenLabs music**
```bash
python tools/music.py --prompt "Upbeat corporate" --duration 120
```

**Sound effects:**
```bash
python tools/sfx.py --preset whoosh  # Transitions
python tools/sfx.py --preset pop     # UI interactions
python tools/sfx.py --preset success # Completion
```

#### Step 4: Scene Review

**Launch Remotion Studio for visual verification:**
```bash
cd projects/{name}
npm run studio  # Opens localhost:3000
```

**Review checklist per scene:**
- [ ] Visual renders correctly
- [ ] Timing matches narration
- [ ] Transitions smooth
- [ ] Text readable
- [ ] Brand colors accurate
- [ ] Audio synced

**Iterative refinement:**
- Adjust timing in `config.ts`
- Tweak styles in scene components
- Replace assets if needed
- Re-sync audio

#### Step 5: Design Polish

**For slide-based scenes:**

Load `knowledge/frameworks/design/frontend-design.md` and refine:
- Typography hierarchy
- Color contrast
- Animation timing
- Layout composition
- Visual hierarchy

**Run design review:**
```bash
/design --scene {scene-id}
# Opens focused design session with frontend-design skill
```

#### Step 6: Rendering

**Preview render (fast, lower quality):**
```bash
npm run render -- --quality=low
```

**Final render (production quality):**
```bash
npm run render
# Outputs: out/{name}.mp4
```

**Render options:**
- `--codec=h264` (default, widely compatible)
- `--codec=h265` (smaller file size)
- `--resolution=1080p` (default)
- `--resolution=720p` (smaller file)
- `--fps=30` (default)
- `--fps=60` (smoother motion)

#### Step 7: Post-Production Utilities

**Add music to existing video:**
```bash
python tools/addmusic.py --input video.mp4 \\
  --prompt "Subtle ambient" --output final.mp4
```

**Redub with different voice:**
```bash
python tools/redub.py --input video.mp4 \\
  --voice-id {ID} --output dubbed.mp4
```

**Remove watermarks:**
```bash
python tools/dewatermark.py --input video.mp4 \\
  --preset sora --output clean.mp4 --cloud modal
```

**Upscale resolution:**
```bash
python tools/upscale.py --input video.mp4 \\
  --scale 2x --output hd.mp4 --cloud modal
```

---

## Multi-Session Project Tracking

### Project Lifecycle

```
planning → assets → review → audio → editing → rendering → complete
```

### project.json Schema

```json
{
  "name": "kaicalls-demo-v1",
  "template": "product-demo",
  "brand": "kaicalls",
  "created": "2026-03-28T15:00:00Z",
  "updated": "2026-03-28T16:30:00Z",
  "phase": "audio",
  "scenes": [
    {
      "id": 1,
      "type": "title",
      "duration": 5,
      "visual": "slide",
      "narration": "Introducing KaiCalls",
      "status": "ready"
    },
    {
      "id": 2,
      "type": "demo",
      "duration": 20,
      "visual": "demos/call-handling.mp4",
      "narration": "Watch how it handles calls...",
      "status": "asset-present"
    }
  ],
  "audio": {
    "voiceover": {
      "file": "audio/voiceover.mp3",
      "status": "present",
      "provider": "qwen3",
      "speaker": "Ryan"
    },
    "music": {
      "file": "audio/background.mp3",
      "status": "needed",
      "preset": "corporate-bg"
    }
  },
  "estimates": {
    "totalDurationSeconds": 90
  },
  "sessions": [
    {
      "date": "2026-03-28",
      "phase": "planning",
      "summary": "Created project, defined scenes"
    },
    {
      "date": "2026-03-28",
      "phase": "assets",
      "summary": "Recorded demo video"
    }
  ]
}
```

### Intent vs Reality Reconciliation

**On project resume:**

1. **Scan filesystem** - Check what assets actually exist
2. **Compare to intent** - What does project.json expect?
3. **Update statuses:**
   - `asset-needed` + file exists → `asset-present`
   - `ready` + file missing → `asset-missing`
4. **Flag discrepancies** - Alert user to missing/unexpected files
5. **Regenerate CLAUDE.md** - Auto-generated status document

**CLAUDE.md example:**
```markdown
# Project: kaicalls-demo-v1

**Template:** product-demo | **Brand:** kaicalls | **Phase:** audio
**Last Updated:** 30 minutes ago

## Current Status

All demo assets are present. Voiceover generated. Ready for final review.

## Scenes

| # | Scene | Type | Visual | Status |
|---|-------|------|--------|--------|
| 1 | Title | title | slide | ✅ Ready |
| 2 | Demo | demo | demos/call-handling.mp4 | ✅ Present |
| 3 | Stats | stats | slide | ✅ Ready |
| 4 | CTA | cta | slide | ✅ Ready |

## Audio

- Voiceover: ✅ Generated (Qwen3-TTS, Ryan voice)
- Music: ⬜ Optional background music

## Next Actions

1. **Preview in Remotion Studio**
   ```bash
   cd projects/kaicalls-demo-v1 && npm run studio
   ```

2. **Render final video**
   ```bash
   npm run render
   ```

## Session History

- 2026-03-28: Created project, defined scenes (planning)
- 2026-03-28: Recorded demo video (assets)
- 2026-03-28: Generated voiceover (audio)
```

### Session Continuity

**First session:** Planning + scene definition  
**Second session:** Asset creation  
**Third session:** Audio generation  
**Fourth session:** Review + polish  
**Fifth session:** Final render

**Between sessions:**
- project.json tracks state
- CLAUDE.md provides instant context
- Automatic reconciliation on resume
- No context loss

---

## Brand Integration

### Brand Profiles

```
brands/{brand}/
├── brand.json       # Colors, fonts, typography
├── voice.json       # Voice settings (speaker, style)
└── assets/          # Logo, backgrounds, graphics
```

### brand.json Example

```json
{
  "name": "KaiCalls",
  "colors": {
    "primary": "#3B82F6",
    "secondary": "#10B981",
    "background": "#111827",
    "text": "#F9FAFB"
  },
  "fonts": {
    "heading": {
      "family": "Inter",
      "weight": 700
    },
    "body": {
      "family": "Inter",
      "weight": 400
    }
  },
  "logo": "assets/logo.svg",
  "style": "modern-tech"
}
```

### voice.json Example

```json
{
  "provider": "qwen3",
  "speaker": "Ryan",
  "tone": "professional-warm",
  "pace": "moderate",
  "elevenlabs": {
    "voice_id": "YOUR_VOICE_ID",
    "stability": 0.75,
    "similarity_boost": 0.75
  }
}
```

**Auto-application:**
- Brand colors applied to all slides
- Brand fonts used throughout
- Logo appears on title/credits
- Voice settings used for all voiceovers

---

## Transition Library

**7 custom transitions + 4 Remotion official:**

| Transition | Description | Use Case |
|------------|-------------|----------|
| `glitch()` | Digital distortion + RGB shift | Tech/glitch aesthetic |
| `rgbSplit()` | Chromatic aberration | Energetic transitions |
| `zoomBlur()` | Radial motion blur | Dramatic reveals |
| `lightLeak()` | Cinematic lens flare | Professional polish |
| `clockWipe()` | Radial sweep reveal | Time-based content |
| `pixelate()` | Digital mosaic | Retro/8-bit style |
| `checkerboard()` | Grid-based reveal (9 patterns) | Clean, geometric |
| `slide()` | Slide in/out (official) | Standard transitions |
| `fade()` | Crossfade (official) | Subtle transitions |
| `wipe()` | Directional wipe (official) | Directional flow |
| `flip()` | 3D flip (official) | Playful transitions |

**Usage in scenes:**
```typescript
import { glitch, slide } from '@/lib/transitions';

<Sequence from={0} durationInFrames={150}>
  <Title />
</Sequence>
<Sequence from={150} durationInFrames={600}>
  <Demo transition={glitch({ duration: 30 })} />
</Sequence>
```

---

## Cloud GPU Integration

### Modal (Recommended)

**Setup:**
```bash
/video-setup
# Deploys all tools automatically
# $30/month free compute on Starter plan
```

**Tools deployed:**
- qwen3_tts - Text-to-speech (~$0.01/video)
- flux2 - Image generation (~$0.02/image)
- music_gen - Music generation (~$0.05/track)
- sadtalker - Talking head video (~$0.10/video)
- ltx2 - AI video generation (~$0.23/clip)
- image_edit - Image editing (~$0.03/image)
- upscale - Image upscaling (~$0.01/image)
- dewatermark - Watermark removal (~$0.10/video)

**Typical monthly cost:** $1-3 for a few videos (within free tier)

### RunPod (Alternative)

**Setup:**
```bash
python tools/qwen3_tts.py --setup
python tools/flux2.py --setup
# ... repeat for each tool
```

**Pay-per-second, no minimums**

---

## Quality Gates

**Before rendering:**

1. [ ] **Script approved** - Hooks strong, no AI slop
2. [ ] **All assets present** - No missing demos/images
3. [ ] **Timing validated** - Scene durations match narration
4. [ ] **Audio synced** - Voiceover aligns with visuals
5. [ ] **Brand consistent** - Colors, fonts, logo correct
6. [ ] **Transitions smooth** - No jarring cuts
7. [ ] **Text readable** - Contrast sufficient, size appropriate
8. [ ] **Preview reviewed** - Remotion Studio walkthrough complete

**After rendering:**

9. [ ] **Resolution correct** - 1080p or as specified
10. [ ] **Audio levels balanced** - Voiceover audible over music
11. [ ] **File size reasonable** - Under platform limits
12. [ ] **Format compatible** - Works on target platform

---

## Output Organization

```
workspace/video/
├── _video-projects.md              # Index of all projects
├── projects/
│   ├── kaicalls-demo-v1/
│   │   ├── project.json
│   │   ├── VOICEOVER-SCRIPT.md
│   │   ├── CLAUDE.md
│   │   ├── src/
│   │   ├── public/
│   │   └── out/
│   │       └── kaicalls-demo-v1.mp4
│   └── tropibot-launch/
│       └── ...
├── scripts/                         # Script-only outputs
│   ├── tiktok/
│   ├── youtube/
│   └── reels/
└── _production-guide.md
```

---

## Commands Integration

### /kai-video (entry point)

**Script only:**
```bash
/kai-video script --platform tiktok --topic "KaiCalls demo"
# Generates script, stops
```

**Full production:**
```bash
/kai-video produce --template product-demo --brand kaicalls
# Full pipeline: script → assets → audio → render
```

**Resume project:**
```bash
/kai-video resume kaicalls-demo-v1
# Picks up where left off
```

### /video-setup (one-time)

```bash
/video-setup
# Interactive setup:
# 1. Cloud GPU provider (Modal/RunPod)
# 2. API keys (ElevenLabs optional)
# 3. Tool deployment
# 4. Verification
```

### /record-demo (asset creation)

```bash
/record-demo --url https://app.kaicalls.com --output call-demo
# Opens browser, records interactions, saves MP4
```

### /generate-voiceover (audio creation)

```bash
/generate-voiceover --project kaicalls-demo-v1
# Reads VOICEOVER-SCRIPT.md, generates audio per scene
```

### /scene-review (quality check)

```bash
/scene-review --project kaicalls-demo-v1
# Opens Remotion Studio, walks through each scene
```

### /design (visual refinement)

```bash
/design --scene 3 --project kaicalls-demo-v1
# Focused design session for specific scene
```

### /voice-clone (brand voice)

```bash
/voice-clone --brand kaicalls
# Records sample, creates cloned voice
```

---

## Cost Estimates

**Full video production (60-90 seconds):**

| Component | Tool | Cost |
|-----------|------|------|
| Script generation | Claude | ~$0.10 |
| Voiceover (AI) | Qwen3-TTS | ~$0.01 |
| Music (AI) | ACE-Step | ~$0.05 |
| Images (if needed) | FLUX.2 | ~$0.04 |
| Rendering | Local (Remotion) | $0.00 |
| **Total** | | **~$0.20** |

**With premium features:**
- ElevenLabs voiceover: +$0.30
- AI video clips (LTX-2): +$0.23/clip
- Talking head (SadTalker): +$0.10

**Free tier covers:** 100+ videos/month on Modal Starter plan ($30 free compute)

---

## Examples & Templates

**Load these when starting production:**

**For product demos:**
- `templates/product-demo/` - Marketing video structure
- `examples/digital-samba-skill-demo/` - Finished product demo

**For explainers:**
- `templates/explainer/` - Educational content structure
- `examples/schlumbergera/` - Sprint review example

**For social shorts:**
- `templates/social-short/` - Vertical video optimized
- Hook-first structure, 15-60 seconds

**All examples include:**
- Full source code
- Rendered MP4 output
- Production notes
- Lessons learned

---

## Key Principles

1. **Script first, production second** - Never skip script quality for production speed
2. **Multi-session by default** - Projects span days/weeks, track state meticulously
3. **Intent vs reality** - Filesystem is truth, reconcile on every resume
4. **Brand consistency** - Auto-apply brand profiles, don't re-specify colors/fonts
5. **Quality gates mandatory** - Review before render, verify after
6. **Cost-conscious** - Prefer free/cheap AI tools, Modal free tier sufficient
7. **Platform-optimized** - Different outputs for TikTok vs YouTube vs Reels

---

## Evolution

**This skill combines:**
- Original `kai-video` script generation (March 2026)
- `claude-code-video-toolkit` production pipeline (March 2026)
- Multi-session project tracking from video toolkit
- Brand integration from marketing harness

**Continuous improvement:**
- Track what works per platform
- Refine templates based on performance
- Add new transitions, scenes, effects
- Optimize costs and render times

**Feedback loop:**
- Video performs well → template promoted
- Script resonates → hook formula added
- Production bottleneck → tool improved
- Cost spike → cheaper alternative found

---

## Integration with Other Skills

**Combines with:**
- `kai-content-calendar` - Schedule video releases
- `kai-social` - Auto-generate social posts from video
- `kai-repurpose` - Extract clips for multiple platforms
- `kai-analytics` - Track video performance
- `kai-brand` - Maintain brand consistency

**Feeds into:**
- Product launches (video + email + ads)
- Content marketing (blog + video + social)
- Sales enablement (demo videos)
- Customer success (tutorial videos)

**Example workflow:**
```bash
# 1. Plan content
/kai-content-calendar --month April

# 2. Produce video
/kai-video produce --template product-demo --brand kaicalls

# 3. Repurpose for social
/kai-repurpose --source projects/kaicalls-demo-v1/out/video.mp4

# 4. Schedule posts
/kai-social --schedule --video

# 5. Track performance
/kai-analytics --video-performance
```

---

## Troubleshooting

**"Asset not found" error:**
- Check `project.json` paths match filesystem
- Run intent reconciliation (automatic on resume)
- Verify file moved to correct directory

**"Audio out of sync":**
- Adjust timing in `config.ts`
- Regenerate voiceover with updated script
- Use Remotion Studio to visually verify sync

**"Render fails":**
- Check FFmpeg installed (`ffmpeg -version`)
- Verify all assets exist
- Run preview render first (`--quality=low`)

**"Tool timeout on Modal":**
- Check Modal account has compute credits
- Verify tool deployed (`modal app list`)
- Try RunPod alternative

**"Brand colors not applied":**
- Verify `brand.json` in brands/ directory
- Check brand name matches in `project.json`
- Regenerate `src/config/brand.ts`

---

## Next Steps After This Skill

**When user says "create video":**

1. **Clarify scope:**
   - Script only? Or full production?
   - Which platform(s)?
   - Timeline?

2. **Choose path:**
   - **Script only:** Use original kai-video workflow
   - **Full production:** Use production pipeline

3. **For production:**
   - Check if setup complete (`/video-setup`)
   - Select template
   - Create project
   - Guide through pipeline

4. **Track progress:**
   - Update project.json after each step
   - Regenerate CLAUDE.md
   - Flag blockers clearly

5. **On resume:**
   - Scan filesystem
   - Reconcile intent vs reality
   - Present current status
   - Suggest next action

---

**This skill is the union of script generation (marketing focus) and video production (technical execution). Use the appropriate parts based on user needs. Always start with script quality — production amplifies good scripts, it doesn't fix bad ones.**
