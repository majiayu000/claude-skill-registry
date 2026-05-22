---
name: architecture-selector
description: Architecture Drivers分析、代替案比較（3案以上）、ATAM Lite評価マトリクスによるアーキテクチャ選定を行い、ADR（Architecture Decision Record）を生成するスキル。
doc_contract:
  review_interval_days: 90
---

# Architecture Selector

このスキルは Phase 0 Discovery & Architecture の Step 1.5B として、機能のアーキテクチャ選定を体系的に実施します。Architecture Drivers の分析、3案以上の代替案生成、ATAM Lite 評価マトリクスによる客観的比較を行い、最終的に Nygard 形式の ADR（Architecture Decision Record）を出力します。

## 役割分界

> **位置付け**: feature-pilot から呼ばれる Tier 2 Pipeline スキル（NEW_FEATURE専用、Tier L以上で実行）

```
[feature-pilot] ─ NEW_FEATURE (Tier L/XL)
  │
  ├─ [feature-architect] → BRIEF.md + CONTEXT.json
  │     │
  │     ├─ [domain-modeler] → DOMAIN-MODEL.md (optional)
  │     │
  │     └─ [architecture-selector] → ADR-<id>.md  ← ★ このスキル
  │
  └─ [feature-spec-generator] → SPEC.md + screens/
```

| スキル                    | 責務                        | Output                     |     必須     |
| ------------------------- | --------------------------- | -------------------------- | :----------: |
| **feature-architect**     | 意図確定、コンテキスト収集  | `BRIEF.md`, `CONTEXT.json` |      ✅      |
| **domain-modeler**        | ドメインモデル設計          | `DOMAIN-MODEL.md`          |     任意     |
| **architecture-selector** | アーキテクチャ選定、ADR生成 | `ADR-<id>.md`              | ✅ (Tier L+) |

**役割分離原則**:

- **Architect**: "何を作るか" (What) - 意図、範囲、コンテキスト定義
- **Domain Modeler**: "何を扱うか" (Domain) - エンティティ、集約、境界
- **Architecture Selector**: "どう構成するか" (Structure) - アーキテクチャ決定、トレードオフ評価

---

## プロトコル (Protocol)

### 0段階: 入力検証 (Input Validation)

1. **引数受け取り**: `feature_id` と BRIEF.md パスを受け取る
2. **BRIEF.md 存在確認**:
   - `docs/features/<id>-<name>/BRIEF.md` の存在を確認
   - 存在しない場合: エラー終了 `"BRIEF.md が見つかりません。先に feature-architect を実行してください。"`
3. **DOMAIN-MODEL.md 存在確認** (任意):
   - `docs/features/<id>-<name>/DOMAIN-MODEL.md` を検索
   - 存在すれば入力として参照（エンティティ、集約、境界コンテキストの情報を活用）
   - 存在しなくても続行（BRIEF.md の情報のみで分析）
4. **CONTEXT.json 確認**:
   - `docs/features/<id>-<name>/CONTEXT.json` を読み取り、機能の要件・制約を把握

### 0.5段階: Platform Constraints ロード (Platform Constraints Loading)

> **Two-Layer Architecture**: Platform制約を機械的に参照し、Feature ADRの前提制約とする。

1. **constraints.json 存在確認**:
   - `docs/architecture/constraints.json` の存在を確認
   - **存在する場合**: JSON をパースし、`constraints[]` と `tech_stack` を読み込む
     - `constraints[].must` / `constraints[].must_not` を Technical Constraints のベースとして設定
     - `tech_stack` からフレームワーク/バージョン制約を自動設定
     - `deviation_policy` を確認し、逸脱が許可される条件を把握
   - **存在しない場合**: フォールバック動作（1.3段階のハードコード制約を使用）
2. **Platform制約サマリー出力**:
   - 読み込んだ Platform Constraints の一覧をログ表示
   - Feature ADR で逸脱が必要な場合は `Platform Deviation Justification` セクション必須を通知

---

### 1段階: Architecture Drivers 分析 (Architecture Drivers Analysis)

> BRIEF.md、DOMAIN-MODEL.md（存在する場合）、CONTEXT.json、およびコードベーススキャン結果から Architecture Drivers を抽出する。

#### 1.1 Functional Drivers（機能要件からの制約）

機能要件がアーキテクチャに課す制約を特定する:

- データフロー要件（リアルタイム同期、バッチ処理等）
- 統合要件（外部API、Edge Function連携等）
- データ量・種類の制約

#### 1.2 Quality Attribute Drivers（品質属性要件）

> **参照**: [references/quality-attribute-catalog.md](references/quality-attribute-catalog.md)

品質属性の中から、この機能で特に重要なものを特定する:

- Performance Efficiency（応答時間、スループット）
- Security（認証、認可、データ保護）
- Reliability（可用性、障害耐性）
- Maintainability（モジュール性、テスト容易性）
- Usability（学習容易性、操作性）

各属性に重要度（H/M/L）を付与する。

#### 1.3 Technical Constraints（技術的制約）

> **優先参照**: `docs/architecture/constraints.json` が存在する場合、そこから制約を機械的に読み込む。
> 存在しない場合は以下のフォールバック値を使用する。

**constraints.json から自動ロード（存在時）**:

- `constraints[].category` ごとの `must` / `must_not` を展開
- `tech_stack` からフレームワーク/バージョン/パターンを参照

**フォールバック（constraints.json 非存在時）**:

- **アーキテクチャ**: Feature-First + Simplified Clean Architecture + React Hooks 3.1+
- **バックエンド**: API Routes (Next.js)
- **データモデル**: TypeScript + Zod (不変)
- **状態管理**: React Hooks + Custom Hooks（直接DOM操作禁止）
- **プラットフォーム**: Web (モダンブラウザ)

#### 1.4 Business Constraints（ビジネス制約）

- コスト制約（Supabase 無料枠/有料プラン）
- スケジュール制約（MVP 優先順位）
- チーム規模（AI主導開発）
- Japan-First + Global-Ready 戦略

---

### 2段階: Alternatives 生成 (Alternatives Generation)

> 最低3つの代替案を生成する。各案は Architecture Drivers に対する応答として設計する。

#### Option A: 推奨案

- 全ての Architecture Drivers をバランスよく満たす案
- 既存アーキテクチャとの整合性が最も高い案
- 概要、メリット、デメリット、リスクを記述

#### Option B: 代替案

- 特定の品質属性を優先した案（例: パフォーマンス重視）
- Option A とは異なるトレードオフを選択
- 概要、メリット、デメリット、リスクを記述

#### Option C: 最小構成案

- 最小限の実装コストで要件を満たす案
- MVP フェーズに適した軽量アプローチ
- 概要、メリット、デメリット、リスクを記述

#### 追加 Option（必要に応じて）

- 機能の複雑度が高い場合、Option D 以降を追加可能
- 各案は明確に異なるトレードオフを提示すること

---

### 3段階: ATAM Lite Matrix (ATAM Lite Evaluation)

> **参照**: [references/atam-lite-guide.md](references/atam-lite-guide.md)

#### 3.1 評価マトリクス作成

Quality Attributes vs Options のトレードオフマトリクスを作成:

| Quality Attribute | Weight | Option A | Option B | Option C |
| ----------------- | ------ | -------- | -------- | -------- |
| Performance       | H/M/L  | +++/++/+ | +++/++/+ | +++/++/+ |
| Security          | H/M/L  | +++/++/+ | +++/++/+ | +++/++/+ |
| Maintainability   | H/M/L  | +++/++/+ | +++/++/+ | +++/++/+ |
| ...               |        |          |          |          |

評価基準:

- `+++`: 非常に良好（品質属性を完全に満たす）
- `++`: 良好（品質属性を概ね満たす）
- `+`: 最低限（品質属性を最低限満たす）
- `-`: 不十分（品質属性を満たさない）

#### 3.2 Sensitivity Points（変更感度が高い点）

アーキテクチャの小さな変更が品質属性に大きな影響を与えるポイントを特定する。

#### 3.3 Tradeoff Points（品質属性間のトレードオフ）

ある品質属性の改善が他の品質属性の低下を引き起こすポイントを特定する。

#### 3.4 Risk Themes（リスクテーマ）

複数の Sensitivity Points や Tradeoff Points から浮かび上がるリスクのパターンをまとめる。

---

### 4段階: ADR 生成 (ADR Generation)

> **参照**: [references/adr-template.md](references/adr-template.md)

Nygard 形式の ADR を生成し、以下のパスに出力する:

```
docs/features/<id>-<name>/ADR-<id>.md
```

**ADR 構造**:

```markdown
# ADR-{feature_id}: {Decision Title}

## Status

Proposed

## Context

{決定が必要な背景・状況}

## Architecture Drivers

### Functional Drivers

### Quality Attribute Drivers

### Technical Constraints

### Business Constraints

## Alternatives Considered

### Option A: {名前}（推奨）

- Description: ...
- Pros: ...
- Cons: ...
- Risk: ...

### Option B: {名前}

...

### Option C: {名前}

...

## ATAM Lite Evaluation

| Quality Attribute | Weight | Option A | Option B | Option C |
| ----------------- | ------ | -------- | -------- | -------- |
| Performance       | H/M/L  | +++      | ++       | +        |
| Security          | H/M/L  | ++       | +++      | +        |
| ...               |        |          |          |          |

### Sensitivity Points

### Tradeoff Points

### Risk Themes

## Decision

Option {X} を選択する。

## Consequences

### Positive

### Negative

### Risks

## References

- BRIEF: {path}
- Domain Model: {path} (if exists)
```

---

## Model Routing

| タスク               | モデル                | 理由                                                 |
| -------------------- | --------------------- | ---------------------------------------------------- |
| コードベーススキャン | haiku                 | 単純なファイル探索・パターンマッチング               |
| Drivers 分析         | sonnet                | 要件からの制約抽出、標準的な分析タスク               |
| トレードオフ分析     | **opus**              | 品質属性間の複雑なトレードオフ評価に高度な推論が必要 |
| ADR 生成             | sonnet                | 構造化文書の生成、テンプレートベース                 |
| フォールバック       | haiku → sonnet → opus | 3回連続エラー時に自動昇格                            |

---

## AI 行動指針

### DO（すべきこと）

- ✅ 最低3つの代替案を生成する
- ✅ ATAM Lite マトリクスで客観的に評価する
- ✅ プロジェクト プロジェクトの既存アーキテクチャ（Feature-First + Simplified Clean Architecture + React Hooks）を前提制約として考慮する
- ✅ トレードオフ分析に Opus モデルを使用する
- ✅ BRIEF.md の内容を尊重し、ユーザーの意図に沿った選定を行う
- ✅ DOMAIN-MODEL.md が存在する場合、ドメインモデルとの整合性を検証する
- ✅ 各 Option のリスクを明確に記述する
- ✅ Sensitivity Points と Tradeoff Points を具体的に特定する
- ✅ 既存コードベースの実態をスキャンして制約を把握する

### DON'T（してはいけないこと）

- ❌ CONTEXT.json を直接変更しない（Option B 原則: feature-architect が CONTEXT.json の唯一の責任者）
- ❌ 1つの案のみ提示しない（最低3案必須）
- ❌ 既存アーキテクチャと矛盾する案を推奨しない（代替案として提示は可、推奨は不可）
- ❌ Weight なしで評価マトリクスを作成しない（品質属性の重要度は必須）
- ❌ BRIEF.md の存在確認なしに実行しない
- ❌ 根拠なく特定の Option を推奨しない（ATAM Lite の評価結果に基づくこと）

---

## 出力ファイル

| ファイル | パス                                    | 説明                                        |
| -------- | --------------------------------------- | ------------------------------------------- |
| **ADR**  | `docs/features/<id>-<name>/ADR-<id>.md` | Architecture Decision Record（Nygard 形式） |

---

## 使用例

```bash
# Standard モード（Tier L/XL）
/architecture-selector --feature-id 029-vocabulary-book

# feature-pilot パイプラインからの自動呼び出し
# (feature-pilot が Tier L以上と判別した場合に自動実行)
```

---

## 参照文書

- [ADR テンプレートガイド](references/adr-template.md) - Michael Nygard 形式 ADR の書き方
- [ATAM Lite 評価ガイド](references/atam-lite-guide.md) - ATAM Lite マトリクスの作成手順
- [品質属性カタログ](references/quality-attribute-catalog.md) - ISO 25010 ベースの品質属性一覧
- [feature-architect スキル](../feature-architect/SKILL.md) - BRIEF.md / CONTEXT.json 生成元
- [feature-pilot スキル](../feature-pilot/SKILL.md) - 上位オーケストレータ
