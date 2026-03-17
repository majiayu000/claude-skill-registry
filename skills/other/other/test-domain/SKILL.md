---
name: test-domain
description: ドメイン単位テスト実行
user-invocable: true
argument-hint: [ドメイン名]
allowed-tools: Read, Bash
---

# civicship-api ドメイン単体テスト

特定のドメインのテストのみを実行し、詳細なレポートとカバレッジを生成します。全体テスト（数分）ではなく、特定ドメインのみ（数秒）で高速フィードバックを提供します。

## 使用方法

```bash
# 特定のドメインのテストを実行
/test-domain opportunity

# カバレッジ付きで実行
/test-domain user --coverage

# 全てのテストを実行
/test-domain
```

**引数:**
- `$ARGUMENTS[0]`: ドメイン名（例: `opportunity`, `user`, `wallet`）
- オプション: `--coverage` カバレッジレポートを生成

---

## テストプロセス

### ステップ1: ドメインの特定

`$ARGUMENTS` が指定された場合、そのドメインのテストファイルを検索:

```bash
DOMAIN_NAME="$ARGUMENTS"

# ドメインのテストファイルを検索
find src/application/domain -path "*/${DOMAIN_NAME}/*" -name "*.test.ts"
find __tests__ -path "*/${DOMAIN_NAME}/*" -name "*.test.ts"
```

**検証:**
- ドメインが存在することを確認
- テストファイルが存在することを確認

**テストファイルが見つからない場合:**

```markdown
⚠️  ドメイン `${DOMAIN_NAME}` のテストファイルが見つかりませんでした

以下を確認してください:
1. ドメイン名が正しいか（例: `opportunity`, `user`, `wallet`）
2. テストファイルが存在するか
   - `src/application/domain/**/${DOMAIN_NAME}/**/*.test.ts`
   - `__tests__/**/${DOMAIN_NAME}/**/*.test.ts`
```

---

### ステップ2: テストファイルの一覧表示

見つかったテストファイルを表示:

```markdown
## テスト対象ファイル

以下のテストファイルを実行します:

- src/application/domain/experience/opportunity/service.test.ts
- src/application/domain/experience/opportunity/data/converter.test.ts
- __tests__/unit/opportunity/usecase.test.ts
- __tests__/integration/opportunity/graphql.test.ts

合計: 4ファイル
```

---

### ステップ3: テストの実行

**基本実行（カバレッジなし）:**

```bash
pnpm test src/application/domain/**/${DOMAIN_NAME}/**/*.test.ts __tests__/**/${DOMAIN_NAME}/**/*.test.ts --runInBand
```

**カバレッジ付き実行:**

```bash
pnpm test:coverage src/application/domain/**/${DOMAIN_NAME}/**/*.test.ts __tests__/**/${DOMAIN_NAME}/**/*.test.ts --runInBand
```

**重要:**
- `--runInBand` フラグを必ず使用（データベーステストのシリアル実行）
- トランザクションの競合を防ぐため

---

### ステップ4: テスト結果の解析

**成功した場合:**

```markdown
## テスト結果

✅ 全てのテストが成功しました

**統計:**
- テストスイート: 4 passed
- テスト数: 24 passed
- 実行時間: 3.2秒

**カバレッジ:**
- Statements: 95.2%
- Branches: 88.7%
- Functions: 92.1%
- Lines: 94.8%
```

**失敗した場合:**

```markdown
## テスト結果

❌ 一部のテストが失敗しました

**統計:**
- テストスイート: 3 passed, 1 failed
- テスト数: 20 passed, 4 failed
- 実行時間: 3.5秒

### 失敗したテスト

1. **OpportunityService.createOpportunity**
   - ファイル: `src/application/domain/experience/opportunity/service.test.ts:45`
   - エラー: `Expected communityId to be validated`
   - 修正案: Serviceでのバリデーションロジックを確認

2. **OpportunityUseCase.managerCreateOpportunity**
   - ファイル: `__tests__/unit/opportunity/usecase.test.ts:120`
   - エラー: `TypeError: Cannot read property 'id' of null`
   - 修正案: モックデータが正しくセットアップされているか確認

### 推奨アクション

1. 失敗したテストファイルを確認
2. モックやフィクスチャデータを見直す
3. テストを修正して再実行: `/test-domain opportunity`
```

---

### ステップ5: カバレッジ分析（--coverage オプション時）

カバレッジレポートを読み取り、分析:

```bash
# カバレッジレポートの表示
cat coverage/lcov-report/index.html
```

**カバレッジが低い場合の警告:**

```markdown
## カバレッジ警告

⚠️  以下のファイルはカバレッジが低いです（< 80%）:

| ファイル | Statements | Branches | Functions | Lines |
|---------|-----------|----------|-----------|-------|
| service.ts | 68.2% | 55.3% | 70.0% | 67.8% |
| converter.ts | 75.4% | 62.1% | 80.0% | 74.9% |

### 推奨事項

1. **service.ts** のエッジケースをカバーするテストを追加
2. **converter.ts** のエラーハンドリングをテスト
3. ブランチカバレッジを向上（条件分岐のテスト）
```

---

## テストパターンごとの実行

### ユニットテストのみ実行

```bash
/test-domain opportunity --unit
```

対象: `__tests__/unit/**/${DOMAIN_NAME}/**/*.test.ts`

### 統合テストのみ実行

```bash
/test-domain opportunity --integration
```

対象: `__tests__/integration/**/${DOMAIN_NAME}/**/*.test.ts`

### E2Eテストのみ実行

```bash
/test-domain opportunity --e2e
```

対象: `__tests__/e2e/**/${DOMAIN_NAME}/**/*.test.ts`

---

## テスト種類別のガイドライン

### ユニットテスト（Unit Tests）

**対象:**
- Service層のビジネスロジック
- Converter層の変換ロジック
- Presenter層のフォーマッティング
- Validator層のバリデーション

**特徴:**
- 依存関係をモック化
- 高速実行（ミリ秒単位）
- データベース接続不要

**例:**

```typescript
describe("OpportunityService", () => {
  let service: OpportunityService;
  let mockRepository: jest.Mocked<IOpportunityRepository>;

  beforeEach(() => {
    mockRepository = {
      create: jest.fn(),
      find: jest.fn(),
    } as any;

    service = new OpportunityService(mockRepository);
  });

  it("should create opportunity with valid data", async () => {
    const input = { title: "Test", description: "Test" };
    mockRepository.create.mockResolvedValue(mockOpportunity);

    const result = await service.createOpportunity(ctx, input, "community-id", tx);

    expect(result).toBeDefined();
    expect(mockRepository.create).toHaveBeenCalledWith(ctx, expect.any(Object), tx);
  });
});
```

---

### 統合テスト（Integration Tests）

**対象:**
- UseCase ↔ Service ↔ Repository の連携
- データベース操作の実際の動作
- トランザクション管理

**特徴:**
- 実際のデータベースを使用
- 実際の依存関係を使用
- 中速実行（秒単位）

**例:**

```typescript
describe("OpportunityUseCase Integration", () => {
  let usecase: OpportunityUseCase;
  let ctx: IContext;

  beforeEach(async () => {
    // 実際のDIコンテナから解決
    usecase = container.resolve(OpportunityUseCase);
    ctx = await createTestContext();
  });

  afterEach(async () => {
    // テストデータのクリーンアップ
    await cleanupTestData();
  });

  it("should create opportunity and commit transaction", async () => {
    const input: GqlOpportunityCreateInput = {
      title: "Test Opportunity",
      description: "Test Description",
    };

    const result = await usecase.managerCreateOpportunity({ input, permission }, ctx);

    expect(result.opportunity).toBeDefined();

    // データベースで確認
    const saved = await prisma.opportunity.findUnique({ where: { id: result.opportunity.id } });
    expect(saved).toBeDefined();
  });
});
```

---

### E2Eテスト（End-to-End Tests）

**対象:**
- GraphQL API エンドポイント
- ユーザージャーニー全体
- 認証・認可フロー

**特徴:**
- 実際のHTTPリクエスト
- 実際の認証トークン
- 低速実行（秒〜分単位）

**例:**

```typescript
describe("Opportunity GraphQL API", () => {
  let server: ApolloServer;
  let token: string;

  beforeAll(async () => {
    server = await createTestServer();
    token = await generateTestToken({ role: "manager" });
  });

  it("should create opportunity via GraphQL mutation", async () => {
    const mutation = `
      mutation {
        opportunityCreate(input: {
          title: "Test Opportunity"
          description: "Test Description"
        }) {
          opportunity {
            id
            title
          }
        }
      }
    `;

    const response = await server.executeOperation(
      { query: mutation },
      { req: { headers: { authorization: `Bearer ${token}` } } }
    );

    expect(response.data?.opportunityCreate.opportunity).toBeDefined();
  });
});
```

---

## テスト失敗時のデバッグ

### 一般的な失敗原因

1. **モックの設定ミス**
   ```typescript
   // ❌ 間違い
   mockRepository.create.mockResolvedValue(undefined);

   // ✅ 正しい
   mockRepository.create.mockResolvedValue(mockOpportunity);
   ```

2. **トランザクション関連**
   ```typescript
   // ❌ 間違い: txを渡していない
   await service.createOpportunity(ctx, input, communityId);

   // ✅ 正しい: txを渡す
   await service.createOpportunity(ctx, input, communityId, tx);
   ```

3. **非同期処理の待機忘れ**
   ```typescript
   // ❌ 間違い: await なし
   service.createOpportunity(ctx, input, communityId, tx);

   // ✅ 正しい: await あり
   await service.createOpportunity(ctx, input, communityId, tx);
   ```

4. **テストデータのクリーンアップ漏れ**
   ```typescript
   afterEach(async () => {
     // ✅ 必ずクリーンアップ
     await prisma.opportunity.deleteMany({ where: { title: { startsWith: "Test" } } });
   });
   ```

---

## ベストプラクティス

### テスト作成時

- ✅ **AAA パターン** を使用（Arrange, Act, Assert）
- ✅ **1テスト1アサーション** を原則とする
- ✅ **説明的なテスト名** を使用
  - 良い例: `"should throw error when communityId is invalid"`
  - 悪い例: `"test create opportunity"`
- ✅ **beforeEach/afterEach** でセットアップとクリーンアップ
- ✅ **describe ブロック** で論理的にグループ化

### テスト実行時

- ✅ 変更後は **必ず該当ドメインのテストを実行**
- ✅ PRマージ前に **全テストを実行**
- ✅ カバレッジを **定期的に確認**（目標: 80%以上）
- ✅ 失敗したテストを **すぐに修正**

---

## テストカバレッジ目標

| レイヤー | 目標カバレッジ | 理由 |
|---------|---------------|------|
| **Service** | 90%以上 | ビジネスロジックの中核 |
| **UseCase** | 85%以上 | フロー制御の検証 |
| **Converter** | 95%以上 | シンプルな変換ロジック |
| **Presenter** | 95%以上 | シンプルなフォーマッティング |
| **Repository** | 80%以上 | 統合テストでカバー |
| **Resolver** | 70%以上 | E2Eテストでカバー |

---

## 参考資料

以下については `@CLAUDE.md` を参照してください:
- テストコマンド（`pnpm test`）
- テスト構造
- Prisma Fabbrica（ファクトリ）の使用
- テストフィクスチャ
