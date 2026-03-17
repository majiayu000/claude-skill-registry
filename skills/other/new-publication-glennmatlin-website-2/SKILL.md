---
name: new-publication
description: Add an academic publication entry with proper metadata, links, and optional academic badges. Use when adding papers, preprints, or other scholarly works.
allowed-tools: Write, Bash(mkdir:*)
---

# Adding a New Publication

## Instructions

When adding a publication:

1. **Generate the slug** from title or citation key:
   - Use format: `lastname-year-keyword` or `keyword-year`
   - Example: "matlin-2024-flame" or "unfoldml-2022"

2. **Create directory structure**:
   ```
   publications/<slug>/
   ├── index.qmd
   ├── paper.pdf      (if available)
   └── featured.png   (optional thumbnail)
   ```

3. **Create index.qmd with comprehensive frontmatter**:
   ```yaml
   ---
   title: "Full Paper Title"
   author:
     - Glenn Matlin
     - Co-Author Name
   date: YYYY-MM-DD
   categories: [Conference Paper, Journal Article, Preprint, Workshop]
   description: "One-line summary for listings"

   # Publication metadata
   venue: "Conference/Journal Name (Abbreviated)"
   venue-full: "Full Conference/Journal Name"
   year: YYYY

   # Links (include what's available)
   doi: "10.xxxx/xxxxx"
   pdf: paper.pdf
   code: "https://github.com/..."
   slides: "slides.pdf"
   video: "https://youtube.com/..."
   arxiv: "https://arxiv.org/abs/..."

   # For academic badges
   altmetric-id: ""      # Altmetric DOI or ID
   dimensions-id: ""     # Dimensions publication ID

   # Featured on homepage?
   featured: true
   ---
   ```

4. **Add abstract and content**:
   ```markdown
   ## Abstract

   Full abstract text here...

   ## BibTeX

   ```bibtex
   @inproceedings{key2024,
     title={...},
     author={...},
     booktitle={...},
     year={2024}
   }
   ```

   ## Links

   - [Paper PDF](paper.pdf)
   - [Code Repository](https://github.com/...)
   - [Presentation Slides](slides.pdf)
   ```

## Publication Types

Use appropriate category:
- `Conference Paper` - Peer-reviewed conference proceedings
- `Journal Article` - Journal publications
- `Preprint` - arXiv or other preprint servers
- `Workshop Paper` - Workshop proceedings
- `Thesis` - Dissertation or thesis
- `Technical Report` - Tech reports, white papers

## Academic Badges

To enable Altmetric/Dimensions badges, include in the page:

```html
<!-- Altmetric Badge -->
<div class="altmetric-embed" data-badge-type="medium-donut" data-doi="10.xxxx/xxxxx"></div>

<!-- Dimensions Badge -->
<span class="__dimensions_badge_embed__" data-doi="10.xxxx/xxxxx"></span>
```

## Example

**File**: `publications/flame-2024/index.qmd`

```yaml
---
title: "FLAME: Financial Language Model Evaluation Framework"
author:
  - Glenn Matlin
  - Other Authors
date: 2024-06-15
categories: [Conference Paper]
description: "A comprehensive framework for evaluating LLMs on financial tasks"
venue: "ACL 2024"
venue-full: "Annual Meeting of the Association for Computational Linguistics"
year: 2024
doi: "10.xxxx/xxxxx"
code: "https://github.com/gmatlin/flame"
featured: true
---
```
