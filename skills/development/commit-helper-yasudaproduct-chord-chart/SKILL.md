---
name: commit-helper
description: Git コミットメッセージ作成とPR作成を支援。コミット、プッシュ、プルリクエスト作成の際に使用。
disable-model-invocation: true
---

# コミット・PR作成スキル

ChordBook プロジェクトの Git ワークフローガイドラインです。

## コミットメッセージ規約

### フォーマット
```
<type>: <subject>
```

### Type 一覧
| Type | 説明 |
|------|------|
| `feat` | 新機能 |
| `fix` | バグ修正 |
| `docs` | ドキュメントのみの変更 |
| `style` | コードの意味に影響しない変更（空白、フォーマット等） |
| `refactor` | バグ修正でも新機能でもないコード変更 |
| `test` | テストの追加・修正 |
| `chore` | ビルドプロセスや補助ツールの変更 |

### 例
```
feat: 楽曲検索機能を追加
fix: ログイン時のエラーハンドリングを修正
docs: API仕様書を更新
refactor: Song エンティティのバリデーションを整理
test: SongController の単体テストを追加
chore: ESLint 設定を更新
```

## コミット作成手順

1. **変更内容を確認**
   ```bash
   git status
   git diff
   ```

2. **ステージング**
   ```bash
   git add <specific-files>  # 特定ファイルを追加（推奨）
   # または
   git add -A  # 全ファイル追加
   ```

3. **コミット**
   ```bash
   git commit -m "<type>: <subject>"
   ```

## プルリクエスト作成

### PR タイトル
コミットメッセージと同じ規約を使用：
```
feat: 楽曲検索機能を追加
```

### PR 本文テンプレート

```markdown
## 概要
<!-- 変更内容の簡潔な説明 -->

## 変更内容
-
-

## テスト方法
- [ ]
- [ ]

## スクリーンショット（UI変更がある場合）

## 関連Issue
closes #
```

### PR 作成コマンド
```bash
gh pr create --title "<type>: <subject>" --body "..."
```

## ブランチ運用

### ブランチ命名規則
```
feature/<機能名>    # 新機能
fix/<バグ名>        # バグ修正
docs/<ドキュメント名> # ドキュメント
refactor/<対象>     # リファクタリング
```

### 例
```
feature/song-search
fix/login-error-handling
docs/api-specification
refactor/song-validation
```

## 注意事項

- コミット前に `pnpm lint` (FE) や `dotnet build` (BE) を実行
- 機密情報（.env, credentials）をコミットしない
- 大きな変更は小さなコミットに分割
- コミットは論理的な単位で行う
