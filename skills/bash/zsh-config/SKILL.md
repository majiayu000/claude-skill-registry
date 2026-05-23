---
description: "zsh設定管理。関数・config・aliasの追加・編集・確認。トリガー: zsh, shell, alias, function, config, zshrc"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
---

# zsh-config スキル

zsh設定ファイル（関数、config、alias）の管理を行う。

## ディレクトリ構造

```
/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/
├── .zshrc           # メイン設定
├── .aliases         # エイリアス定義
├── functions/       # カスタム関数
│   ├── _git_delete_branch
│   ├── change-extension
│   ├── envup
│   └── mcd
└── configs/         # モジュール設定
    ├── pre/         # 最初にロード
    ├── *.zsh        # メイン設定
    └── post/        # 最後にロード
        ├── path.zsh
        ├── completion.zsh
        └── mise.zsh
```

## ロード順序

1. `zsh/functions/*` - カスタム関数
2. `zsh/configs/pre/*` - プリ設定
3. `zsh/configs/*.zsh` - メイン設定
4. `zsh/configs/post/*` - ポスト設定
5. `~/.aliases` - エイリアス
6. oh-my-zsh (plugins: git, zsh-autosuggestions)

## 利用可能なコマンド

### 現在の設定確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/.zshrc
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/.aliases
```

### 関数一覧

```bash
ls -la /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/functions/
```

### 設定ファイル一覧

```bash
ls -la /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/configs/
ls -la /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/configs/post/
```

### エイリアス検索

```bash
grep -n "alias" /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/.aliases
```

### 既存関数確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/functions/<function-name>
```

## 実行フロー

### 新しい関数追加

1. 既存関数を確認して命名規則を把握
2. `/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/functions/<name>` にファイル作成
3. 関数定義を記述

関数テンプレート:

```bash
# Description of the function

function <name>() {
  # function body
}
```

### 新しいエイリアス追加

1. `/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/zsh/.aliases` を編集
2. `alias <name>="<command>"` 形式で追加

### 新しいconfig追加

1. ロードタイミングを決定（pre/main/post）
2. 適切なディレクトリにファイル作成
3. 設定を記述

## 使用例

- "新しいzsh関数を追加"
- "aliasを確認"
- "mcd関数の内容を見せて"
- "PATH設定を確認"
- "新しいエイリアスを追加"

## 既存のconfig一覧

| ファイル | 内容 |
|---------|------|
| color.zsh | 色設定 |
| editor.zsh | エディタ設定 |
| history.zsh | 履歴設定 |
| homebrew.zsh | Homebrew設定 |
| keybindings.zsh | キーバインド |
| options.zsh | zshオプション |
| prompt.zsh | プロンプト設定 |
| post/path.zsh | PATH設定 |
| post/completion.zsh | 補完設定 |
| post/mise.zsh | mise設定 |

## 注意事項

- oh-my-zshプラグインとの名前衝突を避ける（例: `g` は git プラグインで使用）
- 関数名の確認: `alias` コマンドで既存エイリアスをチェック
- 設定変更後は `source ~/.zshrc` で反映
- 新規ファイルは実行権限不要（sourceで読み込み）
