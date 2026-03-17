---
name: feature-spec-generator
description: ユーザーストーリー、Why、要求事項を入力として受け取り、実装可能なSPEC.mdとScreen文書を生成するスキル。開発者の意図をAIが実装できる契約文書に変換する。
doc_contract:
  review_interval_days: 90
---

# Feature Spec Generator

> **コアコンセプト**: "意図 → 契約"の変換器 (Intent to Contract)

このスキルは開発者が入力した**ユーザーストーリー、Why(目的)、要求事項**を受けて、AIが実装できる具体的な契約文書(SPEC/Screen)に変換します。

## 入力形式

> **必須前提条件**: `CONTEXT.json`が必ず存在しなければなりません。
> CONTEXT.jsonは**feature-architect**が生成します。このスキルはCONTEXT.jsonを**読み取りのみ**行います。

### 必須入力

| 入力             | 説明                          | 例                                               |
| ---------------- | ----------------------------- | ------------------------------------------------ |
| **機能ID**       | feature-architectが割当てたID | `029-vocabulary-book`                            |
| **CONTEXT.json** | 機能ディレクトリに存在        | `docs/features/029-vocabulary-book/CONTEXT.json` |

### 選択的追加入力

以下はCONTEXT.jsonの情報を補完または具体化する際に使用します:

| 入力タイプ       | 説明                      | 例                       |
| ---------------- | ------------------------- | ------------------------ |
| **追加要求事項** | CONTEXTにない詳細要求事項 | "オフライン同期サポート" |
| **制約条件**     | 追加的な技術/ビジネス制約 | "既存データ構造の再利用" |

---

## プロトコル (Protocol)

### Phase 0: CONTEXT.json検証 (Context Validation)

> **必須前提**: feature-architectが生成したCONTEXT.jsonが存在しなければなりません。

1. **CONTEXT.json存在確認**:

   ```
   docs/features/<機能ID>/CONTEXT.json 存在有無確認
   ├── 存在 → Phase 1へ進行
   └── 未存在 → エラー: "CONTEXT.jsonがありません。feature-architectを先に実行してください。"
   ```

2. **CONTEXT.jsonロードおよび検証**:

   ```
   CONTEXT.jsonで必須フィールド確認:
   ├── feature_id
   ├── title
   ├── why
   └── quick_resume.current_state == "SpecDrafting"
   ```

3. **機能情報抽出**:
   - CONTEXT.jsonからwhy, user_story, requirements, assumptions読み取り
   - 追加入力があればCONTEXT情報とマージ

4. **BRIEF.md検証および抽出**:

   ```
   CONTEXT.jsonのartifacts.briefパスからBRIEF.md確認
   ├── 存在 → BRIEFから以下の情報を抽出:
   |   ├── Section 0: 原本リクエスト (FR設計時の意図参照)
   |   ├── Section 2: User Stories → FRマッピング基盤
   |   ├── Section 4: BDD AC → FR AC参照
   |   ├── Section 5: In/Out Scope → SPEC §1.4 Goals/Non-Goals
   |   └── Section 6: Constraints → SPEC §0反映
   └── 未存在 → Warning: "BRIEF.mdがありません。意図追跡が制限されます。"
             (エラーではない - SPEC生成を続行)
   ```

5. **検証結果出力**:

   ```markdown
   CONTEXT.json検証完了

   **機能ID**: 029-vocabulary-book
   **機能名**: 単語帳管理

   **CONTEXTから抽出された要素**:

   - Why: 復習効率30%向上
   - ユーザーストーリー: 学習者として単語帳を管理したい
   - 要求事項: 単語追加/削除/お気に入り機能

   → SPEC生成のためのコンテキスト収集を開始します。
   ```

### Phase 1: コンテキスト収集 (Context Discovery)

1. **CONTEXT.json参照** (読み取り専用):
   - `docs/features/<feature-id>/CONTEXT.json`読み取り (Phase 0で検証済み)
   - referencesセクションから関連コード/スペックパス確認
   - **この段階でCONTEXT.jsonを生成しない** (feature-architectの責任)

2. **必須ファイル収集**:

   | カテゴリ             | ファイル                                                                                             |    必須    | 抽出情報                                |
   | -------------------- | ---------------------------------------------------------------------------------------------------- | :--------: | --------------------------------------- |
   | **型定義**           | `src/features/<feature>/types/*.ts`                                                                  |    必須    | TypeScriptインターフェース、Zodスキーマ |
   | **API Route**        | `src/app/api/<route>/route.ts`                                                                       | 条件付き\* | レスポンススキーマ、エラーコード        |
   | **既存SPEC**         | `docs/features/*/SPEC-*.md`                                                                          |    任意    | 参考パターン                            |
   | **既存コード**       | `src/features/<feature>/components/`, `src/features/<feature>/hooks/`, `src/features/<feature>/api/` |    任意    | 既存パターン                            |
   | **デザインアセット** | `docs/features/<feature-id>/design/`                                                                 |    任意    | カラートークン、レイアウト参照          |
   | **UI Flow SSOT**     | `docs/ui-flow/ui-flow.json`                                                                          |    必須    | 既存パネル・状態・SSE・フェーズ定義     |

   > 条件付き\* = 該当機能がAPI Routeを使用する場合必須

3. **CONTEXT.json referencesセクション** (関連コード情報):
   ```json
   {
     "references": {
       "related_specs": ["SPEC-006-srs-review-system.md"],
       "related_code": {
         "components": ["src/features/vocabulary/components/*.tsx"],
         "hooks": ["src/features/vocabulary/hooks/*.ts"],
         "api": ["src/features/vocabulary/api/*.ts"]
       },
       "api_routes": ["src/app/api/vocabulary/route.ts"]
     }
   }
   ```

### Phase 2: 対話型明確化 (Interactive Clarification)

> **原則**: 最大7問に圧縮してユーザーに質問

#### Q&A → BRIEF.md記録プロトコル

> Phase 2の各質問-回答ペアをBRIEF.md Section 8 (Clarification Log)に記録します。

**記録手順**:

1. ユーザーに質問後回答受信
2. BRIEF.mdのSection 8テーブルに行追加:
   ```markdown
   | {番号} | {質問内容} | {回答内容} | {影響セクション} | {日付} |
   ```
3. 回答に応じてBRIEF.mdの関連セクションも更新 (例: Scope変更時Section 5修正)

**例**:

```markdown
| 1 | オフラインでのデータ追加時の処理方法? | ローカル保存後同期 | §5 Scope, §6 Constraints | 2026-02-11 |
| 2 | エラー表示方式? | トースト | §4 AC-03 | 2026-02-11 |
```

#### 7問上限ルール (Autonomy Control)

| 質問カウント | 状態         | 行動                         |
| :----------: | ------------ | ---------------------------- |
|     1-6      | 正常         | 質問後待機                   |
|      7       | 上限到達     | 最後の質問後**自律停止**     |
|    7超過     | AwaitingUser | 追加質問不可、デフォルト選択 |

**7問上限到達時の処理**:

1. CONTEXT.jsonの`quick_resume.question_count`を7に設定
2. `quick_resume.current_state`を`AwaitingUser`に遷移
3. 未回答項目は**デフォルト(推奨案)自動選択**または**仮定(Assumption)として記録**
4. ユーザーに上限到達通知:

   ```markdown
   7問質問上限到達

   未回答項目は推奨案で自動選択されました:

   - Q4: オフライン動作 → "ローカル保存後同期" (推奨案)
   - Q5: エラー表示 → "トースト" (推奨案)

   この仮定を変更するには回答してください。
   そうでなければSPEC生成を続行します。
   ```

**CONTEXT.json question_count更新**:

```json
{
  "quick_resume": {
    "question_count": 3,
    "current_state": "SpecDrafting"
  },
  "autonomy_control": {
    "max_questions_per_session": 7,
    "current_autonomy_level": "supervised"
  }
}
```

**質問カテゴリ** (各カテゴリから必要なもののみ):

| カテゴリ               | 質問例                                                       |
| ---------------------- | ------------------------------------------------------------ |
| **画面/UX**            | 新画面 vs 既存画面拡張? エラー表示方式(トースト/ダイアログ)? |
| **状態管理**           | 状態単位(画面別/グローバル)? 失敗状態含む?                   |
| **データ**             | 新データ構造必要? API連携方式?                               |
| **テスト**             | 統合テスト範囲? モック(mock)方針?                            |
| **Product/Engagement** | Engagementコアループ? Aha Moment? 無料/有料境界?             |

**質問形式**:

```markdown
## SPEC生成のための明確化質問

入力を分析した結果、以下の事項の確認が必要です:

### Q1. 画面構成 [UX]

この機能を**新しいパネル**で追加しますか、既存の**パネルに統合**しますか?

- [ ] A: 新パネル (レイアウトに追加)
- [ ] B: 既存パネル内セクションとして統合 (推奨)

### Q2. データ連携 [DATA]

APIとのデータ連携方式はどうしますか?

- [ ] A: リアルタイムストリーミング (推奨)
- [ ] B: ポーリング
- [ ] C: MVPで除外

(最大7問)
```

### Phase 3: SPEC生成 (Spec Generation)

1. **2案提示** (保守的/拡張的):

   ```markdown
   ## SPEC草案提案

   ### Option A: 保守的アプローチ

   - 既存システム再利用
   - 新規データ構造1個
   - 実装複雑度: 低

   ### Option B: 拡張的アプローチ

   - カスタムアルゴリズム導入
   - 新規データ構造3個
   - 実装複雑度: 高

   どちらの方向で進めますか?
   ```

2. **選択後SPEC生成**:
   - `SPEC-<NNN>-<feature-name>.md`生成
   - `screens/<screen-name>.md`生成 (**feature_type別必須/選択判定** — 以下参照)

   **Screen文書生成ルール** (feature_type基準):

   |  feature_type   | screens/生成 | 条件                                                |
   | :-------------: | :----------: | --------------------------------------------------- |
   | **ui_feature**  |   **必須**   | 最低1つのScreen文書必須。欠落時Readiness Gate No-Go |
   | backend_feature |     不要     | サーバーロジック専用 — Screen該当なし               |
   | system_feature  |     選択     | 設定UI等のユーザー対面画面があれば生成              |

   > **CONTEXT.jsonの`feature_type`フィールドを必ず確認**して判定します。
   > `feature_type`がnullまたは未設定の場合、BRIEF/SPEC内容からUI画面存在有無を推論して判定します。

   **§6.5 Product Requirements生成** (ユーザー対面機能のみ):
   - BRIEF §5.5 → SPEC §6.5.1 Engagement Loop (Hook Model 4段階 → 実装可能なトリガー/報酬メカニズム)
   - BRIEF §5.6 → SPEC §6.5.2 Competitive Context (差別化ポイント → 実装優先順位に反映)
   - BRIEF §5.7 → SPEC §6.5.3 Conversion Design (Soft Paywall トリガー条件 → FRに分解)
   - Backend-only機能: §6.5に "N/A - Backend-only" 表記

3. **Screen文書 §13 Design Reference自動生成**:

   ```
   docs/features/<feature-id>/design/ ディレクトリ存在有無確認
   ├── 存在 → Screen文書に§13 Design Reference追加:
   |   ├── design/内ファイル一覧 → ファイルテーブル生成
   |   ├── code.html存在時 → カラートークン抽出 (hex → Theme マッピング注意警告含む)
   |   ├── Screen Docとデザイン差分 → 差分テーブル生成
   |   └── CONTEXT.jsonのartifacts.design_assets更新
   └── 未存在 → §13省略 (ディレクトリ自体を生成しない)
   ```

   > **SSOT原則**: §13は視覚参考用であり、Screen Doc §3~§8が実装の定義である。

4. **§1.5 UI Flow Contract 生成** (ui_feature 必須):

   > Phase 1 で収集した `docs/ui-flow/ui-flow.json` を参照して §1.5 を生成

   ```
   feature_type判定:
   ├── ui_feature → §1.5 UI Flow Contract 必須生成
   ├── backend_feature → "N/A - Backend-only 機能で UI Flow Contract 省略"
   └── system_feature → UI画面がある場合のみ生成
   ```

   **生成プロセス**:

   ```
   1. ui-flow.json から既存 panels/sse_mapping/phases を読み取り
   2. この機能が追加・変更するパネルを特定:
      ├── 新パネル → operation: "new", visibility条件を定義
      ├── 既存変更 → operation: "modify", 変更内容を記述
      └── 参照のみ → operation: "reference"
   3. §1.5.1 パネル宣言テーブル生成
   4. §1.5.2 SSE イベントマッピングテーブル生成
   5. §1.5.3 フェーズ統合テーブル生成
   6. §1.5.4 状態遷移ダイアグラム生成
   7. json:schema/ui_flow_contract ブロック生成 (機械可読)
   ```

   **検証**: `panels[].name` が ui-flow.json の既存パネル名規約に従っていること

### Phase 3.5: API Contract & NFR生成 (必須)

> "常時必須" - AIがAPI契約と品質基準を明確に把握

#### API Contract (必須)

**判断基準**:

```
API Route使用有無:
├── 使用なし → "N/A - クライアントサイドのみ"明示 (空セクション禁止)
├── 使用あり (エンドポイント1-2個)
|   └── SPEC内API Contractセクションに直接記述
└── 使用あり (エンドポイント3個+)
    └── 別途API-{NNN}-{name}.md生成 + SPECにリンク
```

**API Contract必須要素**:

| 要素               | 必須 | 内容                                             |
| ------------------ | :--: | ------------------------------------------------ |
| エンドポイント一覧 | 必須 | Method, Path, Auth有無                           |
| Request Schema     | 必須 | Zodスキーマ (required, properties)               |
| Response Schema    | 必須 | Zodスキーマ (status, data, error)                |
| Error Codes        | 必須 | HTTPコード、アプリエラーコード、クライアント対応 |

**スキーマ抽出プロセス**:

```
1. API Routeのroute.ts読み取り
2. Zodスキーマまたはレスポンス型定義を検索
3. エラーハンドリングコードからエラーコード抽出
4. API Contractセクションにスキーマ形式で文書化
```

**SSOT原則案内**:

```markdown
> **SSOT原則**
>
> コードのZodスキーマ/型定義が真実の源泉です。
> この文書はコードを反映し、衝突時コードが優先します。
>
> API Routeコード位置: `src/app/api/{name}/route.ts`
```

#### NFR (必須)

> 性能、同時接続、コスト、観測性要求事項明示

**必須項目**:

| 項目              |    必須    | 該当なし時            |
| ----------------- | :--------: | --------------------- |
| 性能 (応答時間)   |    必須    | "一般CRUD - 標準適用" |
| 信頼性 (リトライ) |    必須    | ポリシー明示必須      |
| コスト (AI使用時) | 条件付き\* | N/A (AI未使用)        |
| 観測性            |    任意    | "標準ロギング適用"    |

> 条件付き\* = AI/LLMを使用する機能でのみ必須

**分離決定時の質問 (7問上限内)**:

API複雑度が不確定な場合ユーザーに確認:

```markdown
### Q. API文書分離 [API]

API Routeが3個以上またはAPI契約が複雑です。どう処理しますか?

- [ ] A: SPEC内に統合 (簡素化推奨)
- [ ] B: 別途API-{NNN}.md分離 (詳細管理必要時)
```

### Phase 3.7: 並列実装ガイド生成 (Parallel Implementation Guide)

> **適用条件**: FRが3個以上の機能でのみ生成。2個以下は`N/A - 順次実装`表記。

#### 生成プロセス

1. **FR依存性分析** (レイヤー基盤自動推論):

   ```
   Type/Schema FR  → depends_onなし
   Hook FR         → Type/Schemaに依存
   Component FR    → Hookに依存
   API Route FR    → 独立 (サーバーサイド)
   ```

2. **トポロジーソート** → 並列バッチ自動計算

3. **各FRのファイルをFoundation/Backend/Frontend/Testに分類**

4. **§0.10, §0.11セクション生成**

#### §0.10 FR Dependency Graphテンプレート

```markdown
### 0.10 FR Dependency Graph

#### 0.10.1 依存性テーブル

|   FR-ID    | 説明   | depends_on | レイヤー    | 複雑度 |
| :--------: | ------ | :--------: | ----------- | :----: |
| FR-{NNN}01 | {説明} |     -      | Type/Schema |   S    |
| FR-{NNN}02 | {説明} | FR-{NNN}01 | Hook        |   M    |
| FR-{NNN}03 | {説明} | FR-{NNN}01 | Hook        |   M    |
| FR-{NNN}04 | {説明} |   02, 03   | Component   |   L    |
| FR-{NNN}05 | {説明} |     -      | API Route   |   M    |

レイヤー: Type/Schema | Hook | Component | API Route | Page
複雑度: S (<50 LOC) | M (50-150) | L (150-300) | XL (300+)

#### 0.10.2 並列バッチ (トポロジーソート)

| バッチ | FR一覧       | 並列可能 | 予想時間 |
| :----: | ------------ | :------: | :------: |
|   B1   | FR-01, FR-05 |   Yes    |   N分    |
|   B2   | FR-02, FR-03 |   Yes    |   N分    |
|   B3   | FR-04        |    No    |   N分    |
```

#### §0.11 Parallel Work Unitsテンプレート

```markdown
### 0.11 Parallel Work Units

#### 0.11.1 Foundation (Lead Agent)

| 項目           | ファイル     | 関連FR |
| -------------- | ------------ | :----: |
| Zodスキーマ    | `types/*.ts` |  ALL   |
| Hook Interface | `hooks/*.ts` |  ALL   |
| Barrel File    | `index.ts`   |  ALL   |

#### 0.11.2 Backend Work Units

| PWU-ID | FR-ID | 作業   | ファイル                 |
| :----: | :---: | ------ | ------------------------ |
| BE-01  | FR-XX | {説明} | `api/*.ts`               |
| BE-02  | FR-XX | {説明} | `src/app/api/*/route.ts` |

#### 0.11.3 Frontend Work Units

| PWU-ID | FR-ID | 作業   | ファイル           |
| :----: | :---: | ------ | ------------------ |
| FE-01  | FR-XX | {説明} | `hooks/*.ts`       |
| FE-02  | FR-XX | {説明} | `components/*.tsx` |

#### 0.11.4 Test Work Units

| PWU-ID  | FR-ID | 対象      | ファイル                                        |
| :-----: | :---: | --------- | ----------------------------------------------- |
| TEST-01 | FR-XX | Hook      | `tests/unit/features/.../hooks/*.test.ts`       |
| TEST-02 | FR-XX | Component | `tests/unit/features/.../components/*.test.tsx` |

#### 0.11.5 Integration Checklist

- [ ] Hook → 実際のAPI接続
- [ ] Component → 実際のHookバインディング
- [ ] npm run lint エラー0
- [ ] npm test 全体通過
```

### Phase 4: 検証および引継ぎ (Validation & Handover)

0. **BRIEF <-> SPEC Traceabilityマッピング** (BRIEF存在時):

   > BRIEF.mdが存在する場合、CONTEXT.jsonのtraceabilityセクションを埋めます。

   **マッピングプロセス**:

   ```
   1. BRIEF Section 2からUser Story IDs抽出 (US-01, US-02, ...)
   2. BRIEF Section 4からBDD AC名抽出 (AC-01, AC-02, ...)
   3. 生成されたSPECからFR IDs抽出 (FR-XXXNN)
   4. マッピング生成:
      - user_story_to_fr: 各US → 関連FRマッピング
      - bdd_to_fr: 各AC → 関連FRマッピング
   5. マッピングされていない項目 → unmapped_*配列に記録
   6. CONTEXT.jsonのtraceabilityセクションに保存
   ```

   **CONTEXT.json更新例**:

   ```json
   {
     "traceability": {
       "user_story_to_fr": [
         { "user_story_id": "US-01", "fr_ids": ["FR-02901", "FR-02902"] },
         { "user_story_id": "US-02", "fr_ids": ["FR-02903"] }
       ],
       "bdd_to_fr": [
         { "scenario_name": "AC-01", "fr_ids": ["FR-02901"] },
         { "scenario_name": "AC-02", "fr_ids": ["FR-02902", "FR-02903"] }
       ],
       "unmapped_user_stories": [],
       "unmapped_bdd_scenarios": [],
       "validated_at": null
     }
   }
   ```

   **未マッピング項目処理**: unmapped配列に項目がある場合Warning出力:

   ```markdown
   Traceability Warning:

   - US-03: FRマッピングなし (Out of Scopeか確認必要)
   - AC-04: FRマッピングなし
   ```

1. **交差参照検証 (Cross-Reference Validation)** 必須:

   > **目的**: Target Filesで定義した項目がData Schemaに反映されているか確認

   | 定義した項目    | Target Files必須項目                 | 検証 |
   | --------------- | ------------------------------------ | :--: |
   | 新規Zodスキーマ | `Type/Schema`レイヤー + ファイルパス |  OK  |
   | 新規API Route   | `API Route`レイヤー + ディレクトリ   |  OK  |

   **検証プロセス**:

   ```
   1. 新規Zodスキーマ定義有無確認
      ├── 定義あり → Target FilesにType/Schemaレイヤー存在確認
      |   ├── 存在 → Pass
      |   └── 欠落 → 追加必要: `src/features/{feature}/types/{schema}.ts`
      └── 既存再利用のみ → N/A (Type/Schemaレイヤー省略可能)

   2. 新規API Route定義有無確認
      ├── 定義あり → Target FilesにAPI Routeレイヤー存在確認
      └── 既存再利用/N/A → API Routeレイヤー省略可能
   ```

   **自動修正**: 検証失敗時§0.1 Target Filesに欠落レイヤーを自動追加

1-B. **§0.10/§0.11交差検証** (FR 3個+時):

| 検証項目                           | 条件                                          | 結果 |
| ---------------------------------- | --------------------------------------------- | :--: |
| 全FRが§0.10に登録                  | §2のFR一覧 ↔ §0.10依存性テーブル              |  OK  |
| 循環依存なし                       | depends_onグラフにサイクルなし                |  OK  |
| §0.1ファイル ↔ §0.11 PWUマッピング | Target Filesの全ファイルがPWUに割当て済み     |  OK  |
| Foundation完全性                   | 全Zodスキーマ + Hook Interfaceが§0.11.1に登録 |  OK  |

**検証プロセス**:

```
1. §2のFR一覧抽出 → §0.10依存性テーブルと照合
   ├── 全て登録済み → Pass
   └── 欠落FR存在 → §0.10に追加必要
2. depends_onグラフで循環検知 (DFS基盤)
   ├── 循環なし → Pass
   └── 循環発見 → 依存性再設計必要
3. §0.1 Target Filesのファイル → §0.11 PWUマッピング検証
   ├── 全てマッピング済み → Pass
   └── 未マッピングファイル → 適切なPWUに割当て必要
```

2. **自体検証チェックリスト**:

   **セクション0必須項目**:
   - [ ] **§0.0 Project Context**: ネーミング規則、用語集参照
   - [ ] **§0.1 Target Files**: Globパターン、条件付きファイル条件明示
   - [ ] **§0.2.1 Core State**: 核心状態要素、状態enum定義
   - [ ] **§0.2.2 Architecture Guidance**: Hook/Component分離基準、ネーミング規則
   - [ ] **§0.2.3 State Transitions**: 状態一覧 + 遷移テーブル
   - [ ] **§0.3 Error Handling**: エラー種別処理ポリシー
   - [ ] **§0.4.1 Data Schema**: Zodスキーマフィールド/型/nullable定義
   - [ ] **§0.5 API Contract**: Request/Response Schema, Error Codes (またはN/A)
   - [ ] **§0.6 NFR**: 性能目標、AIコスト上限 (該当時)
   - [ ] **§0.7 AI Logic & Prompts (AI機能)**:
     - [ ] AI未使用時 "N/A" 明示
     - [ ] AI使用時 System Prompt + Response Schema定義
   - [ ] **§0.8 Safety & Guardrails (AI機能)**: 入出力検証, Rate Limiting
   - [ ] **§0.9 Design Tokens**: 使用するテーマトークン参照
   - [ ] **§0.10 FR Dependency Graph** (FR 3個+時): 依存性テーブル、並列バッチ
   - [ ] **§0.11 Parallel Work Units** (§0.10存在時): Foundation/BE/FE/Test分解

   **概要セクション**:
   - [ ] **§1.4 Goals / Non-Goals**: 範囲明確化
   - [ ] **§1.5 UI Flow Contract**: パネル宣言/SSE/フェーズ + `json:schema/ui_flow_contract` ブロック

   **機能要求事項**:
   - [ ] SPECの全FRが入力された要求事項をカバー
   - [ ] 全ACが**BDD 5カラムテーブル形式**
   - [ ] 全FRに**Exception Flowsテーブル**存在
   - [ ] **§2.X Business Rules**: pseudocode + Edge cases

   **検証 & テスト**:
   - [ ] **§5.1 Test Scenarios**: 正常/空/エラーシナリオ一覧
   - [ ] **§5.2 Acceptance Checklist**: 手動検証項目

   **メッセージ定義**:
   - [ ] **§6 メッセージ定義**: messages.tsキー一覧 (日本語)

   **Product Requirements** (ユーザー対面機能のみ):
   - [ ] **§6.5.1 Engagement Loop**: Hook Model 4段階 + Aha Moment定義 (N/A許容)
   - [ ] **§6.5.2 Competitive Context**: 競合ベンチマーク (N/A許容)
   - [ ] **§6.5.3 Conversion Design**: 無料/有料境界 + Soft Paywall (N/A許容)

   **一般**:
   - [ ] 空セクションなし (該当なければ "N/A" 明示)
   - [ ] SSOT参照パス正確

3. **引継ぎメッセージ**:

   ```markdown
   SPEC生成完了

   生成されたファイル:

   - docs/features/029-vocabulary-book/SPEC-029-vocabulary-book.md
   - docs/features/029-vocabulary-book/screens/vocabulary-list.md

   次のステップ:
   → 検証を進めてから実装を開始してください。
   ```

---

## SPEC必須セクション (Next.js/Feature-First/React Hooks最適化)

> **v3.0**: IEEE 830 SRS + FSD/FRD統合、Zero-Context実装サポート

| #         | セクション                |    必須    | 説明                                                      |
| --------- | ------------------------- | :--------: | --------------------------------------------------------- |
| **0.0**   | **Project Context**       |    必須    | ネーミング規則、用語集参照                                |
| 0.1       | Target Files              |    必須    | 影響範囲 (Globパターン) + 条件付きファイル                |
| **0.2.1** | **Core State**            |    必須    | 核心状態要素、状態enum                                    |
| **0.2.2** | **Architecture Guidance** |    必須    | Hook/Component分離基準、ネーミング規則                    |
| **0.2.3** | **State Transitions**     |    必須    | 状態一覧 + 遷移テーブル                                   |
| 0.3       | Error Handling            |    必須    | エラー種別処理ポリシー                                    |
| 0.4.1     | Data Schema               |    必須    | Zodスキーマ + TypeScriptフィールド/型定義                 |
| 0.5       | API Contract              |    必須    | Request/Response Schema, Error Codes                      |
| 0.6       | NFR                       |    必須    | 性能、コスト (AI使用時)                                   |
| 0.7       | AI Logic & Prompts        | 条件付き\* | System Prompt, Response Schema (AI機能必須)               |
| 0.8       | Safety & Guardrails       | 条件付き\* | 入出力検証, Rate Limit (AI機能必須)                       |
| **0.9**   | **Design Tokens**         |    任意    | 使用するテーマトークン参照                                |
| **0.10**  | **FR Dependency Graph**   |    任意    | FR間依存性DAG + 並列バッチ (FR 3個+で必須)                |
| **0.11**  | **Parallel Work Units**   |    任意    | Foundation/Backend/Frontend/Test分解 (0.10存在時必須)     |
| 1         | 概要                      |    必須    | WHY, User Story, MVP範囲                                  |
| 1.4       | Goals / Non-Goals         |    必須    | 範囲明確化                                                |
| **1.5**   | **UI Flow Contract**      |    必須    | SPA状態駆動パネル表示契約 (`ui-flow.json` SSOT連携)       |
| 2         | 機能要求事項              |    必須    | FR単位明細 (BDD AC, EC, EF)                               |
| **2.X**   | **Business Rules**        |    必須    | ビジネスロジックpseudocode                                |
| 3         | 依存性 & リスク           |    必須    | 先行依存性、リスク                                        |
| 4         | 画面文書                  |    任意    | Screen文書参照 (UI変更時)                                 |
| **5**     | **検証 & テスト**         |    必須    | Test Scenarios, Acceptance Checklist                      |
| **6**     | **メッセージ定義**        |    必須    | messages.tsキー一覧                                       |
| **6.5**   | **Product Requirements**  |    任意    | Engagement Loop, Conversion, AARRR (ユーザー対面機能のみ) |
| **7**     | **変更履歴**              |    必須    | バージョン管理                                            |

> 条件付き\* = AI/LLM使用機能でのみ必須、未使用時"N/A"明示

---

## 失敗ケース対処

| ケース                         | 対処                                                         |
| ------------------------------ | ------------------------------------------------------------ |
| **入力不十分**                 | Phase 2で核心質問で補完、最小要求事項収集                    |
| **技術的制約で実装不可**       | 代替案(Plan B)をSPECに併記                                   |
| **ユーザー回答曖昧**           | デフォルト(推奨案)選択して進行、SPECに"仮定(Assumption)"明示 |
| **7問上限到達**                | 未回答項目は推奨案自動選択、SPECに仮定明示                   |
| **Tier 1セキュリティ作業検知** | 自律停止、ユーザー確認必須 (認証/決済/PII関連)               |

---

## AI行動指針

### DO (すべきこと)

- 入力された要求事項をSPECの全FRに反映
- 既存パターン参照 (類似SPECファイル読み取り)
- 質問は最大7個に圧縮
- 仮定(Assumption)を明示的に記録
- テストパスを具体的に指定

### DON'T (してはならないこと)

- 入力された要求事項を無視してSPEC作成
- ユーザー確認なしに新しいデータ構造追加を決定
- 空セクションでSPEC生成 (記載内容がなければ "N/A - 該当なし" 明示)
- PRDレベルの膨大な文書生成 (SPECは単一機能に集中)

---

## CONTEXT.json更新 (更新専用)

> **状態遷移**: `SpecDrafting` (維持) → SPEC生成完了記録
>
> **注意**: このスキルはCONTEXT.jsonを**更新のみ**します。**生成はfeature-architectの責任**です。

作業完了時**既存CONTEXT.jsonを更新**します:

```markdown
## CONTEXT.json更新内容

1. Read `docs/features/<id>/CONTEXT.json`
2. Edit:
   - quick_resume.current_state → "SpecDrafting"
   - quick_resume.current_task → "SPEC.md生成完了、Readiness Gate待ち"
   - quick_resume.next_actions → ["Readiness Gate実行", "Go時実装開始"]
   - quick_resume.last_updated_at → 現在時刻
   - progress.fr_total → SPECに定義されたFR個数
   - progress.details → FR別初期状態 (全て"pending")
   - artifacts.spec → SPEC.mdパス
   - artifacts.screens → Screen文書パス一覧
   - artifacts.design_assets → design/ディレクトリ存在時 `{directory, files}`、未存在時 `null`
   - decisions[] += SPEC作成中の決定記録
   - history[] += 状態遷移記録
   - traceability → BRIEF <-> SPECマッピング結果 (Phase 4 Step 0で生成)

3. **references.related_code同期** 必須:

   > **目的**: §0.1 Target FilesとCONTEXT.jsonの一貫性保障
   - 新規Zodスキーマ定義時:
     → `references.related_code.types[]`にファイルパス追加
     → 例: `"src/features/analysis/types/analysis-result.ts"`

   - 新規Hook定義時:
     → `references.related_code.hooks[]`にファイルパス追加
     → 例: `"src/features/analysis/hooks/use-analysis.ts"`

   - 新規Component定義時:
     → `references.related_code.components[]`にファイルパス追加
     → 例: `"src/features/analysis/components/AnalysisPanel.tsx"`

   - 新規Page定義時:
     → `references.related_code.pages[]`にファイルパス追加
     → 例: `"src/app/analysis/page.tsx"`
```

**更新例**:

```json
{
  "quick_resume": {
    "current_state": "SpecDrafting",
    "current_task": "SPEC-029.md生成完了、Readiness Gate待ち",
    "next_actions": ["Readiness Gate実行", "Go判定時実装開始"],
    "last_updated_at": "2026-02-11T11:00:00+09:00"
  },
  "progress": {
    "percentage": 0,
    "fr_total": 5,
    "fr_completed": 0,
    "fr_in_progress": 0,
    "details": {
      "FR-02901": { "status": "pending", "weight": 1 },
      "FR-02902": { "status": "pending", "weight": 1 },
      "FR-02903": { "status": "pending", "weight": 2 },
      "FR-02904": { "status": "pending", "weight": 1 },
      "FR-02905": { "status": "pending", "weight": 1 }
    }
  },
  "artifacts": {
    "spec": "docs/features/029-vocabulary-book/SPEC-029.md",
    "screens": ["docs/features/029-vocabulary-book/screens/vocabulary-list-screen.md"]
  },
  "references": {
    "related_code": {
      "types": ["src/features/vocabulary/types/vocabulary-item.ts"],
      "hooks": ["src/features/vocabulary/hooks/use-vocabulary.ts"],
      "components": ["src/features/vocabulary/components/VocabularyList.tsx"],
      "pages": []
    }
  },
  "history": [
    {
      "at": "2026-02-11T11:00:00+09:00",
      "from_state": "InputReceived",
      "to_state": "SpecDrafting",
      "triggered_by": "feature-spec-generator",
      "note": "SPEC-029.md + 1個Screen文書生成"
    }
  ]
}
```

> **注意**: `references.related_code`のファイル一覧は§0.1 Target Filesと一致する必要があります。

---

## 使用例

> **前提条件**: CONTEXT.jsonが存在する必要があります (feature-architect実行後)

```bash
# 基本使用法 - 機能IDで呼び出し (推奨)
/feature-spec-generator 029-vocabulary-book

# 追加要求事項とともに
/feature-spec-generator 029-vocabulary-book --req "オフライン同期サポート"

# feature-pilotから自動呼び出し (ユーザーは直接呼び出し不要)
# pilotがarchitect完了後自動で呼び出す
```

**サポートしないパターン**:

```bash
# ユーザーストーリーで直接開始 (非サポート - architect先に実行必要)
/feature-spec-generator 学習者として単語帳を管理したい  # NG

# CONTEXT.jsonなしに呼び出し (非サポート)
/feature-spec-generator --why "復習効率向上"  # NG
```

---

## 統合ワークフロー

> **Option B原則**: feature-architectがCONTEXT.jsonを生成した後にのみこのスキルが実行されます。

```
[意図入力]
  |  ユーザーストーリー / Why / 要求事項 / タスク
  v
[feature-architect] ──────────────────────────┐
  |  意図分析 + ID割当 + CONTEXT.json生成     |
  v──────────────────────────────────────────┘
[feature-spec-generator] ─────────────────────┐
  |  CONTEXT.json基盤SPEC/Screen生成          |
  |  (CONTEXT読み取り + 対話で明確化)          |
  v──────────────────────────────────────────┘
[Implementation] → SPEC準拠実装
```

> **必須ワークフロー**: architect (CONTEXT生成) → spec-generator (SPEC生成) → 実装

---

## 参照文書

- [SPECテンプレート](../../docs/_templates/spec_template.md)
- [Screenテンプレート](../../docs/_templates/screen_template.md)
- [APIテンプレート](../../docs/_templates/api_template.md) - 別途API文書分離時使用
