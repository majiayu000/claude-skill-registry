---
name: feature-dev
description: Automate 7-phase feature development with specialized agents (code-explorer, code-architect, code-reviewer). Use for multi-file features, architectural decisions, or encountering ambiguous requirements, integration patterns, design approach errors.

  Keywords: feature development, code exploration, architecture design, code review, workflow automation, slash command, agents, discovery phase, implementation planning, quality review
license: MIT
allowed-tools: ["Read", "Write", "Edit", "Bash", "Task"]
metadata:
  version: 1.0.0
  author: Sid Bidasaria
  agents:
    - code-explorer
    - code-architect
    - code-reviewer
---

# Feature Development Workflow

A comprehensive, structured workflow for feature development with specialized agents for codebase exploration, architecture design, and quality review.

## Quick Start

Launch the guided feature development workflow:

```bash
/feature-dev Add user authentication with OAuth
```

Or interactively:

```bash
/feature-dev
```

The workflow will guide you through 7 distinct phases automatically.

## Overview

Building features requires more than just writing code. This skill provides a systematic approach that:
- **Understands the codebase** before making changes
- **Asks clarifying questions** to resolve ambiguities
- **Designs thoughtfully** with multiple architecture options
- **Reviews for quality** after implementation

## The 7-Phase Workflow

### Phase 1: Discovery
**Goal**: Understand what needs to be built

- Clarifies unclear feature requests
- Identifies problem, constraints, and requirements
- Summarizes understanding and confirms with user

**Example**:
```
User: /feature-dev Add caching
Agent: Let me understand what you need...
       - What should be cached? (API responses, computed values, etc.)
       - What are your performance requirements?
       - Do you have a preferred caching solution?
```

### Phase 2: Codebase Exploration
**Goal**: Understand relevant existing code and patterns

- Launches 2-3 `code-explorer` agents in parallel
- Explores similar features, architecture, UI patterns
- Reads all identified files for deep understanding
- Presents comprehensive summary of findings

**Agents launched**:
- "Find features similar to [feature] and trace implementation"
- "Map the architecture and abstractions for [area]"
- "Analyze current implementation of [related feature]"

**Example output**:
```
Found similar features:
- User authentication (src/auth/): Uses JWT tokens, middleware pattern
- Session management (src/session/): Redis-backed, 24hr expiry

Key files:
- src/auth/AuthService.ts:45 - Core authentication logic
- src/middleware/authMiddleware.ts:12 - Request authentication
```

### Phase 3: Clarifying Questions
**Goal**: Fill in gaps and resolve all ambiguities

- Reviews codebase findings and feature request
- Identifies underspecified aspects (edge cases, error handling, integration points)
- Presents organized list of questions
- **Waits for answers before proceeding**

**Example**:
```
Before designing, I need to clarify:

1. OAuth provider: Which providers? (Google, GitHub, custom?)
2. User data: Store OAuth tokens or just profile?
3. Existing auth: Replace or add alongside current auth?
4. Sessions: Integrate with existing session management?
5. Error handling: How to handle OAuth failures?
```

**Critical**: Ensures nothing is ambiguous before design begins.

### Phase 4: Architecture Design
**Goal**: Design multiple implementation approaches

- Launches 2-3 `code-architect` agents with different focuses:
  - **Minimal changes**: Smallest change, maximum reuse
  - **Clean architecture**: Maintainability, elegant abstractions
  - **Pragmatic balance**: Speed + quality
- Presents comparison with trade-offs and recommendation
- **Asks which approach to use**

**Example output**:
```
Approach 1: Minimal Changes
- Extend existing AuthService with OAuth methods
Pros: Fast, low risk
Cons: Couples OAuth to existing auth

Approach 2: Clean Architecture
- New OAuthService with dedicated interface
Pros: Clean separation, testable
Cons: More files, more refactoring

Approach 3: Pragmatic Balance
- New OAuthProvider abstraction
Pros: Balanced complexity and cleanliness
Cons: Some coupling remains

Recommendation: Approach 3 - clean boundaries without excessive refactoring
```

### Phase 5: Implementation
**Goal**: Build the feature

- **Waits for explicit approval** before starting
- Reads all relevant files from previous phases
- Implements following chosen architecture
- Follows codebase conventions strictly
- Updates todos to track progress

### Phase 6: Quality Review
**Goal**: Ensure code is simple, DRY, elegant, and functionally correct

- Launches 3 `code-reviewer` agents in parallel:
  - **Simplicity/DRY/Elegance**: Code quality
  - **Bugs/Correctness**: Functional correctness
  - **Conventions/Abstractions**: Project standards
- Consolidates findings and identifies high severity issues
- **Asks what to do**: Fix now, fix later, or proceed as-is

**Example output**:
```
High Priority Issues:
1. Missing error handling in OAuth callback (src/auth/oauth.ts:67)
2. Memory leak: OAuth state not cleaned up (src/auth/oauth.ts:89)

Medium Priority:
1. Could simplify token refresh logic (src/auth/oauth.ts:120)

What would you like to do?
```

### Phase 7: Summary
**Goal**: Document what was accomplished

- Marks all todos complete
- Summarizes what was built, key decisions, files modified
- Suggests next steps

## Specialized Agents

### code-explorer
**Purpose**: Deeply analyzes existing codebase features by tracing execution paths

**Focus**:
- Entry points and call chains
- Data flow and transformations
- Architecture layers and patterns
- Implementation details

**Output**:
- Entry points with file:line references
- Step-by-step execution flow
- Key components and responsibilities
- Essential files to read

**Triggered**: Automatically in Phase 2, or manually

### code-architect
**Purpose**: Designs feature architectures and implementation blueprints

**Focus**:
- Codebase pattern analysis
- Architecture decisions
- Component design
- Implementation roadmap

**Output**:
- Patterns and conventions found
- Architecture decision with rationale
- Complete component design
- Implementation map with build sequence

**Triggered**: Automatically in Phase 4, or manually

### code-reviewer
**Purpose**: Reviews code for bugs, quality issues, and project conventions

**Focus**:
- Project guideline compliance (CLAUDE.md)
- Bug detection
- Code quality issues
- Confidence-based filtering (≥80% confidence only)

**Output**:
- Critical issues (confidence 75-100)
- Important issues (confidence 50-74)
- Specific fixes with file:line references

**Triggered**: Automatically in Phase 6, or manually

## Usage Patterns

### Full workflow (recommended for new features)
```bash
/feature-dev Add rate limiting to API endpoints
```

### Manual agent invocation

**Explore a feature**:
```
"Launch code-explorer to trace how authentication works"
```

**Design architecture**:
```
"Launch code-architect to design the caching layer"
```

**Review code**:
```
"Launch code-reviewer to check my recent changes"
```

## When to Use

**Use for**:
- New features that touch multiple files
- Features requiring architectural decisions
- Complex integrations with existing code
- Features where requirements are somewhat unclear

**Don't use for**:
- Single-line bug fixes
- Trivial changes
- Well-defined simple tasks
- Urgent hotfixes

## Best Practices

1. **Use the full workflow for complex features**: The 7 phases ensure thorough planning
2. **Answer clarifying questions thoughtfully**: Phase 3 prevents future confusion
3. **Choose architecture deliberately**: Phase 4 gives options for a reason
4. **Don't skip code review**: Phase 6 catches issues before production
5. **Read the suggested files**: Phase 2 identifies key files—read them for context

## Common Issues

### Agents take too long
**Cause**: Normal for large codebases
**Solution**: Agents run in parallel when possible. Thoroughness pays off in better understanding.

### Too many clarifying questions
**Cause**: Feature request too vague
**Solution**: Be more specific in initial request. Provide context about constraints upfront.

### Architecture options overwhelming
**Cause**: Multiple valid approaches presented
**Solution**: Trust the recommendation (based on codebase analysis). Pick pragmatic option when in doubt.

## Requirements

- Claude Code installed
- Git repository (for code review)
- Existing codebase (workflow learns from existing patterns)

## Tips

- **Be specific in feature request**: More detail = fewer clarifying questions
- **Trust the process**: Each phase builds on the previous one
- **Review agent outputs**: Agents provide valuable codebase insights
- **Don't skip phases**: Each phase serves a purpose
- **Use for learning**: Exploration phase teaches you about your own codebase

## Verification Checklist

After using the workflow:

- [ ] All 7 phases completed successfully
- [ ] Clarifying questions answered in Phase 3
- [ ] Architecture approach selected in Phase 4
- [ ] Implementation approved before Phase 5 started
- [ ] Code review findings addressed in Phase 6
- [ ] Summary generated with next steps in Phase 7
- [ ] Feature works as expected
- [ ] Code follows project conventions

## References

For detailed workflow documentation, see `README.md`

For agent specifications, see:
- `agents/code-explorer.md`
- `agents/code-architect.md`
- `agents/code-reviewer.md`

For slash command implementation, see `commands/feature-dev.md`
