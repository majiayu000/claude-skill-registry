---
name: jekyll-article-generator
description: Specialized agent for generating high-quality articles and blog posts using jekyll-TeXt-theme, with expertise in software verification and validation. Use when creating course materials, lecture notes, topic articles, or blog posts for the Spring 2026 coursework site.
---

# Jekyll TeXt Theme Article Generator

This agent specializes in generating publication-quality articles and blog posts for the jekyll-TeXt-theme Jekyll site, with deep expertise in software verification and validation topics.

## Purpose and Scope

Generate well-structured, publication-ready articles and blog posts that:
- Follow jekyll-TeXt-theme conventions and best practices
- Use proper article layout and front matter
- Maintain academic and professional tone
- Cover software verification, validation, testing, and related topics
- Can serve as course materials, lecture notes, or blog content

## Target Location

This skill is project-specific and should be stored at:
- `.cursor/skills/jekyll-article-generator/` (in the spring-2026 project)

## Trigger Scenarios

Automatically apply this skill when users request:
- Creating new articles or blog posts
- Generating course materials or lecture notes
- Writing topic articles for software verification topics
- Converting notes to publication format
- Creating documentation or tutorial content

## Key Domain Knowledge

### Software Verification & Validation Expertise

The agent understands:
- **Verification vs. Validation**: Building the product right vs. building the right product
- **Testing Techniques**: Black box, white box, model-based, graph-based, fault-based testing
- **Formal Methods**: Model checking, theorem proving, formal verification
- **Testing Tools**: LangSmith, testing frameworks, coverage tools
- **AI/LLM Testing**: Evaluation methods, prompt testing, LLM quality assurance
- **Industry Practices**: Test adequacy criteria, coverage metrics, test strategies

### Jekyll TeXt Theme Knowledge

The agent understands:
- **Layouts**: `article`, `page`, `home`, `landing`, `archive`
- **Front Matter**: Required and optional fields for articles
- **Article Structure**: Excerpt separation with `<!--more-->`, proper heading hierarchy
- **Theme Features**: MathJax, Mermaid diagrams, syntax highlighting
- **Navigation Configuration**: Header and sidebar navigation via `_data/navigation.yml`

## Article Format Standards

### Front Matter Template

```yaml
---
layout: article
title: Article Title
key: unique-article-key
tags:
  - Tag1
  - Tag2
  - Tag3
permalink: /path/to/article/
mathjax: true  # Optional: for mathematical notation
mermaid: true  # Optional: for diagrams
---
```

### Content Structure

1. **Opening Paragraph** (Excerpt)
   - Engaging introduction
   - Clear statement of topic
   - Sets context and expectations

2. **Excerpt Separator**
   - `<!--more-->` after first paragraph or section
   - Marks where excerpt ends in article lists

3. **Main Content**
   - Logical sections with proper headings (##, ###)
   - Examples and code blocks where appropriate
   - Clear explanations and definitions
   - Academic tone with professional language

4. **Conclusion/Summary**
   - Key takeaways
   - Further reading/resources
   - Navigation to related articles

### Style Guidelines

- **Tone**: Academic but accessible, professional yet engaging
- **Structure**: Clear hierarchy with descriptive headings
- **Examples**: Include code examples, diagrams, or practical illustrations
- **Citations**: Reference course materials, standards, or research when appropriate
- **Formatting**: Use Markdown features (code blocks, lists, emphasis) effectively

## Examples

### Course Topic Article

```yaml
---
layout: article
title: Black Box Testing
key: topic-black-box-testing
tags:
  - Testing
  - Black Box
  - Functional Testing
permalink: /software-verification/topics/black-box-testing/
---

Black box testing is a fundamental testing methodology where the internal structure of the software is not known to the tester. Instead, testers focus on functionality and behavior based on specifications.

<!--more-->

## Understanding Black Box Testing

[Main content here...]
```

### Lecture Notes Article

```yaml
---
layout: article
title: Lecture 5: Model-Based Testing
key: lecture-05-model-based-testing
tags:
  - Lecture Notes
  - Model-Based Testing
  - CS-5374
date: 2026-02-12
permalink: /software-verification/lectures/2026-02-12-model-based-testing/
---

This lecture covers model-based testing techniques and their application in software verification.

<!--more-->

## Topics Covered

[Lecture content...]
```

## Best Practices

1. **Always use `layout: article`** for articles and blog posts
2. **Include `key` field** with unique identifier (letter + alphanumeric)
3. **Add relevant tags** for categorization and navigation
4. **Use `<!--more-->` separator** after excerpt
5. **Maintain heading hierarchy** (## for main sections, ### for subsections)
6. **Include code examples** in appropriate language blocks
7. **Link to related articles** and resources
8. **Use MathJax/Mermaid** when mathematical notation or diagrams are needed

## Navigation Checklist

When creating articles that need navigation:

- [ ] Determine if article should appear in header or sidebar navigation
- [ ] Check `_data/navigation.yml` for existing navigation structures
- [ ] Add article to appropriate navigation structure if needed
- [ ] Use consistent URL patterns with other related articles
- [ ] If using sidebar, add `sidebar: { nav: nav-name }` to front matter
- [ ] Verify navigation URLs match article permalinks
- [ ] Ensure navigation hierarchy is logical and well-organized

## Quality Checklist

Before finalizing an article, ensure:
- [ ] Front matter includes `layout: article`, `title`, `key`, `tags`, `permalink`
- [ ] Sidebar navigation configured if article is part of a topic series
- [ ] Opening paragraph serves as good excerpt
- [ ] `<!--more-->` separator is present
- [ ] Content is well-structured with proper headings
- [ ] Academic tone is maintained throughout
- [ ] Technical terms are defined or explained
- [ ] Examples or illustrations are included where appropriate
- [ ] Links to related content are provided
- [ ] Navigation is updated in `_data/navigation.yml` if article should appear in menus
- [ ] Content is publication-ready

## Navigation Configuration

### Understanding `_data/navigation.yml`

The jekyll-TeXt-theme uses `_data/navigation.yml` to define navigation. The agent must understand two types:

#### Header Navigation

Defined under the `header` key. Used for main site navigation menu:

```yaml
header:
  - title:      Home
    url:        /
  - title:      Docs
    url:        /docs/en/quick-start
    key:        docs  # Optional: unique identifier
  - titles:     # Multi-language support
      en:       Archive
      zh:       归档
    url:        /archive.html
  - title:      External Link
    url:        https://example.com
```

**Key Points**:
- Each item has `title` (or `titles` for multi-language) and `url`
- Optional `key` field for unique identification
- Can include external URLs
- Supports single `title` or `titles` object for internationalization

#### Sidebar Navigation

Defined as named navigation structures. Used for article sidebar navigation:

```yaml
course-topics:
  - title:      Fundamentals
    children:
      - title:  Introduction to V&V
        url:    /software-verification/topics/01-introduction-vv/
      - title:  Adequacy Criterion
        url:    /software-verification/topics/02-adequacy-criterion/
  - title:      Testing Techniques
    children:
      - title:  Black Box Testing
        url:    /software-verification/topics/04-black-box-testing/
      - title:  White Box Testing
        url:    /software-verification/topics/05-white-box-testing/
```

**Key Points**:
- Named navigation structure (e.g., `course-topics:`, `docs-en:`)
- Hierarchical structure with `children` arrays
- Each child has `title` and `url`
- Supports nested navigation (parent → children)

### Using Sidebar Navigation in Articles

To enable sidebar navigation in an article, add to front matter:

```yaml
---
layout: article
title: Article Title
sidebar:
  nav: course-topics  # References navigation structure in navigation.yml
---
```

### Navigation Best Practices

When creating articles, consider navigation:

1. **Header Navigation**: Add important pages/sections to `header` in `_data/navigation.yml`
2. **Sidebar Navigation**: Create named navigation structures for topic groups
3. **Update Navigation**: When creating new articles, update `navigation.yml` if they should appear in navigation
4. **Consistent URLs**: Use consistent permalink patterns for related articles
5. **Hierarchical Organization**: Use `children` to group related topics under parent categories

### Example Navigation File

Complete `_data/navigation.yml` structure:

```yaml
header:
  - title: Home
    url: /
  - title: Software Verification
    url: /software-verification/introduction/
  - title: Topics
    url: /software-verification/introduction/
  - title: Courses
    url: /courses/

# Sidebar navigation for course topics
course-topics:
  - title: Introduction
    children:
      - title: Introduction to V&V
        url: /software-verification/topics/01-introduction-vv/
      - title: Adequacy Criterion
        url: /software-verification/topics/02-adequacy-criterion/
  - title: Testing Methods
    children:
      - title: Black Box Testing
        url: /software-verification/topics/04-black-box-testing/
      - title: White Box Testing
        url: /software-verification/topics/05-white-box-testing/
      - title: Model-based Testing
        url: /software-verification/topics/06-model-based-testing/
```

## Integration with Course Site

Articles should:
- Reference course data from `_data/` directories when appropriate
- Use Liquid templating for dynamic content
- Follow site navigation structure defined in `_data/navigation.yml`
- Update navigation.yml when creating new article series or sections
- Link to related lectures, topics, or resources
- Use sidebar navigation where appropriate for topic organization
- Maintain consistency with existing course materials

## Navigation Workflow

When creating articles that should appear in navigation:

1. **Determine Navigation Type**: 
   - Header navigation: For main site navigation items
   - Sidebar navigation: For topic-based article organization

2. **Check Existing Navigation**: Review `_data/navigation.yml` for existing structures

3. **Update Navigation File**: 
   - Add to `header:` for main navigation items
   - Add to appropriate sidebar navigation structure (e.g., `course-topics:`)
   - Maintain hierarchical structure with `children` where appropriate

4. **Reference in Front Matter**: 
   - If using sidebar, add `sidebar: { nav: navigation-name }` to article front matter

5. **Maintain Consistency**: 
   - Use consistent URL patterns
   - Group related articles under same parent in sidebar
   - Keep navigation structures organized and logical

## Workflow

When generating articles:

1. **Understand Requirements**: Clarify article type, topic, and audience
2. **Gather Context**: Review related course materials or existing articles
3. **Check Navigation**: Review `_data/navigation.yml` to see where article fits
4. **Create Structure**: Plan sections and content flow
5. **Write Content**: Generate article following format standards
6. **Update Navigation**: Add article to appropriate navigation structure if needed
7. **Review and Refine**: Ensure quality, consistency, and completeness
8. **Add Metadata**: Include tags, links, front matter, and sidebar navigation if applicable

## Navigation Examples

### Example: Complete Navigation File

Reference the `_data/navigation.yml` structure from the jekyll-TeXt-theme repository:
- **Header Navigation**: Simple flat structure with `title` and `url`
- **Sidebar Navigation**: Hierarchical structure with named navigation groups
- **Multi-language Support**: Use `titles` object instead of `title` for i18n

### Example: Using Sidebar in Article

```yaml
---
layout: article
title: Black Box Testing
key: topic-black-box-testing
tags:
  - Testing
sidebar:
  nav: course-topics  # References navigation structure in _data/navigation.yml
permalink: /software-verification/topics/04-black-box-testing/
---
```

This will display the `course-topics` navigation in the sidebar when viewing this article.

### Example: Multi-language Navigation

```yaml
header:
  - titles:
      en: Archive
      zh: 归档
    url: /archive.html
```

Use `titles` object for internationalization support.

## Reference Files

- **Theme Navigation**: https://github.com/sweeden-ttu/jekyll-TeXt-theme/blob/master/docs/_data/navigation.yml
- **Site Navigation**: `_data/navigation.yml` (should be created/updated as articles are added)
- **Article Examples**: See `/software-verification/_pages/topics/` for examples of course topic articles
- **Navigation Documentation**: See theme docs at `/docs/en/navigation` or `/docs/zh/navigation`
