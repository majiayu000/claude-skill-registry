---
name: libprompt
description: >
  libprompt - Prompt template management with Mustache. PromptLoader loads
  .prompt.md files from directories and renders them with variable substitution.
  Use for managing LLM system prompts, creating reusable prompt templates, and
  dynamic prompt generation.
---

# libprompt Skill

## When to Use

- Managing LLM system prompts as templates
- Loading prompt files from directories
- Rendering prompts with dynamic variables
- Organizing prompts for different agents

## Key Concepts

**PromptLoader**: Loads .prompt.md files from a directory and renders them using
Mustache templating syntax.

**Mustache templating**: Use `{{variable}}` syntax for dynamic content
insertion.

## Usage Patterns

### Pattern 1: Load and render prompt

```javascript
import { PromptLoader } from "@copilot-ld/libprompt";

const loader = new PromptLoader("./prompts");
const systemPrompt = await loader.render("system", {
  agentName: "Assistant",
  capabilities: ["search", "calculate"],
});
```

### Pattern 2: Prompt file structure

```markdown
<!-- prompts/system.prompt.md -->

You are {{agentName}}.

Your capabilities: {{#capabilities}}

- {{.}} {{/capabilities}}
```

## Integration

Used by Memory service to load agent system prompts. Prompts stored in
config/agents/\*/prompts/.
