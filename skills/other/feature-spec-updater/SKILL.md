---
name: feature-spec-updater
description: |
  既存SPECを修正するスキル。新規SPEC生成(feature-spec-generator)と異なり、既存SPECをロードして変更された部分のみ更新する。
  変更履歴管理、diff表示、影響範囲分析を提供する。

  "SPEC修正", "SPEC更新", "機能変更", "FR追加", "FR修正" 等のリクエストでトリガーされる。

  <example>
  user: "006-srs-review-systemの復習間隔をSM-2からLeitnerに変更して"
  assistant: "feature-spec-updaterを使用して既存SPECを修正します"
  </example>

  <example>
  user: "005 SPECにオフラインモードFRを追加して"
  assistant: "feature-spec-updaterを使用してFRを追加します"
  </example>
doc_contract:
  review_interval_days: 90
---

# Feature Spec Update

> **核心コンセプト**: "変更追跡が可能な修正" (Tracked Modification)
> **SPECバージョン**: v3.0 - IEEE 830 SRS + FSD/FRD統合、Zero-Context実装支援

既存SPECを安全に修正するスキル。全体上書きではなく**変更された部分のみ更新**し、**変更履歴**を残す。

**v3.0 主要変更**:

- **$0.0 Project Context (v3.0新規)**: ネーミング規則、用語集(`docs/glossary.md`)参照
- $0.2.2 React Hook Specifications: ライフサイクル・依存配列ポリシー
- $0.2.3 State Transitions: 状態遷移ダイアグラム (Tier 1-2)
- $0.3 Error Handling: 4つのサブセクションに拡張
- $0.4 Data Schema & Validation: Zodスキーマ、型定義、バリデーション必須
- $0.5 API Contract: 常時必須 (API未使用時 "N/A" 明示)
- $0.6 NFR: 性能、同時性、信頼性、コスト、観測性必須
- $0.7 AI Logic & Prompts: System Prompt、Response Schema、変数注入 (AI機能必須)
- $0.8 Safety & Guardrails: 入出力検証、Rate Limit、Fallback (AI機能必須)
- **$0.9 Design Tokens (v3.0新規)**: テーマトークン参照
- $1.4 Goals / Non-Goals: 範囲明確化必須
- **$1.5 Screen Flow (v3.0新規)**: 画面間ナビゲーションダイアグラム
- $2 Exception Flows: 各FRに例外フローテーブル必須
- **$2.X Business Rules (v3.0新規)**: ビジネスロジックpseudocode
- $3.4 Sequence Diagrams: Tier 1-2機能で必須
- **$5 検証 & テスト (v3.0新規)**: Test Fixtures、Acceptance Checklist
- **$6 メッセージ定義 (v3.0新規)**: messages.tsキーネーミング規則

## spec-generator vs spec-updater比較

| 項目             | spec-generator     | spec-updater                     |
| ---------------- | ------------------ | -------------------------------- |
| **用途**         | 新規SPEC生成       | 既存SPEC修正                     |
| **入力**         | CONTEXT.json       | CONTEXT.json + **既存SPEC**      |
| **出力**         | 全体SPEC新規       | **変更されたセクションのみ**修正 |
| **変更履歴**     | 初回バージョンのみ | **全変更記録**                   |
| **上書きリスク** | なし (新規)        | **防止ロジック内蔵**             |

---

## プロトコル (Protocol)

### Phase 0: 文書およびコードロード (Document & Code Loading)

1. **必須ファイルロード**:

   ```
   docs/features/<ID>/
   ├── CONTEXT.json          # 統合コンテキスト (SSOT)
   ├── SPEC-<ID>-*.md        # 既存SPEC (必須)
   └── CONTEXT.json          # 統合コンテキスト (SSOT)

   src/app/api/              # $0.5 変更時必須
   └── [endpoint]/route.ts   # API Routeコード
   ```

   > **参考**: `CONTEXT.json`が唯一のコンテキストSSOTです。

2. **変更タイプ別ファイル収集**:

   | 変更タイプ            | 追加収集必要ファイル             |
   | --------------------- | -------------------------------- |
   | $0.4 Zodスキーマ変更  | `src/features/*/types/*.ts`      |
   | $0.5 API契約変更      | `src/app/api/*/route.ts`         |
   | $0.6 NFR変更          | 既存SPECの性能/コストセクション  |
   | $0.9 Design Token変更 | `src/app/globals.css` テーマ定義 |

3. **SPEC未存在時の却下**:

   ```markdown
   既存SPECなし - spec-generatorへの転換が必要

   `docs/features/029-vocabulary-book/SPEC-*.md`が存在しません。

   -> /feature-spec-generator 029 を実行してSPECを先に生成してください。
   ```

### Phase 1: 変更範囲分析 (Change Scope Analysis)

1. **変更タイプ判別**:

   | 変更タイプ                | トリガーシグナル               | 影響範囲                  | 影響セクション  |
   | ------------------------- | ------------------------------ | ------------------------- | --------------- |
   | **Project Context変更**   | ネーミング規則変更             | AI実装契約修正            | $0.0 (v3.0)     |
   | **FR追加**                | "~機能追加", "新要求事項"      | 新FRセクション生成        | $2              |
   | **FR修正**                | "FR-XXXXX変更", "動作修正"     | 該当FRのみ修正            | $2              |
   | **FR削除**                | "FR-XXXXX削除", "機能削除"     | 該当FR削除 + 影響分析     | $2, $3          |
   | **セクション0修正**       | Target Files, Architecture変更 | AI実装契約修正            | $0.1~$0.3       |
   | **React Hook仕様変更**    | ライフサイクル・依存配列変更   | Hookライフサイクル        | $0.2.2 (v3.0)   |
   | **State Transitions変更** | 状態マシン変更                 | 状態遷移図                | $0.2.3 (v3.0)   |
   | **Error Handling変更**    | エラーハンドリングポリシー変更 | 4レベルエラー処理         | $0.3 (v3.0拡張) |
   | **Zodスキーマ変更**       | バリデーション追加/修正        | 型定義 + バリデーション   | $0.4            |
   | **API Contract変更**      | Request/Response変更           | API Contract文書          | $0.5            |
   | **NFR変更**               | 性能/コスト目標変更            | 非機能要求事項            | $0.6            |
   | **AI Prompt変更**         | プロンプト/応答スキーマ変更    | AI Logic文書              | $0.7            |
   | **AI安全性変更**          | 検証ルール/Rate Limit変更      | Safety文書                | $0.8            |
   | **Design Token変更**      | テーマトークン追加/変更        | UI一貫性                  | $0.9 (v3.0)     |
   | **Goals/Non-Goals変更**   | 範囲拡張/縮小                  | 範囲定義                  | $1.4            |
   | **Screen Flow変更**       | ナビゲーション変更             | Screen Flowダイアグラム   | $1.5 (v3.0)     |
   | **Business Logic変更**    | 核心ロジック変更               | Business Rules pseudocode | $2.X (v3.0)     |
   | **Exception Flow変更**    | エラー処理方式変更             | FR内EFテーブル            | $2 EF           |
   | **Sequence Diagram変更**  | コンポーネントフロー変更       | 依存性セクション          | $3.4            |
   | **Screen修正**            | UI変更、画面修正               | Screen文書修正            | $4              |
   | **テスト仕様変更**        | テスト条件変更                 | 検証セクション            | $5 (v3.0)       |
   | **メッセージキー変更**    | messages.tsキー追加/変更       | メッセージ定義            | $6 (v3.0)       |

2. **影響範囲出力**:

   ```markdown
   ## 変更範囲分析

   **リクエスト**: 復習間隔をSM-2からLeitnerに変更

   ### 影響を受ける項目

   | 項目        | 現在                     | 変更後                  | 影響セクション |
   | ----------- | ------------------------ | ----------------------- | -------------- |
   | FR-00602    | SM-2アルゴリズム使用     | Leitnerボックスシステム | $2             |
   | Zodスキーマ | `intervalDays`フィールド | `boxLevel`フィールド    | $0.4           |
   | Custom Hook | `useReviewInterval()`    | ロジック全面変更        | $0.1           |

   ### 連鎖影響

   - Screen: review-session画面の間隔表示UI
   - Test: `tests/unit/features/review/hooks/use-review-interval.test.ts`

   ### 追加確認必要

   - [ ] 既存ユーザーデータマイグレーション方針

   このまま進めますか?
   ```

### Phase 2: 修正計画策定 (Modification Planning)

1. **修正単位決定**:
   - **Atomic Update**: 単一FRのみ変更 (推奨)
   - **Batch Update**: 関連FRまとめて変更
   - **Major Update**: セクション全体再作成 (注意必要)

2. **修正前バックアップ提案** (Major Update時):

   ````markdown
   Major Update検知

   この変更はSPECの30%以上を修正します。
   進行前にバックアップを推奨します:

   ```bash
   cp SPEC-006-srs-review-system.md SPEC-006-srs-review-system.md.bak
   ```
   ````

   続行しますか?

   ```

   ```

### Phase 3: SPEC修正 (Spec Modification)

1. **変更適用**:
   - 既存内容を維持しながら変更された部分のみ修正
   - **絶対に全体ファイル再作成禁止**

2. **変更履歴追加** (SPEC最下部):

   ```markdown
   ## 変更履歴

   | バージョン | 日付       | 変更内容                        | 影響FR   |
   | ---------- | ---------- | ------------------------------- | -------- |
   | 1.0        | 2026-01-15 | 初回作成                        | -        |
   | 1.1        | 2026-01-25 | SM-2 -> Leitnerアルゴリズム変更 | FR-00602 |
   ```

3. **diffスタイル出力**:

   ````markdown
   ## 変更事項 (Diff)

   ### FR-00602: 復習間隔計算

   ```diff
   - SM-2アルゴリズムを使用して次の復習時点を計算する。
   - interval = base_interval * easiness_factor
   + Leitnerボックスシステムを使用して次の復習時点を計算する。
   + box_level 1: 1日, 2: 3日, 3: 7日, 4: 14日, 5: 30日
   ```
   ````

   ### $0.4 Zodスキーマ変更

   ```diff
   import { z } from 'zod';

   export const srsItemSchema = z.object({
   -   intervalDays: z.number().int(),
   -   easinessFactor: z.number(),
   +   boxLevel: z.number().int().min(1).max(5),
   +   nextReviewAt: z.string().datetime(),
   });

   export type SrsItem = z.infer<typeof srsItemSchema>;
   ```

   ```

   ```

### Phase 4: 検証および引継ぎ (Validation & Handover)

1. **自己検証** (v3.0チェックリスト):

   **基本検証**:
   - [ ] 変更されたFRのACが完全か?
   - [ ] **ACがBDD 5カラムテーブル形式か?** (`| AC | Given | When | Then | 観測点 |`)
   - [ ] **EF(Exception Flows)テーブルが存在するか?**
   - [ ] 連鎖影響を受ける文書(Screen等)も更新されたか?
   - [ ] 変更履歴($7)が追加されたか?

   **$0.0 Project Context変更時 (v3.0)**:
   - [ ] ネーミング規則が既存パターンと一貫しているか?
   - [ ] 用語集参照(`docs/glossary.md`)が維持されているか?

   **$0.2.2 React Hook Specifications変更時 (v3.0)**:
   - [ ] ライフサイクル・依存配列ポリシーが明示されているか?
   - [ ] Hookの生成・破棄タイミングが明確か?

   **$0.2.3 State Transitions変更時 (v3.0)**:
   - [ ] 状態遷移ダイアグラムが更新されているか?
   - [ ] 許可された遷移と不変条件が定義されているか?

   **$0.3 Error Handling変更時 (v3.0拡張)**:
   - [ ] Hook/API/Component/Global 4レベルが定義されているか?
   - [ ] 各エラータイプ別処理ポリシーが明示されているか?

   **$0.4 Data Schema変更時**:
   - [ ] $0.4.1 Zodスキーマが型定義と一致しているか?
   - [ ] $0.4.2 バリデーションルールが完全か?

   **$0.5 API Contract変更時**:
   - [ ] Request/Response SchemaがAPI Routeコードと一致しているか?
   - [ ] Error Codesが完全に定義されているか?
   - [ ] クライアント側対応方針が明示されているか?

   **$0.6 NFR変更時**:
   - [ ] 性能目標(レスポンス時間等)が測定可能な形式で記述されているか?
   - [ ] AI使用機能であればコスト上限が明示されているか?

   **$0.7 AI Logic & Prompts変更時**:
   - [ ] System Prompt全体テキストが記載されているか? (要約禁止)
   - [ ] Response SchemaがAPI RouteのresponseSchemaと一致しているか?
   - [ ] Prompt変数注入テーブルが完全か?
   - [ ] 役割定義テーブルが更新されているか?

   **$0.8 Safety & Guardrails変更時**:
   - [ ] 入力/出力検証規則が明確に定義されているか?
   - [ ] Rate Limitingポリシーが明示されているか?
   - [ ] Fallback戦略 + ユーザーメッセージが定義されているか?

   **$0.9 Design Tokens変更時 (v3.0)**:
   - [ ] テーマガイド(`globals.css`)参照が維持されているか?
   - [ ] カスタムトークンが必要であれば定義されているか?

   **$1.4 Goals / Non-Goals変更時**:
   - [ ] Goalsが具体的なチェックリストで作成されているか?
   - [ ] Non-Goalsに「なぜ除外したか」理由が明示されているか?

   **$1.5 Screen Flow変更時 (v3.0)**:
   - [ ] 画面間ナビゲーションダイアグラムが更新されているか?
   - [ ] 進入点/終了点が明示されているか?

   **$2.X Business Rules変更時 (v3.0)**:
   - [ ] ビジネスロジックpseudocodeが更新されているか?
   - [ ] Edge casesが明示されているか?

   **$3.4 Sequence Diagrams変更時**:
   - [ ] Happy Path + Error Path最小2つが存在するか?
   - [ ] 責任分担テーブルが更新されているか?
   - [ ] タイムアウトポリシーが明示されているか?

   **$5 検証 & テスト変更時 (v3.0)**:
   - [ ] Test Fixturesが更新されているか?
   - [ ] Acceptance Checklistが変更事項を反映しているか?

   **$6 メッセージ定義変更時 (v3.0)**:
   - [ ] messages.tsキーネーミング規則が遵守されているか?
   - [ ] 追加するキー一覧が完全か?

2. **引継ぎメッセージ**:

   ```markdown
   SPEC修正完了

   **修正されたファイル**:

   - `SPEC-006-srs-review-system.md` (FR-00602修正)

   **変更要約**:

   - SM-2 -> Leitnerアルゴリズム変更
   - Data Schema: `boxLevel`フィールド追加

   **次のステップ**:
   -> /ai-readiness-gate 006 を実行して検証してください。
   または直接実装を開始できます。
   ```

---

## 修正タイプ別詳細

### FR追加

```markdown
## 新FR追加様式

### FR-XXXNN: [機能名]

**Priority**: P0/P1/P2
**Complexity**: Low/Medium/High

#### 説明

[機能説明]

#### Acceptance Criteria (BDD 5カラムテーブル)

| AC  | Given (事前条件) | When (行動) | Then (期待結果) | 観測点          |
| :-: | ---------------- | ----------- | --------------- | --------------- |
| AC1 | {事前条件}       | {行動}      | {期待結果}      | {検証変数/状態} |
| AC2 | {事前条件}       | {行動}      | {期待結果}      | {検証変数/状態} |

#### Edge Cases

- EC1: [例外状況] -> [処理方法]

#### AI Implementation Hint

- Target: `src/features/...`
- Pattern: [参考すべき既存コード]
```

### FR修正

1. 既存FR内容読み取り
2. 変更部分のみ修正 (Editツール使用)
3. 変更履歴に記録

### FR削除

1. 削除するFR確認
2. 依存する他のFR確認
3. 削除後番号再整列**禁止** (gap維持)
4. 変更履歴に"削除"記録

### Zodスキーマ変更 ($0.4)

1. 既存$0.4型定義読み取り
2. 変更フィールドのみdiffで表示
3. **Zodバリデーションルールの完全性確認**
4. 関連するCustom Hookも併せて修正

````markdown
## Zodスキーマ変更例

### $0.4 修正

```diff
export const reviewItemSchema = z.object({
+   boxLevel: z.number().int().min(1).max(5),  // 新規
-   intervalDays: z.number().int(),             // 削除予定
});
```
````

> 関連ファイル: `src/features/review/types/index.ts` の更新が必要

````

### API Contract変更 ($0.5)

1. 既存$0.5 Request/Response Schema読み取り
2. 変更フィールドのみdiffで表示
3. **Error Codes漏れ確認** (新エラー条件発生時)
4. API Routeコードとの同期確認

```markdown
## API Contract変更例

### Response Schema変更

```diff
{
  "data": {
-   "interval_days": { "type": "integer" },
+   "box_level": { "type": "integer", "minimum": 1, "maximum": 5 },
+   "next_review_at": { "type": "string", "format": "date-time" }
  }
}
````

> API Route同期必要: `src/app/api/srs-calculate/route.ts`

````

### NFR変更 ($0.6)

1. 既存$0.6性能/コスト目標読み取り
2. 変更項目のみ修正
3. **測定方法の一貫性維持**

### AI Logic & Prompts変更 ($0.7)

> AI機能でプロンプトやレスポンススキーマを変更する場合

1. 既存$0.7セクション読み取り
2. **変更されるプロンプト全体テキスト記載** (要約禁止)
3. Response Schema変更時API Routeコードとの同期確認
4. 変数注入テーブル更新

```markdown
## AIプロンプト変更例

### $0.7.2 System Prompt変更

**Coach Prompt** (変更):
```diff
- ## Feedback Rules
- 1. Be encouraging, not critical
+ ## Feedback Rules
+ 1. Be encouraging but direct
+ 2. Always provide the grammar rule name
````

> API Route同期必要: `src/app/api/ai-tutor-chat/route.ts`

````

### Safety & Guardrails変更 ($0.8)

> Rate Limit、検証規則、Fallback戦略変更時

1. 既存$0.8セクション読み取り
2. 変更項目のみdiffで表示
3. **ポリシーの一貫性維持**

```markdown
## Rate Limit変更例

### $0.8.3 Rate Limiting変更

```diff
| 制限項目 | 無料プラン | 有料プラン | 超過時 |
- | AI呼び出し/日 | 50回 | 500回 | 日次上限通知 |
+ | AI呼び出し/日 | 30回 | 300回 | 日次上限通知 + アップグレード誘導 |
````

> クライアント + API Route双方の更新が必要

````

### Goals / Non-Goals変更 ($1.4)

> 機能範囲の拡大/縮小時

1. 既存$1.4セクション読み取り
2. Goals追加/削除時、該当FRとの連動確認
3. **Non-Goals追加時「なぜ除外したか」理由必須**

```markdown
## Non-Goals追加例

### $1.4 Non-Goals変更

```diff
| 除外項目 | 除外理由 | 代替 |
| 単語帳共有 | MVP範囲超過 | Phase 2 |
+ | AI自動翻訳 | 著作権問題未解決 | ユーザー直接入力 |
````

> 関連FRリクエストが来たらNon-Goals参照するよう案内

````

### Exception Flows追加/修正 ($2 EF)

> エラー処理方式変更時

1. 該当FRのEFテーブル読み取り
2. 新しい例外状況追加または既存処理方式修正
3. **復旧パス明示必須**

```markdown
## Exception Flow追加例

### FR-02901 EF変更

```diff
| EF | トリガー条件 | システム反応 | ユーザーメッセージ | 復旧パス |
| EF3 | 認証期限切れ | トークン更新 | (透明処理) | 失敗時ログイン |
+ | EF6 | ストレージ不足 | エラー状態 | "ストレージが不足しています" | キャッシュクリア案内 |
````

````

### Sequence Diagrams変更 ($3.4)

> コンポーネント間フロー変更時 (Tier 1-2)

1. 既存$3.4ダイアグラム読み取り
2. 変更されるステップのみdiffで表示
3. **責任分担テーブル + タイムアウトポリシー同期**

```markdown
## Sequence Diagram変更例

### SD-001変更 (新ステップ追加)

```diff
User          UI/Page           Custom Hook        API Route
 |               |                  |                 |
 |--[1] 単語入力->|                  |                 |
 |               |--[2] addWord()-->|                 |
+|               |                  |--[2.5] AI検証()->|
+|               |                  |<-[2.6] 検証結果-|
 |               |                  |--[3] POST /api/words->|
````

**責任分担テーブル更新**:
| ステップ | コンポーネント | 責任 |
| 2.5-2.6 | API Route | AI基盤単語検証 (新規) |

````

---

## AI行動指針

### DO (すべきこと)
- 既存SPECを先に完全に読み取り
- 変更範囲を明確に分析後修正開始
- diff形式で変更事項表示
- 変更履歴($7)必ず追加
- 連鎖影響を受ける文書確認
- **$0.0変更時、用語集(`docs/glossary.md`)参照維持** (v3.0)
- **$0.2.2変更時、React Hookライフサイクルポリシー明示** (v3.0)
- **$0.2.3変更時、状態遷移ダイアグラム同期** (v3.0)
- **$0.3変更時、4レベル(Hook/API/Component/Global)検討** (v3.0)
- **$0.4変更時、Zodスキーマの完全性確認**
- **$0.5変更時、API Routeコード同期確認**
- **$0.7変更時、プロンプト全体テキスト記載**
- **$0.8変更時、Rate Limitポリシーの一貫性維持**
- **$0.9変更時、テーマガイド参照維持** (v3.0)
- **$1.4 Non-Goals追加時「なぜ除外」理由必須**
- **$1.5変更時、Screen Flowダイアグラム同期** (v3.0)
- **$2 EF変更時、復旧パス明示**
- **$2.X変更時、Business Rules pseudocode同期** (v3.0)
- **$3.4変更時、責任分担テーブル同期**
- **$5変更時、Test Fixtures同期** (v3.0)
- **$6変更時、messages.tsメッセージキーネーミング規則遵守** (v3.0)

### DON'T (してはならないこと)
- 全体SPECファイル再作成 (Writeツールで全体上書き禁止)
- 変更範囲分析なしにいきなり修正
- 削除されたFR番号再使用
- 変更履歴($7)漏れ
- **SPECのみ修正して実際のコード同期漏れ**
- **$0.0 用語集のin-SPEC重複定義** (v3.0)
- **$0.5 API変更時Error Codes更新漏れ**
- **$0.7 プロンプトを要約して記載**
- **$0.8 Fallback戦略なしにエラー処理変更**
- **$1.4 Non-Goalsで「後で」とだけ記載して理由漏れ**
- **$3.4 Sequence Diagram変更時タイムアウトポリシー漏れ**

---

## CONTEXT.json直接更新

> **状態遷移**: `Idle` -> `SpecUpdating`
> **参照**: [context_schema.json](../../docs/_templates/context_schema.json) | [context_template.json](../../docs/_templates/context_template.json)

作業完了時**CONTEXT.jsonを直接更新**します:

```markdown
## CONTEXT.json更新内容

1. Read `docs/features/<id>/CONTEXT.json`
2. Edit:
   - quick_resume.current_state -> "SpecUpdating"
   - quick_resume.current_task -> "SPEC修正完了、Readiness Gate待ち"
   - quick_resume.next_actions -> ["Readiness Gate実行", "Go時実装進行"]
   - quick_resume.last_updated_at -> 現在時刻
   - artifacts.spec -> 修正されたSPECパス
   - decisions[] += 修正決定記録
   - history[] += 状態遷移記録
````

**更新例**:

```json
{
  "quick_resume": {
    "current_state": "SpecUpdating",
    "current_task": "SPEC-006修正完了 - SM-2 -> Leitner変更",
    "next_actions": ["Readiness Gate実行", "影響を受けるScreen文書確認"],
    "last_updated_at": "2026-01-25T14:00:00+09:00"
  },
  "decisions": [
    {
      "at": "2026-01-25T14:00:00+09:00",
      "summary": "復習アルゴリズムSM-2 -> Leitner変更",
      "rationale": "実装簡素化 + ユーザー直感性"
    }
  ],
  "history": [
    {
      "at": "2026-01-25T14:00:00+09:00",
      "from_state": "Idle",
      "to_state": "SpecUpdating",
      "triggered_by": "feature-spec-updater",
      "note": "SPEC v1.1 - FR-00602アルゴリズム変更"
    }
  ]
}
```

---

## 使用例

```bash
# 基本使用 (機能ID + 変更内容)
/feature-spec-updater 006 "SM-2をLeitnerに変更"

# FR追加
/feature-spec-updater 005 --add-fr "オフラインセッション保存機能"

# FR修正
/feature-spec-updater 006 --modify FR-00602 "間隔計算ロジック変更"

# Zodスキーマ変更
/feature-spec-updater 006 --section 0.4 "boxLevelフィールド追加"

# API Contract変更
/feature-spec-updater 002 --section 0.5 "レスポンスにconfidence_score追加"

# 対話型モード
/feature-spec-updater 006
```

---

## feature-pilotとの統合

```
[feature-pilot自動判別]
     |
     +-- SPECなし -> /feature-spec-generator
     |
     +-- SPECあり -> /feature-spec-updater <-- 自動選択
```

feature-pilotがMODIFY_FEATUREと分類すると自動的にこのスキルが呼び出される。

---

## 参照文書

- [feature-spec-generatorスキル](../feature-spec-generator/SKILL.md) - 新規SPEC生成用
- [ai-readiness-gateスキル](../ai-readiness-gate/SKILL.md) - 検証用
- [SPECテンプレート v3.0](../../docs/_templates/spec_template.md) - IEEE 830 + FSD/FRD統合
- [SPECセクションガイド v3.0](../feature-spec-generator/references/spec-sections.md) - セクション別作成指針
- [CONTEXTスキーマ](../../docs/_templates/context_schema.json) - コンテキストSSOT
- [用語集 (Glossary)](../../docs/glossary.md) - $0.0で参照、in-SPEC重複禁止
