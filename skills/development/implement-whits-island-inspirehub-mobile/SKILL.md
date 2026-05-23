---
name: implement
description: Issueコメントの文脈（Plan等）を読み、ブランチ作成→実装→PR作成まで実行する
user-invocable: true
argument-hint: "(Issueの内容に従って実装を進める)"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebSearch, WebFetch
---

# /implement — 実装スキル

Issueの文脈（過去のコメント・Plan等）を読み取り、実装からPR作成までを一気通貫で実行する。

## 前提

- **Planは事前にIssueコメントで合意済み**であること
- Issueコメントに方針・Plan等がない場合は、自分で調査して最善の実装を行う

## フロー

### 1. コンテキスト把握

- Issueの本文と全コメントを読む
- Plan（方針コメント）があればそれに従う
- 設計ドキュメント（`docs/design/`）やAPI仕様も必要に応じて参照

### 2. ブランチ作成

- mainから `claude/issue-{number}` ブランチを作成
- やり直しの場合はブランチを削除して同名で再作成

### 3. 実装

- CLAUDE.mdおよび `.claude/rules/` のルールに従って実装
- コミットメッセージはConventional Commits準拠
- **注意**: コミットメッセージには `Closes #` を含めない（PR本文でのみ使用）

### 4. shared層テスト（条件付き）

- `git diff main...HEAD --name-only` で `shared/` 配下の変更をチェック
- **shared層に変更がある場合のみ** `./gradlew :shared:testDebugUnitTest` を実行
- 変更がない場合はテストをスキップ（iOS/Android UIのみの変更の場合）
- テストが通ることを確認してからPR作成に進む

### 5. PR作成

**必ず `gh pr create` コマンドでPRを作成すること**

```bash
gh pr create \
  --title "feat: タイトル" \
  --body "$(cat <<'EOF'
Closes #{issue番号}

## 変更内容
- ...

## テスト
✅ ./gradlew :shared:testDebugUnitTest - テスト結果

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

- タイトルは Conventional Commits 形式
- 本文に `Closes #{issue番号}` を必ず含める
- 変更内容のSummaryを記載
- テスト結果を記載

### 6. 完了

PR作成後、タスク完了。

- Xcode Cloud は PR作成を検知して自動的に Dev版ビルド＆TestFlight配信を開始
- PR番号で自動的にビルドが識別される
- タグpushは不要（シンプル化）

## やり直し

ユーザーが `@claude やり直して` とコメントした場合:

1. `claude/issue-{number}` ブランチを削除（remote含む）
2. 同名ブランチをmainから再作成
3. 最初から実装し直す

## 注意事項

- **iOSビルドは実行しない**（GitHub Actions上のLinuxで動作するため）
- iOSの動作確認はXcode Cloud → TestFlight配信後に人間が行う
- PR作成後、Xcode Cloudが自動的にビルド＆TestFlight配信を開始
