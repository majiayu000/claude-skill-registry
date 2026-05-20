---
name: literature-review
description: Systematic search methodology, taxonomy construction, citation graph exploration, and related work synthesis for ML research.
---

# Literature Review for ML Research

## Search Strategy by Research Phase

### Decision Table: Search Approach

| Phase | Goal | Primary Source | Strategy |
|-------|------|---------------|----------|
| Scoping | Understand landscape | Survey papers, textbooks | Start broad, read abstracts only |
| Deep dive | Core related work | Semantic Scholar, Google Scholar | Citation graph: forward + backward |
| Gap finding | Identify what is missing | Recent venue proceedings | Filter by venue + year, read intros |
| Positioning | Place your contribution | Top-cited papers in subfield | Compare methods, build taxonomy |
| Camera-ready | Complete related work | arxiv, workshop papers | Fill gaps reviewers might flag |

### Decision Table: Source Selection

| Source | Best For | Limitations |
|--------|----------|-------------|
| Google Scholar | Broad search, citation counts | Noisy results, includes predatory |
| Semantic Scholar | Citation graph, API access | Smaller index than GS |
| arxiv | Preprints, latest work | No peer review, variable quality |
| DBLP | Venue-specific search | Metadata only, no full text |
| Connected Papers | Visual citation graph | Limited to seed paper quality |
| Papers With Code | SOTA tables, code links | Benchmark-centric bias |
| ACL Anthology | NLP-specific | Single domain |

## Systematic Search Methodology

### Query Construction

```
# Start with core concept combinations
query_templates = [
    # Broad
    '"{method}" AND "{task}"',
    # Venue-scoped
    '"{method}" AND "{task}" site:arxiv.org',
    # Recent
    '"{method}" AND "{task}" after:2023',
    # Author-scoped
    'author:"{known_author}" "{topic}"',
]

# Example for a transformer efficiency paper:
queries = [
    '"efficient transformer" AND "long sequence"',
    '"linear attention" OR "sparse attention"',
    '"subquadratic" AND "self-attention"',
    '"flash attention" OR "memory efficient attention"',
]
```

### Semantic Scholar API Usage

```python
import requests
from typing import Optional

S2_API = "https://api.semanticscholar.org/graph/v1"

def search_papers(
    query: str,
    year_range: Optional[str] = "2020-2025",
    limit: int = 20,
    fields: str = "title,year,citationCount,abstract,authors,venue",
) -> list[dict]:
    """Search Semantic Scholar for papers."""
    params = {
        "query": query,
        "limit": limit,
        "fields": fields,
    }
    if year_range:
        params["year"] = year_range
    resp = requests.get(f"{S2_API}/paper/search", params=params)
    resp.raise_for_status()
    return resp.json().get("data", [])

def get_citations(paper_id: str, direction: str = "citations") -> list[dict]:
    """Get forward (citations) or backward (references) links.

    direction: 'citations' (who cites this) or 'references' (who this cites)
    """
    fields = "title,year,citationCount,authors,venue"
    resp = requests.get(
        f"{S2_API}/paper/{paper_id}/{direction}",
        params={"fields": fields, "limit": 100},
    )
    resp.raise_for_status()
    return resp.json().get("data", [])

# Usage
papers = search_papers("flash attention efficient transformer")
for p in papers[:5]:
    print(f"[{p['year']}] {p['title']} (cited: {p['citationCount']})")
```

## Paper Summary Template

```markdown
### Paper: {Title}
- **Authors**: {First Author} et al., {Year}
- **Venue**: {Conference/Journal}
- **Citations**: {count} (as of {date})

#### Problem
{One sentence: what problem does this solve?}

#### Method
{2-3 sentences: key technical contribution}

#### Results
{Key numbers: which benchmarks, what improvement over what baseline}

#### Relevance to Our Work
{How it relates: extends/contradicts/enables/competes with our approach}

#### Limitations
{What they don't address that we do, or known weaknesses}
```

## Comparison Table Template

```markdown
| Method | Year | Task | Key Idea | Complexity | Acc. | Code |
|--------|------|------|----------|------------|------|------|
| Method A | 2023 | X | Does Y via Z | O(n log n) | 92.1 | Yes |
| Method B | 2024 | X | Does Y via W | O(n) | 93.4 | No |
| Ours | 2025 | X | Does Y via V | O(n) | 94.2 | Yes |
```

## Taxonomy Construction

### Building a Taxonomy

```
Step 1: Collect 30-50 papers in the space
Step 2: Tag each paper along orthogonal axes:
  - Approach type (e.g., attention-based, convolution-based, hybrid)
  - Training paradigm (supervised, self-supervised, few-shot)
  - Scale (small model, foundation model)
  - Application domain (vision, language, multimodal)
Step 3: Group papers that share tags -> these form taxonomy branches
Step 4: Identify sparse cells -> these are research gaps
```

### Related Work Section Structure

```latex
\section{Related Work}
% Organize by conceptual axis, not chronologically

\paragraph{Efficient Attention Mechanisms.}
Linear attention~\citep{katharopoulos2020} replaces softmax with...
Sparse attention patterns~\citep{child2019,beltagy2020} reduce complexity by...
Our work differs in that...

\paragraph{Knowledge Distillation for Transformers.}
\citet{sanh2019} showed that... \citet{jiao2020} extended this to...
Unlike these approaches, we...

\paragraph{Dynamic Computation.}
Early exit~\citep{schwartz2020} and token pruning~\citep{goyal2020} adaptively...
Our method is complementary to these techniques and can be combined with...
```

## Staying Current

### Monitoring Strategy

| Channel | Frequency | Action |
|---------|-----------|--------|
| arxiv-sanity / Hugging Face Daily Papers | Daily | Skim titles, star relevant |
| Key author Twitter/X feeds | Weekly | Note new preprints |
| Top venue proceedings (NeurIPS, ICML, ICLR) | Per cycle | Read all accepted in subfield |
| Google Scholar alerts | As notified | Check forward citations of key papers |
| ML subreddits, Discord servers | Weekly | Track community reception |

### arxiv Monitoring Script

```python
import arxiv

def search_recent(
    query: str,
    max_results: int = 20,
    sort_by: arxiv.SortCriterion = arxiv.SortCriterion.SubmittedDate,
) -> list[dict]:
    """Fetch recent arxiv papers matching query."""
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=sort_by,
    )
    results = []
    for paper in search.results():
        results.append({
            "title": paper.title,
            "authors": [a.name for a in paper.authors[:3]],
            "abstract": paper.summary[:200],
            "url": paper.entry_id,
            "published": paper.published.strftime("%Y-%m-%d"),
        })
    return results

papers = search_recent("cat:cs.LG AND ti:efficient AND ti:attention")
```

## Gotchas and Anti-Patterns

### Citation Bias
- Over-citing top labs / top venues while ignoring work from smaller groups.
- Citing only papers that support your narrative. Reviewers will flag missing contradicting work.
- **Fix**: Explicitly search for papers that contradict or weaken your claims. Include them and explain differences.

### Missing Non-Arxiv Work
- Many fields publish primarily in journals (medical imaging, robotics). Arxiv-only search misses these.
- Workshop papers often contain early versions of important ideas.
- **Fix**: Search DBLP and Google Scholar in addition to arxiv. Check domain-specific repositories (e.g., PubMed for medical ML).

### Conflating Citation Count with Impact
- Recent papers have low citation counts regardless of quality.
- Some high-citation papers are cited mainly for datasets, not methods.
- **Fix**: Weight recent papers by venue and author track record, not citations alone. Read the paper before citing.

### Recency Bias
- Ignoring foundational older work that established the concepts you build on.
- Citing the latest version of an idea without crediting the original.
- **Fix**: Trace ideas back to their origin. Cite both the original and the most relevant recent extension.

### Superficial Reading
- Citing based on abstract only leads to mischaracterization.
- **Fix**: For any paper in your related work section, read at minimum: abstract, intro, method section, and main results table. For direct competitors, read the full paper.

### Incomplete Search Termination
- Stopping search when you have "enough" references without systematic coverage.
- **Fix**: Define search scope upfront (queries, venues, year range). Track coverage in a spreadsheet. Stop when new queries return only already-seen papers.

## Agent Team Mode

For comprehensive literature reviews covering 30+ papers across multiple sources and subfields.

### Team Configuration

```yaml
team:
  recommended_size: 4
  agent_roles:
    - name: searcher-arxiv
      type: Explore
      focus: "Search arxiv for preprints, recent submissions, related work"
      skills_loaded: ["research:literature-review"]
    - name: searcher-scholar
      type: Explore
      focus: "Search Semantic Scholar and Google Scholar for peer-reviewed work"
      skills_loaded: ["research:literature-review"]
    - name: searcher-venues
      type: Explore
      focus: "Search specific top venues (NeurIPS, ICML, ICLR, ACL) proceedings"
      skills_loaded: ["research:literature-review"]
    - name: citation-explorer
      type: Explore
      focus: "Forward + backward citation graph exploration from seed papers"
      skills_loaded: ["research:literature-review"]
  file_ownership: "shared-read-only"
  lead_mode: "hands-on"
```

### Team Workflow

1. Lead defines search scope (queries, year range, target venues) and distributes query sets
2. All searchers execute their queries in parallel across different sources
3. citation-explorer starts from known seed papers, explores citation graph
4. Lead deduplicates results, builds comparison table, constructs taxonomy
5. Lead identifies sparse taxonomy cells (research gaps) and writes related work synthesis

### Single-Agent Fallback

Without team mode, execute all phases sequentially (default behavior). Team mode is an optional enhancement.
