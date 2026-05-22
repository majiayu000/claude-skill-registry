---
name: flutter-debug-cycle
description: Complete Flutter debugging toolkit combining PDCA methodology, Dart logging patterns, and MCP tools. Use when debugging Flutter apps - visual issues, runtime behavior, widget problems, or verifying fixes through device testing.
---

# Flutter Debug Cycle

Flutter開発に特化したPDCAデバッグツールキット。

## Required: Load These Skills

**You MUST read all of the following files before proceeding:**

1. `${CLAUDE_PLUGIN_ROOT}/skills/debug-cycle/SKILL.md`
   - PDCA methodology and workflow

2. `${CLAUDE_PLUGIN_ROOT}/skills/debug-log-patterns/references/dart-flutter.md`
   - Dart/Flutter logging patterns

3. `${CLAUDE_PLUGIN_ROOT}/skills/dart-mcp-tools/SKILL.md`
   - Dart/Flutter MCP tools (hot reload, logs, widget inspection)

4. `${CLAUDE_PLUGIN_ROOT}/skills/mobile-debug-tools/SKILL.md`
   - Mobile-MCP tools (screenshots, touch, UI inspection)

## Workflow Summary

```
PLAN:  Symptom → Hypothesis → Log points (use debug-cycle)
DO:    Add debugPrint (use dart-flutter patterns) → hot_restart (use dart-mcp-tools)
CHECK: get_app_logs (dart-mcp-tools) → take_screenshot (mobile-debug-tools) → Analyze
ACT:   Confirmed → Fix | Refuted → New hypothesis | Unclear → More logs
```

## Flutter-Specific Tips

- **Hot Reload vs Restart**: `initState` の変更は `hot_restart` が必要
- **Widget rebuild tracking**: `build()` メソッドにログを追加して再描画を追跡
- **State management debugging**: Provider/Riverpod/BLoC の状態変更をログ
- **Gesture conflicts**: 親子Widgetのタップ競合は両方にログを追加して調査
