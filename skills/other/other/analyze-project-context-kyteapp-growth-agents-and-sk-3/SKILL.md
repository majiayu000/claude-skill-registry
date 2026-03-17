---
name: analyze-project-context
description: Use when starting work on any project (technical or non-technical) to understand structure, standards, and best practices before making changes
---

# Analyze Project Context

## Overview

Build comprehensive, evidence-based understanding of ANY project type (code, documentation, content, mixed) before making changes. Works for technical projects, content projects, documentation repositories, and everything in between.

**Core principle:** Discover what exists, infer patterns, document best practices, establish constitution.

## When to Use

Use when:
- Starting work on a new project
- User asks to "analyze the project" or "understand the codebase"
- Before making significant changes
- Need to understand project structure and conventions
- Setting up AI agent workflow for a project

Works for:
- Software projects (Node.js, Python, Go, etc.)
- Documentation repositories
- Content projects (marketing, writing, guides)
- Mixed projects (docs + code)
- Design projects (templates, assets)
- Any organized file structure

## Core Principles

- **Evidence Over Assumption:** Discover what exists, don't assume structure
- **Pattern Recognition:** Infer conventions from existing files
- **Universal Applicability:** Works for any project type
- **Document Findings:** Create AGENTS.md and constitution.md
- **Depth Control:** Use discovery budget (max 2-3 tool calls per category) to avoid analysis paralysis

## Workflow

### 1. Project Type Detection

**Action:** Identify project type from file structure

**Discovery:**
- Check for README.md, README, or similar (project overview)
- Look for technical indicators: `package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`, `pom.xml`, etc.
- Look for content indicators: `docs/`, `content/`, `posts/`, `guides/`, `templates/`
- Check for existing AI/agent files: `.github/`, `.specify/`

**Classify as:**
- **Technical:** Has package managers, source code, build configs
- **Content:** Primarily markdown, templates, media files
- **Documentation:** Organized docs structure, no executable code
- **Mixed:** Contains both code and significant content/docs

### 2. Structural Discovery

**Action:** Map the project organization

**Universal Checks:**
- README.md or equivalent (purpose, structure, getting started)
- Directory structure (identify main folders and their purposes)
- File naming patterns (kebab-case, camelCase, snake_case)
- Organization principles (by feature, by type, by topic)

**Technical Projects (if detected):**
- Package manager files (`package.json`, `requirements.txt`, etc.)
- Source directories (`src/`, `lib/`, `app/`)
- Test directories (`test/`, `__tests__/`, `spec/`)
- Build configs and tooling

**Content Projects (if detected):**
- Content organization (`docs/`, `content/`, `posts/`, `guides/`)
- Templates and reusable components
- Media assets (`images/`, `assets/`, `static/`)
- Style guides or brand guidelines

### 3. Pattern & Convention Discovery

**Action:** Infer project conventions from existing files

**Sample 3-5 representative files** to extract:
- Naming conventions (files, directories, identifiers)
- Structural patterns (how are similar things organized?)
- Documentation patterns (inline comments, separate docs, both?)
- Metadata usage (frontmatter, headers, tags)

**For Technical Projects:**
- Code style (linters, formatters, config files)
- Testing patterns (framework, file locations, naming)
- Import/module patterns
- Error handling conventions

**For Content Projects:**
- Content structure (headings, sections, metadata)
- Cross-referencing patterns (links, includes, references)
- Asset organization and naming
- Version control patterns (drafts, published, archived)

### 4. Standards Documentation Discovery

**Action:** Find existing standards, guidelines, or best practices

**Check for:**
- CONTRIBUTING.md (contribution guidelines)
- STYLE.md or style guides
- ARCHITECTURE.md or technical docs
- AGENTS.md (AI agent best practices) - if exists
- constitution.md (project principles) - if exists
- Templates or examples directory

**Extract existing standards** from these files (don't reinvent what exists)

### 5. Technology Analysis (If Technical Project)

**Action:** Identify actual technology stack

**Sources:**
- Package manager files (dependencies, dev dependencies)
- Config files (tsconfig, babel, webpack, etc.)
- Import/require statements in source files
- Build scripts and deployment configs

**Optional Validation:**
- For major frameworks, verify version-specific patterns
- Check if code matches current best practices for that version
- Identify deprecated patterns or outdated dependencies

**Skip this section** for non-technical projects

### 6. Create AGENTS.md (Best Practices for AI Agents)

**Action:** Generate or update `.github/AGENTS.md` with project-specific best practices

**Structure:**
```markdown
# AI Agent Best Practices: [Project Name]

**Generated:** [Date]
**Project Type:** [Technical/Content/Documentation/Mixed]

## Project Overview
[From README - purpose, goals, audience]

## Working with This Project

### File Organization
- [Pattern 1]: [Explanation and examples]
- [Pattern 2]: [Explanation and examples]

### Naming Conventions
- Files: [Convention with examples]
- [Other identifiers]: [Convention with examples]

### Common Tasks
1. [Task]: [How to do it correctly]
2. [Task]: [How to do it correctly]

### Quality Standards
- [Standard 1]: [What to check]
- [Standard 2]: [What to check]

### What NOT to Do
- ❌ [Anti-pattern]: [Why to avoid]
- ❌ [Anti-pattern]: [Why to avoid]

### Technology-Specific Notes
[Only if technical project - framework versions, patterns, gotchas]

## Related Files
- Constitution: `.specify/memory/constitution.md` (if exists)
- [Other relevant docs]
```

**Base content on discovered patterns** - this is project-specific, not generic advice

### 7. Create/Update Constitution (Project Principles)

**Action:** Trigger `speckit-constitution` skill to create or update `.specify/memory/constitution.md`

**If constitution doesn't exist:**
- Invoke `speckit-constitution` skill
- Suggest principles based on discovered patterns
- Let user refine interactively

**If constitution exists:**
- Report path and note it was found
- Validate current project follows constitution
- Report any violations or gaps

**Constitution should capture:**
- Non-negotiable project principles (MUST)
- Strong recommendations (SHOULD)
- Forbidden patterns or approaches
- Quality gates and standards
- Technology constraints (if technical project)

### 8. Synthesis & Report

**Action:** Generate structured analysis report

**Format:**
```markdown
# Project Analysis: [Project Name]

## Executive Summary
- **Project Type:** [Type]
- **Primary Purpose:** [From README]
- **Key Characteristics:** [3-5 bullet points]

## Structure
[Directory tree or organization description]

## Conventions & Patterns
[Key patterns discovered]

## Standards & Guidelines
- Existing: [List of found docs]
- Created: AGENTS.md with project best practices
- Constitution: [Created/Updated/Found at path]

## Recommendations
1. [Action]: [Reason]
2. [Action]: [Reason]

## Next Steps
[Suggested actions - use existing skills, workflows, or custom tasks]
```

**Present options to user:**
1. Review AGENTS.md and constitution.md
2. Start implementing features (use speckit workflow)
3. Run specific analysis (code quality, documentation coverage, etc.)

## Anti-Patterns (What NOT to Do)

### Universal Anti-Patterns
- **NEVER** assume project structure without verification
- **NEVER** create AGENTS.md with generic, non-specific advice
- **NEVER** skip constitution creation/update
- **NEVER** hallucinate file paths that don't exist
- **NEVER** overwrite existing standards without reviewing them first

### Technical Project Anti-Patterns
- **NEVER** assume framework patterns without checking versions (e.g., Next.js App Router vs Pages)
- **NEVER** skip validation of major dependencies
- **NEVER** guess package manager (could be npm, yarn, pnpm, bun)

### Content Project Anti-Patterns
- **NEVER** ignore existing content organization patterns
- **NEVER** assume markdown is the only format (could be MDX, AsciiDoc, reStructuredText)
- **NEVER** overlook asset organization and naming conventions

## Common Mistakes

| Mistake | Reality |
|---------|---------|
| "All projects have package.json" | Content projects, docs repos don't have code dependencies |
| "I'll skip AGENTS.md for simple projects" | Even simple projects benefit from documented patterns |
| "Constitution is only for code projects" | ALL projects need principles (quality, style, structure) |
| "Generic best practices are enough" | Project-specific patterns are what make AGENTS.md valuable |
| "I can infer everything from README" | READMEs often incomplete - inspect actual files |

## Quick Reference

| Project Type | Key Discovery | Constitution Focus |
|--------------|---------------|-------------------|
| **Technical** | Package manager, tech stack, code patterns | Code quality, tech constraints, testing |
| **Content** | Content structure, frontmatter, assets | Style, tone, structure, publishing |
| **Documentation** | Doc organization, cross-references | Accuracy, consistency, completeness |
| **Mixed** | Both code and content patterns | Both technical and content standards |

## Success Indicators

Analysis is complete when:
- ✅ Project type correctly identified
- ✅ Key directories and organization patterns discovered
- ✅ File naming and structure conventions documented
- ✅ AGENTS.md created with project-specific best practices
- ✅ Constitution created or verified
- ✅ Report generated with actionable next steps
- ✅ No assumptions made without evidence

## Output

**Created Files:**
```
.github/
└── AGENTS.md                  # Project-specific AI agent best practices

.specify/memory/
└── constitution.md            # Project principles (created or updated)
```

**Analysis Report:**
- Project classification
- Structure and conventions
- Standards documentation
- Recommendations and next steps

## Related Skills

- **speckit-constitution** - Create/update project constitution (invoked automatically)
- **speckit** - Full spec-driven development workflow (suggested next step for features)
- **brainstorming** - Explore requirements before making changes
