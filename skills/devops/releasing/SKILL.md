---
name: releasing
description: BoxLogのリリース作業をガイド。バージョン決定、重複チェック、リリースノート作成、タグ付けまでの全プロセスを支援。
---

# Releasing Skill

BoxLogプロジェクトのリリース作業を安全かつ確実に実行するためのスキルです。

## このスキルを使用するタイミング

以下のキーワードが含まれる場合に自動的に起動：

- 「リリース」「release」
- 「バージョンアップ」「version」
- 「タグを作成」「タグ付け」
- 「v0.X.0をリリース」

## リリースワークフロー概要

```
Phase 0: 準備（PRマージ前）
  ├── 0.1 バージョン番号決定・重複チェック ← 最重要
  ├── 0.2 コード品質確認（lint, typecheck, test, build）
  ├── 0.3 package.json更新
  └── 0.4 リリースノート作成

Phase 1: PRマージ
  ├── 1.1 PR作成
  ├── 1.2 CI/CD確認
  └── 1.3 マージ

Phase 2: タグ作成
  ├── 2.1 mainブランチ更新
  ├── 2.2 Gitタグ作成・プッシュ
  └── 2.3 GitHub Release確認

Phase 3: デプロイ確認
Phase 4: リリース後作業
```

## 必須チェック項目

### Phase 0.1: バージョン重複チェック（スキップ厳禁）

```bash
# 1. 既存リリースを確認
gh release list

# 2. 重複チェック
VERSION="0.X.0"  # リリースするバージョン
gh release view v${VERSION} 2>/dev/null && echo "❌ Already exists!" || echo "✅ OK"
```

**重複が見つかった場合**: 必ず「v0.X.0ではなくv0.Y.0じゃないですか？」と確認する

### Phase 0.2: コード品質

```bash
npm run lint && npm run typecheck && npm run test:run && npm run build
```

### Phase 0.3: バージョン更新

```bash
# PATCH: バグ修正 (0.3.0 → 0.3.1)
npm version patch --no-git-tag-version

# MINOR: 新機能 (0.3.0 → 0.4.0)
npm version minor --no-git-tag-version

# MAJOR: 破壊的変更 (0.3.0 → 1.0.0)
npm version major --no-git-tag-version
```

### Phase 0.4: リリースノート作成（詳細化必須）

#### Step 1: PRとコミット情報を取得

```bash
# 前回リリース以降の全PRを取得
gh pr list --state merged --base main --limit 100 --json number,title,mergedAt

# 各PRのコミット詳細を取得（重要：PRタイトルだけでは不十分）
for pr in <PR番号リスト>; do
  echo "=== PR #$pr ==="
  gh pr view $pr --json title,body --jq '.title + "\n" + .body'
  echo "--- Commits ---"
  gh pr view $pr --json commits --jq '.commits[].messageHeadline'
done
```

#### Step 2: 詳細なリリースノートを作成

**粒度の基準**: 第三者が見ても「何が変わったか」がわかるレベル

**❌ 悪い例（抽象的）**:

```markdown
- タグ機能リファクタリング
- パフォーマンス改善
```

**✅ 良い例（具体的）**:

```markdown
#### タグ機能の大幅強化 ([#910])

**データモデル変更**

- タグの親子階層モデルへ移行（`tag_groups` テーブル → `parent_id` カラム）
- 子タグの昇格処理を含むタグマージ機能

**UI/UX改善**

- タグ作成モーダルをポータルで実装（モーダル内でも正常動作）
- カレンダーサイドバーでのタグドラッグ&ドロップ並び替え
- 未タグ付けフィルターにアイコンと件数表示

**楽観的更新**

- タグ作成・編集・削除・マージ・並び替えに楽観的更新を実装
```

#### Step 3: 必須セクション

1. **新機能 (Added)**: 機能名 + 具体的な実装内容
2. **変更 (Changed)**: 何がどう変わったか + 影響範囲
3. **バグ修正 (Fixed)**: 問題の原因 + 修正内容
4. **パフォーマンス (Performance)**: 最適化内容 + 改善値（あれば）
5. **破壊的変更 (Breaking Changes)**: DB変更、削除されたAPI/コンポーネント

#### チェックリスト

- [ ] 各PRのコミットを確認した
- [ ] 抽象的な記述を具体化した
- [ ] データモデル変更を明記した
- [ ] 削除されたコンポーネント/機能をリストした
- [ ] Full Changelogリンクがある

## 詳細ドキュメント

完全なチェックリスト: `docs/releases/RELEASE_CHECKLIST.md`

## よくある失敗

| 失敗                   | 対策                                           |
| ---------------------- | ---------------------------------------------- |
| バージョン重複         | Phase 0.1で必ず `gh release view`              |
| package.json更新忘れ   | Phase 0.3でPRマージ前に更新                    |
| Full Changelog抜け     | template.mdをコピーして使用                    |
| 一部PRのみ記載         | `gh pr list --state merged` で全件取得         |
| リリースノートが抽象的 | 各PRのコミットを取得して具体的な変更内容を記載 |
| 破壊的変更の記載漏れ   | DB変更、削除コンポーネントを明記               |

## スクリプト

### バージョン重複チェック

```bash
.claude/skills/releasing/scripts/check-version.sh 0.X.0
```

### マージ済みPR取得

```bash
.claude/skills/releasing/scripts/get-merged-prs.sh
```
