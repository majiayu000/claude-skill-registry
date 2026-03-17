---
description: "Homebrewパッケージ管理。パッケージの追加・削除・検索、Brewfile更新。トリガー: brew, homebrew, package, cask, install, uninstall"
allowed-tools:
  - Bash
  - Read
  - Edit
  - Grep
---

# brew-manage スキル

Homebrewパッケージの追加・削除・検索、およびBrewfileの管理を行う。

## 利用可能なコマンド

### パッケージ検索

```bash
brew search <keyword>
```

### パッケージ情報

```bash
brew info <package>
```

### パッケージインストール

```bash
brew install <package>
# または cask の場合
brew install --cask <cask-name>
```

### パッケージ削除

```bash
brew uninstall <package>
```

### 現在のBrewfile確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/Brewfile
```

### Brewfile更新（現在の状態をダンプ）

```bash
brew bundle dump --force --file=/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/Brewfile
```

### Brewfileからインストール

```bash
brew bundle --file=/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/Brewfile
```

### インストール済みパッケージ一覧

```bash
brew list
brew list --cask
```

### 古いパッケージ確認

```bash
brew outdated
```

### パッケージ更新

```bash
brew upgrade
# または特定パッケージ
brew upgrade <package>
```

## 実行フロー

### パッケージ追加の場合

1. `brew search` でパッケージ確認
2. `brew info` で詳細確認
3. `brew install` でインストール
4. `brew bundle dump --force` でBrewfile更新
5. 変更内容を確認して報告

### パッケージ削除の場合

1. `brew list | grep <package>` で存在確認
2. `brew uninstall <package>` で削除
3. `brew bundle dump --force` でBrewfile更新
4. 変更内容を確認して報告

## 使用例

- "ripgrepをインストールして"
- "brew install bat"
- "Raycastを追加"（cask）
- "node関連のパッケージを検索"
- "不要なパッケージを削除"
- "Brewfileを最新状態に更新"

## Brewfileの構造

| セクション | 説明 |
|-----------|------|
| `tap` | サードパーティリポジトリ |
| `brew` | CLIツール |
| `cask` | GUIアプリケーション |
| `vscode` | VS Code拡張機能 |

## 注意事項

- caskはGUIアプリ用（`--cask`フラグ必須）
- インストール後は必ずBrewfileを更新
- 依存関係の確認: `brew deps <package>`
