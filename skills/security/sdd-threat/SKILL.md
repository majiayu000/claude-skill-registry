---
name: sdd-threat
description: STRIDE脅威モデリングに基づくthreat-model.mdを生成。保護対象資産・信頼境界・脅威・緩和策を定義し、セキュリティ要件を導出する。
argument-hint: "[spec-slug] [target-dir(optional)]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Glob, Grep
model: opus
---

# sdd-threat — STRIDE Threat Modeling Generator

## 0. 目的
- 設計段階でセキュリティリスクを特定
- STRIDE（Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege）で体系的に分析
- 緩和策をセキュリティ要件（REQ-SEC-xxx）として導出

## 1. 入力と出力

### 入力
- /sdd-threat $ARGUMENTS
  - $0 = spec-slug（例: google-ad-report）
  - $1 = target-dir（任意。未指定なら `.kiro/specs/<spec-slug>/` を使う）
- 前提: requirements.md と design.md が存在すること

### 出力（必須）
- <target-dir>/threat-model.md

### 参照
- templates/threat-model.template.md : 脅威モデルテンプレート
- <target-dir>/requirements.md : 要件定義
- <target-dir>/design.md : 設計書

## 2. 重要ルール

1. **STRIDE厳守**: 6カテゴリで網羅的に分析
2. **リスクスコアリング**: 影響度×可能性でリスクレベル算出
3. **緩和策→要件化**: 各緩和策をREQ-SEC-xxxとして要件に追加
4. **信頼境界明確化**: どこでセキュリティ検証が必要か明示

## 3. STRIDEカテゴリ

| カテゴリ | 日本語 | 脅威例 |
|---------|--------|--------|
| **S**poofing | なりすまし | 認証情報盗取、セッションハイジャック |
| **T**ampering | 改ざん | リクエスト改ざん、SQLインジェクション |
| **R**epudiation | 否認 | 操作否認、証跡不備 |
| **I**nformation Disclosure | 情報漏洩 | PII漏洩、エラーメッセージ漏洩 |
| **D**enial of Service | サービス拒否 | DDoS、リソース枯渇 |
| **E**levation of Privilege | 権限昇格 | IDOR、ロールバイパス |

## 4. 手順

### Step A: 入力読み込み
1. design.md からシステム構成を抽出
2. 外部インターフェース、データフローを特定
3. 保護対象資産を列挙

### Step B: 資産の特定
1. データ資産（認証情報、PII、ビジネスデータ等）
2. 機能資産（重要な処理、API）
3. 資産ごとに重要度（Critical/High/Medium/Low）を設定

### Step C: 信頼境界の定義
1. システム境界図（DFD）を作成
2. 各境界での保護機構を明記
3. 境界をまたぐデータフローを特定

### Step D: STRIDE分析
1. 各資産・信頼境界に対してSTRIDE6カテゴリで脅威を列挙
2. 攻撃シナリオを具体的に記述
3. 影響度（Critical/High/Medium/Low）を評価
4. 発生可能性（High/Medium/Low）を評価
5. リスクレベルをマトリックスで算出

### Step E: 緩和策の定義
1. 各脅威に対する緩和策を記述
2. 緩和策を優先度順（P1/P2/P3）にソート
3. 実装コスト（Low/Medium/High）を評価

### Step F: セキュリティ要件の導出
1. 緩和策をREQ-SEC-xxx形式で要件化
2. EARS構文で記述
3. 受入テスト（GWT）を追加

## 5. リスクマトリックス

```
        │ Low        Medium      High        Critical
────────┼───────────────────────────────────────────────
High    │ Medium     High        Critical    Critical
Medium  │ Low        Medium      High        Critical
Low     │ Low        Low         Medium      High
────────┼───────────────────────────────────────────────
可能性  │                     影響度
```

## 6. 実行例

```bash
/sdd-threat google-ad-report
```

前提:
- .kiro/specs/google-ad-report/requirements.md
- .kiro/specs/google-ad-report/design.md

出力:
- .kiro/specs/google-ad-report/threat-model.md
