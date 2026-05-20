---
name: api-compatibility-check
description: API互換性を検証
user-invocable: true
argument-hint: [変更後のスキーマパスまたはPR番号]
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

# civicship-api API互換性チェック

GraphQL APIの**後方互換性**を自動検証し、既存クライアント（iOS, Android, Web）に影響を与える**破壊的変更**を検出します。安全なAPI進化を支援します。

## 使用方法

```bash
# GraphQLスキーマファイルの互換性チェック
/api-compatibility-check src/application/domain/account/wallet/schema/type.graphql

# PR全体のAPIチェック
/api-compatibility-check --pr <PR番号>

# ドメイン全体のスキーマチェック
/api-compatibility-check wallet
```

**引数:**
- `$ARGUMENTS`: GraphQLスキーマファイルのパス、ドメイン名、またはPR番号

---

## API互換性チェックプロセス

### ステップ1: スキーマ変更の抽出

変更されたGraphQLスキーマファイルを特定:

```bash
# PR番号が指定された場合（引数から取得）
PR_NUMBER="${ARGUMENTS}"
gh pr diff "$PR_NUMBER" --name-only | grep "\.graphql$"

# ファイルパスが指定された場合
FILE_PATH="src/application/domain/account/wallet/schema/type.graphql"

# ドメイン名が指定された場合
DOMAIN="wallet"
find src/application/domain -path "*/${DOMAIN}/schema/*.graphql"

# 変更内容を取得
git diff origin/main -- "$FILE_PATH"
```

**変更の種類を分類:**

```markdown
## GraphQLスキーマ変更の分類

### 型定義の変更

#### Type（オブジェクト型）
- [ ] 新しい型の追加
- [ ] 既存の型の削除
- [ ] 型名の変更
- [ ] フィールドの追加
- [ ] フィールドの削除
- [ ] フィールド型の変更
- [ ] フィールドのnullability変更

#### Input（入力型）
- [ ] 新しいInputの追加
- [ ] 既存Inputの削除
- [ ] 必須フィールドの追加
- [ ] フィールドの削除

#### Enum（列挙型）
- [ ] 新しいEnumの追加
- [ ] Enum値の追加
- [ ] Enum値の削除
- [ ] Enum値の変更

#### Interface（インターフェース）
- [ ] 新しいInterfaceの追加
- [ ] Interfaceの削除
- [ ] Interface実装の変更

---

### Query/Mutationの変更

#### Query
- [ ] 新しいQueryの追加
- [ ] Queryの削除
- [ ] Query名の変更
- [ ] 引数の追加（必須/オプショナル）
- [ ] 引数の削除
- [ ] 戻り値の型変更

#### Mutation
- [ ] 新しいMutationの追加
- [ ] Mutationの削除
- [ ] Mutation名の変更
- [ ] 引数の追加（必須/オプショナル）
- [ ] 引数の削除
- [ ] 戻り値の型変更
```

---

### ステップ2: 破壊的変更の検出

**破壊的変更（Breaking Changes）**を自動検出:

#### **パターン1: フィールドの削除**

```markdown
### 🔴 Critical: フィールドの削除

**変更前:**
\`\`\`graphql
type GqlWallet {
  id: ID!
  balance: Int!
  description: String  # このフィールドが削除
  createdAt: DateTime!
}
\`\`\`

**変更後:**
\`\`\`graphql
type GqlWallet {
  id: ID!
  balance: Int!
  # description フィールド削除
  createdAt: DateTime!
}
\`\`\`

---

**破壊的変更の理由:**
- 既存クライアントが `description` フィールドをクエリしている
- クライアントのクエリが失敗（フィールド不存在エラー）

**影響範囲:**
- iOS: `WalletViewModel.swift` で `description` を使用
- Android: `WalletFragment.kt` で `description` を使用
- Web: `WalletCard.tsx` で `description` を表示

**影響度:** 🔴 Critical（既存機能が動作しなくなる）

---

**推奨対策:**

**オプションA: 非推奨化（推奨）**
\`\`\`graphql
type GqlWallet {
  id: ID!
  balance: Int!
  description: String @deprecated(reason: "Use 'note' field instead")
  note: String  # 新フィールド
  createdAt: DateTime!
}
\`\`\`

**移行期間:** 6ヶ月
- Month 1-3: 両方のフィールドを返す
- Month 4-6: クライアント移行を促す警告
- Month 7: `description` フィールドを削除

---

**オプションB: 別名フィールド（エイリアス）**
\`\`\`graphql
type GqlWallet {
  id: ID!
  balance: Int!
  note: String
  description: String  # noteのエイリアス（内部実装は同じ）
  createdAt: DateTime!
}
\`\`\`

**実装:**
\`\`\`typescript
GqlWallet: {
  description: (parent) => parent.note,  // エイリアス
  note: (parent) => parent.note
}
\`\`\`

---

**オプションC: スキーマバージョニング**
\`\`\`
/graphql/v1 - description フィールドあり
/graphql/v2 - description フィールドなし
\`\`\`

**非推奨:** 運用コストが高い、最終手段のみ
```

---

#### **パターン2: Non-null → Nullable への変更**

```markdown
### 🟡 Warning: Non-null → Nullable への変更

**変更前:**
\`\`\`graphql
type GqlWallet {
  balance: Int!  # Non-null
}
\`\`\`

**変更後:**
\`\`\`graphql
type GqlWallet {
  balance: Int  # Nullable
}
\`\`\`

---

**破壊的変更の理由:**
- TypeScriptクライアント: `wallet.balance` の型が `number` → `number | null` に変更
- 既存コードが nullチェックしていない場合、実行時エラー

**影響範囲:**
- TypeScriptクライアント: 全ての `wallet.balance` 使用箇所
- Swift/Kotlinクライアント: Optional型への変更必要

**影響度:** 🟡 Medium（型エラー、実行時エラーの可能性）

---

**推奨対策:**

**対策1: クライアントコード修正**
\`\`\`typescript
// 修正前
const points = wallet.balance;

// 修正後
const points = wallet.balance ?? 0;  // nullの場合は0
\`\`\`

**対策2: スキーマ変更の再検討**
- 本当に nullable が必要か？
- デフォルト値（0）を返すことで Non-null を維持できないか？

**移行計画:**
1. Week 1-2: クライアントチームにnullチェック追加を依頼
2. Week 3: 全クライアントの修正完了確認
3. Week 4: スキーマ変更をデプロイ
```

---

#### **パターン3: Nullable → Non-null への変更**

```markdown
### 🔴 Critical: Nullable → Non-null への変更

**変更前:**
\`\`\`graphql
type GqlWallet {
  description: String  # Nullable
}
\`\`\`

**変更後:**
\`\`\`graphql
type GqlWallet {
  description: String!  # Non-null
}
\`\`\`

---

**破壊的変更の理由:**
- バックエンドが null を返す可能性があるのに、スキーマは Non-null を約束
- GraphQLエラーが発生（null を返せない）

**影響範囲:**
- 既存データに `description = null` のレコードが存在
- GraphQLクエリが全てエラーになる可能性

**影響度:** 🔴 Critical（サービス停止の可能性）

---

**推奨対策:**

**対策1: データマイグレーション（必須）**
\`\`\`sql
-- 既存の null データにデフォルト値を設定
UPDATE t_wallets SET description = '（説明なし）' WHERE description IS NULL;
\`\`\`

**対策2: バックエンド実装の確認**
\`\`\`typescript
// Presenterで必ず値を返すように
static toGraphQL(wallet: PrismaWallet): GqlWallet {
  return {
    description: wallet.description || '（説明なし）',  // null の場合デフォルト値
  };
}
\`\`\`

**移行計画:**
1. データマイグレーション実行
2. バックエンド実装でnullを返さないように修正
3. テストで null が返らないことを確認
4. スキーマ変更をデプロイ
```

---

#### **パターン4: 型の変更**

```markdown
### 🔴 Critical: フィールド型の変更

**変更前:**
\`\`\`graphql
type GqlWallet {
  balance: Int!
}
\`\`\`

**変更後:**
\`\`\`graphql
type GqlWallet {
  balance: Float!  # Int → Float
}
\`\`\`

---

**破壊的変更の理由:**
- クライアントの型定義が変わる（`number (int)` → `number (float)`）
- 精度の問題（小数点以下の扱い）
- 既存のバリデーションロジックが動作しない可能性

**影響範囲:**
- 全クライアント: `balance` を使用する全ての箇所
- 既存のバリデーション: 整数チェックが無効化

**影響度:** 🔴 Critical

---

**推奨対策:**

**対策1: 新フィールド追加（推奨）**
\`\`\`graphql
type GqlWallet {
  balance: Int! @deprecated(reason: "Use balanceV2 instead")
  balanceV2: Float!
}
\`\`\`

**移行期間:** 6ヶ月

---

**対策2: 単位変更（別の型として扱う）**
\`\`\`graphql
type GqlWallet {
  balancePoints: Int!  # ポイント単位
  balanceYen: Float!   # 円単位
}
\`\`\`

**注意:** 型変更は極力避け、新フィールド追加を推奨
```

---

#### **パターン5: 必須引数の追加**

```markdown
### 🔴 Critical: 必須引数の追加

**変更前:**
\`\`\`graphql
type Query {
  walletList(userId: ID!): [GqlWallet!]!
}
\`\`\`

**変更後:**
\`\`\`graphql
type Query {
  walletList(
    userId: ID!
    communityId: ID!  # 新しい必須引数
  ): [GqlWallet!]!
}
\`\`\`

---

**破壊的変更の理由:**
- 既存のクエリが全てエラーになる（必須引数が不足）
- クライアントコードの全面修正が必要

**影響範囲:**
- 全クライアント: `walletList` クエリを使用する全ての箇所

**影響度:** 🔴 Critical

---

**推奨対策:**

**対策1: オプショナル引数として追加（推奨）**
\`\`\`graphql
type Query {
  walletList(
    userId: ID!
    communityId: ID  # オプショナル（nullable）
  ): [GqlWallet!]!
}
\`\`\`

**実装:**
\`\`\`typescript
async walletList(_, { userId, communityId }, ctx) {
  if (!communityId) {
    // communityId が未指定の場合は全てのウォレットを返す
    return this.usecase.listAllWallets(userId, ctx);
  }
  return this.usecase.listWalletsByCommunity(userId, communityId, ctx);
}
\`\`\`

---

**対策2: デフォルト値を設定**
\`\`\`graphql
type Query {
  walletList(
    userId: ID!
    communityId: ID! = "default"  # デフォルト値
  ): [GqlWallet!]!
}
\`\`\`

**注意:** GraphQL標準ではデフォルト値をサポートするが、セマンティクスに注意

---

**対策3: 新しいQueryを追加**
\`\`\`graphql
type Query {
  walletList(userId: ID!): [GqlWallet!]!  # 既存
  walletListByCommunity(userId: ID!, communityId: ID!): [GqlWallet!]!  # 新規
}
\`\`\`

**推奨:** 既存Queryは維持、新しいQueryで新機能を提供
```

---

#### **パターン6: Enum値の削除**

```markdown
### 🔴 Critical: Enum値の削除

**変更前:**
\`\`\`graphql
enum GqlWalletStatus {
  ACTIVE
  INACTIVE
  SUSPENDED  # この値を削除
}
\`\`\`

**変更後:**
\`\`\`graphql
enum GqlWalletStatus {
  ACTIVE
  INACTIVE
  # SUSPENDED 削除
}
\`\`\`

---

**破壊的変更の理由:**
- 既存データに `SUSPENDED` ステータスのウォレットが存在
- GraphQLクエリが失敗（不正なEnum値）
- クライアントが `SUSPENDED` を期待している

**影響範囲:**
- 既存データ: `status = SUSPENDED` のレコード
- クライアント: `SUSPENDED` を扱うコード

**影響度:** 🔴 Critical

---

**推奨対策:**

**対策1: 非推奨化（推奨）**
\`\`\`graphql
enum GqlWalletStatus {
  ACTIVE
  INACTIVE
  SUSPENDED @deprecated(reason: "Use INACTIVE instead")
}
\`\`\`

**移行計画:**
1. 既存の `SUSPENDED` データを `INACTIVE` に移行
2. 6ヶ月の非推奨期間
3. Enum値削除

---

**対策2: マッピング**
\`\`\`typescript
// Presenter でマッピング
static toGraphQL(wallet: PrismaWallet): GqlWallet {
  const statusMap = {
    ACTIVE: 'ACTIVE',
    INACTIVE: 'INACTIVE',
    SUSPENDED: 'INACTIVE',  // SUSPENDED → INACTIVE にマップ
  };
  return {
    status: statusMap[wallet.status] || 'INACTIVE',
  };
}
\`\`\`
```

---

### ステップ3: 非破壊的変更の検出

**安全な変更（Non-Breaking Changes）**を確認:

```markdown
## 非破壊的変更（安全）

以下の変更は既存クライアントに**影響を与えません**:

### ✅ 安全な変更

#### 型の追加
- [ ] 新しい Type の追加
- [ ] 新しい Input の追加
- [ ] 新しい Enum の追加

#### フィールドの追加
- [ ] Type に新しいフィールドを追加（nullable または デフォルト値あり）
- [ ] Input にオプショナルフィールドを追加

#### Query/Mutation の追加
- [ ] 新しい Query の追加
- [ ] 新しい Mutation の追加
- [ ] Query/Mutation にオプショナル引数を追加

#### Enum値の追加
- [ ] Enum に新しい値を追加

#### Nullable → Non-null（レスポンス）
- [ ] レスポンス型を Nullable → Non-null に変更（常に値を返す場合）
  - 注意: データとバックエンド実装を確認

---

### 📋 変更例

**安全な変更の例:**

\`\`\`graphql
# 変更前
type GqlWallet {
  id: ID!
  balance: Int!
}

# 変更後（安全）
type GqlWallet {
  id: ID!
  balance: Int!
  expiresAt: DateTime  # 新しいフィールド追加（nullable）
  note: String         # 新しいフィールド追加（nullable）
}
\`\`\`

**理由:** 既存のクエリは新しいフィールドを要求しないため、影響なし
```

---

### ステップ4: クライアント影響分析

各クライアントへの影響を評価:

```markdown
## クライアント影響分析

### iOS アプリ

**影響を受けるファイル（推定）:**
- `WalletViewModel.swift` - ウォレット表示ロジック
- `WalletListViewController.swift` - ウォレット一覧画面
- `PointTransferViewModel.swift` - ポイント送受信

**破壊的変更による影響:**
- [ ] `balance: Int` → `balance: Float` の型変更
  - Swift側の型を `Int` → `Double` に変更
  - 影響箇所: 15ファイル
  - 修正工数: 2日

- [ ] `description` フィールドの削除
  - UI表示ロジックの修正
  - 影響箇所: 3ファイル
  - 修正工数: 0.5日

**総工数:** 2.5日

---

### Android アプリ

**影響を受けるファイル（推定）:**
- `WalletFragment.kt` - ウォレット表示
- `WalletAdapter.kt` - ウォレットリスト
- `PointTransferActivity.kt` - ポイント送受信

**破壊的変更による影響:**
- [ ] `balance: Int` → `balance: Float` の型変更
  - Kotlin側の型を `Int` → `Float` に変更
  - 影響箇所: 12ファイル
  - 修正工数: 2日

- [ ] `description` フィールドの削除
  - UI表示ロジックの修正
  - 影響箇所: 2ファイル
  - 修正工数: 0.5日

**総工数:** 2.5日

---

### Web アプリ

**影響を受けるファイル（推定）:**
- `WalletCard.tsx` - ウォレットカードコンポーネント
- `WalletList.tsx` - ウォレット一覧
- `PointTransfer.tsx` - ポイント送受信

**破壊的変更による影響:**
- [ ] `balance: Int` → `balance: Float` の型変更
  - TypeScript型定義の変更（自動生成）
  - 影響箇所: 8ファイル
  - 修正工数: 1日

- [ ] `description` フィールドの削除
  - コンポーネントの修正
  - 影響箇所: 3ファイル
  - 修正工数: 0.5日

**総工数:** 1.5日

---

### 総工数見積もり

| クライアント | 修正工数 | テスト工数 | 合計 |
|------------|---------|-----------|------|
| iOS | 2.5日 | 1日 | 3.5日 |
| Android | 2.5日 | 1日 | 3.5日 |
| Web | 1.5日 | 0.5日 | 2日 |
| **合計** | **6.5日** | **2.5日** | **9日** |
```

---

### ステップ5: 互換性スコアの算出

API互換性を数値化:

```markdown
## API互換性スコア

### スコア計算式

\`\`\`
互換性スコア = 100 - (Critical * 10 + Warning * 5 + Info * 1)
\`\`\`

### 検出結果

- **Critical（破壊的変更）:** 3件
  - フィールド削除: 1件
  - 型変更: 1件
  - 必須引数追加: 1件

- **Warning（注意が必要）:** 2件
  - Non-null → Nullable: 1件
  - Enum値追加: 1件

- **Info（軽微な変更）:** 5件
  - フィールド追加: 5件

### 互換性スコア

\`\`\`
スコア = 100 - (3 * 10 + 2 * 5 + 5 * 1)
      = 100 - (30 + 10 + 5)
      = 55 / 100
\`\`\`

**評価:** 🔴 Poor（破壊的変更が多い）

---

### スコア基準

| スコア | 評価 | 判断 |
|--------|------|------|
| 90-100 | 🟢 Excellent | リリース可能 |
| 70-89 | 🟡 Good | 軽微な修正で可能 |
| 50-69 | 🟠 Fair | 対策必須 |
| 0-49 | 🔴 Poor | 大幅な見直し必要 |

**現在のスコア: 55 / 100** → 🟠 Fair
```

---

### ステップ6: スキーマ進化戦略の提案

安全なスキーマ進化の方針を提案:

```markdown
## スキーマ進化戦略

### 原則

1. **非破壊的変更を優先**
   - フィールド削除 → 非推奨化
   - 型変更 → 新フィールド追加
   - 必須引数追加 → オプショナル化

2. **段階的移行**
   - 非推奨化期間: 6ヶ月
   - クライアント移行完了後に削除

3. **バージョニングは最終手段**
   - 運用コストが高い
   - 本当に必要な場合のみ

---

### 推奨アクション

#### Action 1: フィールド削除の回避

**現在の変更:**
\`\`\`graphql
type GqlWallet {
  id: ID!
  balance: Int!
  # description: String  # 削除予定
}
\`\`\`

**推奨変更:**
\`\`\`graphql
type GqlWallet {
  id: ID!
  balance: Int!
  description: String @deprecated(reason: "No longer used, will be removed in v2.0")
}
\`\`\`

**実装:**
\`\`\`typescript
// Presenter でダミー値を返す
static toGraphQL(wallet: PrismaWallet): GqlWallet {
  return {
    description: "",  // 空文字列を返す（削除しない）
  };
}
\`\`\`

---

#### Action 2: 型変更の回避

**現在の変更:**
\`\`\`graphql
type GqlWallet {
  balance: Float!  # Int から Float に変更
}
\`\`\`

**推奨変更:**
\`\`\`graphql
type GqlWallet {
  balance: Int! @deprecated(reason: "Use balanceV2 for decimal support")
  balanceV2: Float!
}
\`\`\`

**実装:**
\`\`\`typescript
static toGraphQL(wallet: PrismaWallet): GqlWallet {
  return {
    balance: Math.floor(wallet.balance),  # 既存フィールドは整数
    balanceV2: wallet.balance,            # 新フィールドは小数対応
  };
}
\`\`\`

---

#### Action 3: 必須引数追加の回避

**現在の変更:**
\`\`\`graphql
type Query {
  walletList(userId: ID!, communityId: ID!): [GqlWallet!]!  # communityId 必須
}
\`\`\`

**推奨変更:**
\`\`\`graphql
type Query {
  walletList(userId: ID!, communityId: ID): [GqlWallet!]!  # communityId オプショナル
}
\`\`\`

**実装:**
\`\`\`typescript
async walletList(_, { userId, communityId }, ctx) {
  if (communityId) {
    return this.usecase.listByCommunity(userId, communityId, ctx);
  }
  // communityId未指定時は全ウォレット
  return this.usecase.listAll(userId, ctx);
}
\`\`\`
```

---

### ステップ7: 移行計画の策定

破壊的変更の移行スケジュール:

```markdown
## 移行計画

### タイムライン（6ヶ月）

#### Month 1-2: 非推奨化フェーズ

**Week 1:**
- [ ] `@deprecated` ディレクティブを追加
- [ ] ドキュメントに非推奨の理由を記載
- [ ] クライアントチームに通知

**Week 2-8:**
- [ ] クライアントチームが新フィールドへ移行
- [ ] 移行状況を監視（旧フィールドの使用率）

---

#### Month 3-4: 移行促進フェーズ

**Week 9-12:**
- [ ] 旧フィールドの使用率をモニタリング
- [ ] 使用率が高い場合、クライアントチームに再通知
- [ ] 移行期限を明確化

**Week 13-16:**
- [ ] 最終移行期限のアナウンス（Month 6 末）
- [ ] クライアント移行完了の確認

---

#### Month 5-6: 削除準備フェーズ

**Week 17-20:**
- [ ] 全クライアントの移行完了確認
- [ ] 旧フィールドの使用率 < 1%
- [ ] 削除のリハーサル（ステージング環境）

**Week 21-24:**
- [ ] 本番環境で旧フィールド削除
- [ ] スキーマから `@deprecated` 削除
- [ ] ドキュメント更新

---

### 移行完了条件

- [ ] iOS アプリ: 最新バージョンが新フィールドを使用
- [ ] Android アプリ: 最新バージョンが新フィールドを使用
- [ ] Web アプリ: デプロイ済み
- [ ] 旧フィールドの使用率 < 1%
- [ ] 全ステークホルダーの承認
```

---

### ステップ8: テスト戦略

API互換性のテスト:

```markdown
## テスト戦略

### GraphQLスキーマテスト

**ツール:** `@graphql-inspector/cli`

\`\`\`bash
# スキーマの破壊的変更を検出
npx graphql-inspector diff \
  --schema="origin/main:src/presentation/graphql/schema.graphql" \
  --schema="HEAD:src/presentation/graphql/schema.graphql"
\`\`\`

**出力例:**
\`\`\`
✖ Field 'description' was removed from type 'GqlWallet' (FIELD_REMOVED)
✖ Type of field 'balance' changed from 'Int!' to 'Float!' (FIELD_TYPE_CHANGED)
✔ Field 'expiresAt' was added to type 'GqlWallet' (FIELD_ADDED)
\`\`\`

---

### 既存クエリの互換性テスト

**テストファイル:** `__tests__/compatibility/graphql-schema.test.ts`

\`\`\`typescript
describe("GraphQL Schema Compatibility", () => {
  it("既存のクエリが動作する", async () => {
    const query = \`
      query {
        wallet(id: "wallet-id") {
          id
          balance
          description  # 非推奨フィールドも動作すること
        }
      }
    \`;

    const response = await executeQuery(query);
    expect(response.errors).toBeUndefined();
    expect(response.data.wallet).toBeDefined();
  });

  it("非推奨フィールドに警告が含まれる", async () => {
    const query = \`
      query {
        wallet(id: "wallet-id") {
          description @deprecated
        }
      }
    \`;

    const response = await executeQuery(query);
    // 警告はあるがエラーではない
    expect(response.data.wallet).toBeDefined();
  });
});
\`\`\`

---

### クライアント統合テスト

**iOS:**
\`\`\`swift
func testWalletQueryBackwardCompatibility() {
    let query = WalletQuery(id: "wallet-id")

    apollo.fetch(query: query) { result in
        XCTAssertNotNil(result.data?.wallet)
        XCTAssertNotNil(result.data?.wallet.balance)
        // description は非推奨だが動作すること
        XCTAssertNotNil(result.data?.wallet.description)
    }
}
\`\`\`

**Android:**
\`\`\`kotlin
@Test
fun testWalletQueryBackwardCompatibility() {
    val query = WalletQuery(id = "wallet-id")

    apolloClient.query(query).execute().let { response ->
        assertNotNull(response.data?.wallet)
        assertNotNull(response.data?.wallet?.balance)
        // description は非推奨だが動作すること
        assertNotNull(response.data?.wallet?.description)
    }
}
\`\`\`
```

---

### ステップ9: 監視とアラート

API使用状況の監視:

```markdown
## 監視とアラート

### 非推奨フィールドの使用状況

**メトリクス:**
\`\`\`typescript
// GraphQL Resolverで使用状況を記録
GqlWallet: {
  description: (parent, _, ctx) => {
    // 非推奨フィールドへのアクセスをログ
    metrics.increment("graphql.deprecated_field.access", {
      field: "GqlWallet.description",
      client: ctx.clientName,
      version: ctx.clientVersion
    });
    return parent.description || "";
  }
}
\`\`\`

**ダッシュボード:**
- 非推奨フィールドの使用率（日次）
- クライアント別の使用状況
- バージョン別の使用状況

---

### アラート設定

**警告レベル:**
- 非推奨フィールド使用率 > 50% で通知（移行が進んでいない）
- 削除予定日の1ヶ月前に使用率 > 10% で警告

**緊急レベル:**
- 破壊的変更デプロイ後、エラー率 > 5% で緊急アラート
```

---

### ステップ10: 互換性レポートの生成

全ての分析結果を統合:

```markdown
# API互換性レポート

**対象スキーマ:** wallet/schema/type.graphql
**分析日:** YYYY-MM-DD
**互換性スコア:** 55 / 100 🟠 Fair

---

## 破壊的変更（3件）

### 1. フィールドの削除: GqlWallet.description

**影響度:** 🔴 Critical
**影響範囲:** iOS (3ファイル), Android (2ファイル), Web (3ファイル)
**推奨対策:** 非推奨化（6ヶ月間）
**工数:** 0.5日 × 3クライアント = 1.5日

---

### 2. 型の変更: GqlWallet.balance (Int → Float)

**影響度:** 🔴 Critical
**影響範囲:** iOS (15ファイル), Android (12ファイル), Web (8ファイル)
**推奨対策:** 新フィールド `balanceV2` 追加
**工数:** 2日 × 3クライアント = 6日

---

### 3. 必須引数の追加: walletList.communityId

**影響度:** 🔴 Critical
**影響範囲:** 全クライアント
**推奨対策:** オプショナル引数に変更
**工数:** 1日 × 3クライアント = 3日

---

## 総工数

| 項目 | 工数 |
|------|------|
| クライアント修正 | 10.5日 |
| テスト | 2.5日 |
| 移行期間 | 6ヶ月 |

---

## 推奨アクション

1. **即座:** 破壊的変更を非破壊的変更に修正
2. **Week 1:** 非推奨化ディレクティブ追加
3. **Month 1-6:** クライアント移行期間
4. **Month 7:** 旧フィールド削除

---

## 承認

- [ ] テックリード
- [ ] iOSリード
- [ ] Androidリード
- [ ] Webリード
```

---

## 活用例

### 例1: PRのAPI互換性チェック

```bash
/api-compatibility-check --pr <PR番号>
```

**出力:**
- 破壊的変更: 2件
- 互換性スコア: 70 / 100
- 推奨対策: 非推奨化

---

### 例2: 特定スキーマファイルのチェック

```bash
/api-compatibility-check src/application/domain/account/wallet/schema/type.graphql
```

**出力:**
- 変更内容の分析
- クライアント影響評価
- 移行計画

---

## 注意事項

### チェックの限界

- ❌ クライアント側の実装詳細（どのフィールドを実際に使用しているか）
- ❌ ビジネスロジックの意味的な変更
- ❌ パフォーマンスへの影響

### 推奨される併用スキル

- `/map-impact-analysis` - バックエンド側の影響範囲
- `/phased-delivery-plan` - 段階的な移行計画
- `/check-requirement-delta` - 要件との整合性

---

## 参考資料

以下については `@CLAUDE.md` を参照してください:
- GraphQL命名規則
- スキーマ設計のベストプラクティス
- 非推奨化の方針
