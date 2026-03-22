---
name: verify-rule
description: Validate that a rule has all required files (analyzer, descriptor, test cases, docs) and passes tests. Use after implementing or modifying a rule to confirm completeness.
user-invocable: true
allowed-tools: Bash, Read, Glob, Grep
argument-hint: [RuleId]
hooks:
  Stop:
    - command: "bash .claude/hooks/log-skill-usage.sh verify-rule"
---

# Verify a Rule is Complete

Rule ID: `$ARGUMENTS`

Run each check below and report pass/fail for each.

## 1. Analyzer file exists
- Glob for `src/Spire.Analyzers/Rules/$ARGUMENTS*Analyzer.cs`
- Verify it has `[DiagnosticAnalyzer(LanguageNames.CSharp)]`
- Verify it references a descriptor from `Descriptors.cs`

## 2. Descriptor registered
- Grep `src/Spire.Analyzers/Descriptors.cs` for `id: "$ARGUMENTS"`

## 3. Test structure exists
- Verify test folder exists: `tests/Spire.Analyzers.Tests/$ARGUMENTS/`
- Verify test runner exists: `tests/Spire.Analyzers.Tests/$ARGUMENTS/${ARGUMENTS}Tests.cs`
- Verify test runner inherits `AnalyzerTestBase<...>` and overrides `RuleId`
- Verify case folder exists: `tests/Spire.Analyzers.Tests/$ARGUMENTS/cases/`
- Verify shared preamble exists: `tests/Spire.Analyzers.Tests/$ARGUMENTS/cases/_shared.cs`
- Count `should_fail` case files (need >= 3): files starting with `//@ should_fail`
- Count `should_pass` case files (need >= 3): files starting with `//@ should_pass`
- Verify all case files have proper headers (`//@ should_fail` or `//@ should_pass` on line 1)
- Verify all `should_fail` files have at least one `//~ ERROR` or `//~^ ERROR` marker

## 4. Documentation exists
- Look for `docs/rules/$ARGUMENTS.md`
- Verify it has all 5 required sections per `.claude/rules/documentation-conventions.md`: Title, Property table, Description, Examples, When to Suppress

## 5. Tests pass
```
dotnet test --filter "FullyQualifiedName~$ARGUMENTS"
```

## 6. Summary
Print a pass/fail checklist with counts.

## Constraints

- Do NOT create missing files — only report what's missing
- Do NOT modify existing code or documentation
- This is a read-only verification — if checks fail, report them and stop
- Do NOT lower the thresholds (3 detection, 3 false-positive test cases minimum)
