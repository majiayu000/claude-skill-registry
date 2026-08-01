---
name: ios-cli-tasks
description: QuickTypeの`.vscode/tasks.json`に定義されたiOSアプリ開発用コマンド（Simulator起動、xcodebuild、simctlインストール/起動など）をCLIから再現する。タスクごとの依存関係を解決してシミュレータ検証を自動化したいときに使用する。
---

name: ios-cli-tasks
description: QuickTypeの`.vscode/tasks.json`に定義されたiOSアプリ開発用コマンド（Simulator起動、xcodebuild、simctlインストール/起動など）をCLIから再現する。タスクごとの依存関係を解決してシミュレータ検証を自動化したいときに使用する。
---

# iOS CLI Tasks

QuickTypeリポジトリ直下で `.vscode/tasks.json` に定義された iOS ビルド/シミュレータ系コマンドを CLI から呼び出すための手順とスクリプトです。VSCode UI を開かなくても同じワークフローを再現できます。

## 1. リファレンス
- タスクの目的とコマンドは [references/ios-cli-commands.md](references/ios-cli-commands.md) を参照してください。

## 2. CLIスクリプト
`scripts/run_ios_cli_task.py` はタスクラベルをキーに依存関係を解決しながらコマンドを順次実行します。

### 2.1 事前条件
- QuickTypeリポジトリ直下で実行すること。
- Xcodeコマンドラインツールとシミュレータが使用可能であること。

### 2.2 使い方
```bash
# タスク一覧
python3 skills/ios-cli-tasks/scripts/run_ios_cli_task.py --list

# 例1: シミュレータの起動のみ
python3 skills/ios-cli-tasks/scripts/run_ios_cli_task.py "Simulator: Open"

# 例2: 依存関係込みでビルド→インストール→起動まで実行
python3 skills/ios-cli-tasks/scripts/run_ios_cli_task.py "iOS: Boot iPhone 16 Pro & Run"
```
- 依存タスクは一度だけ実行されます。
- コマンドが失敗した場合はその場で停止し、エラーを報告します。

### 2.3 トラブルシューティング
- `.vscode/tasks.json` のタスク名が変わった場合はスクリプトに自動反映されますが、コマンド側の仕様変更があればリファレンスファイルを更新してください。
- `xcrun simctl` 系で「No devices are booted」となる場合は `Simulator: Open` または `xcrun simctl boot` を先に実行してください。

## 3. 運用ノート
1. CIで用いる際もローカルと同じ `xcodebuild` パラメータになるため、ビルド差異が出にくくなります。
2. `.vscode/tasks.json` を更新したら本スキルのリファレンスも更新し、変更日の記載を忘れないでください（例: `2024年11月05日 更新`）。
3. `run_ios_cli_task.py` の派生ツールが必要になった場合は `scripts/` 以下に追記し、SKILL.mdから参照してください。
