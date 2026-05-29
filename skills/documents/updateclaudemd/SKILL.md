---
name: updateclaudemd
description: >
  Use when user says "update CLAUDE.md", "refresh the docs", "sync claude config",
  "optimize project instructions", "clean up CLAUDE.md", or when documentation
  is stale, verbose, or out of sync with codebase reality.
argument-hint: (no arguments)
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash(wc:*, head:*)
hooks:
  PreToolUse:
    - matcher: "Write"
      command: "cp CLAUDE.md CLAUDE.md.bak 2>/dev/null || true"
      once: true
---

# Update and Optimize CLAUDE.md

Maintain a clean, focused, and accurate CLAUDE.md file for this project.

## Principles

**CLAUDE.md is shared as context in EVERY Claude Code session.**
- Keep it under 150-250 lines for most projects
- Focus on patterns and principles, not verbose documentation
- Remove redundancy and one-time setup instructions
- Prioritize actionable information that helps code effectively

## Step 1: Read Current State

Read the existing `CLAUDE.md` file to understand its current structure and content.

## Step 2: Understand the Codebase

Explore the project comprehensively to gather accurate knowledge:

1. **Discover the technology stack**
   - Find and read the primary configuration file (package.json, Cargo.toml, requirements.txt, go.mod, etc.)
   - Identify the language, framework, and runtime
   - Note the package/dependency manager

2. **Map the project structure**
   - Use Glob to discover source files and their extensions
   - Identify key directories and their purposes
   - Understand the architectural layout

3. **Identify core systems**
   - Authentication/authorization approach
   - Database or data layer architecture
   - API patterns and endpoints
   - External service integrations

4. **Find the patterns**
   - How are common tasks accomplished in this codebase?
   - What are the established conventions?
   - What design patterns are in use?

5. **Note environment requirements**
   - Required environment variables
   - Configuration needs
   - Development setup requirements

## Step 3: Reconcile and Optimize

Compare codebase reality with current documentation:

**Verify accuracy:**
- Are commands still correct?
- Are dependencies/versions current?
- Are file paths and structures accurate?
- Are environment variables complete?

**Cut aggressively:**
- Remove full code blocks that duplicate source files
- Eliminate verbose explanations
- Delete troubleshooting that's one-time setup
- Remove checklists and detailed how-tos
- Consolidate repetitive information
- Cut "why this matters" philosophical sections

**Keep the essentials:**
- Architecture decisions and patterns
- Essential development commands
- Coding conventions and best practices
- Common code patterns (brief examples only)
- Critical gotchas and non-obvious behaviors
- Design system rules (if applicable)

## Step 4: Structure for Scanning

Organize into clear sections appropriate for this project type:

**Universal sections:**
- Project Overview (tech stack, key philosophy)
- Package Manager (which tool to use)
- Development Commands (essential workflows)
- Architecture Principles (key decisions and patterns)
- Project Structure (directory layout)
- Common Patterns (brief code examples)
- Development Notes (gotchas, quirks)
- Coding Principles (team conventions)

**Conditional sections:**
- Design System (if frontend project)
- Database Schema (high-level only, reference source files)
- Environment Variables (list required, no values)
- Deployment Notes (if relevant to development)

## Step 5: Write the Optimized Version

Update CLAUDE.md with:
- ✅ Scannable structure with clear headers
- ✅ Concise, actionable content
- ✅ Accurate reflection of current codebase
- ✅ Focus on patterns, not verbose docs
- ✅ Technology-appropriate guidance
- ✅ Minimal redundancy

## Output Summary

Provide:
- Line count: before → after
- Major changes made
- Sections removed/added
- Key corrections applied
