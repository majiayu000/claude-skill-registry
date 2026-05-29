---
name: cryptographic-practices
description: |
  暗号化・ハッシュ・CSPRNG・鍵管理の実装を安全に進めるためのスキル。
  要件整理から設計、実装、監査までの一連フローを提供する。

  Anchors:
  • Applied Cryptography / 適用: アルゴリズム選定と強度判断 / 目的: 標準準拠の基礎固め
  • Web Application Security / 適用: 脅威モデリング / 目的: 実装リスクの明確化
  • NIST SP 800-57 / 適用: 鍵管理 / 目的: ライフサイクル設計

  Trigger:
  Use when implementing cryptographic functions, selecting algorithms, generating secure random values, managing encryption keys, or auditing crypto implementations.
  cryptographic practices, crypto implementation, key management, csprng, algorithm selection
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# cryptographic-practices

## 概要

暗号実装に必要な判断基準と実装手順を整理し、安全なアルゴリズム選定・鍵管理・乱数生成を支援する。

## ワークフロー

### Phase 1: 要件整理

**目的**: 目的・脅威・制約を整理し、暗号要件を明確化する。

**アクション**:

1. 保護対象と脅威を整理する。
2. 目的（機密性/完全性/認証/署名）を明確化する。
3. 既存実装の有無を確認する。

**Task**: `agents/analyze-crypto-requirements.md` を参照

### Phase 2: 設計

**目的**: アルゴリズムと鍵管理の方針を設計する。

**アクション**:

1. `references/algorithm-strength-guide.md` で強度を確認する。
2. `references/key-management-policy.md` で鍵ライフサイクルを設計する。
3. `references/csprng-implementation.md` で乱数生成方針を整理する。

**Task**: `agents/design-crypto-architecture.md` を参照

### Phase 3: 実装

**目的**: 安全な実装と検出を行う。

**アクション**:

1. 設計方針を実装に反映する。
2. `scripts/detect-weak-crypto.mjs` で弱い実装を検出する。
3. 変更点を記録する。

**Task**: `agents/implement-crypto-controls.md` を参照

### Phase 4: 検証と監査

**目的**: 実装の安全性を検証し、監査記録を残す。

**アクション**:

1. `assets/crypto-audit-checklist.md` で監査する。
2. 監査結果をテンプレートに整理する。
3. `scripts/log_usage.mjs` で記録を更新する。

**Task**: `agents/validate-crypto-implementation.md` を参照

## Task仕様ナビ

| Task                           | 起動タイミング | 入力           | 出力                         |
| ------------------------------ | -------------- | -------------- | ---------------------------- |
| analyze-crypto-requirements    | Phase 1開始時  | 目的/制約/脅威 | 暗号要件メモ、リスク一覧     |
| design-crypto-architecture     | Phase 2開始時  | 暗号要件メモ   | アルゴリズム設計、鍵管理方針 |
| implement-crypto-controls      | Phase 3開始時  | 設計方針       | 実装変更メモ、検出結果       |
| validate-crypto-implementation | Phase 4開始時  | 実装変更メモ   | 監査レポート、改善提案       |

**詳細仕様**: 各Taskの詳細は `agents/` ディレクトリを参照

## ベストプラクティス

### すべきこと

| 推奨事項                         | 理由                 |
| -------------------------------- | -------------------- |
| 脅威モデルから設計する           | 要件と実装が一致する |
| 標準アルゴリズムを使う           | 自作暗号のリスク回避 |
| CSPRNGを使用する                 | 予測可能性の排除     |
| 鍵管理をライフサイクルで設計する | 漏洩リスクを抑える   |
| 監査ログを残す                   | 再現性と証跡の確保   |

### 避けるべきこと

| 禁止事項                | 問題点               |
| ----------------------- | -------------------- |
| 弱いアルゴリズムの採用  | 既知の脆弱性を抱える |
| 乱数にMath.randomを使う | 予測可能で危険       |
| 鍵のハードコード        | 漏洩リスクが高い     |
| 監査なしのデプロイ      | 安全性が担保できない |

## リソース参照

### scripts/（決定論的処理）

| スクリプト                       | 機能                         |
| -------------------------------- | ---------------------------- |
| `scripts/detect-weak-crypto.mjs` | 弱い暗号実装の検出           |
| `scripts/validate-skill.mjs`     | スキル構造の検証             |
| `scripts/log_usage.mjs`          | 使用記録と評価メトリクス更新 |

### references/（詳細知識）

| リソース     | パス                                                                             | 読込条件           |
| ------------ | -------------------------------------------------------------------------------- | ------------------ |
| レベル1 基礎 | [references/Level1_basics.md](references/Level1_basics.md)                       | 要件整理時         |
| レベル2 実務 | [references/Level2_intermediate.md](references/Level2_intermediate.md)           | 設計時             |
| レベル3 応用 | [references/Level3_advanced.md](references/Level3_advanced.md)                   | 実装時             |
| レベル4 専門 | [references/Level4_expert.md](references/Level4_expert.md)                       | 監査時             |
| 強度ガイド   | [references/algorithm-strength-guide.md](references/algorithm-strength-guide.md) | アルゴリズム選定時 |
| CSPRNG実装   | [references/csprng-implementation.md](references/csprng-implementation.md)       | 乱数設計時         |
| 鍵管理方針   | [references/key-management-policy.md](references/key-management-policy.md)       | 鍵運用設計時       |
| 脅威整理     | [references/threat-modeling.md](references/threat-modeling.md)                   | 目的整理時         |
| 要求仕様索引 | [references/requirements-index.md](references/requirements-index.md)             | 仕様確認時         |
| 旧スキル     | [references/legacy-skill.md](references/legacy-skill.md)                         | 互換確認時         |

### assets/（テンプレート・素材）

| アセット                                 | 用途                 |
| ---------------------------------------- | -------------------- |
| `assets/crypto-audit-checklist.md`       | 監査チェックリスト   |
| `assets/encryption-config-template.json` | 暗号設定テンプレート |
| `assets/key-rotation-plan.md`            | 鍵ローテーション計画 |
| `assets/crypto-audit-report-template.md` | 監査レポート         |

### 運用ファイル

| ファイル       | 目的                       |
| -------------- | -------------------------- |
| `EVALS.json`   | レベル評価・メトリクス管理 |
| `LOGS.md`      | 実行ログの蓄積             |
| `CHANGELOG.md` | 改善履歴の記録             |
