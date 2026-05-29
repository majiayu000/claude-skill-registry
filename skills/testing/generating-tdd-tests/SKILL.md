---
name: generating-tdd-tests
description: >
  TDD with RGRC cycle and Baby Steps methodology.
  Triggers: TDD, test-driven, RGRC, Baby Steps, テスト駆動, Red-Green-Refactor.
allowed-tools: [Read, Write, Edit, Grep, Glob, Task]
context: fork
user-invocable: false
---

# TDDテスト生成

## RGRCサイクル

| フェーズ | 目標           | ルール                      |
| -------- | -------------- | --------------------------- |
| Red      | 失敗テスト     | 失敗理由を確認              |
| Green    | テストをパス   | "罪を犯してよい" - dirty OK |
| Refactor | クリーンコード | テストをグリーンに保つ      |
| Commit   | 状態を保存     | 全チェックをパス            |

## Baby Steps (2分サイクル)

30秒: 失敗テスト作成 → 1分: パス → 10秒: テスト実行 → 30秒: 小さなリファクタ → 20秒: グリーンならコミット

## テスト設計

| 技法     | 用途                     | 例                     |
| -------- | ------------------------ | ---------------------- |
| 同値分割 | 同じ振る舞いをグループ化 | 年齢: <18, 18-120      |
| 境界値   | 境界をテスト             | 17, 18, 120, 121       |
| 決定表   | 複数条件ロジック         | isLoggedIn × isPremium |

## カバレッジ

| レベル | 目標 | フォーカス       |
| ------ | ---- | ---------------- |
| C0     | 90%  | すべての行を実行 |
| C1     | 80%  | すべてのブランチ |

## 命名

| レベル | パターン                                |
| ------ | --------------------------------------- |
| Suite  | `describe("[対象]", ...)`               |
| Group  | `describe("[メソッド]", ...)`           |
| Test   | `it("when [条件], should [期待]", ...)` |

## フレームワーク検出

| 条件                    | フレームワーク |
| ----------------------- | -------------- |
| `vitest` が deps にある | Vitest         |
| `jest` が deps にある   | Jest           |
| `bun` がランタイム      | Bun test       |
| フレームワークなし      | Vitest         |

## 参照

| トピック         | ファイル                              |
| ---------------- | ------------------------------------- |
| 機能駆動         | `references/feature-driven.md`        |
| バグ駆動         | `references/bug-driven.md`            |
| フレーキーテスト | `references/flaky-test-management.md` |
