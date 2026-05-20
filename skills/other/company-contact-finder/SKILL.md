---
name: company-contact-finder
description: >
  Find decision-makers at a specific company using Crustdata and SixtyFour
  people search via Gooseworks MCP. Given a company name and target titles,
  returns a list of contacts with name, title, LinkedIn URL, and location.
tags: [lead-generation]
---

# company-contact-finder

Find decision-makers at a specific company by name and target titles. Uses Gooseworks MCP tools (Crustdata + SixtyFour databases) with a layered fallback strategy to maximize results.

## Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| company_name | Yes | -- | The company to search (e.g., "EisnerAmper") |
| company_linkedin_url | No | -- | Company LinkedIn URL for disambiguation |
| target_titles | Yes | -- | List of titles to find (e.g., ["Partner", "Controller", "VP Finance"]) |
| num_results | No | 10 | How many contacts to return |

## Procedure

### Step 1: Understand the Request

Parse the user's request to extract:
- **company_name** (required) -- the company to search at
- **company_linkedin_url** (optional) -- helps disambiguate common names
- **target_titles** (required) -- list of job titles or roles to find (e.g., ["Partner", "Controller", "VP Finance", "CFO"])
- **num_results** (optional, default 10) -- how many contacts to return

If the user does not provide target titles, ask for them. Suggest common senior titles based on context:
- For accounting/CPA firms: Partner, Managing Director, Controller, CFO, VP Finance
- For tech companies: VP Engineering, CTO, Head of Product, Director of Engineering
- For general B2B: VP, Director, C-Level, Head of

### Step 2: Natural Language Search (Primary)

This is the fastest and most flexible search method. Build a natural-language query and call the Crustdata NL search.

**Build the query string:**
Join target titles with " OR " and append the company name:
```
"[title1] OR [title2] OR [title3] at [company_name]"
```

**Example:**
```
"Partner OR Controller OR VP Finance at EisnerAmper"
```

**Call:**
```
mcp__gooseworks__crustdata_nl_search(
  query: "Partner OR Controller OR VP Finance at EisnerAmper",
  num_results: 10
)
```

**Parse the response:**
Each result contains: name, title, company, LinkedIn URL, location, and other profile fields. Extract and collect all results into a working list.

### Step 3: Evaluate Results

Check how many results from Step 2 match the target titles at the target company.

**Quality checks:**
1. Filter out results where the company name does not match (fuzzy match is fine -- "EisnerAmper LLP" matches "EisnerAmper")
2. Filter out results where the title does not reasonably match any target title
3. Count remaining high-quality matches

**Decision:**
- If 3+ quality matches found: skip to Step 6 (Output)
- If fewer than 3 quality matches: proceed to Step 4

### Step 4: Structured Filter Search (Fallback 1)

Use Crustdata's structured filter search for more precise matching. Run one search per target title, then merge results.

**For each target title, call:**
```
mcp__gooseworks__crustdata_search(
  filters: {
    "op": "and",
    "conditions": [
      {"column": "current_employers.name", "type": "in", "value": ["[company_name]"]},
      {"column": "current_employers.title", "type": "(.)", "value": "[target_title]"}
    ]
  },
  limit: 25
)
```

**Example for "Partner" at EisnerAmper:**
```
mcp__gooseworks__crustdata_search(
  filters: {
    "op": "and",
    "conditions": [
      {"column": "current_employers.name", "type": "in", "value": ["EisnerAmper"]},
      {"column": "current_employers.title", "type": "(.)", "value": "Partner"}
    ]
  },
  limit: 25
)
```

**Optional seniority filter:** If the user requests senior decision-makers broadly (rather than specific titles), use the seniority_level filter:
```
{"column": "current_employers.seniority_level", "type": "in", "value": ["VP", "C-Level", "Director"]}
```

**After all title searches complete:**
1. Merge all results into one list
2. Deduplicate by LinkedIn URL (keep the first occurrence)
3. Combine with results from Step 2

**Decision:**
- If 3+ total unique quality matches: skip to Step 6 (Output)
- If still fewer than 3: proceed to Step 5

### Step 5: SixtyFour Search (Fallback 2)

SixtyFour is an alternative people database that may have profiles Crustdata does not.

**Call:**
```
mcp__gooseworks__sixtyfour_nl_search(
  query: "[title1] OR [title2] OR [title3] at [company_name]",
  num_results: 10,
  timeout_ms: 30000
)
```

**After results return:**
1. Parse results (format may differ from Crustdata -- extract name, title, company, LinkedIn URL, location)
2. Merge with all previous results
3. Deduplicate by LinkedIn URL

### Step 6: Output

Present the final deduplicated contact list.

**Table format (for the user):**

| # | Name | Title | Company | LinkedIn URL | Location |
|---|------|-------|---------|--------------|----------|
| 1 | Jane Smith | Partner | EisnerAmper | https://linkedin.com/in/janesmith | New York, NY |
| 2 | John Doe | Controller | EisnerAmper | https://linkedin.com/in/johndoe | Chicago, IL |
| ... | | | | | |

**JSON format (for downstream skills):**

```json
{
  "company": "EisnerAmper",
  "search_titles": ["Partner", "Controller", "VP Finance"],
  "contacts": [
    {
      "name": "Jane Smith",
      "title": "Partner",
      "company": "EisnerAmper",
      "linkedin_url": "https://linkedin.com/in/janesmith",
      "location": "New York, NY"
    }
  ],
  "total_found": 10,
  "sources": ["crustdata_nl", "crustdata_structured", "sixtyfour"]
}
```

**Summary line:**
> Found X contacts matching [titles] at [company]. Sources used: [list of sources that returned results].

If fewer than 3 contacts were found after all fallbacks, tell the user:
> Only found X contacts. The company may be small, the titles may be uncommon, or the databases may have limited coverage for this company. Consider broadening the target titles or trying alternate company name spellings.

---

## Gooseworks MCP Tools Reference

| Tool | Purpose | Key Params |
|------|---------|------------|
| `mcp__gooseworks__crustdata_nl_search` | Natural-language people search | `query` (string), `num_results` (int, max 5000), `exclude_profiles` (LinkedIn URLs to skip) |
| `mcp__gooseworks__crustdata_search` | Structured filter search | `filters` (JSON), `limit` (max 1000), `offset` (pagination) |
| `mcp__gooseworks__crustdata_preview` | Preview result count before full search | `query` or `filters` |
| `mcp__gooseworks__crustdata_enrich` | Enrich a single person by LinkedIn URL | `linkedin_url` |
| `mcp__gooseworks__sixtyfour_nl_search` | Alternative NL people search | `query`, `num_results` (max 5000), `timeout_ms` (max 600000) |

### Structured Filter Columns

| Column | Operators | Example Values |
|--------|-----------|----------------|
| `current_employers.name` | `in` (exact list) | `["EisnerAmper", "EisnerAmper LLP"]` |
| `current_employers.title` | `(.)` (fuzzy), `in` (exact) | `"Partner"`, `["Partner", "Managing Partner"]` |
| `current_employers.seniority_level` | `in` | `["VP", "C-Level", "Director", "Manager"]` |
| `current_employers.company_headcount_latest` | `=>`, `<=` | `50`, `1000` |

---

## Examples

### Basic: Find Partners and Controllers at EisnerAmper
```
Find Partners and Controllers at EisnerAmper
```
Agent builds query: `"Partner OR Controller at EisnerAmper"`, calls `crustdata_nl_search` with `num_results=10`.

### With more titles: Find VP Finance and CFO at Sage Intacct users
```
Find VP Finance and CFO at companies using Sage Intacct
```
Agent builds query: `"VP Finance OR CFO at Sage Intacct"`.

### Senior leaders at a specific firm
```
Find Managing Directors at CPA firms in San Francisco
```
Agent builds query: `"Managing Director at CPA firm San Francisco"`.

### With a LinkedIn URL for disambiguation
```
Find Partners at EisnerAmper (https://linkedin.com/company/eisneramper)
```
Agent uses the company name "EisnerAmper" and can use the LinkedIn URL for enrichment if needed.

---

## Troubleshooting

### MCP tools not available / connection errors

The Gooseworks MCP tools require the Gooseworks MCP server to be configured in your environment. If you get errors like "tool not found" or connection failures:

1. **Check MCP server configuration:** Ensure the Gooseworks MCP server is listed in your MCP configuration (e.g., `claude_desktop_config.json` or equivalent).
2. **Server URL:** The Gooseworks server must be running and accessible. Check with your workspace admin for the correct server endpoint.
3. **Authentication:** Gooseworks may require an API key or auth token. Ensure credentials are configured in your MCP server settings.

### No results returned

- Try alternate spellings of the company name (e.g., "EisnerAmper" vs "Eisner Amper" vs "EisnerAmper LLP")
- Broaden target titles (e.g., add "Managing Director" alongside "Partner")
- Use the structured search (Step 4) with fuzzy title matching `(.)` operator
- Try SixtyFour as an alternative database (Step 5)

### Too many irrelevant results

- Add more specific title terms rather than broad ones
- Use the structured search with the `in` operator for exact title matching instead of fuzzy `(.)`
- Filter results by seniority_level to restrict to senior roles

### Duplicate contacts across sources

The skill deduplicates by LinkedIn URL automatically. If you see near-duplicates with slightly different URLs (e.g., trailing slashes), normalize URLs before deduplication by stripping trailing slashes and query parameters.

---

## Metadata

```yaml
metadata:
  requires:
    mcp_servers: ["gooseworks"]
  cost: "Free (Gooseworks MCP usage)"
```
