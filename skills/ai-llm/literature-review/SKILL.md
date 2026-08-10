---
name: literature-review
description: Conduct a structured literature review on a given topic by defining a search strategy, applying inclusion and exclusion criteria, extracting key findings, and synthesizing results into a coherent academic review. Use when the user requests literature review or provides relevant inputs for this workflow.
license: MIT
metadata:
  author: awesome-ai-agent-skills
  version: 1.0.0
---

# Literature Review

This skill enables an AI agent to conduct a rigorous, structured literature review following established academic methodology. The agent defines a search strategy with targeted keywords, applies explicit inclusion and exclusion criteria to filter results, extracts key data from selected papers, and synthesizes the findings into a thematic narrative with a summary table and reference list. The workflow is inspired by systematic review practices (including PRISMA-style reporting) and is suitable for academic research, technology landscape analysis, and evidence-based decision making.

## Workflow

1. **Define the Research Question and Scope:** Work with the user to formulate a precise research question using a framework such as PICO (Population, Intervention, Comparison, Outcome) or a domain-appropriate equivalent. Establish the review's scope: time range, languages, source types (journal articles, conference papers, preprints), and any domain constraints.

2. **Develop the Search Strategy:** Generate a set of search queries using combinations of primary keywords, synonyms, and Boolean operators. Identify the databases and sources to search (e.g., Google Scholar, Semantic Scholar, arXiv, PubMed, ACM Digital Library, IEEE Xplore). Document the complete search strategy for reproducibility.

3. **Screen and Filter Results:** Apply predefined inclusion and exclusion criteria to the search results. Inclusion criteria typically cover topic relevance, publication date range, study type, and language. Exclusion criteria filter out duplicates, non-peer-reviewed opinion pieces, retracted papers, and off-topic results. Record the number of papers at each stage for a PRISMA-style flow.

4. **Extract Key Data:** For each included paper, extract structured information: title, authors, year, venue, research question, methodology, key findings, limitations, and relevance to the review question. Store this data in a consistent format (table or structured notes) for cross-paper comparison.

5. **Synthesize Themes and Findings:** Organize extracted data into themes or categories that emerge across papers. Identify areas of consensus, debate, and gaps in the literature. Write a narrative synthesis that connects individual findings into a coherent story, supported by a summary comparison table.

6. **Write the Review Document:** Produce the final literature review with these sections: introduction and research question, methodology (search strategy, criteria, PRISMA flow), thematic synthesis, discussion of gaps and future directions, and a complete reference list in a standard citation format.

## Usage

Provide the agent with a research topic or question. Optionally specify the desired scope (time range, source types), the number of papers to include, or a particular synthesis format.

```
Conduct a literature review on LLM evaluation benchmarks published between 2022-2025.

Focus: What benchmarks exist, what do they measure, and what gaps remain
in evaluating reasoning, safety, and real-world task completion?
```

## Examples

### Example 1: Literature Review on LLM Evaluation Benchmarks

**User Request:**
> Review the literature on LLM evaluation benchmarks from 2022-2025, focusing on reasoning, safety, and task completion.

**Search Strategy:**

| Database | Query |
|---|---|
| Semantic Scholar | "large language model evaluation benchmark" AND (reasoning OR safety OR "task completion") |
| arXiv | "LLM benchmark" AND ("2023" OR "2024" OR "2025") |
| ACM DL | "language model assessment" AND "benchmark suite" |
| Google Scholar | "LLM evaluation" survey OR "systematic review" 2023..2025 |

**Inclusion/Exclusion Criteria:**

| Criteria | Type | Rule |
|---|---|---|
| Published 2022-2025 | Inclusion | Must be within date range |
| Peer-reviewed or major preprint | Inclusion | Accepted at top venues or arXiv with 10+ citations |
| Proposes or surveys benchmarks | Inclusion | Must discuss specific evaluation frameworks |
| Blog posts / opinion pieces | Exclusion | No non-academic sources |
| Non-English | Exclusion | English-language only |
| Duplicates / superseded versions | Exclusion | Keep most recent version only |

**PRISMA-Style Flow:**
```
Records identified through search: 847
After duplicate removal:           612
After title/abstract screening:    148
After full-text assessment:         42
Final papers included:              42
```

**Synthesis Table (excerpt):**

| Benchmark | Year | Focus Area | Key Metric | Limitations |
|---|---|---|---|---|
| MMLU | 2023 | Knowledge & reasoning | Accuracy across 57 tasks | Static; no multi-step reasoning |
| HumanEval+ | 2023 | Code generation | pass@k | Narrow scope (Python functions) |
| AgentBench | 2023 | Real-world task completion | Success rate across 8 environments | High cost to run; environment-specific |
| TrustLLM | 2024 | Safety & trustworthiness | 6 dimensions including fairness | Self-reported; needs human validation |
| GPQA | 2024 | Graduate-level reasoning | Accuracy on expert-written questions | Small dataset; domain-specific |
| SWE-bench | 2024 | Software engineering tasks | Resolved rate on real GitHub issues | Requires execution infrastructure |

**Synthesized Finding (excerpt):**
> The literature reveals a clear trajectory from static knowledge tests (MMLU) toward dynamic, agentic evaluations (AgentBench, SWE-bench) that measure an LLM's ability to act in realistic environments. However, a significant gap persists: no single benchmark suite comprehensively evaluates reasoning, safety, and task completion together. Most benchmarks optimize for one dimension, creating a fragmented evaluation landscape where models can appear strong on reasoning benchmarks while performing poorly on safety metrics.

---

### Example 2: Systematic Review Protocol with PRISMA-Style Flow

**User Request:**
> Create a systematic review protocol for studying the effectiveness of retrieval-augmented generation (RAG) in reducing LLM hallucinations.

**Research Question (PICO format):**
- **Population:** Large language models (GPT-4 class and above)
- **Intervention:** Retrieval-augmented generation (RAG)
- **Comparison:** Non-RAG baseline (standard prompting)
- **Outcome:** Hallucination rate reduction (measured by factual accuracy metrics)

**Search Strategy:**
```
("retrieval-augmented generation" OR "RAG") AND
("hallucination" OR "factual accuracy" OR "faithfulness") AND
("large language model" OR "LLM" OR "GPT" OR "Claude")
```
Databases: Semantic Scholar, arXiv, ACM Digital Library, Google Scholar
Date range: January 2023 to December 2025

**Screening Protocol:**
```
Phase 1 — Title/Abstract Screening:
  Include if: Empirically measures hallucination with and without RAG
  Exclude if: Theoretical only, no quantitative results, not LLM-focused

Phase 2 — Full-Text Review:
  Include if: Reports specific hallucination metrics (FActScore, ROUGE-L
              against ground truth, human evaluation scores)
  Exclude if: RAG used for non-factual tasks (creative writing, code gen)
```

**Data Extraction Template:**

| Field | Description |
|---|---|
| Paper ID | Unique identifier |
| Model(s) tested | Which LLMs were evaluated |
| RAG architecture | Retrieval method, chunk size, top-k |
| Baseline | What non-RAG setup was compared |
| Hallucination metric | FActScore, human eval, accuracy, etc. |
| Result | Percentage change in hallucination rate |
| Domain | General knowledge, medical, legal, etc. |

**Expected PRISMA Diagram:**
```
Identification:  ~1,200 records from 4 databases
Screening:       ~400 after title/abstract review
Eligibility:     ~80 after full-text assessment
Included:        ~35 meeting all criteria
```

## Best Practices

- **Document every decision for reproducibility.** Record search queries, database dates, and the exact inclusion/exclusion criteria so another researcher could replicate the review.
- **Use structured data extraction.** A consistent extraction template ensures you capture the same fields from every paper, making cross-study comparison possible.
- **Distinguish between quantity and quality of evidence.** A theme supported by 20 blog posts is weaker than one supported by 3 rigorous RCTs. Weight your synthesis accordingly.
- **Report what you did not find.** Gaps in the literature are as important as the findings. Explicitly note underexplored areas, missing populations, or untested conditions.
- **Keep the synthesis thematic, not paper-by-paper.** A literature review that reads as a list of paper summaries is less useful than one organized around themes that weave findings together.
- **Update the search before finalizing.** If the review takes weeks to write, re-run the search before submitting to catch newly published work.

## Edge Cases

- **Insufficient literature:** If fewer than 5 relevant papers exist, acknowledge this and reframe the output as a "scoping review" or "research gap analysis" rather than a comprehensive literature review.
- **Preprint-heavy fields:** In fast-moving areas like AI/ML, much of the relevant work may be on arXiv without peer review. Include preprints but flag their review status and note this as a limitation of the evidence base.
- **Conflicting study results:** When studies reach opposite conclusions, compare their methodologies, sample sizes, and conditions. Present the conflict transparently rather than arbitrarily siding with one study.
- **Interdisciplinary topics:** Reviews spanning multiple fields (e.g., AI + healthcare) may require searching domain-specific databases (PubMed) in addition to CS databases. Adjust the search strategy accordingly and note where terminology differs between fields.
- **Non-English sources:** If the topic has significant literature in other languages, note this limitation if you restrict to English and flag key non-English works that appear in citation lists.
