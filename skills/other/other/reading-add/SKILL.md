---
name: reading-add
description: Add file or URL to reading inbox. Use when "add to reading list", "save for reading", "put this on my reading list", "reading inbox", "read later", "save this paper", or when triaging email attachments for reading. Also triggers when user says "find the paper/attachment and add to reading" — this skill handles both locating and ingesting the material.
user-invocable: false
---

# Add to Reading Inbox

Triage reading material into the Obsidian vault inbox (synced via Syncthing) and optionally to Readwise Reader.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Source | YES | File path, URL, or description of where to find it (e.g., "the attachment from today's email") |
| Project | NO | Obsidian project backlink, e.g. `[[SEC Disclosure]]` |
| Readwise | NO | Whether to also save to Readwise Reader |

## Workflow

```
User says "add X to reading list"
    |
    v
Is the source already a file path or URL?
    |
  YES --> Go to Step 2 (metadata extraction)
    |
   NO --> Step 1: Resolve the source
          |
          User said "attachment" / "inbox" / "email"?
            YES --> superhuman search → download attachment → proceed
          User gave a paper title or author?
            YES --> Search email FIRST, then scholar/web only if not in email
          User pointed to a calendar event?
            YES --> Check event for attachments/links → proceed
          User mentioned "Canvas" / "posted on Canvas"?
            YES --> Canvas API: list modules → find file → download → proceed
```

## Steps

### 1. Resolve Source (when source is not yet a file or URL)

The user often says things like "find the paper from the workshop and add it to reading" without providing a direct path. Your job is to locate the actual file.

**Source resolution priority — follow this order:**

| User says | Search first | Then try |
|-----------|-------------|----------|
| "attachment", "the PDF from", "that paper someone sent" | `superhuman search` for email with attachment | — |
| "paper by [Author]", "the [Title] paper" | `superhuman search` (someone may have sent it) | Google Scholar / web |
| "from the meeting", "from the workshop" | Calendar event → email thread around that event | — |
| "on Canvas", "posted on Canvas", "Canvas copy" | Canvas API: list modules → find the file → download | Ask user which course if ambiguous |
| "this article" + URL in conversation | Use the URL directly | — |

**Downloading email attachments:**

```bash
# Search for the email
superhuman search "workshop paper" --limit 5

# Download the attachment (use the message ID from search results)
superhuman attachment download <message-id> --output /tmp/
```

After downloading, proceed to Step 2 with the downloaded file path.

**Downloading from Canvas LMS:**

If the user mentions Canvas, use the Canvas API to find and download the file. See `references/canvas-courses.md` for course IDs, credentials location, and API patterns.

### 2. Extract Metadata & Rename (files only)

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

### 3. Copy to Vault Inbox

```bash
mkdir -p "/Users/vwh7mb/Documents/Notes/Vault/3. Resources/Inbox"
cp "/path/to/source.pdf" "/Users/vwh7mb/Documents/Notes/Vault/3. Resources/Inbox/Author (Date) - Title.pdf"
```

The vault syncs via Syncthing — file is accessible on all devices (Onyx Boox, etc.) without any extra upload step.

**Multiple attachments:** If the source email has multiple related files (e.g., paper + appendices), copy all of them. Name appendices consistently: `Author (Date) - Title - Appendix.pdf`.

### 4. Add to Daily Note (under Reading heading)

The daily note has multiple sections. Insert the entry **under the `# Reading` heading**, not at the end of the file.

**Step 4a: Ensure daily note exists**

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

**Step 4b: Insert under Reading heading**

Use the Edit tool to insert the new line after `# Reading` (or after the last existing reading item under that heading).

**Format rules:**
- Always a checkbox: `- [ ]`
- For files: use an Obsidian wiki-link to the renamed file: `[[Author (Date) - Title.pdf]]`
- Project backlink inline if provided: `[[Author (Date) - Title.pdf]] [[Project Name]]`
- No backlink if no project context: `[[Author (Date) - Title.pdf]]`
- For URLs: use a markdown link: `[Title](https://example.com)`
- Never add task metadata (dates, priority). The Obsidian Tasks plugin handles that automatically.

### 5. Save to Readwise Reader (optional)

Only when user explicitly requests Readwise.

**For URLs:**
```bash
readwise reader-create-document --url "https://example.com/article" --tags reading-inbox
```

**For files (PDFs, EPUB, etc.):**
```bash
readwise upload "/path/to/file.pdf" --tag reading-inbox
```

### 6. Confirm

Report what was done:
- Renamed filename
- Where the file was saved
- What was added to the daily note
- Whether it was saved to Readwise

## Examples

**"Add this PDF to my reading list"** (file path provided)
```
1. look-at extracts: Title: Mirroring the Market, Authors: Nathan Atkinson, Date: 2026
2. Propose: "Atkinson (2026) - Mirroring the Market.pdf" → user confirms
3. cp to vault inbox
4. Daily note: "- [ ] [[Atkinson (2026) - Mirroring the Market.pdf]]"
```

**"Find the paper attachment for the workshop and put it on my reading list"** (source not provided)
```
1. superhuman search "workshop paper" → find email with PDF attachment
2. superhuman attachment download → /tmp/paper.pdf
3. look-at extracts: Title: Canons and the Court, Authors: Jonathan Choi, Nina Mendelson, Date: 2026
4. Propose: "Choi, Mendelson (2026) - Canons and the Court.pdf" → user confirms
5. cp to vault inbox
6. Daily note: "- [ ] [[Choi, Mendelson (2026) - Canons and the Court.pdf]]"
```

**"Add this paper to reading, related to Pass-through Voting"**
```
Same as above, daily note entry:
"- [ ] [[Atkinson (2026) - Mirroring the Market.pdf]] [[Pass-through Voting]]"
```

**"Save this article to reading and readwise"**
```
1. Daily note: "- [ ] [Article Title](https://example.com/article)"
2. readwise reader-create-document --url "https://example.com/article" --tags reading-inbox
```

## Red Flags — STOP If You Catch Yourself:

| Action | Why Wrong | Do Instead |
|--------|-----------|------------|
| Searching SSRN/web/scholar when user said "attachment" | "Attachment" means email — the file is in the inbox, not on the web. The user will have to correct you and wait while you redo it. | `superhuman search` immediately |
| Using an SSRN/web URL as a proxy for the actual paper | A link is not the paper. The user wants the PDF in their vault for offline reading on their e-reader. | Download the actual file, or ask the user where it is |
| Running `daily:append` to add a reading entry | Appends to the end of the note (after # Work), not under # Reading | Read the daily note file → Edit to insert under `# Reading` |
| Searching calendar, web, SSRN before checking email | Email is the most common source for papers shared with the user. Searching other sources first wastes time and context. | Check email first when the source is ambiguous |

## Iron Law: Correct Section Placement

**NEVER use `daily:append` for reading items.** It appends to the end of the note (after Work section). Instead, always Read the daily note file and Edit to insert under the `# Reading` heading.

```
WRONG: obsidian vault=Vault daily:append content="- [ ] Paper"
  → Ends up after # Work

RIGHT: Read daily note → Edit to insert after # Reading line
  → Entry appears in correct section
```

## Iron Law: Attachment Means Email

**When the user says "attachment", "the paper someone sent", or "that PDF from [person/event]" — search email FIRST.** Do not search the web, SSRN, Google Scholar, or any other source before checking email.

The user's mental model: someone sent them a file → it's in their inbox. Searching elsewhere first is a detour that wastes time, burns context, and forces the user to repeat themselves.

```
WRONG: User says "attachment" → search SSRN → search web → search scholar → finally check email
  → 12+ tool calls wasted, user frustrated

RIGHT: User says "attachment" → superhuman search → download → done
  → 2-3 tool calls, user happy
```
