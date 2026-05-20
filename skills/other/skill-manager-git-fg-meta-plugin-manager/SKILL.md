---
name: skill-manager
description: "Creates skills with automatic quality validation. Use when you need a new skill created with all quality gates enforced (frontmatter, navigation, critical_constraint). Uses TaskList for stateful retry loops with skill-auditor. Not for quick prototypes or when manual skill creation is preferred."
context: fork
agent: general-purpose
skills:
  - quality-standards
  - skill-development
allowed-tools:
  - TaskList
  - TaskGet
  - TaskUpdate
  - TaskCreate
  - Write
---

# Skill Manager: Create Skills with Quality Validation

This skill orchestrates the **Manager Pattern** using TaskList for state management:
1. **TaskList**: Creates task with attempt tracking and draft path in metadata
2. **Task(create)**: Creates skill files, writes path to task metadata
3. **Task(audit)**: Reads draft path from metadata, validates, writes result to metadata
4. **Retry loop**: If audit fails, updates attempt count and retries

## TaskList State Machine

```
Manager → TaskList(taskId)
         → Task(create-skill, taskId)
         → Task(audit-skill, taskId)
           → Writes auditResult to TaskList(taskId, metadata)
         → TaskGet(taskId) checks metadata.auditResult
           → If FAIL: TaskUpdate(taskId, {metadata: {attempt: N+1}}) → Retry create
           → If PASS: Complete
```

## Quick Start

**Create a new skill:**

```markdown
Skill(skill-manager)

Provide:
- skill_name: your-skill-name
- description: "What it does. Use when conditions. Not for exclusions."
- (optional) skills_to_load: helper-skill-1, helper-skill-2
```

## Workflow

```
You → Skill(skill-manager)
      → TaskList: Create task with {skillName, attempt: 1, maxAttempts: 3}
      → Task(create-skill-files, taskId)
        → Creates skill files
        → TaskUpdate(taskId, {metadata: {draftPath: "/path/to/SKILL.md"}})
      → Task(skill-auditor, taskId)
        → TaskGet(taskId) reads metadata.draftPath
        → Reads draft, validates
        → TaskUpdate(taskId, {metadata: {auditResult: {status: "PASS"|"FAIL", issues: [...]}}})
      → TaskGet(taskId) checks metadata.auditResult
        → If FAIL & attempt < maxAttempts:
          → TaskUpdate(taskId, {metadata: {attempt: N+1, previousIssues: [...]}})
          → Retry Task(create-skill-files, taskId)
        → If PASS: Return success

You see only: "Skill 'your-skill-name' created in N attempts. All quality gates passed."
```

## Example

**Your request:**
```
Create a skill named 'data-exporter' that exports data to CSV.
Use when users need to export data, generate reports, or create CSV files.
Not for importing data or JSON exports.
```

**What happens:**

1. **TaskList**: Creates task with `metadata: {skillName: "data-exporter", attempt: 1, maxAttempts: 3}`

2. **Task(create)**: Creates `.claude/skills/data-exporter/SKILL.md`
   - Draft may be missing frontmatter, navigation table, etc.
   - Updates task: `TaskUpdate(taskId, {metadata: {draftPath: ".../data-exporter/SKILL.md"}})`

3. **Task(skill-auditor)**: Forked auditor
   - `TaskGet(taskId)` reads draftPath from metadata
   - Validates draft (sees ONLY the draft, not retry history)
   - `TaskUpdate(taskId, {metadata: {auditResult: {status: "FAIL", issues: ["Missing frontmatter"]}}})`

4. **Retry**: `TaskGet(taskId)` checks auditResult
   - `TaskUpdate(taskId, {metadata: {attempt: 2, previousIssues: [...]}})`
   - Task(create) retries with fix guidance

5. **Re-audit**: skill-auditor validates again
   - `TaskUpdate(taskId, {metadata: {auditResult: {status: "PASS"}}})`

6. **Completion**: Manager checks `TaskGet(taskId)` → status PASS
   - Reports: "Skill 'data-exporter' created in 2 attempts. All quality gates passed."

## Quality Gates Enforced

| Gate | Checks |
| :--- | :--- |
| Frontmatter | `name:`, `description:` with What-When-Not format |
| Navigation | "If you need X → Read Y" table |
| Critical Constraint | Non-negotiable rules footer |
| References | Justified or empty |
| Portability | Self-contained, no external dependencies |

## Why Forked Auditor Matters

```
❌ Without fork (auditor sees history):
"OK I've been trying for 5 messages to get this right,
the user is getting frustrated, I should just pass it"

✅ With fork (auditor sees ONLY draft):
"I don't know how many attempts this took.
I only see the draft. It has issues.
FAIL."
```

## Configuration

### Skills to Preload

```yaml
skills:
  - quality-standards    # For validation
  - skill-development    # For template knowledge
```

### Default Limits

- Max attempts: 3
- If all attempts fail: Returns issues for manual fix

## What Gets Created

```
.claude/skills/{skill_name}/
└── SKILL.md    # Complete skill with frontmatter, navigation, content
```
