---
name: version-control-guidelines
description: Git運用ガイドライン、ブランチ戦略、コミットメッセージ（Conventional Commits）、プルリクエスト作成、個人開発とチーム開発の使い分けを定義する。Gitコミット作成時、ブランチ作成時、PR作成時、またはユーザーがコミットメッセージ、ブランチ戦略、バージョン管理、Conventional Commits、Semantic Versioningに言及した際に使用する。
---

# Version Control Guidelines

## 概要

このSkillは、Gitを使用したバージョン管理の運用ガイドラインを定義する。Conventional Commits形式のコミットメッセージ、適切なPRレビュープロセス、Semantic Versioningによるリリース管理など、品質を担保しつつ効率的な開発を実現することを目的とする。個人開発ではセルフレビュー可、チーム開発では最低1名のレビュー承認が必要となる。

## 責任範囲

このSkillは以下の範囲をカバーする:

- 個人開発とチーム開発の運用方針
- ブランチ戦略（個人開発・チーム開発別）
- コミットメッセージの記述ルール（Conventional Commits形式）
- プルリクエストのガイドライン
- マージ方針とコンフリクト解決
- タグとリリース管理（Semantic Versioning）

## 基本方針

### 共通ルール

以下のルールは個人開発・チーム開発に関わらず適用する:

- コミットメッセージ、PR、IssueにAI自動生成署名を記述しない
- メッセージは原則として英語で記述する
- チームの主要言語が英語以外の場合はその言語の使用を許可する
- プロジェクトにテンプレートがある場合はそちらを優先的に使用する

### 個人開発の場合

- シンプルなブランチ戦略を採用する
- コミットメッセージはConventional Commits形式で記述する
- セルフレビュー可
- 素早く実装して素早くリリースする
- ローカルでの実験的な作業を許容する

### チーム開発の場合

- Git Flowブランチ戦略を採用する
- コミットメッセージはConventional Commits形式で詳細に記述する
- 最低1名のレビュー承認が必要
- 品質とスピードのバランスを取る
- チーム全体でルールを統一する

## ブランチ戦略

### ブランチ戦略: 個人開発の場合

シンプルな2ブランチモデルを採用する。

**メインブランチ**:

- `main`: 本番環境にデプロイ可能な状態を保つ

**作業ブランチ**:

- `feat/機能名`: 新機能の開発
- `fix/修正内容`: バグ修正
- `exp/実験内容`: 実験的な実装（任意）

**運用フロー**:

1. `main`から作業ブランチを作成
2. 作業ブランチで実装
3. 動作確認後、`main`にマージ
4. 作業ブランチを削除

良い例:

```bash
# 新機能の開発
git checkout main
git pull
git checkout -b feat/user-auth
# 実装作業
git add .
git commit -m "ユーザー認証機能を実装"
git push origin feat/user-auth
# mainにマージ（PRは任意）
git checkout main
git merge feat/user-auth
git push origin main
git branch -d feat/user-auth
```

### ブランチ戦略: チーム開発の場合

Git Flow風のブランチモデルを採用する。

**永続ブランチ**:

- `main`: 本番環境にデプロイされている状態
- `develop`: 開発中の最新状態（次回リリース候補）

**一時ブランチ**:

- `feature/機能名`: 新機能の開発（developから分岐）
- `fix/修正内容`: バグ修正（developから分岐）
- `hotfix/緊急修正内容`: 本番環境の緊急修正（mainから分岐）
- `release/バージョン番号`: リリース準備（developから分岐）

**運用フロー**:

1. `develop`から作業ブランチを作成
2. 作業ブランチで実装
3. PRを作成してレビュー依頼
4. レビュー承認後、`develop`にマージ
5. リリース時に`develop`から`release`ブランチを作成
6. `release`ブランチで最終調整後、`main`と`develop`にマージ
7. `main`にタグを付ける

良い例:

```bash
# 新機能の開発
git checkout develop
git pull
git checkout -b feature/user-profile
# 実装作業
git add .
git commit -m "feat: ユーザープロフィール編集機能を実装"
git push origin feature/user-profile
# PRを作成してレビュー依頼
# レビュー承認後、GitHubでマージ
```

ホットフィックスの例:

```bash
# 本番環境の緊急修正
git checkout main
git pull
git checkout -b hotfix/login-error
# 修正作業
git add .
git commit -m "fix: ログインエラーを緊急修正"
git push origin hotfix/login-error
# PRを作成して迅速にレビュー
# マージ後、mainとdevelopの両方に反映
```

## コミットメッセージ

Conventional Commits形式を採用し、詳細な情報を記述する。

**基本形式**:

```text
<type>: <subject>

<body>

<footer>
```

**Type（必須）**:

- `feat`: 新機能
- `fix`: バグ修正
- `docs`: ドキュメント更新
- `style`: コードスタイル修正（フォーマット、セミコロンなど）
- `refactor`: リファクタリング
- `test`: テスト追加・修正
- `chore`: ビルドプロセス、ツール設定など
- `perf`: パフォーマンス改善

**Subject（必須）**:

- 50文字以内
- 命令形で記述（「〜を追加」「〜を修正」）
- 文末にピリオドを付けない

**Body（任意）**:

- 変更の理由や背景を記述
- 箇条書き（-）で記述する
- 72文字で改行

**Footer（任意）**:

- 破壊的変更（Breaking Changes）
- Issue番号（Closes #123, Fixes #456）

良い例:

```text
feat: add user profile editing feature

- Implement profile information editing (name, email, avatar)
- Add validation for profile fields
- Update user settings page UI

Closes #123
```

```text
fix: resolve session timeout issue on login

- Fix session expiration not being set correctly
- Review session management logic
- Set session timeout to 30 minutes

Fixes #456
```

破壊的変更の例:

```text
feat: change authentication API endpoint

- Migrate endpoint from /auth to /api/v2/auth
- Update API documentation
- Add deprecation notice for old endpoint

BREAKING CHANGE: Authentication API endpoint has been changed.
The /auth endpoint is deprecated, please use /api/v2/auth instead.
```

悪い例（AI自動生成署名の使用）:

```text
feat: add user profile editing feature

- Implement profile information editing

Closes #123

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

### コミットの粒度

- 論理的な変更単位でコミットする
- 1つのコミットで1つの変更を表現する
- WIPコミットは避ける（最終的にsquashする）

## プルリクエスト（PR）

**PRのタイトル**:

- コミットメッセージと同様の形式
- 50文字以内で簡潔に

**PRの説明**:

- 変更の概要
- 変更の理由
- 動作確認の内容
- レビュー観点
- 関連Issue（Closes #123）

PRテンプレート例:

```markdown
## Summary
Please describe the summary of this change.

## Changes
- Change 1
- Change 2
- Change 3

## Motivation
Why was this change necessary?

## Testing
- [ ] Tested in local environment
- [ ] Added test cases
- [ ] Verified existing tests pass

## Review Focus
Please describe what reviewers should focus on.

## Related Issues
Closes #123
```

悪い例（AI自動生成署名の使用）:

```markdown
## Summary
Implemented user profile editing feature.

## Changes
- Add profile editing UI
- Add validation logic

Closes #123

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### PRのレビュー

- 個人開発の場合はセルフレビューでOK
- チーム開発の場合は最低1名の承認が必要
- CI/CDが通ることを確認する

**コードレビューのポイント**:

- コーディング規約に従っているか
- テストが適切に追加されているか
- セキュリティ上の問題がないか
- パフォーマンスへの影響
- ドキュメントが更新されているか

**レビューコメントの書き方**:

```markdown
# 良いコメント例
[提案] この処理は共通関数として切り出せそうです。
再利用性が高まると思います。

[質問] この条件分岐の理由を教えていただけますか？

[重要] この実装はSQLインジェクションの脆弱性があります。
プリペアドステートメントを使用してください。

# 悪いコメント例
これはおかしい
なぜこう書いたの？
ダメ
```

## マージ方針

### マージ方法

**個人開発（シンプルブランチ戦略）の場合**:

- Merge Commit: 履歴を残したい場合
- Squash and Merge: コミット履歴をシンプルにしたい場合（推奨）
- Rebase and Merge: 線形の履歴を保ちたい場合

**チーム開発（Git Flow）の場合**:

- `feature` → `develop`: Squash and Merge（推奨）
- `develop` → `main`: Merge Commit（履歴を保つ）
- `hotfix` → `main`: Merge Commit（緊急性を記録）

### コンフリクト解決

- コンフリクトが発生したら、必ず元のブランチを最新化してから解決する
- 解決後は必ずテストを実行する
- 不明な点があればチームに相談する

コンフリクト解決例:

```bash
# developを最新化してコンフリクト解決
git checkout feature/user-profile
git fetch origin
git rebase origin/develop
# コンフリクト解決
git add .
git rebase --continue
# テスト実行
npm test
git push origin feature/user-profile --force-with-lease
```

## タグとリリース管理

セマンティックバージョニング（Semantic Versioning）を採用する。

**バージョン形式**: `MAJOR.MINOR.PATCH`

- `MAJOR`: 破壊的変更
- `MINOR`: 新機能追加（後方互換性あり）
- `PATCH`: バグ修正（後方互換性あり）

良い例:

```bash
# パッチリリース（バグ修正）
git tag -a v1.0.1 -m "ログインバグを修正"

# マイナーリリース（新機能）
git tag -a v1.1.0 -m "ユーザープロフィール機能を追加"

# メジャーリリース（破壊的変更）
git tag -a v2.0.0 -m "認証APIのエンドポイントを変更（Breaking Change）"

git push origin --tags
```

## ベストプラクティス

- 頻繁にコミットする
- 定期的にリモートにpushする（バックアップ）
- 実験的なブランチは気軽に作成する（個人開発の場合）
- 不要になったブランチはこまめに削除する
- developブランチを常に最新に保つ（チーム開発の場合）
- PRは小さく保つ（500行以内を目安）
- レビューは24時間以内に対応する（チーム開発の場合）
- コンフリクトは早めに解消する
- コミット前にテストを実行する
- 機密情報をコミットしない

## チェックリスト

### ブランチ作成時

- [ ] 最新のコードを取得した（個人開発: main、チーム開発: develop）
- [ ] 適切なブランチ名を付けた（個人開発: feat/fix/、チーム開発: feature/fix/）
- [ ] ブランチの目的が明確である

### コミット時

- [ ] Conventional Commits形式でコミットメッセージを記述した
- [ ] メッセージを英語で記述した（チームの主要言語が英語以外の場合はその言語でOK）
- [ ] 本文を箇条書き（-）で記述した
- [ ] AI自動生成署名を含めていない
- [ ] 論理的な変更単位でコミットした
- [ ] テストが通ることを確認した
- [ ] 機密情報を含めていない
- [ ] コーディング規約に従っている

### PR作成時

- [ ] PRテンプレートに従って記載した（プロジェクトにテンプレートがある場合はそちらを優先）
- [ ] 説明を英語で記述した（チームの主要言語が英語以外の場合はその言語でOK）
- [ ] AI自動生成署名を含めていない
- [ ] 関連Issueを参照した（Closes #123）
- [ ] 動作確認を実施した
- [ ] テストを追加した
- [ ] ドキュメントを更新した（必要に応じて）
- [ ] レビュアーを指定した（チーム開発の場合）

### マージ時

- [ ] 動作確認が完了している
- [ ] レビュー承認を得た（個人開発の場合はセルフレビュー、チーム開発の場合は最低1名）
- [ ] CI/CDが通っている
- [ ] コンフリクトが解消されている
- [ ] ベースブランチが最新である（チーム開発の場合は特にdevelopブランチ）
- [ ] テストが通っている

### リリース時

- [ ] 動作確認が完了している
- [ ] releaseブランチから最終確認を実施した（チーム開発の場合）
- [ ] セマンティックバージョニングに従ってタグを付けた
- [ ] リリースノートを作成した
- [ ] mainとdevelopの両方に反映した（チーム開発の場合）
