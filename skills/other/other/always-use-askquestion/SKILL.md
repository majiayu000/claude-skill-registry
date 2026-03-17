---
name: always-use-askquestion
description: Forces the agent to always use the AskQuestion tool for user prompts instead of conversational questions. Apply this whenever asking the user anything - questions, confirmations, choices, or clarifications. Never ask conversational questions when structured options are possible.
---

# Always Use AskQuestion

**CRITICAL RULE**: Whenever you need input from the user, **ALWAYS use the AskQuestion tool**. Never ask conversational questions when you can present structured options.

## When to Use AskQuestion

Use AskQuestion for **ALL** of these situations:

- **Yes/No questions**: "Should I proceed?" "Does this look good?"
- **Multiple choice**: "Which option would you like?" "Select a file"
- **Confirmations**: "Ready to commit?" "Create PR now?"
- **Selections**: "Which branch?" "Pick a component"
- **Preferences**: "How should I handle this?" "What format?"

## ⚠️ COMMON MISTAKE: Don't Batch Multiple Questions Into One String

The most common error is cramming multiple distinct questions into a single prompt string:

❌ **WRONG**:

```
prompt: "I need several things:
1. What should I build?
2. Should I search the codebase?
3. Should I search online?"
```

✅ **CORRECT** - Use separate AskQuestion calls or separate question objects:

```
Questions:
  - id: "requirements", prompt: "Ready to provide requirements?", options: [...]
  - id: "search_codebase", prompt: "Should I search the codebase?", options: [...]
  - id: "search_online", prompt: "Should I search online?", options: [...]
```

Or if questions are sequential (one depends on the previous answer), use separate AskQuestion tool calls.

## Never Use Conversational Questions

❌ **BAD** (conversational):

```
Should I proceed with the changes?
```

✅ **GOOD** (AskQuestion):

```json
AskQuestion({
  "title": "Confirm Changes",
  "questions": [{
    "id": "proceed",
    "prompt": "Should I proceed with the changes?",
    "options": [
      {"id": "yes", "label": "Yes, proceed"},
      {"id": "no", "label": "No, cancel"}
    ]
  }]
})
```

## AskQuestion Structure

Every AskQuestion call must include:

1. **title**: Short header for the dialog (2-5 words)
2. **questions**: Array with at least one question object
   - **id**: Unique identifier for this question
   - **prompt**: The question text to display
   - **options**: Array of at least 2 choices
     - **id**: Unique identifier for this option
     - **label**: Display text for this option
   - **allow_multiple** (optional): Set to `true` for multi-select

## When to Use Multiple Questions vs Separate Calls

**Use multiple question objects in ONE AskQuestion call when:**

- Questions are independent (one doesn't depend on the other)
- User can answer all at once
- Example: "Which file format?" AND "Which location?" (both can be answered together)

**Use SEPARATE AskQuestion calls when:**

- Questions are sequential (one depends on the previous answer)
- Need to show results/context between questions
- Example: "Ready to start?" → (if yes) → "Which option?" → (based on option) → "Confirm?"

## CRITICAL: Each Question Must Be Its Own Object

❌ **WRONG** - Multiple questions crammed into one prompt string:

```
AskQuestion({
  "title": "Initial Information",
  "questions": [
    {
      "id": "info",
      "prompt": "Let me gather information:
        1. Requirements: What needs to be built?
        2. Should I search the codebase?
        3. Should I search online?",
      "options": [
        {"id": "proceed", "label": "I'll provide requirements now"},
        {"id": "abort", "label": "Cancel"}
      ]
    }
  ]
})
```

✅ **CORRECT** - Each question is a separate object in the questions array:

```
AskQuestion({
  "title": "Initial Information",
  "questions": [
    {
      "id": "requirements",
      "prompt": "What needs to be built/fixed/cleaned up?",
      "options": [
        {"id": "provide", "label": "Let me describe the requirements"},
        {"id": "skip", "label": "Skip to next question"}
      ]
    },
    {
      "id": "search_codebase",
      "prompt": "Should I search the codebase for relevant patterns?",
      "options": [
        {"id": "yes", "label": "Yes, search the codebase"},
        {"id": "no", "label": "No, skip"}
      ]
    },
    {
      "id": "search_online",
      "prompt": "Should I search online for established patterns/solutions?",
      "options": [
        {"id": "yes", "label": "Yes, search online"},
        {"id": "no", "label": "No, skip"}
      ]
    }
  ]
})
```

**Or for sequential questions, use separate AskQuestion calls:**

```
Step 1: AskQuestion({
  "title": "Start",
  "questions": [{
    "id": "start",
    "prompt": "Ready to provide requirements?",
    "options": [
      {"id": "proceed", "label": "Yes, I'll provide requirements now"},
      {"id": "abort", "label": "Cancel"}
    ]
  }]
})

Step 2: If proceed, ask conversationally for requirements

Step 3: AskQuestion({
  "title": "Research Options",
  "questions": [{
    "id": "research",
    "prompt": "Should I research before identifying tickets?",
    "options": [
      {"id": "both", "label": "Search codebase AND online"},
      {"id": "codebase", "label": "Search codebase only"},
      {"id": "online", "label": "Search online only"},
      {"id": "skip", "label": "Skip research"}
    ]
  }]
})
```

## Common Patterns

### Yes/No Question

```json
AskQuestion({
  "title": "Confirm Action",
  "questions": [{
    "id": "proceed",
    "prompt": "Would you like to proceed?",
    "options": [
      {"id": "yes", "label": "Yes"},
      {"id": "no", "label": "No"}
    ]
  }]
})
```

### Multiple Choice

```json
AskQuestion({
  "title": "Select Option",
  "questions": [{
    "id": "approach",
    "prompt": "Which approach would you prefer?",
    "options": [
      {"id": "option1", "label": "Option 1: Fast but basic"},
      {"id": "option2", "label": "Option 2: Slower but comprehensive"},
      {"id": "option3", "label": "Option 3: Custom (I'll specify)"}
    ]
  }]
})
```

### With Context in Question

```json
AskQuestion({
  "title": "Lint Errors Found",
  "questions": [{
    "id": "lint",
    "prompt": "Found 3 lint errors in the code:\n\n- Line 45: unused variable\n- Line 67: missing semicolon\n- Line 89: indentation\n\nHow would you like to proceed?",
    "options": [
      {"id": "fix", "label": "Fix automatically"},
      {"id": "manual", "label": "I'll fix them manually"},
      {"id": "ignore", "label": "Ignore for now"}
    ]
  }]
})
```

### Multiple Questions in One Call

Only use multiple question objects when the questions are truly independent and can be answered together:

```json
AskQuestion({
  "title": "Configuration",
  "questions": [
    {
      "id": "location",
      "prompt": "Where should the file be saved?",
      "options": [
        {"id": "local", "label": "Local directory"},
        {"id": "cloud", "label": "Cloud storage"}
      ]
    },
    {
      "id": "format",
      "prompt": "What format should I use?",
      "options": [
        {"id": "json", "label": "JSON"},
        {"id": "yaml", "label": "YAML"}
      ]
    }
  ]
})
```

**Important**: If one question depends on the answer to another, use separate AskQuestion calls instead.

### Multi-Select

```json
AskQuestion({
  "title": "Select Features",
  "questions": [{
    "id": "features",
    "prompt": "Which features would you like to include?",
    "options": [
      {"id": "auth", "label": "Authentication"},
      {"id": "db", "label": "Database"},
      {"id": "api", "label": "API endpoints"},
      {"id": "tests", "label": "Test suite"}
    ],
    "allow_multiple": true
  }]
})
```

## Converting Conversational to AskQuestion

### Example 1: Simple Confirmation

**Before (conversational)**:

```markdown
Ask the user: "Does this look good?"
```

**After (AskQuestion)**:

```json
AskQuestion({
  "title": "Confirm",
  "questions": [{
    "id": "confirm",
    "prompt": "Does this look good?",
    "options": [
      {"id": "yes", "label": "Yes, looks good"},
      {"id": "no", "label": "No, let me adjust"}
    ]
  }]
})
```

### Example 2: Open-Ended with Follow-Up

**Before (conversational)**:

```markdown
Ask the user for the branch name.
```

**After (AskQuestion + conversational)**:

```json
AskQuestion({
  "title": "Branch Name",
  "questions": [{
    "id": "branch",
    "prompt": "How would you like to specify the branch name?",
    "options": [
      {"id": "provide", "label": "Let me specify it now"},
      {"id": "current", "label": "Use current branch"},
      {"id": "abort", "label": "Cancel"}
    ]
  }]
})
```

If "provide" is selected, then ask conversationally for the branch name.

### Example 3: File Selection

**Before (conversational)**:

```markdown
Ask which files to include.
```

**After (AskQuestion)**:

```json
AskQuestion({
  "title": "Select Files",
  "questions": [{
    "id": "files",
    "prompt": "Which files should I include?",
    "options": [
      {"id": "all", "label": "All changed files"},
      {"id": "staged", "label": "Only staged files"},
      {"id": "specific", "label": "Let me specify files"}
    ]
  }]
})
```

Based on the response, handle accordingly.

## When to Combine with Conversational

Some questions require free-form input (file paths, commit messages, descriptions). In these cases:

1. **Use AskQuestion to ask HOW they want to provide it**
2. **Then use conversational follow-up for the actual input**

Example:

```markdown
**Step 1**: Use AskQuestion to ask if they want to provide a custom message

**Step 2**: If yes, ask conversationally: "What message would you like to use?"
```

## Handling Responses

After calling AskQuestion, you receive the user's selection. Document the mapping:

```markdown
Based on the response:

- "yes" → Proceed with the action
- "no" → Cancel and exit
- "custom" → Ask conversationally for custom input
```

## Critical Rules

1. **Never skip AskQuestion** when you have 2+ clear options to present
2. **Always provide at least 2 options** (even if one is "Cancel" or "Abort")
3. **Use clear, action-oriented labels** ("Yes, proceed" not just "Yes")
4. **Include context in the question text** when needed (show errors, file lists, etc.)
5. **Make titles short** (2-5 words max)
6. **Keep option labels concise** but descriptive

## Anti-Patterns to Avoid

❌ **Batching multiple questions into one prompt string**

```markdown
Questions:

- id: "info", prompt: "I need:
  1. What should I build?
  2. Search codebase?
  3. Search online?", options: [...]
```

**Fix**: Each distinct question should be either a separate AskQuestion call or a separate question object in the questions array.

❌ **Asking conversationally when options are clear**

```markdown
Ask the user if they want to continue.
```

❌ **Single option** (not really a choice)

```markdown
Options:

- id: "ok", label: "OK"
```

❌ **Vague labels**

```markdown
Options:

- id: "1", label: "Option 1"
- id: "2", label: "Option 2"
```

❌ **Too many questions at once** (limit to 2-3 per AskQuestion call unless they're truly independent)

## Examples from Real Skills

### From dev-workflow-prepare-commit

```json
AskQuestion({
  "title": "Unstaged Changes Detected",
  "questions": [{
    "id": "unstaged",
    "prompt": "The following files have unstaged changes: [list]. Are these intentionally left unstaged?",
    "options": [
      {"id": "leave", "label": "Yes, leave them unstaged"},
      {"id": "stage", "label": "No, stage all changes"},
      {"id": "review", "label": "Let me review"}
    ]
  }]
})
```

### From dev-workflow-initialize

```json
AskQuestion({
  "title": "Which Ticket?",
  "questions": [{
    "id": "ticket",
    "prompt": "What Jira ticket would you like to start?",
    "options": [
      {"id": "ticket", "label": "Specify a ticket number (e.g., RETIRE-123)"},
      {"id": "unticketed", "label": "Unticketed work (use RETIRE-1908)"}
    ]
  }]
})
```

### From address-pr-feedback

```json
AskQuestion({
  "title": "Comment 3 of 7 - Next Steps",
  "questions": [{
    "id": "action",
    "prompt": "Here's the proposed fix and draft reply. What would you like to do?",
    "options": [
      {"id": "apply", "label": "Apply the proposed fix"},
      {"id": "post", "label": "Post the reply on GitHub"},
      {"id": "both", "label": "Apply fix AND post reply"},
      {"id": "skip", "label": "Skip this comment"},
      {"id": "adjust", "label": "Let me adjust something"}
    ]
  }]
})
```

## Summary

**Default behavior**: If you're about to ask the user anything, stop and ask yourself:

1. Can I present this as 2+ clear options? → **Use AskQuestion**
2. Do I need free-form input? → **Use AskQuestion to ask HOW, then conversational for the actual input**
3. Is this truly open-ended with no predictable answers? → **Only then use conversational**

**Remember**: AskQuestion provides a better user experience with clear, clickable options instead of having to type responses.
