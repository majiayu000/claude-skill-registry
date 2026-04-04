---
description: "auto-sync launchd管理。dotfiles自動同期の状態確認・起動・停止・ログ確認。トリガー: launchd, auto-sync, 自動同期, 同期, sync agent"
allowed-tools:
  - Bash
  - Read
  - Grep
---

# launchd-manage スキル

dotfiles自動同期のlaunchdエージェント管理を行う。

## 概要

auto-syncは毎時dotfilesの変更をGitHubに自動同期するlaunchdエージェント。

- **plistファイル**: `~/Library/LaunchAgents/com.user.dotfiles-sync.plist`
- **実行スクリプト**: `/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/scripts/auto-sync.sh`
- **ログファイル**: `~/Library/Logs/dotfiles-sync.log`
- **実行間隔**: 3600秒（1時間）

## コマンド

### エージェント状態確認

```bash
launchctl list | grep dotfiles
```

### plistファイル確認

```bash
cat ~/Library/LaunchAgents/com.user.dotfiles-sync.plist
```

### 自動同期スクリプト確認

```bash
cat /Users/snkrheadz/ghq/github.com/snkrheadz/laptop/scripts/auto-sync.sh
```

### ログ確認

```bash
cat ~/Library/Logs/dotfiles-sync.log | tail -50
```

### 最新のログエントリ

```bash
tail -20 ~/Library/Logs/dotfiles-sync.log
```

### エージェント停止

```bash
launchctl unload ~/Library/LaunchAgents/com.user.dotfiles-sync.plist
```

### エージェント起動

```bash
launchctl load ~/Library/LaunchAgents/com.user.dotfiles-sync.plist
```

### エージェント再起動

```bash
launchctl unload ~/Library/LaunchAgents/com.user.dotfiles-sync.plist && \
launchctl load ~/Library/LaunchAgents/com.user.dotfiles-sync.plist
```

### 手動で同期実行

```bash
/Users/snkrheadz/ghq/github.com/snkrheadz/laptop/scripts/auto-sync.sh
```

### plistのシンタックスチェック

```bash
plutil -lint ~/Library/LaunchAgents/com.user.dotfiles-sync.plist
```

## plistファイル構造

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "...">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.user.dotfiles-sync</string>
  <key>ProgramArguments</key>
  <array>
    <string>/path/to/auto-sync.sh</string>
  </array>
  <key>StartInterval</key>
  <integer>3600</integer>
  <key>StandardOutPath</key>
  <string>~/Library/Logs/dotfiles-sync.log</string>
  <key>StandardErrorPath</key>
  <string>~/Library/Logs/dotfiles-sync.log</string>
</dict>
</plist>
```

## 実行フロー

### 状態確認

1. launchdエージェントの稼働状態確認
2. plistファイルの存在確認
3. 最新のログエントリを表示

### トラブルシューティング

1. エージェント状態確認
2. ログを確認して最後の実行結果を調査
3. 手動実行でスクリプトの動作確認
4. 必要に応じてエージェント再起動

## 使用例

- "auto-syncの状態を確認"
- "自動同期のログを見せて"
- "auto-syncを再起動"
- "自動同期を一時停止"
- "手動で同期を実行"

## auto-sync.shの動作

1. dotfilesディレクトリに移動
2. `brew bundle dump --force` でBrewfile更新
3. `git add -A` で変更をステージ
4. 変更がある場合のみコミット
5. リモートにプッシュ

## 注意事項

- エージェント停止中は自動同期されない
- 手動同期は `scripts/auto-sync.sh` で実行可能
- ログが肥大化したら手動で削除可能
- ネットワーク接続がない場合、プッシュは失敗する（次回実行時に再試行）
