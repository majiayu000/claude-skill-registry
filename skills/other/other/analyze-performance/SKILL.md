---
name: analyze-performance
description: パフォーマンスボトルネックを特定し、最適化提案を提示
user-invocable: true
argument-hint: [ドメイン名またはファイルパス]
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

# civicship-api パフォーマンス分析

パフォーマンスの**ボトルネック**を特定し、最適化提案を提示します。N+1問題、不要なクエリ、非効率なアルゴリズムを検出します。

## 使用方法

```bash
# ドメイン全体のパフォーマンス分析
/analyze-performance wallet

# 特定ファイルの分析
/analyze-performance src/application/domain/account/wallet/service.ts

# 全体のパフォーマンスレポート
/analyze-performance --all
```

**引数:**
- `$ARGUMENTS`: ドメイン名、ファイルパス、または `--all`

---

## パフォーマンス分析プロセス

### ステップ1: N+1問題の検出

ループ内のクエリ実行を検出:

```bash
# ループ内のawait検索
grep -A 5 "for.*of\|for.*in\|forEach\|map" src/application/domain/${DOMAIN}/**/*.ts | grep -B 3 "await.*find\|await.*query"

# DataLoaderの使用確認
grep -r "ctx.loaders" src/application/domain/${DOMAIN}/**/*.ts
```

**N+1問題レポート:**

```markdown
## N+1問題の検出

### 🔴 Critical: N+1問題あり

#### 問題1: UserResolver.wallets

**ファイル:** `src/application/domain/account/user/controller/resolver.ts:45`

**コード:**
\`\`\`typescript
User: {
  wallets: async (parent, _, ctx) => {
    // 全ユーザーに対してこのクエリが実行される（N+1）
    return await prisma.t_wallets.findMany({
      where: { userId: parent.id }
    });
  }
}
\`\`\`

**問題:**
- 100ユーザーを取得すると、100回のクエリが実行される
- レスポンスタイム: 5秒以上

**推奨修正:**
\`\`\`typescript
User: {
  wallets: (parent, _, ctx) => {
    // DataLoaderでバッチローディング
    return ctx.loaders.walletsByUserId.load(parent.id);
  }
}

// DataLoader定義
const walletsByUserIdLoader = new DataLoader(async (userIds) => {
  const wallets = await prisma.t_wallets.findMany({
    where: { userId: { in: userIds } }
  });
  // userIdごとにグループ化して返す
  return userIds.map(id => wallets.filter(w => w.userId === id));
});
\`\`\`

**効果:**
- クエリ数: 100回 → 1回
- レスポンスタイム: 5秒 → 50ms（100倍改善）

---

### ✅ 正しい実装例

#### Opportunity.community（DataLoader使用）

**ファイル:** `src/application/domain/experience/opportunity/controller/resolver.ts:30`

\`\`\`typescript
Opportunity: {
  community: (parent, _, ctx) => {
    return ctx.loaders.community.load(parent.communityId);
  }
}
\`\`\`

**評価:** N+1問題なし
```

---

### ステップ2: 不要なクエリの検出

同じデータを複数回取得している箇所を検出:

```bash
# 同じクエリが複数回実行されている可能性
grep -A 3 "findUnique\|findFirst" src/application/domain/${DOMAIN}/**/*.ts | sort | uniq -c | sort -rn
```

**不要クエリレポート:**

```markdown
## 不要なクエリ

### 問題1: 重複したウォレット取得

**ファイル:** `src/application/domain/transaction/point-transfer/service.ts:120`

**コード:**
\`\`\`typescript
async transferPoints(ctx, input, tx) {
  // ウォレットを2回取得（無駄）
  const fromWallet = await this.walletRepo.findById(ctx, input.fromWalletId, tx);
  const toWallet = await this.walletRepo.findById(ctx, input.toWalletId, tx);

  // バリデーション後、再度取得（無駄）
  const fromWalletAgain = await this.walletRepo.findById(ctx, input.fromWalletId, tx);

  // ...
}
\`\`\`

**推奨修正:**
\`\`\`typescript
async transferPoints(ctx, input, tx) {
  // 1回だけ取得
  const [fromWallet, toWallet] = await Promise.all([
    this.walletRepo.findById(ctx, input.fromWalletId, tx),
    this.walletRepo.findById(ctx, input.toWalletId, tx)
  ]);

  // 再取得せず、メモリ上のデータを使用
  // ...
}
\`\`\`

**効果:**
- クエリ数: 3回 → 2回
- レスポンスタイム: 15ms → 10ms
```

---

### ステップ3: SELECT句の最適化

必要以上のカラムを取得している箇所を検出:

```bash
# SELECT * の使用箇所
grep -r "prisma.*\.findMany\|prisma.*\.findUnique" src/application/domain/${DOMAIN}/**/*.ts | grep -v "select:"
```

**SELECT最適化レポート:**

```markdown
## SELECT句の最適化

### 問題1: 全カラム取得

**ファイル:** `src/application/domain/account/wallet/data/repository.ts:50`

**コード:**
\`\`\`typescript
async findById(ctx, id, tx) {
  // 全カラムを取得（無駄が多い）
  return tx.t_wallets.findUnique({ where: { id } });
}
\`\`\`

**問題:**
- 不要なカラム（例: `metadata`, `internalNotes`）も取得
- ネットワーク転送量が増加
- メモリ使用量が増加

**推奨修正:**
\`\`\`typescript
async findById(ctx, id, tx) {
  // 必要なカラムのみ取得
  return tx.t_wallets.findUnique({
    where: { id },
    select: {
      id: true,
      userId: true,
      balance: true,
      expiresAt: true,
      createdAt: true,
      updatedAt: true
    }
  });
}
\`\`\`

**効果:**
- データ転送量: 1KB → 200B（80%削減）
- メモリ使用量: 削減
```

---

### ステップ4: インデックスの確認

データベースインデックスの不足を検出:

```bash
# WHERE句で使用されているカラムを抽出
grep -r "where:" src/application/domain/${DOMAIN}/data/repository.ts | grep -o "{.*}" | sort | uniq

# Prismaスキーマのインデックス確認
grep -A 10 "model t_wallets" prisma/schema.prisma | grep "@@index"
```

**インデックスレポート:**

```markdown
## インデックス分析

### 推奨: インデックス追加

#### インデックス1: t_wallets.expiresAt

**使用箇所:**
- バッチ処理: 有効期限切れポイントの検索
- クエリ: `WHERE expiresAt < NOW()`

**現状:** インデックスなし

**推奨:**
\`\`\`prisma
model t_wallets {
  // ...
  @@index([expiresAt])
}
\`\`\`

**効果:**
- クエリ時間: 500ms → 10ms（50倍改善）

---

#### インデックス2: t_wallets.userId + createdAt

**使用箇所:**
- ウォレット一覧の取得（ユーザーID + 作成日でソート）

**現状:** userId のみインデックス

**推奨:**
\`\`\`prisma
model t_wallets {
  // ...
  @@index([userId, createdAt])
}
\`\`\`

**効果:**
- ソートパフォーマンス向上
```

---

### ステップ5: 非効率なアルゴリズムの検出

計算量が大きいコードを検出:

```markdown
## アルゴリズム分析

### 問題1: ネストループ（O(N²)）

**ファイル:** `src/application/domain/reward/utility/service.ts:80`

**コード:**
\`\`\`typescript
async findMatchingUtilities(ctx, userId) {
  const utilities = await this.repo.findAll(ctx);  // 1,000件
  const userSkills = await this.userSkillRepo.findByUserId(ctx, userId);  // 10件

  // O(N * M) = O(10,000)
  return utilities.filter(utility => {
    return userSkills.some(skill => {
      return utility.requiredSkills.includes(skill.skillId);
    });
  });
}
\`\`\`

**問題:**
- 計算量: O(N * M * K)
- 処理時間: 100ms以上

**推奨修正:**
\`\`\`typescript
async findMatchingUtilities(ctx, userId) {
  const userSkills = await this.userSkillRepo.findByUserId(ctx, userId);
  const skillIds = userSkills.map(s => s.skillId);

  // データベースで絞り込み（O(N)）
  return this.repo.findBySkills(ctx, skillIds);
}

// Repository
async findBySkills(ctx, skillIds) {
  return ctx.issuer.public(ctx, (tx) =>
    tx.t_utilities.findMany({
      where: {
        requiredSkills: { hasSome: skillIds }
      }
    })
  );
}
\`\`\`

**効果:**
- 計算量: O(N) に改善
- 処理時間: 100ms → 10ms
```

---

### ステップ6: キャッシュの提案

頻繁にアクセスされるデータのキャッシュを提案:

```markdown
## キャッシュ戦略

### 提案1: ウォレット残高のキャッシュ

**現状:**
- 残高取得クエリ: 毎回データベースアクセス
- 頻度: 100回/秒

**提案:**
\`\`\`typescript
// Redis キャッシュ
import { Redis } from 'ioredis';
const redis = new Redis();

async findById(ctx, id) {
  // キャッシュ確認
  const cached = await redis.get(\`wallet:\${id}\`);
  if (cached) return JSON.parse(cached);

  // データベースから取得
  const wallet = await this.repo.findById(ctx, id);

  // キャッシュに保存（TTL: 60秒）
  await redis.setex(\`wallet:\${id}\`, 60, JSON.stringify(wallet));

  return wallet;
}
\`\`\`

**効果:**
- データベース負荷: 100回/秒 → 2回/秒（98%削減）
- レスポンスタイム: 5ms → 0.5ms

**注意:**
- キャッシュ無効化のタイミング
- データ整合性の考慮
```

---

### ステップ7: バッチ処理の最適化

バッチ処理のパフォーマンス改善:

```markdown
## バッチ処理の最適化

### 問題1: 1件ずつ処理

**ファイル:** `scripts/expire-points.ts`

**コード:**
\`\`\`typescript
async expirePoints() {
  const expiredWallets = await prisma.t_wallets.findMany({
    where: { expiresAt: { lt: new Date() } }
  });

  // 1件ずつ処理（遅い）
  for (const wallet of expiredWallets) {
    await prisma.t_wallets.update({
      where: { id: wallet.id },
      data: { balance: 0 }
    });
  }
}
\`\`\`

**推奨修正:**
\`\`\`typescript
async expirePoints() {
  // 一括更新（速い）
  await prisma.t_wallets.updateMany({
    where: { expiresAt: { lt: new Date() } },
    data: { balance: 0 }
  });
}
\`\`\`

**効果:**
- 処理時間: 1,000件で 10秒 → 0.5秒（20倍改善）
```

---

### ステップ8: パフォーマンスレポート生成

```markdown
# パフォーマンス分析レポート

**対象:** Walletドメイン
**分析日:** 2026-01-15

---

## エグゼクティブサマリー

### 総合評価

**パフォーマンススコア:** 65 / 100 🟡 改善余地あり

### 検出された問題

- **Critical:** 2件（N+1問題）
- **High:** 3件（不要クエリ、インデックス不足）
- **Medium:** 5件（非効率なアルゴリズム）

### 推定改善効果

| 項目 | 現状 | 改善後 | 効果 |
|------|------|--------|------|
| レスポンスタイム | 500ms | 50ms | 10倍 |
| クエリ数 | 100回/リクエスト | 5回/リクエスト | 95%削減 |
| データベース負荷 | 100% | 20% | 80%削減 |

---

## 優先度別の改善提案

### 🔴 P0: 即座に実施（Critical）

| # | 問題 | 改善内容 | 工数 | 効果 |
|---|------|---------|------|------|
| 1 | N+1問題（UserResolver.wallets） | DataLoader導入 | 2h | レスポンスタイム100倍改善 |
| 2 | インデックス不足（expiresAt） | インデックス追加 | 0.5h | クエリ50倍高速化 |

**Total:** 2.5時間

---

### 🟡 P1: 2週間以内に実施（High）

| # | 問題 | 改善内容 | 工数 | 効果 |
|---|------|---------|------|------|
| 3 | 重複クエリ | リファクタリング | 1h | クエリ数30%削減 |
| 4 | SELECT * 使用 | select句最適化 | 1.5h | 転送量80%削減 |
| 5 | 非効率アルゴリズム | データベースで絞り込み | 3h | 処理時間10倍改善 |

**Total:** 5.5時間

---

### 🟢 P2: 1ヶ月以内に実施（Medium）

| # | 問題 | 改善内容 | 工数 | 効果 |
|---|------|---------|------|------|
| 6-10 | バッチ処理最適化など | 一括更新、キャッシュ導入 | 8h | 全体最適化 |

**Total:** 8時間

---

## 実装計画

### Week 1: Critical対応
- Day 1-2: DataLoader導入
- Day 3: インデックス追加
- Day 4: テスト・検証
- Day 5: 本番デプロイ

### Week 2-3: High対応
- 重複クエリ削減
- SELECT句最適化
- アルゴリズム改善

### Month 2: Medium対応
- キャッシュ導入
- バッチ処理最適化

---

## 承認

- [ ] テックリード
- [ ] DevOpsリード
```

---

## 活用例

### 例1: ドメイン全体の分析

```bash
/analyze-performance wallet
```

**出力:**
- N+1問題の検出
- 最適化提案
- 優先度付き改善計画

---

### 例2: PRの パフォーマンスレビュー

```bash
/analyze-performance --pr 123
```

**出力:**
- 変更によるパフォーマンス影響
- 新たに導入されたボトルネック

---

## 参考資料

- [Prisma Performance Best Practices](https://www.prisma.io/docs/guides/performance-and-optimization)
- [DataLoader Documentation](https://github.com/graphql/dataloader)
- [Database Indexing Guide](https://www.postgresql.org/docs/current/indexes.html)
