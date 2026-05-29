---
name: "policy-qa"
version: "1.0.0"
owner: "Platform AI Team"
description: "Answer policy questions with strict citations. Refuses to answer without sources."
dependencies:
  - mcp: "postgres"       # pgvector for policy corpus
  - mcp: "python"         # retrieval and ranking
capabilities:
  - citations_required: true
  - code_execution: python
  - refuse_without_source: true
guardrails:
  - "NEVER answer without citing sources"
  - "If no relevant sources found, say 'I cannot find relevant policy guidance'"
  - "Include section references and document URLs in citations"
  - "Flag uncertainty: if confidence < 0.8, say 'I'm not certain...'"
  - "No speculation or inference beyond what's in documents"
inputs:
  - question: "Policy question from user"
  - top_k: "Number of sources to retrieve (default: 5)"
  - min_confidence: "Minimum confidence score (default: 0.8)"
workflow:
  - step: "Embed question using same model as policy corpus"
  - step: "Retrieve top_k similar chunks from pgvector"
  - step: "Rank by relevance score"
  - step: "If max score < min_confidence, refuse to answer"
  - step: "Generate answer citing specific sections and documents"
  - step: "Include all source URLs and section references"
  - step: "Log query, sources, answer in audit trail"
success_criteria:
  - "Answers include citations with section references"
  - "Refuses to answer when sources missing or low confidence"
  - "Citation precision ≥0.95 (citations actually support claims)"
  - "All interactions logged for audit"
---

# Policy Q&A Skill

## Purpose

Answer policy and SOP questions with strict source attribution. Refuses to answer without relevant sources. Designed for compliance-sensitive environments.

## Usage

```python
# Ask policy question
answer = policy_qa(
    question="What is the approval workflow for journal entries over $100K?",
    top_k=5,
    min_confidence=0.8
)
```

## Workflow

### 1. Embed Question

```python
from sentence_transformers import SentenceTransformer

def embed_question(question, model_name='sentence-transformers/all-MiniLM-L6-v2'):
    """Embed question using same model as policy corpus"""
    model = SentenceTransformer(model_name)
    embedding = model.encode(question)
    return embedding.tolist()
```

### 2. Retrieve from pgvector

```python
import psycopg2

def retrieve_policy_sources(question_embedding, top_k=5):
    """Retrieve similar policy chunks from pgvector"""

    conn = psycopg2.connect(os.environ['POSTGRES_URL'])
    cursor = conn.cursor()

    # Vector similarity search
    query = """
        SELECT
            id,
            text,
            document_name,
            section,
            page_number,
            url,
            1 - (embedding <=> %s::vector) AS similarity
        FROM policy_chunks
        WHERE 1 - (embedding <=> %s::vector) > 0.3  -- Minimum similarity threshold
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """

    cursor.execute(query, (question_embedding, question_embedding, question_embedding, top_k))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return [{
        'id': r[0],
        'text': r[1],
        'document_name': r[2],
        'section': r[3],
        'page_number': r[4],
        'url': r[5],
        'similarity': r[6],
    } for r in results]
```

### 3. Rank by Relevance

```python
def rank_sources(sources, question):
    """Re-rank sources by relevance using cross-encoder"""
    from sentence_transformers import CrossEncoder

    model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    # Score each source
    pairs = [[question, s['text']] for s in sources]
    scores = model.predict(pairs)

    # Add scores to sources
    for source, score in zip(sources, scores):
        source['relevance_score'] = float(score)

    # Sort by relevance
    sources.sort(key=lambda x: x['relevance_score'], reverse=True)

    return sources
```

### 4. Check Confidence Threshold

```python
def check_confidence(sources, min_confidence=0.8):
    """Check if top source meets confidence threshold"""

    if not sources:
        return False, "No relevant sources found"

    top_score = sources[0]['relevance_score']

    if top_score < min_confidence:
        return False, f"Low confidence ({top_score:.2f} < {min_confidence})"

    return True, None
```

### 5. Generate Answer with Citations

```python
def generate_answer_with_citations(question, sources):
    """Generate answer citing specific sources"""

    # Build context from top sources
    context = "\n\n".join([
        f"[{i+1}] {s['document_name']}, Section: {s['section']}, Page: {s['page_number']}\n{s['text']}"
        for i, s in enumerate(sources[:3])  # Use top 3 sources
    ])

    # Prompt for answer generation
    prompt = f"""
Answer the following question based ONLY on the provided policy documents.
You MUST cite your sources using [1], [2], [3] notation.

Question: {question}

Policy Documents:
{context}

Instructions:
- Answer the question using only information from the provided documents
- Cite sources inline using [1], [2], [3]
- If the documents don't contain the answer, say "I cannot find relevant policy guidance"
- Be specific about policy requirements, procedures, approvals
- Quote exact text when citing requirements

Answer:
"""

    # Generate answer (using LLM)
    answer = call_llm(prompt)

    # Verify citations are present
    if not any(f'[{i+1}]' in answer for i in range(len(sources[:3]))):
        return "I cannot provide an answer without proper citations."

    return answer

def call_llm(prompt):
    """Call LLM API (e.g., Claude, GPT, or local model)"""
    # Implementation depends on LLM choice
    pass
```

### 6. Format Response with Sources

```python
def format_response(answer, sources):
    """Format response with full source references"""

    response = answer + "\n\n---\n\n**Sources:**\n\n"

    for i, source in enumerate(sources[:3], start=1):
        response += f"[{i}] **{source['document_name']}**\n"
        response += f"   Section: {source['section']}\n"
        response += f"   Page: {source['page_number']}\n"
        response += f"   URL: {source['url']}\n"
        response += f"   Relevance: {source['relevance_score']:.2f}\n\n"

    return response
```

### 7. Audit Logging

```python
def log_policy_qa(user, question, sources, answer, refused=False):
    """Log policy Q&A for audit trail"""

    import psycopg2
    from datetime import datetime

    conn = psycopg2.connect(os.environ['POSTGRES_URL'])
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO policy_qa_audit_log (
            user_id, timestamp, question, sources, answer, refused, confidence_score
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        user,
        datetime.now(),
        question,
        json.dumps([s['id'] for s in sources]),
        answer if not refused else None,
        refused,
        sources[0]['relevance_score'] if sources else 0.0,
    ))

    conn.commit()
    cursor.close()
    conn.close()
```

## Full Workflow Example

```python
def policy_qa(question, top_k=5, min_confidence=0.8, user=None):
    """Answer policy question with strict citations"""

    # 1. Embed question
    question_embedding = embed_question(question)

    # 2. Retrieve sources
    sources = retrieve_policy_sources(question_embedding, top_k)

    # 3. Re-rank
    sources = rank_sources(sources, question)

    # 4. Check confidence
    passed, reason = check_confidence(sources, min_confidence)

    if not passed:
        response = f"I cannot answer this question. {reason}"
        log_policy_qa(user, question, sources, response, refused=True)
        return response

    # 5. Generate answer
    answer = generate_answer_with_citations(question, sources)

    # 6. Format with sources
    response = format_response(answer, sources)

    # 7. Audit log
    log_policy_qa(user, question, sources, answer, refused=False)

    return response
```

## Evaluation

Test citation precision:

```yaml
# tests/finance/policy-qa.yaml
suite: policy-qa
thresholds:
  citation_precision: 0.95
  refuses_without_source: true

cases:
  - id: ev-journal-approval
    prompt: "What is the approval workflow for journal entries over $100K?"
    expects:
      - has_citations: true
      - citation_count: [1, 2, 3]  # 1-3 citations
      - cites_correct_policy: true
      - includes_source_urls: true

  - id: ev-low-confidence-refusal
    prompt: "What is the company's policy on flying cars?"
    expects:
      - refuses_to_answer: true
      - mentions_no_sources: true
```

## Policy Corpus Ingestion

Ingest policy documents into pgvector:

```python
def ingest_policy_document(pdf_path, document_name, url):
    """Ingest policy PDF into pgvector"""

    # 1. Extract text from PDF
    from pypdf import PdfReader

    reader = PdfReader(pdf_path)
    sections = []

    for page_num, page in enumerate(reader.pages, start=1):
        text = page.extract_text()

        # Chunk by section headings or fixed size
        chunks = chunk_text(text, chunk_size=500, overlap=100)

        for chunk in chunks:
            sections.append({
                'text': chunk,
                'document_name': document_name,
                'page_number': page_num,
                'section': detect_section(chunk),  # Extract section heading
                'url': url,
            })

    # 2. Embed all chunks
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    texts = [s['text'] for s in sections]
    embeddings = model.encode(texts)

    # 3. Store in pgvector
    conn = psycopg2.connect(os.environ['POSTGRES_URL'])
    cursor = conn.cursor()

    for section, embedding in zip(sections, embeddings):
        cursor.execute("""
            INSERT INTO policy_chunks (
                text, document_name, section, page_number, url, embedding
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            section['text'],
            section['document_name'],
            section['section'],
            section['page_number'],
            section['url'],
            embedding.tolist(),
        ))

    conn.commit()
    cursor.close()
    conn.close()
```

## Schema

```sql
CREATE TABLE policy_chunks (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    document_name VARCHAR(255) NOT NULL,
    section VARCHAR(255),
    page_number INTEGER,
    url TEXT,
    embedding vector(384),  -- MiniLM dimension
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ON policy_chunks USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX ON policy_chunks (document_name, section);

CREATE TABLE policy_qa_audit_log (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    question TEXT NOT NULL,
    sources JSONB,  -- Array of source IDs
    answer TEXT,
    refused BOOLEAN NOT NULL,
    confidence_score FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX ON policy_qa_audit_log (user_id, timestamp);
CREATE INDEX ON policy_qa_audit_log (refused);
```

## Guardrails

### Never Answer Without Sources

```python
if not sources or sources[0]['relevance_score'] < min_confidence:
    return "I cannot find relevant policy guidance on this topic. Please consult the full policy library or contact Compliance."
```

### Flag Uncertainty

```python
if sources[0]['relevance_score'] < 0.9:
    answer = f"⚠️ **Moderate confidence** ({sources[0]['relevance_score']:.2f})\n\n{answer}"
```

### No Speculation

Prompt includes:
```
- Do NOT infer or speculate beyond what's explicitly stated
- If the policy doesn't address this specific case, say so
- Quote exact text when citing requirements
```

## References

- RAG Best Practices: https://www.anthropic.com/research/contextual-retrieval
- Citation Quality: https://arxiv.org/abs/2305.14627
- pgvector: https://github.com/pgvector/pgvector
