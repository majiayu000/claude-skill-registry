---
name: pub-get
description: Install all Dart and npm dependencies in dependency order
disable-model-invocation: true
allowed-tools: Bash
---

# Install Dependencies

Run the dependency installer that handles the tiered monorepo structure.

```bash
./tools/pub_get.sh
```

## What it does

Installs `dart pub get` and `npm install` across all packages and examples in dependency order:

1. **Tier 1 (Core):** `dart_logging`, `dart_node_coverage`, `dart_node_core`, `reflux`
2. **Tier 2 (Packages):** `dart_jsx`, `dart_node_express`, `dart_node_ws`, `dart_node_better_sqlite3`, `dart_node_mcp`, `dart_node_react`, `dart_node_react_native`
3. **Tier 3 (Examples):** `frontend`, `markdown_editor`, `reflux_demo/web_counter`, `too_many_cooks`, `backend`, `mobile`, `jsx_demo`

Order matters because Tier 2 depends on Tier 1, and Tier 3 depends on both.

## After running

Report any failures. If a package fails, it's usually because:
- A dependency in an earlier tier hasn't been published yet (use `dart run tools/switch_deps.dart local` for local dev)
- npm packages need `npm install` in a subdirectory (e.g., `examples/mobile/rn/`)
