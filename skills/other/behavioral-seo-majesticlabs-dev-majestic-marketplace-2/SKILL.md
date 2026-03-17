---
name: behavioral-seo
description: Optimize for behavioral SEO signals including CTR, dwell time, engagement metrics, and Bing-specific factors.
---

# Behavioral SEO

Frameworks for optimizing user behavior signals that impact search rankings.

## Behavioral Metrics Impact

| Metric | Google Impact | Bing Impact | Optimization Focus |
|--------|---------------|-------------|-------------------|
| Click-through rate | High | High | Titles, meta, rich snippets |
| Dwell time | High | Very High | Content quality, intent match |
| Bounce rate | Medium | High | Relevance, page experience |
| Pages per session | Medium | High | Internal linking, related content |
| Return visits | Medium | High | Brand building, email capture |
| Social shares | Low | Very High | Shareable assets, social CTAs |

## CTR Optimization

### Title Tag Formulas

| Formula | Example | Best For |
|---------|---------|----------|
| Number + Outcome | "7 Ways to Boost Conversions" | Lists, how-tos |
| Year + Topic | "2024 Complete Guide to SEO" | Evergreen content |
| Question format | "What Is E-E-A-T? (And Why It Matters)" | Informational |
| Bracket power words | "[2024] | [Free] | [Proven]" | Any content |

### Meta Description Optimization

```
Structure: [Hook] + [Value Prop] + [CTA]

Example: "Struggling with low conversion rates?
This guide reveals 7 proven tactics used by top
e-commerce brands. Get the free checklist."
```

### Rich Snippet Opportunities

| Snippet Type | Markup | CTR Boost |
|--------------|--------|-----------|
| FAQ | FAQPage schema | +15-30% |
| How-to | HowTo schema | +10-20% |
| Review stars | Review schema | +20-35% |
| Table/list | Table markup | +10-20% |

## Dwell Time Optimization

| Factor | Implementation | Impact |
|--------|----------------|--------|
| Content-intent match | Align with search intent | Critical |
| Above-fold hook | Compelling intro, promise value | High |
| Scannable format | Headers, bullets, short paragraphs | High |
| Multimedia | Images, videos, interactive elements | Medium |
| Reading experience | Font size, line height, contrast | Medium |
| Internal links | Keep users exploring | Medium |

## Bounce Rate Reduction

| Issue | Cause | Fix |
|-------|-------|-----|
| High bounce | Intent mismatch | Rewrite for actual search intent |
| Quick exit | Poor first impression | Improve above-fold content |
| Mobile bounce | Bad mobile UX | Mobile-first design |
| Slow load | Page speed | Core Web Vitals optimization |

## Bing-Specific Optimization

Bing weights behavioral and social signals more heavily than Google.

### Key Bing Differences

| Factor | Google Weight | Bing Weight |
|--------|---------------|-------------|
| Social signals | Low | High |
| Fresh content | Medium | High |
| Behavioral metrics | High | Very High |
| Exact-match domains | Low | Medium |
| Image/video | Medium | High |

### Bing Optimization Tactics

1. **IndexNow** - Instant indexing for new content
   ```bash
   # Submit URL immediately
   curl "https://www.bing.com/indexnow?url={url}&key={key}"
   ```

2. **Bing Webmaster Tools** - Submit sitemap, monitor performance

3. **Social Integration**
   - Prominent share buttons
   - Social proof display
   - LinkedIn integration (Microsoft owned)

4. **Edge Browser Optimization**
   - Test in Microsoft Edge
   - Consider Edge-specific features

5. **Bing Places** - Local SEO for physical businesses

## Engagement Metrics

### Time on Page Targets

| Content Type | Target | Below Target Fix |
|--------------|--------|------------------|
| Blog post | 3-5 min | Add depth, multimedia |
| Landing page | 1-2 min | Clearer value prop, UX |
| Product page | 2-3 min | Better images, details |
| Pillar content | 7-10 min | More comprehensive coverage |

### Scroll Depth Goals

| Depth | Target % | Issue If Low |
|-------|----------|--------------|
| 25% | 80%+ | Weak intro, wrong audience |
| 50% | 60%+ | Content quality drop-off |
| 75% | 40%+ | Missing engagement elements |
| 100% | 30%+ | Content too long or poor CTA |

## Measurement

Track via:
- Google Search Console (CTR, impressions)
- Google Analytics (dwell, bounce, pages/session)
- Bing Webmaster Tools (Bing-specific)
- Heatmaps (scroll, click patterns)
