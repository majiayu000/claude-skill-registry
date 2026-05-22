---
description: LSP diagnosticsの警告を検出し修正します。実装完了後の品質チェックとして使用します。
user-invocable: true
---

# LSP警告修正コマンド

このスキルはLua/Neovimプロジェクトの LSP 警告を検出し、自動修正します。

## 使用方法

Taskツールを使用して `fix-lsp-warnings` サブエージェントを呼び出し、プロジェクト全体の警告を修正してください。

```
Task tool:
  subagent_type: fix-lsp-warnings
  prompt: プロジェクト全体のLSP警告を検出し、修正してください。
```

## 実行フロー

1. LSP警告の検出（nvim --headless + lua_ls）
2. 警告の分類と修正
3. 修正の確認
4. lint&テスト実行（make lintとmake test）
