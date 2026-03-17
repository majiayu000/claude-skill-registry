---
name: orchestrator
description: Internal orchestrator for executing skills with phase-based subagent spawning. Parses SKILL.md frontmatter, manages dependencies, and coordinates parallel execution.
disable-model-invocation: true
internal: true
---

# Orchestrator

This skill orchestrates the execution of other skills that declare `phases` in their frontmatter. It spawns subagents via Claude Code's Task tool and manages data flow between phases.

## When to Use

When executing a skill that has a `phases` array in its YAML frontmatter, use this orchestrator pattern instead of inline execution.

## Phase Schema

Skills declare phases in frontmatter:

```yaml
phases:
  - name: string            # Required: Phase identifier
    parallel: boolean       # Execute subagents in parallel (default: false)
    depends_on: [string]    # Phase names that must complete first
    inline: boolean         # Run in main context, not as subagent (default: false)
    subagents:              # List of subagents to spawn (omit for inline phases)
      - skill: string       # Path to sub-skill (e.g., _sub/fetch/get-config)
        type: explore | general-purpose
        args: string        # Arguments with {{VAR}} interpolation
        output: string      # Variable name to store result
        requires: [string]  # Variables that must exist before running
        optional: boolean   # Continue if this fails (default: false)
        fallback: inline    # Fall back to inline execution on failure
        on_error: string    # Message to show on failure
```

## Execution Algorithm

### 1. Parse Phase Declarations

Read the skill's frontmatter and extract the `phases` array. Build a context store initialized with:

```
context = {
  ARGUMENTS: <arguments passed to skill>,
  TODAY: <current date YYYY-MM-DD>,
  TARGET_DATE: <resolved from arguments if applicable>
}
```

### 2. Build Dependency Graph

Create a directed acyclic graph from `depends_on` declarations:
- Verify no circular dependencies
- Identify phases that can run in parallel (no unmet dependencies)

### 3. Execute Phases in Topological Order

For each phase in dependency order:

#### 3a. Check Dependencies

- All phases in `depends_on` must be completed
- All variables in `requires` must exist in context

#### 3b. Execute Phase

**If `inline: true`:**
- Execute the markdown content for this phase in the main conversation context
- Collect any user input or generated content into context
- Do NOT spawn a subagent

**If `subagents` defined:**
- For each subagent, spawn via Task tool:

  ```
  Task(
    description: "Execute {skill.name}: {subagent.skill}",
    prompt: <construct from sub-skill SKILL.md + interpolated args>,
    subagent_type: map_type(subagent.type)
  )
  ```

- Type mapping:
  - `explore` → subagent_type: "Explore" (read-only operations)
  - `general-purpose` → subagent_type: "general-purpose" (can write files)

- If `parallel: true`, spawn all subagents simultaneously in a single message with multiple Task tool calls

#### 3c. Capture Output

- Parse subagent result for structured data (JSON blocks or key-value pairs)
- Store in context under the declared `output` variable name
- Make available for subsequent phases via `{{VARIABLE_NAME}}` interpolation

#### 3d. Handle Errors

| Condition | Action |
|-----------|--------|
| Subagent fails, `optional: true` | Log warning, set output to null, continue |
| Subagent fails, `fallback: inline` | Execute sub-skill content inline instead |
| Subagent fails, no fallback | Abort with error, show `on_error` message |

### 4. Variable Interpolation

Replace `{{VARIABLE}}` patterns in args and markdown with values from context:

```
{{VAULT}} → "/Users/me/vault"
{{DIRECTIVES.user.preferred_name}} → "Michi"
{{CALENDAR.events[0].title}} → "Team Standup"
```

## Subagent Prompt Construction

When spawning a subagent, construct its prompt:

```markdown
Execute the following sub-skill and return the result.

## Sub-skill: {subagent.skill}

{content of sub-skill's SKILL.md}

## Arguments

{interpolated args}

## Context

The following variables are available:
{list of context variables relevant to this subagent}

## Output Format

Return your result in a structured format that can be parsed:

\`\`\`json
{
  "key": "value",
  ...
}
\`\`\`

Or use clear key-value pairs:

RESULT_KEY: result_value
```

## Example Execution

Given a skill with:

```yaml
phases:
  - name: setup
    parallel: true
    subagents:
      - skill: _sub/fetch/get-config
        type: explore
        output: VAULT
      - skill: _sub/fetch/get-directives
        type: explore
        output: DIRECTIVES
        optional: true
  - name: gather
    depends_on: [setup]
    subagents:
      - skill: _sub/fetch/get-calendar
        type: explore
        args: "scope={{TARGET_DATE}}"
        output: CALENDAR
  - name: interact
    depends_on: [gather]
    inline: true
```

Execution proceeds:

1. **Phase: setup** (parallel)
   - Spawn get-config and get-directives simultaneously
   - Wait for both to complete
   - Store results: `context.VAULT`, `context.DIRECTIVES`

2. **Phase: gather** (depends_on: setup)
   - Interpolate args: `scope={{TARGET_DATE}}` → `scope=2026-02-15`
   - Spawn get-calendar
   - Store result: `context.CALENDAR`

3. **Phase: interact** (inline)
   - Execute markdown content in main context
   - User interaction happens here
   - Collect user responses into context

## Debugging

When a skill has `debug: true` in frontmatter, log:

- Phase transitions: `[orchestrator] Starting phase: {name}`
- Subagent spawns: `[orchestrator] Spawning: {skill} (type: {type})`
- Context updates: `[orchestrator] Set {output}: {truncated_value}`
- Timing: `[orchestrator] Phase {name} completed in {ms}ms`

## Notes

- This orchestrator is **internal** — users invoke the parent skill, not the orchestrator directly
- Skills without `phases` frontmatter continue to work as before (no orchestration)
- The orchestrator pattern is opt-in per skill
