---
name: validate-architecture
description: Validate DDD/Clean Architecture compliance in code changes, checking layer violations, transaction patterns, and Row-Level Security
context: fork
agent: Explore
allowed-tools: Read, Grep, Bash
user-invocable: true
argument-hint: [パスまたはドメイン名]
---

# civicship-api アーキテクチャ検証

**DDD (ドメイン駆動設計)** と **Clean Architecture** の原則に基づいてコード変更を検証します。

`$ARGUMENTS` が指定された場合、その特定のパスまたはドメインを検証します。指定がない場合は、現在のブランチの未コミット変更を全て検証します。

---

## 重要なアーキテクチャルール

### 1. レイヤー違反

**Resolverレイヤー** (`controller/resolver.ts`)
- ✅ UseCaseのメソッドのみを呼び出す必要がある
- ✅ フィールドリゾルバではDataLoaderを使用する必要がある（N+1問題防止）
- ❌ ビジネスロジックを書いてはいけない
- ❌ Repositoryを直接呼び出してはいけない

**UseCaseレイヤー** (`usecase.ts`)
- ✅ Serviceを使ってビジネスフローをオーケストレーションする必要がある
- ✅ `ctx.issuer.onlyBelongingCommunity(ctx, async (tx) => {...})` でトランザクションを管理する必要がある
- ✅ 自ドメインおよび他ドメインのServiceを呼び出せる
- ✅ 結果を返す前にPresenterを呼び出す必要がある
- ❌ 他ドメインのUseCaseを呼び出してはいけない（循環依存の原因）

**Serviceレイヤー** (`service.ts`)
- ✅ ビジネスロジックとバリデーションを実装する必要がある
- ✅ Repositoryを呼び出す必要がある
- ✅ 他ドメインのServiceを呼び出せる（読み取り操作のみ）
- ✅ `tx` パラメータを受け取り、Repositoryに渡す必要がある（Service内で `if (tx)` 分岐はしない）
- ❌ GraphQL型（`GqlXxx`）を返してはいけない - Prisma型のみを返す

**Repositoryレイヤー** (`data/repository.ts`)
- ✅ Prismaクエリのみを実行する必要がある
- ✅ Row-Level Security (RLS)のため `ctx.issuer` を使用する必要がある
- ✅ `tx` パラメータをメソッドタイプに応じて処理する必要がある:
  - **Mutationメソッド**（create/update/delete）: 必須の `tx: Prisma.TransactionClient` を受け取り、直接使用（`if (tx)` 分岐なし）
  - **Queryメソッド** トランザクション内外両方で呼ばれる可能性: オプショナルの `tx?: Prisma.TransactionClient` を受け取り、`if (tx)` で分岐
- ❌ ビジネスロジックを含めてはいけない

**Converter** (`data/converter.ts`)
- ✅ 純粋関数である必要がある（GraphQL input → Prisma形式）
- ❌ トランザクションを使用してはいけない
- ❌ データベースクエリを実行してはいけない

**Presenter** (`presenter.ts`)
- ✅ 純粋関数である必要がある（Prisma → GraphQL型）
- ❌ ビジネスロジックを含めてはいけない
- ❌ データベースクエリを実行してはいけない

---

### 2. トランザクションパターンの検証

**パターンA: Mutationメソッド（create/update/delete） - 必須トランザクション**

```typescript
// UseCaseがトランザクションを管理
async managerCreateOpportunity({ input, permission }, ctx) {
  return ctx.issuer.onlyBelongingCommunity(ctx, async (tx) => {
    const record = await this.service.createOpportunity(ctx, input, permission.communityId, tx);
    return OpportunityPresenter.create(record);
  });
}

// Serviceがtxを受け取り、Repositoryに渡す
async createOpportunity(ctx, input, communityId, tx) {
  const data = this.converter.create(input, communityId);
  return await this.repository.create(ctx, data, tx);
}

// Repositoryは必須のtxパラメータを受け取る（分岐なし）
async create(ctx, data, tx: Prisma.TransactionClient) {
  return tx.opportunity.create({
    data,
    select: opportunitySelectDetail,
  });
}
```

**パターンB: Queryメソッド - オプショナルトランザクション（柔軟な使用）**

```typescript
// Repositoryはオプショナルのtxパラメータを受け取り、分岐処理
async findCommunityWallet(ctx, communityId, tx?: Prisma.TransactionClient) {
  if (tx) {
    return tx.wallet.findFirst({
      where: { communityId, type: WalletType.COMMUNITY },
      select: walletSelectDetail,
    });
  }
  return ctx.issuer.public(ctx, (tx) => {
    return tx.wallet.findFirst({
      where: { communityId, type: WalletType.COMMUNITY },
      select: walletSelectDetail,
    });
  });
}
```

**違反としてフラグするもの:**
- ❌ Serviceレイヤーでトランザクションを開始している（UseCaseのみで行う）
- ❌ ServiceからRepositoryへの `tx` パラメータ伝播が欠けている
- ❌ Mutationメソッドがオプショナルの `tx?` を使用している（必須の `tx` にすべき）
- ❌ オプショナルの `tx?` を使用しているQueryメソッドで `if (tx)` 分岐がない

---

### 3. Row-Level Security (RLS) の検証

**必須パターン:**
- `ctx.issuer.public(ctx, tx => {...})` - 公開クエリ
- `ctx.issuer.internal(ctx, tx => {...})` - 内部/管理者クエリ
- `ctx.issuer.onlyBelongingCommunity(ctx, async tx => {...})` - ユーザーの所属コミュニティのみ

**違反としてフラグするもの:**
- ❌ `ctx.issuer` ラッパーなしの直接Prismaクエリ
- ❌ `communityId` 分離チェックの欠如
- ❌ RLSメソッドを使用していないRepository

---

### 4. GraphQL型の命名規則

**正しい:**
- 型: `GqlUser`, `GqlCommunity`
- 入力: `GqlCreateUserInput`, `GqlUpdateCommunityInput`
- ペイロード: `GqlUserPayload`, `GqlCommunityConnection`
- Prisma型: `PrismaUser`, `PrismaCommunity`

**違反としてフラグするもの:**
- ❌ `GqlXxx` 型を返すService
- ❌ Service/Repositoryレイヤーで使用されているGraphQL型
- ❌ 誤った命名規則

---

### 5. DataLoaderによるN+1問題防止

**フィールドリゾルバはDataLoaderを使用する必要がある:**
```typescript
Opportunity: {
  community: (parent, _, ctx) => ctx.loaders.community.load(parent.communityId),
  createdByUser: (parent, _, ctx) => ctx.loaders.user.load(parent.createdBy)
}
```

**違反としてフラグするもの:**
- ❌ データベースへの直接クエリを行うフィールドリゾルバ
- ❌ `controller/dataloader.ts` のDataLoader定義の欠如

---

## 検証プロセス

### ステップ1: 検証対象ファイルの特定

`$ARGUMENTS` が指定された場合:
```bash
# 特定のドメインを検証
find src/application/domain/"$ARGUMENTS" -type f \( -name "*.ts" -o -name "*.graphql" \)
```

指定がない場合:
```bash
# 未コミット変更を検証
git status --porcelain | grep -E '^\s*[MA]' | cut -c 4-
```

### ステップ2: ファイルの読み取りと分析

各ファイルに対してレイヤー固有のチェックを実行:

**`controller/resolver.ts` の場合:**
- Repositoryの直接呼び出しを検索（例: `repository.find`, `repository.create`）
- 全てのフィールドリゾルバが `ctx.loaders` を使用していることを確認

**`usecase.ts` の場合:**
- `ctx.issuer.onlyBelongingCommunity(ctx, async (tx) => ...)` パターンを確認
- 他ドメインのUseCaseの呼び出しをチェック（例: `otherDomainUseCase.doSomething()`）
- 返却前にPresenterを呼び出していることを確認

**`service.ts` の場合:**
- `Gql` 型のインポートまたは返却を検索
- `tx` パラメータが適切に宣言され、渡されていることを確認
- 不適切なクロスドメインUseCaseの呼び出しをチェック

**`data/repository.ts` の場合:**
- 全てのクエリが `ctx.issuer.public/internal/onlyBelongingCommunity` を使用していることを確認
- Mutationメソッド（create/update/delete）が必須の `tx: Prisma.TransactionClient` を使用していることをチェック
- オプショナルの `tx?` を使用するQueryメソッドで `if (tx)` 分岐を実装していることをチェック
- ビジネスロジック（複雑な条件文、バリデーション）を検索

**`data/converter.ts` の場合:**
- `tx` パラメータがないことを確認
- Prismaクライアントの使用がないことを確認

**`presenter.ts` の場合:**
- 純粋関数のみであることを確認
- Prismaクライアントの使用がないことを確認

**`schema/*.graphql` の場合:**
- 型命名が `Gql*` 規約に従っていることを確認
- 対応するResolverの実装があることをチェック

### ステップ3: 検出結果の報告

構造化されたレポートを生成:

```markdown
# アーキテクチャ検証レポート

## サマリー
- 分析ファイル数: X
- 検出違反数: Y
- 重大問題数: Z

## 違反

### レイヤー違反
- [ ] **ファイル**: `src/application/domain/opportunity/controller/resolver.ts:45`
  - **問題**: ResolverがRepositoryを直接呼び出している
  - **修正**: UseCaseメソッドを呼び出すように変更

### トランザクションパターンの問題
- [ ] **ファイル**: `src/application/domain/user/service.ts:120`
  - **問題**: Repositoryへの `tx` パラメータ伝播が欠けている
  - **修正**: `tx` パラメータを追加し、Repositoryメソッドに渡す

### Row-Level Securityの問題
- [ ] **ファイル**: `src/application/domain/community/data/repository.ts:78`
  - **問題**: `ctx.issuer` なしの直接Prismaクエリ
  - **修正**: クエリを `ctx.issuer.public(ctx, tx => ...)` でラップ

### GraphQL型の違反
- [ ] **ファイル**: `src/application/domain/wallet/service.ts:56`
  - **問題**: Serviceが `GqlWallet` 型を返している
  - **修正**: Prisma型を返し、Presenterで変換

### DataLoaderの欠如
- [ ] **ファイル**: `src/application/domain/opportunity/controller/resolver.ts:89`
  - **問題**: フィールドリゾルバが直接データベースクエリを実行
  - **修正**: `ctx.loaders.community.load(parent.communityId)` を使用

## 推奨事項

1. 完全なアーキテクチャガイドラインについては @CLAUDE.md を確認
2. リグレッションがないことを確認するため `pnpm test` を実行
3. Service内のビジネスロジックに対するユニットテストの追加を検討
```

---

## 追加チェック

### 依存性注入の検証
- 全てのService/Repositoryが `src/application/provider.ts` に登録されていることを確認
- `@injectable()` および `@inject("ServiceName")` デコレータをチェック

### GraphQLスキーマの同期
- スキーマ変更後、`pnpm gql:generate` が実行されたことを確認
- TypeScriptコンパイルエラーをチェック

### セキュリティチェック
- パスワードやシークレットがログに出力されていないこと
- Serviceレイヤーでの入力バリデーション
- パラメータ化クエリ（Prismaが処理）

---

## 終了基準

以下の場合にレポートが完成:
- ✅ スコープ内の全ファイルが分析された
- ✅ 各違反にファイルパス、行番号、修正案が含まれる
- ✅ サマリー統計が正確である
- ✅ 推奨事項が実行可能である

---

## 参考資料

完全なアーキテクチャドキュメントと実装パターンについては `@CLAUDE.md` を参照してください。
