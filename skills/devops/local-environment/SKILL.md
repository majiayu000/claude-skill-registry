---
name: local-environment
description: ローカル開発環境の構築・設定を行う際に使用。Docker Compose、サブドメイン設定、データベース構成、SSL証明書、トラブルシューティングに役立つ。
---

# ローカル開発環境ガイド

## ドキュメント

- `documentation/docs/content_02_quickstart/quickstart-01-getting-started.md` - クイックスタート
  - 「ローカル環境のリソースチューニング」セクション - Docker/PostgreSQL/HikariCP/nginx設定
- `documentation/docs/content_11_learning/26-performance-tuning/` - パフォーマンスチューニングガイド
- `docker-compose.yaml` - PostgreSQL構成
- `docker-compose-mysql.yaml` - MySQL構成

---

## 環境構成概要

```
┌─────────────────────────────────────────────────────────────┐
│                    *.local.dev サブドメイン                    │
├─────────────────────────────────────────────────────────────┤
│  api.local.dev      → nginx → idp-server-1/2 (8081/8082)   │
│  mtls.api.local.dev → nginx → idp-server-1/2 (mTLS)       │
│  auth.local.dev     → app-view (認可UI)                     │
│  sample.local.dev   → sample-web (サンプルRP)               │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      データ層                                │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL Primary (:5432) ←→ Replica (:5433)             │
│  Redis (:6379) - セッション/キャッシュ                       │
│  Mockoon (:3010) - 外部サービスモック                        │
└─────────────────────────────────────────────────────────────┘
```

---

## サブドメイン設定

### 方法1: dnsmasq（macOS推奨）

```bash
# セットアップスクリプト実行
./scripts/setup-local-subdomain.sh
```

このスクリプトは以下を設定:
- dnsmasq による `*.local.dev` のローカルDNS解決
- mkcert によるローカルSSL証明書の生成

### 方法2: /etc/hosts（手動設定）

dnsmasqが使えない環境向け:

```bash
# Linux / macOS
sudo sh -c 'echo "127.0.0.1 api.local.dev mtls.api.local.dev auth.local.dev sample.local.dev" >> /etc/hosts'

# Windows (管理者権限のPowerShell)
Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "127.0.0.1 api.local.dev mtls.api.local.dev auth.local.dev sample.local.dev"
```

### 設定確認

```bash
# DNS解決の確認
ping -c 1 api.local.dev
nslookup api.local.dev

# 127.0.0.1 が返されれば正常
```

---

## SSL証明書

### mkcert によるローカル証明書

```bash
# mkcert インストール (macOS)
brew install mkcert

# ルートCA インストール
mkcert -install

# 証明書生成（setup-local-subdomain.sh が自動実行）
mkcert "*.local.dev"
```

証明書ファイルの場所:
- `config/certs/_wildcard.local.dev.pem` - 証明書
- `config/certs/_wildcard.local.dev-key.pem` - 秘密鍵

---

## Docker Compose

### PostgreSQL構成（推奨）

```bash
# 環境変数設定
cp .env.example .env
# または
./init-generate-env.sh postgresql

# ビルド・起動
docker compose build
docker compose up -d
```

### MySQL構成

```bash
# 環境変数設定
./init-generate-env.sh mysql

# ビルド・起動
docker compose -f docker-compose-mysql.yaml build
docker compose -f docker-compose-mysql.yaml up -d
```

### サービス一覧

| サービス | ポート | 説明 |
|---------|-------|------|
| `nginx` | 443 | リバースプロキシ（api.local.dev / mtls.api.local.dev） |
| `idp-server-1` | 8081 | idp-server インスタンス1 |
| `idp-server-2` | 8082 | idp-server インスタンス2 |
| `app-view` | 3000 | 認可UI（auth.local.dev） |
| `sample-web` | 3001 | サンプルRP（sample.local.dev） |
| `postgres-primary` | 5432 | PostgreSQL プライマリ |
| `postgres-replica` | 5433 | PostgreSQL レプリカ |
| `redis` | 6379 | Redis |
| `mockoon` | 3010 | 外部サービスモック |

---

## データベース

### PostgreSQL Primary/Replica構成

```bash
# レプリケーション確認
./scripts/verify-replication.sh

# 個別起動（デバッグ用）
docker compose up -d postgres-primary postgres-replica redis

# マイグレーション実行
docker compose up flyway-migrator
```

### 接続情報

| 項目 | Primary | Replica |
|------|---------|---------|
| ホスト | localhost | localhost |
| ポート | 5432 | 5433 |
| データベース | idp | idp |
| ユーザー | idp_app | idp_app |

### 直接接続

```bash
# Primary
docker compose exec postgres-primary psql -U idp_app -d idp

# Replica
docker compose exec postgres-replica psql -U idp_app -d idp
```

---

## 初期設定

### admin-tenant 初期化

```bash
# 設定ファイル生成
./init-admin-tenant-config.sh

# 初期化実行
./setup.sh
```

### E2Eテスト用データ

```bash
./config/scripts/e2e-test-data.sh
```

---

## よく使うコマンド

```bash
# ヘルスチェック
curl -v https://api.local.dev/actuator/health

# ログ確認
docker compose logs -f idp-server-1
docker compose logs -f nginx

# 再起動
docker compose restart idp-server-1 idp-server-2

# 全停止
docker compose down

# 全削除（ボリューム含む）
docker compose down -v

# E2Eテスト
cd e2e && npm test
```

---

## トラブルシューティング

### サブドメイン関連

| 問題 | 原因 | 解決策 |
|------|------|--------|
| `ping api.local.dev` 失敗 | dnsmasq停止 | `brew services restart dnsmasq` または `/etc/hosts` 手動設定 |
| DNS解決が127.0.0.1以外 | 他DNSリゾルバ優先 | `/etc/resolver/local.dev` ファイル確認 |
| SSL証明書エラー | ルートCA未インストール | `mkcert -install` 実行 |

### Docker関連

| 問題 | 原因 | 解決策 |
|------|------|--------|
| ポート競合 | 他サービスがポート使用中 | `lsof -i :5432` で確認、競合サービス停止 |
| コンテナ起動失敗 | 依存サービス未起動 | `docker compose up -d postgres-primary redis` を先に実行 |
| ディスク容量不足 | Dockerボリューム肥大 | `docker system prune -a` で不要リソース削除 |

### データベース関連

| 問題 | 原因 | 解決策 |
|------|------|--------|
| レプリケーション失敗 | WAL設定不正 | `./scripts/verify-replication.sh` でステータス確認 |
| 接続拒否 | 認証設定不正 | `.env` のDB認証情報確認 |
| マイグレーション失敗 | スキーマ不整合 | `docker compose down -v` で初期化後、再実行 |

### アプリケーション関連

| 問題 | 原因 | 解決策 |
|------|------|--------|
| 502 Bad Gateway | idp-server未起動 | `docker compose logs idp-server-1` でログ確認 |
| 認証失敗 | admin-tenant未初期化 | `./setup.sh` 実行 |
| E2Eテスト失敗 | テストデータ未設定 | `./config/scripts/e2e-test-data.sh` 実行 |

---

## 関連スキル

| スキル | 用途 |
|--------|------|
| `/onboarding` | プロジェクト全体像・学習ロードマップ |
| `/architecture` | アーキテクチャ・レイヤー構造 |
| `/operations` | 運用・監視 |
