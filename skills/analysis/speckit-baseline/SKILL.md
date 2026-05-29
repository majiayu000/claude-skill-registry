---
name: speckit-baseline
description: Generate feature specifications by analyzing existing source code.
allowed-tools: Bash, Read, Write, Grep, Glob
handoffs:
  - label: Clarify Generated Spec
    agent: speckit.clarify
    prompt: Clarify specification requirements
    send: true
  - label: Create Implementation Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
---

# Spec-Kit Baseline

Generate structured feature specifications by analyzing existing source code. Reverse-engineers requirements, user stories, and success criteria from implementation.

## When to Use

- Documenting existing features that lack specifications
- Understanding legacy code before refactoring
- Creating specs for inherited or acquired codebases
- Generating documentation from implemented functionality
- Preparing brownfield code for the Spec Kit workflow

## Execution Workflow

The user's input after the skill invocation specifies the code to analyze. The workflow:

1. **Parse target input**: Identify files, directories, or patterns to analyze
   - Accept file paths, glob patterns, or directory paths
   - If empty: ERROR "No code target provided - specify files, directories, or patterns"

2. **Discover and read source files**:
   - Expand glob patterns to file list
   - Read file contents for analysis
   - Identify primary language(s) and frameworks
   - Map file relationships and dependencies

3. **Analyze code structure**:
   - Identify entry points and public interfaces
   - Extract function/method signatures and behaviors
   - Find data models and entities
   - Detect API endpoints and routes
   - Identify user-facing functionality

4. **Generate short name** (2-4 words) from analyzed code:
   - Use action-noun format (e.g., "user-auth", "payment-processing")
   - Base on primary functionality discovered
   - Preserve technical terms where meaningful

5. **Check for existing branches/specs** and run setup script:
   - Find highest feature number for this short-name
   - Run `.specify/scripts/bash/create-new-feature.sh --json` with calculated number and short-name
   - Get BRANCH_NAME and SPEC_FILE paths from JSON output

6. **Load spec template** from `.specify/templates/spec-template.md`

7. **Generate specification content**:
   - **User Stories**: Infer from user-facing code paths and interactions
   - **Acceptance Scenarios**: Derive from test cases, validation logic, error handling
   - **Functional Requirements**: Extract from business logic and constraints
   - **Key Entities**: Identify from data models and schemas
   - **Success Criteria**: Infer from existing metrics, logging, or performance code
   - **Assumptions**: Document inferences made during analysis

8. **Abstract implementation details**:
   - Convert technical patterns to user-focused requirements
   - Remove framework-specific terminology
   - Focus on WHAT the code does, not HOW it does it
   - Express behaviors in technology-agnostic terms

9. **Create spec quality checklist** at `FEATURE_DIR/checklists/requirements.md`

10. **Report completion** with:
    - Branch name and spec file path
    - Summary of analyzed files
    - Key features discovered
    - Areas needing clarification or review

## Key Points

- Focus on extracting WHAT and WHY from HOW
- Abstract away implementation details in the generated spec
- Document assumptions made during code analysis
- Flag areas where code behavior is unclear
- Preserve discovered business rules and constraints
- Use [NEEDS CLARIFICATION] for ambiguous code sections (max 3)
- Generated specs should be validated by someone who knows the feature

## Example Transformations

**Code Pattern → Spec Requirement**:

- `if (user.role === 'admin')` → "System MUST restrict action to administrator users"
- `password.length >= 8` → "Passwords MUST be at least 8 characters"
- `cache.set(key, value, 3600)` → "System MUST cache results for improved performance"
- `try { ... } catch (e) { notify(e) }` → "System MUST notify users when errors occur"

**Code Pattern → User Story**:

- Login endpoint with OAuth → "As a user, I can sign in using my social account"
- Shopping cart logic → "As a customer, I can add items to my cart for later purchase"
- Report generation → "As an analyst, I can generate reports on system activity"

## Next Steps

After generating spec.md:

- **Clarify** with domain experts using `speckit-clarify`
- **Plan** modernization/refactoring with `speckit-plan`
- **Compare** generated spec with actual requirements to identify gaps

## See Also

- `speckit-specify` - Create specs from descriptions (forward direction)
- `speckit-clarify` - Resolve specification ambiguities
- `speckit-plan` - Create technical implementation strategy
