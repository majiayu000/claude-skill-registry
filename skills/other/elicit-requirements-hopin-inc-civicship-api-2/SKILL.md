---
name: elicit-requirements
description: 要件定義を支援
user-invocable: true
argument-hint: [機能名または概要]
allowed-tools: Read, Grep, Bash
context: fork
---

# civicship-api 要件定義支援

新機能の要件を**段階的に引き出し**、既存システムとの整合性を考慮した**仕様書形式**でまとめます。要件の曖昧さを排除し、実装可能な形に落とし込みます。

## 使用方法

```bash
# 機能概要を指定して要件ヒアリングを開始
/elicit-requirements ポイント有効期限機能

# 既存Issueから要件を抽出
/elicit-requirements #123
```

**引数:**
- `$ARGUMENTS`: 機能名、概要、またはIssue番号

---

## 要件定義プロセス

### ステップ1: 初期ヒアリング（5W1H）

ユーザーから提供された情報を基に、以下の観点で質問を生成:

#### **Why（なぜ）- ビジネス価値**
```markdown
## この機能が必要な理由

- ビジネス上の課題は何ですか？
- 誰のためのものですか？（エンドユーザー、管理者、運営者）
- 現状の何が不便ですか？
- この機能で解決できることは何ですか？
- 優先度はどれくらいですか？（高/中/低）
```

#### **What（何を）- 機能概要**
```markdown
## 実現したい機能

- 具体的に何をする機能ですか？
- どのような操作を提供しますか？
- ユーザーに見える変化は何ですか？
- 既存の機能との関係は？（拡張、置き換え、新規）
```

#### **Who（誰が）- ユーザー・権限**
```markdown
## 利用者と権限

- この機能を使うのは誰ですか？
  - [ ] 一般ユーザー（User）
  - [ ] コミュニティマネージャー（Manager）
  - [ ] 管理者（Admin）
  - [ ] システム（自動処理）
  - [ ] 外部サービス（LINE、Firebase）

- 認証は必要ですか？
- 権限チェックは必要ですか？
- RLS（Row-Level Security）の範囲は？
  - [ ] public（全ユーザー）
  - [ ] onlyBelongingCommunity（所属コミュニティのみ）
  - [ ] internal（管理者のみ）
```

#### **When（いつ）- タイミング・トリガー**
```markdown
## 実行タイミング

- いつ実行されますか？
  - [ ] ユーザー操作時（GraphQL Mutation）
  - [ ] 定期実行（Cron）
  - [ ] イベント駆動（Webhook、Pub/Sub）
  - [ ] バッチ処理

- 実行頻度は？
- タイムアウト要件は？
```

#### **Where（どこで）- 適用範囲**
```markdown
## 適用範囲

- どのドメインに影響しますか？
  - [ ] account（User, Community, Membership, Wallet）
  - [ ] experience（Opportunity, Reservation, Participation）
  - [ ] reward（Utility, Ticket）
  - [ ] transaction（Point Transfer）
  - [ ] notification（LINE Messaging）
  - [ ] content（Article, Image）
  - [ ] location（Place, City, State）

- 対象データの範囲は？
  - 全コミュニティ？ 特定コミュニティのみ？
  - 全ユーザー？ 特定条件のユーザーのみ？
```

#### **How（どのように）- 実現方法**
```markdown
## 技術的な実現方法

- どのレイヤーで実装しますか？
  - [ ] GraphQL API（Query/Mutation）
  - [ ] 内部Service（他ドメインから呼び出し）
  - [ ] バッチ処理（Firebase Functions）
  - [ ] Webhook（外部サービス連携）

- データの永続化は必要ですか？
  - [ ] 新しいテーブル作成
  - [ ] 既存テーブルへのカラム追加
  - [ ] 既存テーブルの変更のみ

- トランザクション要件は？
  - [ ] 単一操作（単純なCRUD）
  - [ ] 複数テーブル更新（トランザクション必須）
  - [ ] 分散トランザクション（複数ドメイン）
```

---

### ステップ2: 既存システムの調査

要件ヒアリング結果を基に、関連する既存実装を調査:

#### **関連ドメインの特定**

```bash
# 関連ドメインのディレクトリを検索
ls -la src/application/domain/

# 関連するGraphQLスキーマを検索
find src/application/domain -name "*.graphql" -path "*/${RELATED_DOMAIN}/*"

# 関連するモデルをPrismaスキーマで確認
grep -A 20 "model t_${TABLE_NAME}" prisma/schema.prisma
```

#### **類似機能の調査**

```bash
# 類似のUseCase実装を検索
find src/application/domain -name "usecase.ts" -path "*/${RELATED_DOMAIN}/*"

# 類似のService実装を検索
find src/application/domain -name "service.ts" -path "*/${RELATED_DOMAIN}/*"

# 類似のGraphQL Mutationを検索
grep -r "mutation.*Create\|mutation.*Update" src/application/domain --include="*.graphql"
```

#### **既存の制約・ルールの確認**

```markdown
## 既存システムの制約

以下のファイルから関連するビジネスルールを抽出:

- **認証ルール**: `src/presentation/graphql/rule.ts`
- **RLSパターン**: 関連ドメインの `data/repository.ts`
- **バリデーション**: 関連ドメインの `service.ts`
- **トランザクションパターン**: 関連ドメインの `usecase.ts`
```

---

### ステップ3: 受け入れ条件の定義

**Given-When-Then** 形式で受け入れ条件を明確化:

```markdown
## 受け入れ条件

### シナリオ1: [正常系の説明]

**Given（前提条件）:**
- ユーザーがコミュニティに所属している
- ウォレットに十分なポイントがある
- [その他の前提条件]

**When（操作）:**
- GraphQL Mutation `xxxCreate` を実行
- 入力パラメータ: `{ field1: "value1", field2: 100 }`

**Then（期待結果）:**
- データベースに新しいレコードが作成される
- ポイントが減算される
- LINE通知が送信される
- GraphQLレスポンスが返る: `{ id, field1, field2, createdAt }`

---

### シナリオ2: [異常系の説明]

**Given（前提条件）:**
- ユーザーがコミュニティに所属していない

**When（操作）:**
- GraphQL Mutation `xxxCreate` を実行

**Then（期待結果）:**
- エラーが返る: `PERMISSION_DENIED`
- データベースは変更されない
- トランザクションがロールバックされる

---

### シナリオ3: [境界値の説明]

**Given（前提条件）:**
- ウォレットのポイントが0

**When（操作）:**
- 1ポイント使用する操作を実行

**Then（期待結果）:**
- エラーが返る: `INSUFFICIENT_POINTS`
- データベースは変更されない
```

---

### ステップ4: データモデルの設計

Prismaスキーマの変更が必要な場合、設計案を提示:

```markdown
## データモデル設計

### オプションA: 新規テーブル作成

\`\`\`prisma
model t_xxx {
  id          String   @id @default(cuid())
  userId      String
  communityId String
  // 新しいフィールド
  fieldName   String
  status      XxxStatus @default(ACTIVE)

  // リレーション
  user        t_users       @relation(fields: [userId], references: [id], onDelete: Cascade)
  community   t_communities @relation(fields: [communityId], references: [id], onDelete: Cascade)

  // タイムスタンプ
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  // インデックス
  @@index([userId])
  @@index([communityId])
  @@index([status])
  @@map("t_xxx")
}

enum XxxStatus {
  ACTIVE
  INACTIVE
  EXPIRED
}
\`\`\`

**マイグレーション名:** `add_xxx_table`

---

### オプションB: 既存テーブルへのカラム追加

\`\`\`prisma
model t_existing {
  // 既存のフィールド
  id        String @id @default(cuid())

  // 追加フィールド
  newField  String?
  newStatus XxxStatus? @default(ACTIVE)

  // ...
}
\`\`\`

**マイグレーション名:** `add_existing_new_field`

**注意:** 既存データへの影響を確認すること
```

---

### ステップ5: GraphQLスキーマ設計

GraphQL型、Query、Mutationの設計案を提示:

```markdown
## GraphQLスキーマ設計

### 型定義（type.graphql）

\`\`\`graphql
"""
[機能の説明]
"""
type GqlXxx {
  """ID"""
  id: ID!

  """フィールドの説明"""
  fieldName: String!

  """ステータス"""
  status: GqlXxxStatus!

  """所属コミュニティ"""
  community: GqlCommunity!

  """作成日時"""
  createdAt: DateTime!

  """更新日時"""
  updatedAt: DateTime!
}

"""ステータス"""
enum GqlXxxStatus {
  """有効"""
  ACTIVE

  """無効"""
  INACTIVE

  """期限切れ"""
  EXPIRED
}

"""作成入力"""
input GqlXxxCreateInput {
  """フィールドの説明"""
  fieldName: String!

  """その他のフィールド"""
  otherField: Int!
}

"""作成結果"""
type GqlXxxCreatePayload {
  """作成されたXxx"""
  xxx: GqlXxx!
}

"""更新入力"""
input GqlXxxUpdateInput {
  """ID"""
  id: ID!

  """フィールドの説明（オプショナル）"""
  fieldName: String
}

"""更新結果"""
type GqlXxxUpdatePayload {
  """更新されたXxx"""
  xxx: GqlXxx!
}
\`\`\`

---

### Query定義（query.graphql）

\`\`\`graphql
extend type Query {
  """
  Xxx一覧を取得
  """
  xxxList(
    """コミュニティID"""
    communityId: ID!

    """ステータスフィルタ"""
    status: GqlXxxStatus

    """ページネーション用カーソル"""
    cursor: ID

    """取得件数（デフォルト: 20）"""
    limit: Int
  ): GqlXxxConnection!

  """
  Xxx詳細を取得
  """
  xxx(
    """ID"""
    id: ID!
  ): GqlXxx
}

"""ページネーション結果"""
type GqlXxxConnection {
  """Xxxリスト"""
  nodes: [GqlXxx!]!

  """次ページのカーソル"""
  cursor: ID

  """次ページが存在するか"""
  hasMore: Boolean!
}
\`\`\`

---

### Mutation定義（mutation.graphql）

\`\`\`graphql
extend type Mutation {
  """
  Xxxを作成（マネージャー権限）
  """
  xxxCreate(
    """入力パラメータ"""
    input: GqlXxxCreateInput!

    """権限情報"""
    permission: GqlPermission!
  ): GqlXxxCreatePayload!

  """
  Xxxを更新（マネージャー権限）
  """
  xxxUpdate(
    """入力パラメータ"""
    input: GqlXxxUpdateInput!

    """権限情報"""
    permission: GqlPermission!
  ): GqlXxxUpdatePayload!

  """
  Xxxを削除（マネージャー権限）
  """
  xxxDelete(
    """ID"""
    id: ID!

    """権限情報"""
    permission: GqlPermission!
  ): GqlXxxDeletePayload!
}

"""削除結果"""
type GqlXxxDeletePayload {
  """削除されたID"""
  id: ID!
}
\`\`\`
```

---

### ステップ6: アーキテクチャ設計

DDD/Clean Architectureに従った実装方針を提示:

```markdown
## アーキテクチャ設計

### ドメイン配置

**新規ドメイン作成が必要な場合:**

\`\`\`
src/application/domain/{category}/{domain-name}/
├── controller/
│   ├── resolver.ts         # GraphQL Resolver
│   └── dataloader.ts       # N+1防止
├── usecase.ts             # トランザクション管理
├── service.ts             # ビジネスロジック
├── data/
│   ├── repository.ts      # Prismaクエリ
│   ├── interface.ts       # Repository契約
│   ├── converter.ts       # 入力変換
│   └── type.ts            # 型定義
├── presenter.ts           # レスポンスフォーマット
└── schema/
    ├── query.graphql
    ├── mutation.graphql
    └── type.graphql
\`\`\`

**カテゴリ選択:**
- `account` - ユーザー、コミュニティ、ウォレット関連
- `experience` - 体験、予約、参加関連
- `reward` - ポイント、チケット、特典関連
- `transaction` - ポイント送受信関連
- `notification` - 通知関連
- `content` - コンテンツ関連
- `location` - 地理情報関連

---

### レイヤー責任分担

#### **Resolver（controller/resolver.ts）**

\`\`\`typescript
@injectable()
export default class XxxResolver {
  constructor(
    @inject("XxxUseCase") private usecase: XxxUseCase
  ) {}

  Query = {
    xxxList: async (_, args, ctx) => {
      return this.usecase.listXxx(args, ctx);
    },

    xxx: async (_, { id }, ctx) => {
      return this.usecase.getXxx(id, ctx);
    }
  };

  Mutation = {
    xxxCreate: async (_, { input, permission }, ctx) => {
      return this.usecase.managerCreateXxx({ input, permission }, ctx);
    }
  };

  Xxx = {
    community: (parent, _, ctx) => ctx.loaders.community.load(parent.communityId)
  };
}
\`\`\`

**責任:** UseCaseを呼ぶだけ、ビジネスロジックなし

---

#### **UseCase（usecase.ts）**

\`\`\`typescript
@injectable()
export default class XxxUseCase {
  constructor(
    @inject("XxxService") private service: XxxService,
    @inject("WalletService") private walletService: WalletService
  ) {}

  async managerCreateXxx({ input, permission }, ctx: IContext) {
    // トランザクション管理（UseCaseの責務）
    return ctx.issuer.onlyBelongingCommunity(ctx, async (tx) => {
      // 1. Xxxを作成
      const xxx = await this.service.createXxx(ctx, input, permission.communityId, tx);

      // 2. ポイント減算（他ドメインのServiceを呼ぶ）
      if (input.pointCost > 0) {
        await this.walletService.transferPoints(ctx, {
          fromUserId: ctx.userId,
          toUserId: permission.communityId,
          points: input.pointCost
        }, tx);
      }

      // 3. Presenterでフォーマット
      return XxxPresenter.create(xxx);
    });
  }
}
\`\`\`

**責任:** フロー制御、トランザクション管理、他ドメインServiceの呼び出し

---

#### **Service（service.ts）**

\`\`\`typescript
@injectable()
export default class XxxService {
  constructor(
    @inject("XxxRepository") private repo: IXxxRepository,
    @inject("XxxConverter") private converter: XxxConverter
  ) {}

  async createXxx(
    ctx: IContext,
    input: GqlXxxCreateInput,
    communityId: string,
    tx: Prisma.TransactionClient
  ): Promise<PrismaXxx> {
    // 1. バリデーション
    if (input.fieldName.length === 0) {
      throw new Error("INVALID_INPUT");
    }

    // 2. ビジネスルール
    const existingCount = await this.repo.countByCommunity(ctx, communityId, tx);
    if (existingCount >= 100) {
      throw new Error("MAX_LIMIT_REACHED");
    }

    // 3. 入力変換
    const data = this.converter.toCreateData(input, communityId);

    // 4. Repository呼び出し（txを渡す）
    return await this.repo.create(ctx, data, tx);
  }
}
\`\`\`

**責任:** ビジネスロジック、バリデーション、txの伝播（分岐なし）

---

#### **Repository（data/repository.ts）**

\`\`\`typescript
@injectable()
export default class XxxRepository implements IXxxRepository {
  async create(
    ctx: IContext,
    data: Prisma.t_xxxCreateInput,
    tx: Prisma.TransactionClient
  ): Promise<PrismaXxx> {
    // txは必須（Mutationのため）
    return tx.t_xxx.create({
      data,
      select: xxxSelect
    });
  }

  async findById(
    ctx: IContext,
    id: string,
    tx?: Prisma.TransactionClient
  ): Promise<PrismaXxx | null> {
    // txはオプショナル（Queryのため）
    if (tx) {
      return tx.t_xxx.findUnique({
        where: { id },
        select: xxxSelect
      });
    }

    return ctx.issuer.public(ctx, (tx) =>
      tx.t_xxx.findUnique({
        where: { id },
        select: xxxSelect
      })
    );
  }
}
\`\`\`

**責任:** Prismaクエリ、RLS、txの分岐処理（Queryのみ）

---

#### **Converter（data/converter.ts）**

\`\`\`typescript
@injectable()
export default class XxxConverter {
  toCreateData(
    input: GqlXxxCreateInput,
    communityId: string
  ): Prisma.t_xxxCreateInput {
    return {
      id: cuid(),
      communityId,
      fieldName: input.fieldName,
      status: "ACTIVE",
      createdAt: new Date(),
      updatedAt: new Date()
    };
  }
}
\`\`\`

**責任:** GraphQL入力 → Prisma形式、純粋関数（副作用なし）

---

#### **Presenter（presenter.ts）**

\`\`\`typescript
export default class XxxPresenter {
  static create(xxx: PrismaXxx): GqlXxxCreatePayload {
    return {
      xxx: this.toGraphQL(xxx)
    };
  }

  static toGraphQL(xxx: PrismaXxx): GqlXxx {
    return {
      id: xxx.id,
      fieldName: xxx.fieldName,
      status: xxx.status,
      communityId: xxx.communityId,
      createdAt: xxx.createdAt,
      updatedAt: xxx.updatedAt
    };
  }
}
\`\`\`

**責任:** Prisma型 → GraphQL型、純粋関数（ビジネスロジックなし）
```

---

### ステップ7: テスト戦略

テストケースの設計:

```markdown
## テスト戦略

### ユニットテスト（Service層）

**ファイル:** `__tests__/unit/{domain}/service.test.ts`

\`\`\`typescript
describe("XxxService", () => {
  let service: XxxService;
  let mockRepo: jest.Mocked<IXxxRepository>;
  let mockConverter: jest.Mocked<XxxConverter>;

  beforeEach(() => {
    mockRepo = {
      create: jest.fn(),
      findById: jest.fn(),
      countByCommunity: jest.fn()
    } as any;

    mockConverter = {
      toCreateData: jest.fn()
    } as any;

    service = new XxxService(mockRepo, mockConverter);
  });

  describe("createXxx", () => {
    it("正常系: Xxxを作成できる", async () => {
      const input: GqlXxxCreateInput = { fieldName: "test" };
      const communityId = "community-id";
      const tx = mockTransaction();

      mockConverter.toCreateData.mockReturnValue(mockData);
      mockRepo.create.mockResolvedValue(mockXxx);
      mockRepo.countByCommunity.mockResolvedValue(0);

      const result = await service.createXxx(ctx, input, communityId, tx);

      expect(result).toEqual(mockXxx);
      expect(mockRepo.create).toHaveBeenCalledWith(ctx, mockData, tx);
    });

    it("異常系: 上限に達している場合エラー", async () => {
      mockRepo.countByCommunity.mockResolvedValue(100);

      await expect(
        service.createXxx(ctx, input, communityId, tx)
      ).rejects.toThrow("MAX_LIMIT_REACHED");
    });
  });
});
\`\`\`

---

### 統合テスト（UseCase層）

**ファイル:** `__tests__/integration/{domain}/usecase.test.ts`

\`\`\`typescript
describe("XxxUseCase Integration", () => {
  let usecase: XxxUseCase;
  let ctx: IContext;

  beforeEach(async () => {
    usecase = container.resolve(XxxUseCase);
    ctx = await createTestContext();
  });

  afterEach(async () => {
    await cleanupTestData();
  });

  it("managerCreateXxx: トランザクション内でXxxを作成", async () => {
    const input: GqlXxxCreateInput = { fieldName: "test" };
    const permission = { communityId: "community-id" };

    const result = await usecase.managerCreateXxx({ input, permission }, ctx);

    expect(result.xxx).toBeDefined();
    expect(result.xxx.fieldName).toBe("test");

    // データベースで確認
    const saved = await prisma.t_xxx.findUnique({ where: { id: result.xxx.id } });
    expect(saved).toBeDefined();
  });
});
\`\`\`

---

### E2Eテスト（GraphQL API）

**ファイル:** `__tests__/e2e/{domain}/graphql.test.ts`

\`\`\`typescript
describe("Xxx GraphQL API", () => {
  let server: ApolloServer;
  let token: string;

  beforeAll(async () => {
    server = await createTestServer();
    token = await generateTestToken({ role: "manager" });
  });

  it("xxxCreate: GraphQL経由でXxxを作成", async () => {
    const mutation = \`
      mutation {
        xxxCreate(
          input: { fieldName: "test" }
          permission: { communityId: "community-id" }
        ) {
          xxx {
            id
            fieldName
            status
          }
        }
      }
    \`;

    const response = await server.executeOperation(
      { query: mutation },
      { req: { headers: { authorization: \`Bearer \${token}\` } } }
    );

    expect(response.data?.xxxCreate.xxx).toBeDefined();
    expect(response.data?.xxxCreate.xxx.fieldName).toBe("test");
  });
});
\`\`\`

---

### テストカバレッジ目標

| レイヤー | 目標カバレッジ |
|---------|---------------|
| Service | 90%以上 |
| UseCase | 85%以上 |
| Converter | 95%以上 |
| Presenter | 95%以上 |
| Repository | 80%以上（統合テストでカバー） |
| Resolver | 70%以上（E2Eテストでカバー） |
```

---

### ステップ8: 非機能要件の確認

パフォーマンス、セキュリティ、運用面の要件を確認:

```markdown
## 非機能要件

### パフォーマンス

- [ ] **レスポンスタイム目標:** 〇〇ms以内
- [ ] **想定同時実行数:** 〇〇リクエスト/秒
- [ ] **N+1問題対策:** DataLoaderを使用
- [ ] **ページネーション:** カーソルベース（大量データ対応）
- [ ] **インデックス:** 頻繁にクエリされるカラムに追加

### セキュリティ

- [ ] **認証:** Firebase Auth必須
- [ ] **認可:** RLS（ctx.issuer）を使用
- [ ] **入力バリデーション:** Service層で実施
- [ ] **SQLインジェクション対策:** Prismaが自動対応
- [ ] **センシティブデータ:** ログに出力しない
- [ ] **レート制限:** 必要に応じて設定

### 運用

- [ ] **監視:** エラーログをFirebase Crashlyticsに送信
- [ ] **アラート:** 〇〇以上のエラー率で通知
- [ ] **バックアップ:** データベース定期バックアップ
- [ ] **ロールバック計画:** マイグレーション失敗時の手順
- [ ] **ドキュメント:** README、CHANGELOG更新

### スケーラビリティ

- [ ] **データ増加への対応:** パーティショニング、アーカイブ戦略
- [ ] **コミュニティ数の増加:** 水平スケーリング可能か
- [ ] **外部API制限:** レート制限、リトライロジック
```

---

### ステップ9: 依存関係と制約の整理

実装時の依存関係と制約を明確化:

```markdown
## 依存関係

### 他ドメインへの依存

- **WalletService** - ポイント減算
- **NotificationService** - LINE通知送信
- **ImageService** - 画像アップロード
- **CommunityService** - コミュニティ情報取得

### 外部サービスへの依存

- **Firebase Auth** - 認証トークン検証
- **Google Cloud Storage** - 画像保存
- **LINE Messaging API** - 通知配信

### データベース制約

- **外部キー:** t_communities, t_users
- **ユニーク制約:** (communityId, fieldName) の組み合わせ
- **NOT NULL制約:** fieldName, status

---

## 技術的制約

- **TypeScript:** 型安全性を保つ
- **Prisma ORM:** 生SQLは原則禁止
- **GraphQL命名規則:** 型は `Gql*` プレフィックス
- **テーブル命名規則:** `t_*` プレフィックス
- **トランザクション:** UseCaseで管理、Serviceに伝播
- **RLS:** 全てのクエリで `ctx.issuer` を使用
```

---

### ステップ10: 要件定義書の生成

全ての情報を統合し、実装可能な形の要件定義書を出力:

```markdown
# 要件定義書: [機能名]

**作成日:** YYYY-MM-DD
**ステータス:** Draft / Review / Approved
**優先度:** High / Medium / Low

---

## 1. 概要

### 1.1 背景・目的

[ビジネス課題と解決したいこと]

### 1.2 スコープ

**対象:**
- [含まれるもの]

**対象外:**
- [含まれないもの]

---

## 2. 機能要件

### 2.1 ユーザーストーリー

**As a** [ユーザーロール]
**I want to** [やりたいこと]
**So that** [達成したい目的]

### 2.2 受け入れ条件

[Given-When-Thenシナリオ]

### 2.3 画面/API仕様

[GraphQLスキーマ設計]

---

## 3. データ設計

### 3.1 データモデル

[Prismaスキーマ設計]

### 3.2 マイグレーション計画

**マイグレーション名:** `add_xxx_table`

**影響範囲:**
- 新規テーブル作成
- 既存データへの影響: なし

---

## 4. アーキテクチャ設計

### 4.1 ドメイン配置

[ディレクトリ構造]

### 4.2 レイヤー責任

[Resolver、UseCase、Service、Repositoryの役割]

---

## 5. 非機能要件

### 5.1 パフォーマンス

[レスポンスタイム、スループット]

### 5.2 セキュリティ

[認証、認可、バリデーション]

### 5.3 運用

[監視、アラート、バックアップ]

---

## 6. テスト計画

### 6.1 テストケース

[ユニット、統合、E2Eテストのケース]

### 6.2 カバレッジ目標

[レイヤー別の目標カバレッジ]

---

## 7. 実装計画

### 7.1 タスク分解

- [ ] Prismaスキーマ変更
- [ ] マイグレーション実行
- [ ] GraphQLスキーマ定義
- [ ] ドメイン実装（Resolver、UseCase、Service、Repository）
- [ ] テスト実装
- [ ] ドキュメント更新

### 7.2 見積もり

**実装工数:** 〇〇日
**テスト工数:** 〇〇日
**総工数:** 〇〇日

---

## 8. リスクと対策

| リスク | 影響度 | 発生確率 | 対策 |
|--------|--------|----------|------|
| [リスク1] | High/Medium/Low | High/Medium/Low | [対策] |

---

## 9. 依存関係

### 9.1 他機能への依存

[依存する既存機能]

### 9.2 他機能への影響

[この機能が影響を与える既存機能]

---

## 10. 承認

**レビュー担当者:**
- [ ] プロダクトオーナー
- [ ] テックリード
- [ ] セキュリティ担当

**承認日:** YYYY-MM-DD
```

---

## 活用例

### 例1: ポイント有効期限機能

```bash
/elicit-requirements ポイント有効期限機能
```

**期待される質問:**
- ポイント有効期限はどのタイミングで設定しますか？（付与時、一律設定）
- 有効期限切れのポイントはどうなりますか？（自動失効、通知あり）
- 既存のポイントに対する影響は？（遡及適用、新規のみ）

**生成される要件定義:**
- データモデル: `t_wallets` に `expiresAt` カラム追加
- GraphQLスキーマ: `GqlWallet` に `expiresAt` フィールド追加
- バッチ処理: 有効期限切れポイントの自動失効
- 通知: 有効期限7日前にLINE通知

---

### 例2: スキルマッチング機能

```bash
/elicit-requirements スキルマッチング機能
```

**期待される質問:**
- ユーザーのスキルはどう登録しますか？（タグ形式、階層構造）
- マッチングアルゴリズムは？（完全一致、類似度スコア）
- どの画面で使いますか？（Opportunity一覧、推薦）

**生成される要件定義:**
- データモデル: `t_user_skills`, `t_opportunity_skills` テーブル追加
- GraphQLスキーマ: `GqlSkill` 型、`skillMatch` Query追加
- アルゴリズム: スキルタグの部分一致スコアリング

---

## 注意事項

### 要件定義の原則

- ✅ **具体的に:** 曖昧な表現を避ける
- ✅ **測定可能に:** 受け入れ条件を明確にする
- ✅ **実現可能に:** 既存システムとの整合性を確認
- ✅ **関連性を保つ:** ビジネス価値と紐づける
- ✅ **期限を設定:** 優先度とスケジュールを決める

### よくある落とし穴

- ❌ **要件が曖昧:** 「柔軟に」「適切に」などの抽象表現
- ❌ **実装詳細の混入:** 要件定義で技術選定しない
- ❌ **スコープクリープ:** 途中で要件を追加しない
- ❌ **既存システム無視:** 互換性を考慮しない

---

## 参考資料

以下については `@CLAUDE.md` を参照してください:
- アーキテクチャパターン
- トランザクション管理
- RLSの使い方
- GraphQL命名規則
