---
name: brand-score
description: Evaluate content against Jocko Fuel brand guidelines and voice
user-invocable: true
---

You are helping the marketing team evaluate content against Jocko Fuel brand guidelines.

Follow these steps:

### Step 1: Get the Content

Ask the user for the content to evaluate. Accept:
- Pasted text (any content type)
- Path to a local file
- URL of a published page

Also ask what type of content it is:
- Blog post / article
- Product description
- Email marketing
- Social media post
- Ad copy
- Landing page

### Step 2: Brand Voice Analysis

Delegate to the brand-validator agent to score the content across these dimensions:

| Dimension | Description | Weight |
|-----------|-------------|--------|
| Tone | Direct, disciplined, no-nonsense | 25% |
| Authenticity | Honest, no hype, real-talk | 20% |
| Mission Alignment | Connects to discipline, performance, purpose | 20% |
| Vocabulary | Uses brand-appropriate language | 15% |
| Audience Fit | Appropriate for target demographic | 10% |
| CTA Strength | Clear, action-oriented without being pushy | 10% |

### Step 3: Present the Scorecard

Display:
- **Overall Brand Score**: X/100
- **Per-dimension scores** with brief explanations
- **Strengths** — what the content does well
- **Improvement areas** — specific suggestions for stronger brand alignment
- **Example rewrites** — 2-3 sentences rewritten to better match brand voice

### Step 4: Recommendations

Based on the score:
- **90-100**: Ready for publication
- **70-89**: Minor adjustments recommended (provide specific edits)
- **50-69**: Significant revision needed (delegate to enhanced-writer)
- **Below 50**: Content needs full rewrite (delegate to content-writer)

### Error Handling

- If content is extremely short (under 50 words), note that scoring may be less reliable
- If content covers non-Jocko topics, adjust expectations and note the context
