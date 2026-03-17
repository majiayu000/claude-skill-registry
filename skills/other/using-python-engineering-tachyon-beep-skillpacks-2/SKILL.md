---
name: using-python-engineering
description: Routes to appropriate Python specialist skill based on symptoms and problem type
---

# Using Python Engineering

## Overview

This meta-skill routes you to the right Python specialist based on symptoms. Python engineering problems fall into distinct categories that require specialized knowledge. Load this skill when you encounter Python-specific issues but aren't sure which specialized skill to use.

**Core Principle**: Different Python problems require different specialists. Match symptoms to the appropriate specialist skill. Don't guess at solutions—route to the expert.

## When to Use

Load this skill when:
- Working with Python and encountering problems
- User mentions: "Python", "type hints", "mypy", "pytest", "async", "pandas", "numpy", "Textual", "TUI"
- Need to implement Python projects or optimize performance
- Setting up Python tooling or fixing lint warnings
- Debugging Python code or profiling performance
- Building terminal user interfaces with Textual

**Don't use for**: Non-Python languages, algorithm theory (not Python-specific), deployment infrastructure (not Python-specific)

---

## How to Access Reference Sheets

**IMPORTANT**: All reference sheets are located in the SAME DIRECTORY as this SKILL.md file.

When this skill is loaded from:
  `skills/using-python-engineering/SKILL.md`

Reference sheets like `systematic-delinting.md` are at:
  `skills/using-python-engineering/systematic-delinting.md`

NOT at:
  `skills/systematic-delinting.md` ← WRONG PATH

When you see a link like `[systematic-delinting.md](systematic-delinting.md)`, read the file from the same directory as this SKILL.md.

---

## Routing by Symptom

### Type Errors and Type Hints

**Symptoms - Learning Type Syntax**:
- "How to use type hints?"
- "Python 3.12 type syntax"
- "Generic types"
- "Protocol vs ABC"
- "TypeVar usage"
- "Configure mypy/pyright"

**Route to**: See [modern-syntax-and-types.md](modern-syntax-and-types.md) for comprehensive type system guidance.

**Why**: Learning type hint syntax, patterns, and configuration.

**Symptoms - Fixing Type Errors**:
- "mypy error: Incompatible types"
- "mypy error: Argument has incompatible type"
- "How to fix mypy errors?"
- "100+ mypy errors, where to start?"
- "When to use type: ignore?"
- "Add types to legacy code"
- "Understanding mypy error messages"

**Route to**: See [resolving-mypy-errors.md](resolving-mypy-errors.md) for systematic mypy error resolution.

**Why**: Resolving type errors requires systematic methodology, understanding error messages, and knowing when to fix vs ignore.

**Example queries**:
- "Getting mypy error about incompatible types" → [resolving-mypy-errors.md](resolving-mypy-errors.md)
- "How to use Python 3.12 type parameter syntax?" → [modern-syntax-and-types.md](modern-syntax-and-types.md)
- "Fix 150 mypy errors systematically" → [resolving-mypy-errors.md](resolving-mypy-errors.md)

---

### Project Setup and Tooling

**Symptoms**:
- "How to structure my Python project?"
- "Setup pyproject.toml"
- "Configure ruff/black/mypy"
- "Dependency management"
- "Pre-commit hooks"
- "Package my project"
- "src layout vs flat layout"

**Route to**: [project-structure-and-tooling.md](project-structure-and-tooling.md)

**Why**: Project setup involves multiple tools (ruff, mypy, pre-commit) and architectural decisions (src vs flat layout). Need comprehensive setup guide.

**Example queries**:
- "Starting new Python project, how to set up?"
- "Configure ruff for my team"
- "Should I use poetry or pip-tools?"

---

### Lint Warnings and Delinting

**Symptoms**:
- "Too many lint warnings"
- "Fix ruff errors"
- "How to delint legacy code?"
- "Systematic approach to fixing lint"
- "Don't want to disable warnings"
- "Clean up codebase lint"

**Route to**: [systematic-delinting.md](systematic-delinting.md)

**Why**: Delinting requires systematic methodology to fix warnings without disabling them or over-refactoring. Process-driven approach needed.

**Example queries**:
- "1000+ lint warnings, where to start?"
- "Fix lint warnings systematically"
- "Legacy code has no linting"

**Note**: If setting UP linting (not fixing), route to [project-structure-and-tooling.md](project-structure-and-tooling.md) first.

---

### Testing Issues

**Symptoms**:
- "pytest not working"
- "Flaky tests"
- "How to structure tests?"
- "Fixture issues"
- "Mock/patch problems"
- "Test coverage"
- "Property-based testing"

**Route to**: [testing-and-quality.md](testing-and-quality.md)

**Why**: Testing requires understanding pytest architecture, fixture scopes, mocking patterns, and test organization strategies.

**Example queries**:
- "Tests fail intermittently"
- "How to use pytest fixtures properly?"
- "Improve test coverage"

---

### Async/Await Issues

**Symptoms**:
- "asyncio not working"
- "async/await errors"
- "Event loop issues"
- "Blocking the event loop"
- "TaskGroup (Python 3.11+)"
- "Async context managers"
- "When to use async?"

**Route to**: [async-patterns-and-concurrency.md](async-patterns-and-concurrency.md)

**Why**: Async programming has unique patterns, pitfalls (blocking event loop), and requires understanding structured concurrency.

**Example queries**:
- "Getting 'coroutine never awaited' error"
- "How to use Python 3.11 TaskGroup?"
- "Async code is slow"

---

### Terminal UI Development (Textual)

**Symptoms**:
- "Building TUI with Textual"
- "Textual app not rendering"
- "compose() not showing widgets"
- "reactive not updating"
- "Textual CSS not working"
- "Widget events not firing"
- "NoMatches when querying"
- "How to test Textual apps"
- "run_test() pilot issues"

**Route to**: [textual-tui-development.md](textual-tui-development.md)

**Why**: Textual has unique patterns for composition, reactivity, CSS styling, and testing that differ from standard Python. The async architecture and reactive data binding require specific approaches.

**Example queries**:
- "Widgets not appearing after compose"
- "UI not updating when data changes"
- "How to use reactive attributes?"
- "Test Textual app with Pilot"

**Note**: For general async issues (event loop, TaskGroup), route to [async-patterns-and-concurrency.md](async-patterns-and-concurrency.md) first. Textual skill is for Textual-specific patterns.

---

### Performance and Profiling

**Symptoms**:
- "Python code is slow"
- "How to profile?"
- "Memory leak"
- "Optimize performance"
- "Bottleneck identification"
- "CPU profiling"
- "Memory profiling"

**Route to**: [debugging-and-profiling.md](debugging-and-profiling.md) FIRST

**Why**: MUST profile before optimizing. Many "performance" problems are actually I/O or algorithm issues. Profile to identify the real bottleneck.

**After profiling**, may route to:
- [async-patterns-and-concurrency.md](async-patterns-and-concurrency.md) if I/O-bound
- [scientific-computing-foundations.md](scientific-computing-foundations.md) if array operations slow
- Same skill for optimization strategies

**Example queries**:
- "Code is slow, how to speed up?"
- "Find bottleneck in my code"
- "Memory usage too high"

---

### Array and DataFrame Operations

**Symptoms**:
- "NumPy operations"
- "Pandas DataFrame slow"
- "Vectorization"
- "Array performance"
- "Replace loops with numpy"
- "DataFrame best practices"
- "Large dataset processing"

**Route to**: [scientific-computing-foundations.md](scientific-computing-foundations.md)

**Why**: NumPy/pandas have specific patterns for vectorization, memory efficiency, and avoiding anti-patterns (iterrows).

**Example queries**:
- "How to vectorize this loop?"
- "Pandas operation too slow"
- "DataFrame memory usage high"

---

### ML Experiment Tracking and Workflows

**Symptoms**:
- "Track ML experiments"
- "MLflow setup"
- "Reproducible ML pipelines"
- "ML model lifecycle"
- "Hyperparameter management"
- "ML monitoring"
- "Data versioning"

**Route to**: [ml-engineering-workflows.md](ml-engineering-workflows.md)

**Why**: ML workflows require experiment tracking, reproducibility patterns, configuration management, and monitoring strategies.

**Example queries**:
- "How to track experiments with MLflow?"
- "Make ML training reproducible"
- "Monitor model in production"

---

## Cross-Cutting Scenarios

### Multiple Skills Needed

Some scenarios require multiple specialized skills in sequence:

**New Python project setup with ML**:
1. Route to [project-structure-and-tooling.md](project-structure-and-tooling.md) (setup)
2. THEN [ml-engineering-workflows.md](ml-engineering-workflows.md) (ML specifics)

**Legacy code cleanup**:
1. Route to [project-structure-and-tooling.md](project-structure-and-tooling.md) (setup linting)
2. THEN [systematic-delinting.md](systematic-delinting.md) (fix warnings)

**Slow pandas code**:
1. Route to [debugging-and-profiling.md](debugging-and-profiling.md) (profile)
2. THEN [scientific-computing-foundations.md](scientific-computing-foundations.md) (optimize)

**Type hints for existing code**:
1. Route to [project-structure-and-tooling.md](project-structure-and-tooling.md) (setup mypy)
2. THEN `modern-syntax-and-types` (add types)

**Load in order of execution**: Setup before optimization, diagnosis before fixes, structure before specialization.

---

## Ambiguous Queries - Ask First

When symptom unclear, ASK ONE clarifying question:

**"Fix my Python code"**
→ Ask: "What specific issue? Type errors? Lint warnings? Tests failing? Performance?"

**"Optimize my code"**
→ Ask: "Optimize what? Speed? Memory? Code quality?"

**"Setup Python project"**
→ Ask: "General project or ML-specific? Starting fresh or fixing existing?"

**"My code doesn't work"**
→ Ask: "What's broken? Import errors? Type errors? Runtime errors? Tests?"

**Never guess when ambiguous. Ask once, route accurately.**

---

## Common Routing Mistakes

| Symptom | Wrong Route | Correct Route | Why |
|---------|-------------|---------------|-----|
| "Code slow" | async-patterns | debugging-and-profiling FIRST | Don't optimize without profiling |
| "Setup linting and fix" | systematic-delinting only | project-structure THEN delinting | Setup before fixing |
| "Pandas slow" | debugging only | debugging THEN scientific-computing | Profile then vectorize |
| "Add type hints" | modern-syntax only | project-structure THEN modern-syntax | Setup mypy first |
| "Fix 1000 lint warnings" | project-structure | systematic-delinting | Process for fixing, not setup |
| "Fix mypy errors" | modern-syntax-and-types | resolving-mypy-errors | Syntax vs resolution process |
| "100 mypy errors" | modern-syntax-and-types | resolving-mypy-errors | Need systematic approach |

**Key principle**: Diagnosis before solutions, setup before optimization, profile before performance fixes.

---

## Red Flags - Stop and Route

If you catch yourself about to:
- Suggest "use async" for slow code → Route to [debugging-and-profiling.md](debugging-and-profiling.md) to profile first
- Show pytest example → Route to [testing-and-quality.md](testing-and-quality.md) for complete patterns
- Suggest "just fix the lint warnings" → Route to [systematic-delinting.md](systematic-delinting.md) for methodology
- Show type hint syntax → Route to `modern-syntax-and-types` for comprehensive guide
- Suggest "use numpy instead" → Route to [scientific-computing-foundations.md](scientific-computing-foundations.md) for vectorization patterns

**All of these mean: You're about to give incomplete advice. Route to the specialist instead.**

---

## Common Rationalizations (Don't Do These)

| Excuse | Reality | What To Do |
|--------|---------|------------|
| "User is rushed, skip routing" | Routing takes 5 seconds. Wrong fix wastes hours. | Route anyway - specialists have quick answers |
| "Simple question" | Simple questions deserve complete answers. | Route to specialist for comprehensive coverage |
| "Just need quick syntax" | Syntax without context leads to misuse. | Route to get syntax + patterns + anti-patterns |
| "User sounds experienced" | Experience in one area ≠ expertise in all Python. | Route based on symptoms, not perceived skill |
| "Already tried X" | May have done X wrong or incompletely. | Route to specialist to verify X properly |
| "Too many skills" | 8 focused skills > 1 overwhelming wall of text. | Use router to navigate - that's its purpose |

**If you catch yourself thinking ANY of these, STOP and route to the specialist.**

---

## Red Flags Checklist - Self-Check Before Answering

Before giving ANY Python advice, ask yourself:

1. ❓ **Did I identify the symptom?**
   - If no → Read query again, identify symptoms

2. ❓ **Is this symptom in my routing table?**
   - If yes → Route to that specialist
   - If no → Ask clarifying question

3. ❓ **Am I about to give advice directly?**
   - If yes → STOP. Why am I not routing?
   - Check rationalization table - am I making excuses?

4. ❓ **Is this a diagnosis issue or solution issue?**
   - Diagnosis → Route to profiling/debugging skill FIRST
   - Solution → Route to appropriate implementation skill

5. ❓ **Is query ambiguous?**
   - If yes → Ask ONE clarifying question
   - If no → Route confidently

6. ❓ **Am I feeling pressure to skip routing?**
   - Time pressure → Route anyway (faster overall)
   - Complexity → Route anyway (specialists handle complexity)
   - User confidence → Route anyway (verify assumptions)
   - "Simple" question → Route anyway (simple deserves correct)

**If you failed ANY check above, do NOT give direct advice. Route to specialist or ask clarifying question.**

---

## Python Engineering Specialist Skills

After routing, load the appropriate specialist skill for detailed guidance:

1. [modern-syntax-and-types.md](modern-syntax-and-types.md) - Type hints, mypy/pyright, Python 3.10-3.12 features, generics, protocols
2. [resolving-mypy-errors.md](resolving-mypy-errors.md) - Systematic mypy error resolution, type: ignore best practices, typing legacy code
3. [project-structure-and-tooling.md](project-structure-and-tooling.md) - pyproject.toml, ruff, pre-commit, dependency management, packaging
4. [systematic-delinting.md](systematic-delinting.md) - Process for fixing lint warnings without disabling or over-refactoring
5. [testing-and-quality.md](testing-and-quality.md) - pytest patterns, fixtures, mocking, coverage, property-based testing
6. [async-patterns-and-concurrency.md](async-patterns-and-concurrency.md) - async/await, asyncio, TaskGroup, structured concurrency, threading
7. [scientific-computing-foundations.md](scientific-computing-foundations.md) - NumPy/pandas, vectorization, memory efficiency, large datasets
8. [ml-engineering-workflows.md](ml-engineering-workflows.md) - MLflow, experiment tracking, reproducibility, monitoring, model lifecycle
9. [debugging-and-profiling.md](debugging-and-profiling.md) - pdb/debugpy, cProfile, memory_profiler, optimization strategies
10. [textual-tui-development.md](textual-tui-development.md) - Textual TUI framework, compose(), reactive attributes, Textual CSS, Pilot testing

---

## When NOT to Use Python Skills

**Skip Python pack when**:
- Non-Python language (use appropriate language pack)
- Algorithm selection (use computer science / algorithms pack)
- Infrastructure/deployment (use DevOps/infrastructure pack)
- Database design (use database pack)

**Python pack is for**: Python-specific implementation, tooling, patterns, debugging, and optimization.

---

## Diagnosis-First Principle

**Critical**: Many Python issues require diagnosis before solutions:

| Issue Type | Diagnosis Skill | Then Solution Skill |
|------------|----------------|---------------------|
| Performance | debugging-and-profiling | async or scientific-computing |
| Slow arrays | debugging-and-profiling | scientific-computing-foundations |
| Type errors | modern-syntax-and-types | modern-syntax-and-types (same) |
| Lint warnings | systematic-delinting | systematic-delinting (same) |

**If unclear what's wrong, route to diagnostic skill first.**

---

## Integration Notes

**Phase 1 - Standalone**: Python skills are self-contained

**Future cross-references**:
- superpowers:test-driven-development (TDD methodology before implementing)
- superpowers:systematic-debugging (systematic debugging before profiling)

**Current focus**: Route within Python pack only. Other packs handle other concerns.
