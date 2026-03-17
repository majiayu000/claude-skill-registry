---
name: platform-architect
description: |
  Platform Architecture の初期構築とメンテナンスを担当するスキル。
  CLAUDE.md / tech-stack-rules.md / feature-first-architecture.md から暗黙のアーキテクチャ決定を抽出し、
  PADR（Platform ADR）、constraints.json、PLATFORM-ARCHITECTURE.md を生成・更新する。

  プロジェクト開始時の初期構築、または新技術導入・大規模変更時のメンテナンスで使用する。

  <example>
  user: "プラットフォームアーキテクチャを文書化して"
  assistant: "platform-architect を使用して Platform Architecture を構築します"
  </example>

  <example>
  user: "新しいバックエンド技術を導入する際のアーキテクチャ影響を評価して"
  assistant: "platform-architect を使用して Platform Architecture を更新します"
  </example>
doc_contract:
  review_interval_days: 180
---

# Platform Architect

> **核心コンセプト**: "暗黙知の明示化、人間+AI二重可読、長期運用"

Platform Architecture（Layer 1）の構築・メンテナンスを担当するスキル。
全機能に適用される共通アーキテクチャ制約を体系的に文書化する。

---

## 役割分界

> **位置付け**: ユーザー直接呼び出し（パイプライン外の独立スキル）

```
Two-Layer Architecture
│
├── Layer 1: Platform Architecture ← ★ このスキルが管理
│   ├── PADR-*.md (Platform ADR)
│   ├── constraints.json (機械可読制約)
│   ├── PLATFORM-ARCHITECTURE.md (Arc42ベース)
│   ├── tech-radar.md (ThoughtWorks形式)
│   ├── c4/platform-c4.md (C4 Level 1-2)
│   └── cross-cutting/ (横断的関心事)
│
└── Layer 2: Feature Architecture ← architecture-selector が管理
    └── docs/features/<id>/ADR-<id>.md
```

| スキル                    | 責務                     | 更新頻度 |
| ------------------------- | ------------------------ | -------- |
| **platform-architect**    | Platform全体の制約管理   | 年1-2回  |
| **architecture-selector** | 機能別アーキテクチャ選定 | 機能ごと |

**Architecture Contract Pattern**:

- **PADR-\*.md**: Why/Context（人間可読）
- **constraints.json**: What/Must/Must-Not（AI/機械可読）

---

## プロトコル (Protocol) - 5フェーズ

### Phase 1: Inventory（棚卸し）

> 既存文書からアーキテクチャ決定を収集する。

**入力文書**（優先順位順）:

1. `CLAUDE.md` - プロジェクトガイドライン、ルール
2. `docs/technical/tech-stack-rules.md` - 技術スタック詳細
3. `docs/technical/feature-first-architecture.md` - アーキテクチャガイド
4. `docs/development/enhanced-pipeline-proposal.md` - パイプライン提案（Appendix B）

**抽出対象**:

- 暗黙的に決定されているが ADR化されていないアーキテクチャ決定
- 技術スタックの選定理由（なぜその技術を選んだか）
- 制約（Must / Must-Not）
- 品質属性の優先順位

**出力**: 暗黙決定リスト（ID、カテゴリ、決定内容、出典文書）

---

### Phase 2: PADR Generation（Platform ADR 生成）

> 各暗黙決定を Nygard 形式 PADR として文書化する。

**PADR 構造**:

```markdown
# PADR-NNN: {タイトル}

## Status

Accepted (遡及作成: YYYY-MM-DD)

## Context

{決定が必要だった背景}

## Architecture Drivers

### Functional Drivers

### Quality Attribute Drivers

### Technical Constraints

### Business Constraints

## Alternatives Considered

### Option A: {名前}（採用）

### Option B: {名前}（不採用）

### Option C: {名前}（不採用）

## ATAM Lite Evaluation

| Quality Attribute | Weight | Option A | Option B | Option C |
|...

## Decision

Option A を選択する。{根拠}

## Consequences

### Positive

### Negative

### Risks

## Rules（制約）

- Must: ...
- Must Not: ...

## References
```

**命名規則**:

- 接頭辞: `PADR-NNN`（Feature ADR の `ADR-<feature_id>` と区別）
- 配置: `docs/architecture/adr/`
- ステータス: `Accepted`（遡及作成のため）

---

### Phase 3: Contract Generation（constraints.json 生成）

> PADR から constraints.json（機械可読制約）を自動生成する。

**スキーマ**: [references/constraints-schema.json](references/constraints-schema.json)

**各 constraint の構造**:

```json
{
  "id": "PC-NNN",
  "source_padr": "PADR-NNN",
  "category": "architecture|state_management|backend|data_model|...",
  "rule": "ルール名",
  "description": "説明",
  "must": ["必須事項1", "必須事項2"],
  "must_not": ["禁止事項1", "禁止事項2"],
  "applies_to": ["glob パターン"],
  "override_allowed": false,
  "enforcement": "critical|high|medium"
}
```

**生成ルール**:

- 各 PADR の `Rules（制約）` セクションから Must/Must-Not を抽出
- `applies_to` は影響範囲のファイルグロブパターン
- `enforcement` は品質属性の Weight から決定（H→critical, M→high, L→medium）

---

### Phase 4: Platform Doc Generation（PLATFORM-ARCHITECTURE.md 生成）

> Arc42 ベース 10 セクション構成のプラットフォーム全体像文書を生成する。

**テンプレート**: [references/platform-architecture-template.md](references/platform-architecture-template.md)

|  #  | セクション             | 内容源                      |
| :-: | ---------------------- | --------------------------- |
|  1  | Introduction & Goals   | CLAUDE.md, business context |
|  2  | Constraints            | constraints.json            |
|  3  | Context & Scope        | c4/platform-c4.md           |
|  4  | Solution Strategy      | PADR-001~006                |
|  5  | Building Blocks        | c4/platform-c4.md (Level 2) |
|  6  | Runtime View           | 主要ユースケースシーケンス  |
|  7  | Deployment View        | Vercel + Next.js デプロイ      |
|  8  | Cross-Cutting Concepts | cross-cutting/\*.md         |
|  9  | Architecture Decisions | PADR サマリー               |
| 10  | Tech Radar             | tech-radar.md               |

**付随ファイル**:

- `tech-radar.md` - ThoughtWorks Tech Radar 形式
- `c4/platform-c4.md` - Mermaid C4 Level 1-2
- `cross-cutting/*.md` - エラーハンドリング、ログ、セキュリティ

---

### Phase 5: Verification（検証）

> constraints.json ↔ PADR 整合性チェック。

**検証項目**:

|  #  | チェック                      | 合格条件                                |
| :-: | ----------------------------- | --------------------------------------- |
|  1  | constraints.json JSON構文     | パースエラーなし                        |
|  2  | PADR ↔ constraint マッピング  | 各PADRに対応するPC-NNNが存在            |
|  3  | Must/Must-Not 網羅性          | PADRのRulesセクションがconstraintに反映 |
|  4  | applies_to パスの妥当性       | globパターンが実際のファイル構造に一致  |
|  5  | tech-radar ↔ constraints 一致 | Adopt技術がconstraintsに反映            |
|  6  | 相互参照の有効性              | 文書間のリンクが有効                    |

**出力**: 検証結果レポート（Pass/Fail + 詳細）

---

## Model Routing

| タスク                           | モデル   | 理由                               |
| -------------------------------- | -------- | ---------------------------------- |
| 文書スキャン（Phase 1）          | haiku    | 単純な情報抽出                     |
| PADR 生成（Phase 2）             | sonnet   | 構造化文書生成                     |
| constraints.json 生成（Phase 3） | sonnet   | JSON生成、パターンマッチング       |
| Platform Doc 生成（Phase 4）     | sonnet   | 大規模文書生成                     |
| ATAM Lite 評価                   | **opus** | トレードオフ分析に高度な推論が必要 |
| 検証（Phase 5）                  | haiku    | パターンマッチング                 |

---

## AI 行動指針

### DO（すべきこと）

- ✅ 既存文書（CLAUDE.md, tech-stack-rules.md）を忠実にPADR化する
- ✅ 各PADRに最低3つの代替案を含める
- ✅ constraints.json のスキーマを厳密に守る
- ✅ PADR と constraints.json の整合性を検証する
- ✅ 業界標準（Arc42, ATAM, Tech Radar）に準拠する
- ✅ Two-Layer Architecture の分離を維持する（Platform vs Feature）
- ✅ deviation_policy を明文化する

### DON'T（してはいけないこと）

- ❌ Feature-level の決定を Platform ADR に含めない
- ❌ constraints.json に PADR にない制約を追加しない
- ❌ 既存の CLAUDE.md ルールと矛盾する PADR を作成しない
- ❌ ATAM Lite 評価なしに決定を記録しない
- ❌ 検証（Phase 5）をスキップしない

---

## 出力ファイル

| ファイル                     | パス                                         | 説明                       |
| ---------------------------- | -------------------------------------------- | -------------------------- |
| **PADR**                     | `docs/architecture/adr/PADR-NNN-*.md`        | Platform ADR               |
| **constraints.json**         | `docs/architecture/constraints.json`         | 機械可読制約               |
| **PLATFORM-ARCHITECTURE.md** | `docs/architecture/PLATFORM-ARCHITECTURE.md` | Arc42ベース全体像          |
| **tech-radar.md**            | `docs/architecture/tech-radar.md`            | 技術採用状況               |
| **C4 図**                    | `docs/architecture/c4/platform-c4.md`        | C4 Level 1-2               |
| **横断的関心事**             | `docs/architecture/cross-cutting/*.md`       | エラー、ログ、セキュリティ |

---

## 使用例

```bash
# 初回構築（全Phase実行）
/platform-architect

# 特定フェーズのみ実行
/platform-architect --phase inventory
/platform-architect --phase verify

# 新技術追加時の更新
/platform-architect --update "新技術名の追加"
```

---

## 実行タイミング

| タイミング                   | アクション                     |
| ---------------------------- | ------------------------------ |
| **プロジェクト開始時**       | 全Phase実行（初期構築）        |
| **新技術導入時**             | Phase 2-5（新PADR追加 + 更新） |
| **大規模リファクタリング時** | Phase 1-5（全体再評価）        |
| **四半期レビュー**           | Phase 5（検証のみ）            |

---

## 参照文書

- [constraints.json スキーマ](references/constraints-schema.json) - 機械可読制約のJSONスキーマ
- [Platform Architecture テンプレート](references/platform-architecture-template.md) - Arc42テンプレート
- [architecture-selector スキル](../architecture-selector/SKILL.md) - Feature-level ADR（Layer 2）
- [feature-pilot スキル](../feature-pilot/SKILL.md) - パイプラインオーケストレータ
- [enhanced-pipeline-proposal.md](../../docs/development/enhanced-pipeline-proposal.md) - Appendix B
