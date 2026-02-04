---
name: dev:feedback
description: |
  実装完了後、学んだことをDESIGN.mdに蓄積。リファクタリング/スキル・ルールの自己改善も提案。
  ストーリー駆動開発の終点。
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

## エージェント委譲ルール

**⚠️ 分析・更新・提案は必ずTaskエージェントに委譲する。自分で実行しない。**

呼び出しパターン（全ステップ共通）:
```
agentContent = Read(".claude/skills/dev/feedback/agents/{agent}.md")
Task({ prompt: agentContent + 追加コンテキスト, subagent_type: {type}, model: {指定モデル} })
```

| Phase | agent | model | type | 追加コンテキスト |
|-------|-------|-------|------|-----------------|
| 1 | analyze-changes.md | sonnet | general-purpose | git diff, feature-slug, story-slug |
| 2a | update-design.md | sonnet | general-purpose | Phase 1のJSON + feature-slug |
| 2c | (code-simplifier) | opus | code-simplifier | docs/features/DESIGN.mdのパス |
| 3 | propose-improvement.md | opus | general-purpose | Phase 1-2の結果 + feature-slug |
| 4 | evaluate-tests.md | haiku | general-purpose | テストファイル一覧 |

## 出力先

| ファイル | Phase |
|----------|-------|
| `docs/features/{feature-slug}/DESIGN.md` | 2a |
| `docs/features/DESIGN.md` | 2b |
| `docs/features/{feature-slug}/IMPROVEMENTS.md` | 3（該当時） |

---

## ★ 実行手順（必ずこの順序で実行）

### Phase 1: 変更内容の収集 → 分析JSON

1. → **エージェント委譲**（analyze-changes.md / sonnet）
2. 分析結果をJSONとして保持

**ゲート**: 分析JSONが得られなければ次に進まない。

### Phase 2a: 機能DESIGN.md更新

1. → **エージェント委譲**（update-design.md / sonnet）
2. `docs/features/{feature-slug}/DESIGN.md` に追記・保存

**ゲート**: 機能DESIGN.mdが更新されなければ次に進まない。

### Phase 2b: 総合DESIGN.md更新 ★必須★

1. Phase 2aの内容から、プロジェクト全体に影響する設計判断を抽出
2. `docs/features/DESIGN.md` に追記（Edit）
3. 判断基準は [references/update-format.md](.claude/skills/dev/feedback/references/update-format.md) を参照

**ゲート**: 総合DESIGN.mdが更新されなければ次に進まない。

### Phase 2c: 総合DESIGNの整理

1. → **エージェント委譲**（code-simplifier / opus）
2. 整理観点は [references/update-format.md](.claude/skills/dev/feedback/references/update-format.md) の「総合DESIGN.md整理の観点」を参照

### Phase 3: 改善提案ドキュメント化（該当時）

1. → **エージェント委譲**（propose-improvement.md / opus）
2. `docs/features/{feature-slug}/IMPROVEMENTS.md` に保存

### Phase 4: テスト資産の整理（TDDタスクがあった場合）

1. → **エージェント委譲**（evaluate-tests.md / haiku）— 保持/簡素化/削除を分類
2. **AskUserQuestion** でテスト整理方針を確認（整理する/すべて保持/スキップ）
3. 選択に応じてテストの簡素化・削除を実行

---

## 完了条件

- [ ] 変更内容が分析された（Phase 1）
- [ ] 機能DESIGN.mdが更新された（Phase 2a）
- [ ] **総合DESIGN.mdが更新された（Phase 2b）** ★必須★
- [ ] 総合DESIGNが整理された（Phase 2c）
- [ ] 改善提案が作成された（該当時）（Phase 3）
- [ ] テスト資産が整理された（TDD時）（Phase 4）

## 参照

- agents/: analyze-changes.md, update-design.md, propose-improvement.md, evaluate-tests.md
- references/: design-template.md, update-format.md, improvement-patterns.md
