---
name: port-plugin
description: Converts Agent Alchemy plugins into formats compatible with other AI coding platforms
user-invocable: true
disable-model-invocation: true
argument-hint: "[--target opencode] [--dry-run]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Edit
  - Bash
  - Task
  - AskUserQuestion
---

# Plugin Porter

Convert Agent Alchemy plugins (skills, agents, hooks, references, MCP configs) into formats compatible with other AI coding platforms using an extensible markdown-based adapter framework, live platform research, and interactive conversion workflows.

**CRITICAL: Complete ALL 7 phases.** The workflow is not complete until Phase 7: Summary is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Every wizard question -> AskUserQuestion
- Selection questions -> AskUserQuestion
- Confirmation questions -> AskUserQuestion
- Yes/no consent questions -> AskUserQuestion
- Clarifying questions -> AskUserQuestion

Text output should only be used for:
- Summarizing selections and findings
- Presenting information and status updates
- Explaining context or conversion details

If you need the user to make a choice or provide input, use AskUserQuestion.

**NEVER do this** (asking via text output):
```
Which plugin groups would you like to port?
1. core-tools
2. dev-tools
3. sdd-tools
```

**ALWAYS do this** (using AskUserQuestion tool):
```yaml
AskUserQuestion:
  questions:
    - header: "Plugin Groups"
      question: "Which plugin groups would you like to port?"
      options:
        - label: "core-tools"
          description: "3 skills, 2 agents — Deep analysis, codebase analysis, language patterns"
        - label: "dev-tools"
          description: "6 skills, 4 agents — Feature dev, code review, docs, changelog"
        - label: "sdd-tools"
          description: "6 skills, 3 agents — Spec creation, task management, execution"
      multiSelect: true
```

### Plan Mode Behavior

**CRITICAL**: This skill performs an interactive conversion workflow, NOT an implementation plan. When invoked during Claude Code's plan mode:

- **DO NOT** create an implementation plan for how to build the porting feature
- **DO NOT** defer conversion to an "execution phase"
- **DO** proceed with the full wizard and conversion workflow immediately
- **DO** write converted files to the output directory as normal

## Phase Overview

Execute these phases in order, completing ALL of them:

1. **Settings & Arguments** - Load configuration and parse arguments
2. **Plugin Selection Wizard** - Interactive selection of plugin groups and components
3. **Dependency Validation** - Build dependency graph and detect missing references
4. **Platform Research** - Spawn research agent to investigate target platform
4.5. **Dry-Run Preview** - Optional preview of expected output before conversion
5. **Wave-Based Conversion** - Convert components via parallel agent team with incompatibility resolution
6. **Output & Reporting** - Write converted files, migration guide, and gap report
7. **Summary** - Present results and next steps

---

## Phase 1: Settings & Arguments

**Goal:** Load configuration, parse arguments, and determine the target platform.

### Step 1: Parse Arguments

Parse `$ARGUMENTS` for:
- `--target <platform>` — Target platform slug (default: `opencode`)
- `--dry-run` — Preview mode; show expected output without writing files

Set `TARGET_PLATFORM` from `--target` value (default: `opencode`).
Set `DRY_RUN` from `--dry-run` flag (default: `false`).

### Step 2: Load Settings

Check if `.claude/agent-alchemy.local.md` exists and read for any `plugin-tools` section with settings:

```markdown
- **plugin-tools**:
  - **default-target**: opencode
  - **default-output-dir**: ported/
  - **auto-research**: true
```

If settings exist, apply them as defaults (CLI arguments override settings file values).

### Step 3: Validate Adapter

Check that an adapter file exists for the target platform:

1. Use `Glob` to check `${CLAUDE_PLUGIN_ROOT}/references/adapters/{TARGET_PLATFORM}.md`
2. If the adapter file exists, read it and store as `ADAPTER`
3. If no adapter file exists:
   - Inform the user: "No adapter file found for '{TARGET_PLATFORM}'. The research agent will investigate the platform from scratch, and a new adapter file can be created from the findings."
   - Set `ADAPTER = null`
   - Continue — the research phase will gather platform information

### Step 4: Load Marketplace Registry

Read the marketplace registry to enumerate available plugin groups:

```
Read: ${CLAUDE_PLUGIN_ROOT}/../../.claude-plugin/marketplace.json
```

Parse the `plugins` array. Each entry has:
- `name` — Full plugin name (e.g., `agent-alchemy-core-tools`)
- `version` — Current version
- `description` — Brief description
- `source` — Relative path to plugin directory (e.g., `./core-tools`)

Build a list of available plugin groups, extracting the short group name from the source path (e.g., `core-tools` from `./core-tools`).

**Exclude `plugin-tools` from the selection list** — the porter should not attempt to port itself.

---

## Phase 2: Plugin Selection Wizard

**Goal:** Guide the user through selecting which plugin groups and individual components to port.

### Step 1: Target Platform Confirmation

Inform the user of the target platform and configuration:

```
Target platform: {TARGET_PLATFORM}
Adapter: {adapter file path or "None — research agent will investigate"}
Dry-run: {DRY_RUN}
```

### Step 2: Group-Level Selection

Present all available plugin groups for selection using `AskUserQuestion` with `multiSelect: true`.

For each plugin group, scan its directory to count components:

1. Use `Glob` to count skills: `claude/{group}/skills/*/SKILL.md`
2. Use `Glob` to count agents: `claude/{group}/agents/*.md`
3. Use `Glob` to check for hooks: `claude/{group}/hooks/hooks.json`
4. Use `Glob` to count reference dirs: `claude/{group}/skills/*/references/`
5. Use `Glob` to check for MCP config: `claude/{group}/.mcp.json`

Build the selection options:

```yaml
AskUserQuestion:
  questions:
    - header: "Plugin Group Selection"
      question: "Which plugin groups would you like to port to {TARGET_PLATFORM}?"
      options:
        - label: "{group-name} (v{version})"
          description: "{skill_count} skills, {agent_count} agents{, hooks}{, MCP config} — {marketplace description}"
      multiSelect: true
```

**Edge case — Empty plugin group:** If a scanned group has zero skills, zero agents, no hooks, and no MCP config, skip it from the selection list and note: "Skipped {group}: no portable components found."

Store the selected groups as `SELECTED_GROUPS`.

If no groups are selected (user cancels or selects nothing), use `AskUserQuestion` to confirm:
```yaml
AskUserQuestion:
  questions:
    - header: "No Selection"
      question: "No plugin groups were selected. Would you like to start over or cancel?"
      options:
        - label: "Start over"
          description: "Return to group selection"
        - label: "Cancel"
          description: "Exit the porter"
      multiSelect: false
```

If "Start over", repeat Step 2. If "Cancel", end the workflow gracefully.

### Step 3: Component-Level Selection

For each selected group, scan and enumerate all individual components, then present for selection.

**Component scanning per group:**

1. **Skills**: For each `claude/{group}/skills/*/SKILL.md`:
   - Read the frontmatter to extract `name` and `description`
   - Check for `references/` subdirectory and count reference files
   - Format: `skill:{group}/{skill-name}` with description

2. **Agents**: For each `claude/{group}/agents/*.md`:
   - Read the frontmatter to extract `name`, `description`, and `model`
   - Format: `agent:{group}/{agent-name}` with description and model tier

3. **Hooks**: If `claude/{group}/hooks/hooks.json` exists:
   - Read the file and count hook entries
   - Format: `hooks:{group}` with hook count and event types

4. **MCP Config**: If `claude/{group}/.mcp.json` exists:
   - Read the file and list configured servers
   - Format: `mcp:{group}` with server names

Present components for each group using `AskUserQuestion`:

```yaml
AskUserQuestion:
  questions:
    - header: "{group-name} Components"
      question: "Select components to port from {group-name}:"
      options:
        - label: "All components"
          description: "Port everything in {group-name} ({total_count} components)"
        - label: "skill: {skill-name}"
          description: "{skill description} ({ref_count} references)"
        - label: "agent: {agent-name}"
          description: "{agent description} (model: {model})"
        - label: "hooks: {group}"
          description: "{hook_count} hooks ({event types})"
        - label: "mcp: {group}"
          description: "MCP config ({server names})"
      multiSelect: true
```

**Edge case — "All components" selected:** If the user selects "All components", include every component from that group in the selection. Do not present further sub-selection.

Build the final component list as `SELECTED_COMPONENTS`, a flat list of component identifiers with their types:

```
[
  { type: "skill", group: "core-tools", name: "deep-analysis", path: "claude/core-tools/skills/deep-analysis/SKILL.md" },
  { type: "agent", group: "core-tools", name: "code-explorer", path: "claude/core-tools/agents/code-explorer.md" },
  { type: "hooks", group: "core-tools", name: "hooks", path: "claude/core-tools/hooks/hooks.json" },
  ...
]
```

### Step 4: Selection Summary

Present a summary of the selection to the user:

```
## Selection Summary

**Target platform:** {TARGET_PLATFORM}
**Plugin groups:** {count} selected
**Total components:** {count}

| Group | Skills | Agents | Hooks | MCP | References |
|-------|--------|--------|-------|-----|------------|
| {group} | {n} | {n} | {yes/no} | {yes/no} | {n} files |

Components:
- {component list with types}
```

Use `AskUserQuestion` to confirm:

```yaml
AskUserQuestion:
  questions:
    - header: "Confirm Selection"
      question: "Proceed with this selection?"
      options:
        - label: "Proceed"
          description: "Continue to dependency validation"
        - label: "Modify selection"
          description: "Go back and change component selection"
        - label: "Cancel"
          description: "Exit the porter"
      multiSelect: false
```

If "Modify selection", return to Step 2.
If "Cancel", end the workflow gracefully.

---

## Phase 3: Dependency Validation

**Goal:** Build a full dependency graph from selected components, detect all five dependency types, flag missing references and external dependencies, and produce a dependency-sorted conversion order for Phase 5.

This phase consumes `SELECTED_COMPONENTS` and `SELECTED_GROUPS` from Phase 2 and produces `DEPENDENCY_GRAPH` (including `CONVERSION_ORDER`) for Phase 5.

### Step 1: Parse Dependencies

For each component in `SELECTED_COMPONENTS`, read its source file and extract all dependency references. Initialize a flat dependency list:

```
DEPENDENCIES = []   // each entry: { source, target_type, target_ref, dep_type, raw_pattern, transitive }
```

Process each component type using the sub-steps below. Apply these error handling rules during scanning:

**Error: Unreadable file.** If a component file cannot be read (permission error, file missing, I/O error), log a warning and continue scanning the remaining components:
```
WARNING: Could not read {component.path} -- skipping dependency scan for this component.
```

**Error: Malformed YAML frontmatter.** If a component's YAML frontmatter cannot be parsed (invalid YAML between `---` delimiters), log a parsing error and fall back to body-only scanning for that component:
```
WARNING: Malformed YAML frontmatter in {component.path} -- scanning body text only for dependencies.
```

#### 1a: Skill Dependencies

For each skill component (`type: "skill"`), read its `SKILL.md` and scan for all five dependency types:

**Dependency Type 1 -- Skill-to-skill references:**

Scan the skill body for patterns that load another skill from the same plugin group:
```
Read ${CLAUDE_PLUGIN_ROOT}/skills/{skill-name}/SKILL.md
```

For each match, extract `{skill-name}` and record:
```
{ source: this_component, target_type: "skill", target_ref: "{this_group}/{skill-name}", dep_type: "skill-to-skill", raw_pattern: "{matched line}", transitive: false }
```

**Dependency Type 2 -- Cross-plugin references:**

Scan the body for patterns that reference a different plugin group:
```
${CLAUDE_PLUGIN_ROOT}/../{source-dir-name}/skills/{skill-name}/SKILL.md
${CLAUDE_PLUGIN_ROOT}/../{source-dir-name}/agents/{agent-name}.md
${CLAUDE_PLUGIN_ROOT}/../{source-dir-name}/
```

For each match, extract `{source-dir-name}` and the component name, and record:
```
{ source: this_component, target_type: "skill" or "agent", target_ref: "{source-dir-name}/{name}", dep_type: "cross-plugin", raw_pattern: "{matched line}", transitive: false }
```

**Dependency Type 3 -- Reference file includes:**

Scan the body for patterns that load reference files:
```
Read ${CLAUDE_PLUGIN_ROOT}/skills/{skill-name}/references/{filename}
${CLAUDE_PLUGIN_ROOT}/skills/{skill-name}/references/{filename}
```

For each match, determine if the reference belongs to this skill or another skill:
- References to this skill's own `references/` directory are internal by definition and do not create a dependency edge
- References to another skill's `references/` directory create a dependency:
```
{ source: this_component, target_type: "reference", target_ref: "{group}/{skill-name}/references/{filename}", dep_type: "reference-include", raw_pattern: "{matched line}", transitive: false }
```

**Dependency Type 4 -- Agent/subagent references:**

Scan the body for Task tool invocations that spawn agents:
```
subagent_type: "{agent-name}"
```

For each match, record:
```
{ source: this_component, target_type: "agent", target_ref: "{group}/{agent-name}", dep_type: "skill-to-skill", raw_pattern: "{matched line}", transitive: false }
```

**External dependencies (non-component):**

Scan for system-level dependencies that cannot be ported as components:
- MCP server tool references: patterns like `mcp__{server}__{tool}` or the `mcp__` prefix in the body or `allowed-tools` list
- Bash script invocations: references to specific script files (paths ending in `.sh`, `.py`, `.js`)

For each external dependency found:
```
{ source: this_component, target_type: "external", target_ref: "{description}", dep_type: "external", raw_pattern: "{matched line}", transitive: false }
```

#### 1b: Agent Dependencies

For each agent component (`type: "agent"`), read its `.md` file:

**Dependency Type 5 -- Agent-to-skill references:**

Parse the YAML frontmatter and extract the `skills:` field (array of skill identifiers). For each skill listed:
```
{ source: this_component, target_type: "skill", target_ref: "{resolved skill reference}", dep_type: "agent-to-skill", raw_pattern: "skills: [{skill}]", transitive: false }
```

Also scan the agent's markdown body for `Read ${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PLUGIN_ROOT}/../` patterns, applying the same Type 1, Type 2, and Type 3 scans from Step 1a.

**Tool dependencies (informational only):**

Parse the `tools:` field from frontmatter. These are Claude Code platform tools classified as `System` dependencies. They do not create dependency edges but are tracked for the gap report.

#### 1c: Hook Dependencies

For each hooks component (`type: "hooks"`), read the `hooks.json` file and parse the JSON:

**Dependency Type 4 -- Hook-to-script references:**

For each hook entry, extract the `command` field and scan for:
- Script file paths: any path in the command string (e.g., `${CLAUDE_PLUGIN_ROOT}/hooks/scripts/auto-approve.sh`)
- Direct script references: paths ending in `.sh`, `.py`, `.js`, or other executable extensions

For each script reference:
```
{ source: this_component, target_type: "script", target_ref: "{script path}", dep_type: "hook-to-script", raw_pattern: "{command value}", transitive: false }
```

Tool matcher patterns in hooks reference Claude Code tool names -- classify these as `System` dependencies for informational tracking only.

#### 1d: MCP Config Dependencies

For each MCP config component (`type: "mcp"`), read the `.mcp.json` file:

Each configured MCP server is an external dependency requiring manual porting on the target platform. Record each server:
```
{ source: this_component, target_type: "external", target_ref: "MCP server: {server_name} ({command})", dep_type: "external", raw_pattern: "{server config snippet}", transitive: false }
```

### Step 2: Build Dependency Graph

Construct a directed dependency graph from the parsed dependencies.

#### 2a: Create Graph Nodes and Edges

**Nodes:** All components in `SELECTED_COMPONENTS`, each identified by `{type}:{group}/{name}`.

**Edges:** For each entry in `DEPENDENCIES` where `dep_type` is NOT `"external"` and NOT a system dependency, create a directed edge from the `source` node to the node matching `target_ref`.

#### 2b: Classify Each Dependency

For each dependency in `DEPENDENCIES`, determine its classification by checking `target_ref` against `SELECTED_COMPONENTS` and `SELECTED_GROUPS`:

| Classification | Condition |
|---|---|
| **Internal** | Target component exists in `SELECTED_COMPONENTS` |
| **External-selected** | Target component's group is in `SELECTED_GROUPS` but the specific component was not individually selected |
| **External-missing** | Target component's group is NOT in `SELECTED_GROUPS` and not available in the marketplace |
| **System** | Target is a Claude Code platform feature (built-in tool, MCP protocol feature) |
| **External** | Target is a non-component dependency (MCP server process, bash script, external service) |

#### 2c: Resolve Deeply Nested References (Recursive)

Dependencies can form chains: Skill A loads Skill B, which loads Skill C, which loads Skill D. To ensure the full transitive dependency tree is captured:

1. Start with the directly parsed dependencies from Step 1 (all have `transitive: false`)
2. Build a set `SCANNED_COMPONENTS` containing all components already processed in Step 1
3. For each dependency classified as `External-missing` or `External-selected`:
   a. Determine the file path of the target component on disk (using the component scanning conventions: `claude/{group}/skills/{name}/SKILL.md` for skills, `claude/{group}/agents/{name}.md` for agents)
   b. If the file exists and the component is NOT in `SCANNED_COMPONENTS`:
      - Read the file and scan it using the same rules from Step 1a/1b/1c/1d
      - Mark all newly discovered dependencies with `transitive: true`
      - Add newly found dependencies to `DEPENDENCIES`
      - Add the component to `SCANNED_COMPONENTS`
   c. If the file does not exist, skip it (it will be reported as unresolvable in Step 4)
4. Repeat step 3 for any newly discovered `External-missing` or `External-selected` dependencies
5. **Recursion depth limit:** Cap at depth 10 to prevent runaway expansion. If depth 10 is reached, log:
   ```
   WARNING: Dependency chain depth limit (10) reached starting from {root component}. Some transitive dependencies may not be fully resolved.
   ```

#### 2d: Detect Circular Dependencies

Run a cycle detection pass on the dependency graph using depth-first search:

1. For each node in the graph, perform a depth-first traversal
2. Maintain a traversal stack (current path from root)
3. If a node is encountered that is already on the current stack, a cycle exists
4. Record each unique cycle (avoid duplicates for cycles detected from different starting nodes):
   ```
   CIRCULAR_REFS = [
     { cycle: ["{component_id_1}", "{component_id_2}", ..., "{component_id_1}"], warning: "Circular dependency detected" }
   ]
   ```
5. Circular references are warnings that do not block conversion. They will be handled during Phase 5 via topological sort with cycle-breaking.

### Step 3: Self-Contained Check

Before alerting the user, determine whether the selection has any unresolved dependencies.

Count dependencies by classification:
- `internal_count` -- dependencies already satisfied within the selection
- `external_selected_count` -- dependencies in selected groups but not individually selected
- `external_missing_count` -- dependencies not in any selected group
- `external_count` -- non-component external dependencies (MCP servers, scripts)
- `system_count` -- Claude Code platform dependencies

**If `external_selected_count == 0` AND `external_missing_count == 0` AND `external_count == 0`:**

The selection is fully self-contained. Display a brief confirmation and skip to Step 5:

```
All dependencies resolved -- no missing cross-plugin references.
{internal_count} internal dependencies found between selected components.
```

**Otherwise**, proceed to Step 4.

### Step 4: Alert on Missing Dependencies

Present the dependency analysis to the user, organized by category:

```
## Dependency Analysis

**Components scanned:** {SELECTED_COMPONENTS.length}
**Total dependencies found:** {DEPENDENCIES.length}
**Internal (resolved):** {internal_count}
**Missing component dependencies:** {external_selected_count + external_missing_count}
**External (manual porting needed):** {external_count}
**System (Claude Code platform):** {system_count}

{If external_selected_count + external_missing_count > 0:}
### Missing Component Dependencies

These selected components depend on components not in your selection:

| Source Component | Depends On | Dependency Type | Group | Reference Pattern |
|---|---|---|---|---|
| {source.name} | {target_ref} | {dep_type} | {target_group} | `{raw_pattern snippet}` |

{If any dependency has transitive: true:}
Note: Dependencies marked with (*) are transitive -- discovered by following dependency chains beyond the initial selection.

{If external_count > 0:}
### External Dependencies (Manual Porting Required)

These dependencies cannot be automatically ported and will require manual setup on the target platform:

| Source Component | External Dependency | Type | Notes |
|---|---|---|---|
| {source.name} | {target_ref} | MCP server / bash script | Requires manual configuration |

These will be documented in the gap report with setup instructions.
```

#### 4a: Resolve Missing Component Dependencies

**If there are missing component dependencies** (`external_selected_count + external_missing_count > 0`):

Use `AskUserQuestion` to let the user decide:

```yaml
AskUserQuestion:
  questions:
    - header: "Missing Dependencies"
      question: "Some selected components depend on {external_selected_count + external_missing_count} components not in your selection. How would you like to handle this?"
      options:
        - label: "Add missing dependencies"
          description: "Include {count} additional components to resolve all references"
        - label: "Proceed without them"
          description: "Continue -- missing references will be flagged in the gap report"
        - label: "Go back to selection"
          description: "Return to component selection to adjust"
      multiSelect: false
```

**If "Add missing dependencies":**
1. For each `External-selected` dependency: locate the component in its group directory, build its component entry (type, group, name, path), and add to `SELECTED_COMPONENTS`
2. For each `External-missing` dependency: scan the component from disk using the component scanning conventions, build its entry, and add to `SELECTED_COMPONENTS`
3. Re-run Steps 1 and 2 to capture any new transitive dependencies introduced by the added components
4. Repeat the self-contained check (Step 3). If new missing dependencies are found, present Step 4 again. Continue until either the selection is self-contained or the user chooses to proceed without remaining dependencies.

**If "Go back to selection":** Return to Phase 2 Step 2.

**If "Proceed without them":** Continue to Step 5. Missing dependencies will be tracked as entries in `CONVERSION_GAPS` during Phase 5.

#### 4b: Report Circular References

**If circular references were detected** (from Step 2d):

Display a warning after the missing dependencies resolution:

```
### Circular References Detected

WARNING: {CIRCULAR_REFS.length} circular dependency chain(s) found:

{For each cycle in CIRCULAR_REFS:}
- {cycle[0]} -> {cycle[1]} -> ... -> {cycle[0]}

These will be handled during conversion (Phase 5) using topological sort with cycle-breaking.
The component with the fewest incoming dependencies in each cycle will be processed first.
```

Circular references do not require user action -- they are informational warnings. Proceed to Step 5.

### Step 5: Dependency Graph Summary

Build the final dependency graph summary and compute the conversion order for Phase 5.

#### 5a: Topological Sort

Compute a dependency-sorted conversion order:

1. Start with components that have zero unresolved dependencies (leaf nodes with no outgoing edges to other selected components)
2. Process in layers: each layer contains components whose dependencies are all in previous layers
3. **Cycle-breaking:** For components involved in circular references, break each cycle by placing the component with the fewest incoming edges first, then continue the sort normally
4. Within each layer, sort alphabetically by `{type}:{group}/{name}` for deterministic ordering

Store the sorted list as `CONVERSION_ORDER`.

#### 5b: Display Summary

```
## Dependency Graph

**Components:** {SELECTED_COMPONENTS.length}
**Internal dependencies:** {internal_count}
**External dependencies (to be flagged):** {external_count + external_missing_count}
**Circular references:** {CIRCULAR_REFS.length or "none"}
**System dependencies:** {system_count} Claude Code platform features

Conversion order (dependency-sorted):
1. {component_id} -- no dependencies
2. {component_id} -- depends on: {dep1}, {dep2}
3. {component_id} -- depends on: {dep1}
...
```

#### 5c: Store Dependency Graph

Store the complete graph as `DEPENDENCY_GRAPH` for consumption by Phase 5:

```
DEPENDENCY_GRAPH = {
  nodes: SELECTED_COMPONENTS,
  edges: DEPENDENCIES,
  circular_refs: CIRCULAR_REFS,
  conversion_order: CONVERSION_ORDER,
  external_deps: [entries where dep_type == "external"],
  classification_counts: { internal, external_selected, external_missing, external, system }
}
```

---

## Phase 4: Platform Research

**Goal:** Spawn a research subagent to investigate the target platform's current plugin architecture, compare findings against the existing adapter file, and produce a merged knowledge base for conversion.

### Step 1: Prepare Research Context

Before spawning the research agent, gather the context it needs:

1. **Count selected components by type** from `SELECTED_COMPONENTS`:
   - `skill_count` — number of skill components
   - `agent_count` — number of agent components
   - `hook_count` — number of hooks components
   - `ref_count` — total reference files across all selected skills
   - `mcp_count` — number of MCP config components

2. **Extract adapter content** (if `ADAPTER` exists):
   - Read the full content of the adapter file at `${CLAUDE_PLUGIN_ROOT}/references/adapters/{TARGET_PLATFORM}.md`
   - Store the raw content as `ADAPTER_CONTENT` for inclusion in the research prompt
   - Extract the adapter's `target_platform_version` field from the Adapter Version section

3. **Build component summary** — a brief list of what is being ported, to help the research agent focus on relevant platform features:
   ```
   Components to convert:
   - Skills: {list of skill names}
   - Agents: {list of agent names with model tiers}
   - Hooks: {yes/no, with event types if yes}
   - References: {count} files
   - MCP configs: {yes/no, with server names if yes}

   Key features used by these components:
   - {e.g., "Task tool for subagent spawning (used by deep-analysis)"}
   - {e.g., "AskUserQuestion for interactive workflows (used by create-spec)"}
   - {e.g., "Cross-plugin composition via ${CLAUDE_PLUGIN_ROOT}/../ paths"}
   ```

### Step 2: Launch Research Agent

Spawn the research agent using the Task tool with `subagent_type: "researcher"` and `model: "sonnet"`:

```
Task tool prompt:
"Research the plugin/extension system for: {TARGET_PLATFORM}

You are researching this platform to support converting Agent Alchemy (Claude Code) plugins to {TARGET_PLATFORM} format. The conversion needs to handle {skill_count} skills, {agent_count} agents, {hook_count} hook configs, {ref_count} reference files, and {mcp_count} MCP configs.

{If ADAPTER exists:}
## Existing Adapter File

An adapter file already exists for this platform. Here is its full content:

---BEGIN ADAPTER---
{ADAPTER_CONTENT}
---END ADAPTER---

IMPORTANT: Compare your research findings against every mapping in this adapter file. In your Adapter Comparison section:
- Flag any mappings that appear outdated based on your research
- Identify new platform features or changes not covered by the adapter
- Note the adapter's platform version ({adapter_platform_version}) vs. the current version you find
- For each stale or missing mapping, provide the corrected/new mapping

{If ADAPTER is null:}
## No Existing Adapter

No adapter file exists for this platform yet. Research from scratch and produce a comprehensive platform profile. Your findings will be the primary source of truth for the conversion engine.

## Components Being Ported

{component_summary from Step 1}

## Research Focus Areas

Investigate these areas thoroughly — they directly affect conversion quality:

1. **Plugin directory structure**: Where plugins live, file naming conventions, required files
2. **Configuration format**: YAML, JSON, TOML, or other formats for plugin metadata
3. **Tool/capability equivalents**: What built-in tools does the platform provide? Map against Claude Code's tools (Read, Write, Edit, Glob, Grep, Bash, Task, WebSearch, WebFetch, AskUserQuestion)
4. **Model configuration**: How are AI models specified? Does the platform support model tiers or selection?
5. **Lifecycle hooks**: Does the platform have pre/post execution hooks? Event system?
6. **Composition mechanism**: How do plugins load or reference other plugins? Is there an equivalent to skill composition via prompt injection?
7. **Path resolution**: Equivalent of ${CLAUDE_PLUGIN_ROOT} for resolving plugin-relative paths
8. **Agent/subagent support**: Can plugins spawn sub-tasks or sub-agents? How?
9. **User interaction**: How do plugins prompt the user for input during execution?
10. **MCP integration**: Does the platform support Model Context Protocol servers?

Return a structured platform profile following your output format specification. Include confidence levels for every finding."
```

**Retry logic:** If the Task tool call fails (agent error, timeout, or empty response), retry once automatically. If the retry also fails, proceed to the research failure handling in Step 5.

### Step 3: Process Research Findings

When the research agent returns its platform profile:

1. **Parse the structured platform profile** from the response. Extract these sections:
   - Research Summary (documentation quality, sources consulted, overall confidence)
   - Plugin System Overview
   - Directory Structure
   - File Format
   - Tool Equivalents table
   - Model Tier Mappings table
   - Composition Patterns
   - Lifecycle Hooks
   - Known Limitations
   - Adapter Comparison (if adapter was provided)
   - Sources list

2. **Store as `RESEARCH_FINDINGS`** — the parsed profile is available throughout the remaining phases for the conversion engine to reference.

3. **Merge research with adapter into `CONVERSION_KNOWLEDGE`:**

   The conversion engine uses a merged knowledge base called `CONVERSION_KNOWLEDGE` that combines the adapter file and research findings with clear precedence rules:

   | Category | Precedence Rule |
   |----------|----------------|
   | Tool name mappings | Adapter takes precedence for established mappings; research fills gaps where adapter has `null` or no entry |
   | Model tier mappings | Adapter takes precedence; research supplements with version-specific notes |
   | Platform version info | Research always takes precedence (it is fresher) |
   | Directory structure | Research takes precedence if it differs from adapter (platform may have changed) |
   | Composition patterns | Research takes precedence if it provides more detail; adapter is baseline |
   | Lifecycle hooks | Research takes precedence if it finds new hook types; adapter is baseline |
   | Known limitations | Union of both — all limitations from adapter AND research are tracked |
   | Path resolution | Research takes precedence if adapter mapping is marked as uncertain |

   When adapter and research agree on a mapping, mark it as `confidence: high`.
   When only one source provides a mapping, mark it as `confidence: medium`.
   When adapter and research disagree, mark it as `confidence: conflict` and flag for user resolution in Step 4.

4. **Check for adapter staleness:**

   Initialize `STALENESS_STATUS` to track the result for migration guide logging:

   ```
   STALENESS_STATUS = {
     checked: false,
     adapter_version: null,
     adapter_platform_version: null,
     research_platform_version: null,
     is_stale: false,
     is_unversioned: false,
     research_has_version: false,
     stale_mappings: [],
     new_features: [],
     user_decision: null,
     error: null
   }
   ```

   **Wrap the entire staleness check in error-safe logic.** If any step below fails (parsing error, unexpected format, etc.), set `STALENESS_STATUS.error` to a description of the failure, log a warning ("Staleness check encountered an error: {error}. Proceeding with conversion."), and continue to Step 4. The staleness check must never block the conversion workflow.

   If `ADAPTER` exists:

   a. **Read adapter version fields** from the Adapter Version section of the adapter file:
      - Extract `adapter_version` (the adapter file's own version, e.g., `1.0.0`)
      - Extract `target_platform_version` (the platform version the adapter was written for, e.g., `0.0.55`)
      - Set `STALENESS_STATUS.checked = true`
      - If neither field is found, set `STALENESS_STATUS.is_unversioned = true` and log a warning: "Adapter file for {TARGET_PLATFORM} has no version fields. Staleness cannot be determined — proceeding with adapter as-is."

   b. **Check if research reported a platform version:**
      - Look for a version in the research findings (Platform Overview, Research Summary, or version-related fields)
      - If research did not report a version, set `STALENESS_STATUS.research_has_version = false` and log a note: "Research did not report a specific platform version for {TARGET_PLATFORM}. Skipping version comparison."
      - If research reported a version, set `STALENESS_STATUS.research_has_version = true` and store it in `STALENESS_STATUS.research_platform_version`

   c. **Compare versions** (only if both adapter and research have version information):
      - Perform version comparison using these rules:
        - **Exact match**: If `target_platform_version` equals `research_platform_version` exactly, versions match — `STALENESS_STATUS.is_stale = false`
        - **Semantic version comparison**: If both versions follow semver format (e.g., `0.0.55`, `1.2.3`), compare numerically. If research version is newer, set `STALENESS_STATUS.is_stale = true`
        - **Fuzzy comparison**: If version formats differ (e.g., adapter has `0.0.55` but research reports `v0.0.55`, `0.0.55-beta`, or a date-based version), attempt normalization:
          - Strip leading `v` or `V` prefix
          - Strip trailing pre-release suffixes (`-alpha`, `-beta`, `-rc.1`, etc.) for comparison
          - If normalized versions match, treat as matching
          - If normalization fails or formats are incomparable, set `STALENESS_STATUS.is_stale = true` (err on the side of warning) and note: "Version format mismatch — adapter: '{adapter_version}', research: '{research_version}'. Treating as potentially stale."

   d. **Collect stale mappings and new features** (regardless of version match, if research provides an Adapter Comparison section):
      - If the Adapter Comparison section flags outdated mappings, collect them as `STALE_MAPPINGS` and store in `STALENESS_STATUS.stale_mappings`
      - If the research found new platform features not in the adapter, collect them as `NEW_FEATURES` and store in `STALENESS_STATUS.new_features`
      - If stale mappings or new features exist even when versions match, set `ADAPTER_STALE = true` (content staleness despite version match)

### Step 4: Resolve Conflicts

If any mappings in `CONVERSION_KNOWLEDGE` are marked as `confidence: conflict`:

1. **Build a conflict list** summarizing each disagreement:
   ```
   Conflicts found between adapter file and research findings:

   1. {mapping_name}:
      - Adapter says: {adapter_value}
      - Research says: {research_value} (source: {url})
      - Impact: {which components are affected}

   2. {mapping_name}:
      ...
   ```

2. **Present conflicts to user via AskUserQuestion** for each conflict (or batch if fewer than 5):

   ```yaml
   AskUserQuestion:
     questions:
       - header: "Research Conflict"
         question: "The adapter file and fresh research disagree on {mapping_name}. Which should be used for conversion?"
         options:
           - label: "Use research finding"
             description: "{research_value} — from {source}, researched today"
           - label: "Use adapter mapping"
             description: "{adapter_value} — from adapter file v{adapter_version}"
           - label: "Skip this mapping"
             description: "Flag as unresolved in the gap report"
         multiSelect: false
   ```

3. **Apply resolutions** to `CONVERSION_KNOWLEDGE`:
   - "Use research finding": Update the mapping to the research value, set `confidence: high`, mark `source: research`
   - "Use adapter mapping": Keep the adapter value, set `confidence: high`, mark `source: adapter`
   - "Skip this mapping": Set `confidence: unresolved`, will appear in the gap report

If there are no conflicts, skip this step entirely.

### Step 5: Present Research Summary

Display a summary of the research findings and merged knowledge to the user:

```
## Platform Research: {TARGET_PLATFORM}

**Documentation quality:** {research_summary.documentation_quality}
**Sources consulted:** {research_summary.sources_consulted}
**Overall confidence:** {research_summary.overall_confidence}

### Key Findings
- **Plugin format:** {file_format description}
- **Tool equivalents:** {matched_count}/{total_count} Claude Code tools have equivalents
- **Model support:** {model_tier_summary}
- **Composition:** {composition_patterns summary}
- **Hooks:** {lifecycle_hooks summary — supported/not supported/partial}
- **Agent spawning:** {agent/subagent support summary}
- **User interaction:** {user interaction mechanism summary}

### Knowledge Sources for Conversion
- Adapter file mappings: {count} mappings
- Research-supplemented mappings: {count} new/updated mappings
- Conflicts resolved: {count}
- Unresolved gaps: {count}

{If STALENESS_STATUS.is_unversioned = true:}
### Adapter Version Notice

NOTE: The adapter file for {TARGET_PLATFORM} has no version fields. Staleness cannot be determined. The adapter will be used as-is, supplemented by research findings.

{If STALENESS_STATUS.research_has_version = false AND ADAPTER exists:}
### Research Version Notice

NOTE: Research did not report a specific platform version for {TARGET_PLATFORM}. Version comparison was skipped. The adapter's target_platform_version ({STALENESS_STATUS.adapter_platform_version}) is assumed current.

{If STALENESS_STATUS.error:}
### Staleness Check Notice

NOTE: The staleness check encountered an error: {STALENESS_STATUS.error}. Conversion will proceed using available adapter and research data.

{If ADAPTER_STALE = true:}
### Adapter Staleness Warning

WARNING: The existing adapter file targets {TARGET_PLATFORM} v{STALENESS_STATUS.adapter_platform_version}, but research found the current version is v{STALENESS_STATUS.research_platform_version}.

Stale mappings detected:
{For each stale mapping in STALENESS_STATUS.stale_mappings:}
- {mapping_name}: adapter says "{old_value}", research found "{new_value}"

New platform features not in adapter:
{For each new feature in STALENESS_STATUS.new_features:}
- {feature_name}: {description}

{If no ADAPTER:}
### New Platform Profile

Research produced a fresh platform profile since no adapter file existed.
Consider saving a new adapter file from these findings after conversion.
```

After displaying the summary, if `ADAPTER_STALE = true`, present the user with options via `AskUserQuestion`:

```yaml
AskUserQuestion:
  questions:
    - header: "Adapter Staleness"
      question: "The adapter file for {TARGET_PLATFORM} appears to be stale (adapter targets v{STALENESS_STATUS.adapter_platform_version}, research found v{STALENESS_STATUS.research_platform_version}). {stale_mapping_count} mappings may be outdated and {new_feature_count} new platform features were found. How would you like to proceed?"
      options:
        - label: "Proceed with existing adapter"
          description: "Continue conversion — research findings will supplement and override stale adapter mappings via CONVERSION_KNOWLEDGE precedence rules"
        - label: "Update adapter file first"
          description: "Pause conversion to update the adapter file with research findings, then resume"
      multiSelect: false
```

**Handle each choice:**

- **"Proceed with existing adapter"**: Set `STALENESS_STATUS.user_decision = "proceed"`. Continue to Phase 5 using `CONVERSION_KNOWLEDGE` as already merged (research takes precedence for stale mappings per the precedence rules in Step 3). Log: "User chose to proceed with existing adapter. Research findings will supplement stale mappings during conversion."

- **"Update adapter file first"**: Set `STALENESS_STATUS.user_decision = "update"`. Before continuing to Phase 5:
  1. Read the current adapter file at `${CLAUDE_PLUGIN_ROOT}/references/adapters/{TARGET_PLATFORM}.md`
  2. Apply research findings to update stale mappings in-place:
     - For each entry in `STALE_MAPPINGS`: update the mapping value in the adapter to match the research finding
     - For each entry in `NEW_FEATURES`: add the feature to the appropriate adapter section
     - Update the `target_platform_version` field to the research-reported version
     - Update the `last_updated` field to today's date
     - Increment the `adapter_version` patch number (e.g., `1.0.0` -> `1.0.1`)
     - Append to the `changelog` field describing the update
  3. Write the updated adapter file
  4. Re-read the updated adapter as `ADAPTER` and re-merge into `CONVERSION_KNOWLEDGE`
  5. Log: "Adapter file updated to target {TARGET_PLATFORM} v{research_platform_version}. Conversion will use updated mappings."

If `STALENESS_STATUS.is_unversioned = true` and stale mappings or new features were found, also present the AskUserQuestion above (since content can be stale even without version fields).

**Record staleness status for migration guide:**

Store `STALENESS_STATUS` for inclusion in the migration guide output (Phase 6). The migration guide should include a "Platform Adapter Status" section documenting:
- Whether a staleness check was performed
- Adapter version vs. research-reported version (if available)
- Whether the adapter was stale, unversioned, or current
- What decision the user made (proceed or update)
- Any stale mappings that were identified
- Any new features discovered by research

### Step 6: Handle Research Failure

If the research agent failed (both initial attempt and retry):

1. **Inform the user** of what happened:
   ```
   The platform research agent was unable to complete its investigation.
   Reason: {error_message or "timeout/empty response"}
   ```

2. **Offer recovery options via AskUserQuestion:**

   ```yaml
   AskUserQuestion:
     questions:
       - header: "Research Issue"
         question: "The platform research agent encountered an issue: {brief_reason}. How would you like to proceed?"
         options:
           - label: "Retry research"
             description: "Launch the research agent again (attempt {retry_count + 1})"
           - label: "Use adapter only"
             description: "Proceed with existing adapter file mappings (no fresh research)"
           - label: "Cancel"
             description: "Exit the porter"
         multiSelect: false
   ```

3. **Handle each choice:**

   - **"Retry research"**: Return to Step 2 and re-launch the research agent. Allow up to 2 total retries (3 attempts total).

   - **"Use adapter only"**:
     - If `ADAPTER` exists: Set `RESEARCH_FINDINGS = null`. Set `CONVERSION_KNOWLEDGE` to adapter mappings only with `confidence: medium` on all entries (no research validation). Inform the user: "Proceeding with adapter file mappings only. Conversion quality may be affected — adapter mappings have not been validated against current platform documentation." Continue to Phase 5.
     - If `ADAPTER` is null: Inform the user: "Cannot proceed — no adapter file exists and research failed. The conversion engine requires at least one source of platform knowledge." Offer:
       ```yaml
       AskUserQuestion:
         questions:
           - header: "No Platform Knowledge Available"
             question: "Neither an adapter file nor research findings are available. What would you like to do?"
             options:
               - label: "Retry research"
                 description: "Try the research agent one more time"
               - label: "Cancel"
                 description: "Exit the porter — conversion cannot proceed without platform knowledge"
             multiSelect: false
       ```

   - **"Cancel"**: End the workflow gracefully with a summary of what was completed so far.

---

## Phase 4.5: Dry-Run Preview

**Goal:** Offer an optional preview of expected conversion output -- showing the target file tree, per-component conversion status, expected issues, and estimated fidelity -- without writing any files or running the full conversion engine.

This phase consumes `SELECTED_COMPONENTS`, `DEPENDENCY_GRAPH` (from Phase 3), and `CONVERSION_KNOWLEDGE` (from Phase 4). It does not modify any of these structures.

### Step 1: Offer Dry-Run Preview

**If `DRY_RUN = true`** (set via `--dry-run` flag): Skip the offer and proceed directly to Step 2 (preview is mandatory).

**If `DRY_RUN = false`**: Use `AskUserQuestion` to offer the preview as an optional step:

```yaml
AskUserQuestion:
  questions:
    - header: "Dry-Run Preview"
      question: "Would you like to preview the expected conversion output before proceeding? This shows the target file tree, per-component status, and expected issues without writing any files."
      options:
        - label: "Run preview"
          description: "Generate and display a dry-run preview of the conversion"
        - label: "Skip preview and convert"
          description: "Proceed directly to interactive conversion (Phase 5)"
      multiSelect: false
```

**If "Skip preview and convert"**: Skip the rest of Phase 4.5 and proceed directly to Phase 5.

**If "Run preview"**: Continue to Step 2.

### Step 2: Generate Preview

Generate the preview by analyzing `CONVERSION_KNOWLEDGE` mappings against each component in `SELECTED_COMPONENTS`. This step predicts conversion outcomes without running the full conversion engine.

**Wrap the entire preview generation in error-safe logic.** If any step below fails (parsing error, unexpected format, etc.), log a warning ("Preview generation encountered an error: {error}. You can still proceed with conversion."), skip to Step 4 (user decision), and offer the option to proceed with conversion despite the preview failure.

#### 2a: Build Target File Tree

For each component in `SELECTED_COMPONENTS`, predict the output file path using `CONVERSION_KNOWLEDGE`:

1. **Skills**: Map source path `claude/{group}/skills/{name}/SKILL.md` to target path using directory structure mappings:
   - Check `CONVERSION_KNOWLEDGE` for `skill_file_pattern` in directory structure mappings
   - If `skill_file_pattern` is defined (e.g., `{name}/SKILL.md`): expand the pattern by replacing `{name}` with the skill name (applying `naming_convention`), then build path: `{plugin_root}/{skill_dir}/{expanded_pattern}` (e.g., `.opencode/skills/deep-analysis/SKILL.md`)
   - If no `skill_file_pattern`: apply `naming_convention` and `file_extension` for a flat filename, then build path: `{plugin_root}/{skill_dir}/{converted_filename}`

2. **Agents**: Map source path `claude/{group}/agents/{name}.md` to target path:
   - If the target platform has an agent concept: `{plugin_root}/{agent_dir}/{converted_filename}`
   - If no agent concept (adapter maps agent type to `null` or alternative): note the mapping strategy (e.g., "merged into skill" or "mapped to fixed type")

3. **Hooks**: Map `claude/{group}/hooks/hooks.json` to the target hooks format:
   - If target supports hooks: `{plugin_root}/{hook_dir}/{target_hook_filename}`
   - If no hook support: note as "unsupported -- will be documented in gap report"

4. **References**: For each reference file in selected skills' `references/` directories:
   - If target supports reference directories: `{plugin_root}/{reference_dir}/{filename}`
   - If no reference support (composition is `none` or `inline`): note as "will be inlined into parent skill"

5. **MCP configs**: Map `claude/{group}/.mcp.json` to the target MCP format:
   - If target supports MCP: `{plugin_root}/{config_dir}/{target_mcp_filename}`
   - If no MCP support: note as "unsupported -- will be documented in gap report"

Store the predicted paths as `PREVIEW_FILE_TREE` -- a list of entries, each containing: `{ source_path, target_path, component_type, component_name, mapping_strategy }`.

#### 2b: Predict Per-Component Conversion Status

For each component, estimate its conversion status by analyzing how well `CONVERSION_KNOWLEDGE` covers the component's features:

1. **Read the component source file** (already loaded during Phase 2/3)
2. **Count mappable features**:
   - Frontmatter fields: count fields, check how many have non-null mappings in frontmatter mappings
   - Tool references: count tools in `allowed-tools` and body, check how many have non-null mappings in tool name mappings
   - Composition references: count `${CLAUDE_PLUGIN_ROOT}` patterns, check if composition mechanism is not `none`
   - Path references: count path patterns, check if path resolution root variable is not null
   - User interaction patterns: count `AskUserQuestion` references, check if a mapping exists
3. **Classify the component**:
   - Count `supported` (non-null mapping exists), `partial` (mapping is `partial:*` or workaround-dependent), and `unsupported` (mapping is `null`) features
   - Apply fidelity estimation to calculate a score range:
     ```
     optimistic_score = ((supported + partial) * 1.0 + unsupported * 0.0) / total * 100
     pessimistic_score = ((supported * 1.0) + (partial * 0.7) + (unsupported * 0.0)) / total * 100
     ```
   - Determine predicted status:
     - Both scores >= 80: `"Full"` -- component is highly portable
     - Pessimistic >= 50: `"Partial"` -- component works but with limitations
     - Pessimistic < 50: `"Unsupported"` -- significant gaps, may not be worthwhile

Store predictions as `PREVIEW_STATUS` -- a list of entries, each containing: `{ component_name, component_type, group, supported_count, partial_count, unsupported_count, total_count, optimistic_score, pessimistic_score, predicted_status }`.

#### 2c: Collect Expected Issues

For each component, identify expected issues from the mapping analysis:

1. **Null tool mappings**: List tools that map to `null` in tool name mappings
2. **Null frontmatter fields**: List fields that map to `null` in frontmatter mappings
3. **Unsupported composition**: Flag if composition mechanism is `none` and component uses composition
4. **Unsupported hooks**: Flag if hook events map to `null` in hook event mappings
5. **Missing cross-plugin support**: Flag if component uses cross-plugin references and composition does not support cross-plugin
6. **No user interaction equivalent**: Flag if component uses `AskUserQuestion` and the mapping is `null`

Group issues by severity:
- **Critical**: Features essential to the component's core function (e.g., Task tool for hub-and-spoke skills)
- **Functional**: Features that affect behavior but the component can work without them (e.g., specific tool references)
- **Cosmetic**: Minor formatting or metadata differences (e.g., omitted frontmatter fields)

Store as `PREVIEW_ISSUES` -- a list of entries, each containing: `{ component_name, feature, severity, reason, adapter_notes }`.

#### 2d: Calculate Estimated Fidelity Range

Compute an overall estimated fidelity range across all components:

```
overall_optimistic = sum(component.optimistic_score * component.weight) / sum(component.weight)
overall_pessimistic = sum(component.pessimistic_score * component.weight) / sum(component.weight)
```

Where `weight` is the same as Phase 5 Step 9:
- `skill` = 3, `agent` = 2, `hooks` = 1, `reference` = 1, `mcp` = 1

Round both scores to the nearest integer.

### Step 3: Display Preview

Present the preview in a structured format.

**Large plugin group handling**: If `SELECTED_COMPONENTS` has more than 20 components, summarize the file tree by grouping files by directory rather than listing every individual file. Show the directory structure with file counts per directory instead.

```
## Dry-Run Preview: {TARGET_PLATFORM}

**Components:** {SELECTED_COMPONENTS.length}
**Estimated fidelity:** {overall_pessimistic}% - {overall_optimistic}%

### Target File Tree

{If 20 or fewer components:}

{target_root}/
  {For each entry in PREVIEW_FILE_TREE, sorted by target_path:}
  {target_path}    <- {source_path} [{mapping_strategy}]

{If more than 20 components:}

{target_root}/
  {skill_dir}/          ({skill_count} files)
  {agent_dir}/          ({agent_count} files)
  {hook_dir}/           ({hook_count} files)
  {reference_dir}/      ({ref_count} files)
  {config_dir}/         ({config_count} files)

### Per-Component Conversion Status

| Component | Type | Group | Status | Fidelity Estimate | Issues |
|-----------|------|-------|--------|-------------------|--------|
{For each entry in PREVIEW_STATUS:}
| {component_name} | {component_type} | {group} | {predicted_status} | {pessimistic_score}% - {optimistic_score}% | {issue_count} |

{If all components have predicted_status == "Unsupported":}
### Warning: All Components Unsupported

All selected components are predicted to have significant conversion gaps on {TARGET_PLATFORM}. The overall estimated fidelity is {overall_pessimistic}% - {overall_optimistic}%. Conversion may not produce useful output. Consider:
- Selecting a different target platform
- Selecting fewer, simpler components
- Reviewing the gap details below before proceeding

### Expected Issues

{If PREVIEW_ISSUES is empty:}
No significant issues detected. All features have direct or partial mappings.

{If PREVIEW_ISSUES is not empty:}
{Group by severity, show critical first:}

**Critical ({critical_count}):**
{For each critical issue:}
- **{component_name}**: `{feature}` -- {reason}{If adapter_notes: " ({adapter_notes})"}

**Functional ({functional_count}):**
{For each functional issue:}
- **{component_name}**: `{feature}` -- {reason}

**Cosmetic ({cosmetic_count}):**
{For each cosmetic issue:}
- **{component_name}**: `{feature}` -- {reason}

### Estimated Fidelity

**Overall:** {overall_pessimistic}% - {overall_optimistic}% (weighted by component complexity)

The fidelity range reflects the best-case (all partial mappings succeed fully) and worst-case (partial mappings contribute reduced fidelity) scenarios. The actual score will be determined during interactive conversion when incompatibilities are resolved.
```

### Step 4: User Decision

After displaying the preview, present the user with a decision via `AskUserQuestion`.

**If `DRY_RUN = true`** (invoked with `--dry-run` flag):

```yaml
AskUserQuestion:
  questions:
    - header: "Dry-Run Complete"
      question: "The dry-run preview is complete. No files were written. Would you like to proceed with the actual conversion?"
      options:
        - label: "Proceed with conversion"
          description: "Continue to Phase 5 (Interactive Conversion) and convert the selected components"
        - label: "Done"
          description: "Exit the porter -- preview only"
      multiSelect: false
```

**If `DRY_RUN = false`** (preview was offered and accepted):

```yaml
AskUserQuestion:
  questions:
    - header: "Preview Complete"
      question: "Preview complete. Proceed with interactive conversion?"
      options:
        - label: "Proceed with conversion"
          description: "Continue to Phase 5 and convert the selected components"
        - label: "Cancel"
          description: "Exit the porter"
      multiSelect: false
```

**Handle choices:**

- **"Proceed with conversion"**: Set `DRY_RUN = false` (in case it was true). Continue to Phase 5.
- **"Done" or "Cancel"**: End the workflow gracefully. Display a brief summary:
  ```
  Porter exited after dry-run preview. No files were written.
  Components analyzed: {count}
  Estimated fidelity: {overall_pessimistic}% - {overall_optimistic}%
  ```

---

## Phase 5: Wave-Based Conversion

**Goal:** Convert each selected component using a wave-based agent team, where each `port-converter` agent (Sonnet) handles a single component in an isolated context. The orchestrator (this skill, Opus) manages session files, spawns agent waves, resolves incompatibilities between waves, and consolidates results.

This phase consumes `SELECTED_COMPONENTS`, `CONVERSION_ORDER`, `DEPENDENCY_GRAPH`, and `CONVERSION_KNOWLEDGE` from Phases 2-4.

### Step 1: Initialize Session

Create the session directory and write shared files that converter agents will read.

#### 1a: Create Session Directory

```bash
mkdir -p .claude/sessions/__port_live__/results
```

**If `.claude/sessions/__port_live__/` already exists** (stale session from a previous interrupted run):
1. Archive the stale session: `mv .claude/sessions/__port_live__ .claude/sessions/port-interrupted-{YYYYMMDD}-{HHMMSS}`
2. Recreate: `mkdir -p .claude/sessions/__port_live__/results`
3. Log: "Archived stale porting session to .claude/sessions/port-interrupted-{timestamp}/"

#### 1b: Serialize Conversion Knowledge

Write `CONVERSION_KNOWLEDGE` to `.claude/sessions/__port_live__/conversion_knowledge.md` following the format specified in `${CLAUDE_PLUGIN_ROOT}/skills/port-plugin/references/session-format.md`.

The file contains all 9 adapter mapping sections (tool names, model tiers, skill frontmatter, agent frontmatter, hook events, directory structure, composition mechanism, path resolution, known limitations) serialized as markdown tables and key-value sections.

**This file is written once and not modified during conversion.**

#### 1c: Serialize Dependency Graph

Write `DEPENDENCY_GRAPH` to `.claude/sessions/__port_live__/dependency_graph.md` following the session format reference.

Include: conversion order with wave assignments, dependency edges, circular references (if any), external dependencies, and classification counts.

**This file is written once and not modified during conversion.**

#### 1d: Initialize Resolution Cache

Write an empty resolution cache to `.claude/sessions/__port_live__/resolution_cache.md`:

```markdown
# Resolution Cache

## Cached Decisions

| Group Key | Decision Type | Workaround Applied | First Component | Apply Globally |
|-----------|-------------|-------------------|-----------------|---------------|
```

This file grows between waves as the orchestrator resolves incompatibilities.

#### 1e: Compute Wave Assignments

Using `CONVERSION_ORDER` from Phase 3's topological sort, assign each component to a wave:

- **Wave 1**: Components with zero dependencies on other selected components (leaf nodes)
- **Wave 2**: Components whose dependencies are all in Wave 1
- **Wave N**: Components whose dependencies are all in Waves 1 through N-1

Cap each wave at 5 concurrent agents (matching the `execute-tasks` pattern).

If a wave has more than 5 components, split it into sub-waves of up to 5, maintaining the same dependency level.

#### 1f: Display Execution Plan

Present the wave-based execution plan:

```
## Phase 5: Wave-Based Conversion

**Session directory:** .claude/sessions/__port_live__/
**Total components:** {count}
**Waves:** {wave_count}
**Max concurrent agents per wave:** 5

### Execution Plan

| Wave | Components | Types |
|------|-----------|-------|
| 1 | {component_list} | {type_summary} |
| 2 | {component_list} | {type_summary} |
| ... | ... | ... |

### Session Files Written
- conversion_knowledge.md — {line_count} lines (merged adapter + research)
- dependency_graph.md — {line_count} lines (serialized graph)
- resolution_cache.md — initialized (empty)
- results/ — empty directory for agent output
```

### Step 2: Execute Waves

Process components wave by wave. For each wave, spawn `port-converter` agents in parallel, then resolve incompatibilities between waves.

#### 2a: Wave Loop

For each wave (starting with Wave 1):

**Display wave start:**
```
### Wave {n}/{total_waves}: {component_count} component(s)
```

**Spawn converter agents** using the Task tool with up to 5 parallel calls in a single turn:

For each component in the current wave, launch a `port-converter` agent:

```
Task tool:
  subagent_type: "agent-alchemy-plugin-tools:port-converter"
  model: "sonnet"
  prompt: |
    Convert this component to {TARGET_PLATFORM} format.

    ## Component Details
    - **Type:** {component.type}
    - **Group:** {component.group}
    - **Name:** {component.name}
    - **Source path:** {component.path}
    - **Component ID:** {component.type}-{component.group}-{component.name}

    ## Session Directory
    {absolute_path_to}/.claude/sessions/__port_live__/

    ## Target Platform
    {TARGET_PLATFORM}

    ## Converter Reference to Load
    {If type == "agent": "${CLAUDE_PLUGIN_ROOT}/references/agent-converter.md"}
    {If type == "hooks": "${CLAUDE_PLUGIN_ROOT}/references/hook-converter.md"}
    {If type == "reference": "${CLAUDE_PLUGIN_ROOT}/references/reference-converter.md"}
    {If type == "mcp": "${CLAUDE_PLUGIN_ROOT}/references/mcp-converter.md"}
    {If type == "skill": "None — skill conversion logic is built into the agent"}

    ## Session Format Reference
    Read ${CLAUDE_PLUGIN_ROOT}/skills/port-plugin/references/session-format.md for the result file format specification.
```

**CRITICAL:** Launch all agents in a wave as parallel Task tool calls in a single message. Do not wait for one agent to finish before launching the next within the same wave. This is the key to context isolation — each agent gets its own context window.

**Wait for all agents in the wave to complete** before proceeding.

#### 2b: Collect Wave Results

After all agents in a wave return:

1. **Read all result files** from `.claude/sessions/__port_live__/results/` for this wave's components:
   ```
   Read: .claude/sessions/__port_live__/results/result-{component-id}.md
   ```

2. **Parse each result file** extracting: metadata, converted content, fidelity report, decisions, gaps, and unresolved incompatibilities

3. **Handle missing or error results**: If an agent failed to write a result file, or the result file has `Status = error`:
   - Log: "WARNING: Conversion failed for {component_id}: {error_reason}"
   - Create a placeholder entry in `CONVERTED_COMPONENTS` with `status = "error"` and `fidelity_score = 0`
   - Add a gap entry: `{ component, feature: "entire_component", reason: "Conversion agent failed", severity: "critical" }`

#### 2c: Resolve Incompatibilities

After collecting all wave results, process unresolved incompatibilities:

1. **Collect all unresolved incompatibilities** from the wave's result files (from the Unresolved Incompatibilities tables)

2. **Group by `group_key`** across all results in the wave

3. **Check resolution cache**: Read `.claude/sessions/__port_live__/resolution_cache.md`. For each group:
   - If `group_key` found with `apply_globally = true`: auto-apply the cached decision to the result file's converted content by replacing the inline marker with the resolution. Record with `resolution_mode: "cached"`.
   - If found with `apply_globally = false`: offer to reuse via AskUserQuestion (see below)
   - If not found: present for user resolution

4. **Present remaining incompatibilities to user** using the resolution flow from `${CLAUDE_PLUGIN_ROOT}/references/incompatibility-resolver.md`:

   - **5 or fewer unique groups** (after cache and auto-resolution): present each individually via `AskUserQuestion`
   - **More than 5 unique groups**: present batch summary with options to review individually, auto-apply workarounds + TODO, omit all, or review critical/functional only

   For repeated `group_key` values (same incompatibility seen in a previous wave):

   ```yaml
   AskUserQuestion:
     questions:
       - header: "Repeated Incompatibility"
         question: "'{feature_name}' was already resolved in {previous_component} (decision: {decision_type}). Apply the same decision to {current_component}?"
         options:
           - label: "Apply same decision"
             description: "{previous_decision_description}"
           - label: "Apply to this and all future occurrences"
             description: "Use '{decision_type}' for all remaining '{feature_name}' incompatibilities"
           - label: "Choose differently for this component"
             description: "Open full resolution options"
         multiSelect: false
   ```

5. **Apply resolutions to result files**: For each resolved incompatibility, update the result file's converted content by replacing the `<!-- UNRESOLVED: ... -->` inline marker with the applied resolution:
   - **Workaround**: Replace marker with the workaround text
   - **Omitted**: Remove the marker and clean up surrounding content
   - **TODO**: Replace marker with `<!-- TODO [{TARGET_PLATFORM}]: {feature_name} -- {reason} -->`

   Use the `Edit` tool to modify result files in place.

6. **Update resolution cache**: Write new decisions to `.claude/sessions/__port_live__/resolution_cache.md` by appending rows to the Cached Decisions table.

7. **Cascade impact check**: Using `DEPENDENCY_GRAPH`, check whether any resolved incompatibility affects components in later waves. If so, log a note:
   ```
   Note: Resolution for '{feature_name}' may affect {count} component(s) in later waves: {component_list}
   ```
   Cached resolutions will propagate automatically to later waves via the resolution cache.

#### 2d: Display Wave Summary

After resolving incompatibilities:

```
Wave {n} complete: {component_count} component(s) converted
| Component | Type | Fidelity | Band |
|-----------|------|----------|------|
| {name} | {type} | {score}% | {band} |

Incompatibilities: {resolved_count} resolved, {auto_count} auto-resolved, {cached_count} from cache
```

**Decision review checkpoint**: If total decisions across all waves so far exceeds 10, or this wave had 3+ individual resolutions, offer a brief decision review summary (informational only — past decisions cannot be changed).

#### 2e: Advance to Next Wave

After completing the current wave:

1. Check if there are remaining waves
2. If yes: proceed to the next wave (return to 2a)
3. If no: proceed to Step 3 (Consolidation)

### Step 3: Consolidation

After all waves are complete, consolidate results from all converter agents into the tracking structures that Phase 6 consumes.

#### 3a: Read All Result Files

Read all result files from `.claude/sessions/__port_live__/results/`:

```
Glob: .claude/sessions/__port_live__/results/result-*.md
```

For each result file, parse:
- **Metadata**: component identification, fidelity score, band, status, target path
- **Converted Content**: the full converted file content
- **Fidelity Report**: scoring breakdown (direct, workaround, todo, omitted counts)
- **Decisions**: all conversion decisions with rationale
- **Gaps**: all identified gaps with severity

#### 3b: Build Tracking Structures

Assemble the data structures that Phase 6 expects:

- `CONVERTED_COMPONENTS` — list of converted component results, each containing: `{ component, converted_content, target_path, fidelity_score, band, status, fidelity_report, decisions[], gaps[] }`
- `CONVERSION_DECISIONS` — flat list of all decisions made across all components (concatenated from all result files), each containing: `{ component, feature, decision_type, original, converted, rationale, confidence, resolution_mode }`
- `CONVERSION_GAPS` — flat list of all gaps across all components (concatenated from all result files), each containing: `{ component, feature, reason, severity, workaround, user_acknowledged }`

#### 3c: Calculate Overall Weighted Fidelity Score

Compute the overall conversion fidelity as a weighted average across all components:

| Component Type | Weight | Rationale |
|----------------|--------|-----------|
| `skill` | 3 | Most complex — largest content, most features, primary deliverable |
| `agent` | 2 | Significant complexity — frontmatter, tools, body, model config |
| `hooks` | 1 | Configuration-oriented, typically fewer features |
| `reference` | 1 | Supporting content, complexity varies |
| `mcp` | 1 | Configuration mapping, typically straightforward |

```
overall_score = sum(component.fidelity_score * component.weight) / sum(component.weight)
```

Round to the nearest integer. Apply color band classification:
- Score >= 80: `band = "green"`, label = "High fidelity"
- Score 50-79: `band = "yellow"`, label = "Moderate fidelity"
- Score < 50: `band = "red"`, label = "Low fidelity"

### Step 4: Conversion Summary

Display the consolidated conversion results:

```
## Phase 5 Complete: Wave-Based Conversion

**Components converted:** {count}/{total}
**Waves executed:** {wave_count}
**Session directory:** .claude/sessions/__port_live__/

| Component | Type | Group | Fidelity | Band | Status | Gaps |
|-----------|------|-------|----------|------|--------|------|
| {name} | {type} | {group} | {score}% | {Green/Yellow/Red} | {full/partial/limited} | {gap_count} |

**Decisions made:** {total_decision_count}
- Direct mappings: {direct_count}
- Workarounds applied: {workaround_count}
- TODO placeholders: {todo_count}
- Features omitted: {omitted_count}
- Auto-resolved (cosmetic): {auto_count}
- Cached resolutions: {cached_count}

**Overall fidelity:** {overall_score}% ({Green/Yellow/Red} -- {High/Moderate/Low} fidelity)
```

Proceed to Phase 6.

---

## Phase 6: Output & Reporting

**Goal:** Write converted files, migration guide, and gap report to the output directory. This phase consumes `CONVERTED_COMPONENTS`, `CONVERSION_DECISIONS`, `CONVERSION_GAPS`, `STALENESS_STATUS`, and `CONVERSION_KNOWLEDGE` from earlier phases. All conversion results come from the session result files consolidated in Phase 5 Step 3. `MAPPINGS` for directory structure can be re-parsed from `.claude/sessions/__port_live__/conversion_knowledge.md` if needed.

### Note: Dry-Run Preview

Dry-run preview is handled in Phase 4.5 (before conversion). If the user chose "Done" or "Cancel" during the dry-run preview, the workflow will have exited before reaching this phase. If Phase 6 is reached, conversion has already been approved.

### Step 1: Determine Output Directory

Build a platform-specific directory suggestion from the adapter's directory structure. The suggestion should reflect where the target platform expects plugin files to live:

1. **Compute the default suggestion:**
   - If `MAPPINGS.directory_structure.plugin_root` is non-null, use it as the base (e.g., `.opencode/` for OpenCode)
   - Prefix with the project root to form a full path suggestion: `{project_root}/{plugin_root}`
   - If `plugin_root` is null or the adapter is unavailable, fall back to `ported/{TARGET_PLATFORM}/`

2. **Compute a neutral alternative:**
   - Always offer `ported/{TARGET_PLATFORM}/` as a project-relative staging directory that avoids overwriting any existing platform configuration

3. **Ask the user** via `AskUserQuestion`:

```yaml
AskUserQuestion:
  questions:
    - header: "Output Directory"
      question: "Where should the converted plugin files be written?"
      options:
        - label: "{computed_platform_suggestion}"
          description: "Target platform's expected plugin location ({MAPPINGS.directory_structure.plugin_root})"
        - label: "ported/{TARGET_PLATFORM}/"
          description: "Staging directory in the project root (safe -- does not overwrite platform config)"
        - label: "Custom path"
          description: "Specify a custom output directory"
      multiSelect: false
```

4. **If "Custom path"**, ask for the directory via a follow-up `AskUserQuestion`:

```yaml
AskUserQuestion:
  questions:
    - header: "Custom Output Directory"
      question: "Enter the path for the output directory (absolute or relative to project root):"
```

5. **Validate the chosen directory:**
   - Resolve relative paths against the project root to produce an absolute path
   - Store the resolved path as `OUTPUT_DIR`

### Step 2: Check for Existing Files

Before writing, check whether `OUTPUT_DIR` already exists and contains files:

1. Use `Glob` to check for any existing files at `{OUTPUT_DIR}/**/*`

2. **If files exist**, warn the user via `AskUserQuestion`:

```yaml
AskUserQuestion:
  questions:
    - header: "Existing Files Detected"
      question: "The output directory '{OUTPUT_DIR}' already contains {file_count} file(s). Writing converted files may overwrite existing content. How would you like to proceed?"
      options:
        - label: "Overwrite existing files"
          description: "Replace any conflicting files -- non-conflicting files are left untouched"
        - label: "Choose a different directory"
          description: "Go back and select a different output location"
        - label: "Cancel"
          description: "Exit the porter without writing files"
      multiSelect: false
```

   - **"Overwrite existing files"**: Continue to Step 3. Existing files that do not conflict with converted output are left untouched.
   - **"Choose a different directory"**: Return to Step 1.
   - **"Cancel"**: End the workflow gracefully. Display a summary of what was converted but not written.

3. **If no files exist** (directory is empty or does not exist), proceed directly to Step 3.

### Step 3: Check for Empty Conversion

If all entries in `CONVERTED_COMPONENTS` have `status = "unsupported"` or `CONVERTED_COMPONENTS` is empty (all components had no mappable features):

1. Inform the user:
   ```
   No components could be converted to {TARGET_PLATFORM} format. All selected components
   are unsupported on the target platform.
   ```

2. Write the gap report only:
   - Create `OUTPUT_DIR` if it does not exist (using `Bash: mkdir -p`)
   - Write `GAP-REPORT.md` to `OUTPUT_DIR/GAP-REPORT.md` (generated in Step 7)
   - Skip Steps 4 and 5 (no plugin files to write)

3. Store `WRITE_RESULTS` with `{ files_written: [], files_failed: [], files_renamed: [], gap_report_only: true }`

4. Skip to Step 6.

### Step 4: Create Target Directory Structure

Build the directory tree following the adapter's directory conventions. The structure is derived from `MAPPINGS.directory_structure`:

1. **Compute required directories** by scanning `CONVERTED_COMPONENTS` for unique target paths:

   ```
   REQUIRED_DIRS = set()
   For each entry in CONVERTED_COMPONENTS where status != "unsupported":
     Extract the directory portion of entry.target_path
     Add to REQUIRED_DIRS
   ```

   Typical directories based on adapter fields:
   - `{OUTPUT_DIR}/{skill_dir}` -- for converted skills (e.g., `{OUTPUT_DIR}/commands/`)
   - `{OUTPUT_DIR}/{agent_dir}` -- for converted agents (if `agent_dir` is non-null)
   - `{OUTPUT_DIR}/{hook_dir}` -- for converted hooks (if `hook_dir` is non-null)
   - `{OUTPUT_DIR}/{reference_dir}` -- for standalone reference files (if `reference_dir` is non-null)
   - `{OUTPUT_DIR}/{config_dir}` -- for configuration files like MCP configs (if `config_dir` is non-null)

   **Per-skill subdirectories:** If `MAPPINGS.directory_structure.skill_file_pattern` contains a subdirectory separator (e.g., `{name}/SKILL.md`), create a subdirectory per skill:
   - For each skill component, expand the pattern with the skill name
   - Add `{OUTPUT_DIR}/{skill_dir}/{skill-name}/` to `REQUIRED_DIRS`
   - Example: pattern `{name}/SKILL.md` with skill `deep-analysis` adds `.opencode/skills/deep-analysis/`

   **Instruction-array references:** If the adapter defines `reference_dir: null` and a Config File Format with `instruction_key`, create a references directory:
   - Add `{OUTPUT_DIR}/references/` to `REQUIRED_DIRS`

   For adapter fields that are `null` (e.g., OpenCode has `reference_dir: null`):
   - Components of that type either map to a different directory (e.g., references use instruction-array), are omitted entirely (gap report only), or use an alternative strategy
   - Do not create directories for null adapter fields unless an alternative strategy requires a directory

2. **Create directories** using `Bash: mkdir -p` for each entry in `REQUIRED_DIRS`:

   ```bash
   mkdir -p "{OUTPUT_DIR}/{dir1}" "{OUTPUT_DIR}/{dir2}" ...
   ```

   **Error handling**: If `mkdir -p` fails (permission denied, disk full, invalid path):
   - Capture the error message
   - Inform the user: "Failed to create directory '{dir}': {error_message}"
   - Use `AskUserQuestion` to offer recovery:

   ```yaml
   AskUserQuestion:
     questions:
       - header: "Directory Creation Failed"
         question: "Could not create the output directory structure: {error_message}. How would you like to proceed?"
         options:
           - label: "Choose a different directory"
             description: "Go back and select a different output location"
           - label: "Cancel"
             description: "Exit the porter without writing files"
         multiSelect: false
   ```

### Step 5: Write Converted Files

Initialize tracking for write results:

```
WRITE_RESULTS = {
  files_written: [],    // { component, target_path, size_bytes }
  files_failed: [],     // { component, target_path, error }
  files_renamed: [],    // { component, original_path, renamed_path, reason }
  gap_report_only: false
}
```

#### 5a: Detect File Path Conflicts

Before writing, scan `CONVERTED_COMPONENTS` for path conflicts -- multiple components that resolve to the same `target_path`:

1. Build a map of `target_path -> [components]`
2. For each path with more than one component:
   - The first component (by `CONVERSION_ORDER` position) keeps the original path
   - Subsequent components get a disambiguation suffix appended before the file extension:
     - Pattern: `{filename}-{group}` or `{filename}-{n}` where `{n}` is an incrementing counter
     - Example: `deep-analysis.md` and `deep-analysis.md` from different groups become `deep-analysis.md` and `deep-analysis-dev-tools.md`
   - Record each rename in `WRITE_RESULTS.files_renamed`
   - Add a note to `CONVERSION_DECISIONS`:
     ```
     { component, feature: "file_path", decision_type: "renamed", original: "{original_path}", converted: "{renamed_path}", rationale: "Path conflict with {conflicting_component}" }
     ```

#### 5b: Write Each Converted Component

Process each entry in `CONVERTED_COMPONENTS` where `status != "unsupported"`, in `CONVERSION_ORDER`:

1. **Determine the full output path:**
   - Combine `OUTPUT_DIR` with the component's `target_path` (which is already relative to the output directory)
   - Apply any renames from Step 5a

2. **Handle inlined reference content:**
   - If the converted content contains `<!-- INLINE: {path} -->` markers from Phase 5 composition flattening:
     - For each marker, look up the referenced file in `CONVERTED_COMPONENTS`
     - If found (the reference was also converted): replace the marker with the converted content
     - If not found (reference was not selected for conversion): replace with the raw source content read from disk
     - If the source file cannot be read: replace the marker with a TODO comment: `<!-- TODO: Could not inline {path} -- file not found or unreadable -->`

3. **Write the file** using the `Write` tool:
   - Write `converted_content` to the full output path

4. **Track the result:**
   - On success: append to `WRITE_RESULTS.files_written` with `{ component: component.name, target_path: full_path, size_bytes: content_length }`
   - On failure: append to `WRITE_RESULTS.files_failed` with `{ component: component.name, target_path: full_path, error: error_message }`

5. **Display progress** for each file:
   ```
   Writing [{n}/{total}]: {target_path} ({component.type}: {component.name})
   ```

#### 5c: Handle Write Failures

After attempting all file writes:

1. **If any files failed** (`WRITE_RESULTS.files_failed` is non-empty):

   Display a summary of failures:
   ```
   WARNING: {failed_count} file(s) could not be written:

   | Component | Target Path | Error |
   |-----------|-------------|-------|
   | {name} | {path} | {error} |
   ```

   These failures will be included in the migration guide and gap report.

2. **If ALL files failed** (no files were successfully written):

   Inform the user:
   ```
   ERROR: No files could be written to {OUTPUT_DIR}. This may indicate a permissions issue
   or an invalid output path.
   ```

   Use `AskUserQuestion` to offer recovery:

   ```yaml
   AskUserQuestion:
     questions:
       - header: "All File Writes Failed"
         question: "No converted files could be written to '{OUTPUT_DIR}'. Error: {most_common_error}. How would you like to proceed?"
         options:
           - label: "Choose a different directory"
             description: "Go back and select a different output location"
           - label: "Continue without writing files"
             description: "Skip file output -- proceed to migration guide and gap report"
           - label: "Cancel"
             description: "Exit the porter"
         multiSelect: false
   ```

   - **"Choose a different directory"**: Return to Step 1 and re-run Steps 2-5.
   - **"Continue without writing files"**: Proceed to Step 6. Migration guide will note that files were not written.
   - **"Cancel"**: End the workflow gracefully.

### Step 5.5: Generate Config File

If the adapter defines a Config File Format section (check `CONVERSION_KNOWLEDGE` for `config_file`, `config_format`, and related fields), generate the unified config file by aggregating fragments from all converted components.

1. **Check for Config File Format**: Look for `config_file` in `CONVERSION_KNOWLEDGE`. If not defined, skip this step entirely.

2. **Collect config fragments** from all result files in `{SESSION_DIR}/results/`:
   - Read each `result-*.md` file's "Config Fragments" section
   - Parse the JSON fragments from each result
   - Categorize fragments by type: agent model configs, MCP configs, reference instruction entries, permission entries

3. **Merge into single config object**: Deep-merge all fragments, with later entries winning on conflict:

   ```
   CONFIG = {}
   For each fragment in collected_fragments (ordered by CONVERSION_ORDER):
     Deep-merge fragment into CONFIG
   ```

   Merge rules:
   - **Agent configs**: Merge under `agent` key — each agent name is a separate sub-key, no conflicts expected
   - **MCP configs**: Merge under `mcp` key — each server name is a separate sub-key
   - **Instruction entries**: Concatenate all instruction paths into a single array, deduplicate
   - **Permission entries**: Merge under `permission` key — last write wins for each tool name

4. **Handle existing config file**: If the config file already exists at the target path (e.g., project already has an `opencode.json`):
   - Read the existing file
   - Deep-merge new config into existing (preserve existing values, add new entries)
   - Record in `CONVERSION_DECISIONS`: "Merged config into existing {config_file}"

5. **Write the config file** using the `Write` tool:
   - Path: `{config_file}` (relative to project root, as defined in the adapter)
   - Format: Use the adapter's `config_format` (json, jsonc, yaml, toml)
   - For JSONC: add brief comments above each section identifying its purpose

6. **Track in WRITE_RESULTS**:
   - On success: append `{ component: "config", target_path: config_file_path, size_bytes: content_length }` to `WRITE_RESULTS.files_written`
   - On failure: append to `WRITE_RESULTS.files_failed`

### Step 6: Generate Migration Guide

Generate the `MIGRATION-GUIDE.md` file in `OUTPUT_DIR`. This file documents the entire conversion for the user's reference, including fidelity scores, all decisions made during the incompatibility resolution process, and post-conversion manual steps.

**Data sources:** This step consumes `CONVERTED_COMPONENTS`, `CONVERSION_DECISIONS`, `CONVERSION_GAPS`, `STALENESS_STATUS`, `WRITE_RESULTS`, and `FIDELITY_REPORT` from earlier phases. All sources are optional -- the guide degrades gracefully when data is missing (see edge case handling below).

#### 6a: Pre-Generation Edge Case Checks

Before building the migration guide content, check for special conditions that affect the guide's structure:

1. **Clean conversion (all components Green band, zero gaps)**:

   If every entry in `CONVERTED_COMPONENTS` has `band == "green"` and `gaps` is empty, set `CLEAN_CONVERSION = true`. The header will include a celebratory note and several sections will be simplified.

2. **Very large conversion (20+ components)**:

   If `CONVERTED_COMPONENTS.length > 20`, set `LARGE_CONVERSION = true`. Per-component details will use a condensed table format instead of individual sub-sections to keep the guide readable.

3. **No incompatibility decisions**:

   If `CONVERSION_DECISIONS` is empty or undefined (e.g., the incompatibility resolver was skipped, or all features had direct mappings), set `NO_DECISIONS = true`. The Decisions Log section will be replaced with a brief note.

4. **Missing decision data (resolver skipped)**:

   If `CONVERSION_DECISIONS` is undefined or null (not just empty), treat it as an empty list. Do not error. Log internally: `"Note: CONVERSION_DECISIONS not available -- incompatibility resolver may have been skipped."` The migration guide will omit the Decisions Log section with an explanatory note.

5. **Missing staleness data**:

   If `STALENESS_STATUS` is undefined or null, skip the Platform Adapter Status section entirely and add a note: `"Platform adapter staleness check was not performed during this conversion."`

#### 6b: Build Migration Guide Content

Build the `MIGRATION-GUIDE.md` with the following sections in order:

**Section 1: Header**

```markdown
# Migration Guide: Agent Alchemy to {TARGET_PLATFORM}

**Generated:** {current_date}
**Source:** Agent Alchemy ({SELECTED_COMPONENTS.length} components from {SELECTED_GROUPS.length} plugin groups)
**Target platform:** {TARGET_PLATFORM}
**Overall fidelity:** {overall_score}% ({Band} -- {Label})

{If CLEAN_CONVERSION:}
> All components were converted with high fidelity (80%+ score) and no conversion
> gaps were identified. This is a clean conversion -- the converted plugin should
> work on {TARGET_PLATFORM} with minimal or no manual adjustments.

{If WRITE_RESULTS.gap_report_only:}
> **Note:** Files were not written to disk during this conversion. This guide
> documents what would have been converted. See the gap report for details.
```

**Section 2: Conversion Fidelity**

```markdown
---

## Conversion Fidelity

**Overall score:** {overall_score}% -- {Band} ({Label})

### Per-Component Scores

| Component | Type | Score | Band | Direct | Workaround | TODO | Omitted | Total Features |
|-----------|------|-------|------|--------|------------|------|---------|----------------|
{For each entry in CONVERTED_COMPONENTS:}
| {name} | {type} | {score}% | {Green/Yellow/Red} | {direct_count} | {workaround_count} | {todo_count} | {omitted_count} | {total_features} |

### Score Legend

| Band | Range | Meaning |
|------|-------|---------|
| Green | 80-100% | High fidelity -- minimal manual work needed |
| Yellow | 50-79% | Moderate fidelity -- some manual work needed |
| Red | 0-49% | Low fidelity -- significant manual work needed |
```

For each component with `band == "yellow"` or `band == "red"`, add a detailed breakdown sub-section:

```markdown
{For each component with band == "yellow" or band == "red":}
### {component_name} -- {score}% ({Band})

**Breakdown:**
- Direct mappings: {direct_count}/{total_features} features ({direct_count/total_features*100}%)
- Workarounds: {workaround_count} features (contributing {workaround_count * 0.7} weighted points)
- TODO placeholders: {todo_count} features (contributing {todo_count * 0.2} weighted points)
- Omitted: {omitted_count} features (no contribution)

{If notes exist:}
**Notes:** {notes list}
```

**Section 3: Platform Adapter Status**

{If `STALENESS_STATUS` is defined:}

```markdown
---

## Platform Adapter Status

| Field | Value |
|-------|-------|
| Staleness check performed | {STALENESS_STATUS.checked ? "yes" : "no"} |
| Adapter version | {STALENESS_STATUS.adapter_version or "unversioned"} |
| Adapter target platform version | {STALENESS_STATUS.adapter_platform_version or "N/A"} |
| Research-reported platform version | {STALENESS_STATUS.research_platform_version or "not reported"} |
| Status | {current / stale / unversioned / check failed} |
| User decision | {STALENESS_STATUS.user_decision or "N/A"} |
| Stale mappings found | {STALENESS_STATUS.stale_mappings.length} |
| New features discovered | {STALENESS_STATUS.new_features.length} |

{If STALENESS_STATUS.stale_mappings.length > 0:}
### Stale Mappings
| Mapping | Adapter Value | Research Value |
|---------|--------------|----------------|
| {name} | {old_value} | {new_value} |

{If STALENESS_STATUS.new_features.length > 0:}
### New Platform Features
{For each feature:}
- {feature_name}: {description}
```

{If `STALENESS_STATUS` is undefined or null:}

```markdown
---

## Platform Adapter Status

Platform adapter staleness check was not performed during this conversion.
```

**Section 4: Conversion Summary**

```markdown
---

## Conversion Summary

| Component | Type | Group | Fidelity | Band | Status | Gaps |
|-----------|------|-------|----------|------|--------|------|
{For each entry in CONVERTED_COMPONENTS:}
| {name} | {type} | {group} | {score}% | {Green/Yellow/Red} | {status} | {gap_count} |
```

**Section 5: Per-Component Details**

This section's format depends on the `LARGE_CONVERSION` flag.

{If `LARGE_CONVERSION` is false (20 or fewer components):}

Generate a full sub-section for each component:

```markdown
---

## Per-Component Details

{For each entry in CONVERTED_COMPONENTS:}
### {component.type}: {component.name} ({component.group})

**Fidelity:** {score}% ({band} -- {label})
**Source:** {component.path}
**Target:** {component.target_path}

#### Feature Mapping

| Feature | Category | Original | Converted | Notes |
|---------|----------|----------|-----------|-------|
{For each decision in entry.decisions:}
| {feature} | {decision_type} | {original} | {converted} | {rationale} |

{If entry.decisions is empty:}
All features were directly mapped with no modifications required.

{If entry.gaps is non-empty:}
#### Gaps

| Feature | Reason | Severity | Workaround |
|---------|--------|----------|------------|
{For each gap in entry.gaps:}
| {feature} | {reason} | {severity} | {workaround or "None"} |
```

{If `LARGE_CONVERSION` is true (more than 20 components):}

Use a condensed table format for all components, followed by detail sub-sections only for components with `band == "yellow"` or `band == "red"`:

```markdown
---

## Per-Component Details

> This conversion included {CONVERTED_COMPONENTS.length} components. Details are
> shown in table format for readability. Components with Yellow or Red fidelity
> bands have expanded detail sections below the table.

### All Components

| Component | Type | Group | Score | Source | Target | Decisions | Gaps |
|-----------|------|-------|-------|--------|--------|-----------|------|
{For each entry in CONVERTED_COMPONENTS:}
| {name} | {type} | {group} | {score}% {band} | {source_path} | {target_path} | {decisions.length} | {gaps.length} |

{For each component with band == "yellow" or band == "red":}
### {component.type}: {component.name} -- {score}% ({band})

**Source:** {component.path}
**Target:** {component.target_path}

| Feature | Category | Original | Converted | Notes |
|---------|----------|----------|-----------|-------|
{For each decision in entry.decisions:}
| {feature} | {decision_type} | {original} | {converted} | {rationale} |

{If entry.gaps is non-empty:}
| Gap Feature | Reason | Severity | Workaround |
|-------------|--------|----------|------------|
{For each gap in entry.gaps:}
| {feature} | {reason} | {severity} | {workaround or "None"} |
```

**Section 6: Decisions Log**

This section consolidates all user decisions from the incompatibility resolver into a single reference. It complements the per-component details by providing a cross-cutting view of every decision made during conversion.

{If `NO_DECISIONS` is true:}

```markdown
---

## Decisions Log

No incompatibility decisions were required during this conversion. All features
had direct mappings to {TARGET_PLATFORM} equivalents.
```

{If `NO_DECISIONS` is false:}

```markdown
---

## Decisions Log

The following decisions were made during incompatibility resolution. Each entry
records what was asked, what was chosen, and the impact on the converted output.

**Summary:** {total_decisions} decisions -- {direct_count} direct, {workaround_count} workarounds, {todo_count} TODOs, {omitted_count} omitted

### By Resolution Mode

{Count decisions by resolution_mode and display:}
- **Individual**: {individual_count} (resolved one at a time via user prompt)
- **Batch**: {batch_count} (resolved as a group of similar incompatibilities)
- **Cached**: {cached_count} (reused a previous decision for the same feature)
- **Auto**: {auto_count} (auto-resolved cosmetic gaps with high-confidence workarounds)

### Decision Details

| # | Component | Feature | Decision | Resolution Mode | Confidence | Rationale |
|---|-----------|---------|----------|-----------------|------------|-----------|
{For each decision in CONVERSION_DECISIONS, numbered sequentially:}
| {n} | {component} | {feature} | {decision_type} | {resolution_mode or "N/A"} | {confidence or "N/A"} | {rationale} |
```

If `CONVERSION_DECISIONS` contains entries but some entries are missing fields (e.g., `resolution_mode` or `confidence` are undefined), display "N/A" for those fields rather than erroring.

**Section 7: Post-Conversion Steps**

This section lists manual actions the user should take after conversion. The steps are derived from three sources:

1. **From `CONVERSION_GAPS`**: Any gap with `severity: "critical"` or `severity: "functional"` implies a manual step
2. **From `CONVERSION_DECISIONS`**: Decisions with `decision_type: "todo"` indicate features needing manual implementation; decisions with `decision_type: "workaround"` where `confidence` is `"low"` or `"uncertain"` need verification
3. **From `STALENESS_STATUS`**: If the adapter is stale, recommend verifying converted output against current platform docs
4. **From platform knowledge**: General post-conversion steps based on the target platform (e.g., install dependencies, configure runtime, run platform-specific validation)

Build the steps using this category-by-decision_type matrix:

| Source | Condition | Manual Step |
|--------|-----------|-------------|
| CONVERSION_GAPS | severity == "critical" | "Implement {feature} manually -- critical to component function" |
| CONVERSION_GAPS | severity == "functional" | "Review {feature} gap in {component} -- may need manual implementation" |
| CONVERSION_DECISIONS | decision_type == "todo" | "Complete TODO placeholder for {feature} in {target_path}" |
| CONVERSION_DECISIONS | decision_type == "workaround" and confidence in ["low", "uncertain"] | "Verify workaround for {feature} in {component} -- confidence: {confidence}" |
| STALENESS_STATUS | status == "stale" | "Adapter may be outdated -- verify converted output against current {TARGET_PLATFORM} documentation" |
| WRITE_RESULTS | files_failed is non-empty | "Retry writing failed files or create them manually: {file_list}" |
| General | always | "Test the converted plugin on {TARGET_PLATFORM}" |
| General | always | "Review all TODO comments in converted files (search for 'TODO [{TARGET_PLATFORM}]')" |
| General | mcp components converted | "Configure MCP servers for {TARGET_PLATFORM} environment" |
| General | hooks were omitted or converted to workarounds | "Verify hook behavior replacements work as expected" |

```markdown
---

## Post-Conversion Steps

The following manual steps are recommended after conversion:

### Required Actions

{For each step derived from critical gaps and TODO decisions:}
{n}. **{component}**: {action_description}
   - Source: `{source_path}`
   - Target: `{target_path}`

{If no required actions:}
No required actions -- all critical features were successfully converted.

### Recommended Verifications

{For each step derived from low-confidence workarounds, functional gaps, and staleness:}
{n}. {verification_description}

### Platform Setup

{For each platform-specific setup step:}
{n}. {setup_instruction}

{General steps always included:}
- Test the converted plugin on {TARGET_PLATFORM} to verify runtime behavior
- Review all TODO comments in converted files (search for `TODO [{TARGET_PLATFORM}]`)
- Consult `GAP-REPORT.md` for a detailed breakdown of all conversion gaps

{If MCP components were converted:}
- Configure MCP servers for your {TARGET_PLATFORM} environment (server URLs, authentication, transport settings)

{If hooks were converted with workarounds or omitted:}
- Verify that hook behavior replacements (or their absence) do not affect your workflow
```

**Section 8: File Inventory**

```markdown
{If WRITE_RESULTS.files_renamed is non-empty:}
---

## File Path Renames

The following files were renamed to avoid path conflicts:

| Component | Original Path | Renamed Path | Reason |
|-----------|--------------|--------------|--------|
{For each rename in WRITE_RESULTS.files_renamed:}
| {component} | {original_path} | {renamed_path} | {reason} |

{If WRITE_RESULTS.files_failed is non-empty:}
---

## Failed File Writes

The following files could not be written:

| Component | Target Path | Error |
|-----------|-------------|-------|
{For each failure in WRITE_RESULTS.files_failed:}
| {component} | {target_path} | {error} |

---

## Output Files

{For each entry in WRITE_RESULTS.files_written:}
- `{target_path}` -- {component.type}: {component.name}
{Always included:}
- `MIGRATION-GUIDE.md` -- this file
- `GAP-REPORT.md` -- conversion gap analysis
```

#### 6c: Append PORT-METADATA Block

After assembling all migration guide sections, append a machine-readable metadata block at the very end of the migration guide content. This block enables the `update-ported-plugin` skill to detect what was ported and when.

Get the current git commit hash via Bash: `git rev-parse HEAD`

Append the following HTML comment block to the end of the migration guide content:

```markdown

<!-- PORT-METADATA
source_commit: {current_HEAD_hash}
port_date: {current_date}
adapter_version: {ADAPTER.adapter_version or "none"}
target_platform: {TARGET_PLATFORM}
target_platform_version: {ADAPTER.target_platform_version or RESEARCH_FINDINGS.platform_version or "unknown"}
components:
{For each entry in CONVERTED_COMPONENTS:}
  - source: {component.source_path}
    target: {component.target_path}
    fidelity: {component.fidelity_score}
PORT-METADATA -->
```

This block **must** be the last content in the file. It is parsed by `update-ported-plugin` to detect source drift and determine which components need re-conversion.

#### 6d: Write Migration Guide

Write the assembled migration guide to `{OUTPUT_DIR}/MIGRATION-GUIDE.md` using the `Write` tool.

If the write fails, log the error and continue to Step 7. The migration guide content should still be displayed in the Phase 7 summary output so the user can access it even if the file write failed.

### Step 7: Generate Gap Report

Generate `GAP-REPORT.md` from `CONVERSION_GAPS`, `CONVERSION_DECISIONS`, and `CONVERSION_KNOWLEDGE`. This report documents every feature that could not be fully converted, providing explanations and workarounds.

#### 3a: Collect and Classify Gap Data

Build the gap report data from the tracking structures:

1. **Gather all gaps** from `CONVERSION_GAPS` (flat list accumulated during Phase 5)
2. **Enrich each gap** with decision context from `CONVERSION_DECISIONS`:
   - Match gaps to decisions by `component` + `feature` keys
   - Pull `decision_type`, `rationale`, `confidence`, and `resolution_mode` from the matching decision
3. **Classify gaps by severity**: Group into `critical`, `functional`, and `cosmetic` buckets
4. **Group similar gaps**: Gaps with identical `feature` names across different components are grouped together for readability (e.g., if `SendMessage` is a gap in 3 agents, present it once with all affected components listed)

#### 3b: Handle Edge Cases

Before generating the report, check for special conditions:

**No gaps (100% conversion):**

If `CONVERSION_GAPS` is empty, generate a brief report:

```markdown
# Gap Report

**Source:** Agent Alchemy ({component_count} components)
**Target:** {TARGET_PLATFORM}
**Date:** {current_date}

## Summary

No conversion gaps were identified. All selected components were fully converted
to {TARGET_PLATFORM} format with direct mappings or applied workarounds.

Refer to `MIGRATION-GUIDE.md` for details on any workarounds that were applied
during conversion.
```

Write this to `{output_directory}/GAP-REPORT.md` and skip the remaining sub-steps.

**All critical gaps:**

If every gap has `severity: "critical"`, add a prominent warning to the summary:

```markdown
> **WARNING**: All identified gaps are critical. The converted plugin may not
> function correctly on {TARGET_PLATFORM} without significant manual work.
> Review each gap below and address the critical items before attempting to
> use the converted plugin.
```

**Many similar gaps (3+ gaps with the same `feature` name):**

Group them into a single entry with a sub-list of affected components rather than repeating the full entry for each. Example:

```markdown
### SendMessage (Critical) — 4 components affected

- **Components:** code-explorer, code-synthesizer, code-architect (all core-tools), code-reviewer (dev-tools)
- **Why:** No inter-agent messaging equivalent on {TARGET_PLATFORM}
- **Workaround:** Remove inter-agent references; restructure as independent workflows
- **Manual steps:** Refactor each agent to operate independently without message passing
```

#### 3c: Generate Report Content

Build the `GAP-REPORT.md` with the following sections in order:

**Section 1: Header and Summary**

```markdown
# Gap Report

**Source:** Agent Alchemy ({component_count} components from {group_names})
**Target:** {TARGET_PLATFORM}
**Date:** {current_date}
**Overall fidelity:** {weighted_average}%

## Summary

| Severity | Count | Description |
|----------|-------|-------------|
| Critical | {critical_count} | Features essential to plugin function — converted plugin may not work without these |
| Functional | {functional_count} | Features that enable specific capabilities — partial functionality loss |
| Cosmetic | {cosmetic_count} | Metadata or documentation features — no behavioral impact |
| **Total** | **{total_count}** | |

{If all critical: insert the all-critical warning from 3b}

### Impact Assessment

{Generate a 2-3 sentence summary based on the gap distribution:}
- If critical_count == 0: "The conversion is high-fidelity. All gaps are functional or cosmetic and the converted plugin should work on {TARGET_PLATFORM} with minor adjustments."
- If critical_count > 0 and critical_count < total_count / 2: "The conversion has {critical_count} critical gap(s) that require manual attention before the converted plugin will function on {TARGET_PLATFORM}. Functional and cosmetic gaps can be addressed incrementally."
- If critical_count >= total_count / 2: "The conversion has significant gaps. Over half of the identified issues are critical, indicating substantial differences between Claude Code and {TARGET_PLATFORM} capabilities. Manual porting effort will be required for core functionality."

### Resolution Breakdown

| Resolution | Count |
|------------|-------|
| Workaround applied | {workaround_count} |
| Feature omitted | {omitted_count} |
| TODO comment added | {todo_count} |
| Auto-resolved | {auto_count} |
```

**Section 2: Gap Details**

Generate one entry per gap (or per grouped gap if similar gaps were merged in step 3b). Sort by severity (critical first, then functional, then cosmetic), then alphabetically by feature name within each severity level.

For each gap entry:

```markdown
## Gaps by Severity

### Critical

#### {feature_name}

| Field | Value |
|-------|-------|
| Component(s) | {component name(s)} |
| Category | {incompatibility category: unmapped tool / unmapped field / unsupported composition / unsupported hook / general gap} |
| Resolution | {decision_type: workaround / omitted / todo} |
| Confidence | {confidence level, if workaround applied} |

**Why it could not be converted:**
{reason — from the gap's `reason` field}

**Suggested workaround or alternative:**
{workaround — from the gap's `workaround` field. If no workaround: "No automated workaround available. Manual implementation required."}

**Manual steps to address:**
{Derive actionable steps from the gap context:}
1. {Step based on decision_type and feature type}
2. {Additional steps as needed}

---

### Functional

{Same entry format as Critical, repeated for each functional gap}

### Cosmetic

{Same entry format as Critical, repeated for each cosmetic gap}
```

**Deriving manual steps:** Use the following patterns based on the gap's category and decision type:

| Category | Decision | Manual Steps |
|----------|----------|-------------|
| Unmapped tool (workaround) | workaround | 1. Review the workaround text in the converted file. 2. Test that the alternative tool behaves as expected on {TARGET_PLATFORM}. |
| Unmapped tool (omitted) | omitted | 1. Identify where the tool was used in the original plugin. 2. Implement equivalent functionality using {TARGET_PLATFORM} native tools. 3. Test the component end-to-end. |
| Unmapped tool (todo) | todo | 1. Search for `TODO [{TARGET_PLATFORM}]` comments in the converted files. 2. Replace each TODO with a working implementation. 3. Test the component. |
| Unmapped field | any | 1. Check if the field's behavior can be configured through {TARGET_PLATFORM} settings. 2. If not, document the behavioral difference for users. |
| Unsupported composition | any | 1. Review the inlined or flattened content in the converted file. 2. Verify the content is complete and correctly placed. 3. If cross-plugin references were involved, ensure all referenced content is available. |
| Unsupported hook | any | 1. Identify the hook's purpose (security, automation, logging). 2. Check {TARGET_PLATFORM} documentation for equivalent lifecycle features. 3. Implement manually or document as a platform limitation. |
| General gap | any | 1. Review the feature's purpose in the original plugin. 2. Check {TARGET_PLATFORM} documentation for any partial equivalent. 3. Implement manually or restructure the workflow to work without this feature. |

**Section 3: Platform Comparison**

Generate a high-level comparison of Claude Code capabilities vs. the target platform, derived from `CONVERSION_KNOWLEDGE` (the merged adapter + research data).

```markdown
## Platform Comparison: Claude Code vs. {TARGET_PLATFORM}

A high-level overview of feature support differences between Claude Code and {TARGET_PLATFORM}.

| Capability | Claude Code | {TARGET_PLATFORM} | Status |
|------------|-------------|---------------------|--------|
| Skills / Custom Commands | YAML frontmatter + markdown body | {target equivalent from CONVERSION_KNOWLEDGE} | {Supported / Partial / Unsupported} |
| Agents | Agent markdown files with model/tools/skills | {target equivalent} | {Supported / Partial / Unsupported} |
| Hooks / Lifecycle Events | hooks.json with PreToolUse, PostToolUse, Stop, etc. | {target equivalent} | {Supported / Partial / Unsupported} |
| Skill Composition | `Read` directive loading skill content | {target equivalent} | {Supported / Partial / Unsupported} |
| Cross-Plugin References | `${CLAUDE_PLUGIN_ROOT}/../{group}/` paths | {target equivalent} | {Supported / Partial / Unsupported} |
| Model Tiering | Per-agent model selection (opus/sonnet/haiku) | {target equivalent} | {Supported / Partial / Unsupported} |
| MCP Server Config | `.mcp.json` with stdio/sse/http transports | {target equivalent} | {Supported / Partial / Unsupported} |
| Interactive Tools | AskUserQuestion with options/multiSelect | {target equivalent} | {Supported / Partial / Unsupported} |
| Task Management | TaskCreate, TaskUpdate, TaskList, TaskGet | {target equivalent} | {Supported / Partial / Unsupported} |
| Team / Multi-Agent | TeamCreate, SendMessage | {target equivalent} | {Supported / Partial / Unsupported} |
| Reference Files | `references/` subdirectories loaded by skills | {target equivalent} | {Supported / Partial / Unsupported} |

**Status legend:**
- **Supported**: Direct equivalent exists on {TARGET_PLATFORM}
- **Partial**: Approximate equivalent exists but with reduced functionality
- **Unsupported**: No equivalent on {TARGET_PLATFORM}
```

Populate each row by checking `CONVERSION_KNOWLEDGE`:
- If the mapping has a non-null target: **Supported**
- If the mapping has a partial target or workaround with high/medium confidence: **Partial**
- If the mapping is null with no workaround: **Unsupported**
- For the "{target equivalent}" column, use the mapped target name/description from the adapter, or "N/A" if unsupported

#### 3d: Handle Missing Gap Data

If `CONVERSION_GAPS` is not available or is malformed (e.g., conversion was interrupted before Phase 5 completed):

1. Check if `CONVERSION_DECISIONS` has any entries -- if so, infer gaps from decisions with `decision_type: "omitted"` or `decision_type: "todo"`
2. If neither structure is available, generate a minimal report:
   ```markdown
   # Gap Report

   **Source:** Agent Alchemy
   **Target:** {TARGET_PLATFORM}
   **Date:** {current_date}

   ## Summary

   Gap data is unavailable. The conversion process may have been interrupted
   before gap tracking was complete. Refer to the converted files for any
   `TODO` comments indicating features that require manual attention.
   ```
3. Write this minimal report and continue to Phase 7 without error

#### 3e: Write Gap Report

Write the assembled report to `{output_directory}/GAP-REPORT.md` using the `Write` tool.

### Step 8: Output Summary

Display a summary of all files written in this phase:

```
## Phase 6 Complete: Output & Reporting

**Output directory:** {OUTPUT_DIR}

### Files Written

| File | Size | Status |
|------|------|--------|
{For each entry in WRITE_RESULTS.files_written:}
| {target_path} | {size_bytes} bytes | Written |
{For each entry in WRITE_RESULTS.files_failed:}
| {target_path} | -- | FAILED: {error} |
| {OUTPUT_DIR}/MIGRATION-GUIDE.md | {size} | Written |
| {OUTPUT_DIR}/GAP-REPORT.md | {size} | Written |

**Total files written:** {WRITE_RESULTS.files_written.length + 2 (guide + report)}
**Failed writes:** {WRITE_RESULTS.files_failed.length}
{If WRITE_RESULTS.files_renamed.length > 0:}
**Files renamed (path conflicts):** {WRITE_RESULTS.files_renamed.length}
```

Proceed to Phase 7.

---

## Phase 7: Summary

**Goal:** Present the conversion results and suggest next steps.

### Step 1: Conversion Summary

Present a summary of the conversion:

```
## Conversion Complete

**Source:** Agent Alchemy ({count} components)
**Target:** {TARGET_PLATFORM}
**Output:** {output_directory}

### Results

| Component | Type | Fidelity | Band | Status |
|-----------|------|----------|------|--------|
| {name} | {type} | {score}% | {Green/Yellow/Red} | {full/partial/limited} |

**Overall fidelity:** {weighted_average}% ({Green/Yellow/Red} -- {High/Moderate/Low} fidelity)
**Components converted:** {count}/{total}
**Gaps identified:** {count}

### Files Written
- {output_directory}/MIGRATION-GUIDE.md
- {output_directory}/GAP-REPORT.md
- {list of converted plugin files}
```

### Step 2: Next Steps

Present recommended next steps:

```
### Next Steps

1. Review the MIGRATION-GUIDE.md for conversion details and decisions
2. Review the GAP-REPORT.md for features that could not be converted
3. Test the converted plugins on {TARGET_PLATFORM}
4. Address any TODO comments left in converted files
5. Update the adapter file if research revealed new platform features
```

### Step 3: Session Cleanup

Archive the live session directory to preserve the conversion record:

1. Generate a timestamped archive name: `port-{TARGET_PLATFORM}-{YYYYMMDD}-{HHMMSS}`
2. Move the session: `mv .claude/sessions/__port_live__ .claude/sessions/{archive_name}`
3. Log: "Session archived to .claude/sessions/{archive_name}/"

**On error or cancellation**: If the workflow is cancelled or fails at any point after the session directory was created (Phase 5 Step 1), still archive the session directory so partial results are preserved for debugging. Use the same archive procedure but append `-interrupted` to the name: `port-{TARGET_PLATFORM}-{YYYYMMDD}-{HHMMSS}-interrupted`.

---

## Error Handling

If any phase fails:
1. Explain what went wrong
2. Use `AskUserQuestion` to ask how to proceed:
   ```yaml
   AskUserQuestion:
     questions:
       - header: "Error Recovery"
         question: "{Description of what failed}. How would you like to proceed?"
         options:
           - label: "Retry this phase"
             description: "Attempt the failed phase again"
           - label: "Skip to next phase"
             description: "Continue without this phase's output"
           - label: "Cancel"
             description: "Exit the porter"
         multiSelect: false
   ```

---

## Reference Files

- `${CLAUDE_PLUGIN_ROOT}/references/adapter-format.md` — Adapter file format specification (9 mapping sections)
- `${CLAUDE_PLUGIN_ROOT}/references/agent-converter.md` — Agent conversion logic (frontmatter mapping, body transformation, gap handling, fidelity scoring)
- `${CLAUDE_PLUGIN_ROOT}/references/hook-converter.md` — Hook conversion logic (event mapping, behavioral classification, workaround strategies)
- `${CLAUDE_PLUGIN_ROOT}/references/reference-converter.md` — Reference file conversion logic (discovery, path transformation, flattening)
- `${CLAUDE_PLUGIN_ROOT}/references/mcp-converter.md` — MCP config conversion logic (server mapping, transport types, tool reference renaming, platform support detection)
- `${CLAUDE_PLUGIN_ROOT}/references/incompatibility-resolver.md` — Incompatibility detection, interactive resolution, batch handling, decision tracking (includes agent vs. orchestrator responsibility split)
- `${CLAUDE_PLUGIN_ROOT}/references/adapters/` — Directory for per-platform adapter files (one markdown file per target platform)
- `${CLAUDE_PLUGIN_ROOT}/skills/port-plugin/references/session-format.md` — Session file format contract between orchestrator and port-converter agents
