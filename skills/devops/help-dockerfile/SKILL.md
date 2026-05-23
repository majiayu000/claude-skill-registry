---
name: help-dockerfile
description: Dockerfile の作成・改善を支援する。「Dockerfile を作って」「Dockerfile 作成」「Dockerfile をレビュー」「Dockerfile 改善」「Dockerfile 最適化」「Dockerfile lint」「マルチステージビルド」「alpine 化」「イメージサイズ削減」「Dockerfile のベストプラクティス」などで起動。
allowed-tools: [Read, Write, Edit, Glob, Bash]
context: fork
agent: shiiman-docker:dockerfile-reviewer
---

# Help Dockerfile

Dockerfile の作成・改善を支援します。

## 対応操作

| 操作 | トリガー例 |
|------|-----------|
| 新規作成 | 「Dockerfile を作って」「Dockerfile 作成」 |
| レビュー/Lint | 「Dockerfile をレビュー」「Dockerfile lint」「Dockerfile 改善」 |
| 最適化 | 「マルチステージビルド」「alpine 化」「サイズ削減」 |

## 実行手順

### 1. 意図の判定

- **新規作成**: 「作って」「作成」「生成」→ 新しい Dockerfile を作成
- **レビュー/Lint**: 「レビュー」「lint」「改善」「チェック」→ Dockerfile を静的解析
- **最適化**: 「最適化」「alpine」「マルチステージ」「サイズ削減」→ 既存 Dockerfile を最適化

### 2. 新規作成の場合

#### プロジェクトの言語/フレームワーク特定

```bash
ls package.json go.mod requirements.txt Gemfile pom.xml build.gradle Cargo.toml 2>/dev/null
```

#### 言語別テンプレート生成

**Node.js** (`package.json` 検出時):

```dockerfile
# Build stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci

# Production stage
FROM node:20-alpine
RUN addgroup -S app && adduser -S app -G app
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
USER app
EXPOSE 3000
CMD ["node", "index.js"]
```

**Go** (`go.mod` 検出時):

```dockerfile
# Build stage
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.* ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# Production stage
FROM scratch
COPY --from=builder /app/main /main
ENTRYPOINT ["/main"]
```

**Python** (`requirements.txt` 検出時):

```dockerfile
# Build stage
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --target=/app/deps -r requirements.txt

# Production stage
FROM python:3.12-slim
RUN useradd -m -r app
WORKDIR /app
ENV PYTHONPATH=/app/deps
COPY --from=builder /app/deps /app/deps
COPY . .
USER app
CMD ["python", "main.py"]
```

#### .dockerignore も同時に作成

```
.git
.gitignore
README.md
Dockerfile*
docker-compose*
.env*
*.log
node_modules
__pycache__
*.pyc
.pytest_cache
coverage
.coverage
dist
build
*.egg-info
```

### 3. レビュー/Lint の場合

Dockerfile の静的解析を行い、ベストプラクティスに基づいた提案をします。

#### Dockerfile の存在確認

```bash
ls Dockerfile* docker/Dockerfile* 2>/dev/null
```

#### ベストプラクティスに基づいてチェック

以下の観点で解析:

**セキュリティ（重要度: 高）**:

| チェック | 問題 | 推奨 |
|----------|------|------|
| `USER` 指定 | root で実行 | 非 root ユーザーを指定 |
| 機密情報 | ハードコードされた秘密 | ARG/ENV + ビルド時注入 |
| `ADD` vs `COPY` | リモート URL や tar 展開 | `COPY` を優先 |
| `apt-get` | キャッシュ残存 | `rm -rf /var/lib/apt/lists/*` |

**パフォーマンス（重要度: 中）**:

| チェック | 問題 | 推奨 |
|----------|------|------|
| マルチステージ | 単一ステージで大きいイメージ | マルチステージビルド |
| レイヤー最適化 | 複数の `RUN` | 1つの `RUN` に結合 |
| `.dockerignore` | 不要ファイルのコピー | `.dockerignore` を作成 |
| ベースイメージ | フルイメージ使用 | alpine/slim を検討 |

**メンテナンス性（重要度: 低）**:

| チェック | 問題 | 推奨 |
|----------|------|------|
| タグ固定 | `FROM node:latest` | `FROM node:20-alpine` |
| `LABEL` | メタデータなし | `LABEL` で情報追加 |
| `WORKDIR` | 相対パス使用 | 絶対パスを指定 |

#### 出力フォーマット（Lint）

```
## Dockerfile 解析結果

**ファイル**: {path}
**ベースイメージ**: {base_image}
**ステージ数**: {stages}

---

### 問題点

| 重要度 | 行 | カテゴリ | 内容 | 推奨 |
|--------|-----|----------|------|------|
| 🔴 高 | 1 | セキュリティ | `FROM node:latest` | タグを固定: `FROM node:20-alpine` |
| 🔴 高 | 25 | セキュリティ | root ユーザーで実行 | `USER node` を追加 |
| 🟡 中 | 10-15 | パフォーマンス | 複数の RUN 命令 | 1つの RUN に結合 |
| 🟢 低 | - | メンテナンス | LABEL がない | メタデータを追加 |

---

### 改善版 Dockerfile（参考）

{最適化された Dockerfile の例}
```

### 4. 最適化の場合

既存の Dockerfile を読み込み、以下の観点で最適化:

#### マルチステージビルド化

単一ステージの Dockerfile をマルチステージに変換:

```dockerfile
# Before
FROM node:20
WORKDIR /app
COPY . .
RUN npm install
CMD ["npm", "start"]

# After
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY . .
CMD ["npm", "start"]
```

#### alpine 化

フルイメージを alpine に変更:

| Before | After | サイズ削減 |
|--------|-------|-----------|
| `node:20` | `node:20-alpine` | ~900MB → ~180MB |
| `python:3.12` | `python:3.12-slim` | ~1GB → ~150MB |
| `golang:1.22` | `golang:1.22-alpine` | ~800MB → ~250MB |

#### レイヤー最適化

```dockerfile
# Before
RUN apt-get update
RUN apt-get install -y curl
RUN apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*

# After
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        git && \
    rm -rf /var/lib/apt/lists/*
```

### 5. 出力フォーマット

```
## Dockerfile 作成完了

**ファイル**: Dockerfile
**ベースイメージ**: {base_image}
**ステージ数**: {stages}
**推定サイズ**: {estimated_size}

### 特徴

- ✅ マルチステージビルド
- ✅ 非 root ユーザー
- ✅ alpine ベースイメージ
- ✅ .dockerignore 同梱

### 次のステップ

1. `docker build -t myapp .` でビルド
2. `docker run -p 3000:3000 myapp` で実行
```

## 注意事項

- ✅ マルチステージビルドを推奨
- ✅ alpine/slim イメージを推奨
- ✅ 非 root ユーザーでの実行を推奨
- ✅ .dockerignore を同時に作成
- ✅ レビューは `/shiiman-docker:lint` に委譲（SSOT）
- ❌ 機密情報をハードコードしない
