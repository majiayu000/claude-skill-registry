---
name: himalaya-email-manager
description: Email management using Himalaya CLI tool (IMAP). Search, summarize, and delete emails from an IMAP account. Supports natural language queries for email operations.
---

# Himalaya Email Manager

Manage emails using Himalaya IMAP CLI tool. Search, summarize, and delete emails from an IMAP account. Use natural language queries for email operations.

## Configuration

Himalaya config: ~/.config/himalaya/config.toml
Invocation: `uv run {skill_directory}/scripts/<script>.py` (handles Python environment and dependencies, do NOT cd into skill directory)

## Get Daily Email Summary

Show emails from the past 24 hours in INBOX and Sent folders:

```bash
uv run {skill_directory}/scripts/email-summary.py
```

**Options:**

- `-v, --verbose` - Show himalaya commands being executed

Output includes:

- Rich table format with timestamps, senders, and subjects
- Categorized by folder (📥 INBOX, 📤 Sent)
- Unicode support (Finnish characters, emojis)

## Search Emails

Find emails by sender, subject, date range, or folder:

```bash
uv run {skill_directory}/scripts/email-search.py [options]
```

**Options:**

- `--folder FOLDER` - Folder to search (default: INBOX)
- `--from SENDER` - Filter by sender email/name (case-insensitive)
- `--subject TEXT` - Filter by subject text (case-insensitive)
- `--date-start DATE` - Start date (YYYY-MM-DD)
- `--date-end DATE` - End date (YYYY-MM-DD)
- `--limit N` - Maximum results (default: 20, capped at 100)
- `--no-limit` - Bypass the 100-result limit cap
- `-v, --verbose` - Show himalaya commands being executed
- `--help` - Show help message

All filters apply with AND logic. Results include message IDs for deletion. Dates must be in YYYY-MM-DD format. FROM filter matches both sender name and email address.

**Examples:**

```bash
# Search by sender
uv run {skill_directory}/scripts/email-search.py --from "spotify.com"

# Search by subject
uv run {skill_directory}/scripts/email-search.py --subject "invoice"

# Search by date range
uv run {skill_directory}/scripts/email-search.py --date-start "2025-12-17" --date-end "2025-12-31"

# Search in Sent folder
uv run {skill_directory}/scripts/email-search.py --folder Sent --limit 10

# Multiple filters
uv run {skill_directory}/scripts/email-search.py --from "@newsletter.com" --subject "unsubscribe" --limit 5

# Search with no limit
uv run {skill_directory}/scripts/email-search.py --limit 200 --no-limit
```

## Save Emails to File

Save email content to a file in various formats:

```bash
uv run {skill_directory}/scripts/email_save.py <message-id> [options]
```

**Options:**

- `--folder FOLDER` - Folder to search (default: INBOX)
- `--output PATH` - Output directory or file path (default: current directory)
- `--format FORMAT` - Output format: markdown, text, or json (default: markdown)
- `--date-prefix` - Add YYYY-MM-DD date prefix to filename (uses email date)
- `--no-download-attachments` - Skip downloading email attachments (default: attachments are downloaded)
- `--attachment-dir PATH` - Directory for attachments (default: current directory, same as email save location)
- `--overwrite` - Overwrite existing file without confirmation
- `-v, --verbose` - Show himalaya commands being executed
- `--help` - Show help message

## Post-Save Attachment Processing

After saving emails with `--download-attachments`, automatically inspect each attachment using vision capabilities:

1. **Use vision to analyze** each image attachment
2. **Classify** the content type (icon, logo, table, signature, complex image)
3. **Convert** to text representation where appropriate
4. **Update** the saved email file with replacements
5. **Delete** replaced attachment files

### Classification Guidelines

| Content Type              | Characteristics                            | Replacement Format                          |
| ------------------------- | ------------------------------------------ | ------------------------------------------- |
| **Icons/Emojis/Symbols**  | Small, single glyph, no text               | Unicode character (e.g., ✓, ★, →)           |
| **Logos**                 | Company/brand imagery, decorative          | Text description: `[Logo: Company Name]`    |
| **Signatures**            | Handwritten-style text, often at email end | Text: `[Signature: Name]` or extracted text |
| **Brief text**            | Very short text content (1-3 words)        | Extracted text verbatim                     |
| **Simple tables**         | Single-line cells, no images               | Markdown table                              |
| **Complex tables**        | Multi-line cells, no images                | ASCII table                                 |
| **Photos/Complex images** | Photographs, screenshots, diagrams         | **Keep unchanged**                          |

### Replacement Process

1. Read the saved email file
2. For each attachment reference in the file:
   a. Inspect the image using vision capability
   b. Determine if it can be replaced with text
   c. If yes: generate appropriate text representation
   d. If no: leave the attachment reference unchanged
3. Write updated content to the email file
4. Delete successfully replaced attachment files

### Example Conversions

**Icon → Unicode:**

```
Before: ![](attachments/checkmark.png)
After: ✓
```

**Simple table → Markdown:**

```markdown
| Header 1 | Header 2 |
| -------- | -------- |
| Value A  | Value B  |
```

**Complex table → ASCII:**

```
+------------+-----------+
| Header 1   | Header 2  |
+------------+-----------+
| Multi-line | Content   |
| cell here  | goes here |
+------------+-----------+
```

**Arguments:**

- `message-id` - Message ID to save (obtained from search results)

**Output formats:**

- **markdown**: Rich format with headers and metadata
- **text**: Plain text with basic headers
- **json**: Raw JSON output from himalaya (envelope + body data)

**Filename behavior:**

- Default: `{message-id}.{ext}`
- With `--date-prefix`: `{YYYY-MM-DD}-{subject-sanitized}.{ext}`
- Subject characters: Spaces and emojis preserved, slashes converted to dashes

**Examples:**

```bash
# Save as markdown to current directory (attachments downloaded by default)
uv run {skill_directory}/scripts/email_save.py 56873

# Save to specific directory (attachments downloaded by default)
uv run {skill_directory}/scripts/email_save.py 56873 --output ~/saved-emails

# Save with date prefix (attachments downloaded by default)
uv run {skill_directory}/scripts/email_save.py 56873 --date-prefix --output /tmp/emails

# Save as text format (attachments downloaded by default)
uv run {skill_directory}/scripts/email_save.py 56873 --format text

# Save as JSON (attachments downloaded by default)
uv run {skill_directory}/scripts/email_save.py 56873 --format json

# Save to specific file path (attachments downloaded by default)
uv run {skill_directory}/scripts/email_save.py 56873 --output ~/important-email.md

# Overwrite existing file without prompt
uv run {skill_directory}/scripts/email_save.py 56873 --overwrite --output ~/email.md

# Save from Sent folder (attachments downloaded by default)
uv run {skill_directory}/scripts/email_save.py --folder Sent 12345 --output ~/sent-emails

# Save without attachments
uv run {skill_directory}/scripts/email_save.py 56873 --no-download-attachments

# Save with attachments to custom directory (default behavior with custom dir)
uv run {skill_directory}/scripts/email_save.py 56873 --attachment-dir ~/attachments
```

## Save Email Workflow (Agent)

When user asks to save an email (attachments are downloaded by default):

1. Run `uv run {skill_directory}/scripts/email_save.py <id> --output <dir>` (attachments are downloaded automatically)
2. Read the list of downloaded attachments from output
3. For each image attachment:
   - Use `look_at` tool or other vision capabilities to inspect the image
   - Classify content and determine if it can be replaced with text
4. If any attachments were replaced:
   - Update the saved email file with text replacements
   - Delete the replaced attachment files
5. Report to user what was saved and what was converted

To skip attachment downloads, use `--no-download-attachments` flag.

### Attachment Classification

- **Replace with Unicode**: Icons, emojis, symbols, checkmarks, arrows
- **Replace with Markdown table**: Tables with single-line text cells
- **Replace with ASCII table**: Tables with multi-line text cells
- **Replace with text**: Very brief text (1-3 words), signatures
- **Keep unchanged**: Photos, screenshots, complex diagrams, charts

## ASCII Table Format

For complex tables with multi-line content, use this standardized format:

```
+------------+---------------+
| Column 1   | Column 2      |
+------------+---------------+
| Line 1     | Multi-line    |
| continues  | content here  |
+------------+---------------+
```

Key characteristics:

- Use `+` for corners
- Use `-` for horizontal lines
- Use `|` for vertical lines
- Column widths match content
- All cells must have aligned pipes

## Delete Emails

Delete emails by message ID with safety preview:

```bash
uv run {skill_directory}/scripts/email-delete.py <message-id> [options]
```

**Options:**

- `--folder FOLDER` - Folder to delete from (default: INBOX)
- `--execute` - Actually perform deletion (default: dry-run mode)
- `-v, --verbose` - Show himalaya commands being executed
- `--help` - Show help message

**Arguments:**

- `message-id` - Message ID to delete (obtained from search results)

**Safety:** Always run in dry-run mode first to verify the correct message.
In interactive mode, you'll be prompted for confirmation before deletion.
When called by OpenCode agent, deletion proceeds immediately with `--execute` flag.

**Examples:**

```bash
# Preview deletion
uv run {skill_directory}/scripts/email-delete.py 56838

# Actually delete (interactive - will prompt for confirmation)
uv run {skill_directory}/scripts/email-delete.py 56838 --execute

# Delete from specific folder
uv run {skill_directory}/scripts/email-delete.py --folder Sent 12345 --execute
```

## Translate Natural Language Queries

Interpret natural language queries as appropriate script calls:

**Summary queries:**

- "Show me today's emails" → email-summary.py
- "What emails did I get today?" → email-summary.py
- "Summary of recent emails" → email-summary.py

**Search queries:**

- "Find emails from Spotify" → email-search.py --from "spotify.com"
- "Show me emails about invoices" → email-search.py --subject "invoice"
- "Search for Atomikettu emails from the past two weeks" → email-search.py --from "atomikettu" --date-start "2025-12-17" --date-end "2025-12-31"
- "What did I send yesterday?" → email-search.py --folder Sent --date-start "2025-12-30" --date-end "2025-12-30"
- "Search INBOX for emails from john@example.com" → email-search.py --from "john@example.com"
- "Find emails with 'newsletter' in subject" → email-search.py --subject "newsletter"

**Save queries:**

- "Save email ID 56873" → `uv run {skill_directory}/scripts/email_save.py 56873`
- "Save as JSON" → `uv run {skill_directory}/scripts/email_save.py 56873 --format json`
- "Save to ~/emails folder with date prefix" → `uv run {skill_directory}/scripts/email_save.py 56873 --output ~/emails --date-prefix`

**Delete queries:**

- "Delete email ID 56838" → email-delete.py 56838 (show preview, ask for confirmation)
- "Remove the email from Spotify" → First search to find ID, then delete with confirmation

## Implementation Notes

**When calling scripts:**

1. Always invoke with `uv run {skill_directory}/scripts/<script-name>.py` (handles environment and deps, do NOT cd into skill directory)
2. For search by sender or subject, use --from and --subject flags
3. Date range uses --date-start and --date-end (YYYY-MM-DD format)
4. Case-insensitive search is automatic - don't worry about capitalization
5. FROM filter searches both sender name and email address
6. Always run delete operations in dry-run mode first without --execute flag
7. Ask user for confirmation before running delete with --execute flag (interactive mode only)
8. Use -v/--verbose to see himalaya commands being executed (for debugging)

**Avoid these pitfalls:**

- Don't use --since or --until (not implemented - use --date-start/--date-end)
- Don't try to search body content (only headers are available in JSON output)
- Don't forget to add --execute flag when actually deleting (dry-run by default)
- Don't use incorrect date format (must be YYYY-MM-DD)

**Follow this workflow for search and delete:**

1. Use email-search.py to find messages
2. Review results with user
3. Use email-delete.py <ID> to preview deletion
4. Get user confirmation
5. Use email-delete.py <ID> --execute to actually delete

**Technical context:**

- Backend: Himalaya v1.1.0 (Rust-based IMAP CLI tool) via Python 3.13 with typer and rich
- Installation: Himalaya must be installed on your system
- Output format: JSON → Rich tables with Python json.loads()
- Authentication: Keyring-based (managed by Himalaya)
- Protocol: IMAP over TLS (direct server communication)
- Date format: YYYY-MM-DD (ISO 8601)
- Case sensitivity: All search filters are case-insensitive using Python .lower()
- Agent detection: Uses sys.stdin.isatty() to determine if running interactively

## Using the Scripts

All scripts use PEP 723 inline metadata and require Python 3.13+.
Invoke with `uv run` using the absolute path to automatically handle Python environment and dependencies:

```bash
uv run {skill_directory}/scripts/<script-name>.py [options]
```

**Dependencies** (auto-managed by uv):

- typer - for CLI argument parsing
- rich - for beautiful terminal output
