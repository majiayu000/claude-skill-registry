---
name: clipboard
description: Copy track content (lyrics, style prompts) to system clipboard
argument-hint: <content-type> <album-name> <track-number>
model: claude-haiku-4-5-20251001
allowed-tools:
  - Read
  - Bash
---

## Your Task

**Input**: $ARGUMENTS

Copy content from track files to the system clipboard for pasting into Suno or other tools.

---

# Clipboard Skill

Copy specific sections from track files directly to your clipboard.

## Step 1: Detect Platform & Check Clipboard Tool

Run detection:

```bash
if command -v pbcopy >/dev/null 2>&1; then
  echo "macOS"
elif command -v clip.exe >/dev/null 2>&1; then
  echo "WSL"
elif command -v xclip >/dev/null 2>&1; then
  echo "Linux-xclip"
elif command -v xsel >/dev/null 2>&1; then
  echo "Linux-xsel"
else
  echo "NONE"
fi
```

**If NONE:**

```
Error: No clipboard utility found.

Install instructions:
- macOS: pbcopy (built-in)
- Linux: sudo apt install xclip
- WSL: clip.exe (built-in)
```

## Step 2: Parse Arguments

Expected format: `<content-type> <album-name> <track-number>`

**Content types:**
- `lyrics` - Suno Lyrics Box
- `style` - Suno Style Box
- `streaming-lyrics` - Streaming Lyrics (for distributors)
- `all` - All Suno inputs (Style + Lyrics combined)

Examples:
- `/clipboard lyrics sample-album 03`
- `/clipboard style sample-album 05`
- `/clipboard streaming-lyrics sample-album 02`
- `/clipboard all sample-album 01`

If arguments are missing:
```
Usage: /clipboard <content-type> <album-name> <track-number>

Content types: lyrics, style, streaming-lyrics, all

Example: /clipboard lyrics sample-album 03
```

## Step 3: Read Config (REQUIRED)

```bash
cat ~/.bitwize-music/config.yaml
```

Extract:
- `paths.content_root` → Base content directory
- `artist.name` → Artist name

## Step 4: Find Track File

Search for track file matching the number:

```bash
find {content_root}/artists/{artist}/albums/*/{{album}}/tracks/ -name "{track-number}-*.md" 2>/dev/null
```

Example: For track `03`, finds `03-t-day-beach.md` or `03-whatever.md`

**If not found:**
```
Error: Track {track-number} not found in album {album}
```

## Step 5: Extract Content

Read the track file and extract the requested section.

### For "lyrics" (Suno Lyrics Box)

Extract everything between:
```markdown
#### Lyrics Box (Suno)
```
and the next `###` or `####` heading.

### For "style" (Suno Style Box)

Extract everything between:
```markdown
#### Style Box (Suno)
```
and the next `###` or `####` heading.

### For "streaming-lyrics" (Streaming Lyrics)

Extract everything between:
```markdown
## Streaming Lyrics
```
and the next `##` heading.

### For "all" (Combined Suno Inputs)

Combine both Style Box and Lyrics Box with a separator:
```
[Style Box content]

---

[Lyrics Box content]
```

## Step 6: Copy to Clipboard

Use the detected platform's clipboard command:

| Platform | Command |
|----------|---------|
| macOS | `pbcopy` |
| WSL | `clip.exe` |
| Linux (xclip) | `xclip -selection clipboard` |
| Linux (xsel) | `xsel --clipboard --input` |

Example:
```bash
echo "content" | pbcopy  # macOS
echo "content" | xclip -selection clipboard  # Linux
```

## Step 7: Confirm

Report:
```
✓ Copied to clipboard: {content-type} from track {track-number}
  Album: {album}
  Track: {track-filename}
```

## Error Handling

**Track file not found:**
```
Error: Track {track-number} not found in album {album}

Available tracks:
- 01-track-name.md
- 02-track-name.md
```

**Content section not found:**
```
Error: {content-type} section not found in track {track-number}

The track file may not have this section yet.
```

**Config missing:**
```
Error: Config not found at ~/.bitwize-music/config.yaml
Run /configure to set up.
```

---

## Examples

### Copy Suno Lyrics

```
/clipboard lyrics sample-album 03
```

Output:
```
✓ Copied to clipboard: lyrics from track 03
  Album: sample-album
  Track: 03-t-day-beach.md
```

### Copy Style Prompt

```
/clipboard style sample-album 05
```

### Copy Streaming Lyrics

```
/clipboard streaming-lyrics sample-album 02
```

### Copy All Suno Inputs

```
/clipboard all sample-album 01
```

Output:
```
✓ Copied to clipboard: all suno inputs from track 01
  Album: sample-album
  Track: 01-intro.md

Contents:
- Style Box
- Lyrics Box
```

---

## Implementation Notes

**Clipboard Detection:**
- Check multiple tools in order of preference
- WSL has `clip.exe` which works from Linux subsystem
- Linux users may have either `xclip` or `xsel`

**Content Extraction:**
- Use sed/awk to extract sections between markdown headings
- Trim leading/trailing whitespace
- Preserve internal formatting (blank lines, indentation)

**Multiple Matches:**
- If track number matches multiple files (shouldn't happen), use the first match
- Warn user if directory structure looks wrong
