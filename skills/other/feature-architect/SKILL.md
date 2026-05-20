---
name: feature-architect
description: ユーザーストーリー/Why/要求事項/タスクを入力として受け取り、コンテキストを収集しfeature-spec-generatorを呼び出してSPEC.mdとScreen文書を生成します。意図 → 文書変換のオーケストレーターです。
doc_contract:
  review_interval_days: 90
---

# Feature Architect

このスキルは上位レベルのユーザー意図を収集し、コンテキストを分析した後、feature-spec-generatorへ連結するオーケストレーター役割を遂行します。

## 役割分界

> **注意: Option B 原則**: feature-architectは**CONTEXT.json生成の唯一の責任者**です。
> feature-spec-generatorはCONTEXT.jsonが存在してはじめて実行されます。

```
[意図入力]
  |  ユーザーストーリー / Why / 要求事項 / タスク
  |
  v
[feature-architect] ─────────────────────┐
  |  意図分析 + ID割当 + コンテキスト収集  |
  |  CONTEXT.json生成 (必須ゲート)        |
  v──────────────────────────────────────┘
[feature-spec-generator] → SPEC.md + screens/
  |  (CONTEXT.json 必須入力)
  v
[Implementation]
```

| スキル                     | 責務                                                        | Output                     | 必須 |
| -------------------------- | ----------------------------------------------------------- | -------------------------- | :--: |
| **feature-architect**      | 意図確定、コンテキスト収集、**BRIEF.md + CONTEXT.json生成** | `BRIEF.md`, `CONTEXT.json` | 必須 |
| **feature-spec-generator** | CONTEXT + BRIEF基盤で実装契約文書化                         | `SPEC.md`, `screens/*.md`  | 必須 |

**役割分離原則**:

- **Architect**: "何を作るか" (What) - 意図、範囲、コンテキスト定義
- **Spec-Generator**: "どう作るか" (How) - 実装契約、テスト条件文書化

---

## 実行モード (Execution Modes)

### Quickモード (Tier 3用)

> **目的**: 単純な機能(Tier 3)でオーバーヘッドなく迅速にCONTEXT.json生成

**発動条件**:

- argsに `--quick` 含む
- またはfeature-pilotがTier 3と判別した場合自動適用

**Quickモード特性**:

| 項目                 | Standardモード |   Quickモード    |
| -------------------- | :------------: | :--------------: |
| 質問数               |    最大7個     |     最大2個      |
| 収集フィールド       |      全体      |     最小3個      |
| コードベーススキャン |      全体      | 対象ファイルのみ |
| 所要時間             |     2-5分      |      < 30秒      |

**Quickモード必須フィールド** (最小3個):

```json
{
  "feature_id": "XXX-feature-name",
  "title": "機能の日本語タイトル",
  "feature_type": "ui_feature",
  "why": "一行の目的",
  "quick_resume": {
    "current_state": "SpecDrafting",
    "current_task": "feature-spec-generatorでSPEC生成待ち",
    "next_actions": ["SPEC.md生成", "実装開始"],
    "last_updated_at": "ISO 8601時間"
  }
}
```

**QuickモードBRIEF**: Section 0, 1, 2, **7 (完成条件/DoD)** を作成 (残り "N/A - Quickモード")

> **重要**: §7 (完成条件) は Quick モードでも**必須**です。DoD がない BRIEF は Readiness Gate で No-Go になります。

**Quickモードプロトコル**:

1. 入力からtitle, why抽出
2. 次のID自動割当 (既存ロジック)
   2.5. feature-registry.json 自動登録
3. 最小BRIEF.md生成 (Section 0 + 1 + 2 + **7 (完成条件/DoD)**)
4. 最小CONTEXT.json生成 (artifacts.briefパス含む)
5. feature-spec-generator即時呼び出し

**使用例**:

```bash
# 明示的Quickモード
/feature-architect --quick "設定画面にダークモードトグル追加"

# feature-pilotから自動適用 (Tier 3判別時)
# (ユーザーは別途指定不要)
```

---

### Standardモード (デフォルト)

> **目的**: Tier 1-2機能で十分なコンテキスト収集

Standardモードは以下「プロトコル」セクションの全段階に従います。

---

## プロトコル (Protocol)

### 0段階: 入力モード判別 (Input Mode Detection)

> argsの内容に基づきモード決定

**自由形モード (デフォルト)**: 既存プロトコルをそのまま実行

---

### 0.5段階: 冪等性事前検査 (Idempotency Pre-flight)

> 半完了状態を検知して安全に再開する段階

**検査項目**:

1. 対象Featureディレクトリが既に存在するか?
   - `CONTEXT.json`存在 → **スキップ (既に完了)**
   - `CONTEXT.json`なし → **正常進行**

**判定テーブル**:

| CONTEXT存在? |   判定   | アクション                |
| :----------: | :------: | ------------------------- |
|     なし     |   正常   | 全体実行                  |
|     あり     | 既に完了 | スキップ + 案内メッセージ |

---

### 1段階: コンテキスト分析およびID割当 (Context Analysis & ID Assignment)

1. **意図分析 (Analyze Intent)**: ユーザーのリクエストから"Why(目標)"と"Value(ユーザー便益)"を抽出します。

2. **機能ID決定 (Determine Feature ID)** - 必須段階:

   > **重要**: ID重複を防止するため、以下のコマンドを**必ず**実行する必要があります。

   ```bash
   # 必須実行 - docs/features/内の既存ID確認
   ls -d docs/features/[0-9][0-9][0-9]-*/ 2>/dev/null | sed 's/.*\/\([0-9]\{3\}\)-.*/\1/' | sort -n | tail -1
   ```

   - **成功時**: 返された数字(例: `028`)に+1して次のIDを割当 (例: `029`)
   - **失敗/空結果時**: `001`で開始
   - **絶対禁止**: ディレクトリスキャンなしに任意のID使用

   - 機能に対してケバブケース(kebab-case)名を生成します (例: `vocabulary-book`)
   - 最終ID形式: `XXX-feature-name` (例: `029-vocabulary-book`)

3. **テンプレート読み込み (Read Template)**:
   - `docs/_templates/context_template.json`を読んでCONTEXT構造を把握します。

### 2段階: 技術探索および草案作成 (Technical Discovery & Drafting)

1. **コードベーススキャン (Scan Codebase)**: `glob`または`grep`を使用して関連する既存コードを識別します。
   - 関連するコンポーネント/Hook/APIファイル (`src/features/<feature>/`構造)
   - 関連するAPI Routeファイル (`src/app/api/`)
   - 類似機能の既存SPEC文書

2. **制約条件推論 (Infer Constraints)**: コードベースを基に技術的制約条件を提案します。
   - _Hard Constraints (必須)_: 既存スキーマ、主要パッケージ、アーキテクチャパターン (React Hooks, Feature-First + Simplified Clean Architecture, Zod)
   - _Soft Constraints (推奨)_: 特定サービスまたはUIコンポーネントの再利用

3. **入力情報整理**: ユーザー入力から抽出した情報を整理します。
   - ユーザーストーリー、Why、要求事項、タスク分類
   - テスト位置 (例: `tests/unit/features/<feature>/hooks/<name>.test.ts`)

4. **暗黙的要求事項チェック (Implicit Requirements Check)**: ユーザーが明示していないがこの機能に必要な項目をドメインチェックリストで点検します。

   > **原則**: 全項目を機械的に適用しない。該当機能に**関連ある項目のみ**検討し、漏れがあれば`open_questions`に追加する。

   | カテゴリ          | チェック項目                           | 該当時アクション                                    |
   | ----------------- | -------------------------------------- | --------------------------------------------------- |
   | **API Route**     | AI/外部API呼び出しが必要か?            | API Route設計 → references.api_routes               |
   | **エラー/空状態** | データなし/読込失敗時のUIは?           | エラーシナリオ → requirementsに反映                 |
   | **既存機能重複**  | 類似機能が既にあるか?                  | 重複防止 → open_questions                           |
   | **UI Flow影響**   | 新パネル/SSEイベント/状態追加が必要か? | feature_type判定根拠 → open_questionsに影響範囲記録 |

   **出力**: 該当なしの項目は省略。漏れ発見時に要約報告:

   ```markdown
   暗黙的要求事項発見:

   - エラー状態: データなし時の空状態UI未定義 → open_questions追加
   ```

5. **feature_type判定 (Feature Type Classification)**: 意図分析とスキャン結果から機能種別を分類します。

   > **スキーマ契約**: `context_schema.json` により architect が CONTEXT 生成時に**必須設定**。

   | feature_type       | 判定基準                                          | 例                               |
   | ------------------ | ------------------------------------------------- | -------------------------------- |
   | `ui_feature`       | ユーザー対面画面を保有（パネル/ページ追加・変更） | コード分析パネル、クイズ画面     |
   | `backend_feature`  | サーバーロジック専用（API Route, DB処理）         | レート制限、バッチ処理           |
   | `system_feature`   | インフラ/プラットフォーム基盤                     | オフライン同期、プッシュ通知基盤 |
   | `strategy_feature` | ビジネス戦略（UA、リテンション施策）              | A/Bテスト、リファラルプログラム  |

   **判定根拠**: ユーザー入力の意図 + コードベーススキャンの結果 + Implicit Requirements Checkの「UI Flow影響」項目。
   **ui-flow.json読み取りは不要** — What(何を作るか)レベルの分類であり、How(パネル配置)の詳細はspec-generatorが担当。

6. **`CONTEXT.json`草案準備**: スキャン結果と入力情報をCONTEXT構造で準備します。

### 3段階: BRIEF生成 → CONTEXT生成 → spec-generator呼び出し (Brief & Context Creation & Handoff)

> **変更事項**: BRIEF.mdをCONTEXT.jsonの前に生成してユーザー意図を保存

1. **ディレクトリ生成**:
   - ディレクトリ生成: `docs/features/<ID>-<name>/`

1.5. **feature-registry.json 自動登録**:

- `docs/features/feature-registry.json` を読み込む
- `src/features/` に使用されるディレクトリ名（ケバブケース）をキーとして登録
- マッピング: `"{src-dir-name}": "{NNN}-{kebab-name}"` を `mappings` に追加
- **冪等性**: 既に登録済みの場合はスキップ
- **例**: `"vocabulary-book": "029-vocabulary-book"`

```bash
# feature-registry.json に登録（Read → Edit で実行）
# mappings に "{feature-dir-name}": "{feature-id}" を追加
```

2. **BRIEF.md生成** (unified_feature_brief.mdテンプレート使用):
   - `docs/_templates/unified_feature_brief.md`テンプレートを基に生成
   - **Section 0**: ユーザー入力原文を**そのまま**コピー (編集/要約禁止)
   - **Section 1-7**: 意図分析 + コードベーススキャン結果を反映
   - **Section 8**: 空のClarification Log (spec-generatorで追加)
   - **Section 9**: コードベーススキャン結果でContext Map作成
   - ファイルパス: `docs/features/<ID>-<name>/BRIEF.md`

3. **ユーザーへBRIEF要約報告 + レビュー依頼**:

   ```markdown
   BRIEF生成完了

   **機能ID**: 029-vocabulary-book
   **機能名**: 単語帳管理

   ### BRIEF要約

   - **Problem**: 学習した単語を体系的に管理する方法がない
   - **User Stories**: 2個 (US-01, US-02)
   - **Acceptance Criteria**: 3個 (AC-01 ~ AC-03)
   - **Scope**: In 3件, Out 2件

   > BRIEFをレビューしてください。修正が必要であればお知らせください。
   > 問題なければCONTEXT.json生成 + SPEC生成を進めます。
   ```

4. **CONTEXT.json生成** (`artifacts.brief`パス含む):
   - ファイル作成: `docs/features/<ID>-<name>/CONTEXT.json`
   - `artifacts.brief` → BRIEF.mdパス設定
   - `architecture` → `null` に初期化 (スキーマ契約: architect が null 初期化、feature-pilot が Discovery Gate 後に更新)
   - `traceability` → 空の初期値 (spec-generatorで埋める)

5. **feature-spec-generator自動呼び出し**:
   - 収集された入力情報(ユーザーストーリー/Why/要求事項/タスク)を伝達
   - CONTEXT.jsonパスを伝達
   - feature-spec-generatorがSPEC.md + screens/を生成

---

## CONTEXT.json生成ガイド

> **参照**: 詳細スキーマは[context_schema.json](../../docs/_templates/context_schema.json)に定義されています。

スキャン結果を次の形式で記録します:

```json
{
  "schema_version": 7,
  "feature_id": "029-vocabulary-book",
  "title": "単語帳管理",
  "feature_type": "ui_feature",
  "why": "学習した単語を体系的に管理して復習効率向上",
  "user_story": "学習者として単語帳を管理したい",
  "requirements": ["単語追加/削除", "お気に入り機能"],
  "quick_resume": {
    "current_state": "SpecDrafting",
    "current_task": "feature-spec-generatorでSPEC生成中",
    "next_actions": ["SPEC.md完了", "実装開始"],
    "last_updated_at": "2026-01-24T10:30:00+09:00"
  },
  "artifacts": {
    "brief": "docs/features/029-vocabulary-book/BRIEF.md",
    "spec": "docs/features/029-vocabulary-book/SPEC-029-vocabulary-book.md"
  },
  "references": {
    "related_specs": ["docs/features/006-srs-review-system/SPEC-006-srs-review-system.md"],
    "related_code": {
      "components": ["src/features/review/components/*.tsx"],
      "hooks": ["src/features/review/hooks/*.ts"],
      "api": ["src/features/review/api/*.ts"]
    },
    "api_routes": []
  },
  "dependencies": {
    "features": ["006-srs-review-system"],
    "packages": []
  },
  "assumptions": ["既存のデータ構造にvocabularyタイプ追加可能"],
  "open_questions": ["単語あたりの最大例文数制限が必要か?"],
  "history": []
}
```

---

## AI行動指針

### DO (すべきこと)

- **必ず`ls -d docs/features/[0-9][0-9][0-9]-*/`コマンドで既存ID確認** (ID重複防止必須)
- ユーザー入力からユーザーストーリー/Why/要求事項/タスクを明確に抽出
- コードベースをスキャンして実際に存在するファイル参照
- 仮定(Assumptions)と未解決質問(Open Questions)を明示的に記録
- **CONTEXT.json生成後feature-spec-generator自動呼び出し**
- CONTEXT.jsonにreferencesセクションとして関連コード/スペックパスを記録
- **BRIEF.mdをCONTEXT.jsonの前に生成**
- **Section 0にユーザー原文をそのまま保存** (編集/要約禁止)
- **ユーザーにBRIEF要約報告後レビュー依頼**
- **§7 完成条件 (DoD) を必ず生成** (Quick モードでも省略禁止 — 検証可能なテスト + 実装要件)
- **feature-registry.json に自動登録**（ディレクトリ生成後、BRIEF.md生成前）
- **feature_type を必ず設定** (スキーマ契約必須 — null での CONTEXT.json 生成禁止)

### DON'T (してはならないこと)

- **ディレクトリスキャンなしに任意のID(例: 001)割当** — 必ず既存ID確認必須
- 存在しないファイルを参照
- feature-spec-generator呼び出しなしに終了
- **BRIEF.mdなしにCONTEXT.jsonのみ生成** (BRIEF → CONTEXT順序必須)
- **Section 0のユーザー原文を編集/要約**
- **§7 (完成条件/DoD) を省略** (Quick モードでも必須 — Readiness Gate の No-Go 対象)
- **feature-registry.json 登録なしに CONTEXT.json のみ生成** — registry 登録は CONTEXT.json 生成の前提条件
- **feature_type を null のまま CONTEXT.json 生成** — スキーマ契約違反、spec-generator が推論に依存する原因

---

## CONTEXT.json直接生成

> **状態遷移**: `Idle` → `SpecDrafting`

作業完了時**CONTEXT.jsonをテンプレートからコピーして生成**します:

```markdown
## CONTEXT.json生成段階

1. `docs/_templates/context_template.json`コピー → `docs/features/<id>/CONTEXT.json`
2. 基本情報設定:
   - feature_id → 割当された機能ID
   - title → 機能の日本語タイトル
   - why → 入力から抽出したWhy
   - user_story → 入力から抽出したユーザーストーリー
   - requirements → 入力から抽出した要求事項リスト
   - feature_type → 2段階 step 5で判定した機能種別
   - artifacts.brief_format_version → "v2.0" (新規生成時は常に最新テンプレート準拠)
3. quick_resume設定:
   - current_state → "SpecDrafting"
   - current_task → "feature-spec-generatorでSPEC生成中"
   - next_actions → ["SPEC.md完了", "実装開始"]
   - last_updated_at → 現在時刻
4. references設定:
   - related_code → スキャンされた関連コードパス
   - api_routes → 関連API Routes
   - dependencies → 依存機能/パッケージ
5. open_questions設定 (ある場合)
6. historyに最初の遷移記録追加
7. **feature-spec-generator呼び出し** → SPEC.md + screens/生成
```

---

## 使用例

```bash
# ユーザーストーリーで開始
/feature-architect 学習者として単語帳を管理したい

# Whyと要求事項を一緒に提供
/feature-architect --why "復習効率30%向上" --req "単語追加/削除/お気に入り"

# 詳細入力 (複数行)
/feature-architect
Why: 学習した単語を体系的に管理
ユーザーストーリー: 学習者として自分だけの単語帳を作りたい
要求事項:
- 単語追加/削除/修正
- お気に入り機能
```

---

## 参照文書

- [CONTEXT.jsonスキーマ](../../docs/_templates/context_schema.json) - 必須フィールド、状態値enum定義
- [CONTEXT.jsonテンプレート](../../docs/_templates/context_template.json) - 初期値コピー用
- [feature-spec-generatorスキル](../feature-spec-generator/SKILL.md) - SPEC生成担当
- [BRIEFテンプレート](../../docs/_templates/unified_feature_brief.md) - BRIEF.md初期生成用
