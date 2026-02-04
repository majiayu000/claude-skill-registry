---
name: project-setup
description: "プロジェクトのClaude Code設定をセットアップ。構成を検出し.claude/settings.local.jsonとhooksを生成。トリガー: /project-setup, プロジェクト設定, formatter設定, project configuration, setup formatter"
user-invocable: true
allowed-tools: Read, Bash, Glob, Grep, Write
model: sonnet
---

# プロジェクトセットアップスキル

プロジェクトの構成を検出し、適切なClaude Code設定を生成します。

## 必須実行ステップ

**このスキルが呼び出されたら、以下のステップを順番に実行すること。**

### Step 1: プロジェクトタイプを検出

```bash
# [Bash] 以下を実行してプロジェクトタイプを判定
ls -la package.json go.mod Cargo.toml pyproject.toml 2>/dev/null
```

検出結果に基づいてプロジェクトタイプを決定:

| 検出ファイル | プロジェクトタイプ | フォーマッター |
|-------------|------------------|--------------|
| `package.json` | Node.js | prettier |
| `go.mod` | Go | gofmt |
| `Cargo.toml` | Rust | rustfmt |
| `pyproject.toml` | Python | ruff |

### Step 2: ディレクトリを作成

```bash
# [Bash] .claude/hooks ディレクトリを作成
mkdir -p .claude/hooks
```

### Step 3: settings.local.json を生成

```bash
# [Write] .claude/settings.local.json を作成
```

### Step 4: format-code.sh を生成

```bash
# [Write] .claude/hooks/format-code.sh を作成（プロジェクトタイプに応じた内容）
```

### Step 5: 実行権限を付与

```bash
# [Bash] 実行権限を付与
chmod +x .claude/hooks/format-code.sh
```

### Step 6: 結果を報告

セットアップ完了後、ユーザーに結果を報告。

---

## 生成ファイルの内容

#### `.claude/settings.local.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

#### `.claude/hooks/format-code.sh`

プロジェクトタイプに応じたフォーマットスクリプトを生成。

**Node.js (prettier) の例:**

```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[[ -z "$file_path" || ! -f "$file_path" ]] && exit 0

case "$file_path" in
    *.ts|*.tsx|*.js|*.jsx|*.json|*.md|*.css|*.scss|*.html)
        # ローカルprettier使用（npxより高速）
        if [[ -f "node_modules/.bin/prettier" ]]; then
            node_modules/.bin/prettier --write "$file_path" 2>/dev/null || true
        fi
        ;;
esac
exit 0
```

**Go (gofmt) の例:**

```bash
#!/bin/bash
input=$(cat)
file_path=$(echo "$input" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
[[ -z "$file_path" || ! -f "$file_path" ]] && exit 0

case "$file_path" in
    *.go)
        gofmt -w "$file_path" 2>/dev/null || true
        ;;
esac
exit 0
```

### 3. 出力形式

セットアップ完了後、以下の形式で報告:

```markdown
## プロジェクトセットアップ完了

### 検出結果
- **タイプ**: Node.js (TypeScript)
- **フォーマッター**: prettier
- **実行方法**: node_modules/.bin/prettier（ローカル）

### 生成ファイル
- `.claude/settings.local.json` - フック設定
- `.claude/hooks/format-code.sh` - フォーマットスクリプト

### .gitignore 追加推奨
以下を`.gitignore`に追加することを推奨:
```
.claude/settings.local.json
```

### 動作確認
ファイルを編集すると、自動的にフォーマッターが実行されます。
```

## 注意事項

- `settings.local.json` はプロジェクト固有のため、`.gitignore` への追加を推奨
- ローカルにフォーマッターがインストールされていない場合は `npm install` 等を案内
- 複数のプロジェクトタイプが検出された場合は、適切なものを選択

## フォーマッター別の拡張子マッピング

| フォーマッター | 対象拡張子 |
|--------------|----------|
| prettier | `.ts`, `.tsx`, `.js`, `.jsx`, `.json`, `.md`, `.css`, `.scss`, `.html` |
| gofmt | `.go` |
| rustfmt | `.rs` |
| ruff | `.py` |
