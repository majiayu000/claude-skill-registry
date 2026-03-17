---
name: git-workflow
description: Git操作とリリースの自動化。コンベンショナルコミット形式(日本語)でのコミットメッセージ生成、セマンティックバージョニング、変更履歴生成、デプロイ手順。commit、version、changelog、git、コミットメッセージ、deploy、release、build時に使用。
---

# Git Workflow スキル

## コミットメッセージ形式

```
<type>(<scope>): <日本語で50文字以内の説明>

<body: 変更点を箇条書き>

<footer: Closes #番号 等>

Co-Authored-By: Claude <noreply@anthropic.com>
```

**タイプ:**

| タイプ | 用途 | 例 |
|--------|------|-----|
| `feat` | 新機能 | feat(auth): ログイン機能を追加 |
| `fix` | バグ修正 | fix(timer): タイマー停止問題を修正 |
| `refactor` | リファクタリング | refactor(utils): ヘルパー関数を整理 |
| `docs` | ドキュメント | docs(readme): セットアップ手順を追加 |
| `style` | コードスタイル | style: フォーマットを統一 |
| `perf` | パフォーマンス | perf(render): 描画速度を最適化 |
| `test` | テスト | test(api): APIテストを追加 |
| `chore` | ビルド・設定 | chore(deps): 依存関係を更新 |
| `ci` | CI/CD | ci(github): ワークフローを追加 |

**スコープ例:** コンポーネント名(`header`, `modal`)、機能名(`auth`, `timer`)、レイヤー名(`api`, `ui`)

## Working Documents参照によるスコープ自動決定

コミット作成時、Working Documentsが存在する場合は自動参照します。

### スコープの自動抽出

1. 現在のブランチからIssue番号を抽出（例: `fix/#123-xxx` → `123`）
2. `docs/working/` ディレクトリで該当Issue番号のWorking Documentsを検索
3. `design.md` の「変更対象ファイル」セクションから主要な変更箇所を抽出
4. スコープを自動決定:
   - 単一機能の場合: 機能名をスコープに使用（例: `auth`, `timer`）
   - 複数機能の場合: 最も影響が大きい機能をスコープに使用
   - 共通UIの場合: `ui` をスコープに使用

### 動作例

```bash
# ブランチ: fix/#123-login-validation
# Working: docs/working/20260205_123_ログインバリデーション修正/design.md
# → design.mdから「app/auth/login/page.tsx」を検出
# → スコープ: auth

git commit -m "fix(auth): ログインバリデーションを修正"
```

### フォールバック

Working Documentsが存在しない、またはスコープが自動決定できない場合は、従来通りファイルパスから判断します。

## コミット手順

```bash
# 1. 変更確認
git diff --staged --stat && git diff --staged

# 2. コミット（複数行はHEREDOC使用）
git commit -m "$(cat <<'EOF'
fix(auth): ログインバリデーションを修正

- メールアドレスの正規表現を改善
- エラーメッセージ表示を追加

Closes #123

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

## セマンティックバージョニング

`MAJOR.MINOR.PATCH` — package.jsonの`version`フィールドを更新。

| 変更種別 | バージョン | コマンド |
|----------|-----------|---------|
| 破壊的変更 | MAJOR | `npm version major` |
| 新機能 | MINOR | `npm version minor` |
| バグ修正 | PATCH | `npm version patch` |

## リリースノート形式

```markdown
# v0.6.0 (2026-02-01)

## 追加
- 新機能の説明

## 修正
- バグ修正の説明

## 変更
- 既存機能の変更
```

## リリースノート自動生成

Git logからコンベンショナルコミット形式のコミットを抽出し、Markdown形式のリリースノートを自動生成します。

```bash
# 前回のタグから現在までの変更を抽出
uv run scripts/generate-release-notes.py --from v0.10.0 --version v0.11.0 --output RELEASE_NOTES.md

# package.jsonのversionも更新
uv run scripts/generate-release-notes.py --from v0.10.0 --version v0.11.0 --update-package-json --output RELEASE_NOTES.md

# 2つのタグ間の差分
uv run scripts/generate-release-notes.py --from v0.9.0 --to v0.10.0 --output RELEASE_NOTES_0.10.0.md
```

**機能:**
- コンベンショナルコミット形式の自動パース（`feat:`, `fix:`, `refactor:` 等）
- カテゴリ別に分類（追加/修正/変更/その他）
- package.jsonのversionフィールド自動更新（オプション）

## デプロイ

**デプロイ前チェック:**
```bash
npm run lint && npm run build && npm run test
```

**Vercel:** `git push origin main` で自動デプロイ
**Firebase Hosting:** `npm run build && firebase deploy --only hosting`

## ルール

- コミットメッセージは**日本語**
- 1コミット = 1つの論理的変更
- mainブランチへの直接コミット禁止
- デプロイ前に必ずテスト実行
