---
name: gitignore-checker
description: コミット前に .gitignore に追加すべきファイルをチェックする。「gitignore チェック」「コミット前チェック」「機密ファイル確認」「.gitignore 確認」「追加すべきファイル」「無視すべきファイル」「gitignore 推奨」などで起動。機密情報や不要なファイルがコミットされないように確認。
allowed-tools: [Read, Bash, Glob, Grep]
context: fork
agent: shiiman-git:security-check
---

# Gitignore Checker

コミット前に .gitignore に追加すべきファイルをチェックします。

## ワークフロー

### 1. 現在のステージング状態を確認

```bash
git status --porcelain
```

### 2. チェック対象ファイルの分析

以下のカテゴリでファイルをチェック:

#### 機密ファイル（必須で .gitignore に追加）

| パターン | 説明 |
|----------|------|
| `.env*` | 環境変数ファイル |
| `*.pem`, `*.key` | 秘密鍵 |
| `credentials.json` | 認証情報 |
| `*.secret` | シークレットファイル |
| `config/secrets.yml` | Rails シークレット |
| `.aws/` | AWS 認証情報 |

#### 一般的に無視すべきファイル

| パターン | 説明 |
|----------|------|
| `node_modules/` | npm パッケージ |
| `vendor/` | 依存パッケージ |
| `.DS_Store` | macOS システムファイル |
| `Thumbs.db` | Windows サムネイル |
| `*.log` | ログファイル |
| `*.tmp`, `*.temp` | 一時ファイル |
| `dist/`, `build/` | ビルド成果物 |
| `coverage/` | テストカバレッジ |

#### IDE 設定ファイル

| パターン | 説明 |
|----------|------|
| `.idea/` | JetBrains IDE |
| `.vscode/` | Visual Studio Code（settings.json は除く） |
| `*.swp`, `*.swo` | Vim スワップファイル |
| `.project`, `.classpath` | Eclipse |

### 3. 既存の .gitignore を確認

```bash
cat .gitignore 2>/dev/null || echo "(.gitignore が存在しません)"
```

### 4. 結果報告

```
## .gitignore チェック結果

### ⚠️ 機密ファイル（コミット禁止）

| ファイル | 状態 | 推奨アクション |
|----------|------|----------------|
| .env | ステージ済 | git reset HEAD .env && .gitignore に追加 |
| credentials.json | 未追跡 | .gitignore に追加 |

### 💡 推奨: .gitignore に追加

| パターン | 理由 |
|----------|------|
| node_modules/ | npm パッケージ（リポジトリに含める必要なし） |
| .DS_Store | macOS システムファイル |

### ✅ 問題なし

機密ファイルは検出されませんでした。
```

### 5. 修正提案（機密ファイルがある場合）

```bash
# ステージから削除
git reset HEAD {ファイル名}

# .gitignore に追加
echo "{パターン}" >> .gitignore
```

## 重要な注意事項

- ✅ コミット前に必ず実行を推奨
- ✅ 機密ファイルは絶対にコミットしない
- ✅ 検出されたファイルは即座に .gitignore に追加
- ❌ 一度コミットした機密情報は履歴に残る（git filter-branch が必要）
