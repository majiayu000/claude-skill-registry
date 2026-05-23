---
context: fork
model: haiku
---

# /article

Quick-create an Article note for communications - blog posts, videos, podcasts, LinkedIn posts, etc.

## Usage

```
/article <title>                              # Create draft article
/article <title> type <article-type>          # Specify format type
/article <title> for <platform>               # Specify target platform
/article <title> from <incubator-idea>        # Link to source incubator idea
/article list [filter]                        # List articles by status
```

## Examples

```
/article Cloud Migration Lessons Learned
/article Event-Driven Architecture Benefits type blog-post for medium
/article Why We Chose Kafka type linkedin-post
/article API Versioning Best Practices from API Strategy Incubator
/article Integration Patterns type video for youtube
```

---

## Create Article: `/article <title> [options]`

Fast capture with sensible defaults.

**Article Types:** article, blog-post, document, guardrail, video, podcast, linkedin-post
**Platforms:** medium, substack, confluence, linkedin, youtube, spotify, internal

1. Parse command for:
   - **title**: Article title (required)
   - **type**: Article format (after "type") - default: `article`
   - **platform**: Target platform (after "for") - default: null
   - **parentIdea**: Incubator idea (after "from") - fuzzy match

2. Generate filename: `Article - {{title}}.md`

3. Create in vault root:

```markdown
---
type: Article
title: {{title}}
created: {{DATE}}
modified: {{DATE}}
tags:
  - activity/documentation
  - {{domain tags based on title/context}}

# Article Classification
articleType: {{type or article}}
platform: {{platform or null}}
targetAudience: {{internal if confluence/internal, external if medium/substack/linkedin, null otherwise}}

# Provenance
parentIdea: {{incubator link or null}}

# Publication
status: draft
publishedUrl: null
publishedDate: null

# Quality Indicators
summary: null
confidence: medium
freshness: current
source: synthesis
verified: false
reviewed: {{DATE}}

# Semantic Discovery
keywords: []

# Relationships
relatedTo: []
---

# {{title}}

## Summary

<!-- One paragraph executive summary -->

## Key Points

-

## Content

<!-- Main article content -->

{{If from incubator: "Based on research from [[Incubator - {{idea}}]]"}}

## Call to Action

<!-- What should the reader do next? -->

## References

-

---

*Created with `/article` skill*
```

4. If `parentIdea` provided:
   - Fuzzy match incubator idea in `+Incubator/` or `+Archive/Incubator/`
   - Format as wiki-link: `"[[Incubator - API Strategy]]"`
   - Add to Related section

5. Infer `targetAudience` from platform:
   - `medium`, `substack`, `linkedin`, `youtube`, `spotify` → `external`
   - `confluence`, `internal` → `internal`
   - null platform → null audience

6. Confirm: `Created [[Article - {{title}}]] ({{articleType}} for {{platform or "unspecified platform"}})`

---

## List Articles: `/article list [filter]`

Filter by status, type, or platform.

**Statuses:** draft, ready, published, archived
**Types:** article, blog-post, document, guardrail, video, podcast, linkedin-post
**Platforms:** medium, substack, confluence, linkedin, youtube, spotify, internal

1. Read vault root for `type: Article` notes
2. Filter by provided criteria
3. Display as table:

| Article | Type | Platform | Status | Modified |
|---------|------|----------|--------|----------|

4. No filter = show count by status

---

## Publish Article: `/article publish <title>`

Mark an article as published.

1. Fuzzy match article by title
2. Ask for published URL
3. Update frontmatter:
   - `status: published`
   - `publishedUrl: {{url}}`
   - `publishedDate: {{DATE}}`
4. Confirm: `Marked [[Article - {{title}}]] as published`

---

## Article Type Reference

| Type | Description | Typical Platforms |
|------|-------------|-------------------|
| `article` | Long-form written content | confluence, internal |
| `blog-post` | External thought leadership | medium, substack |
| `document` | Formal whitepaper or standard | confluence, internal |
| `guardrail` | Technical guardrail or standard | confluence |
| `video` | Tutorial or presentation | youtube, internal |
| `podcast` | Audio discussion or interview | spotify, internal |
| `linkedin-post` | Professional network sharing | linkedin |

---

## Platform Reference

| Platform | Type | Audience |
|----------|------|----------|
| `medium` | Blog | External |
| `substack` | Newsletter | External |
| `confluence` | Wiki | Internal |
| `linkedin` | Professional | External |
| `youtube` | Video | External |
| `spotify` | Podcast | External |
| `internal` | Internal channels | Internal |

---

## Integration with Incubator

Articles are a graduation outcome from the Incubator. When an idea is ready to become a communication piece:

1. Use `/article <title> from <idea>` to create the article
2. Use `/incubator graduate <idea>` to mark the idea as accepted
3. The idea's `outcome` field will link to the new article

Example workflow:
```
# Create article from incubated idea
/article Why Event-Driven Architecture from Event Patterns

# Graduate the incubator idea
incubator graduate Event Patterns
→ Sets outcome to [[Article - Why Event-Driven Architecture]]
```

---

## Reference

- [[Page - Incubator Guide]] - Incubator graduation workflow
- [[.claude/rules/frontmatter-reference.md]] - Article schema
