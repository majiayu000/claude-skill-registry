---
name: database-adapter
description: データベースアダプター（PostgreSQL/MySQL両対応）の開発・修正を行う際に使用。SqlExecutorパターン、マイグレーション、DB固有SQL実装時に役立つ。
---

# データベースアダプター開発ガイド

## ドキュメント

- `libs/idp-server-database/README.md` - データベース設計・マイグレーション
- `documentation/docs/content_10_ai_developer/ai-20-adapters.md` - アダプター実装ガイド
- `documentation/docs/content_10_ai_developer/ai-21-core-adapter.md` - Core Adapterガイド
- `documentation/docs/content_10_ai_developer/ai-22-database.md` - データベースガイド

---

## 機能概要

データベースアダプターは、PostgreSQL/MySQL両方をサポートする永続化層。
- **両DB対応**: 全機能でPostgreSQL/MySQL両方実装必須
- **SqlExecutorパターン**: DB固有SQLを抽象化
- **Flyway**: マイグレーション管理
- **読み書き分離**: `@Transaction` / `@Transaction(readOnly = true)` アノテーション

---

## モジュール構成

```
libs/
├── idp-server-core-adapter/                    # 永続化実装
│   └── .../adapters/datasource/
│       ├── audit/
│       │   ├── command/
│       │   │   ├── AuditLogSqlExecutor.java       # インターフェース
│       │   │   ├── AuditLogSqlExecutors.java      # ファクトリ
│       │   │   ├── PostgresqlExecutor.java        # PostgreSQL実装
│       │   │   └── MysqlExecutor.java             # MySQL実装
│       │   └── query/
│       │       └── (同様の構造)
│       ├── token/
│       ├── identity/
│       ├── authentication/
│       ├── ciba/
│       └── ...
│
├── idp-server-database/                        # マイグレーション
│   ├── postgresql/
│   │   ├── V0_9_0__init_lib.sql               # 初期スキーマ
│   │   └── V1_0_0__*.sql                      # バージョン別マイグレーション
│   └── mysql/
│       ├── V0_9_0__init_lib.mysql.sql         # ※ .mysql.sql 接尾辞
│       └── V0_9_21_1__*.mysql.sql
│
└── idp-server-platform/                        # 共通基盤
    └── .../datasource/
        ├── DatabaseType.java                   # POSTGRESQL, SPANNER, MYSQL
        ├── SqlExecutor.java                    # SQL実行ヘルパー
        └── TransactionManager.java             # トランザクション管理
```

---

## SqlExecutor パターン

### 基本構造

`AuditLogSqlExecutor.java`:

```java
// 1. インターフェース定義（Tenant第一引数）
public interface AuditLogSqlExecutor {
    void insert(Tenant tenant, AuditLog auditLog);
}
```

`PostgresqlExecutor.java`:

```java
// 2. PostgreSQL実装
public class PostgresqlExecutor implements AuditLogSqlExecutor {
    @Override
    public void insert(Tenant tenant, AuditLog auditLog) {
        // SqlExecutorが内部でTransactionManager.getConnection()を使用
        SqlExecutor sqlExecutor = new SqlExecutor();
        String sqlTemplate = """
            INSERT INTO audit_log (
                id, type, description, tenant_id, client_id, user_id, ...
            ) VALUES (
                ?::uuid, ?, ?, ?::uuid, ...
            );
            """;
        List<Object> params = new ArrayList<>();
        params.add(auditLog.id().value());
        // ...
        sqlExecutor.execute(sqlTemplate, params);
    }
}
```

`MysqlExecutor.java`:

```java
// 3. MySQL実装
public class MysqlExecutor implements AuditLogSqlExecutor {
    @Override
    public void insert(Tenant tenant, AuditLog auditLog) {
        SqlExecutor sqlExecutor = new SqlExecutor();
        String sqlTemplate = """
            INSERT INTO audit_log (
                id, type, description, tenant_id, client_id, user_id, ...
            ) VALUES (
                ?, ?, ?, ?, ...
            );
            """;
        // MySQL固有: UUIDキャストなし
        // ...
    }
}
```

`AuditLogSqlExecutors.java`:

```java
// 4. ファクトリ（ディスパッチャー）
public class AuditLogSqlExecutors {
    Map<DatabaseType, AuditLogSqlExecutor> executors;

    public AuditLogSqlExecutors() {
        executors = new HashMap<>();
        executors.put(DatabaseType.POSTGRESQL, new PostgresqlExecutor());
        executors.put(DatabaseType.MYSQL, new MysqlExecutor());
    }

    public AuditLogSqlExecutor get(DatabaseType databaseType) {
        return executors.get(databaseType);
    }
}
```

---

## 読み書き分離

EntryServiceレイヤーで `@Transaction` アノテーションにより制御:

```java
// 書き込み（Primary）
@Transaction
public class OAuthFlowEntryService { ... }

// 読み取り専用（Replica）
@Transaction(readOnly = true)
public class UserinfoEntryService { ... }

@Transaction(readOnly = true)
public class OidcMetaDataEntryService { ... }
```

---

## PostgreSQL vs MySQL 差異

### INSERT時の競合処理

| 操作 | PostgreSQL | MySQL |
|------|-----------|-------|
| UPSERT | `ON CONFLICT (id) DO UPDATE SET ...` | `ON DUPLICATE KEY UPDATE ...` |
| INSERT IGNORE | `ON CONFLICT DO NOTHING` | `INSERT IGNORE INTO ...` |

### UUID型

| 操作 | PostgreSQL | MySQL |
|------|-----------|-------|
| UUIDキャスト | `?::uuid` | `?` (文字列として保存) |

### JSON操作

| 操作 | PostgreSQL | MySQL |
|------|-----------|-------|
| JSON型 | `jsonb` | `JSON` |
| JSON抽出 | `column->>'key'` | `JSON_UNQUOTE(JSON_EXTRACT(column, '$.key'))` |
| JSON検索 | `column @> '{"key": "value"}'` | `JSON_CONTAINS(column, '"value"', '$.key')` |

### 日時操作

| 操作 | PostgreSQL | MySQL |
|------|-----------|-------|
| 現在時刻 | `NOW()` | `NOW()` |
| タイムゾーン | `AT TIME ZONE 'UTC'` | `CONVERT_TZ(..., '+00:00', 'UTC')` |
| 間隔 | `INTERVAL '1 day'` | `INTERVAL 1 DAY` |

---

## マイグレーション

### ファイル命名規則

```
PostgreSQL: V{major}_{minor}_{patch}__{description}.sql
MySQL:      V{major}_{minor}_{patch}__{description}.mysql.sql

例:
- postgresql/V1_2_0__add_user_status_column.sql
- mysql/V1_2_0__add_user_status_column.mysql.sql
```

**注意**: MySQLは `.mysql.sql` 接尾辞が必須。

### 実行方法

```bash
# Docker経由（推奨）
docker compose up flyway-migrator

# 直接実行
./gradlew :libs:idp-server-database:flywayMigrate
```

### 両DB対応マイグレーション

PostgreSQL と MySQL で同じバージョン番号のファイルを作成:

```
libs/idp-server-database/
├── postgresql/
│   └── V1_2_0__add_user_status_column.sql
└── mysql/
    └── V1_2_0__add_user_status_column.mysql.sql
```

---

## Command / Query 分離

### 構造パターン

```
datasource/{domain}/
├── command/                    # 書き込み操作
│   ├── {Domain}CommandSqlExecutor.java
│   ├── {Domain}CommandSqlExecutors.java
│   ├── PostgresqlExecutor.java
│   └── MysqlExecutor.java
└── query/                      # 読み取り操作
    ├── {Domain}QuerySqlExecutor.java
    ├── {Domain}QuerySqlExecutors.java
    ├── PostgresqlExecutor.java
    └── MysqlExecutor.java
```

---

## DatabaseType

`DatabaseType.java`:

```java
public enum DatabaseType {
    POSTGRESQL,
    SPANNER,     // Google Cloud Spanner
    MYSQL;
}
```

---

## コマンド

```bash
# ビルド
./gradlew :libs:idp-server-core-adapter:compileJava
./gradlew :libs:idp-server-database:build

# マイグレーション確認
./gradlew :libs:idp-server-database:flywayInfo

# テスト
./gradlew :libs:idp-server-core-adapter:test
```

---

## チェックリスト

新規DataSource実装時:

- [ ] SqlExecutor インターフェース作成（Tenant第一引数）
- [ ] PostgresqlExecutor 実装
- [ ] MysqlExecutor 実装
- [ ] SqlExecutors ファクトリ作成
- [ ] DataSource クラス作成
- [ ] PostgreSQL マイグレーション追加（.sql）
- [ ] MySQL マイグレーション追加（.mysql.sql）
- [ ] 両DBでテスト実行

---

## トラブルシューティング

### SQL構文エラー

| 問題 | 原因 | 解決策 |
|------|------|--------|
| PostgreSQLで動くがMySQLでエラー | DB固有構文の混在 | 両Executor実装を確認 |
| UUIDキャストエラー | `?::uuid`がMySQLで失敗 | MySQL版では文字列として扱う |
| JSONクエリ失敗 | JSON関数の差異 | 上記JSON操作表を参照 |

### マイグレーション失敗

| 問題 | 原因 | 解決策 |
|------|------|--------|
| MySQLでファイル認識されない | 接尾辞が`.sql` | `.mysql.sql`に変更 |
| バージョン競合 | 既存マイグレーションとの衝突 | `flyway repair` 実行 |
| スキーマ不整合 | 手動変更との不一致 | `docker compose down -v` で初期化 |

---

## 関連スキル

| スキル | 用途 |
|--------|------|
| `/local-environment` | ローカルDB環境構築 |
| `/architecture` | アーキテクチャ全体像 |
| `/operations` | 運用・監視 |
