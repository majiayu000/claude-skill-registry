---
name: Video Content Accessibility
description: Accessibility guidelines for video content including contrast, timing, and readable typography. Use this when designing video layouts, choosing colors/fonts, setting animation durations, or ensuring emoji and visual elements are accompanied by text alternatives.
---

# Video Content Accessibility

This Skill provides Claude Code with specific guidance on how it should handle accessibility in Remotion video compositions.

## When to use this skill:

- Designing video composition layouts and color schemes
- Choosing text sizes and font weights for readability
- Setting animation timing and transition durations
- Using emojis or visual indicators in video content
- Ensuring information hierarchy through visual design
- Testing color contrast in theme.ts color choices

## Instructions

- **Color Contrast**: Maintain high contrast ratios (4.5:1 minimum) for text on backgrounds; test with various backgrounds
- **Readable Typography**: Use large, clear fonts; minimum 48px for body text in 1080x1920 format
- **Text Alternatives**: Ensure all information conveyed visually has text equivalents (e.g., star ratings + numeric score)
- **Animation Timing**: Provide sufficient time for text to be read; minimum 3 seconds for short text
- **Emoji Accessibility**: Use Noto Color Emoji font for consistent emoji rendering; always pair with text labels
- **Motion Sensitivity**: Avoid jarring transitions; use smooth easing functions from `src/lib/animations.ts`
- **Information Hierarchy**: Use size, color, and position to create clear visual hierarchy

**Examples:**
```typescript
// Good: High contrast, large text, sufficient timing, text + visual
import { theme } from '@/lib/theme';

export const BookRating: React.FC<{ rating: number }> = ({ rating }) => (
  <div style={{
    backgroundColor: theme.colors.background, // Dark
    color: theme.colors.text, // Light - high contrast
    fontSize: 64, // Large and readable
    padding: 40,
  }}>
    <div>⭐ {rating.toFixed(1)}</div> {/* Emoji + numeric */}
  </div>
);

// Bad: Low contrast, small text, emoji only
<div style={{ color: '#666', fontSize: 24 }}>
  ⭐⭐⭐⭐
</div>
```
