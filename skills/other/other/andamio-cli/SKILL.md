---
name: andamio-cli
description: Use the Andamio CLI to manage courses, modules, and content. Import compiled modules, export for editing, check auth status, and query course data.
license: MIT
compatibility: Requires the Andamio CLI binary. See andamio.io for installation.
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Andamio CLI

## Description

Manages Andamio platform content using the `andamio` CLI tool. Handles authentication, course queries, module import/export, and the full round-trip workflow from compiled content to live platform.

**CLI location:** `/usr/local/bin/andamio`
**Config:** `~/.andamio/config.json`

## Prerequisites

Before running any commands, verify:

```bash
andamio --version    # CLI installed
andamio user status  # Authentication status
```

If not authenticated:
```bash
andamio user login   # Opens browser for wallet signing
```

If JWT is expired:
```bash
andamio user logout && andamio user login
```

## Command Reference

### Authentication

| Command | Purpose |
|---------|---------|
| `andamio auth login --api-key <key>` | Store API key (read-only access) |
| `andamio auth status` | Check API key status |
| `andamio user login` | Authenticate via browser wallet (required for writes) |
| `andamio user logout` | Clear JWT |
| `andamio user status` | Show auth status + JWT expiry |
| `andamio user me` | Current user dashboard |

### Course Queries

| Command | Purpose |
|---------|---------|
| `andamio course list` | List accessible courses |
| `andamio course get <course-id>` | Course details |
| `andamio course modules <course-id>` | List modules in course |
| `andamio course slts <course-id> <module-code>` | List SLTs for module |
| `andamio course lesson <course-id> <module-code> <slt-index>` | Get single lesson |
| `andamio course intro <course-id> <module-code>` | Get module introduction |
| `andamio course assignment <course-id> <module-code>` | Get module assignment |

### Module Export

```bash
andamio course export <course-id> <module-code> [flags]
```

**Flags:**
- `--output-dir <dir>` — Custom output path (default: `./compiled/<course-slug>/<module-code>/`)
- `--force` — Overwrite existing directory

**Output:** Creates compiled directory with `outline.md`, `lesson-N.md`, `introduction.md`, `assignment.md`, and `assets/` with `.image-manifest.json`.

### Module Import (Update Existing)

```bash
andamio course import <path> --course-id <id> [flags]
```

**Flags:**
- `--course-id <id>` (required) — Target course ID
- `--dry-run` — Show API payload without sending

**Requires:** `andamio user login` (JWT auth)

**Important:** Import only updates existing modules and SLTs. The module must already exist in the course, and SLTs must be created before lessons can be imported. See "Creating New Modules" and "SLT Creation Gotcha" below.

**What import does:**
1. Parses `outline.md` for title, code, SLTs
2. Uploads new images in `assets/` to CDN (preserves manifest entries)
3. Extracts `# H1` from each lesson file as the lesson title
4. Converts remaining markdown to Tiptap JSON content
5. Merges with existing module state
6. Sends update to API

**Critical file format rules:**
- `outline.md`: No `# H1` heading — title comes from YAML `title:` field. Start with `## SLTs` after frontmatter.
- `lesson-N.md`: **Must have `# H1` title** — this becomes the lesson title in the app. Content follows below.
- `introduction.md`: `# H1` becomes intro title, rest is content.
- `assignment.md`: `# H1` becomes assignment title, rest is content.

**SLT locking rules:**
- **DRAFT modules:** Can create/update/delete SLTs and lessons
- **APPROVED/ON_CHAIN modules:** SLTs are locked — can only update lesson content

### Creating New Modules (API Direct)

The CLI has no `create` command yet. Use the API directly:

```bash
# Step 1: Create the empty module shell
andamio_url=$(python3 -c "import json; print(json.load(open('$HOME/.andamio/config.json'))['base_url'])")
jwt=$(python3 -c "import json; print(json.load(open('$HOME/.andamio/config.json'))['user_jwt'])")
api_key=$(python3 -c "import json; print(json.load(open('$HOME/.andamio/config.json'))['api_key'])")

curl -s -X POST "${andamio_url}/api/v2/course/teacher/course-module/create" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${jwt}" \
  -H "x-api-key: ${api_key}" \
  -d '{
    "course_id": "COURSE_ID_HERE",
    "course_module_code": "101",
    "title": "Module Title",
    "sort_order": 1
  }' | python3 -m json.tool

# Step 2: Import content into the newly created module
andamio course import ./compiled/course-slug/101 --course-id <course-id>
```

**Parameters for create:**

| Field | Type | Purpose |
|-------|------|---------|
| `course_module_code` | string | Unique module code (e.g., "101", "intro-cardano") |
| `title` | string | Module display name |
| `sort_order` | integer | Display order (1, 2, 3...) |
| `description` | string | Optional module description |
| `image_url` | string | Optional module image |
| `is_live` | boolean | Whether module is visible |

### Other Commands

| Command | Purpose |
|---------|---------|
| `andamio project list` | List projects |
| `andamio project get <project-id>` | Project details |
| `andamio teacher courses` | Courses where you're a teacher |
| `andamio tx pending` | Pending transactions |
| `andamio tx status <hash>` | Transaction status |
| `andamio spec paths [--filter <pattern>]` | Browse API endpoints |
| `andamio apikey usage` | API key usage stats |

## Workflows

### Import a Single Compiled Module

```bash
# 1. Verify auth
andamio user status

# 2. Dry run first
andamio course import ./compiled/my-course/101 --course-id <id> --dry-run

# 3. Import for real
andamio course import ./compiled/my-course/101 --course-id <id>

# 4. Verify
andamio course slts <id> 101
```

### Import All Modules in a Course

```bash
COURSE_ID="<course-id>"
COURSE_DIR="./compiled/course-slug"

for module_dir in "$COURSE_DIR"/*/; do
  echo "=== Importing $(basename $module_dir) ==="
  andamio course import "$module_dir" --course-id "$COURSE_ID"
done
```

### Create + Import New Modules (Full Flow)

When modules don't exist on the platform yet, three steps are required:

1. **Create module shell** via API (no CLI command yet)
2. **Create SLTs** via API with `slt_index` omitted (triggers create instead of update)
3. **Import content** via CLI (lessons, assignment, introduction, images)

#### SLT Creation Gotcha

The CLI sends SLTs with `slt_index` set, which the API interprets as "update existing." For **new modules with no SLTs**, you must first create them via a direct API call with `slt_index` **omitted**:

```bash
# This CREATES SLTs (slt_index omitted)
curl -s -X POST "${andamio_url}/api/v2/course/teacher/course-module/update" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${jwt}" \
  -H "x-api-key: ${api_key}" \
  -d '{
    "course_id": "COURSE_ID",
    "course_module_code": "101",
    "slts": [
      {"slt_text": "First SLT text"},
      {"slt_text": "Second SLT text"}
    ]
  }'
# Response: "slts_created": 2

# After SLTs exist, CLI import works normally:
andamio course import ./compiled/course/101 --course-id COURSE_ID
# Response: "lessons_created": 2
```

#### Full Script

```bash
COURSE_ID="<course-id>"
COURSE_DIR="./compiled/course-slug"

andamio_url=$(python3 -c "import json; print(json.load(open('$HOME/.andamio/config.json'))['base_url'])")
jwt=$(python3 -c "import json; print(json.load(open('$HOME/.andamio/config.json'))['user_jwt'])")
api_key=$(python3 -c "import json; print(json.load(open('$HOME/.andamio/config.json'))['api_key'])")

sort_order=1
for module_dir in "$COURSE_DIR"/*/; do
  code=$(basename "$module_dir")
  title=$(grep '^title:' "$module_dir/outline.md" | sed 's/title: *"\{0,1\}\(.*\)"\{0,1\}/\1/' | sed 's/"$//')

  echo "=== Module $code: $title ==="

  # Step 1: Create module shell
  curl -s -X POST "${andamio_url}/api/v2/course/teacher/course-module/create" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${jwt}" \
    -H "x-api-key: ${api_key}" \
    -d "{
      \"course_id\": \"${COURSE_ID}\",
      \"course_module_code\": \"${code}\",
      \"title\": \"${title}\",
      \"sort_order\": ${sort_order}
    }"

  # Step 2: Create SLTs (omit slt_index to trigger creation)
  slts=$(grep -E '^\d+\.' "$module_dir/outline.md" | sed 's/^[0-9]*\. *//' | python3 -c "
import sys, json
slts = [{'slt_text': line.strip()} for line in sys.stdin if line.strip()]
print(json.dumps(slts))
")
  curl -s -X POST "${andamio_url}/api/v2/course/teacher/course-module/update" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${jwt}" \
    -H "x-api-key: ${api_key}" \
    -d "{
      \"course_id\": \"${COURSE_ID}\",
      \"course_module_code\": \"${code}\",
      \"slts\": ${slts}
    }" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'  SLTs created: {d.get(\"changes\",{}).get(\"slts_created\",0)}')"

  # Step 3: Import content (lessons, assignment, images)
  andamio course import "$module_dir" --course-id "$COURSE_ID"

  sort_order=$((sort_order + 1))
  echo ""
done
```

### Export → Edit → Re-import (Round Trip)

```bash
# Export
andamio course export <course-id> 101

# Edit locally
vim compiled/course-slug/101/lesson-1.md

# Re-import (manifest preserves existing image URLs)
andamio course import compiled/course-slug/101 --course-id <course-id>
```

## Image Handling

- **Supported:** PNG, JPEG, GIF, WebP (max 5MB per image)
- **Upload:** New images in `assets/` are automatically uploaded to CDN on import
- **Manifest:** `.image-manifest.json` maps filenames → CDN URLs
- **Round-trip safe:** Export downloads images + writes manifest; import re-uses manifest URLs

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `module 'X' not found in course` | Module doesn't exist on platform | Create it first (see "Creating New Modules") |
| `slts_created: 0` on new module | CLI sends `slt_index`, API treats as update of non-existent SLTs | Create SLTs via API with `slt_index` omitted (see "SLT Creation Gotcha") |
| `lessons_created: 0` after import | No SLT slots exist to attach lessons to | Create SLTs first, then re-import |
| `SLT_LOCKED` | Trying to modify SLTs on APPROVED/ON_CHAIN module | Can only update lesson content |
| `unauthorized` | JWT expired or missing | Run `andamio user login` |
| `create via Studio first` | Lesson targets empty SLT slot on locked module | Add SLT via Studio, then import |
| `CONFLICT: Module with this code already exists` | Module code already used in course | Use a different code or import to update |

## Global Flags

All commands support:
- `-o, --output <format>` — Output format: `text` (default), `json`, `csv`, `markdown`

JSON output is useful for scripting:
```bash
andamio course modules <id> -o json | jq '.data[].course_module_code'
```

## Environment

- **Preprod:** `andamio config set-url https://preprod.api.andamio.io`
- **Mainnet:** `andamio config set-url https://mainnet.api.andamio.io`
- **Custom:** Set `ANDAMIO_ALLOW_ANY_URL=1` then `andamio config set-url <url>`
