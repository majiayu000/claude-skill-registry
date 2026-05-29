---
name: codebase-integration
description: Structured workflow for integrating external codebases into agent-studio. Ensures skills, agents, templates, and workflows are properly imported with mandatory router updates.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep, Task]
best_practices:
  - Always analyze source codebase before creating plan
  - Check for existing equivalent skills/agents before importing
  - Update CLAUDE.md routing table after EVERY integration
  - Create integration report and update learnings.md
error_handling: strict
streaming: supported
---

# Codebase Integration

Structured workflow for integrating external codebases (skills, agents, templates, workflows) into the agent-studio framework.

## ROUTER UPDATE REQUIRED (CRITICAL - FINAL STEP)

**After EVERY integration, you MUST:**

1. **Update CLAUDE.md Section 3** - Add new agents to routing table
2. **Update CLAUDE.md Section 8.5** - Add new skills to workflow enhancement section
3. **Update CLAUDE.md Section 3 Workflows** - Add new workflows
4. **Update learnings.md** - Document integration summary

**Verification (RUN THIS):**

```bash
# Check all new items are in CLAUDE.md
grep "<item-name>" .claude/CLAUDE.md || echo "ERROR: NOT IN CLAUDE.md!"
```

**WHY**: Items not in CLAUDE.md are invisible to the Router and will never be used.

---

## When to Use

- Integrating skills/agents from archived codebases
- Porting functionality from external tools (MCP servers, CLI tools)
- Consolidating duplicate functionality
- Importing templates or code style guides

## 8-Phase Integration Workflow

### Phase 1: Source Analysis

Analyze the source codebase to understand what can be integrated.

```javascript
Task({
  subagent_type: 'Explore',
  description: 'Analyze source codebase',
  prompt: `Analyze the codebase at <source-path> for integration.

## Find
1. Skills (SKILL.md files, command definitions)
2. Agents (agent definitions, personas)
3. Templates (code styles, boilerplate)
4. Workflows (multi-step processes)
5. Hooks (pre/post execution)
6. Tools (CLI scripts, utilities)

## Report
- What exists in source
- What already exists in agent-studio (duplicates)
- What is new and should be imported
`,
});
```

### Phase 2: Gap Analysis

Compare source with existing agent-studio content.

**Check for duplicates:**

```bash
# For each skill in source
grep -l "<skill-name>" .claude/skills/*/SKILL.md

# For each agent in source
grep -l "<agent-name>" .claude/agents/**/*.md
```

**Create integration plan:**

- NEW: Items that don't exist
- ENHANCE: Existing items that can be improved
- SKIP: Duplicates or incompatible items

### Phase 3: Create Tasks

Create trackable tasks for each integration item.

```javascript
TaskCreate({
  subject: 'Import <item-name> from <source>',
  description: 'Import, transform, validate, test',
  activeForm: 'Importing <item-name>',
});
```

### Phase 4: Transform and Import

For each item, apply necessary transformations:

**Skills:**

1. Add proper YAML frontmatter (name, description, version, model, tools)
2. Add Memory Protocol section at end
3. Update paths to use `.claude/` structure
4. Validate against skill-definition.schema.json

**Agents:**

1. Add proper YAML frontmatter (name, description, tools, model, temperature, skills)
2. Add Memory Protocol section
3. Ensure Step 0: Load Skills is present
4. Validate against agent-definition.schema.json

**Templates:**

1. Place in `.claude/templates/<category>/`
2. Ensure proper markdown formatting

**Workflows:**

1. Place in `.claude/workflows/` or `.claude/workflows/enterprise/`
2. Update Task() examples to use proper spawn patterns
3. Reference correct agent paths

### Phase 5: Validation

Run validation on all imported items.

```bash
# Validate agents
node .claude/tools/validate-agents.mjs

# Check skill frontmatter
for skill in .claude/skills/*/SKILL.md; do
  grep -q "^name:" "$skill" || echo "MISSING name: $skill"
  grep -q "Memory Protocol" "$skill" || echo "MISSING Memory Protocol: $skill"
done

# Run tests
npm test
```

### Phase 6: Router Update (MANDATORY)

**This step is NOT OPTIONAL. Integration is incomplete without it.**

**For new agents - Add to CLAUDE.md Section 3:**

```markdown
| Request Type | agent-name | `.claude/agents/<category>/<name>.md` |
```

**For new skills - Add to CLAUDE.md Section 8.5:**

```markdown
### <Skill Name>

Use when <trigger condition>:

\`\`\`javascript
Skill({ skill: '<skill-name>' });
\`\`\`

<One-line description of what it does.>
```

**For new workflows - Add to CLAUDE.md Section 3 Workflows:**

```markdown
- `.claude/workflows/<name>.md` - <Description>
```

### Phase 7: Documentation

Create integration report and update memory.

**Integration Report** (`.claude/context/reports/<source>-integration-report.md`):

```markdown
# <Source> Integration Report

**Date**: YYYY-MM-DD
**Status**: COMPLETE

## Items Integrated

- Skills: <count>
- Agents: <count>
- Templates: <count>
- Workflows: <count>

## Files Created

<list>

## Files Modified

<list>

## CLAUDE.md Updates

- Section 3: Added <agents>
- Section 8.5: Added <skills>
- Section 3 Workflows: Added <workflows>
```

**Update learnings.md:**

```markdown
## [YYYY-MM-DD] <Source> Integration Complete

**Status**: COMPLETE

### Items Integrated

- <list>

### Key Patterns

- <patterns adopted>

### CLAUDE.md Updated

- Section 3: <agents>
- Section 8.5: <skills>
```

### Phase 8: Verification

Final verification that integration is complete.

```bash
# Verify all items in CLAUDE.md
for item in <item1> <item2> <item3>; do
  grep -q "$item" .claude/CLAUDE.md || echo "MISSING: $item"
done

# Verify tests pass
npm test

# Verify no broken references
node .claude/tools/validate-agents.mjs
```

## Integration Checklist

Use this checklist for every integration:

```
[ ] Phase 1: Source analyzed
[ ] Phase 2: Gap analysis complete
[ ] Phase 3: Tasks created
[ ] Phase 4: Items transformed and imported
[ ] Phase 5: Validation passed
[ ] Phase 6: CLAUDE.md updated (CRITICAL)
    [ ] Section 3 routing table (agents)
    [ ] Section 8.5 skills (skills)
    [ ] Section 3 workflows (workflows)
[ ] Phase 7: Documentation created
    [ ] Integration report
    [ ] learnings.md updated
[ ] Phase 8: Final verification passed
```

## Common Transformations

### Path Updates

| Source Pattern      | Target Pattern         |
| ------------------- | ---------------------- |
| `conductor/`        | `.claude/context/`     |
| `plugins/`          | `.claude/`             |
| `~/.config/claude/` | `.claude/`             |
| `superpowers:`      | Direct skill reference |

### Frontmatter Requirements

**Skills:**

```yaml
---
name: skill-name
description: One-line description
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
---
```

**Agents:**

```yaml
---
name: agent-name
description: One-line description
tools: [Read, Write, Edit, Bash, Glob, Grep]
model: sonnet
temperature: 0.3
priority: medium
skills:
  - skill-1
  - skill-2
context_files:
  - .claude/context/memory/learnings.md
---
```

## Anti-Patterns

### DO NOT:

- Import without updating CLAUDE.md (Router won't know about new items)
- Skip Memory Protocol section (Agents will forget learnings)
- Copy files without transforming paths (Broken references)
- Skip validation (Silent failures)
- Create duplicate skills/agents (Confusion, wasted context)

### DO:

- Check for existing equivalents first
- Transform all paths to `.claude/` structure
- Add proper frontmatter
- Add Memory Protocol
- Update CLAUDE.md routing table
- Create integration report
- Update learnings.md

## Workflow Integration

This skill implements the external integration workflow. For the complete multi-agent orchestration pattern, see:

**Workflow:** `.claude/workflows/core/external-integration.md`

**Phases covered by this skill:**

- Phase 1: Clone & Isolate (Step 1.1 - isolation to `.claude/context/tmp/`)
- Phase 6: Execute integration (file copying, registry updates, CLAUDE.md updates)
- Phase 7: Cleanup (temp directory removal, documentation)

**Phases handled by other agents:**

- Phase 0: Pre-Check (architect - checks if artifact already exists)
- Phase 2-3: Explore & Plan (architect explores source/target, planner creates integration plan)
- Phase 4-5: Review & Consolidate (architect + security-architect parallel review, planner merges feedback)
- Phase 8: Verify (qa - validates integration works correctly)

**Alignment Notes:**

- **Temp Directory**: Use `.claude/context/tmp/<repo-name>/` for isolation (matches workflow)
- **Rollback**: If integration fails, use `git restore` for CLAUDE.md and registries (see workflow rollback procedure)
- **Gate Decisions**: Respect workflow gate decisions (BLOCKING issues stop integration)

**When to use this skill vs the workflow:**

- **This skill**: Direct integration when you are the executing agent and have already completed planning/review
- **Full workflow**: Multi-agent orchestration requiring parallel exploration, security review, and QA verification

## Related Skills

- `skill-creator` - Creating new skills from scratch
- `agent-creator` - Creating new agents from scratch
- `project-onboarding` - Understanding existing codebases

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- Integration complete -> `.claude/context/memory/learnings.md`
- Issue encountered -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
