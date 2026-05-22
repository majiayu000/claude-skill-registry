---
name: sql-query-helper
description: Generate, optimize, and explain SQL queries with best practices. Use when writing database queries or optimizing SQL performance.
---

# SQL Query Helper Skill

SQLクエリを生成・最適化・説明するスキルです。

## 概要

自然言語からSQL クエリを生成し、既存クエリを最適化します。

## 主な機能

- **クエリ生成**: 要件からSQL を自動生成
- **クエリ最適化**: インデックス活用、N+1解消
- **クエリ説明**: 複雑なクエリを人間が読める形で説明
- **パフォーマンス分析**: EXPLAIN プランの解釈
- **マイグレーション**: DDL文の生成
- **データベース対応**: PostgreSQL、MySQL、SQLite、SQL Server

## 使用方法

```
以下の要件でSQLクエリを生成：
テーブル: users, orders
条件: 2024年に3回以上注文したユーザーのリスト
ソート: 注文回数の降順
```

## 生成例

### 基本的なSELECT

**要件**: アクティブユーザーのメールアドレス一覧

**生成クエリ**:
```sql
SELECT email
FROM users
WHERE active = true
ORDER BY email;
```

### JOIN クエリ

**要件**: ユーザーとその注文の一覧（注文がないユーザーも含む）

**生成クエリ**:
```sql
SELECT
    u.id,
    u.name,
    u.email,
    o.id AS order_id,
    o.total,
    o.created_at AS order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
ORDER BY u.id, o.created_at DESC;
```

### 集計クエリ

**要件**: ユーザー毎の総購入金額（購入あり のみ）

**生成クエリ**:
```sql
SELECT
    u.id,
    u.name,
    COUNT(o.id) AS order_count,
    SUM(o.total) AS total_spent,
    AVG(o.total) AS avg_order_value
FROM users u
INNER JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 0
ORDER BY total_spent DESC;
```

### サブクエリ

**要件**: 平均以上の注文金額のユーザー

**生成クエリ**:
```sql
SELECT
    u.name,
    o.total
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.total > (
    SELECT AVG(total)
    FROM orders
)
ORDER BY o.total DESC;
```

## クエリ最適化

### N+1 問題の解決

**非効率（N+1）**:
```sql
-- 1. すべてのユーザーを取得
SELECT * FROM users;

-- 2. 各ユーザーの注文を個別に取得（Nクエリ）
SELECT * FROM orders WHERE user_id = 1;
SELECT * FROM orders WHERE user_id = 2;
-- ... (ユーザー数だけ繰り返し)
```

**最適化（1クエリ）**:
```sql
SELECT
    u.*,
    o.*
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

### インデックス活用

**遅いクエリ**:
```sql
SELECT * FROM users
WHERE email = 'user@example.com';  -- インデックスなし
```

**インデックス追加**:
```sql
CREATE INDEX idx_users_email ON users(email);
```

**最適化後**:
```sql
-- 同じクエリでも高速化
SELECT * FROM users
WHERE email = 'user@example.com';  -- インデックス使用
```

### WHERE vs HAVING

**非効率**:
```sql
SELECT user_id, COUNT(*) as order_count
FROM orders
GROUP BY user_id
HAVING user_id > 100;  -- GROUP BY後にフィルタ
```

**最適化**:
```sql
SELECT user_id, COUNT(*) as order_count
FROM orders
WHERE user_id > 100  -- GROUP BY前にフィルタ
GROUP BY user_id;
```

### EXISTS vs IN

**大量データで遅い**:
```sql
SELECT * FROM users
WHERE id IN (SELECT user_id FROM orders);
```

**最適化**:
```sql
SELECT * FROM users u
WHERE EXISTS (
    SELECT 1 FROM orders o
    WHERE o.user_id = u.id
);
```

## クエリ説明

**入力**:
```sql
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.created_at > '2024-01-01'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 3
ORDER BY order_count DESC
LIMIT 10;
```

**説明**:
```markdown
このクエリは、**2024年以降に登録したユーザーの中で、4回以上注文したユーザーのトップ10**を取得します。

実行順序:
1. FROM: users テーブルを基準に
2. LEFT JOIN: orders テーブルを結合（注文がなくてもユーザーは含まれる）
3. WHERE: 2024年1月1日以降に作成されたユーザーのみ
4. GROUP BY: ユーザーごとにグループ化
5. HAVING: 注文が4回以上のグループのみ
6. SELECT: ユーザー名と注文数を選択
7. ORDER BY: 注文数の降順
8. LIMIT: 上位10件のみ

結果:
- 列: name（ユーザー名）、order_count（注文回数）
- 行数: 最大10行
```

## DDL生成

**要件**: ユーザーテーブルの作成

**生成DDL**:
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(active);
CREATE INDEX idx_users_created_at ON users(created_at);
```

## データベース別の違い

### PostgreSQL
```sql
-- RETURNING句
INSERT INTO users (name, email)
VALUES ('John', 'john@example.com')
RETURNING id, created_at;

-- ARRAY型
SELECT ARRAY_AGG(name) FROM users;
```

### MySQL
```sql
-- AUTO_INCREMENT
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY
);

-- LIMIT OFFSET
SELECT * FROM users LIMIT 10 OFFSET 20;
```

### SQLite
```sql
-- AUTOINCREMENT
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT
);
```

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22

---

**使用例**:

```
SQLクエリを生成：
- テーブル: products, categories
- 取得: カテゴリ別の商品数と平均価格
- 条件: 在庫ありの商品のみ
- ソート: 商品数の多い順
```

最適化されたSQLクエリが生成されます！
