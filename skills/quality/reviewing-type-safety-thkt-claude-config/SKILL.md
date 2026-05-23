---
name: reviewing-type-safety
description: >
  TypeScript type safety patterns and best practices for maximum type coverage.
  Triggers: TypeScript, type safety, any, 型安全, 型カバレッジ, strict mode.
allowed-tools: [Read, Grep, Glob, Task]
agent: type-safety-reviewer
user-invocable: false
---

# 型安全レビュー

## 検出

| ID  | パターン                      | 修正                          |
| --- | ----------------------------- | ----------------------------- |
| TS1 | `any`                         | `unknown` + 型ガード          |
| TS1 | 暗黙的any                     | 明示的な型アノテーション      |
| TS2 | `value as Type`               | 型ガード関数                  |
| TS2 | `value!` (非nullアサーション) | 明示的なnullチェック          |
| TS3 | `function fn(data)` (型なし)  | `function fn(data: Type)`     |
| TS3 | 戻り値型の欠如                | 明示的な `: ReturnType`       |
| TS4 | 網羅的でない`default:`        | `default: assertNever(value)` |

## 基準

型カバレッジ >= 95%。Any使用 = 0。Strictモード全て有効。

## 参考

| トピック   | ファイル                      |
| ---------- | ----------------------------- |
| カバレッジ | `references/type-coverage.md` |
| ガード     | `references/type-guards.md`   |
| Strict     | `references/strict-mode.md`   |
| Result     | `references/result-type.md`   |
