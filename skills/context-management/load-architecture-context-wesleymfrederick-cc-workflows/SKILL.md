---
name: load-architecture-context
description: Load architecture principles and core conventions for grounding work against project standards - simple context loading for all workflow stages
---

# Context-Aware Evaluation

## Purpose

This skill loads comprehensive architecture context to ground your work against project standards. Use it before creating PRDs, designs, implementation plans, or code to ensure alignment with established principles and conventions.

## What Gets Loaded

**All Architecture Principles:**
- Complete ARCHITECTURE-PRINCIPLES.md (all 9 principle categories)

**Core Architecture Conventions:**
- Code Organization and Structure
- Development Workflow
- Coding Standards and Conventions
- Testing Strategy

## How to Use This Skill

### Step 1: Load Architecture Principles

Use citation-manager to extract the complete principles document:

```bash
citation-manager extract file ARCHITECTURE-PRINCIPLES.md
```

Read and internalize all principle categories to understand project architectural standards.

### Step 2: Load Core Conventions

Use citation-manager to extract each core convention section from ARCHITECTURE.md:

```bash
citation-manager extract header ARCHITECTURE.md "Code Organization and Structure"
citation-manager extract header ARCHITECTURE.md "Development Workflow"
citation-manager extract header ARCHITECTURE.md "Coding Standards and Conventions"
citation-manager extract header ARCHITECTURE.md "Testing Strategy"
```

Read each section to understand how conventions apply to your current work.

### Step 3: Apply Context

With principles and conventions loaded, proceed with your work:
- Creating PRDs: Apply MVP principles, progressive disclosure, clear requirements
- Creating designs: Apply modular design, data-first principles, interface design
- Writing plans: Apply action-based organization, self-contained naming, safety patterns
- Writing code: Follow coding standards, workflow conventions, testing strategy

## When to Use This Skill

Use this skill proactively **before** starting work on:
- Requirements documents (PRDs, user stories)
- Design documents (architecture, ADRs)
- Implementation plans (detailed task breakdowns)
- Code implementation (features, refactoring)
- Test implementation (test plans, test code)

## What This Skill Is NOT

This is **grounding** (loading context before work), not **evaluation** (validating work after completion).

For validation after creating documents, use the `evaluate-against-architecture-principles` skill instead.
