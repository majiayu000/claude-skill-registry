---
name: lint-dotnet
description: Run .NET architecture linter to check for MSBuild/CPM violations
---

# /lint-dotnet

Run the .NET architecture linter on demand to check for violations.

## Execution

```bash
bash "${CLAUDE_PLUGIN_ROOT}/scripts/lint-dotnet.sh" .
```

## Output Format

```
RULE_X|file
  line_number: violation details
```

## Rules

| Rule | Catches | Fix |
|------|---------|-----|
| RULE_A | Hardcoded `Version="1.2.3"` in Directory.Packages.props | Use `$(VariableName)` and define in Version.props |
| RULE_B | Version.props imported outside allowed files | Remove import. Only DPP or eng/DBP allowed. |
| RULE_C | Version.props not a symlink (in consumer repos) | Recreate symlink, never copy the file |
| RULE_G | `<PackageReference Version="...">` in .csproj | Remove Version attr, use CPM |

## Allowed Version.props Import Owners

| File | Purpose |
|------|---------|
| `Directory.Packages.props` | CPM-enabled projects |
| `eng/Directory.Build.props` | CPM-disabled projects |
| `src/Sdk/*/Sdk.props` | SDK entry points (MSBuild auto-imports these) |
| `src/common/*.props` | Shared SDK infrastructure |

All other files importing Version.props = violation.

## Clean Output

```
CLEAN|All rules passed
```

No violations found. Safe to proceed.

## Variable Naming Convention

For unknown packages, generate variable name:
- `Some.Package.Name` -> `SomePackageNameVersion`
- Remove dots and dashes, append "Version"
