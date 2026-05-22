---
name: agent-sdk-definitions
description: Programmatic agent definitions for the Claude Agent SDK in TypeScript and Python. Use when creating agents for SDK-based applications rather than filesystem-based Claude Code.
---

# Agent SDK Definitions

For SDK-based applications, agents can be defined programmatically instead of as markdown files.

## TypeScript Definition

```typescript
import { query, ClaudeAgentOptions, AgentDefinition } from "@anthropic-ai/claude-agent-sdk";

const options: ClaudeAgentOptions = {
  // Parent agent needs Task tool to invoke subagents
  allowed_tools: ["Read", "Grep", "Glob", "Edit", "Write", "Bash", "Task"],

  agents: {
    "code-reviewer": {
      description: "Security-focused code reviewer. Use PROACTIVELY for auth code.",
      prompt: `You are a security code reviewer specializing in authentication
and authorization code. You identify vulnerabilities, suggest fixes,
and ensure best practices are followed.

## Focus Areas
- Authentication flows
- Session management
- Input validation
- Access control

## Output Format
Provide findings as:
1. Severity (Critical/High/Medium/Low)
2. Location (file:line)
3. Issue description
4. Recommended fix`,
      tools: ["Read", "Grep", "Glob"],  // Read-only access
      model: "opus"
    },

    "test-runner": {
      description: "Runs tests and analyzes failures. Use when tests need to be executed.",
      prompt: `You run test suites and analyze failures. You identify root causes
and suggest fixes for failing tests.`,
      // Omit tools to inherit all from parent
      model: "sonnet"
    }
  }
};

// Execute with agents
for await (const message of query({
  prompt: "Review the authentication module for security issues",
  options
})) {
  console.log(message);
}
```

## Python Definition

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Grep", "Glob", "Edit", "Write", "Bash", "Task"],

    agents={
        "code-reviewer": AgentDefinition(
            description="Security-focused code reviewer. Use PROACTIVELY for auth code.",
            prompt="""You are a security code reviewer specializing in authentication
and authorization code. You identify vulnerabilities, suggest fixes,
and ensure best practices are followed.

## Focus Areas
- Authentication flows
- Session management
- Input validation
- Access control""",
            tools=["Read", "Grep", "Glob"],
            model="opus"
        ),

        "test-runner": AgentDefinition(
            description="Runs tests and analyzes failures. Use when tests need to be executed.",
            prompt="You run test suites and analyze failures.",
            # tools omitted = inherit all
            model="sonnet"
        )
    }
)

async def main():
    async for message in query(
        prompt="Review the authentication module",
        options=options
    ):
        print(message)

asyncio.run(main())
```

## AgentDefinition Schema

```typescript
type AgentDefinition = {
  description: string;   // Required: When to invoke (routing key)
  prompt: string;        // Required: System prompt content
  tools?: string[];      // Optional: Allowed tools (omit = inherit all)
  model?: 'sonnet' | 'opus' | 'haiku' | 'inherit';  // Optional: Model override
}
```

## Key Differences from Filesystem Agents

| Aspect | Filesystem (.claude/agents/) | SDK (programmatic) |
|--------|------------------------------|-------------------|
| Format | Markdown with YAML frontmatter | TypeScript/Python objects |
| Loading | Automatic from directory | Passed in options |
| Prompt | Markdown body | String in `prompt` field |
| Use case | Claude Code CLI | Custom SDK applications |

## When to Use SDK Format

- Building custom agent harnesses
- Programmatic agent orchestration
- Dynamic agent creation at runtime
- CI/CD pipelines with agent tasks
- Applications embedding Claude agents

## Providing Both Formats

When a user may use either approach, provide both:

1. **Markdown file** for `.claude/agents/{name}.md`
2. **SDK definition** for programmatic use

This ensures compatibility with both Claude Code CLI and custom SDK applications.
