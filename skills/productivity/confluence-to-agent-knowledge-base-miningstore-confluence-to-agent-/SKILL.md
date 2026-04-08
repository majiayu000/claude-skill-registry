---
name: confluence-to-agent-knowledge-base
description: >
  Turn any Confluence Cloud instance into a private, searchable AI knowledge base
  on GitHub with access-tiered repos. Interactive 6-phase walkthrough using the
  Atlassian MCP connector (no API tokens needed). Ingests pages, compiles a
  structured wiki with categories and summaries, sets up search/Q&A CLI tools,
  splits into access-controlled GitHub repos, and configures weekly auto-sync.
  Use when asked to "migrate confluence", "create knowledge base from confluence",
  "set up a KB", "export confluence to github", "confluence to markdown",
  "build a knowledge base", or "make confluence searchable".
---

# Confluence to Agent Knowledge Base

Convert a company's Confluence spaces into a private, LLM-powered knowledge base
hosted on GitHub. Works for ANY Confluence Cloud instance. No API tokens required —
uses the Atlassian MCP connector for all Confluence access.

## Prerequisites

Before starting, verify:
1. The user has the **Atlassian MCP connector** connected in Claude Code
2. The user has **Python 3.9+** installed
3. The user has **git** configured with push access to their GitHub org

If the Atlassian connector is not connected, tell the user:
"You need to connect your Atlassian account first. Go to Claude Code settings
and add the Atlassian connector, then come back and run this skill again."

## Overview — 6 Phases

Walk the user through these phases interactively:

1. **Discovery** — Find their Confluence, list spaces
2. **Access Tiers** — Group spaces by who should see them
3. **Ingest** — Pull all pages via MCP into markdown files
4. **Compile** — Set up the CLI tool and compile the wiki
5. **GitHub** — Create private repos and push
6. **Auto-Sync** — Schedule weekly updates

Always explain what you're doing at each step. Ask for confirmation before
proceeding to the next phase.

---

## Phase 1: Discovery

### Step 1.1: Find Confluence Instance

Call `getAccessibleAtlassianResources` (no parameters needed).

This returns a list of Atlassian sites. Extract:
- `id` — the cloud ID (use this for all subsequent MCP calls)
- `url` — the site URL (e.g., "https://acme.atlassian.net")
- `name` — the site name

If multiple sites are returned, ask the user which one to use.

Store the `cloudId` and `url` for all subsequent operations.

### Step 1.2: List Spaces

Call `getConfluenceSpaces` with:
- `cloudId`: the site URL or cloud ID from step 1.1

Present results to the user as a table:
```
SPACE KEY    NAME                          TYPE      STATUS    PAGES
─────────────────────────────────────────────────────────────────────
ENG          Engineering Team              global    current   ~
HR           Human Resources               global    current   ~
MGMT         Management                    global    current   ~
...
```

Filter out:
- Archived spaces (unless user requests them)
- Personal spaces (unless user requests them)

Store the full list with `id` (numeric space ID), `key`, `name`, `type`, `status`
for each space. The `id` is required for `getPagesInConfluenceSpace`.

### Step 1.3: Select Spaces

Ask the user: "Which spaces do you want to include in your knowledge base?"

Accept:
- "all" — include everything (excluding archived/personal)
- A list of space keys — e.g., "ENG, HR, MGMT, OPS"
- Exclusions — "all except ARCHIVE, TEST"

Store the selected spaces.

---

## Phase 2: Access Tiers

### Step 2.1: Explain Access Tiers

Tell the user:
"Each access tier becomes a separate private GitHub repo. This lets you control
who sees what — for example, management strategy docs stay separate from the
general team knowledge base.

Most companies use 1-3 tiers:
- **General** — everyone on the team (operations, engineering, onboarding, etc.)
- **Leadership** — executives only (strategy, financials, board docs)
- **Sales** — sales team only (pricing, contracts, pipeline)"

### Step 2.2: Group Spaces

Present the selected spaces and suggest groupings based on space names.
Use these heuristics to suggest tiers:
- Spaces with "management", "executive", "board", "finance", "accounting" in the name → leadership tier
- Spaces with "sales", "pricing", "revenue", "pipeline" in the name → sales tier
- Everything else → general tier

Ask the user to confirm or modify. They might want:
- A single tier (no access restrictions)
- Custom tier names and groupings
- More than 3 tiers

### Step 2.3: Name the Repos

For each tier, determine the repo name:
- General: `{company-slug}-kb`
- Additional tiers: `{company-slug}-kb-{tier-name}`

Example: `acme-kb`, `acme-kb-leadership`, `acme-kb-sales`

Ask the user for their GitHub org/username for the repo URLs.

### Step 2.4: Suggest Categories

For each tier, suggest wiki categories based on the space names in that tier.
Common categories:
- `operations`, `technical`, `sales`, `management`, `onboarding`
- `finance`, `customer-success`, `meetings`, `projects`, `general`

Ask the user to confirm or customize. Every tier should have a `general` catch-all.

---

## Phase 3: Ingest

### Step 3.1: Choose Working Directory

Ask the user where to create the knowledge base directories.
Default suggestion: current working directory or `~/Documents/`.

Create a directory for each tier:
```bash
mkdir -p {base_dir}/{tier-repo-name}/{raw,wiki,output}
```

### Step 3.2: Pull Pages

For each tier, for each space in that tier:

1. Call `getPagesInConfluenceSpace` with:
   - `cloudId`: stored from Phase 1
   - `spaceId`: the numeric space ID (NOT the space key)
   - `contentFormat`: `"markdown"`
   - `limit`: `250`

2. Handle pagination: if `_links.next` exists in the response, there are more
   pages. Extract the cursor from the next URL and call again with the cursor.

3. For each page in the response:
   - Extract: `id`, `title`, `status`, `createdAt`, `body`, `parentId`,
     `version.number`, `version.createdAt`
   - Skip pages with empty or very short body (< 50 chars)
   - Slugify the title: lowercase, replace spaces/special chars with hyphens, max 80 chars
   - Clean the markdown body:
     - Remove blob image URLs: `![...](blob:https://media.staging.atl-paas.net/...)`  → `[image]`
     - Remove custom tags: `<custom ...>...</custom>` → empty
     - Remove zero-width spaces
     - Collapse 4+ blank lines to 3

4. Write to `raw/{space_key_lowercase}/{slug}--{page_id}.md` with this format:

```markdown
---
confluence_id: "{page_id}"
title: "{title}"
space_key: "{SPACE_KEY}"
space_name: "{Space Name}"
status: "{status}"
created_at: "{createdAt}"
updated_at: "{version.createdAt}"
version: {version.number}
labels: []
ingested_at: "{current_iso_timestamp}"
---

# {title}

{cleaned_body}
```

5. After each space, report progress:
   "Pulled {N} pages from {Space Name} ({SPACE_KEY})"

6. Process spaces sequentially to avoid rate limits. Add a brief pause between spaces.

### Step 3.3: Report Totals

After all spaces are ingested, show a summary table per tier:
```
TIER: acme-kb (General)
  Engineering (ENG): 245 pages
  Operations (OPS): 189 pages
  Onboarding (HR): 93 pages
  TOTAL: 527 pages

TIER: acme-kb-leadership
  Management (MGMT): 312 pages
  Accounting (FIN): 87 pages
  TOTAL: 399 pages
```

---

## Phase 4: Compile

### Step 4.1: Set Up Python Project

For each tier directory:

1. Copy the Python source from this skill's references directory.
   Read each file from `~/.claude/skills/confluence-to-agent-knowledge-base/references/` and write
   it to the tier directory:
   - `references/confluence_kb/*.py` → `{tier_dir}/confluence_kb/`
   - `references/pyproject.toml` → `{tier_dir}/pyproject.toml`
   - `references/requirements.txt` → `{tier_dir}/requirements.txt`
   - `references/build_sync_state.py` → `{tier_dir}/build_sync_state.py`

2. Copy setup script:
   - `~/.claude/skills/confluence-to-agent-knowledge-base/scripts/setup.sh` → `{tier_dir}/setup.sh`

### Step 4.2: Configure Space-Category Mapping

Edit `{tier_dir}/confluence_kb/compile_kb.py` and populate the empty
`space_category_map` dict in the `compile_fast` method with the mappings
decided in Phase 2. Example:

```python
space_category_map = {
    "ENG": "technical",
    "OPS": "operations",
    "HR": "onboarding",
    "MGMT": "management",
}
```

Also add title-based overrides for meetings:
```python
if any(w in title_lower for w in ["meeting", "standup", "stand-up", "weekly", "daily"]):
    category = "meetings"
```

### Step 4.3: Generate Config

Write `{tier_dir}/ckb-config.yaml`:

```yaml
company_name: "{Company Name}{tier suffix}"
company_description: >
  {Description of what this tier covers}

confluence:
  url: "{confluence_url}"
  email: "${CONFLUENCE_EMAIL}"
  api_token: "${CONFLUENCE_API_TOKEN}"
  cloud_id: "{cloud_id}"

spaces:
  include:
    - {SPACE_KEY_1}
    - {SPACE_KEY_2}
  exclude: []
  include_archived: false
  include_personal: false

compile:
  model: "claude-sonnet-4-20250514"
  max_tokens: 4096
  categories:
    - {category_1}
    - {category_2}
    - general
  min_content_length: 100
  generate_concepts: true
  generate_backlinks: true

raw_dir: "raw"
wiki_dir: "wiki"
output_dir: "output"
anthropic_api_key: "${ANTHROPIC_API_KEY}"
```

### Step 4.4: Install and Compile

For each tier:

```bash
cd {tier_dir}
python3 -m venv venv
source venv/bin/activate
pip install -q -r requirements.txt
pip install -q -e .
python build_sync_state.py
ckb compile --fast
```

Report the compile results: "Compiled {N} pages into {M} wiki articles across {K} categories"

### Step 4.5: Generate CLAUDE.md

Write a CLAUDE.md for each tier that explains:
- What this repo is (company Knowledge Base compiled from Confluence)
- The directory structure (raw/, wiki/, output/)
- How to search: `ckb search "query"`, read wiki/_summaries.md, read wiki/_index.md
- How agents contribute: write new .md files to wiki/{category}/ with proper frontmatter
- The categories available
- That `source_space: AGENT` marks agent-contributed content

### Step 4.6: Generate README.md

Write a README.md for each tier that includes:
- Repo name and access level
- Setup instructions (clone, bash setup.sh, source venv/bin/activate)
- Authentication options (Claude Pro/Max or Anthropic API key)
- Commands reference table
- Links to other tier repos (if multiple tiers)
- Auto-sync schedule info

### Step 4.7: Generate .gitignore

```
__pycache__/
*.py[cod]
*.egg-info/
venv/
dist/
build/
.env
.env.local
.ckb-sync-state.json
.ckb-search-index.json
.DS_Store
```

---

## Phase 5: GitHub

### Step 5.1: Check for gh CLI

```bash
which gh && gh auth status
```

### Step 5.2a: With gh CLI

For each tier:
```bash
cd {tier_dir}
git init
git add -A
git commit -m "Initial commit: {Company} knowledge base - {N} pages from {M} spaces"
gh repo create {org}/{repo-name} --private --source=. --push \
  --description "{description}"
```

### Step 5.2b: Without gh CLI

Tell the user to create each repo manually on GitHub:
1. Go to https://github.com/organizations/{org}/repositories/new
2. Name: `{repo-name}`, Visibility: Private, Description: `{desc}`
3. Create repository

Then run:
```bash
cd {tier_dir}
git init
git add -A
git commit -m "Initial commit: {Company} knowledge base - {N} pages from {M} spaces"
git remote add origin https://github.com/{org}/{repo-name}.git
git branch -M main
git push -u origin main
```

Or offer to create the repos via browser automation if Chrome MCP tools are available.

### Step 5.3: Access Reminder

For each restricted tier, remind the user:
"Remember to add collaborators to {repo-name}:
Go to https://github.com/{org}/{repo-name}/settings/access
and invite the people who should have access to this tier."

---

## Phase 6: Auto-Sync

### Step 6.1: Create Scheduled Task

Use `create_scheduled_task` to set up weekly sync:

- `taskId`: `{company-slug}-kb-weekly-sync`
- `cronExpression`: `"17 7 * * 1"` (Monday 7:17 AM local)
- `description`: `"Weekly Confluence sync for {Company} Knowledge Base repos"`
- `notifyOnCompletion`: `true`

The task prompt should include:
1. The list of all tiers with: local path, GitHub remote URL, space keys and IDs
2. Instructions to pull pages using `getPagesInConfluenceSpace` MCP tool
3. Instructions to write new/updated pages to raw/
4. Instructions to run `ckb compile --fast` in each tier
5. Instructions to `git add -A && git commit && git push` for each tier with changes

### Step 6.2: Suggest First Run

Tell the user: "I recommend running the sync task once now to pre-approve the
tool permissions. This way future Monday runs won't pause for approval."

Offer to trigger it immediately.

---

## MCP Tool Reference

### Atlassian Tools (available via MCP connector)

| Tool | Required Params | Optional Params |
|------|----------------|-----------------|
| `getAccessibleAtlassianResources` | none | none |
| `getConfluenceSpaces` | `cloudId` | `limit`, `status`, `type` |
| `getPagesInConfluenceSpace` | `cloudId`, `spaceId` | `contentFormat`, `limit`, `cursor`, `sort`, `status`, `title` |
| `getConfluencePage` | `cloudId`, `pageId` | `contentFormat` |

### Scheduled Tasks

| Tool | Required Params |
|------|----------------|
| `create_scheduled_task` | `taskId`, `prompt`, `description` |
| `update_scheduled_task` | `taskId` |
| `list_scheduled_tasks` | none |

---

## Troubleshooting

**"Atlassian MCP connector not connected"**
Direct user to Claude Code settings to connect their Atlassian account.

**"No spaces found"**
Check if the user has Confluence access in their Atlassian account. Some accounts
only have Jira access.

**"Python not available"**
Instruct user to install Python 3.9+ from python.org or via their package manager.

**"gh CLI not available"**
Provide manual GitHub repo creation instructions (Step 5.2b).

**"pip install fails"**
Check Python version (3.9+ required). Try: `python3 -m pip install --upgrade pip`
then retry.

**"ckb compile fails"**
Ensure venv is activated: `source venv/bin/activate`. Check that `pip install -e .`
succeeded.

**"Rate limited during ingest"**
Add longer pauses between spaces. Process one space at a time.

**"Pages have no content"**
Some Confluence pages are container/category pages with no body text.
These are correctly skipped during ingest.
