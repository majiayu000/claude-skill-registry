---
name: explain
description: Explain how code, a feature, or system works
argument-hint: [file, function or feature]
---

# Explain

Provide a clear explanation of how something in the codebase works.

## Instructions

1. **Identify what to explain**: Use `$ARGUMENTS` to determine the target

   - File path → explain that file's purpose and how it works
   - Function/class name → find and explain that specific code
   - Feature name → trace through the codebase to explain the feature end-to-end

2. **Gather context**

   - Read the relevant code
   - Identify dependencies and relationships
   - Look at how it's used (callers, imports)
   - Check for related tests that show intended behavior

3. **Explain clearly**
   - Start with a high-level summary (1-2 sentences)
   - Break down the key components
   - Explain the flow/logic step by step
   - Note any important patterns or design decisions
   - Mention edge cases or gotchas if relevant

## Guidelines

- Adjust depth based on complexity—simple code needs brief explanations
- Use concrete examples from the code when helpful
- Reference specific line numbers for key logic
- If the target is ambiguous, ask for clarification
- Avoid restating code literally; explain the _why_ and _how_
