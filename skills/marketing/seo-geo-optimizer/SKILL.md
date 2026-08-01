---
name: seo-geo-optimizer
description: Comprehensive SEO/GEO/AEO analysis toolkit for optimizing content visibility across traditional search engines (Google, Bing), AI platforms (ChatGPT, Perplexity, Claude, Gemini, Grokipedia), answer engines (Google AI Overviews, Bing Copilot, featured snippets), voice assistants (Google Assistant, Siri, Alexa), and social media (Facebook, Twitter, LinkedIn, WhatsApp, Instagram). Analyzes HTML/Markdown/JSX files for metadata completeness, schema markup, keyword optimization, entity extraction, and generates multi-format audit reports with platform-specific recommendations.
author: Boris Djordjevic, 199 Biotechnologies
license: MIT. Complete terms in LICENSE
---

# SEO/GEO/AEO Optimizer Guide

## Overview

This skill analyzes content for SEO/GEO/AEO optimization across traditional search engines, AI platforms, and answer engines. Use it to audit content files, generate schema markup, validate metadata, extract keywords, and produce comprehensive reports with actionable recommendations.

**2025 Context**: AI-referred traffic grew 527% (Jan-May 2025). Content optimized for AI citation shows 33-40% higher visibility.

## Quick Start

### Comprehensive Audit

```bash
# Generate full audit report (JSON, Markdown, HTML)
python scripts/audit_report.py ~/project/about.html --format all

# Output: ~/Documents/SEO_Audit_YYYY-MM-DD_HH-MM-SS/
# - audit_report.json (raw data)
# - audit_report.md (readable text)
# - audit_report.html (visual dashboard)
```

### Content Analysis

```bash
# Analyze file structure and metadata
python scripts/analyze_content.py ~/project/page.html

# Output: JSON with meta tags, schema, content structure, issues, score
```

### Schema Generation

```bash
# Generate FAQ schema (highest AI citation probability)
python scripts/schema_generator.py faq \
  --question "What is longevity medicine?" \
  --answer "Longevity medicine optimizes biomarkers like LDL <70 mg/dL to reduce cardiovascular risk by 30-40%."

# Generate Article schema with E-E-A-T signals
python scripts/schema_generator.py article \
  --title "Understanding Biomarkers" \
  --author "Dr. Sarah Johnson" \
  --credentials "MD, PhD" \
  --date "2025-01-15"
```

### Content Optimization (Phase 2)

```bash
# Full optimization pipeline for specific platform
python scripts/auto_implementer.py page.html perplexity

# Optimize content structure (meta description, FAQ, data tables)
python scripts/content_optimizer.py page.html

# Platform-specific optimization
python scripts/platform_optimizer.py page.html chatgpt

# Check freshness (3.2x citations for content <30 days old)
python scripts/freshness_monitor.py page.html
```

## Core Operations

### 1. Metadata Validation

Validate meta tags, Open Graph, Twitter Cards, and schema completeness.

```bash
python scripts/metadata_validator.py ~/project/page.html
```

**Fix Critical Issues**:
- Title too short → Expand to 50-60 chars with brand name
- Missing og:image → Add 1200×630px image for social previews
- No schema → Generate FAQ/Article schema for AI citation

### 2. Keyword Analysis

Extract primary, semantic, long-tail, and question-based keywords with semantic clustering.

```bash
# Full analysis with clustering
python scripts/keyword_analyzer.py ~/project/page.html

# Fast mode without clustering
python scripts/keyword_analyzer.py ~/project/page.html --no-clusters
```

**Optimization Tips**:
- Primary keyword density: 1-3% (avoid stuffing)
- Add 3+ question keywords for voice search
- Long-tail phrases (3-4 words) for specificity
- Use keyword clusters to build pillar content strategy

### 3. Entity Extraction

Extract persons, organizations, places for Knowledge Graph optimization.

```bash
python scripts/entity_extractor.py ~/project/page.html
```

**E-E-A-T Signals** (+40% AI citation boost):
- Add full names with credentials (MD, PhD, MBA)
- Include institutional affiliations (Stanford, Harvard)
- Link to external profiles (Google Scholar, LinkedIn)

### 4. Schema Markup Generation

Generate JSON-LD schemas for AI platforms.

#### FAQ Schema (Highest Citation Probability)

```bash
python scripts/schema_generator.py faq \
  --question "What is optimal LDL cholesterol?" \
  --answer "Optimal LDL for longevity is <70 mg/dL, reducing cardiovascular risk by 30-40%."
```

**Voice Search Optimization**:
- Answers ≤29 words for voice assistants
- Natural language questions
- Direct, specific answers

### 5. IndexNow Instant Indexing

Submit URLs directly to search engines for immediate indexing (Bing, Yandex, Seznam, Naver).

```bash
# Generate key (one-time setup)
python scripts/indexnow_submit.py --generate-key --output ./public

# Submit URL after publishing
python scripts/indexnow_submit.py https://yoursite.com/new-page --key YOUR_KEY

# Batch submit
python scripts/indexnow_submit.py --batch urls.txt --key YOUR_KEY
```

**GEO Impact**:
- Bing index feeds AI platforms (ChatGPT, Perplexity, Claude)
- Content indexed in minutes vs weeks
- 3.2x citation boost for fresh content (<30 days)

## Platform Optimization

### ChatGPT (Depth & Authority)
- Comprehensive coverage (1500-2500 words)
- Author credentials prominent (MD, PhD, MBA)
- Citations to primary sources (PubMed, arXiv)
- Evidence-based claims with statistics

### Perplexity (Freshness & Citations)
- Recent `dateModified` (update weekly)
- Inline citations with links
- Specialized, deep-dive content
- Current statistics (2024-2025)

### Claude (Accuracy & Primary Sources)
- Primary source citations only
- Methodology transparent
- Limitations acknowledged
- Data availability stated

### Gemini (Community & Local)
- User reviews and ratings
- Google Business Profile optimized
- Local citations (NAP consistency)
- Traditional authority signals

### Grokipedia (xAI, Transparency & RAG)
- RAG-based citations (20-30% better factual consistency)
- Transparent version history and licensing
- Primary source attribution (publisher + year)
- Wikipedia-derived content requires CC-BY-SA attribution

## AI Citation Optimization

### TL;DR Strategy (+35% Citation Boost)

Place direct answer in first 60 words.

### E-E-A-T Signals (+40% Citation Boost)

**Author Credentials**:
```markdown
**Author**: Dr. Sarah Johnson, MD, PhD, FAAD
**Affiliation**: Stanford School of Medicine
**Published**: 2025-01-15 | **Updated**: 2025-11-11
```

### Voice Search Optimization

**29-Word Answers** for voice assistants.

## Reference Documentation

For detailed guides and templates, see the `reference/` directory:

**Optimization Guides**:
- `citation-optimization-guide.md` - AI citation strategies
- `entity-seo-guide.md` - Knowledge Graph optimization
- `platform-strategies.md` - Platform-specific optimization
- `voice-search-guide.md` - Voice search optimization
- `social-preview-guide.md` - Open Graph, Twitter Cards
- `schema-library.md` - Complete JSON-LD reference

**Templates** (`templates/` directory):
- `meta-tags-template.html` - Complete meta tags
- Schema templates (FAQ, Article, HowTo, Breadcrumb, Organization, Person)

**Industry Examples** (`examples/` directory):
- `medical-clinic/` - Healthcare optimization (15/100 → 92/100)
- `consulting-firm/` - B2B entity SEO (22/100 → 89/100)
- `saas-landing-page/` - LLMO optimization (18/100 → 94/100)

## Common Issues & Solutions

### Low AI Citation Rate

**Solutions**:
1. Add TL;DR in first 60 words (+35% boost)
2. Display author credentials (MD, PhD) (+40% boost)
3. Link to primary sources (PubMed, arXiv)
4. Update `dateModified` weekly
5. Add FAQ schema (highest citation probability)

### Poor Social Media Previews

**Solutions**:
1. Add 1200×630px og:image
2. Use absolute URLs (https://...)
3. Include og:title and og:description
4. Test with platform validators

### Knowledge Graph Not Showing

**Solutions**:
1. Add Organization schema to homepage
2. Create Person schema for key individuals
3. Ensure NAP consistency across web
4. Link external profiles (LinkedIn, Wikipedia)
5. Claim Google Business Profile

## Performance Notes

**Script Execution Times**:
- `analyze_content.py`: <1 second
- `metadata_validator.py`: <1 second
- `keyword_analyzer.py`: <2 seconds
- `entity_extractor.py`: <1 second
- `schema_generator.py`: <1 second
- `audit_report.py`: 3-5 seconds

**Requirements**:
- Python 3.7+
- Stdlib only (no external dependencies)
- Works offline

## Script Reference

**Phase 1: Analysis**:
- `analyze_content.py <file>` - Extract metadata, schema, structure
- `metadata_validator.py <file>` - Validate meta tags, OG, Twitter Cards
- `keyword_analyzer.py <file>` - Extract keywords
- `entity_extractor.py <file>` - Extract entities
- `audit_report.py <file> [options]` - Generate audit reports

**Phase 2: Implementation**:
- `content_optimizer.py <file>` - Rewrite content (meta description, FAQ, data tables)
- `platform_optimizer.py <file> <platform>` - Platform-specific (chatgpt, perplexity, claude, gemini, grokipedia)
- `voice_optimizer.py <file>` - Add voice search optimization (Speakable schema)
- `freshness_monitor.py <file>` - Check content age, recommend updates
- `citation_enhancer.py <file>` - Identify citation opportunities (+41% impact)
- `auto_implementer.py <file> [platform]` - Full optimization pipeline

**Generation**:
- `schema_generator.py <type> [options]` - Generate JSON-LD schemas

**Indexing**:
- `indexnow_submit.py <url> --key KEY` - Submit URL to search engines instantly
- `indexnow_submit.py --batch <file> --key KEY` - Batch submit URLs
- `indexnow_submit.py --generate-key` - Generate IndexNow key

**Supported Files**: HTML, Markdown, React/JSX
**Output Formats**: JSON, Markdown, HTML

## 2025 Statistics

**AI Citation Impact**:
- 527% AI traffic growth (Jan-May 2025)
- 40.58% citations from top 10 SERP results
- +35% boost with TL;DR in first 60 words
- +40% boost with author credentials
- +40% boost with proper heading hierarchy

**Voice Search**:
- 29-word answers optimal
- FAQ schema: highest citation probability
- 80% of voice answers from top 3 results

**Social Media**:
- 1200×630px standard across platforms (Facebook, LinkedIn, WhatsApp)
- Instagram: 1080×1920px for Stories, 1080×1350px for Feed, bio link optimization
- 3x engagement with proper previews
- +250% WhatsApp/iMessage share rate with og:image

## License

MIT License. See LICENSE file for complete terms.
