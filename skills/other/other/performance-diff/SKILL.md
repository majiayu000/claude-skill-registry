---
name: performance-diff
description: 変更前後のパフォーマンスを比較し、リグレッションを検出
user-invocable: true
argument-hint: [PRでは自動、手動では--before/--after指定]
allowed-tools: Read, Grep, Bash
context: fork
---

# civicship-api パフォーマンス比較

コード変更前後の**パフォーマンスを比較**し、リグレッション（性能劣化）を検出します。ベンチマーク結果、クエリ数、レスポンスタイムを分析します。

## 使用方法

```bash
# PRのパフォーマンス比較（自動）
/performance-diff --pr 123

# ブランチ間の比較
/performance-diff --before main --after feature/point-expiration

# 特定ドメインの比較
/performance-diff wallet --before HEAD~1 --after HEAD
```

**引数:**
- `$ARGUMENTS`: ドメイン名、PRでは番号、または `--before`/`--after` オプション

---

## パフォーマンス比較プロセス

### ステップ1: 変更内容の取得

GitでのDiffを取得:

```bash
# PRの差分取得
gh pr diff 123

# ブランチ間の差分
git diff main..feature/point-expiration

# 変更されたファイルのみ
git diff --name-only main..feature/point-expiration
```

**変更サマリー:**

```markdown
## 変更概要

### 変更されたファイル（10ファイル）

**Application Layer:**
- `src/application/domain/account/wallet/service.ts` (+50, -10)
- `src/application/domain/account/wallet/usecase.ts` (+20, -5)
- `src/application/domain/account/wallet/data/repository.ts` (+30, -8)

**Infrastructure Layer:**
- `prisma/schema.prisma` (+5, -0)

**Presentation Layer:**
- `src/application/domain/account/wallet/schema/type.graphql` (+10, -0)

---

### 変更の種類

- [ ] データベーススキーマ変更（カラム追加）
- [ ] 新しいクエリ追加
- [ ] ビジネスロジック変更
- [ ] GraphQL API拡張
```

---

### ステップ2: パフォーマンステストの実行

変更前後でベンチマークを実行:

```bash
# 変更前（main）のパフォーマンステスト
git checkout main
pnpm test:performance > performance-before.txt

# 変更後（feature branch）のパフォーマンステスト
git checkout feature/point-expiration
pnpm test:performance > performance-after.txt

# 差分比較
diff performance-before.txt performance-after.txt
```

**パフォーマンステスト結果:**

```markdown
## パフォーマンステスト結果

### Test: GraphQL Query `wallet(id: "...")`

#### 変更前（main）
\`\`\`
Requests: 1000
Success: 1000 (100%)
Duration: 5.2s
Avg: 5.2ms
P50: 4.8ms
P95: 8.5ms
P99: 12.3ms
\`\`\`

#### 変更後（feature/point-expiration）
\`\`\`
Requests: 1000
Success: 1000 (100%)
Duration: 5.5s
Avg: 5.5ms (+5.8%)
P50: 5.0ms (+4.2%)
P95: 9.0ms (+5.9%)
P99: 13.1ms (+6.5%)
\`\`\`

**評価:** 🟡 軽微な劣化（+5.8%）
**原因:** 有効期限チェックの追加（日付比較）
**許容範囲:** ✅ Yes（+10%以内）

---

### Test: GraphQL Mutation `walletCreate`

#### 変更前
\`\`\`
Requests: 100
Duration: 2.1s
Avg: 21ms
\`\`\`

#### 変更後
\`\`\`
Requests: 100
Duration: 2.3s
Avg: 23ms (+9.5%)
\`\`\`

**評価:** 🟡 軽微な劣化（+9.5%）
**原因:** expiresAt カラムの書き込み追加
**許容範囲:** ✅ Yes（+10%以内）

---

### Test: Batch Process `expirePoints`

#### 変更前
\`\`\`
該当なし（新規処理）
\`\`\`

#### 変更後
\`\`\`
Wallets Processed: 1000
Duration: 8.5s
Avg per wallet: 8.5ms
\`\`\`

**評価:** 🟢 新規処理（ベースラインとして記録）
```

---

### ステップ3: クエリ数の比較

SQLクエリ数の変化を分析:

```markdown
## クエリ数の比較

### GraphQL Query `wallet(id: "...")`

#### 変更前
\`\`\`
SELECT * FROM t_wallets WHERE id = '...'  -- 1クエリ
\`\`\`

**Total:** 1クエリ

---

#### 変更後
\`\`\`
SELECT * FROM t_wallets WHERE id = '...'  -- 1クエリ
\`\`\`

**Total:** 1クエリ（変更なし）

**評価:** ✅ クエリ数増加なし

---

### GraphQL Mutation `pointTransfer`

#### 変更前
\`\`\`
1. SELECT * FROM t_wallets WHERE userId = 'from-user'
2. SELECT * FROM t_wallets WHERE userId = 'to-user'
3. UPDATE t_wallets SET balance = ... WHERE id = 'from-wallet'
4. UPDATE t_wallets SET balance = ... WHERE id = 'to-wallet'
5. INSERT INTO t_point_transactions ...
\`\`\`

**Total:** 5クエリ

---

#### 変更後
\`\`\`
1. SELECT * FROM t_wallets WHERE userId = 'from-user'
2. SELECT * FROM t_wallets WHERE userId = 'to-user'
   （有効期限チェック追加: メモリ内で実行、クエリ不要）
3. UPDATE t_wallets SET balance = ... WHERE id = 'from-wallet'
4. UPDATE t_wallets SET balance = ... WHERE id = 'to-wallet'
5. INSERT INTO t_point_transactions ...
\`\`\`

**Total:** 5クエリ（変更なし）

**評価:** ✅ クエリ数増加なし
```

---

### ステップ4: N+1問題の検出

新たにN+1問題が導入されていないか確認:

```markdown
## N+1問題の検出

### 検証: User.wallets

**変更内容:**
\`\`\`diff
User: {
  wallet: (parent, _, ctx) => {
-   return prisma.t_wallets.findUnique({ where: { userId: parent.id } });
+   return ctx.loaders.wallet.load(parent.id);
  }
}
\`\`\`

**評価:**
- 変更前: N+1問題あり
- 変更後: DataLoader使用、N+1問題解消 ✅

**パフォーマンス改善:**
- 100ユーザー取得時のクエリ数: 100回 → 1回
- レスポンスタイム: 5秒 → 50ms（100倍改善）

**評価:** 🟢 大幅改善
```

---

### ステップ5: データベースインデックスの影響

インデックス追加によるパフォーマンス改善を確認:

```markdown
## インデックスの影響

### 追加されたインデックス

\`\`\`prisma
model t_wallets {
  // ...
+ @@index([expiresAt])
}
\`\`\`

---

### クエリパフォーマンス比較

#### Query: `SELECT * FROM t_wallets WHERE expiresAt < NOW()`

**変更前（インデックスなし）:**
\`\`\`
Seq Scan on t_wallets  (cost=0.00..25.50 rows=10 width=100)
Execution Time: 45.2 ms
\`\`\`

**変更後（インデックスあり）:**
\`\`\`
Index Scan using idx_wallets_expires_at on t_wallets  (cost=0.15..8.17 rows=10 width=100)
Execution Time: 2.1 ms
\`\`\`

**評価:** 🟢 大幅改善（21倍高速化）
```

---

### ステップ6: メモリ使用量の比較

メモリフットプリントの変化:

```markdown
## メモリ使用量

### ヒープメモリ

**変更前:**
- Used Heap: 120 MB
- Heap Limit: 512 MB
- Usage: 23%

**変更後:**
- Used Heap: 125 MB (+4.2%)
- Heap Limit: 512 MB
- Usage: 24%

**評価:** 🟢 許容範囲内（+5%以下）

---

### オブジェクト数

**変更前:**
- Total Objects: 150,000

**変更後:**
- Total Objects: 152,000 (+1.3%)

**評価:** 🟢 微増（問題なし）
```

---

### ステップ7: リグレッション判定

総合的なパフォーマンス評価:

```markdown
## リグレッション判定

### 判定基準

| メトリクス | 閾値 | 変更前 | 変更後 | 差分 | 判定 |
|-----------|------|--------|--------|------|------|
| Avg Response Time | +10% | 5.2ms | 5.5ms | +5.8% | ✅ Pass |
| P95 Response Time | +15% | 8.5ms | 9.0ms | +5.9% | ✅ Pass |
| P99 Response Time | +20% | 12.3ms | 13.1ms | +6.5% | ✅ Pass |
| Query Count | +0 | 5 | 5 | 0 | ✅ Pass |
| Memory Usage | +10% | 120MB | 125MB | +4.2% | ✅ Pass |
| Error Rate | +0% | 0% | 0% | 0% | ✅ Pass |

---

### 総合評価

**スコア:** 95 / 100 🟢 Excellent

**判定:** ✅ **パフォーマンスリグレッションなし**

**コメント:**
- 軽微な劣化はあるが、全て許容範囲内
- 有効期限チェックの追加によるオーバーヘッドは予想通り
- インデックス追加により一部クエリは大幅改善
- N+1問題の解消により全体的なパフォーマンス向上

**推奨アクション:**
- マージ可能
- 本番環境での監視継続
```

---

### ステップ8: パフォーマンス改善の提案

さらなる最適化の提案:

```markdown
## パフォーマンス改善提案

### 提案1: キャッシュ導入

**現状:**
- 有効期限チェックを毎回実行

**提案:**
\`\`\`typescript
// Redis キャッシュ（TTL: 60秒）
const cacheKey = \`wallet:expiration:\${walletId}\`;
const cached = await redis.get(cacheKey);
if (cached) return JSON.parse(cached);

const wallet = await this.repo.findById(ctx, walletId, tx);
await redis.setex(cacheKey, 60, JSON.stringify(wallet));
return wallet;
\`\`\`

**効果:**
- レスポンスタイム: 5.5ms → 0.5ms（11倍改善）
- データベース負荷: 90%削減

---

### 提案2: SELECT句の最適化

**現状:**
\`\`\`typescript
return tx.t_wallets.findUnique({ where: { id } });
\`\`\`

**提案:**
\`\`\`typescript
return tx.t_wallets.findUnique({
  where: { id },
  select: {
    id: true,
    balance: true,
    expiresAt: true,
    // 必要なフィールドのみ
  }
});
\`\`\`

**効果:**
- データ転送量: 80%削減
- メモリ使用量: 削減
```

---

### ステップ9: 比較レポート生成

```markdown
# パフォーマンス比較レポート

**PR:** #123
**ブランチ:** feature/point-expiration
**比較:** main vs feature/point-expiration
**実施日:** 2026-01-15

---

## エグゼクティブサマリー

### 総合評価

**判定:** ✅ **マージ可能**

**スコア:** 95 / 100

**リグレッション:** なし（軽微な劣化は許容範囲内）

---

## 詳細比較

### レスポンスタイム

| エンドポイント | 変更前 | 変更後 | 差分 | 判定 |
|---------------|--------|--------|------|------|
| wallet(id) | 5.2ms | 5.5ms | +5.8% | ✅ |
| walletCreate | 21ms | 23ms | +9.5% | ✅ |
| pointTransfer | 45ms | 46ms | +2.2% | ✅ |

---

### クエリ数

| エンドポイント | 変更前 | 変更後 | 差分 | 判定 |
|---------------|--------|--------|------|------|
| wallet(id) | 1 | 1 | 0 | ✅ |
| pointTransfer | 5 | 5 | 0 | ✅ |

---

### パフォーマンス改善

- **N+1問題解消:** User.wallets（100倍改善）
- **インデックス追加:** expiresAt クエリ（21倍改善）

---

## 推奨アクション

### 即座に実施
- ✅ PR をマージ可能
- 🔔 本番環境で監視継続（24時間）

### 将来的に検討
- キャッシュ導入（さらなる最適化）
- SELECT句の最適化

---

## 承認

- [ ] テックリード
- [ ] DevOpsリード
```

---

## 活用例

### 例1: PRのパフォーマンス比較

```bash
/performance-diff --pr 123
```

**出力:**
- 変更前後の比較
- リグレッション判定
- マージ可否の判断

---

### 例2: リリース前の検証

```bash
/performance-diff --before v1.0.0 --after main
```

**出力:**
- バージョン間の比較
- パフォーマンス推移

---

## 参考資料

- [Performance Testing Best Practices](https://k6.io/docs/testing-guides/performance-testing/)
- [Database Query Performance](https://www.postgresql.org/docs/current/performance-tips.html)
- [GraphQL Performance](https://www.apollographql.com/docs/apollo-server/performance/caching/)
