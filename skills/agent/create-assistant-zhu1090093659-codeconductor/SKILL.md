---
name: create-assistant
description: Interactive assistant creator for CodeConductor. Use when users want to create a new custom assistant, design an AI persona, or configure a specialized helper. Triggers on: "create an assistant", "make a new helper", "design an AI that...", "I need an assistant for...", "帮我创建一个助手", "新建助手".
---

# Create Assistant

Guide users through creating custom assistants via interactive dialogue.

## CRITICAL: File Path Requirements

**STOP! Before creating ANY file, you MUST follow these steps:**

1. **NEVER create files in the current working directory or project folder**
2. **ALWAYS use the CodeConductor system config directory**

### Required Path

The assistant file MUST be created at:

```
C:\Users\{username}\AppData\Roaming\CodeConductor\CodeConductor\config\custom-assistants\{id}\{id}.md   (Windows)
~/Library/Application Support/CodeConductor/CodeConductor/config/custom-assistants/{id}/{id}.md       (macOS)
~/.config/CodeConductor/CodeConductor/config/custom-assistants/{id}/{id}.md                           (Linux)
```

### How to Get the Correct Path

**Step 1**: Call `ipcBridge.fs.getCustomAssistantsDir` first to get the exact path.

**Step 2**: The result will be something like:

- Windows: `C:\Users\zcl\AppData\Roaming\CodeConductor\CodeConductor\config\custom-assistants`
- macOS: `/Users/xxx/Library/Application Support/CodeConductor/CodeConductor/config/custom-assistants`

**Step 3**: Create files inside that directory:

- Directory: `{result}/{assistant-id}/`
- File: `{result}/{assistant-id}/{assistant-id}.md`

### WRONG Examples (DO NOT DO THIS)

```
❌ D:\work\dp2\assistant\xiaohongshu\xiaohongshu.md
❌ ./assistant/my-helper/my-helper.md
❌ ~/.claude/skills/assistant/...
❌ {current-project}/assistant/...
```

### CORRECT Examples

```
✓ C:\Users\zcl\AppData\Roaming\CodeConductor\CodeConductor\config\custom-assistants\xiaohongshu\xiaohongshu.md
✓ ~/Library/Application Support/CodeConductor/CodeConductor/config/custom-assistants/my-helper/my-helper.md
```

---

## Important: Inherited Capabilities

**Custom assistants automatically inherit ALL capabilities from the main agent:**

- All installed **MCP tools** (file operations, web search, browser automation, etc.)
- All enabled **Skills** (pdf, docx, pptx, algorithmic-art, frontend-design, etc.)
- All **system tools** (Read, Write, Bash, Grep, Glob, etc.)

**DO NOT recreate existing functionality in the assistant's rule file.** The rule file should ONLY define:

- The assistant's **persona and role** (who it is)
- **Behavioral guidelines** (how it should respond)
- **Domain-specific constraints** (what it should focus on or avoid)

---

## Workflow

### Step 1: Get the Custom Assistants Directory (MANDATORY FIRST STEP)

**Before doing anything else**, call `ipcBridge.fs.getCustomAssistantsDir` to get the absolute path where the assistant must be created.

### Step 2: Understand User Intent

Ask the user to describe the assistant they want:

- Primary purpose
- Target use cases
- Personality traits

### Step 3: Collect Configuration via ask_user_question

Use the `mcp__popup-mcp__ask_user_question` tool to gather:

- Name (2-20 characters)
- Avatar (single emoji)
- Description (one sentence)
- Agent Type: claude | codex

### Step 4: Generate Rule File

1. Convert name to kebab-case ID (e.g., "小红书助手" → "xiaohongshu-assistant")
2. Create directory: `{custom-assistants-dir}/{id}/`
3. Write rule file: `{custom-assistants-dir}/{id}/{id}.md`

**Rule file structure:**

```markdown
# {Name}

You are {name}, an assistant specialized in {purpose}.

## Mission

- {Primary goal}
- {Secondary goals}

## Operating Rules

- {Behavioral guideline 1}
- {Behavioral guideline 2}
- Use existing skills like `pdf`, `docx` when processing documents
- Leverage MCP tools for file operations and web searches

## Constraints

- {Domain constraint}
- {What to avoid}
```

### Step 5: Notify User

Tell user:

1. Assistant created successfully
2. Show the **exact absolute path** of the created file
3. Remind them the assistant inherits all existing skills and MCP tools
4. Suggest restarting CodeConductor to load the new assistant

---

## ask_user_question Examples

```json
{
  "topic": "Assistant Configuration",
  "questions": [
    {
      "question": "What type of assistant do you want to create?",
      "header": "Type",
      "multiSelect": false,
      "options": [
        { "label": "Coding Helper", "description": "Programming, code review, debugging" },
        { "label": "Document Processor", "description": "PDF, DOCX, format conversion" },
        { "label": "Domain Expert", "description": "Specialized knowledge in a field" },
        { "label": "Task Automation", "description": "Multi-step workflow execution" }
      ]
    }
  ]
}
```

---

## Post-Creation Message Template

```
Assistant "{name}" created successfully!

File created:
- {absolute-path-from-getCustomAssistantsDir}/{id}/{id}.md

Inherited Capabilities:
- All MCP tools (file operations, web search, etc.)
- All enabled skills (pdf, docx, frontend-design, etc.)
- All system tools (Read, Write, Bash, etc.)

Next steps:
1. Restart CodeConductor or refresh the assistants list
2. Go to Settings > Assistants to enable your new assistant
3. Start a new conversation and select "{name}" to test it
```
