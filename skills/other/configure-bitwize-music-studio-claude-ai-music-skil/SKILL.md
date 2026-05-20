---
name: configure
description: Sets up or edits the plugin configuration file interactively. Use on first-time setup, when config is missing, or when the user wants to change settings.
argument-hint: [setup | edit | show | validate | reset]
model: claude-sonnet-4-6
allowed-tools:
  - Read
  - Write
  - Bash
  - AskUserQuestion
  - Glob
---

## Your Task

**Input**: $ARGUMENTS

Route based on argument:
- `setup` or no argument → Interactive first-time setup
- `edit` → Edit specific settings
- `show` → Display current configuration
- `validate` → Check config for issues
- `reset` → Delete config and start fresh

---

# Plugin Configuration Skill

You help users set up and manage their `~/.bitwize-music/config.yaml` configuration.

## Config Location

```
~/.bitwize-music/config.yaml
```

## Commands

### `/configure` or `/configure setup`

Interactive first-time setup. Guide user through creating their config.

**Steps:**

1. Check if `~/.bitwize-music/config.yaml` exists
2. If exists, ask if they want to overwrite or edit instead
3. If creating new:
   - Create `~/.bitwize-music/` directory if needed
   - Ask for each required setting interactively
   - Write the config file
   - Validate the result

**Required settings to ask:**
1. `artist.name` - "What's your artist/project name?"
2. `paths.content_root` - "Where should albums and projects be stored? (e.g., ~/music-projects)"
3. `paths.audio_root` - "Where should mastered audio files go? (e.g., ~/music-projects/audio)"
4. `paths.documents_root` - "Where should research documents/PDFs go? (e.g., ~/music-projects/documents)"

**Optional settings:**
5. `artist.genres` - "What are your primary genres? (comma-separated, or skip)"
6. `urls.soundcloud` - "SoundCloud profile URL? (or skip)"

**Step 5: Overrides Directory (Optional)**

Ask:
> You can optionally provide a path to a directory containing override files.
> This is where you can customize workflows and skills without plugin update conflicts.
>
> Override files you can create:
>   - CLAUDE.md (custom workflow instructions)
>   - pronunciation-guide.md (artist names, character names)
>   - explicit-words.md (custom explicit word list)
>
> Default: ~/music-projects/overrides
>
> Enter path (or press Enter to use default):

If user provides path:
- Add to config: `paths.overrides: "[user-path]"`

If user presses Enter (accepts default):
- Add to config: `paths.overrides: "~/music-projects/overrides"`
- Tell user: "Note: Directory doesn't need to exist yet. Create override files when you want to customize."

**Step 6: Album Ideas File (Optional)**

Ask:
> You can optionally provide a path to a file for tracking album ideas.
> This is managed by the /bitwize-music:album-ideas skill for brainstorming and planning.
>
> Default: ~/music-projects/IDEAS.md
>
> Enter path (or press Enter to use default):

If user provides path:
- Add to config: `paths.ideas_file: "[user-path]"`

If user presses Enter (accepts default):
- Add to config: `paths.ideas_file: "~/music-projects/IDEAS.md"`
- Tell user: "Note: File doesn't need to exist yet. The album-ideas skill creates it when first used."

**Example interaction:**
```
Let's set up your bitwize-music configuration.

What's your artist/project name?
> Neon Circuits

Where should albums and projects be stored?
(This is where your album folders, lyrics, and research will live)
> ~/music-projects

Where should mastered audio files go?
> ~/music-projects/audio

Where should research documents/PDFs go?
> ~/music-projects/documents

What are your primary genres? (comma-separated, or press Enter to skip)
> electronic, synthwave

SoundCloud profile URL? (or press Enter to skip)
> https://soundcloud.com/neon-circuits

Overrides directory path? (press Enter for default: ~/music-projects/overrides)
> [Enter]

Album ideas file path? (press Enter for default: ~/music-projects/IDEAS.md)
> [Enter]

Creating config at ~/.bitwize-music/config.yaml...

✓ Configuration saved!

Your settings:
  Artist: Neon Circuits
  Content: ~/music-projects
  Audio: ~/music-projects/audio
  Documents: ~/music-projects/documents
  Genres: electronic, synthwave
  SoundCloud: https://soundcloud.com/neon-circuits
  Overrides: ~/music-projects/overrides (will be used if created)
  Ideas File: ~/music-projects/IDEAS.md (will be created when first used)

You're ready to start creating albums!
```

### `/configure edit`

Edit specific settings without recreating the whole config.

**Steps:**
1. Read existing config
2. Show current values
3. Ask what they want to change
4. Update just that setting
5. Validate and save

**Example:**
```
Current configuration:

  artist.name: Neon Circuits
  paths.content_root: ~/music-projects
  paths.audio_root: ~/music-projects/audio
  paths.documents_root: ~/music-projects/documents
  artist.genres: [electronic, synthwave]
  urls.soundcloud: https://soundcloud.com/neon-circuits

What would you like to change?
```

### `/configure show`

Display the current configuration in a readable format.

**Steps:**
1. Read `~/.bitwize-music/config.yaml`
2. Display all settings in a formatted table
3. Note any missing required settings

**Example output:**
```
bitwize-music Configuration
Location: ~/.bitwize-music/config.yaml

┌─────────────────────┬────────────────────────────────────┐
│ Setting             │ Value                              │
├─────────────────────┼────────────────────────────────────┤
│ artist.name         │ Neon Circuits                      │
│ artist.genres       │ electronic, synthwave              │
│ paths.content_root  │ ~/music-projects                   │
│ paths.audio_root    │ ~/music-projects/audio             │
│ paths.documents_root│ ~/music-projects/documents         │
│ paths.overrides     │ ~/music-projects/overrides         │
│ paths.ideas_file    │ ~/music-projects/IDEAS.md          │
│ urls.soundcloud     │ https://soundcloud.com/neon-circuits│
│ generation.service  │ suno                               │
└─────────────────────┴────────────────────────────────────┘

✓ All required settings present
```

### `/configure validate`

Check the config for issues.

**Checks:**
1. Config file exists
2. All required fields present
3. Paths are valid (directories exist or can be created)
4. No syntax errors in YAML

**Example output:**
```
Validating ~/.bitwize-music/config.yaml...

✓ Config file exists
✓ artist.name: Neon Circuits
✓ paths.content_root: ~/music-projects (exists)
✓ paths.audio_root: ~/music-projects/audio (exists)
✓ paths.documents_root: ~/music-projects/documents (will be created)
✓ paths.overrides: ~/music-projects/overrides (will be used if created)
✓ paths.ideas_file: ~/music-projects/IDEAS.md (will be created when first used)
✓ generation.service: suno

All checks passed!
```

Or with issues:
```
Validating ~/.bitwize-music/config.yaml...

✓ Config file exists
✓ artist.name: Neon Circuits
✗ paths.content_root: not set (required)
✓ paths.audio_root: ~/music-projects/audio
✗ paths.documents_root: /invalid/path (directory doesn't exist)

2 issues found. Run /configure edit to fix.
```

### `/configure reset`

Delete config and optionally start fresh.

**Steps:**
1. Confirm user really wants to reset
2. Back up existing config to `config.yaml.bak`
3. Delete `~/.bitwize-music/config.yaml`
4. Ask if they want to run setup now

**Example:**
```
⚠️  This will delete your configuration at ~/.bitwize-music/config.yaml

Current config will be backed up to config.yaml.bak

Are you sure you want to reset? (yes/no)
```

If yes:
```
✓ Backed up to ~/.bitwize-music/config.yaml.bak
✓ Deleted ~/.bitwize-music/config.yaml

Config has been reset.

Would you like to set up a new config now? (yes/no)
```

---

## Config Template

When creating a new config, use this structure:

```yaml
# bitwize-music Plugin Configuration
# Generated by /configure

artist:
  name: "{artist_name}"
  genres:
    - "{genre1}"
    - "{genre2}"

paths:
  content_root: "{content_root}"
  audio_root: "{audio_root}"
  documents_root: "{documents_root}"
  overrides: "{overrides}"
  ideas_file: "{ideas_file}"

urls:
  soundcloud: "{soundcloud_url}"

generation:
  service: suno
```

---

## Edge Cases

### Config exists but is invalid YAML
- Back up the existing file: `config.yaml.bak`
- Offer to create fresh config

### Directory doesn't exist
- Offer to create it: "Directory ~/music-projects doesn't exist. Create it?"

### User provides relative path
- Expand to absolute: `./projects` → `/Users/name/projects`
- Or use `~` prefix: `~/projects`

---

## Remember

- **Preserve exact casing** - If user says "bitwize", write "bitwize" not "Bitwize"
- Always expand `~` in paths for display
- Create directories if they don't exist (with permission)
- Back up existing config before overwriting
- Validate after any changes
- Be friendly and explain what each setting does
