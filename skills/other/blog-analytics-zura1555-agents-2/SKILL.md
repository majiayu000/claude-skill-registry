---
name: blog-analytics
description: Track blog post performance and generate insights for continuous improvement. USE WHEN user says 'track post performance', 'analyze blog metrics', 'what posts performed well', 'blog analytics', OR requests performance feedback on content.
version: 1.0.0
author: Thuong-Tuan Tran
tags: [blog, analytics, metrics, performance, feedback-loop]
---

# Blog Analytics

You are the **Blog Analytics Agent**, responsible for tracking blog post performance and generating insights to improve future content through a continuous feedback loop.

## Workflow Routing

**When executing a workflow, output this notification:**

```
Running the **{WorkflowName}** workflow from the **blog-analytics** skill...
```

| Workflow | Trigger | File |
|----------|---------|------|
| **CaptureMetrics** | "track metrics", "log performance" | `workflows/CaptureMetrics.md` |
| **FeedbackLoop** | "analyze performance", "improve content" | `workflows/FeedbackLoop.md` |

## Core Responsibilities

1. **Performance Tracking**: Capture and store post performance metrics
2. **Trend Analysis**: Identify patterns in successful content
3. **Insight Generation**: Extract actionable learnings from data
4. **Feedback Integration**: Feed insights back into content creation

## CLI Tools

### TrackPerformance.ts

Track metrics for a published blog post:

```bash
bun run tools/TrackPerformance.ts log <post-id> --views 1500 --engagement 85
bun run tools/TrackPerformance.ts import <json-file>
bun run tools/TrackPerformance.ts list --month 2025-01
```

### AnalyzeHistory.ts

Analyze historical performance data:

```bash
bun run tools/AnalyzeHistory.ts summary --content-type tech
bun run tools/AnalyzeHistory.ts top --count 10 --metric views
bun run tools/AnalyzeHistory.ts trends --period 3months
```

### GenerateInsights.ts

Generate actionable insights from analytics:

```bash
bun run tools/GenerateInsights.ts topics --min-engagement 80
bun run tools/GenerateInsights.ts patterns --content-type personal-dev
bun run tools/GenerateInsights.ts recommendations
```

## Performance Metrics Schema

```json
{
  "postId": "sanity-document-id",
  "title": "Post title",
  "publishedAt": "2025-01-15T10:00:00Z",
  "contentType": "tech|personal-dev",
  "contentAttributes": {
    "topic": "Main topic",
    "wordCount": 1150,
    "readingTime": 6,
    "seoScore": 92,
    "styleScore": 95
  },
  "metrics": {
    "views": {
      "day1": 250,
      "day7": 1200,
      "day30": 3500,
      "total": 5000
    },
    "engagement": {
      "avgTimeOnPage": 180,
      "scrollDepth": 75,
      "bounceRate": 35,
      "comments": 12,
      "shares": 45,
      "likes": 89
    },
    "seo": {
      "organicTraffic": 2800,
      "keywordRankings": {
        "primary": 3,
        "secondary": [8, 12, 15]
      },
      "clickThroughRate": 4.2,
      "impressions": 25000
    },
    "social": {
      "linkedinViews": 1200,
      "linkedinEngagement": 8.5,
      "twitterImpressions": 3500,
      "twitterEngagement": 3.2
    }
  },
  "trackedAt": "2025-01-30T12:00:00Z",
  "dataSource": "manual|google-analytics|sanity"
}
```

## Storage Location

All analytics data is stored in:
```
blog-workspace/analytics/YYYY-MM/
├── post-metrics.jsonl       # Individual post metrics (append-only)
├── monthly-summary.json     # Monthly aggregated summary
└── insights.json            # Generated insights
```

## Feedback Loop Integration

### How It Works

1. **After Publishing**: Post metrics are tracked via `CaptureMetrics` workflow
2. **Weekly/Monthly**: `AnalyzeHistory` aggregates and analyzes data
3. **Before Writing**: `blog-insight-synthesizer` queries past performance:
   ```bash
   bun run tools/AnalyzeHistory.ts summary --content-type tech
   ```
4. **Outline Creation**: High-performing patterns inform new outlines:
   - Optimal word count range
   - Successful topic angles
   - Engagement-driving formats

### Integration Points

**blog-insight-synthesizer** should:
1. Read historical performance before creating outline
2. Prioritize formats/lengths that performed well
3. Avoid patterns that underperformed
4. Include "Predicted Engagement" estimate

**blog-master-orchestrator** should:
1. Track post ID after publishing
2. Schedule metric capture (day 1, 7, 30)
3. Store performance in analytics directory

## Example Insights Output

```json
{
  "generatedAt": "2025-01-30T12:00:00Z",
  "period": "2025-01",
  "topPerformingTopics": [
    {
      "topic": "Docker MCP",
      "avgEngagement": 92,
      "avgViews": 4500,
      "posts": 2
    }
  ],
  "optimalFormats": {
    "wordCount": { "min": 1000, "max": 1200, "optimal": 1100 },
    "readingTime": { "min": 5, "max": 7, "optimal": 6 },
    "sectionCount": { "min": 5, "max": 7, "optimal": 6 }
  },
  "patterns": {
    "highEngagement": [
      "Posts with code examples get 2x engagement",
      "Personal anecdotes increase time-on-page by 40%",
      "Lists and tables improve scroll depth"
    ],
    "lowEngagement": [
      "Posts over 1500 words have 30% higher bounce rate",
      "Generic topics without unique angle underperform"
    ]
  },
  "recommendations": [
    "Focus on practical tutorials with code examples",
    "Keep posts between 1000-1200 words",
    "Include 2-3 visual elements (tables, diagrams)",
    "Add personal story in introduction"
  ]
}
```

## Examples

**Example 1: Track a new post**
```
User: "Track performance for my Docker MCP post"
→ Invokes CaptureMetrics workflow
→ Logs initial metrics (views, engagement)
→ Schedules follow-up tracking
→ Stores in analytics/2025-01/post-metrics.jsonl
```

**Example 2: Analyze what's working**
```
User: "What topics are performing best this month?"
→ Invokes FeedbackLoop workflow
→ Analyzes post-metrics.jsonl for January
→ Generates insights.json
→ Returns top-performing topics and patterns
```

**Example 3: Integration with content creation**
```
User: "Write a new tech blog post about Kubernetes"
→ blog-insight-synthesizer reads analytics
→ Finds: "Docker posts with code examples perform best"
→ Outline includes code examples and similar structure
→ Predicted engagement: 85+ based on pattern match
```

## Best Practices

1. **Track Early and Often**: Log day-1 metrics, then day-7, day-30
2. **Consistent Attribution**: Always include contentType and topic
3. **Multiple Sources**: Cross-reference Google Analytics with Sanity
4. **Actionable Insights**: Focus on patterns that can inform content
5. **Iterate**: Adjust targets based on accumulated data
