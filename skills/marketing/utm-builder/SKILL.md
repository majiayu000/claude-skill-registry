---
name: utm-builder
description: Generate UTM-tagged URLs for campaign tracking. Create consistent, organized tracking links for Google Analytics, HubSpot, and other analytics platforms. Supports bulk generation, naming conventions, and campaign documentation. Use when creating tracking links, campaign URLs, or organizing marketing attribution.
---

# UTM Builder

Generate consistent, well-organized UTM tracking links for marketing campaigns.

## UTM Parameters

| Parameter | Required | Purpose | Example |
|-----------|----------|---------|---------|
| `utm_source` | Yes | Traffic source | google, linkedin, newsletter |
| `utm_medium` | Yes | Marketing medium | cpc, email, social, organic |
| `utm_campaign` | Yes | Campaign name | spring-sale-2025 |
| `utm_term` | No | Paid search keywords | project+management |
| `utm_content` | No | Differentiate variants | cta-button, hero-image |

## Naming Conventions

### Recommended Format
```
utm_source:    {platform}
utm_medium:    {channel-type}
utm_campaign:  {yyyy-mm}-{campaign-name}
utm_term:      {keyword} (paid search only)
utm_content:   {ad-variant}-{placement}
```

### Source Values (lowercase, no spaces)
```
Paid:
  - google
  - linkedin
  - meta (facebook + instagram)
  - tiktok
  - twitter
  - bing

Organic Social:
  - linkedin-organic
  - twitter-organic
  - facebook-organic

Email:
  - mailchimp
  - hubspot
  - sendgrid
  - newsletter

Referral:
  - partner-{name}
  - affiliate-{name}
  - referral
```

### Medium Values
```
Paid:
  - cpc (cost per click)
  - cpm (cost per impression)
  - display
  - video
  - retargeting

Organic:
  - organic
  - social
  - referral

Direct:
  - email
  - sms
  - push

Content:
  - blog
  - pr
  - podcast
  - webinar
```

### Campaign Naming
```
Format: {date}-{name}-{segment}

Examples:
  - 2025-03-spring-promo
  - 2025-q1-product-launch
  - 2025-04-webinar-ai-trends
  - 2025-03-ebook-marketing-guide
  - evergreen-demo-request
```

## How to Use

### Single URL

```
Create a UTM link for:
URL: https://example.com/pricing
Campaign: Spring promotion on LinkedIn
```

**Output**:
```
https://example.com/pricing?utm_source=linkedin&utm_medium=cpc&utm_campaign=2025-03-spring-promo
```

### Bulk Generation

```
Create UTM links for a multi-channel campaign:
URL: https://example.com/demo
Campaign: Q2 Product Launch

Channels:
- Google Search Ads
- LinkedIn Sponsored Content
- Email newsletter
- Twitter organic post
```

**Output**:
```
═══════════════════════════════════════════════════════════════
CAMPAIGN: Q2 Product Launch
BASE URL: https://example.com/demo
DATE: 2025-Q2
═══════════════════════════════════════════════════════════════

GOOGLE SEARCH ADS:
──────────────────────────────────────────────────────────────
https://example.com/demo?utm_source=google&utm_medium=cpc&utm_campaign=2025-q2-product-launch&utm_term={keyword}

Use {keyword} placeholder for dynamic keyword insertion.

LINKEDIN SPONSORED:
──────────────────────────────────────────────────────────────
Variant A (Image):
https://example.com/demo?utm_source=linkedin&utm_medium=cpc&utm_campaign=2025-q2-product-launch&utm_content=image-a

Variant B (Video):
https://example.com/demo?utm_source=linkedin&utm_medium=cpc&utm_campaign=2025-q2-product-launch&utm_content=video-b

EMAIL NEWSLETTER:
──────────────────────────────────────────────────────────────
Header CTA:
https://example.com/demo?utm_source=newsletter&utm_medium=email&utm_campaign=2025-q2-product-launch&utm_content=header-cta

Footer CTA:
https://example.com/demo?utm_source=newsletter&utm_medium=email&utm_campaign=2025-q2-product-launch&utm_content=footer-cta

TWITTER ORGANIC:
──────────────────────────────────────────────────────────────
https://example.com/demo?utm_source=twitter-organic&utm_medium=social&utm_campaign=2025-q2-product-launch

═══════════════════════════════════════════════════════════════
TRACKING SPREADSHEET
═══════════════════════════════════════════════════════════════
| Channel | Source | Medium | Campaign | Content | Full URL |
|---------|--------|--------|----------|---------|----------|
| Google | google | cpc | 2025-q2-product-launch | - | [url] |
| LinkedIn | linkedin | cpc | 2025-q2-product-launch | image-a | [url] |
| LinkedIn | linkedin | cpc | 2025-q2-product-launch | video-b | [url] |
| Email | newsletter | email | 2025-q2-product-launch | header-cta | [url] |
| Email | newsletter | email | 2025-q2-product-launch | footer-cta | [url] |
| Twitter | twitter-organic | social | 2025-q2-product-launch | - | [url] |
```

### A/B Test Links

```
Create UTM links for A/B testing two landing pages:
URL A: https://example.com/landing-v1
URL B: https://example.com/landing-v2
Campaign: Homepage redesign test
Channel: Google Ads
```

**Output**:
```
VARIANT A (Control):
https://example.com/landing-v1?utm_source=google&utm_medium=cpc&utm_campaign=2025-03-homepage-test&utm_content=control-v1

VARIANT B (Treatment):
https://example.com/landing-v2?utm_source=google&utm_medium=cpc&utm_campaign=2025-03-homepage-test&utm_content=treatment-v2

TRACKING NOTE:
Compare conversion rates in Google Analytics:
Acquisition → Traffic Acquisition → Filter by utm_content
```

## Platform-Specific Tips

### Google Ads
```
Use ValueTrack parameters for dynamic insertion:
- {keyword} - Search keyword
- {matchtype} - Match type (e, p, b)
- {device} - Device (m, t, c)
- {adposition} - Ad position

Example:
?utm_source=google&utm_medium=cpc&utm_campaign=brand&utm_term={keyword}&utm_content={adposition}
```

### LinkedIn Ads
```
Use LinkedIn macros:
- {{CAMPAIGN_NAME}}
- {{CREATIVE_NAME}}
- {{CAMPAIGN_GROUP_NAME}}

Note: LinkedIn auto-appends some tracking; combine carefully.
```

### Meta (Facebook/Instagram)
```
Use URL parameters in ad setup:
- {{ad.name}}
- {{adset.name}}
- {{campaign.name}}

Example:
?utm_source=meta&utm_medium=cpc&utm_campaign={{campaign.name}}&utm_content={{ad.name}}
```

### HubSpot Integration
```
HubSpot auto-recognizes UTM parameters.
Ensure consistency with HubSpot campaign naming.

Best practice:
- Create HubSpot campaign first
- Use exact campaign name in utm_campaign
- Tag all assets (emails, pages, ads) with same campaign
```

## Short URL Integration

For social media, use URL shorteners that preserve UTM:
- **Bitly** - Tracks clicks, preserves UTMs
- **Rebrandly** - Custom branded domains
- **Short.io** - Team features

Example workflow:
1. Generate full UTM URL
2. Shorten with Bitly
3. Use short URL in social posts
4. UTMs still tracked in Google Analytics

## Common Mistakes to Avoid

| Mistake | Problem | Solution |
|---------|---------|----------|
| Inconsistent capitalization | Creates duplicate campaigns in GA | Always use lowercase |
| Spaces in parameters | Breaks URL | Use hyphens or underscores |
| Missing utm_medium | Poor channel attribution | Always include medium |
| Generic campaign names | Hard to analyze | Use date + descriptive name |
| Not documenting | Lost tracking context | Maintain spreadsheet |
| Duplicate utm_source | Confusion in reporting | Standardize naming |

## UTM Audit

### Checklist
- [ ] All lowercase (no mixed case)
- [ ] No spaces (use hyphens)
- [ ] Consistent naming across team
- [ ] Campaign includes date prefix
- [ ] Medium matches channel type
- [ ] Content differentiates variants
- [ ] Documented in tracking spreadsheet

### Analytics Verification
After launching, verify in GA4:
1. Go to Reports → Acquisition → Traffic acquisition
2. Add secondary dimension: Session source/medium
3. Filter by campaign name
4. Confirm data is populating correctly

## Template Library

### Email Campaigns
```
Newsletter:
?utm_source=newsletter&utm_medium=email&utm_campaign={date}-{topic}&utm_content={position}

Drip Sequence:
?utm_source=hubspot&utm_medium=email&utm_campaign={sequence-name}&utm_content=email-{number}

Transactional:
?utm_source=transactional&utm_medium=email&utm_campaign=order-confirmation
```

### Social Media
```
Organic Post:
?utm_source={platform}-organic&utm_medium=social&utm_campaign={date}-{topic}

Paid Social:
?utm_source={platform}&utm_medium=cpc&utm_campaign={date}-{campaign}&utm_content={creative-name}
```

### Content Marketing
```
Blog Post:
?utm_source=blog&utm_medium=organic&utm_campaign={post-slug}

Guest Post:
?utm_source={publication}&utm_medium=referral&utm_campaign=guest-post-{date}

Podcast:
?utm_source={podcast-name}&utm_medium=podcast&utm_campaign={episode}
```

### Partnerships
```
Co-Marketing:
?utm_source=partner-{name}&utm_medium=referral&utm_campaign={joint-campaign}

Affiliate:
?utm_source=affiliate-{name}&utm_medium=referral&utm_campaign=affiliate-program
```

## Integration

Works well with:
- **analytics-interpretation** - Analyze UTM performance
- **marketing-demand-acquisition** - Track paid campaign ROI
- **social-media-analyzer** - Measure social campaign results
- **email-template-generator** - Add tracking to email campaigns
