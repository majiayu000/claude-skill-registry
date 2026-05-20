---
name: security-review
description: セキュリティレビュー
context: fork
agent: Explore
user-invocable: true
argument-hint: [パスまたはドメイン名]
allowed-tools: Read, Grep, Bash
---

# civicship-api セキュリティレビュー

認証、認可、Row-Level Security (RLS)、センシティブデータの取り扱いに焦点を当てたセキュリティレビューを実行します。

`$ARGUMENTS` が指定された場合、その特定のパスまたはドメインをレビューします。指定がない場合は、現在のブランチの未コミット変更を全てレビューします。

---

## セキュリティチェック項目

### 1. 認証（Authentication）

**Firebase Auth 統合:**

```typescript
// ✅ 正しい: ctxからユーザー情報を取得
async someMethod(ctx: IContext) {
  const userId = ctx.user?.uid;
  if (!userId) {
    throw new UnauthorizedError();
  }
}

// ❌ 間違い: 認証チェックなし
async someMethod(ctx: IContext) {
  // ctx.user のチェックなし
  await this.repository.create(...);
}
```

**チェック項目:**
- ✅ Resolver/UseCaseで `ctx.user` が適切に検証されている
- ✅ 認証が必要なMutationで認証チェックが行われている
- ✅ Firebase認証トークンが正しく伝播されている
- ❌ 認証なしでセンシティブな操作が実行されていない

---

### 2. 認可（Authorization）

**Row-Level Security (RLS) の実装:**

```typescript
// ✅ 正しい: ctx.issuerでRLSを適用
async findOpportunity(ctx: IContext, id: string) {
  return ctx.issuer.public(ctx, (tx) => {
    return tx.opportunity.findUnique({
      where: { id },
      select: opportunitySelectDetail,
    });
  });
}

// ❌ 間違い: 直接Prismaクエリ（RLSバイパス）
async findOpportunity(ctx: IContext, id: string) {
  return prismaClient.opportunity.findUnique({
    where: { id },
    select: opportunitySelectDetail,
  });
}
```

**RLSメソッドの種類:**

| メソッド | 用途 | アクセス範囲 |
|---------|------|------------|
| `ctx.issuer.public()` | 公開データ | 全ユーザー |
| `ctx.issuer.internal()` | 内部/管理者操作 | システム管理者 |
| `ctx.issuer.onlyBelongingCommunity()` | ユーザーのコミュニティ | 所属コミュニティのみ |

**チェック項目:**
- ✅ 全てのRepositoryで `ctx.issuer` メソッドを使用している
- ✅ `communityId` によるデータ分離が適切に行われている
- ✅ ユーザーは自分のコミュニティのデータのみにアクセスできる
- ❌ RLSバイパス（直接Prismaクライアント使用）がない

---

### 3. センシティブデータの取り扱い

**ログ出力の安全性:**

```typescript
// ❌ 危険: パスワードをログ出力
logger.info("User login", { email, password });

// ✅ 安全: センシティブデータを除外
logger.info("User login", { email });

// ❌ 危険: APIキーをログ出力
logger.error("API call failed", { apiKey, error });

// ✅ 安全: APIキーをマスク
logger.error("API call failed", { apiKey: "***", error });
```

**センシティブデータの種類:**
- パスワード
- APIキー、シークレット
- 認証トークン
- クレジットカード情報
- 個人識別情報（PII）の一部

**チェック項目:**
- ✅ センシティブデータがログに出力されていない
- ✅ エラーメッセージにセンシティブデータが含まれていない
- ✅ デバッグログが本番環境で無効化されている
- ❌ `console.log` にセンシティブデータが含まれていない

---

### 4. 入力バリデーション

**Service層でのバリデーション:**

```typescript
// ✅ 正しい: 入力バリデーション
async createOpportunity(ctx: IContext, input: GqlOpportunityCreateInput, communityId: string, tx) {
  // バリデーション
  if (!input.title || input.title.length > 200) {
    throw new ValidationError("Title must be 1-200 characters");
  }

  if (!input.description || input.description.length > 5000) {
    throw new ValidationError("Description must be 1-5000 characters");
  }

  if (input.requiredSkills && input.requiredSkills.length > 10) {
    throw new ValidationError("Maximum 10 skills allowed");
  }

  // ビジネスロジック
  const data = this.converter.create(input, communityId);
  return await this.repository.create(ctx, data, tx);
}

// ❌ 間違い: バリデーションなし
async createOpportunity(ctx: IContext, input: GqlOpportunityCreateInput, communityId: string, tx) {
  const data = this.converter.create(input, communityId);
  return await this.repository.create(ctx, data, tx);
}
```

**チェック項目:**
- ✅ Service層で入力バリデーションが行われている
- ✅ 文字列長の制限がある
- ✅ 数値の範囲チェックがある
- ✅ Enum値が許可されたもののみ
- ❌ ユーザー入力が直接SQLに渡されていない（Prismaが防ぐ）

---

### 5. SQLインジェクション対策

**Prismaの安全性:**

```typescript
// ✅ 安全: Prismaのパラメータ化クエリ
await tx.opportunity.findMany({
  where: { title: { contains: userInput } },
});

// ✅ 安全: Prisma型付きクエリ
await tx.$queryRawTyped(getOpportunitiesByTitle(userInput));

// ⚠️  注意: $queryRaw使用時はパラメータ化必須
await tx.$queryRaw`SELECT * FROM t_opportunities WHERE title = ${userInput}`;
// ↑ これは安全（テンプレートリテラルがパラメータ化）

// ❌ 危険: 文字列結合
await tx.$queryRawUnsafe(`SELECT * FROM t_opportunities WHERE title = '${userInput}'`);
// ↑ これは危険（SQLインジェクションの可能性）
```

**チェック項目:**
- ✅ Prismaのパラメータ化クエリを使用している
- ✅ `$queryRaw` 使用時はテンプレートリテラルを使用
- ❌ `$queryRawUnsafe` を使用していない
- ❌ 文字列結合によるSQL構築がない

---

### 6. 環境変数とシークレット管理

**安全な環境変数の使用:**

```typescript
// ✅ 正しい: .envからシークレット読み込み
const apiKey = process.env.FIREBASE_PRIVATE_KEY;

// ✅ 正しい: シークレットをコードに含めない
const config = {
  apiKey: process.env.API_KEY,
  apiSecret: process.env.API_SECRET,
};

// ❌ 危険: シークレットをハードコード
const apiKey = "sk_live_abc123xyz...";

// ❌ 危険: シークレットをGitにコミット
// .env ファイルを .gitignore に追加すること
```

**チェック項目:**
- ✅ シークレットが `.env` ファイルで管理されている
- ✅ `.env` が `.gitignore` に含まれている
- ✅ 本番環境のシークレットが別管理されている
- ❌ ハードコードされたシークレットがない
- ❌ コミット履歴にシークレットが含まれていない

---

### 7. CORS とAPIセキュリティ

**CORS設定:**

```typescript
// ✅ 適切: 特定のオリジンのみ許可
const corsOptions = {
  origin: process.env.ALLOWED_ORIGINS?.split(',') || ['https://app.example.com'],
  credentials: true,
};

// ❌ 危険: 全てのオリジンを許可
const corsOptions = {
  origin: '*',
  credentials: true,
};
```

**チェック項目:**
- ✅ CORS設定が適切に制限されている
- ✅ 認証情報（cookies）を含むリクエストで origin を制限
- ❌ 本番環境で `origin: '*'` を使用していない

---

### 8. レート制限（Rate Limiting）

**GraphQL クエリの制限:**

```typescript
// ✅ 推奨: クエリの複雑度制限
const server = new ApolloServer({
  validationRules: [
    depthLimit(10),  // クエリの深さ制限
    createComplexityLimitRule(1000),  // クエリの複雑度制限
  ],
});

// ✅ 推奨: リクエスト数制限
app.use(rateLimit({
  windowMs: 15 * 60 * 1000,  // 15分
  max: 100,  // 最大100リクエスト
}));
```

**チェック項目:**
- ✅ GraphQLクエリの深さ制限がある
- ✅ クエリの複雑度制限がある
- ✅ レート制限が実装されている
- ⚠️  DoS攻撃への対策が検討されている

---

## セキュリティレビュープロセス

### ステップ1: 対象ファイルの特定

`$ARGUMENTS` が指定された場合:
```bash
# 特定のドメインを検証
find src/application/domain/"$ARGUMENTS" -type f -name "*.ts"
```

指定がない場合:
```bash
# 未コミット変更を検証
git status --porcelain | grep -E '^\s*[MA]' | grep '\.ts$' | cut -c 4-
```

---

### ステップ2: セキュリティスキャン

各ファイルに対して以下をチェック:

**認証チェック:**
```bash
# ctx.user のチェック漏れを検索
grep -n "ctx: IContext" | grep -v "ctx.user"
```

**RLSチェック:**
```bash
# ctx.issuer なしの直接Prismaクエリを検索
grep -n "prismaClient\."
grep -n "prisma\." | grep -v "ctx.issuer"
```

**センシティブデータのログ出力:**
```bash
# パスワードやトークンのログ出力を検索
grep -n "logger.*password"
grep -n "logger.*token"
grep -n "logger.*apiKey"
grep -n "logger.*secret"
grep -n "console.log.*password"
```

**$queryRawUnsafe の使用:**
```bash
# 危険なクエリメソッドを検索
grep -n '\$queryRawUnsafe'
grep -n '\$executeRawUnsafe'
```

**ハードコードされたシークレット:**
```bash
# APIキーやシークレットのハードコードを検索
grep -n "sk_live_"
grep -n "sk_test_"
grep -n "AIza"  # Google API Key
grep -n "AKIA"  # AWS Access Key
```

---

### ステップ3: レポート生成

構造化されたレポートを生成:

```markdown
# セキュリティレビューレポート

## サマリー
- 分析ファイル数: X
- 検出された問題: Y
- 重大な問題: Z
- 警告: W

## 重大な問題（Critical）

### 認証バイパス
- [ ] **ファイル**: `src/application/domain/user/service.ts:45`
  - **問題**: 認証チェックなしでセンシティブな操作を実行
  - **リスク**: 未認証ユーザーがデータを操作可能
  - **修正**: UseCaseで `ctx.user` をチェックし、認証エラーをthrow

### RLSバイパス
- [ ] **ファイル**: `src/application/domain/community/data/repository.ts:78`
  - **問題**: `ctx.issuer` なしの直接Prismaクエリ
  - **リスク**: コミュニティ分離が機能せず、他のコミュニティのデータにアクセス可能
  - **修正**: クエリを `ctx.issuer.public(ctx, tx => ...)` でラップ

### センシティブデータの漏洩
- [ ] **ファイル**: `src/application/domain/auth/service.ts:120`
  - **問題**: パスワードがログに出力されている
  - **リスク**: ログからパスワードが漏洩
  - **修正**: ログからパスワードを除外

## 警告（Warning）

### 入力バリデーション不足
- [ ] **ファイル**: `src/application/domain/opportunity/service.ts:56`
  - **問題**: title の長さチェックがない
  - **リスク**: 極端に長い文字列でデータベース負荷
  - **修正**: 文字列長の制限を追加（1-200文字）

### $queryRaw の使用
- [ ] **ファイル**: `src/application/domain/analytics/repository.ts:89`
  - **問題**: `$queryRaw` を使用（パラメータ化は確認済み）
  - **リスク**: 将来的な変更でSQLインジェクションの可能性
  - **修正**: 可能であればPrismaのタイプセーフメソッドを使用

## 推奨事項

1. 全てのRepositoryで `ctx.issuer` メソッドを使用していることを再確認
2. センシティブデータのログ出力を定期的にスキャン
3. 本番環境のシークレットが適切に管理されていることを確認
4. 定期的なセキュリティ監査の実施を検討
```

---

## セキュリティベストプラクティス

### 開発時

- ✅ **最小権限の原則** を適用（必要な権限のみを付与）
- ✅ **デフォルトで拒否** の方針（明示的に許可されたもののみアクセス可能）
- ✅ **多層防御** を実装（認証、認可、バリデーション）
- ✅ **セキュアコーディング** を実践（入力検証、出力エスケープ）

### レビュー時

- ✅ 認証・認可の実装を **必ず確認**
- ✅ センシティブデータの取り扱いを **慎重にレビュー**
- ✅ 外部入力は **信頼しない** 前提でバリデーション
- ✅ エラーメッセージに **機密情報を含めない**

### デプロイ時

- ✅ 本番環境のシークレットを **別管理**
- ✅ HTTPSを **必ず使用**
- ✅ セキュリティヘッダーを **適切に設定**
- ✅ ログを **定期的に監視**

---

## OWASP Top 10 対策

| 脆弱性 | 対策 | 状態 |
|-------|------|------|
| **A01:2021 Broken Access Control** | RLS（ctx.issuer）の徹底使用 | ✅ 実装済み |
| **A02:2021 Cryptographic Failures** | Firebase Auth、HTTPS、env管理 | ✅ 実装済み |
| **A03:2021 Injection** | Prismaのパラメータ化クエリ | ✅ 実装済み |
| **A04:2021 Insecure Design** | DDD/Clean Architecture | ✅ 実装済み |
| **A05:2021 Security Misconfiguration** | 環境変数、CORS設定 | ✅ 実装済み |
| **A06:2021 Vulnerable Components** | 定期的な依存関係更新 | ⚠️  要監視 |
| **A07:2021 Auth Failures** | Firebase Auth、セッション管理 | ✅ 実装済み |
| **A08:2021 Data Integrity** | トランザクション、RLS | ✅ 実装済み |
| **A09:2021 Logging Failures** | ログ監視、センシティブデータ除外 | ✅ 実装済み |
| **A10:2021 SSRF** | 外部API呼び出しの制限 | ⚠️  要確認 |

---

## 参考資料

以下については `@CLAUDE.md` を参照してください:
- 認証・認可の実装
- Row-Level Security (RLS)
- 環境変数の管理
- セキュリティベストプラクティス
