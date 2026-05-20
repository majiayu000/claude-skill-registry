---
name: pensions-intel
description: "Context-efficient UK pensions legal intelligence via CLI. Use for semantic search, gap analysis, citation chains, and handbook guidance. Triggers on: obligation search, compliance gap, citation, handbook guidance, trustee duties."
version: "1.0"
tier: domain
token_budget: 1200
requires: []
---

# Pensions Legal Intelligence: CLI-First Research

Context-efficient access to UK pensions regulatory data via the apex-intel CLI. Use this skill when you need quick, targeted queries without loading multiple MCP servers.

---

## When To Use

**Trigger conditions:**
- User asks about UK pensions obligations (semantic search)
- User needs compliance gap analysis ("what am I missing?")
- User needs legal citations for obligations
- User wants handbook/guidance on a topic
- User asks "what obligations relate to X?"

**Prefer this over pensions-research skill when:**
- Context window is constrained
- Query is targeted (not exploratory)
- User needs quick answers, not comprehensive research
- Working on multiple topics in one session

**Keywords:**
- "obligation", "search obligations", "find obligations"
- "gap analysis", "compliance gaps", "missing"
- "citation", "cite", "source", "legislation"
- "handbook", "guidance", "TPR guidance"

---

## CLI Tool Location

```
~/Projects/pensions/apex-governance/tools/apex_intel.py
```

Run with: `uv run apex_intel.py <command> [options]`

---

## Command Reference

### search - Semantic Search

Find obligations using natural language:

```bash
uv run apex_intel.py search "trustee disclosure duties"
uv run apex_intel.py search "ESG investment governance" --scheme-type DB
uv run apex_intel.py search "funding requirements" --limit 5 --json
```

Options:
- `--limit, -l` (int): Maximum results (1-50, default: 10)
- `--scheme-type, -s`: Filter by scheme (DB, DC, Hybrid, PSPS, All)
- `--type, -t`: Filter by category (Governance, Reporting, etc.)
- `--json`: Output as JSON for agent consumption

### detail - Full Obligation Details

Get complete obligation with enrichment:

```bash
uv run apex_intel.py detail TPR-GC-001
uv run apex_intel.py detail PA04-S227-001 --json
```

Returns:
- Core info (source act, section, duty holder, priority)
- Statutory provisions
- Case law references
- Related obligations
- Enforcement bodies
- Definitions

### gaps - Compliance Gap Analysis

Identify missing obligations:

```bash
uv run apex_intel.py gaps --known TPR-GC-001,TPR-GC-002
uv run apex_intel.py gaps --known TPR-GC-001 --threshold 60 --priority High
```

Options:
- `--known, -k` (required): Comma-separated obligation IDs
- `--threshold, -t`: Similarity threshold (0-100, default: 50)
  - 60-70: Strict (many gaps)
  - 50: Balanced (recommended)
  - 30-40: Loose (few gaps)
- `--limit, -l`: Max gaps to return
- `--priority, -p`: Filter by priority (High, Medium, Low, Critical)

### similar - Find Related Obligations

Find semantically similar obligations:

```bash
uv run apex_intel.py similar PA04-S227-001
uv run apex_intel.py similar TPR-GC-001 --limit 10 --json
```

### handbook - TPR Handbook Search

Search handbook guidance:

```bash
uv run apex_intel.py handbook "integrated risk management"
uv run apex_intel.py handbook "ESG due diligence" --limit 10
```

### cite - Glass Box Citations

Generate traceable citations:

```bash
uv run apex_intel.py cite TPR-GC-001
uv run apex_intel.py cite PA04-S227-001 --format full
uv run apex_intel.py cite TPR-GC-001 --format legal
```

Formats:
- `short`: ID and source act only
- `full`: Complete with implementing SIs
- `legal`: Formal legal citation

---

## Workflow Patterns

### Pattern 1: Quick Research

```bash
# 1. Search for relevant obligations
uv run apex_intel.py search "disclosure duties" --limit 5 --json

# 2. Get details on most relevant
uv run apex_intel.py detail <obligation_id> --json
```

### Pattern 2: Gap Analysis

```bash
# 1. List obligations user knows about
# (from their input or previous queries)

# 2. Run gap analysis
uv run apex_intel.py gaps --known OB-001,OB-002,OB-003 --threshold 50 --json

# 3. Report gaps with citations
```

### Pattern 3: Citation Chain

```bash
# 1. Get obligation details
uv run apex_intel.py detail TPR-GC-001 --json

# 2. Build citation chain from response
# Obligation → Source Act s.Section → Implementing SI → Enforcement Body
```

### Pattern 4: Comprehensive Research

```bash
# 1. Semantic search
uv run apex_intel.py search "topic" --json

# 2. Get similar obligations for top result
uv run apex_intel.py similar <top_id> --json

# 3. Search handbook for guidance
uv run apex_intel.py handbook "topic" --json

# 4. Combine findings with citations
```

---

## Query Strategy Selection

| User Request | Command | Notes |
|-------------|---------|-------|
| "What obligations...?" | `search` | Semantic search |
| "Are we compliant with...?" | `gaps` | Gap analysis |
| "Citation for...?" | `cite` | Citation chain |
| "TPR guidance on...?" | `handbook` | Handbook search |
| "Related to obligation X" | `similar` | Semantic similarity |
| "Details of X" | `detail` | Full enrichment |

---

## Output Format for Agents

Always use `--json` flag when parsing results programmatically:

```python
import subprocess
import json

result = subprocess.run(
    ["uv", "run", "apex_intel.py", "search", query, "--json"],
    capture_output=True, text=True,
    cwd="~/Projects/pensions/apex-governance/tools"
)
data = json.loads(result.stdout)
obligations = data["results"]
```

---

## Glass Box AI Principle

**Every legal conclusion must be traceable:**

```
Conclusion → Obligation ID → Statutory Provision → Legislation
```

When reporting findings, always include:
1. Obligation ID
2. Source legislation (Act + section)
3. Duty holder
4. TPR priority
5. Enforcement body (if applicable)

**Never state legal positions without citation chains.**

---

## Context Efficiency

This skill uses ~1,200 tokens vs ~8,000+ tokens for full MCP stack.

| Approach | Context Cost | Use Case |
|----------|-------------|----------|
| apex-intel CLI | ~1,200 tokens | Targeted queries |
| Full MCP stack | ~8,000+ tokens | Exploratory research |

**Recommendation:** Use CLI for 80% of queries, MCP for complex multi-hop exploration.

---

## Prerequisites

**Auto-start (default):** The CLI will automatically start the API backend if not running.

**Manual requirements:**
- Backend venv at `backend/.venv` (created with `uv venv --python 3.12 .venv`)
- Dependencies installed

**Optional:**
- Vectorized API at localhost:5001 (for semantic search; falls back to keyword)
- Doppler for credentials: `doppler run -- uv run apex_intel.py ...`

**Disable auto-start:**
```bash
uv run apex_intel.py --no-auto-start search "query"
# or
APEX_AUTO_START=false uv run apex_intel.py search "query"
```
