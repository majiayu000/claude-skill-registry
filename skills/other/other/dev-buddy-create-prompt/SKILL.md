---
name: dev-buddy-create-prompt
description: Create a custom system prompt for dev-buddy executors. Guides user through defining name, description, tools, and prompt content. Saves to ~/.vcp/system-prompts/.
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep, AskUserQuestion
---

# Create Custom System Prompt

Guide the user to create a custom system prompt that can be used in dev-buddy executors.

**Custom prompts directory:** `~/.vcp/system-prompts/`
**Built-in prompts:** `${CLAUDE_PLUGIN_ROOT}/system-prompts/built-in/`

---

## Step 1: Show Existing Prompts

List all available system prompts so the user knows what exists:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/system-prompts.ts" discover
```

Present the list to the user: "Here are the current system prompts (built-in + custom). Which type of prompt would you like to create?"

---

## Step 2: Gather Information

Ask the user via AskUserQuestion:

1. **What kind of prompt?** — Options: reviewer, planner, analyst, implementer, custom
2. **Name** — must be unique, lowercase-with-hyphens (e.g., `perf-reviewer`, `security-analyst`)
3. **Description** — one-line summary of what this prompt does
4. **Purpose** — what specific task/focus area should this prompt excel at?

If the user chose a category (not "custom"), offer to show a relevant built-in prompt as a starting template:
- reviewer → show `code-reviewer.md` or `plan-reviewer.md`
- planner → show `planner.md`
- analyst → show `root-cause-analyst.md`
- implementer → show `implementer.md`

---

## Step 3: Tools (Role-Only Prompts)

**Custom system prompts are role/perspective definitions only.** Stage rules (output format, process, completion requirements) and tool permissions are provided automatically by stage definitions at dispatch time. Custom prompts should NOT include tools, output format, or completion requirements.

Leave `tools` empty in the frontmatter — the stage definition provides the tool list at runtime.

---

## Step 4: Help Write the System Prompt Content

Based on the user's purpose, help them write the system prompt body. Role prompts define the **perspective and expertise** the agent brings — NOT the output format or process (those come from stage definitions).

Include:

1. **Role definition** — "You are a [role] with expertise in [area]."
2. **Core competencies** — 3-5 bullet points of what this agent excels at

Do NOT include output format, process/workflow, or completion requirements — those are provided by the stage definition at dispatch time.

Present the draft to the user for review. Iterate if they want changes.

---

## Step 5: Validate Name

Check the name doesn't collide with built-in prompts:

```bash
bun -e "
import { discoverSystemPrompts } from '${CLAUDE_PLUGIN_ROOT}/scripts/system-prompts.ts';
const builtInDir = '${CLAUDE_PLUGIN_ROOT}/system-prompts/built-in';
const prompts = discoverSystemPrompts(builtInDir);
const name = '{USER_CHOSEN_NAME}';
const collision = prompts.find(p => p.name === name);
console.log(JSON.stringify({ collision: !!collision, source: collision?.source }));
"
```

If collision detected, tell the user and ask for a different name.

---

## Step 6: Write the File

Assemble the complete file with YAML frontmatter and write it:

```markdown
---
name: {name}
description: {description}
tools: {comma-separated tools}
model: inherit
---

{system prompt content}
```

Write to `~/.vcp/system-prompts/{name}.md` using the Write tool:
```
Write(file_path: "~/.vcp/system-prompts/{name}.md", content: "{assembled content}")
```

Ensure the `~/.vcp/system-prompts/` directory exists first:
```bash
mkdir -p ~/.vcp/system-prompts
```

---

## Step 7: Verify

Verify the prompt was created successfully:

```bash
bun "${CLAUDE_PLUGIN_ROOT}/scripts/system-prompts.ts" list
```

The new prompt should appear under "custom". Tell the user:

"Custom prompt '{name}' created successfully! To use it:
1. Go to `/dev-buddy-config` → Executors tab
2. Create a new executor with system_prompt: '{name}'
3. Assign the executor to a stage in the Stages tab"

---

## Anti-Patterns

- Do NOT create prompts with names that match built-in prompts
- Do NOT write to the built-in prompts directory (`system-prompts/built-in/`)
- Do NOT skip the validation step — always check for name collisions
- Do NOT create overly generic prompts — each prompt should have a clear, focused purpose
