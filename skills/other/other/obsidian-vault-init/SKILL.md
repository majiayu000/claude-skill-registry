---
name: obsidian-vault-init
description: |
  Initialises an Obsidian vault for Claude Code workflows. Sets up folder
  structure, frontmatter conventions, templates, starter .base views, and a
  CLAUDE.md that describes the vault so future sessions understand it instantly.
  Activates on "set up obsidian", "init vault", "new vault", or first contact
  with an Obsidian project that has no CLAUDE.md.
allowed-tools: |
  bash: ls, mkdir, find, obsidian-cli, obsidian
  file: read, write
---

# Obsidian Vault Init

<purpose>
The cold start problem. You open a fresh vault (or an existing one with no
structure) and Claude Code has zero context — what folders exist, what templates
to use, what frontmatter properties matter, how notes link together. This skill
bootstraps the vault with sensible structure and leaves a map (CLAUDE.md) so
every future session starts oriented, not lost.
</purpose>

## When To Activate

<triggers>
- User says "set up obsidian", "init vault", "new vault", "bootstrap vault"
- User says "make my vault work with Claude Code"
- Vault exists but has no CLAUDE.md and user asks Claude to create/manage notes
- User says "organise my vault" or "structure my vault"
- Beginning of session where vault has no CLAUDE.md
</triggers>

Do NOT trigger for:
- Vaults that already have a CLAUDE.md (read it instead)
- Single note creation (use obsidian-note-create)
- User explicitly says they don't want structure changes

## Instructions

### Step 1: Detect the Environment

<detect>
Before anything, figure out what you're working with:

```bash
# Where is the vault?
# WSL: vault is likely on Windows filesystem
ls /mnt/c/Users/*/Documents/*vault* 2>/dev/null
ls /mnt/c/Users/*/Obsidian* 2>/dev/null

# Direct Linux/Mac
ls ~/Documents/*vault* 2>/dev/null
ls ~/Obsidian* 2>/dev/null

# If user gave a path, use that
ls "$VAULT_PATH"
```

Check what already exists:

```bash
# Existing structure
find "$VAULT_PATH" -maxdepth 2 -type d | head -30

# Existing templates
find "$VAULT_PATH" -path "*template*" -name "*.md" | head -10

# Existing .base files
find "$VAULT_PATH" -name "*.base" | head -10

# Check for CLAUDE.md
cat "$VAULT_PATH/CLAUDE.md" 2>/dev/null
```

Check which CLI is available:

```bash
which obsidian 2>/dev/null && echo "Official CLI available"
which obsidian-cli 2>/dev/null && echo "Yakitrak CLI available"
```
</detect>

### Step 2: Ask About Vault Purpose

<purpose_check>
Don't assume. Ask:

```
What's this vault for?

1. Personal knowledge management (PKM) - notes, learnings, references
2. Project notes - dev projects, tasks, meetings
3. Journal / daily notes - daily log, reflections
4. Mixed / all of the above

And: do you already have folder conventions you want to keep?
```

Respect existing structure. Build around it, not over it.
</purpose_check>

### Step 3: Create Folder Structure

<folders>
Based on vault purpose, create what's missing:

**PKM vault:**
```
Inbox/              # Quick capture, unsorted
Notes/              # Permanent notes
References/         # Source material, articles, books
Templates/          # Note templates
Attachments/        # Images, PDFs
```

**Project vault:**
```
Projects/           # One subfolder per project
  project-name/
    meetings/
    notes/
    tasks/
Archive/            # Completed projects
Templates/
Attachments/
```

**Journal vault:**
```
Daily/              # Daily notes (YYYY-MM-DD.md)
Weekly/             # Weekly reviews
Notes/              # Longer-form notes
Templates/
Attachments/
```

**Mixed vault:**
```
Inbox/
Projects/
Daily/
Notes/
References/
Templates/
Attachments/
```

Create with:
```bash
mkdir -p "$VAULT_PATH/Inbox" "$VAULT_PATH/Notes" "$VAULT_PATH/Templates" "$VAULT_PATH/Attachments"
```
</folders>

### Step 4: Create Templates

<templates>
Create a template for each major note type. Templates use Obsidian frontmatter
conventions — properties at the top in YAML, then body structure.

**General note template (`Templates/Note.md`):**
```markdown
---
type: note
created: {{date}}
tags: []
status: draft
---

# {{title}}


```

**Meeting template (`Templates/Meeting.md`):**
```markdown
---
type: meeting
project:
date: {{date}}
attendees: []
status: active
tags:
  - meeting
---

# {{title}}

**Date**: {{date}}
**Attendees**:

---

## Agenda


## Notes


## Action Items

- [ ]
```

**Project template (`Templates/Project.md`):**
```markdown
---
type: project
status: active
created: {{date}}
tags:
  - project
---

# {{title}}

## Goal


## Tasks

- [ ]

## Notes


## Links

```

**Daily note template (`Templates/Daily.md`):**
```markdown
---
type: daily
date: {{date}}
tags:
  - daily
---

# {{date}}

## Tasks

- [ ]

## Log


## Links

```

Note: `{{date}}` and `{{title}}` are Templater/core template placeholders.
If the user has Templater installed, use `<% tp.date.now("YYYY-MM-DD") %>` and
`<% tp.file.title %>` instead.
</templates>

### Step 5: Create Starter Base Views

<bases>
Create `.base` files that give instant value:

**All Tasks (`Tasks.base`):**
```yaml
filter:
  - property: type
    operator: "=="
    value: meeting
  - operator: OR
  - property: type
    operator: "=="
    value: project
properties:
  task-status:
    formula: 'this.status'
views:
  - name: All Tasks
    type: table
    properties:
      - file.name
      - status
      - project
      - date
    sort:
      - property: date
        order: desc
```

**Recent Notes (`Recent.base`):**
```yaml
properties: {}
views:
  - name: Recent Notes
    type: table
    properties:
      - file.name
      - type
      - tags
      - file.mtime
    sort:
      - property: file.mtime
        order: desc
    filter:
      - property: file.mtime
        operator: ">="
        value: "{{today - 7 days}}"
```
</bases>

### Step 6: Create CLAUDE.md

<claude_md>
This is the most important file. Every future Claude session reads this first.

Write `CLAUDE.md` at vault root:

```markdown
# Vault: [Vault Name]

## Structure

[List actual folders and their purpose]

## Conventions

### Frontmatter Properties
- `type`: [note, meeting, project, daily, reference]
- `status`: [draft, active, completed, archived]
- `project`: project name (lowercase, kebab-case)
- `tags`: array of tags
- `date`: YYYY-MM-DD
- `created`: YYYY-MM-DD

### File Naming
- Notes: `kebab-case-title.md`
- Daily: `YYYY-MM-DD.md` in Daily/
- Meetings: `YYYY-MM-DD-meeting-title.md` in project meetings folder

### Linking
- Use wikilinks: `[[Note Name]]`
- Use heading links: `[[Note Name#Heading]]`
- Embed with: `![[Note Name]]`
- Images: `![[image.png|500]]` (with width)

### Templates
- [List each template and when to use it]
- Template folder: Templates/

### Tags
- Use nested tags: `#project/name`, `#type/meeting`
- Common: #meeting, #project, #daily, #reference, #task

## CLI

[Available CLI tool and common commands]

## Notes for Claude

- Vault path: [absolute path]
- WSL: [yes/no, and path mapping if yes]
- Templater: [installed/not installed]
- Always check for existing notes before creating duplicates
- Respect the folder → template mapping above
- Keep frontmatter consistent with the property schema
```
</claude_md>

### Step 7: Verify

<verify>
After setup, confirm everything:

```bash
# Check structure exists
find "$VAULT_PATH" -maxdepth 2 -type d

# Check templates
ls "$VAULT_PATH/Templates/"

# Check CLAUDE.md
cat "$VAULT_PATH/CLAUDE.md"

# Check .base files
find "$VAULT_PATH" -name "*.base"
```

Report what was created:
```markdown
Vault initialised at [path]

Created:
- [X] folders
- [Y] templates
- [Z] .base views
- CLAUDE.md (vault map for future sessions)

Next: create your first note with obsidian-note-create
```
</verify>

## Output Format

```markdown
## Vault Init: [Vault Name]

**Path:** [vault path]
**Type:** [PKM / Project / Journal / Mixed]
**CLI:** [Official / Yakitrak / None]

### Created
- Folders: [list]
- Templates: [list]
- Base views: [list]
- CLAUDE.md: yes

### Folder → Template Mapping
| Folder | Template |
|--------|----------|
| Notes/ | Note.md |
| Daily/ | Daily.md |
| Projects/*/meetings/ | Meeting.md |

### Next Steps
1. Open vault in Obsidian to verify
2. Customise templates to your taste
3. Start creating notes
```

## NEVER

- Overwrite existing vault structure without asking
- Delete existing files or folders
- Create structure without asking about vault purpose first
- Skip the CLAUDE.md (it's the whole point)
- Use hardcoded paths — always detect or ask
- Assume Templater is installed — check first

## ALWAYS

- Detect the environment (WSL, CLI availability) before acting
- Respect existing folder structure and conventions
- Create CLAUDE.md with accurate, current vault state
- Use the user's preferred naming conventions if they have them
- Create templates with proper frontmatter matching the property schema
- Report exactly what was created

## Example

**User:** "Set up my obsidian vault for Claude Code. It's at /mnt/c/Users/me/Obsidian/MainVault"

```
Vault Init

Detected:
- WSL environment (path: /mnt/c/...)
- Existing folders: Daily/, Attachments/
- Yakitrak CLI available
- Templater plugin installed (found .obsidian/plugins/templater-obsidian/)
- No CLAUDE.md

What's this vault primarily for?
1. PKM
2. Project notes
3. Journal
4. Mixed

[User: Mixed]

Creating structure around your existing folders...

Created:
- Inbox/ (quick capture)
- Notes/ (permanent notes)
- Projects/ (project folders)
- References/ (source material)
- Templates/ (5 templates: Note, Meeting, Project, Daily, Reference)
- Tasks.base (all tasks view)
- Recent.base (last 7 days)
- CLAUDE.md (vault map)

Kept existing: Daily/, Attachments/

Your vault is ready. Future Claude sessions will read CLAUDE.md first.
```

<failed-attempts>
What DOESN'T work:
- Creating structure without checking what exists first — overwrites user's work
- Using official Obsidian CLI from WSL — it can't reach the Windows Obsidian process
- Assuming folder names — some users use "Journal" not "Daily", "Assets" not "Attachments"
- Skipping CLAUDE.md — next session starts from scratch again
</failed-attempts>
