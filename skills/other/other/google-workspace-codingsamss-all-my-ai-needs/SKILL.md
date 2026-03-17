---
name: google-workspace
description: "Google Workspace read-only via gogcli: Gmail, Drive, Docs, Sheets, Slides, Calendar, Contacts, Tasks, Keep. 查邮件、文件、文档、表格、日程、联系人、任务、笔记。Keywords: gmail email 邮件 drive 云盘 docs sheets calendar 日历 tasks 任务 keep 笔记 gog"
---

# Google Workspace Skill (Read-Only)

Access Google Workspace services from the terminal using gogcli (`gog`). This skill only exposes read-only and safe operations to protect your Google account data.

## Prerequisites

1. gogcli must be installed: `brew install steipete/tap/gogcli`
2. OAuth credentials must be configured (see First-Time Setup below)
3. Run `gog auth status` to verify authentication

## First-Time Setup

1. **Create OAuth credentials** at [Google Cloud Console](https://console.cloud.google.com/apis/credentials):
   - Create a project, enable the APIs you need
   - Create an OAuth 2.0 Client ID (Desktop app type)
   - Download the JSON file

2. **Store credentials:**
   ```bash
   gog auth credentials ~/Downloads/client_secret_*.json
   ```

3. **Authorize your account (choose one):**
   ```bash
   # Recommended: read-only for all services this skill uses
   gog auth add you@gmail.com --services gmail,drive,docs,sheets,slides,calendar,contacts,tasks,keep,people --readonly

   # Minimal: only core services
   gog auth add you@gmail.com --services gmail,drive,calendar,contacts --readonly
   ```

4. **Verify:**
   ```bash
   gog auth status
   ```

5. **Check authorized services:**
   ```bash
   gog auth services
   ```
   Confirm the output includes all services you need. Re-run `auth add` to add missing ones.

## Common Flags

All commands support these flags:
- `--json` / `-j` - JSON output (structured parsing)
- `--plain` / `-p` - TSV output (simple parsing)
- `--account <email>` - Select account (if multiple configured)
- `--max N` - Limit number of results

## Commands

### Gmail

#### Search Emails
**Triggers:** "search email", "find email about", "搜索邮件"
```bash
gog gmail search '<query>' --max 10
```
Uses Gmail search syntax (e.g. `from:boss subject:urgent`, `is:unread`, `newer_than:1d`)

#### Search Messages
**Triggers:** "search messages", "find message"
```bash
gog gmail messages search '<query>' --max 10 --include-body
```

#### Read Email Thread
**Triggers:** "read email", "show thread", "查看邮件"
```bash
gog gmail thread get <threadId>
```
Add `--download --out-dir ./attachments` to save attachments.

#### Read Single Message
**Triggers:** "read message", "get message"
```bash
gog gmail get <messageId>
```

#### Download Attachment
**Triggers:** "download attachment", "下载附件"
```bash
gog gmail attachment <messageId> <attachmentId> --out ~/Downloads/
```

#### List Labels
**Triggers:** "email labels", "gmail labels", "邮件标签"
```bash
gog gmail labels list
```

#### List Filters
**Triggers:** "email filters", "gmail filters"
```bash
gog gmail filters list
```

#### List Drafts
**Triggers:** "my drafts", "草稿"
```bash
gog gmail drafts list --max 10
```

### Google Drive

#### List Files
**Triggers:** "list files", "show drive", "drive files", "云盘文件"
```bash
gog drive ls --max 20
gog drive ls --parent <folderId> --max 20
```

#### Search Files
**Triggers:** "search drive", "find file", "搜索文件"
```bash
gog drive search '<query>' --max 10
```

#### Get File Info
**Triggers:** "file info", "file details"
```bash
gog drive get <fileId>
```

#### Download / Export File
**Triggers:** "download file", "export file", "下载文件"
```bash
gog drive download <fileId> --out ~/Downloads/
gog drive download <fileId> --format pdf
```
Supported formats: `pdf`, `docx`, `pptx`, `xlsx`, `csv`, `txt`, `png`

#### List File Permissions
**Triggers:** "file permissions", "who has access"
```bash
gog drive permissions <fileId>
```

#### List Shared Drives
**Triggers:** "shared drives", "team drives"
```bash
gog drive drives --max 20
```

#### List File Comments
**Triggers:** "file comments", "文件评论"
```bash
gog drive comments list <fileId> --max 20
```

### Google Docs

#### Read Document
**Triggers:** "read doc", "show document", "读文档", "文档内容"
```bash
gog docs cat <docId>
```

#### Document Info
**Triggers:** "doc info", "document details"
```bash
gog docs info <docId>
```

#### List Document Tabs
**Triggers:** "doc tabs", "document tabs"
```bash
gog docs list-tabs <docId>
```

#### Export Document
**Triggers:** "export doc", "导出文档"
```bash
gog docs export <docId> --format pdf --out ~/Downloads/
```
Supported formats: `pdf`, `docx`, `txt`

### Google Sheets

#### Read Sheet Data
**Triggers:** "read sheet", "show spreadsheet", "读表格", "表格数据"
```bash
gog sheets get <spreadsheetId> 'Sheet1!A1:Z100'
```

#### Sheet Metadata
**Triggers:** "sheet info", "spreadsheet info"
```bash
gog sheets metadata <spreadsheetId>
```

#### Export Sheet
**Triggers:** "export sheet", "导出表格"
```bash
gog sheets export <spreadsheetId> --format xlsx --out ~/Downloads/
```
Supported formats: `pdf`, `xlsx`

### Google Slides

#### Presentation Info
**Triggers:** "slides info", "presentation info", "幻灯片信息"
```bash
gog slides info <presentationId>
```

#### List All Slides
**Triggers:** "list slides", "show slides", "查看幻灯片"
```bash
gog slides list-slides <presentationId>
```

#### Read Single Slide
**Triggers:** "read slide", "slide content"
```bash
gog slides read-slide <presentationId> <slideId>
```

#### Export Presentation
**Triggers:** "export slides", "导出幻灯片"
```bash
gog slides export <presentationId> --format pdf --out ~/Downloads/
```
Supported formats: `pdf`, `pptx`

### Google Calendar

#### List Calendars
**Triggers:** "my calendars", "list calendars", "我的日历"
```bash
gog calendar calendars
```

#### Today's Events
**Triggers:** "today's events", "what's on today", "今天的日程", "今日安排"
```bash
gog calendar events primary --today
```

#### This Week's Events
**Triggers:** "this week", "weekly schedule", "本周日程"
```bash
gog calendar events primary --week
```

#### Events in Date Range
**Triggers:** "events from [date] to [date]", "日程查询"
```bash
gog calendar events primary --from <YYYY-MM-DD> --to <YYYY-MM-DD>
```
Relative time example: `--from today --to tomorrow`, or `--days 7`

#### Search Events
**Triggers:** "search calendar", "find event", "搜索日程"
```bash
gog calendar search '<query>' --days 30
```

#### Get Event Details
**Triggers:** "event details", "show event"
```bash
gog calendar event primary <eventId>
```

#### Check Free/Busy
**Triggers:** "am I free", "check availability", "空闲时间"
```bash
gog calendar freebusy --calendars primary --from <start> --to <end>
```

#### Check Conflicts
**Triggers:** "any conflicts", "日程冲突"
```bash
gog calendar conflicts --calendars primary --today
```

### Google Contacts

#### List Contacts
**Triggers:** "my contacts", "list contacts", "通讯录", "联系人列表"
```bash
gog contacts list --max 50
```

#### Search Contacts
**Triggers:** "search contacts", "find contact", "查找联系人"
```bash
gog contacts search '<query>' --max 20
```

#### Get Contact Details
**Triggers:** "contact info", "联系人详情"
```bash
gog contacts get <resourceNameOrEmail>
```

### Google Tasks

#### List Task Lists
**Triggers:** "my task lists", "任务列表"
```bash
gog tasks lists
```

#### List Tasks
**Triggers:** "my tasks", "show tasks", "查看任务"
```bash
gog tasks list <tasklistId> --max 50
```

#### Get Task Details
**Triggers:** "task details", "任务详情"
```bash
gog tasks get <tasklistId> <taskId>
```

### Google Keep (Workspace Only)

#### List Notes
**Triggers:** "my notes", "list keep notes", "笔记列表"
```bash
gog keep list
```

#### Read Note
**Triggers:** "read note", "show note", "查看笔记"
```bash
gog keep get <noteId>
```

#### Search Notes
**Triggers:** "search notes", "搜索笔记"
```bash
gog keep search '<query>'
```

### Account & Auth

#### Check Auth Status
**Triggers:** "google auth", "gog status", "检查认证"
```bash
gog auth status
```

#### List Accounts
**Triggers:** "google accounts", "gog accounts"
```bash
gog auth list
```

#### Who Am I
**Triggers:** "google whoami", "gog whoami"
```bash
gog people me
```

## Important Notes

- This skill is READ-ONLY to protect your Google account data
- Uses official Google APIs via OAuth 2.0
- Requires one-time OAuth setup (see First-Time Setup)
- For multi-account setups, always specify `--account`
- Google Keep is only available for Workspace accounts

## Safety Note

This skill only allows the read-only commands listed above. All write, modify, and delete operations are intentionally excluded. For the full list of excluded commands, see `references/excluded-commands.md`.
