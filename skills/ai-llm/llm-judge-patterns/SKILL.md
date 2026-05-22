---
name: LLM Judge Patterns
description: Comprehensive guide to using LLMs as judges for automated evaluation including prompt patterns, calibration, bias reduction, and multi-judge ensembles
---

# LLM Judge Patterns

## What is LLM-as-Judge?

**Definition:** Using LLMs (GPT-4, Claude) to evaluate other LLM outputs automatically.

### Model
```
Input: Question + Answer (to evaluate)
Judge LLM: GPT-4 or Claude
Output: Score + Reasoning

Example:
Question: "What is the capital of France?"
Answer: "Paris is the capital of France."
Judge: "Score: 5/5 - Correct, concise, directly answers question"
```

---

## Why LLM-as-Judge?

### Human Eval is Slow and Expensive

**Comparison:**
```
Human evaluation:
- 100 answers × 5 min each = 500 min = 8.3 hours
- Cost: $20/hour × 8.3 = $166

LLM-as-judge:
- 100 answers × 2 sec each = 200 sec = 3.3 min
- Cost: 100 × $0.01 = $1
```

### Need to Evaluate Thousands of Outputs

**Scale:**
```
Development: Test 1000+ variations
Production: Evaluate millions of responses
Human eval: Impossible at this scale
LLM-judge: Feasible
```

### Research Shows High Correlation with Human Judgment

**Studies:**
- GPT-4 as judge correlates 0.8+ with human ratings
- Works well for subjective quality (fluency, helpfulness)
- Less reliable for factual correctness

### Enables Continuous Evaluation

**Workflow:**
```
Every response → LLM judge → Score logged → Dashboard
Detect regressions in real-time
```

---

## When to Use LLM-as-Judge

### Subjective Quality (Fluency, Relevance, Helpfulness)

**Good Use Cases:**
```
- Is this answer helpful?
- Is this text fluent and natural?
- Is this response relevant to the question?
- Is this summary coherent?
```

### Complex Rubrics (Multi-Criteria)

**Example:**
```
Evaluate on:
1. Accuracy (1-5)
2. Completeness (1-5)
3. Clarity (1-5)
4. Tone (1-5)

LLM can handle multi-dimensional evaluation
```

### Large-Scale Evaluation

**When:**
```
Need to evaluate 1000+ examples
Human eval too slow/expensive
```

### Rapid Iteration

**Development:**
```
Test 10 prompt variations
Evaluate each on 100 examples
LLM-judge: Minutes
Human eval: Days
```

---

## When NOT to Use LLM-as-Judge

### Objective Correctness (Factual Answers)

**Problem:**
```
Question: "What is 2+2?"
Answer: "5"
LLM judge might say: "The answer is clear and confident" (wrong!)

Better: Exact match or computation
```

### Mathematical Reasoning (Verify with Computation)

**Better Approach:**
```
Execute code to verify answer
Not: Ask LLM if math is correct
```

### Code Correctness (Run Tests)

**Better Approach:**
```
Run unit tests
Check if code compiles
Not: Ask LLM if code is correct
```

### Safety-Critical (Use Human Evaluation)

**Examples:**
```
Medical advice
Legal guidance
Financial recommendations

→ Always use human experts
```

---

## Judge Model Selection

### GPT-4 (Most Commonly Used)

**Pros:**
- High quality judgments
- Good correlation with humans
- Widely tested

**Cons:**
- Expensive ($0.03/1K tokens)
- Can be slow

### Claude Sonnet 4 (Excellent Reasoning)

**Pros:**
- Excellent reasoning
- Good for complex evaluations
- Fast

**Cons:**
- Expensive
- Less tested than GPT-4

### GPT-3.5 (Cheaper, Less Accurate)

**Pros:**
- Cheap ($0.001/1K tokens)
- Fast

**Cons:**
- Less accurate
- More biased

### Open-Source (Llama, Mixtral)

**Pros:**
- Free (if self-hosted)
- Privacy (on-prem)

**Cons:**
- Lower quality
- Requires infrastructure

---

## Judge Prompt Patterns

### Single-Answer Grading

**Pattern:**
```
You are evaluating an AI assistant's response.

Question: {question}
Answer: {answer}

Rate the answer on a scale of 1-5:
1 = Poor
5 = Excellent

Consider:
- Accuracy
- Relevance
- Completeness

Score:
```

**Example:**
```python
def single_answer_grading(question, answer):
    prompt = f"""
    You are evaluating an AI assistant's response.
    
    Question: {question}
    Answer: {answer}
    
    Rate the answer on a scale of 1-5:
    1 = Poor (incorrect, irrelevant, or incomplete)
    5 = Excellent (correct, relevant, and complete)
    
    Provide:
    - Score (1-5)
    - Brief reasoning
    
    Format:
    Score: [number]
    Reasoning: [explanation]
    """
    
    response = llm.generate(prompt)
    score = extract_score(response)
    return score
```

### Pairwise Comparison (A vs B)

**Pattern:**
```
Which answer is better?

Question: {question}
Answer A: {answer_a}
Answer B: {answer_b}

Which is better? A or B?
Explain why.
```

**More Reliable:**
```
Pairwise comparison reduces absolute scoring bias
Humans also find comparisons easier than absolute ratings
```

**Example:**
```python
def pairwise_comparison(question, answer_a, answer_b):
    prompt = f"""
    Question: {question}
    
    Answer A: {answer_a}
    Answer B: {answer_b}
    
    Which answer is better? A or B?
    
    Consider:
    - Accuracy
    - Relevance
    - Clarity
    
    Respond with:
    - Winner: A or B
    - Reasoning: Why is it better?
    
    Format:
    Winner: [A or B]
    Reasoning: [explanation]
    """
    
    response = llm.generate(prompt)
    winner = extract_winner(response)
    return winner
```

**Aggregate via Elo Ratings:**
```python
# After many pairwise comparisons
# Calculate Elo rating for each model
# Higher Elo = better model
```

### Multi-Aspect Evaluation (Rubric)

**Pattern:**
```
Evaluate on multiple criteria:
1. Accuracy (1-5)
2. Relevance (1-5)
3. Completeness (1-5)
4. Clarity (1-5)

Score each separately
```

**Example:**
```python
def multi_aspect_evaluation(question, answer):
    prompt = f"""
    Question: {question}
    Answer: {answer}
    
    Evaluate on these criteria (1-5 scale):
    
    1. Accuracy: Is the information correct?
       1 = Incorrect, 5 = Perfectly accurate
    
    2. Relevance: Does it answer the question?
       1 = Irrelevant, 5 = Highly relevant
    
    3. Completeness: Does it cover all aspects?
       1 = Incomplete, 5 = Comprehensive
    
    4. Clarity: Is it clear and well-written?
       1 = Confusing, 5 = Very clear
    
    Provide scores and brief reasoning for each.
    
    Format:
    Accuracy: [score] - [reasoning]
    Relevance: [score] - [reasoning]
    Completeness: [score] - [reasoning]
    Clarity: [score] - [reasoning]
    Overall: [average score]
    """
    
    response = llm.generate(prompt)
    scores = extract_scores(response)
    return scores
```

### Chain-of-Thought Judging

**Pattern:**
```
First, explain your reasoning
Then, provide score

This increases reliability
```

**Example:**
```python
def cot_judging(question, answer):
    prompt = f"""
    Question: {question}
    Answer: {answer}
    
    Evaluate this answer step by step:
    
    Step 1: Is the answer factually correct?
    Step 2: Does it fully address the question?
    Step 3: Is it clear and well-written?
    
    Based on your analysis, rate the answer (1-5).
    
    Format:
    Step 1: [analysis]
    Step 2: [analysis]
    Step 3: [analysis]
    Final Score: [number]
    """
    
    response = llm.generate(prompt)
    return response
```

---

## Judge Prompt Template

**Comprehensive Template:**
```
You are an expert evaluator assessing AI assistant responses.

Question: {question}
Answer: {answer}
{optional: Ground Truth: {ground_truth}}
{optional: Context: {context}}

Evaluate the answer on these criteria:

1. **Accuracy** (1-5): Is the information factually correct?
   - 1 = Completely incorrect
   - 3 = Partially correct
   - 5 = Fully correct

2. **Relevance** (1-5): Does it address the question?
   - 1 = Completely irrelevant
   - 3 = Partially relevant
   - 5 = Directly addresses question

3. **Completeness** (1-5): Does it cover all aspects?
   - 1 = Missing most information
   - 3 = Covers some aspects
   - 5 = Comprehensive

4. **Clarity** (1-5): Is it clear and well-written?
   - 1 = Confusing or poorly written
   - 3 = Acceptable clarity
   - 5 = Very clear and well-written

Provide:
- Score for each criterion (1-5)
- Brief reasoning for each score
- Overall score (average of all criteria)

Format:
Accuracy: [score] - [reasoning]
Relevance: [score] - [reasoning]
Completeness: [score] - [reasoning]
Clarity: [score] - [reasoning]
Overall: [average score]
```

---

## Judge Calibration

### Compare Judge Scores to Human Scores

**Process:**
```
1. Get 100 examples
2. Human annotators rate each (1-5)
3. LLM judge rates each (1-5)
4. Calculate correlation
```

**Correlation:**
```python
from scipy.stats import pearsonr

human_scores = [4, 5, 3, 4, 2, ...]
judge_scores = [4.2, 4.8, 3.1, 4.5, 2.3, ...]

correlation, p_value = pearsonr(human_scores, judge_scores)
print(f"Correlation: {correlation:.2f}")

# Target: >0.7 (good correlation)
# If <0.7: Adjust prompt or use different judge
```

### Calculate Correlation

See above

### Adjust Prompt if Low Correlation

**If correlation <0.7:**
```
1. Analyze disagreements (where judge differs from human)
2. Update prompt to address issues
3. Re-test correlation
4. Iterate until >0.7
```

### Test on Multiple Examples

**Validation Set:**
```
Use 100-500 examples with human ratings
Ensure diverse (easy, hard, edge cases)
```

---

## Reducing Judge Bias

### Position Bias (Favors First Option in A/B)

**Problem:**
```
Judge tends to prefer Answer A over Answer B
Even when B is better
```

**Mitigation:**
```python
# Randomize order
import random

if random.random() < 0.5:
    winner = compare(question, answer_a, answer_b)
else:
    winner = compare(question, answer_b, answer_a)
    winner = "A" if winner == "B" else "B"  # Flip
```

### Length Bias (Favors Longer Answers)

**Problem:**
```
Judge tends to prefer longer answers
Even if shorter answer is better
```

**Mitigation:**
```
Prompt: "Do not favor longer answers. Concise answers can be better."
Or: Normalize scores by length
```

### Self-Preference Bias (Favors Own Outputs)

**Problem:**
```
GPT-4 as judge tends to prefer GPT-4 outputs
Over Claude outputs
```

**Mitigation:**
```
Use external judge (Claude to judge GPT-4)
Or: Blind evaluation (don't reveal which model)
```

---

## Multi-Judge Ensemble

### Use Multiple Judges (GPT-4 + Claude)

**Approach:**
```python
def multi_judge_ensemble(question, answer):
    # Judge 1: GPT-4
    score_gpt4 = gpt4_judge(question, answer)
    
    # Judge 2: Claude
    score_claude = claude_judge(question, answer)
    
    # Judge 3: GPT-3.5 (cheaper, as tiebreaker)
    score_gpt35 = gpt35_judge(question, answer)
    
    return {
        "gpt4": score_gpt4,
        "claude": score_claude,
        "gpt35": score_gpt35
    }
```

### Aggregate Scores (Majority Vote, Average)

**Majority Vote:**
```python
scores = [4, 5, 4]  # Three judges
majority = max(set(scores), key=scores.count)  # 4
```

**Average:**
```python
scores = [4.2, 4.8, 4.5]
average = sum(scores) / len(scores)  # 4.5
```

**Weighted Average:**
```python
scores = {"gpt4": 4.8, "claude": 4.5, "gpt35": 4.0}
weights = {"gpt4": 0.5, "claude": 0.4, "gpt35": 0.1}

weighted_avg = sum(scores[j] * weights[j] for j in scores)  # 4.58
```

### Increases Reliability

**Why:**
```
Single judge can be wrong
Multiple judges reduce variance
Ensemble is more robust
```

---

## Cost Optimization

### Use Cheaper Judge for Initial Filtering

**Two-Stage:**
```
Stage 1: GPT-3.5 judge (cheap, fast)
  - Filter out clearly bad answers (score <3)
  
Stage 2: GPT-4 judge (expensive, accurate)
  - Evaluate borderline cases (score 3-4)
```

### Use Expensive Judge for Borderline Cases

See above

### Cache Judge Results

**Caching:**
```python
import hashlib
import json

cache = {}

def cached_judge(question, answer):
    # Create cache key
    key = hashlib.md5(f"{question}{answer}".encode()).hexdigest()
    
    # Check cache
    if key in cache:
        return cache[key]
    
    # Call judge
    score = llm_judge(question, answer)
    
    # Cache result
    cache[key] = score
    
    return score
```

---

## Judge Evaluation Frameworks

### G-Eval (Using GPT-4)

**Paper:** "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment"

**Approach:**
```
Use GPT-4 to generate evaluation criteria
Then use GPT-4 to evaluate based on those criteria
```

### Prometheus (Using Llama)

**Open-Source Judge:**
```
Fine-tuned Llama model for evaluation
Free to use
Lower quality than GPT-4 but no API costs
```

### Custom Implementation

See examples throughout this document

---

## Metrics to Track

### Judge-Human Correlation

**Target:** >0.7

**Calculation:**
```python
from scipy.stats import pearsonr

correlation, p_value = pearsonr(human_scores, judge_scores)
```

### Inter-Judge Agreement (If Multiple Judges)

**Kappa Score:**
```python
from sklearn.metrics import cohen_kappa_score

kappa = cohen_kappa_score(judge1_scores, judge2_scores)
# >0.7 = good agreement
```

### Judge Consistency (Same Input → Same Output)

**Test:**
```python
# Evaluate same example 10 times
scores = [judge(question, answer) for _ in range(10)]

# Calculate variance
variance = np.var(scores)
# Low variance = consistent judge
```

---

## Real-World Judge Use Cases

### RAG Answer Evaluation

See RAG Evaluation skill

### Chatbot Response Quality

**Criteria:**
- Helpfulness
- Relevance
- Safety
- Tone

### Content Moderation

**Criteria:**
- Toxicity
- Hate speech
- Misinformation
- Spam

### Translation Quality

**Criteria:**
- Accuracy
- Fluency
- Preserves meaning

### Summarization Quality

**Criteria:**
- Completeness
- Conciseness
- Accuracy

---

## Limitations

### Judge Can Be Wrong (Validate with Humans)

**Always:**
```
Spot-check judge results with human evaluation
Don't blindly trust judge
```

### Expensive (API Costs)

**Cost:**
```
1000 evaluations × $0.01 = $10
10,000 evaluations × $0.01 = $100

Can add up quickly
```

### Judge Bias (Needs Careful Prompting)

See "Reducing Judge Bias" section

### Not Suitable for All Tasks

See "When NOT to Use" section

---

## Implementation

### Judge Prompt Templates

See "Judge Prompt Template" section

### Multi-Judge Aggregation

See "Multi-Judge Ensemble" section

### Calibration Scripts

```python
def calibrate_judge(judge_fn, test_set):
    """
    test_set: List of (question, answer, human_score)
    """
    judge_scores = []
    human_scores = []
    
    for question, answer, human_score in test_set:
        judge_score = judge_fn(question, answer)
        judge_scores.append(judge_score)
        human_scores.append(human_score)
    
    correlation, p_value = pearsonr(human_scores, judge_scores)
    
    return {
        "correlation": correlation,
        "p_value": p_value,
        "judge_scores": judge_scores,
        "human_scores": human_scores
    }
```

---

## Summary

### Quick Reference

**LLM-as-Judge:** Use LLMs to evaluate other LLM outputs

**Why:**
- Fast and cheap vs human eval
- Scales to thousands of examples
- High correlation with humans (>0.8)

**When to Use:**
- Subjective quality
- Complex rubrics
- Large-scale evaluation

**When NOT:**
- Objective correctness
- Math/code (use computation)
- Safety-critical (use humans)

**Judge Models:**
- GPT-4 (best quality)
- Claude (excellent reasoning)
- GPT-3.5 (cheaper)
- Open-source (free but lower quality)

**Prompt Patterns:**
- Single-answer grading
- Pairwise comparison (more reliable)
- Multi-aspect (rubric)
- Chain-of-thought (increases reliability)

**Bias Reduction:**
- Position bias: Randomize order
- Length bias: Normalize or prompt
- Self-preference: External judge

**Multi-Judge:**
- Use multiple judges
- Aggregate (majority vote, average)
- Increases reliability

**Cost Optimization:**
- Cheap judge for filtering
- Expensive judge for borderline
- Cache results

**Calibration:**
- Compare to human scores
- Target correlation >0.7
- Adjust prompt if low

**Limitations:**
- Can be wrong (validate with humans)
- Expensive (API costs)
- Biased (careful prompting)
