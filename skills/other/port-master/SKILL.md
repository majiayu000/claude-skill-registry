---
name: port-master
description: >-
  Convert Claude Code plugins into generic, platform-agnostic format. Supports full conversion
  (skills, agents, hooks), flatten mode (skills only — agents converted to skills, hooks
  absorbed), or nested mode (agents nested as pure markdown within parent skills, hooks absorbed).
  Full mode supports per-group or unified output layouts — unified merges all groups into a
  single directory organized by component type.
  Strips Claude Code-specific implementation details to produce clean markdown files preserving
  only the intent and instructions.
  Use when asked to "make this portable", "convert to generic format", "export plugin",
  "create universal skills", "strip platform dependencies", "make harness-agnostic",
  "decouple from Claude Code", "flatten to skills only", "nest agents in skills", or when
  the user wants their plugin content usable outside Claude Code. Also use when the user wants
  to share skills with teams using different agent frameworks.
argument-hint: <plugin-group> [--all] [--output <dir>] [--flatten] [--nested] [--unified]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, AskUserQuestion
---

# Port Master

Extract the platform-agnostic intent from Claude Code plugins, producing clean markdown files that any agent harness developer can read and adapt. The output preserves the *what* and *why* of each skill, agent, and hook while removing implementation details tied to Claude Code.

The goal is portability through clarity — a developer familiar with any agent framework should be able to read the output and integrate it into their system without needing to understand Claude Code's internals.

Three output modes are supported:
- **Full mode** (default): Produces skills, agents, and hooks — preserves the original component structure in generic format. Supports two output layouts:
  - **Per-group** (default): Each plugin group gets its own subdirectory with separate manifest and integration guide.
  - **Unified** (`--unified`): All groups merged into a single directory — one manifest, one integration guide, components organized by type. Cross-group dependencies become internal. Only meaningful when converting multiple groups.
- **Flatten mode** (`--flatten`): Produces skills only — agents are converted to skills, hooks are absorbed into a `lifecycle-hooks` skill. Use this for agent harnesses that only support skills and not agents or hooks.
- **Nested mode** (`--nested`): Agents become pure markdown instruction files nested within their parent skill's `agents/` directory. Hooks are absorbed into a `lifecycle-hooks` skill. Use this for harnesses that support sub-agent delegation but use skills as the primary organizational unit.

Complete ALL 5 phases. After completing each phase, immediately proceed to the next without waiting for user prompts.

## Critical Rules

### AskUserQuestion is MANDATORY

Use the `AskUserQuestion` tool for ALL questions to the user. Never ask questions through regular text output.

- Selection questions → AskUserQuestion
- Confirmation questions → AskUserQuestion
- Clarifying questions → AskUserQuestion

Text output is only for status updates, summaries, and informational context.

### AskUserQuestion Option Limits

Each question in `AskUserQuestion` supports **2-4 options maximum** (plus a built-in "Other" for free-text input). Never create questions with more than 4 options — use presets, categories, or follow-up questions to stay within limits. When users need to pick from a large set, list all available items in the question text and let users specify via "Other".

### Plan Mode Behavior

This skill performs an interactive conversion workflow. When invoked during plan mode:

- Proceed with the full wizard and conversion workflow immediately
- Write converted files to the output directory as normal
- Do NOT create an implementation plan or defer work to an "execution phase"

## Phase Overview

1. **Configuration Wizard & Component Selection** — Parse arguments, upfront wizard, load registry, interactive selection
2. **Dependency Analysis** — Build dependency graph, classify dependencies, plan smart resolution
3. **Conversion** — Transform each component using rules from `references/conversion-rules.md`
4. **Output Generation** — Write files, manifest, and integration guide
5. **Summary** — Present results and next steps

---

## Phase 1: Configuration Wizard & Component Selection

**Goal:** Gather all configuration (plugins, output directory, output mode) upfront, then select components.

### Step 1: Parse Arguments

Parse `$ARGUMENTS` for:
- Plugin group name(s) — positional arguments
- `--all` — Convert all plugin groups
- `--output <dir>` — Output directory (default: `./ported/`)
- `--flatten` — Skills-only output mode (agents converted to skills, hooks absorbed)
- `--nested` — Nested output mode (agents nested as pure markdown within parent skills, hooks absorbed)
- `--unified` — Unified output layout (all groups merged into a single directory tree; full mode only)

If both `--flatten` and `--nested` are provided, report an error: these flags are mutually exclusive. Ask the user to choose one.

If `--unified` is provided together with `--flatten` or `--nested`, report an error: `--unified` only applies to full mode.

If `--unified` is provided with only one group (not `--all`), ignore it silently — unified and per-group produce identical output for a single group.

### Step 2: Load Marketplace Registry

Read the plugin registry to enumerate available plugin groups:

```
Read: ${CLAUDE_PLUGIN_ROOT}/../../.claude-plugin/marketplace.json
```

Parse the `plugins` array. Each entry has `name`, `version`, `description`, and `source` (relative path like `./core-tools`). Extract the short group name from the source path.

**Exclude `plugin-tools` from the selection list** — the converter should not attempt to convert itself.

For each group, scan its directory to count components:
- Skills: `Glob claude/{group}/skills/*/SKILL.md`
- Agents: `Glob claude/{group}/agents/*.md`
- Hooks: check for `claude/{group}/hooks/hooks.json`

### Step 3: Configuration Wizard

Present configuration options via `AskUserQuestion`. Build the questions array dynamically — include only questions that still need user input (skip questions fully answered by arguments).

**If ALL arguments were provided** (valid plugin names or `--all`, plus `--output` and `--flatten` or `--nested`), skip this step entirely and proceed to Step 4.

Otherwise, build the questions array from the following, including only the ones needed. Combine applicable questions into a single `AskUserQuestion` call (max 4 questions per call).

**Q1: Plugin Groups** — include unless `--all` was specified or all positional args are valid group names.

List all available groups (with component counts) in the question text so users can reference them when choosing "Other". Use preset-based options to stay within the 4-option limit:

```yaml
- header: "Plugin Groups"
  question: "Which plugin groups would you like to convert? Available: {group1} ({N} skills, {M} agents), {group2} (...), ..."
  options:
    - label: "All groups"
      description: "Convert all {count} available plugin groups"
    - label: "Core stack"
      description: "core-tools + dev-tools + claude-tools"
    - label: "SDD pipeline"
      description: "sdd-tools + tdd-tools + claude-tools"
  multiSelect: false
```

Build the preset options dynamically from the available groups — create 2-3 logical groupings based on the plugin descriptions. The user can always type specific group names via the built-in "Other" option.

If positional arguments named specific plugins but any name is invalid, note the invalid name in the question text: "'{invalid-name}' was not found."

**Q2: Output Directory** — include unless `--output` was provided:

```yaml
- header: "Output"
  question: "Where should the converted files be written?"
  options:
    - label: "./ported/ (Recommended)"
      description: "Standard ported output location — timestamped subdirectory created automatically"
    - label: "Custom path"
      description: "Specify a different output directory"
  multiSelect: false
```

**Q3: Output Mode** — include unless `--flatten` or `--nested` was provided:

```yaml
- header: "Output Mode"
  question: "What output format should be used?"
  options:
    - label: "Full (skills, agents, hooks)"
      description: "Preserves original component structure in generic format"
    - label: "Skills only (flatten)"
      description: "Converts agents to skills, absorbs hooks — for harnesses that only support skills"
    - label: "Nested (skills with embedded agents)"
      description: "Agents nested as pure markdown in parent skills, hooks absorbed — for harnesses using skills as primary unit"
  multiSelect: false
```

**Q4: Output Layout** — include only when ALL of these conditions are met:
- Output mode is "Full" (not flatten or nested) — determined by arguments or Q3 answer
- Multiple groups are selected or `--all` was specified — determined by arguments or Q1 answer
- `--unified` was NOT already provided as an argument

```yaml
- header: "Output Layout"
  question: "How should the output be organized?"
  options:
    - label: "Per-group (Recommended)"
      description: "Each group in its own subdirectory with separate manifest and integration guide"
    - label: "Unified"
      description: "All groups merged into one directory — single manifest, single integration guide, components organized by type"
  multiSelect: false
```

Store results as:
- `SELECTED_GROUPS` — plugin groups to convert (parse from preset or "Other" text)
- `OUTPUT_DIR` — base output directory (before timestamp)
- `FLATTEN_MODE` — boolean, true if "Skills only" selected or `--flatten` provided
- `NESTED_MODE` — boolean, true if "Nested" selected or `--nested` provided
- `UNIFIED_LAYOUT` — boolean, true if "Unified" selected or `--unified` provided. Always false in flatten/nested mode or when only one group is selected

### Step 4: Component-Level Selection

For each selected group, enumerate components by reading frontmatter from each file to extract `name` and `description`. Count skills, agents, and hooks.

Present a simplified selection per group using preset options (stays within 4-option limit). List all component names in the question text so users know what's available:

```yaml
AskUserQuestion:
  questions:
    - header: "{group-name}"
      question: "Select components from {group-name} ({total} total — Skills: {skill_names}; Agents: {agent_names}; Hooks: {yes/no}):"
      options:
        - label: "All components (Recommended)"
          description: "Convert all {total} components"
        - label: "Skills only"
          description: "Convert {skill_count} skills, skip agents and hooks"
        - label: "Custom selection"
          description: "Specify which components to include via text"
      multiSelect: false
```

If multiple groups are selected, you can ask about all groups in a single `AskUserQuestion` call (one question per group, max 4 questions per call). For more than 4 groups, use multiple sequential calls.

If the user selects "Custom selection" or types specific names via "Other", parse their response to build the component list.

In **flatten mode**, add context to the question text:
- Note that agents will be converted to skills and hooks will be absorbed into a lifecycle-hooks skill

In **nested mode**, add context to the question text:
- Note that agents will be nested as pure markdown instruction files within their parent skill's `agents/` directory
- Note that hooks will be absorbed into a lifecycle-hooks skill (same as flatten)

Build `SELECTED_COMPONENTS` — a flat list:
```
[{ type: "skill"|"agent"|"hooks", group: "{group}", name: "{name}", path: "{file path}" }]
```

### Step 5: Confirm Selection

Present a summary table showing selected components, output mode, and output directory. Confirm with the user:

```yaml
AskUserQuestion:
  questions:
    - header: "Confirm"
      question: "Proceed with converting {count} components? Output: {output_mode}{layout_suffix}, Directory: {OUTPUT_DIR}"
      options:
        - label: "Proceed"
          description: "Continue to dependency analysis"
        - label: "Modify"
          description: "Change configuration"
        - label: "Cancel"
          description: "Exit"
      multiSelect: false
```

Where `{output_mode}` is "Full", "Flatten (skills only)", or "Nested (skills with embedded agents)". `{layout_suffix}` is ` (unified layout)` when `UNIFIED_LAYOUT` is true, empty string otherwise.

---

## Phase 2: Dependency Analysis & Resolution Planning

**Goal:** Map all dependencies between selected components and plan how to resolve them in the generic output.

### Step 1: Parse Dependencies

For each component in `SELECTED_COMPONENTS`, read its source file and scan for dependency patterns.

**Six dependency patterns to detect:**

| Pattern | Example | Type |
|---------|---------|------|
| Same-plugin skill load | `Read ${CLAUDE_PLUGIN_ROOT}/skills/{name}/SKILL.md` | skill-to-skill |
| Cross-plugin load | `${CLAUDE_PLUGIN_ROOT}/../{group}/skills/{name}/SKILL.md` | cross-plugin |
| Reference file include | `${CLAUDE_PLUGIN_ROOT}/skills/{name}/references/{file}` | reference |
| Agent spawn | `subagent_type: "{name}"` or `subagent_type: "{plugin}:{name}"` | agent-ref |
| Agent skill preload | `skills:` array in agent frontmatter | agent-to-skill |
| Agent-to-agent reference | Agent body mentions another agent by name in spawning context | agent-to-agent |

Also detect external dependencies (MCP servers, shell scripts) for informational tracking.

### Step 2: Classify Dependencies

For each dependency found, classify it:

| Classification | Meaning | Action |
|----------------|---------|--------|
| **Internal** | Target is in `SELECTED_COMPONENTS` | Will be converted; reference by name |
| **External-available** | Target exists on disk but wasn't selected | Reference by name in manifest |
| **External-missing** | Target doesn't exist locally | Note as unresolved in manifest |
| **Reference file** | Points to a `references/*.md` file | Smart resolution (see Step 3) |

**Unified layout adjustment:** When `UNIFIED_LAYOUT` is active, dependencies that would be classified as **External-available** between selected groups are reclassified as **Internal**. A component from group A that depends on a component from group B (both selected) is internal in unified mode because both exist in the same output directory. Only dependencies pointing to groups NOT in `SELECTED_GROUPS` remain external.

### Step 3: Smart Resolution Planning

For each reference file dependency, determine how to handle it based on line count, consumer count, and consumer type.

1. Count lines in the referenced file using `Bash: wc -l < {path}`
2. Determine the **primary owner** — the skill whose source directory originally contained the reference file (from the source path `skills/{owner}/references/{file}`). If the primary owner was not selected for conversion, assign ownership to the first selected consumer
3. Identify all consumers — which skills and agents use this reference

**Decision logic for skill-consumed references:**

- **Under 250 lines AND single consumer** → mark for **inline** (content will be embedded directly in the consuming skill's SKILL.md)
- **250+ lines AND single consumer** → mark as **separate** in the consuming skill's `references/` directory
- **Multiple skill consumers** → mark as **separate** in the **primary owner** skill's `references/` directory; other consumers reference via relative path `../{owner-skill}/references/{file}`

**Decision logic for agent-consumed references (full mode):**

- **Under 250 lines** → mark for **inline** into the agent's body
- **250+ lines** → mark as **promote_to_skill** — the reference becomes a new skill at `skills/{ref-name}/SKILL.md` with its content as the body. The agent's converted text will reference it as a dependency. If the name collides with an existing skill, prefix with the agent name: `{agent-name}-{ref-name}`

**Decision logic for agent-consumed references (flatten mode):**

When `FLATTEN_MODE` is active, agents are converted to skills. Use skill-consumed rules instead of promote_to_skill:

- **Under 250 lines AND single consumer** → mark for **inline** into the agent-as-skill's body
- **250+ lines AND single consumer** → mark as **separate** in the agent-as-skill's `references/` directory
- **Multiple consumers** → mark as **separate** in the **primary owner** skill's `references/` directory

This avoids creating promoted skills when the agent itself is already becoming a skill — the reference can live directly in the agent-as-skill's own `references/` directory.

**Decision logic for agent-consumed references (nested mode):**

When `NESTED_MODE` is active, agents are nested within their parent skill's directory. Use skill-consumed rules (same as flatten), but the "owning skill" for a nested agent's references is the **parent skill** from `AGENT_PARENT_MAP`:

- **Under 250 lines AND single consumer** → mark for **inline** into the nested agent's markdown body
- **250+ lines AND single consumer** → mark as **separate** in the **parent skill's** `references/` directory
- **Multiple consumers** → mark as **separate** in the **primary owner** skill's `references/` directory

This keeps all reference files at the skill directory level — nested agents don't have their own `references/` subdirectory.

**Mixed consumers (skill + agent):** Skill-consumed rules take precedence. The agent references the owning skill's directory.

**Unified layout adjustment:** When `UNIFIED_LAYOUT` is active, cross-group reference resolution follows the same rules as same-group resolution. All skills are siblings under a single `skills/` directory, so cross-skill paths use the standard `../{owner-skill}/references/{file}` convention regardless of which group the skills originated from.

Store decisions as `RESOLUTION_PLAN`:
```
[{ ref_path, line_count, decision: "inline"|"separate"|"promote_to_skill", owner_skill: "{skill-name}", used_by: [component names] }]
```

### Step 3b: Agent-to-Parent Mapping (Nested Mode Only)

Skip this step unless `NESTED_MODE` is active.

For each agent in `SELECTED_COMPONENTS`, determine which skill "owns" it — the parent skill under which the agent will be nested.

**Detection patterns (ordered by priority):**

1. **`subagent_type` references** — Scan all selected skills for `subagent_type` patterns matching the agent name (e.g., `subagent_type: "code-explorer"` or `subagent_type: "core-tools:code-explorer"`). Highest confidence.
2. **Prose spawning references** — Scan skill bodies and their reference files for the agent name appearing in spawning contexts (e.g., "launch a wave-lead", "spawn the code-explorer agent"). Lower confidence but catches agents referenced without `subagent_type`.
3. **Agent-to-agent chains** — Scan other agents' bodies for references to this agent. If agent A spawns agent B, and agent A's parent is skill S, then agent B also nests under skill S.

**Priority resolution when multiple skills reference the same agent:**

- **Same-group skill with `subagent_type`** takes priority
- **Same-group skill with prose reference** is second
- **Agent-spawner's parent skill** is third (for agent-to-agent chains)
- If still tied, the skill with the most references to the agent wins

**Agent-spawns-agent chains:** When an agent spawns another agent (e.g., `wave-lead` spawns `context-manager`), both nest under the same grandparent skill. The `agents/` directory is flat — no nesting within nested agents.

**Orphan agents:** If no selected skill references an agent, mark it as `orphan`. Orphan agents will be promoted to standalone skills during Phase 3.

Store the mapping as `AGENT_PARENT_MAP`:
```
{ agent_name: parent_skill_name | "orphan" }
```

### Step 4: Present Dependency Summary

Show the user:
- Total dependencies found
- How many will be inlined vs. kept as separate files
- Which skill directories will contain `references/` subdirectories and what they own
- Any references promoted from agent references to standalone skills
- Any external/missing dependencies that won't be included
- In **nested mode**, also show:
  - Agent-to-parent mappings discovered (which agent nests under which skill)
  - Any orphan agents that will be promoted to standalone skills
  - Any agents referenced by multiple skills (which skill gets the nesting, which get cross-references)
- In **unified layout**, also show:
  - Cross-group dependencies reclassified as internal (count and list)
  - Any name collisions detected across groups (components with the same type and name from different groups)
- Ask for confirmation to proceed

---

## Phase 3: Conversion

**Goal:** Transform each component into a clean, platform-agnostic format.

Before starting conversion, read the detailed transformation rules:

```
Read ${CLAUDE_PLUGIN_ROOT}/skills/port-master/references/conversion-rules.md
```

Process components in dependency order (leaf nodes first) so that when a component references another, the referenced component has already been converted.

### Skill Conversion

For each skill:

1. **Read source** — Read the SKILL.md file, split into YAML frontmatter and markdown body
2. **Transform frontmatter** — Apply the Skill Frontmatter Rules from conversion-rules.md: keep `name` and `description`, remove platform-specific fields, add `dependencies` list
3. **Transform body** — Apply all Body Transformation Rules from conversion-rules.md in order:
   - Resolve `${CLAUDE_PLUGIN_ROOT}` references (inline small content or add `See: {name}` pointers)
   - Rewrite tool-specific language to generic descriptions
   - Decompose orchestration patterns (teams, tasks, waves) into sequential/parallel prose
   - Remove prompt engineering directives aimed at Claude specifically
   - Generalize settings and configuration references (rule 3f)
   - Apply `.claude/` → `.agents/` path replacement (rule 3g)
4. **Append Integration Notes** — Add a `## Integration Notes` section describing what capabilities the target harness needs to support this skill
5. **Store result** for output in Phase 4

### Agent Conversion (Full Mode)

Skip this section if `FLATTEN_MODE` or `NESTED_MODE` is active — use "Agent-to-Skill Conversion" or "Agent-to-Nested Conversion" below instead.

For each agent:

1. **Read source** — Read the agent `.md` file
2. **Transform frontmatter** — Keep `name` and `description`. Add `role` (inferred from description: explorer, reviewer, architect, executor, etc.). Add `dependencies` for any preloaded skills
3. **Transform body** — Same rules as skills (including 3g path replacement), plus:
   - Resolve `skills:` preloads into prose ("This agent draws on knowledge from {skill-name}")
   - Remove tool-restriction prose ("You only have access to Read, Glob, Grep")
4. **Append Integration Notes**
5. **Store result**

### Hook Conversion (Full Mode)

Skip this section if `FLATTEN_MODE` or `NESTED_MODE` is active — use "Hook-to-Skill Conversion" below instead.

For each hooks component:

1. **Read source** — Read `hooks.json` and parse JSON
2. **Convert to YAML** — Map Claude Code event names to generic lifecycle events using the Hook Event Mapping table from conversion-rules.md
3. **Process hook entries:**
   - **Command hooks** → Copy referenced scripts, resolve `${CLAUDE_PLUGIN_ROOT}` paths to relative paths within the output directory. Apply rule 3g (`.claude/` → `.agents/`) to script content. Add a comment explaining what the script does (read the script to understand its purpose)
   - **Prompt hooks** → Preserve the prompt text as-is (already platform-agnostic). Apply rule 3g to any `.claude/` paths in the prompt text
4. **Add descriptions** — For each hook entry, add a `description` field explaining when and why this hook fires
5. **Store result**

### Agent-to-Nested Conversion (Nested Mode)

Skip this section unless `NESTED_MODE` is active.

For each agent **with a parent** in `AGENT_PARENT_MAP`:

1. **Read source** — Read the agent `.md` file, split into YAML frontmatter and markdown body
2. **Strip frontmatter** — Remove YAML frontmatter entirely (no `---` delimiters in output)
3. **Structure as pure markdown** — Apply the Agent-to-Nested Conversion Rules from Section 9 of conversion-rules.md:
   - `# {Agent Name}` title (from frontmatter `name`)
   - One-line summary (from frontmatter `description`)
   - `## Role` — Rewrite identity framing to role description. Keep the role-based voice (e.g., "Responsible for exploring codebases...") since this is still a sub-agent — do NOT use task instruction framing like flatten mode
   - `## Inputs` — Document expected parameters the agent receives when spawned
   - `## Process` — Preserve numbered workflow steps and phase structure from the body
   - `## Output Format` — Document structured output format if applicable; omit if not
   - `## Guidelines` — Consolidate behavioral rules and constraints; omit if none
4. **Transform body** — Apply all standard Body Transformation Rules (3a-3g from conversion-rules.md) to the content within each section
5. **Convert `skills:` preloads** — Add "This agent draws on knowledge from:" in the Role section, listing each preloaded skill with a brief description
6. **Remove tool-restriction prose** — Same as full/flatten mode
7. **Store result** for output at `skills/{parent-skill}/agents/{agent-name}.md`

For each **orphan agent** (marked as `orphan` in `AGENT_PARENT_MAP`):

1. Apply the Agent-to-Skill conversion rules (same as flatten mode, Section 7 of conversion-rules.md)
2. Store as `skills/{agent-name}/SKILL.md`
3. Append to Integration Notes: "**Origin:** Promoted from orphan agent `{name}` — no parent skill in this package spawns this agent directly"

### Parent Skill Augmentation (Nested Mode)

Skip this section unless `NESTED_MODE` is active.

After converting all nested agents, augment each parent skill's converted SKILL.md:

1. **Add a `## Nested Agents` section** listing all agents nested under this skill:
   ```markdown
   ## Nested Agents

   The `agents/` directory contains instructions for specialized sub-agents.
   Read them when spawning the relevant sub-agent.

   - `agents/{agent-name}.md` — {one-line description from the agent's original description}
   ```

2. **Rewrite spawn instructions** in the parent skill's body to reference nested files:
   - Before: "Spawn N agents via Agent tool with subagent_type: '{name}'"
   - After: "Delegate to N independent {role} agents (see `agents/{name}.md` for instructions)"

3. **Add cross-references** for agents nested under a different skill:
   - "This step uses the **{agent-name}** agent from the **{parent-skill}** skill (see `../{parent-skill}/agents/{agent-name}.md`)"

4. **Add sub-agent capability requirements** to the parent skill's Integration Notes:
   ```markdown
   **Sub-agent capabilities:**
   - **{agent-name}**: Requires {capability list from the agent's original tools field}
   ```

### Agent-to-Skill Conversion (Flatten Mode)

Only applies when `FLATTEN_MODE` is active. Each agent is converted to a skill.

For each agent:

1. **Read source** — Read the agent `.md` file, split into YAML frontmatter and markdown body
2. **Build skill frontmatter:**
   - `name`: Keep the agent name
   - `description`: Keep the agent description. Append " (converted from agent)"
   - `dependencies`: Merge the agent's `skills:` preloads with any detected skill references in the body
3. **Transform body** — Apply all standard Body Transformation Rules (3a-3g from conversion-rules.md), then apply the Agent-to-Skill Reframing Rules from Section 7 of conversion-rules.md:
   - Rewrite agent identity framing ("You are a {role} that...") to task instructions ("When invoked, perform the following {role} tasks:")
   - Remove tool-restriction prose ("You only have access to...")
   - Convert `skills:` preloads into "Prerequisites" section
   - Convert the agent's `tools` list into a capabilities paragraph in Integration Notes
4. **Append Integration Notes** — Use the standard template plus:
   - "**Origin:** Converted from agent `{name}` — originally invoked as a sub-agent, not directly by the user"
   - If the agent had a specific `model` (e.g., Opus, Sonnet), note: "**Complexity hint:** Originally ran on a {model-tier} model — may benefit from a more capable model for reasoning-heavy steps"
   - Include the Tool Capability Summary from Section 7 of conversion-rules.md
5. **Store result** as a skill entry (output to `skills/{name}/SKILL.md`, not `agents/`)

### Hook-to-Skill Conversion (Flatten and Nested Modes)

Only applies when `FLATTEN_MODE` or `NESTED_MODE` is active. ALL hooks from a group are merged into a single `lifecycle-hooks` skill.

If the group has no hooks, skip this section.

1. **Read source** — Read `hooks.json` and parse JSON
2. **Check for name collision** — If a skill named `lifecycle-hooks` already exists in `SELECTED_COMPONENTS` for this group, use `{group}-lifecycle-hooks` as the name instead
3. **Build skill frontmatter** — Apply the structure from Section 8 of conversion-rules.md:
   - `name`: `lifecycle-hooks` (or `{group}-lifecycle-hooks` if collision)
   - `description`: "Behavioral rules and lifecycle event handlers for the {group-name} package. (converted from hooks)"
   - `dependencies`: []
4. **Build skill body** — For each hook entry:
   - Map the Claude Code event name to its generic name using Section 4 (Hook Event Mapping)
   - Create a `## On {generic-event-name}` subsection
   - For **prompt hooks**: include the prompt text verbatim as the rule body
   - For **command hooks**: read the referenced script, summarize its behavior in prose, store the script in `skills/lifecycle-hooks/references/{script-name}.sh` (with rule 3g applied to script content)
   - Group multiple hooks on the same event under one heading with matcher sub-sections
5. **Append Integration Notes** — Use the template from Section 8 of conversion-rules.md
6. **Store result** as a skill entry

### Reference File Handling

For reference files marked as **"separate"** in the `RESOLUTION_PLAN`:

1. Read the source file
2. Clean any `${CLAUDE_PLUGIN_ROOT}` paths in the content
3. Remove Claude Code-specific tool references if present
4. Apply rule 3g (`.claude/` → `.agents/` path replacement) to the content
5. Store for copying to the owning skill's `references/` directory (i.e., `skills/{owner_skill}/references/{file}`)

For reference files marked as **"promote_to_skill"** (full mode only):

1. Read the source file
2. Apply the same body transformation rules (3a-3g from conversion-rules.md) to the content
3. Wrap the content as a new skill with minimal frontmatter (`name` and `description` inferred from the reference content and heading)
4. Store as a new skill entry at `skills/{ref-name}/SKILL.md`
5. Update the consuming agent's `dependencies` list to include the new skill name

For reference files marked as **"inline"** — their content was already embedded during skill/agent conversion.

---

## Phase 4: Output Generation

**Goal:** Write all converted files, the manifest, and the integration guide.

### Step 1: Create Timestamped Output Directory

The output directory (`OUTPUT_DIR`) was determined in Phase 1's Configuration Wizard.

Generate a timestamp in `YYYYMMDD-HHMMSS` format (e.g., `20260304-143052`) using the current date and time.

Create the timestamped output directory structure:
```
{OUTPUT_DIR}/{YYYYMMDD-HHMMSS}/
└── {group-name}/
    └── ...
```

Each selected group gets its own subdirectory under the timestamp. Store the full timestamped path as `TIMESTAMPED_OUTPUT`.

When `UNIFIED_LAYOUT` is active, skip group subdirectories — all components go directly under the timestamp:
```
{OUTPUT_DIR}/{YYYYMMDD-HHMMSS}/
├── manifest.yaml
├── INTEGRATION-GUIDE.md
├── skills/
├── agents/
└── hooks/
```

### Step 2: Write Component Files

Create the output directory structure and write all converted files.

**Full mode** output structure:

```
{TIMESTAMPED_OUTPUT}/{group-name}/
├── manifest.yaml
├── INTEGRATION-GUIDE.md
├── skills/
│   └── {name}/
│       ├── SKILL.md
│       └── references/         (only if this skill owns reference files)
│           └── {file}.md
├── agents/
│   └── {name}.md
└── hooks/
    ├── hooks.yaml
    └── scripts/
        └── {script-name}.sh
```

**Full mode — unified layout** output structure (when `UNIFIED_LAYOUT` is active):

```
{TIMESTAMPED_OUTPUT}/
├── manifest.yaml              (single combined manifest)
├── INTEGRATION-GUIDE.md       (single combined guide)
├── skills/
│   └── {name}/                (all skills from all groups, flat)
│       ├── SKILL.md
│       └── references/
│           └── {file}.md
├── agents/
│   └── {name}.md              (all agents from all groups, flat)
└── hooks/
    ├── hooks.yaml             (merged hooks from all groups)
    └── scripts/
        └── {script-name}.sh
```

**Name collision handling:** When merging components from different groups, names may collide (e.g., two groups both have a `researcher` agent). Detect collisions before writing:

1. Build a map of `{component-type}:{name}` across all groups
2. For any collision, prefix the component name with its origin group: `{group}-{name}` (e.g., `sdd-researcher` and `plugin-researcher`)
3. Update all internal references (dependency lists, spawn instructions, cross-references) to use the prefixed name
4. Record the original name in the manifest's `original_name` field for traceability

**Hooks merging:** When multiple groups have hooks, merge all hook entries into a single `hooks.yaml`. Add an `origin_group` field to each entry. If script names collide across groups, prefix with group name: `{group}-{script-name}.sh`.

**Flatten mode** output structure (skills only — no `agents/` or `hooks/` directories):

```
{TIMESTAMPED_OUTPUT}/{group-name}/
├── manifest.yaml
├── INTEGRATION-GUIDE.md
└── skills/
    └── {name}/
        ├── SKILL.md
        └── references/         (only if this skill owns reference files)
            └── {file}.md
```

In flatten mode, this includes:
- Original skills (converted as normal)
- Agent-converted skills (from Agent-to-Skill conversion)
- The `lifecycle-hooks` skill (from Hook-to-Skill conversion, if hooks existed in the source)

**Nested mode** output structure (skills with embedded agents — no top-level `agents/` or `hooks/`):

```
{TIMESTAMPED_OUTPUT}/{group-name}/
├── manifest.yaml
├── INTEGRATION-GUIDE.md
└── skills/
    └── {name}/
        ├── SKILL.md
        ├── agents/             (only if this skill owns nested agents)
        │   └── {agent-name}.md (pure markdown, no YAML frontmatter)
        └── references/         (only if this skill owns reference files)
            └── {file}.md
```

In nested mode, this includes:
- Original skills (converted as normal, augmented with `## Nested Agents` section if they own agents)
- Nested agent instruction files within their parent skill's `agents/` directory
- Orphan agents promoted to standalone skills (from Agent-to-Skill conversion)
- The `lifecycle-hooks` skill (from Hook-to-Skill conversion, if hooks existed in the source)

Each skill gets its own directory with `SKILL.md` inside. Reference files are co-located in the owning skill's `references/` subdirectory — only create the `references/` subdirectory when at least one separate reference file exists. There is no root-level `references/` directory.

Write each converted component to its appropriate location.

### Step 3: Generate manifest.yaml

The manifest provides a machine-readable inventory of the package:

```yaml
name: {group-name}
description: {from marketplace registry}
mode: "full"                               # or "flatten" or "nested"
source:
  platform: "Claude Code"
  plugin: "{marketplace-name}"
  version: "{version}"
converted: "{YYYY-MM-DD}"

components:
  skills:
    - name: {name}
      file: skills/{name}/SKILL.md
      description: {description}
      origin: skill                        # "skill", "agent", or "hooks"
      references:                          # only if this skill owns reference files
        - name: {ref-name}
          file: skills/{name}/references/{ref-name}.md
          used_by: [{component names}]
  agents:                                  # omit this section in flatten mode
    - name: {name}
      file: agents/{name}.md
      description: {description}
      role: {role}
  hooks:                                   # omit this section in flatten mode
    - event: {generic-event-name}
      file: hooks/hooks.yaml
      description: {what the hook does}

dependencies:
  internal:
    - from: {component}
      to: {component}
      relationship: "{what it loads/uses}"
  external:
    - from: {component}
      to: {external name}
      source_plugin: "{plugin group}"
      relationship: "{what it needs}"
      note: "Not included — convert separately if needed"
```

The `origin` field indicates whether each skill was originally a skill, an agent (converted to skill in flatten mode), or hooks (absorbed into lifecycle-hooks skill). In full mode, all skills have `origin: skill`.

**Full mode — unified layout** manifest (when `UNIFIED_LAYOUT` is active):

```yaml
name: unified-export
description: "Combined export of {group1}, {group2}, ... plugin groups"
mode: "full"
layout: "unified"
source:
  platform: "Claude Code"
  groups:
    - name: {group1}
      plugin: "{marketplace-name-1}"
      version: "{version-1}"
    - name: {group2}
      plugin: "{marketplace-name-2}"
      version: "{version-2}"
converted: "{YYYY-MM-DD}"

components:
  skills:
    - name: {name}
      file: skills/{name}/SKILL.md
      description: {description}
      origin: skill
      origin_group: {group-name}
      original_name: {original-name}    # only present if renamed due to collision
      references:
        - name: {ref-name}
          file: skills/{name}/references/{ref-name}.md
          used_by: [{component names}]
  agents:
    - name: {name}
      file: agents/{name}.md
      description: {description}
      role: {role}
      origin_group: {group-name}
      original_name: {original-name}    # only present if renamed due to collision
  hooks:
    - event: {generic-event-name}
      file: hooks/hooks.yaml
      description: {what the hook does}
      origin_group: {group-name}

dependencies:
  internal:                             # includes cross-group deps that were external in per-group mode
    - from: {component}
      to: {component}
      relationship: "{what it loads/uses}"
  external:                             # only deps pointing to groups NOT in SELECTED_GROUPS
    - from: {component}
      to: {external name}
      source_plugin: "{plugin group}"
      relationship: "{what it needs}"
      note: "Not included — convert separately if needed"
```

Key differences from per-group manifest: `name` is `unified-export`, `layout: "unified"` field added, `source.groups` is an array, every component has `origin_group`, and cross-group dependencies appear as internal.

In **flatten mode**, omit the `agents` and `hooks` sections entirely — all components appear under `skills`.

In **nested mode**, use `mode: "nested"` and represent agents within their parent skill entries:

```yaml
mode: "nested"

components:
  skills:
    - name: {skill-name}
      file: skills/{skill-name}/SKILL.md
      description: {description}
      origin: skill
      nested_agents:                                         # only if this skill has nested agents
        - name: {agent-name}
          file: skills/{skill-name}/agents/{agent-name}.md
          description: {description}
          origin: agent
          role: {role}
      references:                                            # only if this skill owns reference files
        - name: {ref-name}
          file: skills/{skill-name}/references/{ref-name}.md
          used_by: [{component names}]
    - name: {orphan-agent-name}                              # orphan agents appear as top-level skills
      file: skills/{orphan-agent-name}/SKILL.md
      description: {description}
      origin: agent
```

In nested mode, omit top-level `agents` and `hooks` sections. Agents appear as `nested_agents` within their parent skill. Orphan agents appear as top-level skill entries with `origin: agent`.

### Step 4: Generate INTEGRATION-GUIDE.md

The guide helps harness developers understand and integrate the converted components.

**Full mode:**

```markdown
# Integration Guide: {group-name}

## Overview
{What this package provides — summarize the plugin group's purpose}

## Component Inventory
| Component | Type | Description |
|-----------|------|-------------|
{table of all components}

## Capability Requirements
{What features the target harness needs — organized by category:}
- **File operations**: Which components need to read/write/search files
- **Shell execution**: Which components run shell commands
- **User interaction**: Which components prompt for user input
- **Sub-agent delegation**: Which components spawn child agents
- **Web access**: Which components fetch external content (if any)

## Per-Component Notes
{For each component, compile the Integration Notes section from the converted file}

## Dependency Map
{If more than 5 internal dependencies, include a text-based dependency diagram}

## Adaptation Checklist
- [ ] Review each skill's instructions and adapt tool-specific language for your harness
- [ ] Configure agent spawning for components that delegate to sub-agents
- [ ] Set up lifecycle hooks if your harness supports them
- [ ] Resolve external dependencies listed in manifest.yaml
- [ ] Test each component individually before combining
```

**Full mode — unified layout** adjustments to the integration guide:

- Title: `# Integration Guide: Unified Export`
- Add an "Overview" paragraph explaining this package combines components from N groups, with a brief description of each group
- Add a "Source Groups" table:

```markdown
## Source Groups
| Group | Original Plugin | Version | Skills | Agents | Hooks |
|-------|----------------|---------|--------|--------|-------|
{table of all source groups with component counts}
```

- The "Component Inventory" table adds an "Origin Group" column
- Add a "Name Collisions" section (omit entirely if no collisions occurred):

```markdown
## Name Collisions
| Current Name | Original Name | Origin Group | Reason |
|-------------|---------------|-------------|--------|
{collision table}
```

- "Per-Component Notes" grouped by origin group with `### From {group}` subheadings
- "Dependency Map" is a single unified graph — cross-group dependencies appear as internal
- Update the "Adaptation Checklist":

```markdown
## Adaptation Checklist
- [ ] Review each skill's instructions and adapt tool-specific language for your harness
- [ ] Configure agent spawning for components that delegate to sub-agents
- [ ] Set up lifecycle hooks if your harness supports them (hooks merged from {N} groups)
- [ ] Resolve external dependencies listed in manifest.yaml
- [ ] If components were renamed due to collisions, update any external references
- [ ] Test each component individually before combining
```

**Flatten mode** adjustments to the integration guide:

- The "Component Inventory" table uses "skill" for all types, with an "Origin" column showing the original type (skill, agent, hooks)
- The "Capability Requirements" section notes that agent and hook capabilities have been folded into skills
- Add a "Flatten Mode Notes" section after "Per-Component Notes":

```markdown
## Flatten Mode Notes

This package was converted in flatten mode — all components are skills.

### Agent-Converted Skills
{List skills that were originally agents, with their original role context}

### Lifecycle Hooks Skill
{If lifecycle-hooks skill exists: describe the behavioral rules it contains and their original event triggers}

### Capability Notes
{Any tool-scope restrictions from original agents that consumers should be aware of}
```

- Update the "Adaptation Checklist" for flatten mode:

```markdown
## Adaptation Checklist
- [ ] Review each skill's instructions and adapt tool-specific language for your harness
- [ ] Review agent-converted skills for role-appropriate context injection
- [ ] Implement lifecycle-hooks rules as middleware, event handlers, or manual checks
- [ ] Resolve external dependencies listed in manifest.yaml
- [ ] Test each component individually before combining
```

**Nested mode** adjustments to the integration guide:

- The "Component Inventory" table includes columns: Component, Type, Origin, Parent Skill, Description. Nested agents have their parent skill listed; top-level skills and orphans have "—".
- The "Capability Requirements" section notes that agent capabilities are documented within their parent skill's Integration Notes under "Sub-agent capabilities"
- Add a "Nested Mode Notes" section after "Per-Component Notes":

```markdown
## Nested Mode Notes

This package was converted in nested mode — agents are embedded within their parent skills as pure markdown instruction files.

### Nesting Map
| Agent | Parent Skill | Role | Purpose |
|-------|-------------|------|---------|
{table of agent-to-parent mappings from AGENT_PARENT_MAP}

### Reading Nested Agents
Each parent skill's SKILL.md contains a "Nested Agents" section listing its sub-agents with one-line descriptions. The agent files in `agents/` are pure markdown instructions — read them when spawning the corresponding sub-agent. They have no YAML frontmatter.

### Orphan Agents
{If any orphan agents were promoted to standalone skills, list them here with explanation. Otherwise: "No orphan agents — all agents are nested under a parent skill."}

### Cross-Skill Agent References
{If any skills reference agents nested under a different skill, list the cross-references here.}

### Lifecycle Hooks Skill
{Same as flatten mode — describe the behavioral rules it contains and their original event triggers, if hooks existed in the source}
```

- Update the "Adaptation Checklist" for nested mode:

```markdown
## Adaptation Checklist
- [ ] Review each skill's instructions and adapt tool-specific language for your harness
- [ ] For skills with nested agents, configure sub-agent spawning to read instructions from the agents/ directory
- [ ] Review orphan agents (promoted to standalone skills) for role-appropriate context
- [ ] Check cross-skill agent references and ensure relative paths work in your harness
- [ ] Implement lifecycle-hooks rules as middleware, event handlers, or manual checks
- [ ] Resolve external dependencies listed in manifest.yaml
- [ ] Test each component individually before combining
```

### Step 5: Write All Files

Write all files to the output directory using the `Write` tool. Track every file written for the summary.

---

## Phase 5: Summary

**Goal:** Present conversion results and suggest next steps.

### Results Table

```
## Conversion Complete

**Output mode:** {Full | Flatten (skills only) | Nested (skills with embedded agents)}
**Output directory:** {TIMESTAMPED_OUTPUT}

| Component | Type | Origin | Lines (source → output) | Notes |
|-----------|------|--------|------------------------|-------|
{for each component}

**Files written:** {count}
**Skill directories created:** {count}
**References inlined:** {count} ({total lines})
**References co-located with skills:** {count}
**References promoted to skills:** {count} (from agent references, full mode only)
**External dependencies:** {count} (not included)
```

In **unified layout**, add these additional stats:
```
**Output layout:** Unified
**Groups merged:** {count} ({group names})
**Cross-group deps internalized:** {count}
**Name collisions resolved:** {count} (renamed with group prefix)
```

In **flatten mode**, add these additional stats:
```
**Agents converted to skills:** {count}
**Hooks absorbed into lifecycle-hooks:** {count} ({hook_count} events)
```

In **nested mode**, add these additional stats:
```
**Agents nested within skills:** {count} (across {parent_count} parent skills)
**Orphan agents promoted to skills:** {count}
**Hooks absorbed into lifecycle-hooks:** {count} ({hook_count} events)
```

The "Origin" column shows "skill", "agent", or "hooks" — in full mode this always matches "Type", but in flatten mode it shows the original component type before conversion.

### Next Steps

Suggest:
1. Review the INTEGRATION-GUIDE.md for capability requirements
2. Start with the simplest skill to validate integration with the target harness
3. If external dependencies exist, note which plugin groups they come from
4. For components that used team orchestration (now decomposed to sequential/parallel steps), test the simplified workflow to ensure it meets needs
5. In flatten mode: review agent-converted skills to verify the reframing preserved the original intent
6. In nested mode: verify agent-to-parent mappings — ensure each agent is nested under the skill that logically spawns it. Review cross-skill references for accuracy
7. In unified layout: check renamed components (if any collisions occurred) and verify the unified dependency map captures all cross-group relationships
