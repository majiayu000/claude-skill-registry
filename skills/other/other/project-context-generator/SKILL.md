---
name: project-context-generator
description: Transforms user project requirements into a structured CLAUDE.md context file. Use when starting a new project and need to document project goals, architecture, technical stack, constraints, and conventions. This skill creates the foundational project context file that other skills and agents will reference throughout the project lifecycle.
---

# Project Context Generator

## Overview

This skill transforms unstructured project requirements into a comprehensive CLAUDE.md file that serves as the central context document for your project. It establishes project boundaries, technical decisions, and conventions that guide all subsequent development work.

## When to Use This Skill

Use this skill when:
- Starting a new project and need to establish initial context
- Onboarding Claude to an existing project
- Formalizing requirements and constraints for a project
- Updating project context after significant architectural changes

## Workflow

### Step 1: Gather Project Information

Ask the user for project details across these key areas:

**Project Basics:**
- Project name and one-sentence description
- Primary goals and success criteria
- Target users or use cases

**Technical Decisions:**
- Programming language(s) and framework(s)
- Database and data storage approach
- Deployment target (cloud, on-premise, edge, etc.)
- Key third-party services or APIs

**Project Constraints:**
- Performance requirements
- Security/compliance requirements
- Budget or resource limitations
- Timeline or milestones

**Development Conventions:**
- File and folder structure
- Naming conventions (files, variables, functions)
- Code style preferences
- Testing approach

**Example questions:**
- "What type of project is this? (web app, CLI tool, data pipeline, mobile app, etc.)"
- "What is the primary technology stack?"
- "Are there specific constraints or requirements? (performance, security, compliance)"
- "Do you have preferences for code organization or naming conventions?"

### Step 2: Generate CLAUDE.md

Use the template in `references/claude_md_template.md` to create a structured CLAUDE.md file. Fill in each section based on the gathered information.

The CLAUDE.md file should be created in the **`.claude/` directory** of the project.

**Template sections:**
1. **Project Overview** - Name, description, goals
2. **Technical Architecture** - Stack, structure, key decisions
3. **Project Constraints** - Requirements, limitations, compliance
4. **Development Conventions** - Naming, organization, style
5. **Available Skills** - (Empty initially, populated by skill-analyzer)
6. **Missing Skills** - (Empty initially, populated by skill-analyzer)

### Step 3: Review and Iterate

Present the generated CLAUDE.md to the user for review. Ask:
- "Does this accurately capture your project requirements?"
- "Are there missing constraints or conventions I should document?"
- "Should any technical decisions be refined?"

Iterate based on feedback until the user approves.

### Step 4: Next Steps

After CLAUDE.md is created, inform the user:
- "✅ CLAUDE.md created at [path]"
- "Next: Run `skill-analyzer` to identify relevant skills for your project"

## Important Notes

### Separation of Concerns

This skill **only** generates the project context portion of CLAUDE.md (sections 1-4).

The Skills sections (5-6) are intentionally left empty and will be populated by the `skill-analyzer` skill.

### Project-Specific vs. General Knowledge

Keep project-specific information in CLAUDE.md. Do not modify general skills with project details. This maintains skill reusability across projects.

### Living Document

CLAUDE.md should evolve with the project. Users can re-run this skill to update context as requirements change.

## Resources

### references/claude_md_template.md

A comprehensive template for the CLAUDE.md file structure with placeholder sections and guidance for each part.
