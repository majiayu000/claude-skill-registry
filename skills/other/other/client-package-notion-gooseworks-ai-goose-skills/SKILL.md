---
type: playbook
name: client-package-notion
description: >
  Package all work done for a client into a shareable Notion page with subpages
  and Google Sheets. Reads the client's folder (strategies, campaigns, content,
  leads, notes) and builds a structured Notion workspace the client can browse.
  Lead list CSVs are uploaded to Google Sheets and linked from the Notion pages.
  Use when you want to deliver work to a client in a polished, navigable format.
tags: [content]

graph:
  provides:
    - notion-page-tree
    - google-sheet-links
  requires:
    - client-name
  connects_to:
    - skill: company-contact-finder
      when: "Lead lists reference companies that need contact enrichment before delivery"
      passes: company-name
    - skill: setup-outreach-campaign
      when: "Client approves a campaign and wants it launched in Smartlead"
      passes: lead-list, email-sequence
  capabilities: [google-sheets-write]
---

# create-client-package-notion

Package all GTM work for a client into a structured, shareable Notion page with subpages and Google Sheets. Reads the client's workspace folder and builds a navigable delivery package.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| client_name | Yes | -- | Client folder name under `clients/` (e.g., `truewind`) |
| intro_message | No | -- | Custom introduction message for the top-level page. If not provided, generate a professional intro based on the assets found. |
| recipient_name | No | -- | Name of the person receiving the package (used in intro) |
| recipient_context | No | -- | Any framing context for the delivery (e.g., "we built these to capitalize on the Botkeeper shutdown") |
| include_strategies | No | true | Whether to include strategy documents |
| include_campaigns | No | true | Whether to include campaign assets |
| include_content | No | true | Whether to include content drafts |
| include_leads | No | true | Whether to include lead lists (uploaded to Google Sheets) |
| include_conference_speakers | No | true | Whether to include conference speaker data |

## Setup

Requires access to:
- **Notion MCP server** — for creating pages and subpages
- **Rube MCP server** — for creating Google Sheets (via Composio GOOGLESHEETS tools)

No API keys need to be set manually — both are accessed through MCP.

## Procedure

### Step 1: Scan the Client Folder

Read the client folder at `clients/<client_name>/` and inventory all available assets:

```
clients/<client_name>/
├── context.md          # Client context, ICP, positioning
├── competitors.md      # Competitive landscape (optional)
├── notes.md            # Running log of decisions
├── strategies/         # Strategy documents (*.md)
├── campaigns/          # Campaign assets (folders or *.md)
├── content/            # Content drafts (blog posts, comparison pages, etc.)
└── leads/              # Lead lists (*.csv and *.md)
```

For each directory, list all files and read their contents. Build an inventory:

- **Strategies:** List of `.md` files in `strategies/` (skip orchestration prompts or internal-only files)
- **Campaigns:** List of campaign folders or `.md` files in `campaigns/`
- **Content:** List of `.md` files in `content/`
- **Leads:** List of `.csv` files (for Google Sheets upload) and `.md` files (for Notion pages) in `leads/`

If a directory doesn't exist or is empty, skip it in the output.

### Step 2: Upload Lead Lists to Google Sheets

For each `.csv` file found in `leads/`:

1. **Create a new Google Sheet** using `GOOGLESHEETS_CREATE_GOOGLE_SHEET1`
   - Title format: `<Client Name> — <Lead List Name>` (derive from filename)
   - Example: `Truewind — Botkeeper LinkedIn Leads`

2. **Parse the CSV** and write data using `GOOGLESHEETS_BATCH_UPDATE`
   - First row = headers
   - Remaining rows = data
   - Use `first_cell_location: "A1"` and `valueInputOption: "USER_ENTERED"`

3. **Record the spreadsheet URL** for linking in Notion pages later

If there are multiple CSVs, create sheets in parallel.

### Step 3: Plan the Notion Page Structure

Design the page hierarchy based on what assets exist. The general pattern is:

```
Top-Level Page: "<Client Name> — GTM Engineering Package"
├── Introduction (on the top-level page itself)
├── Strategies (subpage — all strategy docs combined or as separate child pages)
├── <Signal-Specific Section> (subpage — groups campaigns + content for a specific signal)
│   ├── Campaign 1 (subpage)
│   ├── Campaign 2 (subpage)
│   ├── Content Asset 1 (subpage)
│   └── Content Asset 2 (subpage)
├── Conference Speakers (subpage — if speaker data exists)
└── Lead Lists (linked as Google Sheets from relevant pages)
```

**Grouping logic:**
- If campaigns and content assets share a common theme (e.g., "botkeeper"), group them under a themed section
- If campaigns are standalone, list them at the top level
- Lead list Google Sheet links should appear on the pages where they're most relevant (e.g., LinkedIn leads linked from the LinkedIn engagement page)
- Conference/speaker data gets its own top-level subpage

**When assets don't fit a theme:** Create a "Campaigns" subpage and a "Content" subpage as catch-all sections.

Present the planned structure to the user and confirm before creating pages.

### Step 4: Create the Top-Level Notion Page

Create a standalone workspace-level page with:

**Title:** `<Client Name> — GTM Engineering: Growth Strategies & Execution` (or similar)

**Content:** An introduction section that includes:
- A greeting to the recipient (if `recipient_name` provided)
- A summary of what's inside (list the sections with brief descriptions)
- Links to the Google Sheets with lead lists
- Any framing context from `recipient_context`
- A closing line

If `intro_message` is provided, use it as-is. Otherwise, generate a professional intro based on:
- What asset types exist (strategies, campaigns, content, leads)
- How many leads were found
- What the key themes are (inferred from strategy/campaign filenames)

Use Notion-flavored Markdown. Do NOT include the page title in the content (Notion renders it automatically from properties).

### Step 5: Create Subpages

For each section in the planned structure, create subpages under the top-level page:

**For strategy documents:**
- Read the full `.md` content from the file
- Convert to Notion-flavored Markdown (adjust table syntax, escape special characters)
- Create as a subpage with the strategy title

**For campaign documents:**
- Read the full `.md` content
- Insert Google Sheet links where lead lists are referenced
- Create as a subpage

**For content assets (blog posts, comparison pages):**
- Read the full `.md` content
- Create as a subpage with the article title

**For lead/conference data in `.md` format:**
- Read the full `.md` content
- Create as a subpage

**For grouped sections (e.g., "Botkeeper Strategies"):**
- Create a parent subpage with a summary/index of what's inside
- Create child subpages under the parent for each individual asset
- Link relevant Google Sheets from the parent summary

Create pages in batches where possible (the Notion API supports creating multiple pages in one call when they share a parent).

### Step 6: Verify and Report

After all pages are created, output a summary:

```
## Package Created

**Top-level page:** [<title>](<notion-url>)

**Subpages:**
- [Strategies](<url>) — 2 strategy documents
- [Botkeeper Strategies](<url>) — 4 assets (2 campaigns, 2 content pieces)
  - [LinkedIn Engagement](<url>)
  - [Listicle Author Outreach](<url>)
  - [SEO Article](<url>)
  - [Comparison Page](<url>)
- [Conference Speakers](<url>)

**Google Sheets:**
- [Lead List 1](<sheets-url>) — 12 leads
- [Lead List 2](<sheets-url>) — 9 leads

**Total:** X pages created, Y Google Sheets created
```

## Notion Markdown Notes

When converting client `.md` files to Notion content, keep these in mind:

- **Tables:** Notion uses `<table>` XML syntax, but standard markdown tables (`| col | col |`) also work
- **Escape special characters:** `\* \~ \` \$ \[ \] \< \> \{ \} \| \^`
- **Links:** Standard markdown `[text](url)` works
- **No H1 in content:** The page title is rendered automatically — start content at H2 or below
- **Empty lines:** Use `<empty-block/>` for intentional blank lines (regular blank lines are stripped)
- **Code blocks:** Do NOT escape characters inside code blocks
- **Subpages:** Use `<page url="...">Title</page>` to reference existing child pages (but pages are created via the API, not inline)

## Output Format

The skill produces:
1. A Notion page URL (top-level) that can be shared with the client
2. A list of all subpage URLs
3. A list of Google Sheet URLs with lead data

## Example Prompts

- "Package everything we've done for Truewind into a Notion page I can send to the founder"
- "Create a client delivery package for Acme Corp with all our campaign work"
- "Build a Notion package for [client] — include strategies, campaigns, and lead lists"
- "Take our work in clients/truewind and create a shareable Notion workspace"
- "Package the client folder into something I can send to the CEO"

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Notion page creation fails | Check that the Notion MCP server is connected. Try creating a simple test page first. |
| Google Sheets creation fails | Verify the Rube MCP server is connected and Google Sheets has an active connection. Run `RUBE_MANAGE_CONNECTIONS` with `toolkits: ["googlesheets"]`. |
| CSV parsing errors | Check the CSV for encoding issues. The skill expects UTF-8 CSVs with a header row. |
| Notion content looks wrong | Review Notion-flavored Markdown spec. Common issues: unescaped special characters, H1 in content (conflicts with page title), or raw HTML that Notion doesn't support. |
| Too many pages to create | Notion API supports batch page creation (up to 100 pages per call with shared parent). Group subpages by parent and batch create. |
| Lead list is empty or malformed | Skip that CSV and note it in the summary. Don't create an empty Google Sheet. |

## Metadata

```yaml
metadata:
  requires:
    mcp_servers: ["notion", "rube"]
  cost: "Free (Notion API + Google Sheets via Composio)"
```
