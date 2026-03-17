---
description: Create programmatic videos with Remotion (React components rendered to MP4). Use when creating animated presentations, product demos, marketing videos, code-generated video, Remotion project, animated explainer.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
context: fork
---

# Remotion - Programmatic Video from React

Create videos entirely in React using Remotion. Each frame is a React component. Write code, render to MP4. No AI model needed - pure programmatic control over every pixel and frame.

## When to Use Remotion vs AI Video

| Use Case | Tool |
|----------|------|
| Precise animations, branded content, data visualizations | **Remotion** (this skill) |
| Creative/artistic video from text description | `/sw-media:video` (AI models) |
| Product demos, marketing, changelogs | **Remotion** |
| Realistic footage, scenes, landscapes | `/sw-media:video` |

## Workflow

### Step 1: Check if Remotion Project Exists

```bash
# Check for existing Remotion setup
if [ -f "package.json" ] && grep -q '"remotion"' package.json 2>/dev/null; then
  echo "Remotion project detected"
else
  echo "No Remotion project found - will scaffold one"
fi
```

### Step 2: Scaffold Project (If Needed)

If no Remotion project exists, scaffold one:

```bash
npx create-video@latest my-video --template blank
cd my-video
npm install
```

Or add Remotion to an existing project:

```bash
npm install remotion @remotion/cli @remotion/bundler
```

### Step 3: Create Video Composition

Create a React component that defines the video. Key Remotion APIs:

```tsx
import { useCurrentFrame, useVideoConfig, interpolate, spring, Sequence } from 'remotion';

export const MyComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width, height } = useVideoConfig();

  // Animate opacity from 0 to 1 over first 30 frames
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: 'clamp',
  });

  // Spring animation
  const scale = spring({ frame, fps, config: { damping: 100 } });

  return (
    <div style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <h1 style={{ opacity, transform: `scale(${scale})`, fontSize: 80 }}>
        Hello World
      </h1>
    </div>
  );
};
```

Register the composition in `src/Root.tsx`:

```tsx
import { Composition } from 'remotion';
import { MyComposition } from './MyComposition';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="MyVideo"
      component={MyComposition}
      durationInFrames={150}  // 5 seconds at 30fps
      fps={30}
      width={1920}
      height={1080}
    />
  );
};
```

### Step 4: Preview (Optional)

```bash
npx remotion studio
# Opens browser at http://localhost:3000 with preview player
```

### Step 5: Render to MP4

```bash
npx remotion render src/index.ts MyVideo out/video.mp4
```

Additional render options:
```bash
# Custom resolution
npx remotion render src/index.ts MyVideo out/video.mp4 --width 1920 --height 1080

# Lower quality for faster rendering
npx remotion render src/index.ts MyVideo out/video.mp4 --quality 80

# Specific frame range
npx remotion render src/index.ts MyVideo out/video.mp4 --frames 0-90

# GIF output
npx remotion render src/index.ts MyVideo out/animation.gif

# PNG sequence
npx remotion render src/index.ts MyVideo out/frames --image-format png
```

### Step 6: Verify Output

```bash
FILE="out/video.mp4"
if [ -f "$FILE" ] && [ -s "$FILE" ]; then
  file "$FILE"
  SIZE=$(du -h "$FILE" | cut -f1)
  echo "Video rendered successfully: $FILE ($SIZE)"
else
  echo "ERROR: Render failed - check console output for errors"
fi
```

## Common Animation Patterns

### Fade In/Out
```tsx
const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
```

### Slide In
```tsx
const translateX = interpolate(frame, [0, 30], [-100, 0], { extrapolateRight: 'clamp' });
```

### Spring Physics
```tsx
const scale = spring({ frame, fps, config: { damping: 10, stiffness: 100 } });
```

### Sequences (Staggered Timing)
```tsx
<Sequence from={0} durationInFrames={60}>
  <Title text="Part 1" />
</Sequence>
<Sequence from={60} durationInFrames={60}>
  <Title text="Part 2" />
</Sequence>
```

### Data-Driven Video
```tsx
// Pass data as props to composition
const data = [
  { label: 'Jan', value: 42 },
  { label: 'Feb', value: 78 },
  { label: 'Mar', value: 95 },
];

// Animate bar chart based on frame
const progress = interpolate(frame, [0, 60], [0, 1], { extrapolateRight: 'clamp' });
```

## Prerequisites Check

Before scaffolding or rendering, verify:

```bash
# Node.js required (v18+)
node --version

# Chrome/Chromium required for rendering
if command -v google-chrome >/dev/null 2>&1; then
  echo "Chrome found"
elif command -v chromium >/dev/null 2>&1; then
  echo "Chromium found"
elif [ -d "/Applications/Google Chrome.app" ]; then
  echo "Chrome found (macOS)"
else
  echo "WARNING: Chrome/Chromium not found - rendering may fail"
  echo "Install: brew install --cask google-chrome (macOS)"
fi
```

## Error Handling

| Error | Action |
|-------|--------|
| Node.js not installed | Tell user to install Node.js 18+ |
| Chrome not found | Suggest `brew install --cask google-chrome` (macOS) or `apt install chromium` (Linux) |
| `npx create-video` fails | Try `npm create video@latest` or check npm registry |
| Render fails with memory error | Reduce resolution or use `--concurrency 1` |
| TypeScript errors | Check composition imports and prop types |

## Remotion Agent Skills (Advanced)

Remotion provides official Claude Code skills for advanced usage:

```bash
# Install Remotion's official agent skills (optional)
npx skills add remotion-dev/skills
```

This adds deeper Remotion knowledge to the AI assistant including animation best practices, performance optimization, and advanced composition patterns.

## Activation Keywords

Remotion, programmatic video, React video, code video, animated presentation, product demo video, marketing video, video from code, render video, create animation from code
