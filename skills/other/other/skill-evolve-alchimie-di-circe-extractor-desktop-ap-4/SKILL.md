---
name: skill-evolve
description: Evolve skills iteratively based on usage tracking and feedback. Use for skills used repeatedly, when failure rate exceeds 10 percent, when user feedback indicates confusion, or when building team expertise over time. Achieves 20 percent consistency improvement through iterative refinement. Triggers on "evolve skill", "improve skill iteratively", "skill evolution", "track skill performance", "refine skill".
---

# Skill Evolve

## Purpose

Convert repeated skill usage into measurable improvement. Track performance, identify failure patterns, and polish iteratively to achieve 20% consistency gain.

**Specialization:** Long-term skill evolution based on real usage data.

## When to Use

- Skill is used repeatedly (3+ times)
- Failure rate exceeds 10%
- User feedback indicates confusion
- New edge cases discovered
- Building team-specific expertise
- Tracking skill evolution over time

**When NOT to use:**
- One-off skill usage
- Initial skill creation (use skill-bootstrap)
- Session-based improvements (use skill-extract-pattern)

## Quick Start

```python
# Track usage
tracker = SkillTracker("my-skill")
tracker.log_usage(task, result)

# Analyze failures
issues = tracker.analyze_failures()

# Polish and measure
improvement = measure_evolution(before_version, after_version)
```

## Core Workflow

```
CREATE (v1.0.0) → USE (track) → ANALYZE (failures) → 
POLISH (v1.1.0) → MEASURE (impact) → REPEAT
```

## Step 1: Create Initial Skill

Use skill-bootstrap to create v1.0.0:

```bash
mkdir -p .claude/skills/my-skill

# Generate SKILL.md with skill-bootstrap
cat > .claude/skills/my-skill/SKILL.md << 'EOF'
---
name: my-skill
description: ...
---
# My Skill
[Initial implementation]
EOF

git add .claude/skills/my-skill
git commit -m "feat: add my-skill capability (v1.0.0)"
```

## Step 2: Track Usage

### Simple Tracking (JSON file)

```python
import json
from datetime import datetime

class SkillTracker:
    def __init__(self, skill_name):
        self.skill_name = skill_name
        self.log_file = f".claude/skills/{skill_name}/usage.json"
    
    def log_usage(self, task, success, issues=None, feedback=None):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'task': task,
            'success': success,
            'issues': issues or [],
            'feedback': feedback
        }
        
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
        except FileNotFoundError:
            logs = []
        
        logs.append(entry)
        
        with open(self.log_file, 'w') as f:
            json.dump(logs, f, indent=2)
    
    def get_consistency(self):
        try:
            with open(self.log_file, 'r') as f:
                logs = json.load(f)
            if not logs:
                return 0.0
            successes = sum(1 for log in logs if log['success'])
            return successes / len(logs)
        except FileNotFoundError:
            return 0.0
```

### Usage Example

```python
tracker = SkillTracker("csv-to-json")

# After each usage
tracker.log_usage(
    task="Transform users.csv to JSON",
    success=True,
    feedback="Worked perfectly"
)

# Or on failure
tracker.log_usage(
    task="Transform products.csv to JSON",
    success=False,
    issues=["encoding_error", "missing_fields"],
    feedback="Failed on UTF-16 encoding"
)
```

## Step 3: Analyze Failures

```python
def analyze_failures(skill_name):
    tracker = SkillTracker(skill_name)
    
    with open(tracker.log_file, 'r') as f:
        logs = json.load(f)
    
    failures = [log for log in logs if not log['success']]
    
    # Group by issue type
    issues_by_type = {}
    for failure in failures:
        for issue in failure['issues']:
            if issue not in issues_by_type:
                issues_by_type[issue] = []
            issues_by_type[issue].append(failure)
    
    return issues_by_type
```

**Example output:**
```
encoding_errors: 3 occurrences
missing_fields: 5 occurrences
malformed_csv: 2 occurrences
```

## Step 4: Polish Based on Data

Address highest-frequency issues first:

```bash
# Analyze
python analyze_skill.py csv-to-json
# → missing_fields: 5 occurrences (highest priority)
```

Update skill:

```markdown
## Error Handling

### Missing Fields
Validate against schema and provide defaults:

```python
required_fields = ['id', 'name', 'email']
for field in required_fields:
    if field not in df.columns:
        df[field] = None
```
```

Commit as part of regular work:

```bash
git add .claude/skills/csv-to-json/SKILL.md
git commit -m "feat: add product import endpoint
- Implement import logic
- Update csv-to-json skill with missing field handling"
```

## Step 5: Measure Improvement

```python
def measure_evolution(skill_name, before_ref, after_ref):
    """
    Compare skill performance before and after polishing
    """
    # Load logs from git history or separate tracking
    before_logs = load_logs(skill_name, before_ref)
    after_logs = load_logs(skill_name, after_ref)
    
    before_consistency = calculate_consistency(before_logs)
    after_consistency = calculate_consistency(after_logs)
    
    improvement = ((after_consistency - before_consistency) / 
                   before_consistency * 100)
    
    return {
        'before': before_consistency,
        'after': after_consistency,
        'improvement_percent': improvement
    }
```

**Target:** 20% consistency improvement per iteration cycle.

## Versioning Strategy

Semantic versioning for skills:

```bash
# MAJOR: Breaking changes
git commit -m "feat!: change required fields (BREAKING)"
# Tag: my-skill-v2.0.0

# MINOR: New features, backwards compatible
git commit -m "feat: add Excel support"
# Tag: my-skill-v1.2.0

# PATCH: Bug fixes, polishing
git commit -m "fix: handle empty CSV files"
# Tag: my-skill-v1.1.1
```

## Example: Skill Evolution

### v1.0.0 - Initial
```yaml
name: csv-to-json
description: Transform CSV to JSON
```
**Consistency: 75%**

### v1.1.0 - Error Handling
Added encoding detection and missing field handling.
**Consistency: 85%** (+10%)

### v1.2.0 - Feature Addition
Added Excel support and data cleaning.
**Consistency: 90%** (+5%)

**Total: 75% → 90% = 20% improvement**

## Polishing Priorities

1. **Fix high-frequency failures first**
2. **Improve unclear instructions**
3. **Add missing error handling**
4. **Provide better examples**
5. **Optimize performance**

## When to Polish

| Condition | Action |
|-----------|--------|
| Failure rate > 10% | Analyze and fix |
| User feedback confusion | Clarify instructions |
| New edge cases | Add handling |
| Better approaches emerge | Evaluate adoption |

## Integration with Other Skills

| Phase | Skill | Output |
|-------|-------|--------|
| Bootstrap | skill-bootstrap | v1.0.0 |
| Harden | skill-hardening | Bulletproof skill |
| Extract | skill-extract-pattern | Session-based improvements |
| **Evolve** | **skill-evolve** | **Long-term iteration** |

## Best Practices

### Keep Tracking Lightweight
- JSON file is sufficient for most cases
- Don't over-engineer tracking
- Focus on actionable data

### Polish Incrementally
- Small improvements add up
- Measure each iteration
- Revert if consistency drops

### Document Evolution
- Keep simple changelog
- Tag stable versions
- Note breaking changes

## Version

v1.0.0 (2025-01-28) - Evolution-focused refactor of skill-continuous-polishing