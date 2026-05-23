---
name: experience-library
description: Capture task outcomes, score performance, and derive rules as token priors for continual learning without model weight changes. Use for post-task feedback, experience capture, pattern extraction, and learning from mistakes. Achieves continual learning for $18 per 100 samples vs $10k fine-tune cost. Triggers on "learn from experience", "capture patterns", "post-task analysis", "continual learning", "experience extraction".
---

# Experience Library Update

## Purpose

Sample task answers, score outcomes, and derive rules as token priors - achieving continual learning for $18/100 samples vs $10k fine-tune cost, without changing model weights.

## When to Use

- Post-task learning and improvement
- Capturing successful patterns
- Learning from failures
- Tool call optimization
- Building domain expertise over time
- Pattern extraction from experience

## Core Instructions

### Pattern: Experience Capture Loop

```python
def update_experience_library(task, answer, outcome):
    """
    Capture and learn from task experience
    """
    # 1. Score the outcome
    score = evaluate_outcome(answer, outcome)

    # 2. Extract patterns if successful
    if score > threshold:
        pattern = extract_pattern(task, answer)
        library.add_rule(pattern)

    # 3. Use as token prior (no weight changes)
    return library.get_relevant_rules(new_task)
```

### Step 1: Score Task Outcome

```python
def evaluate_outcome(answer, outcome):
    """
    Score how well the task was completed

    Returns:
        float: Score from 0.0 (failed) to 1.0 (perfect)
    """
    metrics = {
        'correctness': check_correctness(answer, outcome),
        'efficiency': measure_efficiency(answer),
        'completeness': check_completeness(answer, outcome)
    }

    # Weighted average
    score = (
        metrics['correctness'] * 0.5 +
        metrics['efficiency'] * 0.3 +
        metrics['completeness'] * 0.2
    )

    return score
```

### Step 2: Extract Patterns

```python
def extract_pattern(task, answer):
    """
    Extract reusable pattern from successful task
    """
    pattern = {
        'task_type': classify_task(task),
        'approach': extract_approach(answer),
        'tools_used': extract_tools(answer),
        'context': extract_context(task),
        'success_factors': analyze_success(answer),
        'applicable_to': generalize_pattern(task)
    }

    return pattern
```

### Step 3: Store as Token Prior

```python
class ExperienceLibrary:
    """
    Library of learned patterns (token-based, not model weights)
    """
    def __init__(self):
        self.patterns = []

    def add_rule(self, pattern):
        """Add successful pattern"""
        self.patterns.append({
            'pattern': pattern,
            'timestamp': datetime.now(),
            'usage_count': 0,
            'success_rate': 1.0
        })

    def get_relevant_rules(self, new_task):
        """
        Retrieve patterns relevant to new task
        Returns as token context (not model update)
        """
        task_type = classify_task(new_task)

        relevant = [
            p for p in self.patterns
            if task_type in p['pattern']['applicable_to']
        ]

        # Sort by success rate
        relevant.sort(
            key=lambda x: x['success_rate'],
            reverse=True
        )

        return relevant[:5]  # Top 5 patterns
```

### Step 4: Apply to New Tasks

```python
def execute_with_experience(new_task, library):
    """
    Execute task using learned patterns
    """
    # 1. Get relevant patterns
    patterns = library.get_relevant_rules(new_task)

    # 2. Inject as context (token prior)
    context = format_patterns_as_context(patterns)

    # 3. Execute task with learned context
    result = execute_task(new_task, context=context)

    # 4. Update pattern statistics
    for pattern in patterns:
        pattern['usage_count'] += 1
        if result.success:
            pattern['success_rate'] = update_success_rate(pattern)

    return result
```

## Example Workflow

### Initial Task (No Experience)

```python
task = "Extract data from JSON API"
answer = execute_task(task)
outcome = {"success": True, "time": 5.2}

# Score and capture
score = evaluate_outcome(answer, outcome)  # 0.85
if score > 0.7:
    pattern = extract_pattern(task, answer)
    library.add_rule(pattern)
```

**Extracted Pattern:**
```python
{
    'task_type': 'api_data_extraction',
    'approach': 'use_requests_with_retry',
    'tools_used': ['requests', 'json'],
    'success_factors': [
        'retry_logic',
        'timeout_handling',
        'error_checking'
    ],
    'applicable_to': [
        'api_data_extraction',
        'rest_api_calls',
        'json_parsing'
    ]
}
```

### Similar Task Later (With Experience)

```python
new_task = "Fetch user data from REST API"
# Library automatically provides relevant patterns
patterns = library.get_relevant_rules(new_task)

# Claude receives patterns as token context:
# "Previous successful approach:
#  - Use requests with retry logic
#  - Handle timeouts (30s)
#  - Validate JSON response
#  - Check status codes"

# Execute with learned context
result = execute_with_experience(new_task, library)
# Faster, more reliable due to learned patterns
```

## Performance Characteristics

| Approach | Cost | Time | Permanence |
|----------|------|------|------------|
| Fine-tuning | $10,000 | Days | Permanent (model weights) |
| Experience Library | $18/100 samples | Minutes | Session-based (token context) |

**Advantages of Token Priors:**
- **Cost**: 555x cheaper ($18 vs $10,000)
- **Speed**: Minutes vs days
- **Flexibility**: Easy to update/remove patterns
- **No model changes**: Works with any Claude version
- **Transparency**: Patterns are human-readable

**Trade-offs:**
- Token cost per request (small, ~100-200 tokens)
- Not permanent across sessions (unless persisted)
- Requires pattern storage and retrieval system

## Pattern Storage

```python
# Save patterns to disk
import json

def save_library(library, filename='experience_library.json'):
    """Persist patterns"""
    with open(filename, 'w') as f:
        json.dump(library.patterns, f, default=str)

def load_library(filename='experience_library.json'):
    """Load patterns"""
    library = ExperienceLibrary()
    with open(filename) as f:
        library.patterns = json.load(f)
    return library
```

## Best Practices

### Pattern Quality
- Only store patterns from successful tasks (score > 0.7)
- Include context: task type, tools, environment
- Generalize appropriately (not too specific, not too vague)
- Update success rates based on actual usage

### Pattern Pruning
- Remove low-performing patterns (success_rate < 0.5)
- Merge similar patterns to reduce redundancy
- Keep library size manageable (<100 patterns)

### Context Injection
- Top 5 most relevant patterns per task
- Format as clear, actionable guidance
- Include success factors and pitfalls

## Version

v1.0.0 (2025-10-23) - Based on meta-learning and ReAct optimization patterns

