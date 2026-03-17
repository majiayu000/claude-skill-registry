# MCP Server Integration (80/20 Edition)

**Auto-trigger**: MCP, GitHub operations, filesystem access, external integrations

## Overview

Model Context Protocol connects LLMs to external tools:
- **GitHub**: Issues, PRs, repositories
- **Filesystem**: Enhanced file operations
- **Custom**: SPARQL, validation, domain-specific

## Configuration

```json
{
  "mcpServers": {
    "github": {
      "command": "mcp-server-github",
      "env": {"GITHUB_TOKEN": "${GITHUB_TOKEN}"}
    },
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["/home/user/ggen"]
    }
  }
}
```

## GitHub Operations

### Create Issue
```json
{"tool": "github_create_issue", "arguments": {
  "title": "feat: Add feature X",
  "body": "## Summary\n- Requirement 1\n- Requirement 2",
  "labels": ["enhancement"]
}}
```

### Create PR
```json
{"tool": "github_create_pull_request", "arguments": {
  "title": "feat: Implement X",
  "body": "## Summary\n- Added X\n\n## Receipts\n[Receipt] cargo make test: ✓",
  "head": "claude/feature-branch",
  "base": "main"
}}
```

## Core Principles

### 1. Receipt Collection
```bash
✅ [Receipt] PR #123 created: https://github.com/org/repo/pull/123
✅ [Receipt] File written: path.rs (sha256:abc...)
❌ "I created a PR"  # No evidence
```

### 2. Path Validation
```rust
// Always validate before MCP filesystem calls
if !path.starts_with(allowed_base) { return Err(PathNotAllowed); }
```

### 3. Timeout & Rate Limiting
```rust
timeout(Duration::from_secs(5), mcp_call(tool, args)).await?
```

## Integration with EPIC 9

```
Spec closure → Fan-out 10 agents → Each uses MCP for validation
→ Collision detection → Convergence → PR via GitHub MCP
```

## Security

1. **Never hardcode tokens** - use `${ENV_VAR}`
2. **Validate all paths** - prevent traversal
3. **Rate limit** - prevent API abuse
4. **Timeout all calls** - default 5s

## Common Workflows

### Create Feature with MCP
```bash
/speckit-verify specs/042-feature
/bb80-parallel "[spec]"
mcp_call github_create_pull_request --title "feat: X" --body "$(cat receipts.md)"
```

### Audit Repository
```bash
mcp_call github_search_code --query "unwrap language:rust path:src"
# Receipt: ✅ 0 violations in production
```

## Best Practices

1. **Validate inputs** before MCP calls
2. **Collect receipts** for all operations
3. **Use spec-first** (RDF → ggen sync → MCP)
4. **Apply timeouts** (5s default)
5. **Never hardcode** secrets

**Constitutional**: `MCP = Validated inputs + Receipts + Timeouts + Spec-first`
