---
name: check-requirement-delta
description: 要件の衝突を検出
user-invocable: true
argument-hint: [要件定義書パスまたは機能概要]
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

# civicship-api 要件衝突検出

新機能の要件と既存システムの仕様を比較し、**衝突・矛盾・破壊的変更**を自動検出します。既存の仕様を保護しながら安全に新機能を追加するための分析ツールです。

## 使用方法

```bash
# 要件定義書から衝突を検出
/check-requirement-delta docs/requirements/point-expiration.md

# 機能概要から検出（インタラクティブ）
/check-requirement-delta ポイント有効期限機能
```

**引数:**
- `$ARGUMENTS`: 要件定義書のパス、または機能の概要

---

## 衝突検出プロセス

### ステップ1: 新要件の理解

要件定義書または機能概要から以下を抽出:

```markdown
## 新要件の抽出

### 影響を受けるドメイン
- [ ] account（User, Community, Wallet）
- [ ] experience（Opportunity, Reservation）
- [ ] reward（Utility, Ticket）
- [ ] transaction（Point Transfer）
- [ ] notification（LINE Messaging）

### データモデル変更
- **新規テーブル:** [テーブル名]
- **カラム追加:** [テーブル.カラム名]
- **カラム変更:** [テーブル.カラム名] (型変更、制約変更)
- **カラム削除:** [テーブル.カラム名]

### GraphQL API変更
- **新規Query:** [Query名]
- **新規Mutation:** [Mutation名]
- **型追加:** [GqlXxx]
- **フィールド追加:** [GqlXxx.fieldName]
- **フィールド変更:** [GqlXxx.fieldName] (型変更、nullable変更)
- **非推奨化:** [Query/Mutation/フィールド名]

### ビジネスルール変更
- [既存ルールの変更内容]
```

---

### ステップ2: 既存GraphQLスキーマの分析

全てのGraphQLスキーマファイルを読み取り、影響を受ける型を特定:

```bash
# 全てのGraphQLスキーマファイルを取得
find src/application/domain -name "*.graphql" -type f

# 影響を受ける型を検索
grep -r "type Gql${RELATED_TYPE}" src/application/domain --include="*.graphql"

# 影響を受けるQueryを検索
grep -r "${RELATED_QUERY}" src/application/domain --include="query.graphql"

# 影響を受けるMutationを検索
grep -r "${RELATED_MUTATION}" src/application/domain --include="mutation.graphql"
```

**検出する衝突:**

#### **衝突パターン1: フィールド型の破壊的変更**

```markdown
### 🔴 Critical: フィールド型の変更

**既存仕様:**
\`\`\`graphql
type GqlWallet {
  balance: Int!  # 現在: Int (非null)
}
\`\`\`

**新要件:**
\`\`\`graphql
type GqlWallet {
  balance: Float  # 変更後: Float (nullable)
}
\`\`\`

**衝突理由:**
- Int → Float は破壊的変更（クライアントの型エラー）
- Non-null → Nullable は破壊的変更（既存クライアントがnullチェックしていない）

**影響範囲:**
- GraphQLクライアント: 全て（iOS, Android, Web）
- 依存Query: `walletBalance`, `userWallet`
- 依存Mutation: `pointTransfer`, `pointWithdraw`

**推奨対策:**
1. **非破壊的移行:** 新フィールド `balanceV2: Float` を追加、既存フィールドは非推奨化
2. **バージョニング:** GraphQL APIのバージョン分離
3. **段階的移行:** クライアント更新完了後に旧フィールド削除
```

---

#### **衝突パターン2: 必須フィールドの追加**

```markdown
### 🟡 Warning: 必須フィールドの追加

**既存仕様:**
\`\`\`graphql
input GqlOpportunityCreateInput {
  title: String!
  description: String!
}
\`\`\`

**新要件:**
\`\`\`graphql
input GqlOpportunityCreateInput {
  title: String!
  description: String!
  requiredSkills: [String!]!  # 新規必須フィールド
}
\`\`\`

**衝突理由:**
- 既存のMutation呼び出しコードが全てエラーになる
- 必須フィールド追加は破壊的変更

**影響範囲:**
- 既存クライアント: `opportunityCreate` Mutation呼び出し箇所全て
- テストコード: E2Eテスト、統合テストの修正必要

**推奨対策:**
1. **オプショナル化:** `requiredSkills: [String!]` （nullable）にする
2. **デフォルト値:** 空配列をデフォルトに設定
3. **段階的移行:** 既存データに対してマイグレーションスクリプトでデフォルト値設定
```

---

### ステップ3: 既存Prismaスキーマの分析

データベーススキーマの変更による衝突を検出:

```bash
# Prismaスキーマを読み取り
cat prisma/schema.prisma

# 影響を受けるモデルを検索
grep -A 30 "model t_${TABLE_NAME}" prisma/schema.prisma

# リレーションを確認
grep -B 5 -A 5 "references: \\[${COLUMN_NAME}\\]" prisma/schema.prisma
```

**検出する衝突:**

#### **衝突パターン3: 外部キー制約の違反**

```markdown
### 🔴 Critical: 外部キー制約の違反

**既存仕様:**
\`\`\`prisma
model t_wallets {
  id          String @id @default(cuid())
  userId      String @unique
  user        t_users @relation(fields: [userId], references: [id], onDelete: Cascade)
}
\`\`\`

**新要件:**
\`\`\`prisma
model t_wallets {
  userId      String  # @unique 削除
  # 1ユーザーが複数ウォレットを持てるように変更
}
\`\`\`

**衝突理由:**
- 既存のビジネスロジックは「1ユーザー = 1ウォレット」を前提
- ユニーク制約削除は既存データ整合性に影響

**影響範囲:**
- WalletService.findByUserId() - 複数結果を返す可能性
- UserResolver.wallet フィールド - 配列に変更必要
- ポイント送受信ロジック - どのウォレットから引き落とすか不明

**推奨対策:**
1. **既存仕様維持:** メインウォレット（isPrimary: true）の概念を導入
2. **段階的移行:** 既存ユーザーは1ウォレット、新規ユーザーのみ複数可
3. **データマイグレーション:** 既存全レコードに isPrimary: true を設定
```

---

#### **衝突パターン4: NOT NULL制約の追加**

```markdown
### 🟡 Warning: NOT NULL制約の追加

**既存仕様:**
\`\`\`prisma
model t_opportunities {
  title       String
  description String?
}
\`\`\`

**新要件:**
\`\`\`prisma
model t_opportunities {
  title       String
  description String  # nullable → non-null
}
\`\`\`

**衝突理由:**
- 既存データに description = null のレコードが存在する可能性
- マイグレーション実行時にエラー

**影響範囲:**
- データベース: 既存の null レコードがマイグレーション失敗の原因に
- GraphQLスキーマ: GqlOpportunity.description の型変更必要

**推奨対策:**
1. **データマイグレーション:** 既存 null レコードにデフォルト値設定
   \`\`\`sql
   UPDATE t_opportunities SET description = '' WHERE description IS NULL;
   \`\`\`
2. **段階的移行:** まず既存データを修正、その後にスキーマ変更
3. **バリデーション追加:** 今後のデータ登録時に必須化
```

---

### ステップ4: 既存ビジネスロジックの分析

Service層のビジネスルールとの衝突を検出:

```bash
# 影響を受けるドメインのServiceを読み取り
find src/application/domain -path "*/${DOMAIN}/*" -name "service.ts"

# ビジネスルールの検索（バリデーション、制約チェック）
grep -A 10 "throw new Error" src/application/domain/${DOMAIN}/service.ts

# 既存のビジネスロジックを検索
grep -A 20 "async ${METHOD_NAME}" src/application/domain/${DOMAIN}/service.ts
```

**検出する衝突:**

#### **衝突パターン5: ビジネスルールの矛盾**

```markdown
### 🔴 Critical: ビジネスルールの矛盾

**既存仕様（OpportunityService.ts）:**
\`\`\`typescript
async createOpportunity(ctx, input, communityId, tx) {
  // ルール: Opportunityは1つのコミュニティにのみ属する
  if (input.communityIds && input.communityIds.length > 1) {
    throw new Error("MULTIPLE_COMMUNITIES_NOT_ALLOWED");
  }
  // ...
}
\`\`\`

**新要件:**
\`\`\`
「複数コミュニティでOpportunityを共有できるようにしたい」
\`\`\`

**衝突理由:**
- 既存ロジックが明示的に複数コミュニティを禁止
- データモデル（communityId: String）が単一値のみ想定
- RLS（ctx.issuer.onlyBelongingCommunity）が単一コミュニティ前提

**影響範囲:**
- OpportunityService.createOpportunity() - バリデーションロジック削除
- OpportunityRepository - communityId → communityIds[] に変更
- GraphQLスキーマ - GqlOpportunity.community → communities に変更
- RLS実装 - 複数コミュニティ対応の認可ロジック必要
- 既存データ - communityId を communityIds 配列に移行

**推奨対策:**
1. **要件の再検討:** 本当に複数コミュニティ共有が必要か確認
2. **中間テーブル:** `t_opportunity_communities` を導入（多対多リレーション）
3. **段階的移行:** 既存Opportunityは単一コミュニティ、新規のみ複数可
4. **後方互換性:** `community` フィールドを非推奨化、`communities` を追加
```

---

#### **衝突パターン6: トランザクション境界の変更**

```markdown
### 🟡 Warning: トランザクション境界の変更

**既存仕様（OpportunityUseCase.ts）:**
\`\`\`typescript
async managerCreateOpportunity({ input, permission }, ctx) {
  return ctx.issuer.onlyBelongingCommunity(ctx, async (tx) => {
    // トランザクション内: Opportunity作成のみ
    const opportunity = await this.service.createOpportunity(ctx, input, permission.communityId, tx);
    return OpportunityPresenter.create(opportunity);
  });
}
\`\`\`

**新要件:**
\`\`\`
「Opportunity作成時に自動的にポイントを付与したい」
\`\`\`

**衝突理由:**
- 新要件はトランザクション内で複数ドメインの操作が必要
- WalletService.transferPoints() の呼び出しが必要
- トランザクション境界が拡大し、デッドロックリスク増加

**影響範囲:**
- OpportunityUseCase - WalletServiceへの依存追加
- トランザクション時間 - 処理時間が増加（パフォーマンス劣化）
- ロールバック範囲 - Opportunity作成失敗時にポイント付与もロールバック

**推奨対策:**
1. **分離:** ポイント付与を非同期処理（イベント駆動）に分離
2. **冪等性:** ポイント付与を再実行可能にする（重複防止）
3. **補償トランザクション:** Opportunity削除時にポイント返却
```

---

### ステップ5: 破壊的変更の検出

既存クライアント（iOS, Android, Web）への影響を評価:

```markdown
## 破壊的変更の検出

### API契約の変更

以下の変更は**破壊的変更**とみなされ、既存クライアントに影響を与えます:

#### **Type Changes（型変更）**
- [ ] Non-null → Nullable（`String!` → `String`）
- [ ] Nullable → Non-null（`String` → `String!`）
- [ ] 型の変更（`Int` → `Float`, `String` → `ID`）
- [ ] Enumの値削除

#### **Field Changes（フィールド変更）**
- [ ] フィールド削除
- [ ] フィールド名変更
- [ ] 必須引数の追加

#### **Query/Mutation Changes（操作変更）**
- [ ] Query/Mutation削除
- [ ] Query/Mutation名変更
- [ ] 必須引数の追加
- [ ] 戻り値の型変更

---

### 検出結果の例

\`\`\`markdown
### 🔴 破壊的変更（3件）

1. **GqlWallet.balance の型変更**
   - 変更: `Int!` → `Float`
   - 影響: 全クライアント
   - 対策: 新フィールド `balanceV2` 追加

2. **GqlOpportunityCreateInput に必須フィールド追加**
   - 変更: `requiredSkills: [String!]!` 追加
   - 影響: `opportunityCreate` Mutation呼び出し全て
   - 対策: オプショナル化またはデフォルト値設定

3. **userWallet Query の削除**
   - 変更: Query削除
   - 影響: ユーザーウォレット表示機能
   - 対策: `userWallets` Query（配列）に移行、非推奨化期間設定
\`\`\`

---

### 🟡 非推奨化が必要な変更（5件）

1. **GqlUser.wallet フィールド**
   - 理由: 複数ウォレット対応により `wallets: [GqlWallet!]!` に変更
   - 対策: `wallet` を非推奨化（@deprecated）、6ヶ月後に削除

2. **pointTransfer Mutation の引数変更**
   - 理由: `walletId` 引数の追加（どのウォレットから送るか指定）
   - 対策: オプショナル引数として追加、未指定時はメインウォレット使用
\`\`\`
```

---

### ステップ6: データ整合性の検証

既存データとの整合性を確認:

```bash
# データベースの統計情報を取得
psql $DATABASE_URL -c "SELECT COUNT(*) FROM t_wallets WHERE description IS NULL;"

# ユニーク制約の確認
psql $DATABASE_URL -c "SELECT userId, COUNT(*) FROM t_wallets GROUP BY userId HAVING COUNT(*) > 1;"

# 外部キー制約の確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM t_opportunities WHERE communityId NOT IN (SELECT id FROM t_communities);"
```

**検出する衝突:**

```markdown
### 🔴 Critical: データ整合性違反

**既存データの状態:**
- `t_wallets` テーブル: 1,234件
  - `description IS NULL`: 567件（46%）
  - 複数ウォレット所有ユーザー: 0件

**新要件による影響:**
1. **description を必須化**
   - 影響: 567件のレコードがマイグレーション失敗
   - 対策: 事前に空文字列を設定するスクリプト実行

2. **userId のユニーク制約削除**
   - 影響: 既存の「1ユーザー1ウォレット」制約が消える
   - 対策: アプリケーション層でバリデーション追加

**推奨マイグレーション:**

\`\`\`sql
-- Step 1: 既存データのクリーンアップ
UPDATE t_wallets SET description = '（説明なし）' WHERE description IS NULL;

-- Step 2: スキーマ変更
ALTER TABLE t_wallets ALTER COLUMN description SET NOT NULL;

-- Step 3: 検証
SELECT COUNT(*) FROM t_wallets WHERE description IS NULL;
-- 期待: 0件
\`\`\`
```

---

### ステップ7: パフォーマンス影響の評価

新要件によるパフォーマンス劣化を予測:

```markdown
## パフォーマンス影響評価

### クエリパフォーマンス

**既存仕様:**
\`\`\`sql
-- 単純なクエリ（インデックス使用）
SELECT * FROM t_wallets WHERE userId = '...';
-- 実行時間: 5ms
\`\`\`

**新要件（複数ウォレット対応）:**
\`\`\`sql
-- 複数レコード取得
SELECT * FROM t_wallets WHERE userId = '...';
-- 実行時間: 15ms（レコード数に依存）
\`\`\`

**影響:**
- GraphQLクエリ: `user.wallets` のレスポンスタイム 3倍増
- N+1問題: DataLoaderの実装が必須

**推奨対策:**
1. **インデックス追加:** `CREATE INDEX idx_wallets_user_id ON t_wallets(userId);`
2. **ページネーション:** ウォレット数が多い場合に備えてカーソルベース実装
3. **DataLoader:** UserResolver.wallets でバッチローディング

---

### トランザクション時間

**既存仕様:**
- トランザクション時間: 平均 50ms
- 操作: Opportunity作成のみ

**新要件（ポイント付与追加）:**
- トランザクション時間: 平均 120ms（2.4倍）
- 操作: Opportunity作成 + ポイント付与 + LINE通知

**影響:**
- デッドロックリスク増加
- 同時実行数の低下

**推奨対策:**
1. **非同期処理:** LINE通知をトランザクション外に移動
2. **タイムアウト設定:** 長時間トランザクションの検出
3. **監視:** トランザクション時間のメトリクス追加
```

---

### ステップ8: セキュリティ影響の評価

認証・認可への影響を確認:

```markdown
## セキュリティ影響評価

### RLS（Row-Level Security）の変更

**既存仕様:**
\`\`\`typescript
// 単一コミュニティのみアクセス可能
ctx.issuer.onlyBelongingCommunity(ctx, async (tx) => {
  return tx.t_opportunities.findUnique({ where: { id } });
});
\`\`\`

**新要件（複数コミュニティ共有）:**
\`\`\`typescript
// どのコミュニティに属していればアクセス可能か？
ctx.issuer.onlyBelongingCommunity(ctx, async (tx) => {
  // 問題: 複数コミュニティのうち1つでも所属していればOK？
  return tx.t_opportunities.findUnique({ where: { id } });
});
\`\`\`

**衝突理由:**
- 既存のRLS実装は単一コミュニティ前提
- 複数コミュニティ対応の認可ロジックが未定義

**推奨対策:**
1. **中間テーブルで制御:** `t_opportunity_communities` で所属確認
2. **カスタムRLSメソッド:** `ctx.issuer.belongsToAnyOfCommunities()`
3. **監査ログ:** アクセス履歴の記録

---

### 認可ロジックの変更

**既存仕様:**
\`\`\`typescript
// マネージャー権限チェック
if (permission.role !== "MANAGER") {
  throw new Error("PERMISSION_DENIED");
}
\`\`\`

**新要件:**
\`\`\`
「一般ユーザーもOpportunityを作成できるようにしたい」
\`\`\`

**影響:**
- セキュリティリスク: 悪意のあるユーザーがスパムOpportunityを作成
- データ品質: 承認フローなしで公開される

**推奨対策:**
1. **承認フロー:** 一般ユーザーの作成は `status: DRAFT`、マネージャーが承認
2. **レート制限:** 1ユーザーあたりの作成数制限
3. **監視:** 異常な作成パターンの検出
```

---

### ステップ9: テスト影響の評価

既存テストへの影響を確認:

```bash
# 影響を受けるテストファイルを検索
find __tests__ -name "*.test.ts" | xargs grep -l "${RELATED_MUTATION}\|${RELATED_QUERY}"

# テストカバレッジの確認
pnpm test:coverage src/application/domain/${DOMAIN}
```

**検出する衝突:**

```markdown
## テスト影響評価

### 既存テストの修正必要（15ファイル）

#### ユニットテスト
- `__tests__/unit/wallet/service.test.ts`
  - 修正: `findByUserId()` の戻り値が配列に変更
  - 修正箇所: 12テストケース

- `__tests__/unit/opportunity/usecase.test.ts`
  - 修正: `communityId` → `communityIds` に変更
  - 修正箇所: 8テストケース

#### 統合テスト
- `__tests__/integration/opportunity/graphql.test.ts`
  - 修正: `opportunityCreate` Mutationの引数追加
  - 修正箇所: 5テストケース

#### E2Eテスト
- `__tests__/e2e/user-journey.test.ts`
  - 修正: `user.wallet` → `user.wallets[0]` に変更
  - 修正箇所: 20テストケース

---

### 新規テストの追加必要

#### 複数ウォレット対応
- [ ] ユーザーが複数ウォレットを持つケース
- [ ] メインウォレットの選択ロジック
- [ ] ウォレット間の送金

#### 複数コミュニティ共有
- [ ] Opportunityが複数コミュニティに表示されるケース
- [ ] 認可ロジック（どのコミュニティからでもアクセス可能）
- [ ] 削除時の挙動（全コミュニティから削除）
```

---

### ステップ10: 衝突レポートの生成

全ての分析結果を統合し、優先度付きのレポートを生成:

```markdown
# 要件衝突レポート

**機能名:** [新機能名]
**分析日:** YYYY-MM-DD
**総合リスク評価:** 🔴 High / 🟡 Medium / 🟢 Low

---

## エグゼクティブサマリー

### 衝突の概要
- **Critical衝突:** 3件（実装ブロッカー）
- **Warning衝突:** 5件（対策必要）
- **Info衝突:** 2件（軽微な影響）

### 総合評価
新要件は既存システムに**重大な影響**を与えます。特に以下の3点が実装のブロッカーとなります:
1. GraphQL型の破壊的変更（全クライアント影響）
2. データモデルの根本的変更（ユニーク制約削除）
3. ビジネスルールの矛盾（複数コミュニティ禁止ルール）

**推奨アクション:** 要件の再検討、または段階的移行計画の策定

---

## 衝突詳細

### 🔴 Critical（実装ブロッカー）

#### 1. GraphQL型の破壊的変更: GqlWallet.balance

**カテゴリ:** API契約違反
**影響範囲:** 全クライアント（iOS, Android, Web）
**リスク:** High

**詳細:**
[詳細説明]

**対策:**
1. 新フィールド `balanceV2: Float` 追加
2. 既存フィールド `balance: Int!` は6ヶ月間非推奨化
3. クライアント移行完了後に削除

**工数見積もり:** 3日（実装1日 + クライアント移行2日）

---

#### 2. データモデルの根本的変更: userId ユニーク制約削除

**カテゴリ:** データ整合性違反
**影響範囲:** Walletドメイン全体
**リスク:** High

**詳細:**
[詳細説明]

**対策:**
1. 中間テーブル導入（`t_user_wallets`）
2. メインウォレットの概念追加（`isPrimary: true`）
3. 段階的移行（既存ユーザーは1ウォレット維持）

**工数見積もり:** 5日（設計2日 + 実装2日 + マイグレーション1日）

---

#### 3. ビジネスルールの矛盾: 複数コミュニティ禁止

**カテゴリ:** ビジネスロジック衝突
**影響範囲:** Opportunityドメイン、RLS
**リスク:** High

**詳細:**
[詳細説明]

**対策:**
1. 要件の再検討（本当に複数コミュニティ共有が必要か）
2. 必要な場合: 中間テーブル `t_opportunity_communities` 導入
3. RLS実装の全面見直し

**工数見積もり:** 10日（設計3日 + 実装5日 + テスト2日）

---

### 🟡 Warning（対策必要）

#### 4. トランザクション時間の増加

**カテゴリ:** パフォーマンス劣化
**影響範囲:** OpportunityUseCase
**リスク:** Medium

**詳細:**
[詳細説明]

**対策:**
1. LINE通知を非同期処理に移動
2. トランザクションタイムアウト監視
3. デッドロック検出アラート

**工数見積もり:** 2日

---

[その他のWarning衝突...]

---

### 🟢 Info（軽微な影響）

#### 10. テストコードの修正

**カテゴリ:** テスト影響
**影響範囲:** 15テストファイル
**リスク:** Low

**詳細:**
[詳細説明]

**対策:**
1. モックデータを新仕様に合わせて修正
2. テストケースの追加

**工数見積もり:** 1日

---

## リスクマトリクス

| # | 衝突内容 | 影響度 | 発生確率 | リスク | 対策優先度 |
|---|---------|--------|----------|--------|-----------|
| 1 | GraphQL型の破壊的変更 | High | 100% | 🔴 Critical | P0 |
| 2 | データモデル変更 | High | 100% | 🔴 Critical | P0 |
| 3 | ビジネスルール矛盾 | High | 100% | 🔴 Critical | P0 |
| 4 | トランザクション時間増加 | Medium | 80% | 🟡 Warning | P1 |
| 5 | データ整合性違反 | Medium | 60% | 🟡 Warning | P1 |

---

## 推奨実装計画

### Phase 1: Critical対応（必須）

**Week 1-2:**
1. 要件の再検討ミーティング
2. GraphQL API バージョニング戦略の決定
3. データモデル設計の見直し

**Week 3-4:**
4. 中間テーブルの導入
5. 非破壊的API変更の実装
6. マイグレーションスクリプトの作成

---

### Phase 2: Warning対応（推奨）

**Week 5-6:**
7. パフォーマンス最適化
8. 非同期処理の実装
9. 監視・アラート設定

---

### Phase 3: Info対応（任意）

**Week 7:**
10. テストコード修正
11. ドキュメント更新

---

## 依存関係と制約

### 実装前提条件
- [ ] クライアントチームとのAPI変更調整
- [ ] データベースバックアップ
- [ ] ステージング環境での動作確認

### 外部依存
- クライアント移行期間: 6ヶ月
- データマイグレーション時間: 推定2時間（ダウンタイム）

---

## 次のステップ

### 即座に実施すべきアクション
1. **要件の再検討:** プロダクトオーナーと要件の妥当性を議論
2. **影響範囲の共有:** 関係者（クライアントチーム、QA）に衝突レポート共有
3. **代替案の検討:** より破壊的でない実装方法の検討

### 実装判断基準
- Critical衝突が **0件** になるまで実装開始しない
- Warning衝突は対策を明確化してから着手
- 総工数が見積もりの **1.5倍**を超える場合は要件分割を検討

---

## 承認

**レビュー担当者:**
- [ ] プロダクトオーナー
- [ ] テックリード
- [ ] アーキテクト

**承認日:** YYYY-MM-DD
**判断:** 承認 / 条件付き承認 / 差し戻し
```

---

## 活用例

### 例1: ポイント有効期限機能

```bash
/check-requirement-delta "ウォレットポイントに有効期限を追加したい"
```

**検出される衝突:**
- 🔴 Critical: `t_wallets` テーブルに `expiresAt` カラム追加（既存データは null）
- 🔴 Critical: `GqlWallet` に `expiresAt` フィールド追加（破壊的ではないが必須）
- 🟡 Warning: ポイント送受信時に有効期限チェックロジック追加（パフォーマンス影響）
- 🟢 Info: 有効期限切れポイントの自動失効バッチ処理が必要

**推奨対策:**
1. `expiresAt: DateTime?` として nullable で追加
2. 既存ポイントは有効期限なし（無期限）
3. 新規付与ポイントのみ有効期限設定
4. バッチ処理で有効期限切れを定期チェック

---

### 例2: 複数コミュニティ間のポイント交換

```bash
/check-requirement-delta docs/requirements/cross-community-points.md
```

**検出される衝突:**
- 🔴 Critical: RLSが単一コミュニティ前提（`onlyBelongingCommunity`）
- 🔴 Critical: ポイント送受信が同一コミュニティ内のみ許可
- 🟡 Warning: 為替レート管理が未定義
- 🟡 Warning: トランザクション境界が2つのコミュニティにまたがる

**推奨対策:**
1. 要件の再検討（本当に必要か、ビジネス価値は？）
2. 必要な場合: 中央プールウォレットを介した交換
3. 為替レートマスタテーブルの追加
4. 2フェーズコミットまたはSagaパターン導入

---

## 注意事項

### 衝突検出の限界

このスキルは以下を検出**できません**:
- ❌ 実行時のバグ（ロジックエラー）
- ❌ 暗黙的な仕様（ドキュメント化されていない前提）
- ❌ クライアント側の実装詳細
- ❌ 外部サービスとの連携仕様

### 推奨される併用スキル

衝突検出後、以下のスキルと組み合わせて使用:
- `/map-impact-analysis` - 影響範囲の可視化
- `/phased-delivery-plan` - 段階的リリース計画
- `/side-effect-brainstorming` - 副作用の洗い出し
- `/migration-requirements` - データマイグレーション計画

---

## 参考資料

以下については `@CLAUDE.md` を参照してください:
- アーキテクチャパターン
- トランザクション管理
- RLSの使い方
- GraphQL命名規則
- マイグレーション戦略
