---
name: shell-script
description: シェルスクリプトの作成・レビュー・改善を行うスキル。POSIX準拠とShellCheck対応
---

# Shell Script Skill

シェルスクリプトの作成・レビュー・改善を行うためのスキルです。

## 基本方針

### POSIX準拠

- 可搬性を重視
- bash拡張が必要な場合は shebang で明示

### ShellCheck準拠

- 全てのスクリプトはShellCheckでエラー0を目指す
- 必要な場合のみ `# shellcheck disable=SC####` で抑制

## コーディング規約

### 変数

```bash
# 変数は常にクォート
echo "${variable}"

# ローカル変数には local を使用
local my_var="value"

# 定数は大文字
readonly MY_CONSTANT="value"
```

### エラーハンドリング

```bash
# スクリプト先頭に設定
set -euo pipefail

# エラーメッセージは stderr へ
echo "Error: something went wrong" >&2
exit 1
```

### 関数

```bash
# 関数名はスネークケース
my_function() {
    local arg1="$1"
    # 処理
}
```

## チェックリスト

- [ ] shebang は適切か（#!/bin/bash or #!/bin/sh）
- [ ] `set -euo pipefail` があるか
- [ ] 変数は全てクォートされているか
- [ ] ShellCheckエラーはないか
- [ ] 実行権限の設定は適切か

## 出力形式（レビュー時）

```markdown
## Shell Script Review

### ShellCheck Results
[ShellCheckの結果サマリ]

### Issues
- [問題点と修正提案]

### Improved Script
[改善版スクリプト（必要な場合）]
```
