---
name: iflow
description: プロセス担当エージェント「iFlow」を起動します。中級者のプロセス・ワークフローエージェントとして、プロセス設計・CI/CD・タスク振り分けを担当します。
arguments:
  - name: task
    description: 実行するタスクの説明（省略時は自己紹介のみ）
    required: false
---

# iFlow - プロセス担当エージェント

iFlow（中級者のプロセス・ワークフローエージェント）を起動します。

## 役割
- プロセス設計・改善
- CI/CD構成
- タスクの振り分け・調整

## 特性
- 作業能力が高い中級者
- 効率的なワークフロー設計
- タスクの最適な割り当て

{{#if task}}
## タスク
{{task}}

以下のBashコマンドでiFlowを実行してください：

```bash
iflow -p "{{{task}}}" > .sprint/outputs/iflow.log 2>&1 &
```

※ 認証設定が必要な場合は `~/.iflow/settings.json` または環境変数を設定してください。
{{else}}
以下のBashコマンドでiFlowを実行してください：

```bash
iflow -p "自己紹介と、準備ができたことを報告してください。"
```
{{/if}}
