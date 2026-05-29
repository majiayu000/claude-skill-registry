---
name: update-submodule-changelog
description: |
  サブモジュール（protocols/*, gcloud/*）更新後に docs/changelogs.md を更新する。
  「サブモジュール更新」「changelog更新」「プロトコル変更まとめ」などのキーワードで自動適用。
  git submodule update 後や、依存関係の変更ドキュメント化に使用。
argument-hint: [対象サブモジュール名（省略時は全て）]
allowed-tools: Read, Write, Bash(git:*), Grep, Glob, Task
---

# Submodule Changelog Update Skill

サブモジュール更新後に `docs/changelogs.md` を更新するためのワークフロー。

## 概要

このスキルは以下を行う：
1. サブモジュールの変更を検出
2. 各サブモジュールの CHANGELOG.md や git log から変更内容を収集
3. `docs/changelogs.md` を適切なフォーマットで更新

**重要**: このchangelogは**各プロジェクトの最新リリース情報**を記録するもの。サブモジュールの実際のチェックアウト状態（`git submodule status`）ではなく、各リポジトリの最新タグ・リリースを調査して記載する。

## ワークフロー

### Step 1: サブモジュール変更の検出

```bash
# 変更されたサブモジュールを確認
git status

# 各サブモジュールの最新コミットを確認
git submodule status
```

### Step 2: 変更内容の収集

各サブモジュールについて以下を調査：

```bash
# サブモジュールディレクトリに移動して最近のコミットを確認
cd <submodule-path>
git log --oneline -10

# CHANGELOG.md があれば読む
cat CHANGELOG.md | head -100
```

**調査対象ディレクトリ**:
- `protocols/` - プロトコルサブモジュール（A2A, A2UI, ACP, ADP, AG-UI, AgentSkills, AP2, MCP, MCP-UI, OpenResponses, UCP, x402）
- `gcloud/` - Google Cloud サブモジュール（adk-python, adk-go, adk-js, agent-starter-pack, cloud-run-mcp, gcloud-mcp, gke-mcp, google-analytics-mcp, mcp, mcp-security, genai-toolbox）

### Step 3: changelogs.md の更新

`docs/changelogs.md` を以下の構造で更新：

```markdown
# プロトコル変更ログ

最終更新: YYYY-MM-DD

---

## プロトコル (Protocols)

### <プロトコル名>

**現行バージョン**: <version>

#### 主要な変更点
- **機能名**: 説明

#### 破壊的変更（あれば）
| 変更 | 影響 |
|------|------|
| 変更内容 | 影響範囲 |

#### 参考リンク
- [リンク名](URL)

---

## Google Cloud / ADK

### <コンポーネント名>

**現行バージョン**: <version>

#### 主要な変更点
- **機能名**: 説明

---

## 注目ポイント

### 破壊的変更一覧
| 対象 | 変更内容 | 対応優先度 |
|------|---------|-----------|

### 新規追加プロトコル
1. **名前** - 説明 (管理元)

### セキュリティ更新
- **対象**: 説明
```

## フォーマット規約

### バージョン表記
- semver: `v1.2.3`
- 日付ベース: `YYYY-MM-DD`
- 初期リリース: `初期リリース`
- 最新追従: `latest`

### 変更点の書き方
- **太字**で機能名を記載
- コロン `:` の後に説明
- コード参照は `` ` `` で囲む
- PR/Issue 番号は `(#123)` 形式

### 破壊的変更
- 必ず「破壊的変更」セクションに記載
- 影響範囲を明記
- 移行方法があれば記載

## 調査のヒント

### 最新リリースの確認方法
```bash
# リポジトリの最新タグを確認（チェックアウト状態とは異なる可能性あり）
cd <submodule-path>
git fetch --tags
git tag -l --sort=-v:refname | head -5

# CHANGELOG.md から最新リリースを読む
cat CHANGELOG.md | head -100
```

**注意**: `git submodule status` はチェックアウト状態を表示する。最新リリースを確認するには `git tag` や CHANGELOG.md を見ること。

### CHANGELOG.md がない場合
```bash
# 最近のコミットから変更を推測
git log --oneline -20
git log --pretty=format:"%s" -10

# タグから最新バージョンを確認
git describe --tags --abbrev=0
git tag -l | tail -5
```

### 複数エージェントで並列調査
Task tool を使って Explore エージェントを並列起動し、複数のサブモジュールを同時に調査すると効率的。

## チェックリスト

更新完了前に確認：

- [ ] 最終更新日が今日の日付になっている
- [ ] **バージョンが各リポジトリの最新リリースを反映している**（チェックアウト状態ではない）
- [ ] 新規追加プロトコルが「注目ポイント」に記載されている
- [ ] 破壊的変更が一覧表にまとめられている
- [ ] 各セクションの参考リンクが有効
- [ ] 日本語が自然である
- [ ] 古い情報が削除されている（重要な後方互換情報は除く）

## コミットしない

変更の確認はユーザーに任せる。コミットはユーザーの指示を待つ。
