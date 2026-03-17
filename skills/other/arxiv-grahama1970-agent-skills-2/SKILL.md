---
name: arxiv
description: >
  Search arXiv for papers and extract knowledge into memory.
  Use `search` to find papers, `learn` to extract knowledge.
allowed-tools: Bash, Read
triggers:
  - learn from arxiv
  - learn from this paper
  - extract knowledge from paper
  - find papers on
  - search arxiv
  - arxiv
metadata:
  short-description: arXiv paper search and knowledge extraction
---

# arXiv Skill

Search arXiv and extract knowledge into memory.

## Commands

| Command | Description |
|---------|-------------|
| `search` | Find papers (returns abstracts for triage) |
| `learn` | Extract knowledge into memory |

---

## MANDATORY: Dynamic Context Generation

**NON-NEGOTIABLE:** Before ANY arxiv operation, the agent MUST generate a dynamic context file that captures the current collaboration goals.

### Why This Is Required

Without dynamic context:
- Search returns tangentially related papers
- Abstract triage lacks clear relevance criteria
- Extracted knowledge is generic ("What does paper say about X?")

With dynamic context:
- Search is targeted to specific implementation needs
- Abstract evaluation has clear accept/reject criteria
- Extracted knowledge is actionable ("How to implement X as code")

---

## Workflow: Context-First Paper Discovery

```
0. CONTEXT  → Generate dynamic context from conversation (REQUIRED)
1. SEARCH   → Use context to find relevant papers
2. TRIAGE   → Evaluate abstracts against context goals
3. DECIDE   → User picks which papers to extract
4. LEARN    → Extract with context for focused knowledge chunks
```

### Step 0: Generate Dynamic Context (REQUIRED)

Before searching, the agent MUST create `/tmp/arxiv_context.md` with:

```markdown
# Research Context: [Your Specific Goal]

## What We're Building
[Describe the specific feature/system, e.g., "Theory of Mind for Horus agent"]

## Current State
[What already exists, what's implemented, what we have]

## What We Need From Papers
1. [Specific question 1, e.g., "How to represent belief confidence as data structure"]
2. [Specific question 2, e.g., "When to trigger counterfactual reflection"]
3. [Specific question 3, e.g., "Algorithm for updating beliefs on contradiction"]

## Search Terms to Try
- [term 1]
- [term 2]

## Relevance Criteria for Abstract Triage
- HIGH: Papers that directly address [specific need]
- MEDIUM: Papers with related techniques that could adapt
- LOW: Tangentially related, skip unless nothing better

## Knowledge Extraction Focus
- Extract: [what kind of knowledge, e.g., "algorithms, data structures, update rules"]
- Skip: [what to ignore, e.g., "evaluation metrics, dataset descriptions, future work"]

## Output Format Preference
Phrase as implementation problems, not summaries:
- BAD: "What does the paper say about X?"
- GOOD: "How should we implement X? What code pattern?"
```

### Step 1: Search With Context

After creating context, use it to guide search:

```bash
# Search guided by context goals
./run.sh search -q "theory of mind BDI agent belief tracking" -n 10
```

### Step 2: Triage Against Context

Evaluate each abstract against the context's relevance criteria:

```markdown
## Papers Found - Evaluating Against Context Goals

### 1. **Paper Title** (arXiv:XXXX.XXXXX)
> [Abstract]

**Against context:**
- Addresses goal 1 (belief representation): YES - describes BDI dict structure
- Addresses goal 2 (counterfactual reflection): NO
- **Verdict: HIGH** - directly answers our data structure question

### 2. **Paper Title** (arXiv:XXXX.XXXXX)
> [Abstract]

**Against context:**
- Addresses goal 1: NO
- Addresses goal 2: YES - describes reflection trigger conditions
- **Verdict: HIGH** - directly answers our algorithm question

---
Which papers should I extract?
```

### Step 3: Extract With Context File

Pass the context file to `learn` for focused extraction:

```bash
./run.sh learn 2501.15355 --scope persona-research --context-file /tmp/arxiv_context.md
```

**Do NOT proceed without user confirmation on paper selection.**

---

## `search` - Find Papers

```bash
./run.sh search -q "agent memory" -n 5
```

Returns papers with **full abstracts** for quick triage.

| Option | Description |
|--------|-------------|
| `-q` | Search query (required) |
| `-n` | Max results (default: 10) |
| `-c` | Category filter (e.g., cs.LG) |
| `-m` | Papers from last N months |
| `--smart` | LLM translates natural language query |

---

## `learn` - Extract Knowledge

```bash
./run.sh learn 2601.08058 --scope memory
```

Full pipeline: download → profile → extract → Q&A → interview → store → verify edges.

| Option | Description |
|--------|-------------|
| `--scope` | Memory scope (required) |
| `--context` | Domain focus for relevance |
| `--dry-run` | Preview without storing |
| `--skip-interview` | Auto-accept recommendations |
| `--accurate` | Force PDF + VLM extraction |
| `--mode` | Interview mode: `auto`, `html`, `tui` (default: auto) |


---

## Extraction Mode (HTML-First)

**NEW:** The `learn` command now uses **HTML-first extraction** by default:

1. Downloads HTML from [ar5iv.org](https://ar5iv.org) (arxiv papers converted to clean HTML)
2. Runs quick profile check (counts figures/tables)
3. Routes to appropriate extraction mode

```
arxiv learn <id>
       │
       ├── fast mode (default) ──► ar5iv HTML ──► extractor HTML
       │   - Most research papers       (100% extraction parity)
       │   - Text-heavy content         (no PDF column issues)
       │
       └── accurate mode ──► arxiv PDF ──► extractor PDF + VLM
           - Papers where figures are critical
           - Complex tables with precise values
           - Use: --accurate flag
```

### Why HTML-First?

| Aspect | HTML (ar5iv) | PDF |
|--------|--------------|-----|
| Extraction quality | 100% parity | ~87% (column detection issues) |
| Speed | Fast (~5s) | Slower (~30s-2min) |
| Figure captions | Included | Requires VLM |
| Math rendering | MathML preserved | Text approximation |
| Layout issues | None | 2-column detection problems |

**ar5iv.org** converts arxiv LaTeX source to semantic HTML with MathML equations and proper structure. This eliminates PDF extraction issues.

### When to Use `--accurate`

| Content Type | Recommended Mode | Why |
|--------------|------------------|-----|
| **Most research papers** | default (HTML) | Text + captions are sufficient |
| **Survey papers** | default (HTML) | Broad coverage, exact figures not critical |
| **Papers with critical diagrams** | `--accurate` | When visual content IS the point |
| **Papers with complex data tables** | `--accurate` | When precise numbers matter |

```bash
# Default: HTML extraction (fast, reliable)
./run.sh learn 2601.10025 --scope persona-research

# Force accurate mode for figure-heavy papers
./run.sh learn 2501.15355 --scope tom-research --accurate
```

### Profile-Based Routing

The skill automatically profiles downloaded HTML to suggest extraction mode:

- **< 20 figures AND < 10 tables**: Uses HTML (fast mode)
- **> 20 figures OR > 10 tables**: Suggests accurate mode (or use `--accurate`)

Profile output shows in logs:
```
Profile: 12 figures, 4 tables → Using HTML extraction (fast mode)
```

---

## Happy Path

```bash
# 1. Search - get abstracts
./run.sh search -q "agent memory systems" -n 5

# 2. STOP - discuss abstracts with user, assess relevance

# 3. Learn - extract user-selected papers (HTML extraction by default)
./run.sh learn 2601.10702 --scope memory --context "agent systems"
```

---

## Examples

### Research Survey (HTML extraction - default)
```bash
./run.sh learn 2601.10025 --scope persona-research --context "LLM personality"
```

### Paper with Critical Figures (accurate mode)
```bash
./run.sh learn 2501.15355 --scope tom-research --context "BDI architecture" --accurate
```

### Dry Run First
```bash
# Preview what would be extracted
./run.sh learn 2601.10025 --scope test --dry-run
```

### Download HTML Only
```bash
# Download ar5iv HTML for manual inspection
./run.sh download -i 2501.15355 --format html
```

### Batch Processing (Parallel)
```bash
# Process multiple papers in parallel (default: 2 concurrent)
./run.sh batch 2501.15355 2502.14171 2310.10701 --scope tom-research --context-file /tmp/context.md

# Increase parallelism for faster processing
./run.sh batch 2501.15355 2502.14171 2310.10701 --scope research --parallel 3

# Dry run to preview
./run.sh batch 2501.15355 2502.14171 --scope test --dry-run
```

| Option | Description |
|--------|-------------|
| `--parallel N` | Max papers to process concurrently (default: 2) |
| `--context-file` | Rich context file for focused extraction |
| `--skip-interview` | Auto-accept (default for batch) |
| `--dry-run` | Preview without storing |

**Note:** Recommended parallelism is 2-3 papers. Higher values may hit API rate limits.

---

## Dependencies

| Component | URL | Purpose |
|-----------|-----|---------|
| ar5iv.org | https://ar5iv.org | LaTeX to HTML conversion for arxiv papers |
| extractor skill | (sibling skill) | HTML/PDF content extraction |
| qra skill | (sibling skill) | Q&A pair generation from text |
