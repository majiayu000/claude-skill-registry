---
name: monitoring-readiness
description: 監視要件を定義し、アラート・メトリクス設定を提案
user-invocable: true
argument-hint: [機能名または要件定義書]
allowed-tools: Read, Grep, Bash
context: fork
---

# civicship-api 監視準備

新機能・変更に必要な**監視要件**を定義し、メトリクス、アラート、ダッシュボード設定を提案します。

## 使用方法

```bash
# 新機能の監視要件を生成
/monitoring-readiness "ポイント有効期限機能"

# 要件定義書から監視要件を生成
/monitoring-readiness docs/requirements/point-expiration.md

# 既存機能の監視強化
/monitoring-readiness wallet --enhance
```

**引数:**
- `$ARGUMENTS`: 機能名、要件定義書パス、またはドメイン名

---

## 監視要件定義プロセス

### ステップ1: 監視対象の特定

機能の重要な動作を特定:

```markdown
## 監視対象の特定

**機能:** ポイント有効期限機能

### 主要な処理フロー

1. **ポイント付与時の有効期限設定**
   - トリガー: GraphQL Mutation `walletCreate`
   - 頻度: 100回/日
   - 重要度: 🔴 Critical

2. **有効期限切れポイントの自動失効**
   - トリガー: Cronバッチ（毎日2:00）
   - 頻度: 1回/日
   - 重要度: 🔴 Critical

3. **有効期限通知送信**
   - トリガー: Cronバッチ（毎日10:00）
   - 頻度: 1回/日
   - 重要度: 🟡 High

4. **ポイント使用時の有効期限チェック**
   - トリガー: GraphQL Mutation `pointTransfer`, `utilityExchange`
   - 頻度: 500回/日
   - 重要度: 🔴 Critical
```

---

### ステップ2: メトリクスの設計

監視すべき指標を定義:

```markdown
## メトリクス設計

### カテゴリ1: ビジネスメトリクス

#### 1. 失効ポイント総数（日次）

**メトリクス名:** `wallet.expiration.points_expired_total`
**型:** Counter
**ラベル:**
- `community_id`: コミュニティID
- `reason`: 失効理由（`expired`, `manual`）

**収集方法:**
\`\`\`typescript
// バッチ処理内
metrics.increment('wallet.expiration.points_expired_total', {
  tags: {
    community_id: wallet.communityId,
    reason: 'expired'
  },
  value: expiredPoints
});
\`\`\`

**アラート:**
- 失効ポイント > 100,000pt/日 → 警告（異常値の可能性）
- 失効ポイント = 0 → 警告（バッチ未実行の可能性）

---

#### 2. 失効ユーザー数（日次）

**メトリクス名:** `wallet.expiration.users_affected_total`
**型:** Counter
**ラベル:**
- `community_id`: コミュニティID

**収集方法:**
\`\`\`typescript
metrics.increment('wallet.expiration.users_affected_total', {
  tags: { community_id: wallet.communityId },
  value: affectedUserCount
});
\`\`\`

**アラート:**
- 失効ユーザー > 1,000人/日 → 警告

---

#### 3. 通知送信成功率

**メトリクス名:** `wallet.expiration.notification_success_rate`
**型:** Gauge
**値:** 0.0 ～ 1.0

**収集方法:**
\`\`\`typescript
const successRate = successCount / totalCount;
metrics.gauge('wallet.expiration.notification_success_rate', successRate);
\`\`\`

**アラート:**
- 成功率 < 0.95 → 警告（LINE API問題の可能性）
- 成功率 < 0.8 → 緊急

---

### カテゴリ2: 技術メトリクス

#### 4. バッチ処理実行時間

**メトリクス名:** `wallet.expiration.batch_duration_seconds`
**型:** Histogram
**ラベル:**
- `batch_type`: `expire_points`, `send_notifications`

**収集方法:**
\`\`\`typescript
const startTime = Date.now();
await expirePoints();
const duration = (Date.now() - startTime) / 1000;

metrics.histogram('wallet.expiration.batch_duration_seconds', {
  tags: { batch_type: 'expire_points' },
  value: duration
});
\`\`\`

**アラート:**
- 実行時間 > 60秒 → 警告（パフォーマンス劣化）
- 実行時間 > 300秒 → 緊急（タイムアウトの可能性）

---

#### 5. 有効期限チェックのレスポンスタイム

**メトリクス名:** `wallet.expiration.check_duration_ms`
**型:** Histogram

**収集方法:**
\`\`\`typescript
const start = Date.now();
await this.checkExpiration(wallet);
const duration = Date.now() - start;

metrics.histogram('wallet.expiration.check_duration_ms', duration);
\`\`\`

**アラート:**
- P95 > 100ms → 警告
- P99 > 200ms → 注意

---

#### 6. データベースクエリ時間

**メトリクス名:** `wallet.expiration.db_query_duration_ms`
**型:** Histogram
**ラベル:**
- `query_type`: `find_expired`, `update_balance`

**収集方法:**
\`\`\`typescript
// Prismaミドルウェアで自動収集
prisma.$use(async (params, next) => {
  const start = Date.now();
  const result = await next(params);
  const duration = Date.now() - start;

  metrics.histogram('wallet.expiration.db_query_duration_ms', {
    tags: { query_type: params.action },
    value: duration
  });

  return result;
});
\`\`\`

**アラート:**
- P95 > 50ms → 警告（インデックス不足の可能性）

---

### カテゴリ3: エラーメトリクス

#### 7. エラー発生率

**メトリクス名:** `wallet.expiration.error_rate`
**型:** Counter
**ラベル:**
- `error_type`: `WALLET_EXPIRED`, `BATCH_FAILED`, `NOTIFICATION_FAILED`

**収集方法:**
\`\`\`typescript
try {
  await expirePoints();
} catch (error) {
  metrics.increment('wallet.expiration.error_rate', {
    tags: { error_type: error.code || 'UNKNOWN' }
  });
  throw error;
}
\`\`\`

**アラート:**
- エラー率 > 5% → 警告
- エラー率 > 10% → 緊急
```

---

### ステップ3: アラート設定

アラート条件とエスカレーションを定義:

```markdown
## アラート設定

### アラートレベル

#### 🟢 Info（情報通知）
- **通知先:** Slack #dev-info
- **対応:** 任意（営業時間内に確認）

#### 🟡 Warning（警告）
- **通知先:** Slack #dev-alerts
- **対応:** 24時間以内に確認
- **エスカレーション:** 48時間放置で PagerDuty

#### 🔴 Critical（緊急）
- **通知先:** PagerDuty（オンコール担当）
- **対応:** 即座（15分以内）
- **エスカレーション:** 30分対応なしで上位エスカレーション

---

### アラートルール

#### Alert 1: バッチ処理失敗

\`\`\`yaml
alert: WalletExpirationBatchFailed
expr: increase(wallet_expiration_error_rate{error_type="BATCH_FAILED"}[5m]) > 0
for: 0m
severity: critical
annotations:
  summary: ポイント失効バッチ処理が失敗しました
  description: "バッチ処理が {{ $value }} 回失敗しました"
actions:
  - PagerDuty: オンコール担当に通知
  - Slack: #dev-alerts に通知
  - Runbook: https://wiki.example.com/runbook/wallet-expiration-batch-failed
\`\`\`

---

#### Alert 2: 通知送信成功率低下

\`\`\`yaml
alert: ExpirationNotificationLowSuccessRate
expr: wallet_expiration_notification_success_rate < 0.95
for: 10m
severity: warning
annotations:
  summary: 有効期限通知の成功率が低下しています
  description: "成功率: {{ $value | humanizePercentage }}"
actions:
  - Slack: #dev-alerts
  - Runbook: https://wiki.example.com/runbook/notification-failure
\`\`\`

---

#### Alert 3: バッチ処理時間超過

\`\`\`yaml
alert: ExpirationBatchSlow
expr: histogram_quantile(0.95, wallet_expiration_batch_duration_seconds) > 60
for: 5m
severity: warning
annotations:
  summary: バッチ処理が遅延しています
  description: "P95実行時間: {{ $value }}秒"
actions:
  - Slack: #dev-alerts
\`\`\`

---

#### Alert 4: 異常な失効ポイント数

\`\`\`yaml
alert: AbnormalPointsExpiration
expr: increase(wallet_expiration_points_expired_total[24h]) > 100000
for: 0m
severity: warning
annotations:
  summary: 異常な量のポイントが失効しました
  description: "失効ポイント: {{ $value }}pt"
actions:
  - Slack: #dev-alerts
  - Email: product-owner@example.com
\`\`\`
```

---

### ステップ4: ダッシュボード設計

監視ダッシュボードの設計:

```markdown
## ダッシュボード設計

### Dashboard 1: ポイント有効期限 概要

**ツール:** Grafana / Datadog

#### パネル構成

##### Row 1: ビジネスメトリクス

**Panel 1.1: 失効ポイント総数（時系列）**
- グラフ: 折れ線グラフ
- クエリ: `sum(rate(wallet_expiration_points_expired_total[24h]))`
- Y軸: ポイント数
- X軸: 時間

**Panel 1.2: 失効ユーザー数（時系列）**
- グラフ: 折れ線グラフ
- クエリ: `sum(rate(wallet_expiration_users_affected_total[24h]))`

**Panel 1.3: 通知送信成功率（ゲージ）**
- グラフ: ゲージ
- クエリ: `wallet_expiration_notification_success_rate`
- 閾値:
  - 緑: >= 0.95
  - 黄: 0.8 ～ 0.95
  - 赤: < 0.8

---

##### Row 2: パフォーマンスメトリクス

**Panel 2.1: バッチ処理実行時間（ヒートマップ）**
- グラフ: ヒートマップ
- クエリ: `histogram_quantile(0.95, wallet_expiration_batch_duration_seconds)`

**Panel 2.2: データベースクエリ時間（P50/P95/P99）**
- グラフ: 折れ線グラフ（複数線）
- クエリ:
  - P50: `histogram_quantile(0.5, wallet_expiration_db_query_duration_ms)`
  - P95: `histogram_quantile(0.95, wallet_expiration_db_query_duration_ms)`
  - P99: `histogram_quantile(0.99, wallet_expiration_db_query_duration_ms)`

---

##### Row 3: エラーメトリクス

**Panel 3.1: エラー率（時系列）**
- グラフ: 折れ線グラフ
- クエリ: `sum(rate(wallet_expiration_error_rate[5m])) by (error_type)`
- 凡例: error_type別

**Panel 3.2: 最近のエラーログ（テーブル）**
- グラフ: テーブル
- データソース: Elasticsearch / CloudWatch Logs
- フィールド: timestamp, error_type, error_message, user_id

---

### Dashboard 2: リアルタイム監視

**用途:** オンコール担当者向け

#### パネル構成

**Panel 1: 現在のアラート状況**
- Active Alerts一覧
- 色分け: Critical=赤、Warning=黄

**Panel 2: 今日の失効ポイント**
- 単一値
- クエリ: `sum(increase(wallet_expiration_points_expired_total[24h]))`

**Panel 3: 直近1時間のエラー**
- ログストリーム
```

---

### ステップ5: ログ戦略

構造化ログの設計:

```markdown
## ログ戦略

### ログレベル

- **DEBUG:** 詳細なデバッグ情報（開発環境のみ）
- **INFO:** 通常の処理フロー
- **WARN:** 警告（処理は継続）
- **ERROR:** エラー（処理失敗）

---

### ログ出力

#### ログ1: バッチ処理開始

\`\`\`typescript
logger.info('Wallet expiration batch started', {
  batch_type: 'expire_points',
  timestamp: new Date().toISOString(),
  expected_count: expectedCount
});
\`\`\`

---

#### ログ2: ポイント失効実行

\`\`\`typescript
logger.info('Points expired', {
  user_id: userId,
  wallet_id: walletId,
  expired_points: expiredPoints,
  expires_at: expiresAt,
  remaining_balance: remainingBalance
});
\`\`\`

---

#### ログ3: バッチ処理完了

\`\`\`typescript
logger.info('Wallet expiration batch completed', {
  batch_type: 'expire_points',
  duration_seconds: duration,
  processed_count: processedCount,
  error_count: errorCount
});
\`\`\`

---

#### ログ4: エラー

\`\`\`typescript
logger.error('Wallet expiration batch failed', {
  error: error.message,
  error_code: error.code,
  stack_trace: error.stack,
  wallet_id: walletId
});
\`\`\`

---

### ログ集約

**ツール:** Elasticsearch / CloudWatch Logs

**インデックス:**
- `civicship-api-prod-YYYY.MM.DD`

**検索クエリ例:**
\`\`\`
# 今日の失効ポイント総数
message:"Points expired" AND @timestamp:[now-24h TO now]
| stats sum(expired_points) as total_expired

# エラー発生率
message:"batch failed" AND level:ERROR
| timechart span=5m count()
\`\`\`
```

---

### ステップ6: 監視準備チェックリスト

実装前の確認項目:

```markdown
## 監視準備チェックリスト

### メトリクス

- [ ] ビジネスメトリクスの定義完了
  - [ ] 失効ポイント総数
  - [ ] 失効ユーザー数
  - [ ] 通知送信成功率

- [ ] 技術メトリクスの定義完了
  - [ ] バッチ処理実行時間
  - [ ] データベースクエリ時間
  - [ ] API レスポンスタイム

- [ ] エラーメトリクスの定義完了
  - [ ] エラー発生率
  - [ ] エラー種別分類

---

### アラート

- [ ] アラートルールの定義完了
  - [ ] バッチ処理失敗
  - [ ] 通知送信失敗
  - [ ] パフォーマンス劣化
  - [ ] 異常値検出

- [ ] 通知先の設定完了
  - [ ] Slack #dev-alerts
  - [ ] PagerDuty（オンコール）

- [ ] Runbookの作成完了
  - [ ] バッチ処理失敗時の対処
  - [ ] ロールバック手順

---

### ダッシュボード

- [ ] Grafana / Datadogダッシュボードの作成
  - [ ] ビジネスメトリクス可視化
  - [ ] パフォーマンスメトリクス可視化
  - [ ] エラー可視化

- [ ] ダッシュボードのアクセス権限設定
  - [ ] 開発チーム: 閲覧・編集
  - [ ] プロダクトオーナー: 閲覧のみ

---

### ログ

- [ ] 構造化ログの実装
  - [ ] JSON形式
  - [ ] 必要なフィールド含む

- [ ] ログ集約の設定
  - [ ] Elasticsearch / CloudWatch Logs
  - [ ] 検索クエリの作成

- [ ] ログ保持期間の設定
  - [ ] 本番: 90日
  - [ ] ステージング: 30日

---

### テスト

- [ ] メトリクス収集のテスト
  - [ ] ステージング環境で確認
  - [ ] メトリクスが正しく送信されるか

- [ ] アラート発火のテスト
  - [ ] 手動でアラート条件を満たす
  - [ ] 通知が正しく届くか

- [ ] ダッシュボード表示のテスト
  - [ ] データが正しく表示されるか
```

---

### ステップ7: 監視準備レポート生成

```markdown
# 監視準備レポート

**機能:** ポイント有効期限機能
**作成日:** 2026-01-15

---

## 監視要件サマリー

### メトリクス

- **ビジネスメトリクス:** 3個
- **技術メトリクス:** 3個
- **エラーメトリクス:** 1個
- **合計:** 7個

### アラート

- **Critical:** 2個
- **Warning:** 2個
- **合計:** 4個

### ダッシュボード

- **概要ダッシュボード:** 1個（9パネル）
- **リアルタイムダッシュボード:** 1個（3パネル）

---

## 実装工数

| タスク | 工数 |
|--------|------|
| メトリクス実装 | 4h |
| アラート設定 | 2h |
| ダッシュボード作成 | 3h |
| ログ実装 | 2h |
| テスト | 2h |
| **合計** | **13h** |

---

## 承認

- [ ] テックリード
- [ ] DevOpsリード
- [ ] プロダクトオーナー
```

---

## 活用例

### 例1: 新機能の監視要件

```bash
/monitoring-readiness "ポイント有効期限機能"
```

**出力:**
- メトリクス設計
- アラート設定
- ダッシュボード設計

---

### 例2: 既存機能の監視強化

```bash
/monitoring-readiness wallet --enhance
```

**出力:**
- 既存監視の評価
- 追加すべきメトリクス

---

## 参考資料

- [Prometheus Best Practices](https://prometheus.io/docs/practices/)
- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)
- [Site Reliability Engineering](https://sre.google/books/)
