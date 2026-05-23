---
name: web-performance
description: |
  Next.jsアプリケーションのパフォーマンス最適化スキル。
  Core Web Vitals（LCP、FID、CLS）改善、バンドルサイズ削減、画像・フォント最適化を提供する。

  Anchors:
  • 『High Performance Browser Networking』(Ilya Grigorik) / 適用: ネットワーク最適化 / 目的: レイテンシ削減
  • Web Vitals (Google) / 適用: Core Web Vitals測定 / 目的: UXメトリクス改善
  • Next.js Documentation / 適用: next/image, next/font, App Router / 目的: フレームワーク最適化

  Trigger:
  Use when optimizing Core Web Vitals (LCP, FID, CLS), reducing bundle size, implementing image optimization with next/image, or optimizing font loading with next/font.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Web Performance

## 概要

Next.jsアプリケーションのパフォーマンス最適化を専門とするスキル。
Core Web Vitals（LCP、FID、CLS）改善、バンドルサイズ削減、画像最適化、フォント最適化を通じて、ページ速度向上とユーザー体験改善を実現する。

## ワークフロー

### Phase 1: パフォーマンス監査

**目的**: 現状のパフォーマンスを測定しボトルネックを特定

**アクション**:

1. Lighthouse/PageSpeed Insightsでベースライン測定
2. Core Web Vitals（LCP、FID、CLS）の現在値を記録
3. `scripts/analyze-bundle.mjs` でバンドルサイズを分析
4. 問題の優先度を策定

**Task**: `agents/performance-auditor.md` を参照

### Phase 2: 最適化実装

**目的**: 特定した問題に対する最適化を実装

**アクション（問題種別に応じて選択）**:

| 問題           | エージェント        | 主な施策                     |
| -------------- | ------------------- | ---------------------------- |
| LCP（画像）    | image-optimizer     | next/image、priority属性     |
| FID            | bundle-optimizer    | コード分割、動的インポート   |
| CLS            | rendering-optimizer | フォント最適化、アスペクト比 |
| バンドルサイズ | bundle-optimizer    | Tree Shaking、個別インポート |

**Task**: 問題種別に応じたエージェントを参照

### Phase 3: 検証と記録

**目的**: 改善効果を測定し記録

**アクション**:

1. Lighthouse/Core Web Vitalsで改善後のメトリクスを測定
2. 改善前後の差分を記録
3. `scripts/log_usage.mjs` で実行記録を保存
4. 必要に応じてPhase 2に戻りイテレーション

## Task仕様ナビ

| Task               | 説明                                                  | 参照                            |
| ------------------ | ----------------------------------------------------- | ------------------------------- |
| パフォーマンス監査 | Lighthouse分析、Core Web Vitals測定、ボトルネック特定 | `agents/performance-auditor.md` |
| 画像最適化         | next/image活用、priority設定、placeholder実装         | `agents/image-optimizer.md`     |
| バンドル最適化     | コード分割、動的インポート、Tree Shaking              | `agents/bundle-optimizer.md`    |
| レンダリング最適化 | フォント最適化、CLS防止、スケルトンUI                 | `agents/rendering-optimizer.md` |

## ベストプラクティス

### すべきこと

- 最適化の前後でメトリクスを必ず測定する
- LCP対象画像にはpriority属性を付与する
- next/fontでフォントを最適化しCLSを防止する
- Server Componentsを活用しクライアントバンドルを削減する
- 重いライブラリは動的インポートで遅延読み込みする
- 画像にwidth/heightまたはaspect-ratioを指定する

### 避けるべきこと

- メトリクス測定なしで最適化完了と判断する
- 全ての画像にpriority属性を付与する（LCP画像のみ）
- Barrel Fileからの一括インポート
- use clientを不必要に広範囲に適用する
- 過度な最適化でメンテナンス性を犠牲にする

## リソース参照

### agents/（Task仕様書）

| エージェント        | パス                            | 用途               |
| ------------------- | ------------------------------- | ------------------ |
| performance-auditor | `agents/performance-auditor.md` | パフォーマンス監査 |
| image-optimizer     | `agents/image-optimizer.md`     | 画像最適化         |
| bundle-optimizer    | `agents/bundle-optimizer.md`    | バンドル最適化     |
| rendering-optimizer | `agents/rendering-optimizer.md` | レンダリング最適化 |

### references/（詳細知識）

| リソース        | パス                                  | 用途                 |
| --------------- | ------------------------------------- | -------------------- |
| Core Web Vitals | `references/core-web-vitals.md`       | メトリクス定義と閾値 |
| 最適化パターン  | `references/optimization-patterns.md` | 実装パターン集       |
| 画像最適化      | `references/image-optimization.md`    | next/image詳細       |
| コード分割      | `references/code-splitting.md`        | 分割戦略             |
| 動的インポート  | `references/dynamic-import.md`        | next/dynamic詳細     |
| フォント最適化  | `references/font-optimization.md`     | next/font詳細        |

### scripts/（自動化処理）

| スクリプト         | 用途         | 使用例                                        |
| ------------------ | ------------ | --------------------------------------------- |
| analyze-bundle.mjs | バンドル分析 | `node scripts/analyze-bundle.mjs`             |
| log_usage.mjs      | 使用記録     | `node scripts/log_usage.mjs --result success` |
| validate-skill.mjs | 構造検証     | `node scripts/validate-skill.mjs -v`          |

### assets/（テンプレート）

| テンプレート       | パス                                 | 用途                     |
| ------------------ | ------------------------------------ | ------------------------ |
| 動的インポート     | `assets/dynamic-import-template.md`  | next/dynamicテンプレート |
| 画像コンポーネント | `assets/image-component-template.md` | next/imageテンプレート   |

## 変更履歴

| Version | Date       | Changes                                             |
| ------- | ---------- | --------------------------------------------------- |
| 2.0.0   | 2026-01-01 | 18-skills.md仕様に完全準拠。4エージェント体制に拡張 |
| 1.1.0   | 2025-12-31 | ワークフロー詳細化、Task仕様ナビ追加                |
| 1.0.0   | 2025-12-24 | 初版作成                                            |
