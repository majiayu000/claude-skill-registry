---
name: system-designer
description: C4モデル（Level 1 System Context + Level 2 Container）を使用してシステム設計図を生成するスキル。Mermaid C4図による視覚化を提供する。
doc_contract:
  review_interval_days: 90
---

# System Designer

Phase 0 Discovery & Architecture パイプラインの Step 1.5C として、C4モデル（Level 1-2）に基づくシステム設計図を生成するスキルです。feature-pilot から呼ばれる Tier 2 Pipeline スキルであり、NEW_FEATURE 専用、Tier XL でのみ実行されます。

---

## 役割分界

> **Option B 原則**: system-designer は CONTEXT.json を直接変更しません。
> feature-architect が CONTEXT.json の `architecture` セクションを更新する責任を持ちます。

```
[feature-pilot] (Tier XL 判定)
  │
  ↓
[feature-architect] → BRIEF.md + CONTEXT.json
  │
  ↓
[domain-modeler] → DOMAIN-MODEL.md (任意)
  │
  ↓
[architecture-selector] → ADR-*.md (任意)
  │
  ↓
[system-designer] → SYSTEM-DESIGN.md (C4 Level 1-2)
  │
  ↓
[Implementation]
```

| スキル                    | 責務                                                     | Output                     | 必須 |
| ------------------------- | -------------------------------------------------------- | -------------------------- | :--: |
| **feature-architect**     | 意図確定、コンテキスト収集、BRIEF.md + CONTEXT.json 生成 | `BRIEF.md`, `CONTEXT.json` | 必須 |
| **domain-modeler**        | ドメインモデル設計                                       | `DOMAIN-MODEL.md`          | 任意 |
| **architecture-selector** | アーキテクチャ決定記録                                   | `ADR-*.md`                 | 任意 |
| **system-designer**       | C4 Level 1-2 システム設計図生成                          | `SYSTEM-DESIGN.md`         | 任意 |

---

## プロトコル (Protocol)

### 0段階: 入力検証 (Input Validation)

1. **feature_id を受け取る**: `--feature-id <feature_id>` 引数から取得
2. **BRIEF.md の存在確認**:
   - `docs/features/<id>-<name>/BRIEF.md` が存在すること（必須）
   - 存在しない場合 → エラー: "BRIEF.md が見つかりません。先に feature-architect を実行してください。"
3. **DOMAIN-MODEL.md の存在確認**（任意参照）:
   - `docs/features/<id>-<name>/DOMAIN-MODEL.md` が存在すれば読み込んで参照
   - 存在しなくても続行可能
4. **ADR-\*.md の存在確認**（任意参照）:
   - `docs/features/<id>-<name>/ADR-*.md` が存在すれば読み込んで参照
   - 存在しなくても続行可能

**検証結果テーブル**:

| BRIEF.md | DOMAIN-MODEL.md | ADR-\*.md |           判定            |
| :------: | :-------------: | :-------: | :-----------------------: |
|   存在   |      存在       |   存在    |      全参照して実行       |
|   存在   |      存在       |   なし    | BRIEF + Domain Model 参照 |
|   存在   |      なし       |   存在    |     BRIEF + ADR 参照      |
|   存在   |      なし       |   なし    |     BRIEF のみで実行      |
|   なし   |        -        |     -     |        エラー中断         |

---

### 1段階: System Boundary Analysis

> **モデル**: haiku（境界スキャン）

1. **システム境界の識別**:
   - BRIEF.md の要求事項から、本機能が影響するシステム範囲を特定
   - 機能が触れるコンテナ/サービスを列挙

2. **外部システム/アクターの列挙**:
   - ユーザー（プレイヤー、管理者等）
   - 外部サービス（Gemini AI, Imagen 3, Live API 等）
   - 既存の内部システムとの接点

3. **データフローの把握**:
   - 主要なデータの流れ（入力 → 処理 → 出力）
   - 非同期処理・バッチ処理の有無

4. **既存システムとの統合ポイント確認**:
   - 既存の API Routes との連携
   - 既存のデータモデルとの関係
   - 既存機能との依存関係（CONTEXT.json の dependencies 参照）

---

### 2段階: C4 Level 1 - System Context Diagram

> **モデル**: sonnet（システム分析）

1. **システム全体のコンテキスト図を生成**:
   - 中心に プロジェクト System を配置
   - 外部ユーザー/アクターを配置
   - 外部システムを配置
   - 関係性（Relationship）を矢印で表現

2. **Mermaid C4Context 図で表現**:
   - `references/mermaid-c4-patterns.md` の構文ガイドに従う
   - 各要素に日本語の説明を付与

3. **コンテキスト図の説明を記述**:
   - 各アクター/システムの役割
   - 主要な関係性の意味

---

### 3段階: C4 Level 2 - Container Diagram

> **モデル**: sonnet（システム分析）

1. **コンテナの識別**:
   - プロジェクト プロジェクトの標準コンテナ:
     - **Next.js Web App: フロントエンド（UI表示、React Hooks 状態管理）
     - **データベース: ゲームデータ（ユーザーデータ、対戦データ）
     - **API Routes: サーバーレスAPI（AI対戦、コンテンツ生成）
     - **Gemini AI: 外部サービス（AI対戦エンジン、コンテンツ生成）
     - **Imagen 3: 外部サービス（画像生成）
     - **Live API: 外部サービス（リアルタイム音声・映像対話）
   - 本機能で追加/変更されるコンテナがあれば追加

2. **コンテナ間の通信プロトコル/データフローを定義**:
   - HTTPS/REST, Next.js Client SDK, Gemini API, Live API 等
   - 同期/非同期の区別

3. **Mermaid C4Container 図で表現**:
   - `references/mermaid-c4-patterns.md` の構文ガイドに従う

---

### 4段階: 出力生成

> **モデル**: sonnet（図表生成）

1. **SYSTEM-DESIGN.md を生成**:
   - 出力先: `docs/features/<id>-<name>/SYSTEM-DESIGN.md`
   - 以下の「出力フォーマット」セクションの構造に従う

2. **完了報告**:

   ```markdown
   ## System Designer 実行完了

   **Feature ID**: <feature_id>
   **出力ファイル**: docs/features/<id>-<name>/SYSTEM-DESIGN.md

   ### 生成内容

   - C4 Level 1: System Context Diagram
   - C4 Level 2: Container Diagram
   - Data Flow: Sequence Diagram
   - Non-Functional Considerations

   > SYSTEM-DESIGN.md を確認してください。
   ```

---

## Model Routing Policy

> **MANDATORY**: Task 道具呼び出し時に `model` パラメータを明示

| 作業タイプ                     | モデル | 根拠                                   |
| ------------------------------ | ------ | -------------------------------------- |
| 境界スキャン (boundary_scan)   | haiku  | 単純なファイル探索・列挙作業           |
| システム分析 (system_analysis) | sonnet | C4図の設計・生成には中程度の推論が必要 |
| 図表生成 (diagram_generation)  | sonnet | Mermaid構文の正確な生成が必要          |

**フォールバック戦略**:

- haiku 失敗 → sonnet 自動昇格
- sonnet 失敗 → opus 自動昇格

---

## 出力フォーマット (SYSTEM-DESIGN.md)

```markdown
# System Design: {feature_title}

## 1. Overview

- Feature ID: {feature_id}
- Generated at: {ISO 8601}
- Input artifacts: BRIEF.md, DOMAIN-MODEL.md (if exists), ADR (if exists)

## 2. System Boundary Analysis

### 2.1 Actors

(本機能に関わるアクター一覧)

### 2.2 External Systems

(本機能に関わる外部システム一覧)

### 2.3 Integration Points

(既存システムとの統合ポイント)

## 3. C4 Level 1: System Context

### 3.1 System Context Diagram

(Mermaid C4Context diagram)

### 3.2 Description

(各要素の説明)

## 4. C4 Level 2: Container

### 4.1 Container Diagram

(Mermaid C4Container diagram)

### 4.2 Container Details

| Container | Technology | Responsibility |
| --------- | ---------- | -------------- |

### 4.3 Communication Protocols

(コンテナ間通信の詳細)

## 5. Data Flow

### 5.1 Primary Data Flow

(Mermaid sequence diagram)

### 5.2 Error Handling Flow

(エラー時のデータフロー)

## 6. Non-Functional Considerations

- Scalability
- Security boundaries
- Performance bottlenecks

## 7. References

- BRIEF: {path}
- Domain Model: {path} (if exists)
- ADR: {path} (if exists)
```

---

## AI 行動指針

### DO (すべきこと)

- C4 Level 1 と Level 2 を必ず両方生成する
- Mermaid C4 拡張構文を使用して図を生成する（`references/mermaid-c4-patterns.md` 参照）
- プロジェクト の既存コンテナ（Next.js, API Routes, Gemini 等）を正確に反映する
- 外部システム連携を漏れなく列挙する
- BRIEF.md の要求事項に基づいてシステム境界を定義する
- DOMAIN-MODEL.md が存在すれば、エンティティをコンテナのデータモデルとして反映する
- ADR-\*.md が存在すれば、アーキテクチャ決定を設計に反映する
- データフローのシーケンス図で主要ユースケースを表現する
- Non-Functional Considerations でスケーラビリティ・セキュリティ・性能を考慮する

### DON'T (してはいけないこと)

- CONTEXT.json を直接変更しない（Option B 原則: feature-architect が責任者）
- C4 Level 3（Component）以下に踏み込まない（Phase 0 では Level 2 まで）
- 実装の詳細に踏み込まない（設計レベルに留まる）
- 存在しないファイル/テーブルを参照しない
- BRIEF.md なしで実行しない（必須入力）
- 標準コンテナ（Next.js Web App, Supabase 等）を省略しない

---

## 使用例

```bash
# Tier XL でのみ使用
/system-designer --feature-id 029-vocabulary-book

# feature-pilot からの自動呼び出し（Tier XL判定時）
# (ユーザーは別途指定不要)
```

---

## 参照文書

- [C4モデルガイド](./references/c4-model-guide.md) - C4モデルの概要と適用方法
- [Mermaid C4パターン](./references/mermaid-c4-patterns.md) - Mermaid C4拡張構文のガイド
- [feature-architect スキル](../feature-architect/SKILL.md) - BRIEF.md / CONTEXT.json 生成
- [feature-pilot スキル](../feature-pilot/SKILL.md) - 上位オーケストレーター

---

## 変更履歴

| 日付       | バージョン | 変更内容                                              |
| ---------- | ---------- | ----------------------------------------------------- |
| 2026-02-11 | v1.0       | Phase 0 Discovery & Architecture パイプライン初期実装 |
