---
name: db-migration
description: DBマイグレーション支援
user-invocable: true
allowed-tools: Read, Grep, Bash
---

# civicship-api データベースマイグレーションガイド

Prismaスキーマ変更、マイグレーション作成、型生成をプロジェクトのベストプラクティスに従って安全にガイドします。

## 使用方法

```bash
# マイグレーションワークフローを実行
/db-migration

# マイグレーションステータスのみをチェック
/db-migration status
```

---

## マイグレーションワークフロー

### ステップ1: スキーマ変更の検出

`prisma/schema.prisma` に未コミット変更があるかチェック:

```bash
git status --porcelain prisma/schema.prisma
```

**変更なしの場合:**
- メッセージ表示: "スキーマ変更は検出されませんでした"
- 保留中のマイグレーションをチェック

**変更が検出された場合:**
- diffを表示: `git diff prisma/schema.prisma`
- 検証へ進む

---

### ステップ2: スキーマ変更の検証

スキーマ変更を読み取り、一般的な問題を分析:

**チェック項目:**

1. **破壊的変更**
   - データマイグレーションなしでのカラム削除
   - カラム型の変更（データ損失の可能性）
   - 外部キー依存関係のあるテーブルの削除
   - プライマリキーの変更

2. **制約の欠落**
   - インデックスのない外部キー
   - nullable フィールドに対するユニーク制約
   - non-nullable フィールドへの @default の欠落

3. **命名規則**
   - テーブル名: snake_case（例: `t_users`, `t_opportunities`）
   - カラム名: camelCase（例: `createdAt`, `updatedAt`）
   - Enum名: PascalCase（例: `UserStatus`, `PublishStatus`）

4. **Row-Level Security (RLS)**
   - テーブルは `t_` プレフィックスを持つべき（例: `t_users`）
   - RLSポリシーの更新が必要かチェック

5. **インデックス**
   - 外部キーにはインデックスがあるべき
   - 頻繁にクエリされるカラムにインデックスを追加
   - 複数カラムクエリには複合インデックスを検討

**検証結果を表示:**

```markdown
## スキーマ検証

✅ 破壊的変更は検出されませんでした
✅ 命名規則に従っています
⚠️  外部キーにインデックスがありません: `t_reservations` の `opportunityId`
⚠️  `t_participations` の `status` フィールドに @default の追加を検討してください
```

---

### ステップ3: マイグレーション名の生成

規約に従った説明的なマイグレーション名を提案:

**フォーマット:** `{action}_{subject}_{detail}`

**アクション:**
- `add` - 新しいテーブルまたはカラム
- `update` - 既存構造の変更
- `remove` - テーブルまたはカラムの削除
- `fix` - バグ修正または訂正
- `refactor` - 構造の改善

**例:**
- `add_user_phone_field`
- `update_opportunity_status_enum`
- `remove_deprecated_wallet_type`
- `fix_reservation_foreign_key`
- `refactor_identity_primary_key`

**スキーマdiffを分析して名前を提案:**

```bash
# 新しいテーブルを追加する場合
add_products_table

# フィールドを追加する場合
add_user_email_verified_field

# enumを変更する場合
update_publish_status_enum
```

---

### ステップ4: マイグレーションの作成

**重要: マイグレーションを自動実行しないでください。最初にユーザーの確認を求めてください。**

マイグレーションコマンドを表示し、承認を待機:

```markdown
## マイグレーションコマンド

マイグレーション名 `add_user_phone_field` で作成準備完了

実行コマンド:
\`\`\`bash
pnpm db:migrate add_user_phone_field
\`\`\`

⚠️  **実行前に:**
1. スキーマ変更をもう一度確認
2. 影響を受けるテーブルで開発が行われていないことを確認
3. 本番環境に適用する場合はデータベースをバックアップ

続行しますか？ (yes/no)
```

**ユーザーが確認した場合:**

```bash
pnpm db:migrate add_user_phone_field
```

**期待される出力:**
- `prisma/migrations/` にマイグレーションファイルが作成される
- SQLファイルが生成される

---

### ステップ5: 生成されたSQLのレビュー

生成されたマイグレーションSQLを読み取り、表示:

```bash
# 最新のマイグレーションを見つける
LATEST_MIGRATION=$(ls -t prisma/migrations/ | head -1)

# SQLを表示
cat "prisma/migrations/${LATEST_MIGRATION}/migration.sql"
```

**レビューチェックリスト:**

- ✅ SQL構文が正しい
- ✅ データマイグレーションなしの DROP TABLE がない
- ✅ ALTER TABLE 変更が安全
- ✅ 外部キーに対してインデックスが作成されている
- ✅ デフォルト値が適切

**ユーザーにレビューを依頼:**

```markdown
## 生成されたマイグレーションSQL

\`\`\`sql
[ここにSQLの内容を表示]
\`\`\`

このSQLは正しく見えますか？ (yes/no)
```

---

### ステップ6: Prismaクライアントの生成

マイグレーション作成後、TypeScript型を生成:

```bash
pnpm db:generate
```

**これにより:**
- `@prisma/client` 型が更新される
- TypeScript定義が生成される
- `node_modules/.prisma/client/` が更新される

**生成を確認:**

```bash
# Prismaクライアントが更新されたかチェック
ls -la node_modules/.prisma/client/index.d.ts
```

---

### ステップ7: アプリケーションコードの更新

**更新が必要なアプリケーションコードをチェック:**

1. **Prisma型をインポートしているファイルを検索:**
   ```bash
   grep -r "from '@prisma/client'" src/ --files-with-matches
   ```

2. **Prisma select shapesを持つファイルを検索:**
   ```bash
   grep -r "select.*{" src/application/domain/**/data/type.ts --files-with-matches
   ```

3. **更新が必要な可能性のあるファイルを表示:**

```markdown
## 更新が必要な可能性のあるファイル

以下のファイルはPrisma型をインポートしており、更新が必要な可能性があります:

- src/application/domain/account/user/data/type.ts
- src/application/domain/account/membership/service.ts
- src/application/domain/experience/opportunity/data/repository.ts

これらのファイルで以下を確認してください:
- select shapesの新しいフィールド
- 更新されたenum値
- 変更された型定義
```

---

### ステップ8: TypeScriptコンパイルの確認

型エラーをチェックするためにTypeScriptをコンパイル:

```bash
pnpm build
```

**エラーがある場合:**
- コンパイルエラーを表示
- エラーメッセージに基づいて修正を提案
- 一般的な問題:
  - 型のプロパティの欠落
  - enum値の変更
  - 型の不一致

**成功した場合:**

```markdown
✅ TypeScriptコンパイル成功
✅ 型エラーは検出されませんでした
```

---

### ステップ9: テストの実行

**重要: スキーマ変更後は常にテストを実行してください。**

```bash
pnpm test --runInBand
```

**テストが失敗した場合:**
- 失敗したテストを表示
- 以下をチェックすることを提案:
  - テストフィクスチャ（データの更新が必要な可能性）
  - ファクトリ定義（Prisma Fabbrica）
  - シードデータスクリプト

**テストが成功した場合:**

```markdown
✅ 全てのテストが成功しました
✅ データベーススキーマ変更は既存コードと互換性があります
```

---

### ステップ10: ドキュメントの更新

関連ドキュメントの更新をリマインド:

```markdown
## ドキュメントの更新

以下の更新を検討してください:

- [ ] `docs/database/schema.md` - 新しいテーブル/フィールドをドキュメント化
- [ ] `docs/handbook/FEATURES.md` - 機能ドキュメントを更新
- [ ] GraphQLスキーマコメント - 新しいフィールドの説明を追加
- [ ] `CHANGELOG.md` - マイグレーションをchangelogに追加

Prismaスキーマのコメントは生成された型に自動的に含まれます。
```

---

## マイグレーションのベストプラクティス

### マイグレーション作成前

- ✅ スキーマ変更を慎重にレビュー
- ✅ 破壊的変更をチェック
- ✅ 命名規則に従っていることを確認
- ✅ 適切なインデックスを追加
- ✅ データマイグレーションの必要性を検討

### マイグレーション作成後

- ✅ 生成されたSQLをレビュー
- ✅ `pnpm db:generate` を実行
- ✅ TypeScriptコンパイルエラーを修正
- ✅ `pnpm test --runInBand` でテストを実行
- ✅ 必要に応じてアプリケーションコードを更新
- ✅ ドキュメントを更新

### 本番環境マイグレーション

- ✅ ステージング環境で最初にマイグレーションをテスト
- ✅ 本番データベースをバックアップ
- ✅ 必要に応じてダウンタイムを計画
- ✅ ロールバック計画を用意
- ✅ デプロイ後アプリケーションを監視

---

## 一般的なマイグレーションパターン

### 新しいテーブルの追加

```prisma
model t_products {
  id          String   @id @default(cuid())
  name        String
  price       Int
  communityId String
  community   t_communities @relation(fields: [communityId], references: [id], onDelete: Cascade)
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([communityId])
  @@map("t_products")
}
```

**マイグレーション名:** `add_products_table`

### カラムの追加

```prisma
model t_users {
  // ... 既存のフィールド
  phoneNumber String? // 新しいフィールド
}
```

**マイグレーション名:** `add_user_phone_number_field`

### Enumの更新

```prisma
enum PublishStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
  SCHEDULED  // 新しい値
}
```

**マイグレーション名:** `update_publish_status_enum_add_scheduled`

### インデックスの追加

```prisma
model t_opportunities {
  // ... 既存のフィールド

  @@index([communityId, publishStatus]) // 新しい複合インデックス
}
```

**マイグレーション名:** `add_opportunity_community_status_index`

---

## トラブルシューティング

### マイグレーションが失敗

**エラー:** "Migration failed to apply"

**解決策:**
1. PostgreSQL接続をチェック: `pnpm container:up`
2. `.env` のデータベース認証情報を確認
3. テーブル/カラムが既に存在していないかチェック
4. マイグレーションSQLの構文エラーをレビュー

### 型生成が失敗

**エラー:** "Prisma client generation failed"

**解決策:**
1. Prismaスキーマの構文をチェック: `pnpm prisma format`
2. 全てのリレーションが有効であることを確認
3. 循環依存をチェック
4. 参照される全てのモデルが存在することを確認

### マイグレーション後にテストが失敗

**エラー:** データベースエラーでテストが失敗

**解決策:**
1. 新しいフィールドでテストフィクスチャを更新
2. テストデータベースを再シード: `pnpm db:seed-domain`
3. Prisma Fabブリカファクトリを更新
4. 必須フィールドの欠落をチェック

---

## 参考資料

以下については `@CLAUDE.md` を参照してください:
- データベースコマンド（`pnpm db:*`）
- マイグレーションワークフロー
- Prismaスキーマ規約
- マイグレーション後のテスト
