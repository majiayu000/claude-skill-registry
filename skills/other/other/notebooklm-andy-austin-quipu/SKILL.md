---
name: notebooklm
description: Guide for managing Google NotebookLM from the command line using nlm CLI. Use when the user wants to create notebooks, manage sources, generate audio overviews, or mentions NotebookLM, nlm, notebook management, or research organization.
---

# NotebookLM CLI Guide

This skill helps you interact with Google's NotebookLM from the command line using the nlm CLI tool. Manage notebooks, sources, notes, and generate audio overviews efficiently.

## Quick Start

Basic workflow for using NotebookLM CLI:

1. **Authenticate** - Set up credentials with `nlm auth`
2. **Create notebook** - Start with `nlm create <title>`
3. **Add sources** - Populate with `nlm add <notebook-id> <input>`
4. **Generate content** - Create guides, outlines, or audio with generation commands
5. **Manage notes** - Organize with note commands
6. **Monitor** - Check analytics and source freshness

## What is NotebookLM CLI?

**nlm** is a command-line interface for Google's NotebookLM that enables:

- **Notebook management:** Create, list, and delete research notebooks
- **Source operations:** Add, remove, rename, and refresh content sources
- **Note management:** Create, edit, and organize notes within notebooks
- **Audio generation:** Create and share AI-generated audio overviews
- **Content generation:** Generate guides, outlines, and sections
- **Analytics:** Monitor notebook usage and engagement
- **Batch operations:** Execute multiple commands efficiently

## Authentication

### Initial Setup

Before using nlm commands, authenticate with Google:

```bash
nlm auth
```

This command:
- Opens browser for Google OAuth flow
- Requests NotebookLM API permissions
- Stores credentials securely locally
- Enables subsequent commands

**Re-authentication:**
Run `nlm auth` again if:
- Credentials expire
- Switching Google accounts
- Permission errors occur

## Notebook Commands

### List Notebooks

View all your notebooks:

```bash
nlm list
# or shorthand
nlm ls
```

**Output includes:**
- Notebook ID (for use in other commands)
- Title
- Creation date
- Source count
- Last modified timestamp

**Filtering examples:**
```bash
# List recent notebooks
nlm ls | head -n 10

# Search by title pattern
nlm ls | grep "Research"
```

### Create Notebook

Create a new notebook:

```bash
nlm create "Research Project Title"
```

**Best practices:**
- Use descriptive, searchable titles
- Include project or topic identifiers
- Consider date prefixes for temporal organization: `"2024-Q4: Market Analysis"`

**Returns:**
- Notebook ID (save this for subsequent operations)
- Creation confirmation

**Example workflow:**
```bash
# Create and capture ID
NOTEBOOK_ID=$(nlm create "AI Ethics Research" | grep -oE '[a-f0-9-]{36}')
echo "Created notebook: $NOTEBOOK_ID"
```

### Delete Notebook

Remove a notebook permanently:

```bash
nlm rm <notebook-id>
```

**Warning:** This action is irreversible and deletes:
- All sources in the notebook
- All notes
- Generated content
- Audio overviews

**Safe deletion workflow:**
```bash
# Review before deletion
nlm analytics <notebook-id>
nlm sources <notebook-id>

# Confirm and delete
nlm rm <notebook-id>
```

### Notebook Analytics

View usage statistics:

```bash
nlm analytics <notebook-id>
```

**Metrics include:**
- Total views
- Source interactions
- Note creation count
- Audio overview plays
- Recent activity timestamps
- Engagement trends

**Use cases:**
- Track research progress
- Identify popular content
- Monitor collaboration activity
- Audit notebook usage

## Source Commands

### List Sources

View all sources in a notebook:

```bash
nlm sources <notebook-id>
```

**Output details:**
- Source ID
- Source name/title
- Type (URL, PDF, text, etc.)
- Upload date
- Status (processing, ready, error)
- Word count or size

**Sorting and filtering:**
```bash
# Most recent sources
nlm sources <notebook-id> | head -n 5

# Find specific source type
nlm sources <notebook-id> | grep "PDF"
```

### Add Source

Add content to a notebook:

```bash
nlm add <notebook-id> <input>
```

**Supported input types:**

**URL/webpage:**
```bash
nlm add <notebook-id> "https://example.com/article"
```

**Local file:**
```bash
nlm add <notebook-id> "/path/to/document.pdf"
nlm add <notebook-id> "/path/to/notes.txt"
```

**Text content:**
```bash
nlm add <notebook-id> "Direct text content to add as source"
```

**Multiple sources:**
```bash
# Add multiple URLs
for url in $(cat urls.txt); do
  nlm add <notebook-id> "$url"
  sleep 2  # Rate limiting
done
```

**Supported file formats:**
- PDF documents
- Text files (.txt, .md)
- Word documents (.docx)
- Webpages (URLs)
- Google Docs (share links)

### Remove Source

Delete a source from notebook:

```bash
nlm rm-source <notebook-id> <source-id>
```

**Workflow:**
```bash
# List sources to find ID
nlm sources <notebook-id>

# Remove specific source
nlm rm-source <notebook-id> <source-id>

# Verify removal
nlm sources <notebook-id>
```

**Note:** This does not affect notes or other sources referencing the deleted source.

### Rename Source

Change source display name:

```bash
nlm rename-source <source-id> "New Source Name"
```

**Best practices:**
- Use descriptive names: `"Q3 2024 Financial Report"`
- Include version info: `"API Documentation v2.1"`
- Add context: `"Interview Transcript - Dr. Smith"`

**Example:**
```bash
# Generic URL becomes readable
nlm rename-source <source-id> "McKinsey AI Report 2024"
```

### Refresh Source

Update source content from origin:

```bash
nlm refresh-source <source-id>
```

**Use cases:**
- Update webpage content that changed
- Reload edited Google Docs
- Re-process failed sources

**Note:** Only works for sources with accessible origin URLs (not uploaded files).

### Check Source Freshness

Verify if source content is current:

```bash
nlm check-source <source-id>
```

**Returns:**
- Last update timestamp
- Origin modification date
- Freshness status (current, outdated, unavailable)
- Recommended actions

**Monitoring workflow:**
```bash
# Check all sources in notebook
for source in $(nlm sources <notebook-id> | awk '{print $1}'); do
  nlm check-source $source
done
```

## Note Commands

### List Notes

View all notes in a notebook:

```bash
nlm notes <notebook-id>
```

**Output includes:**
- Note ID
- Title
- Creation date
- Word count
- Last edited timestamp
- Preview snippet

### Create Note

Add a new note to notebook:

```bash
nlm new-note <notebook-id> "Note Title"
```

**Returns:**
- Note ID (for editing)
- Creation confirmation

**Workflow:**
```bash
# Create note and capture ID
NOTE_ID=$(nlm new-note <notebook-id> "Meeting Notes" | grep -oE '[a-f0-9-]{36}')

# Add content immediately
nlm edit-note <notebook-id> $NOTE_ID "Meeting summary content..."
```

### Edit Note

Update note content:

```bash
nlm edit-note <notebook-id> <note-id> "Updated content here"
```

**Content handling:**
- Replaces entire note content
- Use quotes for multi-line content
- Supports markdown formatting

**Examples:**
```bash
# Simple update
nlm edit-note <notebook-id> <note-id> "New findings from research."

# Multi-line with heredoc
nlm edit-note <notebook-id> <note-id> "$(cat <<EOF
# Research Findings

## Key Insights
- Finding 1
- Finding 2

## Next Steps
- Action items here
EOF
)"
```

### Remove Note

Delete a note:

```bash
nlm rm-note <note-id>
```

**Warning:** Permanent deletion - cannot be recovered.

## Audio Commands

### Create Audio Overview

Generate AI audio discussion:

```bash
nlm audio-create <notebook-id> "Instructions for audio generation"
```

**Instructions guide the AI hosts:**
- Focus areas: `"Focus on methodology and findings"`
- Target audience: `"Explain for non-technical audience"`
- Tone: `"Conversational and engaging tone"`
- Length: `"Create 5-minute overview"`
- Emphasis: `"Emphasize practical applications"`

**Examples:**
```bash
# Research summary
nlm audio-create <notebook-id> "Create engaging overview of key findings for general audience"

# Technical deep-dive
nlm audio-create <notebook-id> "Technical analysis of methodologies and data, 10 minutes"

# Comparative analysis
nlm audio-create <notebook-id> "Compare approaches across all sources, highlight differences"
```

**Processing:**
- Generation takes 2-5 minutes
- Check status with `nlm audio-get`
- Receive notification when ready

### Get Audio Overview

Retrieve generated audio:

```bash
nlm audio-get <notebook-id>
```

**Returns:**
- Audio URL (direct download link)
- Duration
- Generation date
- Transcript (if available)
- Status (processing, ready, failed)

**Download workflow:**
```bash
# Get audio URL
AUDIO_URL=$(nlm audio-get <notebook-id> | grep -o 'https://.*\.mp3')

# Download audio
curl -o "notebook-audio.mp3" "$AUDIO_URL"
```

### Delete Audio Overview

Remove generated audio:

```bash
nlm audio-rm <notebook-id>
```

**Use cases:**
- Free up storage
- Remove outdated content before regenerating
- Clear failed generation attempts

**Regeneration workflow:**
```bash
# Remove old audio
nlm audio-rm <notebook-id>

# Generate new with updated instructions
nlm audio-create <notebook-id> "New instructions here"
```

### Share Audio Overview

Get shareable link:

```bash
nlm audio-share <notebook-id>
```

**Returns:**
- Public share URL
- Embed code (optional)
- Expiration info (if applicable)

**Privacy notes:**
- Anyone with link can access
- Does not share notebook sources or notes
- Can be revoked by deleting audio

## Generation Commands

### Generate Notebook Guide

Create comprehensive guide from sources:

```bash
nlm generate-guide <notebook-id>
```

**Output:**
- Structured summary of all sources
- Key themes and concepts
- Important quotes and references
- Suggested reading order
- Knowledge gaps identified

**Use cases:**
- Onboarding to new research area
- Review before deep work
- Share context with collaborators
- Identify information needs

### Generate Content Outline

Create structured outline:

```bash
nlm generate-outline <notebook-id>
```

**Output format:**
- Hierarchical topic structure
- Main themes and subtopics
- Source references per topic
- Suggested organization
- Missing elements

**Applications:**
- Article/paper planning
- Presentation structure
- Research organization
- Content strategy

### Generate New Section

Create focused content section:

```bash
nlm generate-section <notebook-id>
```

**Interactive prompts for:**
- Section topic
- Desired length
- Specific sources to include
- Target audience level
- Output format

**Use cases:**
- Draft article sections
- Create summaries
- Extract specific topics
- Synthesize multiple sources

## Batch Operations

### Execute Multiple Commands

Run commands from file:

```bash
nlm batch <commands-file>
```

**Command file format:**
```text
create "Research Project"
add $NOTEBOOK_ID "https://example.com/article1"
add $NOTEBOOK_ID "https://example.com/article2"
add $NOTEBOOK_ID "/path/to/document.pdf"
generate-guide $NOTEBOOK_ID
audio-create $NOTEBOOK_ID "Create engaging overview"
```

**Best practices:**
- One command per line
- Use variables for IDs
- Include error handling
- Add sleep for rate limiting

**Complex batch example:**
```bash
# batch-commands.txt
create "Market Research Q4 2024"
add $NOTEBOOK_ID "https://reports.example.com/q4"
add $NOTEBOOK_ID "https://analysis.example.com/trends"
add $NOTEBOOK_ID "/data/survey-results.pdf"
new-note $NOTEBOOK_ID "Executive Summary"
generate-outline $NOTEBOOK_ID
audio-create $NOTEBOOK_ID "Focus on key trends and recommendations"
```

**Execution:**
```bash
nlm batch batch-commands.txt
```

## Workflow Patterns

### Research Project Setup

Complete notebook initialization:

```bash
#!/bin/bash

# Create notebook
NOTEBOOK_ID=$(nlm create "Research: AI Ethics 2024" | grep -oE '[a-f0-9-]{36}')
echo "Created notebook: $NOTEBOOK_ID"

# Add primary sources
nlm add $NOTEBOOK_ID "https://arxiv.org/paper1"
nlm add $NOTEBOOK_ID "https://arxiv.org/paper2"
nlm add $NOTEBOOK_ID "/research/literature-review.pdf"

# Create organizational notes
nlm new-note $NOTEBOOK_ID "Research Questions"
nlm new-note $NOTEBOOK_ID "Methodology Notes"
nlm new-note $NOTEBOOK_ID "Key Findings"

# Generate initial guide
nlm generate-guide $NOTEBOOK_ID

echo "Setup complete! Notebook ID: $NOTEBOOK_ID"
```

### Source Management Routine

Regular maintenance workflow:

```bash
#!/bin/bash
NOTEBOOK_ID="your-notebook-id"

# Check source freshness
echo "Checking source freshness..."
for source in $(nlm sources $NOTEBOOK_ID | awk '{print $1}'); do
  nlm check-source $source
done

# Refresh outdated sources
echo "Refreshing outdated sources..."
# (add logic based on check-source output)

# Verify all sources loaded
echo "Source status:"
nlm sources $NOTEBOOK_ID
```

### Audio Generation Pipeline

Complete audio workflow:

```bash
#!/bin/bash
NOTEBOOK_ID="your-notebook-id"

# Remove old audio if exists
nlm audio-rm $NOTEBOOK_ID 2>/dev/null

# Generate new audio
echo "Generating audio overview..."
nlm audio-create $NOTEBOOK_ID "Create engaging 7-minute overview focusing on practical applications for business leaders"

# Wait for completion (check every 30 seconds)
echo "Waiting for audio generation..."
while true; do
  STATUS=$(nlm audio-get $NOTEBOOK_ID | grep "Status")
  if [[ $STATUS == *"ready"* ]]; then
    break
  fi
  sleep 30
done

# Download and share
AUDIO_URL=$(nlm audio-get $NOTEBOOK_ID | grep -o 'https://.*\.mp3')
curl -o "research-overview.mp3" "$AUDIO_URL"

SHARE_LINK=$(nlm audio-share $NOTEBOOK_ID)
echo "Audio ready: $SHARE_LINK"
```

### Content Generation Workflow

Complete content creation:

```bash
#!/bin/bash
NOTEBOOK_ID="your-notebook-id"

# Generate comprehensive guide
echo "Generating notebook guide..."
nlm generate-guide $NOTEBOOK_ID > guide.txt

# Create content outline
echo "Creating outline..."
nlm generate-outline $NOTEBOOK_ID > outline.txt

# Generate individual sections
echo "Generating sections..."
nlm generate-section $NOTEBOOK_ID > section1.txt

# Create summary note
NOTE_ID=$(nlm new-note $NOTEBOOK_ID "Generated Content Summary" | grep -oE '[a-f0-9-]{36}')
nlm edit-note $NOTEBOOK_ID $NOTE_ID "$(cat guide.txt outline.txt)"

echo "Content generation complete!"
```

### Collaborative Research Setup

Prepare notebook for team:

```bash
#!/bin/bash

# Create project notebook
NOTEBOOK_ID=$(nlm create "Team Research: Product Strategy" | grep -oE '[a-f0-9-]{36}')

# Add shared resources
nlm add $NOTEBOOK_ID "https://docs.google.com/shared-doc"
nlm add $NOTEBOOK_ID "https://company.com/market-report"

# Create team notes
nlm new-note $NOTEBOOK_ID "Meeting Notes"
nlm new-note $NOTEBOOK_ID "Action Items"
nlm new-note $NOTEBOOK_ID "Decisions"

# Generate initial materials
nlm generate-guide $NOTEBOOK_ID > team-guide.txt
nlm audio-create $NOTEBOOK_ID "Create onboarding overview for new team members"

# Get share link
AUDIO_SHARE=$(nlm audio-share $NOTEBOOK_ID)
echo "Share audio with team: $AUDIO_SHARE"
echo "Notebook ID for team: $NOTEBOOK_ID"
```

## Best Practices

### Notebook Organization

**Naming conventions:**
- Include project code: `"PROJ-123: Market Analysis"`
- Add dates: `"2024-Q4: Competitive Research"`
- Use tags: `"[AI] [Ethics] Research Compilation"`

**Source management:**
- Rename sources with descriptive titles
- Remove outdated or irrelevant sources
- Check freshness regularly for web sources
- Group related sources with prefixes

**Note structure:**
- Create index note with links
- Use consistent formatting
- Tag notes by category
- Date-stamp entries

### Performance Optimization

**Rate limiting:**
```bash
# Add delays between commands
nlm add $NOTEBOOK_ID "url1"
sleep 2
nlm add $NOTEBOOK_ID "url2"
```

**Batch operations:**
- Group related commands
- Use batch command file
- Handle errors gracefully

**Resource management:**
- Archive completed notebooks
- Delete unused audio overviews
- Remove obsolete sources

### Error Handling

**Common issues:**

**Authentication errors:**
```bash
# Re-authenticate
nlm auth
```

**Rate limit errors:**
```bash
# Add delays
sleep 5
```

**Invalid notebook ID:**
```bash
# Verify ID exists
nlm ls | grep <notebook-id>
```

**Source processing failures:**
```bash
# Check source status
nlm sources <notebook-id>

# Retry failed sources
nlm rm-source <notebook-id> <failed-source-id>
nlm add <notebook-id> <source-input>
```

### Automation Scripts

**Template for automation:**
```bash
#!/bin/bash
set -e  # Exit on error

# Configuration
NOTEBOOK_TITLE="Automated Research $(date +%Y-%m-%d)"
SOURCE_LIST="sources.txt"

# Error handling
trap 'echo "Error on line $LINENO"' ERR

# Create notebook
echo "Creating notebook..."
NOTEBOOK_ID=$(nlm create "$NOTEBOOK_TITLE" | grep -oE '[a-f0-9-]{36}')

# Validate notebook creation
if [ -z "$NOTEBOOK_ID" ]; then
  echo "Failed to create notebook"
  exit 1
fi

# Add sources with error handling
echo "Adding sources..."
while IFS= read -r source; do
  if ! nlm add "$NOTEBOOK_ID" "$source"; then
    echo "Warning: Failed to add source: $source"
  fi
  sleep 2
done < "$SOURCE_LIST"

# Generate content
echo "Generating content..."
nlm generate-guide "$NOTEBOOK_ID"
nlm audio-create "$NOTEBOOK_ID" "Create comprehensive overview"

echo "Complete! Notebook ID: $NOTEBOOK_ID"
```

## Troubleshooting

### Common Issues

**"Authentication failed"**
- Run `nlm auth` to re-authenticate
- Check Google account permissions
- Verify NotebookLM API access

**"Notebook not found"**
- Verify notebook ID with `nlm ls`
- Check for typos in ID
- Ensure notebook not deleted

**"Source processing failed"**
- Check source URL accessibility
- Verify file format supported
- Try re-adding source
- Check file size limits

**"Rate limit exceeded"**
- Add delays between commands
- Use batch operations
- Reduce concurrent requests

**"Audio generation timeout"**
- Normal for large notebooks
- Check status with `nlm audio-get`
- Generation can take 5+ minutes

### Debug Mode

Enable verbose output:

```bash
# Set debug environment variable
export NLM_DEBUG=true

# Run commands with debug info
nlm <command>
```

### Logs and Support

**Check logs:**
```bash
# Location varies by OS
# macOS/Linux: ~/.nlm/logs/
# Windows: %APPDATA%/nlm/logs/

tail -f ~/.nlm/logs/nlm.log
```

**Get help:**
```bash
nlm --help
nlm <command> --help
```

## Advanced Usage

### Scripting Examples

**Bulk notebook creation:**
```bash
#!/bin/bash
# Create multiple project notebooks

PROJECTS=("AI Ethics" "Market Analysis" "Technical Review")

for project in "${PROJECTS[@]}"; do
  NOTEBOOK_ID=$(nlm create "Q4 2024: $project" | grep -oE '[a-f0-9-]{36}')
  echo "$project: $NOTEBOOK_ID" >> notebooks.txt

  # Initialize with template
  nlm new-note "$NOTEBOOK_ID" "Project Overview"
  nlm new-note "$NOTEBOOK_ID" "Resources"
  nlm new-note "$NOTEBOOK_ID" "Tasks"
done
```

**Periodic source refresh:**
```bash
#!/bin/bash
# Refresh all web sources weekly

NOTEBOOK_ID="your-notebook-id"

# Get web sources (filter URLs)
nlm sources $NOTEBOOK_ID | grep "http" | awk '{print $1}' | while read source_id; do
  echo "Refreshing: $source_id"
  nlm refresh-source $source_id
  sleep 5
done
```

**Content export pipeline:**
```bash
#!/bin/bash
# Export all notebook content

NOTEBOOK_ID="your-notebook-id"
OUTPUT_DIR="export-$(date +%Y%m%d)"

mkdir -p "$OUTPUT_DIR"

# Export guide
nlm generate-guide $NOTEBOOK_ID > "$OUTPUT_DIR/guide.md"

# Export outline
nlm generate-outline $NOTEBOOK_ID > "$OUTPUT_DIR/outline.md"

# Export all notes
nlm notes $NOTEBOOK_ID | while read note_id _; do
  nlm edit-note $NOTEBOOK_ID $note_id > "$OUTPUT_DIR/note-$note_id.md" 2>/dev/null || true
done

# Download audio if available
nlm audio-get $NOTEBOOK_ID | grep -o 'https://.*\.mp3' | xargs -I {} curl -o "$OUTPUT_DIR/audio.mp3" {}

echo "Export complete: $OUTPUT_DIR"
```

## Quick Reference

### Essential Commands

```bash
# Setup
nlm auth

# Notebooks
nlm ls                           # List all
nlm create "title"              # Create
nlm rm <id>                     # Delete
nlm analytics <id>              # Stats

# Sources
nlm sources <id>                # List
nlm add <id> <input>           # Add
nlm rm-source <id> <source>    # Remove
nlm rename-source <id> "name"  # Rename
nlm refresh-source <source>    # Refresh
nlm check-source <source>      # Check

# Notes
nlm notes <id>                  # List
nlm new-note <id> "title"      # Create
nlm edit-note <id> <note> "content"  # Edit
nlm rm-note <note>             # Remove

# Audio
nlm audio-create <id> "instructions"  # Create
nlm audio-get <id>              # Get
nlm audio-rm <id>               # Delete
nlm audio-share <id>            # Share

# Generation
nlm generate-guide <id>         # Guide
nlm generate-outline <id>       # Outline
nlm generate-section <id>       # Section

# Batch
nlm batch <file>                # Run commands
```

## Key Principles

1. **Authenticate first** - Run `nlm auth` before any operations
2. **Save notebook IDs** - Store returned IDs for subsequent commands
3. **Descriptive naming** - Use clear, searchable titles for notebooks and sources
4. **Regular maintenance** - Check source freshness and remove outdated content
5. **Rate limiting** - Add delays between batch operations
6. **Error handling** - Check command output and handle failures gracefully
7. **Organize notes** - Structure information consistently across notebooks
8. **Generate content** - Use AI features to synthesize and summarize
9. **Share selectively** - Audio overviews are public when shared
10. **Automate workflows** - Script repetitive tasks for efficiency

## Workflow Summary

When user wants to use NotebookLM CLI:

1. **Verify authentication** - Check credentials with `nlm auth`
2. **Identify operation** - Create, manage, or generate content
3. **Get notebook ID** - List or create notebook as needed
4. **Execute commands** - Run appropriate nlm commands
5. **Handle errors** - Check output and retry if needed
6. **Verify results** - Confirm operations completed successfully
7. **Organize content** - Rename, structure, and maintain sources
8. **Generate insights** - Use AI features for guides, audio, outlines
9. **Share appropriately** - Export or share relevant content
10. **Automate** - Script repetitive workflows for efficiency

Remember: NotebookLM CLI enables powerful research workflows through command-line automation. Combine with bash scripts and automation for maximum productivity.
