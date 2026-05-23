---
name: Regression Benchmarks
description: Comprehensive guide to regression benchmarks for AI systems including test suite creation, CI/CD integration, and continuous benchmarking strategies
---

# Regression Benchmarks

## What are Regression Benchmarks?

**Definition:** Test suite to detect performance degradation - runs on every change like unit tests to catch regressions before deployment.

### Example
```
Before change: Accuracy 90%
After change: Accuracy 85%
→ Regression detected! ❌ Block deployment
```

### Like Unit Tests for AI
```
Unit tests: Verify code correctness
Regression benchmarks: Verify AI performance

Both run automatically on every change
```

---

## Why Regression Benchmarks Matter

### New Features Can Break Existing Functionality
```
Add new feature: Multi-language support
Side effect: English accuracy drops from 90% to 85%
→ Regression benchmark catches this
```

### Model Updates Can Reduce Quality
```
Update model: GPT-3.5 → GPT-4
Unexpected: Latency increases 5x
→ Regression benchmark catches this
```

### Prompt Changes Can Have Unintended Effects
```
Change prompt: Add "Be concise"
Side effect: Completeness drops (answers too short)
→ Regression benchmark catches this
```

### Catch Issues Early (Before Production)
```
Without benchmarks:
Deploy → Users complain → Rollback → Fix → Redeploy
Timeline: Days

With benchmarks:
Change → Benchmark fails → Fix → Benchmark passes → Deploy
Timeline: Hours
```

---

## Components of Regression Suite

### Test Cases (Inputs + Expected Outputs)
```json
{
  "test_id": "test_001",
  "input": "What is the capital of France?",
  "expected_output": "Paris",
  "category": "geography",
  "priority": "high"
}
```

### Evaluation Metrics (How to Score)
```
- Exact match accuracy
- F1 score
- Semantic similarity
- LLM-as-judge score
- Latency
```

### Acceptance Thresholds (What's Acceptable)
```
Absolute thresholds:
- Accuracy > 90%
- Latency P95 < 500ms
- Safety violations = 0

Relative thresholds:
- Accuracy: No worse than -2% vs baseline
- Latency: No worse than +10% vs baseline
```

### Automated Execution (CI/CD)
```yaml
# Run on every PR
on: [pull_request]

jobs:
  regression-tests:
    runs-on: ubuntu-latest
    steps:
      - name: Run regression benchmarks
        run: python run_benchmarks.py
      
      - name: Check thresholds
        run: |
          if [ $ACCURACY -lt 0.90 ]; then
            echo "Accuracy regression detected"
            exit 1
          fi
```

---

## Creating Regression Test Cases

### Representative Examples (Common Queries)
```
Include:
- Most frequent queries (80%)
- Cover all major categories
- Balanced difficulty
```

**Example:**
```json
[
  {"input": "What is 2+2?", "expected": "4", "category": "math", "frequency": "high"},
  {"input": "Capital of France?", "expected": "Paris", "category": "geography", "frequency": "high"},
  {"input": "Who wrote Hamlet?", "expected": "Shakespeare", "category": "literature", "frequency": "medium"}
]
```

### Edge Cases (Where Model Struggles)
```
Include:
- Ambiguous questions
- Multi-hop reasoning
- Rare topics
- Adversarial examples
```

**Example:**
```json
[
  {"input": "What is the best programming language?", "expected": "Subjective, no single answer", "category": "edge_case"},
  {"input": "Capital of Atlantis?", "expected": "Atlantis is fictional", "category": "edge_case"}
]
```

### Historical Failures (Bugs That Happened Before)
```
When bug occurs:
1. Fix bug
2. Add test case to prevent regression
3. Test case runs forever
```

**Example:**
```json
{
  "test_id": "bug_fix_123",
  "input": "What is the population of Paris?",
  "expected": "Should include number, not just 'Paris has a population'",
  "bug_report": "Issue #123: Incomplete answers",
  "added_date": "2024-01-15"
}
```

### Diverse Coverage (Different Categories)
```
Categories:
- Math (10%)
- Geography (10%)
- Science (10%)
- History (10%)
- General knowledge (60%)
```

---

## Test Case Structure

### Input (Question, Prompt, Image)
```json
{
  "input": {
    "type": "question",
    "text": "What is the capital of France?"
  }
}
```

### Expected Behavior (Correct Answer or Quality Criteria)
```json
{
  "expected": {
    "type": "exact_match",
    "value": "Paris"
  }
}
```

**Or quality criteria:**
```json
{
  "expected": {
    "type": "quality_criteria",
    "faithfulness": ">= 0.9",
    "relevance": ">= 0.9",
    "completeness": ">= 0.8"
  }
}
```

### Context (If Needed for Evaluation)
```json
{
  "context": "Paris is the capital and largest city of France."
}
```

### Metadata (Category, Difficulty, Priority)
```json
{
  "metadata": {
    "category": "geography",
    "difficulty": "easy",
    "priority": "high",
    "added_date": "2024-01-15",
    "last_updated": "2024-01-15"
  }
}
```

**Complete Example:**
```json
{
  "test_id": "test_001",
  "input": {
    "type": "question",
    "text": "What is the capital of France?"
  },
  "expected": {
    "type": "exact_match",
    "value": "Paris",
    "acceptable_variants": ["paris", "PARIS"]
  },
  "context": "Paris is the capital and largest city of France.",
  "metadata": {
    "category": "geography",
    "difficulty": "easy",
    "priority": "high"
  }
}
```

---

## Evaluation Strategies

### Exact Match (For Deterministic Outputs)
```python
def exact_match(predicted, expected):
    return predicted.strip().lower() == expected.strip().lower()

# Test
assert exact_match("Paris", "paris") == True
assert exact_match("Lyon", "Paris") == False
```

### Semantic Similarity (For Generated Text)
```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_similarity(predicted, expected, threshold=0.8):
    emb1 = model.encode(predicted)
    emb2 = model.encode(expected)
    similarity = cosine_similarity([emb1], [emb2])[0][0]
    return similarity >= threshold

# Test
assert semantic_similarity("Paris is the capital", "The capital is Paris") == True
```

### LLM-as-Judge (For Quality)
```python
def llm_judge(question, answer, criteria):
    prompt = f"""
    Question: {question}
    Answer: {answer}
    
    Evaluate on criteria: {criteria}
    Score (1-5):
    """
    
    score = llm.generate(prompt)
    return int(score) >= 4  # Pass if >= 4

# Test
assert llm_judge("Capital of France?", "Paris", "correctness") == True
```

### Human Spot Checks (Sample Validation)
```python
# Sample 10% for human review
sample_size = len(test_cases) // 10
sample = random.sample(test_cases, sample_size)

for test in sample:
    human_score = get_human_evaluation(test)
    automated_score = run_test(test)
    
    # Validate automated evaluation
    if abs(human_score - automated_score) > 1:
        flag_for_review(test)
```

---

## Acceptance Criteria

### Absolute Threshold
```python
# Must meet minimum standards
thresholds = {
    "accuracy": 0.90,  # >= 90%
    "latency_p95": 500,  # <= 500ms
    "safety_violations": 0  # = 0
}

def check_absolute_thresholds(results):
    if results["accuracy"] < thresholds["accuracy"]:
        return False, f"Accuracy {results['accuracy']:.2%} < {thresholds['accuracy']:.2%}"
    
    if results["latency_p95"] > thresholds["latency_p95"]:
        return False, f"Latency {results['latency_p95']}ms > {thresholds['latency_p95']}ms"
    
    if results["safety_violations"] > thresholds["safety_violations"]:
        return False, f"Safety violations {results['safety_violations']} > 0"
    
    return True, "All thresholds met"
```

### Relative Threshold (vs Baseline)
```python
# No worse than baseline
relative_thresholds = {
    "accuracy": -0.02,  # No worse than -2%
    "latency": 0.10  # No worse than +10%
}

def check_relative_thresholds(current, baseline):
    accuracy_change = current["accuracy"] - baseline["accuracy"]
    if accuracy_change < relative_thresholds["accuracy"]:
        return False, f"Accuracy dropped {accuracy_change:.2%}"
    
    latency_change = (current["latency"] - baseline["latency"]) / baseline["latency"]
    if latency_change > relative_thresholds["latency"]:
        return False, f"Latency increased {latency_change:.2%}"
    
    return True, "No regression vs baseline"
```

### Per-Category Thresholds (Important Categories Stricter)
```python
category_thresholds = {
    "safety": {"accuracy": 0.99},  # Stricter for safety
    "math": {"accuracy": 0.95},
    "general": {"accuracy": 0.90}
}

def check_category_thresholds(results_by_category):
    for category, results in results_by_category.items():
        threshold = category_thresholds.get(category, {"accuracy": 0.90})
        
        if results["accuracy"] < threshold["accuracy"]:
            return False, f"{category} accuracy {results['accuracy']:.2%} < {threshold['accuracy']:.2%}"
    
    return True, "All categories meet thresholds"
```

---

## Regression Test Types

### Accuracy Tests (Correct Answers)
```python
def test_accuracy():
    results = run_model_on_test_set(test_cases)
    accuracy = sum(r["correct"] for r in results) / len(results)
    assert accuracy >= 0.90, f"Accuracy {accuracy:.2%} < 90%"
```

### Quality Tests (Output Quality)
```python
def test_quality():
    results = evaluate_quality(test_cases)
    avg_quality = sum(r["quality_score"] for r in results) / len(results)
    assert avg_quality >= 4.0, f"Quality {avg_quality:.1f} < 4.0"
```

### Latency Tests (Response Time)
```python
def test_latency():
    latencies = measure_latency(test_cases)
    p95_latency = np.percentile(latencies, 95)
    assert p95_latency <= 500, f"P95 latency {p95_latency}ms > 500ms"
```

### Safety Tests (No Harmful Outputs)
```python
def test_safety():
    results = run_safety_checks(test_cases)
    violations = sum(r["is_unsafe"] for r in results)
    assert violations == 0, f"Safety violations: {violations}"
```

### Consistency Tests (Same Input → Same Output)
```python
def test_consistency():
    # Run same input 10 times
    for test_case in sample(test_cases, 10):
        outputs = [model.predict(test_case["input"]) for _ in range(10)]
        
        # Check all outputs are similar
        unique_outputs = set(outputs)
        assert len(unique_outputs) <= 2, f"Inconsistent outputs: {unique_outputs}"
```

---

## Running Regression Suite

### Trigger
```
- Every code change (PR)
- Every prompt change
- Every model update
- Nightly (full suite)
```

### Execution
```yaml
# GitHub Actions
name: Regression Tests

on:
  pull_request:
  schedule:
    - cron: '0 0 * * *'  # Nightly

jobs:
  regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run regression benchmarks
        run: python run_benchmarks.py
      
      - name: Check results
        run: python check_thresholds.py
```

### Duration
```
Fast enough for CI: Minutes, not hours

Strategies:
- Parallel execution
- Sample subset for PR (100 tests)
- Full suite nightly (1000 tests)
```

### Reporting
```
Clear pass/fail + details

Example output:
✓ Accuracy: 92% (>= 90%)
✓ Latency P95: 450ms (<= 500ms)
✗ Safety: 2 violations (> 0)

Failed tests:
- test_042: Unsafe output detected
- test_137: Unsafe output detected

Overall: FAILED
```

---

## Handling Failures

### Investigate Root Cause
```
Failure detected → Investigate:
1. What changed? (code, prompt, model)
2. Which tests failed?
3. Why did they fail?
```

### Intended Change (Update Benchmark)
```
Example:
- Changed behavior intentionally (new feature)
- Old test no longer valid
- Update test to reflect new expected behavior
```

### Unintended Regression (Fix the Issue)
```
Example:
- Bug introduced
- Performance degraded
- Fix the code/prompt/model
- Re-run benchmarks
```

### Flaky Test (Improve Test Stability)
```
Example:
- Test passes sometimes, fails sometimes
- Non-deterministic model output
- Fix: Use temperature=0, or semantic similarity instead of exact match
```

---

## Golden Set

### Curated Subset of Most Important Tests
```
Golden set: 100 most critical tests
Full suite: 1000 tests

Golden set:
- High-priority tests
- Core functionality
- Safety-critical
- Historical failures
```

### High-Quality Ground Truth
```
Golden set has:
- Expert-verified answers
- Multiple annotators
- Regular review
```

### Regularly Updated
```
Monthly: Review golden set
- Add new important tests
- Remove outdated tests
- Update expected outputs
```

### Always Passing (Except When Intentional)
```
Golden set should always pass
If golden set fails → Critical issue
Block deployment until fixed
```

---

## Versioning Benchmarks

### Benchmark Version Tied to Model Version
```
Model v1.0 → Benchmark v1.0
Model v2.0 → Benchmark v2.0

Each model version has corresponding benchmark
```

### Update Benchmarks When Requirements Change
```
New feature: Multi-language support
→ Add multi-language tests to benchmark
→ Increment benchmark version
```

### Maintain History (Track Improvements Over Time)
```
Benchmark results over time:
v1.0: 85% accuracy
v1.1: 87% accuracy
v1.2: 90% accuracy
v2.0: 92% accuracy

Track progress!
```

---

## Benchmark Coverage

### Functional Coverage (All Features Tested)
```
Features:
- Q&A: 40% of tests
- Summarization: 20%
- Translation: 20%
- Code generation: 20%

All features covered
```

### Edge Case Coverage (Error Conditions, Boundaries)
```
Edge cases:
- Empty input
- Very long input
- Ambiguous questions
- No answer available
- Multiple valid answers
```

### Performance Coverage (Speed, Cost)
```
Performance tests:
- Latency (P50, P95, P99)
- Throughput (requests/sec)
- Cost ($ per 1000 requests)
```

---

## Continuous Benchmarking

### Run on Every PR (Fast Subset)
```yaml
on: [pull_request]

jobs:
  quick-benchmark:
    runs-on: ubuntu-latest
    steps:
      - name: Run quick benchmark (100 tests)
        run: python run_benchmarks.py --quick
```

### Run Nightly (Full Suite)
```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # Every night at midnight

jobs:
  full-benchmark:
    runs-on: ubuntu-latest
    steps:
      - name: Run full benchmark (1000 tests)
        run: python run_benchmarks.py --full
```

### Run on Model Updates (Comprehensive)
```yaml
on:
  workflow_dispatch:
    inputs:
      model_version:
        description: 'Model version to test'
        required: true

jobs:
  model-benchmark:
    runs-on: ubuntu-latest
    steps:
      - name: Run comprehensive benchmark
        run: python run_benchmarks.py --model ${{ github.event.inputs.model_version }}
```

---

## Benchmark Metrics to Track

### Pass Rate (% of Tests Passing)
```python
pass_rate = passed_tests / total_tests
print(f"Pass rate: {pass_rate:.1%}")

# Track over time
# v1.0: 85%
# v1.1: 90%
# v1.2: 95%
```

### Performance vs Baseline (% Change)
```python
baseline_accuracy = 0.90
current_accuracy = 0.92
improvement = (current_accuracy - baseline_accuracy) / baseline_accuracy

print(f"Improvement: {improvement:.1%}")  # +2.2%
```

### Latency (P50, P95, P99)
```python
import numpy as np

latencies = [100, 150, 200, 250, 300, ...]

p50 = np.percentile(latencies, 50)
p95 = np.percentile(latencies, 95)
p99 = np.percentile(latencies, 99)

print(f"P50: {p50}ms, P95: {p95}ms, P99: {p99}ms")
```

### Cost Per Test (LLM API Calls)
```python
total_cost = sum(test["cost"] for test in results)
cost_per_test = total_cost / len(results)

print(f"Cost per test: ${cost_per_test:.4f}")
```

---

## Optimization

### Cache Model Responses (If Deterministic)
```python
import hashlib
import json

cache = {}

def cached_predict(input_text, model):
    # Create cache key
    key = hashlib.md5(f"{input_text}{model.version}".encode()).hexdigest()
    
    # Check cache
    if key in cache:
        return cache[key]
    
    # Predict
    output = model.predict(input_text)
    
    # Cache
    cache[key] = output
    
    return output
```

### Parallelize Test Execution
```python
from concurrent.futures import ThreadPoolExecutor

def run_benchmarks_parallel(test_cases, model):
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(lambda t: run_test(t, model), test_cases))
    
    return results
```

### Sample Large Test Suites (For Fast Feedback)
```python
# For PR: Sample 100 tests (fast)
if is_pr:
    test_cases = random.sample(all_test_cases, 100)

# For nightly: Run all tests (comprehensive)
else:
    test_cases = all_test_cases
```

---

## Integration with CI/CD

### GitHub Actions Workflow
```yaml
name: Regression Benchmarks

on: [pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run benchmarks
        id: benchmark
        run: |
          python run_benchmarks.py > results.txt
          cat results.txt
      
      - name: Check thresholds
        run: |
          ACCURACY=$(grep "Accuracy:" results.txt | awk '{print $2}' | tr -d '%')
          if [ $ACCURACY -lt 90 ]; then
            echo "::error::Accuracy $ACCURACY% < 90%"
            exit 1
          fi
      
      - name: Upload results
        uses: actions/upload-artifact@v2
        with:
          name: benchmark-results
          path: results.txt
```

### Required Check (Block Merge If Failing)
```yaml
# In GitHub repo settings:
# Branch protection rules → Require status checks
# Select: "benchmark" check

# PR cannot merge if benchmark fails
```

### Clear Error Messages (Which Tests Failed)
```python
def report_failures(results):
    failed = [r for r in results if not r["passed"]]
    
    if failed:
        print(f"\n❌ {len(failed)} tests failed:\n")
        for test in failed:
            print(f"  - {test['id']}: {test['error']}")
        
        print(f"\nOverall: FAILED ({len(failed)}/{len(results)} tests failed)")
        sys.exit(1)
    else:
        print(f"\n✓ All {len(results)} tests passed!")
```

### Link to Details (Full Report)
```python
# Generate HTML report
generate_html_report(results, "report.html")

# Upload to S3
upload_to_s3("report.html", f"s3://benchmarks/{commit_sha}/report.html")

# Comment on PR
comment_on_pr(f"Benchmark report: https://benchmarks.example.com/{commit_sha}/report.html")
```

---

## Real-World Regression Examples

### RAG System
```python
test_cases = [
    {
        "question": "What is the capital of France?",
        "expected_faithfulness": ">= 0.9",
        "expected_relevance": ">= 0.9"
    },
    # ... 1000 more tests
]

# Run on every change
results = evaluate_rag(test_cases)

# Check thresholds
assert results["avg_faithfulness"] >= 0.9
assert results["avg_relevance"] >= 0.9
```

### Chatbot
```python
test_cases = [
    {
        "input": "Hello",
        "expected_quality": ">= 4.0",
        "expected_safety": "safe"
    },
    # ... 1000 more tests
]

# Run on every change
results = evaluate_chatbot(test_cases)

# Check thresholds
assert results["avg_quality"] >= 4.0
assert results["safety_violations"] == 0
```

### Code Generation
```python
test_cases = [
    {
        "prompt": "Write a function to reverse a string",
        "expected_correctness": "passes unit tests",
        "expected_style": "follows PEP 8"
    },
    # ... 1000 more tests
]

# Run on every change
results = evaluate_code_generation(test_cases)

# Check thresholds
assert results["correctness_rate"] >= 0.90
assert results["style_violations"] <= 0.10
```

---

## Tools

### pytest (Test Framework)
```python
import pytest

def test_accuracy():
    results = run_benchmarks()
    assert results["accuracy"] >= 0.90

def test_latency():
    results = run_benchmarks()
    assert results["latency_p95"] <= 500
```

### Custom Evaluation Scripts
See examples throughout this document

### CI/CD Platforms
- GitHub Actions
- GitLab CI
- CircleCI
- Jenkins

---

## Summary

**Regression Benchmarks:** Test suite to detect performance degradation

**Why:**
- Catch regressions before deployment
- New features can break existing functionality
- Model/prompt changes can reduce quality

**Components:**
- Test cases (inputs + expected outputs)
- Evaluation metrics
- Acceptance thresholds
- Automated execution (CI/CD)

**Test Types:**
- Accuracy, quality, latency, safety, consistency

**Thresholds:**
- Absolute (>= 90% accuracy)
- Relative (no worse than -2% vs baseline)
- Per-category (stricter for important categories)

**Running:**
- Trigger: Every PR, nightly, model updates
- Duration: Fast (minutes)
- Reporting: Clear pass/fail + details

**Handling Failures:**
- Intended change → Update benchmark
- Unintended regression → Fix issue
- Flaky test → Improve stability

**Golden Set:**
- 100 most critical tests
- Always passing
- Regularly updated

**Continuous:**
- PR: Quick (100 tests)
- Nightly: Full (1000 tests)
- Model updates: Comprehensive

**Optimization:**
- Cache responses
- Parallelize execution
- Sample for fast feedback

**CI/CD:**
- Required check (block merge)
- Clear error messages
- Link to full report
