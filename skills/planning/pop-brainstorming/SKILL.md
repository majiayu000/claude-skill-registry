---
name: brainstorming
description: "Collaborative design refinement that transforms rough ideas into fully-formed specifications through Socratic questioning. Explores alternatives, validates incrementally, and presents designs in digestible chunks for feedback. Use before writing code or implementation plans when requirements are unclear or multiple approaches exist. Do NOT use when requirements are already well-defined, you're implementing a known pattern, or making small changes - proceed directly to implementation instead."
inputs:
  - from: any
    field: topic
    required: false
outputs:
  - field: design_document
    type: file_path
  - field: github_issue
    type: issue_number
next_skills:
  - pop-writing-plans
  - pop-subagent-driven
workflow:
  id: brainstorming
  name: Brainstorming Workflow
  version: 1
  description: Transform rough ideas into fully-formed designs
  steps:
    - id: github_check
      description: Check for existing related work in GitHub
      type: skill
      skill: pop-knowledge-lookup
      next: existing_work_decision
    - id: existing_work_decision
      description: Decide how to proceed with existing work
      type: user_decision
      question: "Found existing work. How should we proceed?"
      header: "Existing"
      options:
        - id: use_existing
          label: "Use existing"
          description: "Build on what's already there"
          next: gather_context
        - id: enhance
          label: "Enhance"
          description: "Extend existing with new features"
          next: gather_context
        - id: fresh
          label: "Start fresh"
          description: "Create new design"
          next: gather_context
      next_map:
        use_existing: gather_context
        enhance: gather_context
        fresh: gather_context
    - id: gather_context
      description: Understand the idea through questions
      type: agent
      agent: code-explorer
      next: approach_decision
    - id: approach_decision
      description: Choose implementation approach
      type: user_decision
      question: "Which approach should we take?"
      header: "Approach"
      options:
        - id: minimal
          label: "Minimal"
          description: "Simple, quick implementation"
          next: present_design
        - id: balanced
          label: "Balanced"
          description: "Standard approach with reasonable coverage"
          next: present_design
        - id: comprehensive
          label: "Comprehensive"
          description: "Full implementation with all edge cases"
          next: present_design
      next_map:
        minimal: present_design
        balanced: present_design
        comprehensive: present_design
    - id: present_design
      description: Present design in sections for validation
      type: skill
      skill: pop-auto-docs
      next: next_step_decision
    - id: next_step_decision
      description: Decide what to do after design
      type: user_decision
      question: "Design complete. What's next?"
      header: "Next Step"
      options:
        - id: plan
          label: "Create plan"
          description: "Generate implementation plan"
          next: create_plan
        - id: issue
          label: "Create issue"
          description: "Create GitHub issue only"
          next: create_issue
        - id: done
          label: "Done"
          description: "Stop here for now"
          next: complete
      next_map:
        plan: create_plan
        issue: create_issue
        done: complete
    - id: create_plan
      description: Generate implementation plan
      type: skill
      skill: pop-writing-plans
      next: complete
    - id: create_issue
      description: Create GitHub issue from design
      type: skill
      skill: pop-research-capture
      next: complete
    - id: complete
      description: Brainstorming workflow complete
      type: terminal
---

# Brainstorming Ideas Into Designs

## Overview

Help turn ideas into fully formed designs and specs through natural collaborative dialogue.

Start by understanding the current project context, then ask questions one at a time to refine the idea. Once you understand what you're building, present the design in small sections (200-300 words), checking after each section whether it looks right so far.

**Announce at start:** "I'm using the brainstorming skill to refine this idea into a design."

## Step 0: GitHub-First Check (Required)

**BEFORE brainstorming**, verify this work hasn't been done or planned:

### 1. Search GitHub Issues

```bash
# Search for existing/related issues
gh issue list --search "<topic keywords>" --state all --json number,title,state --limit 10
```

### 2. Search Existing Skills and Code

```bash
# Search for related skills
grep -r "<keywords>" packages/plugin/skills/ --include="SKILL.md" -l

# Search for related utilities
grep -r "<keywords>" packages/plugin/hooks/utils/ --include="*.py" -l
```

### 3. Check Upstream Context

```python
# Check if another skill passed context to us
from popkit_shared.utils.skill_context import load_skill_context

ctx = load_skill_context()
if ctx and ctx.previous_output:
    # Use existing context instead of re-asking
    topic = ctx.previous_output.get("topic")
    existing_decisions = ctx.shared_decisions
```

### 4. Present Findings via AskUserQuestion

If related issues or code found:

```
Use AskUserQuestion tool with:
- question: "Found existing work related to '<topic>'. How should we proceed?"
- header: "Existing"
- options:
  - label: "Use existing"
    description: "Build on what's already there"
  - label: "Enhance"
    description: "Extend existing with new features"
  - label: "Start fresh"
    description: "Create new (explain why existing doesn't fit)"
- multiSelect: false
```

**Only proceed to brainstorming after completing this check.**

## User Interaction Pattern

**ALWAYS use AskUserQuestion** for decisions and clarifications:

```
Use AskUserQuestion tool with:
- question: Clear, specific question ending with "?"
- header: Short label (max 12 chars): "Approach", "Auth", "Database"
- options: 2-4 choices with labels and descriptions
- multiSelect: false (unless multiple selections make sense)
```

**NEVER present options as plain text** like "1. Option A, 2. Option B - type 1 or 2".

## The Process

**Understanding the idea:**

- Check out the current project state first (files, docs, recent commits)
- Ask questions one at a time to refine the idea using AskUserQuestion
- Only one question per message - if a topic needs more exploration, break it into multiple questions
- Focus on understanding: purpose, constraints, success criteria

**Exploring approaches:**

- Propose 2-3 different approaches with trade-offs using AskUserQuestion
- Each option should have a clear label and description explaining trade-offs
- Lead with your recommended option by listing it first

**Presenting the design:**

- Once you believe you understand what you're building, present the design
- Break it into sections of 200-300 words
- Ask after each section whether it looks right so far
- Cover: architecture, components, data flow, error handling, testing
- Be ready to go back and clarify if something doesn't make sense

## After the Design

**Documentation:**

- Write the validated design to `docs/plans/YYYY-MM-DD-<topic>-design.md`
- Commit the design document to git

**Context Handoff (for downstream skills):**

```python
# Save context for pop-writing-plans or other downstream skills
from popkit_shared.utils.skill_context import save_skill_context, SkillOutput, link_workflow_to_issue

# Save design output
save_skill_context(SkillOutput(
    skill_name="pop-brainstorming",
    status="completed",
    output={
        "topic": "<topic>",
        "approach": "<chosen approach>",
        "design_summary": "<brief summary>"
    },
    artifacts=["docs/plans/YYYY-MM-DD-<topic>-design.md"],
    next_suggested="pop-writing-plans",
    decisions_made=[<list of AskUserQuestion results>]
))

# If GitHub issue exists, link it
if issue_number:
    link_workflow_to_issue(issue_number)
```

**Create or Link GitHub Issue:**

```bash
# If no issue exists, offer to create one
gh issue create --title "[Design] <topic>" --body "Design document: docs/plans/..."
```

**Implementation (if continuing):**

- Use AskUserQuestion: "Design complete. What's next?"
- Options: "Create implementation plan", "Create issue only", "Done for now"
- Use pop:writing-plans skill to create detailed implementation plan (receives context automatically)

## Key Principles

- **One question at a time** - Don't overwhelm with multiple questions
- **Always use AskUserQuestion** - Interactive prompts, never plain text options
- **YAGNI ruthlessly** - Remove unnecessary features from all designs
- **Explore alternatives** - Always propose 2-3 approaches before settling
- **Incremental validation** - Present design in sections, validate each
- **Be flexible** - Go back and clarify when something doesn't make sense

## PDF Input Support

When provided with a PDF file path (design doc, spec, or requirements), read it first:

```
User: Here's the design doc: /path/to/design.pdf
```

**Process PDF input:**

1. Use Read tool to analyze the PDF content
2. Extract key requirements, constraints, and goals
3. Identify areas that need clarification
4. Use extracted context to inform the brainstorming process

**When reading design PDFs:**

- Look for: objectives, user stories, constraints, success criteria
- Note gaps: missing acceptance criteria, unclear requirements
- Identify: dependencies, technical constraints, timeline pressures
- Flag: ambiguities that need clarification during brainstorming

This allows brainstorming to start from existing documentation rather than from scratch.
