---
name: improve-processes
description: "Reflect on current session and suggest improvements to agents, commands, templates, workflows"
model: claude-haiku-4-5-20251001
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /improve-processes

Reflect on the current session and suggest improvements to tooling.

## Usage

```bash
/improve-processes                    # Reflect on entire session
/improve-processes --focus agents     # Focus on agent improvements
/improve-processes --focus commands   # Focus on command improvements
/improve-processes --focus templates  # Focus on template improvements
/improve-processes --focus workflows  # Focus on workflow improvements
```

## What Can Be Improved

| Category | Location | Examples |
|----------|----------|----------|
| **Agents** | `.claude/agents/` | System prompts, specializations |
| **Skills** | `.claude/skills/` | Workflow steps, validation |
| **Templates** | `shared/templates/` | Spec structure, doc skeletons |
| **Workflows** | `CLAUDE.md` | Command chains, processes |
| **Documentation** | Various | Clarity, completeness |

## Execution Flow

### 1. Session Reflection

Analyze conversation to identify:

**Commands & Workflows**
- Which commands were invoked?
- Were any commands missing?
- Did workflow feel natural?

**Friction Points**
- Manual steps repeated?
- Workarounds needed?
- Multiple explanations required?

**Gaps Discovered**
- Missing template sections?
- Agent capabilities lacking?
- Documentation unclear?

**Patterns Emerged**
- Things done multiple times?
- Decisions that should be documented?

### 2. Generate Suggestions

```markdown
## Suggestion N/Total: [Category]

**Observation**:
[What happened that revealed the opportunity]

**Suggestion**:
[Specific, actionable improvement]

**Affected file(s)**:
[Path(s) to modify]

**Rationale**:
[Why this would help]
```

### 3. Interactive Presentation

Present suggestions one at a time:
```
Action for this suggestion?
1. Implement now - Make the change
2. Create issue - Track for later
3. Skip - Not needed
```

### 4. Execute Actions

**Implement now:**
- Read affected file(s)
- Make improvement
- Confirm change

**Create issue:**
- Create in `ideas/meta-repo/issues/`
- Create TASK.md with details

**Skip:**
- Note and move on

### 5. Session Summary

```markdown
## Session Retrospective Complete

### Actions Taken
- Implemented: N improvements
- Issues created: N
- Skipped: N

### Files Modified
- [list of files changed]

### Issues Created
- [list of issues]
```

## Reflection Prompts

### Agent Improvements
- Did any agent lack knowledge?
- Were responses too verbose/terse?
- Did agents coordinate well?

### Skill Improvements
- Were any steps unnecessary?
- Were any steps missing?
- Did arguments make sense?

### Template Improvements
- Did templates have all sections?
- Were sections consistently skipped?
- Were templates too long/short?

### Workflow Improvements
- Did command chain flow naturally?
- Were there missing connections?
- Were there redundant steps?

## When to Use

- End of significant work session
- After implementing new feature
- When something felt "off"
- Periodically as maintenance

## Focus Mode

```bash
/improve-processes --focus templates
```

Narrows reflection to template-related findings only.

## Integration

```
[work session] → /improve-processes → [improvements] → [next session]
```
