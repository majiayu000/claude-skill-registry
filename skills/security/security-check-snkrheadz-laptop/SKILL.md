---
description: "セキュリティスキャン実行。gitleaks、pre-commitフック、秘密情報検出。トリガー: security, gitleaks, pre-commit, secrets, scan"
allowed-tools:
  - Bash
  - Read
  - Grep
---

# security-check スキル

dotfilesリポジトリのセキュリティスキャンを実行する。

## 利用可能なコマンド

### gitleaksスキャン（全ファイル）

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && gitleaks detect --source=. --no-git -v
```

### gitleaksスキャン（Git履歴込み）

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && gitleaks detect --source=. -v
```

### pre-commitフック実行

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && pre-commit run --all-files
```

### pre-commit特定フック実行

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && pre-commit run gitleaks --all-files
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && pre-commit run trailing-whitespace --all-files
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && pre-commit run detect-private-key --all-files
```

### pre-commitフックインストール

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && pre-commit install
```

### pre-commitフック更新

```bash
cd /Users/snkrheadz/ghq/github.com/snkrheadz/laptop && pre-commit autoupdate
```

### 設定ファイル確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/.gitleaks.toml
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/.pre-commit-config.yaml
```

### secrets.env確認（存在のみ）

```bash
ls -la ~/.secrets.env
```

## 実行フロー

### フルセキュリティチェック

1. gitleaksスキャン実行
2. pre-commit全フック実行
3. 結果サマリーを報告

### 問題が見つかった場合

1. 検出された問題の詳細を報告
2. 該当ファイル・行を特定
3. 修正方法を提案

## 使用例

- "セキュリティチェックを実行"
- "gitleaksスキャン"
- "pre-commitを実行"
- "秘密情報がないか確認"
- "セキュリティ設定を確認"

## 設定されているpre-commitフック

| フック | 内容 |
|-------|------|
| `trailing-whitespace` | 行末空白チェック |
| `end-of-file-fixer` | ファイル末尾改行 |
| `check-yaml` | YAML構文チェック |
| `check-added-large-files` | 大きなファイル検出（500KB超） |
| `detect-private-key` | 秘密鍵検出 |
| `check-merge-conflict` | マージコンフリクトマーカー検出 |
| `gitleaks` | 秘密情報スキャン |

## 注意事項

- gitleaksで検出された場合はコミット前に修正が必要
- 秘密情報は `~/.secrets.env` に移動（gitignore済み）
- `.gitleaks.toml` で許可リスト設定可能
