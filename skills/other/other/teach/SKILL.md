---
name: teach
description: "Deep pedagogical guidance - learn technology by doing with Socratic teaching. Use when learning a new framework or wanting to understand WHY, not just HOW."
model: claude-sonnet-4-20250514
allowed-tools: Read, Glob, Grep, WebSearch
---

# /teach

Line-by-line, Socratic teaching. Build genuine understanding while completing real work.

## Usage

```bash
/teach 001              # Learn through issue 001
/teach yourbench 001    # Explicit project
/teach 001 --phase 2.1  # Start at specific phase
```

## Comparison

| Aspect | /implement | /advise | /teach |
|--------|------------|---------|--------|
| Who writes code | AI | You | You |
| Speed | Fast | Medium | Slower |
| Depth | Task completion | Task guidance | Conceptual learning |
| Questions | Few | As needed | Frequent, Socratic |
| Explanations | Minimal | Practical | Line-by-line |
| Granularity | File-level | Step-level | Line-level |

## Teaching Approach

**Core principle**: Break down EVERY piece of code into individual lines and explain each one conceptually.

**Example:**

```
AI: "First line:
     import Database from 'better-sqlite3';

     This imports the better-sqlite3 library. Do you know what 'import' does
     in JavaScript?"

User: "It brings in code from another file?"

AI: "Exactly! The 'from' part tells it which package...

     Ready for the next line?"

User: "Yes"

AI: "Next line:
     import { env } from '@/env';

     This one has curly braces { }. What do you think those mean?"
```

### Teaching Style

- **Micro-steps** - One line at a time
- **Constant checks** - After every 1-3 lines, verify understanding
- **First principles** - Explain WHY syntax exists
- **Build vocabulary** - Name concepts (named vs default exports)
- **No assumptions** - Explain even "obvious" things
- **Connect dots** - Link to previous work
- **Invite questions** - "Want to see that file again?"

## Execution Flow

### 1. Load Context
```bash
Read: ideas/[project]/issues/###-*/TASK.md
Read: ideas/[project]/issues/###-*/PLAN.md
Read: ideas/[project]/specs/SPEC-###.md
Glob: spaces/[project]/docs/project/adrs/ADR-*.md
```

### 2. Line-by-Line Teaching

1. **Assess prior knowledge** - "Have you used X before?"
2. **Present ONE line** - Show only current line
3. **Explain syntax** - Break down each symbol
4. **Explain purpose** - WHY this line exists
5. **Check comprehension** - "Does that make sense?"
6. **Relate to familiar** - Connect to what they know
7. **Answer questions** - Pause for clarifications
8. **Move to next** - Only after understanding confirmed

**Critical: Never show more than 2-3 lines at once**

### 3. Research as Needed

- Use Context7 for authoritative docs
- WebSearch for tutorials, explanations
- Reference codebase as learning examples

### 4. Check Understanding

- "Why did we do X instead of Y?"
- "What do you think would happen if...?"
- "Can you walk me through what you wrote?"

### 5. Update WORKLOG

```markdown
## YYYY-MM-DD HH:MM - TEACHING: Database Setup

**Concepts covered**:
- Import statements: named vs default exports
- TypeScript types
- Singleton pattern

**User demonstrated understanding**:
- Correctly explained named vs default exports
- Asked good clarifying question about singleton

**Areas needing reinforcement**:
- Path resolution methods
```

## When to Use

**Good for:**
- Learning a new framework/library
- Want to understand WHY, not just HOW
- Building mental models
- Comfortable going slower

**Use /advise instead:**
- Know the tech, just need task guidance
- Want faster pace
- Task-focused, not learning-focused

**Use /implement instead:**
- Just want it done quickly
- Will learn by reading code later

## Teaching Techniques

### Socratic Questioning
- "What do you think would happen if...?"
- "Why do you think they designed it this way?"

### Relating to Prior Knowledge
- "Remember how in React you use useState? In Next.js..."

### Building Mental Models
- Draw analogies: "The database is like a filing cabinet..."
- Show alternatives: "We could also do X, but..."

### When User Gets Stuck
1. Stop immediately
2. Ask what's unclear
3. Go even smaller (individual symbols)
4. Use analogies
5. Try different angles
6. Never rush

## Integration

```
/issue → /plan → /teach → [you implement with learning] → /worklog → /commit
```

Mixed approach:
```
/teach (new concepts) → /advise (applying) → /implement (repetitive)
```
