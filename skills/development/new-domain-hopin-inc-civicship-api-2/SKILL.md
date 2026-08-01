---
name: new-domain
description: DDD（ドメイン駆動設計） と Clean Architecture の原則に従い、完全なディレクトリ構造、テンプレートファイル、依存性注入の設定を含む新しいドメインを作成します。
---

---
name: new-domain
description: 新規ドメイン作成
user-invocable: true
argument-hint: [ドメイン名] [親カテゴリ]
allowed-tools: Read, Write, Edit, Bash
---

# civicship-api 新規ドメイン作成

**DDD（ドメイン駆動設計）** と **Clean Architecture** の原則に従い、完全なディレクトリ構造、テンプレートファイル、依存性注入の設定を含む新しいドメインを作成します。

## 使用方法

```bash
# 既存のカテゴリに新しいドメインを作成
/new-domain article content

# 新しいカテゴリに新しいドメインを作成
/new-domain product marketplace
```

**引数:**
- `$ARGUMENTS[0]`: ドメイン名（例: `article`, `product`, `review`）
- `$ARGUMENTS[1]`: 親カテゴリ（例: `content`, `experience`, `account`, `reward`）

---

## ドメイン構造テンプレート

このスキルは以下の完全な構造を作成します:

```
src/application/domain/{category}/{domain-name}/
├── controller/
│   ├── resolver.ts          # GraphQL Query/Mutation/フィールドリゾルバ
│   └── dataloader.ts        # N+1問題防止（バッチローディング）
├── usecase.ts               # ビジネスフローのオーケストレーション
├── service.ts               # ビジネスロジック & バリデーション
├── data/
│   ├── repository.ts        # Prismaデータベースクエリ
│   ├── interface.ts         # Repository インターフェース契約
│   ├── converter.ts         # GraphQL input → Prisma形式
│   └── type.ts              # TypeScript型（Prisma select shapes）
├── presenter.ts             # Prisma → GraphQLレスポンスのフォーマッティング
└── schema/
    ├── query.graphql        # クエリ定義
    ├── mutation.graphql     # ミューテーション定義
    └── type.graphql         # 型定義
```

---

## ステップバイステップのプロセス

### ステップ1: 引数の検証

`$ARGUMENTS` からドメイン名とカテゴリを抽出:

```bash
DOMAIN_NAME="${ARGUMENTS[0]}"    # e.g., "article"
CATEGORY="${ARGUMENTS[1]}"       # e.g., "content"

# PascalCase/camelCaseへの変換
# 例: "point-expiration" → "PointExpiration" / "pointExpiration"
DomainName=$(echo "${DOMAIN_NAME}" | sed -r 's/(^|-)([a-z])/\U\2/g')  # PascalCase
domainName=$(echo "${DOMAIN_NAME}" | sed -r 's/-([a-z])/\U\1/g')      # camelCase
Category=$(echo "${CATEGORY}" | sed 's/\b\(.\)/\u\1/')                # PascalCase
```

**検証:**
- ドメイン名は小文字、英数字、ハイフンのみ
- カテゴリは以下のいずれか: `account`, `content`, `experience`, `reward`, `location`, `transaction`, `notification`
- ドメインが既に存在しないことを確認

### ステップ2: ディレクトリ構造の作成

```bash
BASE_PATH="src/application/domain/${CATEGORY}/${DOMAIN_NAME}"

mkdir -p "${BASE_PATH}/controller"
mkdir -p "${BASE_PATH}/data"
mkdir -p "${BASE_PATH}/schema"
```

### ステップ3: テンプレートファイルの生成

`.claude/skills/new-domain/templates/` のテンプレートに基づいて各ファイルを作成:

1. **controller/resolver.ts** - GraphQLリゾルバ
   - DIを介してUseCaseをインポート
   - Query、Mutation、フィールドリゾルバを定義
   - リレーションシップにDataLoaderを使用

2. **controller/dataloader.ts** - DataLoaderのセットアップ
   - N+1問題防止のバッチローディング
   - 関連エンティティの読み込み

3. **usecase.ts** - ビジネスフローのオーケストレーション
   - `ctx.issuer.onlyBelongingCommunity()` でトランザクションを管理
   - Serviceとpresenterを呼び出す
   - Repositoryへの直接アクセスなし

4. **service.ts** - ビジネスロジック
   - バリデーションとビジネスルール
   - Repositoryを呼び出す
   - `tx` パラメータを受け取り、伝播する

5. **data/repository.ts** - データベースアクセス
   - RLS（`ctx.issuer`）を使用したPrismaクエリ
   - 2つのトランザクションパターン:
     - Mutationメソッド: 必須の `tx: Prisma.TransactionClient`
     - Queryメソッド: オプショナルの `tx?: Prisma.TransactionClient` と `if (tx)` 分岐

6. **data/interface.ts** - Repository契約
   - Repositoryのインターフェース定義

7. **data/converter.ts** - 入力変換
   - GraphQL input → Prisma形式
   - 純粋関数（副作用なし）

8. **data/type.ts** - TypeScript型
   - Prisma select shapes
   - 型定義

9. **presenter.ts** - レスポンスのフォーマッティング
   - Prisma → GraphQL型
   - 純粋関数（ビジネスロジックなし）

10. **schema/query.graphql** - GraphQLクエリ
    - クエリ定義

11. **schema/mutation.graphql** - GraphQLミューテーション
    - ミューテーション定義

12. **schema/type.graphql** - GraphQL型
    - 型、入力、ペイロード定義
    - `Gql*` 命名規則に従う

### ステップ4: 依存性の登録

**ファイル: `src/application/provider.ts`**

インポートを追加（カテゴリセクション内でアルファベット順）:

```typescript
import {{DomainName}}UseCase from "@/application/domain/{{category}}/{{domain-name}}/usecase";
import {{DomainName}}Service from "@/application/domain/{{category}}/{{domain-name}}/service";
import {{DomainName}}Repository from "@/application/domain/{{category}}/{{domain-name}}/data/repository";
import {{DomainName}}Converter from "@/application/domain/{{category}}/{{domain-name}}/data/converter";
```

適切なセクションに登録を追加:

```typescript
// 📦 {{Category}}

container.register("{{DomainName}}UseCase", { useClass: {{DomainName}}UseCase });
container.register("{{DomainName}}Service", { useClass: {{DomainName}}Service });
container.register("{{DomainName}}Repository", { useClass: {{DomainName}}Repository });
container.register("{{DomainName}}Converter", { useClass: {{DomainName}}Converter });
```

### ステップ5: GraphQLリゾルバの登録

**ファイル: `src/presentation/graphql/resolver.ts`**

インポートを追加:

```typescript
import {{DomainName}}Resolver from "@/application/domain/{{category}}/{{domain-name}}/controller/resolver";
```

リゾルバのインスタンス化を追加:

```typescript
const {{domainName}} = container.resolve({{DomainName}}Resolver);
```

resolversオブジェクトに追加:

```typescript
const resolvers = {
  Query: {
    ...{{domainName}}.Query,
    // ...
  },
  Mutation: {
    ...{{domainName}}.Mutation,
    // ...
  },
  {{DomainName}}: {{domainName}}.{{DomainName}},
  // ...
};
```

### ステップ6: コード生成の実行

GraphQLスキーマファイル作成後:

```bash
pnpm gql:generate
```

これにより `src/types/graphql.ts` にTypeScript型が生成されます。

### ステップ7: テストスケルトンの生成

テスト駆動開発を促進するため、テストファイルのスケルトンを生成:

```bash
TEST_BASE="__tests__"

# ユニットテスト（Service層）
mkdir -p "${TEST_BASE}/unit/${CATEGORY}/${DOMAIN_NAME}"
cat > "${TEST_BASE}/unit/${CATEGORY}/${DOMAIN_NAME}/service.test.ts" <<EOF
import { container } from "tsyringe";
import { describe, it, expect, beforeEach } from "@jest/globals";
import ${DomainName}Service from "@/application/domain/${CATEGORY}/${DOMAIN_NAME}/service";

describe("${DomainName}Service", () => {
  let service: ${DomainName}Service;

  beforeEach(() => {
    container.reset();
    // TODO: Mock dependencies
    service = container.resolve(${DomainName}Service);
  });

  describe("TODO: メソッド名", () => {
    it("TODO: テストケース", async () => {
      // TODO: Implement test
      expect(true).toBe(true);
    });
  });
});
EOF

# 統合テスト（UseCase層）
mkdir -p "${TEST_BASE}/integration/${CATEGORY}/${DOMAIN_NAME}"
cat > "${TEST_BASE}/integration/${CATEGORY}/${DOMAIN_NAME}/usecase.test.ts" <<EOF
import { container } from "tsyringe";
import { describe, it, expect, beforeEach } from "@jest/globals";
import ${DomainName}UseCase from "@/application/domain/${CATEGORY}/${DOMAIN_NAME}/usecase";

describe("${DomainName}UseCase", () => {
  let usecase: ${DomainName}UseCase;

  beforeEach(() => {
    container.reset();
    // TODO: Setup database and dependencies
    usecase = container.resolve(${DomainName}UseCase);
  });

  describe("TODO: メソッド名", () => {
    it("TODO: テストケース", async () => {
      // TODO: Implement integration test
      expect(true).toBe(true);
    });
  });
});
EOF

# E2Eテスト（GraphQL API層）
mkdir -p "${TEST_BASE}/e2e/${CATEGORY}/${DOMAIN_NAME}"
cat > "${TEST_BASE}/e2e/${CATEGORY}/${DOMAIN_NAME}/graphql.test.ts" <<EOF
import { describe, it, expect } from "@jest/globals";
import { createTestServer } from "@/test/helper/server";

describe("${DomainName} GraphQL API", () => {
  const server = createTestServer();

  describe("Query", () => {
    it("TODO: クエリテストケース", async () => {
      const query = \`
        query {
          # TODO: Add query
        }
      \`;

      const response = await server.executeOperation({ query });
      expect(response.errors).toBeUndefined();
      // TODO: Add assertions
    });
  });

  describe("Mutation", () => {
    it("TODO: ミューテーションテストケース", async () => {
      const mutation = \`
        mutation {
          # TODO: Add mutation
        }
      \`;

      const response = await server.executeOperation({ query: mutation });
      expect(response.errors).toBeUndefined();
      // TODO: Add assertions
    });
  });
});
EOF
```

**生成されるテストファイル:**
- `__tests__/unit/{{category}}/{{domain-name}}/service.test.ts` - Service層のユニットテスト
- `__tests__/integration/{{category}}/{{domain-name}}/usecase.test.ts` - UseCase層の統合テスト
- `__tests__/e2e/{{category}}/{{domain-name}}/graphql.test.ts` - GraphQL APIのE2Eテスト

### ステップ8: セットアップの確認

1. TypeScriptコンパイルのチェック:
   ```bash
   pnpm build
   ```

2. DI登録の確認:
   - 全てのServiceがエラーなく解決されること

3. 生成されたファイルのレビュー:
   - 各ファイルがアーキテクチャパターンに従っていること
   - TODOやプレースホルダーロジックが残っていないこと

---

## テンプレートプレースホルダー

テンプレートは以下のプレースホルダーを使用します:

| プレースホルダー | 例 | 説明 |
|-------------|---------|-------------|
| `{{DOMAIN_NAME}}` | `article` | ドメイン名（lowercase-kebab-case） |
| `{{DomainName}}` | `Article` | ドメイン名（PascalCase） |
| `{{domainName}}` | `article` | ドメイン名（camelCase） |
| `{{CATEGORY}}` | `content` | カテゴリ名（lowercase） |
| `{{Category}}` | `Content` | カテゴリ名（PascalCase） |

---

## アーキテクチャ準拠チェックリスト

ドメイン作成後、以下を確認:

- ✅ **Resolver** がUseCaseメソッドのみを呼び出している
- ✅ **UseCase** が `ctx.issuer.onlyBelongingCommunity()` でトランザクションを管理
- ✅ **Service** がビジネスロジックを実装し、`tx` をRepositoryに渡している
- ✅ **Repository** が全てのクエリでRLS（`ctx.issuer`）を使用
- ✅ **Repository** が `tx` パラメータを正しく処理（mutationは必須、queryはオプショナル）
- ✅ **Converter** が純粋関数（副作用なし）
- ✅ **Presenter** がPrisma → GraphQL型に変換
- ✅ **GraphQL型** が `Gql*` 命名規則に従っている
- ✅ **DataLoader** がフィールドリゾルバで使用されている（N+1問題防止）
- ✅ **DI登録** が `provider.ts` にある
- ✅ **リゾルバ登録** が `resolver.ts` にある
- ✅ **GraphQL codegen** が正常に実行された
- ✅ **テストファイル** が unit/integration/e2e の3層に存在する

---

## 出力例

`/new-domain product marketplace` 実行後:

```
✅ ドメイン構造を作成しました: src/application/domain/marketplace/product/
✅ 15ファイルを生成しました:
   - controller/resolver.ts
   - controller/dataloader.ts
   - usecase.ts
   - service.ts
   - data/repository.ts
   - data/interface.ts
   - data/converter.ts
   - data/type.ts
   - presenter.ts
   - schema/query.graphql
   - schema/mutation.graphql
   - schema/type.graphql

✅ テストスケルトンを作成しました:
   - __tests__/unit/marketplace/product/service.test.ts
   - __tests__/integration/marketplace/product/usecase.test.ts
   - __tests__/e2e/marketplace/product/graphql.test.ts

✅ src/application/provider.ts を更新しました（4件の登録）
✅ src/presentation/graphql/resolver.ts を更新しました

⚠️  次のステップ:
1. 実行: pnpm gql:generate
2. service.ts にビジネスロジックを実装
3. schema/ ディレクトリにGraphQLスキーマを定義
4. テストファイルのTODOを実装
5. 実行: /validate-architecture marketplace/product
```

---

## 参考資料

完全なアーキテクチャドキュメントと実装パターンについては `@CLAUDE.md` を参照してください。
