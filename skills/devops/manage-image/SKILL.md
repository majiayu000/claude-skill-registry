---
name: manage-image
description: Docker イメージを管理する。「イメージ一覧」「docker images」「イメージ確認」「ビルドして」「docker build」「イメージ作成」「イメージ取得」「docker pull」「イメージダウンロード」「イメージの履歴」「docker history」などで起動。
allowed-tools: [Bash, Read, Glob]
---

# Manage Image

Docker イメージの管理を行います。

## 対応操作

| 操作 | トリガー例 | コマンド |
|------|-----------|----------|
| 一覧表示 | 「イメージ一覧」「images」 | `docker images` |
| ビルド | 「ビルドして」「build」 | `docker build` |
| 取得 | 「イメージ取得」「pull」 | `docker pull` |
| 履歴 | 「イメージ履歴」「history」 | `docker history` |

## 実行手順

### 1. 意図の判定

ユーザーの発話から操作を判定:

- **一覧系**: 「一覧」「images」「確認」→ `docker images`
- **ビルド系**: 「ビルド」「build」「作成」→ `docker build`
- **取得系**: 「取得」「pull」「ダウンロード」→ `docker pull`
- **履歴系**: 「履歴」「history」「レイヤー」→ `docker history`

### 2. イメージ一覧表示

```bash
docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}\t{{.CreatedSince}}"
```

dangling イメージも含める場合:

```bash
docker images -a --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}"
```

### 3. イメージ操作

**ビルド**:

まず Dockerfile の存在確認:

```bash
ls Dockerfile docker-compose.yml compose.yml 2>/dev/null
```

docker-compose.yml がある場合:

```bash
docker compose build [service]
```

Dockerfile のみの場合:

```bash
docker build -t <tag> .
# または
docker build -t <tag> -f <dockerfile> .
```

オプション:

- `--no-cache`: キャッシュなしでビルド
- `--target <stage>`: マルチステージビルドのターゲット指定

**イメージ取得**:

```bash
docker pull <image>:<tag>
```

**履歴表示**:

```bash
docker history <image> --format "table {{.CreatedBy}}\t{{.Size}}"
```

### 4. 出力フォーマット

```
## イメージ一覧

| リポジトリ | タグ | ID | サイズ | 作成日時 |
|-----------|------|-----|--------|----------|
| ... | ... | ... | ... | ... |

合計: {N} イメージ
総サイズ: {total_size}
```

```
## ビルド完了

イメージ: {repository}:{tag}
サイズ: {size}
レイヤー数: {layers}
ビルド時間: {duration}
```

```
## イメージ取得完了

イメージ: {image}:{tag}
ダイジェスト: {digest}
サイズ: {size}
```

## 注意事項

- ✅ ビルド時はタグを指定することを推奨
- ✅ `latest` タグの使用は避けることを推奨
- ✅ マルチステージビルドを推奨（サイズ削減）
- ❌ `docker rmi -f` は使用しない（cleanup コマンドに委譲）
