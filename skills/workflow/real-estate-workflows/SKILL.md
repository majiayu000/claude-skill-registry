---
name: real-estate-workflows
description: End-to-end workflows for real estate content production. Use when orchestrating multi-step processes like URL-to-video generation, batch processing, or social media distribution. Coordinates Firecrawl, AI generation, and Remotion rendering.
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# Real Estate Workflows

## Core Pipeline

### URL → Video Workflow
```
[Listing URL Input]
       ↓
[Firecrawl Extraction]
       ↓
[Data Validation]
       ↓
[AI Script Generation]
       ↓
[TTS Voiceover (Optional)]
       ↓
[Remotion Render]
       ↓
[Upload to Storage]
       ↓
[Notify User]
```

## Workflow API

### Single Video Generation
```typescript
POST /api/workflow/generate-video
{
  listingUrl: "https://zillow.com/...",
  videoType: "property-showcase",
  options: {
    voiceover: true,
    music: "upbeat",
    branding: {
      agentName: "Jane Smith",
      logoUrl: "https://..."
    }
  }
}
```

### Batch Processing
```typescript
POST /api/workflow/batch
{
  urls: ["url1", "url2", "url3"],
  videoType: "social-short",
  options: { ... }
}
```

### Status Tracking
```typescript
GET /api/workflow/status/:jobId

{
  jobId: "job_abc123",
  status: "rendering",
  progress: 65,
  steps: [
    { name: "scrape", status: "complete", duration: 2.3 },
    { name: "script", status: "complete", duration: 4.1 },
    { name: "voiceover", status: "complete", duration: 8.2 },
    { name: "render", status: "in_progress", progress: 45 }
  ],
  estimatedCompletion: "2024-01-15T10:30:00Z"
}
```

## Detailed Rules

- **URL to Video**: See [rules/url-to-video.md](rules/url-to-video.md)
- **Batch Processing**: See [rules/batch-processing.md](rules/batch-processing.md)
- **Social Distribution**: See [rules/social-distribution.md](rules/social-distribution.md)

## Database Schema

### Video Jobs (Convex)
```typescript
defineTable({
  userId: v.string(),
  listingUrl: v.string(),
  videoType: v.string(),
  status: v.string(), // pending, scraping, generating, rendering, complete, failed
  progress: v.number(),
  propertyData: v.optional(v.any()),
  script: v.optional(v.string()),
  voiceoverUrl: v.optional(v.string()),
  videoUrl: v.optional(v.string()),
  thumbnailUrl: v.optional(v.string()),
  error: v.optional(v.string()),
  createdAt: v.number(),
  completedAt: v.optional(v.number()),
})
```

## Error Handling

| Error | Recovery |
|-------|----------|
| Scrape failed | Retry with fallback parser |
| AI timeout | Retry with shorter prompt |
| Render OOM | Reduce resolution, retry |
| Storage failed | Queue for later upload |

## Webhook Notifications

```typescript
// Configure in user settings
POST /webhooks/video-complete
{
  event: "video.complete",
  jobId: "job_abc123",
  videoUrl: "https://storage.../video.mp4",
  propertyAddress: "123 Main St",
  timestamp: "2024-01-15T10:30:00Z"
}
```

## Integrations

- **Firecrawl**: Property data extraction
- **Gemini AI**: Script generation
- **OpenAI TTS**: Voiceover synthesis
- **Remotion Lambda**: Video rendering
- **Supabase Storage**: Asset hosting
- **Convex**: Real-time job tracking
- **Clerk**: User authentication
- **Stripe**: Usage billing
