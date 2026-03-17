---
name: tech-stack-configs
description: container-use環境の技術スタック別設定例とDBマイグレーションテスト手順
---

# 技術スタック別 container-use 設定

container-use環境で各技術スタックを使用するための設定例とDBマイグレーションテスト手順。

---

## 技術スタック別設定例

### Node.js / TypeScript

```python
config = {
    "base_image": "node:20-slim",
    "setup_commands": [
        "npm ci",
        "npx playwright install chromium --with-deps"
    ],
    "envs": [
        "NODE_ENV=test",
        "DATABASE_URL=postgresql://app:password@postgres:5432/testdb"
    ]
}
```

### Python / FastAPI

```python
config = {
    "base_image": "python:3.11-slim",
    "setup_commands": [
        "pip install --no-cache-dir -r requirements.txt",
        "pip install --no-cache-dir -r requirements-dev.txt"
    ],
    "envs": [
        "PYTHONPATH=/workspace",
        "DATABASE_URL=postgresql://app:password@postgres:5432/testdb"
    ]
}
```

### Go

```python
config = {
    "base_image": "golang:1.21-alpine",
    "setup_commands": [
        "go mod download",
        "go install github.com/golang-migrate/migrate/v4/cmd/migrate@latest"
    ],
    "envs": [
        "CGO_ENABLED=0",
        "DATABASE_URL=postgres://app:password@postgres:5432/testdb?sslmode=disable"
    ]
}
```

### Rust

```python
config = {
    "base_image": "rust:1.85-slim",
    "setup_commands": [
        "cargo fetch",
        "cargo build --release"
    ],
    "envs": [
        "DATABASE_URL=postgres://app:password@postgres:5432/testdb"
    ]
}
```

---

## サービス追加例

### PostgreSQL

```python
container-use_environment_add_service(
    environment_source="/path/to/repo",
    environment_id=env_id,
    name="postgres",
    image="postgres:15-alpine",
    envs=[
        "POSTGRES_USER=app",
        "POSTGRES_PASSWORD=password",
        "POSTGRES_DB=testdb"
    ],
    ports=[5432],
    explanation="Add PostgreSQL for database tests"
)
```

### MySQL

```python
container-use_environment_add_service(
    environment_source="/path/to/repo",
    environment_id=env_id,
    name="mysql",
    image="mysql:8",
    envs=[
        "MYSQL_ROOT_PASSWORD=root",
        "MYSQL_DATABASE=testdb",
        "MYSQL_USER=app",
        "MYSQL_PASSWORD=password"
    ],
    ports=[3306],
    explanation="Add MySQL for database tests"
)
```

### Redis

```python
container-use_environment_add_service(
    environment_source="/path/to/repo",
    environment_id=env_id,
    name="redis",
    image="redis:7-alpine",
    ports=[6379],
    explanation="Add Redis for caching tests"
)
```

---

## DBマイグレーションのテスト

### Flyway (SQL migrations)

```python
# マイグレーション実行
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="flyway -url=jdbc:postgresql://postgres:5432/testdb -user=app -password=password migrate",
    explanation="Run Flyway migrations"
)

# ロールバック
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="flyway -url=jdbc:postgresql://postgres:5432/testdb -user=app -password=password undo",
    explanation="Rollback last migration"
)
```

### Prisma (TypeScript)

```python
# マイグレーション実行
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="npx prisma migrate deploy",
    explanation="Run Prisma migrations"
)

# リセット (開発用)
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="npx prisma migrate reset --force",
    explanation="Reset database and rerun migrations"
)
```

### SQLAlchemy / Alembic (Python)

```python
# マイグレーション実行
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="alembic upgrade head",
    explanation="Run Alembic migrations"
)

# ロールバック
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="alembic downgrade -1",
    explanation="Rollback one migration"
)
```

---

## サービス起動待機

```python
# PostgreSQL起動待ち
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="until pg_isready -h postgres -p 5432; do sleep 1; done",
    explanation="Wait for PostgreSQL to be ready"
)

# MySQL起動待ち
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="until mysqladmin ping -h mysql --silent; do sleep 1; done",
    explanation="Wait for MySQL to be ready"
)

# Redis起動待ち
container-use_environment_run_cmd(
    environment_id=env_id,
    environment_source="/path/to/repo",
    command="until redis-cli -h redis ping; do sleep 1; done",
    explanation="Wait for Redis to be ready"
)
```

---

## ネイティブモジュール対応

一部のnpmパッケージはネイティブモジュールのビルドが必要です：

```python
config = {
    "base_image": "node:20-slim",
    "setup_commands": [
        "apt-get update && apt-get install -y build-essential python3",
        "npm ci"
    ]
}
```

| パッケージ | 必要なパッケージ |
|-----------|----------------|
| `bcrypt` | `build-essential`, `python3` |
| `canvas` | `libcairo2-dev`, `libpango1.0-dev` |
| `sharp` | `libvips-dev` |
| `sqlite3` | `build-essential`, `python3` |
