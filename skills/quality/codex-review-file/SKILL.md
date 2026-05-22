---
name: codex-review-file
description: Git管理外のファイルをcodex CLIでレビュー。「このファイルをcodexでレビュー」「設定ファイルをレビュー」時に使用
argument-hint: "<file-path> [review-instructions]"
---

# Codex CLIによるファイルレビュー（Git管理外）

codex execコマンドを使って、Git管理外のファイルをレビューします。

## 使用方法

### 特定ファイルをレビュー
```bash
codex exec -C <directory> --skip-git-repo-check "<file>をレビューしてください"
```

### カスタム指示付きレビュー
```bash
codex exec -C <directory> --skip-git-repo-check "<file>をセキュリティの観点からレビューしてください"
```

## 引数

$ARGUMENTS

- `<file-path>`: レビュー対象のファイルパス
- `[review-instructions]`: レビューの観点や指示（オプション）

## 実行例

```bash
# 設定ファイルのレビュー
codex exec -C ~/.claude --skip-git-repo-check "settings.jsonをJSON構文、セキュリティ、ベストプラクティスの観点からレビューしてください"

# 任意のファイルのレビュー
codex exec -C /path/to/dir --skip-git-repo-check "config.yamlの設定内容を確認してください"
```

## 注意事項

- `--skip-git-repo-check`フラグでGitリポジトリ外でも実行可能
- `-C`オプションで作業ディレクトリを指定
- ファイルの内容はCodexが自動的に読み取ります
