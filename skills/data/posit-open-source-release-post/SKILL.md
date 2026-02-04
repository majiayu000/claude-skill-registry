---
name: release-post
description: >
  Create professional package release blog posts following Tidyverse or Shiny blog conventions.
  Use when the user needs to: (1) Write a release announcement blog post for an R or Python package
  for tidyverse.org or shiny.posit.co, (2) Transform NEWS/changelog content into blog format,
  (3) Generate acknowledgments sections with contributor lists, (4) Format posts following specific
  blog platform requirements. Supports both Tidyverse (hugodown) and Shiny (Quarto) blog formats with
  automated contributor fetching and comprehensive style guidance.
---

# Package Release Post

Create professional R/Python package release blog posts following Tidyverse or Shiny blog conventions.

## Quick Start

1. **Identify the blog platform**: Tidyverse (tidyverse.org) or Shiny (shiny.posit.co)
2. Verify NEWS.md or changelog exists for the package
3. Gather package info: name, version, repository (e.g., "tidyverse/dplyr")
4. Follow the workflow below
5. Use `scripts/get_contributors.R` to generate acknowledgments
6. Reference the appropriate formatting guide for final polish

## Platform Selection

This skill supports two blog platforms with different formatting requirements:

- **Tidyverse blog** (tidyverse.org)
  - Uses hugodown
  - R packages primarily
  - More rigid structure and conventions
  - See `references/tidyverse-formatting.md`

- **Shiny blog** (shiny.posit.co)
  - Uses Quarto
  - R and Python packages
  - More flexible, feature-focused structure
  - See `references/shiny-formatting.md`

**First, determine which platform the post is for**, then follow the general workflow and apply platform-specific formatting.

## General Workflow

These steps apply to both platforms. Content guidelines are based on Tidyverse best practices but adapt them as needed for Shiny posts.

### Step 1: Gather Information

Collect required information:

- **Platform**: Tidyverse or Shiny blog?
- **Package name and version**: e.g., "dplyr 1.2.0" or "shiny 1.9.0"
- **Repository**: GitHub repo in "owner/repo" format
- **Package language**: R or Python
- **NEWS content**: Read the package's NEWS.md, CHANGELOG, or NEWS
- **Package description**: One-sentence core purpose
- **Previous release tag**: For contributor fetching (optional)
- **Featured image**: For frontmatter (optional but recommended)

### Step 2: Structure the Post

Create the post outline following this order:

1. **Frontmatter**: Platform-specific YAML (see formatting references)

2. **Title and Opening**:
   - Title: Package name and version
   - Opening: Announcement with one-sentence package description
   - Installation: Code block with installation command
   - Overview: Brief summary with link to full release notes

3. **Main Content** (choose appropriate sections):
   - **Migration guide** (if breaking changes) - Always first when present
   - **Lifecycle changes** (deprecations, soft-deprecations, defunct)
   - **Feature sections** (one per major feature, descriptive headings)
   - **Minor improvements** (bulleted list)

4. **Acknowledgements** (when appropriate):
   - Use `scripts/get_contributors.R`
   - Format: "A big thank you to all the folks who helped make this release happen:"
   - Comma-separated GitHub links

### Step 3: Apply Content Guidelines

Follow the best practices in `references/content-guidelines.md`:

- **Opening style**: "We're [random adjective expressing excitement] to announce the release of..."
- **Section organization**: Migration → Lifecycle → Features → Improvements → Acknowledgements
- **Tone**: Conversational, professional, enthusiastic but authentic
- **Technical precision**: Use exact function names in backticks
- **Focus on benefits**: Explain "why" not just "what"
- **Code examples**: Realistic, well-commented, properly formatted

### Step 4: Transform NEWS Content

Convert NEWS.md bullets to blog-friendly content:

- **Research features thoroughly**: Don't just copy NEWS bullets—read function docs, check PRs, understand the context
- **Expand context**: Why changes matter, not just what changed
- **Add complete code examples**: Show realistic usage with full workflows, not just function signatures
- **Explain concepts first**: For unfamiliar features, explain what they are and how they work before showing code
- **Group thematically**: Combine related NEWS items into coherent sections
- **Use conversational tone**: Transform terse bullets into prose
- **Link documentation**: Add relevant links to docs and resources
- **Highlight breaking changes**: Make migration paths clear
- **Multi-language parity** (Shiny only): For R+Python packages on the Shiny blog, ensure all examples show both languages in tabsets

### Step 5: Apply Platform-Specific Formatting

**For Tidyverse posts**, read `references/tidyverse-formatting.md` and apply:
- hugodown frontmatter with `slug`, `photo.url`, `photo.author`
- Specific slug format: `packagename-x-y-z` (hyphens replace dots)
- R code blocks with `r` language identifier
- Acknowledgements always included as final section

**For Shiny posts**, read `references/shiny-formatting.md` and apply:
- Quarto frontmatter with YAML anchors for social media
- Flexible title formatting
- Use tabsets for Python/R or Express/Core variations
- Platform-specific code block attributes
- Acknowledgements optional, varies by post type
- May use lead paragraphs, callouts, embedded media

### Step 6: Generate Acknowledgements

Run the contributor script:

```bash
Rscript scripts/get_contributors.R "owner/repo"
```

Or with a specific starting tag for the previous version (or tag used for last release post):

```bash
Rscript scripts/get_contributors.R "owner/repo" "v1.0.0"
```

Copy the markdown output into the Acknowledgements section.

### Step 7: Review and Polish

Platform-agnostic checklist:

- [ ] Frontmatter complete with all required fields
- [ ] Opening clearly states package purpose
- [ ] Installation code block present (both languages if applicable)
- [ ] Sections organized logically
- [ ] Code examples use proper syntax highlighting
- [ ] Function names in backticks with parentheses: `` `function()` ``
- [ ] Package names are not backticked or otherwise styled
- [ ] Tone is conversational but not marketing-speak
- [ ] No superlatives ("powerful", "rich", "seamless", etc.)
- [ ] Features explained with context, not just listed
- [ ] Concepts explained before showing code
- [ ] All examples show R and Python variants (if applicable)
- [ ] Links to full release notes included

Platform-specific checklist:

**Tidyverse:**
- [ ] Slug format: `package-x-y-z` (hyphens, not dots)
- [ ] Photo URL and author included
- [ ] Acknowledgements section is final section
- [ ] All contributors listed alphabetically

**Shiny:**
- [ ] YAML anchors used for description (`&desc`, `*desc`)
- [ ] Social media cards configured (`open-graph`, `twitter-card`)
- [ ] Appropriate filters specified if using tabsets/shinylive
- [ ] Tabsets used for showing paired variants (Python/R, Express/Core)
- [ ] Multi-language tabsets used consistently (for R+Python packages only)

## Reference Documentation

Load these as needed for detailed guidance:

### Content Guidelines
**`references/content-guidelines.md`** - General best practices for all release posts:
- Post structure and organization
- Opening style and tone
- Section hierarchy and organization
- Code examples and formatting
- Before/after patterns
- Acknowledgments conventions

### Platform-Specific Formatting

**`references/tidyverse-formatting.md`** - Tidyverse blog requirements:
- hugodown frontmatter structure
- Slug and title conventions
- Photo attribution
- Code block formatting
- Lifecycle section structure
- Acknowledgements format

**`references/shiny-formatting.md`** - Shiny blog requirements:
- Quarto frontmatter with YAML anchors
- Social media card configuration
- Lead paragraphs and callouts
- Tabsets for variants
- Line highlighting and annotations
- Video embedding
- Flexible acknowledgements

## Resources

- **`scripts/get_contributors.R`**: Fetch formatted contributor list using `usethis::use_tidy_thanks()`
- **`references/content-guidelines.md`**: General content best practices (platform-agnostic)
- **`references/tidyverse-formatting.md`**: Tidyverse-specific formatting requirements
- **`references/shiny-formatting.md`**: Shiny-specific formatting requirements

## Platform-Specific Quick Reference

### Tidyverse Post Template

````markdown
---
output: hugodown::hugo_document
slug: package-x-y-z
title: package x.y.z
date: YYYY-MM-DD
author: Your Name
description: >
    Brief description
photo:
  url: https://unsplash.com/photos/id
  author: Photographer Name
categories: [package]
tags: [package]
---

# package x.y.z

We're pleased to announce the release of package x.y.z...

```r
install.packages("package")
```

...

## Acknowledgements

A big thank you to all the folks who helped make this release happen:

[Contributors from get_contributors.R]
````

### Shiny Post Template

````markdown
---
title: Package Name x.y.z
description: &desc |
  Brief description of the release.
author: "Your Name"
date: "YYYY-MM-DD"

image: feature.png

open-graph:
  image: feature.png
  description: *desc
twitter-card:
  image: feature.png
  description: *desc
---

# package x.y.z

We're excited to announce package x.y.z...

[Installation for Python or R]

...
````

## Tips

- **Breaking changes first**: Put migration guides before features
- **Highlight the wins**: Lead with the most exciting features
- **Show don't tell**: Use code examples liberally
- **Link generously**: Help readers find more information
- **Keep it conversational**: Write like you're explaining to a colleague
- **Be authentic**: Enthusiasm should feel genuine, not marketing-speak
