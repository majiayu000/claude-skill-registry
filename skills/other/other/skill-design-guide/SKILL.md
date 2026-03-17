---
name: skill-design-guide
description: Comprehensive guide for designing, building, testing, and distributing Claude skills. Use when user wants to "create a skill", "build a skill", "write a SKILL.md", "design a workflow skill", "make an MCP skill", or asks about skill structure, frontmatter, trigger phrases, or skill best practices. Walks through the full lifecycle from use case definition to distribution.
metadata:
  author: Ken Collins
  version: 1.0.0
  category: developer-tools
---

# Skill Design Guide

Interactive guide for building Claude skills from scratch. Walks users through
the full lifecycle: use case definition, folder structure, frontmatter,
instructions, design patterns, testing, iteration, and distribution.

## What Is a Skill

A skill is a folder containing instructions that teach Claude how to handle
specific tasks or workflows. Instead of re-explaining preferences and processes
every conversation, skills teach Claude once.

**Required file:** `SKILL.md` — main instructions in Markdown with YAML frontmatter.

**Optional directories:**

- `scripts/` — executable code (Python, Bash, etc.)
- `references/` — documentation loaded as needed
- `assets/` — templates, fonts, icons used in output

**Progressive disclosure (three levels):**

1. YAML frontmatter — always loaded in system prompt. Tells Claude when to use the skill.
2. SKILL.md body — loaded when Claude thinks the skill is relevant. Full instructions.
3. Linked files — scripts, references, assets. Loaded only as needed.

**Three skill categories:**

1. Document and Asset Creation — consistent output (docs, presentations, code, designs)
2. Workflow Automation — multi-step processes with consistent methodology
3. MCP Enhancement — workflow guidance on top of MCP tool access

## Instructions

Guide the user through each step interactively. Ask clarifying questions
before moving to the next step. Do not rush — quality of each step matters
more than speed through the workflow.

### Step 1: Define Use Cases

Ask the user for 2-3 concrete use cases the skill should enable.

For each use case, capture:

- **Trigger:** What the user would say (e.g., "help me plan this sprint")
- **Steps:** What the workflow involves
- **Tools:** Built-in Claude capabilities, MCP tools, or scripts needed
- **Result:** What success looks like

Example of a well-defined use case:

```
Use Case: Project Sprint Planning
Trigger: User says "help me plan this sprint" or "create sprint tasks"
Steps:
1. Fetch current project status from Linear (via MCP)
2. Analyze team capacity
3. Suggest task prioritization
4. Create tasks in Linear with proper labels and estimates
Result: Fully planned sprint with tasks created
```

Determine whether the skill is standalone or MCP-enhanced. Standalone skills
use Claude's built-in capabilities only. MCP-enhanced skills coordinate with
one or more MCP servers.

### Step 2: Set Up Folder Structure

Create the skill folder following these rules:

**Folder naming (kebab-case only):**

- `notion-project-setup` — correct
- `Notion Project Setup` — wrong (spaces, capitals)
- `notion_project_setup` — wrong (underscores)
- `NotionProjectSetup` — wrong (capitals)

**Inside the folder:**

- `SKILL.md` — required, exact casing (not SKILL.MD, skill.md, etc.)
- `scripts/` — if executable code is needed
- `references/` — if detailed documentation is needed
- `assets/` — if templates or static files are needed
- No `README.md` inside the skill folder (docs go in SKILL.md or references/)

### Step 3: Write YAML Frontmatter

The frontmatter is how Claude decides whether to load the skill. This is the
most important part to get right.

**Required format:**

```yaml
---
name: your-skill-name
description: What it does. Use when user asks to [specific phrases].
---
```

**Required fields:**

- `name` — kebab-case, no spaces or capitals, should match folder name
- `description` — must include WHAT the skill does AND WHEN to use it, under 1024 characters, no XML angle brackets

**Optional fields:**

- `license` — e.g., MIT, Apache-2.0
- `compatibility` — environment requirements (1-500 chars)
- `metadata` — custom key-value pairs (author, version, mcp-server, etc.)

**Security restrictions:**

- No XML angle brackets in frontmatter
- No "claude" or "anthropic" in the skill name (reserved)

Consult `references/yaml-frontmatter-reference.md` for the complete field reference.

### Step 4: Write the Description Field

The description determines whether the skill triggers correctly. Structure it as:

```
[What it does] + [When to use it] + [Key capabilities]
```

**Good descriptions:**

```yaml
# Specific and actionable
description: Analyzes Figma design files and generates developer handoff
  documentation. Use when user uploads .fig files, asks for "design specs",
  "component documentation", or "design-to-code handoff".

# Includes trigger phrases
description: Manages Linear project workflows including sprint planning,
  task creation, and status tracking. Use when user mentions "sprint",
  "Linear tasks", "project planning", or asks to "create tickets".

# Clear value proposition
description: End-to-end customer onboarding workflow for PayFlow. Handles
  account creation, payment setup, and subscription management. Use when
  user says "onboard new customer", "set up subscription", or "create
  PayFlow account".
```

**Bad descriptions:**

```yaml
# Too vague — won't trigger reliably
description: Helps with projects.

# Missing triggers — Claude won't know when to load it
description: Creates sophisticated multi-page documentation systems.

# Too technical, no user triggers
description: Implements the Project entity model with hierarchical relationships.
```

If there is risk of over-triggering, add negative triggers:

```yaml
description: Advanced data analysis for CSV files. Use for statistical
  modeling, regression, clustering. Do NOT use for simple data exploration
  (use data-viz skill instead).
```

### Step 5: Write Main Instructions

After the frontmatter, write the instructions in Markdown. Follow this structure:

```markdown
# Your Skill Name

## Instructions

### Step 1: [First Major Step]

Clear explanation of what happens.

Example:
python scripts/fetch_data.py --project-id PROJECT_ID
Expected output: [describe what success looks like]

(More steps as needed)

## Examples

### Example 1: [Common scenario]

User says: "Set up a new marketing campaign"
Actions:

1. Fetch existing campaigns via MCP
2. Create new campaign with provided parameters
   Result: Campaign created with confirmation link

## Troubleshooting

### Error: [Common error message]

Cause: [Why it happens]
Solution: [How to fix]
```

**Best practices:**

- Be specific and actionable — show exact commands, expected outputs
- Include error handling for common failures
- Reference bundled files clearly: "Consult `references/api-patterns.md` for rate limiting guidance"
- Use numbered lists and bullet points over prose
- Put critical instructions at the top with clear headers
- Keep SKILL.md under 5,000 words — move detailed docs to `references/`

**For critical validations**, consider bundling a script that performs checks
programmatically rather than relying on language instructions. Code is
deterministic; language interpretation is not.

### Step 6: Choose a Design Pattern

Help the user select the pattern that fits their use case:

1. **Sequential Workflow Orchestration** — multi-step processes in a specific order with dependencies between steps
2. **Multi-MCP Coordination** — workflows spanning multiple services (e.g., Figma to Drive to Linear to Slack)
3. **Iterative Refinement** — output quality improves with validation and iteration loops
4. **Context-Aware Tool Selection** — same outcome, different tools depending on context (file type, size, etc.)
5. **Domain-Specific Intelligence** — specialized knowledge beyond tool access (compliance, regulations, best practices)

Consult `references/design-patterns.md` for detailed examples and key techniques for each pattern.

### Step 7: Test the Skill

Guide the user through three testing areas:

**Triggering tests:**

- Does it load on obvious task requests?
- Does it load on paraphrased requests?
- Does it stay silent on unrelated topics?

Test queries that should trigger:

```
"Help me set up a new [Service] workspace"
"I need to create a project in [Service]"
"Initialize a [Service] project for Q4 planning"
```

Test queries that should NOT trigger:

```
"What's the weather?"
"Help me write Python code"
"Create a spreadsheet" (unless the skill handles sheets)
```

**Functional tests:**

- Valid outputs generated
- API/MCP calls succeed
- Error handling works
- Edge cases covered

**Performance comparison:**
Compare with and without the skill on the same task. Track: number of messages,
failed API calls, tokens consumed, and whether user corrections were needed.

**Debugging tip:** Ask Claude "When would you use the [skill-name] skill?"
Claude will quote the description back — adjust based on what's missing.

### Step 8: Iterate

Skills are living documents. Watch for these signals:

**Under-triggering** (skill doesn't load when it should):

- Add more trigger phrases and keywords to the description
- Include technical terms users might use
- Check if the description is too narrow

**Over-triggering** (skill loads for unrelated queries):

- Add negative triggers ("Do NOT use for...")
- Narrow the scope of the description
- Clarify specific file types or services

**Execution issues** (skill loads but results are inconsistent):

- Improve instruction specificity
- Add error handling
- Use scripts for deterministic checks instead of language instructions
- Put critical instructions at the top and repeat key points

**Pro tip:** Iterate on a single challenging task until Claude succeeds, then
extract the winning approach into the skill. This provides faster signal than
broad testing.

### Step 9: Distribute

**Claude.ai upload:**

1. Zip the skill folder
2. Settings then Capabilities then Skills then Upload
3. Toggle the skill on

**Claude Code:**
Place the skill folder in the Claude Code skills directory.

**Organization-level deployment:**
Admins can deploy skills workspace-wide with automatic updates and centralized management.

**GitHub (recommended for sharing):**

- Public repo with clear README (repo-level, separate from skill folder)
- Example usage and screenshots
- Link from MCP documentation if applicable

**API (programmatic use):**

- `/v1/skills` endpoint for listing and managing skills
- `container.skills` parameter in Messages API
- Works with Claude Agent SDK for custom agents

When writing about the skill, focus on outcomes not features:

```
Good: "Set up complete project workspaces in seconds instead of 30 minutes
of manual setup."

Bad: "A folder containing YAML frontmatter and Markdown instructions that
calls our MCP server tools."
```

## References

For detailed information beyond these instructions:

- `references/yaml-frontmatter-reference.md` — complete field reference with types, constraints, and annotated examples
- `references/design-patterns.md` — all 5 design patterns with full example structures and key techniques
- `references/troubleshooting.md` — common issues from upload errors to triggering problems to MCP failures
- `references/quality-checklist.md` — pre-upload and post-upload validation checklist
- `references/source/` — full original guide chapters (00 through 06) for authoritative deep reference
