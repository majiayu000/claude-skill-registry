---
name: sdd-slo
description: Google SREに基づくSLO/SLI/SLA定義(slo.md)を生成。信頼性目標・Error Budget・アラート設定を含む運用可能な品質定義。
argument-hint: "[spec-slug] [target-dir(optional)]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep
model: opus
---

# sdd-slo — SLO/SLI/SLA Definition Generator

## 0. 目的
- Google SRE原則に基づく信頼性目標を定義
- SLI（指標）→ SLO（目標）→ SLA（契約）の階層構造
- Error Budget Policy で開発と信頼性のバランスを取る
- 運用可能な形で計測方法とアラートを定義

## 1. 入力と出力

### 入力
- /sdd-slo $ARGUMENTS
  - $0 = spec-slug（例: google-ad-report）
  - $1 = target-dir（任意。未指定なら `.kiro/specs/<spec-slug>/` を使う）
- 前提: requirements.md が存在すること

### 出力（必須）
- <target-dir>/slo.md

### 参照
- templates/slo.template.md : SLOテンプレート
- <target-dir>/requirements.md : 非機能要件からSLO導出

## 2. 重要ルール

1. **SLI先行**: まず測定可能な指標を定義、次に目標を設定
2. **Error Budget**: SLOからError Budgetを計算し、ポリシーを定義
3. **計測可能**: 全SLIにPrometheus/Grafana等での計測クエリを含む
4. **アラート設定**: SLO違反時のアラート条件を明確化

## 3. SLI/SLO/SLA階層

| レベル | 定義 | 例 |
|--------|------|-----|
| **SLI** | Service Level Indicator | 成功率、レイテンシP99、エラー率 |
| **SLO** | Service Level Objective | 可用性 >= 99.5%（30日間） |
| **SLA** | Service Level Agreement | 可用性 >= 99.0%（違反時クレジット） |

## 4. 主要SLIカテゴリ

| カテゴリ | SLI例 | 計測方法 |
|---------|-------|---------|
| **可用性** | リクエスト成功率 | 2xx+3xx / total |
| **レイテンシ** | P50/P95/P99応答時間 | histogram_quantile |
| **エラー率** | 5xxレスポンス率 | 5xx / total |
| **スループット** | RPS | rate(requests_total) |
| **正確性** | データ整合性率 | 検証成功 / 検証総数 |
| **鮮度** | データ遅延時間 | now - last_update |

## 5. 手順

### Step A: 入力読み込み
1. requirements.md から非機能要件を抽出
2. 既存のSLO定義があれば読み込み
3. サービス特性を把握

### Step B: SLI定義
1. 可用性SLI（必須）
2. レイテンシSLI（P50/P95/P99）
3. エラー率SLI
4. サービス固有SLI（あれば）
5. 各SLIに計測クエリ（Prometheus形式）を付与

### Step C: SLO定義
1. 各SLIに目標値を設定
2. 測定期間を定義（30日/四半期）
3. Error Budgetを計算

```
Error Budget = 100% - SLO Target
例: SLO 99.5% → Error Budget 0.5% = 月3.6時間のダウンタイム許容
```

### Step D: Error Budget Policy
1. 消費率に応じたアクション定義
   - 0-50%: 通常開発
   - 50-75%: リスク高い変更保留
   - 75-100%: 新機能停止、信頼性優先
   - 100%+: インシデントモード
2. バーンレートアラート設定

### Step E: SLA定義（必要な場合）
1. SLOより緩い保証値を設定
2. 違反時のペナルティ/クレジット
3. 除外事項（計画メンテナンス等）

### Step F: アラート設定
1. Prometheus Alerting Rules形式
2. Multi-window, Multi-burn-rate アラート推奨
3. 重大度（critical/warning/info）を設定

### Step G: レポート要件
1. 日次/週次/月次レポート内容
2. ダッシュボード構成
3. レビュー会議体制

## 6. 実行例

```bash
/sdd-slo google-ad-report
```

前提:
- .kiro/specs/google-ad-report/requirements.md

出力:
- .kiro/specs/google-ad-report/slo.md
