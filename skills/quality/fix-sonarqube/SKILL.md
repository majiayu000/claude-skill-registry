---
name: fix-sonarqube
description: >
  SonarQube integration via MCP for Java projects. The MCP server runs remotely
  and requires no local setup. Use natural language to query issues, analyze code,
  and check quality gates.
compatibility: All Java projects with SonarQube analysis
metadata:
  version: "2.0.0"
  technology: java
  category: quality
  tags:
    - java
    - sonarqube
    - mcp
    - code-quality
---

# Fix SonarQube

SonarQube integration via MCP (Model Context Protocol) for Java code quality analysis.

## When to use this skill

- Finding and fixing SonarQube issues
- Checking quality gate status
- Analyzing code for quality issues
- Understanding SonarQube rules
- Prioritizing issue remediation
- When asked to "fix sonarqube issues" or "add sonarqube mcp"

## Skill Contents

### Sections

- [When to use this skill](#when-to-use-this-skill) (L23-L31)
- [Quick Start](#quick-start) (L55-L67)
- [MCP Tools Available](#mcp-tools-available) (L68-L78)
- [Common Workflows](#common-workflows) (L79-L102)
- [Supported IDEs](#supported-ides) (L103-L116)
- [References](#references) (L117-L123)
- [Related Rules](#related-rules) (L124-L129)
- [Related Skills](#related-skills) (L130-L135)

### Available Resources

**📚 references/** - Detailed documentation
- [common rules](references/common-rules.md)
- [copilot cli setup](references/copilot-cli-setup.md)
- [intellij setup](references/intellij-setup.md)
- [mcp tools](references/mcp-tools.md)

---

## Quick Start

The SonarQube MCP server runs remotely at `https://sonarqube-mcp.bitso.io/mcp` and is automatically configured in all supported IDEs.

**No setup required** - just use natural language:

```text
"Find HIGH severity issues in my-project"
"Show me details about rule java:S1128"
"What's the quality gate status for my-service?"
"Analyze this code for SonarQube issues"
```

## MCP Tools Available

| Tool | Purpose |
|------|---------|
| `list_projects` | List all SonarQube projects |
| `get_issues` | Get issues for a project |
| `get_issue_details` | Get details for a specific issue |
| `get_rule` | Get rule documentation |
| `get_quality_gate` | Check quality gate status |
| `analyze_code` | Analyze code snippet |

## Common Workflows

### 1. Fix Issues by Severity

```text
"Find all BLOCKER issues in payment-service"
"Get details for issue AYx123..."
"Show me the rule java:S2259"
```

### 2. Check Quality Gate

```text
"What's the quality gate status for my-service?"
"List all projects I have access to"
```

### 3. Understand Rules

```text
"Explain rule java:S1128 (unused imports)"
"What are the CRITICAL rules for Java?"
```

## Supported IDEs

The MCP is automatically available in:

| IDE | Configuration |
|-----|---------------|
| **Cursor** | `.cursor/mcp.json` |
| **VS Code + Copilot** | `.vscode/mcp.json` |
| **Claude Code** | `.mcp.json` |
| **IntelliJ IDEA** | See manual setup |
| **Copilot CLI** | See manual setup |

For IntelliJ and Copilot CLI, see: `java/commands/add-sonarqube-mcp-to-intellij-and-copilot-cli.md`

## References

| Reference | Description |
|-----------|-------------|
| [references/mcp-tools.md](references/mcp-tools.md) | Full MCP tool reference |
| [references/common-rules.md](references/common-rules.md) | Common Java rules |

## Related Rules

- [java-sonarqube-setup](.cursor/rules/java-sonarqube-setup/java-sonarqube-setup.mdc) - Setup guide
- [java-sonarqube-mcp](.cursor/rules/java-sonarqube-mcp/java-sonarqube-mcp.mdc) - MCP tool reference
- [fix-sonarqube-issues](.cursor/commands/fix-sonarqube-issues.md) - Fix command

## Related Skills

| Skill | Purpose |
|-------|---------|
| [java-coverage](.claude/skills/java-coverage/SKILL.md) | JaCoCo coverage for SonarQube |
| [gradle-standards](.claude/skills/gradle-standards/SKILL.md) | SonarQube Gradle plugin |
<!-- AUTO-GENERATED FILE - DO NOT EDIT DIRECTLY -->
<!-- Source: bitsoex/ai-code-instructions → java/skills/fix-sonarqube/SKILL.md -->
<!-- To modify, edit the source file and run the distribution workflow -->

