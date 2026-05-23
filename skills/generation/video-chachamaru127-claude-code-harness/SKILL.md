---
name: video
description: "Generates product demo videos, architecture explanations, and release note videos. Use when user mentions video generation, product demos, or visual documentation. Requires Remotion setup."
allowed-tools: ["Read", "Write", "Edit", "Grep", "Glob", "Bash", "Task", "AskUserQuestion", "WebFetch"]
---

# Video Generation Skills

プロダクト説明動画の自動生成を担当するスキル群です。

---

## 概要

`/generate-video` コマンドの内部で使用されるスキルです。
コードベース分析 → シナリオ提案 → 並列生成のフローを実行します。

## 機能詳細

| 機能 | 詳細 |
|------|------|
| **ベストプラクティス** | See [references/best-practices.md](references/best-practices.md) |
| **コードベース分析** | See [references/analyzer.md](references/analyzer.md) |
| **シナリオプランニング** | See [references/planner.md](references/planner.md) |
| **並列シーン生成** | See [references/generator.md](references/generator.md) |

## Prerequisites

- Remotion がセットアップ済み（`/remotion-setup`）
- Node.js 18+

## `/generate-video` フロー

```
/generate-video
    │
    ├─[Step 1] 分析（analyzer.md）
    │   ├─ フレームワーク検出
    │   ├─ 主要機能検出
    │   ├─ UIコンポーネント検出
    │   └─ プロジェクト資産解析（Plans.md, CHANGELOG等）
    │
    ├─[Step 2] シナリオ提案（planner.md）
    │   ├─ 動画タイプ自動判定
    │   ├─ シーン構成提案
    │   └─ ユーザー確認
    │
    └─[Step 3] 並列生成（generator.md）
        ├─ シーン並列生成（Task tool）
        ├─ 統合 + トランジション
        └─ 最終レンダリング
```

## 実行手順

1. ユーザーが `/generate-video` を実行
2. Remotion セットアップ確認
3. `analyzer.md` でコードベース分析
4. `planner.md` でシナリオ提案 + ユーザー確認
5. `generator.md` で並列生成
6. 完了報告

## 動画タイプ（ファネル別）

| タイプ | ファネル | 長さ目安 | 自動判定条件 | 構成の芯 |
|--------|----------|----------|--------------|----------|
| **LP/広告ティザー** | 認知〜興味 | 30-90秒 | 新規プロジェクト | 痛み→結果→CTA |
| **Introデモ** | 興味→検討 | 2-3分 | UI変更検出 | 1ユースケース完走 |
| **リリースノート** | 検討→確信 | 1-3分 | CHANGELOG更新 | Before/After重視 |
| **アーキテクチャ解説** | 確信→決裁 | 5-30分 | 大規模構造変更 | 実運用+証拠 |
| **オンボーディング** | 継続・活用 | 30秒-数分 | 初回セットアップ | Aha体験への最短パス |

> 詳細: [references/best-practices.md](references/best-practices.md)

## シーンテンプレート

### 90秒ティザー（LP/広告向け）

| 時間 | シーン | 内容 |
|------|--------|------|
| 0-5秒 | Hook | 痛み or 望む結果 |
| 5-15秒 | Problem+Promise | 対象ユーザーと約束 |
| 15-55秒 | Workflow | 象徴ワークフロー |
| 55-70秒 | Differentiator | 差別化の根拠 |
| 70-90秒 | CTA | 次の一手 |

### 3分Introデモ（検討向け）

| 時間 | シーン | 内容 |
|------|--------|------|
| 0-10秒 | Hook | 結論+痛み |
| 10-30秒 | UseCase | ユースケース宣言 |
| 30-140秒 | Demo | 実画面で完走 |
| 140-170秒 | Objection | よくある不安1つ潰す |
| 170-180秒 | CTA | 行動喚起 |

### 共通シーン

| シーン | 推奨時間 | 内容 |
|--------|----------|------|
| イントロ | 3-5秒 | ロゴ + タグライン |
| 機能デモ | 10-30秒 | Playwrightキャプチャ |
| アーキテクチャ図 | 10-20秒 | Mermaid → アニメーション |
| CTA | 3-5秒 | URL + 連絡先 |

> 詳細テンプレート: [references/best-practices.md](references/best-practices.md#テンプレート)

## Notes

- Remotion未セットアップの場合は `/remotion-setup` を案内
- 並列生成数はシーン数に応じて自動調整（max 5）
- 生成された動画は `out/` ディレクトリに出力
