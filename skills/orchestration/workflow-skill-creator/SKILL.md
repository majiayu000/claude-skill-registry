---
name: workflow-skill-creator
description: Compose multiple Claude Code skills into integrated workflows. Creates workflow skills that orchestrate skill sequences, handle dependencies, and automate multi-step processes. Use when building complex workflows, orchestrating multiple skills, or creating end-to-end automation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Workflow Skill Creator

## Overview

workflow-skill-creator provides a systematic workflow for composing multiple existing skills into integrated workflows. It enables creating higher-level skills that orchestrate sequences of other skills, manage dependencies, and automate complex multi-step processes.

**Purpose**: Build workflow skills that compose and orchestrate existing skills

**Pattern**: Workflow-based (5-step process)

**Key Benefit**: Transform multiple standalone skills into cohesive, automated workflows

## When to Use

Use workflow-skill-creator when:
- Building complex multi-step processes
- Orchestrating multiple existing skills
- Creating end-to-end automation workflows
- Standardizing common skill sequences
- Building domain-specific workflow skills
- Automating repetitive multi-skill tasks

## Prerequisites

Before creating workflow skills:
- **Existing skills**: Have 2+ skills to compose
- **Clear goal**: Know the workflow objective
- **Dependencies understood**: Know skill execution order
- **Integration points**: Understand skill inputs/outputs

## Workflow Composition Process

### Step 1: Identify Component Skills

Determine which existing skills will be composed into the workflow.

**What to Identify**:

1. **Workflow Objective**:
   - What does the workflow accomplish end-to-end?
   - What problem does it solve?
   - Who will use it?
   - What's the expected outcome?

2. **Required Capabilities**:
   - What actions are needed?
   - What expertise is required?
   - What tools must be used?
   - What validations are needed?

3. **Candidate Skills**:
   - Which existing skills provide needed capabilities?
   - Are all required skills available?
   - Are some skills missing (need to build)?
   - Are some skills optional (nice-to-have)?

4. **Skill Assessment**:
   - Does each skill do exactly what's needed?
   - Are skills well-documented?
   - Are skills tested and reliable?
   - Are there alternative skills?

**Assessment Template**:

```markdown
# Workflow: [Name]

## Objective:
[What the workflow accomplishes]

## Required Capabilities:
1. [Capability 1]: [What's needed]
2. [Capability 2]: [What's needed]
3. [Capability 3]: [What's needed]

## Component Skills:

### Skill 1: [Name]
- **Provides**: [Capability]
- **Status**: Available/Needs Building
- **Quality**: Tested/Untested
- **Alternative**: [Other options if any]

### Skill 2: [Name]
[Same structure]

## Gaps:
- [Missing capability 1]
- [Missing capability 2]

## Next Steps:
1. [Build missing skill X]
2. [Validate skill Y]
```

**Example**:

```markdown
# Workflow: Skill Development

## Objective:
Complete end-to-end skill development from research to validated, production-ready skill.

## Required Capabilities:
1. Research: Gather patterns, best practices, examples
2. Planning: Design skill structure, define scope
3. Task Breakdown: Create detailed task list with estimates
4. Progress Tracking: Monitor completion, identify blockers
5. Prompt Building: Create high-quality prompts for operations

## Component Skills:

### Skill 1: skill-researcher
- **Provides**: Research capability (web, GitHub, MCP, docs)
- **Status**: Available
- **Quality**: Tested, production-ready
- **Alternative**: Manual research (slower)

### Skill 2: planning-architect
- **Provides**: Skill planning and architecture design
- **Status**: Available
- **Quality**: Tested, production-ready
- **Alternative**: Manual planning (less structured)

### Skill 3: task-development
- **Provides**: Task breakdown with estimates and dependencies
- **Status**: Available
- **Quality**: Tested, production-ready
- **Alternative**: Manual task listing

### Skill 4: todo-management
- **Provides**: Progress tracking and momentum
- **Status**: Available
- **Quality**: Tested, production-ready
- **Alternative**: Manual tracking (less systematic)

### Skill 5: prompt-builder
- **Provides**: High-quality prompt creation
- **Status**: Available
- **Quality**: Tested, production-ready
- **Alternative**: Ad-hoc prompts (lower quality)

## Gaps:
- None (all required skills available)

## Next Steps:
1. Map dependencies between skills
2. Design workflow structure
```

**Questions to Answer**:
- What skills are essential vs. optional?
- Are all required skills available and working?
- What needs to be built before composing?
- Are there alternative skill choices?

**Validation**:
- [ ] Workflow objective clearly defined
- [ ] All required capabilities identified
- [ ] Component skills listed with status
- [ ] Gaps identified
- [ ] Assessment complete

→ **Output**: Component skill list with assessment

→ **Next**: Map how skills flow and depend on each other

### Step 2: Map Dependencies & Flow

Define the execution order and dependencies between component skills.

**What to Map**:

1. **Execution Sequence**:
   - What order should skills execute?
   - Which skills depend on others?
   - What can run in parallel?
   - What must be sequential?

2. **Data Flow**:
   - What does each skill produce?
   - What does each skill consume?
   - How is data passed between skills?
   - Where is intermediate data stored?

3. **Decision Points**:
   - Where are conditional branches?
   - What determines the path taken?
   - What happens on success vs. failure?
   - Are there loops or iterations?

4. **Error Handling**:
   - What can go wrong in each skill?
   - How should errors be handled?
   - Should workflow continue or stop on error?
   - Are there recovery strategies?

**Dependency Mapping Template**:

```markdown
# Workflow Dependencies: [Name]

## Execution Flow:

### Phase 1: [Phase Name]
- **Skill**: [skill-name]
- **Depends On**: [prerequisite skills or "None"]
- **Produces**: [output data/files]
- **Used By**: [subsequent skills]
- **Can Parallelize**: Yes/No

### Phase 2: [Phase Name]
[Same structure]

## Data Flow Diagram:

```
[Skill 1] --[output 1]--> [Skill 2] --[output 2]--> [Skill 3]
                             |
                             +--[output 2a]--> [Skill 4]
```

## Decision Points:

**Decision 1**: [After Skill X]
- **Condition**: [What determines path]
- **Path A**: [If condition true] → [Next skill]
- **Path B**: [If condition false] → [Alternative skill]

## Error Handling:

**Skill X Error**:
- **Type**: [Error category]
- **Response**: [Stop workflow / Continue / Retry]
- **Recovery**: [Manual intervention / Automatic / Fallback]

## Critical Path:
[List skills on critical path that cannot be parallelized]

## Parallel Opportunities:
[List skills that can run simultaneously]
```

**Example**:

```markdown
# Workflow Dependencies: Skill Development

## Execution Flow:

### Phase 1: Research
- **Skill**: skill-researcher
- **Depends On**: None (starting point)
- **Produces**: research-findings.md (patterns, best practices, examples)
- **Used By**: planning-architect (informs planning)
- **Can Parallelize**: No (must complete first)

### Phase 2: Planning
- **Skill**: planning-architect
- **Depends On**: skill-researcher (needs research findings)
- **Produces**: skill-plan.md (structure, scope, approach)
- **Used By**: task-development, prompt-builder
- **Can Parallelize**: No (depends on research)

### Phase 3: Task Breakdown & Prompt Design (Parallel)

**3A: Task Breakdown**
- **Skill**: task-development
- **Depends On**: planning-architect (needs skill plan)
- **Produces**: task-list.md (tasks with estimates, dependencies)
- **Used By**: todo-management
- **Can Parallelize**: Yes (parallel with 3B)

**3B: Prompt Design**
- **Skill**: prompt-builder
- **Depends On**: planning-architect (needs workflow steps from plan)
- **Produces**: prompts.md (high-quality prompts for each operation)
- **Used By**: skill implementation
- **Can Parallelize**: Yes (parallel with 3A)

### Phase 4: Progress Tracking
- **Skill**: todo-management
- **Depends On**: task-development (needs task list)
- **Produces**: todos.md (real-time progress tracking)
- **Used By**: Throughout implementation
- **Can Parallelize**: No (runs continuously during implementation)

## Data Flow Diagram:

```
[skill-researcher]
        ↓
    research-findings.md
        ↓
[planning-architect]
        ↓
    skill-plan.md
        ↓
    ┌───┴────┐
    ↓        ↓
[task-dev] [prompt-builder]
    ↓        ↓
task-list  prompts.md
    ↓
[todo-mgmt]
    ↓
  todos.md
```

## Decision Points:

**Decision 1**: After Research
- **Condition**: Sufficient examples found?
- **Path A**: Yes → Proceed to planning
- **Path B**: No → Additional research or build without examples

**Decision 2**: After Planning
- **Condition**: Skill complexity high?
- **Path A**: Yes → Use task-development for detailed breakdown
- **Path B**: No → Skip task-development, simple task list

## Error Handling:

**skill-researcher Error**:
- **Type**: No relevant sources found
- **Response**: Continue with limited information
- **Recovery**: Warn user, proceed with available knowledge

**planning-architect Error**:
- **Type**: Unclear requirements
- **Response**: Stop workflow
- **Recovery**: Request clarification from user

**task-development Error**:
- **Type**: Dependencies unclear
- **Response**: Continue with best effort
- **Recovery**: Note assumptions, continue

## Critical Path:
1. skill-researcher (must complete)
2. planning-architect (must complete)
3. task-development (must complete)
4. todo-management (continuous)

## Parallel Opportunities:
- Phase 3: task-development + prompt-builder can run simultaneously
```

**Flow Visualization Techniques**:

**Linear Flow**:
```
Skill A → Skill B → Skill C → Skill D
```

**Parallel Flow**:
```
Skill A
  ↓
Skill B
  ↓
┌─┴──┐
↓    ↓
C    D
└─┬──┘
  ↓
Skill E
```

**Conditional Flow**:
```
Skill A
  ↓
[Decision]
  ├─ Yes → Skill B
  └─ No  → Skill C
```

**Validation**:
- [ ] Execution sequence defined
- [ ] Dependencies documented
- [ ] Data flow mapped
- [ ] Decision points identified
- [ ] Error handling planned
- [ ] Parallel opportunities noted

→ **Output**: Dependency map with flow diagram

→ **Next**: Design the overall workflow structure

### Step 3: Design Workflow Structure

Create the architecture and organization for the workflow skill.

**What to Design**:

1. **Skill Organization**:
   - Workflow-based or task-based pattern?
   - How many steps/operations?
   - How to structure SKILL.md?
   - What goes in references/?

2. **Step/Operation Design**:
   - What does each step do?
   - How are component skills invoked?
   - What are inputs/outputs?
   - How is progress communicated?

3. **Integration Approach**:
   - Direct invocation vs. guidance?
   - Automated vs. manual transitions?
   - How to pass data between skills?
   - How to handle user interaction?

4. **Documentation Structure**:
   - How to document the workflow?
   - How to explain skill composition?
   - What examples to provide?
   - What troubleshooting to include?

**Structure Design Template**:

```markdown
# Workflow Structure: [Name]

## Pattern Choice:
[Workflow-based / Task-based] because [rationale]

## SKILL.md Structure:

### Main Content:
1. Overview
2. When to Use
3. Prerequisites
4. [Workflow Steps / Task Operations]
   - Step/Op 1: [Name]
   - Step/Op 2: [Name]
   - Step/Op 3: [Name]
5. Best Practices
6. Common Mistakes
7. Integration Notes

### references/ Directory:
- [reference-1].md: [Purpose]
- [reference-2].md: [Purpose]

### scripts/ Directory (if needed):
- [script-1].py: [Purpose]

## Step/Operation Specifications:

### Step 1: [Name]

**Purpose**: [What this step accomplishes in the workflow]

**Component Skill Used**: [skill-name]

**Integration Method**: [Direct invocation / Guided execution / Manual]

**Inputs**:
- [Input 1]: [Source]
- [Input 2]: [Source]

**Process**:
1. [Action 1]
2. [Action 2]
3. [Invoke component skill]
4. [Post-processing]

**Outputs**:
- [Output 1]: [Format, location]
- [Output 2]: [Format, location]

**Validation**:
- [ ] [Check 1]
- [ ] [Check 2]

**Next**: [Transition to next step]

### Step 2: [Name]
[Same structure]

## User Experience:

**Automation Level**: [Fully automated / Semi-automated / Guided]

**User Touchpoints**:
- [Point 1]: User provides [input]
- [Point 2]: User reviews [output]
- [Point 3]: User confirms [decision]

**Progress Visibility**:
- [How user sees progress]
- [Status updates provided]

## Error Handling Strategy:

**Error Type 1**: [Description]
- **Detection**: [How detected]
- **Response**: [What workflow does]
- **User Action**: [What user should do]

**Error Type 2**: [Description]
[Same structure]
```

**Example**:

```markdown
# Workflow Structure: Skill Development

## Pattern Choice:
Workflow-based because skill development is inherently sequential with clear phases that build on each other.

## SKILL.md Structure:

### Main Content:
1. Overview
2. When to Use (building new skills)
3. Prerequisites (have research goal, understand domain)
4. Skill Development Workflow
   - Step 1: Research Domain & Patterns
   - Step 2: Plan Skill Architecture
   - Step 3: Design Task Breakdown (Optional)
   - Step 4: Create High-Quality Prompts
   - Step 5: Track Implementation Progress
5. Best Practices (research-driven, systematic tracking)
6. Common Mistakes (skipping research, poor prompts)
7. Integration Notes (when to use each component skill)

### references/ Directory:
- workflow-examples.md: Example workflows from official skills
- composition-patterns.md: Common composition patterns
- troubleshooting.md: Common issues and solutions

### scripts/ Directory:
- None (component skills have their own scripts)

## Step Specifications:

### Step 1: Research Domain & Patterns

**Purpose**: Gather comprehensive knowledge about the domain, discover patterns, find examples, and validate approaches.

**Component Skill Used**: skill-researcher

**Integration Method**: Guided execution (user invokes skill-researcher with specific research goals)

**Inputs**:
- Research goal: [From user: "Research patterns for X skill"]
- Research scope: [Domain, technologies, specific questions]

**Process**:
1. User defines research goal
2. Invoke skill-researcher with 5 operations:
   a. Web Search Research (current practices)
   b. MCP Server Research (if integration needed)
   c. GitHub Repository Research (code patterns)
   d. Documentation Research (official specs)
   e. Synthesize Findings (create synthesis document)
3. Review synthesis document
4. Extract key patterns and recommendations

**Outputs**:
- research-findings.md: Comprehensive synthesis
- patterns-identified.md: Key patterns for skill
- examples.md: Code/structure examples

**Validation**:
- [ ] Minimum 3-5 sources consulted
- [ ] Patterns identified across sources
- [ ] Synthesis document created
- [ ] Recommendations are actionable

**Next**: Proceed to Step 2 with research findings

### Step 2: Plan Skill Architecture

**Purpose**: Design skill structure, define scope, choose organizational pattern, plan implementation approach.

**Component Skill Used**: planning-architect

**Integration Method**: Guided execution

**Inputs**:
- research-findings.md (from Step 1)
- Skill objective: [What the skill should accomplish]
- Target users: [Who will use it]

**Process**:
1. Review research findings
2. Invoke planning-architect workflow:
   a. Understand Requirements
   b. Choose Pattern (workflow/task/reference/capabilities)
   c. Design Structure (SKILL.md + references + scripts)
   d. Plan Content (what goes where)
   e. Validate Plan (completeness check)
3. Create skill plan document
4. Review and adjust

**Outputs**:
- skill-plan.md: Complete skill architecture
- structure-outline.md: File structure with sections
- content-specifications.md: What each section covers

**Validation**:
- [ ] Pattern chosen with rationale
- [ ] Structure designed (SKILL.md + references)
- [ ] Content planned for each section
- [ ] Plan validated against requirements

**Next**: Proceed to Step 3 (or skip if simple skill)

### Step 3: Design Task Breakdown (Optional)

**Purpose**: Break down skill implementation into detailed tasks with estimates and dependencies.

**Component Skill Used**: task-development

**Integration Method**: Guided execution (optional for complex skills)

**When to Use**:
- Complex skills (>20 tasks)
- Multiple contributors
- Tight timeline
- Need detailed planning

**When to Skip**:
- Simple skills (<10 tasks)
- Solo developer
- Flexible timeline

**Inputs**:
- skill-plan.md (from Step 2)

**Process**:
1. Review skill plan
2. Invoke task-development workflow:
   a. Analyze Skill Plan
   b. Identify Major Components
   c. Break Down Components into Tasks
   d. Estimate Each Task
   e. Identify Dependencies
   f. Sequence Tasks Optimally
3. Create task list with estimates
4. Identify critical path

**Outputs**:
- task-list.md: Complete task list with estimates
- dependencies.md: Task dependencies and critical path
- schedule.md: Optimal task sequence

**Validation**:
- [ ] All components broken into tasks
- [ ] Estimates provided for each task
- [ ] Dependencies identified
- [ ] Critical path marked
- [ ] Parallel opportunities noted

**Next**: Proceed to Step 4

[Continuing with remaining steps...]

### Step 4: Create High-Quality Prompts

**Purpose**: Build effective prompts for each workflow step or task operation in the skill.

**Component Skill Used**: prompt-builder

**Integration Method**: Guided execution

**Inputs**:
- skill-plan.md (workflow steps or operations)
- task-list.md (if available)

**Process**:
1. Identify each workflow step or operation that needs a prompt
2. For each prompt, invoke prompt-builder workflow:
   a. Understand Context (goal, audience, situation)
   b. Define Task Clearly (action verb, object, criteria)
   c. Structure Prompt (template, format)
   d. Add Context & Examples (background, patterns)
   e. Refine & Validate (quality check, score ≥4)
3. Collect all prompts
4. Review for consistency

**Outputs**:
- prompts.md: All prompts for workflow steps/operations
- validation-scores.md: Quality scores for each prompt

**Validation**:
- [ ] One prompt per workflow step/operation
- [ ] All prompts score ≥4 on quality dimensions
- [ ] Prompts are consistent in style
- [ ] Examples provided where helpful

**Next**: Proceed to Step 5

### Step 5: Track Implementation Progress

**Purpose**: Monitor task completion, identify blockers, maintain momentum throughout implementation.

**Component Skill Used**: todo-management

**Integration Method**: Continuous execution (used throughout implementation)

**Inputs**:
- task-list.md (from Step 3) OR simple task list

**Process**:
1. Initialize todo list from task list
2. Throughout implementation:
   a. Start Task (mark as in_progress)
   b. Complete Task (mark as completed)
   c. Report Progress (generate status reports)
   d. Identify Blockers (document obstacles)
   e. Update Estimates (track actuals vs estimates)
   f. Handle Task Changes (add/remove/modify)
   g. Maintain Momentum (ensure progress)
3. Continue until all tasks completed

**Outputs**:
- todos.md: Real-time task status
- progress-reports/: Status reports generated
- completion-summary.md: Final summary with actuals

**Validation**:
- [ ] Todo list initialized
- [ ] Tasks tracked in real-time
- [ ] Progress reports generated
- [ ] Blockers identified and addressed
- [ ] All tasks completed

**Next**: Skill implementation complete

## User Experience:

**Automation Level**: Semi-automated (user invokes each step, skills execute within)

**User Touchpoints**:
- Start: User defines research goal and skill objective
- Step 1: User reviews research findings, confirms patterns
- Step 2: User reviews skill plan, approves structure
- Step 3: User reviews task breakdown (if used)
- Step 4: User reviews prompts, confirms quality
- Step 5: User implements skill while tracking progress
- End: User has complete, tested skill

**Progress Visibility**:
- Each step shows completion status
- Step 5 (todo-management) provides continuous progress updates
- User always knows current phase and next action

## Error Handling Strategy:

**Error: Insufficient Research Findings**
- **Detection**: Step 1 synthesis has <3 sources
- **Response**: Workflow suggests additional research
- **User Action**: Conduct more research or proceed with limited information

**Error: Unclear Requirements**
- **Detection**: Step 2 planning cannot define clear scope
- **Response**: Workflow stops, requests clarification
- **User Action**: Provide more detail about skill objective

**Error: Task Estimates Wildly Off**
- **Detection**: Step 5 shows actual times >>estimates
- **Response**: Workflow notes learning opportunity
- **User Action**: Update estimates for future reference

**Error: Blocker in Implementation**
- **Detection**: Step 5 task marked as blocked
- **Response**: Workflow flags blocker, suggests resolution strategies
- **User Action**: Address blocker or escalate
```

**Design Principles**:

1. **Clarity First**:
   - Each step has clear purpose
   - Inputs/outputs explicit
   - Transitions obvious

2. **Flexibility**:
   - Optional steps where appropriate
   - Multiple paths allowed
   - Graceful degradation

3. **Visibility**:
   - Progress always visible
   - User knows next action
   - Errors clearly communicated

4. **Composability**:
   - Skills remain independent
   - Workflow orchestrates, doesn't replace
   - Can use skills individually if needed

**Validation**:
- [ ] Pattern chosen (workflow/task-based)
- [ ] SKILL.md structure designed
- [ ] Each step/operation specified
- [ ] Integration methods defined
- [ ] User experience mapped
- [ ] Error handling planned

→ **Output**: Complete workflow structure design

→ **Next**: Implement the workflow skill

### Step 4: Implement Composition

Write the workflow skill SKILL.md and supporting files.

**What to Implement**:

1. **SKILL.md Core**:
   - YAML frontmatter (name, description with triggers)
   - Overview section
   - When to Use section
   - Prerequisites section
   - Workflow steps or task operations (main content)
   - Best practices section
   - Common mistakes section
   - Integration notes

2. **Workflow Steps/Operations**:
   - Clear titles
   - Purpose statements
   - Component skill invocations
   - Input specifications
   - Process descriptions
   - Output specifications
   - Validation checklists
   - Transitions (for workflows)

3. **Reference Files** (if needed):
   - Detailed guides on specific topics
   - Examples and patterns
   - Troubleshooting guides

4. **Scripts** (if needed):
   - Automation helpers
   - Validation tools

**Implementation Checklist**:

**YAML Frontmatter**:
- [ ] `name:` in hyphen-case matching directory
- [ ] `description:` with "Use when" triggers
- [ ] No extra fields

**Overview**:
- [ ] Clear explanation of workflow purpose
- [ ] Pattern type stated
- [ ] Key benefit highlighted

**When to Use**:
- [ ] 3-5 specific scenarios listed
- [ ] Helps users identify when this workflow applies

**Prerequisites**:
- [ ] Required skills listed
- [ ] Required knowledge stated
- [ ] Pre-existing artifacts needed

**Main Content (Steps/Operations)**:

For each step/operation:
- [ ] Clear, action-oriented title
- [ ] Purpose statement (why this step exists)
- [ ] Component skill(s) identified
- [ ] Integration method explained
- [ ] Inputs listed with sources
- [ ] Process broken into sub-steps
- [ ] Outputs specified with formats
- [ ] Validation checklist provided
- [ ] Next step indicated (for workflows)

**Best Practices**:
- [ ] 3-5 key practices listed
- [ ] Each practice has rationale

**Common Mistakes**:
- [ ] 3-5 common mistakes identified
- [ ] Each has fix/solution

**Integration Notes**:
- [ ] Explains when to use which component skill
- [ ] Shows how skills work together
- [ ] Notes any special considerations

**Writing Guidelines**:

**Voice and Style**:
- Imperative for instructions ("Invoke skill-researcher...")
- Active voice ("The workflow orchestrates..." not "Skills are orchestrated...")
- Present tense for descriptions
- Clear, concise sentences

**Formatting**:
- Use `code blocks` for skill names, file names, commands
- Use **bold** for emphasis
- Use headings hierarchically (##, ###, ####)
- Use numbered lists for sequences
- Use bullet lists for unordered items
- Use checkboxes [ ] for validation criteria

**Examples**:
- Provide concrete examples where helpful
- Show actual content, not placeholders
- Explain what examples demonstrate

**Cross-References**:
- Link to component skills when mentioned
- Reference related documentation
- Point to examples in references/

**Example SKILL.md Structure**:

```markdown
---
name: skill-development-workflow
description: Complete end-to-end skill development workflow orchestrating research, planning, task breakdown, prompt design, and progress tracking. Use when building new Claude Code skills, creating workflow skills, or following systematic development process.
---

# Skill Development Workflow

## Overview

skill-development-workflow provides a complete end-to-end process for developing Claude Code skills. It orchestrates five component skills (skill-researcher, planning-architect, task-development, prompt-builder, todo-management) into a cohesive workflow that takes you from initial concept to validated, production-ready skill.

**Purpose**: Systematic, research-driven skill development

**Pattern**: Workflow-based (5-step process)

**Key Benefit**: Comprehensive skill development using proven best practices

## When to Use

Use skill-development-workflow when:
- Building a new Claude Code skill from scratch
- Want to follow systematic, research-driven approach
- Need to ensure quality through structured process
- Building complex workflows or orchestrations
- Want to leverage existing toolkit skills

## Prerequisites

Before starting this workflow:
- **Clear objective**: Know what skill you want to build
- **Component skills available**: skill-researcher, planning-architect, task-development, prompt-builder, todo-management
- **Time allocated**: 4-8 hours for complete workflow
- **Implementation time**: Additional time to actually build the skill

## Skill Development Workflow

### Step 1: Research Domain & Patterns

[Full step content as designed in Step 3...]

### Step 2: Plan Skill Architecture

[Full step content as designed in Step 3...]

### Step 3: Design Task Breakdown (Optional)

[Full step content as designed in Step 3...]

### Step 4: Create High-Quality Prompts

[Full step content as designed in Step 3...]

### Step 5: Track Implementation Progress

[Full step content as designed in Step 3...]

## Best Practices

1. **Research First**: Always start with research, don't skip
   - Grounds skill in proven patterns
   - Discovers existing solutions
   - Validates approach

2. **Plan Before Building**: Complete planning before implementation
   - Prevents rework
   - Ensures coherent structure
   - Identifies gaps early

3. **Use All Steps**: Don't skip steps (except optional Step 3 for simple skills)
   - Each step builds on previous
   - Compound benefits
   - Higher quality outcome

4. **Track Progress**: Use todo-management throughout
   - Maintains momentum
   - Identifies blockers early
   - Ensures completion

5. **Iterate Prompts**: Spend time on Step 4 prompt quality
   - Better prompts = better skill
   - Validation prevents issues
   - Consistency improves usability

## Common Mistakes

### Mistake 1: Skipping Research
**Problem**: Building skill without understanding patterns, reinventing solutions
**Fix**: Always complete Step 1 research, minimum 3-5 sources

### Mistake 2: Vague Planning
**Problem**: Starting implementation without clear structure
**Fix**: Complete Step 2 fully, validate plan before proceeding

### Mistake 3: Poor Prompt Quality
**Problem**: Using first-draft prompts without validation
**Fix**: Use Step 4 prompt-builder, ensure all prompts score ≥4

### Mistake 4: No Progress Tracking
**Problem**: Losing momentum, tasks incomplete, blockers unaddressed
**Fix**: Use Step 5 todo-management continuously throughout implementation

### Mistake 5: Trying to Do Everything at Once
**Problem**: Attempting all steps simultaneously, getting overwhelmed
**Fix**: Follow sequential workflow, complete each step before next

## Integration Notes

### Component Skills Used:

**skill-researcher** (Step 1):
- Used once at beginning
- Provides foundation for all subsequent steps
- Essential, do not skip

**planning-architect** (Step 2):
- Used once after research
- Depends on research findings
- Produces plan used by Steps 3-4

**task-development** (Step 3):
- Optional for simple skills
- Used once after planning
- For complex skills or team coordination

**prompt-builder** (Step 4):
- Used for each workflow step/operation
- Multiple invocations (one per prompt)
- Quality-critical step

**todo-management** (Step 5):
- Used continuously during implementation
- Started after task breakdown (or simple task list)
- Runs until skill complete

### When to Use Individually:

You can use component skills individually outside this workflow:
- skill-researcher: Any research need
- planning-architect: Planning any skill
- task-development: Breaking down any work
- prompt-builder: Creating any prompt
- todo-management: Tracking any task list

This workflow orchestrates them for complete skill development.

---

For composition patterns and examples, see references/composition-patterns.md.

For workflow design principles, see references/workflow-design.md.

For skill integration techniques, see references/skill-integration.md.
```

**Validation**:
- [ ] SKILL.md complete with all sections
- [ ] YAML frontmatter correct
- [ ] Each step/operation fully specified
- [ ] Component skill invocations clear
- [ ] Examples provided where helpful
- [ ] References created (if needed)
- [ ] Scripts implemented (if needed)
- [ ] Writing quality high

→ **Output**: Complete workflow skill files

→ **Next**: Test and validate the workflow

### Step 5: Test & Validate

Verify the workflow skill works correctly and provides value.

**What to Test**:

1. **Structure Validation**:
   - YAML frontmatter correct?
   - File structure complete?
   - All sections present?
   - Links work?

2. **Functional Validation**:
   - Can workflow be executed?
   - Do component skills work?
   - Do transitions make sense?
   - Is data flow correct?

3. **Usability Validation**:
   - Is workflow clear to follow?
   - Are instructions sufficient?
   - Do examples help?
   - Can user complete workflow?

4. **Quality Validation**:
   - Does workflow achieve objective?
   - Are outputs useful?
   - Is quality high?
   - Worth the effort?

**Testing Process**:

**1. Dry Run** (Mental execution):
- Read through entire workflow
- Imagine executing each step
- Identify unclear points
- Note missing information

**2. Component Test** (Test individual skills):
- Verify each component skill works
- Test with sample inputs
- Confirm outputs as expected
- Check error handling

**3. Integration Test** (Test workflow flow):
- Execute workflow end-to-end
- Use realistic scenario
- Follow all steps in order
- Note any friction points

**4. User Test** (Have someone else try):
- Fresh perspective catches issues
- Validates clarity
- Tests completeness
- Identifies improvements

**Validation Checklist**:

**Structure**:
- [ ] YAML frontmatter valid
- [ ] All sections present
- [ ] References accessible
- [ ] Scripts functional (if any)
- [ ] Links work

**Content**:
- [ ] Overview clear
- [ ] Prerequisites stated
- [ ] Steps/operations complete
- [ ] Inputs/outputs specified
- [ ] Validation criteria provided

**Component Integration**:
- [ ] All component skills identified
- [ ] Integration methods clear
- [ ] Data flow logical
- [ ] Dependencies handled

**Usability**:
- [ ] Easy to follow
- [ ] Instructions sufficient
- [ ] Examples helpful
- [ ] Error guidance provided

**Quality**:
- [ ] Achieves stated objective
- [ ] Outputs are useful
- [ ] Efficient (not overly complex)
- [ ] Worth using over manual approach

**Issues Found**:

For each issue:
1. Document the issue
2. Assess severity (Critical/High/Medium/Low)
3. Determine fix
4. Apply fix
5. Retest

**Example Issue Log**:

```markdown
## Issue 1: Unclear Transition
**Severity**: Medium
**Location**: Step 2 → Step 3
**Problem**: Not clear when to skip Step 3
**Fix**: Add explicit criteria for skipping
**Status**: Fixed, retested

## Issue 2: Missing Example
**Severity**: Low
**Location**: Step 4
**Problem**: No example of good prompt
**Fix**: Added example prompt with validation scores
**Status**: Fixed

## Issue 3: Component Skill Not Working
**Severity**: Critical
**Location**: Step 1, skill-researcher
**Problem**: WebSearch tool not available in test environment
**Fix**: Added note about environment requirements
**Status**: Fixed, added to prerequisites
```

**Validation Report Template**:

```markdown
# Validation Report: [Workflow Name]

**Date**: [YYYY-MM-DD]
**Validator**: [Name]
**Test Scenario**: [What was tested]

## Structure Validation: PASS/FAIL
[Details of structure checks]

## Functional Validation: PASS/FAIL
[Details of functional tests]

## Usability Validation: PASS/FAIL
[Details of usability assessment]

## Quality Validation: PASS/FAIL
[Details of quality evaluation]

## Issues Found: [Count]
[List of issues with severity and status]

## Overall Assessment: PASS/FAIL
[Summary and recommendation]

## Next Steps:
1. [Action item 1]
2. [Action item 2]
```

**Validation**:
- [ ] Dry run completed
- [ ] Component skills tested
- [ ] Integration tested end-to-end
- [ ] User testing conducted (if possible)
- [ ] Issues documented and fixed
- [ ] Validation report created
- [ ] Workflow ready for use

→ **Output**: Validated workflow skill ready for production

## Best Practices

### Workflow Composition

**1. Start Simple**:
- Compose 2-3 skills first
- Add complexity gradually
- Test at each stage
- Validate benefits

**2. Maintain Independence**:
- Component skills remain usable individually
- Workflow orchestrates, doesn't replace
- Loose coupling
- Clear interfaces

**3. Design for Users**:
- Clear transitions
- Obvious next steps
- Helpful examples
- Error guidance

**4. Document Thoroughly**:
- Why each component skill?
- How do they integrate?
- What are tradeoffs?
- When to use alternatives?

**5. Test Rigorously**:
- Dry run first
- Test components
- Test integration
- Test with users

### Integration Patterns

**Sequential Workflows**:
```
Skill A → Skill B → Skill C
```
- Each step completes before next
- Clear dependencies
- Predictable flow

**Parallel Workflows**:
```
    ┌→ Skill B ┐
Skill A         → Skill D
    └→ Skill C ┘
```
- Independent skills run together
- Efficiency gains
- Requires coordination

**Conditional Workflows**:
```
Skill A
  ↓
[Decision]
  ├─ Path 1 → Skill B
  └─ Path 2 → Skill C
```
- Branches based on conditions
- Flexible workflows
- Handle variations

**Iterative Workflows**:
```
Skill A → Skill B → Skill C
            ↑         ↓
            └─[Loop]──┘
```
- Repeat until condition met
- Continuous improvement
- Progressive refinement

## Common Mistakes

### Mistake 1: Over-Orchestration

**Problem**: Workflow too rigid, removes flexibility
- Forces specific tool/approach
- Prevents adaptation
- Reduces usability

**Fix**: Keep workflows flexible
- Allow optional steps
- Permit alternative paths
- Enable partial execution

### Mistake 2: Under-Documentation

**Problem**: Users don't understand how skills compose
- Missing integration explanations
- No examples
- Unclear benefits

**Fix**: Document thoroughly
- Explain each composition
- Show concrete examples
- Clarify value proposition

### Mistake 3: Tight Coupling

**Problem**: Workflow breaks if component skill changes
- Hard dependencies
- Fragile integration
- Difficult maintenance

**Fix**: Loose coupling
- Document interfaces, not implementations
- Allow substitutions
- Version compatibility notes

### Mistake 4: No Error Handling

**Problem**: Workflow fails silently or ungracefully
- No recovery strategies
- Unclear error messages
- Workflow stops without guidance

**Fix**: Plan error handling
- Define error responses
- Provide recovery paths
- Give clear guidance

### Mistake 5: Skipping Validation

**Problem**: Workflow released without testing
- Hidden bugs
- Poor usability
- User frustration

**Fix**: Test thoroughly
- Dry run
- Component testing
- Integration testing
- User testing

## Integration with Other Skills

### With planning-architect

**Use workflow-skill-creator** when planning workflow skills
- Compose planning with other skills
- Create meta-planning workflows

**Flow**: plan workflow → use workflow-skill-creator → build workflow skill

### With skill-researcher

**Use workflow-skill-creator** after researching workflow patterns
- Research common workflows
- Identify composition opportunities
- Apply patterns

**Flow**: research workflows → identify patterns → compose skills

### With prompt-builder

**Use workflow-skill-creator** with prompt-builder for workflow step prompts
- Each workflow step needs prompts
- Prompt-builder ensures quality
- Workflow orchestrates execution

**Flow**: design workflow → build prompts for steps → implement workflow

## Quick Reference

### The 5-Step Process

1. **Identify Component Skills**: What skills to compose?
2. **Map Dependencies & Flow**: How do skills relate?
3. **Design Workflow Structure**: What's the architecture?
4. **Implement Composition**: Write SKILL.md and files
5. **Test & Validate**: Does it work?

### Composition Checklist

- [ ] Workflow objective clear
- [ ] Component skills identified and available
- [ ] Dependencies mapped
- [ ] Flow diagram created
- [ ] Structure designed
- [ ] SKILL.md implemented
- [ ] Component integrations working
- [ ] Tested end-to-end
- [ ] Documentation complete
- [ ] Ready for use

### Integration Patterns

- **Sequential**: A → B → C
- **Parallel**: A → (B + C) → D
- **Conditional**: A → [decision] → B or C
- **Iterative**: A → B → [loop] → C

---

For detailed composition patterns and examples, see references/composition-patterns.md.

For workflow design principles and architectures, see references/workflow-design.md.

For skill integration techniques and best practices, see references/skill-integration.md.
