---
name: google-drive
description: |
  gogcli (gog) を使用してGoogle Driveを操作するスキル。ファイルの検索、アップロード、ダウンロード、共有、フォルダ管理などをCLI経由で実行。
  Use when: (1) ドライブのファイルを検索したい、(2) ファイルをアップロードしたい、(3) ファイルをダウンロードしたい、(4) Google Driveを操作したい、(5) ファイルを共有したい、(6) フォルダを作成したい
  Trigger: drive, ドライブ, google drive, ファイル検索, アップロード, ダウンロード, 共有
---

# Google Drive Operations with gogcli

`gog` CLIを使用してGoogle Driveを操作する。

## Prerequisites

```bash
# Installation
brew install gogcli

# Authentication (初回のみ)
gog auth login
```

## Commands Reference

### List Files

```bash
# ルートフォルダのファイル一覧
gog drive ls

# 特定フォルダの一覧
gog drive ls --parent="<folderId>"

# 最大件数指定
gog drive ls --max=50

# クエリフィルタ付き
gog drive ls --query="mimeType='application/vnd.google-apps.folder'"
```

### Search Files

```bash
# フルテキスト検索
gog drive search "検索キーワード"

# 複数キーワード
gog drive search "報告書 2024"

# JSON形式で出力
gog drive search "議事録" --json --max=20
```

### Download Files

```bash
# ファイルをダウンロード
gog drive download <fileId>

# 出力先を指定
gog drive download <fileId> --out="/path/to/output.pdf"

# Google Docsのエクスポート形式を指定
gog drive download <fileId> --format=pdf    # PDF形式
gog drive download <fileId> --format=docx   # Word形式
gog drive download <fileId> --format=xlsx   # Excel形式
gog drive download <fileId> --format=pptx   # PowerPoint形式
gog drive download <fileId> --format=csv    # CSV形式
gog drive download <fileId> --format=txt    # テキスト形式
```

### Upload Files

```bash
# ファイルをアップロード（ルートへ）
gog drive upload /path/to/file.pdf

# ファイル名を変更してアップロード
gog drive upload /path/to/file.pdf --name="新しいファイル名.pdf"

# 特定フォルダへアップロード
gog drive upload /path/to/file.pdf --parent="<folderId>"
```

### Create Folder

```bash
# ルートにフォルダ作成
gog drive mkdir "新しいフォルダ"

# 特定フォルダ内にサブフォルダ作成
gog drive mkdir "サブフォルダ" --parent="<parentFolderId>"
```

### File Operations

```bash
# ファイルのメタデータ取得
gog drive get <fileId>

# ファイルをコピー
gog drive copy <fileId> "コピー後の名前"

# ファイルを移動
gog drive move <fileId> --parent="<newParentFolderId>"

# ファイル名を変更
gog drive rename <fileId> "新しい名前"

# ファイルを削除（ゴミ箱へ）
gog drive delete <fileId>

# WebのURLを取得
gog drive url <fileId>
```

### Share Files

```bash
# 特定ユーザーと共有（閲覧権限）
gog drive share <fileId> --email="user@example.com" --role="reader"

# 特定ユーザーと共有（編集権限）
gog drive share <fileId> --email="user@example.com" --role="writer"

# 公開リンクを作成
gog drive share <fileId> --anyone --role="reader"

# 権限一覧を表示
gog drive permissions <fileId>

# 権限を削除
gog drive unshare <fileId> <permissionId>
```

### Shared Drives

```bash
# 共有ドライブ一覧
gog drive drives
```

### Comments

```bash
# ファイルのコメント一覧
gog drive comments list <fileId>

# コメントを追加
gog drive comments add <fileId> "コメント内容"
```

## Common Workflows

### 最近のファイルを確認

```bash
gog drive ls --max=10
```

### 特定の名前のファイルを検索

```bash
gog drive search "週報"
```

### Google Docsをローカルにダウンロード

```bash
# PDF形式でダウンロード
gog drive download <fileId> --format=pdf --out="./document.pdf"
```

### ローカルファイルを特定フォルダにアップロード

```bash
# まずフォルダIDを確認
gog drive search "プロジェクトフォルダ" --json

# フォルダにアップロード
gog drive upload ./report.pdf --parent="<folderId>"
```

## Output Formats

| Flag | Description |
|------|-------------|
| `--json` | JSON形式で出力（スクリプト向け） |
| `--plain` | TSV形式で出力（パース容易） |
| (default) | 人間が読みやすい形式 |

## Tips

- `--account=email@example.com` で複数アカウントを切り替え
- ファイルIDはURLから取得可能: `https://drive.google.com/file/d/<fileId>/view`
- フォルダIDもURLから取得可能: `https://drive.google.com/drive/folders/<folderId>`
- `--force` で確認をスキップ（削除時など注意して使用）
