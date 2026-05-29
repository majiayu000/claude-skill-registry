---
name: faion-reflexion
description: "Learn from mistakes and successes. Stores patterns, errors, and solutions in memory. Prevents repeating errors. Use after task completion or failure."
user-invocable: false
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion
---

# Reflexion Learning Skill

**Communication with user: User's language. Documents: English.**

## Purpose

Implement PDCA (Plan-Do-Check-Act) learning cycle. Store patterns and mistakes for future reference.

**ROI: Prevent 5-50K tokens of repeated mistakes**

## Memory Structure

```
~/.sdd/memory/
├── patterns_learned.jsonl    # Successful patterns
├── mistakes_learned.jsonl    # Errors and solutions
├── workflow_metrics.jsonl    # Execution metrics
└── session_context.md        # Current session state
```

## PDCA Cycle

```
Plan (hypothesis)
  ↓
Do (experiment)
  ↓
Check (self-evaluation)
  ↓
Act (improvement)
  ↓
Store (memory update)
```

---

## When to Use

### After Task Success
```
1. Extract what worked
2. Identify reusable patterns
3. Store in patterns_learned.jsonl
4. Update workflow_metrics.jsonl
```

### After Task Failure
```
1. Analyze root cause
2. Check if similar error exists in mistakes_learned.jsonl
3. If exists: Show previous solution
4. If new: Store error + solution
5. Update workflow_metrics.jsonl
```

### Before Task Start
```
1. Check mistakes_learned.jsonl for similar task types
2. If found: Show warnings and prevention tips
3. Check patterns_learned.jsonl for best practices
4. If found: Suggest approach
```

---

## Data Formats

### patterns_learned.jsonl
```json
{
  "id": "PAT-001",
  "timestamp": "2025-01-16T10:00:00Z",
  "project": "qcdoc",
  "task_type": "api_endpoint",
  "pattern_name": "django_rest_viewset",
  "description": "Use ModelViewSet with serializer for CRUD",
  "context": "When creating REST API endpoints",
  "code_example": "class FooViewSet(ModelViewSet):\n    ...",
  "success_count": 5,
  "tags": ["django", "rest", "api"]
}
```

### mistakes_learned.jsonl
```json
{
  "id": "ERR-001",
  "timestamp": "2025-01-16T10:00:00Z",
  "project": "qcdoc",
  "task_type": "database_migration",
  "error_type": "migration_conflict",
  "description": "Migration failed due to circular dependency",
  "root_cause": "Model A references Model B which references Model A",
  "solution": "Use string reference 'app.Model' instead of direct import",
  "prevention": "Always check for circular imports before migration",
  "occurrence_count": 2,
  "tags": ["django", "migration", "circular"]
}
```

### workflow_metrics.jsonl
```json
{
  "timestamp": "2025-01-16T10:00:00Z",
  "project": "qcdoc",
  "feature": "01-auth",
  "task_id": "TASK_001",
  "task_type": "api_endpoint",
  "complexity": "medium",
  "estimated_tokens": 5000,
  "actual_tokens": 4200,
  "success": true,
  "duration_minutes": 15,
  "patterns_used": ["PAT-001"],
  "errors_encountered": []
}
```

---

## Workflow

### Recording Success
```
1. User says task completed successfully
2. AskUserQuestion: "Що спрацювало добре?"
   - Code pattern
   - Architecture decision
   - Tool usage
   - Process improvement
3. Extract pattern details
4. Write to patterns_learned.jsonl
5. Update workflow_metrics.jsonl
```

### Recording Failure
```
1. User reports error or failure
2. AskUserQuestion: "Що пішло не так?"
   - Code error
   - Architecture mistake
   - Missing requirement
   - Tool issue
3. Analyze root cause
4. Check existing mistakes for similar
5. If new: Store in mistakes_learned.jsonl
6. Suggest solution
7. Update workflow_metrics.jsonl
```

### Pre-Task Check
```
1. Read task type from TASK_*.md
2. Search mistakes_learned.jsonl for matching tags
3. If found: Show warnings
4. Search patterns_learned.jsonl for matching tags
5. If found: Show recommendations
```

---

## Output Format

### Pattern Recorded
```markdown
## Pattern Recorded ✅

**ID:** PAT-{NNN}
**Type:** {task_type}
**Pattern:** {pattern_name}

### Description
{description}

### When to Use
{context}

### Example
```{language}
{code_example}
```

Stored in `~/.sdd/memory/patterns_learned.jsonl`
```

### Mistake Recorded
```markdown
## Mistake Recorded ⚠️

**ID:** ERR-{NNN}
**Type:** {error_type}

### What Happened
{description}

### Root Cause
{root_cause}

### Solution
{solution}

### Prevention
{prevention}

Stored in `~/.sdd/memory/mistakes_learned.jsonl`
```

### Pre-Task Warnings
```markdown
## Pre-Task Check: {task_type}

### ⚠️ Known Pitfalls
1. **ERR-{NNN}:** {description}
   - Prevention: {prevention}

### ✅ Recommended Patterns
1. **PAT-{NNN}:** {pattern_name}
   - Context: {context}
```

---

## Integration

- After `/faion-execute-task` → Record success/failure
- Before `/faion-execute-task` → Check for warnings
- After any error → Analyze and store
- Weekly → Review metrics, identify trends

## Metrics Analysis

Monthly analysis of workflow_metrics.jsonl:
- Most common error types
- Most used patterns
- Token efficiency trends
- Success rate by task type
- Estimation accuracy
