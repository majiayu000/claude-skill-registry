---
name: Ground Truth Management
description: Comprehensive guide to creating, managing, and maintaining ground truth datasets for AI evaluation including annotation, quality control, and versioning
---

# Ground Truth Management

## What is Ground Truth?

**Definition:** Correct answers for evaluation - human-verified data that serves as the gold standard for measuring AI performance.

### Example
```
Question: "What is the capital of France?"
Ground Truth: "Paris"

AI Answer: "Paris" → Correct ✓
AI Answer: "Lyon" → Incorrect ✗
```

---

## Why Ground Truth Matters

### Measure Accuracy Objectively
```
Without ground truth: "This answer seems good" (subjective)
With ground truth: "Accuracy: 85%" (objective)
```

### Train and Validate Models
```
Training: Learn from ground truth examples
Validation: Measure performance on ground truth test set
```

### Regression Testing
```
Before change: Accuracy 90%
After change: Accuracy 85%
→ Regression detected!
```

### Benchmarking
```
Model A: 90% accuracy on ground truth
Model B: 85% accuracy on ground truth
→ Model A is better
```

---

## Types of Ground Truth

### Exact Match: Single Correct Answer
```json
{
  "question": "What is 2+2?",
  "answer": "4"
}
```

### Multiple Acceptable Answers
```json
{
  "question": "What is the capital of France?",
  "acceptable_answers": ["Paris", "paris", "PARIS", "The capital is Paris"]
}
```

### Rubric-Based: Quality Scale
```json
{
  "question": "Summarize this article",
  "rubric": {
    "1": "Poor summary, missing key points",
    "3": "Adequate summary, covers main points",
    "5": "Excellent summary, concise and comprehensive"
  }
}
```

### Human Preference: Comparison Rankings
```json
{
  "question": "Which answer is better?",
  "answer_a": "Paris is the capital of France.",
  "answer_b": "The capital of France is Paris, a city of 2.1 million people.",
  "preference": "B",
  "reasoning": "More informative"
}
```

---

## Creating Ground Truth

### Manual Annotation (Humans Label)
```
Process:
1. Collect examples (questions, documents, images)
2. Human annotators label each
3. Quality control (review annotations)
4. Store in dataset
```

### Expert Review (For Specialized Domains)
```
Medical: Doctors annotate
Legal: Lawyers annotate
Technical: Engineers annotate

Higher quality but more expensive
```

### Crowdsourcing (Amazon MTurk)
```
Pros:
- Fast (many workers)
- Cheap ($0.10-1.00 per annotation)

Cons:
- Variable quality
- Need quality control
```

### Synthetic Generation (For Some Tasks)
```
LLM-generated questions + answers
Careful validation needed
Good for scale, risky for quality
Use for augmentation, not sole source
```

---

## Ground Truth Dataset Structure

### Input (Question, Document, Image)
```json
{
  "input": {
    "type": "question",
    "text": "What is the capital of France?"
  }
}
```

### Expected Output (Answer, Label, Summary)
```json
{
  "expected_output": {
    "type": "answer",
    "text": "Paris",
    "acceptable_variants": ["paris", "PARIS"]
  }
}
```

### Metadata (Difficulty, Category, Source)
```json
{
  "metadata": {
    "difficulty": "easy",
    "category": "geography",
    "source": "wikipedia",
    "language": "en"
  }
}
```

### Annotation Info (Who, When, Confidence)
```json
{
  "annotation": {
    "annotator_id": "annotator_123",
    "timestamp": "2024-01-15T10:00:00Z",
    "confidence": 0.95,
    "time_spent_seconds": 30
  }
}
```

**Complete Example:**
```json
{
  "id": "example_001",
  "input": {
    "type": "question",
    "text": "What is the capital of France?"
  },
  "expected_output": {
    "type": "answer",
    "text": "Paris",
    "acceptable_variants": ["paris", "PARIS", "The capital is Paris"]
  },
  "metadata": {
    "difficulty": "easy",
    "category": "geography",
    "source": "wikipedia",
    "language": "en"
  },
  "annotation": {
    "annotator_id": "annotator_123",
    "timestamp": "2024-01-15T10:00:00Z",
    "confidence": 0.95
  }
}
```

---

## Annotation Guidelines

### Clear Instructions
```markdown
# Annotation Guidelines

## Task
Label whether the answer is correct.

## Instructions
1. Read the question carefully
2. Read the answer
3. Determine if answer is factually correct
4. Mark as "Correct" or "Incorrect"

## Examples
Question: "What is 2+2?"
Answer: "4"
Label: Correct

Question: "What is 2+2?"
Answer: "5"
Label: Incorrect
```

### Examples (Good and Bad)
```markdown
## Good Example
Question: "What is the capital of France?"
Answer: "Paris"
Label: Correct
Reasoning: Factually accurate and directly answers question

## Bad Example
Question: "What is the capital of France?"
Answer: "France is a country in Europe"
Label: Incorrect
Reasoning: Doesn't answer the question
```

### Edge Case Handling
```markdown
## Edge Cases

### Partially Correct
Question: "What are the capitals of France and Germany?"
Answer: "Paris"
Label: Partially Correct (missing Germany)

### Ambiguous Question
Question: "What is the best programming language?"
Label: N/A - Subjective question, no single correct answer

### No Answer in Context
Question: "What is the population of Paris?"
Context: "Paris is the capital of France."
Label: "Cannot be determined from context"
```

### Consistency Checks
```markdown
## Consistency Rules

1. Same question → Same answer
2. Synonyms are acceptable ("car" = "automobile")
3. Case-insensitive ("Paris" = "paris")
4. Extra details are OK ("Paris" vs "Paris, France")
```

---

## Quality Control

### Multiple Annotators Per Example
```
Each example labeled by 3 annotators
Majority vote determines final label
Catches individual annotator errors
```

### Inter-Annotator Agreement (IAA)
```
Measure: Do annotators agree?
Metric: Cohen's Kappa (κ)
Target: κ > 0.7 (good agreement)
```

### Gold Standard Subset (Known Answers)
```
10% of examples have known correct labels
Mix into annotation tasks
Measure annotator accuracy on gold standard
Remove low-quality annotators
```

### Spot Checks by Experts
```
Expert reviews 10% of annotations
Validates quality
Identifies systematic errors
```

---

## Inter-Annotator Agreement

### Kappa Score (Cohen's κ)
```python
from sklearn.metrics import cohen_kappa_score

annotator1 = [1, 0, 1, 1, 0]  # Labels from annotator 1
annotator2 = [1, 0, 1, 0, 0]  # Labels from annotator 2

kappa = cohen_kappa_score(annotator1, annotator2)
print(f"Kappa: {kappa:.2f}")

# Interpretation:
# κ < 0.4: Poor agreement
# κ 0.4-0.6: Moderate agreement
# κ 0.6-0.8: Good agreement
# κ > 0.8: Excellent agreement
```

### Fleiss' κ (Multiple Annotators)
```python
from statsmodels.stats.inter_rater import fleiss_kappa

# 3 annotators, 5 examples
# Each row: [count_label_0, count_label_1]
data = [
    [0, 3],  # Example 1: All 3 annotators chose label 1
    [1, 2],  # Example 2: 1 chose 0, 2 chose 1
    [3, 0],  # Example 3: All 3 chose label 0
    [2, 1],  # Example 4: 2 chose 0, 1 chose 1
    [0, 3],  # Example 5: All 3 chose label 1
]

kappa = fleiss_kappa(data)
print(f"Fleiss' Kappa: {kappa:.2f}")
```

### Percentage Agreement
```python
def percentage_agreement(annotator1, annotator2):
    agreements = sum(a == b for a, b in zip(annotator1, annotator2))
    total = len(annotator1)
    return agreements / total

agreement = percentage_agreement(annotator1, annotator2)
print(f"Agreement: {agreement:.1%}")
```

### Target: >0.7 (Good Agreement)
```
If κ < 0.7:
1. Review annotation guidelines (unclear?)
2. Provide more examples
3. Train annotators
4. Simplify task
```

---

## Resolving Disagreements

### Majority Vote
```python
def majority_vote(labels):
    from collections import Counter
    counts = Counter(labels)
    majority_label = counts.most_common(1)[0][0]
    return majority_label

# 3 annotators
labels = [1, 1, 0]  # Two say 1, one says 0
final_label = majority_vote(labels)  # 1
```

### Expert Adjudication
```
If no majority (e.g., 1, 0, 2):
→ Expert reviews and decides
```

### Discussion and Consensus
```
Annotators discuss disagreement
Reach consensus
Update guidelines if needed
```

### Update Guidelines
```
If systematic disagreements:
→ Guidelines unclear
→ Update and re-annotate
```

---

## Ground Truth for Different Tasks

### Classification: Category Labels
```json
{
  "text": "This product is amazing!",
  "label": "positive"
}
```

### Q&A: Correct Answers + Acceptable Variants
```json
{
  "question": "What is the capital of France?",
  "answer": "Paris",
  "acceptable_variants": ["paris", "PARIS", "The capital is Paris"]
}
```

### Summarization: Reference Summaries
```json
{
  "document": "Long article text...",
  "reference_summary": "Concise summary of key points"
}
```

### RAG: Question + Context + Answer
```json
{
  "question": "What is the capital of France?",
  "context": "Paris is the capital and largest city of France.",
  "answer": "Paris",
  "relevant_chunks": ["Paris is the capital and largest city of France."]
}
```

### Generation: Multiple Acceptable Outputs
```json
{
  "prompt": "Write a haiku about spring",
  "acceptable_outputs": [
    "Cherry blossoms bloom\nGentle breeze carries petals\nSpring has arrived now",
    "Flowers start to bloom\nBirds sing in the morning light\nSpring is here at last"
  ]
}
```

---

## Dataset Size

### Evaluation Set: 100-1000 Examples (Representative)
```
Purpose: Quick evaluation during development
Size: 100-1000 examples
Quality: High (manually curated)
Coverage: Representative of production
```

### Test Set: 500-5000 Examples (Comprehensive)
```
Purpose: Final evaluation before deployment
Size: 500-5000 examples
Quality: High (gold standard)
Coverage: Comprehensive (all categories, edge cases)
```

### Quality > Quantity
```
Better: 100 high-quality examples
Worse: 1000 low-quality examples
```

### Cover Edge Cases
```
Include:
- Common cases (80%)
- Edge cases (15%)
- Adversarial cases (5%)
```

---

## Dataset Maintenance

### Version Control (Like Code)
```bash
# Git for dataset versioning
git init
git add dataset.jsonl
git commit -m "Initial dataset v1.0"

# Tag versions
git tag v1.0

# Update dataset
git add dataset.jsonl
git commit -m "Added 100 new examples"
git tag v1.1
```

### Regular Updates (New Examples)
```
Monthly: Add 50-100 new examples
Quarterly: Major update (500+ examples)
```

### Remove Outdated Examples
```
Examples that are:
- No longer relevant
- Incorrect (facts changed)
- Duplicates
```

### Track Changes (Changelog)
```markdown
# Dataset Changelog

## v1.2 (2024-02-01)
- Added 100 new examples (geography category)
- Removed 20 outdated examples
- Fixed 5 incorrect labels

## v1.1 (2024-01-01)
- Added 50 new examples (science category)
- Updated annotation guidelines

## v1.0 (2023-12-01)
- Initial release (500 examples)
```

---

## Stratified Sampling

### Balance by Difficulty
```
Easy: 40%
Medium: 40%
Hard: 20%
```

### Balance by Category
```
Geography: 25%
Science: 25%
History: 25%
Math: 25%
```

### Include Edge Cases
```
Common cases: 80%
Edge cases: 15%
Adversarial: 5%
```

### Representative of Production
```
Sample from actual production queries
Ensures dataset matches real usage
```

---

## Synthetic Ground Truth

### LLM-Generated Questions + Answers
```python
def generate_synthetic_qa(document):
    prompt = f"""
    Document: {document}
    
    Generate 5 question-answer pairs based on this document.
    
    Format:
    Q1: [question]
    A1: [answer]
    ...
    """
    
    response = llm.generate(prompt)
    qa_pairs = parse_qa_pairs(response)
    return qa_pairs
```

### Careful Validation Needed
```
LLM-generated data can have:
- Hallucinations
- Incorrect facts
- Biased questions

→ Always validate with humans
```

### Good for Scale, Risky for Quality
```
Pros: Can generate 1000s quickly
Cons: Quality varies, needs validation
```

### Use for Augmentation, Not Sole Source
```
Strategy:
- 80% human-annotated (high quality)
- 20% synthetic (validated)
```

---

## Domain-Specific Ground Truth

### Medical: Expert Annotations
```
Annotators: Licensed doctors
Cost: $50-100 per hour
Quality: Very high
Use case: Medical diagnosis, treatment recommendations
```

### Legal: Lawyer Review
```
Annotators: Licensed lawyers
Cost: $100-300 per hour
Quality: Very high
Use case: Legal document analysis, case law
```

### Technical: Engineer Verification
```
Annotators: Senior engineers
Cost: $50-150 per hour
Quality: High
Use case: Code review, technical Q&A
```

---

## Ground Truth Storage

### JSON/JSONL Files
```jsonl
{"id": "1", "question": "What is 2+2?", "answer": "4"}
{"id": "2", "question": "Capital of France?", "answer": "Paris"}
```

### Database (PostgreSQL, MongoDB)
```sql
CREATE TABLE ground_truth (
  id UUID PRIMARY KEY,
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  category VARCHAR(50),
  difficulty VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Version Control (Git)
```bash
git add dataset/
git commit -m "Update ground truth dataset"
git push
```

### Cloud Storage (S3 + Versioning)
```bash
# Upload to S3 with versioning
aws s3 cp dataset.jsonl s3://my-bucket/ground-truth/v1.0/dataset.jsonl
aws s3api put-bucket-versioning --bucket my-bucket --versioning-configuration Status=Enabled
```

---

## Ground Truth for RAG

**Structure:**
```json
{
  "question": "What is the capital of France?",
  "expected_answer": "Paris",
  "relevant_document_chunks": [
    "Paris is the capital and largest city of France."
  ],
  "evaluation_criteria": {
    "faithfulness": "Answer must be grounded in context",
    "relevance": "Answer must directly address question",
    "completeness": "Answer should mention Paris"
  }
}
```

---

## Evaluation with Ground Truth

### Exact Match Accuracy
```python
def exact_match(predicted, ground_truth):
    return predicted.strip().lower() == ground_truth.strip().lower()

accuracy = sum(exact_match(p, gt) for p, gt in zip(predicted, ground_truth)) / len(predicted)
```

### F1 Score (For Overlapping Spans)
```python
def f1_score(predicted, ground_truth):
    pred_tokens = set(predicted.lower().split())
    gt_tokens = set(ground_truth.lower().split())
    
    common = pred_tokens & gt_tokens
    if len(pred_tokens) == 0 or len(gt_tokens) == 0:
        return 0
    
    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(gt_tokens)
    
    if precision + recall == 0:
        return 0
    
    f1 = 2 * (precision * recall) / (precision + recall)
    return f1
```

### BLEU/ROUGE (For Generation)
```python
from nltk.translate.bleu_score import sentence_bleu

reference = [["Paris", "is", "the", "capital"]]
candidate = ["Paris", "is", "the", "capital"]

bleu = sentence_bleu(reference, candidate)
```

### Semantic Similarity (Embedding Distance)
```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

emb1 = model.encode("Paris is the capital of France")
emb2 = model.encode("The capital of France is Paris")

similarity = cosine_similarity([emb1], [emb2])[0][0]
```

---

## Continuous Ground Truth

### Production Feedback (User Thumbs Up/Down)
```python
# Log user feedback
feedback = {
    "question": "What is the capital of France?",
    "answer": "Paris",
    "user_feedback": "thumbs_up",
    "timestamp": "2024-01-15T10:00:00Z"
}

# Add to ground truth if positive
if feedback["user_feedback"] == "thumbs_up":
    add_to_ground_truth(feedback["question"], feedback["answer"])
```

### Human Review of Flagged Outputs
```
User flags answer as incorrect
→ Human reviews
→ If incorrect, add correct answer to ground truth
→ If correct, keep as is
```

### Incrementally Add to Dataset
```
Monthly: Review 100 flagged examples
Add 50 to ground truth
Update dataset version
```

---

## Tools

### Annotation: Label Studio, Prodigy, CVAT

**Label Studio:**
```bash
pip install label-studio
label-studio start
# Open http://localhost:8080
```

**Prodigy:**
```bash
pip install prodigy
prodigy textcat.manual dataset_name source.jsonl --label positive,negative
```

### Management: DVC (Data Version Control)
```bash
pip install dvc
dvc init
dvc add dataset.jsonl
git add dataset.jsonl.dvc .gitignore
git commit -m "Add dataset"
dvc push
```

### Storage: S3, GCS, Local Files

See "Ground Truth Storage" section

---

## Summary

**Ground Truth:** Correct answers for evaluation

**Why:**
- Measure accuracy objectively
- Train/validate models
- Regression testing
- Benchmarking

**Types:**
- Exact match
- Multiple acceptable answers
- Rubric-based
- Human preference

**Creating:**
- Manual annotation
- Expert review
- Crowdsourcing
- Synthetic (with validation)

**Quality Control:**
- Multiple annotators
- Inter-annotator agreement (κ > 0.7)
- Gold standard subset
- Expert spot checks

**Dataset Size:**
- Eval: 100-1000 (representative)
- Test: 500-5000 (comprehensive)
- Quality > quantity

**Maintenance:**
- Version control (Git)
- Regular updates
- Remove outdated
- Changelog

**Tools:**
- Annotation: Label Studio, Prodigy
- Management: DVC
- Storage: S3, GCS, Git
