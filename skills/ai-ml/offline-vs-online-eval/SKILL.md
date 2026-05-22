---
name: Offline vs Online Evaluation
description: Comprehensive guide to offline and online evaluation strategies including A/B testing, shadow mode, canary deployments, and bridging offline-online metrics
---

# Offline vs Online Evaluation

## Definitions

### Offline Evaluation
**Test on static dataset before deployment**
```
Dataset: Ground truth test set (fixed)
When: During development
Metrics: Accuracy, F1, BLEU, RAG metrics
Environment: Development/staging
```

### Online Evaluation
**Measure in production with real users**
```
Dataset: Live traffic (dynamic)
When: In production
Metrics: User satisfaction, task success, engagement
Environment: Production
```

---

## Why Both Matter

### Offline: Fast Iteration, Controlled Testing
```
Pros:
- Fast (minutes to hours)
- Reproducible (same dataset)
- Safe (no user impact)
- Cheap (no production traffic)

Use for:
- Rapid development
- Comparing models
- Regression testing
```

### Online: Real-World Performance, Actual User Impact
```
Pros:
- Real performance (actual users)
- Actual impact (business metrics)
- Catches issues offline can't (latency, UX)

Use for:
- Final validation
- Measuring business impact
- Continuous monitoring
```

### Need Both for Complete Picture
```
Offline: "Model A is 5% more accurate"
Online: "Model A increases user satisfaction by 10%"

Both needed to make informed decisions
```

---

## Offline Evaluation

### When
During development, before deployment

### Dataset
Ground truth test set (500-5000 examples)

### Metrics
- **Accuracy:** % correct
- **F1 Score:** Precision + recall
- **BLEU/ROUGE:** Generation quality
- **RAG Metrics:** Faithfulness, relevance

### Pros
- **Fast:** Evaluate 1000 examples in minutes
- **Reproducible:** Same dataset → same results
- **Safe:** No user impact
- **Cheap:** No production costs

### Cons
- **May not reflect real performance:** Test set ≠ production
- **Missing context:** No user behavior, latency, UX
- **Dataset drift:** Production changes over time

### Process
```
1. Create evaluation dataset (ground truth)
2. Run model on dataset
3. Compute metrics
4. Compare to baseline
5. Iterate until metrics improve
6. Deploy to production
```

---

## Online Evaluation

### When
In production with real users

### Dataset
Live traffic (actual user queries)

### Metrics
- **User satisfaction:** Thumbs up/down, ratings
- **Task success:** Did user achieve goal?
- **Engagement:** Click-through rate, time on page
- **Efficiency:** Time to complete, steps needed
- **Safety:** Violations, flags, escalations

### Pros
- **Real performance:** Actual users, actual queries
- **Actual impact:** Business metrics (revenue, retention)
- **Catches real issues:** Latency, UX, edge cases

### Cons
- **Slower:** Need traffic, statistical significance
- **Risky:** Bad model affects real users
- **Requires traffic:** Can't test without users

### Methods
- A/B testing
- Shadow mode
- Canary deployment
- Interleaving

---

## Online Evaluation Methods

### A/B Testing (Two Variants)

**Setup:**
```
Control (A): Current model (50% of users)
Treatment (B): New model (50% of users)

Random assignment of users
Measure metrics for both
Statistical significance test
Ship winner
```

**Example:**
```python
import random

def assign_variant(user_id):
    if hash(user_id) % 2 == 0:
        return "A"  # Control
    else:
        return "B"  # Treatment

# Serve model based on variant
variant = assign_variant(user_id)
if variant == "A":
    answer = model_a.predict(question)
else:
    answer = model_b.predict(question)

# Log result
log_result(user_id, variant, question, answer, user_feedback)
```

**Statistical Significance:**
```python
from scipy.stats import ttest_ind

satisfaction_a = [4, 5, 3, 4, 5, ...]  # User ratings for A
satisfaction_b = [5, 5, 4, 5, 4, ...]  # User ratings for B

t_stat, p_value = ttest_ind(satisfaction_a, satisfaction_b)

if p_value < 0.05:
    print("Statistically significant difference!")
    if mean(satisfaction_b) > mean(satisfaction_a):
        print("Ship variant B")
else:
    print("No significant difference")
```

### Shadow Mode (Log but Don't Serve)

**Setup:**
```
Production: Serve model A (current)
Shadow: Run model B in background (don't serve)
Compare: Model B predictions vs model A predictions
No user impact: Users only see model A
```

**Example:**
```python
# Serve current model
answer_a = model_a.predict(question)
serve_to_user(answer_a)

# Run new model in shadow mode (async)
async def shadow_predict():
    answer_b = model_b.predict(question)
    log_shadow_result(question, answer_a, answer_b)
    
    # Compare
    if answer_a != answer_b:
        log_difference(question, answer_a, answer_b)

asyncio.create_task(shadow_predict())
```

**Benefits:**
- No user impact (safe)
- Real production traffic
- Can compare models directly

### Canary Deployment (Small % of Traffic)

**Setup:**
```
1. Deploy new model to 1% of traffic
2. Monitor closely (errors, latency, satisfaction)
3. If good, increase to 5%
4. Gradually increase to 100%
5. Rollback if issues
```

**Example:**
```python
def get_model(user_id):
    # Canary: 5% of users get new model
    if hash(user_id) % 100 < 5:
        return model_b  # New model (canary)
    else:
        return model_a  # Current model

model = get_model(user_id)
answer = model.predict(question)

# Monitor metrics
monitor_metrics(model_version=model.version, user_id=user_id)
```

**Rollback:**
```python
# If error rate > 5% for canary
if canary_error_rate > 0.05:
    rollback_to_previous_version()
    alert_team("Canary deployment failed")
```

### Interleaving (Mix Results)

**Setup:**
```
Show results from both models, interleaved
Track which results users click
Infer which model is better
```

**Example (Search Ranking):**
```
Model A results: [R1_A, R2_A, R3_A, R4_A]
Model B results: [R1_B, R2_B, R3_B, R4_B]

Interleaved: [R1_A, R1_B, R2_A, R2_B, R3_A, R3_B]

User clicks: R1_B, R2_A
→ Model B: 1 click, Model A: 1 click
```

---

## Online Metrics

### Engagement
- **Click-through rate (CTR):** % of users who click
- **Time on page:** How long users stay
- **Pages per session:** How many pages viewed
- **Bounce rate:** % who leave immediately

### Satisfaction
- **Thumbs up/down:** Explicit feedback
- **Star ratings:** 1-5 scale
- **NPS (Net Promoter Score):** "Would you recommend?"
- **CSAT (Customer Satisfaction):** "How satisfied are you?"

### Task Success
- **Completion rate:** % who complete task
- **Success rate:** % who achieve goal
- **Retry rate:** % who retry query
- **Abandonment rate:** % who give up

### Efficiency
- **Time to complete:** How long to finish task
- **Steps needed:** How many interactions
- **Query reformulations:** How many retries

### Safety
- **Violation rate:** % of harmful outputs
- **Flag rate:** % of flagged responses
- **Escalation rate:** % requiring human intervention

---

## Implicit Signals

### Did User Click Result? (Relevance)
```
User clicks result → Likely relevant
User doesn't click → Likely not relevant
```

### Did User Reformulate Query? (Dissatisfaction)
```
User reformulates → Dissatisfied with answer
User doesn't reformulate → Satisfied
```

### Did User Abandon? (Failure)
```
User abandons → Failed to help
User continues → Successful
```

### Session Length (Engagement)
```
Long session → Engaged
Short session → Not engaged (or very efficient)
```

---

## Explicit Feedback

### Thumbs Up/Down
```python
feedback = {
    "question": "What is the capital of France?",
    "answer": "Paris",
    "feedback": "thumbs_up",  # or "thumbs_down"
    "timestamp": "2024-01-15T10:00:00Z"
}

# Aggregate
thumbs_up_rate = thumbs_up / (thumbs_up + thumbs_down)
```

### Star Ratings (1-5)
```python
rating = {
    "question": "What is the capital of France?",
    "answer": "Paris",
    "rating": 5,  # 1-5 scale
    "timestamp": "2024-01-15T10:00:00Z"
}

# Aggregate
avg_rating = sum(ratings) / len(ratings)
```

### Written Feedback
```python
feedback = {
    "question": "What is the capital of France?",
    "answer": "Paris",
    "feedback_text": "Perfect answer, very helpful!",
    "timestamp": "2024-01-15T10:00:00Z"
}

# Analyze sentiment
sentiment = analyze_sentiment(feedback_text)
```

### Bug Reports
```python
bug_report = {
    "question": "What is the capital of France?",
    "answer": "Lyon",  # Incorrect
    "issue": "Incorrect answer",
    "timestamp": "2024-01-15T10:00:00Z"
}

# Track and fix
add_to_ground_truth(question, correct_answer="Paris")
```

---

## Bridging Offline and Online

### Offline Metrics Should Correlate with Online
```
Hypothesis: Higher offline accuracy → Higher online satisfaction

Test:
- Model A: 85% offline accuracy → 75% thumbs up
- Model B: 90% offline accuracy → 80% thumbs up

Correlation: ✓ Offline predicts online
```

### Validate Offline Improvements Lead to Online Gains
```
Process:
1. Improve offline metric (85% → 90% accuracy)
2. Deploy to production (A/B test)
3. Measure online metric (75% → 80% thumbs up)
4. If online improves → Offline metric is good proxy
5. If online doesn't improve → Offline metric is misleading
```

### Offline for Filtering, Online for Final Decision
```
Workflow:
1. Offline: Test 10 model variants
2. Filter: Keep top 3 (based on offline metrics)
3. Online: A/B test top 3
4. Ship: Best performer online
```

---

## When Offline and Online Disagree

### Example
```
Offline: Model A is better (90% vs 85% accuracy)
Online: Model B performs better (80% vs 75% thumbs up)
```

### Possible Reasons

**Dataset Not Representative:**
```
Test set: Simple questions
Production: Complex, ambiguous questions
→ Test set doesn't match reality
```

**Metric Doesn't Capture What Matters:**
```
Offline: Accuracy (correct answer)
Online: Helpfulness (useful answer)
→ Correct ≠ helpful
```

**User Behavior Differs from Test Set:**
```
Test set: Factual questions
Production: Conversational queries
→ Different use cases
```

### Trust Online (But Investigate Why)
```
Online metrics = actual user impact
→ Trust online

But investigate:
- Why did offline mislead?
- Update offline dataset/metrics
- Improve offline-online correlation
```

---

## Continuous Evaluation

### Log All Predictions + Outcomes
```python
log_entry = {
    "timestamp": "2024-01-15T10:00:00Z",
    "question": "What is the capital of France?",
    "answer": "Paris",
    "model_version": "v1.2.0",
    "latency_ms": 250,
    "user_feedback": "thumbs_up",
    "user_id": "user123"
}

db.logs.insert(log_entry)
```

### Offline Eval on Recent Data
```python
# Weekly: Evaluate on last week's data
recent_data = db.logs.find({
    "timestamp": {"$gte": one_week_ago}
}).limit(1000)

# Evaluate
results = evaluate_model(recent_data)

# Compare to baseline
if results["accuracy"] < baseline_accuracy - 0.05:
    alert("Model performance degraded!")
```

### Online Eval via A/B Tests
```
Monthly: A/B test new model variant
Measure: User satisfaction, task success
Ship: If statistically significant improvement
```

### Monitor Metrics Dashboard
```
Dashboard:
- Offline metrics (accuracy, F1)
- Online metrics (thumbs up rate, task success)
- Latency (P50, P95, P99)
- Error rate
- Traffic volume

Alerts:
- Accuracy drops >5%
- Thumbs up rate drops >10%
- Latency P95 >1s
- Error rate >1%
```

---

## Guardrails for Online Eval

### Automated Rollback (If Metrics Drop)
```python
def monitor_canary():
    while True:
        metrics = get_canary_metrics()
        
        if metrics["error_rate"] > 0.05:
            rollback()
            alert("High error rate, rolled back")
        
        if metrics["thumbs_down_rate"] > 0.3:
            rollback()
            alert("High dissatisfaction, rolled back")
        
        time.sleep(60)  # Check every minute
```

### Manual Review (Before Wide Rollout)
```
Process:
1. Canary to 1% (automated)
2. Monitor for 24 hours
3. Manual review (check logs, user feedback)
4. If good, increase to 10%
5. Repeat until 100%
```

### Sampling (Don't Test on All Traffic)
```
Start small:
- 1% canary (low risk)
- Monitor closely
- Gradually increase
- Never test unproven model on 100% traffic
```

### Reversibility (Easy to Revert)
```
Feature flags:
- Easy to turn off new model
- Instant rollback
- No code deployment needed
```

---

## Offline-to-Online Workflow

### 1. Develop: Offline Eval on Test Set
```
Iterate on model
Evaluate on test set (1000 examples)
Improve until offline metrics good
```

### 2. Validate: Shadow Mode (Offline on Live Traffic)
```
Run in shadow mode (1 week)
Evaluate on live traffic (offline metrics)
Compare to current model
```

### 3. Test: Canary to 1% (Online, Minimal Risk)
```
Deploy to 1% of users
Monitor online metrics (24 hours)
If good, proceed
```

### 4. Expand: Gradual Rollout to 100%
```
1% → 5% → 10% → 25% → 50% → 100%
Monitor at each step
Rollback if issues
```

### 5. Monitor: Continuous Online Evaluation
```
Track metrics in production
Detect regressions
A/B test improvements
```

---

## Real-World Examples

### Search Ranking
```
Offline: NDCG@10 (ranking quality)
Online: Click-through rate (CTR)

Correlation: High NDCG → High CTR
```

### Recommendation
```
Offline: Precision@k, recall@k
Online: Engagement (clicks, watch time)

Correlation: High precision → High engagement
```

### RAG
```
Offline: Faithfulness, relevance
Online: Thumbs up rate, task success

Correlation: High faithfulness → High thumbs up
```

---

## Tools

### Offline
- Custom scripts
- Evaluation frameworks (RAGAS, DeepEval)
- Jupyter notebooks

### Online
- Experimentation platforms (Optimizely, LaunchDarkly)
- Analytics (Google Analytics, Mixpanel)
- APM (Datadog, New Relic)

### Both
- MLOps platforms (MLflow, Weights & Biases)
- Feature flags (LaunchDarkly, Split)
- Monitoring (Prometheus, Grafana)

---

## Summary

**Offline:** Test on static dataset (fast, safe, reproducible)
**Online:** Test in production (real performance, actual impact)

**Need Both:**
- Offline for rapid iteration
- Online for final validation

**Offline Pros:**
- Fast, safe, cheap, reproducible

**Online Pros:**
- Real performance, actual impact

**Online Methods:**
- A/B testing (compare variants)
- Shadow mode (no user impact)
- Canary (gradual rollout)

**Online Metrics:**
- Engagement, satisfaction, task success, efficiency, safety

**Bridging:**
- Offline should correlate with online
- Validate improvements
- Offline for filtering, online for decision

**Workflow:**
1. Develop (offline)
2. Validate (shadow mode)
3. Test (canary 1%)
4. Expand (gradual rollout)
5. Monitor (continuous)

**Guardrails:**
- Automated rollback
- Manual review
- Sampling
- Reversibility
