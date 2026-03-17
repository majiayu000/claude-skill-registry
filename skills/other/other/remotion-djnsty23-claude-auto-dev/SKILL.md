---
name: remotion
description: Best practices for Remotion - video creation in React. Use when working with video compositions, animations, or subtitles.
user-invocable: true
triggers:
  - remotion
  - video
  - animation
  - subtitle
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
model: opus
---

# Remotion Best Practices

Video creation in React using Remotion.

## When to Use

- Creating video compositions
- Adding animations to video
- Working with subtitles/captions
- Embedding media (videos, images, audio)
- Sequencing and timing

## Core Concepts

### Compositions
Define video dimensions, duration, and frame rate:
```tsx
import { Composition } from 'remotion';

<Composition
  id="MyVideo"
  component={MyComponent}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
/>
```

### Animation with useCurrentFrame
```tsx
import { useCurrentFrame, interpolate } from 'remotion';

const MyComponent = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1]);

  return <div style={{ opacity }}>Hello</div>;
};
```

### Sequencing
```tsx
import { Sequence } from 'remotion';

<Sequence from={0} durationInFrames={60}>
  <Scene1 />
</Sequence>
<Sequence from={60} durationInFrames={60}>
  <Scene2 />
</Sequence>
```

## Detailed Rules

Load specific rules for detailed guidance:

| Rule | When to Load |
|------|--------------|
| `rules/animations.md` | Fundamental animation patterns |
| `rules/compositions.md` | Defining compositions, stills, folders |
| `rules/subtitles.md` | Captions and subtitle rendering |
| `rules/timing.md` | Interpolation, easing, springs |
| `rules/videos.md` | Embedding videos - trim, volume, speed |

## Quick Reference

### Interpolation
```tsx
// Linear interpolation
const value = interpolate(frame, [0, 100], [0, 1]);

// With easing
const value = interpolate(frame, [0, 100], [0, 1], {
  easing: Easing.bezier(0.25, 0.1, 0.25, 1),
});

// Clamped (default extrapolateLeft/Right: 'clamp')
const value = interpolate(frame, [0, 100], [0, 1], {
  extrapolateLeft: 'clamp',
  extrapolateRight: 'clamp',
});
```

### Spring Animation
```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const { fps } = useVideoConfig();
const scale = spring({
  frame,
  fps,
  config: { damping: 200 },
});
```

### Media
```tsx
import { Video, Audio, Img, staticFile } from 'remotion';

// Local file
<Video src={staticFile('video.mp4')} />

// With controls
<Video
  src={src}
  volume={0.5}
  startFrom={30}
  endAt={120}
/>
```

## Integration Notes

- Works with React 18+
- Use `staticFile()` for assets in `/public`
- Frame-based timing (not time-based)
- SSR-compatible components

Source: [remotion-dev/skills](https://github.com/remotion-dev/skills)
