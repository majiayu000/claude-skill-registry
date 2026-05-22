---
name: component-docs
description: Guide for documenting project components and features. Creates or updates documentation in docs/components/ by exploring git changes to understand implementation details. Provides templates and conventions for consistent, developer-friendly component catalogs.
---

# Component Documentation Skill

## Overview

This skill helps document components and features in the jimmodel project. It enables developers to create comprehensive, git-driven documentation that captures **what was implemented, where the code lives, what libraries were used, and how it all works together**.

The skill automatically explores git changes to discover implementation details, checks for existing documentation, and either creates new component docs or updates existing ones with the latest changes. All documentation follows consistent templates and conventions, making it easy for future developers to understand each component.

## When to Use This Skill

Trigger this skill when:
- You've just implemented a significant feature or component
- You want to document an existing feature that's undocumented
- You've made updates to a documented component and want to keep docs current
- A teammate needs to understand how a feature works
- You're onboarding and want to document what you're learning

Examples:
- "I just finished implementing the authentication system, help me document it"
- "Update the database schema docs with the new tables I added"
- "Help me document the API routes structure"
- "Create docs for the styling system"

## How It Works

### Core Workflow: Document a Component

See: **`references/workflows/document-component.md`** for detailed step-by-step instructions.

The workflow:

1. **Identify the component** - Determine what you want to document
2. **Explore git changes** - Use git commands to discover what was actually implemented
3. **Check existing docs** - Is this a new component or an update to existing docs?
4. **Gather details** - Extract files, technologies, configuration from git exploration
5. **Create or update docs** - Use the template to write documentation
6. **Validate** - Use the checklist to ensure completeness

### Key Innovation: Git-Driven Discovery

Instead of relying on memory or assumptions, this skill uses git commands to objectively discover:
- Which files were created/modified
- What dependencies were added
- Configuration changes made
- The actual scope of implementation

**See:** `references/git-exploration-guide.md` for git commands and examples.

### Documentation Template

The template in `assets/component-template.md` includes sections for:
- Overview (what and why)
- Files & Locations (where the code is)
- Technologies & Libraries (what was used)
- Configuration (how to set it up)
- How It Works (the implementation)
- Related Documentation (external links)
- Future Considerations (tech debt, improvements)

## Workflows

### 1. **Document a Component (New or Update)**
**File:** `references/workflows/document-component.md`
**Checklist:** `references/checklists/component-docs-checklist.md`

Complete guide for creating or updating a component document. Includes:
- Git exploration strategy to discover implementation details
- Template population based on findings
- Validation steps to ensure quality

### 2. **Quick Checklist for Validation**
**File:** `references/checklists/component-docs-checklist.md`

Use this checklist to verify your component documentation is complete and ready.

## Resources

### references/
- **`workflows/document-component.md`** - Detailed step-by-step workflow for documenting components
- **`checklists/component-docs-checklist.md`** - Checklist to validate documentation completeness
- **`git-exploration-guide.md`** - Guide to using git commands to discover implementation details

### assets/
- **`component-template.md`** - Markdown template showing all sections and example content for component docs

## File Location

All component documentation goes in: **`docs/components/`**

Files follow naming convention: **`[component-name].md`** (kebab-case)

Examples:
- `docs/components/authentication.md`
- `docs/components/database-schema.md`
- `docs/components/api-routes.md`
- `docs/components/styling-system.md`

## Template Sections at a Glance

| Section | Purpose | Key Info |
|---------|---------|----------|
| **Overview** | What and why | 1-2 sentence summary |
| **Files & Locations** | Where the code lives | File paths with descriptions |
| **Technologies & Libraries** | What was used | Library names, versions, docs links |
| **Configuration** | How to set it up | Env vars, config files, setup steps |
| **How It Works** | The implementation | Flow explanation with file references |
| **API Endpoints** | (if applicable) | Route documentation |
| **Usage Examples** | (if applicable) | Code snippets showing usage |
| **Related Documentation** | Reference links | External docs, internal docs |
| **Future Considerations** | (optional) | Tech debt, planned improvements |

## Quick Start Example

**User:** "I just implemented database schema with Drizzle ORM, can you help me document it?"

**What the skill does:**
1. Asks: "Component name?" → "database-schema"
2. Runs git commands to find changed files in `db/schema/`, `drizzle/`, and `package.json`
3. Checks if `docs/components/database-schema.md` exists (doesn't)
4. Extracts from git:
   - Files: `db/schema/index.ts`, `drizzle/migrations/`, `drizzle.config.ts`
   - Libraries: `drizzle-orm`, `@neondatabase/serverless`
   - Config: Database connection setup
5. Creates `docs/components/database-schema.md` using template
6. Validates against checklist

**Result:** A complete, git-informed component document ready for the team.

## Design Principles

1. **Git-Driven** - Use git to discover facts, not opinions
2. **Template-Based** - Consistency across all component docs
3. **Developer-Focused** - Written for future developers to understand quickly
4. **Comprehensive** - Include all context needed to work with the component
5. **Maintainable** - Easy to update as components evolve
