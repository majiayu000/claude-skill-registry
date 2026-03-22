---
name: docs
description: Documentation workflow — edit markdown docs, technical writing, blog content, release notes without touching source code. Applies Content Writer role. Includes SEO review branch for public-facing content.
argument-hint: [documentation target or section]
---

# Documentation

Safe documentation-only workflow. Edit markdown files without touching application source code, configs, or infrastructure. Applies `Agent(content-writer)` for all writing tasks.

**⚠️ CONSTRAINT: This workflow NEVER modifies source code (*.java, *.ts, *.tsx, *.py, *.go), configs (*.yaml, *.yml, *.json), infrastructure (*.tf, Dockerfile, Helm), or dependency files (pom.xml, package.json, requirements.txt).**

## 1. Define Scope

Ask the user (or extract from parent workflow):

- **What documentation?** (technical docs, API reference, README, PRD, design doc, ADR, blog post, release notes, UI copy)
- **Content type**:
  - **Internal** (technical docs, design docs, ADRs) → `Agent(content-writer)` only
  - **Public-facing** (blog, landing page, marketing) → `Agent(content-writer)` + `Agent(seo-engineer)`
- **Action**: Create new / update existing / restructure
- **Target files**: Which `.md` files will be affected

## 2. Apply Roles

| Content Type | Primary Role | Additional Role |
|---|---|---|
| Technical documentation | `Agent(content-writer)` | — |
| API reference | `Agent(content-writer)` | Stack-specific role for accuracy |
| Blog / landing page content | `Agent(content-writer)` | `Agent(seo-engineer)` |
| PRD / acceptance criteria | `Agent(product-manager)` | — |
| Architecture / ADR | `Agent(solution-architect)` | — |
| Release notes | `Agent(content-writer)` | — |
| UI microcopy | `Agent(content-writer)` | `Agent(frontend-engineer)` for context |
| Page content (landing, product) | `Agent(content-designer)` | `Agent(seo-engineer)`, `Agent(ui-ux-designer)` |

## 3. Gather Context

Before writing:

1. **Read project's `CLAUDE.md`** — terminology, conventions, tech stack
2. **Read existing docs** — understand structure, tone, terminology already in use
3. **Identify Diátaxis mode** — Tutorial, How-to, Reference, or Explanation
4. **Check related code** (read-only) — verify technical accuracy of claims

## 4. Write Content

Follow `Agent(content-writer)` standards:

- **Diátaxis framework** for documentation structure
- **English only** unless explicitly requested otherwise
- **Progressive disclosure** — overview first, details on demand
- **Tested examples** — all code snippets must be accurate
- **Consistent terminology** — match existing project conventions

### For Blog / Public Content

Additionally apply `@humanizer` skill — scan for and remove AI writing patterns. Then follow `Agent(seo-engineer)` standards:

- **Title tag**: Descriptive, matches search intent
- **Meta description**: Compelling summary
- **Heading hierarchy**: One H1, logical H2→H3 flow
- **Internal links**: Descriptive anchor text to related content
- **Images**: Descriptive alt text
- **Structured data**: Article/BlogPosting schema (JSON-LD) where applicable
- **No keyword stuffing** — write for users, not crawlers

## 5. Verify

- [ ] All internal links are valid (no broken references)
- [ ] Code examples are accurate and match current implementation
- [ ] Terminology is consistent with project conventions
- [ ] Formatting follows existing documentation patterns
- [ ] No secrets, PII, or internal-only information in public content
- [ ] No source code, config, or infrastructure files were modified

### For Public Content — Humanization Checklist

- [ ] Text scanned for AI writing patterns (`@humanizer` skill)
- [ ] Anti-AI audit performed for text longer than 2 paragraphs
- [ ] Text sounds natural when read aloud

### For Public Content — SEO Checklist

- [ ] Title and meta description present and unique
- [ ] Heading hierarchy is logical (H1→H2→H3)
- [ ] Internal links with descriptive anchors added
- [ ] Images have alt text
- [ ] Page is indexable (no accidental noindex)
- [ ] Canonical URL is correct
- [ ] Structured data validates (Rich Results Test)

## 6. Summary

```
## Documentation Summary
- **Type**: [technical docs / blog / API reference / release notes / etc.]
- **Content mode**: [Tutorial / How-to / Reference / Explanation]
- **Files changed**:
  - [file1.md]: [created/updated — what changed]
  - [file2.md]: [created/updated — what changed]
- **Role(s) applied**: [Agent(content-writer), Agent(seo-engineer) if public]
- **SEO review**: [pass / N/A for internal docs]
- **Verification**: [links valid, formatting correct, no code files modified]
- **Next steps**: [if any]
```

## Integration

- **Roles**: `Agent(content-writer)` (primary), `Agent(seo-engineer)` (public-facing content), `Agent(product-manager)` (PRDs)
- **Skills**: `@humanizer` (AI writing pattern removal for public-facing content)
- **Rules**: `humanize-content` (auto-enforces humanizer pass)
- **Follow-up**: `/seo-review` (for public content), `/pre-commit`, `/create-pr`
- **Related**: `/feature-dev` (inline docs during development), `/release` (release notes)
