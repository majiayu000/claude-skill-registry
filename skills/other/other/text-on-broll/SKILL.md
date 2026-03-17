---
name: text-on-broll
description: Create short-form text-on-video content using AI-generated b-roll (Veo 3.1) composited with on-screen text (Remotion). End-to-end workflow from topic to publishable vertical video. Use when you need Instagram Reels, TikToks, or Shorts with bold text overlays on cinematic footage.
---

# Text on B-Roll

Create scroll-stopping short-form videos by compositing bold on-screen text over AI-generated b-roll footage. The full pipeline: topic in, rendered MP4s out.

**Prerequisite skills (loaded automatically):**
- `video-generator` - Veo 3.1 API for b-roll generation
- `video-caption-creation` - Hook frameworks and text patterns
- `one-liners` - 12 core one-liner patterns
- `nano-banana-image-generator` - Optional: generate a matching static thumbnail

---

## When to Use This Skill

- Promoting a blog post, article, or newsletter on Reels/TikTok/Shorts
- Creating text-forward social videos from a topic or theme
- Building a batch of short-form content around one visual concept
- Any time you want bold text + cinematic b-roll without filming anything

**This skill is NOT for:**
- Podcast clips with audio (use `youtube-clip-extractor`)
- Videos with voiceover or dialogue (use `video-generator` directly)
- Static image posts (use `nano-banana-image-generator`)

---

## Workflow Overview

1. **Understand the topic** - What's the article/theme about?
2. **Generate b-roll** - One photorealistic Veo clip that matches the topic
3. **Write 8-12 text options** - Framework-fitted to proven patterns
4. **User selects favorites** - Pick 2-4 lines
5. **Scaffold Remotion project** - From template
6. **Preview in Studio** - User approves look
7. **Render to MP4** - One video per text option

---

## Step 1: B-Roll Generation

Generate one strong b-roll clip using `video-generator`. The visual should be:

- **Photorealistic** - not illustrated or stylized
- **Extreme close-up or tight shot** - intense, tactile, sensory
- **One simple action** - hands doing something, a single motion
- **Ambient audio only** - no dialogue, no music
- **9:16 vertical, 1080p, 8 seconds**

### B-Roll Prompt Template

```
Extreme close-up, shallow depth of field. [Subject performing tactile action].
[Specific sensory details - textures, colors, materials]. [Paper/surface reacts to the action].
The sound of [specific ambient audio]. Photorealistic, handheld micro-movement,
warm natural light from a nearby window.
```

### B-Roll Quality Checklist

- [ ] Photorealistic (not AI-looking)
- [ ] Strong tactile/sensory quality
- [ ] Simple composition (one focal point)
- [ ] No text or symbols in the footage
- [ ] Vertical 9:16
- [ ] Motion is slow and deliberate (not chaotic)

### Running the Generation

```bash
cd "/Users/charliedeist/Desktop/New Root Docs/OpenEd Vault"
export GEMINI_API_KEY=$(grep GEMINI_API_KEY .env | cut -d'=' -f2) && \
python3 ".claude/skills/video-generator/scripts/generate_video.py" \
  "Your prompt here" \
  --aspect 9:16 --resolution 1080p --duration 8 \
  --name "descriptive-name" \
  --output "Studio/SEO Content Production/" \
  --negative "text overlays, watermarks, blurry, cartoon, illustration, anime"
```

Veo takes 1-6 minutes. If the first result has artifacts, regenerate - don't rework.

---

## Step 2: Write Text Options

Generate 8-12 on-screen text options using proven patterns. The text must work WITHOUT audio context - it stands alone over silent b-roll.

### Pattern Library (Use These)

| Pattern | Format | Example |
|---------|--------|---------|
| **Stop + Complaint** | "Stop [universal frustration]" | "Stop grading kids on how fast they fill in bubbles." |
| **Everyday Observation** | "[Simple truth no one says]" | "Nobody remembers their test scores." |
| **Existential Question** | "[Question that points out absurdity]" | "Who decided 30 bubbles could measure a kid?" |
| **Normalize** | "Normalize [thing people feel guilty about]" | "Normalize letting kids destroy the answer sheet." |
| **Values / Core Belief** | "[Worldview in one line]" | "Curiosity doesn't fit in a bubble." |
| **Mock Instruction** | "[Absurdly specific command]" | "Instructions unclear. Used the Scantron as a canvas." |
| **Polarizing Statement** | "[Challenge common assumption]" | "Scantrons don't measure intelligence. They measure obedience." |
| **Full Quote** | "[Long conversational text that fills screen]" | "We hand kids four choices and call it thinking. Then we wonder why they let AI think for them." |
| **Two-Part Reveal** | Setup → hard cut → punchline | "They said my kid can't think critically." → "She was finger painting while your kid was memorizing answers." |
| **Aspirational** | "This is your sign to [permission]" | "This is your sign to let your kid color outside the bubbles." |

### Text Quality Rules

- **McDonald's Test:** If a truck driver wouldn't get it, simplify
- **First 3 words do 80% of the work.** Front-load the punch
- **Mix lengths:** Include punchy (2-5 words), statement (5-8), narrative (9-15), and full-quote (15+)
- **No AI-isms:** No "delve," "comprehensive," "crucial," "landscape"
- **No correlatives:** Never "X isn't just Y - it's Z"
- **Conversational:** Would you text this to a friend?
- **Specific > vague:** "Stop acting like worksheets are learning" beats "Education should be better"

### Text Sizing Guide

| Text Length | Font Size | Notes |
|-------------|-----------|-------|
| 2-5 words | 78-90px | Big, dominant, centered |
| 5-8 words | 66-78px | Still bold, may wrap to 2 lines |
| 9-15 words | 56-66px | Will wrap to 3-4 lines, still readable |
| 15+ words | 48-56px | Fills more screen, reads like a paragraph |
| Two-part reveal | 60-66px each | Part 1 slightly larger than part 2 |

---

## Step 3: Remotion Composition

### Template Location

Reusable template files are at:
`.claude/skills/text-on-broll/template/`

### Quick Setup

```bash
# Create project directory
mkdir -p "Studio/[project-name]/text-on-broll"
cd "Studio/[project-name]/text-on-broll"

# Init and install
npm init -y
npm install --save remotion @remotion/cli @remotion/player react react-dom
npm install --save-dev typescript @types/react

# Create directories
mkdir -p src public

# Copy b-roll video
cp path/to/generated-video.mp4 public/bg-video.mp4
```

Then create three files from the templates below.

### tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ESNext",
    "module": "commonjs",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

### src/index.ts

```typescript
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";

registerRoot(RemotionRoot);
```

### src/Root.tsx

Register one `<Composition>` per text variant. All compositions share the same settings:

```typescript
import React from "react";
import { Composition } from "remotion";
// Import your compositions from TextOverlay.tsx

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="variant-name"
        component={YourComponent}
        durationInFrames={240}  // 8s at 30fps
        fps={30}
        width={1080}
        height={1920}  // 9:16 vertical
      />
    </>
  );
};
```

### src/TextOverlay.tsx - The Core Component

```typescript
import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  staticFile,
  useCurrentFrame,
} from "remotion";

const IGText: React.FC<{
  text: string;
  fontSize?: number;
  top?: string;
}> = ({ text, fontSize = 72, top = "38%" }) => {
  return (
    <div
      style={{
        position: "absolute",
        top,
        left: "50%",
        transform: "translateX(-50%)",
        width: "85%",
        textAlign: "center",
        zIndex: 10,
      }}
    >
      <span
        style={{
          fontFamily: "'Helvetica Neue', 'Inter', Arial, sans-serif",
          fontWeight: 800,
          fontSize,
          lineHeight: 1.15,
          color: "white",
          WebkitTextStroke: "2.5px rgba(0,0,0,0.9)",
          textShadow: "0 3px 12px rgba(0,0,0,0.5)",
          letterSpacing: "-0.02em",
        }}
      >
        {text}
      </span>
    </div>
  );
};
```

### The IGText Style (Locked In)

This is the approved IG-native text style. Do not change without explicit request:

| Property | Value | Why |
|----------|-------|-----|
| Font family | Helvetica Neue / Inter | Clean, IG-native feel |
| Weight | 800 (extra bold) | Readable over video |
| Color | White | Maximum contrast |
| Stroke | 2.5px rgba(0,0,0,0.9) | Thin black outline, readable on any background |
| Shadow | 0 3px 12px rgba(0,0,0,0.5) | Subtle depth, not cheesy |
| Letter spacing | -0.02em | Tighter, more editorial |
| Line height | 1.15 | Compact multi-line |
| Width | 85% of frame | Safe margins for IG |
| Animation | None | Text appears immediately, no fade/spring |

### Composition Patterns

**Single line (most common):**
```tsx
export const MyComposition: React.FC = () => (
  <AbsoluteFill>
    <OffthreadVideo src={staticFile("bg-video.mp4")} />
    <IGText text="Your text here." fontSize={68} top="32%" />
  </AbsoluteFill>
);
```

**Two-part reveal (hard cut at midpoint):**
```tsx
export const TwoPartReveal: React.FC = () => {
  const frame = useCurrentFrame();
  const midpoint = 108; // ~3.6s at 30fps

  return (
    <AbsoluteFill>
      <OffthreadVideo src={staticFile("bg-video.mp4")} />
      {frame < midpoint && (
        <IGText text="Setup line." fontSize={66} top="30%" />
      )}
      {frame >= midpoint && (
        <IGText text="Punchline." fontSize={60} top="28%" />
      )}
    </AbsoluteFill>
  );
};
```

---

## Step 4: Preview and Render

### Preview

```bash
npx remotion studio --port 3123
```

Opens at http://localhost:3123. Check all compositions. Look for:
- Text readable over the video at all moments
- No text clipping at edges
- Font size appropriate for text length
- Two-part reveal timing feels natural

### Render All Compositions

```bash
# Render a single composition
npx remotion render src/index.ts [composition-id] out/[name].mp4

# Render all compositions in batch
for comp in comp1 comp2 comp3; do
  npx remotion render src/index.ts $comp out/$comp.mp4
done
```

### Render Settings

| Setting | Value |
|---------|-------|
| Codec | H.264 (default) |
| Frame rate | 30fps |
| Resolution | 1080x1920 |
| CRF | 18 (high quality) |

### Output Routing

| Platform | Specs | Notes |
|----------|-------|-------|
| Instagram Reels | 9:16, < 90s, < 4GB | Upload directly |
| TikTok | 9:16, < 10 min, < 287MB | Upload directly |
| YouTube Shorts | 9:16, < 60s | Upload directly |
| Stories | 9:16, < 15s per story | May need to trim to 8s |

---

## Batch Production Workflow

For creating multiple videos from one topic (e.g., promoting an article):

1. **Generate 1 b-roll clip** that captures the topic's visual metaphor
2. **Write 10 text options** across all pattern types
3. **User picks 3-4 favorites**
4. **Scaffold 1 Remotion project** with all selected as separate compositions
5. **Preview all in Studio**, adjust sizes/positions
6. **Batch render** all compositions
7. **Pair each video with a platform-specific caption** (from content-repurposer)

This gives you 3-4 unique videos from one generation session, each with different text but the same compelling visual.

---

## Skill Chain

This skill works best as part of a content production chain:

```
Source Content (article, newsletter, podcast)
    ↓
text-on-broll (this skill) → 3-4 vertical videos
    ↓
content-repurposer → platform captions for each video
    ↓
Post to IG Reels, TikTok, Shorts
```

**Related skills:**
- `video-generator` - B-roll generation (called by this skill)
- `video-caption-creation` - Hook frameworks (referenced by this skill)
- `nano-banana-image-generator` - Static thumbnail for the same content
- `content-repurposer` - Platform captions to pair with each video
- `one-liners` - Text pattern library
- `short-form-video` - Broader short-form strategy and philosophy

---

## Examples

### Example: Education Article Promotion

**Topic:** Article about standardized testing and creative agency

**B-roll prompt:** "Extreme close-up, shallow depth of field. A child's small paint-covered fingers slowly drag through thick finger paint across a standardized test bubble sheet. Paint smears vibrant orange and blue across neat rows of bubbles. The sound of wet paint dragging across paper. Photorealistic, handheld micro-movement, warm natural light."

**Text options selected:**
1. "Stop grading kids on how fast they fill in bubbles." (Stop + Complaint)
2. "Curiosity doesn't fit in a bubble." (Values)
3. "They said my kid can't think critically." → "She was finger painting while your kid was memorizing answers." (Two-Part Reveal)

**Result:** 3 vertical videos, same b-roll, different text - each targets a different scroll-stop trigger.
