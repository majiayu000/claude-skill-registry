---
name: linear-extended
description: Extended Linear operations - manage project milestones and download images
  from issues. Use for project phases (Alpha, Beta, Launch), milestone management,
  or extracting images/screenshots from issues
---

---
name: linear-extended
description: Extended Linear operations - manage project milestones and download images from issues. Use for project phases (Alpha, Beta, Launch), milestone management, or extracting images/screenshots from issues. Triggers: "show milestones", "create milestone", "update milestone", "project phases", "download images from issue", "get issue images", "extract screenshots".
---

# Linear Extended

Extended operations for Linear: milestones and issue image downloads.

## Setup

Install dependencies once:
```bash
cd <skill-dir>/scripts && npm install
```

## Authentication

Two methods supported: OAuth (recommended) or API key.

### Option A: OAuth Login (Recommended)

First, create an OAuth app in Linear:
1. Go to Linear Settings > API > OAuth Applications
2. Create new app with redirect URI: `urn:ietf:wg:oauth:2.0:oob`
3. Save the `client_id` and `client_secret`

Then authenticate:
```bash
# First time: provide credentials (saved for future use)
node <skill-dir>/scripts/auth-login.js --client-id "YOUR_CLIENT_ID" --client-secret "YOUR_CLIENT_SECRET"

# Subsequent logins (credentials remembered)
node <skill-dir>/scripts/auth-login.js
```

Follow the prompts: open the URL in browser, authorize, paste the code back.

### Option B: API Key

Set `LINEAR_API_KEY` environment variable with a personal API key from Linear Settings > API.

### Check Auth Status
```bash
node <skill-dir>/scripts/auth-status.js
```

### Logout
```bash
node <skill-dir>/scripts/auth-logout.js        # Keep client credentials
node <skill-dir>/scripts/auth-logout.js --all  # Clear everything
```

## List Milestones

```bash
node <skill-dir>/scripts/milestones-list.js <project-name-or-id>
```

Example:
```bash
node <skill-dir>/scripts/milestones-list.js Candlekeep
```

## Create Milestone

```bash
node <skill-dir>/scripts/milestones-create.js <project> --name "Name" [--description "..."] [--target-date "YYYY-MM-DD"]
```

Example:
```bash
node <skill-dir>/scripts/milestones-create.js Candlekeep --name "Alpha" --description "Internal testing" --target-date "2025-01-15"
```

## Update Milestone

```bash
node <skill-dir>/scripts/milestones-update.js <milestone-id> [--name "..."] [--description "..."] [--target-date "..."]
```

Example:
```bash
node <skill-dir>/scripts/milestones-update.js abc123 --name "Beta" --target-date "2025-02-01"
```

## Delete Milestone

```bash
node <skill-dir>/scripts/milestones-delete.js <milestone-id>
```

## Get Project with Milestones

```bash
node <skill-dir>/scripts/project-get.js <project-name-or-id> [--with-milestones]
```

Example:
```bash
node <skill-dir>/scripts/project-get.js Candlekeep --with-milestones
```

## Download Issue Images

Download images from a Linear issue (attachments and inline images from description):

```bash
node <skill-dir>/scripts/issue-images.js <issue-id> [--output-dir <path>] [--list-only]
```

Options:
- `--output-dir <path>`: Directory to save images (default: ./linear-images)
- `--list-only`: Show image URLs without downloading

Examples:
```bash
# Download all images from issue CND-121
node <skill-dir>/scripts/issue-images.js CND-121

# List images without downloading
node <skill-dir>/scripts/issue-images.js CND-121 --list-only

# Save to specific directory
node <skill-dir>/scripts/issue-images.js CND-121 --output-dir /tmp/issue-images
```

## Output

All scripts output JSON. Success includes data, errors include `{ "error": "message" }`.
