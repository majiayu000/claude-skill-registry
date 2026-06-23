---
name: specs-explore
description: "Explore codebase before committing to a change. Phase executor skill for specs.explore command."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion, TodoWrite
model: inherit
license: MIT
metadata:
  author: gentleman-programming
  version: "1.0"
---

# specs-explore Skill

Investigate the codebase, think through problems, compare approaches, and return a structured analysis. Only create `exploration.md` when `--spec` is provided.

## What You Receive

The orchestrator will give you:
- A topic or feature to explore
- `--spec` path (optional)
- `--lang` framework (optional)

## Execution Steps

### Step 1: Understand the Request

Parse what the user wants to explore:
- Is this a new feature? A bug fix? A refactor?
- What domain does it touch?

### Step 2: Investigate the Codebase

Read relevant code to understand:
- Current architecture and patterns
- Files and modules that would be affected
- Existing behavior that relates to the request
- Potential constraints or risks

```
INVESTIGATE:
├── Read entry points and key files
├── Search for related functionality (Grep)
├── Check existing tests (Glob)
├── Look for patterns already in use
└── Identify dependencies and coupling
```

### Step 3: Analyze Options

If there are multiple approaches, compare them:

| Approach | Pros | Cons | Complexity |
|----------|------|------|------------|
| Option A | ... | ... | Low/Med/High |
| Option B | ... | ... | Low/Med/High |

### Step 4: Persist Artifact (if `--spec` is provided)

If `--spec=docs/specs/001-add-jwt-auth` is specified, write to `docs/specs/001-add-jwt-auth/exploration.md`:

```markdown
## Exploration: {topic}

### Current State
{How the system works today relevant to this topic}

### Affected Areas
- `path/to/file.ext` — {why it's affected}
- `path/to/other.ext` — {why it's affected}

### Approaches
1. **{Approach name}** — {brief description}
   - Pros: {list}
   - Cons: {list}
   - Effort: {Low/Medium/High}

2. **{Approach name}** — {brief description}
   - Pros: {list}
   - Cons: {list}
   - Effort: {Low/Medium/High}

### Recommendation
{Your recommended approach and why}

### Risks
- {Risk 1}
- {Risk 2}

### Ready for Proposal
{Yes/No — and what the user should know}
```

### Step 5: Return Result

Return the same structured analysis (inline), plus:

**Status Report:**
- **status**: `done` | `blocked` | `partial`
- **executive_summary**: 1-sentence description of what was explored and key recommendation
- **artifact**: `{spec}/exploration.md` (if `--spec` provided) or "none"
- **next_recommended**: `specs.brainstorm` (if spec provided) or `none` (if standalone)
- **risks**: risks discovered, or "None"

---

## Rules

- The ONLY file you MAY create is `exploration.md` inside the spec folder (if `--spec` provided)
- DO NOT modify any existing code or files
- ALWAYS read real code, never guess about the codebase
- Keep your analysis CONCISE — summary, not a novel
- If you can't find enough information, say so clearly
- If the request is too vague, ask for clarification