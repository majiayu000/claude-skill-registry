---
name: event-driven-file-watching
description: |
  Chokidarライブラリを中心としたファイルシステム監視の専門スキル。
  Observer Patternによる効率的なファイル変更検知、クロスプラットフォーム対応、
  EventEmitterによる疎結合な通知システムを設計・実装する。

  Anchors:
  • Node.js EventEmitter / 適用: イベント駆動設計 / 目的: 疎結合な通知メカニズム
  • Chokidar Documentation / 適用: ファイル監視設定 / 目的: クロスプラットフォーム監視
  • Observer Pattern (GoF) / 適用: イベント通知設計 / 目的: 変更検知と通知の分離

  Trigger:
  Use when implementing file system watching, Chokidar configuration, file change detection, or event-based file monitoring systems.
  file watching, chokidar, fs watch, file change, event emitter, observer pattern, hot reload

allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# Event-Driven File Watching

## 概要

Chokidarライブラリを使用したファイルシステム監視の設計・実装スキル。Observer Patternに基づく疎結合なイベント通知システムを構築し、クロスプラットフォームで動作する効率的な監視機構を提供する。

## ワークフロー

### Phase 1: アーキテクチャ設計

**目的**: ファイル監視システムのアーキテクチャを設計

**アクション**:

1. 監視要件の整理（対象パス、イベントタイプ）
2. 実行環境の確認（OS、ファイル数）
3. Chokidar設定の設計
4. イベントフローの設計

**Task**: `agents/watcher-architect.md` を参照

### Phase 2: イベントハンドラ実装

**目的**: Observer Patternに基づくイベントハンドラを実装

**アクション**:

1. Chokidar watcher の初期化
2. イベントハンドラの実装
3. エラーハンドリングの追加
4. リソースクリーンアップの実装

**Task**: `agents/event-handler-implementer.md` を参照

### Phase 3: パフォーマンス最適化

**目的**: メモリ・CPU・スループットの最適化

**アクション**:

1. debounce/throttle の適用
2. ignored パターンの最適化
3. polling vs native の選択
4. メモリリーク対策

**Task**: `agents/performance-optimizer.md` を参照

## Task仕様（ナビゲーション）

| Task                      | 起動タイミング | 入力       | 出力                 |
| ------------------------- | -------------- | ---------- | -------------------- |
| watcher-architect         | Phase 1開始時  | 監視要件   | アーキテクチャ設計書 |
| event-handler-implementer | Phase 2開始時  | 設計書     | 実装コード           |
| performance-optimizer     | Phase 3開始時  | 実装コード | 最適化済みコード     |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリの対応ファイルを参照

## ベストプラクティス

### すべきこと

- `awaitWriteFinish` で書き込み完了を待機
- `ignored` パターンでnode_modules等を除外
- エラーイベントを必ずハンドル
- `watcher.close()` でリソース解放
- debounce で高頻度イベントを制御
- 相対パスより絶対パスを使用

### 避けるべきこと

- 大規模ディレクトリでの再帰監視（要フィルタ）
- polling を不要に有効化（パフォーマンス低下）
- watcher の close 忘れ（メモリリーク）
- ready イベント前のファイル操作
- 同期処理をイベントハンドラ内で実行

## リソース参照

### references/（詳細知識）

| リソース                 | パス                                                                                   | 用途             |
| ------------------------ | -------------------------------------------------------------------------------------- | ---------------- |
| Chokidar設定リファレンス | See [references/chokidar-config-reference.md](references/chokidar-config-reference.md) | オプション詳細   |
| EventEmitterパターン     | See [references/event-emitter-patterns.md](references/event-emitter-patterns.md)       | イベント通知設計 |

### scripts/（決定論的処理）

| スクリプト           | 用途               | 使用例                                        |
| -------------------- | ------------------ | --------------------------------------------- |
| `log_usage.mjs`      | フィードバック記録 | `node scripts/log_usage.mjs --result success` |
| `validate-skill.mjs` | スキル構造検証     | `node scripts/validate-skill.mjs`             |

### assets/（テンプレート）

| テンプレート          | 用途                         |
| --------------------- | ---------------------------- |
| `watcher-template.ts` | ファイル監視実装テンプレート |

## 変更履歴

| Version | Date       | Changes                            |
| ------- | ---------- | ---------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md完全準拠版として再構築 |
| 1.1.0   | 2025-12-31 | agents実装、EVALS/LOGS追加         |
| 1.0.0   | 2025-12-24 | 初版作成                           |
