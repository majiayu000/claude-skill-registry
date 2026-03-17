---
name: obsidian-note-create
description: |
  Creates well-structured Obsidian notes with proper frontmatter, wikilinks,
  and template adherence. Detects available CLI (official, Yakitrak, or direct
  file write) and uses the best option. Reads vault conventions from CLAUDE.md
  before creating. Activates on "create note", "new note", "add to obsidian",
  or when creating markdown files in an Obsidian vault.
allowed-tools: |
  bash: ls, find, obsidian-cli, obsidian, cat
  file: read, write
---

# Obsidian Note Create

<purpose>
Creating an Obsidian note isn't just writing a markdown file. It's frontmatter
with the right properties, in the right folder, following the right template,
with wikilinks to related notes. Get any of that wrong and the note is an orphan
that doesn't show up in bases, has wrong metadata, or breaks linking conventions.
This skill ensures notes are created correctly every time.
</purpose>

## When To Activate

<triggers>
- User says "create note", "new note", "add note"
- User says "add to obsidian", "save to vault"
- User says "make a note about..."
- Creating a .md file inside a known Obsidian vault
- After granola-sync, research, or any skill that produces note-worthy output
</triggers>

Do NOT trigger for:
- Editing existing notes (just edit them directly)
- Non-Obsidian markdown files
- Files outside a vault

## Instructions

### Step 1: Read Vault Conventions

<conventions>
Before creating anything, check for context:

```bash
# Read vault map
cat "$VAULT_PATH/CLAUDE.md" 2>/dev/null

# If no CLAUDE.md, detect conventions from existing notes
find "$VAULT_PATH" -name "*.md" -maxdepth 2 | head -20
head -20 "$VAULT_PATH"/<some-existing-note>.md  # check frontmatter pattern
```

Extract:
- Folder structure (where does this type of note go?)
- Frontmatter schema (what properties are used?)
- Template for this note type
- Naming convention
- Tag conventions

If no CLAUDE.md exists and vault looks unstructured, suggest running
obsidian-vault-init first.
</conventions>

### Step 2: Determine Note Type and Location

<placement>
Match the note to the right type and folder:

| Content | Type | Typical Folder |
|---------|------|---------------|
| Meeting notes | meeting | Projects/{project}/meetings/ |
| Task/todo list | task | Projects/{project}/ |
| Research/reference | reference | References/ |
| General note | note | Notes/ |
| Daily entry | daily | Daily/ |
| Project overview | project | Projects/{project}/ |
| Quick capture | inbox | Inbox/ |

If unsure, ask. Don't guess the folder.
</placement>

### Step 3: Detect Available CLI

<cli_detect>
Try in order of preference:

```bash
# 1. Official Obsidian CLI (best if available and Obsidian is running)
which obsidian 2>/dev/null && obsidian help 2>/dev/null

# 2. Yakitrak CLI (works without Obsidian running)
which obsidian-cli 2>/dev/null

# 3. Direct file write (always works)
echo "Falling back to direct file write"
```

**Official CLI:**
```bash
obsidian create name="Note Title" content="..." template="Template" silent
```

**Yakitrak CLI:**
```bash
obsidian-cli create "Note Title" --content "..." --vault "VaultName"
```

**Direct file write:**
```bash
# Write directly — works everywhere including WSL
```

Use the best available option. Don't fail just because a CLI isn't installed.
</cli_detect>

### Step 4: Build the Note

<build>
Every note has three parts:

**1. Frontmatter** — YAML properties matching vault schema:
```yaml
---
type: [note type]
created: YYYY-MM-DD
status: draft
tags:
  - [relevant tags]
# Additional properties per note type
---
```

**2. Title and metadata** — Human-readable header:
```markdown
# Note Title

**Created**: YYYY-MM-DD
```

**3. Body** — Content structured per template:
```markdown
## Section

Content with [[wikilinks]] to related notes.
```
</build>

### Step 5: Add Wikilinks

<linking>
Before writing, search for related notes to link:

```bash
# Find related notes by keyword
grep -rl "keyword" "$VAULT_PATH" --include="*.md" | head -10

# Find notes with matching tags
grep -rl "tags:.*keyword" "$VAULT_PATH" --include="*.md" | head -5
```

Add wikilinks to related notes:
- `[[Related Note]]` — link to the note
- `[[Related Note#Specific Heading]]` — link to a section
- `[[Related Note|Display Text]]` — link with custom display text

Don't force links. Only link where genuinely related.
</linking>

### Step 6: Check for Duplicates

<dedup>
Before creating, verify no duplicate exists:

```bash
# Check by filename
find "$VAULT_PATH" -name "*similar-name*" -name "*.md"

# Check by title in frontmatter
grep -rl "# Similar Title" "$VAULT_PATH" --include="*.md"
```

If a similar note exists, ask the user:
- Append to existing note?
- Create new note and link to existing?
- Replace existing note?
</dedup>

### Step 7: Write and Confirm

<write>
Write the note, then confirm:

```markdown
Note created: [[Note Title]]

Location: Notes/note-title.md
Type: note
Links: [[Related Note 1]], [[Related Note 2]]
```

If using CLI, verify it worked:
```bash
obsidian read file="Note Title" 2>/dev/null || cat "$VAULT_PATH/Notes/note-title.md"
```
</write>

## Filename Convention

```
kebab-case-title.md          # General notes
YYYY-MM-DD.md                # Daily notes
YYYY-MM-DD-meeting-title.md  # Meeting notes
project-name.md              # Project overviews
```

- Always lowercase
- Hyphens not underscores
- No spaces (they break some tools)
- Date prefix for time-sensitive notes

## Frontmatter Property Reference

<properties>
Standard properties used across note types:

| Property | Type | Values | Used By |
|----------|------|--------|---------|
| type | text | note, meeting, project, daily, reference, task | Base views, filters |
| status | text | draft, active, completed, archived | Base views, filters |
| created | date | YYYY-MM-DD | Sorting, filtering |
| date | date | YYYY-MM-DD | Meetings, daily notes |
| project | text | project-name | Grouping, linking |
| tags | list | tag strings | Search, bases |
| attendees | list | names | Meeting notes |
| source | text | origin identifier | Tracking where content came from |

Don't invent new properties unless needed. Stick to the schema.
</properties>

## Output Format

```markdown
## Note Created

**Title:** [[Note Title]]
**Path:** folder/note-title.md
**Type:** [note type]
**Template:** [template used]
**Links:** [[Link 1]], [[Link 2]]

[Preview of first 5 lines]
```

## NEVER

- Create notes without checking vault conventions first
- Skip frontmatter (every note needs it)
- Use spaces in filenames
- Create duplicates without asking
- Invent frontmatter properties not in the vault schema
- Put notes in the wrong folder for their type
- Create a note without at least checking for related notes to link

## ALWAYS

- Read CLAUDE.md (or detect conventions) before creating
- Use the best available CLI, fall back to direct file write
- Follow the vault's naming convention
- Include proper frontmatter matching the vault schema
- Check for duplicates before creating
- Search for related notes and add wikilinks where relevant
- Confirm what was created and where

## Example

**User:** "Create a note about the API rate limiting approach we just discussed"

```
Reading vault conventions from CLAUDE.md...

Vault: MainVault
Convention: Notes go in Notes/, type: note, status: draft

Checking for related notes...
Found: [[api-design]], [[backend-architecture]]

No duplicate found for "api-rate-limiting".

Note created: [[API Rate Limiting]]

Path: Notes/api-rate-limiting.md
Type: note
Links: [[api-design]], [[backend-architecture]]

---
type: note
created: 2026-02-12
status: draft
tags:
  - api
  - architecture
---

# API Rate Limiting

Approach discussed for handling rate limits on the public API.

## Decision

- Token bucket algorithm with [[api-design|existing API gateway]]
- 100 requests/minute per API key
- 429 response with Retry-After header

## Links

- Related: [[api-design]], [[backend-architecture]]
```

<failed-attempts>
What DOESN'T work:
- Creating notes without reading CLAUDE.md first — wrong folder, wrong frontmatter
- Using official CLI from WSL when Obsidian runs on Windows — connection fails
- Assuming property names — one vault uses "status", another uses "state"
- Forcing wikilinks to notes that don't exist yet (creates dead links)
</failed-attempts>
