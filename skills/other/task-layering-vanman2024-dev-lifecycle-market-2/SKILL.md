---
name: Task Layering
description: Breaks down specs into complexity-stratified tasks. Use when organizing tasks, assigning work to agents, or when user mentions task layering, task stratification, or parallel task execution.
allowed-tools: Read, Write, Bash
---

# Task Layering

This skill provides task stratification by complexity and agent assignment for parallel execution.

## What This Skill Provides

### 1. Complexity Stratification
- Trivial (0): < 5 minutes, simple changes
- Simple (1): < 30 minutes, straightforward implementation
- Moderate (2): < 2 hours, requires thought
- Complex (3): > 2 hours, architectural decisions

### 2. Agent Assignment Strategy
- **@claude**: Complex (3), security, architecture
- **@copilot**: Trivial (0), Simple (1)
- **@qwen**: Performance optimization
- **@gemini**: Documentation
- **@codex**: Testing, TDD

### 3. Layer Organization
- **Foundation Layer**: Must complete first (dependencies)
- **Parallel Layer**: Can execute simultaneously
- **Integration Layer**: Combines parallel work

### 4. Output Files
- `layered-tasks.md` - All tasks stratified by complexity
- `claude-tasks.md` - Tasks assigned to Claude
- `copilot-tasks.md` - Tasks assigned to Copilot
- `qwen-tasks.md` - Tasks for performance work
- `gemini-tasks.md` - Documentation tasks
- `codex-tasks.md` - Testing tasks

## Instructions

### Stratifying Tasks

When user wants to layer tasks from a spec:

1. Read the spec's tasks.md file
2. Analyze each task for:
   - Estimated time to complete
   - Required expertise level
   - Dependencies on other tasks
   - Appropriate agent assignment

3. Create layered-tasks.md with format:
   ```markdown
   # Layered Tasks: [Spec Name]

   ## Foundation Layer (Sequential)
   - [Complex] Task 1 (@claude) - Requires arch decisions
   - [Moderate] Task 2 (@claude) - Core implementation

   ## Parallel Layer (Concurrent)
   - [Simple] Task 3 (@copilot) - UI component
   - [Simple] Task 4 (@copilot) - Data model
   - [Moderate] Task 5 (@qwen) - Query optimization

   ## Integration Layer (Sequential)
   - [Moderate] Task 6 (@claude) - Integrate components
   - [Simple] Task 7 (@codex) - Integration tests
   ```

4. Create agent-specific task files for distribution

### Task Complexity Analysis

**Trivial (0) Examples:**
- Update constant value
- Fix typo
- Add simple validation

**Simple (1) Examples:**
- Create CRUD component
- Add new API endpoint
- Write unit test

**Moderate (2) Examples:**
- Implement authentication flow
- Optimize database queries
- Refactor module structure

**Complex (3) Examples:**
- Design system architecture
- Implement security layer
- Create caching strategy

## Layered Tasks Format

```markdown
# Layered Tasks: Feature Name

## Summary
- Total tasks: 15
- Foundation: 3 tasks
- Parallel: 10 tasks
- Integration: 2 tasks

## Foundation Layer
Must complete in order before parallel work:

### 1. [Complex] Design Data Schema (@claude)
**Dependencies**: None
**Estimate**: 3 hours
**Description**: Design database schema and relationships

## Parallel Layer
Can execute simultaneously:

### 2. [Simple] Create User Model (@copilot)
**Dependencies**: Task 1
**Estimate**: 20 minutes

### 3. [Simple] Create Auth Component (@copilot)
**Dependencies**: Task 1
**Estimate**: 30 minutes

## Integration Layer
Combine parallel work:

### 15. [Moderate] Integration Testing (@codex)
**Dependencies**: All parallel tasks
**Estimate**: 1 hour
```

## Success Criteria

- ✅ Tasks are stratified by realistic complexity
- ✅ Dependencies are identified correctly
- ✅ Agent assignments match expertise
- ✅ Layers enable maximum parallelization
- ✅ Output files are complete and actionable

---

**Plugin**: 04-iterate
**Skill Type**: Analysis + Organization
**Auto-invocation**: Yes (via description matching)
