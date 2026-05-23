---
name: plan
description: "Research, design, and decompose a project plan into beads tasks. Integrated planning pipeline from idea to actionable work."
allowed-tools: Read, Bash, Glob, Grep, Write, AskUserQuestion, Task
---

# Plan: $ARGUMENTS

**Note: The current year is 2026.** Use this when dating plans and searching for recent documentation.

Transform feature descriptions, bug reports, or improvement ideas into well-structured plan documents and decompose them into beads tasks.

## Feature Description

<feature_description> $ARGUMENTS </feature_description>

**If the feature description above is empty, ask the user:** "What would you like to plan? Please describe the feature, bug fix, or improvement you have in mind."

Do not proceed until you have a clear feature description from the user.

### Step 0: Idea Refinement

**Check for brainstorm output first:**

Before asking questions, look for recent brainstorm documents in `docs/brainstorms/` that match this feature:

```bash
ls -la docs/brainstorms/*.md 2>/dev/null | head -10
```

**Relevance criteria:** A brainstorm is relevant if:
- The topic (from filename or content) semantically matches the feature description
- Created within the last 14 days
- If multiple candidates match, use the most recent one

**If a relevant brainstorm exists:**
1. Read the brainstorm document
2. Announce: "Found brainstorm from [date]: [topic]. Using as context for planning."
3. Extract key decisions, chosen approach, and open questions
4. **Skip the idea refinement questions below** - the brainstorm already answered WHAT to build
5. Use brainstorm decisions as input to the research phase

**If multiple brainstorms could match:**
Use **AskUserQuestion tool** to ask which brainstorm to use, or whether to proceed without one.

**If no brainstorm found (or not relevant), run idea refinement:**

Refine the idea through collaborative dialogue using the **AskUserQuestion tool**:

- Ask questions one at a time to understand the idea fully
- Prefer multiple choice questions when natural options exist
- Focus on understanding: purpose, constraints, and success criteria
- Continue until the idea is clear OR user says "proceed"

**Gather signals for research decision.** During refinement, note:

- **User's familiarity**: Do they know the codebase patterns? Are they pointing to examples?
- **User's intent**: Speed vs thoroughness? Exploration vs execution?
- **Topic risk**: Security, payments, external APIs warrant more caution
- **Uncertainty level**: Is the approach clear or open-ended?

**Skip option:** If the feature description is already detailed, offer:
"Your description is clear. Should I proceed with research, or would you like to refine it further?"

## Main Tasks

### Step 1: Local Research (Always Runs - Parallel)

<thinking>
First, I need to understand the project's conventions, existing patterns, and any documented learnings. This is fast and local - it informs whether external research is needed.
</thinking>

Run these agents **in parallel** to gather local context:

- Task repo-research-analyst(feature_description)
- Task learnings-researcher(feature_description)

**What to look for:**
- **Repo research:** existing patterns, CLAUDE.md guidance, technology familiarity, pattern consistency
- **Learnings:** documented solutions in `docs/solutions/` that might apply (gotchas, patterns, lessons learned)

These findings inform the next step.

### Step 1.5: Research Decision

Based on signals from Step 0 and findings from Step 1, decide on external research.

**High-risk topics -> always research.** Security, payments, external APIs, data privacy. The cost of missing something is too high. This takes precedence over speed signals.

**Strong local context -> skip external research.** Codebase has good patterns, CLAUDE.md has guidance, user knows what they want. External research adds little value.

**Uncertainty or unfamiliar territory -> research.** User is exploring, codebase has no examples, new technology. External perspective is valuable.

**Announce the decision and proceed.** Brief explanation, then continue. User can redirect if needed.

Examples:
- "Your codebase has solid patterns for this. Proceeding without external research."
- "This involves payment processing, so I'll research current best practices first."

### Step 1.5b: External Research (Conditional)

**Only run if Step 1.5 indicates external research is valuable.**

Run these agents in parallel:

- Task best-practices-researcher(feature_description)
- Task framework-docs-researcher(feature_description)

### Step 1.6: Consolidate Research

After all research steps complete, consolidate findings:

- Document relevant file paths from repo research (e.g., `app/services/example_service.rb:42`)
- **Include relevant institutional learnings** from `docs/solutions/` (key insights, gotchas to avoid)
- Note external documentation URLs and best practices (if external research was done)
- List related issues or PRs discovered
- Capture CLAUDE.md conventions

**Optional validation:** Briefly summarize findings and ask if anything looks off or missing before proceeding to planning.

### Step 2: Issue Planning & Structure

<thinking>
Think like a product manager - what would make this plan clear and actionable? Consider multiple perspectives.
</thinking>

**Title & Categorization:**

- [ ] Draft clear, searchable title using conventional format (e.g., `feat: Add user authentication`, `fix: Cart total calculation`)
- [ ] Determine issue type: enhancement, bug, refactor
- [ ] Convert title to filename: add today's date prefix, strip prefix colon, kebab-case, add `-plan` suffix
  - Example: `feat: Add User Authentication` -> `2026-01-21-feat-add-user-authentication-plan.md`
  - Keep it descriptive (3-5 words after prefix) so plans are findable by context

**Stakeholder Analysis:**

- [ ] Identify who will be affected (end users, developers, operations)
- [ ] Consider implementation complexity and required expertise

**Content Planning:**

- [ ] Choose appropriate detail level based on complexity and audience
- [ ] List all necessary sections for the chosen template
- [ ] Gather supporting materials (error logs, screenshots, design mockups)
- [ ] Prepare code examples or reproduction steps if applicable

### Step 3: SpecFlow Analysis

After planning the issue structure, run SpecFlow Analyzer to validate and refine the feature specification:

- Task spec-flow-analyzer(feature_description, research_findings)

**SpecFlow Analyzer Output:**

- [ ] Review SpecFlow analysis results
- [ ] Incorporate any identified gaps or edge cases into the plan
- [ ] Update acceptance criteria based on SpecFlow findings

### Step 4: Choose Implementation Detail Level

Select how comprehensive the plan should be. Simpler is mostly better.

#### MINIMAL (Quick Plan)

**Best for:** Simple bugs, small improvements, clear features

**Includes:**
- Problem statement or feature description
- Basic acceptance criteria
- Essential context only

**Structure:**

````markdown
---
title: [Issue Title]
type: [feat|fix|refactor]
date: YYYY-MM-DD
---

# [Issue Title]

[Brief problem/feature description]

## Acceptance Criteria

- [ ] Core requirement 1
- [ ] Core requirement 2

## Context

[Any critical information]

## MVP

### example_file.rb

```ruby
class Example
  def initialize
    @name = "example"
  end
end
```

## References

- Related issue: #[issue_number]
- Documentation: [relevant_docs_url]
````

#### MORE (Standard Plan)

**Best for:** Most features, complex bugs, team collaboration

**Includes everything from MINIMAL plus:**
- Detailed background and motivation
- Technical considerations
- Success metrics
- Dependencies and risks
- Basic implementation suggestions

**Structure:**

```markdown
---
title: [Issue Title]
type: [feat|fix|refactor]
date: YYYY-MM-DD
---

# [Issue Title]

## Overview

[Comprehensive description]

## Problem Statement / Motivation

[Why this matters]

## Proposed Solution

[High-level approach]

## Technical Considerations

- Architecture impacts
- Performance implications
- Security considerations

## Acceptance Criteria

- [ ] Detailed requirement 1
- [ ] Detailed requirement 2
- [ ] Testing requirements

## Success Metrics

[How we measure success]

## Dependencies & Risks

[What could block or complicate this]

## References & Research

- Similar implementations: [file_path:line_number]
- Best practices: [documentation_url]
- Related PRs: #[pr_number]
```

#### A LOT (Comprehensive Plan)

**Best for:** Major features, architectural changes, complex integrations

**Includes everything from MORE plus:**
- Detailed implementation plan with phases
- Alternative approaches considered
- Extensive technical specifications
- Resource requirements and timeline
- Future considerations and extensibility
- Risk mitigation strategies
- Documentation requirements

**Structure:**

```markdown
---
title: [Issue Title]
type: [feat|fix|refactor]
date: YYYY-MM-DD
---

# [Issue Title]

## Overview

[Executive summary]

## Problem Statement

[Detailed problem analysis]

## Proposed Solution

[Comprehensive solution design]

## Technical Approach

### Architecture

[Detailed technical design]

### Implementation Phases

#### Phase 1: [Foundation]

- Tasks and deliverables
- Success criteria
- Estimated effort

#### Phase 2: [Core Implementation]

- Tasks and deliverables
- Success criteria
- Estimated effort

#### Phase 3: [Polish & Optimization]

- Tasks and deliverables
- Success criteria
- Estimated effort

## Alternative Approaches Considered

[Other solutions evaluated and why rejected]

## Acceptance Criteria

### Functional Requirements

- [ ] Detailed functional criteria

### Non-Functional Requirements

- [ ] Performance targets
- [ ] Security requirements
- [ ] Accessibility standards

### Quality Gates

- [ ] Test coverage requirements
- [ ] Documentation completeness
- [ ] Code review approval

## Success Metrics

[Detailed KPIs and measurement methods]

## Dependencies & Prerequisites

[Detailed dependency analysis]

## Risk Analysis & Mitigation

[Comprehensive risk assessment]

## Resource Requirements

[Team, time, infrastructure needs]

## Future Considerations

[Extensibility and long-term vision]

## Documentation Plan

[What docs need updating]

## References & Research

### Internal References

- Architecture decisions: [file_path:line_number]
- Similar features: [file_path:line_number]
- Configuration: [file_path:line_number]

### External References

- Framework documentation: [url]
- Best practices guide: [url]
- Industry standards: [url]

### Related Work

- Previous PRs: #[pr_numbers]
- Related issues: #[issue_numbers]
- Design documents: [links]
```

### Step 5: Issue Creation & Formatting

<thinking>
Apply best practices for clarity and actionability, making the plan easy to scan and understand.
</thinking>

**Content Formatting:**

- [ ] Use clear, descriptive headings with proper hierarchy (##, ###)
- [ ] Include code examples in triple backticks with language syntax highlighting
- [ ] Use task lists (- [ ]) for trackable items
- [ ] Add collapsible sections for lengthy logs or optional details using `<details>` tags
- [ ] Add names of files in pseudo code examples and todo lists
- [ ] Add an ERD mermaid diagram if applicable for new model changes

**Cross-Referencing:**

- [ ] Link to related issues/PRs using #number format
- [ ] Reference specific commits with SHA hashes when relevant
- [ ] Add links to external resources with descriptive text

**Pre-submission Checklist:**

- [ ] Title is searchable and descriptive
- [ ] All template sections are complete
- [ ] Links and references are working
- [ ] Acceptance criteria are measurable

## Output Format

**Filename:** Use the date and kebab-case filename from Step 2 Title & Categorization.

```
docs/plans/YYYY-MM-DD-<type>-<descriptive-name>-plan.md
```

Examples:
- `docs/plans/2026-01-15-feat-user-authentication-flow-plan.md`
- `docs/plans/2026-02-03-fix-checkout-race-condition-plan.md`
- `docs/plans/2026-03-10-refactor-api-client-extraction-plan.md`
- BAD: `docs/plans/2026-01-15-feat-thing-plan.md` (not descriptive)
- BAD: `docs/plans/2026-01-15-feat-new-feature-plan.md` (too vague)
- BAD: `docs/plans/2026-01-15-feat: user auth-plan.md` (invalid characters)
- BAD: `docs/plans/feat-user-auth-plan.md` (missing date prefix)

```bash
mkdir -p docs/plans
```

## Phase 5: Decompose into Beads

After writing the plan document, decompose into beads tasks.

### 5.1 Create Parent Epic(s)

```bash
bd create "<epic title>" --type epic --priority <P1/P2/P3> --description "<description>"
```

### 5.2 Create Features and Tasks

For each feature under an epic:
```bash
bd create "<feature title>" --type feature --priority <P1/P2/P3> --description "<description with acceptance criteria>"
```

For each task under a feature:
```bash
bd create "<task title>" --type task --priority <P1/P2/P3> --description "<description with acceptance criteria>"
```

### 5.3 Wire Dependencies

```bash
bd dep add <child-id> <parent-id>
```

### 5.4 Sync

```bash
bd sync
```

### 5.5 Show Results

```bash
bd list
bd ready
```

## Phase 6: Post-Plan Menu

Use **AskUserQuestion tool** to present options:

**Question:** "Plan created and decomposed into beads tasks. What would you like to do next?"

**Options:**
1. **Deepen the plan** - Run `/deepen-plan` for more detail and research
2. **Review the plan** - Run `/multi-review` for specialized feedback
3. **Dispatch workers** - Run `/dispatch` to start parallel execution
4. **Work solo** - Pick a task with `/start-task`
5. **Create GitHub issue** - Push plan to GitHub for team visibility
6. **Simplify** - Reduce detail level

Based on selection:
- **Deepen** -> Call `/deepen-plan` with the plan file path
- **Review** -> Call `/multi-review` with the plan file path
- **Dispatch** -> Call `/dispatch`
- **Work solo** -> Call `/start-task`
- **Create GitHub issue** -> See "Issue Creation" section below
- **Simplify** -> Ask "What should I simplify?" then regenerate simpler version

Loop back to options after Simplify changes until user selects an execution path.

## Issue Creation

When user selects "Create GitHub issue":

Use the title and type from Step 2 (already in context):

```bash
gh issue create --title "<type>: <title>" --body-file <plan_path>
```

**After creation:**
- Display the issue URL
- Ask if they want to proceed to `/dispatch`, `/start-task`, or `/multi-review`

NEVER CODE! Just research, plan, and decompose into tasks.
