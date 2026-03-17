---
name: reviewing-ai-papers
description: Analyze AI/ML technical content (papers, articles, blog posts) and extract actionable insights filtered through enterprise AI engineering lens. Use when user provides URL/document for AI/ML content analysis, asks to "review this paper", or mentions technical content in domains like RAG, embeddings, fine-tuning, prompt engineering, LLM deployment.
metadata:
  version: 0.1.0
---

# Reviewing AI Papers

When users request analysis of AI/ML technical content (papers, articles, blog posts), extract actionable insights filtered through an enterprise AI engineering lens and store valuable discoveries to memory for cross-session recall.

## Contextual Priorities

**Technical Architecture:**
- RAG systems (semantic/lexical search, hybrid retrieval)
- Vector database optimization and embedding strategies
- Model fine-tuning for specialized scientific domains
- Knowledge distillation for secure on-premise deployment

**Implementation & Operations:**
- Prompt engineering and in-context learning techniques
- Security and IP protection in AI systems
- Scientific accuracy and hallucination mitigation
- AWS integration (Bedrock/SageMaker)

**Enterprise & Adoption:**
- Enterprise deployment in regulated environments
- Building trust with scientific/legal stakeholders
- Internal customer success strategies
- Build vs. buy decision frameworks

## Analytical Standards

- **Maintain objectivity**: Extract factual insights without amplifying source hype
- **Challenge novelty claims**: Identify what practitioners already use as baselines. Distinguish "applies existing techniques" from "genuinely new methods"
- **Separate rigor from novelty**: Well-executed study of standard techniques ≠ methodological breakthrough
- **Confidence transparency**: Distinguish established facts, emerging trends, speculative claims
- **Contextual filtering**: Prioritize insights mapping to current challenges

## Analysis Structure

### For Substantive Content

**Article Assessment** (2-3 sentences)
- Core topic and primary claims
- Credibility: author expertise, evidence quality, methodology rigor

**Prioritized Insights**
- High Priority: Direct applications to active projects
- Medium Priority: Adjacent technologies worth monitoring
- Low Priority: Interesting but not immediately actionable

**Technical Evaluation**
- Distinguish novel methods from standard practice presented as innovation
- Flag implementation challenges, risks, resource requirements
- Note contradictions with established best practices

**Actionable Recommendations**
- Research deeper: Specific areas requiring investigation
- Evaluate for implementation: Techniques worth prototyping
- Share with teams: Which teams benefit from this content
- Monitor trends: Emerging areas to track

**Immediate Applications**
Map insights to current projects. Identify quick wins or POC opportunities.

### For Thin Content

- State limitations upfront
- Extract marginal insights if any
- Recommend alternatives if topic matters
- Keep brief

## Memory Integration

**Automatic storage triggers:**
- High-priority insights (directly applicable)
- Novel techniques worth prototyping
- Pattern recognitions across papers
- Contradictions to established practice

**Storage format:**
```python
remember(
    "[Source: {title or url}] {condensed insight}",
    "world",
    tags=["paper-insight", "{domain}", "{technique}"],
    conf=0.85  # higher for strong evidence
)
```

**Compression rule:**
- Full analysis → conversation (what user sees)
- Condensed insight → memory (searchable nugget with attribution)
- Store the actionable kernel, not the whole analysis

**Example:**

Analysis says: "Hybrid retrieval (BM25 + dense) shows 23% improvement over pure semantic search for scientific queries. Two-stage approach..."

Store as: `"[Source: arxiv.org/abs/2401.xxxxx] Hybrid BM25+dense retrieval: 23% lift over semantic-only for scientific corpora. Requires 10K+ domain examples for fine-tuning benefit."`

Tags: `["paper-insight", "rag", "hybrid-retrieval", "scientific-domain"]`

## Output Standards

- **Conciseness**: Actionable insights, not content restatement
- **Precision**: Distinguish demonstrates/suggests/claims/speculates
- **Relevance**: Connect to focus areas or state no connection
- **Adaptive depth**: Match length to content value

## Constraints

- No hype amplification
- No timelines unless requested
- No speculation beyond article
- Note contradictions explicitly
- State limitations on thin content
