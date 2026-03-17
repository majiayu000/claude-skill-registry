---
name: x-algorithm
description: X/Twitter For You feed ranking algorithm - optimize tweets for maximum reach
metadata:
  tags: twitter, x, algorithm, social, ranking, engagement
  source: https://github.com/xai-org/x-algorithm
---

# X Algorithm Skill

Optimize tweets and threads for the X (Twitter) For You feed algorithm.

## How the Algorithm Works

The X For You feed uses a Grok-based Phoenix transformer that predicts engagement probabilities for each tweet. No hand-engineered features—it learns entirely from engagement patterns.

### The Formula

```
Final Score = Σ (weight × P(action))
```

Each tweet gets scored by predicting the probability you'll take various actions, then weighting them.

### What It Predicts

**Positive signals (boost score):**
| Signal | What It Measures |
|--------|------------------|
| `P(favorite)` | Likelihood of like |
| `P(reply)` | Likelihood of reply |
| `P(repost)` | Likelihood of repost |
| `P(quote)` | Likelihood of quote tweet |
| `P(click)` | Likelihood of clicking through |
| `P(profile_click)` | Likelihood of visiting author's profile |
| `P(video_view)` | Likelihood of watching video |
| `P(photo_expand)` | Likelihood of expanding image |
| `P(share)` | Likelihood of sharing externally |
| `P(dwell)` | Time spent reading/viewing |
| `P(follow_author)` | Likelihood of following |

**Negative signals (reduce score):**
| Signal | What It Measures |
|--------|------------------|
| `P(not_interested)` | Likelihood of "Not interested" |
| `P(block_author)` | Likelihood of blocking |
| `P(mute_author)` | Likelihood of muting |
| `P(report)` | Likelihood of reporting |

### Additional Ranking Factors

- **Author Diversity**: Repeated posts from same author get attenuated
- **Out-of-Network Boost**: Discovered content (not from follows) gets special scoring
- **Candidate Isolation**: Each tweet scored independently

## Commands

```
/x-algorithm analyze [tweet]     # Score a tweet draft
/x-algorithm optimize [tweet]    # Suggest improvements
/x-algorithm signals             # Show all ranking signals
/x-algorithm hooks               # Generate high-engagement hooks
```

## Usage

### Analyzing a Tweet

```
/x-algorithm analyze "Just shipped a new feature"

ANALYSIS:
┌─────────────────────────────────────────────────┐
│  Tweet: "Just shipped a new feature"            │
├─────────────────────────────────────────────────┤
│  Predicted signals:                             │
│  ├─ P(favorite)      LOW   - no emotional hook  │
│  ├─ P(reply)         LOW   - no question/gap    │
│  ├─ P(repost)        LOW   - no value to share  │
│  ├─ P(quote)         LOW   - nothing to add to  │
│  ├─ P(dwell)         LOW   - too short          │
│  └─ P(not_interested) MED  - generic update     │
│                                                 │
│  Overall: WEAK                                  │
│                                                 │
│  Issues:                                        │
│  • No specificity (what feature? why care?)     │
│  • No emotional trigger                         │
│  • No reason to engage                          │
└─────────────────────────────────────────────────┘

Optimize? (yes/no)
```

### Optimizing a Tweet

```
/x-algorithm optimize "Just shipped a new feature"

OPTIMIZED VERSIONS:

v1 (curiosity gap):
"The feature everyone asked for just shipped.

Took 6 months. Here's why it was worth the wait:"

v2 (social proof):
"1,247 people requested this feature.

Today we shipped it.

[screenshot]"

v3 (contrarian):
"Everyone said this feature was impossible.

We built it anyway.

Here's how:"

---

Which version, or iterate?
```

## Optimization Principles

### Maximize Positive Signals

**For P(favorite) - likes:**
- Strong opinion or take
- Relatable observation
- Emotional resonance
- Beautiful visually

**For P(reply) - replies:**
- Ask a question
- Create a knowledge gap
- Be slightly wrong (people love to correct)
- Request input

**For P(repost) - reposts:**
- Provide shareable value (tips, insights)
- Create "I wish I said that" moments
- Make people look smart for sharing

**For P(quote) - quotes:**
- Leave room for commentary
- Take a stance others want to respond to
- Share something people want to add context to

**For P(dwell) - time on tweet:**
- Longer, readable content
- Images that require study
- Threads with substance
- Videos

**For P(follow) - new followers:**
- Demonstrate unique expertise
- Show personality
- Consistent topic/niche

### Minimize Negative Signals

**Avoid P(not_interested):**
- Don't be generic
- Don't repeat what everyone says
- Don't post off-topic

**Avoid P(block/mute):**
- Don't be annoying
- Don't spam
- Don't be hostile
- Don't engage in bad faith

**Avoid P(report):**
- Don't violate ToS
- Don't harass
- Don't spread misinfo

## High-Engagement Patterns

### The Hook Patterns

```
1. CURIOSITY GAP
   "I spent 3 years learning [X]. Here's what I wish I knew:"

2. CONTRARIAN
   "Unpopular opinion: [hot take]"

3. STORY OPENER
   "In 2019 I was [relatable struggle]. Now I [impressive outcome]."

4. SPECIFIC NUMBER
   "I've [done X] 847 times. Here's what works:"

5. BEFORE/AFTER
   "I used to [common mistake]. Then I learned [insight]."

6. QUESTION
   "What's one thing you wish you learned earlier about [X]?"
```

### Thread Structures That Work

```
LISTICLE:
"10 [things] about [topic]:"
→ High dwell, easy to repost individual tweets

BUILD-UP:
1. Hook
2. Context
3. Insight
4. Proof
5. Implication
6. CTA
→ Maximizes dwell across thread

STORY:
1. "It was 2AM when..."
2. Rising action
3. Crisis point
4. Resolution
5. Lesson
6. CTA
→ High engagement, emotional resonance
```

### Visual Content

```
IMAGES:
- Screenshots > stock photos
- Before/after comparisons
- Data visualizations
- Behind-the-scenes

VIDEOS:
- Hook in first 1-3 seconds
- Subtitles (most watch muted)
- Native upload > links
- <2 min optimal
```

## Integration with /content

When using `/content thread` or `/content post`, the X algorithm principles are automatically applied:

```
/content thread "our new pricing model"

Applying X algorithm optimization...
├─ Hook pattern: SPECIFIC NUMBER
├─ Thread structure: BUILD-UP
├─ Engagement triggers: curiosity, social proof
└─ Visual: screenshot recommendation

[generates thread with algorithm principles]
```

## Author Diversity Consideration

The algorithm attenuates repeated authors. Posting strategy matters:

```
SUBOPTIMAL:
Post → Post → Post → Post (same hour)
Algorithm reduces later posts' reach

BETTER:
Post → [gap] → Post → [gap] → Post
Each post gets full scoring potential
```

## Out-of-Network Discovery

To reach beyond your followers:

```
- Quote tweet popular accounts (your take on their content)
- Reply meaningfully to trending topics
- Create highly repostable content (others share to their network)
- Post content that generates quotes (your reach + quoter's reach)
```

## Metrics to Watch

After posting, monitor:

| Metric | What It Tells You |
|--------|-------------------|
| Impressions from For You | Algorithm reach |
| Impressions from profile | Direct followers |
| Engagement rate | Content quality signal |
| Quote:Repost ratio | How "discussable" content is |
| Reply quality | Community engagement depth |

## Source

Based on the open-sourced X algorithm:
https://github.com/xai-org/x-algorithm

The algorithm is continuously updated. Check the repo for latest changes.
