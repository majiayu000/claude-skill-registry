---
name: ccn:update-topic
description: Add an entry to an existing topic file in .notes/
disable-model-invocation: true
argument-hint: [topic-name]
---

# Update Topic Skill

This skill adds a timestamped entry to an existing topic file in the `.notes/` directory.

## Instructions for Claude

When this command is invoked with `/ccn:update-topic $ARGUMENTS`:

### Step 1: Validate argument

If `$ARGUMENTS` is empty or not provided:
- Show error: "Error: Topic name required"
- Show usage: "Usage: /ccn:update-topic <topic-name>"
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

Use the **Read** tool to check if `.notes/{filename}` exists.

- If the file DOES NOT exist:
  - Tell user: "Error: Topic not found: .notes/{filename}"
  - Tell user: "Use /ccn:create-topic to create a new topic first"
  - STOP - do not continue

- If the file EXISTS:
  - Continue to next step

### Step 4: Prompt for entry details

Ask the user for entry information:

1. **Entry title**: Ask "What is the title for this entry?"
2. **Entry content**: Ask "What content would you like to add? (You can provide multiple lines)"

Wait for the user to provide both pieces of information before continuing.

### Step 5: Read existing file

Use the **Read** tool to get the complete current content of `.notes/{filename}`.

### Step 6: Parse and update frontmatter

Extract the YAML frontmatter (the content between the first two `---` lines):

1. Parse the frontmatter to preserve existing fields
2. Update the `last_updated` field to today's date (YYYY-MM-DD)
3. Keep all other fields unchanged

### Step 7: Append new entry

Add the new entry to the end of the file with this format:

```markdown
### [YYYY-MM-DD] {entry title}

{entry content}
```

**Formatting notes:**
- Use H3 heading (`###`) for the entry
- Include today's date in square brackets
- Add a blank line between heading and content
- Add blank lines before and after the entry for readability

### Step 8: Write updated file

Use the **Write** tool to write the complete updated content back to `.notes/{filename}`.

The final file structure should be:
1. Updated frontmatter (with new last_updated date)
2. All existing content (unchanged)
3. New entry appended at the end

### Step 9: Confirm completion

Tell the user: "Updated: .notes/{filename}"

## Error Handling

If any tool fails (Read, Write):
- Show the error message
- Explain what went wrong
- Do NOT overwrite files if there's an error parsing content
