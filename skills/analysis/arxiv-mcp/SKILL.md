---
name: arxiv-mcp
description: Search and retrieve academic papers from arXiv.org using WebFetch and Exa. No MCP server required - uses existing tools to access arXiv API directly.
version: 2.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [WebFetch, mcp__Exa__web_search_exa]

# No MCP server required - uses WebFetch + Exa
requires_mcp_server: false
mcp_server_status: not_required

best_practices:
  - Use specific search queries for better results
  - Combine author and keyword searches when appropriate
  - Use Exa for semantic search, WebFetch for specific paper IDs
  - Check multiple related papers for comprehensive research
error_handling: graceful
streaming: supported
---

# arXiv Search Skill

<identity>
arXiv Search Skill - Search and retrieve academic papers from arXiv.org using existing tools (WebFetch, Exa). No MCP server installation required.
</identity>

## ✅ No Installation Required

This skill uses **existing tools** to access arXiv:

- **WebFetch** - Direct access to arXiv API
- **Exa** - Semantic search with arXiv filtering

Works immediately - no MCP server, no restart needed.

<capabilities>
- Search academic papers by keywords, authors, categories, or date ranges
- Retrieve detailed paper metadata (title, authors, abstract, categories, PDF link)
- Get specific papers by arXiv ID
- Find related papers based on categories and keywords
- Filter by arXiv categories (cs.AI, cs.LG, cs.CV, math.*, physics.*, etc.)
- No API key required - uses public arXiv API
</capabilities>

<instructions>
<execution_process>

## Method 1: WebFetch with arXiv API (Recommended for specific queries)

The arXiv API is publicly accessible at `http://export.arxiv.org/api/query`.

### Search by Keywords

```javascript
WebFetch({
  url: 'http://export.arxiv.org/api/query?search_query=all:transformer+attention&max_results=10&sortBy=relevance',
  prompt: 'Extract paper titles, authors, abstracts, arXiv IDs, and PDF links from these results',
});
```

### Search by Author

```javascript
WebFetch({
  url: 'http://export.arxiv.org/api/query?search_query=au:LeCun&max_results=10&sortBy=submittedDate',
  prompt: 'Extract paper titles, authors, abstracts, and arXiv IDs',
});
```

### Search by Category

```javascript
WebFetch({
  url: 'http://export.arxiv.org/api/query?search_query=cat:cs.LG&max_results=15&sortBy=submittedDate',
  prompt: 'Extract paper titles, authors, abstracts, categories, and arXiv IDs',
});
```

### Get Specific Paper by ID

```javascript
WebFetch({
  url: 'http://export.arxiv.org/api/query?id_list=2301.07041',
  prompt:
    'Extract full details: title, all authors, abstract, categories, published date, PDF link',
});
```

### API Query Parameters

| Parameter      | Description                                                 | Example                                       |
| -------------- | ----------------------------------------------------------- | --------------------------------------------- |
| `search_query` | Search terms with field prefixes                            | `all:transformer`, `au:LeCun`, `ti:attention` |
| `id_list`      | Comma-separated arXiv IDs                                   | `2301.07041,2302.13971`                       |
| `max_results`  | Number of results (default 10, max 100)                     | `max_results=20`                              |
| `start`        | Offset for pagination                                       | `start=10`                                    |
| `sortBy`       | Sort order: `relevance`, `lastUpdatedDate`, `submittedDate` | `sortBy=submittedDate`                        |
| `sortOrder`    | `ascending` or `descending`                                 | `sortOrder=descending`                        |

### Field Prefixes for search_query

| Prefix | Field      | Example                   |
| ------ | ---------- | ------------------------- |
| `all:` | All fields | `all:machine+learning`    |
| `ti:`  | Title      | `ti:transformer`          |
| `au:`  | Author     | `au:Vaswani`              |
| `abs:` | Abstract   | `abs:attention+mechanism` |
| `cat:` | Category   | `cat:cs.LG`               |
| `co:`  | Comment    | `co:accepted`             |

### Boolean Operators

Combine terms with `AND`, `OR`, `ANDNOT`:

```
search_query=ti:transformer+AND+abs:attention
search_query=au:LeCun+OR+au:Bengio
search_query=cat:cs.LG+ANDNOT+ti:survey
```

---

## Method 2: Exa Search (Better for semantic/natural language queries)

Use Exa for more natural language queries with arXiv filtering:

### Semantic Search

```javascript
mcp__Exa__web_search_exa({
  query: 'site:arxiv.org transformer architecture attention mechanism deep learning',
  numResults: 10,
});
```

### Recent Papers in a Field

```javascript
mcp__Exa__web_search_exa({
  query: 'site:arxiv.org large language model scaling laws 2024',
  numResults: 15,
});
```

### Author-Focused Search

```javascript
mcp__Exa__web_search_exa({
  query: 'site:arxiv.org author:"Yann LeCun" deep learning',
  numResults: 10,
});
```

---

## Common arXiv Categories

| Category   | Field                           |
| ---------- | ------------------------------- |
| cs.AI      | Artificial Intelligence         |
| cs.LG      | Machine Learning                |
| cs.CL      | Computation and Language (NLP)  |
| cs.CV      | Computer Vision                 |
| cs.SE      | Software Engineering            |
| cs.CR      | Cryptography and Security       |
| stat.ML    | Machine Learning (Statistics)   |
| math.\*    | Mathematics (all subcategories) |
| physics.\* | Physics (all subcategories)     |
| q-bio.\*   | Quantitative Biology            |
| econ.\*    | Economics                       |

---

## Workflow: Complete Research Process

### Step 1: Initial Search

```javascript
// Start with broad Exa search for semantic matching
mcp__Exa__web_search_exa({
  query: 'site:arxiv.org transformer attention mechanism neural networks',
  numResults: 10,
});
```

### Step 2: Get Specific Papers

```javascript
// Get details for interesting papers by ID
WebFetch({
  url: 'http://export.arxiv.org/api/query?id_list=2301.07041,2302.13971',
  prompt: 'Extract full metadata for each paper: title, authors, abstract, categories, PDF URL',
});
```

### Step 3: Find Related Work

```javascript
// Search by category of interesting paper
WebFetch({
  url: 'http://export.arxiv.org/api/query?search_query=cat:cs.LG+AND+ti:attention&max_results=10&sortBy=submittedDate',
  prompt: 'Find related papers, extract titles and abstracts',
});
```

### Step 4: Get Recent Papers

```javascript
// Latest papers in the field
WebFetch({
  url: 'http://export.arxiv.org/api/query?search_query=cat:cs.LG&max_results=20&sortBy=submittedDate&sortOrder=descending',
  prompt: 'Extract the 20 most recent machine learning papers',
});
```

</execution_process>

<best_practices>

1. **Use Exa for discovery**: Natural language queries find semantically related papers
2. **Use WebFetch for precision**: Specific IDs, categories, or API queries
3. **Combine approaches**: Exa to discover, WebFetch to deep-dive
4. **Use specific queries**: "transformer attention mechanism" > "machine learning"
5. **Check multiple categories**: Papers often span cs.AI + cs.LG + cs.CL
6. **Sort by date for recent work**: `sortBy=submittedDate&sortOrder=descending`

</best_practices>
</instructions>

<examples>
<usage_example>
**Example 1: Search for transformer papers**:

```javascript
WebFetch({
  url: 'http://export.arxiv.org/api/query?search_query=ti:transformer+AND+abs:attention&max_results=10&sortBy=relevance',
  prompt: 'Extract paper titles, authors, abstracts, and arXiv IDs',
});
```

**Example 2: Find papers by researcher**:

```javascript
WebFetch({
  url: 'http://export.arxiv.org/api/query?search_query=au:Vaswani&max_results=15',
  prompt: 'List all papers by this author with titles and dates',
});
```

**Example 3: Get recent ML papers**:

```javascript
WebFetch({
  url: 'http://export.arxiv.org/api/query?search_query=cat:cs.LG&max_results=20&sortBy=submittedDate&sortOrder=descending',
  prompt: 'Extract the 20 most recent machine learning papers with titles and abstracts',
});
```

**Example 4: Semantic search with Exa**:

```javascript
mcp__Exa__web_search_exa({
  query: 'site:arxiv.org multimodal large language models vision 2024',
  numResults: 10,
});
```

**Example 5: Get specific paper details**:

```javascript
WebFetch({
  url: 'http://export.arxiv.org/api/query?id_list=1706.03762',
  prompt: "Extract complete details for the 'Attention Is All You Need' paper",
});
```

</usage_example>
</examples>

## Agent Integration

This skill is automatically assigned to:

- **researcher** - Academic research, literature review
- **scientific-research-expert** - Deep scientific analysis
- **developer** - Finding technical papers for implementation

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
