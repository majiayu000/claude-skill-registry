---
name: dependency-checker
description: Analyzes the Agent Alchemy plugin ecosystem to detect dependency issues across all plugin groups
user-invocable: true
disable-model-invocation: true
argument-hint: "[--plugin <group>] [--verbose] [--report-file <path>]"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
---

# Dependency Checker

Analyze the Agent Alchemy plugin ecosystem to detect dependency issues, broken paths, orphaned components, and documentation drift. Produces a health report with severity-ranked findings.

**CRITICAL: Complete ALL 5 phases.** The workflow is not complete until Phase 5: Report is finished. After completing each phase, immediately proceed to the next phase without waiting for user prompts.

## Critical Rules

### AskUserQuestion is MANDATORY

**IMPORTANT**: You MUST use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Report presentation -> AskUserQuestion
- Action selection -> AskUserQuestion
- View mode selection -> AskUserQuestion

Text output should only be used for:
- Displaying progress updates between phases
- Presenting intermediate analysis summaries (inventory counts, graph stats)
- Phase transition markers

If you need the user to make a choice or provide input, use AskUserQuestion.

**NEVER do this** (asking via text output):
```
Would you like to view findings by severity or by plugin group?
1. By severity
2. By plugin group
```

**ALWAYS do this** (using AskUserQuestion tool):
```yaml
AskUserQuestion:
  questions:
    - header: "View Mode"
      question: "How would you like to view the findings?"
      options:
        - label: "By severity"
          description: "Group findings from critical to low"
        - label: "By plugin group"
          description: "Filter findings to a specific plugin group"
      multiSelect: false
```

### Plan Mode Behavior

**CRITICAL**: This skill performs an interactive analysis workflow, NOT an implementation plan. When invoked during Claude Code's plan mode:

- **DO NOT** create an implementation plan for how to build the analysis
- **DO NOT** defer analysis to an "execution phase"
- **DO** proceed with the full analysis workflow immediately
- **DO** write report files as normal if `--report-file` is specified

## Phase Overview

Execute these phases in order, completing ALL of them:

1. **Load & Discover** — Parse arguments, load settings, build component inventory
2. **Build Dependency Graph** — Parse every component file to extract dependency edges
3. **Analyze** — Run 7 detection passes over the dependency graph
4. **Cross-Reference Documentation** — Compare graph against CLAUDE.md/README docs for drift
5. **Report** — Present findings interactively; optionally export

---

## Phase 1: Load & Discover

**Goal:** Parse arguments, load settings, build a complete component inventory of the plugin ecosystem.

### Step 1: Parse Arguments

Parse `$ARGUMENTS` for:
- `--plugin <group>` — Filter to one plugin group by short directory name (e.g., `core-tools`). Default: analyze all groups.
- `--verbose` — Include healthy/passing entries in the report, not just issues. Default: `false`.
- `--report-file <path>` — Export the full report as a markdown file to the given path. Default: none (interactive only).

Set variables:
- `FILTER_GROUP` from `--plugin` value (default: `null` = all groups)
- `VERBOSE_MODE` from `--verbose` flag (default: `false`)
- `REPORT_FILE` from `--report-file` value (default: `null`)

### Step 2: Load Settings

Read settings from `.claude/agent-alchemy.local.md` if it exists. Look for the `plugin-tools.dependency-checker` section in the YAML frontmatter.

| Setting | Default | Description |
|---------|---------|-------------|
| `severity-threshold` | `low` | Minimum severity to show: `critical`, `high`, `medium`, `low` |
| `check-docs-drift` | `true` | Whether to run Phase 4 documentation cross-referencing |
| `line-count-tolerance` | `10` | Percentage tolerance for line count drift in CLAUDE.md tables |

If the settings file doesn't exist or the section is missing, use defaults.

### Step 3: Load Marketplace Registry

Read the marketplace registry:
```
Read: ${CLAUDE_PLUGIN_ROOT}/../../.claude-plugin/marketplace.json
```

Build a registry map: `{ plugin_name -> { version, source_dir, description } }` for each entry in the `plugins` array. The `source_dir` is derived from the `source` field (strip leading `./`).

### Step 4: Discover Components

For each plugin group directory under `claude/` (or only `FILTER_GROUP` if set), enumerate all components using Glob:

**Skills:**
```
Glob: claude/{group}/skills/*/SKILL.md
```
For each found skill, read its YAML frontmatter to extract:
- `name`, `description`, `user-invocable`, `disable-model-invocation`
- `allowed-tools` list
- `skills` list (if present — for agent-like skill composition)

**Agents:**
```
Glob: claude/{group}/agents/*.md
```
For each found agent, read its YAML frontmatter to extract:
- `name`, `description`, `model`
- `tools` list
- `skills` list (these are skill bindings that must resolve to real skills)

**Shared references (plugin-level):**
```
Glob: claude/{group}/references/**/*.md
```

**Skill-local references:**
```
Glob: claude/{group}/skills/*/references/**/*.md
```

**Hooks:**
```
Glob: claude/{group}/hooks/hooks.json
```
If found, read and parse the JSON to extract hook entries.

**Hook scripts:**
```
Glob: claude/{group}/hooks/*.sh
```

### Step 5: Display Inventory Summary

Display a text summary of what was discovered:

```
[Phase 1/5] Plugin Ecosystem Inventory

| Group | Skills | Agents | Shared Refs | Skill Refs | Hooks | Scripts |
|-------|--------|--------|-------------|------------|-------|---------|
| core-tools | N | N | N | N | N | N |
| dev-tools | N | N | N | N | N | N |
| ... | ... | ... | ... | ... | ... | ... |
| **Total** | **N** | **N** | **N** | **N** | **N** | **N** |
```

---

## Phase 2: Build Dependency Graph

**Goal:** Parse every component file to extract all dependency edges, building a directed graph of the ecosystem.

### Step 1: Define Edge Types

The graph has the following edge types:

| Edge Type | Source | Target | Pattern |
|-----------|--------|--------|---------|
| `skill-loads-skill` | Skill | Skill (same plugin) | `${CLAUDE_PLUGIN_ROOT}/skills/{name}/SKILL.md` (without `/../`) |
| `skill-loads-skill-cross` | Skill | Skill (other plugin) | `${CLAUDE_PLUGIN_ROOT}/../{group}/skills/{name}/SKILL.md` |
| `skill-loads-shared-ref` | Skill | Shared reference | `${CLAUDE_PLUGIN_ROOT}/references/{path}` |
| `skill-loads-local-ref` | Skill | Skill-local reference | `${CLAUDE_PLUGIN_ROOT}/skills/{name}/references/{path}` |
| `skill-loads-cross-ref` | Skill | Cross-plugin reference | `${CLAUDE_PLUGIN_ROOT}/../{group}/(skills/{name}/)?references/{path}` |
| `skill-spawns-agent` | Skill | Agent | `subagent_type` references in skill body |
| `skill-reads-registry` | Skill | Registry | `${CLAUDE_PLUGIN_ROOT}/../../.claude-plugin/` patterns |
| `agent-binds-skill` | Agent | Skill | `skills:` list in YAML frontmatter |
| `hook-runs-script` | Hook config | Hook script | `${CLAUDE_PLUGIN_ROOT}/hooks/{script}` in command strings |

### Step 2: Extract Edges from Skills

For each SKILL.md file discovered in Phase 1, scan the **full file content** (not just frontmatter) using these regex patterns:

**Cross-plugin skill loads:**
```regex
\$\{CLAUDE_PLUGIN_ROOT\}/\.\./([^/]+)/skills/([^/]+)/SKILL\.md
```
Creates edge: `skill-loads-skill-cross` from current skill to `{group}:{skill_name}`

**Same-plugin skill loads:**
```regex
\$\{CLAUDE_PLUGIN_ROOT\}/skills/([^/]+)/SKILL\.md
```
Match only if the path does NOT contain `/../` before it. Creates edge: `skill-loads-skill` from current skill to `{skill_name}` within the same plugin.

**Shared reference loads (same plugin):**
```regex
\$\{CLAUDE_PLUGIN_ROOT\}/references/([^\s"'`)+]+\.md)
```
Creates edge: `skill-loads-shared-ref`

**Skill-local reference loads:**
```regex
\$\{CLAUDE_PLUGIN_ROOT\}/skills/([^/]+)/references/([^\s"'`)+]+\.md)
```
Creates edge: `skill-loads-local-ref`

**Cross-plugin reference loads:**
```regex
\$\{CLAUDE_PLUGIN_ROOT\}/\.\./([^/]+)/(skills/[^/]+/)?references/([^\s"'`)+]+\.md)
```
Creates edge: `skill-loads-cross-ref`

**Agent spawning:**
```regex
subagent_type[:\s]*["']?([^"'\s,}]+)
```
Creates edge: `skill-spawns-agent` from current skill to the resolved agent name.

**Registry reads:**
```regex
\$\{CLAUDE_PLUGIN_ROOT\}/\.\./\.\./\.claude-plugin/
```
Creates edge: `skill-reads-registry`

### Step 3: Extract Edges from Agents

For each agent `.md` file, parse its YAML frontmatter and extract the `skills:` list.

Each entry in the `skills:` list creates an `agent-binds-skill` edge. The skill name must be resolved to a skill within the **same plugin group** as the agent (since agent frontmatter skill bindings are group-local).

### Step 4: Extract Edges from Hooks

For each `hooks.json` file, parse the JSON and scan all `command` strings for script references:

```regex
\$\{CLAUDE_PLUGIN_ROOT\}/hooks/([^\s"']+)
```
Creates edge: `hook-runs-script` from the hook config to the referenced script file.

### Step 5: Display Graph Summary

```
[Phase 2/5] Dependency Graph Built

Nodes: N total (N skills, N agents, N shared refs, N skill refs, N hooks, N scripts)
Edges: N total
  - skill-loads-skill: N (same-plugin: N, cross-plugin: N)
  - skill-loads-ref: N (shared: N, local: N, cross-plugin: N)
  - skill-spawns-agent: N
  - skill-reads-registry: N
  - agent-binds-skill: N
  - hook-runs-script: N
```

---

## Phase 3: Analyze (7 Detection Passes)

**Goal:** Run 7 detection passes over the dependency graph to find issues. Each pass produces findings with a severity level.

Filter findings by `severity-threshold` setting — only retain findings at or above the configured threshold.

### Pass 1: Circular Dependencies (Critical)

Run DFS cycle detection on the `skill-loads-skill` and `skill-loads-skill-cross` edges (the skill-to-skill subgraph).

Algorithm:
1. For each skill node, perform DFS tracking the visit stack
2. If a node is encountered that is already in the current visit stack, a cycle is detected
3. Record the full cycle path: `skill_A -> skill_B -> ... -> skill_A`

Each cycle found is a **Critical** severity finding.

### Pass 2: Missing Dependencies (High)

For every edge in the graph, verify that the target node exists on disk:

- `skill-loads-skill` / `skill-loads-skill-cross`: Check the target SKILL.md file exists
- `skill-loads-shared-ref` / `skill-loads-local-ref` / `skill-loads-cross-ref`: Check the target .md file exists
- `skill-spawns-agent`: Resolve the agent name to a file. Agent names may be:
  - Bare names (e.g., `"code-explorer"`) — look in the same plugin group's `agents/` directory
  - Qualified names (e.g., `"agent-alchemy-core-tools:code-explorer"`) — map marketplace name to source dir, then look in that group's `agents/`
- `agent-binds-skill`: Check the skill exists in the same plugin group's `skills/` directory
- `hook-runs-script`: Check the script file exists

Each missing target is a **High** severity finding. Include the source file, expected target path, and edge type.

### Pass 3: Broken Cross-Plugin Paths (Medium)

Scan all SKILL.md and agent `.md` files for path anti-patterns:

**Anti-pattern 1 — Marketplace name in path:**
```regex
agent-alchemy-[a-z-]+/
```
Paths should use short directory names (e.g., `core-tools`), not marketplace names (e.g., `agent-alchemy-core-tools`).

**Anti-pattern 2 — Hardcoded absolute paths:**
```regex
/Users/|/home/|/tmp/.*claude/
```
Paths should use `${CLAUDE_PLUGIN_ROOT}` variable, not absolute paths.

**Anti-pattern 3 — Incorrect nesting depth:**
```regex
\$\{CLAUDE_PLUGIN_ROOT\}/\.\./\.\./\.\./
```
Triple `../` or deeper should not appear (maximum is `../../` for registry access).

Each finding is **Medium** severity.

### Pass 4: Orphaned Components (Low)

Find components with zero inbound edges (nothing references them):

- **Skills**: Only flag non-user-invocable skills with zero inbound edges. User-invocable skills are entry points and are expected to have no inbound edges.
- **Agents**: Flag agents with zero `skill-spawns-agent` inbound edges (no skill spawns them) AND zero `agent-binds-skill` outbound edges isn't sufficient — check that nothing spawns them.
- **Shared references**: Flag `.md` files in `references/` directories with zero `skill-loads-shared-ref` or `skill-loads-cross-ref` inbound edges.
- **Skill-local references**: Flag `.md` files in `skills/*/references/` with zero `skill-loads-local-ref` inbound edges.
- **Hook scripts**: Flag `.sh` files in `hooks/` with zero `hook-runs-script` inbound edges.

Each orphaned component is a **Low** severity finding. Note: files in `references/adapters/` subdirectories may be dynamically loaded based on arguments and should be flagged with a caveat noting they may be loaded dynamically.

### Pass 5: Agent-Skill Mismatches (High)

For each agent's `skills:` list in its frontmatter:

1. **Unresolvable skill names**: The skill name doesn't match any skill in the same plugin group. Flag as High severity with the agent name, unresolvable skill name, and a suggestion of possible matches (fuzzy).

2. **Ambiguous cross-plugin bindings**: If the skill name matches skills in multiple plugin groups but no qualifier is provided, flag as High severity.

Note: Agent `skills:` bindings in Claude Code are resolved within the same plugin group. A skill name in an agent's `skills:` list refers to a skill directory name under the agent's own plugin group's `skills/` directory.

### Pass 6: Marketplace Consistency (Medium)

Compare the marketplace registry against actual directories:

1. **Missing registry entries**: Directories under `claude/` that look like plugin groups (contain `skills/` or `agents/` subdirectories) but have no corresponding entry in `marketplace.json`. Exclude `.claude-plugin/` itself.

2. **Stale registry entries**: Entries in `marketplace.json` whose `source` path doesn't resolve to an existing directory.

3. **Source path mismatches**: Registry entry `source` field doesn't match the actual directory name.

Each finding is **Medium** severity.

### Pass 7: Hook Integrity (Low)

For each `hooks.json` file:

1. **Invalid matcher patterns**: Check that `matcher` values reference valid Claude Code tool names. Known valid tools include: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`, `WebFetch`, `WebSearch`, `Task`, `AskUserQuestion`, `NotebookEdit`, `SendMessage`, `TodoWrite`. Matchers using `|` for OR are valid. Flag unrecognized tool names.

2. **Missing scripts**: Already covered by Pass 2 (missing dependencies), but if the script reference uses a non-standard path pattern (not `${CLAUDE_PLUGIN_ROOT}/hooks/`), flag it.

3. **Timeout values**: If `timeout` is set, verify it's a positive number. Flag zero or negative timeouts.

4. **Invalid hook types**: Verify `type` field is a recognized value (`command`, `prompt`).

Each finding is **Low** severity.

### Step: Display Analysis Summary

```
[Phase 3/5] Analysis Complete

| Pass | Check | Severity | Findings |
|------|-------|----------|----------|
| 1 | Circular dependencies | Critical | N |
| 2 | Missing dependencies | High | N |
| 3 | Broken cross-plugin paths | Medium | N |
| 4 | Orphaned components | Low | N |
| 5 | Agent-skill mismatches | High | N |
| 6 | Marketplace consistency | Medium | N |
| 7 | Hook integrity | Low | N |
| | **Total** | | **N** |
```

---

## Phase 4: Cross-Reference Documentation

**Goal:** Compare the dependency graph against documentation files (CLAUDE.md, plugin README files) to detect drift. Skip this phase if the `check-docs-drift` setting is `false`.

If `check-docs-drift` is `false`, display:
```
[Phase 4/5] Documentation cross-referencing skipped (check-docs-drift: false)
```
Then proceed to Phase 5.

### Check 1: CLAUDE.md Plugin Inventory Table

Read the root `CLAUDE.md` file and parse the **Plugin Inventory** table.

For each row in the table:
- **Skill count**: Compare the comma-separated skill names in the "Skills" column against the actual skills discovered in Phase 1. Flag missing or extra skills.
- **Agent count**: Compare the comma-separated agent names in the "Agents" column against actual agents. Flag missing or extra agents.
- **Version**: Compare the version in the table against the version in `marketplace.json`. Flag mismatches.

Each drift finding is **Medium** severity with type `docs-drift`.

### Check 2: CLAUDE.md Composition Chains

Read the **Key Skill Composition Chains** section in CLAUDE.md. For each documented chain:
- Verify the source skill exists
- Verify the target skill/agent exists
- Check that the edge exists in the dependency graph (the source actually loads/spawns the target)

Flag documented chains that don't match the actual graph as **Medium** severity `docs-drift`.

Do NOT flag undocumented chains — CLAUDE.md only documents "key" chains, not all of them.

### Check 3: CLAUDE.md Critical Plugin Files Table

Read the **Critical Plugin Files** table. For each row:
- Verify the file exists at the listed path
- Get the actual line count using `Bash: wc -l`
- Compare against the documented line count. Apply the `line-count-tolerance` setting (default 10%). Flag if the actual count differs by more than the tolerance percentage.

Each finding is **Low** severity with type `docs-drift`.

### Check 4: Plugin README Files

For each plugin group, read its `README.md` (if it exists):
- Parse the skills table and compare listed skills against actual skills in that group
- Parse the agents table and compare listed agents against actual agents in that group

Flag missing or extra entries as **Medium** severity with type `docs-drift`.

### Display Documentation Summary

```
[Phase 4/5] Documentation Cross-Reference

| Source | Check | Findings |
|--------|-------|----------|
| CLAUDE.md | Plugin Inventory | N |
| CLAUDE.md | Composition Chains | N |
| CLAUDE.md | Critical Files | N |
| README files | Skill/Agent tables | N |
| **Total** | | **N** |
```

---

## Phase 5: Report

**Goal:** Present findings interactively; optionally export as a markdown file.

### Step 1: Compute Health Score

```
health_score = (components_without_issues / total_components) × 100
```

Where `total_components` is the count of all skills, agents, references, and scripts discovered in Phase 1. A component "has issues" if it appears in any finding from Phase 3 or Phase 4.

Determine health indicator:
- 90-100%: "Healthy"
- 70-89%: "Needs Attention"
- 50-69%: "Outdated"
- 0-49%: "Critical Issues"

### Step 2: Auto-Export (if --report-file)

If `REPORT_FILE` is set, write the full report before presenting the interactive menu. The markdown report should include:

1. **Header** with ecosystem name, date, health score
2. **Inventory summary** table from Phase 1
3. **Dependency graph statistics** from Phase 2
4. **Dependency graph diagram** — Load `Read ${CLAUDE_PLUGIN_ROOT}/../core-tools/skills/technical-diagrams/SKILL.md`, then generate a Mermaid flowchart showing plugin groups as subgraphs and key cross-plugin dependency edges. Limit to 15-20 nodes max. Highlight nodes involved in findings using `danger` (critical) or `warning` (high) classDef styles.
5. **All findings** grouped by severity (critical → low), each with:
   - Component involved
   - Issue type and description
   - Expected vs actual (where applicable)
   - Suggested fix
6. **Documentation drift findings** from Phase 4 (if run)
7. **Health score** and recommendation

```
Write: {REPORT_FILE}
```

Display: `Report exported to: {REPORT_FILE}`

### Step 3: Present Interactive Report

Present the summary via AskUserQuestion:

```yaml
AskUserQuestion:
  questions:
    - header: "Dependency Health Report"
      question: |
        ## Plugin Ecosystem — {health_indicator}

        **Health Score: {health_score}%** ({components_without_issues}/{total_components} components clean)

        | Severity | Count |
        |----------|-------|
        | Critical | N |
        | High | N |
        | Medium | N |
        | Low | N |

        {total_findings} findings across {groups_with_issues} plugin groups.

        How would you like to explore the results?
      options:
        - label: "View all findings"
          description: "Findings grouped by severity, from critical to low"
        - label: "View by plugin group"
          description: "Select a plugin group to see its findings"
        - label: "View dependency graph"
          description: "Text-based graph showing all dependency edges"
        - label: "Done"
          description: "Exit the dependency checker"
      multiSelect: false
```

### Step 4: Handle User Selections

**View all findings:**
Display all findings grouped by severity (critical first), each showing:
- **Component**: The file or component involved
- **Issue**: Description of the problem
- **Expected**: What was expected (if applicable)
- **Actual**: What was found (if applicable)
- **Fix**: Suggested remediation

After displaying, loop back to the interactive menu (Step 3).

**View by plugin group:**
Present a follow-up AskUserQuestion with the plugin groups as options. After the user selects a group, display only findings involving components in that group. Then loop back to the interactive menu.

**View dependency graph:**
Display a text-based representation of the dependency graph:
```
core-tools/
  skills/
    deep-analysis
      -> spawns: code-explorer (core-tools), code-synthesizer (core-tools)
      <- loaded by: codebase-analysis (core-tools), feature-dev (dev-tools), docs-manager (dev-tools), create-spec (sdd-tools)
    codebase-analysis
      -> loads: deep-analysis (core-tools)
      -> loads ref: report-template.md, actionable-insights-template.md
  agents/
    code-explorer
      -> binds: project-conventions, language-patterns
      <- spawned by: deep-analysis
...
```

Also generate a Mermaid flowchart version showing plugin groups as subgraphs with color-coded finding severity (`danger` classDef for critical, `warning` for high, `primary`/`secondary` for clean nodes). Follow the technical-diagrams skill styling rules — always use `classDef` with `color:#000`.

After displaying, loop back to the interactive menu.

**Done:**
Exit the workflow. Display a final one-line summary:
```
Dependency check complete. {total_findings} findings ({critical_count} critical, {high_count} high).
```

---

## Error Handling

### No Plugin Groups Found

If no plugin group directories are found under `claude/` (or the filtered group doesn't exist):
1. Display an error message listing what was searched
2. If `--plugin` was used, suggest valid group names from the marketplace registry
3. Exit the workflow

### Marketplace Registry Missing

If `marketplace.json` doesn't exist or can't be parsed:
1. Log a warning: `Warning: marketplace.json not found or invalid. Skipping marketplace consistency checks (Pass 6).`
2. Continue with all other passes — the registry is only needed for Pass 6 and documentation drift checks.

### Malformed Component Files

If a SKILL.md or agent `.md` file can't have its YAML frontmatter parsed:
1. Log a warning for that specific file
2. Skip edge extraction for that file
3. Add a **Medium** severity finding: `"Malformed frontmatter: {file_path}"`
4. Continue processing other files

### Large Ecosystem Performance

The analysis reads every component file. For performance:
- Read frontmatter-only when only frontmatter fields are needed (agents)
- Read full file content when body scanning is needed (skills — for `subagent_type` and path patterns)
- Use Glob results from Phase 1 to avoid redundant file discovery

---

## Finding Schema

Every finding produced by Phase 3 and Phase 4 follows this structure:

```
{
  id: "{pass_number}.{index}",
  severity: "critical" | "high" | "medium" | "low",
  type: "circular-dep" | "missing-dep" | "broken-path" | "orphaned" |
        "agent-skill-mismatch" | "marketplace-inconsistency" |
        "hook-integrity" | "docs-drift",
  component: "{group}/{component_type}/{name}",
  message: "Human-readable description of the issue",
  expected: "What was expected (optional)",
  actual: "What was found (optional)",
  fix: "Suggested remediation"
}
```

---

## Dependency Patterns Reference

These are the regex patterns used in Phase 2 for edge extraction. They are provided here as a quick reference — the authoritative patterns are in Phase 2 above.

| Dependency Type | Regex Pattern |
|----------------|---------------|
| Cross-plugin skill load | `\$\{CLAUDE_PLUGIN_ROOT\}/\.\./([^/]+)/skills/([^/]+)/SKILL\.md` |
| Same-plugin skill load | `\$\{CLAUDE_PLUGIN_ROOT\}/skills/([^/]+)/SKILL\.md` (without preceding `/../`) |
| Shared reference load | `\$\{CLAUDE_PLUGIN_ROOT\}/references/([^\s"'` `)]+\.md)` |
| Skill-local reference load | `\$\{CLAUDE_PLUGIN_ROOT\}/skills/([^/]+)/references/([^\s"'` `)]+\.md)` |
| Cross-plugin reference | `\$\{CLAUDE_PLUGIN_ROOT\}/\.\./([^/]+)/(skills/[^/]+/)?references/([^\s"'` `)]+\.md)` |
| Agent spawning | `subagent_type[:\s]*["']?([^"'\s,}]+)` |
| Registry read | `\$\{CLAUDE_PLUGIN_ROOT\}/\.\./\.\./\.claude-plugin/` |
| Hook script | `\$\{CLAUDE_PLUGIN_ROOT\}/hooks/([^\s"']+)` |
| Agent skill binding | YAML `skills:` list in agent frontmatter |
