---
name: gsc-optimization
description: Generic Google Search Console optimization patterns for any website. Use when analyzing search performance, keyword rankings, or SEO metrics. Framework for project-specific implementations.
---

# GSC Optimization Framework

Generic patterns for Google Search Console analysis and SEO optimization.

## When to Use

- Analyzing keyword rankings
- Monitoring search performance
- Identifying SEO opportunities
- Tracking CTR and impressions
- Competitor keyword research

## NOT Project-Specific

This is a **framework skill** providing generic patterns. For project-specific implementations:
- Create implementation skill in your project
- Reference this framework with `extends: "analytics-framework/gsc-optimization"`
- Add project-specific keywords via skill.config.json

## Core Concepts

### GSC Metrics

| Metric | Description | Good Target |
|--------|-------------|-------------|
| **Impressions** | How often your site appears in search | Growing trend |
| **Clicks** | Actual visits from search | 3-5% CTR |
| **CTR** | Click-through rate (clicks/impressions) | >3% |
| **Position** | Average ranking position | <10 (first page) |

### Keyword Research Strategy

```
1. Find high-impression, low-CTR keywords → Optimize titles/descriptions
2. Track position 11-20 keywords → Push to first page
3. Identify declining keywords → Content refresh needed
4. Monitor branded vs non-branded → Brand awareness
```

## Implementation Patterns

### 1. Setup @akson Analytics Package

```bash
npm install @akson/cortex-analytics @akson/cortex-gsc
```

### 2. Configure Service Account

```bash
# 1. Create service account in Google Cloud Console
# 2. Enable Google Search Console API
# 3. Add service account email to GSC property
#    - Go to https://search.google.com/search-console
#    - Select property → Settings → Users and permissions
#    - Add service account email with "Full" permission
# 4. Download JSON key and store securely
```

**Environment Variables:**
```bash
GSC_SITE_URL="https://your-domain.com"
GOOGLE_SERVICE_ACCOUNT_KEY_FILE="config/gsc-automation.json"
```

### 3. Keyword Ranking Analysis

```bash
# Check rankings for specific keywords
npx @akson/cortex-analytics gsc rankings \
  -k "keyword 1" "keyword 2" "keyword 3" \
  -s 2024-01-01 -e 2024-01-31

# Top performing pages
npx @akson/cortex-analytics gsc top-pages \
  -s 2024-01-01 -e 2024-01-31 --limit 20

# Top keywords
npx @akson/cortex-analytics gsc top-keywords \
  -s 2024-01-01 -e 2024-01-31 --limit 50

# Comprehensive report
npx @akson/cortex-analytics gsc comprehensive-report \
  -s 2024-01-01 -e 2024-01-31 --output report.json
```

### 4. Programmatic Analysis

```typescript
import { GSCService } from '@akson/cortex-gsc';

async function analyzeKeywords() {
  const gsc = new GSCService({
    siteUrl: process.env.GSC_SITE_URL!,
    keyFile: process.env.GOOGLE_SERVICE_ACCOUNT_KEY_FILE!
  });

  // Get keyword performance
  const keywords = await gsc.getKeywordPerformance({
    startDate: '2024-01-01',
    endDate: '2024-01-31',
    keywords: ['keyword1', 'keyword2']
  });

  // Analyze opportunities
  const opportunities = keywords.filter(k =>
    k.impressions > 1000 && k.ctr < 0.03 // High impressions, low CTR
  );

  return opportunities;
}
```

## Optimization Strategies

### 1. Title & Description Optimization

**Problem:** High impressions, low CTR (< 3%)

**Solution:** Optimize meta titles and descriptions

```html
<!-- Before: Generic title -->
<title>Home Page</title>
<meta name="description" content="Welcome to our website">

<!-- After: Keyword-rich, compelling -->
<title>Custom Military Badges | Swiss Army Merchandise | MyArmy.ch</title>
<meta name="description" content="Premium custom military badges for Swiss Army personnel. High-quality funktionsabzeichen with free design. Order today!">
```

**Expected Impact:**
- CTR increase: 50-100%
- Impressions: May decrease initially (more targeted)
- Clicks: Should increase 2-3x

### 2. Content Gap Analysis

**Find keywords where competitors rank but you don't:**

```typescript
async function findContentGaps(yourKeywords: string[], competitorKeywords: string[]) {
  const gaps = competitorKeywords.filter(k => !yourKeywords.includes(k));
  return gaps.sort((a, b) => b.impressions - a.impressions);
}
```

**Action:** Create content targeting gap keywords

### 3. Position Improvement Strategy

**Target:** Keywords ranking position 11-20 (page 2)

**Tactics:**
1. Add 300-500 words of relevant content
2. Improve internal linking
3. Add schema markup
4. Optimize images with alt text
5. Build 2-3 quality backlinks

**Timeline:** 2-4 weeks to see movement

### 4. Declining Keyword Recovery

**Warning Signs:**
- Position drops >5 spots
- Impressions down >30%
- CTR declining

**Recovery Actions:**
```
1. Check page still exists (not 404)
2. Verify content hasn't been removed
3. Update publish date
4. Refresh statistics and data
5. Add new section with recent info
6. Check for algorithm updates
```

## Tracking & Monitoring

### Weekly Keyword Report

```bash
# Create automated report
cat > scripts/weekly-seo-report.sh << 'EOF'
#!/bin/bash
DATE=$(date +%Y-%m-%d)
npx @akson/cortex-analytics gsc comprehensive-report \
  -s $(date -d '7 days ago' +%Y-%m-%d) \
  -e $DATE \
  --output "reports/seo-$DATE.json"
EOF

chmod +x scripts/weekly-seo-report.sh

# Run weekly with cron
crontab -e
# Add: 0 9 * * 1 /path/to/weekly-seo-report.sh
```

### Alert Thresholds

```typescript
interface SEOAlert {
  keyword: string;
  type: 'opportunity' | 'warning' | 'critical';
  reason: string;
}

function checkAlerts(data: KeywordData[]): SEOAlert[] {
  const alerts: SEOAlert[] = [];

  data.forEach(kw => {
    // Opportunity: High impressions, low CTR
    if (kw.impressions > 1000 && kw.ctr < 0.03) {
      alerts.push({
        keyword: kw.query,
        type: 'opportunity',
        reason: `High impressions (${kw.impressions}), low CTR (${(kw.ctr * 100).toFixed(1)}%)`
      });
    }

    // Warning: Position drop
    if (kw.positionChange < -5) {
      alerts.push({
        keyword: kw.query,
        type: 'warning',
        reason: `Position dropped ${Math.abs(kw.positionChange)} spots`
      });
    }

    // Critical: First page to second page
    if (kw.previousPosition <= 10 && kw.position > 10) {
      alerts.push({
        keyword: kw.query,
        type: 'critical',
        reason: `Fell from page 1 to page 2`
      });
    }
  });

  return alerts;
}
```

## Configuration Requirements

**Environment Variables:**
- `GSC_SITE_URL` - Your website URL (must match GSC property)
- `GOOGLE_SERVICE_ACCOUNT_KEY_FILE` - Path to service account JSON

**Service Account Permissions:**
- Added to GSC property with "Full" access
- `webmasters.readonly` scope

**Target Keywords:**
Define in skill.config.json:
```json
{
  "configuration": {
    "primary_keywords": ["keyword1", "keyword2"],
    "secondary_keywords": ["keyword3", "keyword4"],
    "brand_keywords": ["brand", "company name"]
  }
}
```

## Key Rules

### DO:
- Track keyword trends over time (not single snapshots)
- Focus on intent-driven keywords (not just volume)
- Monitor both branded and non-branded terms
- Set realistic CTR targets based on position
- Analyze competitor rankings
- Document changes and their impact

### DON'T:
- Obsess over daily fluctuations (use weekly/monthly trends)
- Ignore high-impression, low-CTR keywords
- Target keywords without search intent match
- Forget to check mobile vs desktop performance
- Neglect position 11-20 keywords (low-hanging fruit)
- Make multiple changes at once (can't measure impact)

## SEO Best Practices

### 1. Content-to-Keyword Match

```
Keyword Intent → Content Type
- Informational ("what is X") → Guide/Tutorial
- Commercial ("best X") → Comparison/Review
- Transactional ("buy X") → Product Page
- Navigational ("X login") → Landing Page
```

### 2. Internal Linking Strategy

```
Homepage
├── Category Pages (target: 3-5 keywords each)
│   └── Product/Article Pages (target: 1-2 keywords)
└── About/Contact (brand keywords)
```

### 3. Schema Markup

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Custom Military Badge",
  "description": "High-quality swiss army badge",
  "brand": "MyArmy",
  "offers": {
    "@type": "Offer",
    "price": "149.90",
    "priceCurrency": "CHF"
  }
}
```

## Resources

- **@akson/cortex-gsc**: GSC analysis package
- **@akson/cortex-analytics**: Unified analytics CLI
- **GSC API Docs**: https://developers.google.com/webmaster-tools
- **Search Quality Guidelines**: https://developers.google.com/search/docs/fundamentals/creating-helpful-content

## Example Implementations

See project-specific skills that extend this framework:
- `myarmy-skills/seo-myarmy` - Swiss military keyword optimization
- Your implementation here!
