---
name: new-rule
description: Scaffold the test structure, descriptor, and docs for a new rule (TDD — tests before analyzer). Use when adding a new diagnostic rule.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
argument-hint: [RuleId] [RuleTitle]
hooks:
  Stop:
    - command: "bash .claude/hooks/log-skill-usage.sh new-rule"
---

# Scaffold a New Rule (TDD)

Arguments: `$ARGUMENTS`
Example: `/new-rule {RuleId} "Large struct passed by value"`

## Validation

1. Parse `$1` as the rule ID and everything after as the title
2. Verify the rule ID matches the prefix defined in CLAUDE.md followed by a numeric ID — reject otherwise
3. Verify no existing descriptor matches `id: "$1"` in `src/Spire.Analyzers/Descriptors.cs` — abort if duplicate

## Scaffolding (TDD order — tests and descriptor BEFORE analyzer)

4. Add descriptor to `src/Spire.Analyzers/Descriptors.cs`
   - Field name: `{RuleId}_{TitlePascalCase}`
   - Add in sequential order
5. Create test folder: `tests/Spire.Analyzers.Tests/{RuleId}/`
6. Create test case folder: `tests/Spire.Analyzers.Tests/{RuleId}/cases/`
7. Create shared preamble: `tests/Spire.Analyzers.Tests/{RuleId}/cases/_shared.cs`
   - Use `global using` directives (not plain `using`) — they apply to all case files since `_shared.cs` is a separate syntax tree in the same compilation
   - Always include: `global using System;`, `global using System.Collections.Generic;`, `global using System.Threading.Tasks;`, `global using Spire.Analyzers;`
   - Add rule-specific `global using` directives as needed (e.g., `global using System.Buffers;`)
   - Include shared type definitions relevant to the rule
8. Create test runner from template: `tests/Spire.Analyzers.Tests/{RuleId}/{RuleId}Tests.cs`
   - Replace `{{RULE_ID}}`, `{{ANALYZER_TYPE}}`
   - Inherits `AnalyzerTestBase<TAnalyzer>` — cases discovered at runtime, no `[InlineData]` needed
9. Create docs: `docs/rules/{RuleId}.md`
   - Replace `{{RULE_ID}}`, `{{RULE_TITLE}}`
   - Follow `docs/style-guide.md` for documentation style

## Verify

10. Run `dotnet build` — must succeed with zero warnings
11. Report all created files

## What this skill does NOT do

- **Does NOT create the analyzer file** — that is the implementer's job, after tests are written
- **Does NOT create test case files** — the lead writes those based on the rule plan's spec tables
- Only scaffolds the structure so the lead can immediately start writing test cases

## Constraints

- Do NOT implement detection logic — the analyzer file is not created at this stage
- Do NOT modify existing analyzer files or descriptors (only append the new descriptor)
- Do NOT proceed if validation fails — report the error and stop
