---
name: task-delegation
description: Project-agnostic skill for delegating execution work to subagents with skill activation, parallel execution, and quality verification.
---

# Task Delegation Skill

## Delegation Pattern

```
Plan → Create Task → Design Approach → Delegate → Review → Commit
```

**Main Thread (You):** Planning, architecture, coordination, review, user communication
**Subagents:** Execution of well-defined work items with clear outputs

## When to Delegate

✅ **Always delegate:**
- Execution work taking >5 minutes of focused effort
- Writing, research, analysis with defined scope
- Work that can run in parallel with other tasks
- Repetitive mechanical tasks (formatting, compilation, migration)
- Well-defined scope with clear output format

✅ **Benefits:**
- Parallel execution across independent tasks
- Better planning with full project context
- Focused execution produces higher quality
- Cost optimization through model assignment

## When NOT to Delegate

❌ **Never delegate:**
- Task creation or search (use MCP tools directly in main thread)
- Planning and architectural decisions (requires full context)
- Editorial judgment (requires project continuity)
- Answering user questions (requires conversation flow)
- Dependency modeling (requires cross-task analysis)
- Work taking <5 minutes (delegation overhead exceeds execution time)

## Model Assignment Strategy

Choose model based on task complexity and cost optimization:

| Task Type | Model | Rationale |
|-----------|-------|-----------|
| Simple mechanical work | **Haiku** | Cost-efficient; Skills compensate for smaller model |
| Research compilation | **Haiku** | Search and compile work; Skills enforce quality |
| Structured writing | **Sonnet** | Balance capability/cost; structured output |
| Technical analysis | **Sonnet** | Synthesis required beyond Haiku capability |
| Deep critique | **Opus** | Maximum analytical insight needed |
| Complex synthesis | **Opus** | Scholarly rigor, philosophical depth, 10K+ word expansion |

**Cost Optimization Principle:**
Use smallest model capable of task with Skills active. Skills elevate Haiku/Sonnet to achieve quality standards previously requiring larger models.

**How to Assign:**
- Check task's `assignee` field in Backlog (if project uses task assignment)
- Specify model explicitly when delegating: `model='haiku'` or `model='opus'`
- Default to Sonnet for general-purpose work if uncertain

## Task Description for Skill Activation

Skills activate automatically when task description contains trigger keywords.

**Pattern:** `[Action] + [Skill Trigger] + [Context]`

**Examples:**

```bash
# Activates essay-research-compilation skill
"Compile comprehensive research for Essay 11 (Step 1)"

# Activates essay-first-draft skill
"Write first draft for Essay 11 based on research.md (Step 2)"

# Activates essay-critique skill
"Create comprehensive critique for Essay 11 draft (Step 3)"
```

**Trigger Keywords by Skill Type:**
- Research: "research compilation", "Step 1", "gather sources", "compile research"
- Drafting: "first draft", "Step 2", "write draft"
- Critique: "comprehensive critique", "Step 3", "analyze draft"
- Final drafts: "final draft", "Step 4", "expand to 10,000 words"

**Best Practices:**
- Include step number if workflow uses numbered steps
- Reference input files explicitly ("based on research.md")
- State output format ("produce draft-1.md")
- Keep description concise but keyword-rich for matching

## Verifying Skill Activation

After delegating, check subagent's initial response for Skill confirmation.

**Positive Confirmation:**
```
"Using essay-research-compilation Skill to guide research compilation..."
"Activating essay-first-draft Skill for structured writing..."
```

**If Skill Did NOT Activate:**
1. Check task description for missing trigger keywords
2. Redelegate with clearer keywords: "research compilation (Step 1)" not just "gather data"
3. Confirm Skill exists in `.claude/skills/` directory
4. Verify Skill's trigger patterns in SKILL.md frontmatter

**Why Activation Matters:**
Skills provide comprehensive templates, examples, and verification checklists. Without activation, subagent lacks guidance that prevents common errors.

## Delegation Workflow

### 1. Plan in Main Thread
- Understand full scope and dependencies
- Break work into independent subtasks if possible
- Identify which subtasks can run in parallel
- Design approach and output format

### 2. Create Tasks (if using Backlog)
```bash
# Create parent task
task_create(title, description, acceptanceCriteria, assignee=['model-name'])

# Create subtasks with dependencies
task_create(title, description, parentTaskId='parent-id', assignee=['haiku'])
```

### 3. Delegate to Subagent
```bash
# Single delegation
Task tool with:
  - Clear description (triggers Skills)
  - Model specification (haiku/sonnet/opus)
  - Reference to input files
  - Expected output format

# Parallel delegation (independent tasks)
Multiple Task tool calls in single message:
  - Task 1: "Research Essay 3 (Step 1)" → haiku
  - Task 2: "Research Essay 5 (Step 1)" → haiku
  - Task 3: "Research Essay 10 (Step 1)" → haiku
```

### 4. Review Output
- Check against task acceptance criteria
- Verify Skill guidelines followed (see Skill's verification checklist)
- Confirm output format matches expectations
- Test for scope creep (output should match defined scope, nothing more)

### 5. Commit and Document
```bash
git commit -m "[task-id] Brief description

Detailed explanation of what was completed."
```

Update task with commit reference:
```bash
task_edit(id='task-id', notesAppend=['Completed in commit abc123'])
```

## Parallel Execution

**Pattern:** Launch multiple subagents for independent tasks in single message.

**When to Use:**
- Tasks have no dependencies between them
- Different essays at same workflow step
- Different sections of large document
- Independent research compilations

**Example:**
```bash
# Single message with 3 parallel Task tool calls:
Task 1: "Research Essay 3 Data Readiness (Step 1)" model=haiku
Task 2: "Research Essay 5 Technical Debt (Step 1)" model=haiku
Task 3: "Research Essay 10 Infrastructure (Step 1)" model=haiku
```

**Benefits:**
- Maximize throughput (3 tasks complete in parallel vs sequential)
- Efficient use of session time
- No coordination overhead (tasks are independent)

**Dependency Modeling:**
If Task B depends on Task A output, run sequentially:
1. Delegate Task A, wait for completion
2. Review Task A output
3. Delegate Task B with reference to Task A output

## Reviewing Subagent Output

**Verification Checklist:**

1. **Completeness:**
   - All acceptance criteria met?
   - Output file exists at expected path?
   - Required sections present?

2. **Skill Adherence:**
   - Check against Skill's verification checklist (in SKILL.md)
   - Example: essay-research-compilation requires 100% citation completeness
   - Example: essay-first-draft requires minimum 5 human experience paragraphs

3. **Format:**
   - Matches expected structure?
   - File naming correct?
   - No unexpected additions?

4. **Scope:**
   - Output matches defined scope (no scope creep)?
   - Subagent didn't make editorial decisions requiring main thread judgment?

**If Quality Insufficient:**
- Provide specific feedback referencing Skill section
- Example: "Section 2 needs causal analysis per essay-first-draft guidelines"
- Redelegate with clarification, not vague "improve this"

## Handling Subagent Failures

**Common Issues and Fixes:**

| Issue | Root Cause | Fix |
|-------|------------|-----|
| Skill didn't activate | Missing trigger keywords | Redelegate with "Step X" or skill name in description |
| Output missing required sections | Unclear acceptance criteria | Add specific checklist to task description |
| Scope creep | Vague task description | Define exact input files and output format |
| Wrong model used | Model not specified | Explicitly set model parameter in Task tool |
| Quality below standard | Skill verification skipped | Review against Skill checklist, return specific sections |

**Escalation Pattern:**
1. First attempt: Redelegate with clarification
2. Second attempt: Provide Skill excerpt as context
3. Third attempt: Break into smaller subtasks or execute in main thread

## Success Criteria

**Well-delegated task produces:**
- ✅ Output matching acceptance criteria exactly
- ✅ Skill guidelines followed (verified via checklist)
- ✅ No scope creep (output ≤ defined scope)
- ✅ Correct format and location
- ✅ Can commit immediately without revision

**Signs of poor delegation:**
- ❌ Multiple revision rounds needed
- ❌ Subagent made editorial decisions
- ❌ Output contains work outside defined scope
- ❌ Missing required sections
- ❌ Skill didn't activate (preventable with better description)

## Quick Reference

**Delegation Decision Tree:**

```
Is this execution work >5 min? → NO → Do in main thread
  ↓ YES
Is scope well-defined? → NO → Plan first, then delegate
  ↓ YES
Can it run in parallel? → YES → Launch multiple subagents
  ↓ NO
Does it depend on other work? → YES → Wait for dependency
  ↓ NO
Delegate with:
  - Clear description (trigger Skills)
  - Model assignment (haiku/sonnet/opus)
  - Input files referenced
  - Output format specified
```

**Model Selection:**
- Mechanical/research → Haiku
- Structured writing → Sonnet
- Complex synthesis → Opus
- When uncertain → Sonnet (balanced default)

**Parallel Pattern:**
- Independent tasks → Single message, multiple Task calls
- Dependent tasks → Sequential delegation

**Review Pattern:**
- Check acceptance criteria
- Verify Skill checklist
- Confirm format
- Test scope
