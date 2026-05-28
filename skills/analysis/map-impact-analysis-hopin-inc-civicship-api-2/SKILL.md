---
name: map-impact-analysis
description: 影響範囲を分析
user-invocable: true
argument-hint: [変更対象ファイルまたはドメイン名]
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

# civicship-api 影響範囲分析

コード変更の**影響範囲を可視化**し、影響を受けるファイル、ドメイン、機能を特定します。テストすべき範囲を明確にし、予期しない副作用を防ぎます。

## 使用方法

```bash
# 特定ファイルの変更影響を分析
/map-impact-analysis src/application/domain/account/wallet/service.ts

# ドメイン全体の影響を分析
/map-impact-analysis wallet

# 複数ファイルの影響を分析（PRのdiffから）
/map-impact-analysis --pr <PR番号>
```

**引数:**
- `$ARGUMENTS`: ファイルパス、ドメイン名、またはPR番号

---

## 影響範囲分析プロセス

### ステップ1: 変更対象の特定

変更対象のファイルを特定し、種類を分類:

```bash
# ファイルが指定された場合
FILE_PATH="src/application/domain/account/wallet/service.ts"

# ドメイン名が指定された場合
DOMAIN="wallet"
find src/application/domain -path "*/${DOMAIN}/*" -name "*.ts"

# PR番号が指定された場合（引数から取得）
PR_NUMBER="${ARGUMENTS}"
gh pr diff "$PR_NUMBER" --name-only
```

**ファイル種類の分類:**

```markdown
## 変更対象ファイル

### レイヤー分類

**Application Layer:**
- [x] Service層 (`service.ts`) - ビジネスロジック
- [x] UseCase層 (`usecase.ts`) - フロー制御
- [ ] Repository層 (`data/repository.ts`) - データアクセス
- [ ] Converter層 (`data/converter.ts`) - 入力変換
- [ ] Presenter層 (`presenter.ts`) - 出力変換
- [ ] Resolver層 (`controller/resolver.ts`) - GraphQLエンドポイント
- [ ] DataLoader層 (`controller/dataloader.ts`) - バッチローディング

**Infrastructure Layer:**
- [ ] Prismaスキーマ (`prisma/schema.prisma`)
- [ ] マイグレーション (`prisma/migrations/`)

**Presentation Layer:**
- [ ] GraphQLスキーマ (`schema/*.graphql`)
- [ ] 認証ルール (`presentation/graphql/rule.ts`)
- [ ] ミドルウェア (`presentation/middleware/`)

**その他:**
- [ ] 型定義 (`src/types/`)
- [ ] 設定ファイル (`src/config/`)
- [ ] ユーティリティ (`src/lib/`, `src/util/`)
```

---

### ステップ2: 直接的な依存関係の解析

変更対象ファイルに**直接依存しているファイル**を特定:

```bash
# ファイルが他のファイルにimportされている箇所を検索
FILE_NAME="WalletService"
grep -r "import.*${FILE_NAME}" src/ --include="*.ts" --exclude="*.test.ts"

# クラス名/関数名が使用されている箇所を検索
grep -r "${FILE_NAME}" src/ --include="*.ts" --exclude="*.test.ts"

# DI（Dependency Injection）での使用箇所を検索
grep -r "@inject.*${FILE_NAME}" src/ --include="*.ts"
```

**影響を受けるファイルのリスト:**

```markdown
## 直接的な依存関係（12ファイル）

### 同じドメイン内（6ファイル）

1. **src/application/domain/account/wallet/usecase.ts**
   - 依存関係: `WalletService` をコンストラクタでインジェクト
   - 使用箇所: 8箇所（全てのUseCaseメソッド）
   - 影響度: 🔴 High

2. **src/application/domain/account/wallet/data/repository.ts**
   - 依存関係: `WalletService` から呼び出し
   - 使用箇所: 5箇所（CRUD操作）
   - 影響度: 🟡 Medium

3. **src/application/domain/account/wallet/controller/resolver.ts**
   - 依存関係: UseCaseを経由して間接的に依存
   - 使用箇所: 全GraphQLエンドポイント
   - 影響度: 🔴 High

[...以下略...]

---

### 他ドメインからの依存（6ファイル）

1. **src/application/domain/transaction/point-transfer/service.ts**
   - 依存関係: ポイント送受信時に `WalletService` を呼び出し
   - 使用箇所: `transferPoints()` メソッド
   - 影響度: 🔴 High（コアビジネスロジック）

2. **src/application/domain/reward/utility/usecase.ts**
   - 依存関係: 特典交換時にポイント減算
   - 使用箇所: `exchangeUtility()` メソッド
   - 影響度: 🟡 Medium

3. **src/application/domain/experience/opportunity/usecase.ts**
   - 依存関係: Opportunity参加時にポイント減算
   - 使用箇所: `participateOpportunity()` メソッド
   - 影響度: 🟡 Medium

[...以下略...]
```

---

### ステップ3: 間接的な依存関係の解析

**間接的に影響を受けるファイル**を特定（依存の連鎖）:

`madge` を使用して、完全な依存関係グラフを生成し、再帰的な依存を正確に追跡:

```bash
# madge で依存関係グラフを生成（JSON形式）
npx madge --json src/application/domain/"${DOMAIN}" > dependencies.json

# 循環依存の検出（あれば警告）
npx madge --circular src/application/domain/"${DOMAIN}"

# 依存関係を可視化（SVG画像）
npx madge --image impact-graph.svg src/application/domain/"${DOMAIN}"

# 特定ファイルに依存しているファイルを抽出
npx madge --depends "${CHANGED_FILE}" src/

# 特定ファイルが依存しているファイルを抽出
npx madge --orphans src/application/domain/"${DOMAIN}"
```

**madgeの利点:**
- ✅ 再帰的な依存関係を完全に追跡（N階層の依存連鎖）
- ✅ 循環依存の自動検出
- ✅ 依存関係の可視化（SVG/画像生成）
- ✅ JSON出力でプログラマティックな解析が可能

**依存関係グラフ:**

```markdown
## 依存関係グラフ

\`\`\`
WalletService.ts (変更対象)
│
├─ WalletUseCase.ts (直接依存)
│  │
│  ├─ WalletResolver.ts (間接依存: GraphQL)
│  │  └─ クライアント: iOS, Android, Web (影響)
│  │
│  └─ WalletDataLoader.ts (間接依存: N+1防止)
│
├─ PointTransferService.ts (直接依存)
│  │
│  ├─ PointTransferUseCase.ts (間接依存)
│  │  └─ PointTransferResolver.ts (間接依存: GraphQL)
│  │
│  └─ NotificationService.ts (間接依存: LINE通知)
│
└─ UtilityUseCase.ts (直接依存)
   └─ UtilityResolver.ts (間接依存: GraphQL)
\`\`\`

---

## 影響の連鎖（3レベル）

### Level 1: 直接依存（6ファイル）
- WalletUseCase.ts
- PointTransferService.ts
- UtilityUseCase.ts
- OpportunityUseCase.ts
- MembershipService.ts
- WalletRepository.ts

### Level 2: 間接依存（12ファイル）
- WalletResolver.ts
- PointTransferUseCase.ts
- PointTransferResolver.ts
- UtilityResolver.ts
- OpportunityResolver.ts
- MembershipUseCase.ts
- NotificationService.ts
- [...]

### Level 3: さらに間接的な依存（8ファイル）
- UserResolver.ts（user.wallet フィールド）
- CommunityResolver.ts（community.wallets フィールド）
- LineMessageService.ts（ポイント通知）
- [...]
```

---

### ステップ4: データベーススキーマの影響分析

Prismaスキーマ変更による影響を分析:

```bash
# 変更対象がPrismaスキーマの場合
if [[ "$FILE_PATH" == *"prisma/schema.prisma"* ]]; then
  # 影響を受けるモデルを特定
  git diff origin/main -- prisma/schema.prisma
fi

# モデルを使用しているファイルを検索
grep -r "t_wallets" src/ --include="*.ts"
```

**Prismaスキーマ変更の影響:**

```markdown
## Prismaスキーマ変更の影響

### 変更内容

\`\`\`diff
model t_wallets {
  id          String   @id @default(cuid())
  userId      String   @unique
+ expiresAt   DateTime?  # 新規追加
  createdAt   DateTime @default(now())
}
\`\`\`

---

### 影響を受けるファイル（25ファイル）

#### Repository層（直接影響）
- **src/application/domain/account/wallet/data/repository.ts**
  - 影響: SELECT句に `expiresAt` 追加必要
  - 影響度: 🔴 High

- **src/application/domain/account/wallet/data/type.ts**
  - 影響: `walletSelect` の型定義更新
  - 影響度: 🔴 High

#### Service層（間接影響）
- **src/application/domain/account/wallet/service.ts**
  - 影響: 有効期限チェックロジック追加
  - 影響度: 🟡 Medium

#### Presenter層（間接影響）
- **src/application/domain/account/wallet/presenter.ts**
  - 影響: GraphQL型への変換ロジック追加
  - 影響度: 🟡 Medium

#### テストファイル（全て更新必要）
- **__tests__/unit/wallet/service.test.ts**
  - 影響: モックデータに `expiresAt` 追加
  - 影響度: 🟢 Low

[...以下略...]
```

---

### ステップ5: GraphQLスキーマの影響分析

GraphQLスキーマ変更によるクライアント側への影響:

```bash
# GraphQLスキーマファイルの変更を検出
find src/application/domain -name "*.graphql" -newer .git/ORIG_HEAD

# 変更されたGraphQL型を抽出
git diff origin/main -- '**/*.graphql' | grep "^[+-].*type\|^[+-].*input\|^[+-].*enum"
```

**GraphQLスキーマ変更の影響:**

```markdown
## GraphQLスキーマ変更の影響

### 変更内容

\`\`\`diff
type GqlWallet {
  id: ID!
  balance: Int!
+ expiresAt: DateTime  # 新規追加
  createdAt: DateTime!
}
\`\`\`

---

### 影響を受けるクライアント

#### iOS アプリ
- **影響ファイル:** `WalletViewModel.swift`
- **影響範囲:** ウォレット表示画面
- **対応必要:** `expiresAt` フィールドの表示追加
- **破壊的変更:** ❌ なし（フィールド追加のみ）
- **影響度:** 🟢 Low（オプショナルフィールド）

#### Android アプリ
- **影響ファイル:** `WalletFragment.kt`
- **影響範囲:** ウォレット表示画面
- **対応必要:** `expiresAt` フィールドの表示追加
- **破壊的変更:** ❌ なし
- **影響度:** 🟢 Low

#### Web アプリ
- **影響ファイル:** `WalletCard.tsx`
- **影響範囲:** ウォレットカードコンポーネント
- **対応必要:** `expiresAt` の表示ロジック追加
- **破壊的変更:** ❌ なし
- **影響度:** 🟢 Low

---

### 破壊的変更のチェック

- [ ] Non-null → Nullable
- [ ] Nullable → Non-null
- [ ] 型の変更（Int → Float, String → ID など）
- [ ] フィールド削除
- [ ] フィールド名変更
- [ ] 必須引数の追加
- [ ] Enum値の削除

**結果:** ✅ 破壊的変更なし
```

---

### ステップ6: ビジネスロジックの影響分析

ビジネスルール変更による他機能への影響:

```bash
# Service層のビジネスロジックを分析
FILE="src/application/domain/account/wallet/service.ts"

# 変更されたメソッドを特定
git diff origin/main -- "$FILE" | grep "^[+-].*async\|^[+-].*function"

# そのメソッドを呼び出している箇所を検索
METHOD_NAME="findByUserId"
grep -r "${METHOD_NAME}" src/ --include="*.ts" --exclude="*.test.ts"
```

**ビジネスロジック変更の影響:**

```markdown
## ビジネスロジック変更の影響

### 変更されたメソッド

#### `WalletService.findByUserId()`

**変更前:**
\`\`\`typescript
async findByUserId(ctx, userId, tx?) {
  // 単一のウォレットを返す
  return this.repo.findByUserId(ctx, userId, tx);
}
\`\`\`

**変更後:**
\`\`\`typescript
async findByUserId(ctx, userId, tx?) {
  // 有効期限チェックを追加
  const wallet = await this.repo.findByUserId(ctx, userId, tx);
  if (wallet.expiresAt && wallet.expiresAt < new Date()) {
    throw new Error("WALLET_EXPIRED");
  }
  return wallet;
}
\`\`\`

---

### 影響を受ける機能（8機能）

#### 1. ポイント送受信機能
**ファイル:** `src/application/domain/transaction/point-transfer/service.ts`
**使用箇所:** `transferPoints()` メソッド内で `findByUserId()` を呼び出し

**影響:**
- 送信元ウォレットが有効期限切れの場合、`WALLET_EXPIRED` エラー
- 送信先ウォレットが有効期限切れの場合も同様

**対応必要:**
- エラーハンドリングの追加
- ユーザーへのエラーメッセージ表示

**影響度:** 🔴 High（コアビジネスロジック）

---

#### 2. 特典交換機能
**ファイル:** `src/application/domain/reward/utility/usecase.ts`
**使用箇所:** `exchangeUtility()` メソッド内

**影響:**
- 有効期限切れウォレットでの交換不可
- エラーハンドリング必要

**影響度:** 🟡 Medium

---

[...以下略...]
```

---

### ステップ7: テスト影響範囲の特定

変更によって影響を受けるテストファイルを特定:

```bash
# ユニットテストの検索
find __tests__/unit -name "*.test.ts" | xargs grep -l "WalletService"

# 統合テストの検索
find __tests__/integration -name "*.test.ts" | xargs grep -l "wallet"

# E2Eテストの検索
find __tests__/e2e -name "*.test.ts" | xargs grep -l "pointTransfer\|walletBalance"
```

**テスト影響範囲:**

```markdown
## テスト影響範囲

### 修正が必要なテスト（18ファイル）

#### ユニットテスト（8ファイル）

1. **__tests__/unit/wallet/service.test.ts**
   - 修正内容: `expiresAt` をモックデータに追加
   - 新規テストケース: 有効期限切れのエラーハンドリング
   - 見積もり: 1時間

2. **__tests__/unit/wallet/usecase.test.ts**
   - 修正内容: 有効期限チェックのモック
   - 新規テストケース: `WALLET_EXPIRED` エラーのハンドリング
   - 見積もり: 1時間

3. **__tests__/unit/point-transfer/service.test.ts**
   - 修正内容: ウォレット有効期限のテストケース追加
   - 新規テストケース: 送信元/送信先の有効期限エラー
   - 見積もり: 2時間

[...以下略...]

---

#### 統合テスト（6ファイル）

1. **__tests__/integration/wallet/graphql.test.ts**
   - 修正内容: GraphQLレスポンスに `expiresAt` を追加
   - 新規テストケース: 有効期限付きウォレットのCRUD
   - 見積もり: 2時間

[...以下略...]

---

#### E2Eテスト（4ファイル）

1. **__tests__/e2e/user-journey.test.ts**
   - 修正内容: ユーザージャーニーに有効期限チェックを追加
   - 新規テストケース: 有効期限切れポイントでの操作エラー
   - 見積もり: 3時間

[...以下略...]

---

### テスト工数見積もり

| テスト種別 | ファイル数 | 既存テスト修正 | 新規テスト追加 | 合計工数 |
|-----------|-----------|---------------|---------------|---------|
| ユニット | 8 | 8時間 | 12時間 | 20時間 |
| 統合 | 6 | 12時間 | 8時間 | 20時間 |
| E2E | 4 | 12時間 | 4時間 | 16時間 |
| **合計** | **18** | **32時間** | **24時間** | **56時間** |
```

---

### ステップ8: パフォーマンス影響の評価

変更によるパフォーマンスへの影響を評価:

```markdown
## パフォーマンス影響評価

### クエリパフォーマンス

#### 変更前
\`\`\`sql
SELECT id, userId, balance, createdAt
FROM t_wallets
WHERE userId = 'user-id';
-- 実行時間: 5ms
\`\`\`

#### 変更後
\`\`\`sql
SELECT id, userId, balance, expiresAt, createdAt
FROM t_wallets
WHERE userId = 'user-id';
-- 実行時間: 5ms（変化なし）
\`\`\`

**結論:** 🟢 パフォーマンス影響なし（カラム追加のみ）

---

### ビジネスロジックのパフォーマンス

#### 変更前
\`\`\`typescript
async findByUserId(ctx, userId, tx?) {
  return this.repo.findByUserId(ctx, userId, tx);
}
// 実行時間: 平均 10ms
\`\`\`

#### 変更後
\`\`\`typescript
async findByUserId(ctx, userId, tx?) {
  const wallet = await this.repo.findByUserId(ctx, userId, tx);
  if (wallet.expiresAt && wallet.expiresAt < new Date()) {
    throw new Error("WALLET_EXPIRED");
  }
  return wallet;
}
// 実行時間: 平均 10ms（変化なし）
\`\`\`

**結論:** 🟢 パフォーマンス影響なし（メモリ内の日付比較のみ）

---

### N+1問題のチェック

\`\`\`typescript
// UserResolver.wallets でDataLoaderを使用しているか確認
User: {
  wallet: (parent, _, ctx) => ctx.loaders.wallet.load(parent.id)
}
\`\`\`

**結論:** ✅ DataLoaderを使用、N+1問題なし
```

---

### ステップ9: セキュリティ影響の評価

変更によるセキュリティリスクを評価:

```markdown
## セキュリティ影響評価

### 認証・認可の変更

#### RLS（Row-Level Security）への影響

**変更前:**
\`\`\`typescript
async findByUserId(ctx, userId, tx?) {
  return ctx.issuer.public(ctx, (tx) =>
    tx.t_wallets.findUnique({ where: { userId } })
  );
}
\`\`\`

**変更後:**
\`\`\`typescript
// RLSロジックに変更なし
async findByUserId(ctx, userId, tx?) {
  const wallet = await ctx.issuer.public(ctx, (tx) =>
    tx.t_wallets.findUnique({ where: { userId } })
  );
  // 有効期限チェック追加
  if (wallet.expiresAt && wallet.expiresAt < new Date()) {
    throw new Error("WALLET_EXPIRED");
  }
  return wallet;
}
\`\`\`

**結論:** ✅ RLSへの影響なし

---

### 新しいセキュリティリスク

#### リスク1: 有効期限の改ざん
**シナリオ:** 悪意のあるユーザーが有効期限を延長しようとする

**対策:**
- 有効期限の更新は管理者権限のみ
- 監査ログの記録
- 異常な有効期限変更の検出

**実装状況:** ✅ 既に対策済み（管理者権限チェック）

---

#### リスク2: DoS攻撃（大量の有効期限チェック）
**シナリオ:** 大量のウォレットアクセスで有効期限チェックが負荷に

**対策:**
- レート制限
- キャッシング（有効期限のメモリキャッシュ）

**実装状況:** ⚠️  要検討（現時点で未実装）

---

### センシティブデータの取り扱い

- [ ] 有効期限はセンシティブデータか？ → ❌ いいえ
- [ ] ログに出力して良いか？ → ✅ はい
- [ ] クライアントに返して良いか？ → ✅ はい

**結論:** セキュリティ上の新しいリスクは低い
```

---

### ステップ10: 影響範囲レポートの生成

全ての分析結果を統合し、優先度付きのレポートを生成:

```markdown
# 影響範囲分析レポート

**変更対象:** WalletService.ts（有効期限チェック追加）
**分析日:** YYYY-MM-DD
**総合リスク評価:** 🟡 Medium

---

## エグゼクティブサマリー

### 影響範囲の概要
- **影響ファイル数:** 38ファイル
  - 直接依存: 6ファイル
  - 間接依存: 20ファイル
  - テストファイル: 18ファイル
- **影響ドメイン数:** 5ドメイン
  - account, transaction, reward, experience, notification
- **影響機能数:** 8機能
  - ポイント送受信、特典交換、Opportunity参加、など

### リスク評価
- **🔴 High Risk:** 3機能（ポイント送受信、ウォレット表示、特典交換）
- **🟡 Medium Risk:** 5機能
- **🟢 Low Risk:** テスト修正

### 推奨アクション
1. **優先テスト:** ポイント送受信、特典交換のE2Eテスト
2. **段階的リリース:** カナリアリリースで影響を監視
3. **監視強化:** `WALLET_EXPIRED` エラーの頻度監視

---

## 影響ファイル一覧

### 🔴 High Impact（6ファイル）

| ファイル | 影響度 | 影響内容 | 対応必要 |
|---------|--------|---------|---------|
| WalletUseCase.ts | 🔴 High | エラーハンドリング追加 | 必須 |
| PointTransferService.ts | 🔴 High | 有効期限チェック対応 | 必須 |
| WalletResolver.ts | 🔴 High | GraphQLエラー処理 | 必須 |
| UtilityUseCase.ts | 🔴 High | 交換処理のエラー対応 | 必須 |
| OpportunityUseCase.ts | 🔴 High | 参加処理のエラー対応 | 必須 |
| WalletRepository.ts | 🔴 High | SELECT句更新 | 必須 |

---

### 🟡 Medium Impact（20ファイル）

[詳細リスト...]

---

### 🟢 Low Impact（12ファイル）

[テストファイルなど...]

---

## ドメイン間の依存関係

\`\`\`mermaid
graph TD
    A[Wallet Domain] -->|直接依存| B[Transaction Domain]
    A -->|直接依存| C[Reward Domain]
    A -->|直接依存| D[Experience Domain]
    B -->|間接依存| E[Notification Domain]
    C -->|間接依存| E
    D -->|間接依存| E
\`\`\`

---

## テスト戦略

### Phase 1: ユニットテスト（優先度: High）
- [ ] WalletService の有効期限チェックロジック
- [ ] エラーハンドリング（`WALLET_EXPIRED`）
- [ ] 境界値テスト（有効期限当日、翌日）

**工数:** 20時間

---

### Phase 2: 統合テスト（優先度: High）
- [ ] ポイント送受信フロー（有効期限切れ）
- [ ] 特典交換フロー（有効期限切れ）
- [ ] GraphQL APIのエラーレスポンス

**工数:** 20時間

---

### Phase 3: E2Eテスト（優先度: Medium）
- [ ] ユーザージャーニー（有効期限切れシナリオ）
- [ ] エラーメッセージの表示確認

**工数:** 16時間

---

### テストカバレッジ目標
- ユニット: 95%以上（有効期限ロジック）
- 統合: 85%以上
- E2E: 主要フローをカバー

---

## リリース計画

### リスク緩和策

1. **フィーチャーフラグ**
   \`\`\`typescript
   if (FEATURE_FLAGS.WALLET_EXPIRATION_CHECK) {
     // 有効期限チェック
   }
   \`\`\`

2. **カナリアリリース**
   - 10% → 50% → 100%

3. **ロールバック計画**
   - フラグOFF で即座にロールバック可能

---

### 監視項目

- `WALLET_EXPIRED` エラー発生率
- ポイント送受信の成功率
- GraphQLエラー率

**アラート:**
- エラー率 > 5% で警告

---

## 次のステップ

### 即座に実施すべきアクション

1. **影響ファイルのレビュー:** High Impactの6ファイルを優先
2. **テスト計画の策定:** 56時間の工数を確保
3. **ステークホルダーへの共有:** 影響範囲を関係者に通知

### 実装前チェックリスト

- [ ] 全ての依存ファイルを確認
- [ ] テスト戦略を承認
- [ ] フィーチャーフラグ実装
- [ ] ロールバック計画を確認
- [ ] 監視・アラート設定

---

## 承認

**レビュー担当者:**
- [ ] テックリード
- [ ] QAリード
- [ ] アーキテクト

**承認日:** YYYY-MM-DD
```

---

## 活用例

### 例1: Service層の変更

```bash
/map-impact-analysis src/application/domain/account/wallet/service.ts
```

**実行されるコマンド例:**
```bash
# 依存関係グラフを生成
npx madge --json src/application/domain/account/wallet > wallet-deps.json

# 循環依存をチェック
npx madge --circular src/application/domain/account/wallet

# 依存関係を可視化
npx madge --image wallet-impact.svg src/application/domain/account/wallet
```

**生成されるレポート:**
- 直接依存: 6ファイル（madgeで正確に特定）
- 間接依存: 20ファイル（再帰的に追跡）
- 影響ドメイン: 5つ
- テスト影響: 18ファイル
- 依存関係グラフ画像: `wallet-impact.svg`

---

### 例2: Prismaスキーマの変更

```bash
/map-impact-analysis prisma/schema.prisma
```

**生成されるレポート:**
- モデル変更の影響: 25ファイル
- マイグレーション計画
- 型定義の更新必要箇所

---

### 例3: PR全体の影響分析

```bash
/map-impact-analysis --pr <PR番号>
```

**生成されるレポート:**
- PR内の全変更ファイルの影響を統合分析
- ドメイン横断的な影響を可視化
- 総合的なリスク評価

---

## 注意事項

### 影響範囲分析の限界

このスキルは以下を検出**できません**:
- ❌ 動的な依存関係（実行時にのみ決まる）
- ❌ 外部サービスへの影響（LINE API、Firebase など）
- ❌ クライアント側の実装詳細（iOS/Android/Webの具体的な影響）
- ❌ ビジネス要件上の暗黙的な依存

### madge使用時の注意

- **初回実行**: `npx madge` が初回はパッケージをダウンロードするため、時間がかかる場合があります
- **パフォーマンス**: 大規模なディレクトリ（`src/` 全体など）では処理に時間がかかるため、ドメイン単位での実行を推奨
- **循環依存**: 検出された循環依存は必ず修正が必要（アーキテクチャ違反）

### 推奨される併用スキル

影響範囲分析後、以下のスキルと組み合わせて使用:
- `/test-domain` - 影響を受けるドメインのテスト実行
- `/api-compatibility-check` - GraphQL APIの互換性チェック
- `/phased-delivery-plan` - 段階的リリース計画

---

## 参考資料

以下については `@CLAUDE.md` を参照してください:
- アーキテクチャパターン
- ドメイン間の依存関係ルール
- テスト戦略
- リリースプロセス
