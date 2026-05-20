---
name: create-spec
description: Create a new specification through an adaptive interview process with proactive recommendations and optional research. Use when user says "create spec", "new spec", "generate spec", or wants to start a specification document.
user-invocable: true
disable-model-invocation: false
allowed-tools: AskUserQuestion, Task, Read, Write, Glob, Grep, Bash, TeamCreate, TeamDelete, TaskCreate, TaskUpdate, TaskList, TaskGet, SendMessage
---

# Create Spec Skill

You are initiating the spec creation workflow. This process gathers requirements through an adaptive, multi-round interview and generates a comprehensive specification document.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Every interview round question → AskUserQuestion
- Confirmation questions → AskUserQuestion
- Yes/no consent questions → AskUserQuestion
- Clarifying questions → AskUserQuestion

Text output should only be used for:
- Summarizing what you've learned
- Presenting information
- Explaining context

If you need the user to make a choice or provide input, use AskUserQuestion.

**NEVER do this** (asking via text output):
```
What features are most important to you?
1. Performance
2. Usability
3. Security
```

**ALWAYS do this** (using AskUserQuestion tool):
```yaml
AskUserQuestion:
  questions:
    - header: "Priority"
      question: "What features are most important to you?"
      options:
        - label: "Performance"
          description: "Speed and responsiveness"
        - label: "Usability"
          description: "Ease of use"
        - label: "Security"
          description: "Data protection"
      multiSelect: true
```

### Plan Mode Behavior

**CRITICAL**: This skill generates a spec document, NOT an implementation plan. When invoked during Claude Code's plan mode:

- **DO NOT** create an implementation plan for how to build the spec's described features
- **DO NOT** defer spec generation to an "execution phase"
- **DO** proceed with the full interview and spec generation workflow immediately
- **DO** write the spec file to the output path as normal

The spec is a planning artifact itself — generating it IS the planning activity.

## Workflow Overview

This workflow has six phases:

1. **Settings Check** — Load user configuration
2. **Initial Inputs** — Gather spec name, type, depth, and description
3. **Adaptive Interview** — Multi-round depth-aware interview with recommendations and optional research
4. **Recommendations Round** — Dedicated round for accumulated best-practice suggestions (if applicable)
5. **Pre-Compilation Summary** — Present gathered requirements for user confirmation
6. **Spec Compilation** — Generate spec from template and write to file

---

## Phase 1: Settings Check

Check if there is a settings file at `.claude/claude-alchemy.local.md` to get any custom configuration like output path or author name.

---

## Phase 2: Initial Inputs

Use `AskUserQuestion` to gather the essential starting information with these four questions:

**Question 1 - Spec Name:**
- Header: "Spec Name"
- Question: "What would you like to name this spec?"
- Options: Allow text input for a descriptive name

**Question 2 - Type:**
- Header: "Type"
- Question: "What type of product/feature is this?"
- Options:
  - "New product" - A completely new product being built from scratch
  - "New feature" - A new feature for an existing product

**Question 3 - Depth:**
- Header: "Depth"
- Question: "How detailed should the spec be?"
- Options:
  - "High-level overview (Recommended)" - Executive summary with key features and goals
  - "Detailed specifications" - Standard spec with acceptance criteria and phases
  - "Full technical documentation" - Comprehensive specs with API definitions and data models

**Question 4 - Description:**
- Header: "Description"
- Question: "Briefly describe the product/feature and its key requirements"
- Options: Allow text input describing the problem, main features, and constraints

---

## Phase 3: Adaptive Interview

### Prepare for Interview

Before starting Round 1, read these reference files to load the full question bank and trigger patterns:

1. `references/interview-questions.md` — Question bank organized by category and depth level
2. `references/recommendation-triggers.md` — Trigger patterns for proactive recommendations across all domains

Use these as your primary source for questions and trigger detection throughout the interview.

### Interview Strategy

#### Depth-Aware Questioning

Adapt your interview depth based on the requested level:

**High-level overview** (2-3 rounds):
- Focus on problem, goals, key features, and success metrics
- Skip deep technical details
- Ask broader, strategic questions
- Total of 6-10 questions across all rounds

**Detailed specifications** (3-4 rounds):
- Balanced coverage of all categories
- Include acceptance criteria for features
- Cover technical constraints without deep architecture
- Total of 12-18 questions across all rounds

**Full technical documentation** (4-5 rounds):
- Deep probing on all areas
- Request specific API endpoints, data models
- Detailed performance and security requirements
- Total of 18-25 questions across all rounds

#### Question Categories

Cover all four categories, but adjust depth based on level:

1. **Problem & Goals**: Problem statement, success metrics, user personas, business value
2. **Functional Requirements**: Features, user stories, acceptance criteria, workflows
3. **Technical Specs**: Architecture, tech stack, data models, APIs, constraints
4. **Implementation**: Phases, dependencies, risks, out of scope items

#### Adaptive Behavior

- **Build on previous answers**: Reference what the user already told you
- **Skip irrelevant questions**: If user says "no preference" on tech stack, skip detailed tech questions
- **Probe deeper on important areas**: If user indicates something is critical, ask follow-up questions
- **Explore codebase when helpful**: For "new feature" type, offer to explore relevant code (with user approval)
- **If something is unclear, ask for clarification** rather than assuming

### Round Structure

Each round MUST:
1. Summarize what you've learned so far (briefly) — use text output
2. Ask 3-5 focused questions using `AskUserQuestion` — REQUIRED, never use text for questions
3. Use a mix of multiple choice (for structured data) and open text (for details)
4. **Detect triggers**: Note any recommendation triggers in user responses
5. **Offer inline insights** (optional): If triggers detected, offer 1-2 brief recommendations
6. Acknowledge responses before moving to next round

**Question Guidelines:**
- Keep questions clear and specific
- Provide helpful options for multiple choice where appropriate
- Use "Other" option for flexibility
- Group related questions together
- Don't overwhelm — max 4 questions per AskUserQuestion call

**Example Question Patterns:**

For structured choices:
```yaml
header: "Priority"
question: "What priority is this feature?"
options:
  - label: "P0 - Critical"
    description: "Must have for initial release"
  - label: "P1 - High"
    description: "Important but can follow fast"
  - label: "P2 - Medium"
    description: "Nice to have"
```

For open-ended input:
```yaml
header: "Problem"
question: "What specific problem are you trying to solve?"
options:
  - label: "Efficiency"
    description: "Users spend too much time on manual tasks"
  - label: "Quality"
    description: "Current solution produces errors or poor results"
  - label: "Access"
    description: "Users can't do something they need to do"
```

### Proactive Recommendations

Throughout the interview, watch for patterns in user responses that indicate opportunities for best-practice recommendations. When detected, offer relevant suggestions based on industry standards.

**Trigger Detection**: After receiving user responses each round, scan for trigger keywords from the loaded `references/recommendation-triggers.md`. The file covers domains including: Authentication, Scale & Performance, Security & Compliance, Real-Time Features, File & Media, API Design, Search & Discovery, Testing, and Accessibility.

**When to Offer Recommendations:**
- **Inline insights**: Brief suggestions during rounds when triggers detected (max 2 per round)
- **Recommendations round**: Accumulated recommendations presented in Phase 4
- Always present recommendations for user approval — never assume acceptance

**Inline Insight Format:**
```yaml
AskUserQuestion:
  questions:
    - header: "Quick Insight"
      question: "{Brief recommendation}. Would you like to include this in the spec?"
      options:
        - label: "Include this"
          description: "Add to spec requirements"
        - label: "Tell me more"
          description: "Get more details"
        - label: "Skip"
          description: "Continue without this"
      multiSelect: false
```

**For detailed recommendation templates, refer to:** `references/recommendation-format.md`

**Tracking Recommendations:**
Maintain internal tracking of detected triggers and accepted recommendations:
- Detected triggers with source round
- Accepted recommendations with target spec section
- Skipped/modified recommendations

**Trigger Detection per Round:**
- After receiving user responses, scan for trigger keywords
- Note triggers internally for the recommendations round
- For high-priority triggers (compliance, security), consider inline insight immediately

### Codebase Exploration (New Feature Type)

If the product type is "New feature for existing product":

1. Use `AskUserQuestion` to offer exploration options:
   ```yaml
   questions:
     - header: "Codebase"
       question: "How would you like to explore the codebase before we start the interview?"
       options:
         - label: "Deep team analysis (Recommended)"
           description: "Thorough parallel exploration with synthesis — 3-5 minutes"
         - label: "Quick exploration"
           description: "Basic pattern scanning with Glob/Grep/Read — 1-2 minutes"
         - label: "Skip"
           description: "Continue without code exploration"
       multiSelect: false
   ```

2. **If "Deep team analysis" selected:**
   1. Read the teams-deep-analysis skill: `${CLAUDE_PLUGIN_ROOT}/../tools/skills/teams-deep-analysis/SKILL.md`
   2. Follow its full workflow (Phases 1-4) with analysis context set to:
      ```
      Feature exploration for spec: {spec_name}. Description: {user's description from Phase 2}.
      Focus on: existing patterns, conventions, integration points, data models to extend,
      and similar features that could serve as implementation references.
      ```
   3. After the analysis completes and control returns, store the synthesized findings internally as "Codebase Context" for use in subsequent interview rounds and spec compilation
   4. Present a brief summary of key findings to the user before starting the interview

   **Error handling / fallback:**
   If the teams-deep-analysis workflow fails at any point (TeamCreate fails, agents fail, etc.):
   1. Inform the user that deep analysis encountered an issue
   2. Use `AskUserQuestion` to offer fallback:
      ```yaml
      questions:
        - header: "Fallback"
          question: "Deep analysis encountered an issue. How would you like to proceed?"
          options:
            - label: "Quick exploration"
              description: "Fall back to basic Glob/Grep/Read exploration"
            - label: "Skip"
              description: "Continue without codebase analysis"
          multiSelect: false
      ```
   3. If quick exploration: use basic Glob/Grep/Read (see below)
   4. If skip: continue to Phase 3 Round 1 with whatever findings were gathered

3. **If "Quick exploration" selected:**
   - Use `Glob`, `Grep`, and `Read` to understand:
     - Existing patterns and conventions
     - Related features that could inform this one
     - Integration points
     - Data models that might be extended
   - Share relevant findings with the user
   - Use findings to inform follow-up questions

4. **If "Skip" selected:**
   - Continue directly to Phase 3 Round 1

### Using Exploration Findings in Interview

When codebase exploration was performed (deep or quick), use the findings throughout the interview:

1. **Tailor technical questions** — Reference specific files, patterns, and conventions discovered during exploration
2. **Skip answered questions** — If exploration already revealed tech stack, data models, or architecture, confirm rather than ask open-ended questions
3. **Ask targeted integration questions** — e.g., "The codebase uses {pattern X} for similar features. Should this feature follow the same pattern?"
4. **Surface risks early** — If exploration found challenges (tight coupling, missing tests, complex dependencies), ask about acceptable trade-offs
5. **Inform recommendations** — Use exploration findings as evidence for recommendations in Phase 4

Store findings internally as "Codebase Context" and reference throughout interview and spec compilation.

### External Research

Research can be invoked in two ways: on-demand when the user requests it, or proactively for specific high-value topics.

#### On-Demand Research

When the user explicitly requests research about technologies or general topics during the interview, invoke the research agent.

**Technical research triggers:**
- "Research the {API/library} documentation"
- "Look up what {technology} supports"
- "Check the docs for {feature}"
- "What does {library} provide for {feature}?"

**General topic research triggers:**
- "Research best practices for {area}"
- "How do competitors handle {feature}?"
- "What are the industry standards for {area}?"
- "Research {compliance} requirements" (GDPR, HIPAA, WCAG, etc.)
- "Help me understand the problem space for {domain}"
- "What do users expect from {feature type}?"

#### Proactive Research

**You MAY proactively research** (without explicit user request) for specific high-value topics:

**Auto-research triggers:**
- **Compliance mentions**: GDPR, HIPAA, PCI DSS, SOC 2, WCAG, ADA compliance
- **User uncertainty**: "I'm not sure", "what do you recommend?", "what's standard?"
- **Complex trade-offs**: When multiple valid approaches exist and current information would help

**Proactive research limit**: Maximum 2 proactive research calls per interview to avoid slowing down the process.

**Before proactive research**, briefly inform the user:
```
Since you mentioned GDPR compliance, let me quickly research the current requirements to ensure we capture them accurately.
```

#### Invoking Research

Use the Task tool with subagent_type `claude-alchemy-sdd:research-agent`:

```
Task prompt template:
"Research {topic} for spec '{spec_name}'.

Context: {What section of the spec this relates to}
Depth level: {high-level/detailed/full-tech}

Specific questions:
- {Question 1}
- {Question 2}

Return findings in spec-ready format."
```

#### Incorporating Research Findings

After receiving research results:

1. **Add to interview notes** under the appropriate category:
   - Technical findings → Technical Specifications
   - Best practices → Functional Requirements
   - Compliance → Non-Functional Requirements
   - Competitive → Problem Statement / Solution Overview

2. **Use findings for recommendations**: Research-backed recommendations are more valuable; include source attribution

3. **Use findings to ask informed follow-ups**: Research may reveal new areas to explore

4. **Credit sources**: Include research sources in spec references section

#### Tracking Research Usage

Track proactive research usage during the interview:
```
Proactive Research: 1/2 used
- [Round 2] GDPR requirements - informed compliance recommendation
```

### Early Exit

If the user indicates they want to wrap up early (signals like "I think that's enough", "let's wrap up", "that covers it", "skip the rest"), handle it gracefully:

1. Acknowledge the request
2. Present a truncated summary of what was gathered so far using the Pre-Compilation Summary format (Phase 5)
3. Use `AskUserQuestion` to confirm:
   ```yaml
   questions:
     - header: "Early Completion"
       question: "Here's what I've gathered so far. Should I generate the spec with this information, or would you like to add anything?"
       options:
         - label: "Generate spec"
           description: "Proceed with what we have"
         - label: "Add more"
           description: "I want to provide additional details"
       multiSelect: false
   ```
4. If generating, add `**Status**: Draft (Partial)` to the spec metadata to indicate incomplete coverage
5. Proceed to Phase 6 (Spec Compilation)

---

## Phase 4: Recommendations Round

After completing the main interview rounds and before the summary, present a dedicated recommendations round.

### When to Include

- **Skip for high-level depth**: High-level specs focus on problem/goals; recommendations may be premature
- **Include for detailed/full-tech**: These depths benefit from architectural and technical recommendations
- **Skip if no triggers detected**: If no recommendation triggers were found, proceed directly to Phase 5

### Recommendation Categories

Present recommendations organized by category:

1. **Architecture**: Patterns, scaling approaches, data models
2. **Security**: Authentication, encryption, compliance
3. **User Experience**: Accessibility, performance, error handling
4. **Operational**: Monitoring, deployment, testing strategies

### Presentation Format

Introduce the recommendations round briefly:

```
Based on what you've shared, I have a few recommendations based on industry best practices.
I'll present each for your review — you can accept, modify, or skip any of them.
```

Then present each recommendation using `AskUserQuestion`:

```yaml
AskUserQuestion:
  questions:
    - header: "Recommendation {N} of {Total}: {Category}"
      question: "{Recommendation}\n\n**Why this matters:**\n{Brief rationale}"
      options:
        - label: "Accept"
          description: "Include in spec"
        - label: "Modify"
          description: "Adjust this recommendation"
        - label: "Skip"
          description: "Don't include"
      multiSelect: false
```

### Handling Modifications

If user selects "Modify":
1. Ask what they'd like to change using `AskUserQuestion`
2. Present the modified recommendation for confirmation
3. Add the modified version to accepted recommendations

### Tracking

After the recommendations round, update internal tracking:
- Mark each recommendation as accepted, modified, or skipped
- Note the target spec section for accepted recommendations
- Modified recommendations include the user's adjustments

---

## Phase 5: Pre-Compilation Summary

Before compilation, present a comprehensive summary:

```markdown
## Requirements Summary

### Problem & Goals
- Problem: {summarized problem statement}
- Success Metrics: {list metrics}
- Primary User: {persona description}
- Business Value: {why this matters}

### Functional Requirements
{List each feature with acceptance criteria}

### Technical Specifications
- Tech Stack: {choices or constraints}
- Integrations: {systems to integrate with}
- Performance: {requirements}
- Security: {requirements}

### Implementation
- Phases: {list phases}
- Dependencies: {list dependencies}
- Risks: {list risks}
- Out of Scope: {list exclusions}

### Agent Recommendations (Accepted)
*The following recommendations were suggested based on industry best practices and accepted during the interview:*

1. **{Category}**: {Recommendation title}
   - Rationale: {Why this was recommended}
   - Applies to: {Which section/feature}

{Continue for all accepted recommendations, or note "No recommendations accepted" if none}

### Open Questions
{Any unresolved items}
```

**Important**: Clearly distinguish the "Agent Recommendations" section from user-provided requirements. This transparency helps stakeholders understand which requirements came from the user versus agent suggestions.

Then use `AskUserQuestion` to confirm:

```yaml
questions:
  - header: "Summary Review"
    question: "Is this requirements summary accurate and complete?"
    options:
      - label: "Yes, proceed to spec"
        description: "Summary is accurate, generate the spec"
      - label: "Needs corrections"
        description: "I have changes or additions"
    multiSelect: false
```

If user selects "Needs corrections", ask what they'd like to change using AskUserQuestion, then update the summary and confirm again.

**Never skip the summary confirmation step.** Only proceed to compilation after user explicitly confirms via AskUserQuestion.

---

## Phase 6: Spec Compilation

### Template Selection

Choose the appropriate template based on depth level:

| Depth Level | Template | Use Case |
|-------------|----------|----------|
| High-level overview | `references/templates/high-level.md` | Executive summaries, stakeholder alignment, initial scoping |
| Detailed specifications | `references/templates/detailed.md` | Standard development specs with clear requirements |
| Full technical documentation | `references/templates/full-tech.md` | Complex features requiring API specs, data models, architecture |

### Compilation Steps

1. **Read the appropriate template** based on depth level

2. **Check for settings** at `.claude/claude-alchemy.local.md` for:
   - Custom output path
   - Author name

3. **Apply spec metadata formatting**:
   - Use the title format `# {spec-name} PRD`
   - Include these metadata fields in the header block after Status:
     - `**Spec Type**`: The product type selected during the interview
     - `**Spec Depth**`: The depth level selected
     - `**Description**`: The initial description provided by the user
   - If early exit was used, set `**Status**: Draft (Partial)`

4. **Organize information** into template sections

5. **Fill gaps** by inferring logical requirements (flag assumptions clearly)

6. **Add acceptance criteria** for each functional requirement

7. **Define phases** with clear completion criteria

8. **Insert checkpoint gates** at critical decision points

9. **Review for completeness** before writing

10. **Write the spec** to the configured output path (default: `specs/SPEC-{name}.md`)

11. **Present the completed spec location** to the user

### Writing Guidelines

#### Requirement Formatting

```markdown
### REQ-001: [Requirement Name]

**Priority**: P0 (Critical) | P1 (High) | P2 (Medium) | P3 (Low)

**Description**: Clear, concise statement of what is needed.

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

**Notes**: Any additional context or constraints.
```

#### User Story Format

```markdown
**As a** [user type]
**I want** [capability]
**So that** [benefit/value]
```

#### API Specification Format (Full Tech Only)

```markdown
#### Endpoint: `METHOD /path`

**Purpose**: Brief description

**Request**:
- Headers: `Content-Type: application/json`
- Body:
  ```json
  {
    "field": "type - description"
  }
  ```

**Response**:
- `200 OK`: Success response schema
- `400 Bad Request`: Validation errors
- `401 Unauthorized`: Authentication required
```

---

## Core Principles

These principles guide how specs should be structured:

### 1. Phase-Based Milestones (Not Timelines)

Specs should define clear phases with completion criteria rather than time estimates:

- **Phase 1: Foundation** - Core infrastructure and data models
- **Phase 2: Core Features** - Primary user-facing functionality
- **Phase 3: Enhancement** - Secondary features and optimizations
- **Phase 4: Polish** - UX refinement, edge cases, documentation

### 2. Testable Requirements

Every requirement should include:
- **Clear acceptance criteria** - Specific, measurable conditions for completion
- **Test scenarios** - How to verify the requirement is met
- **Edge cases** - Known boundary conditions to handle

### 3. Human Checkpoint Gates

Define explicit points where human review is required:
- Architecture decisions before implementation begins
- API contract review before integration work
- Security review before authentication/authorization features
- UX review before user-facing changes ship

### 4. Context for AI Consumption

Structure specs for optimal AI assistant consumption:
- Use consistent heading hierarchy
- Include code examples where applicable
- Reference existing patterns in the codebase
- Provide clear file location guidance

---

## Reference Files

- `references/interview-questions.md` — Question bank organized by category and depth level
- `references/recommendation-triggers.md` — Trigger patterns for proactive recommendations
- `references/recommendation-format.md` — Templates for presenting recommendations
- `references/templates/high-level.md` — Streamlined executive overview template
- `references/templates/detailed.md` — Standard spec template with all sections
- `references/templates/full-tech.md` — Extended template with technical specifications
