---
name: umbraco-skill-code-analyzer
description: Analyze code examples in SKILL.md files for correctness using static analysis and TypeScript compilation
version: 1.0.0
location: managed
allowed-tools: Bash
---

# Umbraco Skill Code Analyzer

Static analysis tool that validates code examples in SKILL.md files.

## What It Checks

- **Import paths** - Validates `@umbraco-cms/backoffice/*` imports against known modules
- **Extension types** - Checks `type:` values against known Umbraco extension types
- **Deprecated patterns** - Flags outdated code patterns
- **TypeScript compilation** - Optional syntax/type checking

## Usage

```bash
cd .claude/skills/umbraco-skill-code-analyzer/scripts
npm install --silent
npx tsx analyze-code.ts
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CHECK_TYPESCRIPT` | `true` | Set to `false` to skip TypeScript compilation |

## Output

Produces `code-analysis-report.json` in project root with structure:

```json
{
  "timestamp": "...",
  "skillsScanned": 69,
  "codeBlocksAnalyzed": 473,
  "issuesFound": 34,
  "skills": [
    {
      "skillPath": "...",
      "skillName": "...",
      "codeBlocks": 5,
      "issues": [
        {
          "line": 33,
          "type": "invalid-import",
          "value": "@umbraco-cms/backoffice/unknown",
          "message": "Unknown import path",
          "severity": "warning"
        }
      ]
    }
  ],
  "statistics": {
    "totalCodeBlocks": 473,
    "typescriptBlocks": 368,
    "importIssues": 16,
    "extensionTypeIssues": 21,
    "compilationErrors": 0,
    "deprecatedPatterns": 15
  }
}
```

## Issue Types

| Type | Severity | Description |
|------|----------|-------------|
| `invalid-import` | warning | Unknown `@umbraco-cms/backoffice/*` module |
| `unknown-extension-type` | warning | Unrecognized extension `type:` value |
| `deprecated-pattern` | warning | Outdated code pattern detected |
| `typescript-error` | error | TypeScript compilation failed |

## Updating Known Values

The script maintains lists of known modules and extension types. To update:

1. Edit `analyze-code.ts`
2. Add to `KNOWN_BACKOFFICE_MODULES` set
3. Add to `KNOWN_EXTENSION_TYPES` set
