---
name: share-transcript
description: This skill should be used when the user asks to "share this session", "upload transcript", "create gist", "share conversation", or wants to publish the current Claude Code session as a GitHub Gist.
---

# Share Transcript

Uploads the current Claude Code session to GitHub Gist and adds it to the project's gist index.

## Instructions

### Step 1: Find Current Session File

1. Get the current working directory to identify the project
2. Find the most recent session file for this project:

```bash
# Extract project path from current directory
PROJECT_PATH=$(pwd)
PROJECT_SLUG=$(echo "$PROJECT_PATH" | sed 's/\//-/g')

# Find most recent session file for this project
SESSION_FILE=$(find ~/.claude/projects -path "*${PROJECT_SLUG}*" -name "*.jsonl" -type f -printf "%T@ %p\n" 2>/dev/null | sort -rn | head -1 | awk '{print $2}')

# Verify file exists
if [ -z "$SESSION_FILE" ]; then
  echo "Error: No session file found for this project"
  exit 1
fi

echo "Found session: $SESSION_FILE"
```

### Step 2: Upload to GitHub Gist

Run the claude-code-transcripts tool:

```bash
claude-code-transcripts json --gist "$SESSION_FILE"
```

This will output something like:
```
Generated page-001.html
Generated page-002.html
Generated /tmp/claude-session-<id>/index.html (13 prompts, 3 pages)
Creating GitHub gist...
Gist: https://gist.github.com/username/gist-id
Preview: https://gisthost.github.io/?gist-id/index.html
```

### Step 3: Parse Output

Extract the two URLs from the output:
- Look for line starting with "Gist: " to get the gist URL
- Look for line starting with "Preview: " to get the preview URL

### Step 4: Get Description from User

Use AskUserQuestion to ask the user for:

**Question**: "What's a brief description for this session?"

**Options**:
- "Feature planning session"
- "Implementation work"
- "Debugging session"
- "Architecture discussion"

Allow custom text input via "Other" option.

Also ask for the feature number if relevant (optional).

### Step 5: Update gist-list.md

1. Check if `aidocs/gist-list.md` exists in the current project
2. Get current date in YYYY-MM-DD format
3. Create the new entry:

```markdown
- **{description}** ({date})
  - Gist: {gist-url}
  - Preview: {preview-url}
```

4. Append to the file (after the `---` separator and any existing entries)

### Step 6: Confirm Completion

Display:
- ✅ Gist created successfully
- The preview URL (as a clickable link if possible)
- ✅ Added to aidocs/gist-list.md
- Suggested next action: "Share the preview URL with your team"

## Error Handling

**If session file not found**:
```
❌ Error: Could not find session file for this project

The session may not have been saved yet, or this directory may not be a Claude Code project.

Try running a command first to ensure a session exists.
```

**If gist upload fails**:
```
❌ Error: Failed to upload gist

Verify GitHub authentication:
  gh auth status
  gh auth login

Then retry: /share-transcript
```

**If gist-list.md doesn't exist**:
Create it with the header:
```markdown
# Claude Code Session Gists

Shareable links to notable Claude Code sessions for this project.

---
```

## Example Output

```
Finding current session...
✓ Found: ~/.claude/projects/-home-cip-src-giant-computer-aegis/af4d62e3.jsonl

Uploading to GitHub Gist...
✓ Generated 3 pages (13 prompts)
✓ Gist created: https://gist.github.com/ianphil/ef6f4483dc1dda8e8865b629e143752f

[User provides description: "Feature 001 MCP Integration - Planning & Work Plan Setup"]

✓ Added to aidocs/gist-list.md

Preview URL: https://gisthost.github.io/?ef6f4483dc1dda8e8865b629e143752f/index.html

Share this URL with your team!
```

## Notes

- Always append to gist-list.md, never overwrite
- Keep descriptions concise (under 80 characters)
- Include feature number if applicable
- Use current date in YYYY-MM-DD format
- Preview URL is the one to share (more readable than raw gist)
