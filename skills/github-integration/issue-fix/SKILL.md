---
name: issue-fix
description: >-
  ユーザーが「Issue #N を解決」「Issueを解決して」「Issue を fix」等と要求した時に使用。
  GitHub Issueの完全な解決ワークフローを自動実行。
  Issue分析、テストファースト開発、最小限の修正実装、PR作成まで一貫して処理。
allowed-tools: Read, Write, Grep, Glob, Bash, Git
---

### 手順
1. Issue分析: 内容/再現手順を抽出し、影響ファイルを特定（Grep/Glob）
2. テストファースト: 再現テストを先に追加/更新し、`go test` で失敗を確認
3. 修正実装: 必要最小限の修正でテストをグリーンに
4. ドキュメント更新: `CHANGELOG.md` を更新
5. PR作成: ブランチ→コミット→PRを作成（本文はテンプレ準拠で他のスキルが生成可能）
