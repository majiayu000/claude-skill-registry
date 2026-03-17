---
name: hooks
description: >
  Claude Code の Hook 作成・管理ガイド。PreToolUse、PostToolUse、Stop等のフック実装。
  使用タイミング: (1) 危険操作をブロックしたい時 (2) ツール実行後に提案を出したい時
  (3) セッション終了時にクリーンアップしたい時 (4) Claude Codeをカスタマイズしたい時。
  トリガー例: 「フックを作って」「PreToolUseフック」「危険操作をブロック」
  「コミット後に提案」「Claude Codeのhooks」
---

# hooks - Claude Code Hooks

Claude Code の Hook 作成・管理ガイド。

---

## 概要

Hooks はツール実行の前後に自動で実行されるスクリプト。

| タイプ | タイミング | 用途 |
|--------|-----------|------|
| PreToolUse | ツール実行**前** | 検証、危険操作ブロック |
| PostToolUse | ツール実行**後** | 提案、ログ記録 |
| Stop | 会話終了時 | クリーンアップ |

---

## Hook 作成

### 1. スクリプト作成

```bash
#!/bin/bash
# .claude/hooks/my-hook.sh

# 環境変数
# TOOL_NAME: ツール名 (Write, Edit, Bash, etc.)
# TOOL_INPUT: JSON形式の入力パラメータ

# 終了コード
# 0: 成功（許可）
# 1: 警告（許可、メッセージ表示）
# 2: ブロック（実行を停止）

# 例: 危険なコマンドをブロック
if echo "$TOOL_INPUT" | grep -q "rm -rf /"; then
  echo "🚫 危険なコマンドをブロックしました" >&2
  exit 2
fi

exit 0
```

### 2. 実行権限付与

```bash
chmod +x .claude/hooks/my-hook.sh
```

### 3. 設定ファイルに登録

```json
// .claude/settings.local.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/project/.claude/hooks/my-hook.sh"
          }
        ]
      }
    ]
  }
}
```

---

## 実用的な Hook 例

### PreToolUse: 危険操作ブロック

```bash
#!/bin/bash
# validate-dangerous-ops.sh

case "$TOOL_NAME" in
  "Bash")
    COMMAND=$(echo "$TOOL_INPUT" | jq -r '.command // empty')

    # force push をブロック
    if echo "$COMMAND" | grep -qE 'git push.*(--force|-f).*(main|master)'; then
      echo "🚫 main/master への force push は禁止です" >&2
      exit 2
    fi
    ;;

  "Write"|"Edit")
    FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.file_path // empty')

    # .env ファイル編集を警告
    if echo "$FILE_PATH" | grep -qE '\.env'; then
      echo "⚠️ 環境変数ファイルを編集しようとしています" >&2
      exit 1  # 警告のみ
    fi
    ;;
esac

exit 0
```

### PostToolUse: コミット後の提案

```bash
#!/bin/bash
# suggest-after-commit.sh

# git commit 後のみ発火
if ! echo "$TOOL_INPUT" | grep -q "git commit"; then
  exit 0
fi

# 変更ファイルをチェック
CHANGED=$(git diff-tree --no-commit-id --name-only -r HEAD 2>/dev/null)

if echo "$CHANGED" | grep -q "schema"; then
  echo "" >&2
  echo "💡 スキーマが変更されました" >&2
  echo "   マイグレーションファイルの作成を検討してください" >&2
  exit 1
fi

exit 0
```

### Stop: セッション終了時クリーンアップ

```bash
#!/bin/bash
# cleanup-on-stop.sh

# マージ済みブランチの確認
MERGED=$(git branch --merged main | grep -v main | grep -v '\*')

if [ -n "$MERGED" ]; then
  echo "" >&2
  echo "🧹 マージ済みブランチがあります:" >&2
  echo "$MERGED" >&2
  echo "   削除を検討してください: git branch -d <branch>" >&2
  exit 1
fi

exit 0
```

---

## 設定構造

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|Bash",  // 正規表現でマッチ
        "hooks": [
          { "type": "command", "command": "/path/to/hook.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "hooks": [
          { "type": "command", "command": "/path/to/hook.sh" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "/path/to/hook.sh" }
        ]
      }
    ]
  }
}
```

---

## デバッグ

```bash
# 直接実行してテスト
TOOL_NAME="Bash" TOOL_INPUT='{"command":"git push --force main"}' ./my-hook.sh
echo $?  # 終了コード確認
```

---

## ベストプラクティス

1. **非ブロッキング**: 長時間処理は避ける
2. **stderr に出力**: stdout ではなく stderr に出力
3. **提案のみ**: 自動実行せず、人間に判断を委ねる
4. **jq でパース**: JSON パースには jq を使用
5. **フェイルセーフ**: jq がない場合は許可（exit 0）
