---
name: mcp-cli-scripts
description: |
  Build CLI scripts alongside MCP servers for terminal environments. File I/O, batch processing, caching, richer output formats. Templates for TypeScript scripts and SCRIPTS.md.

  Use when: MCP companion scripts, batch processing, saving results to files, CLI API wrappers. Troubleshoot: context too large, no file access, batch input.
user-invocable: true
---

# MCP CLI Scripts Pattern

**Status**: Production Ready
**Last Updated**: 2026-01-09
**Dependencies**: tsx (dev dependency)
**Current Versions**: tsx@4.21.0

---

## Why CLI Scripts Alongside MCP Servers?

When building MCP servers, also create companion CLI scripts that provide the same (and often extended) functionality for use with Claude Code in terminal environments.

| Aspect | Remote MCP (Claude.ai) | CLI Scripts (Claude Code) |
|--------|------------------------|---------------------------|
| Context | Results flow through model context window | Results stay local, only relevant parts shared |
| File System | No access | Full read/write access |
| Batch Operations | One call at a time | Can process files of inputs |
| Caching | Stateless | Can cache results locally |
| Output | JSON to model | JSON, CSV, table, file, or stdout |
| Chaining | Model orchestrates | Scripts can pipe/chain directly |

---

## Directory Structure

```
mcp-{name}/
├── src/
│   └── index.ts              # MCP server (for Claude.ai, remote clients)
├── scripts/
│   ├── {tool-name}.ts        # One script per tool
│   ├── {another-tool}.ts
│   └── _shared.ts            # Shared auth/config helpers (optional)
├── SCRIPTS.md                # Documents available scripts for Claude Code
├── package.json
└── README.md
```

---

## The 5 Design Principles

### 1. One Script Per Tool

Each script does one thing well, matching an MCP tool but with extended capabilities.

### 2. JSON Output by Default

Scripts output JSON to stdout for easy parsing. Claude Code can read and use the results.

```typescript
// Good - structured output
console.log(JSON.stringify({ success: true, data: result }, null, 2));

// Avoid - unstructured text (unless --format text requested)
console.log("Found 5 results:");
```

### 3. Extended Capabilities for Local Use

CLI scripts can offer features that don't make sense for remote MCP:

```typescript
// Input/Output files
--input data.csv          // Batch process from file
--output results.json     // Save results to file
--append                  // Append to existing file

// Caching
--cache                   // Use local cache
--cache-ttl 3600          // Cache for 1 hour
--no-cache                // Force fresh request

// Output formats
--format json|csv|table   // Different output formats
--quiet                   // Suppress non-essential output
--verbose                 // Extra debugging info

// Batch operations
--batch                   // Process multiple items
--concurrency 5           // Parallel processing limit
```

### 4. Consistent Argument Patterns

Use consistent patterns across all scripts:

```bash
# Standard patterns
--input <file>            # Read input from file
--output <file>           # Write output to file
--format <type>           # Output format
--profile <name>          # Auth profile (for multi-account)
--verbose                 # Debug output
--help                    # Show usage
```

### 5. Shebang and Direct Execution

Scripts should be directly executable:

```typescript
#!/usr/bin/env npx tsx
/**
 * Brief description of what this script does
 *
 * Usage:
 *   npx tsx scripts/tool-name.ts <required-arg>
 *   npx tsx scripts/tool-name.ts --option value
 *
 * Examples:
 *   npx tsx scripts/tool-name.ts 12345
 *   npx tsx scripts/tool-name.ts --input batch.csv --output results.json
 */
```

---

## Critical Rules

### Always Do

✅ Use `#!/usr/bin/env npx tsx` shebang (not node or ts-node)
✅ Output JSON to stdout by default
✅ Use consistent argument patterns across all scripts
✅ Document scripts in SCRIPTS.md
✅ Handle errors with structured JSON: `{ success: false, error: "..." }`

### Never Do

❌ Use `console.log()` for prose output (use structured JSON)
❌ Use different argument patterns per script
❌ Forget to document the script in SCRIPTS.md
❌ Use `node` or `ts-node` in shebang (tsx handles ESM+TypeScript)

---

## When to Use Scripts vs MCP

**Use CLI scripts when:**
- Working in terminal/Claude Code environment
- Need to save results to files
- Processing batch inputs from files
- Chaining multiple operations
- Need caching for repeated lookups
- Want richer output formats

**Use MCP tools when:**
- In Claude.ai web interface
- Simple one-off lookups
- No file I/O needed
- Building conversational flows

---

## Shared Code Between MCP and Scripts

If you want to share logic between MCP and scripts, extract to a core module:

```
src/
├── core/
│   ├── lookup.ts         # Pure function, no I/O assumptions
│   └── index.ts          # Export all core functions
├── mcp/
│   └── index.ts          # MCP handlers, import from core
└── cli/
    └── lookup.ts         # CLI wrapper, import from core
```

However, keeping them separate is also fine - the scripts may evolve to have capabilities the MCP can't support, and that's okay.

---

## Using Bundled Resources

### Templates (templates/)

**script-template.ts**: Complete TypeScript script template with argument parsing, JSON output, and file I/O patterns.

```bash
# Copy to your project
cp ~/.claude/skills/mcp-cli-scripts/templates/script-template.ts scripts/new-tool.ts
```

**SCRIPTS-TEMPLATE.md**: Template for documenting available scripts in an MCP server repo.

```bash
# Copy to your project
cp ~/.claude/skills/mcp-cli-scripts/templates/SCRIPTS-TEMPLATE.md SCRIPTS.md
```

### Rules (rules/)

**mcp-cli-scripts.md**: Correction rules for script files. Copy to `.claude/rules/` in projects:

```bash
cp ~/.claude/skills/mcp-cli-scripts/rules/mcp-cli-scripts.md .claude/rules/
```

---

## Dependencies

**Required**:
- tsx@4.21.0 - TypeScript execution without compilation

Add to package.json:
```json
{
  "devDependencies": {
    "tsx": "^4.21.0"
  }
}
```

---

## Official Documentation

- **tsx**: https://github.com/privatenumber/tsx
- **Node.js CLI**: https://nodejs.org/api/cli.html

---

## Package Versions (Verified 2026-01-09)

```json
{
  "devDependencies": {
    "tsx": "^4.21.0"
  }
}
```

---

## Complete Setup Checklist

- [ ] Create `scripts/` directory in MCP server project
- [ ] Add tsx to devDependencies
- [ ] Create first script from template
- [ ] Create SCRIPTS.md from template
- [ ] Test script: `npx tsx scripts/tool-name.ts --help`
- [ ] Verify JSON output format
- [ ] Document all scripts in SCRIPTS.md
