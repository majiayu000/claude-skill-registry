---
name: legacy-audit
description: 技術的負債を評価
user-invocable: true
argument-hint: [ドメイン名またはファイルパス]
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

# civicship-api レガシーコード監査

既存コードの**品質を評価**し、**技術的負債**を特定します。リファクタリングの優先度を判定し、改善ロードマップを提示します。

## 使用方法

```bash
# ドメイン全体を監査
/legacy-audit wallet

# 特定ファイルを監査
/legacy-audit src/application/domain/account/wallet/service.ts

# プロジェクト全体を監査（時間がかかります）
/legacy-audit --all
```

**引数:**
- `$ARGUMENTS`: ドメイン名、ファイルパス、または `--all`

---

## レガシーコード監査プロセス

### ステップ1: コードの基本情報収集

監査対象のコードベース統計:

```bash
# 対象ドメインのファイル数
find src/application/domain/"${DOMAIN}" -name "*.ts" | wc -l

# 総行数
find src/application/domain/"${DOMAIN}" -name "*.ts" | xargs wc -l | tail -1

# 最終更新日
find src/application/domain/"${DOMAIN}" -name "*.ts" -exec stat -c "%y %n" {} \; | sort

# Gitコミット履歴
git log --oneline --since="1 year ago" -- src/application/domain/"${DOMAIN}" | wc -l
```

**基本情報レポート:**

```markdown
## コードベース統計

### ファイル構成

| レイヤー | ファイル数 | 総行数 | 平均行数/ファイル |
|---------|-----------|--------|------------------|
| Service | 1 | 450行 | 450行 |
| UseCase | 1 | 320行 | 320行 |
| Repository | 1 | 280行 | 280行 |
| Resolver | 1 | 180行 | 180行 |
| Presenter | 1 | 120行 | 120行 |
| Converter | 1 | 90行 | 90行 |
| **合計** | **6** | **1,440行** | **240行** |

---

### 変更履歴

- **最終更新:** 2025-12-15
- **作成日:** 2023-06-20
- **コミット数（1年間）:** 45回
- **主要コントリビューター:** 3名

---

### ファイルサイズ分布

| ファイル | 行数 | 評価 |
|---------|------|------|
| service.ts | 450行 | 🟡 やや大きい |
| usecase.ts | 320行 | 🟢 適切 |
| repository.ts | 280行 | 🟢 適切 |
| resolver.ts | 180行 | 🟢 適切 |
| presenter.ts | 120行 | 🟢 適切 |
| converter.ts | 90行 | 🟢 適切 |

**基準:**
- 🟢 < 300行: 適切
- 🟡 300-500行: やや大きい、分割検討
- 🔴 > 500行: 大きすぎる、分割必須
```

---

### ステップ2: アーキテクチャ遵守度の評価

DDD/Clean Architectureの原則への準拠:

```bash
# レイヤー違反の検出
grep -r "import.*repository" src/application/domain/"${DOMAIN}"/usecase.ts
grep -r "import.*GqlWallet" src/application/domain/"${DOMAIN}"/service.ts

# 循環依存の検出
npx madge --circular src/application/domain/"${DOMAIN}"
```

**アーキテクチャ評価:**

```markdown
## アーキテクチャ遵守度

### レイヤー責任の遵守

#### ✅ 正しい実装パターン

**UseCase:**
\`\`\`typescript
// ✅ Good: Serviceを呼び出し、トランザクション管理
async managerCreateWallet({ input, permission }, ctx) {
  return ctx.issuer.onlyBelongingCommunity(ctx, async (tx) => {
    const wallet = await this.service.createWallet(ctx, input, permission.communityId, tx);
    return WalletPresenter.create(wallet);
  });
}
\`\`\`

**Service:**
\`\`\`typescript
// ✅ Good: ビジネスロジック、Repositoryを呼び出し
async createWallet(ctx, input, communityId, tx) {
  // バリデーション
  if (input.initialBalance < 0) {
    throw new Error("INVALID_BALANCE");
  }

  // Repository呼び出し
  const data = this.converter.toCreateData(input, communityId);
  return await this.repo.create(ctx, data, tx);
}
\`\`\`

---

#### ❌ 検出された違反

**違反1: ServiceからRepositoryを直接呼ばずにUseCaseを呼ぶ**
\`\`\`typescript
// ❌ Bad: ServiceからUseCaseを呼んでいる（循環依存リスク）
async someMethod(ctx) {
  const wallet = await this.walletUseCase.getWallet(id, ctx);  // NG
}
\`\`\`

**推奨修正:**
\`\`\`typescript
// ✅ Good: 他ドメインのServiceを呼ぶ
async someMethod(ctx) {
  const wallet = await this.walletService.findById(ctx, id);  // OK
}
\`\`\`

**影響度:** 🟡 Medium
**修正優先度:** P1（中優先度）

---

**違反2: ServiceがGraphQL型を返している**
\`\`\`typescript
// ❌ Bad: ServiceがGqlWalletを返している
async getWallet(ctx, id): Promise<GqlWallet> {
  const wallet = await this.repo.findById(ctx, id);
  return WalletPresenter.toGraphQL(wallet);  // Presenterの呼び出しはUseCaseの責務
}
\`\`\`

**推奨修正:**
\`\`\`typescript
// ✅ Good: ServiceはPrisma型を返す
async getWallet(ctx, id): Promise<PrismaWallet> {
  return await this.repo.findById(ctx, id);
}

// UseCaseでPresenterを呼ぶ
async getWallet(id, ctx) {
  const wallet = await this.service.getWallet(ctx, id);
  return WalletPresenter.toGraphQL(wallet);  // ここで変換
}
\`\`\`

**影響度:** 🟡 Medium
**修正優先度:** P2（低優先度、動作には影響なし）

---

### 依存関係の健全性

#### 循環依存のチェック

\`\`\`bash
npx madge --circular src/application/domain/account/wallet
\`\`\`

**結果:**
- ✅ 循環依存なし

---

#### 依存の方向性

\`\`\`
Resolver → UseCase → Service → Repository
                         ↓
                    Converter
                         ↓
                    Presenter
\`\`\`

**評価:** ✅ 依存の方向性は正しい
```

---

### ステップ3: コード品質指標の測定

複雑度、重複、テストカバレッジを評価:

```bash
# 循環的複雑度（Cyclomatic Complexity）
npx ts-complexity src/application/domain/"${DOMAIN}"/**/*.ts

# コード重複の検出
npx jscpd src/application/domain/"${DOMAIN}"

# テストカバレッジ
pnpm test:coverage src/application/domain/"${DOMAIN}"
```

**コード品質レポート:**

```markdown
## コード品質指標

### 循環的複雑度（Cyclomatic Complexity）

| ファイル | メソッド | 複雑度 | 評価 |
|---------|---------|--------|------|
| service.ts | createWallet | 5 | 🟢 低い |
| service.ts | updateWallet | 8 | 🟡 中程度 |
| service.ts | transferPoints | 15 | 🔴 高い |
| service.ts | calculateBalance | 12 | 🟡 中程度 |

**基準:**
- 🟢 1-10: 低い（理解しやすい）
- 🟡 11-20: 中程度（分割検討）
- 🔴 21+: 高い（分割必須）

**問題のあるメソッド:** 1件
- `transferPoints()` (複雑度: 15) → 分割を推奨

---

### コード重複

- **重複率:** 3.5%
- **重複ブロック数:** 2箇所

**重複箇所1:**
\`\`\`typescript
// wallet/service.ts:120-135 と reward/service.ts:45-60 で重複
const balance = await this.repo.findByUserId(ctx, userId, tx);
if (!balance) {
  throw new Error("WALLET_NOT_FOUND");
}
if (balance.amount < requiredAmount) {
  throw new Error("INSUFFICIENT_BALANCE");
}
\`\`\`

**推奨修正:**
- 共通ロジックを `WalletService` の `validateBalance()` メソッドに抽出
- 他ドメインから呼び出し

**影響度:** 🟢 Low
**修正優先度:** P3（低優先度、現状問題なし）

---

### テストカバレッジ

| レイヤー | カバレッジ | 評価 |
|---------|-----------|------|
| Service | 92% | 🟢 良好 |
| UseCase | 85% | 🟢 良好 |
| Repository | 78% | 🟡 改善余地あり |
| Converter | 95% | 🟢 優秀 |
| Presenter | 98% | 🟢 優秀 |
| **平均** | **89.6%** | **🟢 良好** |

**未カバーの箇所:**
- Repository: エラーハンドリング（7箇所）
- UseCase: 例外的なケース（3箇所）

**推奨アクション:**
- Repository のエラーケースをテスト追加
- 目標: 全レイヤー 90%以上
```

---

### ステップ4: 技術的負債の特定

リファクタリングが必要な箇所を特定:

```markdown
## 技術的負債

### 負債の分類

#### 🔴 Critical（高優先度）

**負債1: 巨大なメソッド**

**ファイル:** `service.ts:245-380`
**メソッド:** `transferPoints()`
**問題:** 135行の巨大メソッド、複雑度15

**内容:**
- ポイント送受信ロジック
- バリデーション
- ポイント減算
- ポイント加算
- トランザクション記録
- LINE通知

**推奨修正:**
\`\`\`typescript
// 分割後
async transferPoints(ctx, input, tx) {
  await this.validateTransfer(ctx, input, tx);
  await this.deductPoints(ctx, input.fromUserId, input.amount, tx);
  await this.addPoints(ctx, input.toUserId, input.amount, tx);
  await this.recordTransaction(ctx, input, tx);
  // LINE通知は非同期で別処理
}
\`\`\`

**修正工数:** 4時間
**影響範囲:** Service層のみ（外部インターフェース変更なし）
**リスク:** 🟡 Medium（十分なテストでカバー）

---

#### 🟡 Warning（中優先度）

**負債2: マジックナンバー**

**ファイル:** `service.ts:120, 145, 230`
**問題:** ハードコードされた数値

\`\`\`typescript
// ❌ Bad
if (balance < 100) {  // 100は何？
  throw new Error("INSUFFICIENT_BALANCE");
}

if (transferAmount > 10000) {  // 10000は何？
  // 高額送金の承認プロセス
}
\`\`\`

**推奨修正:**
\`\`\`typescript
// ✅ Good
const MINIMUM_BALANCE = 100;  // 最低残高
const HIGH_AMOUNT_THRESHOLD = 10000;  // 高額送金の閾値

if (balance < MINIMUM_BALANCE) {
  throw new Error("INSUFFICIENT_BALANCE");
}

if (transferAmount > HIGH_AMOUNT_THRESHOLD) {
  // 高額送金の承認プロセス
}
\`\`\`

**修正工数:** 1時間
**影響範囲:** Service層のみ
**リスク:** 🟢 Low

---

**負債3: 例外処理の不統一**

**ファイル:** 複数ファイル
**問題:** エラーメッセージが統一されていない

\`\`\`typescript
// 不統一な例外処理
throw new Error("WALLET_NOT_FOUND");  // service.ts
throw new Error("Wallet not found");  // usecase.ts
throw new Error("ウォレットが見つかりません");  // resolver.ts
\`\`\`

**推奨修正:**
\`\`\`typescript
// エラーコード定数を定義
export const ErrorCodes = {
  WALLET_NOT_FOUND: "WALLET_NOT_FOUND",
  INSUFFICIENT_BALANCE: "INSUFFICIENT_BALANCE",
  // ...
} as const;

// 使用
throw new Error(ErrorCodes.WALLET_NOT_FOUND);
\`\`\`

**修正工数:** 2時間
**影響範囲:** 全レイヤー
**リスク:** 🟡 Medium（エラーハンドリングのテスト必要）

---

#### 🟢 Info（低優先度）

**負債4: コメント不足**

**ファイル:** 複数ファイル
**問題:** 複雑なロジックにコメントがない

**推奨修正:**
- ビジネスルールにコメント追加
- JSDocでメソッドの説明を追加

**修正工数:** 3時間
**影響範囲:** ドキュメントのみ
**リスク:** 🟢 None
```

---

### ステップ5: パフォーマンス問題の検出

パフォーマンス上の問題を特定:

```bash
# N+1問題の検出
grep -A 10 "for.*of\|for.*in\|forEach" src/application/domain/"${DOMAIN}"/**/*.ts | grep -B 5 "await.*find\|await.*query"

# 不要なクエリの検出
grep -A 5 "findMany" src/application/domain/"${DOMAIN}"/data/repository.ts
```

**パフォーマンス評価:**

```markdown
## パフォーマンス問題

### 検出された問題

#### 問題1: N+1クエリの可能性

**ファイル:** `usecase.ts:85-95`
**コード:**
\`\`\`typescript
// ❌ Potential N+1
const wallets = await this.service.listWallets(ctx, communityId);
for (const wallet of wallets) {
  const user = await this.userService.findById(ctx, wallet.userId);  // N+1!
  // ...
}
\`\`\`

**推奨修正:**
\`\`\`typescript
// ✅ Good: DataLoaderを使用
const wallets = await this.service.listWallets(ctx, communityId);
const users = await ctx.loaders.user.loadMany(wallets.map(w => w.userId));
\`\`\`

**影響度:** 🔴 High（ウォレット数に比例して遅延）
**修正優先度:** P0（最高優先度）
**修正工数:** 2時間

---

#### 問題2: 不要な全件取得

**ファイル:** `repository.ts:120`
**コード:**
\`\`\`typescript
// ❌ Bad: ページネーションなし
async findAll(ctx) {
  return ctx.issuer.public(ctx, (tx) =>
    tx.t_wallets.findMany()  // 全件取得（数千件の可能性）
  );
}
\`\`\`

**推奨修正:**
\`\`\`typescript
// ✅ Good: カーソルベースページネーション
async findAll(ctx, cursor?: string, limit = 20) {
  return ctx.issuer.public(ctx, (tx) =>
    tx.t_wallets.findMany({
      take: limit,
      skip: cursor ? 1 : 0,
      cursor: cursor ? { id: cursor } : undefined,
      orderBy: { createdAt: 'desc' }
    })
  );
}
\`\`\`

**影響度:** 🟡 Medium
**修正優先度:** P1
**修正工数:** 3時間

---

### パフォーマンスメトリクス

| メソッド | 実行時間 | 評価 |
|---------|---------|------|
| findById | 5ms | 🟢 優秀 |
| listWallets | 120ms | 🟡 改善余地あり |
| transferPoints | 80ms | 🟢 良好 |
| calculateBalance | 45ms | 🟢 良好 |

**目標:** 全メソッド < 100ms
```

---

### ステップ6: セキュリティ問題の検出

セキュリティ上の問題を特定:

```bash
# センシティブデータのログ出力
grep -r "console.log\|logger.info" src/application/domain/"${DOMAIN}" | grep -i "password\|token\|secret\|key"

# RLSの実装確認
grep -r "prisma\.t_wallets" src/application/domain/"${DOMAIN}" | grep -v "ctx.issuer"
```

**セキュリティ評価:**

```markdown
## セキュリティ問題

### 検出された問題

#### 問題1: RLSの未適用

**ファイル:** `repository.ts:155`
**コード:**
\`\`\`typescript
// ❌ Bad: ctx.issuer を使用していない
async findByUserId(ctx, userId) {
  return await ctx.prisma.t_wallets.findUnique({ where: { userId } });
}
\`\`\`

**推奨修正:**
\`\`\`typescript
// ✅ Good: RLSを適用
async findByUserId(ctx, userId, tx?) {
  if (tx) {
    return tx.t_wallets.findUnique({ where: { userId } });
  }
  return ctx.issuer.public(ctx, (tx) =>
    tx.t_wallets.findUnique({ where: { userId } })
  );
}
\`\`\`

**影響度:** 🔴 Critical（セキュリティリスク）
**修正優先度:** P0（最高優先度）
**修正工数:** 1時間

---

#### 問題2: センシティブデータのログ出力

**ファイル:** `service.ts:200`
**コード:**
\`\`\`typescript
// ❌ Bad: ユーザー情報全体をログ出力
console.log("Transfer:", { fromUser, toUser, amount });
\`\`\`

**推奨修正:**
\`\`\`typescript
// ✅ Good: IDのみログ出力
logger.info("Transfer:", { fromUserId: fromUser.id, toUserId: toUser.id, amount });
\`\`\`

**影響度:** 🟡 Medium
**修正優先度:** P1
**修正工数:** 0.5時間

---

### セキュリティチェックリスト

- [ ] RLS（Row-Level Security）の適用
- [ ] 認証・認可の確認
- [ ] 入力バリデーション
- [ ] SQLインジェクション対策（Prismaで自動対応）
- [ ] センシティブデータの保護
- [ ] ログ出力の安全性

**評価:** 🟡 概ね良好、2件の改善必要
```

---

### ステップ7: 保守性の評価

コードの保守しやすさを評価:

```markdown
## 保守性評価

### ドキュメント

#### コメント率

| ファイル | コメント行 / 総行数 | 評価 |
|---------|-------------------|------|
| service.ts | 45 / 450 (10%) | 🟡 不足 |
| usecase.ts | 30 / 320 (9%) | 🟡 不足 |
| repository.ts | 20 / 280 (7%) | 🔴 不足 |
| converter.ts | 15 / 90 (17%) | 🟢 良好 |
| presenter.ts | 10 / 120 (8%) | 🟡 不足 |

**推奨:** 15%以上

---

#### JSDocの有無

- [ ] Public メソッドにJSDoc: 40%
- [ ] Private メソッドにJSDoc: 10%
- [ ] 複雑なロジックにコメント: 30%

**推奨:** Public 80%以上、複雑なロジック 100%

---

### 命名規則

#### 変数名の明確性

\`\`\`typescript
// ❌ Bad: 不明確な変数名
const w = await this.repo.find(ctx, id);
const amt = input.amount;
const flg = true;

// ✅ Good: 明確な変数名
const wallet = await this.repo.find(ctx, id);
const transferAmount = input.amount;
const isActive = true;
\`\`\`

**検出:** 5箇所で不明確な変数名
**修正優先度:** P2（低優先度、可読性の問題）

---

### 型安全性

#### `any` 型の使用

\`\`\`bash
grep -r ": any" src/application/domain/"${DOMAIN}"
\`\`\`

**検出:** 2箇所で `any` 型を使用
- `service.ts:340` - 外部APIのレスポンス
- `converter.ts:65` - 動的なフィールド変換

**推奨:** 型定義を追加してTypeScript の恩恵を最大化

---

### 依存関係の管理

#### 外部ライブラリへの依存

- Prisma: ✅ 適切
- tsyringe: ✅ 適切
- 独自ユーティリティ: 🟡 一部抽出可能

**評価:** 依存関係は健全
```

---

### ステップ8: テスタビリティの評価

テストのしやすさを評価:

```markdown
## テスタビリティ

### テストカバレッジの詳細

#### 未カバー箇所

**Service層:**
- [ ] エッジケース: 残高0のときの送金
- [ ] エラーハンドリング: Repository失敗時
- [ ] 境界値: 最大送金額

**UseCase層:**
- [ ] トランザクションロールバック
- [ ] 他ドメインServiceの失敗時

**Repository層:**
- [ ] データベース接続エラー
- [ ] タイムアウト

---

### モックのしやすさ

\`\`\`typescript
// ✅ Good: DIを使用、モックしやすい
constructor(
  @inject("WalletRepository") private repo: IWalletRepository,
  @inject("WalletConverter") private converter: WalletConverter
) {}

// テストでモック
const mockRepo = {
  findById: jest.fn(),
  create: jest.fn()
};
container.register("WalletRepository", { useValue: mockRepo });
\`\`\`

**評価:** ✅ モックしやすい（DI使用）

---

### テストの品質

#### 既存テストの評価

- **AAA（Arrange-Act-Assert）パターン:** 🟢 遵守
- **テストの独立性:** 🟢 良好
- **テストデータのクリーンアップ:** 🟢 実施
- **テスト名の明確性:** 🟡 一部改善余地

**推奨改善:**
- テスト名を日本語にして可読性向上
- Given-When-Then形式のコメント追加
```

---

### ステップ9: リファクタリング優先度の決定

技術的負債の優先順位付け:

```markdown
## リファクタリング優先度

### 優先度マトリクス

\`\`\`
高Impact │ P0: RLS未適用     │ P1: N+1問題      │
        │ P0: 巨大メソッド   │ P1: 全件取得     │
        │                   │ P1: 例外処理統一  │
        ├───────────────────┼─────────────────┤
低Impact │ P2: マジックナンバー│ P3: コメント不足  │
        │ P2: 変数名        │ P3: JSDoc不足    │
        └───────────────────┴─────────────────┘
          低Effort            高Effort
\`\`\`

---

### P0: 即座に修正（Critical）

| # | 負債 | 影響度 | 工数 | 期限 |
|---|------|--------|------|------|
| 1 | RLS未適用 | 🔴 Critical | 1h | 即時 |
| 2 | 巨大メソッド分割 | 🔴 High | 4h | 1週間以内 |

**総工数:** 5時間
**リスク:** RLSは最優先、セキュリティリスク

---

### P1: 近日中に修正（High）

| # | 負債 | 影響度 | 工数 | 期限 |
|---|------|--------|------|------|
| 3 | N+1問題 | 🔴 High | 2h | 2週間以内 |
| 4 | 全件取得 | 🟡 Medium | 3h | 2週間以内 |
| 5 | 例外処理統一 | 🟡 Medium | 2h | 1ヶ月以内 |
| 6 | センシティブログ | 🟡 Medium | 0.5h | 2週間以内 |

**総工数:** 7.5時間

---

### P2: 計画的に修正（Medium）

| # | 負債 | 影響度 | 工数 | 期限 |
|---|------|--------|------|------|
| 7 | マジックナンバー | 🟢 Low | 1h | 1ヶ月以内 |
| 8 | 変数名の改善 | 🟢 Low | 1h | 3ヶ月以内 |

**総工数:** 2時間

---

### P3: 時間があれば修正（Low）

| # | 負債 | 影響度 | 工数 | 期限 |
|---|------|--------|------|------|
| 9 | コメント追加 | 🟢 Low | 3h | 6ヶ月以内 |
| 10 | JSDoc追加 | 🟢 Low | 2h | 6ヶ月以内 |

**総工数:** 5時間

---

### 総工数見積もり

- **P0（Critical）:** 5時間
- **P1（High）:** 7.5時間
- **P2（Medium）:** 2時間
- **P3（Low）:** 5時間
- **合計:** 19.5時間（約2.5日）
```

---

### ステップ10: 改善ロードマップの生成

リファクタリング計画:

```markdown
# リファクタリングロードマップ

**ドメイン:** Wallet
**監査日:** YYYY-MM-DD
**総合評価:** 🟡 B（良好だが改善余地あり）

---

## Week 1: Critical対応

### Day 1-2
- [ ] RLS未適用箇所の修正（1時間）
- [ ] テスト追加（1時間）
- [ ] コードレビュー

### Day 3-5
- [ ] 巨大メソッドの分割（4時間）
- [ ] ユニットテスト追加（2時間）
- [ ] リファクタリングレビュー

---

## Week 2-3: High対応

### Day 6-10
- [ ] N+1問題の修正（2時間）
- [ ] 全件取得の修正（3時間）
- [ ] センシティブログの修正（0.5時間）
- [ ] テスト追加（2時間）

### Day 11-15
- [ ] 例外処理の統一（2時間）
- [ ] エラーコード定数の定義（0.5時間）
- [ ] 全ドメインへの適用（1時間）

---

## Month 2: Medium/Low対応

### Week 4-6
- [ ] マジックナンバーの定数化
- [ ] 変数名の改善
- [ ] コメント・JSDocの追加

---

## 成功指標

### リファクタリング完了条件

- [ ] P0負債: 0件
- [ ] P1負債: < 2件
- [ ] テストカバレッジ: > 90%
- [ ] 循環的複雑度: 全メソッド < 10
- [ ] セキュリティ問題: 0件

---

## 承認

- [ ] テックリード
- [ ] アーキテクト
- [ ] QAリード
```

---

## 活用例

### 例1: ドメイン全体の監査

```bash
/legacy-audit wallet
```

**出力:**
- 技術的負債: 10件
- リファクタリング工数: 19.5時間
- 優先度付きロードマップ

---

### 例2: 特定ファイルの監査

```bash
/legacy-audit src/application/domain/account/wallet/service.ts
```

**出力:**
- ファイル単位の詳細分析
- メソッド別の複雑度
- 改善提案

---

## 注意事項

### 監査の限界

- ❌ 実行時のバグ（静的解析の限界）
- ❌ ビジネスロジックの正しさ
- ❌ UX/UIの問題

### 推奨される併用スキル

- `/validate-architecture` - アーキテクチャ準拠の検証
- `/test-domain` - テストカバレッジの確認
- `/security-review` - セキュリティ深掘り

---

## 参考資料

以下については `@CLAUDE.md` を参照してください:
- アーキテクチャパターン
- コード品質基準
- リファクタリング戦略
