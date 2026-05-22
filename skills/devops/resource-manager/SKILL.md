---
name: resource-manager
description: Docker のリソースを管理する。「ネットワーク確認」「docker network」「ネットワーク一覧」「ボリューム確認」「docker volume」「ボリューム一覧」「ディスク確認」「docker system df」「ディスク使用量」「容量確認」などで起動。
allowed-tools: [Bash]
---

# Resource Manager

Docker のネットワーク、ボリューム、ディスク使用量を管理します。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| ネットワーク一覧 | 「ネットワーク確認」 | `docker network ls` |
| ネットワーク詳細 | 「ネットワーク詳細」 | `docker network inspect` |
| ボリューム一覧 | 「ボリューム確認」 | `docker volume ls` |
| ボリューム詳細 | 「ボリューム詳細」 | `docker volume inspect` |
| ディスク使用量 | 「ディスク確認」「容量」 | `docker system df` |

## 実行手順

### 1. 意図の判定

ユーザーの発話から操作を判定:

- **ネットワーク系**: 「ネットワーク」「network」→ `docker network`
- **ボリューム系**: 「ボリューム」「volume」「永続化」→ `docker volume`
- **ディスク系**: 「ディスク」「容量」「使用量」「df」→ `docker system df`

### 2. ネットワーク操作

**一覧表示**:

```bash
docker network ls --format "table {{.ID}}\t{{.Name}}\t{{.Driver}}\t{{.Scope}}"
```

**詳細表示**:

```bash
docker network inspect <network> --format '{{json .}}' | jq '.'
```

接続中のコンテナを確認:

```bash
docker network inspect <network> --format '{{range .Containers}}{{.Name}} {{end}}'
```

### 3. ボリューム操作

**一覧表示**:

```bash
docker volume ls --format "table {{.Name}}\t{{.Driver}}\t{{.Scope}}"
```

**詳細表示**:

```bash
docker volume inspect <volume> --format '{{json .}}' | jq '.'
```

**使用量確認**:

```bash
docker system df -v | grep -A 100 "Local Volumes"
```

### 4. ディスク使用量

**概要**:

```bash
docker system df
```

**詳細**:

```bash
docker system df -v
```

### 5. 出力フォーマット

```
## ネットワーク一覧

| ID | 名前 | ドライバー | スコープ |
|----|------|-----------|----------|
| ... | ... | ... | ... |

合計: {N} ネットワーク
```

```
## ボリューム一覧

| 名前 | ドライバー | スコープ |
|------|-----------|----------|
| ... | ... | ... |

合計: {N} ボリューム
```

```
## Docker ディスク使用量

| タイプ | 総数 | アクティブ | サイズ | 回収可能 |
|--------|------|-----------|--------|----------|
| Images | ... | ... | ... | ... |
| Containers | ... | ... | ... | ... |
| Local Volumes | ... | ... | ... | ... |
| Build Cache | ... | ... | ... | ... |

**合計使用量**: {total}
**回収可能**: {reclaimable}

### 提案

{使用量が多い場合}
ディスク使用量が多くなっています。
`/shiiman-docker:cleanup --dry-run` で削除対象を確認できます。
```

## 注意事項

- ✅ ネットワーク/ボリュームの詳細は inspect で確認
- ✅ ディスク使用量が多い場合は cleanup を提案
- ❌ `docker network rm` は使用しない（cleanup に委譲）
- ❌ `docker volume rm` は使用しない（データ保護）
- ❌ `docker volume prune` は使用しない（データ保護）
