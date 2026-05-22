---
name: compose-manager
description: Docker Compose を管理する。「compose 起動」「docker-compose up」「サービス起動」「compose 停止」「サービス止めて」「down」「compose ログ」「サービスのログ」「compose ps」「サービス状態」「compose build」「サービスビルド」などで起動。
allowed-tools: [Bash, Read, Glob]
context: fork
---

# Compose Manager

Docker Compose の管理を行います。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| 起動 | 「compose 起動」「up」 | `docker compose up` |
| 停止 | 「compose 停止」「down」 | `docker compose down` |
| 状態確認 | 「compose ps」「サービス状態」 | `docker compose ps` |
| ログ | 「compose ログ」 | `docker compose logs` |
| ビルド | 「compose build」 | `docker compose build` |
| 再起動 | 「compose restart」 | `docker compose restart` |

## 実行手順

### 1. Compose ファイルの確認

```bash
ls docker-compose.yml compose.yml docker-compose.yaml compose.yaml 2>/dev/null
```

ファイルが見つからない場合はエラーを表示。

### 2. 意図の判定

ユーザーの発話から操作を判定:

- **起動系**: 「起動」「up」「立ち上げ」「start」→ `docker compose up`
- **停止系**: 「停止」「down」「止めて」→ `docker compose down`
- **状態系**: 「状態」「ps」「確認」→ `docker compose ps`
- **ログ系**: 「ログ」「logs」→ `docker compose logs`
- **ビルド系**: 「ビルド」「build」→ `docker compose build`
- **再起動系**: 「再起動」「restart」→ `docker compose restart`

### 3. Compose 操作

**サービス起動**:

```bash
# フォアグラウンド
docker compose up

# バックグラウンド（推奨）
docker compose up -d

# ビルドしてから起動
docker compose up -d --build

# 特定サービスのみ
docker compose up -d <service>
```

**サービス停止**:

```bash
docker compose down

# ボリュームも削除（要確認）
docker compose down -v
```

⚠️ `--volumes` / `-v` 使用時は必ずユーザーに確認:

```
⚠️ --volumes オプションが指定されています。

以下のボリュームが削除されます:
{ボリューム一覧}

データベースのデータなど、永続化されたデータが失われる可能性があります。

続行しますか？
```

**サービス状態確認**:

```bash
docker compose ps --format "table {{.Name}}\t{{.Service}}\t{{.Status}}\t{{.Ports}}"
```

**サービスログ**:

```bash
# 全サービス
docker compose logs --tail 100

# 特定サービス
docker compose logs --tail 100 <service>

# リアルタイム
docker compose logs -f <service>
```

**サービスビルド**:

```bash
docker compose build

# キャッシュなし
docker compose build --no-cache

# 特定サービス
docker compose build <service>
```

**サービス再起動**:

```bash
docker compose restart

# 特定サービス
docker compose restart <service>
```

### 4. 出力フォーマット

```
## サービス状態

| 名前 | サービス | 状態 | ポート |
|------|----------|------|--------|
| ... | ... | ... | ... |

実行中: {N} / 定義済み: {M}
```

```
## サービス起動完了

| サービス | 状態 | ポート |
|----------|------|--------|
| ... | ... | ... |

ログ確認: `/shiiman-docker:logs --compose`
停止: 「compose down」または `/shiiman-docker:cleanup`
```

```
## サービス停止完了

停止したサービス: {N} 個
削除したネットワーク: {networks}
{ボリューム削除した場合: 削除したボリューム: {volumes}}
```

## 注意事項

- ✅ 起動時は `-d`（デタッチモード）を推奨
- ✅ `down -v` は必ずユーザー確認を行う
- ✅ Compose ファイルの存在を事前確認
- ❌ `docker compose kill` は使用しない
- ❌ `docker compose rm -f` は使用しない
