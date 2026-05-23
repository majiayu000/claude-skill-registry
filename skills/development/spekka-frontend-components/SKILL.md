---
name: Remotion Video Components
description: React component patterns for Remotion video compositions using frame-based rendering. Use this when creating or modifying video sequence components in src/compositions/, src/components/, or any .tsx file that renders video content. Applies functional, purely frame-driven component design.
---

# Remotion Video Components

This Skill provides Claude Code with specific guidance on how it should handle frontend components.

## When to use this skill:

- Creating new video sequence components (IntroSequence, BookReveal, etc.)
- Building reusable video components in src/components/
- Modifying existing Remotion composition files in src/compositions/
- Implementing frame-based animations with useCurrentFrame
- Composing complex video sequences from smaller components
- Refactoring video components for reusability

## Instructions

- **Remotion Components**: All video components use Remotion's React-based API with `useCurrentFrame()` and `useVideoConfig()`
- **Single Responsibility**: Each sequence component handles one video segment (IntroSequence, BookReveal, StatsReveal, etc.)
- **Frame-Based Timing**: Components receive `startFrame` prop for timing calculations, not time-based values
- **TypeScript Props**: Define explicit prop interfaces for all components with strong typing
- **Reusable Animations**: Extract common animations to `src/lib/animations.ts` (fadeIn, slideIn, scaleIn, etc.)
- **Composition Pattern**: Combine sequence components in `src/compositions/MonthlyRecap/index.tsx`
- **No Runtime State**: Remotion compositions should be purely functional based on frame number, avoid useState
- **Path Aliases**: Use `@/` for imports (e.g., `import { KineticText } from '@/components/KineticText'`)

**Examples:**
```typescript
// Good: Clear props, frame-based, functional
import { useCurrentFrame } from 'remotion';
import { fadeIn } from '@/lib/animations';

interface IntroSequenceProps {
  startFrame: number;
  title: string;
}

export const IntroSequence: React.FC<IntroSequenceProps> = ({ startFrame, title }) => {
  const frame = useCurrentFrame();
  const opacity = fadeIn(frame, startFrame, 15);

  return (
    <div style={{ opacity }}>
      <h1>{title}</h1>
    </div>
  );
};

// Bad: Time-based, stateful, unclear props
export const Intro = ({ start, data }) => {
  const [visible, setVisible] = useState(false);
  return <div>{data.title}</div>;
};
```
