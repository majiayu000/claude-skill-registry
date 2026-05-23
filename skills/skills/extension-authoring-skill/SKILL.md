---
name: "extension-authoring"
description: "Comprehensive guide for authoring Claude Code extensions including skills (SKILL.md), hooks, slash commands, and subagents. Use when: creating skills, writing hooks, making slash commands, building subagents, learning Claude Code extensions."
---

<objective>
This skill is the definitive guide for authoring Claude Code extensions. It covers four extension types:

1. **Skills** - Modular capabilities in SKILL.md files that provide domain expertise
2. **Hooks** - Event-driven automation that executes on tool use and session events
3. **Slash Commands** - Reusable prompts triggered with `/command-name` syntax
4. **Subagents** - Specialized Claude instances for delegated tasks

All four extension types share core principles: pure XML structure, YAML frontmatter, and clear success criteria. This skill teaches you to create effective extensions following best practices.
</objective>

<intake>
What would you like to create or learn about?

1. **Skill** - SKILL.md file for domain expertise
2. **Hook** - Event-driven automation (PreToolUse, PostToolUse, Stop, etc.)
3. **Slash Command** - Reusable prompt with `/command-name`
4. **Subagent** - Specialized agent for delegated tasks
5. **Guidance** - Help deciding which extension type to use

**Respond with a number or describe what you want to build.**
</intake>

<routing>
| Response | Action |
|----------|--------|
| 1, "skill", "SKILL.md" | Read [reference/skills.md](reference/skills.md) |
| 2, "hook", "hooks" | Read [reference/hooks.md](reference/hooks.md) |
| 3, "command", "slash" | Read [reference/commands.md](reference/commands.md) |
| 4, "subagent", "agent" | Read [reference/subagents.md](reference/subagents.md) |
| 5, "guidance", "help" | Use decision tree below |

**After reading the reference, follow its workflow exactly.**
</routing>

<decision_tree>
**Which extension type should I use?**

```
Is it triggered by specific Claude Code events?
  (tool use, session start/end, user prompt submit)
    YES --> Hook

Is it a reusable prompt the user invokes with /command-name?
    YES --> Slash Command

Is it an isolated task that runs autonomously without user interaction?
    YES --> Subagent

Is it domain knowledge or workflow guidance Claude loads on demand?
    YES --> Skill
```

**Quick decision matrix:**

| Need | Extension Type |
|------|---------------|
| Validate commands before execution | Hook (PreToolUse) |
| Auto-format code after edits | Hook (PostToolUse) |
| Desktop notification when input needed | Hook (Notification) |
| Reusable git commit workflow | Slash Command |
| Code review checklist | Slash Command |
| Delegated research task | Subagent |
| Autonomous test writing | Subagent |
| API integration knowledge | Skill |
| Multi-step workflow guidance | Skill |
</decision_tree>

<shared_principles>
These principles apply to ALL Claude Code extension types:

<xml_structure>
**Use pure XML structure. Remove ALL markdown headings from body content.**

```xml
<objective>What it does</objective>
<workflow>How to do it</workflow>
<success_criteria>How to know it worked</success_criteria>
```

Keep markdown formatting WITHIN content (bold, lists, code blocks).

**Why XML?**
- Semantic meaning for Claude (not just visual formatting)
- Unambiguous section boundaries
- Token efficient (~15 tokens vs ~20 for markdown headings)
- Reliable parsing and progressive disclosure
</xml_structure>

<yaml_frontmatter>
All extensions require YAML frontmatter:

```yaml
---
name: extension-name       # lowercase-with-hyphens
description: What it does and when to use it (third person)
---
```

**Name conventions:** `create-*`, `manage-*`, `setup-*`, `generate-*`

**Description rules:**
- Third person (never "I" or "you")
- Include WHAT it does AND WHEN to use it
- Maximum 1024 characters
</yaml_frontmatter>

<conciseness>
Context window is shared. Only add what Claude doesn't already know.

- Assume Claude is smart
- Challenge every piece of content: "Does this justify its token cost?"
- Provide default approach with escape hatch, not a list of options
- Keep main files under 500 lines, split to reference files
</conciseness>

<success_criteria>
Every extension should define clear completion criteria:

```xml
<success_criteria>
- Specific measurable outcome 1
- Specific measurable outcome 2
- How to verify it worked
</success_criteria>
```
</success_criteria>
</shared_principles>

<quick_reference>
**File locations:**

| Extension | Project Location | User Location |
|-----------|-----------------|---------------|
| Skill | `.claude/skills/` | `~/.claude/skills/` |
| Hook | `.claude/hooks.json` | `~/.claude/hooks.json` |
| Slash Command | `.claude/commands/` | `~/.claude/commands/` |
| Subagent | `.claude/agents/` | `~/.claude/agents/` |

**Minimal examples:**

<skill_example>
```markdown
---
name: process-pdfs
description: Extract text from PDF files. Use when working with PDFs.
---

<objective>Extract text from PDF files using pdfplumber.</objective>

<quick_start>
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
</quick_start>

<success_criteria>Text extracted without errors.</success_criteria>
```
</skill_example>

<hook_example>
```json
{
  "hooks": {
    "Notification": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "osascript -e 'display notification \"Claude needs input\" with title \"Claude Code\"'"
          }
        ]
      }
    ]
  }
}
```
</hook_example>

<command_example>
```markdown
---
description: Create a git commit
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

<objective>Create a git commit for current changes.</objective>

<context>
Current status: ! `git status`
Changes: ! `git diff HEAD`
</context>

<process>
1. Review changes
2. Stage relevant files
3. Create commit following repository conventions
</process>

<success_criteria>Commit created successfully.</success_criteria>
```
</command_example>

<subagent_example>
```markdown
---
name: code-reviewer
description: Reviews code for quality and security. Use after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
---

<role>
You are a senior code reviewer focused on quality and security.
</role>

<workflow>
1. Read modified files
2. Identify issues
3. Provide specific feedback with file:line references
</workflow>

<constraints>
- NEVER modify code, only review
- ALWAYS provide actionable feedback
</constraints>
```
</subagent_example>
</quick_reference>

<reference_index>
**Detailed guides:**

| Reference | Content |
|-----------|---------|
| [reference/skills.md](reference/skills.md) | SKILL.md structure, router pattern, progressive disclosure |
| [reference/hooks.md](reference/hooks.md) | Hook types, matchers, input/output schemas, examples |
| [reference/commands.md](reference/commands.md) | Slash command YAML, arguments, dynamic context |
| [reference/subagents.md](reference/subagents.md) | Agent configuration, execution model, orchestration |
</reference_index>

<anti_patterns>
**Common mistakes across all extension types:**

<pitfall name="markdown_headings">
```markdown
## Bad - Using markdown headings
```

```xml
<good>Using XML tags instead</good>
```
</pitfall>

<pitfall name="vague_descriptions">
```yaml
description: Helps with stuff  # Bad
description: Extract text from PDF files. Use when processing documents.  # Good
```
</pitfall>

<pitfall name="first_person">
```yaml
description: I help you process files  # Bad - first person
description: Processes files for analysis  # Good - third person
```
</pitfall>

<pitfall name="too_many_options">
Provide ONE default approach with escape hatch, not a menu of alternatives.
</pitfall>
</anti_patterns>

<success_criteria>
A well-authored Claude Code extension has:

- Valid YAML frontmatter with descriptive name and description
- Pure XML structure (no markdown headings in body)
- Clear objective/purpose statement
- Defined success criteria or completion verification
- Appropriate level of detail (not over-engineered)
- Real-world testing and iteration
- Documentation in third person
</success_criteria>
