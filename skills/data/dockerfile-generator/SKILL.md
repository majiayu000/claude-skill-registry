---
name: dockerfile-generator
description: Generate optimized Dockerfiles with multi-stage builds and best practices. Use when containerizing applications or creating Docker configurations.
---

# Dockerfile Generator Skill

最適化されたDockerfileを生成するスキルです。

## 概要

プロジェクトの種類に応じた、セキュアで効率的なDockerfileを自動生成します。

## 主な機能

- **マルチステージビルド**: イメージサイズ削減
- **セキュリティ**: 非rootユーザー、最小権限
- **キャッシュ最適化**: ビルド時間短縮
- **ベストプラクティス**: Docker推奨設定
- **複数言語対応**: Node.js、Python、Go、Java等

## 生成例

### Node.js (Express)

```dockerfile
# マルチステージビルド
FROM node:18-alpine AS builder

WORKDIR /app

# 依存関係のみ先にコピー（キャッシュ最適化）
COPY package*.json ./
RUN npm ci --only=production

# ソースコードコピー
COPY . .

# 本番イメージ
FROM node:18-alpine

# 非rootユーザー作成
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

WORKDIR /app

# ビルド成果物をコピー
COPY --from=builder --chown=nodejs:nodejs /app/node_modules ./node_modules
COPY --chown=nodejs:nodejs . .

USER nodejs

EXPOSE 3000

CMD ["node", "server.js"]
```

### Python (FastAPI)

```dockerfile
FROM python:3.11-slim AS builder

WORKDIR /app

# システム依存関係
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Python依存関係
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# 本番イメージ
FROM python:3.11-slim

RUN adduser --disabled-password --gecos '' appuser

WORKDIR /app

# ビルドしたパッケージをコピー
COPY --from=builder /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

USER appuser

ENV PATH=/home/appuser/.local/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Go

```dockerfile
# ビルドステージ
FROM golang:1.21-alpine AS builder

WORKDIR /app

# 依存関係
COPY go.mod go.sum ./
RUN go mod download

# ビルド
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

# 最小イメージ
FROM scratch

COPY --from=builder /app/main /main

EXPOSE 8080

ENTRYPOINT ["/main"]
```

### React (静的サイト)

```dockerfile
# ビルドステージ
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# Nginxで配信
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

## .dockerignore

```
node_modules
npm-debug.log
.git
.gitignore
README.md
.env
.DS_Store
*.log
dist
build
coverage
```

## docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  database:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

volumes:
  postgres_data:
```

## ベストプラクティス

1. **マルチステージビルド**: イメージサイズ削減
2. **レイヤーキャッシュ**: 変更の少ないファイルから順に
3. **非rootユーザー**: セキュリティ向上
4. **.dockerignore**: 不要ファイル除外
5. **ヘルスチェック**: コンテナ監視

## バージョン情報

- スキルバージョン: 1.0.0
