---
name: prompt-builder
description: Build effective prompts for Claude Code skills. Creates clear, specific, actionable prompts using engineering principles, templates, and validation. Use when creating skill instructions, workflow steps, task operations, or any Claude prompt.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebSearch, WebFetch
---

# Prompt Builder

## Overview

prompt-builder provides a systematic workflow for creating effective prompts in Claude Code skills. It applies prompt engineering principles, uses proven templates, and validates quality to ensure prompts are clear, specific, actionable, and produce reliable results.

**Purpose**: Create high-quality prompts for skills, workflows, tasks, and operations

**Pattern**: Workflow-based (5-step process)

**Key Benefit**: Transforms vague instructions into precise, effective prompts that Claude can execute reliably

## When to Use

Use prompt-builder when:
- Creating new skill instructions
- Writing workflow steps that Claude will execute
- Defining task operations
- Building automation prompts
- Improving existing prompts that produce inconsistent results
- Ensuring prompts follow best practices

## Prerequisites

Before building prompts:
- **Clear objective**: Know what the prompt should accomplish
- **Context understanding**: Understand the situation where the prompt will be used
- **Success criteria**: Define what "good output" looks like

## Prompt Building Workflow

### Step 1: Understand Context

Before writing any prompt, understand the full context.

**What to Identify**:

1. **Goal**: What should this prompt accomplish?
   - Create something new?
   - Transform existing content?
   - Analyze and provide insights?
   - Make a decision?

2. **Audience**: Who will use this prompt?
   - Claude directly (in skill)?
   - Developer building skills?
   - End user interacting with system?

3. **Situation**: When/where will this prompt be used?
   - Part of sequential workflow?
   - Independent task operation?
   - Conditional branch?
   - Error recovery?

4. **Constraints**: What limitations exist?
   - Time limits?
   - Output format requirements?
   - Tools available/unavailable?
   - Dependencies on other steps?

5. **Success criteria**: How do you know it worked?
   - Measurable outcome?
   - Specific format?
   - Validation criteria?

**Questions to Ask**:
- What problem does this prompt solve?
- What does "success" look like?
- What could go wrong?
- What information does Claude need?
- What should Claude NOT do?

**Example Context Analysis**:

```markdown
Goal: Have Claude write a comprehensive guide for a reference file
Audience: Claude (executing skill)
Situation: Step 3 of 6 in skill-building workflow
Constraints: Must be <5,000 words, specific format
Success: Complete guide covering all topics, properly formatted
```

**Common Context Mistakes**:
- ❌ Skip context analysis, jump straight to writing
- ❌ Assume context is obvious
- ❌ Don't define success criteria
- ❌ Ignore constraints

**Best Practices**:
- ✅ Write down context explicitly
- ✅ Identify all constraints upfront
- ✅ Define measurable success
- ✅ Consider edge cases

→ **Output**: Context analysis document

→ **Next**: With context clear, define the specific task

### Step 2: Define Task Clearly

Transform the goal into a clear, specific, actionable task definition.

**Task Definition Elements**:

1. **Action Verb**: What specific action?
   - Good: "Write", "Analyze", "Create", "Transform", "Extract"
   - Avoid: "Handle", "Deal with", "Work on", "Process"

2. **Object**: What is being acted upon?
   - Be specific: "the authentication module" not "the code"
   - Include type: "markdown file", "Python function", "data structure"

3. **Constraints**: What limits or requirements?
   - Format: "as a bulleted list", "in JSON format"
   - Length: "under 500 words", "10-15 items"
   - Style: "imperative voice", "technical language"

4. **Quality Criteria**: What makes output good?
   - Completeness: "covering all edge cases"
   - Accuracy: "matching the specification exactly"
   - Usability: "beginner-friendly explanations"

5. **Context References**: What information to use?
   - "based on the examples in references/"
   - "following the pattern from Step 2"
   - "using the template below"

**Task Clarity Checklist**:
- [ ] Action verb is specific and unambiguous
- [ ] Object is clearly identified
- [ ] Constraints are explicitly stated
- [ ] Success criteria are measurable
- [ ] Context references are provided
- [ ] Can be completed without additional questions

**Good vs Bad Task Definitions**:

❌ **Bad**: "Update the documentation"
- Vague action, unclear object, no criteria

✅ **Good**: "Write a Getting Started section for README.md covering installation, basic usage, and first example. Use imperative voice, keep under 300 words, include 2-3 code examples."
- Clear action, specific object, defined constraints and criteria

❌ **Bad**: "Make the code better"
- Subjective, unmeasurable, no direction

✅ **Good**: "Refactor the authentication function to use async/await pattern, add error handling for network failures, and include JSDoc comments for each parameter."
- Specific improvements, clear criteria, measurable outcome

**Task Definition Template**:

```markdown
[ACTION VERB] [SPECIFIC OBJECT] that [QUALITY CRITERIA].

Constraints:
- [Format/Structure requirement]
- [Length/Size requirement]
- [Style/Tone requirement]

Success means:
- [Measurable criterion 1]
- [Measurable criterion 2]
- [Measurable criterion 3]

Use/Reference:
- [Context source 1]
- [Context source 2]
```

**Example Task Definition**:

```markdown
Write a comprehensive dependency management guide that explains identification,
documentation, critical path analysis, and optimization strategies.

Constraints:
- Structure: 4 main sections with subsections
- Length: 600-800 words per section
- Style: Technical but accessible, use examples
- Format: Markdown with code examples

Success means:
- All dependency types covered (hard, soft, none)
- Critical path calculation explained with formula
- Optimization strategies include specific techniques
- Examples demonstrate each concept

Use/Reference:
- Project management best practices
- Task scheduling algorithms
- skill-builder patterns for reference organization
```

→ **Output**: Clear task definition with measurable criteria

→ **Next**: Structure the prompt effectively

### Step 3: Structure Prompt

Organize the prompt using proven templates and patterns.

**Core Prompt Structure**:

```markdown
[CONTEXT SETTING]
[TASK DEFINITION]
[CONSTRAINTS & REQUIREMENTS]
[OUTPUT FORMAT]
[EXAMPLES (if needed)]
[VALIDATION CRITERIA]
```

**1. Context Setting** (1-3 sentences)

Establish the situation and frame the task:
- What role is Claude playing?
- What's the broader goal?
- Why is this task needed?

Example:
```markdown
You are creating a reference guide for a Claude Code skill. This guide will be
loaded on-demand when users need detailed information about dependency management.
The guide should be comprehensive yet practical.
```

**2. Task Definition** (From Step 2)

State exactly what to do:

Example:
```markdown
Write a dependency management guide covering: identification, documentation,
critical path analysis, and optimization strategies.
```

**3. Constraints & Requirements**

List all limitations and requirements:

Example:
```markdown
Requirements:
- 4 main sections: Identification, Documentation, Analysis, Optimization
- 600-800 words per section
- Include code examples and formulas
- Use markdown formatting with headers, lists, code blocks
- Technical but accessible language

Constraints:
- No external dependencies or libraries
- Must work with generic task structures
- Examples should be realistic but not project-specific
```

**4. Output Format**

Specify exact structure expected:

Example:
```markdown
Format:
# Dependency Management Guide

## 1. Identifying Dependencies
[Content with examples]

## 2. Documenting Dependencies
[Content with templates]

## 3. Critical Path Analysis
[Content with formulas]

## 4. Optimization Strategies
[Content with techniques]
```

**5. Examples** (if helpful)

Provide patterns to follow:

Example:
```markdown
Example dependency documentation:
```
Task 5: Write API integration (3h)
  Depends on: Task 2 (auth complete), Task 3 (models defined)
  Type: Hard (blocking)
  Rationale: Cannot call API without authentication and data models
```
```

**6. Validation Criteria**

How to verify success:

Example:
```markdown
Verify the guide:
- [ ] All 4 sections present and complete
- [ ] Each section 600-800 words
- [ ] Code examples in each section
- [ ] Critical path formula included
- [ ] Practical optimization techniques provided
- [ ] Markdown formatting correct
```

**Template Selection Guide**:

**Workflow Step Prompt**:
```markdown
## Step [N]: [Action Name]

[Step description and purpose]

**What to Do**:
[Detailed instructions]

**Inputs**: [What's available from previous steps]
**Outputs**: [What this step produces]
**Next**: [Where to go next]
```

**Task Operation Prompt**:
```markdown
## Operation [N]: [Operation Name]

[Operation description]

**When to Use**: [Trigger conditions]
**Prerequisites**: [What's needed]
**Steps**: [How to execute]
**Validation**: [How to verify success]
```

**Analysis Prompt**:
```markdown
Analyze [object] to [goal].

Context:
[Relevant background]

Analysis dimensions:
1. [Aspect 1]: [What to examine]
2. [Aspect 2]: [What to examine]
3. [Aspect 3]: [What to examine]

Output format:
[Structure of analysis]

Provide specific examples and evidence for each dimension.
```

**Creation Prompt**:
```markdown
Create [object] that [criteria].

Specifications:
- [Requirement 1]
- [Requirement 2]
- [Requirement 3]

Structure:
[Format/organization]

Example: [Pattern to follow]

Validation: [Success criteria]
```

→ **Output**: Structured prompt following template

→ **Next**: Add context and examples

### Step 4: Add Context & Examples

Enhance the prompt with necessary background and patterns.

**Types of Context to Add**:

**1. Background Information**

Provide essential knowledge:
- Technical concepts Claude should understand
- Domain-specific terminology
- Related patterns or principles
- Historical context (why this way?)

Example:
```markdown
Background: Critical path is the longest sequence of dependent tasks
determining minimum project duration. Tasks on the critical path have
zero slack - any delay extends the project. Non-critical tasks have
slack and can be delayed without affecting completion.
```

**2. Reference Materials**

Point to existing resources:
- Templates to follow
- Previous examples
- Style guides
- Technical specifications

Example:
```markdown
Reference: See examples/medirecords-integration/ for a similar two-phase
workflow pattern. Follow the same structure of planning phase → implementation
phase with validation steps between.
```

**3. Constraints & Boundaries**

Define what NOT to do:
- Scope limitations
- Excluded options
- Anti-patterns to avoid
- Error conditions

Example:
```markdown
Do NOT:
- Include project-specific details
- Assume external tools/libraries
- Use placeholders like "TODO" or "FILL IN"
- Skip validation steps
- Create files outside specified directory
```

**4. Examples & Patterns**

Show concrete instances:

**Good Examples** - What success looks like:
```markdown
Example of good dependency documentation:

Task 7: Implement error handling (2h)
  Depends on: Task 5 (API integration complete)
  Type: Hard (must handle API errors)
  Impact: Blocks Task 9 (testing), Task 10 (deployment)
  Critical path: Yes (on critical path)
  Rationale: Cannot test or deploy without proper error handling
```

**Bad Examples** - Common mistakes:
```markdown
Example of poor dependency documentation (DON'T DO THIS):

Task 7: Error stuff (2h)
  Depends on: Maybe task 5?

This is vague, unclear type, no rationale, doesn't help scheduling.
```

**Before/After** - Improvements:
```markdown
Before: "Update the database code"
After: "Refactor database query functions to use parameterized queries
preventing SQL injection, add connection pooling for performance, and
implement retry logic for transient failures."
```

**5. Success Patterns**

Describe characteristics of good output:
- Quality indicators
- Completeness checks
- Style markers
- Validation approaches

Example:
```markdown
High-quality dependency analysis includes:
✅ Every task has dependencies listed (even if "none")
✅ Dependency types specified (hard/soft/none)
✅ Rationale explains WHY the dependency exists
✅ Critical path is identified and marked
✅ Parallel opportunities are noted
✅ Risk areas highlighted
```

**Context Organization**:

Place context strategically:
- **Before task**: Background, definitions, principles
- **During task**: Templates, formats, examples to follow
- **After task**: Validation, success criteria, next steps

**Context Amount Guidelines**:

Too little context:
- Claude makes assumptions
- Output varies widely
- Requires follow-up questions

Too much context:
- Overwhelms the task
- Dilutes key requirements
- Slows processing

Right amount:
- Sufficient for reliable execution
- Focused on task-relevant info
- Examples demonstrate patterns
- Validation criteria clear

**Context Checklist**:
- [ ] Background explains WHY
- [ ] Examples show HOW
- [ ] Constraints define boundaries
- [ ] Validation ensures quality
- [ ] References available if needed

→ **Output**: Enhanced prompt with context and examples

→ **Next**: Refine and validate quality

### Step 5: Refine & Validate

Polish the prompt and verify it meets quality standards.

**Refinement Process**:

**1. Clarity Check**

Read through as if you're Claude:
- Is every instruction clear?
- Are terms defined?
- Is the sequence logical?
- Are transitions smooth?

**Clarity Improvements**:
- Replace vague terms with specific ones
- Break long sentences into shorter ones
- Use active voice ("Write X" not "X should be written")
- Add connective words (Then, Next, After, Before)

**2. Completeness Check**

Verify nothing is missing:
- [ ] Context provided?
- [ ] Task clearly defined?
- [ ] All constraints listed?
- [ ] Output format specified?
- [ ] Examples included (if needed)?
- [ ] Validation criteria given?

**3. Specificity Check**

Ensure precision:
- Numbers exact ("15 items" not "several items")
- Formats detailed ("JSON with keys X, Y, Z" not "JSON format")
- Actions specific ("Extract function names" not "Look at the code")
- Criteria measurable ("Under 500 words" not "Brief")

**4. Consistency Check**

Verify alignment:
- Terms used consistently throughout
- Examples match specifications
- Constraints don't contradict
- Validation matches requirements

**5. Conciseness Check**

Remove unnecessary words:
- Eliminate redundancy
- Combine similar points
- Remove filler phrases
- Keep focus tight

Before: "In order to create the file, you should write content that includes..."
After: "Write a file containing..."

**Validation Criteria**:

**Quality Dimensions**:

1. **Clarity** (1-5): Can Claude understand without questions?
   - 5: Crystal clear, no ambiguity
   - 3: Mostly clear, minor confusion possible
   - 1: Vague, requires clarification

2. **Specificity** (1-5): Are requirements precise?
   - 5: All details specified exactly
   - 3: Key details specified, some inference needed
   - 1: High-level only, lots of guessing

3. **Completeness** (1-5): Is everything needed present?
   - 5: All context, examples, criteria included
   - 3: Basics present, some gaps
   - 1: Missing critical information

4. **Actionability** (1-5): Can Claude execute immediately?
   - 5: Ready to execute, no preparation needed
   - 3: Mostly ready, minor prep needed
   - 1: Requires significant additional work

5. **Reliability** (1-5): Will it produce consistent results?
   - 5: Same prompt → same quality output every time
   - 3: Generally consistent, occasional variation
   - 1: Highly variable output

**Target**: All dimensions ≥4 for production prompts

**Validation Questions**:

**Clarity**:
- Could a different person understand this prompt the same way?
- Are there any ambiguous words or phrases?
- Is the sequence of steps logical and clear?

**Specificity**:
- Are all measurements/quantities exact?
- Are formats precisely defined?
- Are examples specific and concrete?

**Completeness**:
- Does Claude have all information needed?
- Are edge cases covered?
- Are validation criteria provided?

**Actionability**:
- Can Claude start immediately?
- Are all dependencies available?
- Is the first action clear?

**Reliability**:
- Would this produce the same output twice?
- Are there subjective terms that vary?
- Are success criteria objective?

**Testing Strategies**:

1. **Dry Run**: Execute mentally step by step
2. **Peer Review**: Have someone else read it
3. **Actual Test**: Try the prompt with Claude
4. **Iteration**: Refine based on results

**Common Issues & Fixes**:

**Issue**: Prompt produces varying output
**Fix**: Add more constraints, specify format exactly, provide examples

**Issue**: Claude asks clarifying questions
**Fix**: Context incomplete, add background information

**Issue**: Output doesn't match expectations
**Fix**: Success criteria unclear, make validation explicit

**Issue**: Prompt too long (>1000 words)
**Fix**: Move details to references, keep core prompt focused

**Issue**: Assumes knowledge Claude doesn't have
**Fix**: Add background section, define terms, provide context

**Final Checklist**:

Before using the prompt:
- [ ] Read aloud - does it flow naturally?
- [ ] Check all dimensions ≥4
- [ ] Verify examples match specs
- [ ] Confirm validation is measurable
- [ ] Test with Claude if possible
- [ ] Document any assumptions

→ **Output**: Refined, validated, production-ready prompt

## Best Practices

### Prompt Engineering Principles

**1. Clarity First**
- Use simple, direct language
- Define technical terms
- Break complex tasks into steps
- Use examples to clarify

**2. Be Specific**
- Exact numbers, not ranges (unless necessary)
- Precise formats, not general descriptions
- Specific actions, not vague requests
- Measurable criteria, not subjective

**3. Provide Context**
- Explain why the task matters
- Give relevant background
- Reference related materials
- Define scope boundaries

**4. Show Examples**
- Good examples (what to emulate)
- Bad examples (what to avoid)
- Before/after (how to improve)
- Edge cases (how to handle)

**5. Enable Validation**
- Measurable success criteria
- Objective quality indicators
- Checkable outputs
- Clear pass/fail

**6. Think Iteratively**
- Start simple, add detail
- Test and refine
- Learn from results
- Improve over time

### Prompt Patterns

**Instruction Pattern**:
```
Do [action] to achieve [goal].
Include [elements].
Follow [format].
```

**Analysis Pattern**:
```
Analyze [object] for [aspects].
Consider [dimensions].
Provide [output type].
```

**Creation Pattern**:
```
Create [object] with [properties].
Use [template/pattern].
Ensure [quality criteria].
```

**Transformation Pattern**:
```
Transform [input] into [output].
Apply [rules/changes].
Maintain [constraints].
```

### Quality Indicators

**High-Quality Prompts**:
- ✅ One clear objective per prompt
- ✅ All constraints explicit
- ✅ Examples demonstrate patterns
- ✅ Validation criteria measurable
- ✅ Context sufficient but not excessive
- ✅ Language precise and unambiguous

**Low-Quality Prompts**:
- ❌ Multiple conflicting objectives
- ❌ Implicit assumptions
- ❌ No examples or validation
- ❌ Vague success criteria
- ❌ Missing context
- ❌ Ambiguous language

## Common Mistakes

### Mistake 1: Vague Task Definition

**Problem**: "Make the code better"
- Subjective, unmeasurable, no direction

**Fix**: "Refactor the authentication module to use async/await, add input validation, and document each function with JSDoc comments"
- Specific changes, clear criteria, measurable

### Mistake 2: Missing Constraints

**Problem**: "Write a guide"
- No length, format, audience specified

**Fix**: "Write a 500-word beginner-friendly guide in markdown format covering installation, basic usage, and first example"
- Length specified, audience clear, format defined

### Mistake 3: No Examples

**Problem**: Instructions only, no patterns shown
- Claude guesses at style/format

**Fix**: Include 2-3 examples demonstrating the pattern
- Claude sees what "good" looks like

### Mistake 4: Unclear Success Criteria

**Problem**: "Create good documentation"
- "Good" is subjective

**Fix**: "Create documentation covering all public APIs, with description, parameters, return values, and usage example for each"
- Objective, checkable, measurable

### Mistake 5: Too Much Context

**Problem**: 2000-word background before 1-sentence task
- Obscures the actual task

**Fix**: Brief context (2-3 sentences), then task, then references to detailed background
- Focused, actionable, with optional depth

### Mistake 6: Assuming Knowledge

**Problem**: "Implement the standard pattern"
- Assumes Claude knows which pattern

**Fix**: "Implement the Repository pattern: create interface IRepository<T>, implement with generic class, use dependency injection"
- Explicit about what "standard pattern" means

## Integration with Other Skills

### With skill-builder-generic

**Use prompt-builder** to create high-quality prompts for skill instructions
- Each workflow step is a prompt
- Each task operation is a prompt
- Reference guides include prompt examples

**Flow**: skill-builder → prompt-builder → improved skills

### With planning-architect

**Use prompt-builder** to create clear prompts in skill plans
- Plan includes example prompts
- Workflow steps defined as prompts
- Validation includes prompt quality

**Flow**: plan skill → build prompts → validate prompts

### With review-multi

**Use prompt-builder** as validation criteria for prompt quality
- Review checks prompt clarity
- Review verifies specificity
- Review ensures validation criteria

**Flow**: create skill → review prompts → refine prompts

## Quick Reference

### The 5-Step Workflow

1. **Understand Context**: Goal, audience, situation, constraints, success
2. **Define Task**: Action verb + object + constraints + criteria
3. **Structure Prompt**: Template + format + organization
4. **Add Context**: Background + examples + boundaries
5. **Refine & Validate**: Clarity + completeness + specificity + test

### Quality Checklist

- [ ] Clear action verb and specific object
- [ ] All constraints explicitly listed
- [ ] Success criteria measurable
- [ ] Context provides necessary background
- [ ] Examples demonstrate patterns
- [ ] Format/structure specified
- [ ] Validation criteria included
- [ ] Language precise and unambiguous
- [ ] All dimensions score ≥4
- [ ] Tested (if possible)

### Key Principles

- **Clarity First**: Simple, direct, unambiguous
- **Be Specific**: Exact requirements, precise criteria
- **Provide Context**: Background, examples, boundaries
- **Enable Validation**: Measurable, objective, checkable

---

For detailed guides on prompt engineering principles, templates, and examples, see the references/ directory.

For automated prompt validation, use scripts/validate-prompt.py.
