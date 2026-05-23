---
name: write-atomic-tasks
description: |
  Writes precise, autonomous-execution-ready tasks using the SMART+ framework (Specific,
  Measurable, Actionable, Referenced, Testable, +Context). Transforms vague task descriptions
  into detailed specifications with file paths, verification commands, and clear success criteria.
  Use when writing tasks for any agent, creating todos, planning features, decomposing work,
  or when tasks lack precision. Triggers on "write task", "create todo", "break down feature",
  "make task precise", "task is vague", or when task descriptions are missing file paths,
  verification steps, or clear success criteria. Works with todo.md, task lists, project
  planning documents, and agent instructions.
---

# Write Atomic Tasks

## Quick Start

Transform vague task descriptions into precise, autonomous-execution-ready specifications:

```markdown
❌ BEFORE (vague):
- [ ] Add error handling

✅ AFTER (precise):
- [ ] Task 1: Add ConnectionError and TimeoutError handling to ClaudeAgentClient.query()
      - Retry 3 times with exponential backoff (1s, 2s, 4s)
      - Raise AgentConnectionError after retries exhausted
      - Location: src/temet_run/agent/client.py:ClaudeAgentClient.query
      - Verify: pytest tests/unit/agent/test_client.py passes
```

## Table of Contents

1. When to Use This Skill
2. What This Skill Does
3. The SMART+ Framework
4. Task Template
5. Precision Checklist
6. Forbidden Vague Patterns
7. Task Decomposition Rules
8. Examples: Vague → Precise Transformation
9. Validation Process
10. Supporting Files
11. Expected Outcomes
12. Requirements
13. Red Flags to Avoid

## 1. When to Use This Skill

**Explicit Triggers:**
- "Write a task for..."
- "Create todo items for..."
- "Break down this feature into tasks"
- "Make this task more precise"
- "How should I write this as a task?"

**Implicit Triggers:**
- Task description lacks file paths
- No verification command specified
- Vague action verbs ("fix", "add", "update" without specifics)
- Missing success criteria
- Task would require clarifying questions before starting

**Debugging/Quality Scenarios:**
- Reviewing task list for autonomous execution readiness
- Agent keeps asking clarifying questions about tasks
- Tasks take longer than expected due to ambiguity
- Post-mortem reveals task interpretation issues

## 2. What This Skill Does

This skill transforms vague task descriptions into precise, autonomous-execution-ready specifications by:

1. **Applying SMART+ Framework** - Ensuring every task is Specific, Measurable, Actionable, Referenced, Testable, with Context
2. **Adding Critical Metadata** - File paths, verification commands, success criteria
3. **Decomposing Large Work** - Breaking complex tasks into 30-minute chunks
4. **Eliminating Vague Patterns** - Replacing forbidden phrases with precise alternatives
5. **Validating Precision** - Checking that tasks answer all 6 precision questions

## 3. The SMART+ Framework

Every task MUST include these components:

| Component | Description | Example |
|-----------|-------------|---------|
| **S**pecific | What exactly to do | "Add retry logic to `ClaudeAgentClient.query()`" not "Add retry logic" |
| **M**easurable | How to verify completion | "Tests pass, mypy clean" |
| **A**ctionable | Clear first step | "Create file `src/temet_run/agent/retry.py`" |
| **R**eferenced | File paths, functions, classes | "in `agent/client.py:ClaudeAgentClient`" |
| **T**estable | Success criteria | "3 retries with exponential backoff, circuit breaker after 5 failures" |
| **+Context** | Why this matters (optional) | "Needed for ADR-016 conversation persistence" |

## 4. Task Template

```markdown
- [ ] Task N: [ACTION VERB] [SPECIFIC TARGET] [SUCCESS CRITERIA]
      Location: [file paths or module names]
      Verify: [how to confirm completion]
```

**Complete Example:**
```markdown
- [ ] Task 1: Add ConversationError exception hierarchy to agent/errors.py
      - Create: ConversationError(base), MessageError, StateError
      - Location: src/temet_run/agent/errors.py
      - Verify: mypy passes, errors importable from temet_run.agent
```

## 5. Precision Checklist

Before writing a task, verify it answers ALL these questions:

1. ✅ **WHAT file(s)?** → Include full path from project root
2. ✅ **WHAT function/class?** → Name the specific target
3. ✅ **WHAT action?** → Use precise verbs: Create, Add, Modify, Remove, Rename, Extract, Move
4. ✅ **WHAT inputs/outputs?** → Specify types, fields, parameters
5. ✅ **HOW to verify?** → Command to run: `pytest path`, `mypy src/`, `uv run temet-run ...`
6. ✅ **WHY doing this?** → Link to ADR, issue, or parent task (optional but helpful)

## 6. Forbidden Vague Patterns

**NEVER write tasks containing these vague phrases:**

| ❌ Forbidden Pattern | ✅ Precise Alternative |
|---------------------|------------------------|
| "Implement the feature" | "Implement X method in Y class with Z behavior" |
| "Add tests" | "Add unit tests for X covering cases A, B, C" |
| "Fix the bug" | "Fix TypeError in X:line Y caused by Z" |
| "Update the code" | "Update X function to accept Y parameter" |
| "Handle errors" | "Add try/except for ConnectionError in X, retry 3 times" |
| "Refactor" | "Extract X logic from Y into new Z class" |
| "Improve performance" | "Reduce X function runtime from 500ms to <100ms by caching Y" |
| "Add logging" | "Add structlog info-level logging to X function for events A, B, C" |
| "Document the code" | "Add Google-style docstring to X function with Args, Returns, Raises" |

## 7. Task Decomposition Rules

**Large tasks MUST be broken down:**

1. **One concern per task** - Don't mix "create model AND write tests AND add CLI"
2. **Max 30 minutes of work** - If longer, split it
3. **Dependencies explicit** - "Task 3 depends on Task 2" or use sub-numbering (2.1, 2.2)
4. **Verification per task** - Each task independently verifiable

**Decomposition Example:**
```markdown
## Feature: Add conversation history command

- [ ] Task 1: Create ConversationRepository protocol
      Location: src/temet_run/domain/repositories.py
      Verify: mypy passes

- [ ] Task 2: Implement JsonlConversationRepository
      Location: src/temet_run/infrastructure/repositories/conversation.py
      Verify: Unit tests pass (create tests/unit/infrastructure/test_conversation_repo.py)

- [ ] Task 3: Add `history` subcommand to CLI
      Location: src/temet_run/main.py (add to agents group)
      Verify: `uv run temet-run agents history --help` shows usage

- [ ] Task 4: Integration test for history command
      Location: tests/integration/test_cli_history.py
      Verify: pytest tests/integration/test_cli_history.py passes
```

## 8. Examples: Vague → Precise Transformation

See `examples/transformation-examples.md` for comprehensive examples covering:
- Error handling tasks
- Data model implementation
- Test writing tasks
- Bug fixes
- Feature additions
- Refactoring work

**Inline Example:**

```markdown
❌ VAGUE:
- [ ] Add error handling to the client

✅ PRECISE:
- [ ] Add ConnectionError and TimeoutError handling to ClaudeAgentClient.query()
      - Retry 3 times with exponential backoff (1s, 2s, 4s)
      - Raise AgentConnectionError after retries exhausted
      - Location: src/temet_run/agent/client.py:ClaudeAgentClient.query
      - Verify: pytest tests/unit/agent/test_client.py passes
```

## 9. Validation Process

**To validate a task for precision:**

1. Read the task description
2. Apply the 6-question checklist (Section 5)
3. Check for forbidden vague patterns (Section 6)
4. Verify SMART+ components present (Section 3)
5. Confirm task is <30 minutes of work

**Validation Script (if available):**
```bash
python ~/.claude/skills/write-atomic-tasks/scripts/validate_task.py "task description"
```

**Manual Validation Output:**
```
Task: "Add error handling to the client"

❌ FAILED Precision Check:
- Missing: Specific file path
- Missing: Function/class name
- Missing: Verification command
- Vague pattern: "Add error handling" (see Section 6)

Suggested rewrite:
- [ ] Add ConnectionError handling to ClaudeAgentClient.query()
      Location: src/temet_run/agent/client.py:ClaudeAgentClient.query
      Verify: pytest tests/unit/agent/test_client.py passes
```

## 10. Supporting Files

- **examples/transformation-examples.md** - 10+ examples of vague → precise transformations
- **references/smart-framework-deep-dive.md** - Detailed explanation of SMART+ components
- **scripts/validate_task.py** - Automated task precision validator
- **templates/task-template.md** - Copy-paste task template with placeholders

## 11. Expected Outcomes

### Successful Task Writing

When tasks are written with this skill:

✅ **Agents can execute autonomously** - No clarifying questions needed
✅ **Clear verification** - Unambiguous success/failure determination
✅ **Predictable effort** - Tasks complete in <30 minutes
✅ **Reduced rework** - Fewer interpretation errors
✅ **Better planning** - Accurate time estimates from precise scoping

### Before/After Metrics

| Metric | Before (Vague Tasks) | After (Precise Tasks) |
|--------|---------------------|----------------------|
| Clarifying questions per task | 2-5 questions | 0 questions |
| Task completion time variance | ±200% | ±20% |
| Rework due to misunderstanding | 30% of tasks | <5% of tasks |
| Autonomous execution success | 40% | 95% |
| Time spent planning vs doing | 20/80 | 40/60 |

## 12. Requirements

**Knowledge:**
- Understanding of SMART goal framework
- Familiarity with project file structure
- Awareness of verification commands (pytest, mypy, etc.)

**Tools:**
- None (skill is language/framework agnostic)

**Environment:**
- Works with any task management system
- Compatible with todo.md, Jira, GitHub Issues, etc.

## 13. Red Flags to Avoid

**Red Flags Checklist:**

- [ ] ❌ Task description fits on one line but has no metadata
- [ ] ❌ No file path mentioned
- [ ] ❌ Action verb is generic ("fix", "update", "add")
- [ ] ❌ No verification command provided
- [ ] ❌ Success criteria is subjective ("make it better")
- [ ] ❌ Task mixes multiple concerns (AND, THEN, ALSO in description)
- [ ] ❌ Task would take >30 minutes but isn't decomposed
- [ ] ❌ Contains forbidden vague patterns (Section 6)
- [ ] ❌ Missing inputs/outputs specification for data operations
- [ ] ❌ No link to parent task/ADR/issue for context

**Common Mistakes:**

1. **Too granular** - "Add import statement" is usually too small, combine with actual work
2. **Too high-level** - "Implement authentication" needs 10+ subtasks
3. **Technology assumption** - "Add React component" when framework not decided
4. **Implicit dependencies** - "Write tests" assumes code exists, make dependency explicit

## Notes

- **This skill is framework-agnostic** - Works for any programming language or project type
- **Precision scales with task complexity** - Simple tasks need less metadata than complex ones
- **Context determines precision level** - Solo developer vs distributed team changes requirements
- **Tasks are living documents** - Update tasks when requirements change, don't let them drift
- **Autonomous execution is the goal** - If a task requires synchronous communication, it's not precise enough
