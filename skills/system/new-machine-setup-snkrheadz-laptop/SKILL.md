---
description: "新マシンセットアップガイド。macOS初期設定からdotfiles適用までの手順案内。トリガー: 新マシン, setup, 移行, 新しいMac, セットアップ"
allowed-tools:
  - Bash
  - Read
  - WebFetch
---

# new-machine-setup スキル

新しいmacOSマシンのセットアップ手順を案内する。

## セットアップ手順概要

### Phase 1: macOS初期設定

1. **システム環境設定**
   - Apple IDでサインイン
   - iCloud設定
   - キーボード/トラックパッド設定

2. **Xcode Command Line Tools**
   ```bash
   xcode-select --install
   ```

### Phase 2: Homebrewインストール

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Phase 3: 基本ツールインストール

```bash
# Apple Silicon Macの場合
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

# Git インストール
brew install git gh
```

### Phase 4: SSH設定

```bash
# SSH鍵の生成（既存がない場合）
ssh-keygen -t ed25519 -C "your@email.com"

# ssh-agentに追加
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# GitHub CLI で認証
gh auth login
```

### Phase 5: dotfilesクローン

```bash
# ghqでクローン（推奨）
brew install ghq
ghq get git@github.com:snkrheadz/laptop.git

# または直接クローン
git clone git@github.com:snkrheadz/laptop.git ~/ghq/github.com/snkrheadz/laptop
```

### Phase 6: install.sh実行

```bash
cd ~/ghq/github.com/snkrheadz/laptop
./install.sh
```

これにより以下が実行される:
- バックアップ作成
- シンボリックリンク作成
- Homebrew パッケージインストール
- pre-commit フック設定
- auto-sync launchd設定
- mise ランタイムインストール

### Phase 7: シェル再起動

```bash
exec zsh
```

### Phase 8: 追加設定

1. **秘密情報の設定**
   ```bash
   # ~/.secrets.env を編集（install.shで作成済み）
   vim ~/.secrets.env
   ```

2. **アプリケーション設定**
   - 各アプリのログイン/同期設定

3. **IDEプラグイン**
   - VS Code拡張機能は Brewfile から自動インストール

## 旧マシンからの移行

### データ移行

| 項目 | 方法 |
|-----|------|
| SSH鍵 | 手動コピーまたは新規生成 |
| API keys | `~/.secrets.env` 参照 |
| プロジェクト | `ghq get` で再クローン |
| Homebrewパッケージ | Brewfileから復元 |

### 確認事項

```bash
# 移行後の確認
brew bundle check --file=~/ghq/github.com/snkrheadz/laptop/Brewfile
mise list
git config --global user.name
git config --global user.email
```

## 使用例

- "新しいMacのセットアップ手順を教えて"
- "dotfilesの適用方法"
- "Homebrewのインストール方法"
- "新マシンへの移行手順"
- "セットアップチェックリスト"

## チェックリスト

- [ ] Xcode Command Line Tools
- [ ] Homebrew
- [ ] Git/GitHub CLI
- [ ] SSH鍵設定
- [ ] dotfilesクローン
- [ ] install.sh実行
- [ ] シェル再起動
- [ ] ~/.secrets.env設定
- [ ] mise runtimes確認
- [ ] auto-sync動作確認

## トラブルシューティング

### Homebrewのパスが通らない

```bash
# Apple Silicon Mac
eval "$(/opt/homebrew/bin/brew shellenv)"

# Intel Mac
eval "$(/usr/local/bin/brew shellenv)"
```

### permissionエラー

```bash
# /opt/homebrew の権限修正
sudo chown -R $(whoami) /opt/homebrew
```

### install.shが失敗

1. エラーメッセージを確認
2. 依存ツールが入っているか確認
3. ネットワーク接続を確認
4. 手動で各ステップを実行して問題特定

## 注意事項

- SSH鍵は慎重に扱う（移行時は暗号化転送推奨）
- install.shは冪等（何度実行してもOK）
- 既存設定は自動バックアップされる
- Apple Silicon/Intel Macでパスが異なる
