---
name: instructions-development
description: This skill should be used when the user asks to "create CLAUDE.md", "initialize CLAUDE.md", "sync CLAUDE.md with code", "update documentation from codebase", "create .claude/rules/", "manage modular rules", "split large CLAUDE.md", or mentions project documentation setup. Manages complete lifecycle of project instructions including creation, synchronization with code patterns, and modular organization.
---

# Project Instructions Development

Manages the complete lifecycle of project instructions: creating initial documentation, syncing with codebase patterns, and organizing modular rules.

## When to Use This Skill

Use when:
- "Create CLAUDE.md for this project"
- "Initialize CLAUDE.md" or "generate CLAUDE.md"
- "Sync CLAUDE.md with my code"
- "Update documentation from codebase"
- "Extract patterns from code"
- "Create .claude/rules/ structure"
- "Split large CLAUDE.md"
- "Manage modular documentation"

## What This Skill Does

Provides 4 main operations:
- ✅ **Initialize**: Create new CLAUDE.md with opinionated baseline standards
- ✅ **Sync**: Analyze codebase and update documentation with detected patterns
- ✅ **Organize**: Create or manage .claude/rules/ modular structure
- ✅ **Split**: Break large CLAUDE.md into focused rule files

**Note**: .claude/rules/ only works in project directories, not in global ~/.claude/

## CRITICAL RULES

### Language
- **CLAUDE.md MUST be 100% in English** (industry standard)
- Never mix languages in documentation
- Code, comments, and docs all in English

### No Dynamic Data
- **NEVER include**: line counts, file counts, commit statistics, dates, timestamps
- **NEVER write**: "Analyzed X files", "Y lines of code", "Created on..."
- **Only include**: stable patterns, timeless structures, architectural principles

### User Confirmation
- **ALWAYS ask questions** to understand context and preferences
- **ALWAYS show preview** before writing any files
- **ALWAYS get explicit confirmation** before creating/modifying files

## Instructions

### Step 0: Check Global Configuration (CRITICAL)

**Before creating any project-level documentation, ALWAYS read the user's global CLAUDE.md:**

```bash
# Check if global CLAUDE.md exists
~/.claude/CLAUDE.md
```

**If it exists:**
- Read and analyze what rules are already defined globally
- **DO NOT duplicate** global rules in project CLAUDE.md
- Only add project-specific patterns that differ from or extend global rules
- Mention to user: "I found your global CLAUDE.md - I'll only add project-specific rules"

**If it doesn't exist:**
- Proceed normally with project documentation

### Step 1: Determine Operation and Complexity

Use AskUserQuestion tool with THREE questions:

```json
{
  "questions": [
    {
      "question": "What do you need help with?",
      "header": "Operation",
      "multiSelect": false,
      "options": [
        {
          "label": "Create new CLAUDE.md",
          "description": "Start from scratch with opinionated baseline"
        },
        {
          "label": "Sync CLAUDE.md with existing code",
          "description": "Analyze codebase to detect patterns and update docs"
        },
        {
          "label": "Split large CLAUDE.md into rules/",
          "description": "Break CLAUDE.md (>500 lines) into focused files"
        }
      ]
    },
    {
      "question": "What complexity level?",
      "header": "Structure",
      "multiSelect": false,
      "options": [
        {
          "label": "Simple (just CLAUDE.md)",
          "description": "Single file, good for small/medium projects"
        },
        {
          "label": "Modular (CLAUDE.md + .claude/rules/)",
          "description": "Multiple files with path patterns, for large projects"
        }
      ]
    },
    {
      "question": "Should this be shared with your team or kept local?",
      "header": "Sharing",
      "multiSelect": false,
      "options": [
        {
          "label": "Shared (CLAUDE.md)",
          "description": "Committed to git, shared across team and sessions"
        },
        {
          "label": "Local only (CLAUDE.local.md)",
          "description": "Git-ignored, personal workspace rules only"
        }
      ]
    }
  ]
}
```

Route to workflow:
- **Create new + Simple + Shared** → Initialize Workflow (Step 2) - CLAUDE.md
- **Create new + Simple + Local** → Initialize Workflow (Step 2) - CLAUDE.local.md + add to .gitignore
- **Create new + Modular + Shared** → Initialize Workflow (Step 2) + Organize Workflow (Step 4) - CLAUDE.md
- **Create new + Modular + Local** → Initialize Workflow (Step 2) + Organize Workflow (Step 4) - CLAUDE.local.md + add to .gitignore
- **Sync + Simple + Shared** → Sync Workflow (Step 3) - update CLAUDE.md
- **Sync + Simple + Local** → Sync Workflow (Step 3) - update CLAUDE.local.md
- **Sync + Modular** → Sync Workflow (Step 3) + Organize Workflow (Step 4)
- **Split** → Split Workflow (Step 5)

---

### Step 2: Initialize Workflow (Create New CLAUDE.md)

Create opinionated baseline CLAUDE.md for new projects.

**Process**:

1. **Determine filename** (from Step 1 answer):
   - Shared → `CLAUDE.md`
   - Local only → `CLAUDE.local.md`

2. **Detect project type**
   - Check if it's a code project (package.json, requirements.txt, go.mod, etc.)
   - Or non-code (docs, notes, research, etc.)
   - Ask user if unclear

3. **Think through design**:
   - Minimum viable CLAUDE.md?
   - Similar projects/patterns?
   - Architectural trade-offs?
   - Common pitfalls in this stack?

4. **Show preview** with:
   - Structure outline
   - Key sections
   - Estimated line count
   - Architecture reasoning
   - Filename that will be created

5. **Generate and write** (after confirmation):
   - Single file: ~150-250 lines
   - Modular: ~100-150 lines with references to rules/
   - Use determined filename from step 1

6. **If local only (CLAUDE.local.md):**
   - Add `CLAUDE.local.md` to `.gitignore`
   - Create .gitignore if it doesn't exist
   - Inform user it's git-ignored

7. **Inform user** with next steps

**See `references/initialize-workflow.md` for complete details**

---

### Step 3: Sync Workflow (Analyze Code and Update Docs)

Analyze codebase to extract patterns and update documentation.

**Process**:

1. **Detect current setup**:
   - Check if CLAUDE.md exists
   - Check if .claude/rules/ exists
   - Determine mode: CREATE, UPDATE Single, UPDATE Modular

2. **Analyze codebase** (use Task tool with Explore agent):
   - Main source directory
   - Tech stack
   - Folder organization
   - Test patterns

3. **Extract patterns**:
   - Naming conventions (files, functions, variables)
   - Architectural pattern (FSD, Feature-First, etc.)
   - Import patterns
   - Testing conventions
   - Component/API patterns

4. **Think through findings**:
   - Stable (>80%) vs emerging patterns
   - What to document vs leave implicit
   - Single file or modular approach

5. **Show findings** to user:
   - Detected patterns
   - Mismatches with documented patterns
   - Recommendations

6. **Ask approach** (AskUserQuestion):
   - Update CLAUDE.md (single file)
   - Create .claude/rules/ (modular)
   - Show both options

7. **Generate updates** and write (after confirmation)

8. **Inform user** with summary of changes

**See `references/sync-workflow.md` for complete details**

---

### Step 4: Organize Workflow (Create .claude/rules/ Structure)

Set up modular documentation with focused rule files.

**Process**:

1. **Detect stack** (same as initialize)

2. **Ask which rules to create** (AskUserQuestion):
   - coding-standards.md (recommended)
   - architecture.md (recommended)
   - testing.md
   - api.md

3. **Think through design**:
   - What in each file vs CLAUDE.md
   - Path patterns for each file
   - Keep each file <200 lines

4. **Show preview**:
   - File structure
   - Estimated line counts
   - Path patterns
   - CLAUDE.md updates

5. **Create files** (after confirmation):
   - Create .claude/rules/ directory
   - Create each rule file with YAML frontmatter
   - Update CLAUDE.md to reference rules

6. **Inform user** with structure overview

**See `references/organize-and-split-workflows.md` for templates and details**

---

### Step 5: Split Workflow (Break Large CLAUDE.md)

Break CLAUDE.md (>500 lines) into focused modular files.

**Process**:

1. **Read and analyze CLAUDE.md**:
   - Identify sections
   - Core vs detailed content
   - Line counts per section

2. **Think through split strategy**:
   - What stays in CLAUDE.md (core standards)
   - What moves to rules/ (detailed guidelines)
   - Organize by topic
   - Path patterns

3. **Show split preview**:
   - Current vs after structure
   - What moves where
   - Line count reduction

4. **Execute split** (after confirmation):
   - Create .claude/rules/
   - Create rule files with moved content
   - Update CLAUDE.md (remove moved, add references)

5. **Inform user** with results

**See `references/organize-and-split-workflows.md` for complete details**

---

## Architecture Pattern Selection

Quick reference:

| Stack | Recommended Pattern |
|-------|-------------------|
| React/Vue SPA | Feature-Sliced Design (FSD) |
| Next.js | FSD or Feature-First |
| Express/Fastify | Feature-First |
| NestJS | Feature-First |
| Django/Flask | MVC |
| Rails | MVC |
| Spring Boot | Package by Feature |
| Go API | Package by Feature |

**See `references/architecture-patterns.md` for complete guide**

## Path Pattern Examples

```yaml
# Coding standards for TypeScript
---
paths: src/**/*.{ts,tsx}
---

# Testing conventions
---
paths: **/*.{test,spec}.*
---

# API-specific rules
---
paths: src/{api,routes}/**/*
---
```

## Related Settings Configuration

### respectGitignore

Control whether `@-mention` file picker respects .gitignore:

```json
{
  "respectGitignore": true
}
```

Add to `.claude/settings.json` (project-specific) or `~/.claude/settings.json` (global).

**Use when:** You want file suggestions to exclude gitignored files

### fileSuggestion

Customize `@` file search commands:

```json
{
  "fileSuggestion": {
    "command": "rg --files",
    "timeout": 5000
  }
}
```

**Use when:**
- You want faster file search than default
- You need custom filtering logic
- You have specific tooling (e.g., fd, find with custom flags)

These settings affect how documentation discovery and file reference tools work.

## Best Practices

1. ✅ Ask questions first - Understand user needs
2. ✅ Show previews - Confirm before writing
3. ✅ English only - 100% English content
4. ✅ No dynamic data - Only stable patterns
5. ✅ Opinionated defaults - But let user choose
6. ✅ Explain choices - Why this architecture?
7. ✅ Keep concise - CLAUDE.md 150-250 lines, rules <200 lines
8. ✅ Think step-by-step - Analyze before generating
9. ✅ Progressive disclosure - Core in CLAUDE.md, details in rules/

## Anti-Patterns

- ❌ Generating without asking questions
- ❌ Writing files without preview/confirmation
- ❌ Including line counts, file counts, dates, statistics
- ❌ Mixed languages (English + other)
- ❌ "Analyzed X files" or dynamic statements
- ❌ Timestamps or "last updated"
- ❌ Overly long files (>500 lines CLAUDE.md, >200 lines rules)
- ❌ Not explaining architectural choices
- ❌ Duplicating content between CLAUDE.md and rules/

## Additional Resources

### Reference Files

Complete workflows and detailed guides:

- **`references/initialize-workflow.md`** - Creating new CLAUDE.md from scratch
- **`references/sync-workflow.md`** - Analyzing code and extracting patterns
- **`references/organize-and-split-workflows.md`** - Managing .claude/rules/ structure
- **`references/modular-organization.md`** - Modular documentation guide
- **`references/architecture-patterns.md`** - Complete architecture pattern guide

### Examples

Study these as templates:

- **`examples/minimal-claude-md.md`** - Single file example (~200 lines)
- **`examples/modular-setup/`** - Complete modular structure
  - CLAUDE.md (minimal core)
  - .claude/rules/coding-standards.md
  - .claude/rules/architecture.md

## Quick Decision Trees

### Which Approach?

```
Project size?
├─ <10k lines → Single file CLAUDE.md
└─ >10k lines → Modular with .claude/rules/

Different rules for different areas?
├─ Yes → Modular (use path patterns)
└─ No → Single file
```

### Which Operation?

```
Have documentation?
├─ No → Initialize workflow
└─ Yes → Is it outdated?
    ├─ Yes → Sync workflow
    └─ No → Is it >500 lines?
        ├─ Yes → Split workflow
        └─ No → Organize workflow (if want modular)
```

### Which Architecture?

```
Type of project?
├─ Frontend SPA (React/Vue)
│   ├─ Large (>50k lines) → FSD
│   └─ Medium → Feature-First
├─ Backend API
│   ├─ Go/Java/C# → Package by Feature
│   ├─ Express/Flask/FastAPI → Feature-First
│   └─ Django/Rails → MVC
└─ Unsure → Ask user preferences
```

## Output Examples

**Initialize (Single File)**:
- New CLAUDE.md: 150-250 lines
- English, opinionated baseline
- Core standards + Architecture + Git

**Initialize (Modular)**:
- Minimal CLAUDE.md: 100-150 lines
- Note to run organize workflow next

**Sync**:
- Updated CLAUDE.md with detected patterns
- Or created/updated .claude/rules/ files
- Summary of changes

**Organize**:
- .claude/rules/ structure
- Focused files (<200 lines each)
- Updated CLAUDE.md with references

**Split**:
- Reduced CLAUDE.md (~100-150 lines)
- New .claude/rules/ files
- Better organization

---

*All outputs: 100% English, no dynamic data, user-confirmed, ready to use*
