---
name: codex-system
description: |
  Codex CLI handles planning, design, and complex code implementation.
  Use for: architecture design, implementation planning, complex algorithms,
  debugging (root cause analysis), trade-off evaluation, code review.
  External research is NOT Codex's job — use Gemini CLI (Google Search grounding) instead.
  Explicit triggers: "plan", "design", "architecture", "think deeper",
  "analyze", "debug", "complex", "optimize".
metadata:
  short-description: Codex CLI — planning, design, and complex implementation
---

# Codex System — Planning, Design & Complex Implementation

**Codex CLI は計画・設計と難しいコード実装を担当する。**

> **詳細ルール**: `.claude/rules/codex-delegation.md`

## Codex の2つの役割

### 1. 計画・設計（Plan & Design）

- アーキテクチャ設計、モジュール構成
- 実装計画の策定（ステップ分解、依存関係整理）
- トレードオフ評価、技術選定
- コードレビュー（品質・正確性分析）

### 2. 難しいコード実装（Complex Implementation）

- 複雑なアルゴリズム、最適化
- 根本原因が不明なデバッグ
- 高度なリファクタリング
- マルチステップの実装タスク

## When to Consult (MUST)

| Situation | Trigger Examples |
|-----------|------------------|
| **Planning** | 「計画を立てて」「アーキテクチャ」 / "Plan" "Architecture" |
| **Design decisions** | 「どう設計？」 / "How to design?" |
| **Complex implementation** | 「実装方法」「どう作る？」 / "How to implement?" |
| **Debugging** | 「なぜ動かない？」「エラー」 / "Debug" "Error" |
| **Trade-off analysis** | 「どちらがいい？」「比較して」 / "Compare" "Which?" |
| **Refactoring** | 「リファクタ」「シンプルに」 / "Refactor" "Simplify" |
| **Code review** | 「レビューして」 / "Review" "Check" |

## When NOT to Consult

- 単純なファイル編集、typo修正
- 明示的なユーザー指示に従うだけの作業
- git commit、テスト実行、lint
- **コードベース分析** → Gemini CLI（1M context で大規模分析対応）
- **外部情報取得** → Gemini CLI（Google Search grounding）
- **マルチモーダル処理** → Gemini CLI（PDF/動画/音声/画像）

## How to Consult

### Subagent Pattern（推奨）

```
Task tool parameters:
- subagent_type: "general-purpose"
- run_in_background: true (optional)
- prompt: |
    Consult Codex about: {topic}

    codex exec --model gpt-5.3-codex --sandbox read-only --full-auto "
    {question for Codex}
    " 2>/dev/null

    Return CONCISE summary (key recommendation + rationale).
```

### Direct Call (〜50行の回答)

```bash
codex exec --model gpt-5.3-codex --sandbox read-only --full-auto "Brief question" 2>/dev/null
```

### Codex に実装させる場合

```bash
codex exec --model gpt-5.3-codex --sandbox workspace-write --full-auto "
Implement: {task description}
Requirements: {requirements}
Files: {file paths}
" 2>/dev/null
```

### Sandbox Modes

| Mode | Use Case |
|------|----------|
| `read-only` | 設計、レビュー、デバッグ分析 |
| `workspace-write` | 実装、修正、リファクタリング |

## Task Templates

### Implementation Planning

```bash
codex exec --model gpt-5.3-codex --sandbox read-only --full-auto "
Create an implementation plan for: {feature}

Context: {relevant architecture/code}

Provide:
1. Step-by-step plan with dependencies
2. Files to create/modify
3. Key design decisions
4. Risks and mitigations
" 2>/dev/null
```

### Design Review

```bash
codex exec --model gpt-5.3-codex --sandbox read-only --full-auto "
Review this design approach for: {feature}

Context: {relevant code or architecture}

Evaluate:
1. Is this approach sound?
2. Alternative approaches?
3. Potential issues?
4. Recommendations?
" 2>/dev/null
```

### Debug Analysis

```bash
codex exec --model gpt-5.3-codex --sandbox read-only --full-auto "
Debug this issue:

Error: {error message}
Code: {relevant code}
Context: {what was happening}

Analyze root cause and suggest fixes.
" 2>/dev/null
```

## Language Protocol

1. Ask Codex in **English**
2. Receive response in **English**
3. Execute based on advice
4. Report to user in **Japanese**

## Why Codex?

- **Deep reasoning**: Complex analysis and problem-solving
- **Planning expertise**: Architecture and implementation strategies
- **Code mastery**: Complex algorithms, optimization, debugging
- **Consistency**: Same project context via `context-loader` skill
