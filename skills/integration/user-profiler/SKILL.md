---
name: user-profiler
description: Slack ユーザーのプロファイル情報を取得する。「ユーザー情報」「プロファイル見せて」「ユーザープロファイル」「〇〇さんの情報」「このユーザーは誰」「アカウント情報」「メンバー情報」などで起動。公式Slack MCPの `slack_get_user_profile` を使用。
allowed-tools: [FetchMcpResource]
---

# User Profiler

Slack ユーザーのプロファイル情報を取得します。

## ワークフロー

### 1. ユーザーIDの確認

対象ユーザーのIDを確認

### 2. プロファイル取得

公式Slack MCPの `slack_get_user_profile` ツールを使用:

```
slack_get_user_profile(
  user_id="U01234567"
)
```

### 3. 結果の表示

ユーザープロファイル情報を表示:

```
# ユーザープロファイル

名前: 山田太郎
表示名: yamada
メール: yamada@example.com
タイトル: Senior Engineer
ステータス: 🏠 リモートワーク中
```

## 注意事項

このスキルは読み取り専用です。プロファイル情報の変更はできません。

## コマンド連携

実際の処理は `/shiiman-slack:user-profile` に委譲します（SSOT として扱う）。
