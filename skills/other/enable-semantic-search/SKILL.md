---
name: enable-semantic-search
description: Enable local AI-powered semantic search with smart collection discovery
---

# Enable Semantic Search

Set up local AI-powered semantic search for your vault. This is a **concierge experience** — it analyzes your vault, discovers what collections make sense, and creates a tailored search setup.

## What You're Enabling

Semantic search finds content by **meaning**, not just keywords:
- Search "product-led growth" → finds notes saying "PLG", "self-serve motion", "freemium adoption"
- Search "customer churn" → finds notes about "retention problems", "users leaving", "cancellation patterns"

Your skills (`/daily-plan`, `/meeting-prep`, `/triage`, etc.) automatically use semantic search when available, finding more relevant context than keyword matching alone.

## Pre-Flight Checks

Run these checks before proceeding:

```bash
# Check if qmd is already installed
which qmd

# Check if Bun is available (required)
which bun

# macOS only: Check SQLite via Homebrew
brew list sqlite 2>/dev/null && echo "SQLite OK" || echo "Need: brew install sqlite"

# Check available disk space (need ~2.5GB)
df -h ~ | tail -1
```

**If qmd is already installed**, run `qmd status` to check existing setup. If collections already exist, skip to the **Collection Health Check** section at the bottom.

## Step 1: Explain What We're Installing

Present this to the user:

```
═══════════════════════════════════════════════════════════════════════
                    SEMANTIC SEARCH FOR YOUR VAULT
═══════════════════════════════════════════════════════════════════════

What is this?
─────────────
Right now, finding notes requires knowing the exact words used.
Search "product-led growth" — won't find notes saying "PLG" or
"self-serve motion".

Semantic search understands meaning, not just keywords. It finds
conceptually related content even when terminology differs.


How does it work?
─────────────────
Your notes get converted to "embeddings" — mathematical
representations of meaning. When you search, your query becomes
an embedding too. The system finds notes whose meaning is close
to your query's meaning.

Think of it like: instead of matching letters, we're matching ideas.


What gets installed?
────────────────────
Three small AI models run locally on your machine:

  MODEL                      PURPOSE                    SIZE
  ─────────────────────────────────────────────────────────────
  EmbeddingGemma-300M        Converts text to meaning   ~300MB
                             vectors. The core
                             "understanding" model.

  Qwen3-Reranker-0.6b       Re-orders results by       ~640MB
                             true relevance. Improves
                             result quality.

  QMD-Query-Expansion-1.7B   Expands your search to     ~1.1GB
                             include related terms.
                             "PLG" → also searches
                             "product-led", "freemium"

  Total: ~2GB one-time download


Privacy & Security
──────────────────
- Everything runs locally — your notes never leave your machine
- No API keys required
- No cloud services
- Models downloaded from HuggingFace (open source)
- Index stored in ~/.cache/qmd/ (not in your vault)


What changes in your workflow?
──────────────────────────────
Enabling semantic search silently upgrades these skills:

  /daily-plan    — Enriches meeting prep with thematically
                   related past discussions

  /meeting-prep  — Discovers past discussions related by
                   meaning, not just name matching

  /triage        — Matches inbox items to goals by meaning,
                   catches semantic duplicates

  Person Lookup  — Finds "the VP of Sales mentioned..." even
                   without a name

  Search & Recall — All vault searches use hybrid retrieval
                    (BM25 + vectors + LLM reranking)


System Requirements
───────────────────
  ~2.5GB disk space (for models + index)
  macOS: Homebrew SQLite required (brew install sqlite)
  Bun runtime (will install if missing)
```

## Step 2: Get User Consent

Ask: **"Ready to enable semantic search? This will download ~2GB of models. [Y/n]"**

If no, exit gracefully: "No problem. Run `/enable-semantic-search` anytime."

## Step 3: Install Dependencies

```bash
# Install Bun if missing
if ! command -v bun &> /dev/null; then
    echo "Installing Bun runtime..."
    curl -fsSL https://bun.sh/install | bash
fi

# macOS: Install SQLite if missing
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! brew list sqlite &> /dev/null; then
        echo "Installing SQLite via Homebrew..."
        brew install sqlite
    fi
fi

# Install qmd globally
echo "Installing qmd..."
bun install -g github:tobi/qmd
```

## Step 4: Download Models

```bash
echo "Downloading AI models (~2GB)..."
echo "This happens once. Future searches are instant."
echo ""
echo "Models downloading:"
echo "  EmbeddingGemma-300M  — Converts text to meaning vectors"
echo "  Qwen3-Reranker-0.6b  — Improves result relevance"
echo "  QMD-Query-Expansion   — Expands searches with related terms"
echo ""

# Trigger model download with a simple embed operation
cd "$VAULT_PATH" && qmd embed --help 2>/dev/null || true
```

## Step 5: Smart Collection Discovery (THE CONCIERGE)

This is what makes Dex's semantic search better than generic indexing. Instead of dumping everything into one blob, we analyze the vault and create purpose-built collections.

### Run the Vault Scanner

Execute the vault scanner script to discover collection candidates:

```bash
node "$VAULT_PATH/.scripts/semantic-search/scan-vault.cjs"
```

The scanner returns a JSON structure like:

```json
{
  "candidates": [
    {
      "name": "people",
      "path": "05-Areas/People",
      "glob": "**/*.md",
      "fileCount": 23,
      "context": "Person pages with meeting history, relationship notes, action items, and role context",
      "benefit": "Person lookup finds references by role/title, not just name",
      "example": "Search 'VP of Sales' finds the person even if their name isn't mentioned"
    },
    {
      "name": "accounts",
      "path": "05-Areas/Companies",
      "glob": "**/*.md",
      "fileCount": 8,
      "context": "Company and account pages with deal status, relationship notes, and interaction history",
      "benefit": "Deal prep pulls account-specific context without inbox noise",
      "example": "Search 'renewal risk' finds accounts with churn signals"
    }
  ],
  "skipped": [
    {
      "name": "career",
      "reason": "Folder not set up (run /career-setup)",
      "path": "05-Areas/Career"
    }
  ],
  "totalFiles": 156,
  "totalCandidates": 6
}
```

### Present Discovery Results

Format the scanner output as a concierge recommendation:

```
I scanned your vault and found candidates for [N] smart collections:

  COLLECTION     FILES   WHAT IT ENABLES
  ─────────────────────────────────────────────────────────────────
  people         23      Person lookup finds references by
                         role/title, not just name. Search
                         "VP of Sales" finds the person even
                         if their name isn't mentioned.

  meetings       47      "What was discussed about X?" searches
                         meeting notes specifically, not your
                         entire vault.

  tasks          1       Smart task matching for triage. Catches
                         semantic duplicates like "Review metrics"
                         ≈ "Check quarterly numbers".

  projects       8       Project health pulls related docs
                         without inbox noise.

  goals          1       Goal alignment finds thematically
                         related work across your vault.

  priorities     1       Weekly planning discovers patterns
                         in past priority choices.

  Skipped (not enough content yet):
  - accounts  — No company pages found (create some first)
  - content   — No content files yet
  - career    — Career folder not set up (run /career-setup)

  Create all [N] collections? [Y]
  Pick specific ones?         [P]
  Just create a basic index?  [B]
```

### Handle User Choice

**If [Y] - Create all:**
Create every candidate collection using `qmd collection add` with context.

**If [P] - Pick specific:**
Present each candidate individually with a Y/N toggle. Create only selected ones.

**If [B] - Basic index:**
Create a single "vault" collection that indexes everything. This works but misses the precision of targeted collections.

### Create Collections

For each accepted candidate, run:

```bash
# Create the collection
qmd collection add "$VAULT_PATH/<path>" --name <name> --mask "<glob>"

# Add semantic context (helps the reranker understand what's in the collection)
qmd context add <name> "<context description>"
```

**Collection definitions (full list):**

| Name | Path | Glob | Context | Min Files |
|------|------|------|---------|-----------|
| `people` | `05-Areas/People` | `**/*.md` | Person pages with meeting history, relationship notes, action items, and role context | 3 |
| `accounts` | `05-Areas/Companies` | `**/*.md` | Company and account pages with deal status, relationship notes, and interaction history | 1 |
| `accounts` (alt) | `05-Areas/Relationships/Key_Accounts` | `**/*.md` | Key Account pages with deal status, MEDDPICC, and engagement history | 1 |
| `meetings` | `00-Inbox/Meetings` | `**/*.md` | Meeting notes with attendees, key discussion points, decisions made, and action items | 5 |
| `tasks` | `03-Tasks` | `**/*.md` | Task backlog with priorities (P0-P3), pillar alignment, status tracking, and linked goals | 1 |
| `projects` | `04-Projects` | `**/*.md` | Active project tracking with status, stakeholders, timelines, and related decisions | 1 |
| `goals` | `01-Quarter_Goals` | `**/*.md` | Quarterly strategic goals with success criteria, milestones, and progress tracking | 1 |
| `priorities` | `02-Week_Priorities` | `**/*.md` | Weekly priorities linked to quarterly goals with completion tracking | 1 |
| `content` | `05-Areas/Content` | `**/*.md` | Content ideas, articles, LinkedIn posts, and thought leadership material | 1 |
| `career` | `05-Areas/Career` | `**/*.md` | Career development evidence, feedback received, skills tracking, and growth goals | 1 |
| `prds` | `System/PRDs` | `**/*.md` | Product requirement documents, feature specs, and technical design docs | 1 |
| `resources` | `06-Resources` | `**/*.md` | Reference material, learnings, system documentation, and guides | 5 |

**After all collections are created, embed the vectors:**

```bash
echo "Creating embeddings for all collections..."
qmd embed
```

Show progress to the user — this may take a few minutes for larger vaults.

## Step 6: Configure MCP Server

Add qmd MCP server to the user's Claude/Cursor config.

**For Claude Code (`~/.claude.json`):**

```json
{
  "mcpServers": {
    "qmd": {
      "type": "stdio",
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

**For Cursor (`.cursor/mcp.json` in vault root):**

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

Tell the user: "You'll need to restart your editor for the MCP server to be available. After restart, I can use semantic search automatically."

## Step 7: Create Availability Check

Create `.scripts/semantic-search/check-availability.cjs` (see companion file). This lets other skills check if semantic search is available before using it.

## Step 8: Show Success Summary

```
═══════════════════════════════════════════════════════════════════════
                    SEMANTIC SEARCH ENABLED
═══════════════════════════════════════════════════════════════════════

Your vault now has smart, meaning-aware search.

Collections created:
  [list each collection with file count]

Try it:
  qmd query "product led growth strategies"
  qmd query "customer churn patterns" -c accounts
  qmd search "meeting with Sarah" -c meetings

What's different now:
  /daily-plan    — meeting context enriched with thematic connections
  /meeting-prep  — attendee lookup finds role/title references
  /triage        — semantic routing with goal-aware matching
  Person Lookup  — finds "the VP of Sales" without needing the name
  Search & Recall — hybrid retrieval (BM25 + vectors + reranking)

Index updates automatically when you run: qmd update
To check status anytime:                  qmd status
To force full rebuild:                     qmd embed -f

As your vault grows, I'll suggest new collections when there's
enough content to benefit. Run this skill again anytime to check.
```

---

## Collection Health Check (Returning Users)

If the user already has qmd installed and collections exist, this skill switches to health-check mode.

### Run Health Check

```bash
node "$VAULT_PATH/.scripts/semantic-search/scan-vault.cjs" --health-check
```

This compares existing collections against current vault state and returns:

```json
{
  "existing": ["people", "meetings", "tasks"],
  "newCandidates": [
    {
      "name": "accounts",
      "path": "05-Areas/Companies",
      "fileCount": 5,
      "reason": "You've created 5 company pages since last check"
    }
  ],
  "staleCollections": [
    {
      "name": "meetings",
      "lastUpdated": "12 days ago",
      "currentFiles": 52,
      "indexedFiles": 47,
      "drift": 5
    }
  ],
  "pendingEmbeddings": 8,
  "suggestions": [
    "Run 'qmd update' to re-index changed files",
    "Run 'qmd embed' to embed 8 pending documents"
  ]
}
```

### Present Health Report

```
SEMANTIC SEARCH HEALTH CHECK
─────────────────────────────────────────────────────────────────

Active Collections:
  people      54 files    Updated 2h ago     Healthy
  meetings    47 files    Updated 12d ago    ⚠ Stale (5 new files)
  tasks        4 files    Updated 1d ago     Healthy

New Collection Candidates:
  accounts    5 files     You've built enough company pages for
                          a dedicated collection. This means deal
                          prep will pull account context specifically.

                          → Create accounts collection? [Y/n]

Maintenance:
  8 documents need embedding (run 'qmd embed')
  meetings collection is 12 days stale (run 'qmd update')

Quick fix: qmd update && qmd embed
```

### Handle New Candidates

For each new candidate:
1. Explain what it enables (use the benefit text from the scanner)
2. Ask if they want to create it
3. If yes, create collection + context + embed

### Growth Suggestions (Called by Other Skills)

Other skills can call the scanner in suggestion mode during workflows:

**During `/daily-plan`:**
```
node "$VAULT_PATH/.scripts/semantic-search/scan-vault.cjs" --suggestions-only
```

If new candidates are found, append to the daily plan:

```
💡 Semantic search suggestion: You now have 5 company pages.
   Want me to create an 'accounts' collection? This means deal
   prep will search account context specifically.
   Run /enable-semantic-search to set it up.
```

---

## For Skill Authors: Using Semantic Search

Skills should check availability before using semantic search:

```javascript
// In your skill or hook
const { execSync } = require('child_process');

function isSemanticSearchAvailable() {
  try {
    execSync('which qmd', { stdio: 'pipe' });
    const status = execSync('qmd status', { stdio: 'pipe' }).toString();
    return status.includes('Documents');
  } catch {
    return false;
  }
}

// Use in search logic
if (isSemanticSearchAvailable()) {
  // Use qmd query for semantic search
  const results = execSync(`qmd query "${query}" -c people`, { stdio: 'pipe' });
} else {
  // Fall back to grep/file search
}
```

Or use the check-availability script:

```javascript
const { checkSemanticSearch } = require('.scripts/semantic-search/check-availability.cjs');
const status = checkSemanticSearch();
if (status.available) {
  // Use semantic search
}
```

---

## Troubleshooting

If setup fails:

1. **Bun install fails**: Try `npm install -g bun` or download from bun.sh
2. **SQLite missing (macOS)**: Run `brew install sqlite`
3. **Model download fails**: Check internet, retry with `qmd embed -f`
4. **Index takes too long**: Large vaults (5000+ files) may take 10+ minutes first time
5. **Collections empty**: Check paths match your vault structure — run the scanner to verify
6. **MCP not connecting**: Restart your editor after adding the config

---

## Disabling

To remove semantic search:

```bash
# Remove index
qmd cleanup

# Remove the qmd binary
bun remove -g qmd

# Remove MCP config (manual — delete the "qmd" entry from your config)
```

Your vault files are never modified — removing qmd just removes the search index.
