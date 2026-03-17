---
name: profile-switch
description: 保存済みの Google 認証プロファイルを切り替える。「アカウント切替」「プロファイル変更」「別アカウントで使いたい」「Google アカウントを変える」「認証を切り替え」などで起動。
allowed-tools: [Read, Bash]
---

# Profile Switch

保存済み認証プロファイルを切り替えます。

## 実行方法

### プロファイル一覧を表示

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_auth.py profiles
```

### プロファイルを切り替え

```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_auth.py switch <profile-name>
```

例:
```bash
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_auth.py switch work
python ${CLAUDE_PLUGIN_ROOT}/scripts/google_auth.py switch personal
```

## 保存場所

- 設定ディレクトリ: `~/.config/shiiman-google/`
- トークンファイル: `~/.config/shiiman-google/tokens/<profile-name>.json`
- アクティブプロファイル: `~/.config/shiiman-google/active-profile`

## 注意事項

- 切り替え先のプロファイルは事前に認証されている必要があります
- 新しいプロファイルを追加するには「Google ログイン」と言ってください
