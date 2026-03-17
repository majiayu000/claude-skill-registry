---
name: writing-product-specs
description: Use when asked to design a new feature or project
---

# Writing Product Specifications

## Overview

Write comprehensive product specification documents that clearly communicate what we're building, why we're building it, and how we'll know it's successful. Document everything stakeholders need to understand: the problem context, target audience, requirements, success criteria, and tradeoffs. Give them a complete picture of the feature or project.

Assume the reader is a skilled product person or engineer, but knows nothing about this specific feature or the problem domain. Assume they need clear context to understand the "why" behind the work.

Announce at start: "I'm using the writing-product-specs skill to create the product specification."

Context: This should be run when designing a new feature or planning a project that needs clear requirements documentation.

Save specs to artifacts named spec-<feature-name>-MM-DD-YYYY.md (or as requested by the user).

**Core principle:** Product specifications are detailed descriptions of the features and functionality of a product. They are used to communicate the requirements of the product to the development team.

## When to Use This Skill

Use this skill when:
- You are explicitly asked to write a product specification, product spec, or PRD (Product Requirements Document)
- You are asked to design a new feature and need to document requirements before implementation
- You are planning a project and need to define what will be built and why
- You need to communicate product requirements to stakeholders, engineers, or designers
- A feature request needs to be expanded into a detailed specification with context, requirements, and success criteria
- You are asked to document the "what" and "why" of a product decision before moving to implementation

## Process for Writing a Product Spec

Follow this process to elicit the necessary information and compose a comprehensive product specification.

### Step 1: Understand the Requested Feature or Project

Ask questions to understand the feature or project. Gather information about:

- **What is it?** What feature or project are we building? What does it do?
- **Who is the audience?** Who are we solving this problem for? What are their roles, personas, or characteristics?
- **What are their problems?** What specific pain points or challenges does the audience face? What is broken or missing?
- **How will this feature/project solve them?** What is the proposed solution? How does it address the problems?
- **How will they benefit? What specifically is the benefit?** What value does this deliver? What outcomes or improvements will users experience?
- **How will we know if we've succeeded?** What are the success metrics, validation criteria, or observable outcomes?
- **How will we know if we've failed?** What would indicate failure? What are the failure modes or negative indicators?
- **What are we NOT doing?** What is explicitly out of scope? What related features or capabilities are we excluding?

Continue asking questions until you have enough information to draft a complete spec. Don't proceed to drafting until you have clear answers to these core questions.

### Step 2: Draft the Specification

Using the information gathered, draft the product specification following the document structure outlined in the **Product Spec Format** section. Present the complete draft to the user.

### Step 3: Iterate Based on Feedback

After presenting the draft:
- Ask the user for edits, clarifications, or additions
- Identify gaps in the spec and ask targeted questions to fill them
- Revise the spec based on feedback
- Continue iterating until the user confirms the spec is complete and accurate

### Step 4: Finalize and Save

Once the user confirms the spec is good enough:
- Review the final spec against the document structure in **Product Spec Format**
- Save the artifact as `spec-<feature-name>-MM-DD-YYYY.md` (or as requested by the user)

## Product Spec Format

Below is the format for a product spec. Each section should be written with clear, actionable guidance.

# [Project / Feature Title]

**Instructions:** Provide a brief (1-2 sentences max) description of what we are building. This is the tl;dr that should explain the entire project and its benefits in a few sentences. A reader should understand the core value proposition from this title and description alone.

**What to include:**
- Clear, descriptive title that captures the feature/project
- One to two sentences summarizing what is being built
- The primary benefit or value this delivers

## Background

### Context

**Instructions:** Describe the world the problem exists in and the problem in broad strokes. Set the stage for why this work matters. Explain the current state, what's happening in the market or user workflows, and why this problem has emerged or become important now.

**What to include:**
- Current state of the world/workflow/system
- Why this problem exists or has become relevant
- Any relevant trends, constraints, or external factors
- The gap between current state and desired state

### Audience

**Instructions:** Identify who we are solving this problem for. Be specific about user personas, roles, or user types. Map to common user personas if possible (e.g., doc writer, product engineer, devops/IT, customer's customer / reader of docs, etc.). If there are multiple audiences, list them and explain how each benefits.

**What to include:**
- Primary user personas or roles affected
- Secondary audiences if applicable
- How each audience will benefit from the solution
- Any specific user characteristics or needs that matter

### Problem Statements

**Instructions:** List the specific problems we are solving. Use bullet format, one problem per bullet. Be succinct and direct—the background context has already been established. Each problem statement should be clear, specific, and actionable.

**What to include:**
- Each problem as a separate bullet point
- Specific, concrete problems (avoid vague statements)
- Problems that are directly addressable by the solution
- Focus on user pain points or business needs

## Hypothesis

**Instructions:** Explain why we believe solving these problems will help customers achieve their goals. This is the "why" behind the "what"—the reasoning that connects the problems to the proposed solution. Articulate the expected outcome and the logic that supports it.

**What to include:**
- The expected outcome if problems are solved
- The logical connection between problems and solution
- Why this approach will be effective
- Any assumptions being made

## Success Criteria

**Instructions:** Define how we will know that the problem is solved. These should be measurable, testable, or observable indicators of success. Include both quantitative metrics (if applicable) and qualitative validation steps.

**What to include:**
- Specific, measurable metrics (e.g., adoption rates, performance improvements, user satisfaction scores)
- QA/validation steps or acceptance criteria
- Observable behaviors or outcomes that indicate success
- Timeframes or thresholds for success (if relevant)

## Requirements

**Instructions:** List what is necessary for us to build in order to solve this problem. Be specific about functional requirements, technical requirements, and constraints. Organize by priority or category if helpful. Each requirement should be clear enough that an engineer can understand what needs to be built.

**What to include:**
- Functional requirements (what the system/feature must do)
- Technical requirements (performance, scalability, compatibility needs)
- User experience requirements (if applicable)
- Integration or dependency requirements
- Prioritization (must-have vs. nice-to-have) if relevant

## Non-requirements

**Instructions:** Explicitly state what we are not doing, what is out of scope, and what we don't have to do. This prevents scope creep and sets clear boundaries. Be specific about related features or capabilities that might seem related but are explicitly excluded.

**What to include:**
- Features or capabilities explicitly out of scope
- Related problems we are not solving
- Future work that might seem related but isn't part of this spec
- Assumptions about what we don't need to build

## Tradeoffs and concerns

**Instructions:** When you write this section just include the placeholder below in italics.

    Especially from engineering, what hard decisions will we have to make in order to implement this solution? What future problems might we have to solve because we chose to implement this?
