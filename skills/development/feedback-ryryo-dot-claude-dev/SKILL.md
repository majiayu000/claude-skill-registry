---
name: dev:feedback
description: |
  実装完了後、学んだことをDESIGN.mdに蓄積。スキル/ルールの自己改善も提案。
  PR作成・Worktreeクリーンアップまで実行。ストーリー駆動開発の終点。
  「フィードバック」「/dev:feedback」で起動。

  Trigger:
  フィードバック, 学習事項蓄積, /dev:feedback, feedback, design update
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - AskUserQuestion
---

# フィードバック → 仕様書蓄積（dev:feedback）

## 概要

実装完了後、学んだことをシステム仕様書（DESIGN.md）に蓄積。
繰り返しパターンはスキル/ルール化を提案し、meta-skill-creatorと連携。

## 入力

- feature-slug, story-slug
- 実装済みコード（git diff）
- output/フォルダのレポート（あれば）

## 出力

| ファイル                                       | 必須   | 内容                                                                          |
| ---------------------------------------------- | ------ | ----------------------------------------------------------------------------- |
| `docs/features/{feature-slug}/DESIGN.md`       | ✅     | 機能固有の設計判断・学習事項                                                  |
| `docs/features/DESIGN.md`                      | ✅     | **プロジェクト全体に影響する設計判断**                                        |
| `docs/features/{feature-slug}/IMPROVEMENTS.md` | 該当時 | 改善提案・スキル/ルール化候補・リファクタリング案（後続エージェント用ガイド） |

---

## ワークフロー

```
Phase 1: 変更内容の収集
    → agents/analyze-changes.md [sonnet]
    → 変更ファイル・学習事項・改善/リファクタリング候補の素材を抽出
        ↓
Phase 2a: 機能DESIGN.md更新
    → agents/update-design.md [sonnet]
    → docs/features/{feature-slug}/DESIGN.md に追記
        ↓
Phase 2b: 総合DESIGN.md更新 [sonnet]
    → docs/features/DESIGN.md に重要な設計判断を反映
    → プロジェクト全体に影響する学びを記録
        ↓
Phase 2c: 総合DESIGNの整理（SIMPLIFY）
    → code-simplifierエージェント [opus]
    → 明瞭性・一貫性・保守性の向上
        ↓
Phase 3: 改善提案・リファクタリング計画のドキュメント化
    → agents/propose-improvement.md [opus]
    → スキル化/ルール化候補とリファクタリング候補を1つのMDに整理
    → 実作業は行わず、後続エージェントが参照できるガイドのみ生成
        ↓
Phase 4: テスト資産の整理（TDDタスクがあった場合）
    → 長期的価値があるテスト → 保持・維持
    → 一時的価値のみ → 簡素化または削除
    → ユーザー確認後に整理を実行
        ↓
Phase 5: PR作成・Worktreeクリーンアップ
    → PR作成（gh pr create）
    → マージ後、Worktree削除
        ↓
Phase 6: 進行中ストーリー一覧の更新
    → in-progress-stories.tmp再生成
    → 完了したストーリーを一覧から削除
```

---

## Phase 1: 変更内容の収集

```bash
git diff --stat HEAD~5
git log --oneline -10
```

```javascript
Task({
  description: "変更分析",
  prompt: `git diffから以下を抽出してください:

1. 変更されたファイル一覧
2. 追加された機能
3. 設計判断（なぜこの構造にしたか）
4. 技術的な発見
5. 注意点・ハマりどころ
6. 将来の改善・リファクタリング候補になりそうなポイント
   - 重複している実装や似たような処理
   - 一時的なワークアラウンド
   - 複雑で簡素化の余地がある箇所
7. 共通パターン・抽象化できそうな構造

出力形式: JSON`,
  subagent_type: "general-purpose",
  model: "sonnet",
});
```

→ 詳細: [agents/analyze-changes.md](.claude/skills/dev/feedback/agents/analyze-changes.md)

---

## Phase 2a: 機能DESIGN.md更新

既存のDESIGN.mdがあれば追記、なければ新規作成。

```javascript
Task({
  description: "機能DESIGN.md更新",
  prompt: `docs/features/{feature-slug}/DESIGN.md を更新してください。

追記内容:
- 設計判断（なぜこの構造にしたか）
- 技術的な発見
- 注意点・ハマりどころ

フォーマット: references/update-format.md を参照`,
  subagent_type: "general-purpose",
  model: "sonnet",
});
```

→ 詳細: [agents/update-design.md](.claude/skills/dev/feedback/agents/update-design.md)
→ テンプレートや具体的な記述フォーマットは [references/design-template.md](.claude/skills/dev/feedback/references/design-template.md) を参照

---

## Phase 2b: 総合DESIGN.md更新 ★必須ステップ★

> ⚠️ **このステップをスキップしない**: 機能DESIGN.mdの更新後、必ず総合DESIGN.mdも更新すること。

プロジェクト全体に影響する重要な設計判断を `docs/features/DESIGN.md` に反映する。

### 更新判断基準

| 項目                     | 総合DESIGN.mdに記載 | 機能DESIGN.mdのみ |
| ------------------------ | ------------------- | ----------------- |
| アーキテクチャ決定       | ✅                  | -                 |
| 技術スタック選定         | ✅                  | -                 |
| 共通パターン発見         | ✅                  | -                 |
| 機能固有の実装詳細       | -                   | ✅                |
| 一時的なワークアラウンド | -                   | ✅                |

### 更新手順

1. **Phase 2aで追記した内容を確認**
2. **以下に該当するものを抽出**:
   - 他機能にも適用できる設計判断
   - プロジェクト全体の方針に関わる決定
   - 技術スタックやライブラリの選定理由
3. **`docs/features/DESIGN.md` に追記**

```javascript
// Phase 2aの結果を基に、総合DESIGN.mdを更新
Edit({
  file_path: "docs/features/DESIGN.md",
  // 「## 設計判断」または「## 更新履歴」セクションに追記
});
```

※ 総合DESIGN.md側の具体的なセクション構成や見出しレベルも、
必要に応じて [references/design-template.md](.claude/skills/dev/feedback/references/design-template.md) をガイドとして利用する

---

## Phase 2c: 総合DESIGNの整理（SIMPLIFY）

Phase 2b で更新した `docs/features/DESIGN.md` に対して、
**記述の明瞭性・一貫性・保守性** を高めるための整理を行う。
コードではなく、あくまで「総合DESIGN.mdの内容」を対象とする。

```javascript
Task({
  description: "総合DESIGN.mdの整理",
  prompt: `docs/features/DESIGN.md を読み込み、内容を整理してください。

対象: docs/features/DESIGN.md 全体（特に今回追加・更新した箇所）

観点:
- 明瞭性: 用語・文章がわかりやすく、一貫した表現になっているか
- 一貫性: セクション構成や見出しレベル、フォーマットが統一されているか
- 保守性: 将来の変更時に迷わないような構造・粒度になっているか

注意:
- 設計判断そのものの意味や意図は変えない
- 情報を削る場合は、重複や冗長な表現に限る
- 必要であれば「用語の定義」「参照リンク」などの補足を追加してよい`,
  subagent_type: "code-simplifier",
  model: "sonnet",
});
```

### 整理対象

| カテゴリ     | 確認項目                                               |
| ------------ | ------------------------------------------------------ |
| 用語・表現   | 同じ概念に同じ用語を使えているか                       |
| セクション   | 見出し構造が論理的で、ナビゲーションしやすいか         |
| 冗長さ       | 不要な重複や回りくどい表現が残っていないか             |
| 将来の追記性 | 後から設計判断を追加しやすいフォーマットになっているか |

---

## Phase 3: 改善提案・リファクタリング計画のドキュメント化

Phase 1〜2cで得た情報（DESIGN更新内容・コード整理の結果・暗黙のパターン）をもとに、
**改善提案・リファクタリング候補・スキル/ルール化候補**を1つのMarkdownドキュメントにまとめる。

このPhaseでは **実際のスキル作成/ルール追加/リファクタリング作業は行わず**、
後続エージェントがこのドキュメントだけを見て作業できるようにする。

```javascript
Task({
  description: "改善・リファクタリング提案ドキュメントの作成",
  prompt: `以下の情報を入力として、改善提案とリファクタリング計画をMarkdownでまとめてください。

入力:
- Phase 1（変更分析）のJSON出力
- docs/features/{feature-slug}/DESIGN.md の更新内容
- docs/features/DESIGN.md に追加された設計判断
- コード整理（SIMPLIFY）の結果、気づいた改善ポイント

出力先:
- docs/features/{feature-slug}/IMPROVEMENTS.md

Markdownの構成:

# 改善・リファクタリング提案 ({feature-slug}, {story-slug})

## 1. スキル化候補
- {パターン名}
  - 背景 / 文脈
  - 適用条件
  - 期待される効果
  - 想定されるSKILL.mdの場所（例: .claude/skills/...）

## 2. ルール化候補
- {ルール名}
  - 背景 / 文脈
  - 適用条件
  - 期待される効果
  - 想定されるRULE.mdの場所（例: .cursor/rules/...）

## 3. リファクタリング候補
- {対象ファイルと概要}
  - 目的（なぜ変えるのか）
  - 変更の方針（どのように変えるか）
  - 想定される影響範囲
  - 実施時のチェックポイント（テストや確認観点）

## 4. メモ / 補足
- その他、後続エージェントが知っておくべき前提・注意点

注意:
- ここではコードや設定ファイルを直接変更しない
- 実作業は別エージェント（例: dev:developing や meta-skill-creator）に委ねる前提で、
  「目的・背景・手順・影響範囲」がわかるレベルまで具体的に書く
- 基本的には Phase 1 で抽出した情報を前提とし、git diff や履歴のフルスキャンは繰り返さない
- ただし、改善案やリファクタリング案を具体化するために必要な箇所があれば、その部分に限ってコードや履歴を追加で参照してよい
- 実装コード自体の詳細な再分析ではなく、「どこをどう改善するか」を説明できるレベルまで情報を補うことに留める`,
  subagent_type: "general-purpose",
  model: "opus",
});
```

→ 詳細: [agents/propose-improvement.md](.claude/skills/dev/feedback/agents/propose-improvement.md)
→ パターン基準: [references/improvement-patterns.md](.claude/skills/dev/feedback/references/improvement-patterns.md)

---

## フィードバック記録

meta-skill-creatorの機構を活用:

| ファイル    | 用途              | 更新タイミング |
| ----------- | ----------------- | -------------- |
| LOGS.md     | 実行記録          | 毎回実行後     |
| EVALS.json  | メトリクス        | 毎回実行後     |
| patterns.md | 成功/失敗パターン | パターン発見時 |

→ 詳細: [references/feedback-loop.md](.claude/skills/dev/feedback/references/feedback-loop.md)

---

## Phase 4: テスト資産の整理（TDDタスクがあった場合）

実装完了後、テストコードの扱いを決定する。

### 5.1 テスト資産の評価

```javascript
Task({
  description: "テスト資産評価",
  prompt: `TDDで作成されたテストを評価してください。

各テストについて以下を判断:

| 判断基準 | アクション |
|---------|-----------|
| **長期的な価値がある** | テスト資産として保持・維持 |
| **一時的な価値のみ** | テストを簡素化、または削除候補 |

評価ポイント:
- 回帰テストとして価値があるか
- メンテナンスコストに見合うか
- ドキュメントとしての価値があるか

出力形式:
- 保持推奨: [テスト名一覧]
- 簡素化/削除候補: [テスト名一覧と理由]`,
  subagent_type: "general-purpose",
  model: "haiku",
});
```

### 5.2 ユーザー確認

```javascript
AskUserQuestion({
  questions: [
    {
      question: "テスト資産を整理しますか？",
      header: "テスト整理",
      options: [
        { label: "整理する", description: "候補のテストを簡素化/削除" },
        { label: "すべて保持", description: "テストは変更しない" },
        { label: "後で判断", description: "今回はスキップ" },
      ],
      multiSelect: false,
    },
  ],
});
```

**考え方**:

- すべてのテストを残す必要はない
- 開発プロセスでの役割を終えたテストは積極的に整理する
- メンテナンスコストとのバランスを考慮

---

## Phase 5: PR作成・Worktreeクリーンアップ

### 6.1 PR作成確認

```javascript
AskUserQuestion({
  questions: [
    {
      question: "PRを作成しますか？",
      header: "PR作成",
      options: [
        { label: "PRを作成", description: "gh pr create でPRを作成" },
        { label: "後で手動で作成", description: "今回はスキップ" },
      ],
      multiSelect: false,
    },
  ],
});
```

### 6.2 PR作成（選択時）

```bash
# 変更をプッシュ
git push -u origin HEAD

# PRを作成
gh pr create --title "{story-slug}" --body "$(cat <<'EOF'
## Summary
- {実装内容のサマリー}

## Changes
- {変更ファイル一覧}

## Test plan
- [ ] テストが通ること
- [ ] 動作確認

🤖 Generated with Claude Code
EOF
)"
```

### 6.3 Worktreeクリーンアップ

PRがマージされた後のクリーンアップ手順を案内:

```markdown
📋 **PR作成完了**

PRがマージされたら、以下のコマンドでWorktreeを削除してください:

\`\`\`bash

# メインブランチに戻る

cd /path/to/main/repo

# Worktreeを削除

git worktree remove ../{branch-name}

# ブランチを削除（オプション）

git branch -d {branch-name}
\`\`\`
```

**自動クリーンアップ（オプション）**:

```javascript
AskUserQuestion({
  questions: [
    {
      question: "PRマージ後にWorktreeを自動削除しますか？",
      header: "クリーンアップ",
      options: [
        {
          label: "自動削除",
          description: "マージ確認後にWorktreeとブランチを削除",
        },
        { label: "手動で削除", description: "削除コマンドを表示のみ" },
      ],
      multiSelect: false,
    },
  ],
});
```

---

## Phase 6: 進行中ストーリー一覧の更新

### 7.1 in-progress-stories.tmp更新

ストーリー完了後、進行中ストーリー一覧から削除してセッションメモリを更新する。

```bash
# プロジェクトルートを検出
if [ -f "CLAUDE.md" ]; then
  PROJECT_ROOT=$(pwd)
elif git rev-parse --show-toplevel > /dev/null 2>&1; then
  PROJECT_ROOT=$(git rev-parse --show-toplevel)
else
  PROJECT_ROOT=$(pwd)
fi

# 進行中ストーリー一覧を再生成（完了したストーリーを除外）
STORIES_LIST="$HOME/.claude/sessions/in-progress-stories.tmp"
: > "$STORIES_LIST"  # ファイルを空にする

find "$PROJECT_ROOT" -name "TODO.md" -type f | while read -r todo_file; do
  # 未完了タスクが存在するかチェック
  if grep -q "^- \[ \]" "$todo_file" || grep -q "^- \[~\]" "$todo_file"; then
    STORY_DIR=$(dirname "$todo_file")
    REL_PATH=${STORY_DIR#$PROJECT_ROOT/}

    # 進捗情報を取得
    TOTAL=$(grep -c "^- \[" "$todo_file")
    COMPLETED=$(grep -c "^- \[x\]" "$todo_file")
    PROGRESS="$COMPLETED/$TOTAL"

    # Last Updatedを取得
    LAST_UPDATED=$(grep -m 1 "^\*\*Last Updated\*\*:" "$todo_file" | sed 's/^\*\*Last Updated\*\*: //')
    if [ -z "$LAST_UPDATED" ]; then
      LAST_UPDATED="unknown"
    fi

    echo "- $REL_PATH ($PROGRESS completed, updated: $LAST_UPDATED)" >> "$STORIES_LIST"
  fi
done

if [ -s "$STORIES_LIST" ]; then
  echo "[dev:feedback] Updated in-progress stories list (removed completed story)"
else
  echo "[dev:feedback] No in-progress stories remaining"
fi
```

### 目的

- 完了したストーリーをセッションメモリから削除
- 次回セッション開始時に正確な進行中ストーリー一覧を表示
- SessionStart hookでの表示精度を向上

---

## 完了条件

- [ ] 変更内容が分析された（Phase 1）
- [ ] 機能DESIGN.mdが更新された（Phase 2a）
- [ ] **総合DESIGN.mdが更新された（Phase 2b）** ★必須★
- [ ] コード整理が実行された（Phase 2c）
- [ ] 改善・リファクタリング提案MDが作成された（該当あれば）（Phase 3）
- [ ] テスト資産の整理が実行された（TDDタスクがあった場合）（Phase 4）
- [ ] PR作成が完了した（または手動作成を選択）（Phase 5）
- [ ] Worktreeクリーンアップ手順を案内した（Phase 5）
- [ ] in-progress-stories.tmpが更新された（Phase 6）

## 関連スキル

- **dev:story**: 次のストーリーのタスク生成
- **meta-skill-creator**: スキル/ルール作成（改善提案時に連携）

## 参照

- DESIGN.mdは「実装の記録」として育てていく
- 仕様書を最初に作るのではなく、**実装後のフィードバックで徐々に蓄積・更新**
