---
name: apex-video-generator
description: Generate real estate marketing videos from property data. Use when creating property showcases, social media content, market reports, or neighborhood tours. Integrates Firecrawl scraped data with Remotion rendering.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Apex Real Estate Video Generator

## Video Types

| Type | ID | Duration | Aspect | Use Case |
|------|-----|----------|--------|----------|
| Property Showcase | `property-showcase` | 30s | 16:9 | Listing promotion |
| Social Short | `social-short` | 9s | 9:16 | TikTok/Reels |
| Market Stats | `market-stats` | 20s | 16:9 | Monthly reports |
| Neighborhood Tour | `neighborhood-tour` | 45s | 16:9 | Area marketing |
| Agent Intro | `agent-intro` | 15s | 9:16 | Personal branding |
| Testimonial | `testimonial` | 20s | 16:9 | Social proof |
| Just Listed | `just-listed` | 12s | 9:16 | New listing alert |
| Just Sold | `just-sold` | 12s | 9:16 | Sales proof |
| Open House | `open-house` | 15s | 9:16 | Event promotion |
| Price Drop | `price-drop` | 10s | 9:16 | Price reduction |

## Data Flow

```
[Listing URL] → [Firecrawl Extract] → [Property Data]
                                           ↓
[AI Script Generator] ← [Property Data + Video Type]
         ↓
[Remotion Composition] → [Rendered Video]
         ↓
[Optional: OpenAI TTS] → [Voiceover Audio]
```

## API Usage

### Generate Video
```typescript
POST /api/video/generate
{
  listingUrl: "https://zillow.com/...",
  videoType: "property-showcase",
  voiceoverEnabled: true,
  branding: {
    agentName: "John Doe",
    brokerageName: "Apex Realty",
    logoUrl: "https://...",
    primaryColor: "#0dccf2"
  }
}

// Response
{
  success: true,
  videoId: "vid_abc123",
  status: "rendering",
  estimatedTime: 120 // seconds
}
```

### Check Status
```typescript
GET /api/video/status?id=vid_abc123

{
  status: "complete",
  videoUrl: "https://storage.../video.mp4",
  thumbnailUrl: "https://storage.../thumb.jpg",
  duration: 30,
  propertyData: { ... }
}
```

## Template Details

See individual rules for each video type:
- **Property Showcase**: See [rules/property-showcase.md](rules/property-showcase.md)
- **Social Shorts**: See [rules/social-shorts.md](rules/social-shorts.md)
- **Market Stats**: See [rules/market-stats.md](rules/market-stats.md)
- **Neighborhood Tour**: See [rules/neighborhood-tour.md](rules/neighborhood-tour.md)
- **Testimonial**: See [rules/testimonial-video.md](rules/testimonial-video.md)

## Branding System

All videos support custom branding:
- Agent name and photo
- Brokerage logo
- Primary accent color
- Contact information
- Social media handles
- Custom fonts (from Google Fonts)

## Scene Structure

### Property Showcase (30s)
1. **Hook** (0-3s): Stunning hero shot + price
2. **Stats** (3-7s): Beds, baths, sqft animation
3. **Gallery** (7-20s): Photo slideshow with Ken Burns
4. **Features** (20-25s): Key highlights list
5. **CTA** (25-30s): Contact info + logo

### Social Short (9s)
1. **Hook** (0-2s): Eye-catching visual + text
2. **Value** (2-6s): 3 key stats animated
3. **CTA** (6-9s): Swipe up / Contact

## Integration Points

- **Firecrawl**: Property data extraction
- **Gemini AI**: Script generation
- **OpenAI TTS**: Voiceover generation
- **Remotion Lambda**: Cloud rendering
- **Supabase Storage**: Video hosting
- **Convex**: Job tracking and history
