---
name: continuous-skill-polishing
description: Convert repeated tasks into versioned skills, track performance gaps, and iteratively polish through Git version control. Use for identifying repeated patterns, improving skill consistency, tracking skill evolution, and addressing failure cases. Achieves 20% consistency improvement through iterative refinement. Triggers on "improve skill", "polish skill", "repeated task", "skill evolution", "version skill", "refine pattern".
---

# Continuous Skill Polishing

## Purpose

Convert repeated tasks into skills, version control them in Git, and polish iteratively based on usage feedback to achieve 20% consistency gain.

## When to Use

- Identifying repeated task patterns
- Improving skill consistency
- Addressing skill failure cases
- Tracking skill evolution over time
- Refining based on user feedback
- Building team-specific expertise

## Core Instructions

### Step 1: Identify Repeated Task

```python
def identify_repeated_tasks(task_history):
    """
    Analyze task history to find repeated patterns
    """
    # Cluster similar tasks
    clusters = cluster_tasks_by_similarity(task_history)

    # Find clusters with multiple instances
    repeated = [
        cluster for cluster in clusters
        if len(cluster) >= 3  # Repeated 3+ times
    ]

    return repeated


def should_create_skill(task_cluster):
    """
    Determine if cluster warrants a skill
    """
    criteria = {
        'frequency': len(task_cluster) >= 3,  # Repeated often
        'consistency': has_consistent_pattern(task_cluster),  # Similar approach
        'complexity': is_sufficiently_complex(task_cluster),  # Not trivial
        'value': provides_reusable_value(task_cluster)  # Worth capturing
    }

    return all(criteria.values())
```

### Step 2: Create Initial Skill

```bash
# Identify repeated task
task="Transform CSV to JSON with validation"

# Create skill directory
mkdir -p .claude/skills/csv-to-json-transformer

# Generate initial SKILL.md
cat > .claude/skills/csv-to-json-transformer/SKILL.md << 'EOF'
---
name: csv-to-json-transformer
description: Transform CSV files to JSON with schema validation...
---

# CSV to JSON Transformer

[Initial implementation based on repeated pattern]
EOF

# Version control
git add .claude/skills/csv-to-json-transformer
git commit -m "feat: add csv-to-json-transformer skill (v1.0.0)"
```

### Step 3: Track Usage and Failures

```python
class SkillTracker:
    """Track skill usage and performance"""

    def __init__(self, skill_name):
        self.skill_name = skill_name
        self.usage_log = []

    def log_usage(self, task, result):
        """Log each skill usage"""
        self.usage_log.append({
            'timestamp': datetime.now(),
            'task': task,
            'success': result.success,
            'issues': result.issues,
            'feedback': result.user_feedback
        })

    def analyze_failures(self):
        """Identify patterns in failures"""
        failures = [
            log for log in self.usage_log
            if not log['success']
        ]

        # Group by issue type
        issues_by_type = {}
        for failure in failures:
            for issue in failure['issues']:
                issue_type = classify_issue(issue)
                if issue_type not in issues_by_type:
                    issues_by_type[issue_type] = []
                issues_by_type[issue_type].append(failure)

        return issues_by_type

    def calculate_consistency(self):
        """Calculate skill consistency score"""
        if not self.usage_log:
            return 0.0

        successes = sum(1 for log in self.usage_log if log['success'])
        return successes / len(self.usage_log)
```

### Step 4: Polish Based on Feedback

```bash
# Analyze failure patterns
python analyze_skill.py csv-to-json-transformer

# Output:
# Issue type: encoding_errors (3 occurrences)
# Issue type: missing_fields (5 occurrences)
# Issue type: malformed_csv (2 occurrences)

# Update skill to address issues
cat >> .claude/skills/csv-to-json-transformer/SKILL.md << 'EOF'

## Error Handling

### Encoding Issues
Handle various encodings (UTF-8, Latin-1, etc.):
```python
encodings = ['utf-8', 'latin-1', 'cp1252']
for encoding in encodings:
    try:
        df = pd.read_csv(file, encoding=encoding)
        break
    except UnicodeDecodeError:
        continue
```

### Missing Fields
Validate against schema and provide defaults:
```python
required_fields = ['id', 'name', 'email']
for field in required_fields:
    if field not in df.columns:
        df[field] = None  # or default value
```
EOF

# Version control the improvement
git add .claude/skills/csv-to-json-transformer/SKILL.md
git commit -m "polish: improve error handling for encoding and missing fields"
git tag csv-to-json-v1.1.0
```

### Step 5: Measure Improvement

```python
def measure_polish_impact(skill_name, before_version, after_version):
    """
    Compare skill performance before and after polishing
    """
    before_logs = load_usage_logs(skill_name, before_version)
    after_logs = load_usage_logs(skill_name, after_version)

    before_consistency = calculate_consistency(before_logs)
    after_consistency = calculate_consistency(after_logs)

    improvement = ((after_consistency - before_consistency) /
                   before_consistency * 100)

    return {
        'before': before_consistency,
        'after': after_consistency,
        'improvement_percent': improvement
    }

# Example output:
# {
#     'before': 0.75,  # 75% success rate
#     'after': 0.90,   # 90% success rate
#     'improvement_percent': 20.0  # 20% improvement
# }
```

## Polish Workflow

```
1. CREATE
   └─> Initial skill from repeated pattern
       └─> Git commit: "feat: add skill (v1.0.0)"

2. USE
   └─> Apply skill to tasks
       └─> Track successes and failures

3. ANALYZE
   └─> Identify failure patterns
       └─> Group by issue type
       └─> Prioritize most common issues

4. POLISH
   └─> Update skill to address issues
       └─> Add error handling
       └─> Improve instructions
       └─> Add examples
       └─> Git commit: "polish: [specific improvement]"

5. MEASURE
   └─> Compare before/after consistency
       └─> If improved: keep changes
       └─> If worse: revert and try different approach

6. REPEAT
   └─> Continue polishing based on new feedback
```

## Versioning Strategy

```bash
# Semantic versioning for skills
# v[MAJOR].[MINOR].[PATCH]

# MAJOR: Breaking changes to skill interface
git commit -m "feat!: change required fields (BREAKING CHANGE)"
git tag csv-to-json-v2.0.0

# MINOR: New features, backwards compatible
git commit -m "feat: add Excel support"
git tag csv-to-json-v1.2.0

# PATCH: Bug fixes, polishing
git commit -m "fix: handle empty CSV files"
git tag csv-to-json-v1.1.1
```

## Example: Skill Evolution

### v1.0.0 - Initial
```yaml
---
name: csv-to-json-transformer
description: Transform CSV to JSON
---
# Basic CSV to JSON transformation
```
**Consistency: 75%**

### v1.1.0 - Error Handling Polish
```yaml
---
name: csv-to-json-transformer
description: Transform CSV to JSON with encoding detection and validation
---
# CSV to JSON with error handling
- Handle multiple encodings
- Validate required fields
```
**Consistency: 85%** (+10%)

### v1.2.0 - Feature Addition
```yaml
---
name: csv-to-json-transformer
description: Transform CSV/Excel to JSON with schema validation and data cleaning
---
# CSV/Excel to JSON
- Multiple format support
- Schema validation
- Data cleaning and normalization
```
**Consistency: 90%** (+5%)

**Total improvement: v1.0.0 → v1.2.0 = 20% consistency gain**

## Best Practices

### When to Create a Skill
- Task repeated 3+ times
- Consistent approach across instances
- Sufficiently complex (not trivial)
- Provides reusable value

### When to Polish
- Failure rate > 10%
- User feedback indicates confusion
- New edge cases discovered
- Competing better approaches emerge

### Polishing Priorities
1. Fix high-frequency failures first
2. Improve unclear instructions
3. Add missing error handling
4. Provide better examples
5. Optimize performance

### Git Workflow
- Use feature branches for major changes
- Tag stable versions
- Keep CHANGELOG.md updated
- Document breaking changes

## Performance Characteristics

- **20% consistency improvement** through iterative polishing
- **Git version history** provides complete evolution trail
- **Measurable progress** via before/after metrics
- **Team collaboration** through shared skill repository

## Version

v1.0.0 (2025-10-23) - Based on skill evolution patterns

