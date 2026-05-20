---
name: remotion-best-practices
description: Generate Remotion video compositions with React. Use when creating videos, animations, property showcases, or any video rendering task. Provides frame-based animation patterns, composition setup, and Remotion-specific APIs.
allowed-tools: Read, Grep, Glob, Bash(npm:*, npx:remotion*)
---

# Remotion Video Generation

## Core Principles
1. ALL animations use `useCurrentFrame()` - NEVER CSS transitions
2. Use `staticFile()` for local assets in /public
3. Always clamp interpolations with `extrapolateRight: 'clamp'`
4. Premount sequences with `premountFor` prop for smooth transitions
5. Use `delayRender()` and `continueRender()` for async data

## Quick Reference

### Animation Pattern
```tsx
import { useCurrentFrame, interpolate } from 'remotion';

const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], {
  extrapolateRight: 'clamp',
});
const scale = interpolate(frame, [0, 30], [0.8, 1], {
  extrapolateRight: 'clamp',
  easing: Easing.out(Easing.cubic),
});
```

### Composition Setup
```tsx
import { Composition } from 'remotion';

<Composition
  id="PropertyVideo"
  component={PropertyShowcase}
  durationInFrames={300}
  fps={30}
  width={1920}
  height={1080}
  schema={PropertySchema}
  defaultProps={{ ... }}
/>
```

### Sequence Pattern
```tsx
<Sequence from={0} durationInFrames={90}>
  <Scene1 />
</Sequence>
<Sequence from={90} durationInFrames={90}>
  <Scene2 />
</Sequence>
```

## Detailed Rules
- **Animations**: See [rules/animations.md](rules/animations.md)
- **Compositions**: See [rules/compositions.md](rules/compositions.md)
- **Timing**: See [rules/timing.md](rules/timing.md)
- **Assets**: See [rules/assets.md](rules/assets.md)
- **Transitions**: See [rules/transitions.md](rules/transitions.md)
- **Captions**: See [rules/captions.md](rules/captions.md)

## Common Patterns

### Spring Animation
```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

const { fps } = useVideoConfig();
const scale = spring({
  fps,
  frame,
  config: { damping: 200 },
});
```

### Loading External Assets
```tsx
import { delayRender, continueRender, staticFile } from 'remotion';

const [handle] = useState(() => delayRender());
useEffect(() => {
  loadAsset().then(() => continueRender(handle));
}, []);
```

### Audio Sync
```tsx
import { Audio, Sequence } from 'remotion';

<Audio src={voiceoverUrl} volume={1} />
<Sequence from={30}> {/* Start after 1 second */}
  <AnimatedText />
</Sequence>
```
