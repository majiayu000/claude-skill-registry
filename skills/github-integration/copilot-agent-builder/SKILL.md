---
name: copilot-agent-builder
description: Generate custom GitHub Copilot agents (.agent.md files) for VS Code with proper YAML frontmatter, tools configuration, and handoff workflows. Use when "create copilot agent", "generate github copilot agent", "new copilot agent for", "make a copilot agent", or "build copilot agent".
allowed-tools: Read, Write, Glob, Bash, AskUserQuestion
---

# GitHub Copilot Agent Builder

Generate custom GitHub Copilot agents following VS Code's `.agent.md` format with proper YAML frontmatter and markdown instructions.

## When to Activate

Trigger this skill when user says:
- "create copilot agent"
- "generate github copilot agent"
- "new copilot agent for [purpose]"
- "make a copilot agent"
- "build copilot agent"
- "copilot custom agent"

## Agent Creation Process

### Step 1: Gather Requirements

Ask user for agent configuration:

1. **Agent Purpose & Name**:
   - What should the agent do? (e.g., "plan features", "review security", "write tests")
   - Suggested name: Extract from purpose (e.g., "planner", "security-reviewer", "test-writer")

2. **Tools Selection** (multi-select):
   - `fetch` - Retrieve web content and documentation
   - `search` - Search codebase and files
   - `githubRepo` - Access GitHub repository data
   - `usages` - Find code references and usage patterns
   - `files` - File operations
   - Custom tools if available

3. **Handoff Workflows** (optional):
   - Should this agent hand off to another? (e.g., planner → coder)
   - Handoff agent name
   - Handoff prompt text
   - Auto-send handoff? (yes/no)

4. **Additional Configuration** (optional):
   - Specific model to use?
   - Argument hint for users?

### Step 2: Validate Directory Structure

```bash
# Ensure .github/agents directory exists
mkdir -p .github/agents
```

### Step 3: Generate Agent File

Create `.github/agents/{agent-name}.agent.md` with:

**YAML Frontmatter Structure**:
```yaml
---
description: [Brief overview shown in chat input]
name: [Agent identifier, lowercase with hyphens]
tools: [Array of tool names]
handoffs:  # Optional
  - label: [Button text]
    agent: [Target agent name]
    prompt: [Handoff message]
    send: [true/false - auto-submit?]
model: [Optional - specific model name]
argument-hint: [Optional - user guidance text]
---
```

**Markdown Body**:
- Clear role definition
- Specific instructions
- Tool usage guidance (reference as `#tool:toolname`)
- Output format expectations
- Constraints and guidelines

### Step 4: Validate Format

Ensure generated file has:
- ✓ Valid YAML frontmatter with `---` delimiters
- ✓ All required fields (description, name)
- ✓ Tools array properly formatted
- ✓ Handoffs array if specified (with label, agent, prompt, send)
- ✓ Markdown instructions that are clear and actionable

### Step 5: Confirm Creation

Show user:
```markdown
✅ GitHub Copilot Agent Created

📁 Location: `.github/agents/{name}.agent.md`
🎯 Agent: {name}
📝 Description: {description}
🛠️  Tools: {tools list}

To use:
1. Reload VS Code window (Cmd/Ctrl + Shift + P → "Reload Window")
2. Open GitHub Copilot Chat
3. Type `@{name}` to invoke your custom agent

{If handoffs configured: "This agent can hand off to: {handoff targets}"}
```

## Output Format

After creation, provide:

1. **File path confirmation**
2. **Configuration summary** (name, description, tools, handoffs)
3. **Usage instructions** (how to reload and use)
4. **Next steps** (testing suggestions)

## Reference Documentation

- Templates and structures → `templates.md`
- Real-world examples → `examples.md`

## Important Guidelines

1. **Naming Convention**: Use lowercase with hyphens (e.g., `feature-planner`, `security-reviewer`)
2. **Description**: Brief (1-2 sentences), shown in chat input UI
3. **Tools**: Only include tools the agent actually needs
4. **Handoffs**: Enable multi-step workflows (planning → implementation → testing)
5. **Instructions**: Be specific about what the agent should and shouldn't do
6. **Tool References**: Use `#tool:toolname` syntax in markdown body

## Common Agent Patterns

**Planning Agent**:
- Tools: `fetch`, `search`, `githubRepo`, `usages`
- Handoff: To implementation agent
- Focus: Analysis and planning, no code edits

**Implementation Agent**:
- Tools: `search`, `files`, `usages`
- Handoff: To testing agent
- Focus: Write and modify code

**Review Agent**:
- Tools: `search`, `githubRepo`, `usages`
- Handoff: Back to implementation for fixes
- Focus: Quality, security, performance checks

**Testing Agent**:
- Tools: `search`, `files`
- Handoff: Back to implementation or to review
- Focus: Test creation and validation

---

**Ready to build custom GitHub Copilot agents!**
