---
name: pr-ci-sonar-closure
description: >
  PR を人間に引き渡す直前に CI 完了監視→失敗解析→get-sonar-feedback→/pr-review レポート→最終報告までを一気通貫で実行するフロー。
---
## ゴール
- CI が完走し、失敗時は原因と対処方針を記録したうえで再実行する
- `get-sonar-feedback <pr>` で重大指摘がない状態を確認する（残る場合は TODO と根拠を残す）
- `/pr-review` を用いた最終レビューと、人間レビュアーに渡すための要約コメントを作成する

## 事前条件と入力
1. 作業中ブランチが対象 PR に紐づいていること  
2. `gh` CLI がログイン済み  
3. `get-sonar-feedback` コマンドが利用可能  
4. `/ci-status` `/pr-review` など既存コマンドを呼べる状態

## 手順

### 1. PR メタ情報の取得
```bash
TARGET_REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
PR_NUMBER=$(gh pr view --json number -q .number 2>/dev/null || gh pr status --json currentBranch -q '.currentBranch.pullRequest.number')
```
- どちらか取得できない場合はユーザーへ確認。

### 2. CI 完了を監視
- `gh pr checks "$PR_NUMBER" --repo "$TARGET_REPO" --watch`
- 実行中に失敗が出たら `/ci-status` の手順でログを精査し、修正 or 再実行。  
- 再実行後も同じコマンドで完了まで待機する。

### 3. CI 失敗時の対処
1. `/ci-status` を実行して失敗したジョブと原因を特定
2. 関連ファイルを修正し、必要なテストを回す
3. `git status -sb` で差分を確認してからコミット/プッシュ
4. 再度 Step 2 へ戻り、CI が緑になるまで繰り返す

### 4. get-sonar-feedback の実行
- Sonar CI は完了まで約10分かかることがあるため、CI 完了後に待機する。
```bash
source .envrc && get-sonar-feedback pr
```
- `.codex/prompts/sonar-feedback.md` のフローに従い、Critical/High を最優先で処理
- 指摘が残る場合は修正→コミット/プッシュ→Step 2 に戻って CI 完了を待機し、再度この手順を実行する
- 解決できない場合は理由と代替策を明記し、TODO を残してレビュアーに伝える

### 5. PR レビュー結果の整理
- `/pr-review $TARGET_REPO $PR_NUMBER` を実行し、差分・テスト・CI 状況をまとめる
- `USER_DIRECTIVES` があれば反映方法をレポートに記載

### 6. 人間レビュアーへの報告
- 上記結果をまとめた文章をコメント下書きとして生成  
- 含めるべき内容:
  - CI ステータス（成功/失敗・再実行履歴）
  - Sonar 指摘の対応状況
  - 追加で行ったテストや確認事項
  - レビュアーに見てほしい観点
- 必要に応じて `gh pr comment` や `gh pr view --json url` を使い、URL とともに共有する
- 最終報告前にコミット/プッシュが完了していることを必ず確認する

## リスクとメモ
- CI 失敗を無視して次工程へ進まない
- Sonar で Critical が残ったまま完了させない
- 途中で不明点が出たら直ちにユーザーへ質問し、独断のフォールバックを行わない
