---
name: analyze-arxiv-paper
description: 'Deep analysis of an arXiv research paper for inclusion in news digest
  research deep-dives. Extracts key contributions, methodology, results, limitations,
  and generates a practitioner-focused summary with potential impacts.

  '
license: MIT
compatibility: Requires OpenAI-compatible LLM API access
metadata:
  domain: news
  category: diagnostic
  requires-approval: false
  confidence: 0.85
  mcp-servers: []
input:
- name: paper
  type: ArxivPaper
  description: Paper with arxiv_id, title, authors, abstract, categories, pdf_url
- name: analysis_depth
  type: str
  default: standard
  description: '"standard" for digest inclusion, "deep" for featured research spotlight'
output:
- name: analysis
  type: PaperAnalysis
  description: Comprehensive paper analysis with summary, key findings, and impact
    assessment
- name: digest_worthy
  type: bool
  description: Whether paper is noteworthy enough for digest inclusion
- name: spotlight_candidate
  type: bool
  description: Whether paper deserves a featured research deep-dive
---

# Analyze ArXiv Paper

Perform deep analysis of a research paper to determine its newsworthiness and generate a practitioner-focused summary.

## When to Use

- Evaluating papers for digest inclusion
- Creating research deep-dive sections
- Assessing impact and relevance of new research
- Keywords: arxiv, research, paper analysis, academic, deep-dive

## Prerequisites

- Paper has valid title and abstract
- LLM API available for analysis

## Input Schema

```json
{
  "paper": {
    "arxiv_id": "2601.12345",
    "title": "Paper Title",
    "authors": ["Author One", "Author Two"],
    "abstract": "Paper abstract text...",
    "categories": ["cs.AI", "cs.LG"],
    "pdf_url": "https://arxiv.org/pdf/2601.12345.pdf"
  },
  "analysis_depth": "standard"
}
```

## Actions

### Step 1: Extract Core Information

Parse the paper metadata:
1. Title and authors
2. Primary and secondary categories
3. Abstract text

### Step 2: Identify Research Type

Classify the paper into one of:
- **New Method**: Proposes a new technique or algorithm
- **Benchmark/Evaluation**: Compares existing methods
- **Application**: Applies existing methods to new domain
- **Survey**: Reviews existing literature
- **Theoretical**: Proves theoretical results
- **Dataset**: Introduces new dataset
- **System**: Describes a working system

### Step 3: Extract Key Contributions

From the abstract, identify:
1. **Main Claim**: What does the paper claim to achieve?
2. **Key Innovation**: What's novel about the approach?
3. **Results Summary**: What results are reported?
4. **Comparison Baseline**: What is it compared against?

### Step 4: Assess Relevance

Score relevance to AI practitioners (1-10):
- **Practical applicability**: Can this be used in real applications?
- **Timeliness**: Does this address current hot topics?
- **Novelty**: How new is the approach?
- **Impact potential**: Could this change how things are done?

### Step 5: Generate Practitioner Summary

Write a 2-3 paragraph summary that:
1. Explains what the paper does in accessible terms
2. Highlights why practitioners should care
3. Notes any limitations or caveats
4. Suggests potential applications

### Step 6: Extract Key Takeaways

List 3-5 bullet points of key takeaways:
- What's the main insight?
- What's the practical implication?
- What are the limitations?

### Step 7: Identify Potential Impacts

Assess how this research might impact:
- **Industry**: Near-term commercial applications
- **Research**: Future research directions
- **Open Source**: Likely open-source implementations
- **Adoption Timeline**: Immediate, 6 months, 1 year, longer

### Step 8: Determine Digest Worthiness

A paper is digest-worthy if:
- Relevance score >= 7, OR
- From a major lab (OpenAI, Google, Meta, etc.), OR
- Addresses a trending topic, OR
- Introduces widely-anticipated capability

### Step 9: Determine Spotlight Candidacy

A paper deserves a featured deep-dive if:
- Relevance score >= 8, AND
- High practical applicability, AND
- Likely to influence the field

## Output Schema

```json
{
  "analysis": {
    "arxiv_id": "2601.12345",
    "title": "Paper Title",
    "authors": ["Author One", "Author Two"],
    "research_type": "new_method",
    "main_claim": "We propose a new approach that...",
    "key_innovation": "Unlike prior work, we...",
    "results_summary": "Our method achieves X% improvement over...",
    "practitioner_summary": "This paper introduces...",
    "key_takeaways": [
      "Main insight about the approach",
      "Practical implication for developers",
      "Important limitation to note"
    ],
    "relevance_scores": {
      "practical_applicability": 8,
      "timeliness": 9,
      "novelty": 7,
      "impact_potential": 8,
      "overall": 8
    },
    "potential_impacts": {
      "industry": "Could improve LLM inference efficiency by 2x",
      "research": "Opens new direction for efficient training",
      "open_source": "Likely implementation within 1 month",
      "adoption_timeline": "6_months"
    },
    "topics": ["efficiency", "inference", "llm"],
    "related_to": ["LoRA", "quantization", "distillation"]
  },
  "digest_worthy": true,
  "spotlight_candidate": true
}
```

## Success Criteria

- [ ] Research type correctly identified
- [ ] Main claim extracted from abstract
- [ ] Practitioner summary is accessible (no jargon without explanation)
- [ ] Key takeaways are actionable
- [ ] Relevance scores are justified
- [ ] Digest/spotlight recommendations align with scores

## Failure Handling

| Error Type | Handling Strategy |
|------------|-------------------|
| Abstract too short | Use title-only analysis, lower confidence |
| LLM analysis fails | Return basic metadata with "analysis_failed" flag |
| Unknown research type | Default to "other" type |

## Examples

### Example 1: High-Impact New Method

**Input:**
```json
{
  "paper": {
    "arxiv_id": "2601.54321",
    "title": "FlashAttention-3: Faster Attention with Better Hardware Utilization",
    "authors": ["Tri Dao", "Daniel Fu"],
    "abstract": "We present FlashAttention-3, which achieves 2x speedup over FlashAttention-2 through improved memory access patterns and better GPU utilization. Our method reduces memory bandwidth bottlenecks and enables longer context windows with lower latency.",
    "categories": ["cs.LG", "cs.AI"],
    "pdf_url": "https://arxiv.org/pdf/2601.54321.pdf"
  },
  "analysis_depth": "deep"
}
```

**Output:**
```json
{
  "analysis": {
    "arxiv_id": "2601.54321",
    "title": "FlashAttention-3: Faster Attention with Better Hardware Utilization",
    "authors": ["Tri Dao", "Daniel Fu"],
    "research_type": "new_method",
    "main_claim": "FlashAttention-3 achieves 2x speedup over FlashAttention-2 through improved memory access patterns",
    "key_innovation": "Better GPU memory bandwidth utilization and reduced overhead",
    "results_summary": "2x speedup, longer context windows, lower latency",
    "practitioner_summary": "FlashAttention-3 represents the next evolution in efficient attention mechanisms. For practitioners running LLM inference, this could mean serving twice as many requests with the same hardware, or supporting context windows twice as long. The improvements come from better understanding of GPU memory hierarchies, making this immediately applicable to any transformer-based model. However, adoption requires updating to the latest CUDA toolkit and may need model-specific tuning.",
    "key_takeaways": [
      "2x inference speedup for transformer attention layers",
      "Enables longer context windows without proportional memory increase",
      "Requires latest GPU drivers but no model architecture changes",
      "Particularly impactful for production LLM serving"
    ],
    "relevance_scores": {
      "practical_applicability": 10,
      "timeliness": 10,
      "novelty": 8,
      "impact_potential": 9,
      "overall": 9
    },
    "potential_impacts": {
      "industry": "Immediate cost reduction for LLM inference providers",
      "research": "New baseline for attention efficiency research",
      "open_source": "Implementation expected within weeks",
      "adoption_timeline": "immediate"
    },
    "topics": ["attention", "efficiency", "inference", "transformers"],
    "related_to": ["FlashAttention-2", "xFormers", "memory-efficient attention"]
  },
  "digest_worthy": true,
  "spotlight_candidate": true
}
```

### Example 2: Niche Research Paper

**Input:**
```json
{
  "paper": {
    "arxiv_id": "2601.99999",
    "title": "Improved Convergence Bounds for Federated Learning with Non-IID Data",
    "authors": ["Academic Researcher"],
    "abstract": "We provide tighter convergence bounds for federated averaging under non-IID data distributions. Our theoretical analysis shows that...",
    "categories": ["cs.LG"],
    "pdf_url": "https://arxiv.org/pdf/2601.99999.pdf"
  },
  "analysis_depth": "standard"
}
```

**Output:**
```json
{
  "analysis": {
    "arxiv_id": "2601.99999",
    "title": "Improved Convergence Bounds for Federated Learning with Non-IID Data",
    "authors": ["Academic Researcher"],
    "research_type": "theoretical",
    "main_claim": "Tighter convergence bounds for federated learning",
    "key_innovation": "Improved theoretical analysis of non-IID scenarios",
    "results_summary": "Better mathematical bounds, limited empirical validation",
    "practitioner_summary": "This paper improves our theoretical understanding of federated learning convergence, specifically for scenarios where data across clients is not identically distributed. While the results are mathematically interesting, the practical implications are limited - the bounds are still conservative and don't directly translate to better algorithms. Practitioners working on federated learning may find this useful for understanding worst-case scenarios.",
    "key_takeaways": [
      "Theoretical improvement, limited practical impact",
      "Relevant only to federated learning researchers",
      "No new algorithms or empirical improvements"
    ],
    "relevance_scores": {
      "practical_applicability": 3,
      "timeliness": 5,
      "novelty": 6,
      "impact_potential": 4,
      "overall": 4
    },
    "potential_impacts": {
      "industry": "Minimal direct impact",
      "research": "Incremental contribution to FL theory",
      "open_source": "No implementation expected",
      "adoption_timeline": "not_applicable"
    },
    "topics": ["federated learning", "convergence", "theory"],
    "related_to": ["FedAvg", "non-IID data"]
  },
  "digest_worthy": false,
  "spotlight_candidate": false
}
```

## Related Skills

- [fetch-arxiv-papers](../../collection/fetch-arxiv-papers/SKILL.md) - Fetch papers for analysis
- [compose-executive-digest](../../action/compose-executive-digest/SKILL.md) - Include analysis in digest

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-02-01 | Added test cases and improved clarity |
| 1.0.0 | 2026-01-27 | Initial version |

## Test Cases

### Test Case 1: High-Impact Paper

**Input:**
```json
{
  "paper": {
    "arxiv_id": "2601.54321",
    "title": "FlashAttention-3: Faster Attention with Better Hardware Utilization",
    "authors": ["Tri Dao", "Daniel Fu"],
    "abstract": "We present FlashAttention-3, which achieves 2x speedup over FlashAttention-2 through improved memory access patterns and better GPU utilization. Our method reduces memory bandwidth bottlenecks and enables longer context windows with lower latency.",
    "categories": ["cs.LG", "cs.AI"],
    "pdf_url": "https://arxiv.org/pdf/2601.54321.pdf"
  },
  "analysis_depth": "deep"
}
```

**Expected Output:**
```json
{
  "analysis": {
    "arxiv_id": "2601.54321",
    "title": "FlashAttention-3: Faster Attention with Better Hardware Utilization",
    "authors": ["Tri Dao", "Daniel Fu"],
    "research_type": "new_method",
    "main_claim": "FlashAttention-3 achieves 2x speedup over FlashAttention-2 through improved memory access patterns",
    "key_innovation": "Better GPU memory bandwidth utilization and reduced overhead",
    "results_summary": "2x speedup, longer context windows, lower latency",
    "practitioner_summary": "FlashAttention-3 represents the next evolution in efficient attention mechanisms. For practitioners running LLM inference, this could mean serving twice as many requests with the same hardware, or supporting context windows twice as long. The improvements come from better understanding of GPU memory hierarchies, making this immediately applicable to any transformer-based model. However, adoption requires updating to the latest CUDA toolkit and may need model-specific tuning.",
    "key_takeaways": [
      "2x inference speedup for transformer attention layers",
      "Enables longer context windows without proportional memory increase",
      "Requires latest GPU drivers but no model architecture changes",
      "Particularly impactful for production LLM serving"
    ],
    "relevance_scores": {
      "practical_applicability": 10,
      "timeliness": 10,
      "novelty": 8,
      "impact_potential": 9,
      "overall": 9
    },
    "potential_impacts": {
      "industry": "Immediate cost reduction for LLM inference providers",
      "research": "New baseline for attention efficiency research",
      "open_source": "Implementation expected within weeks",
      "adoption_timeline": "immediate"
    },
    "topics": ["attention", "efficiency", "inference", "transformers"],
    "related_to": ["FlashAttention-2", "xFormers", "memory-efficient attention"]
  },
  "digest_worthy": true,
  "spotlight_candidate": true
}
```

### Test Case 2: Niche Research Paper

**Input:**
```json
{
  "paper": {
    "arxiv_id": "2601.99999",
    "title": "Improved Convergence Bounds for Federated Learning with Non-IID Data",
    "authors": ["Academic Researcher"],
    "abstract": "We provide tighter convergence bounds for federated averaging under non-IID data distributions. Our theoretical analysis shows that...",
    "categories": ["cs.LG"],
    "pdf_url": "https://arxiv.org/pdf/2601.99999.pdf"
  },
  "analysis_depth": "standard"
}
```

**Expected Output:**
```json
{
  "analysis": {
    "arxiv_id": "2601.99999",
    "title": "Improved Convergence Bounds for Federated Learning with Non-IID Data",
    "authors": ["Academic Researcher"],
    "research_type": "theoretical",
    "main_claim": "Tighter convergence bounds for federated learning",
    "key_innovation": "Improved theoretical analysis of non-IID scenarios",
    "results_summary": "Better mathematical bounds, limited empirical validation",
    "practitioner_summary": "This paper improves our theoretical understanding of federated learning convergence, specifically for scenarios where data across clients is not identically distributed. While the results are mathematically interesting, the practical implications are limited - the bounds are still conservative and don't directly translate to better algorithms. Practitioners working on federated learning may find this useful for understanding worst-case scenarios.",
    "key_takeaways": [
      "Theoretical improvement, limited practical impact",
      "Relevant only to federated learning researchers",
      "No new algorithms or empirical improvements"
    ],
    "relevance_scores": {
      "practical_applicability": 3,
      "timeliness": 5,
      "novelty": 6,
      "impact_potential": 4,
      "overall": 4
    },
    "potential_impacts": {
      "industry": "Minimal direct impact",
      "research": "Incremental contribution to FL theory",
      "open_source": "No implementation expected",
      "adoption_timeline": "not_applicable"
    },
    "topics": ["federated learning", "convergence", "theory"],
    "related_to": ["FedAvg", "non-IID data"]
  },
  "digest_worthy": false,
  "spotlight_candidate": false
}
```