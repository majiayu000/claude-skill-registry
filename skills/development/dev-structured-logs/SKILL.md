---
name: dev-structured-logs
description: Migrate legacy string-based logging in .NET/C# code to structured logging templates, insert CommandHandler logging scopes, and validate or update Serilog File sink settings in appsettings JSON files. Use when users ask to modernize ILogger or Serilog usage through safe rewrites, run dry-run logging migration previews, apply structured logging rewrites, or enforce JSON file sink formatter and path conventions. For general backend design and observability guidance use $software-csharp-backend, for NUnit test design use $qa-testing-nunit, and for pipeline changes use $ops-nuke-cicd.
---

# Structured Logs

Run conservative, review-friendly rewrites for legacy log calls and Serilog JSON config. Default to dry-run and always produce machine-readable preview output.

This is an operation skill for deterministic logging rewrites. Do not use it as a general backend observability or CI/CD guidance skill.

## Workflow

1. Run dry-run first:

```bash
python .codex/skills/dev-structured-logs/scripts/structured_logs.py --path <repo> --dry-run
```

2. Review:
- `<repo>/patch.diff`
- `<repo>/preview-report.json`

3. Apply only after review:

```bash
python .codex/skills/dev-structured-logs/scripts/structured_logs.py --path <repo> --apply --backup-dir <dir>
```

4. Optionally commit:

```bash
python .codex/skills/dev-structured-logs/scripts/structured_logs.py --path <repo> --apply --commit-msg "chore: structured logging migration"
```

If the task expands into service design, runtime observability strategy, or API-layer refactoring, switch to `$software-csharp-backend`.
If the task expands into `nuke/Build.cs` or CI execution changes, switch to `$ops-nuke-cicd`.

## CLI Contract

Support these options:

```bash
--path <repo>
[--dry-run]
[--apply]
[--preview-file <path>]
[--backup-dir <dir>]
[--enable-handler-scope]
[--handler-pattern <pattern>]
[--log-framework <serilog|microsoft|auto>]
[--exclude <glob>] (repeatable)
[--commit-msg "message"]
```

Behavior:
- Default mode is dry-run when `--apply` is not provided.
- CommandHandler scope insertion is disabled by default; enable it explicitly with `--enable-handler-scope`.
- Do not touch excluded/generated folders: `bin/`, `obj/`, `node_modules/`, `packages/`, `.git/`, `.vs/`.
- Flag risky rewrites in `preview-report.json` with `risk_level` and `reason`.

## Part 1: Logging Transformation Rules

Rewrite only `logger.Log*` and `_logger.Log*` style invocations where message argument uses:
- String concatenation
- `String.Format(...)`
- String interpolation (`$"..."`)

Transform to message templates with properties and argument list.
Preserve interpolation expressions as argument expressions (including ternary expressions).

Preserve:
- Exception overload ordering (`LogError(ex, "...", args...)`)
- Original expression order

If any message argument has potential side effects (method call, `new`, increment/decrement, compound assignment):
- Extract expression to temporary variable before logging call
- Mark change as manual review in report

Do not attempt risky cross-statement rewrites. Keep changes local to call sites.

## Part 2: CommandHandler Scope Rules

Detect handlers by either:
- Class implementing `ICommandHandler<T>`
- Public methods matching handler pattern (default `Handle|HandleAsync`) with first parameter treated as command object

When `--enable-handler-scope` is set, at method start insert scope when missing:
- Build dictionary from command key properties: `UserId`, `TransactionId`, `TransferId`, `VerificationId`, `SessionId`, `Id`
- Initialize scope items with dictionary collection initializer style, for example:
```csharp
var __scopeItems = new Dictionary<string, object>
{
    ["Property1"] = command.Property1
};
```
- Use `using var _scope = _logger.BeginScope(__scopeItems);`

Skip if an equivalent command-property `BeginScope` block already exists in method prologue.

## Part 3: Serilog appsettings Rules

Auto-detect Serilog via `*.csproj` package references containing `Serilog`, `Serilog.*`, or `Sc.Infrastructure.Serilog`.
If any `*.csproj` file contains one of those package names, treat repository as Serilog-enabled and apply Serilog configuration updates to all `appsettings.json` files in the repository.

If Serilog is detected, inspect all `appsettings.json` files in the repository.

For each Serilog `File` sink with object `Args` (including nested `WriteTo` pipelines such as `Async` -> `Logger` -> `configureLogger` -> `WriteTo`):
- Ensure `Args.path` ends with `.json`
- If `Args.path` is a debug log file path (for example `*.debug`), rename it to `.debug.json`
- Set `Args.formatter` to:
  - `Sc.Infrastructure.Serilog.CustomJsonFormatter, Sc.Infrastructure.Serilog`
- Remove `Args.outputTemplate`

Do not modify non-File sinks.
If Serilog section or File sink does not exist, do nothing.

## Outputs

Always produce in repo root:
- `patch.diff` unified diff
- `preview-report.json` entries:
  - `file`
  - `line`
  - `original`
  - `transformed`
  - `risk_level`
  - `reason`

When applying:
- Create backups in `--backup-dir` or `.codex/skills/dev-structured-logs/backups`
- Apply file updates
- If `--commit-msg` is supplied, attempt git commit

## Examples

Use files in `examples/` to validate behavior:
- `concatenation.before.cs` / `concatenation.after.cs`
- `string-format.before.cs` / `string-format.after.cs`
- `interpolation.before.cs` / `interpolation.after.cs`
- `side-effect.before.cs` / `side-effect.after.cs`
- `handler-scope.before.cs` / `handler-scope.after.cs`
- `appsettings.before.json` / `appsettings.after.json`
