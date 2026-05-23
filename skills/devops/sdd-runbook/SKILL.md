---
name: sdd-runbook
description: インシデント対応手順書(runbook.md)を生成。Severity定義・共通対応手順・シナリオ別対応・ロールバック手順を含む。
argument-hint: "[spec-slug] [target-dir(optional)]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep
model: opus
---

# sdd-runbook — Incident Response Runbook Generator

## 0. 目的
- インシデント発生時に迅速かつ正確に対応するための手順書
- Severity定義で優先度を明確化
- シナリオ別の具体的な対応コマンドを提供
- ロールバック手順で復旧を確実に

## 1. 入力と出力

### 入力
- /sdd-runbook $ARGUMENTS
  - $0 = spec-slug（例: google-ad-report）
  - $1 = target-dir（任意。未指定なら `.kiro/specs/<spec-slug>/` を使う）
- 前提: design.md と slo.md が存在すること

### 出力（必須）
- <target-dir>/runbook.md

### 参照
- templates/runbook.template.md : Runbookテンプレート
- <target-dir>/design.md : システム構成
- <target-dir>/slo.md : SLO/SLI定義

## 2. 重要ルール

1. **コピペ実行可能**: コマンドはそのまま実行できる形式
2. **Severity明確化**: 初動目標・解決目標を数値で定義
3. **チェックリスト形式**: 見落としを防ぐ
4. **ポストモーテム必須**: 再発防止のためのRCAプロセス

## 3. Severity定義

| Severity | 定義 | 初動目標 | 解決目標 |
|----------|------|---------|---------|
| **SEV1** | サービス全停止、データ損失リスク | 15分 | 4時間 |
| **SEV2** | 主要機能停止、大規模影響 | 30分 | 8時間 |
| **SEV3** | 一部機能停止、限定影響 | 1時間 | 24時間 |
| **SEV4** | 軽微な問題 | 4時間 | 1週間 |

## 4. 手順

### Step A: 入力読み込み
1. design.md からシステム構成を抽出
2. slo.md からSLI/アラート条件を抽出
3. 主要コンポーネントと依存関係を把握

### Step B: 概要セクション
1. 対象サービス情報
2. オンコール連絡先
3. 重要リンク（ダッシュボード、ログ、アラート）

### Step C: 共通対応手順
1. 初動対応フロー（アラート確認→コミュニケーション→調査）
2. 緊急コマンド集（kubectl, psql等）
3. 復旧確認チェックリスト

### Step D: シナリオ別対応
システム特性に応じて以下を網羅:
- 高レイテンシ
- 高エラー率
- DB接続障害
- メモリ/CPU枯渇
- 外部API障害
- セキュリティインシデント

各シナリオに:
1. 症状の定義
2. 確認手順（コマンド付き）
3. 緩和策（優先順位付き）

### Step E: ロールバック手順
1. アプリケーションロールバック
2. DBマイグレーションロールバック
3. 設定変更ロールバック
4. 各手順にコマンド例を含む

### Step F: チェックリスト
1. 復旧確認チェックリスト
2. インシデントクローズチェックリスト
3. ポストモーテムテンプレート

## 5. コマンド形式

```bash
# 説明コメント
実行可能なコマンド --with-real-flags

# 例: Pod状態確認
kubectl get pods -n <namespace> -o wide
```

プレースホルダーは `<placeholder>` 形式で明示。

## 6. 実行例

```bash
/sdd-runbook google-ad-report
```

前提:
- .kiro/specs/google-ad-report/design.md
- .kiro/specs/google-ad-report/slo.md

出力:
- .kiro/specs/google-ad-report/runbook.md
