---
name: codex
description: コーディング担当エージェント「Codex」を起動します。中上級者のコーディングエージェントとして、コード実装・設計・技術課題解決を担当します。
arguments:
  - name: task
    description: 実行するタスクの説明（省略時は自己紹介のみ）
    required: false
---

# Codex - コーディング担当エージェント

Codex（中上級者のコーディングエージェント）を起動します。

## 役割
- コードの実装・リード
- 設計・アーキテクチャの検討
- 技術的な課題解決

## 特性
- 作業能力が高い中上級者
- Java、Minecraftプラグイン開発に精通
- テスト駆動開発、リファクタリングが得意

{{#if task}}
## タスク
{{task}}

以下のBashコマンドでCodexを実行してください：

```bash
codex exec --full-auto --sandbox read-only --cd /workspaces/java/Minecraft-Java-Plaugin-forRPG "{{{task}}}"
```

結果をログファイルに保存する場合：

```bash
mkdir -p .sprint/outputs
codex exec --full-auto --sandbox read-only --cd /workspaces/java/Minecraft-Java-Plaugin-forRPG "{{{task}}}" > .sprint/outputs/codex.log 2>&1 &
```
{{else}}
以下のBashコマンドでCodexを実行してください：

```bash
codex exec --full-auto --sandbox read-only --cd /workspaces/java/Minecraft-Java-Plaugin-forRPG "自己紹介と、準備ができたことを報告してください。"
```
{{/if}}
