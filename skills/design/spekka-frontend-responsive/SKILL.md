---
name: Fixed Video Format (9:16)
description: Fixed 1080x1920 pixel video format with percentage-based positioning. Use this when laying out video compositions, positioning elements on the canvas, or calculating dimensions. All videos render at exactly 9:16 aspect ratio for TikTok/Instagram Reels.
---

# Fixed Video Format (9:16)

This Skill provides Claude Code with specific guidance on how it should handle the fixed 9:16 video format.

## When to use this skill:

- Positioning elements in any video composition
- Calculating element dimensions and coordinates
- Using VIDEO_CONFIG.width and VIDEO_CONFIG.height
- Defining safe zones for platform UI overlays
- Creating layouts optimized for vertical viewing
- Testing compositions in Remotion Studio preview

## Instructions

- **Fixed Dimensions**: All videos render at exactly 1080x1920 pixels (9:16 portrait); no responsive design needed
- **VIDEO_CONFIG Constants**: Use `VIDEO_CONFIG` from `src/lib/theme.ts` for width/height values
- **Percentage-Based Layout**: Position elements using percentages of VIDEO_CONFIG dimensions for maintainability
- **TikTok Optimization**: Format optimized for TikTok/Instagram Reels vertical viewing
- **Safe Zones**: Keep important content within central 90% to account for platform UI overlays
- **Consistent Aspect Ratio**: All compositions must maintain 9:16 aspect ratio; test in Remotion Studio preview

**Examples:**
```typescript
// Good: Use VIDEO_CONFIG, percentage-based positioning
import { VIDEO_CONFIG } from '@/lib/theme';

export const BookCover: React.FC = () => (
  <img
    src={coverUrl}
    style={{
      position: 'absolute',
      top: VIDEO_CONFIG.height * 0.15, // 15% from top
      left: VIDEO_CONFIG.width * 0.1,  // 10% from left
      width: VIDEO_CONFIG.width * 0.8,  // 80% width
      height: VIDEO_CONFIG.width * 0.8 * 1.5, // Maintain book aspect ratio
    }}
  />
);

// Bad: Hardcoded pixels, no VIDEO_CONFIG reference
<img
  style={{
    position: 'absolute',
    top: 300,
    left: 100,
    width: 800,
  }}
/>
```
