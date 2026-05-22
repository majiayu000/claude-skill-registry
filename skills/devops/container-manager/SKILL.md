---
name: container-manager
description: Docker コンテナを管理する。「コンテナ一覧」「docker ps」「コンテナ確認」「コンテナ止めて」「コンテナ起動」「コンテナ再起動」「コンテナに入って」「コンテナの状態」「実行中のコンテナ」「コンテナのリソース」「docker stats」「docker inspect」などで起動。
allowed-tools: [Bash, Read]
---

# Container Manager

Docker コンテナの管理を行います。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| 一覧表示 | 「コンテナ一覧」「docker ps」 | `docker ps` |
| 起動 | 「コンテナ起動」「start」 | `docker start` |
| 停止 | 「コンテナ止めて」「stop」 | `docker stop` |
| 再起動 | 「再起動して」「restart」 | `docker restart` |
| 実行 | 「コンテナに入って」「exec」 | `docker exec` |
| リソース | 「リソース確認」「stats」 | `docker stats` |
| 詳細 | 「詳細情報」「inspect」 | `docker inspect` |

## 実行手順

### 1. 意図の判定

ユーザーの発話から操作を判定:

- **一覧/確認系**: 「一覧」「確認」「見せて」「ps」→ `docker ps`
- **起動系**: 「起動」「start」「動かして」→ `docker start`
- **停止系**: 「止めて」「stop」「停止」→ `docker stop`
- **再起動系**: 「再起動」「restart」→ `docker restart`
- **実行系**: 「入って」「exec」「シェル」→ `docker exec`
- **リソース系**: 「リソース」「stats」「CPU」「メモリ」→ `docker stats`
- **詳細系**: 「詳細」「inspect」「設定」→ `docker inspect`

### 2. コンテナ一覧表示

```bash
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
```

停止中も含める場合:

```bash
docker ps -a --format "table {{.ID}}\t{{.Names}}\t{{.Image}}\t{{.Status}}"
```

### 3. コンテナ操作

**起動**:

```bash
docker start <container>
```

**停止**:

```bash
docker stop <container>
```

**再起動**:

```bash
docker restart <container>
```

**コンテナ内でコマンド実行**:

```bash
docker exec -it <container> /bin/sh
# または
docker exec -it <container> /bin/bash
```

**リソース使用量**:

```bash
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
```

**詳細情報**:

```bash
docker inspect <container> --format '{{json .}}' | jq '.'
# または特定の情報
docker inspect <container> --format '{{.State.Status}}'
docker inspect <container> --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'
```

### 4. 出力フォーマット

```
## コンテナ一覧

| ID | 名前 | イメージ | 状態 | ポート |
|----|------|----------|------|--------|
| ... | ... | ... | ... | ... |

実行中: {N} / 全体: {M}
```

```
## リソース使用量

| コンテナ | CPU | メモリ | ネットワーク | ディスク |
|----------|-----|--------|-------------|----------|
| ... | ... | ... | ... | ... |
```

## 注意事項

- ✅ 停止操作前に確認を求める（本番環境の可能性）
- ✅ `exec` ではインタラクティブモード（`-it`）を使用
- ❌ `docker kill` は使用しない（graceful shutdown を優先）
- ❌ `docker rm` は使用しない（cleanup コマンドに委譲）
