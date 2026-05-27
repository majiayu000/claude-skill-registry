---
name: claudemd-optimizer
description: |
  Optimize CLAUDE.md files based on Claude 4 best practices from Anthropic's official documentation. Use when reviewing or improving CLAUDE.md, creating new project instructions, analyzing prompt effectiveness, or applying Claude 4 model-specific optimizations. Triggers: "CLAUDE.mdを最適化", "プロジェクト指示を改善", "optimize CLAUDE.md", "review system prompt".
alwaysApply: false
---

# CLAUDE.md Optimizer

Claude 4公式ベストプラクティスに基づき、CLAUDE.mdファイルを最適化するスキル。

## Execution Flow

### 1. Read target CLAUDE.md
既存の内容を確認。なければ新規作成を提案。

### 2. Analyze against Claude 4 principles
詳細は `claude4-principles.md` を参照。主要評価軸:
- **明示性**: 指示が具体的か。修飾語（"as many as possible"）を使っているか
- **コンテキスト**: なぜそのルールが必要か説明しているか
- **構造**: XMLタグで整理されているか（必要な場合）
- **過剰防止**: 過度なエンジニアリングを抑制する指示があるか

### 3. Apply optimizations
チェックリストは `checklist.md` を参照。主要な最適化:
- 曖昧な指示 → 明示的・具体的な指示に変換
- ルールのみ → 理由（なぜ）を追加
- 過度な冗長性 → 簡潔かつ必要十分に
- 不足している重要指示を追加（過剰エンジニアリング防止など）

### 4. Report improvements
変更点とClaude 4原則への対応を説明。

## Output Format
課題 → 改善案 → 変更点（テーブル形式）の順で報告。

## Reference Files
- `claude4-principles.md`: Claude 4モデル固有のベストプラクティス詳細
- `checklist.md`: CLAUDE.md最適化チェックリスト
