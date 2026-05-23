---
name: multipart-upload
description: |
  大容量ファイルのマルチパートアップロードを専門とするスキル。
  ネットワークの不安定性を前提とした堅牢なファイル転送を設計し、
  チャンク分割、リトライ、進捗追跡、チェックサム検証を統合的に提供する。

  Anchors:
  • Computer Networks (Andrew Tanenbaum) / 適用: ネットワーク不安定性への対応 / 目的: 堅牢なファイル転送設計
  • The Pragmatic Programmer / 適用: 実践的な実装パターン / 目的: 保守性の高いコード設計
  • RFC 7233 Range Requests / 適用: チャンク分割と再開機能 / 目的: 標準準拠の実装

  Trigger:
  Use when implementing large file uploads, chunked file transfer, resumable uploads, upload progress tracking, or data integrity verification with checksums.
  multipart, upload, chunked, resumable, progress tracking, checksum, file transfer, large file
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Multipart Upload

## 概要

大容量ファイルのマルチパートアップロードを専門とするスキル。
ネットワークの不安定性を前提とした堅牢なファイル転送を設計し、
チャンク分割、リトライ、進捗追跡、チェックサム検証を統合的に提供する。

## ワークフロー

### Phase 1: 要件分析と設計方針決定

**目的**: アップロード要件を分析し、最適な設計方針を決定

**参照エージェント**: `agents/requirements-analysis.md`

**アクション**:

1. `references/basics.md` でマルチパートアップロードの基本概念を理解
2. ファイルサイズとネットワーク環境を確認
3. `references/chunk-strategies.md` でチャンクサイズ戦略を選定
4. `scripts/analyze-upload-config.mjs` で設定の妥当性を検証

### Phase 2: 実装

**目的**: チャンク分割、リトライ、進捗追跡機能を実装

**参照エージェント**: `agents/implementation.md`

**アクション**:

1. `references/patterns.md` で実装パターンを確認
2. `assets/chunk-uploader-template.ts` をベースに実装
3. `references/progress-tracking.md` で進捗表示を実装
4. `references/checksum-verification.md` でデータ整合性検証を追加

### Phase 3: 検証

**目的**: アップロード機能の検証と最適化

**参照エージェント**: `agents/validation.md`

**アクション**:

1. `scripts/validate-upload.mjs` でチェックサム検証
2. 中断再開機能のテスト
3. ネットワーク障害時のリトライ動作確認
4. `scripts/log_usage.mjs` で実行記録を保存

## リソース参照

### 参照ドキュメント

| ドキュメント                                                                   | 内容                         |
| ------------------------------------------------------------------------------ | ---------------------------- |
| [references/basics.md](references/basics.md)                                   | マルチパートアップロード基礎 |
| [references/patterns.md](references/patterns.md)                               | 実装パターン                 |
| [references/chunk-strategies.md](references/chunk-strategies.md)               | チャンク分割戦略             |
| [references/chunk-size-optimization.md](references/chunk-size-optimization.md) | チャンクサイズ最適化         |
| [references/progress-tracking.md](references/progress-tracking.md)             | 進捗追跡パターン             |
| [references/checksum-verification.md](references/checksum-verification.md)     | チェックサム検証             |

### エージェント

| エージェント                      | 役割                   |
| --------------------------------- | ---------------------- |
| `agents/requirements-analysis.md` | 要件分析、設計方針決定 |
| `agents/implementation.md`        | 実装ガイド             |
| `agents/validation.md`            | 検証、品質確認         |

### スクリプト

| スクリプト                          | 用途                 |
| ----------------------------------- | -------------------- |
| `scripts/analyze-upload-config.mjs` | 設定検証、推奨値算出 |
| `scripts/validate-upload.mjs`       | チェックサム検証     |
| `scripts/validate-skill.mjs`        | スキル構造検証       |
| `scripts/log_usage.mjs`             | 使用記録             |

### テンプレート

| テンプレート                        | 用途                       |
| ----------------------------------- | -------------------------- |
| `assets/chunk-uploader-template.ts` | チャンクアップローダー実装 |
| `assets/upload-client-template.ts`  | アップロードクライアント   |
| `assets/upload-manager-template.ts` | 複数ファイル管理           |

## ベストプラクティス

### すべきこと

- ファイルサイズに応じたチャンクサイズの動的決定
- 各チャンクのチェックサム検証
- 中断再開可能な状態管理
- リトライ時の指数バックオフ
- 進捗のリアルタイム表示
- ネットワーク状況に応じた並列数調整

### 避けるべきこと

- 固定チャンクサイズの使用（ファイルサイズ無視）
- リトライなしのアップロード
- 進捗情報なしの長時間アップロード
- チェックサム検証の省略
- 状態管理なしの大容量アップロード
