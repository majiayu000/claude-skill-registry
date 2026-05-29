---
name: personality-profiler
description: Generate rich personality profiles from social media data exports (Twitter/X, LinkedIn, Instagram). Use when a user wants to analyze their social media presence, create a personality profile for AI personalization, understand their communication patterns, or extract insights from their digital footprint. Triggers on requests like "analyze my Twitter data", "create a personality profile", "what can you learn about me from my posts", "personalize an AI for me", or when users provide social media export files.
---

# Personality Profiler

Generate comprehensive, extensible personality profiles from social media data exports.

## Overview

This skill analyzes exported social media data to create detailed personality profiles suitable for:
1. AI assistant personalization (training data for personalized responses)
2. Self-reflection and pattern discovery

## Workflow

1. **Receive data** — User provides exported data files (JSON/CSV)
2. **Parse data** — Extract posts, comments, interactions using platform-specific parsers
3. **Analyze dimensions** — Evaluate across 8 personality dimensions
4. **Generate profile** — Output structured profile in extensible JSON format
5. **Summarize insights** — Provide human-readable summary

## Supported Platforms

| Platform | Export Type | Key Files |
|----------|-------------|-----------|
| Twitter/X | ZIP archive | `tweets.js`, `like.js`, `profile.js` |
| LinkedIn | ZIP archive | `Profile.csv`, `Connections.csv`, `Comments.csv`, `Shares.csv` |
| Instagram | ZIP archive | `content/posts_1.json`, `comments.json`, `profile.json` |

For detailed format specifications, see [references/platform-formats.md](references/platform-formats.md).

## Analysis Dimensions

Analyze content across these 8 dimensions:

### 1. Communication Style
- **Tone**: formal ↔ casual, serious ↔ playful, direct ↔ diplomatic
- **Verbosity**: concise ↔ elaborate, uses bullet points vs paragraphs
- **Vocabulary**: technical level, industry jargon, colloquialisms

### 2. Interests & Expertise
- **Topics**: recurring themes, domains of focus
- **Depth**: surface mentions vs deep engagement
- **Evolution**: how interests have changed over time

### 3. Values & Beliefs
- **Priorities**: what matters most (inferred from emphasis)
- **Advocacy**: causes supported or promoted
- **Philosophy**: worldview indicators

### 4. Social Patterns
- **Engagement style**: initiator vs responder, commenter vs creator
- **Network orientation**: broad reach vs tight community
- **Interaction tone**: supportive, challenging, neutral

### 5. Emotional Expression
- **Range**: emotional vocabulary breadth
- **Valence**: positive/negative tendency
- **Triggers**: what elicits strong reactions

### 6. Cognitive Style
- **Reasoning**: analytical vs intuitive, data-driven vs narrative
- **Complexity**: nuanced vs straightforward positions
- **Openness**: receptivity to new ideas

### 7. Professional Identity
- **Domain**: industry, role, expertise areas
- **Aspirations**: career direction signals
- **Network**: professional relationship patterns

### 8. Temporal Patterns
- **Activity rhythms**: when they post, reply, engage
- **Content cycles**: seasonal or event-driven patterns
- **Growth trajectory**: how expression has evolved

## Profile Schema

Output profiles in this extensible JSON structure:

```json
{
  "version": "1.0",
  "generated_at": "ISO-8601 timestamp",
  "data_sources": [
    {
      "platform": "twitter|linkedin|instagram",
      "date_range": {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"},
      "item_count": 1234
    }
  ],
  "profile": {
    "summary": "2-3 paragraph narrative summary",
    "dimensions": {
      "communication_style": {
        "confidence": 0.0-1.0,
        "traits": {
          "formality": {"value": -1.0 to 1.0, "evidence": ["quote1", "quote2"]},
          "verbosity": {"value": -1.0 to 1.0, "evidence": []},
          "directness": {"value": -1.0 to 1.0, "evidence": []}
        },
        "patterns": ["pattern1", "pattern2"],
        "recommendations_for_ai": "How an AI should communicate with this person"
      }
    },
    "notable_quotes": [
      {"text": "quote", "context": "why notable", "dimension": "which dimension"}
    ],
    "keywords": ["term1", "term2"],
    "topics_ranked": [
      {"topic": "name", "frequency": 0.0-1.0, "sentiment": -1.0 to 1.0}
    ]
  },
  "extensions": {}
}
```

The `extensions` field allows adding custom dimensions without breaking compatibility.

## Process

### Step 1: Data Ingestion

When user provides files:

1. Identify platform from file structure
2. Locate key content files (see platform table above)
3. Parse using appropriate format handler
4. Normalize to common internal structure:

```json
{
  "items": [
    {
      "id": "unique_id",
      "type": "post|comment|share|like",
      "timestamp": "ISO-8601",
      "content": "text content",
      "metadata": {
        "platform": "twitter",
        "engagement": {"likes": 0, "replies": 0, "shares": 0},
        "context": "reply_to_id or null"
      }
    }
  ]
}
```

### Step 2: Content Analysis

For each dimension:

1. **Extract signals** — Find relevant content snippets
2. **Score traits** — Rate on dimension-specific scales
3. **Gather evidence** — Collect representative quotes
4. **Calculate confidence** — Based on data volume and consistency

Minimum thresholds for confident analysis:
- 50+ posts for basic profile
- 200+ posts for detailed profile
- 500+ posts for high-confidence profile

If below thresholds, note reduced confidence in output.

### Step 3: Profile Generation

1. Populate all dimension objects in schema
2. Write narrative summary synthesizing key findings
3. Extract notable quotes (5-10 most characteristic)
4. Rank topics by frequency and engagement
5. Generate AI personalization recommendations

### Step 4: Output Delivery

Provide two outputs:

1. **JSON profile** — Complete structured data (save as `personality_profile.json`)
2. **Markdown summary** — Human-readable insights document

## AI Personalization Recommendations

For each dimension, include specific guidance for AI systems:

**Example recommendations:**
```
communication_style.recommendations_for_ai:
"Use a conversational but informed tone. Avoid excessive formality.
Include occasional humor. Lead with conclusions, then supporting detail.
Match their tendency for medium-length responses (2-3 paragraphs)."

interests.recommendations_for_ai:
"Can reference machine learning, distributed systems, and startup culture
without explanation. Assume familiarity with Python ecosystem. May enjoy
tangential connections to philosophy of technology."
```

## Handling Multiple Platforms

When analyzing data from multiple platforms:

1. Process each platform separately first
2. Cross-reference for consistency
3. Note platform-specific behaviors (e.g., more formal on LinkedIn)
4. Weight professional platforms for work identity
5. Weight personal platforms for authentic voice
6. Merge into unified profile with platform annotations

## Privacy Considerations

Before processing:

1. Confirm user owns the data
2. Note that analysis stays local (no external API calls for content)
3. Offer to redact specific people/topics if requested
4. Output can be edited before use

## Extending the Profile

The profile schema supports extensions:

```json
{
  "extensions": {
    "custom_dimension": {
      "confidence": 0.8,
      "traits": {},
      "patterns": [],
      "recommendations_for_ai": ""
    },
    "domain_specific": {
      "developer_profile": {
        "languages": ["python", "rust"],
        "paradigm_preference": "functional-leaning"
      }
    }
  }
}
```

Users can request custom dimensions by describing what they want analyzed.
