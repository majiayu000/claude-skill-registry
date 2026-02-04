---
name: spec_driven_development.constitution
description: "Creates foundational governance principles and development guidelines for the project. Use when starting a new project or establishing standards."
user-invocable: false
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Priorities Captured**: Did the agent gather specific development priorities from the user?
            2. **Principles Defined**: Are governance principles clear and actionable?
            3. **Technology Guidance**: Does the constitution include relevant technology stack preferences?
            4. **Quality Standards**: Are quality standards and testing expectations defined?
            5. **File Created**: Has constitution.md been created in the project's documentation folder?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
  SubagentStop:
    - hooks:
        - type: prompt
          prompt: |
            You must evaluate whether Claude has met all the below quality criteria for the request.

            ## Quality Criteria

            1. **Priorities Captured**: Did the agent gather specific development priorities from the user?
            2. **Principles Defined**: Are governance principles clear and actionable?
            3. **Technology Guidance**: Does the constitution include relevant technology stack preferences?
            4. **Quality Standards**: Are quality standards and testing expectations defined?
            5. **File Created**: Has constitution.md been created in the project's documentation folder?

            ## Instructions

            Review the conversation and determine if ALL quality criteria above have been satisfied.
            Look for evidence that each criterion has been addressed.

            If the agent has included `<promise>✓ Quality Criteria Met</promise>` in their response AND
            all criteria appear to be met, respond with: {"ok": true}

            If criteria are NOT met OR the promise tag is missing, respond with:
            {"ok": false, "reason": "**AGENT: TAKE ACTION** - [which criteria failed and why]"}
---

# spec_driven_development.constitution

**Step 1/6** in **spec_driven_development** workflow

> Spec-driven development workflow that turns specifications into working implementations through structured planning.


## Instructions

**Goal**: Creates foundational governance principles and development guidelines for the project. Use when starting a new project or establishing standards.

# Establish Constitution

## Objective

Create a foundational governance document (`constitution.md`) that establishes project principles, development guidelines, and quality standards that will guide all subsequent specification and implementation work.

## Task

Guide the user through defining their project's constitution by asking structured questions about their development priorities, quality standards, and governance preferences.

**Important**: Use the AskUserQuestion tool to ask structured questions when gathering information from the user.

**Critical**: This step captures principles and standards, not implementation code. The constitution describes what technologies and patterns to use, not how to code them. Do not include code examples - those belong only in the implement step.

### Step 1: Understand Development Priorities

Ask structured questions to understand the project's core values:

1. **What are your top development priorities?** (Select all that apply)
   - Code quality and maintainability
   - Test coverage and reliability
   - Performance and scalability
   - Security and data protection
   - UX consistency and accessibility
   - Developer experience and productivity
   - Documentation quality

2. **What's the primary nature of this project?**
   - New greenfield development
   - Adding features to existing codebase
   - Refactoring/modernization effort
   - Prototype/experimental work

3. **Who are the stakeholders?**
   - Who will review specifications?
   - Who will review code?
   - Who are the end users?

### Step 2: Define Technology Preferences

Gather technology stack information:

1. **What's your preferred technology stack?**
   - Languages (e.g., TypeScript, Python, Go)
   - Frameworks (e.g., React, Django, FastAPI)
   - Databases (e.g., PostgreSQL, MongoDB, SQLite)
   - Infrastructure (e.g., AWS, GCP, self-hosted)

2. **What are your testing preferences?**
   - Unit testing framework preferences
   - Integration testing approach
   - E2E testing tools (if applicable)
   - Required coverage thresholds

3. **What coding standards do you follow?**
   - Style guides (e.g., Airbnb, Google, PEP 8)
   - Linting/formatting tools
   - Code review requirements

### Step 3: Establish Quality Standards

Define what "good" looks like:

1. **What are your code quality requirements?**
   - Type safety requirements
   - Documentation requirements (JSDoc, docstrings, etc.)
   - Maximum complexity thresholds
   - Required patterns (e.g., dependency injection, SOLID)

2. **What are your testing requirements?**
   - Minimum test coverage percentage
   - Required test types (unit, integration, e2e)
   - Performance benchmarks

3. **What are your security requirements?**
   - Authentication/authorization standards
   - Data handling requirements
   - Compliance needs (GDPR, HIPAA, etc.)

### Step 4: Define Governance Rules

Establish how the project will be managed:

1. **What's your branching strategy?**
   - Main branch protection rules
   - Feature branch naming conventions
   - PR/MR requirements

2. **What are your review requirements?**
   - Number of required reviewers
   - Who can approve what types of changes
   - Automated checks that must pass

3. **How should specifications be maintained?**
   - When should specs be updated?
   - Who owns spec maintenance?
   - How are spec changes tracked?

### Step 5: Create the Constitution File

After gathering all information, create the constitution document.

**Create the constitution file** at `[docs_folder]/constitution.md`:

```markdown
# Project Constitution

## Overview

[Brief description of the project and its purpose]

## Development Priorities

[Ordered list of priorities gathered from Step 1]

1. [Top priority]
2. [Second priority]
   ...

## Technology Stack

### Languages

- [Primary language]: [Version]

### Frameworks

- [Framework]: [Version]

### Databases

- [Database]: [Purpose]

### Infrastructure

- [Platform]: [Services used]

## Quality Standards

### Code Quality

- [Standard 1]
- [Standard 2]

### Testing Requirements

- Minimum coverage: [X]%
- Required test types: [List]

### Security Requirements

- [Requirement 1]
- [Requirement 2]

## Governance

### Branching Strategy

[Description]

### Review Requirements

- Required reviewers: [Number]
- Required checks: [List]

### Specification Maintenance

[How specs should be updated and tracked]

## Principles

[3-5 guiding principles that should inform all development decisions]

1. **[Principle Name]**: [Description]
2. **[Principle Name]**: [Description]
   ...
```

## Example Dialog

```
Claude: I'll help you establish a constitution for your project. This will define the governance
principles and development guidelines that will guide all specifications and implementations.

Let's start with your development priorities. What matters most to you?

[Uses AskUserQuestion with multi-select options for priorities]

User: [Selects: Code quality, Test coverage, Security]

Claude: Great choices. Now let me understand your technology preferences.

What's your primary language and framework?

User: We're using TypeScript with Next.js and PostgreSQL

Claude: Perfect. What are your testing requirements? Do you have specific coverage thresholds
or required test types?

User: We need 80% coverage minimum, with unit tests for all business logic and integration
tests for API endpoints.

Claude: Got it. What about security? Are there specific compliance requirements or security
standards you need to follow?

User: We handle user data, so GDPR compliance is important. All data must be encrypted at
rest and in transit.

[Continues gathering information...]

Claude: Based on our conversation, here's the constitution I've created:

[Shows constitution content]

✓ Constitution established!

**File created:**
- [docs_folder]/constitution.md

**Next step:**
Run `/spec_driven_development.specify` to create your first feature specification.
```

## Output Format

### [docs_folder]/constitution.md

A markdown document containing:

- Project overview
- Prioritized development values
- Technology stack with versions
- Quality standards and thresholds
- Governance rules and processes
- Guiding principles

**Location**: `[docs_folder]/constitution.md`

After creating the file:

1. Summarize the key principles established
2. Confirm the file has been created
3. Tell the user to run `/spec_driven_development.specify` to create their first feature specification

## Quality Criteria

- Asked structured questions to understand user priorities
- Technology preferences are specific and versioned
- Quality standards include measurable thresholds
- Governance rules are actionable
- Principles are clear and will guide future decisions
- File created in correct location
- **No implementation code**: Constitution describes standards, not code examples



## Required Inputs

**User Parameters** - Gather from user before starting:
- **development_priorities**: Key priorities like code quality, testing, UX consistency, performance


## Work Branch

Use branch format: `deepwork/spec_driven_development-[instance]-YYYYMMDD`

- If on a matching work branch: continue using it
- If on main/master: create new branch with `git checkout -b deepwork/spec_driven_development-[instance]-$(date +%Y%m%d)`

## Outputs

**Required outputs**:
- `[docs_folder]/constitution.md`

## Guardrails

- Do NOT skip prerequisite verification if this step has dependencies
- Do NOT produce partial outputs; complete all required outputs before finishing
- Do NOT proceed without required inputs; ask the user if any are missing
- Do NOT modify files outside the scope of this step's defined outputs

## Quality Validation

Stop hooks will automatically validate your work. The loop continues until all criteria pass.

**Criteria (all must be satisfied)**:
1. **Priorities Captured**: Did the agent gather specific development priorities from the user?
2. **Principles Defined**: Are governance principles clear and actionable?
3. **Technology Guidance**: Does the constitution include relevant technology stack preferences?
4. **Quality Standards**: Are quality standards and testing expectations defined?
5. **File Created**: Has constitution.md been created in the project's documentation folder?


**To complete**: Include `<promise>✓ Quality Criteria Met</promise>` in your final response only after verifying ALL criteria are satisfied.

## On Completion

1. Verify outputs are created
2. Inform user: "Step 1/6 complete, outputs: [docs_folder]/constitution.md"
3. **Continue workflow**: Use Skill tool to invoke `/spec_driven_development.specify`

---

**Reference files**: `.deepwork/jobs/spec_driven_development/job.yml`, `.deepwork/jobs/spec_driven_development/steps/constitution.md`