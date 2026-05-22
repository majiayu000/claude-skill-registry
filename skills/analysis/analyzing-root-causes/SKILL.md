---
name: analyzing-root-causes
description: >
  Root cause analysis with 5 Whys methodology.
  Triggers: root cause, 5 Whys, なぜなぜ分析, 根本原因, 原因分析, symptom fix, 対症療法.
allowed-tools: [Read, Grep, Glob, Task]
context: fork
user-invocable: false
---

# 根本原因分析 - 5 Whys

## 症状 vs 根本原因

| タイプ       | 例                            | 結果           |
| ------------ | ----------------------------- | -------------- |
| 症状修正     | DOM待ちのためにsetTimeout追加 | 後で壊れる     |
| 根本原因修正 | React refを適切に使用         | 恒久的な解決   |
| 症状修正     | 二重送信防止フラグを追加      | 複雑性が増大   |
| 根本原因修正 | 送信中にボタンを無効化        | シンプルな修正 |

## 5 Whysプロセス

| Step | 質問                 | 明らかになること   |
| ---- | -------------------- | ------------------ |
| 1    | なぜ発生する？       | 観察可能な事実     |
| 2    | なぜそれが起こる？   | 実装詳細           |
| 3    | なぜそうなっている？ | 設計決定           |
| 4    | なぜそれが存在する？ | アーキテクチャ制約 |
| 5    | なぜそう設計された？ | 根本原因           |

## 参考

| トピック | ファイル                         |
| -------- | -------------------------------- |
| 5 Whys   | `references/five-whys.md`        |
| パターン | `references/symptom-patterns.md` |
