---
context: fork
---

# /sync-notion-pages

Bidirectional sync between Obsidian notes and Notion pages for collaborative planning.

## Usage

```
/sync-notion-pages                      # Check all tracked pages for changes
/sync-notion-pages <note>               # Sync a specific note
/sync-notion-pages --push <note>        # Force push to Notion
/sync-notion-pages --pull <note>        # Force pull from Notion
/sync-notion-pages --link <note> <url>  # Link note to Notion page
/sync-notion-pages --unlink <note>      # Remove sync tracking from note
/sync-notion-pages --status             # Show sync status dashboard
```

## Prerequisites

- Notion MCP server must be connected (tools like `mcp__MCP_DOCKER__API-retrieve-a-page`)
- Notes must have `notionPageId` in frontmatter to be tracked

## Instructions

### Phase 1: Parse Command

1. Identify operation mode:
   - No args: Check all tracked pages
   - `<note>`: Sync specific note (detect direction automatically)
   - `--push <note>`: Force push local → Notion
   - `--pull <note>`: Force pull Notion → local
   - `--link <note> <url>`: Link existing note to Notion page
   - `--unlink <note>`: Remove sync tracking
   - `--status`: Show dashboard

2. If note specified, find it:
   - Search by filename or title
   - Verify note exists
   - Check if tracked (has `notionPageId`)

### Phase 2: Load Manifest

Read `.claude/sync/notion-pages-manifest.json`:

```json
{
  "version": "1.0",
  "lastFullSync": "2026-01-20T14:00:00Z",
  "trackedPages": {
    "<pageId>": {
      "localFile": "Trip - Lisbon March 2026.md",
      "notionUrl": "https://...",
      "notionLastEdited": "2026-01-20T14:30:00Z",
      "localLastModified": "2026-01-20T15:00:00Z",
      "lastSynced": "2026-01-20T14:00:00Z",
      "syncStatus": "local-ahead"
    }
  }
}
```

### Phase 3: Operations

#### 3A: Link Operation (`--link`)

1. Parse Notion URL to extract page ID:
   - Format: `https://www.notion.so/Page-Title-<pageId>` or `https://www.notion.so/<pageId>`
   - Page ID is typically 32 characters with optional hyphens

2. Fetch page from Notion using `mcp__MCP_DOCKER__API-retrieve-a-page`:

   ```
   page_id: "<extracted-page-id>"
   ```

3. Add sync fields to note frontmatter:

   ```yaml
   notionPageId: "<pageId>"
   notionUrl: "<full-url>"
   lastSynced: null
   syncStatus: unsynced
   ```

4. Add entry to manifest

5. Report success

#### 3B: Status Operation (`--status`)

1. For each tracked page in manifest:
   - Fetch Notion page `last_edited_time`
   - Get local file modified timestamp
   - Calculate sync status

2. Display dashboard:

   ```markdown
   # Notion Page Sync Status

   | Note          | Status      | Local Modified   | Notion Modified  | Last Synced      |
   | ------------- | ----------- | ---------------- | ---------------- | ---------------- |
   | Trip - Lisbon | local-ahead | 2026-01-21 10:00 | 2026-01-20 14:30 | 2026-01-20 14:00 |
   ```

3. Summarise:
   - X pages synced
   - X pages local-ahead (need push)
   - X pages remote-ahead (need pull)
   - X pages in conflict

#### 3C: Check/Sync Operation (default or specific note)

For each tracked page (or specific note):

1. **Fetch Notion metadata:**

   ```
   mcp__MCP_DOCKER__API-retrieve-a-page with page_id
   ```

   Extract `last_edited_time`

2. **Get local file modified time:**
   - Read file and check `modified` in frontmatter
   - Also check filesystem modified time as backup

3. **Compare against lastSynced:**

   ```
   localChanged = localModified > lastSynced
   remoteChanged = notionLastEdited > lastSynced

   Status:
   - synced: !localChanged && !remoteChanged
   - local-ahead: localChanged && !remoteChanged
   - remote-ahead: !localChanged && remoteChanged
   - conflict: localChanged && remoteChanged
   ```

4. **Take action based on status:**
   - `synced`: Report "No changes"
   - `local-ahead`: Auto-push to Notion
   - `remote-ahead`: Auto-pull from Notion
   - `conflict`: Prompt user for resolution

#### 3D: Push Operation (`--push` or auto-push)

1. **Read local note content:**
   - Parse frontmatter
   - Extract markdown body (skip frontmatter and callouts)

2. **Convert Markdown → Notion blocks:**

   | Markdown     | Notion Block Type      |
   | ------------ | ---------------------- | --- | ----- |
   | `# H1`       | heading_1              |
   | `## H2`      | heading_2              |
   | `### H3`     | heading_3              |
   | `paragraph`  | paragraph              |
   | `- item`     | bulleted_list_item     |
   | `1. item`    | numbered_list_item     |
   | `- [ ] task` | to_do (checked: false) |
   | `- [x] task` | to_do (checked: true)  |
   | `> quote`    | quote                  |
   | `code`       | code                   |
   | `            | table                  | `   | table |

3. **Clear existing Notion blocks:**
   - Get current blocks: `mcp__MCP_DOCKER__API-get-block-children`
   - Delete each block: `mcp__MCP_DOCKER__API-delete-a-block`

4. **Append new blocks:**
   - Use `mcp__MCP_DOCKER__API-patch-block-children` to add converted blocks

5. **Update timestamps:**
   - Update frontmatter `lastSynced` to now
   - Update manifest with new sync time
   - Set `syncStatus: synced`

#### 3E: Pull Operation (`--pull` or auto-pull)

1. **Fetch Notion page content:**

   ```
   mcp__MCP_DOCKER__API-retrieve-a-page with page_id
   mcp__MCP_DOCKER__API-get-block-children with block_id=page_id
   ```

2. **Convert Notion blocks → Markdown:**

   For each block, convert to markdown:

   ```javascript
   function blockToMarkdown(block) {
     switch (block.type) {
       case "heading_1":
         return `# ${getRichText(block.heading_1.rich_text)}`;
       case "heading_2":
         return `## ${getRichText(block.heading_2.rich_text)}`;
       case "heading_3":
         return `### ${getRichText(block.heading_3.rich_text)}`;
       case "paragraph":
         return getRichText(block.paragraph.rich_text);
       case "bulleted_list_item":
         return `- ${getRichText(block.bulleted_list_item.rich_text)}`;
       case "numbered_list_item":
         return `1. ${getRichText(block.numbered_list_item.rich_text)}`;
       case "to_do":
         const checked = block.to_do.checked ? "x" : " ";
         return `- [${checked}] ${getRichText(block.to_do.rich_text)}`;
       case "quote":
         return `> ${getRichText(block.quote.rich_text)}`;
       case "code":
         return `\`\`\`${block.code.language}\n${getRichText(block.code.rich_text)}\n\`\`\``;
       case "divider":
         return "---";
       default:
         return "";
     }
   }

   function getRichText(richTextArray) {
     return richTextArray.map((t) => t.plain_text).join("");
   }
   ```

3. **Preserve frontmatter:**
   - Read current note frontmatter
   - Update `modified` to today
   - Update `lastSynced` to now
   - Set `syncStatus: synced`

4. **Preserve local-only sections:**
   - Keep callout blocks (e.g., `> [!info]`)
   - Keep frontmatter
   - Replace body content

5. **Write updated note**

6. **Update manifest**

### Phase 4: Conflict Resolution

When both sides changed since last sync:

1. **Show diff summary:**

   ```markdown
   ## Conflict Detected: Trip - Lisbon March 2026

   **Local changes since 2026-01-20 14:00:**

   - Modified flights section
   - Added new activities

   **Notion changes since 2026-01-20 14:00:**

   - Collaborator added restaurant suggestions
   - Updated accommodation notes
   ```

2. **Offer resolution options using AskUserQuestion:**
   - Keep local (push to Notion)
   - Keep remote (pull from Notion)
   - Skip (resolve manually later)

3. **Execute chosen resolution:**
   - If keep local: Run push operation
   - If keep remote: Run pull operation
   - If skip: Leave status as `conflict`

### Phase 5: Report

```markdown
# Notion Page Sync Report

**Synced at:** 2026-01-21T10:30:00Z

## Summary

| Action              | Count |
| ------------------- | ----- |
| Synced (no changes) | 2     |
| Pushed to Notion    | 1     |
| Pulled from Notion  | 0     |
| Conflicts           | 0     |
| Errors              | 0     |

## Details

### Pushed: Trip - Lisbon March 2026

- Local modified: 2026-01-21 10:00
- Notion updated: 2026-01-21 10:30

## Next Steps

- Review synced content in Notion
- Check for any formatting issues
```

## Content Preservation Rules

### Always Preserve in Local Note:

- Frontmatter (sync adds/updates specific fields)
- Local callout blocks (`> [!info]`, `> [!warning]`)
- Links to other Obsidian notes (`[[Note Name]]`)

### Always Push to Notion:

- Headings
- Paragraphs
- Lists (bulleted, numbered, tasks)
- Tables
- Code blocks

### Handle Specially:

- Wiki-links: Convert `[[Note]]` to plain text when pushing
- Callouts: Skip when pushing (Notion doesn't support same format)
- Embedded content: Skip (handle manually)

## Error Handling

| Error                   | Action                              |
| ----------------------- | ----------------------------------- |
| Notion API rate limited | Wait and retry                      |
| Page not found          | Remove from tracking, notify user   |
| Invalid page ID         | Report error, suggest re-linking    |
| Network timeout         | Retry once, then report             |
| Malformed blocks        | Skip block, continue, report at end |

## Manifest Location

`.claude/sync/notion-pages-manifest.json`

This is separate from the Confluence sync manifest at `.claude/sync/manifest.json`.

## Example Workflow

### First-time setup for a note:

```
User: /sync-notion-pages --link "Trip - Lisbon March 2026" https://www.notion.so/Lisbon-March-2026-2ee76da238c981459c88ca451e112c39

Claude:
1. Extracts page ID: 2ee76da238c981459c88ca451e112c39
2. Fetches Notion page to verify
3. Updates note frontmatter with sync fields
4. Adds to manifest
5. Reports: "Linked Trip - Lisbon March 2026 to Notion page"
```

### Regular sync check:

```
User: /sync-notion-pages

Claude:
1. Loads manifest
2. For each tracked page, checks timestamps
3. Reports status for all pages
4. Offers to sync any that need it
```

### Force push after local edits:

```
User: /sync-notion-pages --push "Trip - Lisbon March 2026"

Claude:
1. Reads local note
2. Converts to Notion blocks
3. Updates Notion page
4. Updates timestamps
5. Reports success
```
