---
name: l-step
description: Lステップ機能（シナリオ配信・セグメント・LINE連携）の段階的実装。/l-step phase1 〜 phase6 で各フェーズを実行。
---

# Lステップ機能 実装スキル

このスキルはLステップのような機能を段階的に実装します。

## 使い方

```bash
/l-step phase1   # データベース基盤
/l-step phase2   # シナリオ基本機能
/l-step phase3   # 条件分岐機能
/l-step phase4   # セグメント配信
/l-step phase5   # LINE連携
/l-step phase6   # テスト・最適化
/l-step all      # 全フェーズ順次実行
```

## フェーズ概要

| Phase | 内容 | 主要ファイル |
|-------|------|-------------|
| 1 | DB基盤 | supabase/migrations/, lib/types/ |
| 2 | シナリオ基本 | app/api/scenarios/, lib/scenarios/ |
| 3 | 条件分岐 | lib/scenarios/condition-evaluator.ts |
| 4 | セグメント | app/api/segments/, lib/segments/ |
| 5 | LINE連携 | app/api/line/, lib/line/ |
| 6 | テスト | __tests__/, e2e/ |

## 実行時の注意

1. **フェーズ順序を守る** - Phase 1から順番に実行
2. **各フェーズ完了後に確認** - ビルド・テストが通ることを確認
3. **エラー時は/build-fix** - ビルドエラーが出たら修正

## アーキテクチャ

```
シナリオ登録 → Cronジョブ(1分) → ステップ実行 → 次ステップへ
                    ↓
              条件チェック → Yes/No分岐
                    ↓
              メール送信 or LINE送信
```

## データベース構造

```
scenarios (シナリオ定義)
  └── scenario_steps (ステップ)
        └── scenario_enrollments (登録状態)

segments (セグメント)
  └── segment_rules (ルール)

contacts
  └── contact_custom_values (カスタム属性)
  └── contact_line_links (LINE紐付け)

line_accounts (LINE連携)
```
