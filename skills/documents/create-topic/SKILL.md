---
name: ccn:create-topic
description: Create a new topic file in .notes/ with frontmatter template
disable-model-invocation: true
argument-hint: [topic-name]
---

# Create Topic Skill

This skill creates a new topic file in the `.notes/` directory with structured frontmatter and section headers.

## Instructions for Claude

When this command is invoked with `/ccn:create-topic $ARGUMENTS`:

### Step 1: Validate argument

If `$ARGUMENTS` is empty or not provided:
- Show error: "Error: Topic name required"
- Show usage: "Usage: /ccn:create-topic <topic-name>"
- STOP - do not continue

### Step 2: Normalize topic name to filename

Take the provided topic name and transform it:
1. Replace all spaces with underscores
2. Replace all hyphens with underscores
3. Convert to UPPERCASE
4. Add `.md` extension

Examples:
- "api-design" → "API_DESIGN.md"
- "my topic" → "MY_TOPIC.md"
- "error_handling" → "ERROR_HANDLING.md"

Store the result as the filename.

### Step 3: Check if file exists

Use the **Read** tool to check if `.notes/{filename}` already exists.

- If the file EXISTS:
  - Tell user: "Error: Topic already exists: .notes/{filename}"
  - Tell user: "Use /ccn:update-topic to add entries to this topic"
  - STOP - do not continue

- If the file DOES NOT exist:
  - Continue to next step

### Step 4: Create .notes/ directory if needed

Use the **Bash** tool to ensure the directory exists:
```bash
mkdir -p .notes
```

### Step 5: Generate frontmatter

Create YAML frontmatter with these fields:

1. **description**: "Knowledge and patterns for {original topic name}"
   - Use the original input, not the normalized filename
   - Example: input "api-design" → "Knowledge and patterns for api-design"

2. **keywords**: Generate array from normalized filename
   - Split filename (without .md) on underscores
   - Lowercase each part
   - Include the combined form (full filename without .md, lowercased)
   - Example: "API_DESIGN.md" → `["api", "design", "api_design"]`

3. **last_updated**: Today's date in YYYY-MM-DD format

### Step 6: Create file with template

Use the **Write** tool to create `.notes/{filename}` with this structure:

```markdown
---
description: "Knowledge and patterns for {topic}"
keywords: [{keyword array}]
last_updated: "YYYY-MM-DD"
---

# {Topic Name}

## Overview

(Add overview content here)

## Key Concepts

(Document key concepts here)

## Patterns

(Capture recurring patterns here)

## Notes

(Add detailed notes here)

---

*Topic created: YYYY-MM-DD*
```

**Important formatting notes:**
- Use the original topic name (not normalized) for the H1 heading
- Use proper YAML array syntax for keywords
- Include the footer timestamp at the bottom

### Step 7: Confirm completion

Tell the user: "Created: .notes/{filename}"

## Error Handling

If any tool fails (mkdir, Read, Write):
- Show the error message
- Explain what went wrong
- Do NOT create partial files
