---
name: language-shell
description: Shell scripting standards and safety practices. Use when language shell guidance is required or when selecting Shell as a thin wrapper or OS-near glue layer.
allowed-tools:
  - Bash(shellcheck)
---
## Key Execution Capabilities

### Script Validation

- Run syntax checking: `bash -n`, `sh -n`, `zsh -n`
- Execute static analysis with shellcheck
- Validate shebang lines and strict mode compliance
- Check for security vulnerabilities and coding violations

### Tool Integration

- Use `shellcheck` for comprehensive linting
- Leverage shell-specific parameter expansion features
- Apply POSIX vs bash vs zsh feature detection
- Implement platform-specific compatibility checks

### Execution Context

- Process script files from filesystem layer
- Generate structured reports with line-by-line findings
- Create minimal, rule-compliant patches for violations
- Maintain separation between governance rules and execution tools

## Error Handling

This skill provides execution-layer error handling for shell script analysis:
- Invalid file formats or permissions
- Tool availability issues (missing shellcheck, etc.)
- Platform-specific limitations
- Syntax validation failures

## Usage Notes

- Always delegate to governance rules for policy decisions
- Focus on concrete tool execution and result processing
- Provide deterministic, tool-first analysis results
- Maintain separation between rule definition and rule application
