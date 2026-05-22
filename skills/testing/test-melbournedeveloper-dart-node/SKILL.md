---
name: test
description: Run tests and coverage for dart_node packages. Automatically detects which packages to test based on changed files.
argument-hint: "[--tier N] [--all] [package...]"
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
---

# Run Tests & Coverage

## Step 1: Determine what to test

If `$ARGUMENTS` specifies a tier or package, use that. Otherwise, **detect which packages were affected by recent changes**:

```bash
git diff --name-only main
```

Map changed files to packages:

| Changed path | Test target |
|---|---|
| `packages/dart_node_core/` | `packages/dart_node_core` |
| `packages/dart_node_express/` | `packages/dart_node_express` |
| `packages/dart_node_ws/` | `packages/dart_node_ws` |
| `packages/dart_node_better_sqlite3/` | `packages/dart_node_better_sqlite3` |
| `packages/dart_node_mcp/` | `packages/dart_node_mcp` |
| `packages/dart_node_react/` | `packages/dart_node_react` |
| `packages/dart_node_react_native/` | `packages/dart_node_react_native` |
| `packages/dart_logging/` | `packages/dart_logging` |
| `packages/reflux/` | `packages/reflux` |
| `packages/dart_jsx/` | `packages/dart_jsx` |
| `examples/frontend/` | `examples/frontend` |
| `examples/too_many_cooks/` | `examples/too_many_cooks` |
| `examples/markdown_editor/` | `examples/markdown_editor` |
| `examples/reflux_demo/` | `examples/reflux_demo/web_counter` |
| `tools/` or root config | Run `--all` |

If a Tier 1 package changed, also run its downstream dependents in Tier 2/3.

## Step 2: Run tests

**Specific packages** (preferred — faster):
```bash
./tools/test.sh packages/dart_node_core packages/dart_node_express
```

**Full tier**:
```bash
./tools/test.sh --tier 1
```

**Everything** (use `--all` arg or when root files changed):
```bash
./tools/test.sh
```

## Step 3: Coverage for affected packages

For each Node package that was tested, run the coverage tool:

```bash
cd packages/<name> && dart run ../dart_node_coverage/bin/coverage.dart
```

Node packages (use coverage CLI): `dart_node_core`, `dart_node_express`, `dart_node_ws`, `dart_node_better_sqlite3`, `dart_node_mcp`, `dart_node_react_native`

Browser packages (use `dart test -p chrome`): `dart_node_react`

Standard packages (use `dart test --coverage`): `dart_logging`, `reflux`

Minimum coverage: **80%**. If below threshold, read `coverage/lcov.info` and identify uncovered lines.

## Tiers reference

- **Tier 1:** `dart_logging`, `dart_node_core`
- **Tier 2:** `reflux`, `dart_node_express`, `dart_node_ws`, `dart_node_better_sqlite3`, `dart_node_mcp`, `dart_node_react_native`, `dart_node_react`
- **Tier 3:** `examples/frontend`, `examples/markdown_editor`, `examples/reflux_demo/web_counter`, `examples/too_many_cooks`

## After running

1. Report PASS/FAIL per package with coverage percentages
2. If failures occur, read the log from `logs/<package>.log` and diagnose
3. If coverage is below 80%, suggest specific test cases to add
4. Never skip tests, remove assertions, or silently swallow failures
