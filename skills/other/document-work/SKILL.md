---
name: document-work
description: |
  Work documentation and pattern capture workflow. Use after completing significant
  work to capture patterns, decisions, and learnings in project memory files
  for future reference.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Document Work Workflow

**When to use**: After completing significant features, at end of work sessions, when new patterns emerge, before context handoffs

---

## When to Use

| Trigger | Action |
|---------|--------|
| Completed major feature | Document patterns + decision |
| End of work session | Update state.md |
| New pattern identified | Add to patterns.md |
| Architecture decision made | Create memory file |
| Before vacation/handoff | Full documentation pass |

---

## Prerequisites

- [ ] Git repository with recent commits to analyze
- [ ] `.claude/` directory exists in project
- [ ] Understanding of what work was done (or access to git history)

---

## Process Overview

```
1. Analyze Recent Changes
   └── git log, git diff, file changes
         ↓
2. Identify Documentation Needs
   └── Patterns? Decisions? State updates?
         ↓
3. Generate Documentation
   └── patterns.md, memory/, state.md, project.md
         ↓
4. Verify Completeness
   └── Checklist validation
```

---

## Phase 1: Analyze Recent Work

### AI Will Review

- Recent git commits (last N commits or since date)
- Files changed and their purpose
- Code patterns introduced or refined
- Decisions made during implementation
- Current work status and next steps

### Discovery Commands

```bash
# View recent commits
git log --oneline -20

# View commits since a date
git log --since="2025-01-01" --oneline

# View files changed in recent commits
git log --oneline --name-only -10

# View detailed diff of recent work
git diff HEAD~5..HEAD --stat
```

### Questions AI May Ask

1. What date range or commits should I analyze?
2. Are there specific decisions you want documented?
3. Any patterns you noticed that should be captured?
4. Who might need context from this work?
5. Is there work in progress that should be captured in state.md?

---

## Phase 2: Identify Documentation Needs

### Pattern Detection Criteria

Document as a pattern when:

- Same code structure used 3+ times
- New API contract established
- Error handling approach standardized
- Testing approach that should be reused
- Configuration pattern worth preserving
- Component structure that became a convention

### Decision Documentation Criteria

Create a memory file when:

- Chose between multiple valid approaches
- Made tradeoff that affects future work
- Established precedent for the codebase
- Something future developers should understand
- Rejected an approach for specific reasons
- External constraints influenced the decision

### State Update Criteria

Update state.md when:

- Work in progress that spans sessions
- Blockers encountered
- Next steps identified
- Dependencies on external factors
- Context needed for next session

### Project Update Criteria

Update project.md when:

- New technology added to stack
- Architecture significantly changed
- New integration added
- Major dependency introduced

---

## Phase 3: Generate Documentation

### Output File Formats

#### patterns.md Entry

```markdown
## [Pattern Name]

**When to use**: [Context where this pattern applies]

**Example**:

```[language]
// Pattern implementation code
```

**Why**: [Rationale for this approach]

**See also**: [Related patterns or files]
```

#### memory/YYYY-MM-DD-topic.md

```markdown
# [Decision Title]

**Date**: YYYY-MM-DD
**Status**: Decided | In Progress | Deprecated
**Affects**: [List of affected areas/files]

## Context

[What was the situation? What problem were we solving?]

## Options Considered

### Option A: [Name]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]

### Option B: [Name]
- **Pros**: [Benefits]
- **Cons**: [Drawbacks]

## Decision

[What was chosen and why]

## Consequences

- [What this means going forward]
- [Any technical debt incurred]
- [Future work enabled or blocked]

## References

- [Related PRs, issues, or documentation]
```

#### state.md

```markdown
# Current Work Status

**Last Updated**: YYYY-MM-DD
**Author**: [Name or AI]

## In Progress

- [ ] [Task description with context]
- [ ] [Another task]

## Recently Completed

- [x] [Completed task] (YYYY-MM-DD)
- [x] [Another completed task] (YYYY-MM-DD)

## Blockers

- **[Blocker name]**: [Description and what's needed to unblock]

## Next Steps

1. [Immediate next action]
2. [Following action]
3. [Future consideration]

## Context for Next Session

[Key context to preserve - what state is the code in, what was the last thing worked on, any gotchas to be aware of]

## Notes

[Any other relevant information]
```

#### project.md Updates

When updating project.md, add to relevant sections:

```markdown
## Recent Changes

### [Date] - [Change Category]
- Added [technology/pattern/integration]
- Reason: [Why this was added]
- Impact: [What this affects]
```

---

## Phase 4: Verification

### Documentation Checklist

- [ ] All significant patterns documented in patterns.md
- [ ] Key decisions have memory files with full context
- [ ] state.md reflects current work status (if applicable)
- [ ] project.md updated if architecture changed
- [ ] Documentation is searchable/findable
- [ ] No sensitive information in docs (credentials, PII)
- [ ] Examples are accurate and runnable
- [ ] Cross-references between related docs

### Quality Checks

- [ ] Pattern examples compile/run
- [ ] Decision rationale is clear to someone unfamiliar
- [ ] State.md has enough context for cold start
- [ ] Memory files are dated correctly
- [ ] No duplicate patterns documented

---

## Usage Examples

### Example 1: End of Feature Session

**User Request:**
```
@.claude/skills/document-work/SKILL.md

Document the work from today's session on the authentication feature.
We made some decisions about JWT vs sessions and established a new
error handling pattern.
```

**AI Will:**
1. Review git commits from today
2. Identify the JWT vs sessions decision → Create memory file
3. Extract error handling pattern → Add to patterns.md
4. Update state.md with current progress

**Output:**
- `.claude/memory/2025-01-14-auth-token-strategy.md`
- Updated `CLAUDE.md` with error handling section
- Updated `CLAUDE.md` with auth feature progress

---

### Example 2: Pattern Discovery

**User Request:**
```
@.claude/skills/document-work/SKILL.md

I noticed we've been using the same API response format across
multiple endpoints. Let's document this as a pattern.
```

**AI Will:**
1. Search codebase for API response patterns
2. Identify the common structure
3. Document as pattern with examples

**Output:**
- Updated `CLAUDE.md` with API response format section

---

### Example 3: Full Documentation Pass (Handoff)

**User Request:**
```
@.claude/skills/document-work/SKILL.md

I'm handing off this project next week. Please review all recent
work (last 2 weeks) and ensure comprehensive documentation for
the next developer.
```

**AI Will:**
1. Review git log for last 2 weeks
2. Identify all significant changes
3. Create memory files for major decisions
4. Document any undocumented patterns
5. Create comprehensive state.md
6. Update project.md with recent architecture changes

**Output:**
- Multiple memory files for decisions
- Updated patterns.md
- Comprehensive state.md for handoff
- Updated project.md

---

### Example 4: Quick State Update

**User Request:**
```
@.claude/skills/document-work/SKILL.md

Just update state.md - I'm stopping for today and want to capture
where I left off on the payment integration.
```

**AI Will:**
1. Ask about current progress
2. Update state.md with in-progress work and next steps

**Output:**
- Updated `CLAUDE.md`

---

## Tips for Effective Documentation

### For Patterns

- Include both good and bad examples
- Explain the "why" not just the "what"
- Link to real implementations in codebase
- Note any exceptions to the pattern

### For Decisions

- Be explicit about rejected options
- Document constraints that influenced the decision
- Include links to relevant discussions/PRs
- Note if decision is reversible

### For State

- Write for your future self (or replacement)
- Include enough context to resume without memory
- List specific files that were being modified
- Note any temporary workarounds in place

---

## Related Workflows

| Workflow | Relationship |
|----------|--------------|
| **create-prd.md** | For planning new work (before implementation) |
| **cleanup-project.md** | For archiving old documentation |
| **generate-tasks.md** | For breaking down documented requirements |
| **update-framework.md** | For updating Samuel itself |

---

## Automation Suggestions

Consider using this workflow:

- **After each PR merge**: Quick pattern + decision check
- **End of sprint**: Full documentation pass
- **Before vacation**: Comprehensive state capture
- **Quarterly**: Review and consolidate memory files
