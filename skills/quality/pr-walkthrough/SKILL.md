---
name: "pr-walkthrough"
description: "Step-by-step PR code walkthrough session"
argument-hint: "[pr-number]"
---

Walks through a PR's changes interactively, explaining one file and one section at a time - like a human would sit and explain their code. Each step requires user to say "next" to continue.

## Optional PR number from user input
"$ARGUMENTS"

### Argument Handling
- If PR number provided: Use specified PR
- If empty: Use PR for current branch (via `gh pr view`)

## Process

### Step 1: Initialize Review Session
Fetch the PR and map all changes into reviewable blocks:

```bash
# Get PR number
if [ -n "$ARGUMENTS" ]; then
  PR_NUM="$ARGUMENTS"
else
  PR_NUM=$(gh pr view --json number --jq '.number' 2>/dev/null)
  if [ -z "$PR_NUM" ]; then
    echo "Error: No PR number provided and current branch has no associated PR"
    exit 1
  fi
fi

# Get PR info
PR_INFO=$(gh pr view "$PR_NUM" --json title,author,url,files)
PR_TITLE=$(echo "$PR_INFO" | jq -r '.title')
PR_URL=$(echo "$PR_INFO" | jq -r '.url')

# Get list of changed files
FILES=$(echo "$PR_INFO" | jq -r '.files[]? | .path')
```

### Step 2: Map All Review Blocks
Create a structured map of all changes to review:

1. **For each changed file:**
   - Get the full diff using `gh pr diff "$PR_NUM" -- "$FILE_PATH"`
   - Parse diff into logical sections (functions, classes, imports, etc.)
   - Identify the nature of each change (new file, modified function, etc.)

2. **Create review structure:**
   ```
   File 1: path/to/file.py
     - Section 1.1: New imports (lines X-Y)
     - Section 1.2: Modified function_name() (lines A-B)
     - Section 1.3: New class ClassName (lines C-D)
   File 2: path/to/other.py
     - Section 2.1: ...
   ...
   ```

3. **Display the map:**
   Show user the complete structure of what will be reviewed, like a table of contents

### Step 3: Interactive Walkthrough
For each section in order:

1. **Display current context:**
   ```
   📍 Currently reviewing: File X/Y - Section A/B
   File: path/to/file.py
   Section: Modified function_name() (lines 42-58)
   ```

2. **Explain at high level:**
   - What this section does (1-2 sentences)
   - Why this change was needed
   - How it fits into the PR's overall goal
   - Note any important details that will be covered later

3. **Show the actual code change:**
   - Display the relevant diff section
   - Highlight key parts without going into deep details yet

4. **Wait for user:**
   - Explicitly state: "Type 'next' when ready to continue, or ask questions about this section"
   - DO NOT proceed until user says "next" or asks a clarifying question
   - If user asks questions, answer them in depth before moving on

5. **Handle user input:**
   - If user says "next": Move to next section
   - If user asks "why...": Explain the reasoning in depth
   - If user asks "how...": Explain the implementation details
   - If user asks "what if...": Discuss edge cases and alternatives
   - If user says "back": Go to previous section
   - If user says "skip file": Jump to next file

### Step 4: File Transitions
When finishing a file:
1. Provide a brief summary of what changed in that file
2. Explain how it connects to the next file (if relevant)
3. Show progress: "Completed file X/Y"
4. Wait for "next" before starting the next file

### Step 5: Review Complete
When all sections are reviewed:
1. Provide a high-level summary of all changes
2. Highlight the key takeaways
3. Ask if user wants to revisit any specific sections

## Important Notes

- **Never auto-proceed**: Always wait for explicit "next" command
- **One section at a time**: Never explain multiple sections at once
- **High-level first**: Save implementation details for when user asks
- **Be conversational**: Explain like you're pair programming
- **Track state**: Remember which section we're on throughout the conversation
- **Handle questions**: When user asks questions, go deeper on that specific topic
