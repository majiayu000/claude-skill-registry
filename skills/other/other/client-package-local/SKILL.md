---
type: playbook
name: client-package-local
description: >
  Package all work done for a client into a local filesystem delivery package
  with .md files and Google Sheets. Reads the client's folder (strategies, campaigns,
  content, leads, notes) and builds a structured directory with dated deliverables.
  Lead lists are uploaded to Google Sheets and linked from the markdown files.
  Use when you want to deliver work to a client in a polished, navigable format
  without requiring Notion.
tags: [content]

graph:
  provides:
    - client-package-directory
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
  capabilities: [google-sheets-write, csv-export]
---

# create-client-package

Package all GTM work for a client into a structured local delivery package with dated .md files and Google Sheets. Reads the client's workspace folder and builds a navigable directory of deliverables.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| client_name | Yes | -- | Client folder name under `clients/` (e.g., `truewind`) |
| date | No | today's date | Date string in `YYYY-MM-DD` format, used for folder and file naming |
| intro_message | No | -- | Custom introduction message for the overview file. If not provided, generate one based on assets found. |
| recipient_name | No | -- | Name of the person receiving the package (used in intro) |
| recipient_context | No | -- | Any framing context for the delivery (e.g., "we built these to capitalize on the Botkeeper shutdown") |
| include_strategies | No | true | Whether to include strategy documents |
| include_campaigns | No | true | Whether to include campaign assets |
| include_content | No | true | Whether to include content drafts |
| include_leads | No | true | Whether to include lead lists (uploaded to Google Sheets) |

## Setup

Requires access to:
- **Rube MCP server** — for creating Google Sheets (via Composio GOOGLESHEETS tools)

No API keys need to be set manually — Google Sheets access is through MCP.

## Output Directory Structure

```
clients/<client_name>/client-package/<YYYY-MM-DD>/
├── Overview - <YYYY-MM-DD>.md
├── Lead Lists - <YYYY-MM-DD>.md
└── Strategies - <YYYY-MM-DD>/
    ├── <Strategy 1 Name>/
    │   ├── overview.md
    │   ├── <Substrategy 1 Name> - <YYYY-MM-DD>.md
    │   ├── <Substrategy 2 Name> - <YYYY-MM-DD>.md
    │   ├── <substrategy-1-leads>.csv
    │   └── <substrategy-2-leads>.csv
    ├── <Strategy 2 Name>/
    │   ├── overview.md
    │   ├── ...
    └── ...
```

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
└── leads/              # Lead lists (*.csv, *.json, *.md)
```

For each directory, list all files and read their contents. Build an inventory:

- **Strategies:** List of `.md` files in `strategies/` (skip `ORCHESTRATION-PROMPT.md` and other internal-only files)
- **Campaigns:** List of campaign folders or `.md` files in `campaigns/`
- **Content:** List of `.md` files in `content/`
- **Leads:** List of `.csv` and `.json` files in `leads/` (for Google Sheets upload) and `.md` files (for reference)

If a directory doesn't exist or is empty, skip it.

### Step 2: Identify Strategies and Map Assets

Each strategy in `strategies/` is a top-level theme. For each strategy:

1. **Read the strategy .md file** to understand the strategy name, summary, and execution plan
2. **Map campaigns to strategies** — match campaigns in `campaigns/` to strategies by name/theme (e.g., `hiring-hurting-outreach` maps to the `hiring-hurting` strategy)
3. **Map content to strategies** — match content in `content/` to strategies by name/theme (e.g., `botkeeper-shut-down-what-accounting-firms-should-do-next.md` maps to `botkeeper-shutdown` strategy)
4. **Map leads to strategies** — match lead files in `leads/` to strategies by name/theme (e.g., `botkeeper-linkedin-leads.csv` maps to `botkeeper-shutdown` strategy)

Assets that don't clearly map to a strategy should be grouped under a "General" or "Ungrouped" section.

### Step 3: Upload Lead Lists to Google Sheets

For each lead list file (`.csv` or `.json`) found in `leads/`:

1. **Parse the file** and extract structured data
   - For `.csv`: parse directly
   - For `.json`: read the JSON, flatten into tabular format

2. **Ensure required columns exist.** Every Google Sheet MUST include these columns (add them if missing, populate with available data or mark as "N/A"):
   - `Name` — lead's full name
   - `Company` — company name
   - `Title` — job title
   - `LinkedIn URL` — LinkedIn profile URL
   - `Source` — how we found them (e.g., "LinkedIn Post", "Job Posting", "Conference", "Web Archive")
   - `Qualification Status` — e.g., "Qualified", "Not Qualified", "Needs Review"
   - `Qualification Reasoning` — why they qualified or didn't

   Additional columns from the source data should be preserved after the required columns.

3. **Create a new Google Sheet** using `RUBE_SEARCH_TOOLS` to find `GOOGLESHEETS_CREATE_GOOGLE_SHEET1`, then execute:
   - Title format: `<Client Name> — <Lead List Name> (<date>)`
   - Example: `Truewind — Botkeeper LinkedIn Leads (2026-02-24)`

4. **Write data** using `GOOGLESHEETS_BATCH_UPDATE`:
   - First row = headers (required columns first, then additional columns)
   - Remaining rows = data
   - Use `first_cell_location: "A1"` and `valueInputOption: "USER_ENTERED"`

5. **Record the spreadsheet URL** for linking in the Lead Lists summary file

If there are multiple lead files, create sheets in parallel where possible.

### Step 4: Create the Package Directory

Create the output directory structure:

```bash
mkdir -p clients/<client_name>/client-package/<date>
mkdir -p clients/<client_name>/client-package/<date>/Strategies - <date>
```

### Step 5: Create the Overview File

Create `Overview - <date>.md` with:

- A greeting to the recipient (if `recipient_name` provided)
- A summary of the engagement — what strategies were developed, how many leads were found, what campaigns were built
- A table of contents linking to the other files in the package
- Any framing context from `recipient_context`
- A closing line

Example structure:

```markdown
# GTM Engineering Package — <Client Name>

**Prepared:** <date>
**For:** <recipient_name> (if provided)

## Summary

<Brief overview of what was done — strategies developed, leads found, campaigns built>

## What's Inside

### Strategies
- **<Strategy 1>** — <one-line summary>
- **<Strategy 2>** — <one-line summary>

### Lead Lists
See [Lead Lists - <date>](./Lead Lists - <date>.md) for all lead lists with Google Sheet links.

**Total leads found:** <count across all lists>

### Campaigns
<List of campaigns built, with which strategy they belong to>

### Content
<List of content pieces created>

---

<closing line>
```

### Step 6: Create the Lead Lists File

Create `Lead Lists - <date>.md` with:

- A bulleted list of all Google Sheet links created in Step 3
- For each sheet: the name, number of leads, a brief description of the source/strategy, and the Google Sheet URL

Example:

```markdown
# Lead Lists — <Client Name>

**Date:** <date>

## Sheets

- **[Truewind — Botkeeper LinkedIn Leads](https://docs.google.com/spreadsheets/d/...)** — 10 leads from LinkedIn posts/comments about Botkeeper shutdown
- **[Truewind — Hiring Signal Leads](https://docs.google.com/spreadsheets/d/...)** — 25 leads from job posting intent signals
- **[Truewind — Conference Speakers Q1-Q2 2026](https://docs.google.com/spreadsheets/d/...)** — 15 leads from accounting conference speaker lists

**Total:** X leads across Y sheets
```

### Step 7: Create Strategy Subfolders

For each strategy identified in Step 2, create a subfolder under `Strategies - <date>/`:

```
Strategies - <date>/
└── <Strategy Name>/
    ├── overview.md
    ├── <Substrategy/Campaign 1> - <date>.md
    ├── <Substrategy/Campaign 2> - <date>.md
    ├── <substrategy-1-leads>.csv
    └── <substrategy-2-leads>.csv
```

#### overview.md

A summary of the strategy:
- Strategy name and one-paragraph summary
- The signal being tracked
- Target ICP / filters
- List of substrategies, campaigns, and content pieces with brief descriptions
- Links to the Google Sheets for any related lead lists

#### Substrategy / Campaign .md files

For each campaign or content asset mapped to this strategy:
- Copy the meaningful content from the original file
- Clean up any internal-only notes or orchestration details
- Include links to relevant Google Sheets
- Name the file: `<Descriptive Name> - <date>.md`

#### Lead .csv files

For each lead list that maps to this strategy:
- Export a copy of the lead data as a `.csv` file in the strategy subfolder
- Use the standardized columns (Name, Company, Title, LinkedIn URL, Source, Qualification Status, Qualification Reasoning) plus any additional relevant columns
- Name the file descriptively: `<strategy-name>-leads.csv` or `<specific-source>-leads.csv`

### Step 8: Verify and Report

After all files are created, output a summary:

```
## Package Created

**Location:** clients/<client_name>/client-package/<date>/

**Files:**
- Overview - <date>.md
- Lead Lists - <date>.md
- Strategies - <date>/
  - <Strategy 1>/
    - overview.md
    - <Substrategy 1> - <date>.md
    - <substrategy-1>-leads.csv
  - <Strategy 2>/
    - overview.md
    - ...

**Google Sheets:**
- [Lead List 1](<sheets-url>) — 12 leads
- [Lead List 2](<sheets-url>) — 9 leads

**Total:** X files created, Y Google Sheets created, Z total leads
```

## Example Prompts

- "Package everything we've done for Truewind into a shareable folder"
- "Create a client delivery package for Acme Corp with all our work"
- "Build a package for [client] — include strategies, campaigns, and lead lists"
- "Take our work in clients/truewind and create a deliverable"
- "Package the client folder into something I can send to the founder"

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Google Sheets creation fails | Verify the Rube MCP server is connected and Google Sheets has an active connection. Run `RUBE_MANAGE_CONNECTIONS` with `toolkits: ["googlesheets"]`. |
| CSV parsing errors | Check the CSV for encoding issues. The skill expects UTF-8 CSVs with a header row. |
| JSON lead files have nested structure | Flatten the JSON to tabular format before uploading. Extract the key fields into the required columns. |
| Lead list is empty or malformed | Skip that file and note it in the summary. Don't create an empty Google Sheet. |
| Strategy mapping is ambiguous | When a campaign or lead list could belong to multiple strategies, place it under the most specific match. If truly ambiguous, ask the user. |
| No strategies folder exists | Create a single "General" strategy folder and place all assets there. |

## Metadata

```yaml
metadata:
  requires:
    mcp_servers: ["rube"]
  cost: "Free (Google Sheets via Composio)"
```
