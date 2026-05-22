---
name: brief
description: "Create or update project brief through interactive discovery. Use when starting any new idea, revisiting an idea after time away, or when vision feels unclear."
model: claude-opus-4-5-20251101
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /brief

Create or improve project brief through conversational discovery.

## Usage

```bash
/brief                           # Interactive discovery for current or new project
/brief --project coordinatr      # Brief for specific project
/brief --review                  # Analyze existing brief (no edits)
/brief --force                   # Start from scratch
```

## Output Location

```
ideas/[project]/project-brief.md
```

## Execution Flow

### 1. Determine Mode

- **No brief exists** -> Full Discovery Mode
- **Brief exists, no flags** -> Gap-driven update mode
- **`--review` flag** -> Analysis mode (no edits)
- **`--force` flag** -> Fresh start (after confirmation)

### 2. Invoke brief-strategist Agent

For discovery, conduct 6-phase interactive conversation (one question at a time).

### 3. Six-Phase Discovery Topics

1. **Problem Discovery** - What problem? Who experiences it? Current solutions?
2. **Solution Exploration** - How does your solution work? Core value proposition?
3. **Audience Definition** - Who exactly is the target user? Characteristics?
4. **Feature Prioritization** - MVP features? What can wait?
5. **Differentiation** - What makes this different from alternatives?
6. **Success Metrics** - How will you measure success?

## Brief Structure

```markdown
---
status: draft | active | paused | archived
created: YYYY-MM-DD
updated: YYYY-MM-DD
---

# Project Brief: [Project Name]

## Executive Summary
[One-paragraph overview]

## Problem Statement
[Detailed problem description and impact]

## Solution Approach
[How the solution addresses the problem]

## Target Audience
[Specific user personas and characteristics]

## Success Criteria
[Measurable outcomes and validation metrics]

## Scope and Constraints
[Project boundaries and limitations]

## Project Phases
[High-level implementation roadmap]

## Risk Assessment
[Key risks and mitigation strategies]
```

## When to Use

- Starting a new idea
- Revisiting an idea after time away
- Before creating specifications
- When vision feels unclear

**Not needed for**: Quick notes (use notes/), technical research (/research), feature details (/spec)

## Next Steps After Brief

```
/brief -> /critique -> /research -> /spec -> /plan
```
