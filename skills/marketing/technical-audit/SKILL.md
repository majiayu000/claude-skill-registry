---
name: technical-audit
description: Technical SEO audit methodology including crawlability, indexability, and Core Web Vitals analysis. Use when auditing pages or sites for technical SEO issues.
---

# Technical Audit

## When to Use

- Auditing pages for technical SEO issues
- Analyzing Core Web Vitals performance
- Checking schema markup implementation
- Validating crawlability and indexability

## Audit Categories

### 1. Indexability

| Check | Requirement | Severity |
|-------|-------------|----------|
| Title Tag | Present, 50-60 chars, contains keyword | CRITICAL |
| Meta Description | Present, 150-160 chars | HIGH |
| Canonical Tag | Present, self-referencing or correct | HIGH |
| Robots Meta | No noindex on important pages | CRITICAL |
| Robots.txt | Not blocking important content | CRITICAL |

### 2. Content Structure

| Check | Requirement | Severity |
|-------|-------------|----------|
| H1 Tag | Exactly 1, contains keyword | CRITICAL |
| Heading Hierarchy | H1 -> H2 -> H3 (no skips) | HIGH |
| Word Count | Meets or exceeds competitor benchmark | MEDIUM |
| Content Uniqueness | No duplicate content issues | HIGH |

### 3. Core Web Vitals

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | <2.5s | 2.5s-4.0s | >4.0s |
| INP (Interaction to Next Paint) | <200ms | 200ms-500ms | >500ms |
| CLS (Cumulative Layout Shift) | <0.1 | 0.1-0.25 | >0.25 |

**Measurement Methods:**
1. Chrome DevTools MCP (preferred)
2. PageSpeed Insights API
3. Lighthouse CLI
4. Manual measurement via web.dev

### 4. Schema Markup

| Page Type | Recommended Schema |
|-----------|-------------------|
| Article/Blog | Article, BlogPosting |
| FAQ page | FAQPage |
| How-to guide | HowTo |
| Product page | Product |
| Local business | LocalBusiness |
| Person/Author | Person |

### 5. Links

| Check | Requirement | Severity |
|-------|-------------|----------|
| Internal Links | Minimum 3 per page | HIGH |
| Broken Links | 0 | CRITICAL |
| External Links | At least 1 authoritative | LOW |
| Orphan Pages | 0 (all pages linked from somewhere) | MEDIUM |

## Audit Process

### Step 1: Fetch Page
```bash
# Use WebFetch or curl
curl -s "$URL" > page.html
```

### Step 2: Parse Structure
- Extract title, meta description, canonical
- Map heading hierarchy
- Count words
- List all links

### Step 3: Analyze Performance
- Use PageSpeed Insights API or Chrome DevTools MCP
- Document all Core Web Vitals
- Note specific issues (large images, render-blocking JS)

### Step 4: Check Schema
- Look for JSON-LD in page source
- Validate using Google Rich Results Test
- Note missing or incomplete properties

### Step 5: Score and Report
- Calculate overall score (0-100)
- List all issues by severity
- Provide specific fix recommendations

## Output Format

```markdown
## Technical SEO Audit Report

**URL**: {url}
**Date**: {date}
**Overall Score**: {score}/100

### Core Web Vitals
| Metric | Value | Status |
|--------|-------|--------|
| LCP | {value}s | GOOD/NEEDS IMPROVEMENT/POOR |
| INP | {value}ms | GOOD/NEEDS IMPROVEMENT/POOR |
| CLS | {value} | GOOD/NEEDS IMPROVEMENT/POOR |

**Measurement Method**: {Chrome DevTools MCP | PageSpeed API | Lighthouse | Manual}

### Issues Found

**CRITICAL ({count})**:
1. {issue} - {location} - {fix recommendation}

**HIGH ({count})**:
1. {issue} - {location} - {fix recommendation}

**MEDIUM ({count})**:
1. {issue} - {location} - {fix recommendation}

### Recommendations
1. {priority fix 1}
2. {priority fix 2}
3. {priority fix 3}
```
