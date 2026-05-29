---
name: usage-optimization
version: "1.0.0"
category: ai
description: "Usage Optimization Skill"
---

# Usage Optimization Skill

> Version: 1.0.0
> Category: Optimization
> Triggers: High usage alerts, efficiency improvements, batch operations

## Quick Reference

### Effectiveness Ratings

| Approach | Rating | Time Saved |
|----------|--------|------------|
| Script + AI Input + AI Command | ⭐⭐⭐⭐⭐ | 90% |
| Git Operations (Claude) | ⭐⭐⭐⭐⭐ | 80% |
| Script + Input File | ⭐⭐⭐⭐ | 70% |
| Preparing Input Files | ⭐⭐⭐⭐ | 75% |
| Script Only (no input) | ⭐⭐⭐ | 40% |
| LLM Descriptions | ⭐ | -20% |

## Best Practice: Execution Over Description

```
❌ BAD: "Can you describe what analyze_data.py does?"
    Result: Long description, no actionable output

✅ GOOD: "Prepare input file for data analysis and provide command"
    Result: Working configuration + executable command + actual results
```

## Optimal Workflow Pattern

```
1. ⭐⭐⭐⭐⭐ AI prepares input YAML file
   └─ Following template in templates/input_config.yaml
   └─ Validated against schema
   └─ Version controlled in config/input/

2. ⭐⭐⭐⭐⭐ AI provides exact bash command
   └─ Points to correct script in scripts/
   └─ References prepared input file
   └─ Includes all necessary flags

3. ⭐⭐⭐⭐⭐ User executes command
   └─ Copy/paste provided command
   └─ Review output and results
   └─ Version control any changes

4. ⭐⭐⭐⭐⭐ Use Claude for git operations
   └─ Commit results
   └─ Create meaningful commit messages
   └─ Manage branches and PRs
```

## Prompt Optimization

### Context-First Prompts

```markdown
## Task Context
- Repository: digitalmodel (Work)
- Complexity: Medium
- Time sensitivity: Production hotfix
- Dependencies: None
- Testing required: Yes

## Specifications
[Full specifications here]

## Output Format
[Exact format needed]

## Constraints
[Any limitations]

Generate [specific deliverable] following this context.
```

### Batch Operations Template

```markdown
I need to perform the following operations across multiple repositories:

## Scope
- Repositories: [list or "all work" or "all personal"]
- Operation type: [commit/sync/test/build/deploy]

## Configuration
```yaml
operation: batch_commit
scope: work_repositories
config:
  message: "Update dependencies to latest"
  auto_push: true
  run_tests: true
```

## Expected Output
- Status report per repository
- Aggregate success/failure metrics
- Next actions if any failures
```

## Anti-Patterns to Avoid

### ❌ Description-Only Requests
```
BAD: "Describe what this script does"
Result: No actionable output, wasted tokens
```

### ❌ Skipping Questions
```
BAD: Directly generating from vague requirements
GOOD: "Before generating, I need to understand: [list]"
```

### ❌ Making Assumptions
```
BAD: "I'll assume we want JWT authentication"
GOOD: "Should we use JWT, sessions, or OAuth?"
```

## Usage Monitoring Commands

```bash
# Check usage
./scripts/monitoring/check_claude_usage.sh check

# View today's summary
./scripts/monitoring/check_claude_usage.sh today

# View recommendations
./scripts/monitoring/check_claude_usage.sh rec

# Log a task
./scripts/monitoring/check_claude_usage.sh log sonnet digitalmodel "Feature work"
```

## Daily Checklist

**Before Starting Work:**
- [ ] Check usage at https://claude.ai/settings/usage
- [ ] Note Sonnet percentage
- [ ] Plan model distribution for session
- [ ] Batch similar tasks together

**During Work:**
- [ ] Use Haiku for quick queries
- [ ] Reserve Sonnet for standard implementations
- [ ] Use Opus only for complex decisions
- [ ] Batch related questions

**End of Session:**
- [ ] Review usage increase
- [ ] Update usage log
- [ ] Plan next session if approaching limits

## Target Metrics

| Metric | Current | Target |
|--------|---------|--------|
| Sonnet usage | 79% | <60% |
| Overall usage | 52% | <70% |
| Model distribution | Unbalanced | 30/40/30 |

## Full Reference

See: @docs/AI_AGENT_USAGE_OPTIMIZATION_PLAN.md
See: @docs/modules/ai/AI_USAGE_GUIDELINES.md

---

*Use this when optimizing AI usage, improving efficiency, or managing usage limits.*
