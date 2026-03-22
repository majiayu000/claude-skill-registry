---
name: box
description: |
  Box API integration with managed OAuth. Manage files, folders, collaborations, and cloud storage.
  Use this skill when users want to upload, download, share, or organize files and folders in Box.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
  Requires network access and valid Maton API key.
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# Box

Access the Box API with managed OAuth authentication. Manage files, folders, collaborations, shared links, and cloud storage.

## Quick Start

```bash
# Get current user info
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/box/2.0/users/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## Base URL

```
https://gateway.maton.ai/box/2.0/{resource}
```

The gateway proxies requests to `api.box.com/2.0` and automatically injects your OAuth token.

## Authentication

All requests require the Maton API key in the Authorization header:

```
Authorization: Bearer $MATON_API_KEY
```

**Environment Variable:** Set your API key as `MATON_API_KEY`:

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### Getting Your API Key

1. Sign in or create an account at [maton.ai](https://maton.ai)
2. Go to [maton.ai/settings](https://maton.ai/settings)
3. Copy your API key

## Connection Management

Manage your Box OAuth connections at `https://ctrl.maton.ai`.

### List Connections

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=box&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Create Connection

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'box'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Get Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**Response:**
```json
{
  "connection": {
    "connection_id": "bd484938-0902-4fc0-9ffb-2549d7d91f1d",
    "status": "ACTIVE",
    "creation_time": "2026-02-08T21:14:41.808115Z",
    "last_updated_time": "2026-02-08T21:16:10.100340Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "box",
    "metadata": {}
  }
}
```

Open the returned `url` in a browser to complete OAuth authorization.

### Delete Connection

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Specifying Connection

If you have multiple Box connections, specify which one to use with the `Maton-Connection` header:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/box/2.0/users/me')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', 'bd484938-0902-4fc0-9ffb-2549d7d91f1d')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

If omitted, the gateway uses the default (oldest) active connection.

## API Reference

### User Info

#### Get Current User

```bash
GET /box/2.0/users/me
```

**Response:**
```json
{
  "type": "user",
  "id": "48806418054",
  "name": "Chris",
  "login": "chris@example.com",
  "created_at": "2026-02-08T13:12:34-08:00",
  "modified_at": "2026-02-08T13:12:35-08:00",
  "language": "en",
  "timezone": "America/Los_Angeles",
  "space_amount": 10737418240,
  "space_used": 0,
  "max_upload_size": 262144000,
  "status": "active",
  "avatar_url": "https://app.box.com/api/avatar/large/48806418054"
}
```

#### Get User

```bash
GET /box/2.0/users/{user_id}
```

### Folder Operations

#### Get Root Folder

The root folder has ID `0`:

```bash
GET /box/2.0/folders/0
```

#### Get Folder

```bash
GET /box/2.0/folders/{folder_id}
```

**Response:**
```json
{
  "type": "folder",
  "id": "365037181307",
  "name": "My Folder",
  "description": "Folder description",
  "size": 0,
  "path_collection": {
    "total_count": 1,
    "entries": [
      {"type": "folder", "id": "0", "name": "All Files"}
    ]
  },
  "created_by": {"type": "user", "id": "48806418054", "name": "Chris"},
  "owned_by": {"type": "user", "id": "48806418054", "name": "Chris"},
  "item_status": "active"
}
```

#### List Folder Items

```bash
GET /box/2.0/folders/{folder_id}/items
```

Query parameters:
- `limit` - Maximum items to return (default 100, max 1000)
- `offset` - Offset for pagination
- `fields` - Comma-separated list of fields to include

**Response:**
```json
{
  "total_count": 1,
  "entries": [
    {
      "type": "folder",
      "id": "365036703666",
      "name": "Subfolder"
    }
  ],
  "offset": 0,
  "limit": 100
}
```

#### Create Folder

```bash
POST /box/2.0/folders
Content-Type: application/json

{
  "name": "New Folder",
  "parent": {"id": "0"}
}
```

**Response:**
```json
{
  "type": "folder",
  "id": "365037181307",
  "name": "New Folder",
  "created_at": "2026-02-08T14:56:17-08:00"
}
```

#### Update Folder

```bash
PUT /box/2.0/folders/{folder_id}
Content-Type: application/json

{
  "name": "Updated Folder Name",
  "description": "Updated description"
}
```

#### Copy Folder

```bash
POST /box/2.0/folders/{folder_id}/copy
Content-Type: application/json

{
  "name": "Copied Folder",
  "parent": {"id": "0"}
}
```

#### Delete Folder

```bash
DELETE /box/2.0/folders/{folder_id}
```

Query parameters:
- `recursive` - Set to `true` to delete non-empty folders

Returns 204 No Content on success.

### File Operations

#### Get File Info

```bash
GET /box/2.0/files/{file_id}
```

#### Download File

```bash
GET /box/2.0/files/{file_id}/content
```

Returns a redirect to the download URL.

#### Upload File

```bash
POST https://upload.box.com/api/2.0/files/content
Content-Type: multipart/form-data

attributes={"name":"file.txt","parent":{"id":"0"}}
file=<binary data>
```

**Note:** File uploads use a different base URL: `upload.box.com`

#### Update File Info

```bash
PUT /box/2.0/files/{file_id}
Content-Type: application/json

{
  "name": "renamed-file.txt",
  "description": "File description"
}
```

#### Copy File

```bash
POST /box/2.0/files/{file_id}/copy
Content-Type: application/json

{
  "name": "copied-file.txt",
  "parent": {"id": "0"}
}
```

#### Delete File

```bash
DELETE /box/2.0/files/{file_id}
```

Returns 204 No Content on success.

#### Get File Versions

```bash
GET /box/2.0/files/{file_id}/versions
```

### Shared Links

Create a shared link by updating a file or folder:

```bash
PUT /box/2.0/folders/{folder_id}
Content-Type: application/json

{
  "shared_link": {
    "access": "open"
  }
}
```

Access levels:
- `open` - Anyone with the link
- `company` - Only users in the enterprise
- `collaborators` - Only collaborators

**Response includes:**
```json
{
  "shared_link": {
    "url": "https://app.box.com/s/sisarrztrenabyygfwqggbwommf8uucv",
    "access": "open",
    "effective_access": "open",
    "is_password_enabled": false,
    "permissions": {
      "can_preview": true,
      "can_download": true,
      "can_edit": false
    }
  }
}
```

### Collaborations

#### List Folder Collaborations

```bash
GET /box/2.0/folders/{folder_id}/collaborations
```

#### Create Collaboration

```bash
POST /box/2.0/collaborations
Content-Type: application/json

{
  "item": {"type": "folder", "id": "365037181307"},
  "accessible_by": {"type": "user", "login": "user@example.com"},
  "role": "editor"
}
```

Roles: `editor`, `viewer`, `previewer`, `uploader`, `previewer_uploader`, `viewer_uploader`, `co-owner`

#### Update Collaboration

```bash
PUT /box/2.0/collaborations/{collaboration_id}
Content-Type: application/json

{
  "role": "viewer"
}
```

#### Delete Collaboration

```bash
DELETE /box/2.0/collaborations/{collaboration_id}
```

### Search

```bash
GET /box/2.0/search?query=document
```

Query parameters:
- `query` - Search query (required)
- `type` - Filter by type: `file`, `folder`, `web_link`
- `file_extensions` - Comma-separated extensions
- `ancestor_folder_ids` - Limit to specific folders
- `limit` - Max results (default 30)
- `offset` - Pagination offset

**Response:**
```json
{
  "total_count": 5,
  "entries": [...],
  "limit": 30,
  "offset": 0,
  "type": "search_results_items"
}
```

### Events

```bash
GET /box/2.0/events
```

Query parameters:
- `stream_type` - `all`, `changes`, `sync`, `admin_logs`
- `stream_position` - Position to start from
- `limit` - Max events to return

**Response:**
```json
{
  "chunk_size": 4,
  "next_stream_position": "30401068076164269",
  "entries": [...]
}
```

### Trash

#### List Trashed Items

```bash
GET /box/2.0/folders/trash/items
```

#### Get Trashed Item

```bash
GET /box/2.0/files/{file_id}/trash
GET /box/2.0/folders/{folder_id}/trash
```

#### Restore Trashed Item

```bash
POST /box/2.0/files/{file_id}
POST /box/2.0/folders/{folder_id}
```

#### Permanently Delete

```bash
DELETE /box/2.0/files/{file_id}/trash
DELETE /box/2.0/folders/{folder_id}/trash
```

### Collections (Favorites)

#### List Collections

```bash
GET /box/2.0/collections
```

**Response:**
```json
{
  "total_count": 1,
  "entries": [
    {
      "type": "collection",
      "name": "Favorites",
      "collection_type": "favorites",
      "id": "35223030868"
    }
  ]
}
```

#### Get Collection Items

```bash
GET /box/2.0/collections/{collection_id}/items
```

### Recent Items

```bash
GET /box/2.0/recent_items
```

### Webhooks

#### List Webhooks

```bash
GET /box/2.0/webhooks
```

#### Create Webhook

```bash
POST /box/2.0/webhooks
Content-Type: application/json

{
  "target": {"id": "365037181307", "type": "folder"},
  "address": "https://example.com/webhook",
  "triggers": ["FILE.UPLOADED", "FILE.DOWNLOADED"]
}
```

**Note:** Webhook creation may require enterprise permissions.

#### Delete Webhook

```bash
DELETE /box/2.0/webhooks/{webhook_id}
```

## Pagination

Box uses offset-based pagination:

```bash
GET /box/2.0/folders/0/items?limit=100&offset=0
GET /box/2.0/folders/0/items?limit=100&offset=100
```

Some endpoints use marker-based pagination with `marker` parameter.

**Response:**
```json
{
  "total_count": 250,
  "entries": [...],
  "offset": 0,
  "limit": 100
}
```

## Code Examples

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/box/2.0/folders/0/items',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const data = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/box/2.0/folders/0/items',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'}
)
data = response.json()
```

### Python (Create Folder)

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/box/2.0/folders',
    headers={
        'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}',
        'Content-Type': 'application/json'
    },
    json={
        'name': 'New Folder',
        'parent': {'id': '0'}
    }
)
folder = response.json()
print(f"Created folder: {folder['id']}")
```

## Notes

- Root folder ID is `0`
- File uploads use `upload.box.com` instead of `api.box.com`
- Delete operations return 204 No Content on success
- Use `fields` parameter to request specific fields and reduce response size
- Shared links can have password protection and expiration dates
- Some operations (list users, create webhooks) require enterprise admin permissions
- ETags can be used for conditional updates with `If-Match` header
- IMPORTANT: When piping curl output to `jq` or other commands, environment variables like `$MATON_API_KEY` may not expand correctly in some shell environments

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Missing Box connection or bad request |
| 401 | Invalid or missing Maton API key |
| 403 | Insufficient permissions for the operation |
| 404 | Resource not found |
| 409 | Conflict (e.g., item with same name exists) |
| 429 | Rate limited |
| 4xx/5xx | Passthrough error from Box API |

Box errors include detailed messages:
```json
{
  "type": "error",
  "status": 409,
  "code": "item_name_in_use",
  "message": "Item with the same name already exists"
}
```

### Troubleshooting: API Key Issues

1. Check that the `MATON_API_KEY` environment variable is set:

```bash
echo $MATON_API_KEY
```

2. Verify the API key is valid by listing connections:

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Troubleshooting: Invalid App Name

1. Ensure your URL path starts with `box`. For example:

- Correct: `https://gateway.maton.ai/box/2.0/users/me`
- Incorrect: `https://gateway.maton.ai/2.0/users/me`

## Resources

- [Box API Reference](https://developer.box.com/reference)
- [Box Developer Documentation](https://developer.box.com/guides)
- [Authentication Guide](https://developer.box.com/guides/authentication)
- [Box SDKs](https://developer.box.com/sdks-and-tools)
- [Maton Community](https://discord.com/invite/dBfFAcefs2)
- [Maton Support](mailto:support@maton.ai)
