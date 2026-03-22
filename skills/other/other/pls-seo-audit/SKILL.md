---
name: seo-audit
description: Scan content and websites for SEO gaps, identify opportunities to outrank competitors. Use when: (1) Analyzing page SEO, (2) Checking meta tags and structured data, (3) Reviewing content for keyword optimization, (4) Auditing technical SEO factors.
---

# SEO Audit

Comprehensive SEO analysis for content and websites.

## Quick Audit Checklist

### On-Page SEO

```markdown
- [ ] Title tag (50-60 chars, keyword near front)
- [ ] Meta description (150-160 chars, compelling)
- [ ] H1 tag (one per page, includes target keyword)
- [ ] H2-H6 hierarchy (logical structure)
- [ ] Image alt text (descriptive, keyword-relevant)
- [ ] Internal links (3-5 per page minimum)
- [ ] URL structure (short, descriptive, hyphens)
- [ ] Canonical tags (prevent duplicate content)
```

### Technical SEO

```markdown
- [ ] Page speed (<3s load time)
- [ ] Mobile-friendly (responsive design)
- [ ] HTTPS (SSL certificate valid)
- [ ] XML sitemap (submitted to Search Console)
- [ ] Robots.txt (properly configured)
- [ ] Structured data (Schema.org markup)
- [ ] Core Web Vitals (LCP, FID, CLS)
```

### Content Quality

```markdown
- [ ] Keyword in first 100 words
- [ ] Content length matches intent
- [ ] No keyword stuffing (<2% density)
- [ ] Readable (Flesch-Kincaid score)
- [ ] Unique value (not duplicate content)
- [ ] Fresh content (updated regularly)
```

---

## Technical SEO Commands

### Page Speed Analysis

```bash
# Using PageSpeed Insights API
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&strategy=mobile"

# Using lighthouse locally
npx lighthouse https://example.com --view
```

### Check Robots.txt

```bash
curl https://example.com/robots.txt
```

### Check Sitemap

```bash
curl https://example.com/sitemap.xml | xmllint --format -
```

### SSL Certificate Check

```bash
openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -dates
```

### Mobile-Friendly Test

```bash
# Google's Mobile-Friendly Test API
curl "https://searchconsole.googleapis.com/v1/urlTestingTools/mobileFriendlyTest:run?key=YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

---

## Content Analysis

### Keyword Density

```python
import re
from collections import Counter

def keyword_density(text, keyword):
    words = re.findall(r'\b\w+\b', text.lower())
    keyword_count = text.lower().count(keyword.lower())
    density = (keyword_count / len(words)) * 100
    return {
        "keyword": keyword,
        "count": keyword_count,
        "total_words": len(words),
        "density": f"{density:.2f}%"
    }

# Target: 1-2% density
```

### Readability Score

```python
import textstat

text = "Your content here..."

flesch = textstat.flesch_reading_ease(text)
# 90-100: Very Easy
# 60-70: Standard
# 0-30: Very Difficult

grade = textstat.flesch_kincaid_grade(text)
# Target: 8-9 for general audience
```

### Content Structure Analysis

```python
from bs4 import BeautifulSoup

def analyze_headings(html):
    soup = BeautifulSoup(html, 'html.parser')
    headings = {
        'h1': soup.find_all('h1'),
        'h2': soup.find_all('h2'),
        'h3': soup.find_all('h3'),
    }
    
    issues = []
    if len(headings['h1']) == 0:
        issues.append("Missing H1 tag")
    elif len(headings['h1']) > 1:
        issues.append("Multiple H1 tags (should be one)")
    
    return {
        "counts": {k: len(v) for k, v in headings.items()},
        "issues": issues
    }
```

---

## Meta Tag Analysis

### Extract Meta Tags

```python
from bs4 import BeautifulSoup
import requests

def audit_meta_tags(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find('title')
    description = soup.find('meta', attrs={'name': 'description'})
    keywords = soup.find('meta', attrs={'name': 'keywords'})
    
    issues = []
    
    if not title or len(title.text) < 30:
        issues.append("Title too short or missing")
    elif len(title.text) > 60:
        issues.append("Title too long (>60 chars)")
    
    if not description:
        issues.append("Meta description missing")
    elif len(description.get('content', '')) < 120:
        issues.append("Meta description too short")
    elif len(description.get('content', '')) > 160:
        issues.append("Meta description too long")
    
    return {
        "title": title.text if title else None,
        "description": description.get('content') if description else None,
        "issues": issues
    }
```

---

## Structured Data Check

### Validate Schema Markup

```bash
# Using Google's Rich Results Test
curl "https://searchconsole.googleapis.com/v1/urlTestingTools/richResultsTest:run" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

### Common Schema Types

```json
// Article
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Title",
  "author": {"@type": "Person", "name": "Author"},
  "datePublished": "2026-01-01"
}

// Local Business
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Business Name",
  "address": {"@type": "PostalAddress", "streetAddress": "123 Main"},
  "telephone": "+1-555-555-5555"
}

// FAQ
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "Question?",
    "acceptedAnswer": {"@type": "Answer", "text": "Answer"}
  }]
}
```

---

## Competitor Analysis

### Compare Page Metrics

```python
import requests
from bs4 import BeautifulSoup

def compare_seo(target_url, competitor_url):
    def get_metrics(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return {
            "title_len": len(soup.find('title').text) if soup.find('title') else 0,
            "h1_count": len(soup.find_all('h1')),
            "h2_count": len(soup.find_all('h2')),
            "word_count": len(soup.get_text().split()),
            "images": len(soup.find_all('img')),
            "images_no_alt": len([i for i in soup.find_all('img') if not i.get('alt')])
        }
    
    return {
        "target": get_metrics(target_url),
        "competitor": get_metrics(competitor_url)
    }
```

---

## SEO Audit Report Template

```markdown
# SEO Audit Report

## Summary
- **Score:** X/100
- **Critical Issues:** X
- **Warnings:** X
- **Passed:** X

## Critical Issues
1. [Issue description]
   - Impact: [High/Medium/Low]
   - Fix: [Recommended action]

## Technical SEO
| Factor | Status | Notes |
|--------|--------|-------|
| Page Speed | ⚠️ | 4.2s load time |
| Mobile | ✅ | Responsive |
| HTTPS | ✅ | Valid SSL |
| Sitemap | ✅ | Submitted |

## On-Page SEO
| Factor | Status | Notes |
|--------|--------|-------|
| Title | ✅ | 55 chars |
| Meta Desc | ⚠️ | Too short |
| H1 | ✅ | Present |
| Images | ⚠️ | 3 missing alt |

## Recommendations
1. [Priority 1]
2. [Priority 2]
3. [Priority 3]
```
