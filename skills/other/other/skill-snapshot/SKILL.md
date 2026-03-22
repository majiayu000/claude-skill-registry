---
name: reading-add
description: Add file or URL to reading inbox. Use when "add to reading list", "save for reading", "put this on my reading list", "reading inbox", "read later", or when triaging email attachments for reading.
user-invocable: false
---

# Add to Reading Inbox

Triage reading material into the Obsidian vault inbox (synced via Syncthing) and optionally to Readwise Reader.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Source | YES | File path (local/attachment) OR URL |
| Project | NO | Obsidian project backlink, e.g. `[[SEC Disclosure]]` |
| Readwise | NO | Whether to also save to Readwise Reader |

## Workflow

```
Source provided
    |
    v
Is it a local file (PDF, DOCX, etc.)?
    |
  YES --> 1. Extract metadata (title, authors, date) via look-at
    |      2. Propose filename: Author (Date) - Title.ext
    |      3. Confirm with user
    |      4. Copy renamed file to vault inbox
    |      5. Add daily note entry (under Reading heading)
    |      6. If readwise requested: upload file to Reader
    |
   NO (URL) --> 1. Add daily note entry (under Reading heading)
                2. If readwise requested: save URL to Reader
```

## Steps

### 1. Extract Metadata & Rename (files only)

Use look-at to extract metadata from the first page:

```bash
LOOK_AT=$(${CLAUDE_SKILL_DIR}/../../skills/look-at/scripts/look_at.py) && python3 "$LOOK_AT" \
    --file "/path/to/file.pdf" \
    --goal "Extract the title, authors, and date/year from the first page. Return as: Title: ..., Authors: ..., Date: ..."
```

**Naming convention: `Author (Date) - Title.ext`**

| Scenario | Filename |
|----------|----------|
| Single author | `Bishop (2026) - Activist Defense Firms.pdf` |
| Two authors | `Bishop, Hu (2026) - Activist Defense Firms.pdf` |
| Three+ authors | `Bishop et al. (2026) - Activist Defense Firms.pdf` |
| No date | `Bishop - Activist Defense Firms.pdf` |
| Non-academic (firm/org) | `BlackRock (2026) - Stewardship Report.pdf` |

Use last names only. Truncate long titles to a readable short form.

**Confirm the proposed filename with the user before copying.** Gemini may misread abbreviated dates (e.g., `25-Feb-26` → wrong year). Always verify.

### 2. Copy to Vault Inbox

```bash
mkdir -p "/Users/vwh7mb/Documents/Notes/Vault/3. Resources/Inbox"
cp "/path/to/source.pdf" "/Users/vwh7mb/Documents/Notes/Vault/3. Resources/Inbox/Author (Date) - Title.pdf"
```

The vault syncs via Syncthing — file is accessible on all devices (Onyx Boox, etc.) without any extra upload step.

### 3. Add to Daily Note (under Reading heading)

The daily note has multiple sections. Insert the entry **under the `# Reading` heading**, not at the end of the file.

**Step 3a: Ensure daily note exists**

```bash
obsidian vault=Vault daily:read >/dev/null 2>&1 || obsidian vault=Vault daily:append content=""
```

If `obsidian` CLI is unavailable, create manually:

```bash
TODAY=$(date +%Y-%m-%d)
DAILY="/Users/vwh7mb/Documents/Notes/Vault/3. Resources/Daily Notes/${TODAY}.md"
if [ ! -f "$DAILY" ]; then
  cat > "$DAILY" << 'TMPL'
# To-Dos
# Reading
# Meetings
# Work
TMPL
fi
```

**Step 3b: Insert under Reading heading**

Use the Edit tool to insert the new line after `# Reading` (or after the last existing reading item under that heading).

**Format rules:**
- Always a checkbox: `- [ ]`
- For files: use an Obsidian wiki-link to the renamed file: `[[Author (Date) - Title.pdf]]`
- Project backlink inline if provided: `[[Author (Date) - Title.pdf]] [[Project Name]]`
- No backlink if no project context: `[[Author (Date) - Title.pdf]]`
- For URLs: use a markdown link: `[Title](https://example.com)`
- Never add task metadata (dates, priority). The Obsidian Tasks plugin handles that automatically.

### 4. Save to Readwise Reader (optional)

Only when user explicitly requests Readwise.

**For URLs:**
```bash
readwise save "https://example.com/article" --tag reading-inbox
```

**For files (PDFs, EPUB, etc.):**
```bash
readwise upload "/path/to/file.pdf" --tag reading-inbox
```

### 5. Confirm

Report what was done:
- Renamed filename
- Where the file was saved
- What was added to the daily note
- Whether it was saved to Readwise

## Examples

**"Add this PDF to my reading list"**
```
1. look-at extracts: Title: Mirroring the Market, Authors: Nathan Atkinson, Date: 2026
2. Propose: "Atkinson (2026) - Mirroring the Market.pdf" → user confirms
3. cp to vault inbox
4. Daily note: "- [ ] [[Atkinson (2026) - Mirroring the Market.pdf]]"
```

**"Add this paper to reading, related to Pass-through Voting"**
```
Same as above, daily note entry:
"- [ ] [[Atkinson (2026) - Mirroring the Market.pdf]] [[Pass-through Voting]]"
```

**"Save this article to reading and readwise"**
```
1. Daily note: "- [ ] [Article Title](https://example.com/article)"
2. readwise save "https://example.com/article" --tag reading-inbox
```

**"Add this PDF to reading and readwise"**
```
1-3. Extract metadata, rename, copy to inbox
4. readwise upload "/path/to/renamed.pdf" --tag reading-inbox
5. Daily note: "- [ ] [[Author (Date) - Title.pdf]]"
```

## Iron Law: Correct Section Placement

**NEVER use `daily:append` for reading items.** It appends to the end of the note (after Work section). Instead, always Read the daily note file and Edit to insert under the `# Reading` heading.

```
WRONG: obsidian vault=Vault daily:append content="- [ ] Paper"
  → Ends up after # Work

RIGHT: Read daily note → Edit to insert after # Reading line
  → Entry appears in correct section
```
