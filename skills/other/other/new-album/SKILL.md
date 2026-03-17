---
name: new-album
description: Creates a new album with the correct directory structure and templates. Use IMMEDIATELY when the user says 'make a new album' or similar, before any discussion.
argument-hint: <album-name> <genre>
model: claude-haiku-4-5-20251001
allowed-tools:
  - Read
  - Bash
  - Write
---

## Your Task

**Input**: $ARGUMENTS

Create a new album directory structure with all required files and templates.

---

# New Album Skill

You create the complete album directory structure based on config.

## Step 1: Parse Arguments

Expected formats:
- `<album-name> <genre>` — standard album
- `<album-name> documentary <genre>` — true-story/documentary album (creates RESEARCH.md + SOURCES.md)

Examples:
- `sample-album electronic`
- `my-new-album hip-hop`
- `protest-songs folk`
- `the-heist documentary hip-hop`

Valid genres (primary categories):
- `hip-hop`
- `electronic`
- `rock`
- `folk`
- `country`
- `pop`
- `metal`
- `jazz`
- `rnb`
- `classical`
- `reggae`
- `punk`
- `indie-folk`
- `blues`
- `gospel`
- `latin`
- `k-pop`

**Parsing logic:**
1. If 3 arguments and second is `documentary`: album = arg1, genre = arg3, documentary = true
2. If 2 arguments: album = arg1, genre = arg2, documentary = false
3. If 2 arguments and neither matches a valid genre: ask for clarification
4. If only 1 argument or none: ask the user

**After parsing, if documentary flag was not set, ask:**
"Is this a documentary/true-story album? (This adds research and sources templates.)"

If arguments are missing, ask:
```
Usage: /new-album <album-name> <genre>
       /new-album <album-name> documentary <genre>

Example: /new-album sample-album electronic
         /new-album the-heist documentary hip-hop

Valid genres: hip-hop, electronic, rock, folk, country, pop, metal, jazz, rnb, classical, reggae, punk, indie-folk, blues, gospel, latin, k-pop
```

## Step 2: Create Album via MCP

Call `create_album_structure(album_slug, genre, documentary)` — creates the complete directory structure with templates in one call.

- Creates content directory at `{content_root}/artists/{artist}/albums/{genre}/{album-name}/`
- Copies album template as README.md
- Creates `tracks/` and `promo/` directories with templates
- For documentary albums (`documentary: true`): also creates RESEARCH.md and SOURCES.md
- Returns `{created: bool, path: str, files: [...]}`
- If album already exists, returns an error

**Note**: Audio and documents directories are NOT created (those are created when needed by import-audio/import-art).

## Step 3: Confirm

Report:
```
Created album: {album-name}
Location: {album_path}

Files created:
- README.md (album template)
- tracks/ (empty, ready for track files)
- promo/ (social media copy templates)

Next steps:
  Option 1 - Interactive (Recommended):
    Run /bitwize-music:album-conceptualizer to design your album concept
    through the 7 Planning Phases.

  Option 2 - Manual:
    1. Edit README.md with your album concept
    2. Create tracks with /import-track or manually in tracks/
```

## Error Handling

**Config file missing:**
```
Error: Config not found at ~/.bitwize-music/config.yaml
Run /configure to set up.
```

**Invalid genre:**
```
Error: Invalid genre "{genre}"

Valid genres: hip-hop, electronic, rock, folk, country, pop, metal, jazz, rnb, classical, reggae, punk, indie-folk, blues, gospel, latin, k-pop
```

**Album already exists:**
```
Error: Album already exists at {album_path}
```

**Templates not found:**
```
Error: Templates not found. Is the plugin installed correctly?
Expected at: ${CLAUDE_PLUGIN_ROOT}/templates/
```

---

## Examples

```
/new-album sample-album electronic
```

Config has:
```yaml
paths:
  content_root: ~/bitwize-music
artist:
  name: bitwize
```

Result:
```
Created album: sample-album
Location: ~/bitwize-music/artists/bitwize/albums/electronic/sample-album/

Files created:
- README.md (album template)
- tracks/ (empty, ready for track files)

Next steps:
  Option 1 - Interactive (Recommended):
    Run /bitwize-music:album-conceptualizer to design your album concept
    through the 7 Planning Phases.

  Option 2 - Manual:
    1. Edit README.md with your album concept
    2. Create tracks with /import-track or manually in tracks/
```

---

## True Story Albums

If user mentions this is a documentary or true-story album:

```
/new-album the-heist documentary hip-hop
```

The `create_album_structure(album_slug, genre, documentary=true)` call automatically creates RESEARCH.md and SOURCES.md from templates.

Report:
```
Created album: the-heist (documentary)
Location: ~/bitwize-music/artists/bitwize/albums/hip-hop/the-heist/

Files created:
- README.md (album template)
- RESEARCH.md (research template)
- SOURCES.md (sources template)
- tracks/ (empty, ready for track files)
```

---

## Common Mistakes

### ❌ Don't: Create directories manually

**Wrong:**
```bash
# Manual mkdir, config reading, template copying
cat ~/.bitwize-music/config.yaml
mkdir -p ~/music-projects/artists/bitwize/albums/...
cp templates/album.md ...
```

**Right:**
```
# Single MCP call handles everything
create_album_structure(album_slug, genre, documentary)
```

The MCP tool reads config, resolves paths, creates directories, and copies templates automatically.

### ❌ Don't: Use wrong genre category

**Wrong:**
```bash
# Using subgenre instead of primary category
/new-album my-album boom-bap        # boom-bap is a subgenre
/new-album my-album trap            # trap is a subgenre
```

**Right:**
```bash
# Use primary genre category
/new-album my-album hip-hop         # boom-bap and trap go in hip-hop
/new-album my-album electronic      # house, techno go in electronic
```

Valid primary genres: `hip-hop`, `electronic`, `rock`, `folk`, `country`, `pop`, `metal`, `jazz`, `rnb`, `classical`, `reggae`, `punk`, `indie-folk`, `blues`, `gospel`, `latin`, `k-pop`
