---
name: claude-code
description: Activate when users ask about Claude Code installation, slash commands (/cook, /plan, /fix, /test, /docs, /design, /git), creating/managing Agent Skills, configuring MCP servers, setting up hooks/plugins, IDE integration (VS Code, JetBrains), CI/CD workflows, enterprise deployment (SSO, RBAC, sandboxing), troubleshooting authentication/performance issues, or advanced features (extended thinking, caching, checkpointing).
---

# Claude Code

Anthropic's agentic coding tool combining autonomous planning, execution, and validation with extensibility through skills, plugins, MCP servers, and hooks.

## Core Concepts

**Subagents**: Specialized agents (planner, code-reviewer, tester, debugger, docs-manager, ui-ux-designer, database-admin)

**Agent Skills**: Modular capabilities with SKILL.md + bundled resources (scripts, references, assets) loaded progressively

**Slash Commands**: User-defined operations in `.claude/commands/` expanding to prompts

**Hooks**: Event-driven shell commands (SessionStart, PreToolUse, PostToolUse, Stop, SubagentStop)

**MCP Servers**: Model Context Protocol integrations for external tools (GitHub, Jira, databases)

**Plugins**: Packaged collections distributed via marketplace

## Reference Guide

Load references as needed for specific topics:

| Topic | Reference File | Contents |
|-------|----------------|----------|
| Installation & setup | `references/getting-started.md` | Prerequisites, installation methods, authentication |
| Slash commands | `references/slash-commands.md` | Full catalog: /cook, /plan, /fix, /test, /docs, /git, /design |
| Workflow examples | `references/common-workflows.md` | Feature implementation, bug fixing, testing, git ops |
| Creating skills | `references/agent-skills.md` | Skill structure, metadata, bundled resources |
| MCP servers | `references/mcp-integration.md` | Configuration, common servers, authentication |
| Hooks system | `references/hooks-comprehensive.md` | Event types, command/prompt hooks, tool matchers |
| Plugins | `references/hooks-and-plugins.md` | Plugin structure, marketplace, installation |
| Configuration | `references/configuration.md` | Settings hierarchy, model config, output styles |
| Enterprise | `references/enterprise-features.md` | SSO, RBAC, sandboxing, audit logging, deployment |
| IDE integration | `references/ide-integration.md` | VS Code extension, JetBrains plugin |
| CI/CD | `references/cicd-integration.md` | GitHub Actions, GitLab workflows |
| Advanced features | `references/advanced-features.md` | Extended thinking, caching, checkpointing |
| Troubleshooting | `references/troubleshooting.md` | Auth failures, MCP issues, performance, debug mode |
| API reference | `references/api-reference.md` | Admin, Messages, Files, Models, Skills APIs |
| Best practices | `references/best-practices.md` | Project organization, security, performance, cost |

## Instructions

When answering questions:

1. Identify topic from user query
2. Load relevant reference files (use table above)
3. Provide specific guidance with examples
4. For complex queries, load multiple references

**Documentation sources:**
- Context7 llms.txt: `https://context7.com/websites/claude_en_claude-code/llms.txt?tokens=10000`
- Topic search: `https://context7.com/websites/claude_en_claude-code/llms.txt?topic=<topic>&tokens=5000`
- Official docs: https://docs.claude.com/en/docs/claude-code/
- GitHub: https://github.com/anthropics/claude-code
- Support: support.claude.com
