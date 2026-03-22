---
name: release
description: 'Execute the release workflow when the user asks `release` or `/release`: sync develop, update version/changelog, create `chore(release)` commit, collect closing issues, create develop->main release PR, and verify release/publish artifacts.'
---

# Release Workflow

LLM主導でバージョン更新とリリースコミットを作成し、ワークフローでタグ・Release・配布を完了する。

## Preflight

- `gh auth status` が成功すること
- `git status --short` が空であること
- `origin/develop` を最新化できること

## フロー

```text
release (/release) 実行
    ↓
① origin/develop を pull してローカルを最新化
    ↓
② バージョン更新（Cargo.toml, CHANGELOG.md）
    ↓
③ chore(release): vX.Y.Z コミット作成
    ↓
④ Closing Issue を収集
    ↓
⑤ develop → main マージ（PR本文に Closing Issues 記載）
    ↓
⑥ release.yml がタグ作成 → GitHub Release作成
    ↓
⑦ publish.yml がバイナリビルド → Release にアタッチ
```

## 手順

### 0. ローカルを最新化（必須）

```bash
git fetch origin
git pull origin develop
```

### 1. バージョン更新

```toml
[workspace.package]
version = "X.Y.Z"
```

### 2. CHANGELOG.md 更新

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- 新機能の説明

### Fixed
- バグ修正の説明
```

### 3. リリースコミット作成

```bash
git add Cargo.toml Cargo.lock CHANGELOG.md
git commit -m "chore(release): vX.Y.Z"
git push origin develop
```

### 4. Closing Issue の収集

1. 前回タグ〜HEADのコミットからPR番号抽出

```bash
LAST_TAG=$(git describe --tags --abbrev=0)
PR_NUMBERS=$(git log ${LAST_TAG}..HEAD --oneline \
  | grep -oE '(#[0-9]+)|\bMerge pull request #[0-9]+' \
  | grep -oE '[0-9]+' | sort -u)
```

1. 各PR本文から closing keyword 抽出

```bash
CLOSING_ISSUES=""
for pr in $PR_NUMBERS; do
  BODY=$(gh pr view "$pr" --json body -q '.body' 2>/dev/null || true)
  ISSUES=$(echo "$BODY" \
    | grep -oiE '(close[sd]?|fix(e[sd])?|resolve[sd]?)\s+#[0-9]+' \
    | grep -oE '[0-9]+' || true)
  CLOSING_ISSUES="$CLOSING_ISSUES $ISSUES"
done
CLOSING_ISSUES=$(echo "$CLOSING_ISSUES" | tr ' ' '\n' | sort -u | grep -v '^$')
```

1. PR番号を除外してIssueのみ残す

```bash
REAL_ISSUES=""
for num in $CLOSING_ISSUES; do
  IS_PR=$(gh api "repos/{owner}/{repo}/issues/$num" \
    --jq 'has("pull_request") and .pull_request != null' 2>/dev/null || echo "false")
  if [ "$IS_PR" = "false" ]; then
    REAL_ISSUES="$REAL_ISSUES $num"
  fi
done
```

1. PR本文用に出力

```bash
for num in $REAL_ISSUES; do
  echo "Closes #$num"
done
```

### 5. main へマージ

```bash
# 推奨: 既存スクリプト経由
./scripts/prepare-release.sh

# または prepare-release workflow を直接起動
gh workflow run prepare-release.yml

# 手動PR作成の場合
gh pr create --base main --head develop \
  --title "chore(release): vX.Y.Z"
```

### 6. 配布確認

- `gh release view vX.Y.Z`
- `gh run list --workflow=publish.yml --limit 3`
- [GitHub Releases](https://github.com/akiojin/llmlb/releases)

## 注意

- バージョンは [Semantic Versioning](https://semver.org/) に従う
- `chore(release):` プレフィックスは必須（release.yml のトリガー条件）
- `gh auth login` 済みであること
