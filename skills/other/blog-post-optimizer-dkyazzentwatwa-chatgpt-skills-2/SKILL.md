---
name: blog-post-optimizer
description: Analyze blog posts for SEO, readability, headline quality, and content structure. Generate meta tags and optimization recommendations with scoring.
---

# Blog Post Optimizer

Comprehensive content analysis toolkit for optimizing blog posts, articles, and web content. Analyzes headlines, SEO elements, content structure, readability, and generates actionable recommendations with scores.

## Quick Start

```python
from scripts.blog_post_optimizer import BlogPostOptimizer

# Initialize optimizer
optimizer = BlogPostOptimizer()

# Analyze a blog post
with open('blog_post.md', 'r') as f:
    content = f.read()

# Full analysis
results = optimizer.analyze_full(
    content=content,
    headline="10 Ways to Boost Your Productivity",
    keywords=["productivity", "time management", "efficiency"]
)

# View scores
print(f"Overall Score: {results['overall_score']}/100")
print(f"Headline Score: {results['headline']['score']}/100")
print(f"SEO Score: {results['seo']['score']}/100")
print(f"Readability Grade: {results['readability']['grade_level']}")

# Export HTML report
optimizer.export_html_report(results, 'report.html')
```

## Features

### 1. Headline Analysis
- **Power Words Detection** - Identifies emotional trigger words
- **Character Count** - Optimal range 50-60 characters
- **Emotional Impact** - Measures headline engagement potential
- **A/B Suggestions** - Generate alternative headlines

### 2. SEO Optimization
- **Keyword Density** - Target 1-2% for primary keyword
- **Keyword Prominence** - Check placement in first 100 words
- **Meta Description** - Auto-generate 150-160 characters
- **Title Tag** - Optimize for 50-60 characters
- **URL Slug** - Generate SEO-friendly slugs

### 3. Content Structure
- **Heading Hierarchy** - Validate H1/H2/H3 structure
- **Paragraph Length** - Ideal 3-5 sentences
- **List Usage** - Detect numbered and bulleted lists
- **Image Placement** - Check for visual elements
- **Subheading Distribution** - Ensure consistent spacing

### 4. Readability Analysis
- **Flesch-Kincaid Grade** - Target grade 8-10
- **Reading Ease** - 60-70 is ideal
- **Sentence Complexity** - Average words per sentence
- **Passive Voice** - Percentage (aim for <10%)

### 5. Content Statistics
- **Word Count** - Article length tracking
- **Reading Time** - Estimated at 265 words/minute
- **Character Count** - Total characters
- **Average Sentence Length** - Words per sentence

### 6. Meta Tag Generation
- **Open Graph** - Social media preview tags
- **Twitter Cards** - Twitter-specific meta tags
- **Schema.org** - Article structured data (JSON-LD)

## API Reference

### BlogPostOptimizer

```python
optimizer = BlogPostOptimizer()
```

### analyze_headline(headline: str) -> Dict
Analyze headline effectiveness.

**Returns**:
```python
{
    'score': 75,  # 0-100
    'character_count': 52,
    'power_words': ['boost', 'proven'],
    'emotional_impact': 68,
    'suggestions': [
        "10 Proven Ways to Boost Your Productivity Today",
        "Boost Your Productivity: 10 Essential Strategies"
    ]
}
```

### analyze_seo(content: str, keywords: List[str]) -> Dict
Analyze SEO elements.

**Returns**:
```python
{
    'score': 80,
    'keyword_density': {'productivity': 1.8, 'time management': 0.9},
    'keyword_prominence': True,  # In first 100 words
    'meta_description': 'Discover 10 proven ways to boost productivity...',
    'title_tag': '10 Ways to Boost Productivity | Your Site',
    'url_slug': 'boost-productivity-10-ways'
}
```

### analyze_structure(content: str) -> Dict
Analyze content structure.

**Returns**:
```python
{
    'score': 85,
    'h1_count': 1,
    'h2_count': 10,
    'avg_paragraph_length': 4.2,  # Sentences
    'list_count': 3,
    'warnings': ['Paragraph on line 45 is too long (8 sentences)']
}
```

### analyze_readability(content: str) -> Dict
Calculate readability scores.

**Returns**:
```python
{
    'flesch_kincaid_grade': 8.5,
    'reading_ease': 65.2,
    'avg_sentence_length': 15.3,
    'passive_voice_pct': 8.5,
    'complexity_score': 72
}
```

### calculate_content_stats(content: str) -> Dict
Calculate basic content statistics.

**Returns**:
```python
{
    'word_count': 1250,
    'reading_time_minutes': 5,
    'character_count': 7890,
    'sentence_count': 85,
    'paragraph_count': 28
}
```

### generate_meta_tags(title: str, description: str, keywords: List[str]) -> Dict
Generate social media and SEO meta tags.

**Returns**:
```python
{
    'open_graph': {
        'og:title': '10 Ways to Boost Your Productivity',
        'og:description': 'Discover proven strategies...',
        'og:type': 'article'
    },
    'twitter_card': {
        'twitter:card': 'summary_large_image',
        'twitter:title': '10 Ways to Boost Your Productivity'
    },
    'schema_org': {
        '@context': 'https://schema.org',
        '@type': 'Article',
        'headline': '10 Ways to Boost Your Productivity'
    }
}
```

### analyze_full(content: str, headline: str, keywords: List[str]) -> Dict
Complete analysis combining all methods.

**Returns**:
```python
{
    'overall_score': 78,
    'headline': {...},
    'seo': {...},
    'structure': {...},
    'readability': {...},
    'stats': {...},
    'recommendations': [
        {'priority': 'high', 'issue': '...', 'fix': '...'}
    ]
}
```

### export_html_report(results: Dict, output_path: str)
Generate color-coded HTML report with charts and recommendations.

## CLI Usage

### Single Blog Post Analysis

```bash
python scripts/blog_post_optimizer.py \
    --input blog_post.md \
    --headline "10 Ways to Boost Your Productivity" \
    --keywords "productivity,time management,efficiency" \
    --output report.html \
    --format html
```

### Quick Analysis (JSON Output)

```bash
python scripts/blog_post_optimizer.py \
    --input article.txt \
    --headline "Ultimate Guide to Python" \
    --keywords "python,programming" \
    --format json
```

### Headline Analysis Only

```bash
python scripts/blog_post_optimizer.py \
    --headline-only "10 Productivity Hacks You Need to Know"
```

## CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input`, `-i` | Input file (txt/md/html) | - |
| `--headline` | Blog post headline | Extracted from content |
| `--keywords`, `-k` | Comma-separated keywords | - |
| `--output`, `-o` | Output file path | stdout |
| `--format`, `-f` | Output format (json/html) | json |
| `--headline-only` | Analyze headline only | False |

## Examples

### Example 1: Full Analysis with HTML Report

```python
optimizer = BlogPostOptimizer()

with open('article.md') as f:
    content = f.read()

results = optimizer.analyze_full(
    content=content,
    headline="The Complete Guide to Remote Work",
    keywords=["remote work", "productivity", "work from home"]
)

optimizer.export_html_report(results, 'seo_report.html')
```

### Example 2: Headline Optimization

```python
optimizer = BlogPostOptimizer()

headline = "Ways to Improve Your Writing"
analysis = optimizer.analyze_headline(headline)

print(f"Score: {analysis['score']}/100")
print(f"Power words found: {', '.join(analysis['power_words'])}")
print("\nSuggestions:")
for suggestion in analysis['suggestions']:
    print(f"  - {suggestion}")
```

### Example 3: SEO Keyword Analysis

```python
optimizer = BlogPostOptimizer()

with open('post.md') as f:
    content = f.read()

seo = optimizer.analyze_seo(
    content=content,
    keywords=["python", "tutorial", "beginners"]
)

for keyword, density in seo['keyword_density'].items():
    print(f"{keyword}: {density:.1f}%")
```

## Dependencies

```
nltk>=3.8.0
textblob>=0.17.0
beautifulsoup4>=4.12.0
pandas>=2.0.0
matplotlib>=3.7.0
reportlab>=4.0.0
lxml>=4.9.0
```

## Limitations

- **HTML Parsing**: Complex HTML structures may affect accuracy
- **Keyword Context**: Doesn't account for keyword context (positive/negative)
- **Language**: English only for readability and power words
- **Power Words**: Subjective; effectiveness varies by audience
- **Readability**: Formulas are guides, not absolute measures
- **SEO**: Search engine algorithms constantly change
- **Image Analysis**: Cannot analyze actual image content
- **External Links**: Doesn't validate external link quality
