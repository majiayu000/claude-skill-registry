---
name: extract-prompt
description: Turn successful interactions into reusable prompts
disable-model-invocation: true
---

# Extract Reusable Prompt from Conversation

Analyze this conversation and extract a reusable prompt that captures the successful pattern.

## Process

### Step 1: Analyze the Conversation

Review the entire conversation and identify:

**What was the goal?**
- What were we trying to accomplish?
- What problem were we solving?

**What made it successful?**
- What specific instructions led to good results?
- What constraints or guidelines were important?
- What structure or process did we follow?

**What was the key pattern?**
- Can this be generalized beyond this specific case?
- What made this approach effective?
- What would need to change for different contexts?

### Step 2: Extract the Pattern

Identify the core pattern:

**The problem it solves:**
[General class of problems this addresses]

**The approach:**
[The method or structure that worked]

**Critical elements:**
- [Key instruction 1 that made it work]
- [Key instruction 2]
- [Key constraint or guideline]

**Optional elements:**
- [Things that helped but aren't essential]

### Step 3: Generalize the Instructions

Convert the specific conversation into general instructions:

**From specific:**
"Read src/auth/oauth.ts and explain how it works"

**To general:**
"Read [FILE] and explain how it works"

**From specific:**
"Don't suggest improvements to the authentication system"

**To general:**
"Document what exists without suggesting improvements"

### Step 4: Structure the Prompt

Create a structured prompt document following the template:

```markdown
---
title: [Descriptive Title]
type: prompt
tags: [tag1, tag2, tag3]
tools: [applicable-tools]
status: draft
created: [YYYY-MM-DD]
version: 1.0.0
related: []
source: extracted-from-conversation
---

# [Title]

## Applicability

[When is this prompt appropriate? What problems does it solve?]

**Critical for:**
- [Use case 1]
- [Use case 2]

**Do NOT use for:**
- [Anti-pattern 1]
- [Anti-pattern 2]

## The Prompt

\```
[The actual prompt text, generalized and structured]

[Include key sections like:]

## Critical Rules

[Non-negotiable guidelines]

## Process

[Step-by-step workflow if applicable]

### Step 1: [Name]
[Instructions]

### Step 2: [Name]
[Instructions]

## Guidelines

[Best practices and recommendations]
\```

## Usage Scenario

**Context:**
[Describe a concrete scenario]

**Input:**
\```
[What you would actually say to the AI]
\```

**Expected Output:**
\```
[What the AI should produce]
\```

## Success Criteria

[What success looks like]
- [Expected outcome 1]
- [Expected outcome 2]

## Variations

[Different versions for different contexts]

## Related Links

[Links to sources or related information]

## Additional Context

[Caveats or tips]

## Changelog

- 1.0.0 ([YYYY-MM-DD]): Initial extraction from conversation
```

### Step 5: Provide Context from This Conversation

Include specific details:

**What we did:**
[Summary of this specific conversation]

**What worked well:**
[Specific things that led to success]

**What could be generalized:**
[Parts that apply to similar situations]

**Example from this conversation:**
[Use this conversation as the example in the prompt]

### Step 6: Determine Filename

Following naming conventions:

**For workflows (multi-step):**
`prompt-workflow-[descriptive-slug].md`

**For tasks (single focused task):**
`prompt-task-[descriptive-slug].md`

**For system prompts:**
`prompt-system-[descriptive-slug].md`

### Step 7: Classify and Tag

**Type:** prompt
**Status:** draft (needs testing)
**Tags:** [Extract 3-5 relevant tags]
**Tools:** [Which tools would this work with?]

### Step 8: Present Draft

```
I've extracted a reusable prompt from our conversation.

**Pattern identified:** [Name of pattern]

**Key insight:** [What made this work]

**Proposed filename:** content/prompt-[type]-[slug].md

**Draft prompt:**
[Show the structured prompt document]

This prompt could be useful for [use cases].

Shall I:
1. Save this prompt to the content/ directory
2. Make adjustments first
3. Test it in a new conversation
```

## Guidelines

1. **Generalize without losing specificity** - Keep concrete examples but make instructions general
2. **Capture the "why"** - Don't just transcribe, explain what made it work
3. **Include anti-patterns** - Document when NOT to use it
4. **Provide examples** - Use this conversation as a concrete example
5. **Start with "draft" status** - Needs testing before "tested" or "verified"
6. **Cross-reference** - Link to related prompts
7. **Iterate** - First version doesn't have to be perfect
