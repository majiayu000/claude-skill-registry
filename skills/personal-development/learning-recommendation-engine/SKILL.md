---
name: learning-recommendation-engine
description: Generate personalized content recommendations based on learner profiles, performance, preferences, and learning analytics. Use for adaptive learning systems, content discovery, and personalized guidance. Activates on "recommend content", "next best", "personalization", or "what should I learn next".
---

# Learning Recommendation Engine

Recommend optimal learning resources, activities, and pathways based on learner data and performance patterns.

## When to Use
- Personalized content recommendations
- Next-best-action suggestions
- Resource matching
- Difficulty adaptation
- Intervention triggers

## Recommendation Logic
- Collaborative filtering (learners like you learned X)
- Content-based (similar to what you've done)
- Performance-based (fill your gaps)
- Goal-oriented (towards your objectives)
- Engagement-based (what keeps you learning)

## CLI Interface
```bash
/learning.recommendation-engine --learner-profile "profile.json" --context "struggling with calculus"
/learning.recommendation-engine --next-best-action --performance "recent-scores.json"
```

## Output
- Ranked recommendations with rationale
- Personalized learning queue
- Intervention triggers
- Resource suggestions

## Composition
**Input from**: `/learning.pathway-designer`, `/curriculum.analyze-outcomes`
**Output to**: Personalized learning experience

## Exit Codes
- **0**: Recommendations generated
- **1**: Insufficient learner data
- **2**: Invalid profile format
