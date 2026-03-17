---
name: niche-signal-discovery
description: "Discover niche first-party signals that differentiate Closed Won vs Closed Lost accounts for ICP analysis. Use when the user provides won/lost customer domain lists and wants differential signals (website content, job listings, tech stack, maturity markers) to build account scoring models and prospecting criteria. Triggers: ICP analysis, niche signals, won vs lost analysis, differential signals, signal discovery, ICP signal report, account scoring signals, lead scoring, first-party signals, buyer signals."
---

# Niche Signal Discovery

Discover differential signals between Closed Won and Closed Lost accounts by extracting multi-page website content and job listings, then computing Laplace-smoothed lift scores to identify what distinguishes buyers from non-buyers.

## Prerequisites

**Required:**

- **Deepline CLI** — All enrichment runs through `deepline enrich` (no separate API keys for exa, crustdata, etc.)
- **Python 3** — Analysis script uses standard library only (csv, json, re, argparse — no pip packages)

**NOT required:**

- ❌ No exa API key (accessed via Deepline)
- ❌ No crustdata API key (accessed via Deepline)
- ❌ No external Python packages (no pip install needed)
- ❌ No OpenAI/Anthropic API keys (deterministic analysis, no LLM calls)

**Credits:** Enrichment consumes Deepline credits (~6 credits/company for exa + crustdata). Always get user approval before running paid enrichment.

## Deepline-First Principle

**Always use Deepline CLI (`deepline enrich`, `deepline tools`, `deepline playground`) for enrichment, data extraction, and batch operations.** Deepline provides:
- Batch enrichment with automatic CSV column management
- Built-in tool integrations (exa_search, crustdata, apollo, etc.)
- Playground UI for inspecting and iterating on enrichment results
- Idempotent reruns — re-running updates existing columns instead of duplicating

Use `deepline enrich` for all enrichment steps. Use `deepline tools execute` for one-off tool calls. Use `deepline playground` for inspecting results. Refer to the `gtm-meta-skill` for Deepline command patterns and provider playbooks.

## Input Requirements

- Won and lost customer domain lists (minimum 20 won + 10 lost for statistical significance)
- **Target company context** — What they sell, who they sell to, key personas (discovered in Step 0)

## Pipeline

```
0. Discover target company (what they sell, who they sell to, differentiation)
0.5. Discover ecosystem (competitors, tech stack category, buyer personas)
1. Prepare input CSV (domain, status)
1.5. Generate vertical-specific configs (keywords, tools, job roles)
2. Multi-page website extraction + job listings (Deepline enrichment)
3. Quality gate — verify coverage (>80% with content)
3.5. Review generated configs (validate against enriched data)
4. Run differential analysis (scripts/analyze_signals.py)
5. Generate report (using references/report-template.md)
6. Review with signal interpretation rules (references/signal-interpretation.md)
```

## Step 0: Target Company Discovery

**CRITICAL: Do this FIRST before any enrichment or config generation.**

Use web search to understand what the target company sells and who they sell to:

```bash
# Example for Air Inc
WebSearch: "air.inc product what do they sell"
WebSearch: "air.inc customers use cases who uses"
WebFetch: https://air.inc/ "What does Air.inc sell? Who are their target customers?"
```

**Document the following:**

1. **Product category** — e.g., "Creative Operations & DAM platform", "AR automation software", "Sales engagement platform"
2. **Target buyer persona** — e.g., "Marketing and creative teams", "Finance/AR teams", "Sales Development Reps"
3. **Key differentiation** — What makes them unique vs competitors
4. **Example customers** (if available) — Who currently uses the product

**Why this matters:** The entire pipeline (exa query, keywords, tech stack, job roles) adapts based on this discovery. Skipping this step results in generic/irrelevant signals.

## Step 0.5: Ecosystem Discovery

Use web search to discover the competitive landscape and buyer ecosystem:

**Competitor Discovery:**
```bash
WebSearch: "{product category} software companies"
WebSearch: "{product category} alternatives competitors"
```

Example for Air Inc (creative ops/DAM):
```bash
WebSearch: "creative operations software digital asset management platforms"
WebSearch: "DAM software alternatives Bynder Widen competitors"
```

**Tech Stack Discovery:**
```bash
WebSearch: "{buyer persona} common tools tech stack"
WebSearch: "{industry} companies use what software"
```

Example for Air Inc (marketing/creative teams):
```bash
WebSearch: "marketing teams creative teams common tools software stack"
WebSearch: "creative operations teams use Figma Adobe tools integrations"
```

**Job Role Discovery:**
```bash
WebSearch: "{buyer persona} job titles roles responsibilities"
WebSearch: "companies hiring {buyer persona} job listings"
```

Example for Air Inc:
```bash
WebSearch: "creative operations job titles creative director content manager roles"
WebSearch: "companies hiring creative operations manager brand manager"
```

**Document findings:**

- Competitor products (3-5 names) — Used to identify migration opportunities (companies currently using these tools)
- Common tech stack tools (10-15 by category) — Used for infrastructure signals
- Buyer job titles (10-15 variations) — Used for hiring intent signals

## Step 1: Prepare Input CSV

Create `output/{company}-icp-input.csv`:

```csv
domain,status
customer1.com,won
customer2.com,won
non-customer1.com,lost
non-customer2.com,lost
```

## Step 1.5: Generate Vertical-Specific Configs

**Using the discovery from Steps 0 and 0.5**, create three JSON config files.

See `references/keyword-catalog.md` for JSON format and generation guidance.

```bash
# Create config files in output/{company}/
output/{company}-keywords.json    # keyword categories
output/{company}-tools.json       # tech stack tools by category
output/{company}-job-roles.json   # job role categories
```

**Generation approach:**

1. **Keywords** — Mix of:
   - Product category terms (e.g., "creative ops", "asset management" for Air Inc)
   - Buyer pain points (e.g., "fragmented tools", "content discovery")
   - Competitor names for migration segment (e.g., "bynder", "widen") — companies using these are migration opportunities, not excluded
   - Generic business maturity (e.g., "security", "compliance", "integrations")

2. **Tech Stack** — Tools from ecosystem discovery:
   - Infrastructure tools buyer persona uses (e.g., "figma", "adobe creative cloud")
   - Adjacent tools in buyer workflow (e.g., "contentful", "monday.com")
   - Competitor tools for migration segment — companies using these represent displacement opportunities

3. **Job Roles** — Titles from role discovery:
   - Buyer persona variations (e.g., "creative director", "content manager", "brand manager")
   - Adjacent roles (e.g., "marketing operations", "brand designer")
   - Generic growth roles (e.g., "product", "engineering")

**Example generation for Air Inc** (creative ops/DAM):

```json
// keywords.json
{
  "creative_operations": [
    "creative ops", "creative operations", "asset management", "DAM",
    "content library", "brand guidelines", "creative workflow", "creative review"
  ],
  "buyer_pain_points": [
    "fragmented tools", "content discovery", "version control",
    "creative approval", "asset organization", "brand consistency"
  ],
  "business_model": [
    "contact sales", "plan", "enterprise", "pricing", "demo",
    "subscription", "free trial"
  ],
  "company_maturity": [
    "compliance", "security", "integration", "api", "sso", "soc 2"
  ],
  "anti_fit": [
    "bynder", "widen", "brandfolder", "canto", "dam platform"
  ]
}
```

```json
// tools.json
{
  "creative_design": [
    "figma", "sketch", "adobe creative cloud", "canva", "invision"
  ],
  "marketing_ops": [
    "hubspot", "marketo", "contentful", "wordpress", "webflow"
  ],
  "project_management": [
    "monday.com", "asana", "jira", "clickup", "notion"
  ],
  "video_production": [
    "frame.io", "vimeo", "wistia", "loom"
  ]
}
```

```json
// job-roles.json
{
  "creative_leadership": ["creative director", "head of creative", "vp creative"],
  "content_management": ["content manager", "content director", "brand manager"],
  "creative_ops": ["creative operations", "creative ops manager", "brand operations"],
  "marketing_ops": ["marketing operations", "marops", "marketing ops manager"],
  "design": ["product designer", "brand designer", "visual designer"],
  "marketing_general": ["marketing manager", "demand gen", "growth marketing"]
}
```

**Validation:** Do the generated configs match the target's vertical and buyer persona? If not, refine based on Step 0/0.5 findings.

## Step 2: Deepline Enrichment

**CRITICAL: Never scrape just the homepage.** Use `exa_search` with `contents.text` to discover AND scrape ~8 pages per domain in a single API call.

**Generate exa query dynamically based on target's product category:**

```bash
# Generic query (works for most B2B SaaS)
QUERY="company product features integrations customers security pricing careers about case-studies"

# Vertical-specific adjustments:
# - Creative/marketing tools: add "portfolio", "use cases", "creative workflow"
# - Finance tools: add "compliance", "reporting", "accounting integrations"
# - Sales tools: add "playbooks", "outbound", "pipeline"
# - Developer tools: add "documentation", "api reference", "github"
```

**Example for Air Inc (creative ops):**

```bash
deepline enrich \
  --input output/air-inc-icp-input.csv \
  --output output/air-inc-enriched.csv \
  --with 'website=exa_search:{"query":"company product features portfolio use cases creative workflow customers integrations security pricing careers about","numResults":8,"type":"auto","includeDomains":["{{domain}}"],"contents":{"text":{"maxCharacters":3000,"verbosity":"compact","includeSections":["body"]}}}' \
  --with 'jobs=crustdata_job_listings:{"companyDomains":"{{domain}}","limit":50}' \
  --json
```

**Why exa_search with contents (not parallel_extract)?**
- Discovers pages AND returns content in one call — no separate page discovery step
- ~8 pages per domain, ~3K chars each = ~24K chars per company
- Cost: ~5 credits/company (exa) + ~1 credit (crustdata jobs) = ~6 credits/company

Get user credit approval before running. Example: "60 companies x 6 credits = ~360 credits."

## Step 3: Quality Gate

After enrichment, verify before proceeding:
- **Coverage**: >80% of companies should have website content. If <80%, check domain spelling and retry failed rows.
- **Content depth**: Average should be 6-8 pages per company, 12-20K chars.
- **Job listings**: Won companies should have more job data than lost (expected — larger/scaling companies win more).

If coverage is poor, re-run failed domains with `--rows` targeting specific rows.

## Step 3.5: Review Generated Configs

**Before running analysis**, spot-check the generated configs against enriched data:

```bash
# Sample a few enriched companies
deepline playground output/{company}-enriched.csv

# In playground UI, check:
# - Do website pages mention the keywords in keywords.json?
# - Do job listings mention the roles in job-roles.json?
# - Do integrations/tech stack pages mention the tools in tools.json?
```

**Red flags:**

- Keywords appear in <10% of enriched companies → too niche, broaden
- Keywords appear in >90% of companies → too generic, refine
- Product category keywords (what the target SELLS) appear frequently in Won companies → wrong product category, these companies are competitors not buyers
- Job roles missing from actual job listings → wrong buyer persona, revise

**Fix and re-generate configs if needed.**

## Step 4: Differential Analysis

Run the analysis script with the config files:

```bash
python3 scripts/analyze_signals.py \
  --input output/{company}-enriched.csv \
  --keywords output/{company}-keywords.json \
  --tools output/{company}-tools.json \
  --job-roles output/{company}-job-roles.json \
  --output output/{company}-analysis.json
```

The script auto-detects `__dl_full_result__` columns for website and jobs data. Override with `--website-col N --jobs-col N` if needed.

**What the script computes:**

- Substring-match presence per company per keyword (NOT exact-token TF-IDF)
- Laplace-smoothed lift: `((won + 0.5) / (won_total + 1)) / ((lost + 0.5) / (lost_total + 1))`
- Source breakdown per keyword (website only / jobs only / both)
- Tech stack tool mentions across categories
- Job role prevalence in won vs lost
- Anti-fit signals (lift < 0.5x)
- Source evidence: exact quotes (±40 chars) with page URLs and job listing URLs per keyword

## Step 5: Report Generation

Read `references/report-template.md` for the full report structure and quality rules.

Key quality rules:
- **Raw counts always**: `15% (6)` not just `15%`
- **Sample sizes in headers**: `Won (n=37)`, `Lost (n=18)`
- **Bold only lift > 2x**
- **Source evidence required**: After each keyword table, add exact quotes with linked sources for top 3 keywords. The analysis script outputs `evidence` per keyword with `company`, `source_type`, `quote`, `url`, and `page_title`/`job_title`. Format:
  ```
  > **Evidence — "keyword":**
  > - [company.com](url) (page title): "...exact quote with keyword..."
  > - [company.com](url) (job: "Job Title"): "...exact quote from listing..."
  ```
- **Source breakdown for hiring signals**: Add a Source column showing `3w / 20j / 2both` format
- **Niche tech stack tools**: Report specific SaaS tools by category, not generic keywords
- **Anti-fit signals in separate section**
- **Interpretation column required**: Explains WHY each signal matters for the target company

## Step 6: Signal Interpretation Review

Read `references/signal-interpretation.md` before writing interpretation columns. Key rules:
- Website content mentioning what the target sells = competitor signal (NOT buyer)
- Job listings = highest-intent buyer signal
- Same keyword means different things on product page vs careers page vs blog
- Tech stack tools need context — do they create or solve the target's problem?

## Enrichment Data Structure

Website data: `__dl_full_result__` column containing exa_search response.
```
data.results[].text — page content
data.results[].url — page URL
data.results[].title — page title
```

Job listings: `__dl_full_result__` column containing crustdata response.
```
data.listings[].title — job title (NOT "job_title")
data.listings[].description — job description (NOT "job_description")
data.listings[].category — job category
data.listings[].url — listing URL
```

## Credit Estimation

| Step | Credits per row | Total (60 companies) |
|------|----------------|---------------------|
| exa_search with contents | ~5 | ~300 |
| crustdata_job_listings | ~1 | ~60 |
| **Total** | **~6** | **~360** |

Always get user approval before running paid enrichment steps.

## Common Pitfalls

1. **Skipping target discovery (Step 0)** — Without understanding what the target sells, you'll generate generic/irrelevant configs
2. **Homepage-only scraping**: Always use multi-page discovery. Homepage alone misses pricing, integrations, security.
3. **Using hardcoded examples** — Don't copy sales-focused keywords for a creative-ops tool. Generate configs per vertical.
4. **Generic tech stack**: Search for niche SaaS tools specific to buyer persona, not generic ones (AWS, Slack).
5. **Ignoring source context**: "prospect" on a product page = seller signal. "prospect" in a job listing = buyer signal.
6. **Missing lost data**: Verify lost companies have content before analysis. Empty lost = meaningless lift scores.
7. **Substring false positives**: "sequenc" matches "consequences". Spot-check high-lift keywords for false matches.
8. **Skipping config review (Step 3.5)** — Always validate generated configs against enriched data before analysis.

## References

- **[keyword-catalog.md](references/keyword-catalog.md)**: Read when generating configs (Step 1.5). Contains JSON format, generation patterns, and multi-vertical examples.
- **[report-template.md](references/report-template.md)**: Read when generating the report (Step 5). Full section structure, table formats, inline example format, quality rules.
- **[signal-interpretation.md](references/signal-interpretation.md)**: Read when writing interpretation columns or reviewing signal quality. Buyer vs seller vs competitor rules.
- **[scripts/analyze_signals.py](scripts/analyze_signals.py)**: Deterministic analysis script. Run in Step 4. Auto-detects columns, accepts custom keywords/tools via JSON.
