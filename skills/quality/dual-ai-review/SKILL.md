---
name: dual-ai-review
description: |
  2つの独立したAIエージェントによるコードレビュー（Evaluator-Optimizer）。
  Use when: (1) user says「デュアルAI」「二重チェック」「厳格レビュー」,
  (2) user wants high-quality code verification,
  (3) user mentions「セキュリティレビュー」「実装検証」.
  Do NOT use for: 通常のコードレビュー（code-reviewerを使用）、
  セキュリティスキャン（security-scan-trivyを使用）。
---

# Dual-AI Review Skill

2つの独立したAIエージェントがコード変更をレビューするスキル。

## 概要

Anthropicの「Evaluator-Optimizer」パターンに基づく品質保証システム。
- **Implementation AI**: コードを書く/修正する
- **Verification AI**: 脆弱性と問題をレビューする

## 使用場面

- 重要なコード変更のレビュー時
- セキュリティが重要な機能の実装時
- リグレッション防止が必要な場合
- 30-60%のバグ削減を目指す時

## ワークフロー

```
User Request
  └──> Implementation AI (backend-developer, api-developer)
       └──> Code Written
            └──> Verification AI (code-reviewer, security-*)
                 └──> Issues Found?
                      ├── Yes: Fix Instructions → Implementation AI → Re-verify (max 3)
                      └── No: ACCEPT
```

## 使用方法

```
/dual-ai-review
```

## 関連エージェント

- backend-developer
- api-developer
- code-reviewer
- security-scanner
