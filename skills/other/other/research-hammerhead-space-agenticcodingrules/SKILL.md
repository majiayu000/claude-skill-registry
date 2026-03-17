---
name: research
description: Systematic technical and scientific research for algorithms, papers, libraries, and implementation strategies. Use when investigating new algorithms, comparing approaches, finding reference implementations, reviewing literature, or gathering information before design decisions.
---

# Technical Research

## Purpose

Conduct thorough, structured research to inform design and implementation decisions. Produce actionable findings with clear sources, not just raw information dumps.

## When to Use

- Investigating an algorithm or method before implementing it
- Comparing competing approaches (solvers, formulations, libraries)
- Finding reference implementations or validation data
- Understanding a mathematical formulation from the literature
- Evaluating whether an external package meets requirements

## Process

### 1. Define the Research Question

Clarify with the user:
- What specific question needs answering?
- What decisions will this research inform?
- Are there known starting points (papers, packages, textbooks)?
- What constraints matter (performance, accuracy, AD-compatibility, license)?

### 2. Search Strategy

Execute multiple search angles:
- **Academic/algorithmic**: search for papers, textbook references, survey articles
- **Implementation**: search for existing Julia packages, GitHub repos, reference code
- **Community**: search Julia Discourse, relevant forums, package documentation
- **Comparison**: search for benchmarks, trade-off analyses, known limitations

Formulate 3-5 query variations per angle for coverage.

### 3. Evaluate Sources

For each source found:
- **Relevance**: Does it directly address the research question?
- **Authority**: Is it a peer-reviewed paper, official docs, or a blog post?
- **Recency**: Is the information current? Are there newer approaches?
- **Applicability**: Does it match our constraints (Julia, AD-compatible, etc.)?

### 4. Synthesize Findings

Organize results into a structured summary:

```markdown
## Research: [Topic]

### Question
[The specific question being investigated]

### Key Findings
- Finding 1 (with source)
- Finding 2 (with source)

### Approaches Compared
| Approach | Pros | Cons | Source |
|----------|------|------|--------|
| ...      | ...  | ...  | ...    |

### Recommendation
[Clear recommendation with rationale]

### Open Questions
[Anything unresolved that needs further investigation]

### References
1. [Author, Title, Year, URL/DOI]
```

### 5. Verify Key Claims

- Cross-reference important claims across multiple sources
- Flag contradictions or disagreements in the literature
- Note where consensus exists vs. active debate

## Output Requirements

- Always provide source URLs or citations for claims
- Use direct quotes for important technical statements
- Clearly distinguish established facts from opinions/recommendations
- Identify gaps where information is missing or uncertain
- End with actionable next steps
