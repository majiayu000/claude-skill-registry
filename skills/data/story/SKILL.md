---
name: dev:story
description: |
  ストーリーからTDD/E2E/TASK分岐付きタスクリスト（TODO.md）を生成。
  ストーリー駆動開発の起点となるスキル。
  「タスクを作成」「/dev:story」で起動。

  Trigger:
  タスクを作成, ストーリーからタスク, /dev:story, story to tasks
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

# ストーリー → タスク生成（dev:story）

## エージェント委譲ルール

**⚠️ 分析・分解・分類は必ずTaskエージェントに委譲する。自分で実行しない。**

呼び出しパターン（全ステップ共通）:
```
agentContent = Read(".claude/skills/dev/story/agents/{agent}.md")
Task({ prompt: agentContent + 追加コンテキスト, subagent_type: "general-purpose", model: {指定モデル} })
```

| Step | agent | model | 追加コンテキスト |
|------|-------|-------|-----------------|
| 1a | analyze-story.md | opus | ユーザーのストーリー |
| 1b | resolve-slug.md | haiku | story-analysis.json + 既存slug一覧 |
| 2 | decompose-tasks.md | sonnet | story-analysis.jsonのパス |
| 3 | assign-workflow.md | haiku | task-list.jsonのパス |

## 出力先

`docs/features/{feature-slug}/{story-slug}/` に3ファイルを**順次**保存する。

---

## ★ 実行手順（必ずこの順序で実行）

### Step 1: ストーリー分析 → story-analysis.json

1. ユーザーからストーリーを聞き取る
2. → **エージェント委譲**（analyze-story.md / opus）
3. → **エージェント委譲**（resolve-slug.md / haiku）— 既存slugとの類似判定・候補整理
4. **AskUserQuestion** で feature-slug / story-slug を確定（resolve-slugの推奨順で選択肢提示）
5. `mkdir -p docs/features/{feature-slug}/{story-slug}`
6. **Write** で `story-analysis.json` を保存

**ゲート**: `story-analysis.json` が存在しなければ次に進まない。

### Step 2: タスク分解 → task-list.json

1. → **エージェント委譲**（decompose-tasks.md / sonnet）
   - エージェント内でGlob/Readによるコード探索・context作成を行う
2. 技術選定・方針に判断が必要ならAskUserQuestionで確認（自明ならスキップ可）
3. **Write** で `task-list.json` を保存

**ゲート**: `task-list.json` が存在しなければ次に進まない。

### Step 3: ワークフロー分類 → TODO.md

1. → **エージェント委譲**（assign-workflow.md / haiku）
2. **Write** で `TODO.md` を保存

**ゲート**: `TODO.md` が存在しなければ次に進まない。

### Step 4: ユーザー確認

- **実装開始** → dev:developing を呼び出し
- **修正が必要** → ユーザー指示に従いTODO.mdを修正 → 再確認

---

## 完了条件

以下3ファイルがすべて保存されていること:

| ファイル | Phase |
|----------|-------|
| `story-analysis.json` | Step 1 |
| `task-list.json` | Step 2 |
| `TODO.md` | Step 3 |

- 各タスクにTDD/E2E/TASKラベルが付与されている
- ユーザーが承認済み

## 参照

- agents/: analyze-story.md, decompose-tasks.md, assign-workflow.md
- references/: tdd-criteria.md, e2e-criteria.md, task-criteria.md
- ルール: `.claude/rules/workflow/workflow-branching.md`（自動適用）
