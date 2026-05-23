---
name: Global Coding Style
description: TypeScript and Remotion-specific coding style conventions for naming, formatting, and organization. Use this when writing any TypeScript code, creating new files, naming variables/functions/types, or structuring imports. Enforces frame-based timing and path alias usage.
---

# Global Coding Style

This Skill provides Claude Code with specific guidance on how it should handle global coding style.

## When to use this skill:

- Writing or editing any .ts or .tsx files
- Creating new functions, variables, or type definitions
- Naming components, interfaces, or constants
- Organizing imports and file structure
- Defining animation timing or duration values
- Refactoring code for consistency

## Instructions

- **TypeScript Naming**: Use camelCase for variables/functions (`getUserData`, `frameCount`), PascalCase for types/interfaces/components (`MonthlyRecap`, `RecapBook`), UPPER_SNAKE_CASE for constants (`VIDEO_CONFIG`, `FRAME_RATE`)
- **Automated Formatting**: Use ESLint with TypeScript rules; 2-space indentation for .ts/.tsx files
- **Path Aliases**: Use `@/` prefix for imports from `src/` (e.g., `import { theme } from '@/lib/theme'`)
- **Meaningful Names**: Choose descriptive names that reveal intent; avoid abbreviations except for standard video terms (fps, codec, ssr)
- **Small, Focused Functions**: Keep functions small and focused; Remotion compositions should be modular sequences
- **Frame-Based Timing**: Always use frame numbers, not milliseconds (e.g., `duration: 150` not `duration: 5000`)
- **Remove Dead Code**: Delete unused code, commented-out blocks, and imports rather than leaving them as clutter
- **Backward compatibility only when required:** Unless specifically instructed otherwise, assume you do not need to write additional code logic to handle backward compatibility
- **DRY Principle**: Extract reusable animations to `src/lib/animations.ts`, reusable components to `src/components/`

**Examples:**
```typescript
// Good: Frame-based, clear naming, path alias
import { fadeIn } from '@/lib/animations';
const INTRO_DURATION = 75; // frames at 30fps
export const IntroSequence: React.FC<{ startFrame: number }> = ({ startFrame }) => {
  const opacity = fadeIn(frame, startFrame, 15);
  return <div style={{ opacity }}>...</div>;
};

// Bad: Milliseconds, unclear naming, relative import
import { fadeIn } from '../../lib/animations';
const dur = 2500; // ms
export const intro = ({ start }) => {
  const o = fadeIn(frame, start, 500);
  return <div style={{ opacity: o }}>...</div>;
};
```
