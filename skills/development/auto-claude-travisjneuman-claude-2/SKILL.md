---
name: auto-claude
description: Autonomous multi-agent coding with git worktree isolation, QA validation, and memory. Use for complex features requiring autonomous implementation.
tags: [autonomous, development, qa, worktree, memory]
---

# Auto-Claude: Autonomous Coding Framework

Autonomous multi-agent system for complex feature implementation with QA validation.

## When to Use

✅ **Use Auto-Claude for:**

- **Complexity 3-4** - Well-defined features, multiple files
- Established codebases with clear patterns
- Repetitive tasks (CRUD, forms, API endpoints, auth flows)
- When you prefer review-at-end vs step-by-step
- Features requiring iterative refinement with QA validation

❌ **Don't use Auto-Claude for:**

- **Complexity 1-2** - Use manual `/start-task` instead
- **Complexity 5+** - Use `/gsd:new-project` instead
- Greenfield projects (no existing codebase patterns)
- Exploratory/research tasks (unclear requirements)
- Simple typo fixes or config changes
- Tasks requiring human decision-making during implementation

**Quick Guide:**

- Complexity 1-2 → Manual implementation
- Complexity 3-4 → **Auto-Claude** (autonomous)
- Complexity 5+ → GSD (multi-phase)

## Core Capabilities

1. **Codebase Analysis** - Generates semantic baseline
2. **Spec Generation** - Creates detailed implementation plan
3. **Autonomous Implementation** - Multi-agent coordination
4. **Git Worktree Isolation** - Safe development in separate worktree
5. **QA Validation** - Iterative quality checks
6. **Memory System** - Graphiti-powered context retention

## Workflow

```bash
# From project directory:
/auto-claude Add user authentication with JWT tokens
```

**What Happens:**

1. Analyzes project structure → generates baseline
2. Creates implementation spec → stores in ~/.auto-claude/specs/
3. Creates git worktree → isolated development environment
4. Autonomous agents implement → with QA loops
5. Returns completed code → ready for review

**Output Location:** `~/.auto-claude/` (gitignored)

## Integration with Existing Workflows

**Manual Implementation:**

```
/start-task [description]  → Claude implements step-by-step
```

**Autonomous Implementation:**

```
/auto-claude [description] → Auto-Claude implements autonomously
```

**Multi-Phase Projects:**

```
/gsd:new-project          → GSD for project management
```

## Configuration

**Location:** `~/.auto-claude/.env`

**Required:**

- `CLAUDE_CODE_OAUTH_TOKEN` - Get from `/settings` in Claude Code

**Optional (Recommended):**

- `GRAPHITI_ENABLED=true` - Semantic memory
- `GOOGLE_API_KEY` - For Gemini embeddings (memory feature)
- Alternative: Ollama (local) or disable memory

## Trade-offs

**Strengths:**

- Autonomous with minimal oversight
- QA validation ensures quality
- Git worktree prevents main branch disruption
- Memory learns from previous sessions

**Limitations:**

- Best for established codebases
- Requires clear specifications
- Uses tokens for multi-agent iterations
- Manual merge required after completion

## Examples

**Good use cases:**

- "Add user authentication with JWT tokens and session management"
- "Implement dark mode toggle with localStorage persistence"
- "Refactor API layer to use async/await instead of callbacks"
- "Add pagination to user list with 20 items per page"
- "Create export-to-CSV functionality for reports"

**Poor use cases:**

- "Fix typo in README" (too simple)
- "Explore best approach for state management" (exploratory)
- "Build entire e-commerce platform" (too large, use GSD)
- "Make the app better" (too vague)

## Typical Timeline

- **Analysis:** 30 seconds
- **Spec Generation:** 1-2 minutes
- **Implementation:** 5-15 minutes (depends on complexity)
- **QA Validation:** 2-5 minutes
- **Your Review:** 5-10 minutes

**Total:** 15-30 minutes for most features

## Related

- `generic-feature-developer` - Manual implementation patterns
- `debug-systematic` - Systematic debugging
- `test-specialist` - Testing strategies

## Documentation

See `~/.claude/docs/AUTO-CLAUDE-GUIDE.md` for:

- Complete setup instructions
- Real-world examples with detailed walkthroughs
- Troubleshooting guide
- Performance tips
- Comparison with other workflows
