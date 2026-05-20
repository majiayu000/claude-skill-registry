---
name: syntax-tree
description: Print the Roslyn syntax tree for C# code. Use to discover which SyntaxNode types and properties to match in an analyzer.
user-invocable: true
allowed-tools: Bash, Read, Write
argument-hint: <C# code or path to .cs file>
hooks:
  Stop:
    - command: "bash .claude/hooks/log-skill-usage.sh syntax-tree"
---

# Print Syntax Tree

Arguments: `$ARGUMENTS`

1. If `$ARGUMENTS` is a path to an existing `.cs` file, run directly:
   ```
   dotnet run --project tools/SyntaxTreeViewer -- "$ARGUMENTS"
   ```

2. If `$ARGUMENTS` is inline C# code, pipe it via stdin:
   ```bash
   cat <<'CSHARP_EOF' | dotnet run --project tools/SyntaxTreeViewer -- --stdin
   $ARGUMENTS
   CSHARP_EOF
   ```

3. Return the formatted AST output.

## Constraints

- Do NOT interpret, analyze, or summarize the output — return the raw AST as-is
- Do NOT modify any project files
- Do NOT modify the SyntaxTreeViewer tool
