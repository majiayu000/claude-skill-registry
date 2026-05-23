---
description: "ランタイム管理（mise）。Go, Node.js, Python, Rubyのバージョン管理。トリガー: mise, runtime, node, go, python, ruby, version"
allowed-tools:
  - Bash
  - Read
  - Edit
---

# mise-runtime スキル

miseを使用したランタイム（Go, Node.js, Python, Ruby）のバージョン管理を行う。

## 現在の設定

設定ファイル: `/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/mise/config.toml`

現在のランタイム:

| ツール | バージョン |
|-------|-----------|
| Go | 1.24.3 |
| Node.js | 25.2.1, 22.16.0 |
| Python | 3.13 |
| Ruby | 3.4.8 |

## 利用可能なコマンド

### インストール済みランタイム一覧

```bash
mise list
```

### 利用可能なバージョン確認

```bash
mise ls-remote go
mise ls-remote node
mise ls-remote python
mise ls-remote ruby
```

### 特定バージョンインストール

```bash
mise install go@1.24.3
mise install node@22.16.0
mise install python@3.13
mise install ruby@3.4.8
```

### グローバルバージョン設定

```bash
mise use --global go@1.24.3
```

### 設定からすべてインストール

```bash
mise install
```

### 現在のバージョン確認

```bash
mise current
```

### 設定ファイル信頼

```bash
mise trust ~/.config/mise/config.toml
```

### アンインストール

```bash
mise uninstall go@1.23.0
```

### ランタイム更新

```bash
mise upgrade
```

### 設定ファイル確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/mise/config.toml
```

## 実行フロー

### 新しいバージョン追加

1. `mise ls-remote <tool>` で利用可能バージョン確認
2. `mise install <tool>@<version>` でインストール
3. `/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/mise/config.toml` を編集
4. 変更内容を確認

### バージョン切り替え

1. `mise list` で現在のバージョン確認
2. 必要なバージョンがなければインストール
3. `mise use <tool>@<version>` で切り替え

## 使用例

- "Node.js 22を追加して"
- "mise list"
- "Goの最新バージョンは？"
- "Python 3.12をインストール"
- "現在のランタイムバージョンを確認"

## config.toml の構造

```toml
[tools]
go = "1.24.3"
node = ["25.2.1", "22.16.0"]  # 複数バージョン
python = "3.13"
ruby = "3.4.8"

[settings]
auto_install = true
trusted_config_paths = ["~"]
```

## 注意事項

- Node.jsは複数バージョン併用可能（配列で指定）
- config.toml編集後は`mise install`で反映
- シンボリックリンク: `~/.config/mise/config.toml` -> dotfilesリポジトリ
