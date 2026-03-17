---
name: release-har
description: "Universal release automation. CHANGELOG, commit, tag, GitHub Release supported. Use when user mentions release, version bump, create tag, publish release. Do NOT load for: harness release (use x-release-harness instead)."
description-en: "Universal release automation. CHANGELOG, commit, tag, GitHub Release supported. Use when user mentions release, version bump, create tag, publish release. Do NOT load for: harness release (use x-release-harness instead)."
description-ja: "汎用リリース自動化。CHANGELOG、コミット、タグ、GitHub Release をサポート。Use when user mentions release, version bump, create tag, publish release. Do NOT load for: harness release (use x-release-harness instead)."
allowed-tools: ["Read", "Write", "Edit", "Bash"]
argument-hint: "[patch|minor|major|--dry-run|--announce]"
context: fork
---

# Release Har Skill

Universal release automation skill. Works with any project.

## Quick Reference

- "**release**" → `/release-har`
- "**bump version**" → `/release-har patch`
- "**minor release**" → `/release-har minor`
- "**preview only**" → `/release-har --dry-run`

## References

| Document | 内容 |
|----------|------|
| [references/release-notes-template.md](references/release-notes-template.md) | GitHub Release Notes テンプレート（4セクション構造） |
| [references/changelog-format.md](references/changelog-format.md) | CHANGELOG.md フォーマット（Keep a Changelog 準拠） |
| [.claude/rules/github-release.md](../../.claude/rules/github-release.md) | Release Notes フォーマットルール（正本） |

---

## Branch Policy

**単独開発プロジェクトでは main への直接 push を許容する。**

- CI が `push: branches: [main]` で全検証を実行するため、PR なしでも品質ゲートは機能する
- `release.yml` が `v*` タグ push 時に GitHub Release の存在を保証するセーフティネットとして動作する
- force push（`--force` / `--force-with-lease`）は禁止

共同開発者がいるプロジェクトでは、PR 経由のマージに切り替えること。

---

## Execution Flow

### Pre-flight: 事前チェック（必須）

リリース開始前に以下を確認する。失敗した場合はリリースを停止し修正を促す。

```bash
# 1. gh コマンドの存在確認
if ! command -v gh &>/dev/null; then
  echo "⚠️  gh コマンドが見つかりません。GitHub Release の作成はスキップします。"
  GH_AVAILABLE=false
else
  GH_AVAILABLE=true
fi

# 2. 未コミット変更の確認
if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "❌ 未コミットの変更があります。コミットまたはスタッシュ後にリリースしてください。"
  git status --short
  exit 1
fi

# 3. バージョンファイル同期確認（VERSION と plugin.json が存在する場合）
if [ -f "VERSION" ] && [ -f ".claude-plugin/plugin.json" ]; then
  V_VERSION=$(cat VERSION | tr -d '[:space:]')
  V_PLUGIN=$(grep '"version"' .claude-plugin/plugin.json | sed 's/.*"version": "\([^"]*\)".*/\1/')
  if [ "$V_VERSION" != "$V_PLUGIN" ]; then
    echo "❌ バージョン不一致: VERSION=$V_VERSION, plugin.json=$V_PLUGIN"
    echo "   修正: ./scripts/sync-version.sh sync"
    exit 1
  fi
fi
```

| チェック | 失敗時の動作 |
|----------|-------------|
| gh コマンド存在 | 警告のみ・続行（GitHub Release のみスキップ） |
| 未コミット変更 | **停止**（コミットまたはスタッシュを促す） |
| バージョンファイル同期 | **停止**（sync-version.sh sync を促す） |

---

### Step 1: 変更分析

以下を並列取得する。

```bash
# 前タグを取得
PREV_TAG=$(git describe --tags --abbrev=0 HEAD~1 2>/dev/null \
  || git tag --sort=-v:refname | head -1 2>/dev/null \
  || echo "")

# 構造化コミットログ（フォーマット: {hash}|{subject}|{author}|{date}）
if [ -n "$PREV_TAG" ]; then
  LOG=$(git log --format="%h|%s|%an|%ad" --date=short "${PREV_TAG}..HEAD")
else
  LOG=$(git log --format="%h|%s|%an|%ad" --date=short --all | head -20)
fi

# OWNER/REPO 取得（gh 優先 → git remote フォールバック）
if command -v gh &>/dev/null; then
  REPO_FULL=$(gh repo view --json nameWithOwner -q '.nameWithOwner' 2>/dev/null || echo "")
fi
if [ -z "${REPO_FULL:-}" ]; then
  REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
  REPO_FULL=$(echo "$REMOTE_URL" \
    | sed -E 's|https://github\.com/||; s|git@github\.com:||; s|\.git$||')
fi
```

#### Conventional Commits 分類

| Prefix | CHANGELOG カテゴリ |
|--------|-------------------|
| `feat:` / `feat(...):` | **Added** |
| `fix:` / `fix(...):` | **Fixed** |
| `docs:` / `perf:` / `refactor:` / `test:` / `chore:` | **Changed** |
| その他 / 分類不能 | **Changed** |

**BREAKING CHANGE 検出**: `feat!:` / `fix!:` 等の `!` 付きタイプ、または本文に `BREAKING CHANGE:` を含むコミット。

Conventional Commits を使っていないプロジェクトでは、Claude がコミットメッセージを意味的に判断して分類する。

#### 変更分析サマリ表示

```
📊 変更分析サマリ (vPREV → vNEW候補)
━━━━━━━━━━━━━━━━━━━━━━━━━
- feat     : N 件  → Added
- fix      : M 件  → Fixed
- other    : L 件  → Changed
- breaking : K 件  → Breaking Changes ⚠️
─────────────────────────────────
- contributors: X 名
- compare: https://github.com/{OWNER}/{REPO}/compare/{PREV_TAG}...HEAD
━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

### Step 2: SemVer 判定

Step 1 の分析結果に基づいてバージョンを提案する。

```bash
PREV_VERSION=${PREV_TAG#v}   # "v1.2.3" → "1.2.3"
MAJOR=$(echo "$PREV_VERSION" | cut -d. -f1)
MINOR=$(echo "$PREV_VERSION" | cut -d. -f2)
PATCH=$(echo "$PREV_VERSION" | cut -d. -f3)

if [ "${BREAKING_COUNT:-0}" -ge 1 ]; then
  SUGGESTED_VERSION="$((MAJOR+1)).0.0"   # major
elif [ "${FEAT_COUNT:-0}" -ge 1 ]; then
  SUGGESTED_VERSION="${MAJOR}.$((MINOR+1)).0"  # minor
else
  SUGGESTED_VERSION="${MAJOR}.${MINOR}.$((PATCH+1))"  # patch
fi
```

**表示例**: `📦 SemVer 判定: MINOR (1.2.3 → 1.3.0)  理由: feat: 3件, fix: 2件, breaking: 0件`

| 引数 | 動作 |
|------|------|
| `/release-har patch` | 確認なしで PATCH 採用 |
| `/release-har minor` | 確認なしで MINOR 採用 |
| `/release-har major` | 確認なしで MAJOR 採用 |
| 引数なし | 自動判定結果を表示し、ユーザーに確認 |

**0.x.y 初期開発段階**: MAJOR=0 の場合は SemVer 2.0.0 §4 に従い、breaking change でも minor バンプ (0.x+1.0) または major (1.0.0) をユーザーに選択させる。

---

### Step 3: diff 要約 & Release Notes 草稿生成

コミットメッセージだけでなく実際のコード差分を読み、Highlights と Before/After テーブルを生成する。

```bash
# 変更ファイルを確認（テスト・ロックファイルは低優先）
git diff --stat "${PREV_TAG}..HEAD"

# 重要ファイルの diff を読む（src/ 配下を優先）
git diff "${PREV_TAG}..HEAD" -- <重要ファイルパス> | head -100
```

Claude が生成するもの（最大3件）:
- **Highlights**: ユーザー視点での価値（1-3文）
- **Before / After テーブル**: 変更前後の状態

テンプレート詳細: [references/release-notes-template.md](references/release-notes-template.md)

---

### Step 4: dry-run プレビュー（デフォルト前段）

**本実行前に必ずプレビューを表示する**（`--dry-run` なし通常実行でも同様）。

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔍 リリースプレビュー: v{PREV} → v{NEW}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 タグ: vX.Y.Z
📁 更新ファイル: CHANGELOG.md, VERSION, package.json（存在する場合）

📄 CHANGELOG エントリ（全文）:
{CHANGELOG エントリ}

🧹 Documentation Cleanup:
  CHANGELOG: {正規化対象 N 件}（日付フォーマット、セクション見出し等）
  README: {更新対象 M 件}（バージョン参照、機能一覧等）

📝 GitHub Release Notes（全文）:
{4セクション構造の Release Notes}

🔗 Compare URL: {COMPARE_URL}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
この内容で実行しますか？ (yes / no / 修正指示)
```

| 回答 | 動作 |
|------|------|
| `yes` | Step 5 以降の本実行へ |
| `no` | 中止 |
| 修正指示 | Release Notes を修正して再プレビュー |

**`--dry-run` オプション時**: プレビュー後に終了（本実行なし）。

---

### Step 5: CHANGELOG 更新（存在する場合）

CHANGELOG.md があれば更新する。フォーマット詳細: [references/changelog-format.md](references/changelog-format.md)

```markdown
## [X.Y.Z] - YYYY-MM-DD

### 🎯 What's Changed for You

**{one-line バリュー要約}**

| Before | After |
|--------|-------|
| {旧状態} | {新状態} |

### Added
- **{Feature}**: {description}

### Fixed
- **{Fix}**: {description}
```

CHANGELOG_ja.md が存在する場合は同内容を日本語で更新する。

**CHANGELOG が存在しない場合はスキップ。**

---

### Step 5.5: Documentation Cleanup（既存ドキュメント整備）

リリースのタイミングで、既存ドキュメントの品質も整える。**新規エントリの追加だけでなく、過去の汚れも修正する。**

#### CHANGELOG 既存エントリの正規化

過去エントリが Keep a Changelog 1.1.0 に準拠していない場合、正規化する。

| チェック項目 | 修正例 |
|-------------|--------|
| 日付フォーマット | `2026/02/23` → `2026-02-23` (ISO 8601) |
| セクション見出し | `### New Features` → `### Added` |
| 空セクション | 内容のない見出しを削除 |
| リンク切れ | Compare URL のタグ名修正 |
| マークダウン構文 | テーブル崩れ、リスト記法の統一 |

CHANGELOG_ja.md が存在する場合、同等の整備を実施する。

#### README の更新

| チェック項目 | 修正内容 |
|-------------|---------|
| バージョン番号 | バッジ、インストール例、参照を新バージョンに更新 |
| 機能一覧 | 実態と乖離している記述を修正 |
| コマンド/API 例 | 廃止・変更されたものを更新 |
| リンク切れ | 存在しないファイルへのリンクを修正 |

**判断基準**: 明らかに古い・壊れている箇所のみ修正する。意図的なスタイルの違いは尊重する。README が存在しない場合はスキップ。

---

### Step 6: バージョンファイル更新

プロジェクトに応じてバージョンを更新する。

| ファイル | 更新方法 |
|---------|---------|
| `VERSION` | ファイル内容を直接書き換え |
| `package.json` | `"version": "X.Y.Z"` を更新 |
| `pyproject.toml` | `version = "X.Y.Z"` を更新 |
| `Cargo.toml` | `version = "X.Y.Z"` を更新 |
| `.claude-plugin/plugin.json` | `./scripts/sync-version.sh sync` を実行 |

**該当ファイルが存在しない場合はスキップ。**

Node.js プロジェクト: `npm version patch --no-git-tag-version` も利用可。

---

### Step 7: コミット & タグ

```bash
# 変更対象ファイルのみ明示的に追加（git add -A は使用しない）
git add CHANGELOG.md README.md VERSION package.json  # 実際に変更したファイルのみ

# コミット（変更がある場合のみ）
git commit -m "chore: release vX.Y.Z"

# タグ作成
git tag -a vX.Y.Z -m "Release vX.Y.Z"
```

---

### Step 8: Push

```bash
git push origin $(git branch --show-current)
git push origin vX.Y.Z
```

---

### Step 9: GitHub Release（オプション）

ユーザー確認後に GitHub Release を作成する。Release Notes は英語必須。

```bash
gh release create vX.Y.Z \
  --title "vX.Y.Z - {release title}" \
  --notes "$(cat <<'EOF'
## What's Changed

**{one-line バリュー要約}**

### Before / After

| Before | After |
|--------|-------|
| {旧状態} | {新状態} |

---

## Highlights

- **{Feature}**: {description}

## Notable Changes

### Added

- **{feature}**: {description}

### Fixed

- **{fix}**: {description}

## Full Changelog

**Full Changelog**: ${COMPARE_URL}

---

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

フォーマットルール: [.claude/rules/github-release.md](../../.claude/rules/github-release.md)
テンプレート詳細: [references/release-notes-template.md](references/release-notes-template.md)

**必須事項**:
- Release Notes は英語
- Before/After テーブルは省略不可
- `Generated with [Claude Code](https://claude.com/claude-code)` フッターは省略不可
- Breaking Changes がない場合はそのセクションを省略
- Highlights は最大3件

### Step 10: X (Twitter) 告知文生成（`--announce` 指定時のみ）

`/release-har --announce` で実行した場合、GitHub Release 作成後に X 向け告知文を自動生成する。

#### 生成ロジック

Step 3（diff 要約）で生成した Highlights のうち最も重要な1〜2点を1行ずつに圧縮し、280文字以内の告知文を作成する。

#### フォーマット

```
🚀 v{VERSION} released!

{Highlights から抽出した1行要約（日本語または英語、プロジェクトの言語に合わせる）}
{2行目（任意）}

{GitHub Release URL}
```

**例**:
```
🚀 v1.3.0 released!

Pre-flight checks + Claude diff summarization で配信品質が向上。
SemVer 自動判定と dry-run プレビューで事故を防止。

https://github.com/OWNER/REPO/releases/tag/v1.3.0
```

#### 制約

| 制約 | 値 |
|------|-----|
| 最大文字数 | 280文字（X の制限） |
| 絵文字 | 最小限（🚀 のみ推奨） |
| リンク | 必須（GitHub Release URL） |
| 言語 | プロジェクトの主要言語に合わせる |

生成後、そのままコピーできる形式でユーザーに提示する。投稿は Claude では行わない（手動コピー＆ペースト）。

---

## Options

| Option | Description |
|--------|-------------|
| `patch` | パッチバージョンを自動インクリメント |
| `minor` | マイナーバージョンを自動インクリメント |
| `major` | メジャーバージョンを自動インクリメント |
| `--dry-run` | プレビューのみ（ファイル変更・コミット・タグ・push なし） |
| `--announce` | リリース後に X（旧 Twitter）向け告知文を生成 |

---

## Related Skills

- `x-release-harness` - Harness plugin 専用リリース（ローカルのみ）
- `verify` - リリース前の検証
