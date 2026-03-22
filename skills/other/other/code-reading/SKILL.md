---
name: code-reading
description: Understand unfamiliar codebases quickly - navigation strategies, building mental models, finding entry points
category: General Cross Cutting
---

# Skill: code-reading

## What I do

I teach efficient codebase navigation: find entry points, trace data flow, build mental models, and understand architecture without reading everything. Goal: productive understanding in minutes, not hours.

## When to use me

- Joining or exploring a new project
- Working in an unfamiliar part of the codebase
- Understanding dependencies before making changes
- Debugging code you didn't write
- Code review of unfamiliar areas

## Core principles

1. **Top-down first** - Structure before details (directory → packages → functions)
2. **Follow the data** - Trace how data flows through layers
3. **Tests tell truth** - Tests show intended behaviour better than comments
4. **Read selectively** - Only what's relevant to your current task
5. **Build incrementally** - Understanding grows over multiple passes

## Reading strategy

```
5-MIN OVERVIEW
[ ] README - What does this do?
[ ] Directory structure (tree -L 2 -d)
[ ] Entry points (main, handlers, CLI commands)
[ ] Dependencies (go.mod, package.json)
[ ] Tests - What behaviour is specified?

TARGETED DEEP-DIVE (task-specific)
[ ] Find the layer relevant to your task
[ ] Trace one request/action end-to-end
[ ] Read tests for the area you'll change
[ ] Identify patterns used (repository, service, factory)
[ ] Map dependencies of the code you'll modify
```

## Patterns & examples

**Finding entry points:**
```bash
# Go main
grep -rn "func main" --include="*.go"

# CLI commands
grep -rn "cobra\.\|flag\." --include="*.go"

# Test entry points
grep -rn "var _ = Describe\|func Test" --include="*_test.go"

# KaRiya-specific: Intent entry points
ls internal/cli/intents/*/intent.go
```

**Tracing data flow:**
```
User action → Intent (state machine)
    → Screen (UI component)
    → Service (business logic)
    → Repository (data access)
    → Domain entity (data structure)

# Find each layer:
grep -rn "type.*Service struct" --include="*.go"
grep -rn "type.*Repository interface" --include="*.go"
```

**Building a component map:**
```markdown
## Feature: Timeline

Entry: intents/browsetimeline/intent.go
Screen: screens/timeline/list_screen.go
Data: domain/career/event.go
Logic: service/timeline_service.go
Storage: repository/event_repository.go

Flow: Intent → ListScreen → TableBehavior → Service → Repository
```

**Reading by goal:**
```
BUG FIX: Symptom → error message → trace backwards → read tests
FEATURE: Find similar feature → trace its implementation → copy pattern
REVIEW: PR description → tests → implementation → edge cases
```

## Anti-patterns to avoid

- ❌ Reading linearly like a book (follow the flow instead)
- ❌ Trying to understand everything at once (scope to your task)
- ❌ Ignoring tests (they're executable documentation)
- ❌ Assuming without verifying (check the code, don't guess)
- ❌ Skipping the README and directory structure overview

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Code-Quality/Code Reading.md`

## Related skills

- `research` - Systematic investigation methodology
- `architecture` - Understanding structural patterns
- `debug-test` - Debugging unfamiliar test failures
- `question-resolver` - Answering questions about code
