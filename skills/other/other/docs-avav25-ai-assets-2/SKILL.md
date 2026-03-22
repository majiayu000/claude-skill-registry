---
name: docs
description: Documentation workflow for updating markdown docs, technical writing, PRDs, release notes, and public content without touching application source code.
argument-hint: "[documentation target or section]"
---

# Documentation

Documentation-only workflow. Edit markdown files without touching application source code, configs, or infrastructure.

## Scope

Allowed:

- Markdown docs, PRDs, ADRs
- Release notes
- Blog or marketing copy
- UI microcopy

Not allowed:

- Application source code
- Build config or infrastructure code
- Dependency manifests

## 1. Gather Context

Read:

1. Root `AGENTS.md`
2. Relevant scoped `AGENTS.md`
3. Existing docs in the target area — understand structure, tone, terminology
4. Related code (read-only) when needed for technical accuracy

## 2. Classify the Content

Identify the content type:

| Type | Approach |
|---|---|
| Internal technical docs | Concise, accurate, match existing style |
| Product or planning docs | Structured, stakeholder-readable |
| Public-facing (blog, landing page, marketing) | SEO-aware + humanizer pass |
| Release communication | Changelog format, audience-appropriate |
| UI microcopy | Concise, clear, action-oriented |

## 3. Write

Rules:

- English only unless the user requests otherwise
- Match existing terminology and conventions
- Keep examples technically accurate
- Prefer concise, scannable structure (Diataxis framework where appropriate)
- Progressive disclosure — overview first, details on demand

### For Public Content

Additionally:

- Title tag: descriptive, matches search intent
- Meta description: compelling summary
- Heading hierarchy: one H1, logical H2 → H3 flow
- Internal links: descriptive anchor text to related content
- Images: descriptive alt text
- Structured data: Article/BlogPosting schema where applicable

### Humanization (public content only)

Apply `humanizer` skill:

1. Scan for AI writing patterns
2. Rewrite problematic sections
3. Anti-AI audit for text longer than 2 paragraphs
4. Verify text sounds natural when read aloud

## 4. Verify

Check:

- [ ] All internal links resolve (no broken references)
- [ ] Code examples are accurate and match current implementation
- [ ] Terminology matches project conventions
- [ ] Formatting follows existing documentation patterns
- [ ] No secrets, PII, or internal-only information in public content
- [ ] No source code, config, or infrastructure files were changed

### For Public Content — Humanization Checklist

- [ ] Text scanned for AI writing patterns
- [ ] Anti-AI audit performed for text longer than 2 paragraphs
- [ ] Text sounds natural when read aloud

### For Public Content — SEO Checklist

- [ ] Title and meta description present and unique
- [ ] Heading hierarchy is logical (H1 → H2 → H3)
- [ ] Internal links with descriptive anchors added
- [ ] Images have alt text
- [ ] Page is indexable (no accidental noindex)
- [ ] Canonical URL is correct

## 5. Report

Summarize:

- Content type and Diataxis mode (Tutorial / How-to / Reference / Explanation)
- Files changed (created/updated — what changed)
- SEO review status (pass / N/A for internal docs)
- Humanization status (pass / N/A for internal docs)
- Verification result
- Next steps if any

## Integration

- **Skills**: `humanizer` (AI writing pattern removal for public-facing content), `content-creation` (content brief and tools for blog/landing pages)
- **Rules**: `humanize-content` (enforces humanizer pass on public content)
- **Follow-up**: `seo-review` (for public content), `pre-commit`, `create-pr`
