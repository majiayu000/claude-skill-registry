---
name: release-har
description: "汎用リリース自動化。CHANGELOG、コミット、タグ、GitHub Release をサポート。Use when user mentions release, version bump, create tag, publish release. Do NOT load for: harness release (use x-release-harness instead)."
allowed-tools: ["Read", "Write", "Edit", "Bash"]
argument-hint: "[patch|minor|major]"
context: fork
---

# Release Har Skill

汎用的なリリース自動化スキル。任意のプロジェクトで使用可能。

## Quick Reference

- "**リリースして**" → `/release-har`
- "**バージョンを上げて**" → `/release-har patch`
- "**マイナーリリース**" → `/release-har minor`

---

## Execution Flow

### Step 1: 現在の状態確認

以下を並列で実行:

```bash
# 未コミットの変更
git status

# 変更ファイル一覧
git diff --stat

# 最近のコミット履歴
git log --oneline -10

# 既存タグの確認
git tag --sort=-v:refname | head -5
```

### Step 2: バージョン決定

[Semantic Versioning](https://semver.org/) に基づいてバージョンを決定:

| バージョン | 変更内容 |
|-----------|----------|
| **patch** (x.y.Z) | バグ修正、軽微な改善 |
| **minor** (x.Y.0) | 新機能（後方互換性あり） |
| **major** (X.0.0) | 破壊的変更 |

ユーザーに確認: "次のバージョンは？ (例: 1.2.3)"

### Step 3: CHANGELOG 更新（存在する場合）

プロジェクトに CHANGELOG.md があれば更新:

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- 新機能

### Changed
- 変更点

### Fixed
- バグ修正
```

**CHANGELOG が存在しない場合はスキップ**

### Step 4: バージョンファイル更新（プロジェクト依存）

プロジェクトの構成に応じてバージョンファイルを更新:

| ファイル | 更新方法 |
|----------|----------|
| `package.json` | `"version": "X.Y.Z"` |
| `pyproject.toml` | `version = "X.Y.Z"` |
| `VERSION` | 内容を直接更新 |
| `Cargo.toml` | `version = "X.Y.Z"` |

**該当ファイルがなければスキップ**

### Step 5: コミットとタグ

```bash
# ステージング
git add -A

# コミット（変更がある場合のみ）
git commit -m "chore: release vX.Y.Z"

# タグ作成
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

### Step 6: プッシュ

```bash
# ブランチをプッシュ
git push origin $(git branch --show-current)

# タグをプッシュ
git push origin vX.Y.Z
```

### Step 7: GitHub Release（オプション）

ユーザーに確認後、GitHub Release を作成:

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z - タイトル" \
  --notes "$(cat <<'EOF'
## What's Changed

- 変更内容1
- 変更内容2

**Full Changelog**: https://github.com/OWNER/REPO/compare/vPREV...vX.Y.Z
EOF
)"
```

---

## オプション

| オプション | 説明 |
|-----------|------|
| `patch` | パッチバージョンを自動インクリメント |
| `minor` | マイナーバージョンを自動インクリメント |
| `major` | メジャーバージョンを自動インクリメント |
| `--dry-run` | 実行せずに確認のみ |

---

## プロジェクト固有の対応

### Node.js (package.json)

```bash
npm version patch --no-git-tag-version
```

### Python (pyproject.toml)

手動で `version = "X.Y.Z"` を更新

### Rust (Cargo.toml)

手動で `version = "X.Y.Z"` を更新

---

## Related Skills

- `x-release-harness` - Harness プラグイン専用リリース（ローカルのみ）
- `verify` - リリース前の検証
