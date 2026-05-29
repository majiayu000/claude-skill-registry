---
name: update-system-map
description: Update the System Knowledge Map documentation
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Task
---

# Update System Knowledge Map

Perform a codebase archaeology investigation and update `docs/SYSTEM_KNOWLEDGE_MAP.md` with current system state.

## Investigation Plan

### Phase 1: Reconnaissance (Tech Stack)
1. Read `package.json` for dependencies and scripts
2. Read `nuxt.config.ts` for framework configuration
3. List `app/` directory structure

### Phase 2: Data Model Discovery (The Nouns)
1. Read `content.config.ts` for collection schemas and content types
2. Count items in `content/`, `content/authors/`, `content/podcasts/`
3. Identify any new entity types or schema changes

### Phase 3: Capabilities Discovery (The Verbs)
1. List `app/pages/` for route handlers
2. List `server/api/` for API endpoints
3. Read key pages to understand features
4. List `app/composables/` for reusable logic

### Phase 4: Business Rules
1. Grep for validation logic in `content.config.ts`
2. Check for any new business rules in server/api handlers
3. Review any constants or config files

### Phase 5: Generate Report
Update `docs/SYSTEM_KNOWLEDGE_MAP.md` with:

```markdown
# System Knowledge Map

> Auto-generated codebase archaeology report for non-technical stakeholders
> Last updated: [current date]

## 1. High-Level Overview
- What this system does (1-2 sentences)
- Tech stack table

## 2. Core Business Entities (The Nouns)
- Content (with all type variants and key attributes)
- Authors
- Podcasts
- Tweets
- Any new entities

## 3. Key Capabilities (The Verbs)
- Content management features
- Discovery & navigation features
- Visualization features
- Reading experience features

## 4. Business Rules & Logic
- Validation rules with file:line references
- Workflows (e.g., reading status)
- Naming conventions

## 5. Integrations
- External services
- Internal modules

## 6. API Surface
- All endpoints with methods and purposes

## 7. File Structure
- Key directories and their purposes

## 8. Current Scale
- Approximate counts of content, authors, etc.
```

## Important Guidelines

- **Be thorough**: Read actual files, don't assume
- **Include counts**: Provide real numbers for scale section
- **Add line references**: For business rules, include `file.ts:line`
- **Update timestamp**: Always update the "Last updated" date
- **Preserve structure**: Keep the same section headings for consistency
