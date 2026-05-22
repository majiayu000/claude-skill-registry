---
name: Summarization Engine
slug: summarization-engine
description: Generate accurate summaries of long documents and text collections
category: ai-ml
complexity: intermediate
version: "1.0.0"
author: "ID8Labs"
triggers:
  - "summarize document"
  - "text summarization"
  - "generate summary"
  - "document summary"
  - "condense text"
tags:
  - summarization
  - NLP
  - document-processing
  - text-generation
  - content
---

# Summarization Engine

The Summarization Engine skill guides you through building systems that condense long documents into concise, accurate summaries. From extractive approaches that select key sentences to abstractive methods that generate new text, this skill covers the full spectrum of summarization techniques.

Effective summarization requires understanding what information matters, maintaining accuracy while condensing, and adapting to different document types and summary requirements. This skill helps you choose the right approach and implement robust summarization pipelines.

Whether you're summarizing news articles, research papers, meeting transcripts, or legal documents, this skill ensures your summaries are accurate, relevant, and useful.

## Core Workflows

### Workflow 1: Choose Summarization Approach
1. **Analyze** requirements:
   - Summary length (ratio or fixed length)
   - Accuracy requirements (factual precision)
   - Style preferences (extractive vs abstractive)
   - Speed and scale constraints
2. **Compare** approaches:
   | Approach | Accuracy | Fluency | Speed | Best For |
   |----------|----------|---------|-------|----------|
   | Extractive | High | Variable | Fast | Legal, medical, precision |
   | Abstractive (small) | Medium | Good | Fast | General content |
   | Abstractive (LLM) | High | Excellent | Slow | Quality-critical |
   | Hybrid | High | Good | Medium | Balanced needs |
3. **Select** based on tradeoffs:
   - Extractive: When accuracy is critical
   - Abstractive: When fluency matters
   - Hybrid: When both matter
4. **Design** evaluation criteria

### Workflow 2: Implement Extractive Summarization
1. **Score** sentences:
   ```python
   from sklearn.feature_extraction.text import TfidfVectorizer
   import numpy as np

   def extractive_summarize(text, num_sentences=3):
       # Split into sentences
       sentences = sent_tokenize(text)

       # Score by TF-IDF importance
       vectorizer = TfidfVectorizer()
       tfidf_matrix = vectorizer.fit_transform(sentences)

       # Score each sentence by sum of TF-IDF scores
       scores = np.array(tfidf_matrix.sum(axis=1)).flatten()

       # Select top sentences maintaining order
       top_indices = np.argsort(scores)[-num_sentences:]
       top_indices = sorted(top_indices)  # Maintain original order

       summary_sentences = [sentences[i] for i in top_indices]
       return " ".join(summary_sentences)
   ```
2. **Add** additional scoring factors:
   - Position (first sentences often important)
   - Named entity density
   - Similarity to title/heading
3. **Remove** redundancy:
   - Skip sentences too similar to already selected
4. **Post-process** for coherence

### Workflow 3: Implement Abstractive Summarization
1. **Set up** summarization model:
   ```python
   from transformers import pipeline

   class AbstractiveSummarizer:
       def __init__(self, model="facebook/bart-large-cnn"):
           self.summarizer = pipeline("summarization", model=model)
           self.max_input_length = 1024  # Model-specific limit

       def summarize(self, text, max_length=150, min_length=50):
           # Handle long documents
           if len(text.split()) > self.max_input_length:
               return self.summarize_long(text, max_length, min_length)

           result = self.summarizer(
               text,
               max_length=max_length,
               min_length=min_length,
               do_sample=False
           )
           return result[0]["summary_text"]

       def summarize_long(self, text, max_length, min_length):
           # Chunk and summarize iteratively
           chunks = self.chunk_text(text)
           summaries = [self.summarize(chunk) for chunk in chunks]

           # Combine and re-summarize if needed
           combined = " ".join(summaries)
           if len(combined.split()) > max_length:
               return self.summarize(combined, max_length, min_length)
           return combined
   ```
2. **Handle** long documents with chunking
3. **Validate** factual accuracy
4. **Post-process** for formatting

## Quick Reference

| Action | Command/Trigger |
|--------|-----------------|
| Summarize text | "Summarize this document" |
| Choose approach | "Best summarization for [document type]" |
| Control length | "Summarize in [N] words/sentences" |
| Multi-document | "Summarize these documents together" |
| Evaluate summary | "Check summary quality" |
| Reduce hallucination | "Improve summary accuracy" |

## Best Practices

- **Preserve Key Information**: Summaries must capture what matters
  - Identify key entities, facts, and conclusions
  - Verify critical information is retained
  - Don't sacrifice accuracy for brevity

- **Maintain Factual Accuracy**: Abstractive summarization can hallucinate
  - Verify generated facts against source
  - Use extractive for high-stakes domains
  - Consider hybrid approaches

- **Handle Long Documents**: Most models have length limits
  - Chunk strategically (by section, paragraph)
  - Use hierarchical summarization
  - Preserve context across chunks

- **Match Style to Purpose**: Different uses need different summaries
  - Executive summary: Key conclusions first
  - Abstract: Balanced overview
  - Bullet points: Scannable key facts
  - Progressive disclosure: Multiple detail levels

- **Evaluate Properly**: ROUGE scores don't tell the whole story
  - Check factual accuracy manually
  - Assess coherence and readability
  - Compare against human summaries

- **Consider Multi-Document**: Often need to summarize multiple sources
  - Identify common themes and differences
  - Handle contradictions appropriately
  - Attribute information to sources

## Advanced Techniques

### LLM-Based Summarization
Use large language models for high-quality summaries:
```python
def llm_summarize(text, style="executive", max_words=150):
    style_instructions = {
        "executive": "Focus on key conclusions, decisions, and action items.",
        "technical": "Preserve technical details and methodology.",
        "narrative": "Maintain the story arc and key events.",
        "bullet": "Format as bullet points with key facts."
    }

    prompt = f"""Summarize the following text in approximately {max_words} words.
{style_instructions.get(style, "")}

Important:
- Only include information from the source text
- Maintain accuracy of facts, numbers, and names
- Preserve the most important information

Text to summarize:
{text}

Summary:"""

    return llm.complete(prompt, max_tokens=max_words * 2)
```

### Hierarchical Summarization
Summarize very long documents iteratively:
```python
def hierarchical_summarize(document, target_length=500):
    """
    Summarize long documents through progressive compression.
    """
    # Level 1: Split into sections
    sections = split_into_sections(document)

    # Level 2: Summarize each section
    section_summaries = []
    for section in sections:
        summary = summarize(section, max_length=200)
        section_summaries.append({
            "title": section.title,
            "summary": summary
        })

    # Level 3: Combine section summaries
    combined = "\n\n".join([
        f"{s['title']}: {s['summary']}"
        for s in section_summaries
    ])

    # Level 4: Final summary if still too long
    if len(combined.split()) > target_length:
        return summarize(combined, max_length=target_length)

    return combined
```

### Multi-Document Summarization
Synthesize information from multiple sources:
```python
def multi_document_summarize(documents, topic=None):
    """
    Summarize multiple documents into coherent summary.
    """
    # Step 1: Summarize each document
    doc_summaries = []
    for i, doc in enumerate(documents):
        summary = summarize(doc.text)
        doc_summaries.append({
            "source": doc.source,
            "summary": summary
        })

    # Step 2: Identify themes and differences
    prompt = f"""Given these summaries from different sources about {topic or "a topic"}:

{chr(10).join(f"Source {i+1} ({s['source']}): {s['summary']}" for i, s in enumerate(doc_summaries))}

Create a unified summary that:
1. Identifies common themes across sources
2. Notes any contradictions or different perspectives
3. Attributes key claims to their sources
4. Presents a balanced, comprehensive view

Unified summary:"""

    return llm.complete(prompt)
```

### Factual Consistency Checking
Verify summaries don't hallucinate:
```python
def check_factual_consistency(source, summary):
    """
    Verify summary facts against source document.
    """
    # Extract claims from summary
    claims = extract_claims(summary)

    # Check each claim against source
    results = []
    for claim in claims:
        prompt = f"""Does the source document support this claim?

Source: {source}

Claim: {claim}

Answer:
- SUPPORTED: The claim is directly supported by the source
- NOT SUPPORTED: The claim is not in the source
- CONTRADICTED: The source contradicts this claim

Provide answer and brief explanation."""

        result = llm.complete(prompt)
        results.append({
            "claim": claim,
            "status": parse_status(result),
            "explanation": result
        })

    return {
        "claims_checked": len(results),
        "supported": sum(1 for r in results if r["status"] == "SUPPORTED"),
        "not_supported": sum(1 for r in results if r["status"] == "NOT SUPPORTED"),
        "contradicted": sum(1 for r in results if r["status"] == "CONTRADICTED"),
        "details": results
    }
```

### Query-Focused Summarization
Generate summaries tailored to specific questions:
```python
def query_focused_summarize(document, query):
    """
    Summarize document with focus on answering specific question.
    """
    prompt = f"""Summarize the following document, focusing specifically on information relevant to this question:

Question: {query}

Document:
{document}

Provide a summary that:
1. Directly addresses the question
2. Includes relevant supporting details from the document
3. Notes if the document doesn't fully answer the question
4. Stays focused on query-relevant information

Summary:"""

    return llm.complete(prompt)
```

## Common Pitfalls to Avoid

- Trusting abstractive summaries without factual verification
- Not handling documents longer than model context limits
- Using ROUGE scores as the only evaluation metric
- Ignoring document structure when chunking
- Generating summaries that don't match user needs
- Not attributing information in multi-document summaries
- Over-compressing and losing critical information
- Assuming summaries are ready to use without human review
