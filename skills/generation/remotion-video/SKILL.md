---
name: remotion-video
description: Create programmatic videos using Remotion (React). This skill provides visual style guidelines, animation patterns, and workflow for creating explainer videos with a risograph aesthetic. Use when creating short-form video content for Skill Stack.
---

# Remotion Video Creator

Create programmatic videos using Remotion - React components that render to video. This skill encodes the Skill Stack visual style and lessons learned from building explainer content.

## Purpose

Build short-form video content (10-60 seconds) that explains Skill Stack concepts with a distinctive risograph-inspired aesthetic. Videos are code, so they're version-controlled, reproducible, and infinitely editable.

## When to Use This Skill

- Creating explainer videos for Skill Stack concepts
- Building animated social content (vertical 9:16, square 1:1, landscape 16:9)
- Visualizing technical workflows or progressive disclosure
- Any video where precise timing and typography matter

**Not for:**
- Live footage editing (use traditional video tools)
- Complex 3D graphics (Remotion is 2D-focused)
- Quick one-off graphics (use Figma or Canva)

---

## Project Setup

### Quick Start

```bash
# Create new Remotion project
npx create-video@latest my-video

# Install dependencies
cd my-video && npm install

# Add Google Fonts
npm install @remotion/google-fonts

# Start studio
npm run start  # Opens http://localhost:3000
```

### File Structure

```
my-video/
├── src/
│   ├── Root.tsx           # Composition definitions
│   ├── Main.tsx           # Main video component
│   └── components/        # Reusable elements
├── package.json
├── remotion.config.ts
└── out/                   # Rendered videos
```

### Composition Setup (Root.tsx)

Always create multiple aspect ratios for each video:

```tsx
import { Composition, Folder } from "remotion";
import { MyVideo } from "./MyVideo";

export const RemotionRoot = () => (
  <>
    <Folder name="MyVideo">
      <Composition
        id="MyVideo-Vertical"
        component={MyVideo}
        durationInFrames={600}  // 20 seconds at 30fps
        fps={30}
        width={1080}
        height={1920}  // 9:16
      />
      <Composition
        id="MyVideo-Square"
        component={MyVideo}
        durationInFrames={600}
        fps={30}
        width={1080}
        height={1080}  // 1:1
      />
      <Composition
        id="MyVideo-Landscape"
        component={MyVideo}
        durationInFrames={600}
        fps={30}
        width={1920}
        height={1080}  // 16:9
      />
    </Folder>
  </>
);
```

---

## Visual Style: Skill Stack Risograph

### Color Palette

```tsx
const C = {
  paper: "#FAF8F5",    // Warm off-white background
  coral: "#D4694A",    // Accent, CTAs, highlights
  teal: "#1E4D4D",     // Headers, selected states
  ink: "#1C1C1C",      // Body text
  muted: "#666666",    // Secondary text
  dimmed: "#AAAAAA",   // Tertiary, disabled
  white: "#FFFFFF",    // Cards, containers
};
```

### Typography

```tsx
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadPlayfair } from "@remotion/google-fonts/PlayfairDisplay";
import { loadFont as loadJetBrains } from "@remotion/google-fonts/JetBrainsMono";

// Body text, UI labels
const { fontFamily: inter } = loadInter("normal", {
  weights: ["400", "500", "600"],
  subsets: ["latin"],
});

// Headlines, quotes, emotional text
const { fontFamily: playfair } = loadPlayfair("normal", {
  weights: ["400", "500", "600", "700"],
  subsets: ["latin"],
});

// Code, technical content, skill names
const { fontFamily: mono } = loadJetBrains("normal", {
  weights: ["400", "500"],
  subsets: ["latin"],
});
```

### Font Size Guidelines

**Minimum readable sizes for video:**

| Element | Square (1080) | Vertical (1080w) | Landscape (1920w) |
|---------|---------------|------------------|-------------------|
| Headlines | 64-84px | 64-84px | 72-96px |
| Skill names | 36-40px | 36-40px | 40-48px |
| Body text | 28-32px | 28-32px | 32-36px |
| Labels | 24-28px | 24-28px | 28-32px |
| Annotation | 22-24px | 22-24px | 24-28px |

**Key lesson:** Always larger than you think. Video compresses detail.

### Grain Overlay

```tsx
const GrainOverlay: React.FC = () => {
  const frame = useCurrentFrame();

  return (
    <AbsoluteFill
      style={{
        pointerEvents: "none",
        opacity: 0.04,
        mixBlendMode: "multiply",
      }}
    >
      <svg width="100%" height="100%">
        <defs>
          <filter id="grain">
            <feTurbulence
              type="fractalNoise"
              baseFrequency="0.8"
              numOctaves="4"
              seed={Math.floor(frame / 4)}  // Animate grain
            />
          </filter>
        </defs>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};
```

---

## Animation Patterns

### Core Tools

```tsx
import {
  useCurrentFrame,
  useVideoConfig,
  AbsoluteFill,
  interpolate,
  spring,
  Sequence,
} from "remotion";
```

### Fade In/Out

```tsx
const fadeIn = interpolate(frame, [0, 30], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

const fadeOut = interpolate(frame, [150, 180], [1, 0], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

// Combine for scene opacity
<div style={{ opacity: fadeIn * fadeOut }}>
```

### Spring Animations

```tsx
const { fps } = useVideoConfig();

// Smooth entrance
const entrance = spring({
  frame: frame - 20,  // Delay by 20 frames
  fps,
  config: { damping: 100 },  // Smooth, no bounce
});

// Bouncy selection
const selectPulse = spring({
  frame: frame - 15,
  fps,
  config: { damping: 12, stiffness: 100 },  // Bouncy
});

// Apply to transform
<div style={{
  opacity: interpolate(entrance, [0, 1], [0, 1]),
  transform: `translateY(${interpolate(entrance, [0, 1], [20, 0])}px)`,
}}>
```

### Typewriter Effect

```tsx
const ScenePrompt: React.FC<{ frame: number }> = ({ frame }) => {
  const text = "Your prompt text here";
  const charsToShow = Math.floor(frame / 2);  // 15 chars/sec at 30fps
  const visibleText = text.slice(0, charsToShow);
  const isTyping = charsToShow < text.length;
  const cursorBlink = Math.floor(frame / 18) % 2 === 0;

  return (
    <div>
      "{visibleText}
      {(isTyping || cursorBlink) && (
        <span style={{
          backgroundColor: C.coral,
          marginLeft: 4,
          opacity: cursorBlink ? 1 : 0,
        }}>
          {"\u00A0"}
        </span>
      )}
      {!isTyping && '"'}
    </div>
  );
};
```

### Staggered List Animation

```tsx
const ITEMS = ["item-1", "item-2", "item-3"];

{ITEMS.map((item, i) => {
  const delay = i * 25;  // 25 frames between each
  const s = spring({
    frame: Math.max(0, frame - delay - 20),
    fps,
    config: { damping: 100 },
  });

  return (
    <div
      key={item}
      style={{
        opacity: interpolate(s, [0, 1], [0, 1]),
        transform: `translateY(${interpolate(s, [0, 1], [20, 0])}px)`,
      }}
    >
      {item}
    </div>
  );
})}
```

---

## Scene Timing Guidelines

### Duration Math

- **30 fps** = 30 frames per second
- **10 seconds** = 300 frames
- **20 seconds** = 600 frames

### Pacing Lessons Learned

**Too fast is the #1 mistake.** Viewers need time to:
1. Notice a scene change
2. Read text
3. Process meaning
4. Prepare for next change

**Minimum scene durations:**

| Scene Type | Minimum | Comfortable |
|------------|---------|-------------|
| Typewriter text | 3-4 sec | 5-6 sec |
| List appearing | 4-5 sec | 6-8 sec |
| Selection/highlight | 3-4 sec | 5 sec |
| Technical diagram | 4-5 sec | 6-8 sec |
| Punchline/CTA | 2-3 sec | 3-4 sec |

### Scene Overlap Pattern

Scenes should cross-fade, not hard cut:

```tsx
// Scene timing for 20-second video (600 frames)
{frame < 200 && <ScenePrompt frame={frame} />}
{frame >= 160 && frame < 340 && <SceneScan frame={frame - 160} />}
{frame >= 300 && frame < 460 && <SceneSelect frame={frame - 300} />}
{frame >= 420 && frame < 560 && <SceneLoad frame={frame - 420} />}
{frame >= 520 && <ScenePunchline frame={frame - 520} />}
```

The 40-frame overlap (1.3 seconds) creates smooth cross-fades when combined with fadeIn/fadeOut interpolations.

---

## Workflow

### Phase 1: Storyboard

Before coding, define:

1. **Core message** - What's the one thing viewers should learn?
2. **Scene breakdown** - 4-6 scenes, each with one idea
3. **Total duration** - 10-20 seconds for social, 30-60 for explainers
4. **Text content** - Exact words for each scene

### Phase 2: Scaffold

1. Create composition with proper duration
2. Build scene components with placeholder content
3. Set up basic timing (scene ranges)
4. Test that all scenes appear

### Phase 3: Style

1. Apply color palette and fonts
2. Add grain overlay
3. Ensure font sizes are readable
4. Test on phone (vertical) and desktop (landscape)

### Phase 4: Animate

1. Add fadeIn/fadeOut to each scene
2. Add spring animations for entrances
3. Fine-tune timing - almost always needs to be slower
4. Test full playback multiple times

### Phase 5: Render

```bash
# Render specific composition
npx remotion render MyVideo-Square out/square.mp4

# Render all formats
npx remotion render MyVideo-Vertical out/vertical.mp4
npx remotion render MyVideo-Square out/square.mp4
npx remotion render MyVideo-Landscape out/landscape.mp4
```

---

## Common Mistakes

### ❌ Centering Issues

**Problem:** Content appears in top-left corner.

**Fix:** Use AbsoluteFill with flexbox, not position: absolute.

```tsx
// ✅ Correct
<AbsoluteFill style={{
  justifyContent: "center",
  alignItems: "center",
}}>

// ❌ Wrong
<div style={{ position: "absolute", left: "50%", top: "50%" }}>
```

### ❌ Tiny Fonts

**Problem:** Text readable in studio, illegible on phone.

**Fix:** Minimum 28px for body text, 64px for headlines.

### ❌ Too Fast

**Problem:** Can't read text before it disappears.

**Fix:** Double your initial duration estimate. Each scene needs 4-8 seconds minimum.

### ❌ Hard Cuts

**Problem:** Jarring transitions between scenes.

**Fix:** Overlap scenes by 30-50 frames with fadeIn/fadeOut.

### ❌ No Aspect Ratio Support

**Problem:** Video looks wrong on different platforms.

**Fix:** Create all three compositions (vertical, square, landscape) from the start.

---

## Caption Integration

Remotion has first-class caption support. Three options by cost:

### Option 1: Native Whisper (Recommended - Free)

```bash
npm install @remotion/captions @remotion/install-whisper-cpp
npx @remotion/install-whisper-cpp --model large-v3-turbo
```

```tsx
import { transcribe } from "@remotion/captions";

const result = await transcribe({
  inputPath: "/path/to/audio.mp3",
  model: "large-v3-turbo",
  language: "en",
});
// result.captions = [{ text: "Hello", startTime: 0, endTime: 0.5 }, ...]
```

### Option 2: ZapCap API ($0.10/min)
For batch processing without local model setup.

### Option 3: Submagic API ($0.69/min)
Pre-styled "viral" caption templates, but expensive.

**Full workflow details:** See `references/caption-workflow.md`

---

## Community Resources

### Discord
[Remotion Discord](https://remotion.dev/discord) - 6,000+ members. Active #help and #showcase channels. Creator (Jonny Burger) responds directly.

### Key Templates to Study

| Template | Use Case | Link |
|----------|----------|------|
| TikTok | Vertical social video | [remotion-dev/template-tiktok](https://github.com/remotion-dev/template-tiktok) |
| Audiogram | Podcast clips | [remotion-dev/template-audiogram](https://github.com/remotion-dev/template-audiogram) |
| GitHub Unwrapped | Data-driven video | [remotion-dev/github-unwrapped](https://github.com/remotion-dev/github-unwrapped) |
| claude-remotion-kickstart | AI-assisted workflow | Community starter for Claude + Remotion |

### Essential Packages

```bash
# Captions
npm install @remotion/captions @remotion/install-whisper-cpp

# Graphics
npm install @remotion/skia  # 2D vector graphics
npm install @remotion/three # 3D with Three.js
npm install @remotion/lottie # Lottie animations

# Rendering
npm install @remotion/lambda  # AWS serverless rendering
npm install @remotion/player  # Embed in web apps
```

**Full resource list:** See `references/community-resources.md`

---

## Bundled Resources

- `references/what-is-a-skill.tsx` - Full example component from "What Is A Skill" video
- `references/caption-workflow.md` - Complete caption integration guide (Whisper, ZapCap, Submagic)
- `references/community-resources.md` - Templates, packages, learning path

---

## Related Skills

- **video-caption-creation** - Captions and hashtags for the rendered video
- **youtube-scriptwriting** - For longer explainer video scripts
- **social-content-creation** - Repurpose video concepts to static posts

---

## Version History

- **v1.1** (2026-01-22): Caption & community integration
  - Added native Whisper caption workflow via `@remotion/captions`
  - Added caption style presets (minimal, bold, karaoke, brand)
  - Added community resources (Discord, templates, packages)
  - New reference files: `caption-workflow.md`, `community-resources.md`
  - Cost comparison: Whisper (free) vs ZapCap ($0.10/min) vs Submagic ($0.69/min)

- **v1.0** (2026-01-21): Initial skill creation
  - Risograph visual style
  - Animation patterns (spring, interpolate, typewriter)
  - Timing guidelines (learned from "too fast" iteration)
  - Scene overlap pattern

---

*Videos are code. Version control them, iterate on them, and build a library of reusable components.*
