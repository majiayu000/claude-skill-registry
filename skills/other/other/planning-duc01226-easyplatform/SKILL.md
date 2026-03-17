---
name: planning
version: 2.0.0
description: "[Planning] Use when you need to research, analyze, investigate, plan, design, or architect technical solutions. Includes comprehensive research phase with Gemini CLI, WebSearch, and 5-research limit. Triggers on keywords like "research", "analyze", "investigate options", "explore solutions", "compare approaches", "evaluate alternatives", "plan", "design", "architect"."
allowed-tools: NONE
license: MIT
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

## Quick Summary

**Goal:** Create detailed technical implementation plans through research, codebase analysis, solution design, and comprehensive documentation (includes research phase merged from `research` skill).

**Workflow:**

1. **Research** — Parallel researcher agents, sequential-thinking, docs-seeker, GitHub analysis (max 5 researches)
2. **Design Context** — Extract Figma specs if URLs present in source artifacts
3. **Codebase Understanding** — Parallel scout agents, read essential docs (development-rules.md, codebase-summary.md, code-standards.md)
4. **Solution Design** — Trade-off analysis, security, performance, edge cases, architecture
5. **Plan Creation** — YAML frontmatter plan.md + detailed phase-XX-\*.md files
6. **Review** — Run `/plan-review` to validate, ask user to confirm

**Key Rules:**

- **DO NOT** implement code - only create plans
- **DO NOT** use EnterPlanMode tool - already in planning workflow
- **ALWAYS** run `/plan-review` after plan creation
- **COLLABORATE**: Ask decision questions, present options with recommendations

# Planning

Create detailed technical implementation plans through research, codebase analysis, solution design, and comprehensive documentation.

> **Note:** This skill includes the research phase (merged from `research` skill). Use for comprehensive planning that requires investigation before implementation.

## PLANNING-ONLY — Collaboration Required

> **DO NOT** use the `EnterPlanMode` tool — you are ALREADY in a planning workflow.
> **DO NOT** implement or execute any code changes.
> **COLLABORATE** with the user: ask decision questions, present options with recommendations.
> After plan creation, ALWAYS run `/plan-review` to validate the plan.
> ASK user to confirm the plan before any next step.

## When to Use

Use this skill when:

- Researching or investigating solutions
- Analyzing approaches and alternatives
- Planning new feature implementations
- Architecting system designs
- Evaluating technical approaches
- Creating implementation roadmaps
- Breaking down complex requirements
- Assessing technical trade-offs

## Disambiguation

- For quick bug triage and systematic debugging, use `debug` instead
- This skill focuses on upfront planning and research before implementation

## Core Responsibilities & Rules

Always honoring **YAGNI**, **KISS**, and **DRY** principles.
**Be honest, be brutal, straight to the point, and be concise.**

### 1. Research & Analysis (**Skip if:** Provided with researcher reports)

> _Content sourced from `references/research-phase.md`_

#### Core Activities

##### Parallel Researcher Agents

- Spawn multiple `researcher` agents in parallel to investigate different approaches
- Wait for all researcher agents to report back before proceeding
- Each researcher investigates a specific aspect or approach

##### Sequential Thinking

- Use `sequential-thinking` skill for dynamic and reflective problem-solving
- Structured thinking process for complex analysis
- Enables multi-step reasoning with revision capability

##### Documentation Research

- Use `docs-seeker` skill to read and understand documentation
- Research plugins, packages, and frameworks
- Find latest technical documentation using llms.txt standard

##### GitHub Analysis

- Use `gh` command to read and analyze:
    - GitHub Actions logs
    - Pull requests
    - Issues and discussions
- Extract relevant technical context from GitHub resources

##### Remote Repository Analysis

When given GitHub repository URL, generate fresh codebase summary:

```bash
# usage:
repomix --remote <github-repo-url>
# example:
repomix --remote https://github.com/mrgoonie/human-mcp
```

##### Debugger Delegation

- Delegate to `debugger` agent for root cause analysis
- Use when investigating complex issues or bugs
- Debugger agent specializes in diagnostic tasks

#### Search Strategy

##### Primary: Gemini CLI

Check if `gemini` bash command is available:

```bash
gemini -m gemini-2.5-flash -p "...your search prompt..."
# Timeout: 10 minutes
```

Save output using `Report:` path from `## Naming` section (include all citations).

##### Fallback: WebSearch Tool

If gemini unavailable, use `WebSearch` tool. Run multiple searches in parallel.

##### Query Crafting

- Craft precise search queries with relevant keywords
- Include terms like "best practices", "2024", "latest", "security", "performance"
- Search for official documentation, GitHub repositories, and authoritative blogs
- Prioritize results from recognized authorities (official docs, major tech companies, respected developers)

##### IMPORTANT: 5-Research Limit

You are allowed to perform at most **5 researches (max 5 tool calls)**. User might request less. Think carefully based on the task before performing each research.

#### Deep Content Analysis

- When you find a potential GitHub repository URL, use `docs-seeker` skill to read it
- Focus on official documentation, API references, and technical specifications
- Analyze README files from popular GitHub repositories
- Review changelog and release notes for version-specific information

##### Video Content Research

- Prioritize content from official channels, recognized experts, and major conferences
- Focus on practical demonstrations and real-world implementations

##### Cross-Reference Validation

- Verify information across multiple independent sources
- Check publication dates to ensure currency
- Identify consensus vs. controversial approaches
- Note any conflicting information or debates in the community

#### Research Report Template

```markdown
# Research Report: [Topic]

## Executive Summary

[2-3 paragraph overview of key findings and recommendations]

## Research Methodology

- Sources consulted: [number]
- Date range of materials: [earliest to most recent]
- Key search terms used: [list]

## Key Findings

### 1. Technology Overview

[Comprehensive description of the technology/topic]

### 2. Current State & Trends

[Latest developments, version information, adoption trends]

### 3. Best Practices

[Detailed list of recommended practices with explanations]

### 4. Security Considerations

[Security implications, vulnerabilities, and mitigation strategies]

### 5. Performance Insights

[Performance characteristics, optimization techniques, benchmarks]

## Comparative Analysis

[If applicable, comparison of different solutions/approaches]

## Implementation Recommendations

### Quick Start Guide

[Step-by-step getting started instructions]

### Code Examples

[Relevant code snippets with explanations]

### Common Pitfalls

[Mistakes to avoid and their solutions]

## Resources & References

### Official Documentation

- [Linked list of official docs]

### Recommended Tutorials

- [Curated list with descriptions]

### Community Resources

- [Forums, Discord servers, Stack Overflow tags]

## Appendices

### A. Glossary

### B. Version Compatibility Matrix

### C. Raw Research Notes (optional)
```

#### Research Quality Standards

Ensure all research meets these criteria:

- **Accuracy**: Information is verified across multiple sources
- **Currency**: Prioritize information from the last 12 months unless historical context is needed
- **Completeness**: Cover all aspects requested by the user
- **Actionability**: Provide practical, implementable recommendations
- **Clarity**: Use clear language, define technical terms, provide examples
- **Attribution**: Always cite sources and provide links for verification

#### Special Considerations

- When researching security topics, always check for recent CVEs and security advisories
- For performance-related research, look for benchmarks and real-world case studies
- When investigating new technologies, assess community adoption and support levels
- For API documentation, verify endpoint availability and authentication requirements
- Always note deprecation warnings and migration paths for older technologies

#### Research Best Practices

- Research breadth before depth
- Document findings for synthesis phase
- Identify multiple approaches for comparison
- Consider edge cases during research
- Note security implications early
- Sacrifice grammar for concision in reports
- List unresolved questions at the end

### 2. Design Context Extraction

> _Content sourced from `references/figma-integration.md`_

**Skip if:** No Figma URLs in source artifacts OR backend-only changes

When planning UI features:

1. Check source PBI/design-spec for Figma URLs
2. Extract design context via Figma MCP (if available)
3. Include design specifications in plan phases
4. Map design tokens to implementation

#### When to Apply

**Apply when:**

- Source artifact contains Figma URLs
- Task involves UI/frontend implementation
- Design specifications are referenced

**Skip when:**

- Backend-only changes
- No Figma URLs in artifacts
- Figma MCP not available (graceful degradation)

#### Detection Phase

##### 1. Scan Source Artifacts

Check these locations for Figma URLs:

- PBI `## Design Reference` section
- Design spec `figma_file:` and `figma_nodes:` frontmatter
- Feature doc Section 6 (Design Reference)

##### 2. Parse URLs

Extract from each URL:

- `file_key`: Figma file identifier
- `node_id`: Specific frame/component (URL format: `1-3`)
- Convert to API format: `1-3` → `1:3`

**URL Pattern:**

```
https://figma.com/design/{file_key}/{name}?node-id={node_id}
```

#### Extraction Phase

##### 1. Check MCP Availability

```
If Figma MCP available:
  → Proceed with extraction
Else:
  → Log: "Figma MCP not configured, skipping design extraction"
  → Continue with URL references only
```

##### 2. Call MCP for Each Node

Prefer specific nodes over full files:

```
For each {file_key, node_id} pair:
  If node_id exists:
    Call: mcp__figma__get_file_nodes(file_key, [node_id])
  Else:
    Skip file-level extraction (too expensive)
```

##### 3. Extract Key Information

From response, extract:

| Property       | Source Field                            |
| -------------- | --------------------------------------- |
| **Structure**  | `children[].name`, `children[].type`    |
| **Layout**     | `layoutMode`, `itemSpacing`, `padding*` |
| **Dimensions** | `absoluteBoundingBox.width/height`      |
| **Colors**     | `fills[].color` (r,g,b,a → rgba)        |
| **Typography** | `style.fontFamily/fontSize/fontWeight`  |

##### 4. Token Budget Enforcement

| Response Size | Action                                |
| ------------- | ------------------------------------- |
| <2K tokens    | Use full response                     |
| 2K-5K tokens  | Summarize to key properties           |
| >5K tokens    | Extract only critical info, warn user |

#### Integration Phase

##### 1. Add to Plan Context

Include in plan.md overview:

```markdown
## Design Context

Design specifications extracted from Figma:

| Component | Figma Node         | Key Specs              |
| --------- | ------------------ | ---------------------- |
| {name}    | [{node_id}]({url}) | {dimensions}, {layout} |

### Extracted Specifications

{Formatted design context from extraction}
```

##### 2. Reference in Implementation Phases

For frontend phases, include:

```markdown
## Design Specifications

From Figma node `{node_id}`:

### Layout

- Direction: {Horizontal/Vertical}
- Gap: {spacing}px
- Padding: {T/R/B/L}px

### Visual

- Background: {color} → map to `--color-bg-*`
- Border: {width}px {color} → map to `--border-*`

### Typography (if text)

- Font: {family} → map to `--font-family-*`
- Size: {size}px → map to `--font-size-*`
- Weight: {weight} → map to `--font-weight-*`
```

##### 3. Design Token Mapping

Map extracted values to existing tokens:

| Figma Value    | Design Token         | Notes            |
| -------------- | -------------------- | ---------------- |
| #FFFFFF        | `--color-bg-primary` | Exact match      |
| 16px           | `--spacing-md`       | Standard spacing |
| Inter 400 14px | `--font-body`        | Body text        |

Reference: `docs/design-system/tokens.scss` for available tokens.

#### Fallback Behavior

When extraction fails:

1. **MCP Not Available:**
    - Log warning
    - Note in plan: "Design context not extracted (MCP unavailable)"
    - Continue with URL references only

2. **Node Not Found:**
    - Try parent node
    - Note which nodes failed
    - Continue with available data

3. **Rate Limited:**
    - Extract first 3 nodes only
    - Note in plan which nodes were skipped

4. **Token Budget Exceeded:**
    - Summarize aggressively
    - Include only dimensions, colors, layout
    - Link to full Figma for details

#### Figma Output Template

```markdown
## Figma Design Context

> Extracted via Figma MCP on {date}

### Source Designs

| Design | Node          | Status    |
| ------ | ------------- | --------- |
| {name} | [{id}]({url}) | Extracted |

### {Component Name}

**Node:** `{node_id}`
**Type:** {Frame/Component/Group}
**Dimensions:** {width} x {height}px

#### Layout

- Direction: {layoutMode}
- Gap: {itemSpacing}px
- Padding: {paddingTop}/{paddingRight}/{paddingBottom}/{paddingLeft}px

#### Visual

| Property      | Value            | Token Mapping       |
| ------------- | ---------------- | ------------------- |
| Background    | {fill color}     | `--color-*`         |
| Border        | {stroke}         | `--border-*`        |
| Corner Radius | {cornerRadius}px | `--border-radius-*` |

#### Children

- {child1}: {type}
- {child2}: {type}
```

#### No Design Context Template

When no Figma URLs present:

```markdown
## Design Context

No Figma designs referenced. If UI changes are needed:

1. Add Figma links to source PBI `## Design Reference` section
2. Re-run planning to extract design context
```

### 3. Codebase Understanding (**Skip if:** Provided with scout reports)

> _Content sourced from `references/codebase-understanding.md`_

#### Core Activities

##### Parallel Scout Agents

- Use `/scout-ext` (preferred) or `/scout` (fallback) slash command to search the codebase for files needed to complete the task
- Each scout locates files needed for specific task aspects
- Wait for all scout agents to report back before analysis
- Efficient for finding relevant code across large codebases

##### Essential Documentation Review

ALWAYS read these files first:

1. **`./docs/development-rules.md`** (IMPORTANT)
    - File Name Conventions
    - File Size Management
    - Development rules and best practices
    - Code quality standards
    - Security guidelines

2. **`./docs/codebase-summary.md`**
    - Project structure and current status
    - High-level architecture overview
    - Component relationships

3. **`./docs/code-standards.md`**
    - Coding conventions and standards
    - Language-specific patterns
    - Naming conventions

4. **`./docs/design-guidelines.md`** (if exists)
    - Design system guidelines
    - Branding and UI/UX conventions
    - Component library usage

##### Environment Analysis

- Review development environment setup
- Analyze dotenv files and configuration
- Identify required dependencies
- Understand build and deployment processes

##### Pattern Recognition

- Study existing patterns in codebase
- Identify conventions and architectural decisions
- Note consistency in implementation approaches
- Understand error handling patterns

##### Integration Planning

- Identify how new features integrate with existing architecture
- Map dependencies between components
- Understand data flow and state management
- Consider backward compatibility

#### Codebase Understanding Best Practices

- Start with documentation before diving into code
- Use scouts for targeted file discovery
- Document patterns found for consistency
- Note any inconsistencies or technical debt
- Consider impact on existing features

### 4. Solution Design

> _Content sourced from `references/solution-design.md`_

#### Core Principles

- **YAGNI** (You Aren't Gonna Need It) - Don't add functionality until necessary
- **KISS** (Keep It Simple, Stupid) - Prefer simple solutions over complex ones
- **DRY** (Don't Repeat Yourself) - Avoid code duplication

#### Design Activities

##### Technical Trade-off Analysis

- Evaluate multiple approaches for each requirement
- Compare pros and cons of different solutions
- Consider short-term vs long-term implications
- Balance complexity with maintainability
- Assess development effort vs benefit
- Recommend optimal solution based on current best practices

##### Security Assessment

- Identify potential vulnerabilities during design phase
- Consider authentication and authorization requirements
- Assess data protection needs
- Evaluate input validation requirements
- Plan for secure configuration management
- Address OWASP Top 10 concerns
- Consider API security (rate limiting, CORS, etc.)

##### Performance and Scalability

- Identify potential bottlenecks early
- Consider database query optimization needs
- Plan for caching strategies
- Assess resource usage (memory, CPU, network)
- Design for horizontal/vertical scaling
- Plan for load distribution
- Consider asynchronous processing where appropriate

##### Edge Cases and Failure Modes

- Think through error scenarios
- Plan for network failures
- Consider partial failure handling
- Design retry and fallback mechanisms
- Plan for data consistency
- Consider race conditions
- Design for graceful degradation

##### Architecture Design

- Create scalable system architectures
- Design for maintainability
- Plan component interactions
- Design data flow
- Consider microservices vs monolith trade-offs
- Plan API contracts
- Design state management

#### Frontend Solution Design

When designing frontend solutions with Figma context:

##### Design Context Integration

1. **Check for Figma Context**
    - Review extracted design specifications
    - Verify dimensions and spacing match design system
    - Note any custom values needing tokens

2. **Component Structure**
    - Match Figma hierarchy to Angular component tree
    - Identify reusable components
    - Map to existing shared library components

3. **Token Mapping**
    - Map Figma colors to design tokens
    - Verify spacing uses standard tokens
    - Flag any values needing new tokens

4. **Responsive Considerations**
    - Check if Figma shows breakpoint variants
    - Plan responsive behavior for unlisted breakpoints
    - Note any mobile-specific layouts

#### Solution Design Best Practices

- Document design decisions and rationale
- Consider both technical and business requirements
- Think through the entire user journey
- Plan for monitoring and observability
- Design with testing in mind
- Consider deployment and rollback strategies

### 5. Plan Creation and Organization

> _Content sourced from `references/plan-organization.md`_

#### Directory Structure

##### Plan Location

Use `Plan dir:` from `## Naming` section injected by hooks. This is the full computed path.

**Example:** `plans/251101-1505-authentication/` or `ai_docs/feature/MRR-1453/`

##### File Organization

```
{plan-dir}/                                    # From `Plan dir:` in ## Naming
├── research/
│   ├── researcher-XX-report.md
│   └── ...
├── reports/
│   ├── scout-report.md
│   ├── researcher-report.md
│   └── ...
├── plan.md                                    # Overview access point
├── phase-01-setup-environment.md              # Setup environment
├── phase-02-implement-database.md             # Database models
├── phase-03-implement-api-endpoints.md        # API endpoints
├── phase-04-implement-ui-components.md        # UI components
├── phase-05-implement-authentication.md       # Auth & authorization
├── phase-06-implement-profile.md              # Profile page
└── phase-07-write-tests.md                    # Tests
```

##### Active Plan State Tracking

Check the `## Plan Context` section injected by hooks:

- **"Plan: {path}"** = Active plan - use for reports
- **"Suggested: {path}"** = Branch-matched, hint only - do NOT auto-use
- **"Plan: none"** = No active plan

**Pre-Creation Check:**

1. If "Plan:" shows a path → ask "Continue with existing plan? [Y/n]"
2. If "Suggested:" shows a path → inform user (hint only, do NOT auto-use)
3. If "Plan: none" → create new plan using naming from `## Naming` section

**After Creating Plan:**

```bash
# Update session state so subagents get the new plan context:
node .claude/scripts/set-active-plan.cjs {plan-dir}
```

**Report Output Rules:**

1. Use `Report:` and `Plan dir:` from `## Naming` section
2. Active plans use plan-specific reports path
3. Suggested plans use default reports path to prevent old plan pollution

#### Plan File Structure

##### Overview Plan (plan.md)

**IMPORTANT:** All plan.md files MUST include YAML frontmatter. See output standards below for schema.

**Example plan.md structure:**

```markdown
---
title: 'Feature Implementation Plan'
description: 'Add user authentication with OAuth2 support'
status: pending
priority: P1
effort: 8h
issue: 123
branch: kai/feat/oauth-auth
tags: [auth, backend, security]
created: 2025-12-16
---

# Feature Implementation Plan

## Overview

Brief description of what this plan accomplishes.

## Phases

| #   | Phase          | Status  | Effort | Link                            |
| --- | -------------- | ------- | ------ | ------------------------------- |
| 1   | Setup          | Pending | 2h     | [phase-01](./phase-01-setup.md) |
| 2   | Implementation | Pending | 4h     | [phase-02](./phase-02-impl.md)  |
| 3   | Testing        | Pending | 2h     | [phase-03](./phase-03-test.md)  |

## Dependencies

- List key dependencies here
```

**Guidelines:**

- Keep generic and under 80 lines
- List each phase with status/progress
- Link to detailed phase files
- Key dependencies

##### Phase Files (phase-XX-name.md)

Fully respect the `./docs/development-rules.md` file.
Each phase file should contain:

###### Context Links

- Links to related reports, files, documentation

###### Phase Overview

- Priority
- Current status
- Brief description

###### Key Insights

- Important findings from research
- Critical considerations

###### Requirements

- Functional requirements
- Non-functional requirements

###### Architecture

- System design
- Component interactions
- Data flow

###### Related Code Files

- List of files to modify
- List of files to create
- List of files to delete

###### Implementation Steps

- Detailed, numbered steps
- Specific instructions

###### Todo List

- Checkbox list for tracking

###### Success Criteria

- Definition of done
- Validation methods

###### Risk Assessment

- Potential issues
- Mitigation strategies

###### Security Considerations

- Auth/authorization
- Data protection

###### Next Steps

- Dependencies
- Follow-up tasks

### 6. Task Breakdown and Output Standards

> _Content sourced from `references/output-standards.md`_

#### Plan File Format

##### YAML Frontmatter (Required for plan.md)

All `plan.md` files MUST include YAML frontmatter at the top:

```yaml
---
title: '{Brief plan title}'
description: '{One-sentence summary for card preview}'
status: pending # pending | in-progress | completed | cancelled
priority: P2 # P1 (High) | P2 (Medium) | P3 (Low)
effort: 4h # Estimated total effort
issue: 74 # GitHub issue number (if applicable)
branch: kai/feat/feature-name
tags: [frontend, api] # Category tags
created: 2025-12-16
---
```

##### Auto-Population Rules

When creating plans, auto-populate these fields:

- **title**: Extract from task description
- **description**: First sentence of Overview section
- **status**: Always `pending` for new plans
- **priority**: From user request or default `P2`
- **effort**: Sum of phase estimates
- **issue**: Parse from branch name or context
- **branch**: Current git branch (`git branch --show-current`)
- **tags**: Infer from task keywords (e.g., frontend, backend, api, auth)
- **created**: Today's date in YYYY-MM-DD format

##### Tag Vocabulary (Recommended)

Use these predefined tags for consistency:

- **Type**: `feature`, `bugfix`, `refactor`, `docs`, `infra`
- **Domain**: `frontend`, `backend`, `database`, `api`, `auth`
- **Scope**: `critical`, `tech-debt`, `experimental`

#### Task Breakdown Rules

- Transform complex requirements into manageable, actionable tasks
- Each task independently executable with clear dependencies
- Prioritize by dependencies, risk, business value
- Eliminate ambiguity in instructions
- Include specific file paths for all modifications
- Provide clear acceptance criteria per task

##### File Management

List affected files with:

- Full paths (not relative)
- Action type (modify/create/delete)
- Brief change description
- Dependencies on other changes
- Fully respect the `./docs/development-rules.md` file.

#### Output Workflow Process

1. **Initial Analysis** → Read docs, understand context
2. **Research Phase** → Spawn researchers in parallel, investigate approaches
3. **Synthesis** → Analyze reports, identify optimal solution
4. **Design Phase** → Create architecture, implementation design
5. **Plan Documentation** → Write comprehensive plan in Markdown
6. **Review & Refine** → Ensure completeness, clarity, actionability

#### Output Requirements

##### What Planners Do

- Create plans ONLY (no implementation)
- Provide plan file path and summary
- Self-contained plans with necessary context
- Code snippets/pseudocode when clarifying
- Multiple options with trade-offs when appropriate
- Fully respect the `./docs/development-rules.md` file.

##### Writing Style

**IMPORTANT:** Sacrifice grammar for concision

- Focus clarity over eloquence
- Use bullets and lists
- Short sentences
- Remove unnecessary words
- Prioritize actionable info

##### Unresolved Questions

**IMPORTANT:** List unresolved questions at end

- Questions needing clarification
- Technical decisions requiring input
- Unknowns impacting implementation
- Trade-offs requiring business decisions

#### Design Context for UI Phases

If Figma designs were extracted, include in phase files:

```markdown
## Design Specifications

> From Figma: [{component_name}]({figma_url})

### Layout

{Extracted layout specifications}

### Visual Styling

| Property | Figma Value | Token          |
| -------- | ----------- | -------------- |
| {prop}   | {value}     | `--token-name` |

### Implementation Notes

- {Note about design-to-code mapping}
- {Any deviations from design system}
```

When no Figma context:

- Omit section or note "No design specifications provided"

#### Output Quality Standards

##### Thoroughness

- Thorough and specific in research/planning
- Consider edge cases, failure modes
- Think through entire user journey
- Document all assumptions

##### Maintainability

- Consider long-term maintainability
- Design for future modifications
- Document decision rationale
- Avoid over-engineering
- Fully respect the `./docs/development-rules.md` file.

##### Research Depth

- When uncertain, research more
- Multiple options with clear trade-offs
- Validate against best practices
- Consider industry standards

##### Security and Performance

- Address all security concerns
- Identify performance implications
- Plan for scalability
- Consider resource constraints

##### Implementability

- Detailed enough for junior developers
- Validate against existing patterns
- Ensure codebase standards consistency
- Provide clear examples

**Remember:** Plan quality determines implementation success. Be comprehensive, consider all solution aspects.

## Workflow Process

1. **Initial Analysis** → Read codebase docs, understand context
2. **Design Context** → Extract Figma design specs (if URLs present)
3. **Research Phase** → Spawn researchers, investigate approaches
4. **Synthesis** → Analyze reports, identify optimal solution
5. **Design Phase** → Create architecture, implementation design
6. **Plan Documentation** → Write comprehensive plan (include design context)
7. **Review & Refine** → Ensure completeness, clarity, actionability

## Top-Level Output Requirements

- DO NOT implement code - only create plans
- Respond with plan file path and summary
- Ensure self-contained plans with necessary context
- Include code snippets/pseudocode when clarifying
- Provide multiple options with trade-offs when appropriate
- Fully respect the `./docs/development-rules.md` file.

**Plan Directory Structure**

```
plans/
└── {date}-plan-name/
    ├── research/
    │   ├── researcher-XX-report.md
    │   └── ...
    ├── reports/
    │   ├── XX-report.md
    │   └── ...
    ├── scout/
    │   ├── scout-XX-report.md
    │   └── ...
    ├── plan.md
    ├── phase-XX-phase-name-here.md
    └── ...
```

## Active Plan State

Prevents version proliferation by tracking current working plan via session state.

### Active vs Suggested Plans

Check the `## Plan Context` section injected by hooks:

- **"Plan: {path}"** = Active plan, explicitly set via `set-active-plan.cjs` - use for reports
- **"Suggested: {path}"** = Branch-matched, hint only - do NOT auto-use
- **"Plan: none"** = No active plan

### Rules

1. **If "Plan:" shows a path**: Ask "Continue with existing plan? [Y/n]"
2. **If "Suggested:" shows a path**: Inform user, ask if they want to activate or create new
3. **If "Plan: none"**: Create new plan using naming from `## Naming` section
4. **Update on create**: Run `node .claude/scripts/set-active-plan.cjs {plan-dir}`

### Report Output Location

All agents writing reports MUST:

1. Check `## Naming` section injected by hooks for the computed naming pattern
2. Active plans use plan-specific reports path
3. Suggested plans use default reports path (not plan folder)

**Important:** Suggested plans do NOT get plan-specific reports - this prevents pollution of old plan folders.

## Quality Standards

- Be thorough and specific
- Consider long-term maintainability
- Research thoroughly when uncertain
- Address security and performance concerns
- Make plans detailed enough for junior developers
- Validate against existing codebase patterns

**Remember:** Plan quality determines implementation success. Be comprehensive and consider all solution aspects.

## Related

- `feature-implementation`
- `problem-solving`
- `plan-analysis`

---

## **IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks using `TaskCreate`
- Always add a final review todo task to verify work quality and identify fixes/enhancements
- **MANDATORY FINAL TASKS:** After creating all planning todo tasks, ALWAYS add these two final tasks:
  1. **Task: "Run /plan-validate"** — Trigger `/plan-validate` skill to interview the user with critical questions and validate plan assumptions
  2. **Task: "Run /plan-review"** — Trigger `/plan-review` skill to auto-review plan for validity, correctness, and best practices

## Important Notes

**IMPORTANT:** Analyze the skills catalog and activate the skills that are needed for the task during the process.
**IMPORTANT:** Ensure token efficiency while maintaining high quality.
**IMPORTANT:** Sacrifice grammar for the sake of concision when writing reports.
**IMPORTANT:** In reports, list any unresolved questions at the end, if any.

## REMINDER — Planning-Only Skill

> **DO NOT** use `EnterPlanMode` tool.
> **DO NOT** start implementing.
> **ALWAYS** validate with `/plan-review` after plan creation.
> **ASK** user to confirm the plan before any implementation begins.
> **ASK** user decision questions with your recommendations when multiple approaches exist.
