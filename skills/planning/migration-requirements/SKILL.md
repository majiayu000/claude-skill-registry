---
name: migration-requirements
description: データマイグレーション計画を策定し、安全な移行手順を提示
user-invocable: true
argument-hint: [マイグレーション概要または要件定義書]
allowed-tools: Read, Grep, Glob, Bash
---

# civicship-api データマイグレーション計画

データベーススキーマ変更に伴う**データマイグレーション計画**を策定します。既存データの変換、検証、ロールバック手順を含む安全な移行計画を提示します。

## 使用方法

```bash
# マイグレーション概要から計画策定
/migration-requirements "t_walletsにexpiresAtカラムを追加"

# 要件定義書から計画策定
/migration-requirements docs/requirements/point-expiration.md

# Prismaマイグレーションファイルから計画策定
/migration-requirements prisma/migrations/20260115_add_wallet_expiration/migration.sql
```

**引数:**
- `$ARGUMENTS`: マイグレーション概要、要件定義書、またはマイグレーションファイルパス

---

## マイグレーション計画プロセス

### ステップ1: スキーマ変更の分析

Prismaスキーマの変更内容を分析:

```bash
# Prismaスキーマの差分確認
git diff origin/main -- prisma/schema.prisma

# 既存のマイグレーション一覧
ls -la prisma/migrations/

# 最新のマイグレーション
cat prisma/migrations/*/migration.sql | tail -50
```

**スキーマ変更レポート:**

```markdown
## スキーマ変更の概要

### 変更内容

**変更前:**
\`\`\`prisma
model t_wallets {
  id          String   @id @default(cuid())
  userId      String   @unique
  balance     Int
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}
\`\`\`

**変更後:**
\`\`\`prisma
model t_wallets {
  id          String   @id @default(cuid())
  userId      String   @unique
  balance     Int
  expiresAt   DateTime?  # 新規追加
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}
\`\`\`

---

### 変更の分類

**種別:** カラム追加（nullable）

**詳細:**
- 追加カラム: `expiresAt`
- 型: `DateTime`
- Nullable: ✅ はい
- デフォルト値: なし（null）
- インデックス: 必要（有効期限でのフィルタリング）

---

### DDL（Data Definition Language）

\`\`\`sql
-- Prismaが生成するマイグレーションSQL
ALTER TABLE "t_wallets" ADD COLUMN "expiresAt" TIMESTAMP(3);

-- インデックス追加（パフォーマンス最適化）
CREATE INDEX "idx_wallets_expires_at" ON "t_wallets"("expiresAt");
\`\`\`

**実行時間（推定）:**
- テーブルサイズ: 1,000行
- カラム追加: < 1秒
- インデックス作成: < 5秒
- **合計:** < 10秒
```

---

### ステップ2: 既存データの分析

現在のデータ状況を調査:

```bash
# データ件数
psql $DATABASE_URL -c "SELECT COUNT(*) FROM t_wallets;"

# データサンプル
psql $DATABASE_URL -c "SELECT * FROM t_wallets LIMIT 5;"

# NULL値の確認
psql $DATABASE_URL -c "SELECT COUNT(*) FROM t_wallets WHERE balance IS NULL;"

# データ分布
psql $DATABASE_URL -c "SELECT
  MIN(balance) as min_balance,
  MAX(balance) as max_balance,
  AVG(balance) as avg_balance
FROM t_wallets;"
```

**既存データレポート:**

```markdown
## 既存データの状況

### データ統計

| 項目 | 値 |
|------|-----|
| 総レコード数 | 1,234件 |
| ユーザー数 | 1,234人 |
| 最小残高 | 0pt |
| 最大残高 | 50,000pt |
| 平均残高 | 3,500pt |
| 総ポイント数 | 4,318,900pt |

---

### データ品質

#### NULL値の確認
- `balance IS NULL`: 0件 ✅
- `userId IS NULL`: 0件 ✅
- `createdAt IS NULL`: 0件 ✅

#### ユニーク制約の確認
- `userId` の重複: 0件 ✅

#### 参照整合性の確認
\`\`\`sql
-- 孤立レコード（対応するユーザーが存在しない）
SELECT COUNT(*) FROM t_wallets w
LEFT JOIN t_users u ON w.userId = u.id
WHERE u.id IS NULL;
-- 結果: 0件 ✅
\`\`\`

---

### データ分布

#### 残高の分布
| 範囲 | 件数 | 割合 |
|------|------|------|
| 0pt | 120件 | 9.7% |
| 1-1,000pt | 450件 | 36.5% |
| 1,001-5,000pt | 500件 | 40.5% |
| 5,001-10,000pt | 120件 | 9.7% |
| 10,001pt以上 | 44件 | 3.6% |

#### 作成日の分布
- 最古: 2023-06-20
- 最新: 2026-01-15
- 期間: 2年7ヶ月
```

---

### ステップ3: マイグレーション戦略の決定

データ移行の方針を決定:

```markdown
## マイグレーション戦略

### オプション比較

#### オプションA: 空カラム追加のみ（推奨）

**手順:**
1. `expiresAt` カラムを追加（全て null）
2. アプリケーションで新規ポイント付与時のみ有効期限設定

**メリット:**
- ✅ シンプル、リスク最小
- ✅ ダウンタイムなし
- ✅ ロールバック容易

**デメリット:**
- ❌ 既存ポイントは無期限のまま
- ❌ ユーザー間で不公平感

**実行時間:** < 10秒

---

#### オプションB: 既存データに遡及的に有効期限設定

**手順:**
1. `expiresAt` カラムを追加
2. 既存レコードに有効期限を設定
   - 例: `createdAt + 1年`

**メリット:**
- ✅ 全ポイントで有効期限が統一
- ✅ 公平性

**デメリット:**
- ❌ 既存ユーザーへの影響大
- ❌ 事前通知が必要
- ❌ 法的リスク（利用規約との整合性）

**実行時間:** < 30秒

---

#### オプションC: 段階的移行

**手順:**
1. `expiresAt` カラムを追加（全て null）
2. バックグラウンドで徐々に既存データに設定
   - 1日100件ずつ

**メリット:**
- ✅ データベース負荷分散
- ✅ 問題発生時に停止可能

**デメリット:**
- ❌ 実装が複雑
- ❌ 完了まで時間がかかる

**実行時間:** 12日（1,234件 ÷ 100件/日）

---

### 推奨戦略

**採用:** オプションA（空カラム追加のみ）

**理由:**
1. リスク最小
2. 既存ユーザーへの影響なし
3. 新規ポイントから段階的に適用

**注意点:**
- 利用規約で「新規付与ポイントのみ有効期限適用」を明記
```

---

### ステップ4: マイグレーション手順の策定

詳細な実行手順:

```markdown
## マイグレーション実行手順

### Phase 1: 準備（本番実行の1週間前）

#### Step 1: ステージング環境での検証

\`\`\`bash
# 1. ステージング環境にマイグレーション適用
cd /path/to/civicship-api
pnpm db:migrate

# 2. Prisma Client再生成
pnpm db:generate

# 3. TypeScript型チェック
pnpm tsc --noEmit

# 4. テスト実行
pnpm test

# 5. アプリケーション起動確認
pnpm dev
\`\`\`

**確認項目:**
- [ ] マイグレーション成功
- [ ] 型エラーなし
- [ ] テスト全てパス
- [ ] アプリケーション正常起動

---

#### Step 2: バックアップ戦略の確認

\`\`\`bash
# データベースバックアップ
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# バックアップサイズ確認
ls -lh backup_*.sql

# バックアップの検証（リストア可能か）
psql test_db < backup_20260115_120000.sql
\`\`\`

**確認項目:**
- [ ] バックアップファイル作成
- [ ] バックアップサイズ確認（推定: 50MB）
- [ ] リストア可能確認

---

#### Step 3: ロールバック手順の準備

\`\`\`bash
# ロールバック用SQLを作成
cat > rollback.sql <<'EOF'
-- インデックス削除
DROP INDEX IF EXISTS "idx_wallets_expires_at";

-- カラム削除
ALTER TABLE "t_wallets" DROP COLUMN IF EXISTS "expiresAt";
EOF

# ドライラン（実際には実行しない）
psql $DATABASE_URL --dry-run < rollback.sql
\`\`\`

---

### Phase 2: 本番実行（メンテナンスウィンドウ）

#### 推奨実行タイミング

- **曜日:** 火曜日または水曜日
- **時間帯:** 深夜 2:00-3:00 AM（トラフィック最小）
- **所要時間:** 15分（マイグレーション10秒 + 検証5分 + バッファ）

---

#### Step 1: メンテナンスモード開始

\`\`\`bash
# アプリケーション停止（オプショナル）
# ダウンタイムなしで実行可能だが、安全のため推奨
docker-compose stop api

# メンテナンスページ表示（nginx設定）
# または、Read-onlyモードに切り替え
\`\`\`

**所要時間:** 1分

---

#### Step 2: データベースバックアップ

\`\`\`bash
# 本番データベースのバックアップ
pg_dump $PROD_DATABASE_URL > backup_prod_$(date +%Y%m%d_%H%M%S).sql

# S3にアップロード（長期保存）
aws s3 cp backup_prod_*.sql s3://civicship-backups/
\`\`\`

**所要時間:** 2分

---

#### Step 3: マイグレーション実行

\`\`\`bash
# Prismaマイグレーション実行
pnpm db:deploy

# 実行されるSQL:
# ALTER TABLE "t_wallets" ADD COLUMN "expiresAt" TIMESTAMP(3);
# CREATE INDEX "idx_wallets_expires_at" ON "t_wallets"("expiresAt");
\`\`\`

**所要時間:** 10秒

---

#### Step 4: データ検証

\`\`\`bash
# カラムが追加されたか確認
psql $PROD_DATABASE_URL -c "\d t_wallets"

# インデックスが作成されたか確認
psql $PROD_DATABASE_URL -c "\di idx_wallets_expires_at"

# 既存データが保持されているか確認
psql $PROD_DATABASE_URL -c "SELECT COUNT(*) FROM t_wallets;"
# 期待値: 1,234件（変更なし）

# expiresAt が全て null か確認
psql $PROD_DATABASE_URL -c "SELECT COUNT(*) FROM t_wallets WHERE expiresAt IS NOT NULL;"
# 期待値: 0件
\`\`\`

**所要時間:** 1分

---

#### Step 5: アプリケーション再起動

\`\`\`bash
# Prisma Client再生成
pnpm db:generate

# アプリケーション起動
docker-compose up -d api

# ヘルスチェック
curl https://api.civicship.jp/health

# GraphQLエンドポイント確認
curl -X POST https://api.civicship.jp/graphql \
  -H "Content-Type: application/json" \
  -d '{"query": "{ __schema { types { name } } }"}'
\`\`\`

**所要時間:** 2分

---

#### Step 6: 動作確認

\`\`\`bash
# ウォレット取得のテスト
curl -X POST https://api.civicship.jp/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TEST_TOKEN" \
  -d '{"query": "{ wallet(id: \"wallet-id\") { id balance expiresAt } }"}'

# 期待結果:
# { "data": { "wallet": { "id": "...", "balance": 1000, "expiresAt": null } } }
\`\`\`

**確認項目:**
- [ ] GraphQLクエリが成功
- [ ] `expiresAt` フィールドが返る（null）
- [ ] 既存機能が正常動作

**所要時間:** 3分

---

#### Step 7: メンテナンスモード終了

\`\`\`bash
# メンテナンスページを外す
# または、Read-onlyモードを解除
\`\`\`

**所要時間:** 1分

---

### Phase 3: 事後監視（実行後24時間）

#### 監視項目

\`\`\`bash
# エラーログの確認
tail -f /var/log/civicship-api/error.log | grep -i "wallet"

# データベース接続エラー
tail -f /var/log/civicship-api/db.log

# GraphQLエラー率
# Datadog/Grafanaダッシュボードで確認
\`\`\`

**アラート設定:**
- エラー率 > 1% で警告
- エラー率 > 5% で緊急（ロールバック検討）

---

#### パフォーマンス監視

\`\`\`sql
-- クエリパフォーマンス確認
EXPLAIN ANALYZE SELECT * FROM t_wallets WHERE expiresAt < NOW();

-- インデックスが使用されているか
EXPLAIN SELECT * FROM t_wallets WHERE expiresAt < '2026-12-31';
-- 期待: Index Scan using idx_wallets_expires_at
\`\`\`

**目標:**
- クエリ時間: < 50ms
- インデックス使用率: 100%
```

---

### ステップ5: ロールバック計画

マイグレーション失敗時の対処:

```markdown
## ロールバック計画

### シナリオ1: マイグレーション実行失敗

**状況:**
- `ALTER TABLE` がエラーで失敗
- カラムが追加されていない

**対処:**
\`\`\`bash
# 1. エラーログ確認
tail -100 /var/log/postgresql/postgresql.log

# 2. 原因調査
# - 権限不足
# - ディスク容量不足
# - テーブルロック

# 3. 問題解決後、再実行
pnpm db:deploy
\`\`\`

**所要時間:** 10分

---

### シナリオ2: アプリケーションエラー発生

**状況:**
- マイグレーションは成功
- アプリケーションがエラーを出す

**対処:**

#### 即座のロールバック

\`\`\`bash
# 1. バックアップからリストア
psql $PROD_DATABASE_URL < backup_prod_20260115_020000.sql

# 2. Prisma Client を旧バージョンに
git checkout HEAD~1 -- prisma/schema.prisma
pnpm db:generate

# 3. アプリケーション再起動
docker-compose restart api
\`\`\`

**所要時間:** 5分

**注意:**
- マイグレーション後に書き込まれたデータは失われる
- メンテナンスモード中であれば影響なし

---

#### カラム削除のみ（データ保持）

\`\`\`bash
# カラムのみ削除（データは保持）
psql $PROD_DATABASE_URL <<EOF
DROP INDEX IF EXISTS "idx_wallets_expires_at";
ALTER TABLE "t_wallets" DROP COLUMN "expiresAt";
EOF

# Prisma Client 再生成
git checkout HEAD~1 -- prisma/schema.prisma
pnpm db:generate

# アプリケーション再起動
docker-compose restart api
\`\`\`

**所要時間:** 2分

---

### シナリオ3: パフォーマンス劣化

**状況:**
- マイグレーションは成功
- クエリが遅い

**対処:**

\`\`\`bash
# インデックスの確認
psql $PROD_DATABASE_URL -c "\di idx_wallets_expires_at"

# インデックスが無い場合、作成
psql $PROD_DATABASE_URL -c "CREATE INDEX idx_wallets_expires_at ON t_wallets(expiresAt);"

# インデックスの再構築
psql $PROD_DATABASE_URL -c "REINDEX INDEX idx_wallets_expires_at;"
\`\`\`

**所要時間:** 1分

---

### ロールバック判断基準

以下の条件に該当する場合、ロールバック実施:

- [ ] エラー率 > 5% が10分以上継続
- [ ] データベース接続エラーが頻発
- [ ] クエリタイムアウトが頻発
- [ ] データ不整合が検出された
```

---

### ステップ6: データ検証計画

マイグレーション後のデータ整合性を確認:

```markdown
## データ検証計画

### 自動検証スクリプト

\`\`\`sql
-- 検証1: レコード数が一致
SELECT COUNT(*) FROM t_wallets;
-- 期待: 1,234件（変更前と同じ）

-- 検証2: expiresAt が全て null
SELECT COUNT(*) FROM t_wallets WHERE expiresAt IS NOT NULL;
-- 期待: 0件

-- 検証3: 既存カラムの値が保持されている
SELECT
  COUNT(*) as total,
  COUNT(CASE WHEN balance < 0 THEN 1 END) as invalid_balance,
  COUNT(CASE WHEN userId IS NULL THEN 1 END) as null_user
FROM t_wallets;
-- 期待: total=1234, invalid_balance=0, null_user=0

-- 検証4: ユニーク制約が保持されている
SELECT userId, COUNT(*)
FROM t_wallets
GROUP BY userId
HAVING COUNT(*) > 1;
-- 期待: 0件

-- 検証5: 外部キー制約が保持されている
SELECT COUNT(*) FROM t_wallets w
LEFT JOIN t_users u ON w.userId = u.id
WHERE u.id IS NULL;
-- 期待: 0件
\`\`\`

---

### 手動検証項目

- [ ] GraphQL `wallet` クエリが正常動作
- [ ] ウォレット作成が正常動作
- [ ] ポイント送受信が正常動作
- [ ] 特典交換が正常動作
- [ ] 管理画面でウォレット表示が正常

---

### 検証レポート

\`\`\`markdown
# マイグレーション検証レポート

**実行日時:** 2026-01-15 02:05:00
**実行者:** DevOps Team
**環境:** Production

## 検証結果

| 検証項目 | 結果 | 備考 |
|---------|------|------|
| レコード数一致 | ✅ Pass | 1,234件 |
| expiresAt null確認 | ✅ Pass | 0件 |
| 既存データ保持 | ✅ Pass | 異常なし |
| ユニーク制約 | ✅ Pass | 重複なし |
| 外部キー制約 | ✅ Pass | 孤立レコードなし |
| GraphQLクエリ | ✅ Pass | 正常動作 |
| ポイント送受信 | ✅ Pass | 正常動作 |

## 総合評価

✅ **マイグレーション成功**

---

**承認者:**
- DevOpsリード: ◯◯
- テックリード: ◯◯
\`\`\`
```

---

### ステップ7: 段階的データ移行（オプション）

既存データに有効期限を設定する場合:

```markdown
## 段階的データ移行（オプションB採用時）

### バッチ処理による段階的移行

\`\`\`typescript
// scripts/migrate-wallet-expiration.ts

import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

async function migrateWalletExpiration() {
  const BATCH_SIZE = 100;
  const EXPIRATION_YEARS = 1;

  let offset = 0;
  let processedCount = 0;

  while (true) {
    // 100件ずつ取得
    const wallets = await prisma.t_wallets.findMany({
      where: { expiresAt: null },
      take: BATCH_SIZE,
      skip: offset,
      orderBy: { createdAt: 'asc' }
    });

    if (wallets.length === 0) break;

    // 有効期限を設定（createdAt + 1年）
    for (const wallet of wallets) {
      const expiresAt = new Date(wallet.createdAt);
      expiresAt.setFullYear(expiresAt.getFullYear() + EXPIRATION_YEARS);

      await prisma.t_wallets.update({
        where: { id: wallet.id },
        data: { expiresAt }
      });

      processedCount++;
      console.log(\`Processed: \${processedCount} / 1234\`);
    }

    offset += BATCH_SIZE;

    // 1秒スリープ（データベース負荷軽減）
    await new Promise(resolve => setTimeout(resolve, 1000));
  }

  console.log(\`Migration completed: \${processedCount} wallets updated\`);
}

migrateWalletExpiration().catch(console.error);
\`\`\`

---

### 実行スケジュール

| Day | 処理件数 | 進捗 |
|-----|---------|------|
| 1 | 100件 | 8.1% |
| 2 | 100件 | 16.2% |
| 3 | 100件 | 24.3% |
| ... | ... | ... |
| 12 | 100件 | 97.2% |
| 13 | 34件 | 100% |

**総所要期間:** 13日

---

### 監視とアラート

\`\`\`typescript
// 進捗監視
const progress = await prisma.t_wallets.count({
  where: { expiresAt: { not: null } }
});

const total = await prisma.t_wallets.count();
const percentage = (progress / total) * 100;

console.log(\`Progress: \${percentage.toFixed(1)}%\`);
\`\`\`

**アラート:**
- バッチ処理失敗時に通知
- 1日の処理件数が0件の場合に警告
```

---

### ステップ8: コミュニケーション計画

ステークホルダーへの通知:

```markdown
## コミュニケーション計画

### マイグレーション1週間前

**対象:** 全ステークホルダー

**内容:**
\`\`\`
件名: [予告] データベースマイグレーション実施のお知らせ

本文:
2026年1月22日（水）深夜2:00-2:15に、データベースマイグレーションを実施します。

【作業内容】
- t_walletsテーブルへのカラム追加（expiresAt）

【影響】
- サービスダウンタイム: なし（予定）
- 機能への影響: なし

【作業時間】
- 開始: 2026-01-22 02:00
- 終了: 2026-01-22 02:15（予定）

【担当】
- DevOpsチーム

ご質問がありましたら、DevOpsチームまでお願いします。
\`\`\`

---

### マイグレーション当日（実施前）

**対象:** 技術チーム

**内容:**
\`\`\`
件名: [開始] データベースマイグレーション開始

本文:
2:00 からマイグレーションを開始します。

【チェックリスト】
- [x] バックアップ完了
- [x] ロールバック手順確認
- [x] 監視ダッシュボード準備

【連絡先】
- 作業担当: ◯◯（Slack: @xxx）
- バックアップ: ◯◯（Slack: @yyy）
\`\`\`

---

### マイグレーション完了後

**対象:** 全ステークホルダー

**内容:**
\`\`\`
件名: [完了] データベースマイグレーション完了のお知らせ

本文:
データベースマイグレーションが正常に完了しました。

【実施内容】
- t_walletsテーブルへのカラム追加（expiresAt）

【結果】
- ステータス: ✅ 成功
- 実行時間: 2:00-2:10（10分）
- データ検証: ✅ 全て正常

【影響】
- サービスダウンタイム: なし
- データ損失: なし

引き続き24時間監視を継続します。

【報告】
DevOpsチーム
\`\`\`
```

---

### ステップ9: リスク評価

マイグレーションのリスクを評価:

```markdown
## リスク評価

### 技術的リスク

| リスク | 発生確率 | 影響度 | 対策 |
|--------|---------|--------|------|
| マイグレーション失敗 | 低 (5%) | 高 | ステージング検証、バックアップ |
| アプリケーションエラー | 低 (10%) | 中 | 型チェック、テスト |
| パフォーマンス劣化 | 低 (5%) | 中 | インデックス作成、監視 |
| データ不整合 | 極低 (1%) | 高 | 検証スクリプト |

---

### ビジネスリスク

| リスク | 発生確率 | 影響度 | 対策 |
|--------|---------|--------|------|
| ダウンタイム | 低 (10%) | 中 | メンテナンスウィンドウ設定 |
| ユーザーへの影響 | 極低 (1%) | 低 | 既存データ変更なし |
| データ損失 | 極低 (1%) | 高 | バックアップ、検証 |

---

### 総合リスク評価

**リスクレベル:** 🟢 Low

**推奨:** マイグレーション実施可能
```

---

### ステップ10: マイグレーション完了レポート

実施後のレポートテンプレート:

```markdown
# データマイグレーション完了レポート

**マイグレーション:** ポイント有効期限機能（t_wallets.expiresAt追加）
**実施日:** 2026-01-15
**担当:** DevOpsチーム

---

## エグゼクティブサマリー

### 結果

✅ **マイグレーション成功**

- 実行時間: 10分（予定15分）
- ダウンタイム: 0分
- データ損失: なし
- エラー: なし

---

## 詳細

### タイムライン

| 時刻 | イベント | ステータス |
|------|---------|-----------|
| 02:00 | メンテナンス開始 | ✅ |
| 02:01 | バックアップ開始 | ✅ |
| 02:03 | バックアップ完了 | ✅ |
| 02:04 | マイグレーション実行 | ✅ |
| 02:05 | データ検証 | ✅ |
| 02:07 | アプリケーション再起動 | ✅ |
| 02:09 | 動作確認 | ✅ |
| 02:10 | メンテナンス終了 | ✅ |

---

### データ検証結果

| 検証項目 | 結果 |
|---------|------|
| レコード数 | ✅ 1,234件（変更なし） |
| expiresAt null | ✅ 全てnull |
| データ整合性 | ✅ 異常なし |
| インデックス作成 | ✅ 正常 |
| GraphQLクエリ | ✅ 正常動作 |

---

### パフォーマンス

| メトリクス | 変更前 | 変更後 | 差分 |
|-----------|--------|--------|------|
| クエリ時間 | 45ms | 46ms | +1ms |
| エラー率 | 0.1% | 0.1% | ±0% |
| レスポンスタイム | 120ms | 121ms | +1ms |

**評価:** パフォーマンス影響なし

---

### 教訓

#### うまくいったこと
- ステージング環境での事前検証
- 詳細なロールバック計画
- バッ クアップの迅速な取得

#### 改善点
- マイグレーション時間をさらに短縮可能
- 自動検証スクリプトの追加

---

## 承認

- DevOpsリード: ◯◯
- テックリード: ◯◯
- プロダクトオーナー: ◯◯
```

---

## 活用例

### 例1: カラム追加のマイグレーション

```bash
/migration-requirements "t_walletsにexpiresAtカラムを追加"
```

**出力:**
- スキーマ変更分析
- データ移行計画
- 実行手順書

---

### 例2: テーブル追加のマイグレーション

```bash
/migration-requirements "t_point_expiration_logsテーブルを新規作成"
```

**出力:**
- DDL生成
- 初期データ投入計画
- インデックス設計

---

## 注意事項

### マイグレーションの原則

- ✅ **必ずバックアップを取る**
- ✅ **ステージングで検証**
- ✅ **ロールバック計画を用意**
- ✅ **段階的に実施**（大規模変更は分割）
- ✅ **メンテナンスウィンドウを設定**

### よくある失敗

- ❌ バックアップなしで実施
- ❌ 本番でいきなり実施
- ❌ ロールバック計画なし
- ❌ データ検証をスキップ

### 推奨される併用スキル

- `/check-requirement-delta` - スキーマ変更の影響確認
- `/phased-delivery-plan` - 段階的リリース計画
- `/side-effect-brainstorming` - マイグレーションの副作用

---

## 参考資料

- [Prisma Migrations](https://www.prisma.io/docs/concepts/components/prisma-migrate)
- [PostgreSQL ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html)
- [Database Migration Best Practices](https://www.prisma.io/docs/guides/migrate/production-troubleshooting)
