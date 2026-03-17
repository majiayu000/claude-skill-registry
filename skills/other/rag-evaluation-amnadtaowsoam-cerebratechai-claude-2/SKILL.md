---
name: RAG Evaluation
description: Comprehensive guide to evaluating Retrieval-Augmented Generation systems including retrieval metrics, generation quality, faithfulness, and end-to-end evaluation frameworks
---

# RAG Evaluation

## What is RAG Evaluation?

**Definition:** Measuring quality of both retrieval and generation components in RAG systems.

### Components
```
RAG System = Retrieval + Generation

Retrieval: Query → Relevant documents
Generation: Documents + Query → Answer

Both need evaluation!
```

### Evaluation Levels
```
1. Component-level: Retrieval quality, generation quality
2. End-to-end: Overall answer quality
3. User-level: User satisfaction, task success
```

---

## Why RAG Evaluation Matters

### RAG Quality Varies Widely

**Example:**
```
Query: "What is the capital of France?"

Bad RAG:
- Retrieves: Document about French cuisine
- Generates: "France is known for its wine" (irrelevant)

Good RAG:
- Retrieves: Document about Paris
- Generates: "The capital of France is Paris" (correct)
```

### Retrieval Errors → Wrong Context → Bad Answers

**Error Cascade:**
```
Poor retrieval (irrelevant docs)
→ Wrong context for LLM
→ LLM generates answer from wrong info
→ Hallucination or incorrect answer
```

### Need Metrics to Improve Systematically

**Without Metrics:**
```
"This answer seems wrong" → Unclear what to fix
```

**With Metrics:**
```
Context Precision: 0.3 (low) → Improve retrieval
Faithfulness: 0.6 (low) → Improve prompt to reduce hallucination
```

---

## RAG Components to Evaluate

### 1. Retrieval: Are Relevant Docs Retrieved?

**Metrics:**
- Precision@k
- Recall@k
- MRR (Mean Reciprocal Rank)
- NDCG

### 2. Context: Is Context Sufficient for Answer?

**Metrics:**
- Context relevance
- Context precision
- Context recall

### 3. Generation: Is Answer Correct, Relevant, Safe?

**Metrics:**
- Faithfulness (no hallucination)
- Answer relevance
- Correctness
- Completeness
- Safety

---

## Retrieval Evaluation Metrics

### Precision@k: % of Top-k Results Relevant

**Formula:**
```
Precision@k = (# relevant docs in top-k) / k
```

**Example:**
```
Query: "Python list methods"
Top 5 results:
1. Python list.append() ✓ (relevant)
2. Python list.extend() ✓ (relevant)
3. Java ArrayList ✗ (not relevant)
4. Python list.pop() ✓ (relevant)
5. Python dictionaries ✗ (not relevant)

Precision@5 = 3/5 = 0.6
```

### Recall@k: % of Relevant Docs in Top-k

**Formula:**
```
Recall@k = (# relevant docs in top-k) / (total # relevant docs)
```

**Example:**
```
Total relevant docs: 10
Relevant docs in top-5: 3

Recall@5 = 3/10 = 0.3
```

### MRR (Mean Reciprocal Rank): Position of First Relevant Doc

**Formula:**
```
RR = 1 / (rank of first relevant doc)
MRR = average RR across queries
```

**Example:**
```
Query 1: First relevant at position 1 → RR = 1/1 = 1.0
Query 2: First relevant at position 3 → RR = 1/3 = 0.33
Query 3: First relevant at position 2 → RR = 1/2 = 0.5

MRR = (1.0 + 0.33 + 0.5) / 3 = 0.61
```

### NDCG (Normalized Discounted Cumulative Gain)

**Purpose:** Considers both relevance and position

**Formula:**
```
DCG@k = Σ (relevance_i / log2(i+1))
NDCG@k = DCG@k / IDCG@k (normalized)
```

**Example:**
```
Top 3 results with relevance scores (0-3):
Position 1: relevance = 3
Position 2: relevance = 2
Position 3: relevance = 1

DCG@3 = 3/log2(2) + 2/log2(3) + 1/log2(4)
      = 3/1 + 2/1.58 + 1/2
      = 3 + 1.26 + 0.5 = 4.76
```

### Context Relevance Score

**LLM-as-Judge:**
```python
def evaluate_context_relevance(query, context):
    prompt = f"""
    Query: {query}
    Context: {context}
    
    Rate the relevance of the context to the query on a scale of 1-5:
    1 = Not relevant at all
    5 = Highly relevant
    
    Score:
    """
    
    score = llm.generate(prompt)
    return int(score)
```

---

## Generation Evaluation Metrics

### Faithfulness: Answer Grounded in Context (No Hallucination)

**Definition:** All claims in answer are supported by context

**Example:**
```
Context: "Paris is the capital of France. It has a population of 2.1 million."
Question: "What is the capital of France?"

Faithful answer: "Paris is the capital of France."
Unfaithful answer: "Paris is the capital of France with 10 million people." (hallucination)
```

### Answer Relevance: Answer Addresses the Question

**Definition:** Answer is on-topic and addresses what was asked

**Example:**
```
Question: "What is the capital of France?"

Relevant answer: "The capital of France is Paris."
Irrelevant answer: "France is a country in Europe." (true but doesn't answer)
```

### Correctness: Answer is Factually Correct

**Definition:** Answer matches ground truth

**Example:**
```
Question: "What is 2+2?"
Ground truth: "4"

Correct answer: "4"
Incorrect answer: "5"
```

### Completeness: Answer Covers All Aspects

**Definition:** Answer addresses all parts of question

**Example:**
```
Question: "What are the capital and population of France?"

Complete answer: "The capital of France is Paris, with a population of about 67 million."
Incomplete answer: "The capital is Paris." (missing population)
```

---

## Faithfulness Evaluation

### Method 1: LLM-as-Judge (Does Answer Match Context?)

**Prompt:**
```python
def evaluate_faithfulness(context, answer):
    prompt = f"""
    Context: {context}
    Answer: {answer}
    
    Is the answer fully supported by the context? 
    Check if all claims in the answer can be verified from the context.
    
    Respond with:
    - "Yes" if all claims are supported
    - "No" if any claim is not supported or contradicts the context
    - Explain your reasoning
    
    Verdict:
    """
    
    response = llm.generate(prompt)
    return "Yes" in response
```

### Method 2: NLI Model (Entailment Check)

**Natural Language Inference:**
```python
from transformers import pipeline

nli = pipeline("text-classification", model="roberta-large-mnli")

def check_faithfulness(context, answer):
    # Check if context entails answer
    result = nli(f"{context} [SEP] {answer}")
    
    # result: {"label": "ENTAILMENT", "score": 0.95}
    return result["label"] == "ENTAILMENT"
```

### Method 3: Citation Checking (Are Claims Cited?)

**Approach:**
```
1. Extract claims from answer
2. For each claim, check if it appears in context
3. Calculate % of claims with citations
```

**Example:**
```python
def check_citations(context, answer):
    # Extract sentences from answer
    claims = answer.split('.')
    
    cited_claims = 0
    for claim in claims:
        if claim.strip() in context:
            cited_claims += 1
    
    citation_rate = cited_claims / len(claims)
    return citation_rate
```

---

## Answer Relevance Evaluation

### LLM-as-Judge: "Does Answer Address Question?"

**Prompt:**
```python
def evaluate_relevance(question, answer):
    prompt = f"""
    Question: {question}
    Answer: {answer}
    
    Does the answer directly address the question?
    
    Rate on scale 1-5:
    1 = Completely irrelevant
    5 = Perfectly addresses the question
    
    Score:
    """
    
    score = llm.generate(prompt)
    return int(score)
```

### Semantic Similarity (Answer vs Expected Answer)

**Embedding-Based:**
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(answer, expected_answer):
    # Encode both answers
    emb1 = model.encode(answer)
    emb2 = model.encode(expected_answer)
    
    # Cosine similarity
    similarity = cosine_similarity([emb1], [emb2])[0][0]
    return similarity
```

### User Feedback (Thumbs Up/Down)

**Implicit Signal:**
```python
# Track user feedback
feedback = {
    "question": "What is the capital of France?",
    "answer": "Paris is the capital of France.",
    "user_feedback": "thumbs_up",  # or "thumbs_down"
    "timestamp": "2024-01-15T10:00:00Z"
}

# Aggregate
thumbs_up_rate = thumbs_up / (thumbs_up + thumbs_down)
```

---

## Correctness Evaluation

### Ground Truth Comparison (If Available)

**Exact Match:**
```python
def exact_match(answer, ground_truth):
    return answer.strip().lower() == ground_truth.strip().lower()
```

**F1 Score (Token Overlap):**
```python
def f1_score(answer, ground_truth):
    answer_tokens = set(answer.lower().split())
    gt_tokens = set(ground_truth.lower().split())
    
    if len(answer_tokens) == 0 or len(gt_tokens) == 0:
        return 0
    
    common = answer_tokens & gt_tokens
    precision = len(common) / len(answer_tokens)
    recall = len(common) / len(gt_tokens)
    
    if precision + recall == 0:
        return 0
    
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1
```

### LLM-as-Judge with Rubric

**Prompt:**
```python
def evaluate_correctness(question, answer, ground_truth):
    prompt = f"""
    Question: {question}
    Expected Answer: {ground_truth}
    Actual Answer: {answer}
    
    Is the actual answer correct compared to the expected answer?
    Consider:
    - Factual accuracy
    - Completeness
    - Semantic equivalence (different wording is OK)
    
    Rate on scale 1-5:
    1 = Completely incorrect
    5 = Perfectly correct
    
    Score:
    """
    
    score = llm.generate(prompt)
    return int(score)
```

### Human Evaluation (Gold Standard)

**Process:**
```
1. Sample answers (e.g., 100 random)
2. Human annotators rate correctness (1-5)
3. Calculate inter-annotator agreement
4. Use as gold standard
5. Validate automated metrics against human scores
```

---

## RAG-Specific Metrics

### Context Precision: Relevant Chunks in Context

**Definition:** % of retrieved chunks that are relevant

**Formula:**
```
Context Precision = (# relevant chunks) / (# total chunks retrieved)
```

**Example:**
```
Retrieved 5 chunks:
- Chunk 1: Relevant ✓
- Chunk 2: Relevant ✓
- Chunk 3: Not relevant ✗
- Chunk 4: Relevant ✓
- Chunk 5: Not relevant ✗

Context Precision = 3/5 = 0.6
```

### Context Recall: All Needed Info Retrieved

**Definition:** % of needed information that was retrieved

**Formula:**
```
Context Recall = (# needed facts retrieved) / (# total needed facts)
```

**Example:**
```
Question: "What are the capital and population of France?"
Needed facts: [capital, population]

Retrieved context contains:
- Capital: Yes ✓
- Population: No ✗

Context Recall = 1/2 = 0.5
```

### Context Relevance: Context Relevance to Question

**LLM-as-Judge:**
```python
def context_relevance(question, context):
    prompt = f"""
    Question: {question}
    Context: {context}
    
    How relevant is the context to answering the question?
    
    Rate 1-5:
    1 = Not relevant
    5 = Highly relevant
    
    Score:
    """
    
    score = llm.generate(prompt)
    return int(score) / 5  # Normalize to 0-1
```

### Answer Faithfulness: No Hallucinations

See "Faithfulness Evaluation" section above

### Answer Relevance: On-Topic Answer

See "Answer Relevance Evaluation" section above

---

## Creating Evaluation Dataset

### Question-Answer Pairs (Ground Truth)

**Structure:**
```json
{
  "question": "What is the capital of France?",
  "answer": "Paris",
  "category": "geography",
  "difficulty": "easy"
}
```

### Question-Context-Answer Triples

**Structure:**
```json
{
  "question": "What is the capital of France?",
  "context": "Paris is the capital and largest city of France. It has a population of 2.1 million.",
  "answer": "Paris is the capital of France.",
  "relevant_chunks": ["Paris is the capital and largest city of France."]
}
```

### Diverse Questions (Simple, Complex, Multi-Hop)

**Simple:**
```
"What is the capital of France?" → Single fact
```

**Complex:**
```
"Compare the populations of Paris and London." → Multiple facts + reasoning
```

**Multi-Hop:**
```
"What is the population of the capital of France?" → Requires 2 steps:
1. Find capital of France (Paris)
2. Find population of Paris
```

### Edge Cases (Ambiguous, No Answer)

**Ambiguous:**
```
"What is the best programming language?" → Subjective, no single answer
```

**No Answer:**
```
"What is the capital of Atlantis?" → No valid answer (fictional place)
```

**Unanswerable from Context:**
```
Context: "Paris is a city in France."
Question: "What is the population of Paris?"
Answer: "Cannot be determined from the given context."
```

---

## Evaluation Frameworks

### RAGAS (Popular Framework)

**Install:**
```bash
pip install ragas
```

**Usage:**
```python
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# Prepare dataset
dataset = {
    "question": ["What is the capital of France?"],
    "answer": ["Paris is the capital of France."],
    "contexts": [["Paris is the capital of France. It has 2.1M people."]],
    "ground_truth": ["Paris"]
}

# Evaluate
result = evaluate(
    dataset,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ]
)

print(result)
# {
#   "faithfulness": 0.95,
#   "answer_relevancy": 0.98,
#   "context_precision": 1.0,
#   "context_recall": 1.0
# }
```

### TruLens

**Features:**
- Real-time evaluation
- Feedback functions
- Dashboard

**Usage:**
```python
from trulens_eval import TruChain, Feedback, Tru

# Define feedback functions
f_groundedness = Feedback(groundedness_measure).on_output()
f_answer_relevance = Feedback(relevance_measure).on_input_output()

# Wrap your RAG chain
tru_recorder = TruChain(
    rag_chain,
    app_id="my_rag_app",
    feedbacks=[f_groundedness, f_answer_relevance]
)

# Use as normal
with tru_recorder:
    answer = rag_chain.run("What is the capital of France?")

# View dashboard
tru = Tru()
tru.run_dashboard()
```

### DeepEval

**Features:**
- Multiple metrics
- LLM-as-judge
- Custom metrics

**Usage:**
```python
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric

# Define test case
test_case = {
    "input": "What is the capital of France?",
    "actual_output": "Paris is the capital of France.",
    "expected_output": "Paris",
    "context": ["Paris is the capital of France."]
}

# Evaluate
metrics = [
    AnswerRelevancyMetric(),
    FaithfulnessMetric()
]

result = evaluate(test_case, metrics)
```

### Langfuse

**Features:**
- Observability
- Tracing
- Evaluation
- Analytics

### Custom Evaluation Scripts

**Example:**
```python
def evaluate_rag(questions, answers, contexts, ground_truths):
    results = []
    
    for q, a, c, gt in zip(questions, answers, contexts, ground_truths):
        result = {
            "question": q,
            "answer": a,
            "faithfulness": evaluate_faithfulness(c, a),
            "relevance": evaluate_relevance(q, a),
            "correctness": f1_score(a, gt),
            "context_precision": calculate_context_precision(q, c)
        }
        results.append(result)
    
    # Aggregate
    avg_faithfulness = sum(r["faithfulness"] for r in results) / len(results)
    avg_relevance = sum(r["relevance"] for r in results) / len(results)
    
    return {
        "avg_faithfulness": avg_faithfulness,
        "avg_relevance": avg_relevance,
        "results": results
    }
```

---

## RAGAS Metrics

### Context Precision

**Definition:** Measures if all retrieved contexts are relevant

**Calculation:**
```
For each context chunk:
  Is it relevant to answering the question?

Context Precision = (# relevant chunks) / (# total chunks)
```

### Context Recall

**Definition:** Measures if all needed information was retrieved

**Calculation:**
```
For each fact in ground truth:
  Is it present in retrieved context?

Context Recall = (# facts found) / (# total facts needed)
```

### Faithfulness

**Definition:** Measures if answer is grounded in context

**Calculation:**
```
For each claim in answer:
  Can it be inferred from context?

Faithfulness = (# supported claims) / (# total claims)
```

### Answer Relevance

**Definition:** Measures if answer addresses the question

**Calculation:**
```
Generate questions from answer
Compare to original question
Similarity score
```

### Answer Semantic Similarity

**Definition:** Semantic similarity between answer and ground truth

**Calculation:**
```
Embedding similarity (cosine)
```

### Answer Correctness

**Definition:** Combination of semantic similarity and factual correctness

**Calculation:**
```
Weighted average of:
- Semantic similarity (50%)
- Factual overlap (50%)
```

---

## LLM-as-Judge Patterns

### Use GPT-4 or Claude to Grade Answers

**Example:**
```python
import openai

def llm_judge(question, answer, context):
    prompt = f"""
    You are evaluating a RAG system's answer.
    
    Question: {question}
    Context: {context}
    Answer: {answer}
    
    Evaluate on these criteria (1-5 scale):
    1. Faithfulness: Is answer supported by context?
    2. Relevance: Does answer address the question?
    3. Completeness: Does answer cover all aspects?
    
    Provide scores and brief reasoning.
    
    Format:
    Faithfulness: [score] - [reasoning]
    Relevance: [score] - [reasoning]
    Completeness: [score] - [reasoning]
    Overall: [average score]
    """
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content
```

### Provide Rubric (1-5 Scale)

**Rubric:**
```
Faithfulness:
5 = All claims fully supported by context
4 = Most claims supported, minor unsupported details
3 = Some claims supported, some not
2 = Few claims supported
1 = No claims supported (hallucination)

Relevance:
5 = Perfectly addresses question
4 = Addresses question with minor irrelevant details
3 = Partially addresses question
2 = Barely addresses question
1 = Completely irrelevant
```

### Check Faithfulness, Relevance, Quality

See examples above

### Aggregate Scores

**Aggregation:**
```python
def aggregate_scores(evaluations):
    avg_faithfulness = sum(e["faithfulness"] for e in evaluations) / len(evaluations)
    avg_relevance = sum(e["relevance"] for e in evaluations) / len(evaluations)
    avg_completeness = sum(e["completeness"] for e in evaluations) / len(evaluations)
    
    overall = (avg_faithfulness + avg_relevance + avg_completeness) / 3
    
    return {
        "faithfulness": avg_faithfulness,
        "relevance": avg_relevance,
        "completeness": avg_completeness,
        "overall": overall
    }
```

---

## Human Evaluation

### Gold Standard but Expensive

**Cost:**
```
100 evaluations × 5 minutes each = 500 minutes = 8.3 hours
At $20/hour = $166

vs LLM-as-judge:
100 evaluations × $0.01 each = $1
```

### Use for Spot Checks

**Strategy:**
```
1. Evaluate 1000 examples with LLM-judge
2. Sample 100 for human evaluation
3. Compare human vs LLM scores
4. Validate LLM-judge is reliable
```

### Validate LLM-Judge Correlation

**Correlation:**
```python
from scipy.stats import pearsonr

human_scores = [4, 5, 3, 4, 2, ...]
llm_scores = [4.2, 4.8, 3.1, 4.5, 2.3, ...]

correlation, p_value = pearsonr(human_scores, llm_scores)
print(f"Correlation: {correlation:.2f}")  # Target: >0.7
```

### Annotation Guidelines

**Example:**
```markdown
# RAG Answer Evaluation Guidelines

## Faithfulness (1-5)
- Check if each claim in answer is supported by context
- 5 = All claims supported
- 1 = No claims supported (hallucination)

## Relevance (1-5)
- Does answer address the question?
- 5 = Perfectly addresses question
- 1 = Completely irrelevant

## Examples:
[Provide 5-10 examples with scores and explanations]
```

---

## A/B Testing RAG Systems

### Variant A vs Variant B

**Setup:**
```
Variant A: Current RAG system (baseline)
Variant B: New RAG system (improved retrieval)

Test: Same 100 questions
```

### Same Questions, Different Systems

**Process:**
```
For each question:
  - Run through Variant A
  - Run through Variant B
  - Evaluate both answers
  - Compare metrics
```

### Measure Metrics for Both

**Metrics:**
```python
results_a = evaluate_rag(questions, answers_a, contexts_a, ground_truths)
results_b = evaluate_rag(questions, answers_b, contexts_b, ground_truths)

comparison = {
    "variant_a": {
        "faithfulness": results_a["avg_faithfulness"],
        "relevance": results_a["avg_relevance"]
    },
    "variant_b": {
        "faithfulness": results_b["avg_faithfulness"],
        "relevance": results_b["avg_relevance"]
    },
    "improvement": {
        "faithfulness": results_b["avg_faithfulness"] - results_a["avg_faithfulness"],
        "relevance": results_b["avg_relevance"] - results_a["avg_relevance"]
    }
}
```

### Statistical Significance

**T-Test:**
```python
from scipy.stats import ttest_rel

faithfulness_a = [r["faithfulness"] for r in results_a]
faithfulness_b = [r["faithfulness"] for r in results_b]

t_stat, p_value = ttest_rel(faithfulness_a, faithfulness_b)

if p_value < 0.05:
    print("Statistically significant improvement!")
else:
    print("No significant difference")
```

---

## Retrieval Optimization

### Tune Chunk Size

**Experiment:**
```
Chunk sizes: 256, 512, 1024, 2048 tokens
Measure: Context precision, context recall
Find optimal chunk size
```

### Tune Number of Chunks (Top-k)

**Experiment:**
```
Top-k: 1, 3, 5, 10, 20
Measure: Context recall (more chunks = higher recall)
         Context precision (more chunks = lower precision)
Find optimal k (balance recall and precision)
```

### Improve Embeddings (Fine-Tuning)

**Approach:**
```
1. Collect query-document pairs
2. Fine-tune embedding model
3. Evaluate retrieval quality
4. Deploy if improved
```

### Hybrid Search (Keyword + Semantic)

**Combination:**
```
BM25 (keyword search) + Vector search (semantic)
Combine scores (e.g., 0.5 * BM25 + 0.5 * Vector)
```

### Re-Ranking

**Process:**
```
1. Retrieve top-100 with fast retrieval (vector search)
2. Re-rank with slow but accurate model (cross-encoder)
3. Return top-5
```

---

## Generation Optimization

### Prompt Engineering

**Improve Prompt:**
```
Bad prompt:
"Answer the question based on the context."

Good prompt:
"Answer the question using only information from the context. 
If the answer is not in the context, say 'I don't know.'
Be concise and accurate."
```

### Model Selection (GPT-4 vs Claude)

**Comparison:**
```
Test both models on same dataset
Measure: Faithfulness, relevance, cost, latency
Choose best for your use case
```

### Temperature Tuning

**Experiment:**
```
Temperature: 0.0, 0.3, 0.7, 1.0
Measure: Faithfulness (lower temp = more faithful)
         Creativity (higher temp = more creative)
```

### System Prompts

**Example:**
```
System: "You are a helpful assistant that answers questions based on provided context. 
Always cite the context when making claims. 
If the answer is not in the context, say so."
```

---

## Continuous Evaluation

### Log All Queries + Answers

**Logging:**
```python
log_entry = {
    "timestamp": "2024-01-15T10:00:00Z",
    "question": "What is the capital of France?",
    "answer": "Paris is the capital of France.",
    "contexts": ["Paris is the capital..."],
    "latency_ms": 250,
    "user_id": "user123"
}

# Store in database or log file
db.logs.insert(log_entry)
```

### Sample for Evaluation

**Sampling:**
```python
# Sample 1% of queries for evaluation
sample = db.logs.aggregate([
    {"$sample": {"size": 100}}  # Random sample of 100
])

# Evaluate sample
evaluate_rag(sample)
```

### Track Metrics Over Time

**Dashboard:**
```
Faithfulness over time:
Jan: 0.85
Feb: 0.87 ↑
Mar: 0.82 ↓ (regression!)
Apr: 0.90 ↑
```

### Regression Detection

**Alert:**
```python
if current_faithfulness < baseline_faithfulness - 0.05:
    send_alert("Faithfulness dropped by 5%!")
```

---

## Real-World RAG Evaluation

### Customer Support Chatbot

**Metrics:**
- Faithfulness (no hallucination)
- Answer relevance
- Resolution rate (did user's issue get resolved?)
- User satisfaction (thumbs up/down)

### Technical Documentation Q&A

**Metrics:**
- Correctness (accurate technical info)
- Completeness (covers all aspects)
- Code example quality (if applicable)

### Legal Document Search

**Metrics:**
- Precision (only relevant cases)
- Recall (all relevant cases found)
- Citation accuracy (correct case references)

---

## Implementation

### RAGAS Evaluation Script

See "RAGAS" section above

### Custom Metrics

```python
def custom_rag_eval(question, answer, context, ground_truth):
    return {
        "faithfulness": evaluate_faithfulness(context, answer),
        "relevance": evaluate_relevance(question, answer),
        "correctness": f1_score(answer, ground_truth),
        "context_precision": calculate_context_precision(question, context),
        "latency": measure_latency()
    }
```

### LLM-as-Judge Prompts

See "LLM-as-Judge Patterns" section above

---

## Summary

### Quick Reference

**RAG Evaluation:** Measure retrieval + generation quality

**Components:**
- Retrieval: Precision@k, Recall@k, MRR, NDCG
- Context: Precision, recall, relevance
- Generation: Faithfulness, relevance, correctness

**Key Metrics:**
- Faithfulness: No hallucination
- Answer relevance: On-topic
- Context precision: Relevant chunks
- Context recall: All needed info

**Frameworks:**
- RAGAS (popular)
- TruLens (real-time)
- DeepEval (LLM-judge)
- Custom scripts

**Evaluation Methods:**
- LLM-as-judge (GPT-4, Claude)
- NLI models (entailment)
- Embedding similarity
- Human evaluation (gold standard)

**Optimization:**
- Retrieval: Chunk size, top-k, embeddings, hybrid search
- Generation: Prompts, model, temperature

**Continuous:**
- Log queries
- Sample for evaluation
- Track metrics
- Detect regressions
