---
name: start-feature
description: "Start a feature specification directly, skipping formal discussion documentation. For adding features to existing projects where you already know what you're building."
disable-model-invocation: true
---

Invoke the **technical-specification** skill for this conversation with inline feature context.

## Instructions

Follow these steps EXACTLY as written. Do not skip steps or combine them.

This skill is for **feature mode** - a streamlined path to specification when you already know what you're building and don't need formal discussion documentation.

## Step 1: Gather Feature Context

Ask the user these questions (can be combined into one prompt):

1. **What feature are you adding?**
   - Brief description of what you're building

2. **What's the scope?**
   - Core functionality to implement
   - Edge cases you're already aware of

3. **Any constraints or integration points?**
   - How this integrates with existing code
   - Technical decisions already made
   - Conventions to follow

**Note**: If the user has already provided this context in their initial message, don't ask again - acknowledge what they've shared and proceed.

## Step 2: Suggest a Topic Name

Based on the feature description, suggest a topic name for the specification file:

```
Based on what you've described, I'd suggest the topic name: {suggested-topic}

This will create: docs/workflow/specification/{suggested-topic}.md

Is this name okay, or would you prefer something else?
```

## Step 3: Check for Existing Specifications

Look in `docs/workflow/specification/` for naming conflicts:

```bash
ls docs/workflow/specification/
```

If a specification with the same name exists, inform the user and ask how to proceed:
- Append to existing specification
- Choose a different name
- Replace existing specification

## Step 4: Invoke Specification Skill

Pass the gathered context to the [technical-specification](../technical-specification/SKILL.md) skill:

```
Feature specification for: {topic}

## Feature Context (from user)

{paste the gathered feature description, scope, and constraints}

---

Begin specification building using the technical-specification skill.

This is feature mode - there is no discussion document to reference.
Work from the inline context provided above.
```

## Notes

- The specification skill contains instructions for synthesizing the inline context, presenting it for validation, and building the specification
- Output is a standard specification file at `docs/workflow/specification/{topic}.md`
- From there, the user can proceed to `/start-planning` as normal
- This path skips formal discussion documentation - use the full workflow for complex features that need debate captured
