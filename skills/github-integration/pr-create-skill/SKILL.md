---
name: pr-create-skill
description: 明示的に呼び出されたときにのみ読み込みます。エージェントが自律的に呼び出す必要はありません。
---

## 事前確認

- ユーザからマージ先のブランチを受け取ります。
- 現在開いているブランチ名に含まれる {大文字の英字列-数字}を Jira に紐つく {PROJECT-KEY} と認識します。

## 実行内容
- `git diff` で、現在のブランチとリモートのマージ先ブランチを比較し、変更の詳細を確認（例: `this_branch` と `origin/main` を比較）
- `gh pr create` でプルリクエストを作成
  - プルリクエストの内容に記載する文章は、すべて説明的にして、想定ターゲットの存在しない内容にしてください。

Pull Request 作成には以下を参照してください。

- [Pull Request テンプレート](./references/PULL_REQUEST_TEMPLATE.md)
- [ドキュメント作成ガイドライン](../common/references/documents.md)
