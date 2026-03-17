---
name: obsidian-qa-saver
description: Save Q&A conversations to Obsidian notes with proper formatting, metadata, and organization. Use this skill when the user explicitly requests to save a conversation, question-answer exchange, or explanation to their Obsidian vault. Automatically formats content as document-style notes with timestamps, tags, and project links.
---

# Obsidian Q&A Saver

Save question-and-answer conversations to Obsidian notes with proper formatting, metadata, and organization.

## When to Use This Skill

Use this skill when the user explicitly requests to:
- Save a conversation or Q&A exchange to Obsidian
- Export an explanation or discussion to their notes
- Document a technical discussion for future reference
- Archive project-related conversations

**Important:** Only trigger this skill when the user explicitly asks to save content to Obsidian. Do not proactively suggest saving unless the conversation clearly warrants documentation.

## Skill Overview

This skill helps capture valuable Q&A exchanges into well-structured Obsidian notes. It:
1. Identifies the Q&A content to save (from current conversation)
2. Extracts and formats the content appropriately
3. Generates metadata (tags, timestamps, project links)
4. Creates a properly formatted Markdown file
5. Saves it to the appropriate location in the Obsidian vault

## How to Use This Skill

### Step 1: Identify Content to Save

Ask the user what they want to save:
- "Which part of our conversation would you like to save?"
- "Should I save the entire conversation or specific Q&A exchanges?"
- "What topic or project is this related to?"

If the user says "save this conversation," determine the relevant portion based on context.

### Step 2: Determine Organization

Ask the user about organization:
- **Topic/Project**: "What topic or project folder should this go in?" (e.g., "Elios Project", "Python Learning")
- **Note Title**: "What would you like to title this note?" (suggest a descriptive title based on content)

Default structure: `{Obsidian Vault}/{Topic or Project}/{Note Title}.md`

### Step 3: Extract and Format Content

Transform the Q&A content into document format:

**From dialogue format:**
```
User: How do I implement dependency injection?
Assistant: Dependency injection is a pattern where...
```

**To document format:**
```markdown
## Implementing Dependency Injection

Dependency injection is a pattern where dependencies are provided to a class rather than created internally...

### Key Concepts

- **Inversion of Control**: The framework controls object creation
- **Loose Coupling**: Classes depend on abstractions, not concrete implementations

### Example Implementation

[Include code examples from the conversation]

### Best Practices

[Extract best practices mentioned]
```

**Formatting Guidelines:**
- Use headers (##, ###) to structure content
- Convert Q&A to narrative sections with clear headings
- Preserve code blocks with proper language tags
- Add bullet points for lists and key concepts
- Include examples and explanations inline
- Remove conversational fillers ("let me", "I'll help you", etc.)
- Make content self-contained and reference-ready

### Step 4: Generate Metadata

Create YAML frontmatter with:

```yaml
---
created: YYYY-MM-DD HH:MM
updated: YYYY-MM-DD HH:MM
tags:
  - tag1
  - tag2
  - project/name
aliases: []
---
```

**Tag Guidelines:**
- Use lowercase, kebab-case tags (e.g., `dependency-injection`, `clean-architecture`)
- Add project tags (e.g., `project/elios`)
- Include technology tags (e.g., `python`, `fastapi`, `architecture`)
- Add concept tags (e.g., `design-patterns`, `best-practices`)

**Project Links:**
Add relevant links at the top of the document:
```markdown
**Related:**
- [[Project Overview]]
- [[Architecture Documentation]]
- [[Implementation Notes]]
```

### Step 5: Create the Note File

Use the `scripts/save_to_obsidian.py` script to save the note:

```bash
python .claude/skills/obsidian-qa-saver/scripts/save_to_obsidian.py \
  --vault-path "/path/to/obsidian/vault" \
  --folder "Topic or Project" \
  --title "Note Title" \
  --content "content.md" \
  --tags "tag1,tag2,tag3"
```

The script will:
1. Create the folder if it doesn't exist
2. Generate the YAML frontmatter
3. Add project links if specified
4. Save the note with proper formatting
5. Return the file path for confirmation

### Step 6: Confirm with User

After saving, confirm:
```
✓ Saved to: /path/to/vault/Topic or Project/Note Title.md

The note includes:
- Formatted Q&A as document-style content
- Tags: #tag1 #tag2 #tag3
- Timestamps: 2025-01-31 14:30
- Project links: [[Related Note 1]], [[Related Note 2]]

You can find it in your Obsidian vault under "Topic or Project" folder.
```

## Script Reference

### `scripts/save_to_obsidian.py`

Python script for saving formatted notes to Obsidian vault.

**Usage:**
```bash
python scripts/save_to_obsidian.py \
  --vault-path "/path/to/vault" \
  --folder "folder/name" \
  --title "Note Title" \
  --content "content.md" \
  --tags "tag1,tag2" \
  --links "[[Link 1]],[[Link 2]]"
```

**Arguments:**
- `--vault-path`: Path to Obsidian vault (required)
- `--folder`: Folder within vault (optional, defaults to root)
- `--title`: Note title (required)
- `--content`: Path to content file or direct content string (required)
- `--tags`: Comma-separated tags (optional)
- `--links`: Comma-separated wiki links for related notes (optional)

**Returns:** File path of created note

## Template Reference

### `assets/obsidian-note-template.md`

Standard template for Obsidian notes created by this skill. The template includes:
- YAML frontmatter structure
- Related links section
- Content placeholder
- Standard formatting

Use this template as a reference when manually formatting notes.

## Best Practices

### Content Transformation

**Do:**
- Transform conversational Q&A into article-style prose
- Use clear, descriptive headers
- Preserve technical accuracy
- Include all code examples with proper formatting
- Make content searchable and reference-ready

**Don't:**
- Keep conversational phrases ("let me help", "I think", etc.)
- Include meta-commentary about the conversation
- Save incomplete or fragmented exchanges
- Duplicate information unnecessarily

### Organization

**Do:**
- Use consistent folder naming (Title Case for projects, lowercase for topics)
- Create meaningful tags that aid discovery
- Link to related notes for context
- Use descriptive note titles

**Don't:**
- Create deeply nested folder structures
- Use generic titles like "Notes" or "Conversation"
- Over-tag (stick to 3-5 relevant tags)
- Save without asking user for preferences

### Metadata

**Do:**
- Always include creation timestamp
- Use consistent tag format (lowercase, kebab-case)
- Add project-specific tags (e.g., `project/elios`)
- Link to related documentation

**Don't:**
- Forget to add tags
- Use inconsistent tag formats
- Skip the YAML frontmatter
- Omit project context

## Example Use Cases

### Use Case 1: Saving Architecture Discussion

**User:** "Save our discussion about Clean Architecture to Obsidian"

**Process:**
1. Ask: "I'll save our Clean Architecture discussion. Should this go in your 'Elios Project' folder or a general 'Architecture' folder?"
2. Extract Q&A about dependency injection, ports & adapters, etc.
3. Format as "Clean Architecture - Ports & Adapters Pattern"
4. Add tags: `#clean-architecture`, `#design-patterns`, `#project/elios`
5. Link to: `[[Architecture Documentation]]`, `[[Project Structure]]`
6. Save and confirm

### Use Case 2: Saving Code Explanation

**User:** "Can you save that explanation about `__init__.py` files?"

**Process:**
1. Ask: "I'll save the `__init__.py` explanation. What project folder should this go in?"
2. Extract explanation with examples
3. Format as "Understanding Python __init__.py Files"
4. Add tags: `#python`, `#modules`, `#fundamentals`
5. Include all code examples with syntax highlighting
6. Save and confirm

### Use Case 3: Saving Setup Instructions

**User:** "Export the setup steps to my notes"

**Process:**
1. Ask: "I'll save the setup instructions. What should I title this note?"
2. Extract step-by-step instructions
3. Format as numbered list with code blocks
4. Add tags: `#setup`, `#development`, `#project/elios`
5. Link to: `[[README]]`, `[[Configuration Guide]]`
6. Save and confirm

## Error Handling

### Vault Not Found
If the Obsidian vault path doesn't exist:
```
Error: Obsidian vault not found at /path/to/vault

Please provide the correct path to your Obsidian vault.
You can find this in Obsidian: Settings → Files & Links → Vault folder
```

### Folder Creation
If the target folder doesn't exist, create it automatically and inform the user:
```
Created new folder: /path/to/vault/New Topic

Your note has been saved successfully.
```

### File Conflicts
If a note with the same title exists:
```
A note titled "Note Title" already exists in this folder.

Would you like to:
1. Append to existing note
2. Create with timestamp suffix (e.g., "Note Title 2025-01-31")
3. Choose a different title
```

## Integration with Other Skills

This skill works well with:
- **docs-seeker**: Save discovered documentation as notes
- **chrome-devtools**: Save web scraping results or analysis
- **Architecture discussions**: Document design decisions

When used together, these skills enable comprehensive knowledge management in Obsidian.