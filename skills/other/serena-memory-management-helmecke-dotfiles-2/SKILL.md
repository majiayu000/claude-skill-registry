---
name: serena-memory-management
description: This skill should be used when the user asks to "create a memory", "read memories", "manage memories", "document patterns", or when starting work on a Serena project with existing memories. Essential for maintaining project knowledge across conversation sessions and distinguishing documentation from agent-focused memories.
license: MIT
compatibility: opencode
metadata:
  category: development
  version: 1.0.0
  toolbox: serena
---

# Serena Memory Management

Essential for maintaining project knowledge across multiple conversation sessions in Serena. Use this skill when working with Serena's memory system to distinguish between human-focused documentation and agent-focused memories.

## When to Use This Skill

### Primary Triggers (Explicit)

Use this skill when the user says:
- "create a memory" / "write a memory" / "store this for later"
- "read memory" / "check memories" / "what memories exist"
- "update memory" / "edit memory"
- "manage memories" / "organize memories"
- "memorize this" / "remember this pattern"

### Contextual Triggers (Implicit)

Use this skill when:
- Starting work on a project with existing memories
- Completing onboarding (to ensure memories are created)
- Discovering significant patterns during work
- User asks about conventions/patterns from previous sessions
- Making architectural changes that affect stored patterns
- **About to create documentation (README, markdown files, etc.)** - STOP and evaluate target audience first

## Why Memory Management Matters

Serena's memory system is critical for multi-session project work. Without proper memory management:

- **Context is lost** between sessions, forcing re-discovery of patterns
- **Inconsistency emerges** as new work contradicts past decisions
- **Efficiency drops** when answering the same questions repeatedly
- **User frustration grows** from explaining conventions multiple times

The documentation explicitly states that "memories can significantly improve the user experience" by preserving discovered patterns, architectural decisions, and project-specific conventions across conversation boundaries.

## Critical Rule: Documentation vs. Memories

**BEFORE creating any documentation (markdown files, README, guides, etc.), ask yourself:**

> **"Is the primary audience a human or an AI agent?"**

### Decision Matrix

| Target Audience | Use | Why |
|----------------|-----|-----|
| **Humans** (developers, users, stakeholders) | Traditional documentation (markdown, README) | Humans need context, examples, motivation, and narrative explanations |
| **AI Agents** (future sessions, other agents) | Serena memories | Memories are specifically designed for agent consumption, persist across sessions, and are efficiently loaded |

### Anti-Pattern: Creating Agent-Targeted Documentation

❌ **Wrong Approach:**
```
User discovers testing patterns
Agent thinks: "I'll create TESTING-GUIDE.md to document this"
Result: Documentation file that no human reads, but clutters repository
```

✅ **Correct Approach:**
```
User discovers testing patterns
Agent thinks: "This is for future AI sessions, not humans"
Agent: Uses write_memory to create testing-conventions.md memory
Result: Information persists for agents without cluttering repository
```

### Examples

**Create Memory (Not Documentation):**
- API conventions discovered during development
- Database schema patterns specific to this project
- Build/deployment procedures for agents
- Testing strategies and patterns
- Error handling conventions
- Code organization principles

**Create Documentation (Not Memory):**
- User-facing API documentation
- Setup instructions for new developers
- Architecture overview for stakeholders
- Contributing guidelines for open-source projects
- Changelog for releases
- Public API references

### When Both Are Needed

Some information serves both humans AND agents:

**Strategy:** Create human-focused documentation, then create a memory that REFERENCES it:

```markdown
# Memory: setup-process.md

## Quick Reference

Full setup instructions for humans: See README.md

## Key Points for Agents

- Project requires Node.js 18+
- Database migrations run automatically via npm run migrate
- Tests require TEST_DATABASE_URL environment variable
- Build command: npm run build (outputs to dist/)

## Common Issues

- If migrations fail, check database connection in .env
- Tests use separate test database (see .env.test)
```

This approach:
- Avoids duplicating information
- Keeps memory concise and agent-focused
- Maintains single source of truth in documentation

### Evaluation Checklist

Before creating ANY documentation file, answer these questions:

- ☐ Who will read this? (Humans or AI agents?)
- ☐ Is this discoverable patterns or instructional content?
- ☐ Would this information help an agent in future sessions?
- ☐ Is there already documentation this could reference instead?

**If primary audience is AI agents → Use memories, not documentation files.**

## Handling User Documentation Requests

**CRITICAL:** When users explicitly request documentation (e.g., "create a GUIDE.md"), you must still perform target audience analysis. User requests don't override this decision.

### Decision Protocol

When user says "create documentation" or "create a [TOPIC].md file":

**Step 1: Analyze the Information**
- Is this agent-consumable patterns (API conventions, testing strategies, deployment steps)?
- Or human-focused content (onboarding guides, architecture explanations, team guidelines)?

**Step 2: If Agent-Focused → Confidently Use Memories**
Don't hedge, don't ask permission, don't offer alternatives.

**Step 3: Educate the User**
Explain why memories are the correct tool for AI-focused information.

### Response Templates

**❌ Wrong Response (Hedging):**
```
User: "Create DEPLOYMENT.md so the team can reference it"
Agent: "Should I create memories or documentation? Or both?"
```
This defers the decision back to the user and suggests you don't understand the distinction.

**❌ Wrong Response (Blind Compliance):**
```
User: "Create API-CONVENTIONS.md"
Agent: "Sure, creating API-CONVENTIONS.md now..."
```
This creates agent-focused documentation in the repository.

**✅ Correct Response (Confident Education):**
```
User: "Create DEPLOYMENT.md so the team can reference it"
Agent: "I'll create a memory for the deployment patterns since this is operational knowledge for AI agents to apply in future sessions.

If your human team needs deployment documentation, that's different. Tell me specifically what they need:
- Developer onboarding guide?
- Operations runbook?
- Troubleshooting procedures?

And I'll create appropriate human-focused documentation."
```

**✅ Correct Response (Clear Distinction):**
```
User: "Document the API patterns you found"
Agent: "I'll create memories for these API patterns - they're conventions for AI agents to follow consistently.

Memories will:
- Load automatically in future sessions
- Keep your repository clean
- Persist across all agent interactions

These aren't human documentation. If you need API docs for developers, let me know what format works for your team."
```

### Key Principles

1. **User requests inform WHAT to preserve, not HOW** - Just because user says "create docs" doesn't mean documentation files are appropriate

2. **Educate, don't defer** - Confidently explain the memory vs documentation distinction

3. **No hedging** - Don't offer to "create both" or "create either one" - make the correct choice based on target audience

4. **Clarify human needs specifically** - If human documentation is needed, ask about the specific audience and use case

### Red Flags - You're Hedging

If you catch yourself saying:
- "Should I create memories or documentation?"
- "I could create both to cover all bases"
- "Do you want me to create X or Y?"
- "Which would you prefer?"

**STOP.** You're deferring instead of deciding. Analyze the target audience and act confidently.

### Exception: User Explicitly Describes Human Audience

If user says: "Create documentation for our new developers to understand the API patterns"

NOW the target audience is clear (humans: new developers). Create human-focused documentation.

But if user just says "document the API patterns" → Default to memories unless you confirm human audience need.

## The Memory Lifecycle

Memory management follows four distinct phases. Each phase has specific responsibilities and outputs.

### Phase 1: Memory Discovery (Session Start)

**Objective:** Load relevant context before beginning work.

**Mandatory Checklist:**

- ☐ Execute `list_memories` to see what exists
- ☐ Review memory names to identify relevant ones for current task
- ☐ Use `read_memory` on relevant memories (task-oriented selection)
- ☐ Acknowledge learned patterns to user

**Example Flow:**

```
Agent: Let me check existing project memories...
[Calls list_memories]
Agent: Found 3 memories: api-conventions.md, testing-patterns.md, database-schema.md
[Calls read_memory on api-conventions.md and testing-patterns.md]
Agent: I see this project uses REST conventions with error codes in the 4xx range, 
       and follows TDD with Jest. I'll apply these patterns.
```

**Common Mistake:** Starting work without checking memories, then re-discovering patterns that were already documented.

**Why It Matters:** Reading memories at session start costs a few tokens but saves hours of re-discovery and prevents inconsistency with past decisions.

### Phase 2: Memory-Informed Work

**Objective:** Apply learned patterns consistently and notice new patterns worth preserving.

**Principles:**

1. **Apply patterns from memories consistently** throughout the session
2. **Notice new patterns** that emerge during work (naming conventions, architectural decisions, etc.)
3. **Identify information worth preserving** for future sessions
4. **Distinguish signal from noise** - not every detail deserves persistence

**What Deserves Memory:**

✅ **Memorize:**
- Architectural decisions and their rationale
- Project-specific conventions that differ from defaults
- Discovered patterns in existing code
- Complex setup procedures or configurations
- Error handling strategies
- Testing approaches and patterns
- Build/deployment processes

❌ **Don't Memorize:**
- Transient task details ("user asked to fix button color")
- Information already in README/docs
- One-time incidents without patterns
- Temporary workarounds
- Implementation details that change frequently

**Example - Pattern Worth Remembering:**

```markdown
During work, you discover:
- All API routes in src/api/ follow REST conventions
- Error responses always include { code, message, details }
- Authentication uses JWT tokens validated in middleware

This is a PATTERN worth memorizing for future API work.
```

**Example - Detail Not Worth Remembering:**

```markdown
During work:
- User asked to change button color from blue to green
- Fixed typo in README
- Updated dependency version

These are TRANSIENT changes, not patterns. Don't memorize.
```

### Phase 3: Memory Creation/Update

**Objective:** Persist discovered patterns in well-structured, actionable memories.

**Decision Tree:**

```
Discovered something worth preserving?
  │
  ├─ YES → Is target audience humans or AI agents?
  │         │
  │         ├─ AI Agents → Check existing memories with list_memories
  │         │              │
  │         │              ├─ Related memory exists? → UPDATE existing memory
  │         │              │
  │         │              └─ No related memory? → CREATE new memory
  │         │
  │         └─ Humans → Create documentation file (README, guides, etc.)
  │
  └─ NO → Continue work
```

**Creation/Update Checklist:**

- ☐ Decide what deserves persistence (patterns, not transient details)
- ☐ **Verify target audience: Is this for AI agents or humans?**
- ☐ **If for humans → Create documentation file, not memory**
- ☐ Check existing memories for overlap with `list_memories`
- ☐ Choose: update existing memory or create new one
- ☐ Use descriptive, task-oriented name (e.g., "testing-conventions.md")
- ☐ Structure content with markdown headers
- ☐ Include specific examples and file paths
- ☐ Verify content is actionable, not vague

**Good Memory Content Structure:**

```markdown
# [Topic Name]

## Context
Brief explanation of when this pattern applies

## Pattern/Convention
Specific description with examples

## Examples
```code
// Actual code examples with file paths
```

## Rationale
Why this pattern exists (helps future decisions)

## Related
Links to other relevant memories or files
```

**Naming Conventions:**

| Good Names | Bad Names |
|------------|-----------|
| `api-error-handling.md` | `memory1.md` |
| `testing-conventions.md` | `notes.md` |
| `database-schema.md` | `stuff.md` |
| `build-process.md` | `temp.md` |

**Why Naming Matters:** Agents select which memories to read based on names. Descriptive names enable precise memory loading, reducing token waste.

### Phase 4: Memory Maintenance

**Objective:** Keep memories accurate, consolidated, and relevant over time.

**When to Maintain:**

- After major refactoring or architectural changes
- When memories become stale or contradictory
- When similar information is fragmented across multiple memories
- When a memory grows too large (>1000 lines)
- When user explicitly requests memory cleanup

**How to Maintain:**

1. **Review:** Use `list_memories` periodically to see the full set
2. **Consolidate:** Merge fragmented memories covering the same topic
3. **Update:** Use `edit_memory` for targeted changes (preferred) or `write_memory` to replace
4. **Delete:** Use `delete_memory` for obsolete information
5. **Split:** If a memory grows too large, split by subtopic

**Maintenance Example:**

```
Before:
- api-errors-4xx.md
- api-errors-5xx.md
- api-response-format.md

After consolidation:
- api-conventions.md (covers all error handling and responses)
```

**Red Flags Indicating Maintenance Needed:**

- Multiple memories with overlapping content
- Contradictory information across memories
- Memories referencing files that no longer exist
- Memories describing obsolete patterns
- Memories with vague or outdated information

## Anti-Patterns: Common Mistakes to Avoid

### ❌ Anti-Pattern 0: Creating Documentation Instead of Memories

**Problem:** Creating markdown documentation files (guides, how-tos, convention docs) when the target audience is AI agents, not humans.

**Symptoms:**
- Creating files like `CONVENTIONS.md`, `PATTERNS.md`, `AGENT-GUIDE.md` in repository
- Documentation that describes patterns for future development work
- Files that no human developer actually reads
- Information duplicated between documentation and what should be memories

**Example:**

```markdown
# Wrong: Creating docs/API-CONVENTIONS.md in repository

# API Conventions

This document describes our API patterns.

All endpoints return { status, data, error } format...
[500 lines of patterns for agents to follow]
```

This should be a **memory** instead, not a documentation file.

**Impact:** 
- Repository clutter with files humans don't read
- Maintenance burden keeping docs in sync
- Agents don't automatically load documentation files (but do load memories)
- Confusion about source of truth

**Prevention:** Before creating ANY documentation file, ask: **"Is the primary audience humans or AI agents?"** If AI agents, use memories instead.

---

### ❌ Anti-Pattern 1: Memory Hoarding

**Problem:** Creating memories for every minor detail, session transcript, or temporary decision.

**Symptoms:**
- 20+ memories in the project
- Memories with names like "session-notes-2024-01-15.md"
- Most memories are never read again
- High token cost reading irrelevant memories

**Impact:** Signal drowns in noise. Agents waste tokens reading irrelevant information, slowing down every session.

**Prevention:** Only memorize patterns that will apply to future tasks. Ask: "Will this information help in a different session?"

---

### ❌ Anti-Pattern 2: Vague Memory Content

**Bad Examples:**
- "Project uses TypeScript" (too general, not actionable)
- "Some files have tests" (which files? what patterns?)
- "Various patterns exist" (what patterns? where?)
- "Error handling is important" (obvious, not specific)

**Good Examples:**
- "All API routes in src/api/ return { status, data, error } format"
- "Tests in __tests__/ use Jest with custom matchers in test/helpers.ts"
- "Error middleware in src/middleware/errors.ts catches all exceptions and formats responses"

**Impact:** Vague memories don't provide actionable guidance, forcing re-discovery anyway.

**Prevention:** Include specific file paths, code examples, commands, and concrete patterns.

---

### ❌ Anti-Pattern 3: Memory Blind Spots

**Problem:** Starting work without checking memories, then rediscovering patterns.

**Symptoms:**
- Agent says "I notice this project uses pattern X" when it's already in memory
- Inconsistency with past decisions
- User has to repeatedly explain the same conventions

**Impact:** Wastes time re-discovering patterns, creates inconsistency, frustrates users.

**Prevention:** ALWAYS execute `list_memories` and read relevant ones at session start. Make it a mandatory habit.

---

### ❌ Anti-Pattern 4: Stale Memories

**Problem:** Outdated information remaining in memories after codebase changes.

**Example:**
```
Memory says: "API routes are in src/routes/"
Reality: Routes were moved to src/api/ during refactoring
```

**Impact:** Following obsolete patterns, confusion about current state, incorrect implementations.

**Prevention:** After architectural changes, refactoring, or major updates, review and update affected memories.

---

### ❌ Anti-Pattern 5: Poor Naming

**Problem:** Generic, meaningless memory names that don't indicate content.

**Bad Names:**
- `memory1.md`, `memory2.md`
- `notes.md`, `stuff.md`, `info.md`
- `temp.md`, `scratch.md`
- `misc.md`, `various.md`

**Good Names:**
- `api-error-handling.md`
- `database-schema-conventions.md`
- `testing-patterns.md`
- `deployment-process.md`

**Impact:** Agents can't determine which memories to read, leading to either reading all memories (token waste) or reading none (missing context).

**Prevention:** Use descriptive, topic-specific names that clearly indicate content scope.

---

### ❌ Anti-Pattern 6: Duplicate Documentation

**Problem:** Copying content from README, docs, or other documentation into memories, OR creating documentation files when memories are more appropriate.

**Example - Copying Documentation:**
```markdown
# Project Setup (memory)

## Installation
npm install

## Running
npm start

## Testing
npm test
```

This duplicates README content and will drift out of sync.

**Example - Creating Agent-Targeted Documentation:**
```markdown
# Wrong: Creating docs/TESTING-PATTERNS.md

Our project uses Jest with these patterns...
[Details only relevant for AI agents doing future work]
```

This should be a memory, not a documentation file.

**Impact:** 
- Maintenance burden with duplicate information
- Version skew between memory and actual docs
- Repository clutter with agent-focused documentation
- Confusion about source of truth

**Prevention:** 

1. **Memories should COMPLEMENT human-focused documentation**, not duplicate it
2. **Reference docs instead of copying them**
3. **Ask yourself: "Who is the audience?"**
   - Humans → Documentation file
   - AI agents → Memory
4. **When both need the information:** Create human-focused documentation, then create a memory that REFERENCES it with agent-specific notes

## Tool Reference

Serena provides five memory tools:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `list_memories` | Show all stored memories | Start of session, before creating/updating memories |
| `read_memory` | Retrieve stored information | After listing, when memory name indicates relevance |
| `write_memory` | Create or replace memory | Creating new memory or completely rewriting existing one |
| `edit_memory` | Update memory content | Making targeted changes to existing memory (preferred over write) |
| `delete_memory` | Remove obsolete memory | When information is no longer relevant or has been consolidated |

**Tool Selection Logic:**

- **Creating new memory:** Use `write_memory`
- **Small targeted update:** Use `edit_memory` (faster, safer)
- **Complete rewrite:** Use `write_memory`
- **Removing content:** Use `edit_memory` or `delete_memory`

## Examples

See the `examples/` directory for concrete examples:

- **good-memory-example.md:** Shows well-structured, actionable memory content
- **bad-memory-example.md:** Shows vague, unusable content to avoid
- **onboarding-memory-set-example.md:** Shows complete initial memory set after project onboarding

## Workflow Summary

**Session Start (MANDATORY):**

1. `list_memories` → Review names
2. `read_memory` on relevant ones → Load context
3. Acknowledge learned patterns to user

**During Work:**

4. Apply patterns consistently
5. Notice new patterns worth preserving
6. Distinguish signal from noise

**Session End or After Discovery:**

7. **STOP: Evaluate target audience before creating any documentation**
8. If target is AI agents → Check existing memories with `list_memories`
9. Update existing OR create new memory (not documentation file)
10. Use descriptive names and specific content
11. Verify actionability

**Periodically:**

11. Review and consolidate fragmented memories
12. Update after architectural changes
13. Delete obsolete information

## Success Criteria

You're using memories effectively when:

✅ Every session starts with `list_memories` and relevant reads  
✅ Memories contain specific paths, examples, and rationale  
✅ Memory names clearly indicate their content  
✅ You rarely re-discover patterns across sessions  
✅ User doesn't repeat the same explanations  
✅ Memories are updated after architectural changes  
✅ Memory set stays focused (5-15 memories, not 50+)  
✅ **You pause before creating documentation to ask: "Is this for humans or agents?"**  
✅ **Agent-focused information is in memories, not repository documentation files**  

## Final Guidance

**Memory management is not optional for multi-session work.** It's the difference between an agent that learns and improves versus one that starts from zero every conversation.

**Invest time at session start to read memories.** The token cost is small compared to the time saved avoiding re-discovery.

**Be selective about what you memorize.** Quality over quantity. One well-written memory about API conventions is worth more than ten vague notes about individual endpoints.

**Keep memories actionable.** If you can't use the information to make a decision or write code, it doesn't belong in a memory.

**Always ask: "Who is this for?"** Before creating any documentation file, verify the target audience. If it's for AI agents (future sessions, pattern reference), use memories instead of cluttering the repository with agent-focused documentation.
