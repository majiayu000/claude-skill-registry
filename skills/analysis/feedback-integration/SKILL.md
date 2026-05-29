---
name: Feedback Integration
tier: 4
load_policy: conditional
description: Process viewer comments and feedback to improve content
version: 1.0.0
parent_skill: growth-learning
---

# Feedback Integration Skill

> **Listening to Our Listeners**

This skill processes viewer comments and direct feedback to understand impact and improve future sessions.

---

## Purpose

Extract qualitative insights from viewer feedback and integrate into the knowledge base.

---

## Command

```bash
/learn-comments session-name
```

---

## Input Sources

| Source | Type | Value |
|--------|------|-------|
| YouTube Comments | Public | Unfiltered reactions |
| Email Feedback | Private | Detailed testimonials |
| Social Mentions | Public | Organic shares |
| Direct Messages | Private | Personal experiences |

---

## Comment Analysis Process

### 1. Collection

Gather comments from YouTube Studio or API:

```yaml
comments:
  - author: "Seeker123"
    text: "This helped me sleep for the first time in weeks..."
    likes: 42
    timestamp: "2025-01-10T14:32:00Z"
  - author: "MeditatorPro"
    text: "The Eden imagery was so vivid, I felt like I was there"
    likes: 28
    timestamp: "2025-01-11T09:15:00Z"
```

### 2. Categorization

Classify each comment:

| Category | Indicators |
|----------|------------|
| **Impact** | "helped me", "changed my", "finally" |
| **Experience** | "felt like", "saw", "experienced" |
| **Technical** | "audio", "sound", "voice", "quality" |
| **Request** | "could you", "please make", "I wish" |
| **Question** | "how do I", "what is", "when should" |
| **Criticism** | "didn't like", "too long", "confusing" |

### 3. Sentiment Analysis

Score overall sentiment:

| Sentiment | Score Range | Meaning |
|-----------|-------------|---------|
| Very Positive | 0.8-1.0 | Strong resonance |
| Positive | 0.5-0.8 | Good reception |
| Neutral | 0.3-0.5 | Mixed signals |
| Negative | 0.0-0.3 | Issues to address |

### 4. Theme Extraction

Identify recurring themes:

```yaml
themes:
  - theme: "sleep_improvement"
    frequency: 12
    sentiment: 0.9
    sample_quotes:
      - "Finally slept through the night"
      - "Best sleep aid I've found"

  - theme: "vivid_imagery"
    frequency: 8
    sentiment: 0.85
    sample_quotes:
      - "The garden felt so real"
      - "I could actually see the light"
```

### 5. Insight Generation

Convert themes to actionable insights:

```yaml
insight:
  finding: "Eden garden imagery creates exceptionally vivid experiences"
  evidence: "8 comments specifically mentioned vivid imagery in Eden session"
  action: "Use garden/nature settings for healing sessions"
  confidence: medium
  source: "comments"
```

---

## Feedback Categories

### Impact Testimonials

Most valuable for understanding effectiveness:

> "I've struggled with anxiety for years, and this session gave me the first deep relaxation I've felt in months."

**Extract**:
- Outcome achieved: anxiety relief
- Session type: healing
- Impact level: significant
- Time element: long-term struggle resolved

### Experience Reports

Valuable for refining content:

> "When you described the waterfall, I could actually feel the cool mist on my skin."

**Extract**:
- Effective element: waterfall imagery
- Sensory channel: kinesthetic (touch)
- Immersion level: high

### Technical Feedback

Valuable for production quality:

> "The voice was perfect but the binaural felt a bit too loud in my right ear."

**Extract**:
- Voice quality: positive
- Binaural mixing: needs review
- Specific issue: channel balance

### Requests

Valuable for content planning:

> "I'd love a session focused on confidence before presentations."

**Extract**:
- Requested outcome: confidence
- Context: professional/presentations
- Priority: add to topic queue

---

## Negative Feedback Handling

### Constructive Criticism

Address in future sessions:

| Criticism | Response |
|-----------|----------|
| "Too slow at the start" | Review induction pacing |
| "Voice felt monotonous" | Add prosody variation |
| "Couldn't visualize" | Enhance sensory descriptions |
| "Ending was abrupt" | Extend emergence section |

### Non-Constructive

Note but don't over-weight:

| Comment | Response |
|---------|----------|
| "This is fake" | Acknowledge different expectations |
| "Hypnosis is dangerous" | Note misconception, don't change approach |
| Spam/trolling | Ignore |

---

## Knowledge Base Updates

Store insights in `knowledge/lessons_learned.yaml`:

```yaml
- id: "FEEDBACK-2025-001"
  category: "feedback"
  finding: "Kinesthetic imagery (touch sensations) increases immersion"
  evidence: "Multiple comments mention feeling physical sensations"
  action: "Include tactile descriptions in every visualization"
  confidence: medium
  source: "viewer_comments"
  sessions_referenced:
    - "eden-garden-pathworking"
    - "healing-waterfall-journey"
  date_discovered: "2025-01-15"
```

---

## Feedback Loop Timing

| Period | Action |
|--------|--------|
| 24-48 hours | Initial comment surge |
| 7 days | First round analysis |
| 30 days | Comprehensive review |
| 90 days | Long-term impact assessment |

---

## Output

After analysis:

1. **Feedback Summary**: Categorized comments with sentiment
2. **Theme Report**: Recurring patterns with evidence
3. **Insight Updates**: New entries for knowledge base
4. **Action Items**: Specific improvements for next sessions
5. **Request Queue**: Topics requested by viewers

---

## Integration with Analytics

Combine feedback with metrics for complete picture:

| Metric Says | Feedback Says | Conclusion |
|-------------|---------------|------------|
| High retention | "Loved every minute" | True success |
| Low retention | "Got distracted" | Content issue |
| High retention | "Fell asleep" | Works for sleep (intended?) |
| Low likes | "Too different for me" | Niche content, not failure |

---

## Related Resources

- **Skill**: `tier4-growth/analytics-learning/` (quantitative)
- **Knowledge**: `knowledge/lessons_learned.yaml`
