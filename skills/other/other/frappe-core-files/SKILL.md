---
name: frappe-core-files
description: >
  Use when handling file uploads, attachments, private/public file access, or S3 storage configuration.
  Prevents broken file URLs, permission leaks on private files, and failed uploads from incorrect MIME handling.
  Covers File DocType, frappe.get_file, upload API, private vs public directories, S3 integration, file URL patterns, attach field types.
  Keywords: file, upload, attachment, File DocType, private, public, S3, file_url, get_file, attach.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe File Management

## Quick Reference

| Action | Method | Notes |
|--------|--------|-------|
| Save file from bytes | `save_file(fname, content, dt, dn)` | Returns File doc |
| Save file from URL | `save_url(file_url, fname, dt, dn)` | Creates File doc from URL |
| Read file content | `frappe.get_file(fname)` | Returns `[filename, content]` |
| Get file path | `get_file_path(file_name)` | Resolves to absolute path |
| Upload via HTTP | `POST /api/method/upload_file` | Multipart form upload |
| Delete file | `frappe.delete_doc("File", name)` | Removes doc + filesystem file |
| Attach print | `frappe.attach_print(dt, dn, print_format)` | Returns `{"fname", "fcontent"}` |
| Get cached doc | `frappe.get_cached_doc("File", name)` | Read-only, cached |

---

## Decision Tree

```
What file operation do you need?
│
├─ Upload a file from user input?
│  ├─ Via web form → Attach field type (auto-handles upload)
│  └─ Via API → POST /api/method/upload_file
│
├─ Create a file programmatically?
│  ├─ From bytes/content → save_file(fname, content, dt, dn)
│  ├─ From external URL → save_url(file_url, fname, dt, dn)
│  └─ Full control → frappe.get_doc({"doctype": "File", ...}).insert()
│
├─ Read file content?
│  ├─ By filename → frappe.get_file(fname)
│  └─ By File doc → file_doc.get_content()
│
├─ Public or private?
│  ├─ Public (anyone with link) → is_private=0, URL: /files/fname
│  └─ Private (permission-based) → is_private=1, URL: /private/files/fname
│
└─ Generate PDF attachment?
   └─ frappe.attach_print(doctype, name, print_format)
```

---

## File DocType — Core Fields

| Field | Type | Description |
|-------|------|-------------|
| `file_name` | Data | Filename without path |
| `file_url` | Data | URL path (e.g., `/files/report.pdf`) |
| `file_type` | Data | Extension (PDF, PNG, DOCX, etc.) |
| `is_private` | Check | 0 = public, 1 = private |
| `is_folder` | Check | True for folder entries |
| `folder` | Link → File | Parent folder |
| `attached_to_doctype` | Link → DocType | Parent document type |
| `attached_to_name` | Data | Parent document name |
| `attached_to_field` | Data | Field name on parent |
| `content_hash` | Data | SHA-256 for deduplication |
| `file_size` | Int | Size in bytes |

---

## File URL Patterns

| Type | URL Pattern | Filesystem Path |
|------|------------|-----------------|
| Public | `/files/{filename}` | `{site}/public/files/{filename}` |
| Private | `/private/files/{filename}` | `{site}/private/files/{filename}` |
| Remote | `https://...` | Not stored locally |
| API | `/api/method/{path}` | Generated dynamically |

Valid URL prefixes: `http://`, `https://`, `/api/method/`, `/files/`, `/private/files/`.

ALWAYS use `/private/files/` for sensitive documents. Public files are accessible to anyone with the URL, including unauthenticated users.

---

## Permission Model

Frappe files use a three-tier permission model:

1. **Administrator** — unrestricted access to all files
2. **Public files** (`is_private=0`) — readable by anyone with the URL (no authentication required for read)
3. **Private files** (`is_private=1`) — access requires:
   - User is the file owner, OR
   - User has explicit share on the file, OR
   - User has read permission on the `attached_to_doctype`/`attached_to_name` document

NEVER store sensitive data as public files. ALWAYS set `is_private=1` for documents containing personal data, financial records, or confidential information.

---

## Programmatic File Operations

### Save File from Content

```python
from frappe.utils.file_manager import save_file

# Save a generated CSV
csv_content = "Name,Amount\nACME,1000\nGlobex,2000"
file_doc = save_file(
    fname="report.csv",
    content=csv_content.encode("utf-8"),
    dt="Sales Invoice",           # attach to this DocType
    dn="SINV-00001",              # attach to this document
    folder="Home/Attachments",    # optional folder
    is_private=1,                 # private file
)
# file_doc.file_url → "/private/files/report.csv"
```

### Save File from URL

```python
from frappe.utils.file_manager import save_url

file_doc = save_url(
    file_url="https://example.com/logo.png",
    filename="company-logo.png",
    dt="Company",
    dn="My Company",
    folder="Home",
    is_private=0,
)
```

### Read File Content

```python
# By filename
filename, content = frappe.get_file("report.csv")

# By File document
file_doc = frappe.get_doc("File", {"file_name": "report.csv"})
content_bytes = file_doc.get_content()
```

### Create File Document Directly

```python
file_doc = frappe.get_doc({
    "doctype": "File",
    "file_name": "generated-report.pdf",
    "attached_to_doctype": "Sales Invoice",
    "attached_to_name": "SINV-00001",
    "is_private": 1,
    "content": pdf_bytes,  # raw bytes — written to disk on insert
}).insert(ignore_permissions=True)
```

### Generate and Attach PDF

```python
# Create PDF attachment dict (for use with sendmail)
pdf_attachment = frappe.attach_print(
    "Sales Invoice",
    "SINV-00001",
    print_format="Standard",
)
# Returns: {"fname": "Sales Invoice - SINV-00001.pdf", "fcontent": <bytes>}

# Save PDF as file attachment
from frappe.utils.file_manager import save_file

pdf = frappe.get_print("Sales Invoice", "SINV-00001", print_format="Standard", as_pdf=True)
save_file("invoice.pdf", pdf, "Sales Invoice", "SINV-00001", is_private=1)
```

---

## File Upload via REST API

```bash
# Upload file attached to a document
curl -X POST https://site.example.com/api/method/upload_file \
  -H "Authorization: token api_key:api_secret" \
  -F "file=@/path/to/document.pdf" \
  -F "doctype=Sales Invoice" \
  -F "docname=SINV-00001" \
  -F "is_private=1"
```

Response:
```json
{
  "message": {
    "name": "FILE-00001",
    "file_name": "document.pdf",
    "file_url": "/private/files/document.pdf",
    "is_private": 1
  }
}
```

---

## File Size and Extension Limits

**Default max file size:** 10 MB per attachment.

Override in `site_config.json`:
```json
{
  "max_file_size": 20971520
}
```

**Max attachments per document:** Set via Customize Form → Max Attachments field on the DocType.

**Check file size programmatically:**
```python
from frappe.utils.file_manager import check_max_file_size
check_max_file_size(content)  # raises MaxFileSizeReachedError if too large
```

---

## Attach Field Types

| Field Type | Stores | UI |
|------------|--------|----|
| `Attach` | Single file URL | File picker + upload button |
| `Attach Image` | Single image URL | Image preview + upload |

Both store the `file_url` string in the field value. The File DocType record is created separately with `attached_to_field` set.

---

## S3 / Cloud Storage Integration

Frappe supports custom file storage via the `delete_file_data_content` hook and custom upload handlers.

### S3 via frappe-s3-attachment or similar app

```python
# In hooks.py of custom app
delete_file_data_content = "my_app.storage.delete_from_s3"
```

ALWAYS test file deletion when using custom storage backends — the default `delete_file_from_filesystem` only handles local files.

### Configuration Pattern

```python
# site_config.json for S3-compatible storage
{
  "s3_bucket": "my-frappe-files",
  "s3_region": "eu-west-1",
  "s3_access_key": "AKIA...",
  "s3_secret_key": "...",
}
```

---

## Version Differences

| Feature | v14 | v15 | v16 |
|---------|-----|-----|-----|
| File DocType | Available | Available | Available |
| `content_hash` dedup | Available | Available | Available |
| Image optimization | Manual | Auto (1920x1080, 85%) | Auto |
| Import/Export Zip | Not available | Available | Available |

---

## See Also

- [references/examples.md](references/examples.md) — File operation code examples
- [references/anti-patterns.md](references/anti-patterns.md) — Common file handling mistakes
- `frappe-core-permissions` — Permission model for file access
- `frappe-core-database` — Database operations for File queries
