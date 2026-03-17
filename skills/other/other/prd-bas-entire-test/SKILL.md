---
name: prd
description: Create comprehensive Product Requirements Documents (PRDs) for new features or products. Use this skill when the user asks to create a PRD, product spec, feature specification, or product requirements. Generates structured, detailed documentation covering problem statement, user stories, requirements, success metrics, and technical considerations.
---

This skill guides creation of comprehensive Product Requirements Documents (PRDs) that clearly define product features, requirements, and success criteria.

The user provides a feature idea, product concept, or requirement that needs to be documented. The skill helps structure this into a professional PRD that serves as a source of truth for development.

## PRD Structure

A complete PRD should include the following sections:

### 1. Overview
- **Title**: Clear, descriptive name for the feature/product
- **Author**: Document owner
- **Date**: Created/last updated
- **Status**: Draft, In Review, Approved, or In Development

### 2. Problem Statement
- What problem are we solving?
- Who experiences this problem?
- Why is this important to solve now?
- What happens if we don't solve it?

### 3. Goals & Success Metrics
- **Primary Goals**: What are we trying to achieve?
- **Success Metrics**: How will we measure success? (quantifiable KPIs)
- **Non-Goals**: What is explicitly out of scope?

### 4. User Stories & Personas
- Who are the target users?
- What are their needs and pain points?
- User stories in format: "As a [user type], I want [goal] so that [benefit]"

### 5. Requirements

#### Functional Requirements
- Core features and functionality (numbered list)
- User interactions and workflows
- Business logic and rules

#### Non-Functional Requirements
- Performance expectations
- Security requirements
- Accessibility standards
- Browser/device support

### 6. User Experience

#### User Flow
- Step-by-step walkthrough of the user journey
- Entry points and exit points
- Decision trees and branching logic

#### Wireframes/Mockups (if applicable)
- Visual representation of key screens
- Navigation patterns
- Component specifications

### 7. Technical Considerations
- Architecture implications
- Data model changes
- API requirements
- Third-party integrations
- Performance considerations
- Migration/rollout strategy

### 8. Dependencies & Assumptions
- What needs to exist before this can be built?
- What are we assuming to be true?
- Blockers or risks

### 9. Open Questions
- Unresolved decisions
- Areas needing further research
- Items requiring stakeholder input

### 10. Timeline & Milestones
- Proposed phases or milestones (avoid specific dates, focus on sequence)
- MVP vs. full feature scope
- Release strategy

## Workflow

When creating a PRD:

1. **Gather Context**: Ask clarifying questions about the feature/product:
   - What problem does this solve?
   - Who is the target user?
   - What are the must-have vs. nice-to-have features?
   - Are there any constraints (technical, timeline, resources)?

2. **Research Existing Patterns**: If working in an existing codebase:
   - Review similar features for consistency
   - Understand current architecture and patterns
   - Identify reusable components or patterns

3. **Structure the Document**: Create a well-organized PRD following the structure above:
   - Start with a clear problem statement
   - Define measurable success criteria
   - Detail requirements with specificity
   - Include user flows and technical considerations

4. **Be Specific**: Avoid vague language:
   - ❌ "The system should be fast"
   - ✅ "API responses should return in <200ms for 95% of requests"

   - ❌ "Users can manage their profile"
   - ✅ "Users can update their name, email, avatar, and notification preferences from the profile settings page"

5. **Validate Completeness**: Ensure the PRD answers:
   - WHY: Why are we building this?
   - WHO: Who is this for?
   - WHAT: What exactly are we building?
   - HOW: How will it work (user perspective)?
   - WHEN: What's the phased approach?
   - SUCCESS: How do we know it's working?

## Output Format

Generate the PRD as a well-formatted Markdown document based on the [template](./TEMPLATE.md) that can be saved to the project's documentation directory (e.g., `docs/prd/` or `.github/prd/`).

Use clear formatting:
- Headings for sections
- Numbered lists for requirements
- Tables for comparing options
- Code blocks for technical specs
- Checkboxes for tracking items

## Best Practices

- **Clarity over Cleverness**: Write for diverse audiences (designers, engineers, PMs, stakeholders)
- **Measurable Goals**: Every goal should have quantifiable success metrics
- **User-Centric**: Always tie back to user value and problems being solved
- **Living Document**: PRDs should evolve; include revision history
- **Validate Assumptions**: Call out what's assumed vs. validated
- **Scope Management**: Clearly define what's in scope vs. out of scope
- **Visual Aids**: Include diagrams, flows, and mockups when helpful

## Example Usage

User: "Create a PRD for adding a shopping cart to our e-commerce site"

Agent should:
1. Ask clarifying questions (guest checkout? saved carts? cart sharing?)
2. Research existing product/checkout patterns in the codebase
3. Generate comprehensive PRD covering all sections
4. Save to appropriate location (e.g., `docs/prd/shopping-cart.md`)
