---
name: Analytics Learning
tier: 4
load_policy: conditional
description: Process YouTube analytics to extract actionable insights
version: 1.0.0
parent_skill: growth-learning
---

# Analytics Learning Skill

> **Data-Driven Improvement**

This skill processes YouTube Studio analytics to understand what works and improve future sessions.

---

## Purpose

Extract actionable insights from performance data and update the knowledge base.

---

## Command

```bash
/learn-analytics session-name
```

---

## Input Data

User provides from YouTube Studio:

| Metric | Description |
|--------|-------------|
| Views | Total view count |
| Watch Time | Total hours watched |
| Average View Duration | Mean watch time |
| Retention % | % of video watched |
| Likes / Dislikes | Engagement signals |
| Comments | Comment count |
| Shares | Social shares |
| Subscribers Gained | New subscriptions |
| Impressions | How often shown |
| CTR | Click-through rate |

---

## Analysis Process

### 1. Benchmark Comparison

Compare session metrics to portfolio averages:

| Metric | This Session | Average | Verdict |
|--------|--------------|---------|---------|
| Retention | 48% | 42% | Above average |
| Like Ratio | 6.2% | 5.8% | Slightly above |
| Comments | 24 | 18 | Above average |

### 2. Pattern Identification

Correlate session attributes with performance:

| Attribute | Correlation |
|-----------|-------------|
| Topic: Healing | +15% retention |
| Duration: 25 min | Optimal |
| Voice: Neural2-H | Consistent |
| Binaural: Theta | +8% engagement |

### 3. Insight Extraction

Generate specific, actionable findings:

```yaml
- finding: "Healing topics achieve higher retention"
  evidence: "62% vs 45% average across 5 sessions"
  action: "Prioritize healing themes"
  confidence: high
  timestamp: "2025-01-15"
```

### 4. Knowledge Update

Store in `knowledge/lessons_learned.yaml`:

```yaml
lessons:
  - id: "LESSON-2025-001"
    category: "content"
    finding: "Healing topics achieve higher retention"
    evidence: "62% vs 45% average across 5 sessions"
    action: "Prioritize healing themes"
    confidence: high
    sessions_analyzed:
      - "inner-child-healing"
      - "heart-chakra-restore"
      - "grief-release-theta"
    date_discovered: "2025-01-15"
    date_validated: null
```

---

## Retention Analysis

### Retention Curve Patterns

| Pattern | Meaning | Action |
|---------|---------|--------|
| Steep initial drop | Poor hook/intro | Improve pre-talk |
| Drop at 5-7 min | Induction too slow | Tighten pacing |
| Steady through journey | Good engagement | Maintain approach |
| Drop at integration | Exit feels abrupt | Smooth emergence |

### Target Retention by Section

| Section | Target Retention |
|---------|------------------|
| Pre-Talk (0-3 min) | 90%+ |
| Induction (3-8 min) | 75%+ |
| Journey (8-22 min) | 55%+ |
| Integration (22-28 min) | 45%+ |
| Close (28-30 min) | 40%+ |

---

## Engagement Analysis

### Like Ratio Interpretation

| Like Ratio | Interpretation |
|------------|----------------|
| >10% | Exceptional resonance |
| 6-10% | Strong positive response |
| 4-6% | Normal engagement |
| <4% | Review content quality |

### Comment Analysis Signals

| Signal | Meaning |
|--------|---------|
| Emotional sharing | Deep impact |
| Questions | Interest but confusion |
| Requests | Unmet needs |
| Criticism | Quality issues |

---

## Session Attribute Tracking

For each session, track:

```yaml
session_attributes:
  topic: "healing"
  sub_topic: "inner_child"
  duration: 25
  depth_level: "Layer2"
  voice_id: "en-US-Neural2-H"
  binaural_target: "theta"
  archetypes:
    - "Guide"
    - "Healer"
  imagery_style: "eden_garden"

metrics:
  views: 1250
  watch_time_hours: 312
  avg_view_duration: "14:58"
  retention_percent: 48
  likes: 78
  dislikes: 2
  comments: 24
  shares: 12
  subs_gained: 15
  impressions: 8500
  ctr: 14.7
```

---

## Confidence Levels

| Level | Definition |
|-------|------------|
| `high` | 5+ sessions, consistent pattern |
| `medium` | 3-4 sessions, emerging pattern |
| `low` | 1-2 sessions, hypothesis only |

---

## Output

After analysis:

1. **Summary Report**: Key findings with evidence
2. **Knowledge Update**: New entries in `lessons_learned.yaml`
3. **Recommendations**: Actions for next sessions
4. **Questions**: Areas needing more data

---

## Related Resources

- **Skill**: `tier4-growth/feedback-integration/` (comment analysis)
- **Knowledge**: `knowledge/lessons_learned.yaml`
- **Knowledge**: `knowledge/analytics_history/`
