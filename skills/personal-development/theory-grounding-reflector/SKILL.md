---
name: theory-grounding-reflector
description: Extract lessons from task failures using Reflector agent, merge insights via Curator pattern, achieving 10% accuracy improvement without context collapse. Use for post-failure analysis, lesson extraction, self-improvement, and building resilience. Analyzes what went wrong and formulates actionable lessons. Triggers on "learn from failure", "analyze mistake", "reflect on error", "post-mortem", "failure analysis", "what went wrong".
---

# Theory Grounding via Reflector

## Purpose

Reflector agent extracts lessons from task failures, Curator merges insights as delta items, achieving 10% accuracy improvement without context collapse through structured reflection.

## When to Use

- Analyzing task failures
- Learning from mistakes
- Post-mortem analysis
- Self-improvement loops
- Building failure resistance
- Extracting actionable lessons

## Core Instructions

### Reflector Agent Pattern

The Reflector analyzes failures and extracts lessons:

```python
class Reflector:
    """
    Agent that reflects on failures and extracts lessons
    """

    def analyze_failure(self, task, attempt, outcome):
        """
        Analyze what went wrong and why

        Returns:
            Lesson object with root cause and improvement
        """
        # 1. Identify what went wrong
        error_pattern = self.identify_error(attempt, outcome)

        # 2. Determine root cause
        root_cause = self.find_root_cause(error_pattern, task)

        # 3. Formulate lesson
        lesson = self.formulate_lesson(root_cause, task)

        return lesson

    def identify_error(self, attempt, outcome):
        """Classify the type of error"""
        if outcome.status == 'timeout':
            return 'performance_issue'
        elif outcome.status == 'incorrect_result':
            return 'logic_error'
        elif outcome.status == 'exception':
            return 'implementation_error'
        else:
            return 'unknown_error'

    def find_root_cause(self, error_pattern, task):
        """Dig deeper to find root cause"""
        # Analyze task context
        context = analyze_task_context(task)

        # Map error pattern to root cause
        root_causes = {
            'performance_issue': self.analyze_performance(task, context),
            'logic_error': self.analyze_logic(task, context),
            'implementation_error': self.analyze_implementation(task, context)
        }

        return root_causes.get(error_pattern, 'unknown')

    def formulate_lesson(self, root_cause, task):
        """Create actionable lesson"""
        return {
            'category': root_cause['category'],
            'what_happened': root_cause['description'],
            'why_it_happened': root_cause['cause'],
            'how_to_prevent': root_cause['prevention'],
            'applicable_to': generalize_lesson(task),
            'confidence': root_cause['confidence']
        }
```

### Curator Agent Pattern

The Curator manages and merges lessons:

```python
class Curator:
    """
    Agent that merges lessons without context collapse
    """

    def __init__(self, max_lessons=50):
        self.lessons = []
        self.max_lessons = max_lessons

    def merge_lesson(self, new_lesson):
        """
        Add lesson as delta item (no full context reload)
        """
        # Check for duplicate lessons
        similar = self.find_similar_lessons(new_lesson)

        if similar:
            # Merge with existing lesson
            merged = self.merge_similar(similar[0], new_lesson)
            self.update_lesson(similar[0], merged)
        else:
            # Add as new lesson
            self.lessons.append(new_lesson)

        # Prune if needed
        if len(self.lessons) > self.max_lessons:
            self.prune_low_value_lessons()

    def find_similar_lessons(self, lesson):
        """Find lessons with similar patterns"""
        similar = []
        for existing in self.lessons:
            similarity = calculate_similarity(lesson, existing)
            if similarity > 0.8:
                similar.append(existing)
        return similar

    def prune_low_value_lessons(self):
        """
        Remove least valuable lessons to prevent context collapse
        """
        # Sort by: confidence * applicability * recency
        self.lessons.sort(
            key=lambda l: l['confidence'] * len(l['applicable_to']) * l['recency'],
            reverse=True
        )

        # Keep only top lessons
        self.lessons = self.lessons[:self.max_lessons]
```

## Example Workflow

### Failure Occurs

```python
task = "Extract user emails from API response"
attempt = """
response = requests.get(api_url)
emails = response.json()['users']['email']  # KeyError!
"""
outcome = {
    'status': 'exception',
    'error': "KeyError: 'email'",
    'success': False
}
```

### Reflector Analyzes

```python
reflector = Reflector()
lesson = reflector.analyze_failure(task, attempt, outcome)

# Output:
{
    'category': 'data_structure_assumption',
    'what_happened': 'KeyError when accessing email field',
    'why_it_happened': 'Assumed nested structure without validation',
    'how_to_prevent': [
        'Validate response structure first',
        'Use .get() with defaults',
        'Check API documentation for actual structure'
    ],
    'applicable_to': [
        'api_data_extraction',
        'json_parsing',
        'dict_access'
    ],
    'confidence': 0.9
}
```

### Curator Merges

```python
curator = Curator()
curator.merge_lesson(lesson)

# Lesson stored as delta item (minimal tokens)
# No full context reload required
```

### Next Similar Task

```python
new_task = "Extract phone numbers from API response"

# Curator provides relevant lessons as context
relevant_lessons = curator.get_relevant_lessons(new_task)

# Claude receives:
# "Lesson from previous failure:
#  When accessing API data:
#  - Validate response structure first
#  - Use .get() method with defaults
#  - Don't assume nested structures"

# Result: Improved approach
result = """
response = requests.get(api_url)
data = response.json()
users = data.get('users', [])
phones = [user.get('phone') for user in users if 'phone' in user]
"""
# Success! Lesson applied.
```

## Reflection Framework

### Step 1: Capture Failure Context

```python
def capture_failure_context(task, attempt, outcome):
    """Capture complete failure context"""
    return {
        'task': {
            'description': task.description,
            'type': task.type,
            'complexity': task.complexity
        },
        'attempt': {
            'code': attempt.code,
            'approach': attempt.approach,
            'tools_used': attempt.tools
        },
        'outcome': {
            'status': outcome.status,
            'error': outcome.error,
            'partial_results': outcome.partial_results
        },
        'environment': {
            'context_available': get_context(),
            'constraints': get_constraints()
        }
    }
```

### Step 2: Perform Root Cause Analysis

```python
def root_cause_analysis(failure_context):
    """
    5 Whys technique for root cause
    """
    current = failure_context['outcome']['error']
    whys = []

    for i in range(5):
        why = ask_why(current, failure_context)
        whys.append(why)
        if is_root_cause(why):
            break
        current = why

    return {
        'surface_error': failure_context['outcome']['error'],
        'investigation': whys,
        'root_cause': whys[-1]
    }
```

### Step 3: Formulate Actionable Lesson

```python
def formulate_actionable_lesson(root_cause, failure_context):
    """
    Create specific, actionable lesson
    """
    lesson = {
        'title': generate_lesson_title(root_cause),
        'category': classify_lesson(root_cause),
        'description': describe_what_happened(failure_context),
        'prevention': [
            generate_prevention_step(root_cause, i)
            for i in range(3)
        ],
        'detection': generate_early_detection(root_cause),
        'examples': generate_examples(root_cause, failure_context),
        'applicability': determine_applicability(failure_context)
    }

    return lesson
```

## Performance Characteristics

| Metric | Without Reflection | With Reflection | Improvement |
|--------|-------------------|-----------------|-------------|
| Accuracy | Baseline | +10% | 10% improvement |
| Context size | Growing | Stable | No collapse |
| Learning rate | Slow | Fast | Accelerated |
| Mistake repetition | High | Low | Reduced |

**Key benefits:**
- **10% accuracy gain** from structured learning
- **No context collapse** via delta updates
- **Fast learning** from failures
- **Persistent improvement** across sessions

## Best Practices

### Reflection Quality
- Analyze root cause, not just symptoms
- Be specific in lessons
- Include prevention strategies
- Test lessons on similar tasks

### Curator Management
- Limit total lessons (50-100 max)
- Prune low-value lessons regularly
- Merge similar lessons
- Track lesson effectiveness

### Lesson Application
- Provide relevant lessons as context
- Don't overload with all lessons
- Update lesson confidence based on usage
- Remove ineffective lessons

## Integration Pattern

```python
def execute_task_with_reflection(task):
    """
    Task execution with reflection loop
    """
    try:
        # Execute task
        result = execute(task)

        if result.success:
            return result
        else:
            # Failure: activate reflection
            lesson = reflector.analyze_failure(task, result.attempt, result.outcome)
            curator.merge_lesson(lesson)

            # Optionally retry with lesson
            relevant_lessons = curator.get_relevant_lessons(task)
            return execute(task, context=relevant_lessons)

    except Exception as e:
        # Unexpected failure
        lesson = reflector.analyze_exception(task, e)
        curator.merge_lesson(lesson)
        raise
```

## Version

v1.0.0 (2025-10-23) - Based on self-improving agent patterns

