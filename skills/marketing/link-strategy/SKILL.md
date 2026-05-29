---
name: link-strategy
description: Internal linking strategy and anchor text optimization patterns. Use when planning internal links or optimizing site structure.
---

# Link Strategy

## When to Use

- Planning internal linking structure
- Optimizing anchor text
- Building topic clusters
- Improving site architecture

## Internal Linking Principles

### 1. Link from High to Low Authority
- Homepage -> Category Pages -> Individual Posts
- Old established pages -> New pages
- High-traffic pages -> Pages you want to rank

### 2. Use Descriptive Anchor Text
- Good: "SEO keyword research guide"
- Bad: "click here", "read more"
- Include target keyword naturally

### 3. Link Contextually
- Links within body content > Navigation links
- Relevant context around link
- Natural reading flow

### 4. Maintain Reasonable Link Count
- 3-5 internal links per 1000 words
- Avoid excessive linking (100+ links)
- Focus on most relevant pages

## Topic Cluster Model

```
PILLAR PAGE: "Content Marketing" (broad, high volume)
    |
    +-- Supporting Article: "Content Marketing Strategy"
    |   (links to and from pillar)
    |
    +-- Supporting Article: "Content Marketing Examples"
    |   (links to and from pillar)
    |
    +-- Supporting Article: "Content Marketing Tools"
        (links to and from pillar)
```

**Benefits:**
- Establishes topical authority
- Passes PageRank efficiently
- Improves user navigation
- Signals content relationships

## Anchor Text Optimization

### Anchor Text Types

| Type | Example | When to Use |
|------|---------|-------------|
| Exact Match | "SEO tools" | Sparingly (1-2x per page) |
| Partial Match | "best SEO tools for startups" | Primary usage |
| Branded | "SEMrush" | Brand mentions |
| Generic | "click here" | Avoid if possible |
| Naked URL | "https://example.com" | Occasional |

### Best Practices
- Vary anchor text naturally
- Use target keyword in some anchors
- Avoid over-optimization (100% exact match)
- Make text descriptive and clickable

## Link Audit Process

1. **Inventory existing links**
   - Use Glob to find all internal links
   - Map current link structure

2. **Identify orphan pages**
   - Pages with no internal links
   - Add links from relevant content

3. **Find broken links**
   - Test all internal links
   - Fix or remove broken ones

4. **Optimize anchor text**
   - Replace generic anchors
   - Add keyword-rich descriptions

5. **Build topic clusters**
   - Group related content
   - Implement pillar-cluster model

## Output Format

```markdown
## Internal Linking Plan

### Target Page: {url}
**Target Keyword**: {keyword}

### Linking Opportunities

1. **From**: {source_page}
   - **Anchor**: {anchor_text}
   - **Context**: {surrounding_sentence}
   - **Priority**: HIGH/MEDIUM/LOW

2. **From**: {source_page}
   - **Anchor**: {anchor_text}
   - **Context**: {surrounding_sentence}
   - **Priority**: HIGH/MEDIUM/LOW

### Topic Cluster Structure

PILLAR: {main_topic_page}
- Supporting: {page1}
- Supporting: {page2}
- Supporting: {page3}
```
