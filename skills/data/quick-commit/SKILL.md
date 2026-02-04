---
name: quick-commit
description: "簡易コミット。変更をステージング、コミットメッセージ生成、コミット実行を一括で行う。PRは作成しない。トリガー: /quick-commit, クイックコミット, 簡易コミット"
user-invocable: true
allowed-tools: Bash, Read, Grep
model: haiku
---

# クイックコミット

変更をサッと一括コミットするためのスキル。PRは作成せず、ローカルコミットのみ。

## ユースケース

- 作業途中の保存ポイント
- 小さな修正の即コミット
- WIP (Work In Progress) コミット

## 実行フロー

```bash
# 1. 変更確認
git status
git diff --stat

# 2. 全変更をステージング
git add -A

# 3. コミットメッセージ生成
# 変更内容から自動生成

# 4. コミット実行
git commit -m "<message>"
```

## コミットメッセージ規則

### 自動判定

| 変更パターン | Prefix |
|-------------|--------|
| 新規ファイル追加 | `feat:` |
| バグ修正、エラー対応 | `fix:` |
| テストファイル | `test:` |
| ドキュメント (.md) | `docs:` |
| 設定ファイル | `chore:` |
| リファクタリング | `refactor:` |

### メッセージ生成例

```
feat: add user authentication module

- Add login endpoint
- Add JWT token generation
- Add password hashing
```

## 出力形式

```markdown
## クイックコミット完了

### 変更サマリー
- **追加**: 3 files
- **変更**: 2 files
- **削除**: 1 file

### コミット情報
- **ハッシュ**: abc1234
- **メッセージ**: feat: add user authentication module
- **ブランチ**: feature/auth

### 変更ファイル
```
A  src/auth/login.ts
A  src/auth/token.ts
A  src/auth/hash.ts
M  src/api/routes.ts
M  src/types/index.ts
D  src/deprecated/old-auth.ts
```

### 次のアクション
- `git push` でリモートにプッシュ
- `/commit-commands:commit-push-pr` でPR作成
```

## オプション

```bash
# メッセージ指定
/quick-commit fix: resolve null pointer exception

# WIPコミット
/quick-commit --wip
# → "WIP: work in progress" でコミット

# 特定ファイルのみ
/quick-commit src/api/
```

## 注意事項

- **機密ファイル除外**: .env, credentials等は自動除外
- **大量変更時は確認**: 50ファイル以上の変更は確認を求める
- **PRは作成しない**: PRが必要な場合は `/commit-commands:commit-push-pr` を使用
- **amend非対応**: 常に新規コミット（amend は明示的に実行）

## commit-push-pr との違い

| 機能 | quick-commit | commit-push-pr |
|------|--------------|----------------|
| ステージング | ✅ | ✅ |
| コミット | ✅ | ✅ |
| プッシュ | ❌ | ✅ |
| PR作成 | ❌ | ✅ |
| 用途 | 作業途中の保存 | 完成した変更の公開 |
