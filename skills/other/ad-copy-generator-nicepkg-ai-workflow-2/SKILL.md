---
name: ad-copy-generator
description: Generate high-converting ad copy for Google Ads, Meta (Facebook/Instagram), LinkedIn, and TikTok. Creates multiple variations with A/B testing in mind. Includes headlines, descriptions, CTAs, and platform-specific formats. Use when creating ads, generating ad variations, or A/B testing ad copy.
---

# Ad Copy Generator

Generate platform-optimized advertising copy with multiple variations for A/B testing.

## Supported Platforms

| Platform | Ad Types | Key Constraints |
|----------|----------|-----------------|
| Google Ads | Search, Display, YouTube | Headlines 30 chars, Descriptions 90 chars |
| Meta (FB/IG) | Image, Video, Carousel, Stories | Primary text 125 chars, Headline 40 chars |
| LinkedIn | Sponsored Content, Message Ads, Text Ads | Intro 150 chars, Headline 70 chars |
| TikTok | In-Feed, TopView, Spark | Text 100 chars, CTA driven |

## How to Use

### Basic Usage

```
Generate 5 Google Ads variations for a project management SaaS targeting startups
```

```
Create Meta ad copy for a B2B lead generation campaign about [product]
```

```
Write LinkedIn ads for promoting a webinar about [topic]
```

### Advanced Usage

```
Create an A/B test framework with 10 headline variations and 5 description variations for:
- Product: [description]
- Target: [audience]
- Goal: [conversions/awareness/leads]
- USP: [unique selling point]
```

## Output Format

### Google Ads (Responsive Search Ads)

```
CAMPAIGN: [Campaign Name]
TARGET AUDIENCE: [Description]
GOAL: [Conversions/Clicks/Awareness]

HEADLINES (15 required, 30 chars max each):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Value Props (5):
1. [Headline] (XX chars)
2. [Headline] (XX chars)
...

Features (5):
6. [Headline] (XX chars)
...

Social Proof (3):
11. [Headline] (XX chars)
...

CTAs (2):
14. [Headline] (XX chars)
15. [Headline] (XX chars)

DESCRIPTIONS (4 required, 90 chars max each):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
D1: [Primary value prop + CTA] (XX chars)
D2: [Feature list + differentiator] (XX chars)
D3: [Social proof + urgency] (XX chars)
D4: [Backup generic] (XX chars)

RECOMMENDED PINNING:
- Pin H1 to Position 1: [Best headline]
- Pin D1 to Position 1: [Best description]
```

### Meta Ads (Facebook/Instagram)

```
CAMPAIGN: [Campaign Name]
OBJECTIVE: [Traffic/Conversions/Lead Gen]
PLACEMENT: [Feed/Stories/Reels]

VARIATION 1:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Primary Text (125 chars for above-fold):
[Copy that hooks immediately]

Headline (40 chars):
[Benefit-focused headline]

Description (30 chars, optional):
[Supporting text]

CTA Button: [Learn More / Sign Up / Shop Now / Get Quote]

Full Primary Text (if needed):
[Expanded copy for longer format]

---
VARIATION 2:
[Same structure...]

A/B TEST RECOMMENDATION:
- Test 1: Headline A vs B (same primary)
- Test 2: Primary text short vs long
- Test 3: Different CTAs
```

### LinkedIn Ads

```
CAMPAIGN: [Campaign Name]
FORMAT: [Single Image / Carousel / Video / Message]
AUDIENCE: [Job titles, industries, company size]

VARIATION 1:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Introductory Text (150 chars for preview):
[Hook that resonates with professionals]

Full Intro (600 chars max):
[Expanded professional copy]

Headline (70 chars):
[Clear value proposition]

CTA: [Learn More / Download / Register / Request Demo]

---
VARIATION 2:
[Same structure...]
```

## Copywriting Frameworks

### AIDA (Awareness → Interest → Desire → Action)
```
Headline: [Attention-grabbing statement]
Body: [Build interest with benefits]
Desire: [Create want with proof/urgency]
CTA: [Clear action step]
```

### PAS (Problem → Agitate → Solution)
```
Problem: [State the pain point]
Agitate: [Make it worse/urgent]
Solution: [Your product as the answer]
```

### 4Ps (Promise → Picture → Proof → Push)
```
Promise: [What you'll deliver]
Picture: [Paint the transformed state]
Proof: [Evidence it works]
Push: [Urgency to act now]
```

### Before-After-Bridge
```
Before: [Current painful state]
After: [Desired future state]
Bridge: [Your solution gets them there]
```

## Platform-Specific Best Practices

### Google Ads
- Include keywords in headlines (improves Quality Score)
- Use numbers and stats ("Save 50%", "10x Faster")
- Include brand name in at least 2 headlines
- Use power words: Free, New, Exclusive, Limited, Proven
- Always include CTA: Get, Try, Start, Discover, Learn

### Meta Ads
- Hook in first 3 words (most scroll quickly)
- Use emojis sparingly for B2C, avoid for B2B
- Ask questions to increase engagement
- Social proof performs well (X customers trust us)
- Video: Hook in first 3 seconds

### LinkedIn Ads
- Professional tone, but not boring
- Lead with value, not sales pitch
- Industry-specific language builds credibility
- Stats and data resonate with B2B audience
- Thought leadership angle often outperforms direct sales

### TikTok Ads
- Casual, authentic tone (not corporate)
- Hook in first 1-2 seconds
- Trending sounds/formats increase reach
- User-generated content style performs best
- Strong CTA at the end

## A/B Testing Strategy

### Variables to Test

**Headlines**:
1. Question vs. Statement
2. Benefit-led vs. Feature-led
3. With numbers vs. Without
4. Short vs. Long
5. Emotional vs. Rational

**Primary Text**:
1. Short (1-2 sentences) vs. Long (paragraph)
2. Problem-focused vs. Solution-focused
3. First person vs. Second person
4. With social proof vs. Without
5. With urgency vs. Without

**CTAs**:
1. Direct ("Buy Now") vs. Soft ("Learn More")
2. Benefit-based ("Get Your Free Trial") vs. Action-based ("Start Now")

### Testing Protocol
1. Test one variable at a time
2. Run for minimum 7 days or 1000 impressions
3. 95% statistical significance before declaring winner
4. Document all tests and results
5. Apply learnings to future campaigns

## Example Output

**Input**: "Create Google Ads for a CRM software targeting small business owners"

**Output**:

```
CAMPAIGN: CRM-SMB-Search
TARGET: Small business owners, 5-50 employees
GOAL: Free trial signups

HEADLINES (30 chars max):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Value Props:
1. Grow Sales 3x Faster (20 chars)
2. Never Lose a Lead Again (22 chars)
3. CRM Built for Small Biz (23 chars)
4. Close Deals 50% Faster (21 chars)
5. Your Sales, Organized (19 chars)

Features:
6. Easy CRM - No Training (22 chars)
7. All-in-One Sales Tool (20 chars)
8. Mobile CRM App Included (23 chars)
9. Email + Phone + Tasks (20 chars)
10. Integrates with Gmail (20 chars)

Social Proof:
11. 10,000+ Businesses Trust Us (26 chars)
12. 4.9★ Rating on G2 (16 chars)
13. #1 CRM for Small Teams (21 chars)

CTAs:
14. Start Free Trial Today (21 chars)
15. Try Free for 14 Days (19 chars)

DESCRIPTIONS (90 chars max):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
D1: Simple CRM that helps small businesses close more deals. Start your free trial today. (88 chars)
D2: Track leads, manage contacts, and grow revenue. No complex setup. Works in minutes. (83 chars)
D3: Join 10,000+ small businesses. 4.9★ rated. Cancel anytime. Get started free. (76 chars)
D4: The CRM designed for growing businesses. Affordable plans starting at $29/mo. (77 chars)

RECOMMENDED PINNING:
- Pin "CRM Built for Small Biz" to Position 1
- Pin D1 to Position 1
```

## Integration

Works well with:
- **keyword-cluster-builder** - Find keywords to include in ad copy
- **competitive-ads-extractor** - Analyze competitor ad strategies
- **landing-page-copywriter** - Create matching landing page copy
- **social-media-analyzer** - Measure ad performance
