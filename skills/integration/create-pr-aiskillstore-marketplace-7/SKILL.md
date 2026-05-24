---
name: create-pr
description: GitHub Pull Request作成スキル - 変更内容の自動サマリー、PR説明文生成、GitHub PRの作成を行います。git diffでの変更分析、コミットメッセージ取得、変更ファイル分類を行い、高品質なPR説明文を自動生成します。qa-check実行済みであることを前提とし、リモートへのプッシュとgh CLIによるPR作成を実行します。
---

# Create PR Skill - GitHub Pull Request作成スキル

## 役割

GitHub Pull Requestの作成を自動化するスキルです。変更内容の分析、PR説明文の自動生成、GitHub PRの作成を行います。

## 実行フロー

### Phase 1: 事前確認

#### 1-1. ブランチ確認
```bash
# 現在のブランチを確認
git branch --show-current

# mainブランチでないことを確認
# mainブランチの場合はエラー
```

#### 1-2. 変更内容確認
```bash
# リモートブランチとの差分確認
git fetch origin
git log origin/main..HEAD --oneline

# 変更ファイル一覧確認
git diff origin/main...HEAD --name-only

# 変更行数確認
git diff origin/main...HEAD --stat
```

### Phase 2: 変更内容分析

#### 2-1. コミットメッセージ取得
```bash
# 全コミットメッセージ取得
git log origin/main..HEAD --pretty=format:"%s"
```

#### 2-2. 変更ファイル分類
- Backend変更: `backend/` 配下のファイル
- Frontend変更: `frontend/` 配下のファイル
- ドキュメント変更: `documents/` 配下のファイル
- その他: その他のファイル

#### 2-3. 変更種別判定
- 新機能: `feature/` ブランチ、大量の新規ファイル
- バグ修正: `fix/` ブランチ、少数のファイル変更
- リファクタリング: `refactor/` ブランチ
- ドキュメント更新: `docs/` ブランチ

### Phase 3: PR説明文生成

#### 3-1. PRタイトル生成（pr_title未指定時）
```
# 形式: [変更種別] 簡潔な説明 (closes #[issue_number])
# 例:
# - feat: ユーザープロフィール機能の実装 (closes #123)
# - fix: ログインセッションエラーの修正 (closes #456)
# - refactor: UserServiceのDRY原則適用 (closes #789)
# - docs: チャンネル設定機能仕様書を更新 (closes #101)
```

#### 3-2. PR本文生成
````markdown
## 概要
[変更の概要を1-2文で説明]

## 変更内容

### Backend変更（該当する場合）
- **API**: [実装/修正したエンドポイント]
- **データベース**: [追加/変更したテーブル]
- **ビジネスロジック**: [実装/修正した機能]

### Frontend変更（該当する場合）
- **ページ**: [実装/修正したページ]
- **コンポーネント**: [作成/修正したコンポーネント]
- **UI/UX**: [追加/変更した機能]

### ドキュメント変更（該当する場合）
- [更新したドキュメント一覧]

## テスト
- 単体テスト: [テスト数] 件追加/修正
- カバレッジ: [数値]%
- 動作確認: ✅ 完了

## チェックリスト
- [x] コーディング規約準拠
- [x] テスト実装（カバレッジ80%以上）
- [x] Lint/ビルド成功
- [x] ドキュメント更新（該当する場合）
- [x] サーバー起動・動作確認完了

## 関連Issue
Closes #[issue_number]

## スクリーンショット（該当する場合）
[画面キャプチャ等があれば追加]

## 補足
[特記事項があれば記載]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
````

### Phase 4: Git操作

#### 4-1. 変更のコミット確認
```bash
# 未コミットの変更がないか確認
git status

# ステージングされていない変更がある場合は警告
```

#### 4-2. リモートへプッシュ
```bash
# 現在のブランチをリモートにプッシュ
git push -u origin [current-branch]
```

### Phase 5: GitHub PR作成

#### 5-1. gh CLI でPR作成
```bash
# gh CLIを使用してPR作成
gh pr create \
  --base [base_branch] \
  --title "[PRタイトル]" \
  --body "$(cat <<'EOF'
[PR本文]
EOF
)"
```

#### 5-2. PR URL取得
```bash
# 作成されたPRのURLを取得
gh pr view --web
```

### Phase 6: 完了報告

```markdown
## Create PR 完了報告

### PR情報
- **PR URL**: [URL]
- **タイトル**: [PRタイトル]
- **ベースブランチ**: [base_branch]
- **Issue**: #[issue_number]

### 変更サマリー
- Backend変更: [ファイル数] ファイル、[行数] 行
- Frontend変更: [ファイル数] ファイル、[行数] 行
- ドキュメント変更: [ファイル数] ファイル、[行数] 行

### 次のステップ
Pull Requestのレビューを依頼してください。
```

## エラーハンドリング

### mainブランチで実行された場合
- エラーメッセージを表示
- PR作成を中止
- ユーザーに新しいブランチ作成を促す

### 未コミットの変更がある場合
- 警告メッセージを表示
- コミットを促す
- PR作成を中止

### リモートプッシュ失敗
- エラー内容を確認
- リモートブランチとの競合を確認
- ユーザーに手動解決を促す

### gh CLI認証エラー
- gh auth status で認証状態確認
- gh auth login でログインを促す

## 使用ツール

### 必須ツール
- **Bash**: git操作、gh CLI実行

### 推奨ツール
- **Read**: レポートファイル確認（QA結果等）
- **Grep**: 変更内容の詳細確認

## 重要な注意事項

### PR作成前の必須チェック
1. **qa-check実行**: 品質保証が完了していること
2. **すべてコミット済み**: 未コミットの変更がないこと
3. **mainブランチでない**: 作業ブランチであること

### PRタイトル規約
- プレフィックス: feat/fix/refactor/docs/chore のいずれか
- 簡潔かつ具体的な説明
- Issue番号を含める（closes #[number]）

### PR本文の品質
- 変更内容を明確に記載
- テスト実施状況を記載
- チェックリストをすべて確認
- 関連Issueを明記

## 参照ドキュメント

### 必須参照
- `documents/development/development-policy.md`: 開発ガイドライン

### GitHubドキュメント
- GitHub CLI（gh）使用方法
- Pull Request作成ガイド
