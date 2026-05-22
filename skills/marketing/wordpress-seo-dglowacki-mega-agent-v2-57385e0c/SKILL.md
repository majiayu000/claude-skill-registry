---
name: wordpress-seo
description: WordPress content optimization including SEO metadata generation, readability scoring, keyword optimization, and content rewriting patterns. Use when optimizing WordPress posts for search engines.
---

# WordPress SEO Optimization

Tools and patterns for optimizing WordPress content for search engines.

## Quick Start

Optimize content:
```bash
python scripts/optimize_content.py --input post.html --keywords "react,javascript" --output optimized.html
```

Generate metadata:
```bash
python scripts/generate_metadata.py --title "My Post" --content post.html --output metadata.json
```

Calculate readability:
```bash
python scripts/calculate_readability.py --input post.html
```

## SEO Optimization Process

### 1. Content Analysis

Analyze existing content for SEO opportunities:

**Checks:**
- Keyword density (target: 1-2% for primary keyword)
- Heading structure (H1, H2, H3 hierarchy)
- Paragraph length (target: 3-5 sentences)
- Sentence length (target: 15-20 words)
- Internal/external links (target: 2-3 per 500 words)
- Image alt text presence
- Meta description length (target: 150-160 characters)
- Title tag length (target: 50-60 characters)

### 2. Content Optimization

**Optimization patterns:**

#### Keyword Integration
```
Original: "This tutorial shows you how to use React."
Optimized: "This React tutorial demonstrates essential React concepts for beginners."
```

#### Heading Structure
```
Before:
<h2>Introduction</h2>
<h2>Setup</h2>
<h2>Conclusion</h2>

After:
<h1>Complete React Tutorial for Beginners</h1>
<h2>Getting Started with React</h2>
<h3>Setting Up Your Environment</h3>
<h3>Installing Dependencies</h3>
<h2>Conclusion and Next Steps</h2>
```

#### Paragraph Optimization
```
Before:
This is a very long paragraph that goes on and on without any breaks and makes it hard for readers to follow along and understand the key points because everything is crammed into one giant block of text.

After:
This paragraph is concise and focused. It covers one main idea.

Each paragraph should contain 3-5 sentences. This makes content easier to read and scan.
```

### 3. Metadata Generation

Generate SEO-optimized metadata:

**Title Tag:**
- Include primary keyword
- 50-60 characters
- Compelling and click-worthy

**Meta Description:**
- Include primary + secondary keywords
- 150-160 characters
- Clear call-to-action
- Accurately describes content

**Keywords:**
- 3-5 primary/secondary keywords
- Long-tail variations
- Related terms

### 4. Readability Scoring

Calculate content readability using multiple metrics:

**Flesch Reading Ease:**
- 90-100: Very easy (5th grade)
- 80-89: Easy (6th grade)
- 70-79: Fairly easy (7th grade)
- 60-69: Standard (8-9th grade) - **Target**
- 50-59: Fairly difficult (10-12th grade)
- 30-49: Difficult (College)
- 0-29: Very difficult (Graduate)

**Flesch-Kincaid Grade Level:**
- Target: 8-10 (8th-10th grade reading level)

**SMOG Index:**
- Target: 10-12 (10th-12th grade)

**Average Metrics:**
- Words per sentence: 15-20
- Syllables per word: 1.5-2.0
- Characters per word: 4.5-5.5

## Scripts

### optimize_content.py

Optimize WordPress content for SEO.

**Usage:**
```bash
python scripts/optimize_content.py \
    --input post.html \
    --keywords "react,javascript,tutorial" \
    --primary-keyword "react tutorial" \
    --target-readability 65 \
    --output optimized.html
```

**Arguments:**
- `--input`: Input HTML file
- `--keywords`: Comma-separated keywords
- `--primary-keyword`: Primary keyword to optimize for
- `--target-readability`: Target Flesch Reading Ease score (default: 65)
- `--output`: Output HTML file

**Optimizations performed:**
1. Keyword integration in content
2. Heading structure optimization
3. Paragraph length optimization
4. Sentence length optimization
5. Internal link suggestions
6. Image alt text generation
7. Meta description generation

### generate_metadata.py

Generate SEO metadata for WordPress posts.

**Usage:**
```bash
python scripts/generate_metadata.py \
    --title "Complete React Tutorial" \
    --content post.html \
    --keywords "react,javascript" \
    --output metadata.json
```

**Arguments:**
- `--title`: Post title
- `--content`: Post content (HTML or text file)
- `--keywords`: Target keywords
- `--output`: Output JSON file

**Generates:**
```json
{
  "title_tag": "Complete React Tutorial for Beginners | 2026 Guide",
  "meta_description": "Learn React with this comprehensive tutorial covering components, hooks, state management, and more. Perfect for JavaScript developers.",
  "keywords": ["react tutorial", "learn react", "react for beginners", "javascript", "web development"],
  "og_title": "Complete React Tutorial for Beginners",
  "og_description": "Master React fundamentals with step-by-step examples and practical exercises.",
  "og_image": "suggested-image-url.jpg",
  "slug": "complete-react-tutorial-beginners"
}
```

### calculate_readability.py

Calculate readability scores for content.

**Usage:**
```bash
python scripts/calculate_readability.py \
    --input post.html \
    --format html
```

**Arguments:**
- `--input`: Input file
- `--format`: Input format (html, text)

**Output:**
```json
{
  "flesch_reading_ease": 67.5,
  "flesch_kincaid_grade": 8.2,
  "smog_index": 10.1,
  "avg_words_per_sentence": 18.3,
  "avg_syllables_per_word": 1.6,
  "total_words": 1247,
  "total_sentences": 68,
  "readability_level": "Standard (8-9th grade)",
  "recommendation": "Good readability for general audience"
}
```

## SEO Guidelines

See `rules/seo_guidelines.md` for comprehensive SEO best practices:

### Content Quality
- Original, unique content
- Comprehensive coverage of topic
- Value to reader
- Regular updates

### Technical SEO
- Fast page load (< 3 seconds)
- Mobile-friendly design
- HTTPS enabled
- XML sitemap
- Structured data (Schema.org)

### On-Page SEO
- Descriptive URLs with keywords
- Optimized images (compressed, alt text)
- Internal linking structure
- External links to authoritative sources
- Clear heading hierarchy

### Keyword Strategy
- Primary keyword in:
  - Title tag
  - Meta description
  - First paragraph
  - At least one H2
  - Image alt text
  - URL slug
- Secondary keywords throughout content
- Long-tail keyword variations
- LSI (Latent Semantic Indexing) keywords

## Content Rewriting Patterns

### Pattern 1: Keyword Density

```python
def optimize_keyword_density(content: str, keyword: str, target_density: float = 0.015):
    """
    Adjust keyword density to target percentage.

    Target: 1-2% (0.01-0.02)
    """
    # Calculate current density
    word_count = len(content.split())
    keyword_count = content.lower().count(keyword.lower())
    current_density = keyword_count / word_count

    # Suggest additions if too low
    if current_density < target_density:
        needed = int((target_density * word_count) - keyword_count)
        return f"Add '{keyword}' {needed} more times"

    return "Keyword density optimal"
```

### Pattern 2: Heading Optimization

```python
def optimize_headings(html: str, primary_keyword: str):
    """
    Ensure proper heading structure with keyword integration.
    """
    # H1 should contain primary keyword
    # H2s should contain secondary keywords
    # Maintain proper hierarchy (H1 > H2 > H3)
    # 1-2 headings per 300 words
```

### Pattern 3: Readability Enhancement

```python
def enhance_readability(text: str):
    """
    Improve readability by:
    - Breaking long sentences (>25 words)
    - Splitting long paragraphs (>150 words)
    - Adding transition words
    - Using active voice
    - Simplifying complex words
    """
```

## Integration with Agents

### WordPress Agent

```python
from wordpress_seo import optimize_content, generate_metadata

# Get post
post = wordpress_client.get_post(post_id=123)

# Optimize content
optimized_html = optimize_content(
    content=post['content'],
    keywords=['react', 'tutorial'],
    primary_keyword='react tutorial'
)

# Generate metadata
metadata = generate_metadata(
    title=post['title'],
    content=optimized_html,
    keywords=['react', 'tutorial']
)

# Update post
wordpress_client.update_post(
    post_id=123,
    content=optimized_html,
    excerpt=metadata['meta_description'],
    slug=metadata['slug']
)
```

### Reporting Agent

```python
from wordpress_seo import calculate_readability

# Analyze multiple posts
posts = wordpress_client.get_posts(per_page=10)

for post in posts:
    scores = calculate_readability(post['content'])

    if scores['flesch_reading_ease'] < 60:
        # Flag for optimization
        print(f"Post {post['id']} needs readability improvement")
```

## Best Practices

### Content Optimization
1. Focus on reader value first, SEO second
2. Natural keyword integration (avoid keyword stuffing)
3. Use synonyms and related terms
4. Write for humans, optimize for search engines

### Metadata Optimization
1. Unique title and description for each page
2. Include target keywords naturally
3. Make titles compelling (increase CTR)
4. Update metadata when content changes

### Regular Audits
1. Check keyword rankings monthly
2. Update old content quarterly
3. Fix broken links
4. Monitor Core Web Vitals
5. Track organic traffic trends

## Resources

- `rules/seo_guidelines.md` - Complete SEO guidelines
- `examples/before_after.html` - Example optimizations
- `examples/metadata_samples.json` - Metadata examples
