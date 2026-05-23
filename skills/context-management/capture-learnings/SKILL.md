---
name: capture-learnings
description: This skill should be used when the user says 'done for today', 'end session', 'capture learnings', 'wrap up', or asks 'what did we learn?'. Captures actionable insights, patterns, and outcomes from the current session into persistent memory with optional Beads issue tracking.
---

# Session Learning Capture

Capture actionable insights, patterns, and outcomes from the current session into structured, persistent memory. Records what was learned, what worked, what could improve, and any new patterns discovered.

## When to Use

Activate when users:
- Say "done for today", "end session", "let's wrap up", "capture learnings"
- Ask "what did we learn?", "what did we accomplish?", "summary of today"
- Indicate a natural session boundary or project milestone
- Request formalization of insights from work completed

## Session End Questions

Ask these questions conversationally to gather learning data:

1. **What did you learn today?**
   - New insights, surprising discoveries, or unexpected patterns
   - Technologies, frameworks, or techniques encountered
   - Problems solved and approaches that worked

2. **What worked well?**
   - Successful strategies or processes
   - Tools, libraries, or patterns that proved effective
   - Decision-making that led to positive outcomes
   - Collaboration or communication approaches

3. **What would you do differently?**
   - Missteps, inefficiencies, or false starts
   - What didn't work and why
   - Blocked paths and workarounds discovered
   - Time spent on dead ends

4. **Any new patterns discovered?**
   - Recurring themes across tasks
   - Architectural or design patterns identified
   - Common pitfalls in the domain worked on
   - Reusable solutions for future sessions

## Required Information

Gather before generating the learning record:

| Field | Format | Notes |
|-------|--------|-------|
| **session_date** | YYYY-MM-DD | Today's date (auto-generated) |
| **session_duration** | String | "2 hours", "full day", "1 hour 30 min" |
| **project_context** | String | What project/issue was worked on |
| **learnings** | Array | Key insights discovered |
| **what_worked** | Array | Successful approaches |
| **to_improve** | Array | What would change next time |
| **patterns** | Array | New patterns or generalizations |

## Optional Information

| Field | Format | Notes |
|-------|--------|-------|
| **related_issues** | Array | Beads issue IDs (format: `#123`) |
| **tags** | Array | Categorization (e.g., "architecture", "performance", "testing") |
| **blockers_resolved** | Array | Issues that were unblocked |
| **follow_up_tasks** | Array | Work identified for future sessions |
| **code_snippets** | Array | Relevant code examples (file path + line numbers) |

## Output Format

Creates a dated learning record at `.claude/context/session/learnings/YYYY-MM-DD.md` with:

- Structured YAML frontmatter containing metadata
- Four main sections: Learnings, What Worked, Improvements, Patterns
- Links to related Beads issues
- Tags for categorization and searchability
- References to code examples and file locations

## Generation Process

### Step 1: Ask Session End Questions

Ask conversationally in order:

```
Let's capture what we learned today. I'll ask a few questions:

1. What did you learn today? (new insights, surprising patterns, techniques)
2. What worked well? (successful strategies, effective tools, good decisions)
3. What would you do differently? (missteps, inefficiencies, blocked paths)
4. Any new patterns discovered? (recurring themes, reusable solutions)
```

Allow free-form responses. Parse multiple items from each answer.

### Step 2: Gather Optional Context

Ask for additional context if relevant:

```
A few optional questions:

- Were there specific Beads issues or tasks related to this work?
  (Use format: #123, #456)
- What tags best categorize this work?
  (Examples: architecture, performance, testing, tooling, debugging)
- Did you identify any follow-up work for future sessions?
```

### Step 3: Generate Learning Record

Create the file at:
```
.claude/context/session/learnings/YYYY-MM-DD.md
```

Use this YAML frontmatter template:

```yaml
---
date: YYYY-MM-DD
duration: "SESSION_DURATION"
project: "PROJECT_CONTEXT"
tags:
  - tag1
  - tag2
related_issues:
  - "#123"
  - "#456"
blockers_resolved: []
follow_up_tasks: []
---
```

### Step 4: Write Content Sections

Structure the markdown body with four main sections:

#### Learnings

Convert responses to "I learned that..." statements. Include:
- Technical insights
- Process improvements
- Tool discoveries
- Pattern recognition

Example:
```markdown
## Learnings

- I learned that TypeScript's readonly arrays help prevent mutation bugs at compile time
- I learned that sequential rebasing prevents merge conflicts better than parallel merges
- I learned that the beads MQ is the source of truth, not git branches
```

#### What Worked Well

Convert responses to achievement statements. Include:
- Successful strategies
- Effective tools or libraries
- Good decision-making
- Communication approaches

Example:
```markdown
## What Worked Well

- Using the Bash tool with descriptive comments made debugging faster
- Breaking work into TaskCreate items improved focus and tracking
- Asking for clarification early prevented rework
```

#### What I'd Do Differently

Convert responses to "Next time..." statements. Include:
- Inefficiencies to avoid
- Blocked paths to recognize
- Time management improvements
- Decision reversals

Example:
```markdown
## What I'd Do Differently

- Next time, I'd read the entire schema before implementing validation
- Next time, I'd check for existing utilities before writing custom code
- Next time, I'd run tests earlier to catch integration issues sooner
```

#### Patterns Discovered

Generalized insights applicable to future work:
- Architectural patterns
- Testing patterns
- Debugging approaches
- Common pitfalls

Example:
```markdown
## Patterns Discovered

**Pattern: Source of Truth Fallacy**
- Git branches and git ls-remote can show stale state
- Always query the canonical source (in Refinery: beads MQ)
- Applies to: merge queues, deployment tracking, task status

**Pattern: Sequential Over Parallel**
- Sequential operations with clear checkpoints catch issues early
- Parallel operations hide dependencies and create conflicts
- Applies to: merging, deployments, test runs
```

### Step 5: Add Metadata Sections

If applicable, add these optional sections:

#### Code References

Link relevant code snippets:
```markdown
## Code References

- Sequential rebase protocol: `/CLAUDE.md` (lines 245-265)
- Beads MQ check: `handle-failures` step (CLAUDE.md, lines 195-210)
```

#### Follow-up Work

Track identified work for future sessions:
```markdown
## Follow-up Work

- [ ] #123 - Implement caching layer for performance improvement
- [ ] #456 - Add integration tests for new validation logic
- [ ] Create session learnings review process
```

#### Blockers Resolved

Document unblocked work:
```markdown
## Blockers Resolved

- #789 was blocked waiting for schema clarification → resolved by reading TypeScript types
- Performance issue was blocked by misunderstanding sequential rebase → now documented
```

### Step 6: Validate and Display

Before completing:

1. Verify all four main sections have content
2. Verify frontmatter is valid YAML
3. Verify file is readable and well-formatted
4. Display the complete generated file to the user

## File Location

```
.claude/context/session/learnings/YYYY-MM-DD.md
```

The learning records are organized by date for easy session lookup and historical tracking.

## Beads Issue Linking

Link to related issues using standard Beads format:

- When asking: "Were there specific issues related to this work?"
- User provides: `#123`, `#456`
- In frontmatter: Add to `related_issues` array
- In content: Reference with markdown links `[#123](../../../issues/123)`

Format: `- "#123"` (as strings in YAML)

## Indexing and Discovery

Update `.claude/context/session/index.md` if it exists to track:
- New learning records created
- Date range of captured learnings
- Quick reference to important patterns or blockers

Example index entry:
```markdown
- **2026-01-26**: Sequential rebase patterns, Beads MQ verification, source of truth discovery
```

## Example Output

```markdown
---
date: 2026-01-26
duration: "3 hours"
project: "Refinery merge queue processor implementation"
tags:
  - architecture
  - git-operations
  - beads-integration
related_issues:
  - "#42"
  - "#45"
blockers_resolved:
  - "Confusion about Beads MQ as source of truth"
follow_up_tasks:
  - "Document conflict handling strategy in CLAUDE.md"
  - "Create patrol wisp execution guide"
---

## Learnings

- I learned that the Beads MQ (`gt mq list`) is the ONLY canonical source of truth for pending merges - git branches and git ls-remote can show stale state
- I learned that sequential rebase prevents merge conflicts better than parallel merges - each branch must rebase on the current main after the previous one is merged
- I learned that the Refinery's role is to make decisions about conflict handling, not to rely on Go code to auto-resolve
- I learned that the "propulsion principle" means autonomous execution without waiting for confirmation - the hook is the assignment

## What Worked Well

- Breaking down the patrol molecule steps with clear banners made the process understandable
- Using descriptive bash commands with comments improved readability
- Asking clarifying questions about sequential rebase upfront prevented later confusion
- Documenting both the "why" (physics) and "what" (process) made the system intuitive
- Creating a decision matrix for conflict handling gave clarity on when to abort vs. attempt resolution

## What I'd Do Differently

- Next time, I'd explicitly document the source of truth earlier in the context
- Next time, I'd provide working examples of the sequential rebase in action before diving into the theory
- Next time, I'd clarify the "hooked patrol" concept earlier - it's central but explained late
- Next time, I'd include a glossary of Refinery-specific terms (patrol, wisp, polecat, etc.) up front

## Patterns Discovered

**Pattern: Source of Truth Fallacy**
- Systems often have multiple views of the same state (git branches, git ls-remote, task queue)
- Only one is canonical; reading the wrong one causes work to queue up invisibly
- In Refinery: always use `gt mq list`, never `git branch -r`
- Applies to: merge queues, deployment tracking, distributed state systems

**Pattern: Sequential Checkpoints Beat Parallel Operations**
- Parallel operations hide dependencies and create conflicts
- Sequential operations with verification gates (tests must pass) catch issues early
- Each operation must start fresh from the updated baseline
- Applies to: deployments, merges, API calls with side effects

**Pattern: Autonomous Execution Requires Clear Hooks**
- Systems that ask for confirmation create queues and delays
- Systems that define work on hooks and execute autonomously scale
- The hook is the contract - it was placed deliberately
- Applies to: daemon-driven systems, event-driven architectures, queue processors
```

## Tips for Better Learning Capture

- Be specific: "I learned about TypeScript" is less useful than "I learned that readonly prevents mutation bugs"
- Connect to action: What will you do next time differently?
- Generalize patterns: Move beyond today's project to broader applicability
- Link issues: Reference Beads issues so learnings connect to the work
- Review periodically: Check past learning records when starting related work

## Voice Learning

Capture feedback to improve this skill:
- Positive: "This structure helped me remember", "Good question order"
- Negative: "Too many questions", "Hard to remember", "Not relevant to my work"

## Common Patterns to Look For

When asking the session end questions, watch for:

- **Architectural insights**: New ways to structure systems
- **Tool discoveries**: Libraries, frameworks, or utilities that solve problems
- **Process improvements**: Better ways to approach common tasks
- **Testing patterns**: Effective testing strategies discovered
- **Debugging techniques**: New approaches that helped identify issues
- **API patterns**: Reusable integration approaches
- **Error patterns**: Common mistakes that can be avoided

## Session Boundaries

Trigger capture at natural session ends:
- End of work day
- Completion of major feature or milestone
- Shift in project context
- User explicitly requests it
- After resolving significant blockers
- Before starting a completely different task

