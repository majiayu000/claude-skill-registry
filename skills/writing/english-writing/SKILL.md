---
name: english-writing
description: English writing rules for all generated content and code. Trigger: When generating, editing, or reviewing any content, code, documentation, or prompts.
---

# English Writing

## Overview

This skill enforces clear, consistent, and professional English in all generated content, code comments, documentation, and prompts. It ensures that all outputs meet the project's language and style standards.

## Objective

Guarantee that all written output is in English and follows best practices for clarity, directness, and technical accuracy.

## When to Use

- When generating or editing code, documentation, prompts, or reference material
- When reviewing or validating any written output

**Don't use when:**

- Translating to other languages (unless explicitly requested)

## Critical Patterns

### ✅ REQUIRED: All content in English (American spelling)

All generated code, documentation, comments, and prompt content must be written in English, using American spelling.

### ✅ REQUIRED: ASCII apostrophes and hyphens

Use only ASCII apostrophes (') and hyphens (-) in all written content, code, and documentation.

```markdown
# CORRECT

Don't use smart quotes or typographic dashes -- use ' and - only.

# WRONG

Don’t use “smart quotes” or – en dashes.
```

### ✅ REQUIRED: Consistent punctuation, spacing, and capitalization

Ensure all content uses standard punctuation, single spaces after periods, and consistent capitalization for headings, lists, and code comments.

```markdown
# CORRECT

// Fetch user data.

## Usage

# WRONG

// fetch user Data .

## usage
```

### ✅ REQUIRED: Clear, direct language

Use clear, direct, and unambiguous language for both AI and human readers. Avoid filler, redundancy, and vague statements.

```markdown
# CORRECT

Return an error if the file is missing.

# WRONG

It might be a good idea to return an error if the file is missing.
```

### ✅ REQUIRED: Active voice

Use active voice for clarity and directness.

```markdown
# CORRECT

Use useState for local state.

# WRONG

useState should be used for local state.
```

### ✅ REQUIRED: Imperative mood

Write instructions in imperative mood.

```markdown
# CORRECT

Add the dependency to package.json.

# WRONG

You should add the dependency to package.json.
```

### ✅ REQUIRED: No hedging

Avoid hedging language ("consider", "might", "could").

```markdown
# CORRECT

Use strict typing for all TypeScript files.

# WRONG

Consider using strict typing for TypeScript files.
```

### ✅ REQUIRED: Minimal direct address

Avoid unnecessary use of "you"; focus on direct, actionable statements.

## Decision Tree

```
Is the content, code, documentation, or prompt in English (American spelling)? → Proceed
Otherwise → Rewrite in English (American spelling)
Are only ASCII apostrophes and hyphens used? → Proceed
Otherwise → Replace with ASCII characters
Is punctuation, spacing, and capitalization consistent? → Proceed
Otherwise → Fix formatting
Is the language clear and direct? → Proceed
Otherwise → Rewrite for clarity
Is the sentence in active voice? → Proceed
Otherwise → Rewrite in active voice
Is the instruction in imperative mood? → Proceed
Otherwise → Rewrite in imperative mood
Is there hedging language? → Remove hedging
Is there unnecessary direct address? → Remove or rephrase
Otherwise → Content is compliant
```

## Conventions

Refer to conventions for:

- General coding standards
- Formatting and structure

## Scope

These rules apply to all generated code, documentation, comments, and prompt content. They do not apply to conversational responses in chat or user-facing explanations unless those are part of generated documentation or code comments.

## Example

```markdown
# CORRECT

Add the dependency to package.json.

# WRONG

You should add the dependency to package.json.
```

## Edge Cases

- If a code example requires a non-English string (e.g., for i18n), clearly comment the exception.

## Resources

- [validation.md](../skill-creation/references/validation.md)
