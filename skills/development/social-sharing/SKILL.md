---
name: social-sharing
description: Social sharing patterns for StepLeague - OG image generation, share hooks, WhatsApp optimization, and shareable URLs. Use when implementing sharing features, generating OG images, creating share modals, or working with social platform integrations. Keywords: share, OG image, Open Graph, WhatsApp, social, sharing, useShare, share card, metric.
compatibility: Antigravity, Claude Code, Cursor
metadata:
  version: "1.0"
  project: "stepleague"
  last_updated: "2026-01-26"
---

# Social Sharing Skill

## Overview

This skill documents patterns for social sharing in StepLeague, including:
- OG (Open Graph) image generation with Vercel OG
- The `useShare` hook for multi-platform sharing
- WhatsApp-specific optimizations
- Shareable URL structures
- Share analytics tracking
- Modular MetricConfig system for future metrics (PRD-48)

---

## Critical Rules

### 1. Always Use the `useShare` Hook

Never call sharing APIs directly. Always use the `useShare` hook which:
- Handles all platforms (native, WhatsApp, X, copy)
- Tracks analytics automatically
- Provides consistent UX

```typescript
// ✅ CORRECT
import { useShare } from "@/hooks/useShare";

const { share, isSharing, copied, supportsNativeShare } = useShare({
  contentType: 'achievement',
  itemId: cardId,
});

await share({
  title: "My Achievement",
  text: "I walked 12,345 steps today!",
  url: shareUrl,
}, 'whatsapp');

// ❌ WRONG - Direct platform calls
window.open(`https://wa.me/?text=${message}`, '_blank');
```

### 2. OG Images Must Be 1200x630px

All OG images must follow platform standards:
- **Size:** 1200x630 pixels (1.91:1 aspect ratio)
- **File size:** <300KB for fast loading
- **Text coverage:** <20-25% of image
- **Format:** PNG or JPG (no transparency/animation)

### 3. Use MetricConfig for Metric Display

Never hardcode metric types. Use the MetricConfig system for extensibility:

```typescript
// ✅ CORRECT - Config-driven
import { METRIC_CONFIGS, MetricType } from "@/lib/sharing/metricConfig";

const config = METRIC_CONFIGS[metricType];
const display = `${config.formatValue(value)} ${config.unit}`;

// ❌ WRONG - Hardcoded
const display = `${value.toLocaleString()} steps`;
```

### 4. WhatsApp Messages Must Be Concise

Research shows concise messages work best in fitness WhatsApp groups:
- **Max 100 characters** before the URL
- **Include hashtag** for discoverability (#StepLeague)
- **One clear CTA** or achievement

```typescript
// ✅ CORRECT - Concise
"Just hit 12,345 steps today! 🚶 #StepLeague"

// ❌ WRONG - Too long
"Hey everyone! I wanted to share that I walked 12,345 steps today which is amazing because last week I only did 10,000..."
```

---

## OG Image Generation

### File Location

OG image API: `src/app/api/og/route.tsx`

### Using Vercel OG (ImageResponse)

```typescript
import { ImageResponse } from "next/og";
import { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  const { searchParams } = request.nextUrl;

  const metricType = searchParams.get("metric_type") || "steps";
  const value = parseInt(searchParams.get("value") || "0");
  const name = searchParams.get("name") || "Player";
  // ... more params

  return new ImageResponse(
    (
      <div style={{
        height: "100%",
        width: "100%",
        display: "flex",
        // ... styling
      }}>
        {/* Card content */}
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
```

### OG API Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `metric_type` | string | Yes | steps, calories, slp, distance, etc. |
| `value` | number | Yes | The metric value |
| `name` | string | Yes | User's display name |
| `rank` | number | No | League rank (1-based) |
| `period` | string | No | "Today", "This Week", "Jan 1-7" |
| `improvement` | number | No | Improvement percentage |
| `league` | string | No | League name |
| `emoji` | string | No | Override default emoji |
| `theme` | string | No | "dark" or "light" |

### Example URL

```
/api/og?metric_type=steps&value=12345&name=John&rank=3&period=This%20Week&improvement=15&league=Team%20Alpha
```

---

## MetricConfig System

### Type Definition

**File:** `src/lib/sharing/metricConfig.ts`

```typescript
export type MetricType =
  | 'steps'
  | 'calories'
  | 'slp'
  | 'distance'
  | 'swimming'
  | 'cycling'
  | 'running';

export interface MetricConfig {
  type: MetricType;
  displayName: string;      // "Steps", "Calories", "SLP"
  unit: string;             // "steps", "kcal", "SLP", "km"
  emoji: string;            // "🚶", "🔥", "⚡", "🚴"
  gradient: string;         // Tailwind gradient classes
  formatValue: (value: number) => string;
}

export const METRIC_CONFIGS: Record<MetricType, MetricConfig> = {
  steps: {
    type: 'steps',
    displayName: 'Steps',
    unit: 'steps',
    emoji: '🚶',
    gradient: 'from-sky-500 to-emerald-500',
    formatValue: (v) => v.toLocaleString(),
  },
  // Future metrics added here (PRD-48)
};
```

### Usage Pattern

```typescript
function ShareCard({ metricType, value }: Props) {
  const config = METRIC_CONFIGS[metricType];

  return (
    <div className={`bg-gradient-to-r ${config.gradient}`}>
      <span>{config.emoji}</span>
      <span>{config.formatValue(value)} {config.unit}</span>
    </div>
  );
}
```

---

## Share Flow Patterns

### Share Modal Component

**File:** `src/components/sharing/ShareModal.tsx`

WhatsApp-first layout:
1. Card preview (shows exactly what will be shared)
2. Optional message input (max 100 chars)
3. **WhatsApp button** - Large, primary action
4. Secondary buttons (X/Twitter, Copy Link)
5. Native share option (if supported)

### Pre-filled Messages by Card Type

**File:** `src/lib/sharing/shareMessages.ts`

```typescript
export const SHARE_MESSAGES: Record<CardType, (data: ShareData) => string> = {
  daily: (d) => `Just logged ${d.formattedValue} today! ${d.emoji} #StepLeague`,
  weekly: (d) => `My week: ${d.formattedValue} (avg ${d.average}/day) 💪 #StepLeague`,
  personal_best: (d) => `NEW PERSONAL BEST! ${d.formattedValue} 🏆 #StepLeague`,
  streak: (d) => `${d.value} days in a row! 🔥 #StepLeague`,
  challenge: (d) => `Can you beat my ${d.formattedValue}? 💪 #StepLeague`,
  rank_change: (d) => `Moved from #${d.oldRank} to #${d.newRank}! 🚀 #StepLeague`,
};
```

---

## Share URL Structure

### Quick Shares (URL Params)

For simple shares without persistence:

```
/share/[userId]?type=daily&metric=steps&value=12345&period=today&rank=3&league=Team%20Alpha
```

### Persistent Shares (Short Codes)

For trackable shares with analytics:

```
/s/xK7mN2pQ
```

**Database Schema:**

```sql
CREATE TABLE share_cards (
  id UUID PRIMARY KEY,
  short_code VARCHAR(8) UNIQUE NOT NULL,
  user_id UUID REFERENCES users(id),
  card_type VARCHAR(50) NOT NULL,
  metric_type VARCHAR(20) DEFAULT 'steps',
  metric_value INTEGER NOT NULL,
  -- ... additional fields
);
```

### Generating Short Codes

```typescript
import { nanoid } from 'nanoid';

function generateShortCode(): string {
  return nanoid(8); // e.g., "xK7mN2pQ"
}
```

---

## Analytics Tracking

### Share Events

```typescript
// Track share intent (modal opened)
analytics.trackEvent('share_intent', {
  card_type: 'daily',
  metric_type: 'steps',
  source: 'stats_hub', // or 'post_submission', 'milestone'
});

// Track share completion
analytics.share('achievement', cardId, platform);
// Sends to both GA4 and PostHog
```

### UTM Parameters

Always add UTM parameters to share URLs:

```typescript
const shareUrl = new URL(baseUrl);
shareUrl.searchParams.set('utm_source', 'share');
shareUrl.searchParams.set('utm_medium', platform); // 'whatsapp', 'twitter', 'copy'
shareUrl.searchParams.set('utm_campaign', cardType); // 'daily', 'streak', etc.
```

### Share Funnel

Track the full funnel:
1. `share_intent` - User opened share modal
2. `share` - User completed share action
3. `share_link_click` - Recipient clicked shared link
4. `share_conversion` - Recipient signed up

---

## WhatsApp-Specific Optimizations

### Link Preview (OG Tags)

Ensure share pages have proper OG tags:

```typescript
// In page.tsx generateMetadata
export async function generateMetadata({ searchParams }): Promise<Metadata> {
  const ogImageUrl = new URL("/api/og", process.env.NEXT_PUBLIC_APP_URL);
  // Add all params...

  return {
    title,
    description,
    openGraph: {
      title,
      description,
      images: [{
        url: ogImageUrl.toString(),
        width: 1200,
        height: 630,
        alt: title,
      }],
      type: "website",
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [ogImageUrl.toString()],
    },
  };
}
```

### WhatsApp URL Format

```typescript
const waUrl = `https://wa.me/?text=${encodeURIComponent(fullMessage)}`;
window.open(waUrl, "_blank", "noopener,noreferrer");
```

Note: Don't pre-fill the recipient (`https://wa.me/1234567890`) - let users choose.

---

## Integration Points

### Post-Submission Prompt

After successful upload, show share modal:

```typescript
// In BatchSubmissionForm or SubmissionForm
const handleSubmitSuccess = () => {
  // Check user preference
  if (userPreferences.sharePromptsEnabled !== false) {
    setShowShareModal(true);
  }
};
```

### Milestone Detection

```typescript
const STREAK_MILESTONES = [7, 14, 30, 50, 100, 365];

function checkForMilestone(newStreak: number): boolean {
  return STREAK_MILESTONES.includes(newStreak);
}
```

### Personal Best Detection

```typescript
// In submission handler
if (newSteps > userStats.best_day_steps) {
  triggerSharePrompt({ type: 'personal_best', value: newSteps });
}
```

---

## Real Codebase Examples

### useShare Hook

**File:** `src/hooks/useShare.ts`

```typescript
export function useShare(options: UseShareOptions = {}) {
  const share = useCallback(async (data: ShareData, platform: SharePlatform = "native") => {
    // Track in analytics immediately (capture intent)
    if (options.contentType) {
      analytics.share(options.contentType, options.itemId, platform);
    }

    switch (platform) {
      case "whatsapp":
        const waUrl = `https://wa.me/?text=${encodeURIComponent(fullMessage)}`;
        window.open(waUrl, "_blank", "noopener,noreferrer");
        break;
      // ... other platforms
    }
  }, [options]);

  return { share, isSharing, copied, supportsNativeShare };
}
```

### OG Image Route

**File:** `src/app/api/og/route.tsx`

Current implementation generates beautiful cards with:
- Gradient backgrounds
- Emoji badges
- Rank colors (gold for #1, silver for #2, etc.)
- Step counts with locale formatting
- Improvement badges
- StepLeague branding footer

---

## Related Skills

- `analytics-tracking` - Share event tracking patterns
- `design-system` - Card and modal styling
- `api-handler` - OG API route patterns
- `architecture-philosophy` - Modular design principles

---

## Research References

- [Frontiers Psychology - Fitness Social Media Impact](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2025.1635912/full)
- [OG Image Gallery - Dimensions Guide](https://www.ogimage.gallery/libary/the-ultimate-guide-to-og-image-dimensions-2024-update)
- [OpenGraph.xyz - Image Best Practices](https://www.opengraph.xyz/blog/the-ultimate-guide-to-open-graph-images)
