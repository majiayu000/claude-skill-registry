---
name: gspace
description: Use gspace CLI and MCP tools for Google Workspace operations including Drive file management, Gmail, Docs, Sheets, Calendar, and Tasks with 40+ MCP tools available.
---
# Google Workspace (gspace) Skill

You are a Google Workspace specialist with access to both the gspace CLI and MCP (Model Context Protocol) tools. This skill provides comprehensive guidance for working with Google Drive, Gmail, Docs, Sheets, Calendar, and Tasks operations through both interfaces.

## MCP vs CLI: When to Use Each

### Use MCP Tools When:
- **In conversation with user**: MCP tools are available directly in Claude Code sessions
- **Reading metadata**: Checking file properties, permissions, comments
- **Searching content**: Finding files, emails, calendar events, tasks
- **Retrieving information**: Getting email content, file metadata, calendar events
- **Quick lookups**: Fast, single-operation queries
- **Parsing Excel files**: Reading .xlsx file contents
- **Modifying content**: Creating, updating, deleting files, emails, tasks, calendar events

### Use CLI When:
- **Complex workflows**: Multi-step operations requiring scripting
- **Batch operations**: Processing multiple items with shell scripts
- **File uploads/downloads**: Transferring large files to/from local system
- **Interactive operations**: Authentication flows, confirmations
- **Shell automation**: Integration with other command-line tools

## MCP Tools Complete Reference

### Authentication Tools

#### `mcp__gdrive__drive_check_auth`
Verify Google Drive authentication status and OAuth scopes.

```python
# No parameters required
mcp__gdrive__drive_check_auth()
```

**Returns:** Authentication status with account info and required scopes

**Use cases:**
- Verify authentication before file operations
- Diagnose access issues
- Confirm token validity

#### `mcp__gdrive__gmail_check_auth`
Verify Gmail API authentication and required scopes.

```python
mcp__gdrive__gmail_check_auth()
```

#### `mcp__gdrive__calendar_check_auth`
Verify Calendar API authentication and required scopes.

```python
mcp__gdrive__calendar_check_auth()
```

### Google Drive File Operations

#### `mcp__gdrive__drive_files_list`
List files with advanced filtering (owner, dates, type, folder).

**Parameters:**
- `query` (string, optional): Search query for file names
- `type` (string, optional): MIME type filter
- `folder` (string, optional): Search within specific folder ID
- `owner` (string, optional): Filter by file owner email
- `created_after` (string, optional): ISO date (YYYY-MM-DD)
- `created_before` (string, optional): ISO date
- `modified_after` (string, optional): ISO date
- `modified_before` (string, optional): ISO date
- `order_by` (string, optional): Sort order (e.g., "modifiedTime desc")
- `limit` (number, optional): Max results (1-100, default: 10)

```python
# Search by filename
mcp__gdrive__drive_files_list(query="report", limit=20)

# Search by owner and date
mcp__gdrive__drive_files_list(
    owner="user@example.com",
    modified_after="2025-01-01",
    order_by="modifiedTime desc"
)
```

#### `mcp__gdrive__drive_files_download`
Download file with format conversion (PDF, DOCX, XLSX, markdown).

**Parameters:**
- `file_id` (string, required): Google Drive file ID
- `local_path` (string, required): Local file system path
- `export_format` (string, optional): Export format (text, csv, xlsx, pdf, docx, markdown)
- `tab_id` (string, optional): Specific tab ID for multi-tab Docs
- `max_size` (number, optional): Max file size in bytes
- `timeout` (number, optional): Download timeout in milliseconds

```python
# Download Google Doc as markdown
mcp__gdrive__drive_files_download(
    file_id="abc123",
    local_path="/tmp/document.md",
    export_format="markdown"
)

# Download Google Sheet as Excel (preserves all sheets)
mcp__gdrive__drive_files_download(
    file_id="sheet123",
    local_path="/tmp/data.xlsx",
    export_format="xlsx"
)
```

#### `mcp__gdrive__drive_files_upload`
Upload local files with automatic CSV→Sheets conversion.

**Parameters:**
- `local_path` (string, required): Path to local file
- `name` (string, optional): Name in Drive (defaults to filename)
- `parent_folder_id` (string, optional): Parent folder ID
- `description` (string, optional): File description
- `convert_to_google_format` (boolean, optional): Convert CSV to Sheets
- `mime_type` (string, optional): MIME type (auto-detected)

```python
# Upload CSV and convert to Google Sheet
mcp__gdrive__drive_files_upload(
    local_path="/tmp/data.csv",
    name="Sales Data 2025",
    convert_to_google_format=True
)
```

#### `mcp__gdrive__drive_files_copy`
Create file/folder copies with optional renaming.

**Parameters:**
- `file_id` (string, required): ID of file to copy
- `name` (string, optional): Name for copy
- `parent_folder_id` (string, optional): Destination folder

```python
mcp__gdrive__drive_files_copy(
    file_id="abc123",
    name="Backup Copy",
    parent_folder_id="folder456"
)
```

#### `mcp__gdrive__drive_files_rename`
Rename files and folders.

**Parameters:**
- `file_id` (string, required): ID of file to rename
- `name` (string, required): New name

```python
mcp__gdrive__drive_files_rename(
    file_id="abc123",
    name="Updated Document Name"
)
```

#### `mcp__gdrive__drive_files_delete`
Delete files/folders (trash or permanent).

**Parameters:**
- `file_id` (string, required): ID of file to delete
- `permanently` (boolean, optional): Permanent delete vs trash (default: false)

```python
# Move to trash
mcp__gdrive__drive_files_delete(file_id="abc123")

# Permanently delete
mcp__gdrive__drive_files_delete(file_id="abc123", permanently=True)
```

#### `mcp__gdrive__drive_files_metadata`
Get comprehensive file metadata.

**Parameters:**
- `file_id` (string, required): File ID

```python
mcp__gdrive__drive_files_metadata(file_id="abc123")
```

**Returns:** Name, size, mimeType, created/modified times, owner, sharing settings

#### `mcp__gdrive__drive_files_validate_markdown`
Validate Google Docs export to markdown compatibility.

**Parameters:**
- `file_id` (string, required): Google Doc file ID

```python
mcp__gdrive__drive_files_validate_markdown(file_id="doc123")
```

**Returns:** Compatibility score and recommendations

#### `mcp__gdrive__drive_files_list_tabs`
List all tabs in a Google Doc (experimental API).

**Parameters:**
- `file_id` (string, required): Google Doc file ID

```python
mcp__gdrive__drive_files_list_tabs(file_id="doc123")
```

### Google Drive Folder Operations

#### `mcp__gdrive__drive_folders_create`
Create folders with optional descriptions.

**Parameters:**
- `name` (string, required): Folder name
- `parent_folder_id` (string, optional): Parent folder ID
- `description` (string, optional): Folder description

```python
mcp__gdrive__drive_folders_create(
    name="Project Documents",
    description="All project files"
)
```

#### `mcp__gdrive__drive_folders_move`
Move files/folders between locations.

**Parameters:**
- `file_id` (string, required): ID of file/folder to move
- `new_parent_folder_id` (string, required): Destination folder ID
- `remove_from_current_parents` (boolean, optional): Remove from current parents (default: true)

```python
mcp__gdrive__drive_folders_move(
    file_id="abc123",
    new_parent_folder_id="folder456"
)
```

### Permissions Management

#### `mcp__gdrive__permissions_grant`
Grant user/group/domain access to files.

**Parameters:**
- `file_id` (string, required): File ID
- `role` (string, required): reader, writer, commenter, owner
- `type` (string, required): user, group, domain, anyone
- `email` (string, optional): Email address (for user/group)
- `domain` (string, optional): Domain name or "current"

```python
# Grant write access to user
mcp__gdrive__permissions_grant(
    file_id="abc123",
    role="writer",
    type="user",
    email="user@example.com"
)

# Share with entire domain
mcp__gdrive__permissions_grant(
    file_id="abc123",
    role="reader",
    type="domain",
    domain="current"
)
```

#### `mcp__gdrive__permissions_list`
List current file/folder permissions.

**Parameters:**
- `file_id` (string, required): File ID

```python
mcp__gdrive__permissions_list(file_id="abc123")
```

**Returns:** List of permissions with roles and email addresses

#### `mcp__gdrive__permissions_update`
Modify existing permission roles.

**Parameters:**
- `file_id` (string, required): File ID
- `permission_id` (string, required): Permission ID
- `role` (string, required): New role (reader, writer, commenter)

```python
mcp__gdrive__permissions_update(
    file_id="abc123",
    permission_id="perm456",
    role="commenter"
)
```

#### `mcp__gdrive__permissions_revoke`
Remove user/group access.

**Parameters:**
- `file_id` (string, required): File ID
- `permission_id` (string, required): Permission ID to remove

```python
mcp__gdrive__permissions_revoke(
    file_id="abc123",
    permission_id="perm456"
)
```

### Google Docs Operations

#### `mcp__gdrive__docs_create`
Create Google Docs from markdown files.

**Parameters:**
- `local_path` (string, required): Path to markdown file
- `name` (string, required): Document name
- `parent_folder_id` (string, optional): Parent folder ID

```python
mcp__gdrive__docs_create(
    local_path="/tmp/notes.md",
    name="Meeting Notes",
    parent_folder_id="folder123"
)
```

#### `mcp__gdrive__docs_download`
Download Docs as markdown with footnote conversion.

**Parameters:**
- `file_id` (string, required): Google Doc file ID
- `local_path` (string, required): Output path
- `export_format` (string, optional): Export format (markdown, pdf, docx)

```python
mcp__gdrive__docs_download(
    file_id="doc123",
    local_path="/tmp/document.md",
    export_format="markdown"
)
```

#### `mcp__gdrive__docs_apply_text_diff`
Update document content remotely without downloading.

**Parameters:**
- `file_id` (string, required): Google Doc file ID
- `new_content` (string, required): New text content
- `preserve_formatting` (boolean, optional): Keep formatting (default: true)

```python
mcp__gdrive__docs_apply_text_diff(
    file_id="doc123",
    new_content="Updated document text...",
    preserve_formatting=True
)
```

#### `mcp__gdrive__docs_find_replace`
Find and replace text with case-sensitive/insensitive matching.

**Parameters:**
- `file_id` (string, required): Google Doc file ID
- `find_text` (string, required): Text to find
- `replace_text` (string, required): Replacement text
- `match_case` (boolean, optional): Case-sensitive (default: false)
- `tab_id` (string, optional): Specific tab ID

```python
# Case-insensitive replacement
mcp__gdrive__docs_find_replace(
    file_id="doc123",
    find_text="TODO",
    replace_text="DONE"
)

# Case-sensitive replacement
mcp__gdrive__docs_find_replace(
    file_id="doc123",
    find_text="Error",
    replace_text="Warning",
    match_case=True
)
```

### Google Docs Comments

#### `mcp__gdrive__docs_comments_list`
List all comments on a document.

**Parameters:**
- `file_id` (string, required): File ID
- `include_deleted` (boolean, optional): Include deleted comments
- `page_size` (number, optional): Results per page (1-100)
- `page_token` (string, optional): Pagination token

```python
mcp__gdrive__docs_comments_list(
    file_id="doc123",
    page_size=50
)
```

#### `mcp__gdrive__docs_comments_get`
Get specific comment details.

**Parameters:**
- `file_id` (string, required): File ID
- `comment_id` (string, required): Comment ID
- `include_deleted` (boolean, optional): Include deleted replies

```python
mcp__gdrive__docs_comments_get(
    file_id="doc123",
    comment_id="comment456"
)
```

#### `mcp__gdrive__docs_comments_create`
Add new comments to documents.

**Parameters:**
- `file_id` (string, required): File ID
- `content` (string, required): Comment text
- `anchor` (string, optional): Anchor region for specific text

```python
# General comment
mcp__gdrive__docs_comments_create(
    file_id="doc123",
    content="Please review this section"
)
```

#### `mcp__gdrive__docs_comments_reply`
Reply to existing comments.

**Parameters:**
- `file_id` (string, required): File ID
- `comment_id` (string, required): Comment ID
- `content` (string, required): Reply text
- `action` (string, optional): "resolve" or "reopen"

```python
# Reply and resolve
mcp__gdrive__docs_comments_reply(
    file_id="doc123",
    comment_id="comment456",
    content="Fixed, thanks!",
    action="resolve"
)
```

#### `mcp__gdrive__docs_comments_resolve`
Mark comment as resolved.

**Parameters:**
- `file_id` (string, required): File ID
- `comment_id` (string, required): Comment ID

```python
mcp__gdrive__docs_comments_resolve(
    file_id="doc123",
    comment_id="comment456"
)
```

### Google Sheets Operations

#### `mcp__gdrive__sheets_create`
Create sheets with initial headers and data.

**Parameters:**
- `name` (string, required): Spreadsheet name
- `parent_folder_id` (string, optional): Parent folder ID
- `headers` (array, optional): Column headers
- `data` (2D array, optional): Initial data rows

```python
mcp__gdrive__sheets_create(
    name="Customer Database",
    headers=["Name", "Email", "Status"],
    data=[
        ["John Doe", "john@example.com", "Active"],
        ["Jane Smith", "jane@example.com", "Pending"]
    ]
)
```

#### `mcp__gdrive__sheets_update`
Modify specific cells using A1 notation with formula support.

**Parameters:**
- `file_id` (string, required): Spreadsheet ID
- `range` (string, required): A1 notation (e.g., "Sheet1!A1:C3")
- `values` (2D array, required): Cell values
- `input_option` (string, optional): "RAW" or "USER_ENTERED" (default)

```python
# Update with formulas
mcp__gdrive__sheets_update(
    file_id="sheet123",
    range="A1:B2",
    values=[
        ["Product", "Price"],
        ["Widget", "=SUM(B3:B10)"]
    ],
    input_option="USER_ENTERED"
)
```

#### `mcp__gdrive__sheets_append`
Append rows to end of data without range calculation.

**Parameters:**
- `file_id` (string, required): Spreadsheet ID
- `values` (2D array, required): Rows to append
- `range` (string, optional): Starting range (default: "Sheet1!A1")
- `input_option` (string, optional): "RAW" or "USER_ENTERED"

```python
mcp__gdrive__sheets_append(
    file_id="sheet123",
    values=[
        ["New Customer", "new@example.com", "Active"],
        ["Another Customer", "another@example.com", "Pending"]
    ]
)
```

### Google Calendar Operations

#### `mcp__gdrive__calendar_list`
List events with time range filtering and privacy controls.

**Parameters:**
- `calendar_id` (string, optional): Calendar ID (default: "primary")
- `time_min` (string, optional): Start time (RFC3339 format)
- `time_max` (string, optional): End time (RFC3339 format)
- `max_results` (number, optional): Max events (1-2500, default: 50)
- `page_token` (string, optional): Pagination token
- `single_events` (boolean, optional): Expand recurring events (default: true)
- `include_attendees` (boolean, optional): Include attendees (default: false)
- `include_description` (boolean, optional): Include description (default: false)
- `include_location` (boolean, optional): Include location (default: false)

```python
# List this month's events
mcp__gdrive__calendar_list(
    time_min="2025-01-01T00:00:00Z",
    time_max="2025-01-31T23:59:59Z",
    max_results=50
)
```

#### `mcp__gdrive__calendar_search`
Search events by text query with advanced filters.

**Parameters:**
- `q` (string, optional): Free-text search query
- `calendar_id` (string, optional): Calendar ID (default: "primary")
- `time_min` (string, optional): Start time
- `time_max` (string, optional): End time
- `max_results` (number, optional): Max results (1-2500)

```python
mcp__gdrive__calendar_search(
    q="team meeting",
    time_min="2025-01-01T00:00:00Z",
    max_results=10
)
```

#### `mcp__gdrive__calendar_create`
Create events with recurrence support.

**Parameters:**
- `summary` (string, required): Event title
- `start` (string, required): Start time (RFC3339)
- `end` (string, required): End time (RFC3339)
- `calendar_id` (string, optional): Calendar ID
- `description` (string, optional): Event description
- `location` (string, optional): Event location
- `recurrence` (object, optional): Recurrence pattern

```python
# Create single event
mcp__gdrive__calendar_create(
    summary="Sprint Planning",
    start="2025-11-10T14:00:00Z",
    end="2025-11-10T15:00:00Z"
)

# Create recurring event
mcp__gdrive__calendar_create(
    summary="Daily Standup",
    start="2025-11-10T09:00:00Z",
    end="2025-11-10T09:15:00Z",
    recurrence={"frequency": "daily", "count": 30}
)
```

#### `mcp__gdrive__calendar_update`
Modify existing calendar events.

**Parameters:**
- `event_id` (string, required): Event ID
- `calendar_id` (string, optional): Calendar ID
- `summary` (string, optional): New title
- `start` (string, optional): New start time
- `end` (string, optional): New end time
- `description` (string, optional): New description

```python
mcp__gdrive__calendar_update(
    event_id="event123",
    summary="Updated Meeting Title",
    start="2025-11-10T15:00:00Z"
)
```

#### `mcp__gdrive__calendar_delete`
Remove events from calendar.

**Parameters:**
- `event_id` (string, required): Event ID
- `calendar_id` (string, optional): Calendar ID

```python
mcp__gdrive__calendar_delete(event_id="event123")
```

#### `mcp__gdrive__calendar_update_reminders`
Modify event reminder settings.

**Parameters:**
- `event_id` (string, required): Event ID
- `calendar_id` (string, optional): Calendar ID
- `use_default` (boolean, required): Use calendar defaults
- `overrides` (array, optional): Custom reminders (method, minutes)
- `send_updates` (string, optional): "none", "all", "externalOnly"

```python
# Disable all reminders
mcp__gdrive__calendar_update_reminders(
    event_id="event123",
    use_default=False,
    overrides=[]
)

# Set custom reminders
mcp__gdrive__calendar_update_reminders(
    event_id="event123",
    use_default=False,
    overrides=[
        {"method": "popup", "minutes": 10},
        {"method": "email", "minutes": 60}
    ]
)
```

### Gmail Operations

#### `mcp__gdrive__gmail_search`
Search messages with advanced query syntax.

**Parameters:**
- `query` (string, required): Gmail search query
- `max_results` (number, optional): Max messages to return

```python
# Search by sender and subject
mcp__gdrive__gmail_search(
    query="from:boss@company.com subject:urgent",
    max_results=10
)

# Search for attachments
mcp__gdrive__gmail_search(
    query="has:attachment after:2025/01/01"
)
```

#### `mcp__gdrive__gmail_get`
Get full message content with headers.

**Parameters:**
- `message_id` (string, required): Gmail message ID

```python
mcp__gdrive__gmail_get(message_id="msg123")
```

**Returns:** Complete message with headers, body, attachments metadata

#### `mcp__gdrive__gmail_thread`
Get entire conversation thread.

**Parameters:**
- `thread_id` (string, required): Gmail thread ID

```python
mcp__gdrive__gmail_thread(thread_id="thread123")
```

#### `mcp__gdrive__gmail_send`
Send new messages with attachments.

**Parameters:**
- `to` (string, required): Recipient email(s)
- `subject` (string, required): Email subject
- `body` (string, required): Message body
- `cc` (string, optional): CC recipients
- `bcc` (string, optional): BCC recipients
- `attachments` (array, optional): File paths to attach

```python
mcp__gdrive__gmail_send(
    to="user@example.com",
    subject="Project Update",
    body="Please find the attached report.",
    attachments=["/tmp/report.pdf"]
)
```

#### `mcp__gdrive__gmail_draft`
Create draft messages.

**Parameters:**
- `to` (string, required): Recipient email
- `subject` (string, required): Email subject
- `body` (string, required): Message body

```python
mcp__gdrive__gmail_draft(
    to="team@example.com",
    subject="Draft: Review Request",
    body="Please review this document..."
)
```

#### `mcp__gdrive__gmail_send_draft`
Send existing drafts.

**Parameters:**
- `draft_id` (string, required): Draft ID

```python
mcp__gdrive__gmail_send_draft(draft_id="draft123")
```

#### `mcp__gdrive__gmail_list_labels`
List all Gmail labels.

```python
# No parameters required
mcp__gdrive__gmail_list_labels()
```

#### `mcp__gdrive__gmail_label`
Add/remove labels on messages.

**Parameters:**
- `message_id` (string, required): Message ID
- `add_labels` (array, optional): Labels to add
- `remove_labels` (array, optional): Labels to remove

```python
mcp__gdrive__gmail_label(
    message_id="msg123",
    add_labels=["IMPORTANT"],
    remove_labels=["INBOX"]
)
```

#### `mcp__gdrive__gmail_archive`
Archive messages (remove from inbox).

**Parameters:**
- `message_id` (string, required): Message ID

```python
mcp__gdrive__gmail_archive(message_id="msg123")
```

#### `mcp__gdrive__gmail_star`
Star/unstar messages.

**Parameters:**
- `message_id` (string, required): Message ID
- `unstar` (boolean, optional): Unstar message (default: false)

```python
# Star message
mcp__gdrive__gmail_star(message_id="msg123")

# Unstar message
mcp__gdrive__gmail_star(message_id="msg123", unstar=True)
```

#### `mcp__gdrive__gmail_trash`
Move messages to trash.

**Parameters:**
- `message_id` (string, required): Message ID

```python
mcp__gdrive__gmail_trash(message_id="msg123")
```

#### `mcp__gdrive__gmail_delete`
Permanently delete messages.

**Parameters:**
- `message_id` (string, required): Message ID

```python
mcp__gdrive__gmail_delete(message_id="msg123")
```

#### `mcp__gdrive__gmail_download_attachment`
Download message attachments.

**Parameters:**
- `message_id` (string, required): Message ID
- `attachment_id` (string, required): Attachment ID
- `output_path` (string, required): Local output path

```python
mcp__gdrive__gmail_download_attachment(
    message_id="msg123",
    attachment_id="attach456",
    output_path="/tmp/document.pdf"
)
```

### Google Tasks Operations

#### `mcp__gdrive__tasks_list_lists`
List all task lists.

```python
# No parameters required
mcp__gdrive__tasks_list_lists()
```

#### `mcp__gdrive__tasks_get_list`
Get specific task list details.

**Parameters:**
- `task_list_id` (string, required): Task list ID

```python
mcp__gdrive__tasks_get_list(task_list_id="list123")
```

#### `mcp__gdrive__tasks_list`
List tasks in a task list.

**Parameters:**
- `task_list_id` (string, required): Task list ID
- `show_completed` (boolean, optional): Include completed tasks
- `show_deleted` (boolean, optional): Include deleted tasks
- `show_hidden` (boolean, optional): Include hidden tasks

```python
mcp__gdrive__tasks_list(
    task_list_id="list123",
    show_completed=True
)
```

#### `mcp__gdrive__tasks_get`
Get specific task details.

**Parameters:**
- `task_list_id` (string, required): Task list ID
- `task_id` (string, required): Task ID

```python
mcp__gdrive__tasks_get(
    task_list_id="list123",
    task_id="task456"
)
```

#### `mcp__gdrive__tasks_create_list`
Create new task lists.

**Parameters:**
- `title` (string, required): Task list title

```python
mcp__gdrive__tasks_create_list(title="Q1 Goals")
```

#### `mcp__gdrive__tasks_create`
Create new tasks with due dates.

**Parameters:**
- `task_list_id` (string, required): Task list ID
- `title` (string, required): Task title
- `notes` (string, optional): Task notes
- `due` (string, optional): Due date (RFC3339)
- `parent` (string, optional): Parent task ID

```python
mcp__gdrive__tasks_create(
    task_list_id="list123",
    title="Review PR #42",
    due="2025-11-10T17:00:00Z",
    notes="High priority"
)
```

#### `mcp__gdrive__tasks_update`
Modify existing tasks.

**Parameters:**
- `task_list_id` (string, required): Task list ID
- `task_id` (string, required): Task ID
- `title` (string, optional): New title
- `notes` (string, optional): New notes
- `due` (string, optional): New due date
- `status` (string, optional): "needsAction" or "completed"

```python
mcp__gdrive__tasks_update(
    task_list_id="list123",
    task_id="task456",
    title="Updated Task Title",
    status="completed"
)
```

#### `mcp__gdrive__tasks_complete`
Mark tasks as completed.

**Parameters:**
- `task_list_id` (string, required): Task list ID
- `task_id` (string, required): Task ID

```python
mcp__gdrive__tasks_complete(
    task_list_id="list123",
    task_id="task456"
)
```

#### `mcp__gdrive__tasks_delete`
Delete tasks.

**Parameters:**
- `task_list_id` (string, required): Task list ID
- `task_id` (string, required): Task ID

```python
mcp__gdrive__tasks_delete(
    task_list_id="list123",
    task_id="task456"
)
```

#### `mcp__gdrive__tasks_clear_completed`
Clear all completed tasks from a list.

**Parameters:**
- `task_list_id` (string, required): Task list ID

```python
mcp__gdrive__tasks_clear_completed(task_list_id="list123")
```

### XLSX File Operations

#### `mcp__gdrive__parse_xlsx`
Parse Excel (.xlsx) file contents.

**Parameters:**
- `file_id` (string, required): Google Drive file ID of .xlsx file

```python
mcp__gdrive__parse_xlsx(file_id="spreadsheet123")
```

**Returns:** Structured data from Excel file (sheets, rows, columns)

#### `mcp__gdrive__write_xlsx`
Create XLSX file from JSON workbook structure.

**Parameters:**
- `workbook` (object, required): Workbook structure with sheets array
- `file_path` (string, required): Absolute path where XLSX should be created

```python
mcp__gdrive__write_xlsx(
    workbook={
        "sheets": [
            {
                "name": "Q1 Budget",
                "data": [
                    ["Category", "Amount"],
                    ["Salaries", 150000],
                    ["Marketing", 75000]
                ],
                "formulas": {
                    "B4": "=SUM(B2:B3)"
                }
            }
        ]
    },
    file_path="/tmp/output.xlsx"
)
```

## CLI Operations Reference

### Authentication

```bash
# Check authentication status
gspace auth check

# Login (interactive)
gspace auth login
```

### Drive File Operations

```bash
# List files
gspace drive files ls
gspace drive files ls --owner user@example.com --limit 20

# Download files
gspace drive files download FILE_ID /tmp/document.pdf
gspace drive files download FILE_ID /tmp/doc.md --export markdown

# Upload files
gspace drive files upload /path/to/file "File Name"
gspace drive files upload data.csv "Spreadsheet" --convert

# Copy, rename, delete
gspace drive files copy FILE_ID --name "Copy of Document"
gspace drive files rename FILE_ID "New Name"
gspace drive files delete FILE_ID

# Get metadata
gspace drive files metadata FILE_ID
```

### Drive Folders

```bash
# Create folder
gspace drive folders create "Project Documents"

# Move file to folder
gspace drive folders move FILE_ID FOLDER_ID
```

### Permissions

```bash
# Grant permission
gspace permissions grant FILE_ID --type user --role writer --email user@example.com
gspace permissions grant FILE_ID --type domain --role reader --domain current

# List permissions
gspace permissions list FILE_ID

# Update permission
gspace permissions update FILE_ID PERMISSION_ID --role commenter

# Revoke permission
gspace permissions revoke FILE_ID PERMISSION_ID
```

### Google Docs

```bash
# Create doc from markdown
gspace docs create /path/to/notes.md "Document Title"

# Download doc
gspace docs download DOC_ID /tmp/output.md --export markdown

# Find and replace
gspace docs find-replace DOC_ID "old text" "new text"
gspace docs find-replace DOC_ID "Error" "Warning" --match-case

# Comments
gspace docs comments list DOC_ID
gspace docs comments create DOC_ID "Great work!"
gspace docs comments reply DOC_ID COMMENT_ID "Thanks!"
gspace docs comments resolve DOC_ID COMMENT_ID
```

### Google Sheets

```bash
# Create sheet
gspace sheets create "Sales Data" --headers "Product,Price,Quantity"

# Update cells
gspace sheets update SHEET_ID --range "A1:B2" --values '[["Name","Value"],["Item",100]]'

# Append rows
gspace sheets append SHEET_ID --values '[["New Row 1","Value 1"]]'
```

### Google Calendar

```bash
# List events
gspace calendar list --time-min 2025-01-01T00:00:00Z
gspace calendar today
gspace calendar tomorrow

# Search events
gspace calendar search --query "team meeting"

# Create event
gspace calendar create "Sprint Planning" --start "2025-11-10T14:00:00Z" --end "2025-11-10T15:00:00Z"

# Update/delete events
gspace calendar update EVENT_ID --summary "New Title"
gspace calendar delete EVENT_ID

# Update reminders
gspace calendar update-reminders EVENT_ID --disable
```

### Gmail

```bash
# Search emails
gspace gmail search --query "from:boss@company.com subject:urgent"

# Get message/thread
gspace gmail get MESSAGE_ID
gspace gmail thread THREAD_ID

# Send email
gspace gmail send --to user@example.com --subject "Hello" --body "Message"
gspace gmail send --to user@example.com --subject "Report" --attach report.pdf

# Draft management
gspace gmail draft --to team@example.com --subject "Review"
gspace gmail send-draft DRAFT_ID

# Message management
gspace gmail archive MESSAGE_ID
gspace gmail star MESSAGE_ID
gspace gmail trash MESSAGE_ID
gspace gmail delete MESSAGE_ID
gspace gmail label MESSAGE_ID --add IMPORTANT --remove INBOX

# Labels
gspace gmail list-labels

# Download attachment
gspace gmail download-attachment MESSAGE_ID ATTACHMENT_ID /tmp/file.pdf
```

### Google Tasks

```bash
# List task lists
gspace tasks list-lists

# List tasks
gspace tasks list TASK_LIST_ID
gspace tasks list TASK_LIST_ID --show-completed

# Create task
gspace tasks create TASK_LIST_ID "Review PR" --due "2025-11-10T17:00:00Z"

# Update/complete/delete task
gspace tasks update TASK_LIST_ID TASK_ID --title "Updated Title"
gspace tasks complete TASK_LIST_ID TASK_ID
gspace tasks delete TASK_LIST_ID TASK_ID

# Clear completed
gspace tasks clear-completed TASK_LIST_ID
```

## Common Workflows

### Workflow 1: Find and Download Documents (MCP)

```python
# 1. Search for documents
files = mcp__gdrive__drive_files_list(
    query="Q4 report",
    type="application/vnd.google-apps.document",
    limit=10
)

# 2. Download as markdown
mcp__gdrive__drive_files_download(
    file_id=files[0].id,
    local_path="/tmp/report.md",
    export_format="markdown"
)
```

### Workflow 2: Email Task Management (MCP)

```python
# 1. Search for emails with actionable items
messages = mcp__gdrive__gmail_search(
    query="subject:TODO is:unread",
    max_results=20
)

# 2. Create tasks from emails
for message in messages:
    email = mcp__gdrive__gmail_get(message_id=message.id)

    # Create task
    mcp__gdrive__tasks_create(
        task_list_id="default",
        title=f"Follow up: {email.subject}",
        notes=email.snippet
    )

    # Archive email
    mcp__gdrive__gmail_archive(message_id=message.id)
```

### Workflow 3: Calendar Event Cleanup (MCP)

```python
# 1. Search for "do not block" events
events = mcp__gdrive__calendar_search(
    q="do not block",
    time_min="2025-01-01T00:00:00Z"
)

# 2. Disable reminders for each event
for event in events:
    mcp__gdrive__calendar_update_reminders(
        event_id=event.id,
        use_default=False,
        overrides=[]
    )
```

### Workflow 4: Bulk File Permissions (CLI)

```bash
# Share all PDFs in folder with team
gspace drive files ls --folder-id FOLDER_ID --type application/pdf --json | \
  jq -r '.[].id' | \
  while read file_id; do
    gspace permissions grant "$file_id" --type domain --role reader --domain current
  done
```

### Workflow 5: Email Backup (CLI)

```bash
# Download all attachments from specific sender
gspace gmail search --query "from:vendor@example.com has:attachment" --json | \
  jq -r '.[].id' | \
  while read msg_id; do
    gspace gmail get "$msg_id" --json | \
      jq -r '.attachments[].id' | \
      while read attach_id; do
        gspace gmail download-attachment "$msg_id" "$attach_id" "/tmp/backup_${attach_id}.pdf"
      done
  done
```

## Best Practices

### General Principles

1. **Prefer MCP for programmatic operations**: MCP tools provide structured responses
2. **Use CLI for interactive workflows**: Better for shell scripts and automation
3. **Batch operations carefully**: Use pagination and limits to avoid overwhelming responses
4. **Check authentication first**: Use `*_check_auth` tools before operations
5. **Handle errors gracefully**: All MCP tools return error details in responses

### MCP-Specific Best Practices

1. **Use appropriate limits**: Set `limit` or `max_results` to avoid large responses
2. **Leverage filters**: Use owner, date, type filters to narrow searches
3. **Parse responses**: All MCP tools return structured JSON
4. **Privacy controls**: Use calendar privacy flags to minimize PII exposure
5. **Pagination**: Use `page_token` for large result sets

### CLI-Specific Best Practices

1. **JSON output for scripting**: Use `--json` flag with `jq` for processing
2. **Confirm destructive operations**: CLI prompts for confirmations by default
3. **Use environment variables**: Set `GOOGLE_CLOUD_PROJECT` for quota management
4. **Batch with shell loops**: Combine CLI with shell scripts for bulk operations

## Search Query Syntax

### Drive Queries

- `name contains 'text'` - Search by filename
- `fullText contains 'text'` - Search file contents
- `mimeType = 'application/pdf'` - Filter by file type
- `'folder-id' in parents` - Files in specific folder
- `trashed = false` - Exclude trashed files
- `modifiedTime > '2025-01-01T00:00:00'` - Modified after date

**Common MIME types:**
- Google Docs: `application/vnd.google-apps.document`
- Google Sheets: `application/vnd.google-apps.spreadsheet`
- Google Slides: `application/vnd.google-apps.presentation`
- PDF: `application/pdf`

### Gmail Queries

- `from:sender@example.com` - From specific sender
- `to:recipient@example.com` - To specific recipient
- `subject:keyword` - Subject contains keyword
- `has:attachment` - Has attachments
- `filename:pdf` - Specific attachment type
- `after:2025/01/01` - Date filters
- `before:2025/12/31` - Date filters
- `is:unread` - Unread messages
- `is:starred` - Starred messages
- `label:IMPORTANT` - Specific label

## Error Handling

### Common Errors

**Authentication Errors:**
```python
# Check auth status
mcp__gdrive__drive_check_auth()
```

**File Not Found:**
```python
# Verify file exists
try:
    metadata = mcp__gdrive__drive_files_metadata(file_id="abc123")
except:
    # Handle missing file
    pass
```

**Permission Denied:**
```bash
# Re-authenticate with proper scopes
gcloud auth login --enable-gdrive-access
```

## Quick Reference

### MCP Tools by Category

**Authentication:**
- `drive_check_auth`, `gmail_check_auth`, `calendar_check_auth`

**Drive Files:**
- `drive_files_list`, `drive_files_download`, `drive_files_upload`
- `drive_files_copy`, `drive_files_rename`, `drive_files_delete`
- `drive_files_metadata`, `drive_files_validate_markdown`, `drive_files_list_tabs`

**Drive Folders:**
- `drive_folders_create`, `drive_folders_move`

**Permissions:**
- `permissions_grant`, `permissions_list`, `permissions_update`, `permissions_revoke`

**Docs:**
- `docs_create`, `docs_download`, `docs_apply_text_diff`, `docs_find_replace`

**Docs Comments:**
- `docs_comments_list`, `docs_comments_get`, `docs_comments_create`
- `docs_comments_reply`, `docs_comments_resolve`

**Sheets:**
- `sheets_create`, `sheets_update`, `sheets_append`

**Calendar:**
- `calendar_list`, `calendar_search`, `calendar_create`
- `calendar_update`, `calendar_delete`, `calendar_update_reminders`

**Gmail:**
- `gmail_search`, `gmail_get`, `gmail_thread`
- `gmail_send`, `gmail_draft`, `gmail_send_draft`
- `gmail_list_labels`, `gmail_label`, `gmail_archive`, `gmail_star`
- `gmail_trash`, `gmail_delete`, `gmail_download_attachment`

**Tasks:**
- `tasks_list_lists`, `tasks_get_list`, `tasks_list`, `tasks_get`
- `tasks_create_list`, `tasks_create`, `tasks_update`
- `tasks_complete`, `tasks_delete`, `tasks_clear_completed`

**XLSX:**
- `parse_xlsx`, `write_xlsx`

## Summary

**Total MCP Tools:** 40+ comprehensive Google Workspace operations

**Use MCP tools for:**
- All CRUD operations (Create, Read, Update, Delete)
- Searching and filtering content
- Managing permissions and access control
- Email, calendar, and task management
- Document editing and collaboration
- Spreadsheet data manipulation

**Use CLI for:**
- Interactive authentication flows
- Shell script automation
- Batch operations with pipes
- Human-readable output formatting
- Quick shortcuts (calendar today/tomorrow)

**Key advantages:**
- **MCP**: Structured responses, programmatic access, direct integration
- **CLI**: Scriptable, interactive, human-friendly, shell integration
