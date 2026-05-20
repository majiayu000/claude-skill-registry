---
name: domain-modeler
description: |
  DDD Strategic Patterns + Event Storming Liteを使用してドメインモデルを作成するスキル。Bounded Context識別、Ubiquitous Language定義、ドメインイベント洗い出しを行う。

  **核心機能**:
  - Event Storming Lite（Commands → Events → Aggregates）
  - Bounded Context 識別 + Context Map 生成
  - Ubiquitous Language（日英韓3言語）定義

  "domain model", "ドメインモデル", "DDD", "bounded context" 等の要求でトリガーされる。

  <example>
  user: "029-vocabulary-book のドメインモデルを作成して"
  assistant: "domain-modelerを使用してドメインモデル分析を実行します"
  </example>
doc_contract:
  review_interval_days: 90
---

# Domain Modeler（ドメインモデラー）

> **核心コンセプト**: "戦略レベルのドメイン理解を文書化し、実装の基盤を構築する"

Phase 0 Discovery & Architecture パイプラインの Step 1.5A として、BRIEF.md の内容に基づきドメインモデルを分析・生成するスキルです。feature-pilot から呼ばれる Tier 2 Pipeline スキルであり、**NEW_FEATURE 専用**です（MODIFY_FEATURE, BUG_FIX 等では呼ばれません）。

---

## 役割分界

> **Option B 原則**: domain-modeler は CONTEXT.json を直接変更しません。
> feature-architect が CONTEXT.json の `architecture.domain_model` セクションを更新します。

```
[feature-pilot]
  │  NEW_FEATURE 判定
  ↓
[feature-architect] → BRIEF.md + CONTEXT.json 生成
  │
  ↓
[domain-modeler] ──────────────────────────────┐
  │  BRIEF.md 読み込み                          │
  │  Event Storming Lite + Strategic DDD        │
  │  ★ DOMAIN-MODEL.md 生成                    │
  ↓──────────────────────────────────────────────┘
[feature-architect] → CONTEXT.json 更新（architecture.domain_model）
```

| スキル                | 責務                             | Output              | 必須 |
| --------------------- | -------------------------------- | ------------------- | :--: |
| **domain-modeler**    | ドメイン分析、BC識別、用語集生成 | `DOMAIN-MODEL.md`   |  ✅  |
| **feature-architect** | CONTEXT.json への分析結果反映    | `CONTEXT.json` 更新 |  ✅  |

**役割分離原則**:

- **Domain Modeler**: "ドメインをどう理解するか"（Strategic DDD）- BC、用語、イベント
- **Feature Architect**: "何を作るか"（What）- 意図、範囲、コンテキスト管理

---

## 実行モード (Execution Modes)

### Standard モード（デフォルト）

> **目的**: Tier L/XL の機能で Event Storming を含む完全なドメイン分析

全段階（0〜5）を実行します。

### Lightweight モード（--lightweight）

> **目的**: Tier M の機能でオーバーヘッドなく最小限のドメイン分析

**発動条件**:

- args に `--lightweight` を含む
- または feature-pilot が Tier M と判別した場合に自動適用

**Lightweight モード特性**:

| 項目           | Standard モード | Lightweight モード |
| -------------- | :-------------: | :----------------: |
| Event Storming |    完全実行     |      スキップ      |
| BC 識別        |    完全実行     |      簡易実行      |
| 用語集         |  完全（3言語）  |   完全（3言語）    |
| ドメインルール |      完全       |       最小限       |
| 所要時間       |      3-5分      |       < 1分        |

---

## プロトコル (Protocol)

### 0段階: 入力検証 (Input Validation)

1. **引数確認**: `feature_id` と BRIEF.md パスを受け取る
2. **BRIEF.md 存在確認**: ファイルが存在しない場合は即時中断
3. **フラグ確認**: `--lightweight` フラグの有無を確認
4. **Feature ディレクトリ確認**: `docs/features/<id>-<name>/` が存在することを確認

```
検証チェックリスト:
✅ feature_id が有効な形式（XXX-feature-name）
✅ BRIEF.md が存在し読み取り可能
✅ Feature ディレクトリが存在
✅ --lightweight フラグの判定完了
```

**検証失敗時**: エラーメッセージを出力し、即時中断。

---

### 1段階: Context Ingestion（コンテキスト取得）

1. **BRIEF.md 読み込み**:
   - Problem/JTBD セクションからドメインの問題領域を把握
   - User Stories からアクターとアクションを抽出
   - Acceptance Criteria からビジネスルールの候補を識別

2. **既存コードベーススキャン**（model: haiku）:
   - `lib/` 配下の関連ドメインコード探索
   - 既存の Model/Repository/Service の構造把握
   - 関連する DB テーブル（migrations フォルダ）確認

3. **関連 SPEC 文書の参照**:
   - `docs/features/` 配下の関連 SPEC 文書を確認
   - 既存ドメインとの境界・依存関係を把握

---

### 2段階: Event Storming Lite（--lightweight の場合はスキップ）

> **参照**: [references/event-storming-patterns.md](references/event-storming-patterns.md)

1. **ドメインイベント洗い出し**:
   - BRIEF.md の User Stories/Acceptance Criteria からイベントを抽出
   - イベント命名規則: 過去形（例: `VocabularyAdded`, `ReviewCompleted`）
   - 各イベントにトリガー条件と結果を記録

2. **Commands → Events → Aggregates 変換**:
   - ユーザーアクション → Command 識別
   - Command の結果 → Event 定義
   - Event のオーナー → Aggregate 識別

3. **イベントフロー図（Mermaid）生成**:

   ```mermaid
   sequenceDiagram
       actor User
       participant Command
       participant Aggregate
       participant Event
       User->>Command: AddVocabulary
       Command->>Aggregate: Vocabulary
       Aggregate->>Event: VocabularyAdded
   ```

4. **主要ビジネスルール識別**:
   - 各 Aggregate に属するインバリアント（不変条件）を定義
   - ビジネスルールに ID を付与（BR-01, BR-02, ...）

---

### 3段階: Strategic DDD

> **参照**: [references/ddd-strategic-patterns.md](references/ddd-strategic-patterns.md)

1. **Bounded Context 識別**:
   - 1段階で収集したドメイン知識から BC を識別
   - 各 BC の責務範囲を明確化
   - BC 名は英語（PascalCase）で統一

2. **Context Map（関係性マッピング）**:
   - BC 間の関係をパターンで定義:
     - Shared Kernel
     - Customer-Supplier
     - Conformist
     - Anti-Corruption Layer (ACL)
     - Open Host Service / Published Language
   - Mermaid C4/flowchart 図で可視化

3. **ドメイン分類**:
   - **Core Domain**: プロジェクトの競争優位性を生む中核領域
   - **Supporting Domain**: Core を支援するが差別化要素ではない領域
   - **Generic Domain**: 汎用的で既存ソリューションで代替可能な領域

---

### 4段階: Ubiquitous Language（ユビキタス言語）

1. **ドメイン用語集（日英対応）**:
   - 英語（Term）: コード内で使用する正式名称
   - 日本語: ドキュメント・UI 表示用

2. **用語間の関係性マッピング**:
   - IS-A（継承関係）
   - HAS-A（構成関係）
   - USES（利用関係）

3. **用語テーブル形式**:

   | Term (EN)  | 日本語 | Definition     | Context           |
   | ---------- | ------ | -------------- | ----------------- |
   | Vocabulary | 単語   | 学習対象の単語 | VocabularyContext |

---

### 5段階: 出力生成 (Output Generation)

1. **DOMAIN-MODEL.md 生成**:
   - 出力先: `docs/features/<id>-<name>/DOMAIN-MODEL.md`
   - 下記の出力フォーマットに従って生成

2. **完了報告**:
   - 生成されたファイルパスを報告
   - 主要な発見事項（BC 数、用語数、ビジネスルール数）を要約

---

## 出力フォーマット（DOMAIN-MODEL.md の構造）

```markdown
# Domain Model: {feature_title}

## 1. Overview

- Feature ID: {feature_id}
- Generated at: {ISO 8601}
- Mode: Standard | Lightweight
- Source: {BRIEF.md パス}

## 2. Event Storming (Standard mode only)

### 2.1 Domain Events

| Event | Trigger | Result | Aggregate |
| ----- | ------- | ------ | --------- |

### 2.2 Commands & Aggregates

| Command | Actor | Aggregate | Pre-conditions |
| ------- | ----- | --------- | -------------- |

### 2.3 Event Flow

(Mermaid sequence diagram)

## 3. Bounded Contexts

### 3.1 Context Map

(Mermaid C4/flowchart diagram)

### 3.2 Context Details

#### Core Domain

- {BC名}: {責務説明}

#### Supporting Domain

- {BC名}: {責務説明}

#### Generic Domain

- {BC名}: {責務説明}

## 4. Ubiquitous Language

| Term (EN) | 日本語 | Definition | Context |
| --------- | ------ | ---------- | ------- |

## 5. Domain Rules

- BR-01: {ビジネスルール記述}
- BR-02: {ビジネスルール記述}

## 6. Recommendations for Architecture

- 推奨パターン
- 注意すべきトレードオフ
- 既存コードベースとの統合ポイント
```

---

## Model Routing Policy（モデル政策）

> **MANDATORY**: Task 実行時に必ず `model` パラメータを明示

| 作業タイプ           | モデル | 根拠                                               |
| -------------------- | ------ | -------------------------------------------------- |
| コードベーススキャン | haiku  | ファイル探索・パターンマッチングは軽量モデルで十分 |
| ドメイン分析         | sonnet | BC 識別・用語定義には標準的な推論力が必要          |
| Event Storming       | sonnet | イベントフロー分析には中程度の推論力が必要         |

**フォールバック戦略**:

- haiku 失敗 → sonnet 自動昇格
- sonnet 失敗 → opus 自動昇格

---

## 核心原則

1. **戦略レベル維持**: 実装の詳細に踏み込まず、ドメインの戦略的理解に留まる
2. **BRIEF 忠実性**: BRIEF.md の内容に忠実にドメインモデルを生成する
3. **既存パターン尊重**: 既存コードベースの構造・命名パターンを踏襲する
4. **日英対応**: 用語集には必ず英語・日本語の2言語を含める

---

## AI 行動指針

### DO（すべきこと）

- BRIEF.md の内容に忠実にドメインモデルを生成
- 既存コードベースのパターンを尊重
- 用語集に2言語（日英）を含める
- Mermaid 図を使用して視覚的に表現
- BC 間の関係を明確にパターンで定義
- ビジネスルールに一意の ID を付与
- Lightweight モード時は Event Storming をスキップ

### DON'T（してはいけないこと）

- CONTEXT.json を直接変更しない（Option B 原則）
- 実装の詳細に踏み込まない（戦略レベルに留まる）
- 存在しないファイルを参照しない
- BRIEF.md にない情報を勝手に追加しない
- BC の粒度を細かくしすぎない（機能単位で適切に）

---

## 制約事項

| 制約                        | 理由                                     | 違反時                |
| --------------------------- | ---------------------------------------- | --------------------- |
| CONTEXT.json 直接変更禁止   | Option B 原則 - feature-architect が管理 | 即時中断              |
| 実装詳細への踏み込み禁止    | 戦略レベル分析に専念                     | 該当セクション削除    |
| BRIEF.md 非存在時の実行禁止 | 入力ソース不在                           | 即時中断 + エラー報告 |

---

## 実行フロー

```
0段階: 入力検証
  │  feature_id + BRIEF.md 確認 + --lightweight 判定
  ↓
1段階: Context Ingestion
  │  BRIEF.md 読み込み + コードベーススキャン + 関連 SPEC 参照
  ↓
2段階: Event Storming Lite (--lightweight 時スキップ)
  │  Events → Commands → Aggregates + Mermaid 図
  ↓
3段階: Strategic DDD
  │  BC 識別 + Context Map + Core/Supporting/Generic 分類
  ↓
4段階: Ubiquitous Language
  │  用語集（日英韓）+ 関係性マッピング
  ↓
5段階: 出力生成
  │  DOMAIN-MODEL.md 生成 + 完了報告
  ↓
完了
```

---

## 使用例

```bash
# Standard モード（Tier L/XL）
/domain-modeler --feature-id 029-vocabulary-book

# Lightweight モード（Tier M）
/domain-modeler --feature-id 029-vocabulary-book --lightweight
```

---

## 参照文書

- [Event Storming パターンガイド](./references/event-storming-patterns.md) - Event Storming Lite の実行パターン
- [DDD Strategic パターンガイド](./references/ddd-strategic-patterns.md) - BC 識別・Context Map パターン
- [CONTEXT.json スキーマ](../../docs/_templates/context_schema.json) - CONTEXT.json の構造定義
- [BRIEF テンプレート](../../docs/_templates/unified_feature_brief.md) - BRIEF.md の構造定義
- [feature-architect スキル](../feature-architect/SKILL.md) - 上位スキル（CONTEXT.json 管理者）

---

## 変更履歴

| 日付       | バージョン | 変更内容                                                         |
| ---------- | ---------- | ---------------------------------------------------------------- |
| 2026-02-11 | v1.0       | 新規生成 - Phase 0 Discovery & Architecture パイプライン初期実装 |
