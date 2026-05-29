---
name: Growth & Learning
tier: 4
load_policy: conditional
description: Analytics, feedback processing, and continuous improvement
version: 1.0.0
---

# Growth & Learning Skill (Tier 4)

> **The Feedback Loop That Makes Us Better**

This tier contains skills for analyzing performance and improving future sessions.

---

## Purpose

Process feedback, analyze metrics, and continuously improve the Dreamweaving system.

---

## Load Conditions

This tier loads conditionally when:

- Processing YouTube analytics data
- Analyzing viewer comments
- Reviewing code quality
- Applying lessons to new sessions

---

## Sub-Skills

| Skill | Location | Purpose |
|-------|----------|---------|
| **Analytics Learning** | `analytics-learning/` | Process YouTube metrics |
| **Feedback Integration** | `feedback-integration/` | Extract insights from comments |

---

## Feedback Loop

```
Session Published
       ↓
Analytics Collected (30-90 days)
       ↓
Lessons Extracted
       ↓
Knowledge Base Updated
       ↓
Applied to Next Session
       ↓
[Repeat]
```

---

## Key Metrics Tracked

| Category | Metrics |
|----------|---------|
| **Engagement** | Views, likes, comments, shares |
| **Retention** | Average view duration, retention % |
| **Growth** | Subscribers gained, impressions |
| **Quality** | Like ratio, comment sentiment |

---

## Benchmarks

| Metric | Good | Average | Needs Work |
|--------|------|---------|------------|
| Retention (30 min) | >50% | 30-50% | <30% |
| Like Ratio | >8% | 4-8% | <4% |
| Comment Rate | >1% | 0.5-1% | <0.5% |
| Sub Conversion | >2% | 1-2% | <1% |

---

## Knowledge Base Files

| File | Purpose |
|------|---------|
| `knowledge/lessons_learned.yaml` | Accumulated insights |
| `knowledge/best_practices.md` | Evolving standards |
| `knowledge/analytics_history/` | Historical data |

---

## Commands

```bash
# Process analytics for a session
/learn-analytics session-name

# Analyze comments
/learn-comments session-name

# Review code quality
/review-code

# Show accumulated lessons
/show-lessons
```

---

## Integration with Production

When creating new sessions:

1. Check `lessons_learned.yaml` first
2. Apply successful patterns
3. Avoid known pitfalls
4. Test new approaches systematically

---

## Related Resources

- **Serena Memory**: `session_learnings_system`
- **Doc**: `docs/CANONICAL_WORKFLOW.md` (learning section)
