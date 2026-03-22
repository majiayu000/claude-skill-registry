---
name: close-resolved-issues
description: 対応済みの GitHub Issue を検出してクローズする。コードベースと PR を確認し、既に実装済み・マージ済みの Issue を自動的に閉じる。「対応済み Issue を閉じて」「解決済みの Issue をクローズして」のようなリクエストで使う。
context: fork
agent: general-purpose
allowed-tools: Bash(gh issue list:*), Bash(gh pr list:*), Bash(gh issue close:*), Bash(git log:*), Read, Glob, Grep
---

# Close Resolved Issues Skill

Open な Issue を一覧取得し、それぞれの Issue が既に対応済みかを判定してクローズする。

## 前提条件

- `gh` CLI が認証済みであること

## 手順

### 1. Open Issue の取得

```bash
gh issue list --state open --json number,title,labels,milestone,body --limit 100
```

### 2. 対応済み判定

各 Issue について以下を確認する:

1. **コードベースの確認**: Issue の要件に対応するコードが既に実装されているかを調査する
   - 関連するファイル、関数、テストの存在を確認
   - `git log --oneline --all --grep="#<issue-number>"` で関連コミットを検索
2. **PR の確認**: Issue に紐づく PR がマージ済みかを確認する
   ```bash
   gh pr list --state merged --search "close #<issue-number> OR closes #<issue-number> OR fix #<issue-number> OR fixes #<issue-number>" --json number,title
   ```
3. **Issue 内容との照合**: コードベースの現状が Issue の要件を満たしているかを総合的に判断する

### 3. クローズ処理

対応済みと判定した Issue は、理由を添えてクローズする。

```bash
gh issue close <issue-number> --comment "$(cat <<'EOF'
棚卸によりクローズします。

**対応済みの根拠:**
- <対応済みと判断した具体的な根拠を記載>

🤖 *Triaged by Claude Code*
EOF
)"
```

### 4. 結果の報告

クローズした Issue の一覧を以下の形式で報告する:

| # | タイトル | 理由 |
|---|---------|------|
| #XX | <タイトル> | <クローズ理由の要約> |

対象がない場合は「対応済みの Issue はありませんでした」と報告する。

## 注意事項

- Renovate の Dependency Dashboard（#23 など）はクローズ対象外とする
- 判定に迷う場合はクローズせず、その旨を報告するに留める
- `Close: Duplicate` や `Close: WontFix` ラベルが付いた Issue もクローズ対象とする
- Issue のクローズは慎重に行うこと
