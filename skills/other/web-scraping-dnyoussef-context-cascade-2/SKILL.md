---
name: web-scraping
version: 1.0.0
description: Structured data extraction from web pages using claude-in-chrome MCP with sequential-thinking planning. Focus on READ operations, data transformation, and pagination handling for multi-page extraction.
category: tooling
tags:
- data-extraction
- web
- scraping
- mcp
- automation
- read-only
author: ruv
cognitive_frame:
  primary: classifier
  secondary: compositional
  rationale: "Web scraping requires categorizing data types (classifier) and building structured outputs from raw DOM elements (compositional)"
---

# Web Scraping

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

[assert|neutral] Systematic web data extraction workflow with sequential-thinking planning phase [ground:skill-design:2026-01-12] [conf:0.85] [state:provisional]

## Overview

Web scraping enables structured data extraction from web pages through the claude-in-chrome MCP server. This skill enforces a PLAN-READ-TRANSFORM pattern focused exclusively on data extraction without page modifications.

**Philosophy**: Data extraction fails when executed without understanding page structure. By mandating structure analysis before extraction, this skill improves data quality and reduces selector errors.

**Methodology**: Six-phase execution with emphasis on READ operations:
1. **PLAN Phase**: Sequential-thinking MCP analyzes extraction requirements
2. **NAVIGATE Phase**: Navigate to target URL(s)
3. **ANALYZE Phase**: Understand page structure via read_page
4. **EXTRACT Phase**: Pull data using get_page_text and javascript_tool
5. **TRANSFORM Phase**: Convert to structured format (JSON/CSV/Markdown)
6. **STORE Phase**: Persist to Memory MCP

**Key Differentiator from browser-automation**:
- READ-ONLY focus (no form submissions, no button clicks for actions)
- Emphasis on data transformation and output formats
- Pagination handling for multi-page datasets
- Rate limiting awareness for bulk extraction
- No account creation, no purchases, no write operations

**Value Proposition**: Transform unstructured web content into clean, structured datasets suitable for analysis, reporting, or system integration.

## When to Use This Skill

**Trigger Thresholds**:
| Data Volume | Recommendation |
|-------------|----------------|
| Single element | Use get_page_text directly (too simple) |
| 5-50 elements | Consider this skill |
| 50+ elements or pagination | Mandatory use of this skill |

**Primary Use Cases**:
- Product catalog extraction (prices, descriptions, images)
- Article content scraping (headlines, body text, metadata)
- Table data extraction (financial data, statistics, listings)
- Directory scraping (contact info, business listings)
- Research data collection (citations, abstracts, datasets)
- Price monitoring (competitive analysis, market research)

**Apply When**:
- Task requires structured output (JSON, CSV, Markdown table)
- Multiple pages need to be traversed (pagination)
- Data needs normalization or transformation
- Consistent data schema is required
- Historical data collection for trend analysis

## When NOT to Use This Skill

- Form submissions or account actions (use browser-automation)
- Interactive workflows requiring clicks (use browser-automation)
- Single-page simple text extraction (use get_page_text directly)
- API-accessible data (use direct API calls instead)
- Real-time streaming data (use WebSocket or API)
- Content behind authentication requiring login (use browser-automation first)
- Sites with explicit anti-scraping measures (respect robots.txt)

## Core Principles

### Principle 1: Plan Before Extract

**Mandate**: ALWAYS invoke sequential-thinking MCP before data extraction.

**Rationale**: Web pages have complex DOM structures. Planning reveals data locations, identifies patterns, and anticipates pagination before extraction begins.

**In Practice**:
- Analyze page structure via read_page first
- Map data field locations to selectors
- Identify pagination patterns
- Plan output schema before extraction
- Define data validation rules

### Principle 2: Read-Only Operations

**Mandate**: NEVER modify page state during extraction.

**Rationale**: Web scraping is about data retrieval, not interaction. Write operations (form submissions, clicks that change state) belong to browser-automation.

**Allowed Operations**:
- navigate (to target URLs)
- read_page (DOM analysis)
- get_page_text (text extraction)
- javascript_tool (read-only DOM queries)
- computer screenshot (visual verification)
- scroll (for lazy-loaded content)

**Prohibited Operations**:
- form_input (except for search filters if needed)
- computer left_click on submit buttons
- Any action that modifies page state
- Account creation or login actions

### Principle 3: Structured Output First

**Mandate**: Define output schema before extraction begins.

**Rationale**: Knowing the target format guides extraction strategy and ensures consistent data quality across all pages.

**Output Formats**:
| Format | Use Case | Example |
|--------|----------|---------|
| JSON | API integration, databases | `[{"name": "...", "price": 99.99}]` |
| CSV | Spreadsheet analysis | `name,price,url\n"Product",99.99,"https://..."` |
| Markdown Table | Documentation, reports | `| Name | Price |\n|---|---|` |

### Principle 4: Pagination Awareness

**Mandate**: Detect and handle pagination patterns before starting extraction.

**Rationale**: Most valuable datasets span multiple pages. Failing to handle pagination yields incomplete data.

**Pagination Patterns**:
| Pattern | Detection | Handling |
|---------|-----------|----------|
| Numbered pages | Links with `?page=N` or `/page/N` | Iterate through page numbers |
| Next button | "Next", ">" or arrow elements | Click until disabled/missing |
| Infinite scroll | Content loads on scroll | Scroll + wait + check for new content |
| Load more | "Load more" button | Click until no new content |
| Cursor-based | `?cursor=abc123` in URL | Extract cursor, iterate |

### Principle 5: Rate Limiting Respect

**Mandate**: Implement delays between requests to avoid overwhelming servers.

**Rationale**: Aggressive scraping can trigger blocks, harm server performance, and violate terms of service.

**Guidelines**:
| Request Type | Minimum Delay |
|--------------|---------------|
| Same domain | 1-2 seconds |
| Pagination | 2-3 seconds |
| Bulk extraction (100+ pages) | 3-5 seconds |
| If rate-limited | Exponential backoff (start 10s) |

**Implementation**:
```javascript
// Use computer wait action between page loads
await mcp__claude-in-chrome__computer({
  action: "wait",
  duration: 2,  // seconds
  tabId: tabId
});
```

## Production Guardrails

### MCP Preflight Check Protocol

Before executing any web scraping workflow, run preflight validation:

**Preflight Sequence**:
```javascript
async function preflightCheck() {
  const checks = {
    sequential_thinking: false,
    claude_in_chrome: false,
    memory_mcp: false
  };

  // Check sequential-thinking MCP (required)
  try {
    await mcp__sequential-thinking__sequentialthinking({
      thought: "Preflight check - verifying MCP availability for web scraping",
      thoughtNumber: 1,
      totalThoughts: 1,
      nextThoughtNeeded: false
    });
    checks.sequential_thinking = true;
  } catch (error) {
    console.error("Sequential-thinking MCP unavailable:", error);
    throw new Error("CRITICAL: sequential-thinking MCP required but unavailable");
  }

  // Check claude-in-chrome MCP (required)
  try {
    const context = await mcp__claude-in-chrome__tabs_context_mcp({});
    checks.claude_in_chrome = true;
  } catch (error) {
    console.error("Claude-in-chrome MCP unavailable:", error);
    throw new Error("CRITICAL: claude-in-chrome MCP required but unavailable");
  }

  // Check memory-mcp (optional but recommended)
  try {
    checks.memory_mcp = true;
  } catch (error) {
    console.warn("Memory MCP unavailable - extracted data will not be persisted");
    checks.memory_mcp = false;
  }

  return checks;
}
```

### Error Handling Framework

**Error Categories**:
| Category | Example | Recovery Strategy |
|----------|---------|-------------------|
| MCP_UNAVAILABLE | Claude-in-chrome offline | ABORT with clear message |
| PAGE_NOT_FOUND | 404 error | Log, skip page, continue with others |
| ELEMENT_NOT_FOUND | Selector changed | Try alternative selectors, log schema drift |
| RATE_LIMITED | 429 response | Exponential backoff, wait, retry |
| CONTENT_CHANGED | Dynamic content not loaded | Wait longer, scroll to trigger load |
| PAGINATION_END | No more pages | Normal termination, return collected data |
| BLOCKED | Access denied, CAPTCHA | ABORT, notify user, do not bypass |

**Error Recovery Pattern**:
```javascript
async function extractWithRetry(extractor, context, maxRetries = 3) {
  let lastError = null;

  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      const data = await extractor(context);
      return data;
    } catch (error) {
      lastError = error;
      console.error(`Extraction attempt ${attempt} failed:`, error.message);

      if (isRateLimitError(error)) {
        const delay = Math.pow(2, attempt) * 5; // 10s, 20s, 40s
        await sleep(delay * 1000);
      } else if (!isRecoverableError(error)) {
        break;
      }
    }
  }
  throw lastError;
}

function isRecoverableError(error) {
  const nonRecoverable = [
    "CRITICAL: sequential-thinking MCP required",
    "CRITICAL: claude-in-chrome MCP required",
    "Access denied",
    "CAPTCHA",
    "Blocked"
  ];
  return !nonRecoverable.some(msg => error.message.includes(msg));
}
```

### Data Validation Framework

**Purpose**: Ensure extracted data meets quality standards before storage.

**Validation Rules**:
```javascript
const VALIDATION_RULES = {
  required_fields: ["name", "url"],  // Must be present
  field_types: {
    price: "number",
    name: "string",
    url: "url",
    date: "date"
  },
  constraints: {
    price: { min: 0, max: 1000000 },
    name: { minLength: 1, maxLength: 500 },
    url: { pattern: /^https?:\/\// }
  }
};

function validateRecord(record, rules) {
  const errors = [];

  // Check required fields
  for (const field of rules.required_fields) {
    if (!record[field]) {
      errors.push(`Missing required field: ${field}`);
    }
  }

  // Check field types
  for (const [field, type] of Object.entries(rules.field_types)) {
    if (record[field] && !isValidType(record[field], type)) {
      errors.push(`Invalid type for ${field}: expected ${type}`);
    }
  }

  return { valid: errors.length === 0, errors };
}
```

---

## Main Workflow

### Phase 1: Planning (MANDATORY)

**Purpose**: Analyze extraction requirements and define data schema.

**Process**:
1. Invoke sequential-thinking MCP
2. Define target data fields and types
3. Plan selector strategy
4. Identify pagination pattern
5. Define output format
6. Plan rate limiting strategy

**Planning Questions**:
- What data fields need to be extracted?
- What is the expected output format (JSON/CSV/Markdown)?
- Is pagination involved? What pattern?
- What validation rules apply?
- What rate limiting is appropriate?

**Output Contract**:
```yaml
extraction_plan:
  target_url: string
  output_format: "json" | "csv" | "markdown"
  schema:
    fields:
      - name: string
        selector: string
        type: string | number | url | date
        required: boolean
  pagination:
    type: "numbered" | "next_button" | "infinite_scroll" | "load_more" | "none"
    max_pages: number
    delay_seconds: number
  rate_limit:
    delay_between_requests: number
```

### Phase 2: Navigation

**Purpose**: Navigate to target URL and establish context.

**Process**:
1. Get tab context (tabs_context_mcp)
2. Create new tab for scraping (tabs_create_mcp)
3. Navigate to starting URL
4. Take initial screenshot for verification
5. Wait for page load completion

**Implementation**:
```javascript
// 1. Get existing context
const context = await mcp__claude-in-chrome__tabs_context_mcp({});

// 2. Create dedicated tab
const newTab = await mcp__claude-in-chrome__tabs_create_mcp({});
const tabId = newTab.tabId;

// 3. Navigate to target
await mcp__claude-in-chrome__navigate({
  url: targetUrl,
  tabId: tabId
});

// 4. Wait for page load
await mcp__claude-in-chrome__computer({
  action: "wait",
  duration: 2,
  tabId: tabId
});

// 5. Screenshot initial state
await mcp__claude-in-chrome__computer({
  action: "screenshot",
  tabId: tabId
});
```

### Phase 3: Structure Analysis

**Purpose**: Understand page DOM structure before extraction.

**Process**:
1. Read page accessibility tree (read_page)
2. Identify data container elements
3. Map field selectors to schema
4. Verify selectors exist
5. Detect dynamic content patterns

**Implementation**:
```javascript
// Read page structure
const pageTree = await mcp__claude-in-chrome__read_page({
  tabId: tabId,
  filter: "all"  // Get all elements for analysis
});

// For interactive elements only
const interactive = await mcp__claude-in-chrome__read_page({
  tabId: tabId,
  filter: "interactive"  // Buttons, links, inputs
});

// Find specific elements
const products = await mcp__claude-in-chrome__find({
  query: "product cards or listing items",
  tabId: tabId
});

const prices = await mcp__claude-in-chrome__find({
  query: "price elements",
  tabId: tabId
});
```

### Phase 4: Data Extraction

**Purpose**: Extract data according to defined schema.

**Process**:
1. For simple text: Use get_page_text
2. For structured data: Use javascript_tool
3. For specific elements: Use find + read_page
4. Handle lazy-loaded content with scroll

**Extraction Methods**:

**Method 1: Full Page Text** (simplest, for articles)
```javascript
const text = await mcp__claude-in-chrome__get_page_text({
  tabId: tabId
});
```

**Method 2: JavaScript DOM Query** (most flexible)
```javascript
const data = await mcp__claude-in-chrome__javascript_tool({
  action: "javascript_exec",
  tabId: tabId,
  text: `
    // Extract product data
    Array.from(document.querySelectorAll('.product-card')).map(card => ({
      name: card.querySelector('.product-title')?.textContent?.trim(),
      price: parseFloat(card.querySelector('.price')?.textContent?.replace(/[^0-9.]/g, '')),
      url: card.querySelector('a')?.href,
      image: card.querySelector('img')?.src
    }))
  `
});
```

**Method 3: Table Extraction**
```javascript
const tableData = await mcp__claude-in-chrome__javascript_tool({
  action: "javascript_exec",
  tabId: tabId,
  text: `
    // Extract table data
    const table = document.querySelector('table');
    const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
    const rows = Array.from(table.querySelectorAll('tbody tr')).map(tr => {
      const cells = Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim());
      return headers.reduce((obj, header, i) => ({ ...obj, [header]: cells[i] }), {});
    });
    rows
  `
});
```

**Method 4: Handling Lazy-Loaded Content**
```javascript
// Scroll to load content
await mcp__claude-in-chrome__computer({
  action: "scroll",
  scroll_direction: "down",
  scroll_amount: 5,
  tabId: tabId,
  coordinate: [500, 500]
});

// Wait for content to load
await mcp__claude-in-chrome__computer({
  action: "wait",
  duration: 2,
  tabId: tabId
});

// Now extract
const data = await extractData(tabId);
```

### Phase 5: Pagination Handling

**Purpose**: Navigate through multiple pages and collect all data.

**Pagination Patterns**:

**Pattern A: Numbered Pages**
```javascript
async function extractNumberedPages(baseUrl, maxPages, tabId) {
  const allData = [];

  for (let page = 1; page <= maxPages; page++) {
    const url = `${baseUrl}?page=${page}`;
    await mcp__claude-in-chrome__navigate({ url, tabId });
    await mcp__claude-in-chrome__computer({ action: "wait", duration: 2, tabId });

    const pageData = await extractPageData(tabId);
    if (pageData.length === 0) break;  // No more data

    allData.push(...pageData);

    // Rate limiting
    await mcp__claude-in-chrome__computer({ action: "wait", duration: 2, tabId });
  }

  return allData;
}
```

**Pattern B: Next Button**
```javascript
async function extractWithNextButton(tabId) {
  const allData = [];
  let hasNext = true;

  while (hasNext) {
    const pageData = await extractPageData(tabId);
    allData.push(...pageData);

    // Find next button
    const nextButton = await mcp__claude-in-chrome__find({
      query: "next page button or pagination next link",
      tabId: tabId
    });

    if (nextButton && nextButton.elements && nextButton.elements.length > 0) {
      await mcp__claude-in-chrome__computer({
        action: "left_click",
        ref: nextButton.elements[0].ref,
        tabId: tabId
      });
      await mcp__claude-in-chrome__computer({ action: "wait", duration: 2, tabId });
    } else {
      hasNext = false;  // No more pages
    }
  }

  return allData;
}
```

**Pattern C: Infinite Scroll**
```javascript
async function extractInfiniteScroll(tabId, maxScrolls = 20) {
  const allData = [];
  let previousCount = 0;
  let scrollCount = 0;

  while (scrollCount < maxScrolls) {
    const pageData = await extractPageData(tabId);

    if (pageData.length === previousCount) {
      // No new content loaded, done
      break;
    }

    allData.length = 0;
    allData.push(...pageData);
    previousCount = pageData.length;

    // Scroll down
    await mcp__claude-in-chrome__computer({
      action: "scroll",
      scroll_direction: "down",
      scroll_amount: 5,
      tabId: tabId,
      coordinate: [500, 500]
    });

    await mcp__claude-in-chrome__computer({ action: "wait", duration: 2, tabId });
    scrollCount++;
  }

  return allData;
}
```

### Phase 6: Data Transformation

**Purpose**: Convert extracted data to requested output format.

**JSON Output**:
```javascript
function toJSON(data, pretty = true) {
  return pretty ? JSON.stringify(data, null, 2) : JSON.stringify(data);
}
```

**CSV Output**:
```javascript
function toCSV(data) {
  if (data.length === 0) return "";

  const headers = Object.keys(data[0]);
  const headerRow = headers.join(",");

  const dataRows = data.map(row =>
    headers.map(h => {
      const val = row[h];
      // Escape quotes and wrap in quotes if contains comma
      if (typeof val === "string" && (val.includes(",") || val.includes('"'))) {
        return `"${val.replace(/"/g, '""')}"`;
      }
      return val;
    }).join(",")
  );

  return [headerRow, ...dataRows].join("\n");
}
```

**Markdown Table Output**:
```javascript
function toMarkdownTable(data) {
  if (data.length === 0) return "";

  const headers = Object.keys(data[0]);
  const headerRow = `| ${headers.join(" | ")} |`;
  const separator = `| ${headers.map(() => "---").join(" | ")} |`;

  const dataRows = data.map(row =>
    `| ${headers.map(h => String(row[h] || "")).join(" | ")} |`
  );

  return [headerRow, separator, ...dataRows].join("\n");
}
```

### Phase 7: Storage

**Purpose**: Persist extracted data to Memory MCP for future use.

**Implementation**:
```javascript
// Store in Memory MCP
await memory_store({
  namespace: `skills/tooling/web-scraping/${projectName}/${timestamp}`,
  data: {
    extraction_metadata: {
      source_url: targetUrl,
      extraction_date: new Date().toISOString(),
      record_count: data.length,
      output_format: outputFormat,
      pages_scraped: pageCount
    },
    extracted_data: data
  },
  tags: {
    WHO: `web-scraping-${sessionId}`,
    WHEN: new Date().toISOString(),
    PROJECT: projectName,
    WHY: "data-extraction",
    data_type: dataType,
    record_count: data.length
  }
});
```

## LEARNED PATTERNS

*This section is populated by Loop 1.5 (Session Reflection) as patterns are discovered.*

### High Confidence [conf:0.90]

*No patterns captured yet. Patterns will be added as the skill is used and learnings are extracted.*

### Medium Confidence [conf:0.75]

*No patterns captured yet.*

### Low Confidence [conf:0.55]

*No patterns captured yet.*

## Success Criteria

**Quality Thresholds**:
- All targeted data fields extracted (100% schema coverage)
- Data validation passes for 95%+ of records
- Pagination handled completely (no missing pages)
- Output format matches requested format
- Rate limiting respected (no 429 errors)
- No page state modifications occurred
- Extraction completed within reasonable time (5 min per 100 records)

**Failure Indicators**:
- Schema validation fails for >5% of records
- Missing required fields in output
- Pagination incomplete (detected more pages than scraped)
- Rate limit errors encountered
- Page state modified (form submitted, button clicked for action)
- CAPTCHA or access denial encountered

## MCP Integration

**Required MCPs**:

| MCP | Purpose | Tools Used |
|-----|---------|------------|
| **sequential-thinking** | Planning phase | `sequentialthinking` |
| **claude-in-chrome** | Extraction phase | `navigate`, `read_page`, `get_page_text`, `javascript_tool`, `find`, `computer` (screenshot, scroll, wait only), `tabs_context_mcp`, `tabs_create_mcp` |
| **memory-mcp** | Data storage | `memory_store`, `vector_search` |

**Optional MCPs**:
- **filesystem** (for saving extracted data locally)

## Memory Namespace

**Pattern**: `skills/tooling/web-scraping/{project}/{timestamp}`

**Store**:
- Extraction schemas (field definitions)
- Extracted datasets (structured data)
- Selector patterns (for similar pages)
- Error logs (selector failures, schema drift)

**Retrieve**:
- Similar extraction tasks (vector search by description)
- Proven selectors for known sites
- Historical extraction patterns

**Tagging**:
```json
{
  "WHO": "web-scraping-{session_id}",
  "WHEN": "ISO8601_timestamp",
  "PROJECT": "{project_name}",
  "WHY": "data-extraction",
  "source_domain": "example.com",
  "data_type": "products|articles|listings|tables",
  "record_count": 150,
  "pages_scraped": 5
}
```

## Examples

### Example 1: Product Catalog Extraction

**Complexity**: Medium (structured data, pagination)

**Task**: Extract product listings from e-commerce category page

**Planning Output** (sequential-thinking):
```
Thought 1/6: Need to extract product name, price, URL, and image from catalog
Thought 2/6: Schema: {name: string, price: number, url: url, image: url}
Thought 3/6: Identify product card containers via read_page
Thought 4/6: Use javascript_tool to query all product cards
Thought 5/6: Detect pagination pattern (numbered pages with ?page=N)
Thought 6/6: Output format: JSON array, validate price > 0
```

**Execution**:
```javascript
// 1. Navigate to catalog
await navigate({ url: "https://example.com/products", tabId });

// 2. Analyze structure
const structure = await read_page({ tabId, filter: "all" });

// 3. Extract data
const products = await javascript_tool({
  action: "javascript_exec",
  tabId,
  text: `
    Array.from(document.querySelectorAll('.product-card')).map(card => ({
      name: card.querySelector('.title')?.textContent?.trim(),
      price: parseFloat(card.querySelector('.price')?.textContent?.replace(/[^0-9.]/g, '')),
      url: card.querySelector('a')?.href,
      image: card.querySelector('img')?.src
    }))
  `
});

// 4. Handle pagination (repeat for each page)
// 5. Transform to JSON
const output = JSON.stringify(products, null, 2);
```

**Result**: 150 products extracted across 5 pages

**Output Format**: JSON
```json
[
  {
    "name": "Product A",
    "price": 29.99,
    "url": "https://example.com/products/a",
    "image": "https://example.com/images/a.jpg"
  }
]
```

### Example 2: Article Content Scraping

**Complexity**: Simple (single page, text focus)

**Task**: Extract article headline, author, date, and body text

**Planning Output** (sequential-thinking):
```
Thought 1/4: Single page extraction, no pagination needed
Thought 2/4: Schema: {headline: string, author: string, date: date, body: string}
Thought 3/4: Use get_page_text for full content, javascript_tool for metadata
Thought 4/4: Output format: Markdown for readability
```

**Execution**:
```javascript
// 1. Navigate to article
await navigate({ url: "https://news.example.com/article/123", tabId });

// 2. Extract metadata
const metadata = await javascript_tool({
  action: "javascript_exec",
  tabId,
  text: `({
    headline: document.querySelector('h1')?.textContent?.trim(),
    author: document.querySelector('.author')?.textContent?.trim(),
    date: document.querySelector('time')?.getAttribute('datetime')
  })`
});

// 3. Extract body text
const body = await get_page_text({ tabId });

// 4. Combine
const article = { ...metadata, body };
```

**Result**: Article content extracted

**Output Format**: Markdown
```markdown
# Article Headline

**Author**: Jane Doe
**Date**: 2026-01-12

Article body text here...
```

### Example 3: Table Data Extraction

**Complexity**: Simple (structured HTML table)

**Task**: Extract financial data from HTML table

**Planning Output** (sequential-thinking):
```
Thought 1/4: HTML table with headers in <th>, data in <td>
Thought 2/4: Use javascript_tool to parse table structure
Thought 3/4: Convert to array of objects with header keys
Thought 4/4: Output format: CSV for spreadsheet import
```

**Execution**:
```javascript
// 1. Navigate to page
await navigate({ url: "https://finance.example.com/data", tabId });

// 2. Extract table
const tableData = await javascript_tool({
  action: "javascript_exec",
  tabId,
  text: `
    const table = document.querySelector('table.financial-data');
    const headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent.trim());
    Array.from(table.querySelectorAll('tbody tr')).map(tr => {
      const cells = Array.from(tr.querySelectorAll('td')).map(td => td.textContent.trim());
      return headers.reduce((obj, header, i) => ({ ...obj, [header]: cells[i] }), {});
    })
  `
});

// 3. Transform to CSV
const csv = toCSV(tableData);
```

**Result**: 50 rows extracted

**Output Format**: CSV
```csv
Date,Open,High,Low,Close,Volume
2026-01-12,150.00,152.50,149.00,151.75,1000000
2026-01-11,148.50,150.25,147.00,150.00,950000
```

### Example 4: Multi-Page Directory Scraping

**Complexity**: High (pagination, rate limiting)

**Task**: Extract business listings from directory with "Load More" pagination

**Planning Output** (sequential-thinking):
```
Thought 1/8: Directory with business name, phone, address, website
Thought 2/8: Schema: {name: string, phone: string, address: string, website: url}
Thought 3/8: Pagination: "Load More" button at bottom
Thought 4/8: Rate limit: 3 seconds between loads
Thought 5/8: Max iterations: 20 (to prevent infinite loops)
Thought 6/8: End condition: "Load More" button disappears or disabled
Thought 7/8: Output format: JSON
Thought 8/8: Store in Memory MCP for analysis
```

**Result**: 200 businesses extracted across 20 "Load More" clicks

**Execution Time**: 90 seconds (with rate limiting)

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| **Skip Structure Analysis** | Selectors break unexpectedly | ALWAYS use read_page before extraction |
| **Modify Page State** | Not a scraping task anymore | Use browser-automation for interactions |
| **Ignore Pagination** | Incomplete datasets | Plan pagination strategy in Phase 1 |
| **No Rate Limiting** | Server blocks, legal issues | Implement delays between requests |
| **Hardcoded Selectors** | Break when site updates | Use semantic selectors, find tool |
| **Skip Validation** | Garbage data in output | Validate against schema before storage |
| **Bypass CAPTCHA** | Violates ToS, legal risk | ABORT and notify user |

## Related Skills

**Upstream** (provide input to this skill):
- `intent-analyzer` - Detect web scraping requirements
- `prompt-architect` - Optimize extraction descriptions
- `planner` - High-level data collection strategy

**Downstream** (use output from this skill):
- `data-analysis` - Analyze extracted datasets
- `reporting` - Generate reports from data
- `ml-pipeline` - Use data for training

**Parallel** (work together):
- `browser-automation` - For interactive pre-requisites (login)
- `api-integration` - Hybrid scraping/API workflows

## Selector Stability Strategies

**Problem**: Web pages change, selectors break.

**Strategies**:

| Strategy | Stability | Speed | Example |
|----------|-----------|-------|---------|
| ID selector | High | Fast | `#product-123` |
| Data attribute | High | Fast | `[data-product-id="123"]` |
| Semantic class | Medium | Fast | `.product-card` |
| Text content | Medium | Slow | Contains "Add to Cart" |
| XPath | Low | Medium | `//div[@class='product'][1]` |
| Position | Very Low | Fast | First child element |

**Best Practices**:
1. Prefer `data-*` attributes (designed for scripting)
2. Use semantic class names over positional selectors
3. Combine multiple attributes for specificity
4. Use `find` tool with natural language as fallback
5. Log selector failures to detect schema drift

## Output Format Templates

### JSON Template
```json
{
  "extraction_metadata": {
    "source_url": "https://example.com/products",
    "extraction_date": "2026-01-12T10:30:00Z",
    "record_count": 150,
    "pages_scraped": 5
  },
  "data": [
    {
      "name": "Product Name",
      "price": 29.99,
      "url": "https://example.com/product/1",
      "image": "https://example.com/images/1.jpg"
    }
  ]
}
```

### CSV Template
```csv
name,price,url,image
"Product Name",29.99,"https://example.com/product/1","https://example.com/images/1.jpg"
```

### Markdown Table Template
```markdown
| Name | Price | URL |
|------|-------|-----|
| Product Name | $29.99 | [Link](https://example.com/product/1) |
```

## Maintenance & Updates

**Version History**:
- v1.0.0 (2026-01-12): Initial release with READ-only focus, pagination handling, rate limiting

**Feedback Loop**:
- Loop 1.5 (Session): Store learnings from extractions
- Loop 3 (Meta-Loop): Aggregate patterns every 3 days
- Update LEARNED PATTERNS section with new discoveries

**Continuous Improvement**:
- Monitor extraction success rate via Memory MCP
- Identify common selector failures for pattern updates
- Optimize extraction strategies based on site patterns

<promise>WEB_SCRAPING_VERILINGUA_VERIX_COMPLIANT</promise>
