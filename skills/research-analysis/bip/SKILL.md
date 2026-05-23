---
name: bip
description: Unified guidance for using the bipartite reference library CLI. Use when searching for papers, managing the library, or exploring literature via S2/ASTA.
---

# Bip Reference Library

A CLI tool for managing academic references with local storage and external paper search.

**Repository**: Configured via `nexus_path` in `~/.config/bip/config.json`

## ⚠️ CRITICAL: Local-First Search Policy

**ALWAYS search locally before using external APIs. NEVER call ASTA without explicit user permission.**

The nexus library has ~6000 papers. Most relevant papers are already there.

### Required Search Order

1. **Local search FIRST** (always do this):
   ```bash
   bip search "author keyword"
   ```

2. **If `bip search` fails** (e.g., schema error), rebuild the database:
   ```bash
   bip rebuild --force
   ```
   Then retry the search.

3. **Only if not found locally AND user confirms**, use ASTA:
   ```
   "I couldn't find that paper in the local library. Would you like me to search Semantic Scholar (ASTA)?"
   ```

**DO NOT** call `bip asta`, `mcp__asta__*`, or any external API without asking first.

## Argument Handling

When invoked with arguments like `/bip find <query>` or `/bip <query>`:

1. **Always search local library first** with `bip search "<query>"`
2. If local search fails with an error, rebuild the database and retry
3. **Only after exhausting local options**, ask user if they want to search externally
4. For title searches, use the full title; for topic searches, use key terms

## Proactive Concept Discovery

When discussing papers, **always look for opportunities to create concept nodes**:

- Papers that **introduce** new methods, models, or techniques (e.g., "categorical Jacobian")
- Papers that **apply** existing concepts in novel ways
- Connections between papers through shared concepts

Suggest creating concepts when you notice:
- A named method or algorithm being introduced
- A technique being reused across multiple papers
- A bridge between the user's work and external literature

## Quick Reference

| Task | Command |
|------|---------|
| Search local library | `bip search "query"` |
| Search by author | `bip search -a "LastName"` (exact last name, AND logic) |
| Search by title | `bip search -t "keywords"` or `--title` |
| Search by year | `bip search --year 2024` or `--year 2020:` |
| Search by venue | `bip search --venue "Nature"` (partial match) |
| Lookup by DOI | `bip search --doi "10.1234/..."` |
| Combined search | `bip search "topic" -a "Author" --year 2020:` |
| Semantic search | `bip semantic "query"` |
| Get paper details | `bip get <id>` |
| Add paper to collection | `bip s2 add DOI:10.1234/...` |
| Find literature gaps | `bip s2 gaps` |
| Fast paper search (external) | `bip asta search "query"` |
| Find text snippets | `bip asta snippet "query"` |
| Create concept | `bip concept add <id> --name "Name"` |
| Link paper to concept | `bip edge add -s <paper> -t concept:<concept> -r <type> -m "summary"` |
| Papers for concept | `bip concept papers <concept-id>` |
| Concepts for paper | `bip paper concepts <paper-id>` |
| Import projects from config | `bip project import <file>` |
| Import with concept edges | `bip project import <file> --link-concepts` |

## Search Strategy

### Field-Specific Search Flags

Use `--author` and `--year` flags for precise filtering:

```bash
# Search by author (exact last name matching to avoid false positives)
bip search --author "Yu" --author "Bloom"    # Last names only
bip search -a "Tim Yu" -a "Bloom"            # First + last name
bip search -a "Yu, Timothy"                  # Last, First format

# Filter by year
bip search --year 2024           # exact year
bip search --year 2020:2024      # range (inclusive)
bip search --year 2022:          # 2022 and later
bip search --year :2020          # 2020 and earlier

# Combine keyword + filters
bip search "deep mutational scanning" --author "Bloom" --year 2023:
```

**Multiple authors use AND logic** - all must appear in the paper.

**Author matching rules:**
- Single word (e.g., `-a "Yu"`) → exact last name match (won't match "Yujia")
- Two+ words (e.g., `-a "Tim Yu"`) → exact last name + first name prefix
- Comma format (e.g., `-a "Yu, Tim"`) → same as above

### Query Formulation Tips

**Keep queries short and specific** - Long conceptual queries perform poorly:
- Bad: `"correlation between BME criterion and Felsenstein likelihood around correct tree"`
- Good: `"BME Felsenstein likelihood phylogeny"` or `"Bruno WEIGHBOR likelihood"`

**Use --author flag instead of embedding names in query** - Precise last name matching:
- Good: `bip search -a "Yu" -a "Bloom" --year 2022:` (exact last name match)
- Good: `bip search -a "Tim Yu" -a "Bloom"` (first prefix + exact last name)
- Bad: `bip search "Tim Yu Bloom"` (keyword search is substring-based)

**Use specific method/algorithm names**:
- `"WEIGHBOR"`, `"FASTME"`, `"neighbor joining"` rather than general descriptions

### Systematic Search Workflow

For finding a specific paper or result:

1. **Local library first** (fastest, already curated):
   ```bash
   # Use flags for author/year filtering (most reliable)
   bip search -a "AuthorName" --year 2020:
   bip search "topic" -a "Author"

   # Or plain keyword search
   bip search "author topic"
   bip semantic "conceptual description"  # for topic-heavy queries
   ```

2. **External keyword search** with author names:
   ```bash
   bip asta search "AuthorName keyword1 keyword2" --limit 20 --human
   ```

3. **Broaden if needed** - remove author, try synonyms:
   ```bash
   bip asta search "minimum evolution likelihood" --human
   bip asta search "distance method maximum likelihood phylogeny" --human
   ```

4. **Citation tracing** - if you find a related paper, check what cites it:
   ```bash
   bip asta citations DOI:10.xxxx/yyyy --limit 50 --human
   ```

5. **MCP tools directly** - for more control over fields and filters:
   ```
   mcp__asta__search_papers_by_relevance with specific date ranges
   mcp__asta__get_citations with publication_date_range filter
   ```

### Snippet Search Caveats

The `bip asta snippet` command can be **slow and unreliable** (timeouts are common). Alternatives:
- Use keyword search first to find candidate papers
- Use MCP `mcp__asta__snippet_search` directly with smaller limits
- If snippet times out, fall back to `bip asta search`

## S2 vs ASTA: When to Use Which

Both access Semantic Scholar's paper database but through different APIs:

| Use Case | Command | Why |
|----------|---------|-----|
| Add paper to collection | `bip s2 add` | Only S2 can modify local library |
| Find literature gaps | `bip s2 gaps` | Analyzes your collection |
| Explore without adding | `bip asta *` | Faster, read-only |
| Find text snippets in papers | `bip asta snippet` | Unique to ASTA |
| Fast paper search | `bip asta search` | 10x faster rate limit |
| Get citations/references | Either works | ASTA is faster |

**Rule of thumb**: Use `bip asta` for exploration, `bip s2` when you want to modify your library.

See [api-guide.md](api-guide.md) for detailed comparison.

## Common Workflows

### Find a Paper

1. **Search local library first**:
   ```bash
   bip search "Schmidler phylogenetics"
   # or for topic-heavy queries:
   bip semantic "importance sampling MCMC"
   ```

2. **Get PDF path** for a result:
   ```bash
   bip get <id>
   # pdf_path field + "/Users/matsen/Google Drive/My Drive/Paperpile"
   ```

3. **If not in library**, search externally:
   ```bash
   bip asta search "phylogenetic inference"
   ```

### Update Library from Paperpile

1. Export from Paperpile (JSON format) to ~/Downloads
2. Find the export file:
   ```bash
   ls -t ~/Downloads/Paperpile*.json | head -1
   ```
3. Import:
   ```bash
   bip import --format paperpile "<path>"
   ```
4. Optionally delete the export file after confirming success

### Explore Literature

1. **Search by topic**:
   ```bash
   bip asta search "variational inference phylogenetics" --limit 20
   ```

2. **Find specific text passages**:
   ```bash
   bip asta snippet "Bayesian phylogenetic inference"
   ```

3. **Trace citations**:
   ```bash
   bip asta citations DOI:10.1093/sysbio/syy032
   bip asta references DOI:10.1093/sysbio/syy032
   ```

4. **Add interesting papers** to your collection:
   ```bash
   bip s2 add DOI:10.1093/sysbio/syy032
   ```

See [workflows.md](workflows.md) for detailed workflow instructions.

## Output Format

All commands output JSON by default. Add `--human` for readable format:

```bash
bip asta search "phylogenetics" --human
bip s2 lookup DOI:10.1234/example --human
```

## Paper ID Formats

Both S2 and ASTA accept these identifier formats:
- `DOI:10.1093/sysbio/syy032`
- `ARXIV:2106.15928`
- `PMID:19872477`
- `CorpusId:215416146`
- Raw Semantic Scholar ID (40-char hex)

## Concept Nodes (Knowledge Graph)

Build a knowledge graph by creating concepts and linking papers to them.

### Create Concepts

```bash
# Add a concept with name, aliases, and description
bip concept add somatic-hypermutation \
  --name "Somatic Hypermutation" \
  --aliases "SHM,shm" \
  --description "Process by which B cells diversify antibody genes"

# List all concepts
bip concept list --human

# Get a specific concept
bip concept get somatic-hypermutation --human
```

### Link Papers to Concepts

```bash
# Use flags: -s (source paper), -t (target concept with concept: prefix), -r (relationship type), -m (summary)
bip edge add -s Halpern1998-yc -t concept:mutation-selection-model -r introduces \
  -m "Foundational paper defining the mutation-selection model"

bip edge add -s Yaari2013-dg -t concept:somatic-hypermutation -r models \
  -m "Introduces S5F model for SHM targeting"
```

**Note**: Use `concept:` prefix for concept targets, `project:` for project targets.

### Standard Relationship Types

| Type | When to Use |
|------|-------------|
| `introduces` | Paper first presents or defines this concept |
| `applies` | Paper uses concept as a tool or method |
| `models` | Paper creates computational/mathematical model |
| `evaluates-with` | Paper uses concept for evaluation/benchmarking |
| `critiques` | Paper identifies limitations or problems |
| `extends` | Paper builds upon or extends the concept |

### Query the Knowledge Graph

```bash
# Find all papers linked to a concept
bip concept papers somatic-hypermutation --human

# Filter by relationship type
bip concept papers somatic-hypermutation --type introduces

# Find what concepts a paper relates to
bip paper concepts Halpern1998-yc --human
```

### Manage Concepts

```bash
# Update a concept
bip concept update somatic-hypermutation --description "Updated description"

# Delete a concept (warns if papers linked)
bip concept delete unused-concept

# Force delete (removes linked edges too)
bip concept delete old-concept --force

# Merge duplicate concepts
bip concept merge shm somatic-hypermutation --human
```

## Troubleshooting

### Snippet Search Timeouts

`bip asta snippet` frequently times out with "context deadline exceeded". Workarounds:

1. **Reduce limit**: `--limit 5` instead of default
2. **Use MCP directly**: `mcp__asta__snippet_search` with small limit
3. **Fall back to keyword search**: `bip asta search` is more reliable
4. **Retry once** - sometimes it's transient

### No Results Found

If searches return nothing relevant:

1. **Check spelling** of author names and technical terms
2. **Simplify query** - fewer terms, more common synonyms
3. **Try both local and external**:
   ```bash
   bip search "topic"        # local
   bip semantic "topic"      # local semantic
   bip asta search "topic"   # external
   ```
4. **Check date filters** - paper may be too old/new for range

### Paper Not Found by ID

If `bip get <id>` or `bip asta paper <id>` fails:

1. **Verify ID format**: `DOI:10.xxxx/yyyy` (include prefix)
2. **Try alternate IDs**: Same paper may have DOI, PMID, arXiv ID
3. **Search by title instead**: `bip asta search "exact paper title"`

### SQL Schema Errors

If you see errors like `no such column: pmid` or similar schema mismatches:

```bash
bip rebuild --force
```

The SQLite database is ephemeral and rebuilt from the JSONL source of truth. Schema changes require deleting and rebuilding.

### Slow Performance

- `bip s2` commands are rate-limited to 1 req/sec
- Use `bip asta` for bulk exploration (10 req/sec)
- Run searches in parallel when independent
