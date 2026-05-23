---
name: Remotion Video Styling
description: Inline React styling for Remotion video components using theme constants. Use this when styling video compositions, positioning elements on the 1080x1920 canvas, or applying colors/fonts from src/lib/theme.ts. No external CSS files - all styles are inline objects.
---

# Remotion Video Styling

This Skill provides Claude Code with specific guidance on how it should handle styling in Remotion video compositions.

## When to use this skill:

- Styling any video composition or component
- Positioning elements on the 1080x1920 canvas
- Applying colors, fonts, or spacing from theme.ts
- Creating layout structures with absolute positioning
- Implementing responsive sizing using VIDEO_CONFIG
- Defining inline style objects for React components

## Instructions

- **Inline Styles**: Remotion uses React inline styles; define styles as objects with camelCase properties
- **Design Tokens**: Use theme constants from `src/lib/theme.ts` for colors, fonts, and spacing
- **Absolute Positioning**: Video elements use absolute positioning for precise layout control
- **Video Dimensions**: All layouts designed for 1080x1920 (9:16 portrait) from `VIDEO_CONFIG`
- **Typography**: Use system fonts or included fonts (Noto Color Emoji); specify in theme.ts
- **No CSS Files**: Remotion compositions don't use external CSS files; all styles are inline React styles

**Examples:**
```typescript
// Good: Theme constants, inline styles, absolute positioning
import { theme, VIDEO_CONFIG } from '@/lib/theme';

export const BookCover: React.FC = () => (
  <div style={{
    position: 'absolute',
    top: VIDEO_CONFIG.height * 0.2,
    left: VIDEO_CONFIG.width * 0.1,
    width: VIDEO_CONFIG.width * 0.8,
    backgroundColor: theme.colors.background,
    fontFamily: theme.fonts.primary,
    fontSize: 48,
    color: theme.colors.text,
  }}>
    Book Title
  </div>
);

// Bad: CSS classes, relative positioning, hardcoded values
<div className="book-cover" style={{ fontSize: '48px' }}>
  Book Title
</div>
```
