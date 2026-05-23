---
# VERSION: 2.43.0
name: clarify
description: "Intensive requirement clarification using structured AskUserQuestion workflow. Gathers MUST_HAVE (blocking) and NICE_TO_HAVE (optional) information before implementation. Use when: (1) starting new feature implementation, (2) requirements are ambiguous, (3) multiple approaches possible, (4) before writing any code. Triggers: /clarify, 'clarify requirements', 'ask questions', 'gather requirements'."
user-invocable: true
---

# Clarify - Intensive Questioning (v2.37)

Systematically gather requirements using **TLDR semantic search** + AskUserQuestion tool.

## Quick Start

```bash
/clarify  # Start intensive questioning for current task
```

## Pre-Clarification: TLDR Semantic Search (v2.37)

**AUTOMATIC** - Before asking questions, use semantic search to understand existing code:

```bash
# Find existing related functionality (95% token savings)
tldr semantic "$USER_TASK_KEYWORDS" .

# Example: For "add authentication", find existing auth code
tldr semantic "authentication login session user password" .

# Get structure overview for context
tldr structure . --lang "$PRIMARY_LANGUAGE"
```

This helps formulate better questions based on what already exists in the codebase.

## Workflow

### MUST_HAVE Questions (Blocking)

These MUST be answered before proceeding:

```yaml
AskUserQuestion:
  questions:
    - question: "What is the primary goal of this feature?"
      header: "Goal"
      multiSelect: false
      options:
        - label: "New user-facing feature"
        - label: "Internal refactoring"
        - label: "Bug fix"
        - label: "Performance optimization"
```

### Categories to Cover

1. **Functional Requirements**
   - What exactly should this do?
   - What are inputs/outputs?
   - Edge cases?

2. **Technical Constraints**
   - Existing patterns to follow?
   - Technology preferences?
   - Performance requirements?

3. **Integration Points**
   - Existing code interactions?
   - APIs to maintain?
   - Database changes?

4. **Testing & Validation**
   - How will this be tested?
   - Acceptance criteria?

5. **Deployment**
   - Feature flags needed?
   - Rollback strategy?

### NICE_TO_HAVE Questions

Accept defaults but still ask:

```yaml
AskUserQuestion:
  questions:
    - question: "Implementation preferences?"
      header: "Approach"
      multiSelect: true
      options:
        - label: "Minimal changes"
        - label: "Include tests"
        - label: "Add documentation"
```

## Question Templates

### Goal Clarification
```yaml
AskUserQuestion:
  questions:
    - question: "What problem does this solve?"
      header: "Problem"
      options:
        - label: "User pain point"
          description: "Direct user-facing issue"
        - label: "Technical debt"
          description: "Code maintainability"
        - label: "Performance issue"
          description: "Speed/resource usage"
        - label: "Security concern"
          description: "Vulnerability fix"
```

### Scope Definition
```yaml
AskUserQuestion:
  questions:
    - question: "What is the scope?"
      header: "Scope"
      options:
        - label: "Single file"
        - label: "Single module"
        - label: "Multiple modules"
        - label: "Cross-system"
```

### Priority
```yaml
AskUserQuestion:
  questions:
    - question: "Priority level?"
      header: "Priority"
      options:
        - label: "Critical (blocking)"
        - label: "High (this sprint)"
        - label: "Medium (this quarter)"
        - label: "Low (backlog)"
```

## Integration

- Invoked by /orchestrator in Step 1
- **Pre-step: tldr semantic search** (automatic in v2.37)
- Must complete before CLASSIFY step
- Results inform plan complexity

## TLDR Integration (v2.37)

| Phase | TLDR Command | Purpose |
|-------|--------------|---------|
| Before questions | `tldr semantic "$KEYWORDS" .` | Find related code |
| Context gathering | `tldr structure .` | Codebase overview |
| Dependency check | `tldr deps "$FILE" .` | Impact analysis |

## Anti-Patterns

- Never proceed with unanswered MUST_HAVE questions
- Never assume user intent
- Never skip clarification for features
- Never ask more than 4 questions at once (AskUserQuestion limit)
