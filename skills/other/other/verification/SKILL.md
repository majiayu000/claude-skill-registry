---
name: verification
description: 本番環境（bakenkaigi.com）での動作確認ワークフロー。PRマージ後やコード修正後に「動作確認して」「本番確認して」「デプロイ確認して」と言われた時に使用する。ブラウザ自動操作でログイン→PR変更の反映確認→全体チェック→不具合があればIssue起票→修正まで行う。baken-kaigiリポジトリ専用。
version: 1.0.0
tools:
  - Bash
  - Read
  - Edit
  - Write
  - Glob
  - Grep
  - browser
  - gh
skill_type: workflow
auto_invoke: false
---

# 本番環境 動作確認スキル

## 入力形式

```
/verification
```

または PR番号を指定：

```
/verification <PR番号>
```

「動作確認して」「本番確認して」「デプロイ確認して」でも発動する。

## 安全ルール

**絶対禁止:**
- IPAT購入の実行（「購入する」ボタンを押さない。購入確認画面の表示確認まではOK）
- テストアカウント認証情報のコミット
- 本番データの変更・削除

## 認証情報

テストアカウント情報は `.claude/verification.local.json` に平文JSONで保存する（gitignore済みだがファイル自体は暗号化されない）。

```json
{
  "email": "テストユーザーのメールアドレス",
  "password": "テストユーザーのパスワード"
}
```

初回実行時にファイルが存在しない場合、ユーザーに認証情報を確認して保存する。保存後、ファイル権限を `chmod 600` で制限する。

## ワークフロー

### Step 1: 変更内容の把握

**PRマージ直後の場合：**
```bash
gh pr view <number> --json title,body,files
```
変更ファイルから影響範囲を特定し、重点確認ポイントを決定する。

**汎用的な動作確認の場合：**
直近のコミットやユーザーの指示から確認範囲を判断する。特定の指示がなければ全体チェック（Step 5）を実施する。

### Step 2: デプロイ完了の確認

マージ後は自動デプロイが走る（手動デプロイ不要）。

```bash
gh run list --limit 5
```

- `completed` + `success` になるまで待機
- 最大45分（CDK 30分 + AgentCore/EC2 15分）
- 失敗時はユーザーに報告して判断を仰ぐ
- 汎用確認の場合やデプロイ済みの場合はこのステップをスキップ

### Step 3: ブラウザでログイン

Playwright MCP（`browser_*` ツール）を使用する。

1. `browser_navigate` で `https://bakenkaigi.com/login` にアクセス
2. `.claude/verification.local.json` から認証情報を読み込み
3. `browser_snapshot` でログインフォームの要素を取得
4. `browser_fill_form` または `browser_type` でメール・パスワードを入力
5. `browser_click` でログインボタンをクリック
6. `browser_snapshot` でログイン成功を確認（ホーム画面への遷移）
7. Cookie同意バナーが表示された場合は拒否（プライバシー優先）

### Step 4: PR変更の反映確認（重点）

Step 1で特定した変更箇所を優先的に確認：
- UI変更 → 該当ページで視覚的に確認
- API変更 → 関連する画面操作を実行して応答を確認
- バグ修正 → 修正前の再現手順を試して再現しないことを確認
- 新機能 → 機能を実際に操作して期待通り動くことを確認

### Step 5: 全体チェック

[references/verification-checklist.md](references/verification-checklist.md) に従って、各ページを順に確認する。

各ページで必ず以下を実施：
- `browser_console_messages` でJSエラーを確認（level: "error"）
- `browser_network_requests` でAPIエラーを確認
- `browser_take_screenshot` でレイアウト崩れを目視確認
- `browser_snapshot` で要素のアクセシビリティツリーを確認

**開催日データの確認:** レース一覧は開催日にのみデータが表示される。非開催日は「レースがありません」等の表示が正しいことを確認する。

### Step 6: 不具合発見時の対応

不具合を発見した場合：

1. **証拠を残す:** スクリーンショット撮影 + コンソールログ保存
2. **Issue起票:**
   ```bash
   gh issue create --title "bug: [概要]" --body "$(cat <<'EOF'
   ## 再現手順
   1. ...

   ## 期待される動作
   ...

   ## 実際の動作
   ...

   ## スクリーンショット
   （該当する場合添付）

   ## 環境
   - URL: https://bakenkaigi.com/
   - ブラウザ: Chrome
   EOF
   )"
   ```
3. **修正:** featureブランチを作成して修正 → PR作成
4. **再確認:** マージ後、デプロイ完了を待って再度動作確認

### Step 7: 完了報告

全チェック完了後、結果をユーザーに報告：
- 確認した項目数
- 発見した不具合（あれば Issue番号付き）
- 全体の所感
