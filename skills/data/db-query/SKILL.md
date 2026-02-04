---
name: db-query
description: "データベースクエリ・分析支援。SQLクエリの作成、実行、結果の分析を行う。BigQuery、PostgreSQL、MySQL対応。トリガー: /db-query, SQL, クエリ, データ分析, BigQuery"
user-invocable: true
allowed-tools: Bash, Read, Grep, Glob
model: sonnet
---

# データベースクエリ・分析スキル

SQLクエリの作成、実行、結果の分析を支援します。

## 対応データベース

| DB | CLIツール | 接続方法 |
|----|----------|---------|
| BigQuery | `bq` | `bq query --use_legacy_sql=false` |
| PostgreSQL | `psql` | `psql -h host -U user -d db` |
| MySQL | `mysql` | `mysql -h host -u user -p db` |
| SQLite | `sqlite3` | `sqlite3 file.db` |

## 機能

### 1. クエリ作成支援

自然言語からSQLを生成:

```
ユーザー: 「先月のアクティブユーザー数を日別で」

生成SQL:
SELECT
  DATE(created_at) AS date,
  COUNT(DISTINCT user_id) AS active_users
FROM events
WHERE created_at >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH)
  AND event_type = 'login'
GROUP BY date
ORDER BY date;
```

### 2. クエリ実行

```bash
# BigQuery
bq query --use_legacy_sql=false --format=prettyjson '
SELECT ...
'

# PostgreSQL
psql -c "SELECT ..." -h $DB_HOST -U $DB_USER -d $DB_NAME

# MySQL
mysql -e "SELECT ..." -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_NAME
```

### 3. 結果分析

```markdown
## クエリ結果分析

### データサマリー
- **行数**: 1,234
- **期間**: 2025-01-01 〜 2025-01-31

### 主要な発見
1. 1/15に急増（前日比 +150%）
2. 週末は平日の60%程度
3. 平均: 1,000 users/day

### 可視化
| 日付 | ユーザー数 | 傾向 |
|------|-----------|------|
| 1/1  | 500       | ▂ |
| 1/2  | 800       | ▅ |
| 1/15 | 2000      | █ |
```

## クエリパターン集

### ユーザー分析

```sql
-- DAU/WAU/MAU
SELECT
  COUNT(DISTINCT CASE WHEN DATE(ts) = CURRENT_DATE() THEN user_id END) AS dau,
  COUNT(DISTINCT CASE WHEN ts >= DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY) THEN user_id END) AS wau,
  COUNT(DISTINCT CASE WHEN ts >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY) THEN user_id END) AS mau
FROM events;

-- リテンション
WITH cohort AS (
  SELECT
    user_id,
    DATE(MIN(created_at)) AS cohort_date
  FROM users
  GROUP BY user_id
)
SELECT
  cohort_date,
  COUNT(DISTINCT c.user_id) AS cohort_size,
  COUNT(DISTINCT CASE WHEN DATE(e.ts) = DATE_ADD(cohort_date, INTERVAL 7 DAY) THEN c.user_id END) AS day7_retained
FROM cohort c
LEFT JOIN events e ON c.user_id = e.user_id
GROUP BY cohort_date;
```

### パフォーマンス分析

```sql
-- スロークエリ (PostgreSQL)
SELECT
  query,
  calls,
  total_time / 1000 AS total_seconds,
  mean_time / 1000 AS mean_seconds
FROM pg_stat_statements
ORDER BY total_time DESC
LIMIT 10;

-- テーブルサイズ
SELECT
  schemaname,
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname || '.' || tablename)) AS size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname || '.' || tablename) DESC
LIMIT 10;
```

### エラー分析

```sql
-- エラー頻度
SELECT
  error_code,
  error_message,
  COUNT(*) AS count,
  MIN(ts) AS first_seen,
  MAX(ts) AS last_seen
FROM error_logs
WHERE ts >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
GROUP BY error_code, error_message
ORDER BY count DESC;
```

## 出力形式

```markdown
## クエリ実行結果

### クエリ
```sql
SELECT ...
```

### 実行情報
- **データベース**: BigQuery / production
- **実行時間**: 2.3秒
- **スキャン量**: 1.2 GB
- **結果行数**: 1,234

### 結果

| date | active_users | change |
|------|-------------|--------|
| 2025-01-01 | 1,000 | - |
| 2025-01-02 | 1,200 | +20% |
| 2025-01-03 | 950 | -21% |

### 分析

**トレンド**:
- 全体的に横ばい
- 週末に減少傾向

**異常値**:
- 1/15 に急増（イベント影響？）

**推奨アクション**:
1. 1/15 の急増要因を調査
2. 週末施策の検討
```

## セキュリティ注意事項

### 必須ルール

- **SELECT文のみ実行**: DELETE, UPDATE, DROP, INSERT, TRUNCATE, ALTER は絶対に実行しない
- **本番DBへの直接接続は避ける**: 可能な限りレプリカを使用
- **結果の取り扱い**: 個人情報を含む場合は注意
- **クエリログ**: 実行したクエリは記録される前提で

### 安全なクエリ実行

```bash
# PostgreSQL: 読み取り専用トランザクションを使用
psql -c "SET TRANSACTION READ ONLY; SELECT ..." -h $DB_HOST -U $DB_USER -d $DB_NAME

# MySQL: 読み取り専用フラグ
mysql --safe-updates -e "SELECT ..." -h $DB_HOST -u $DB_USER $DB_NAME

# BigQuery: ドライランで事前確認
bq query --dry_run --use_legacy_sql=false 'SELECT ...'
```

### 禁止パターン検出

実行前にクエリを検証し、以下のパターンが含まれる場合は**実行を拒否**:

- `DELETE`, `UPDATE`, `INSERT`, `DROP`, `TRUNCATE`, `ALTER`, `CREATE`
- `; --` (SQLインジェクションパターン)
- `GRANT`, `REVOKE` (権限操作)

## BigQuery 固有

```bash
# テーブル一覧
bq ls project:dataset

# スキーマ確認
bq show --schema project:dataset.table

# クエリ実行（ドライラン）
bq query --dry_run --use_legacy_sql=false 'SELECT ...'

# 結果をテーブルに保存
bq query --destination_table=project:dataset.result 'SELECT ...'
```

## 使用方法

```bash
# 自然言語でクエリ作成
/db-query 先月のDAUを日別で出して

# SQLを直接実行
/db-query --execute "SELECT COUNT(*) FROM users"

# スキーマ確認
/db-query --schema users
```
