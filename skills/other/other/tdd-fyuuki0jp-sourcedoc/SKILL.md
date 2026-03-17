---
name: tdd
description: Detroit-style BDD開発フロー。シナリオテストをメインに据え、振る舞い駆動でテストを設計する。
---

# TDD スキル (Detroit-style BDD)

振る舞い駆動開発（BDD）をデトロイト派アプローチで実践するスキル。
シナリオテストを主軸に、ユースケースの振る舞いをGiven-When-Then形式で記述する。

## 開発サイクル

```
Plan → Skeleton → Red → Green → Integrate
```

| Phase | Agent | 担うもの |
|-------|-------|----------|
| Skeleton | `skeleton` | 型・シグネチャ・intent（why） |
| Red | `red` | シナリオテスト（what） |
| Green | `green` | 実装 |

## Detroit School BDD 原則

### 1. 振る舞い中心

内部実装ではなく、外部から見える振る舞いをテストする。
「この関数は何をするか」ではなく「ユーザー/システムは何を達成できるか」を記述。

### 2. 実オブジェクト協調

モックは外部依存（DB、外部API）のみに限定。
ドメインロジックは実オブジェクトを協調させてテストする。

```typescript
// Good: 実オブジェクト協調
const state = replay(events, applyTodoEventToAggregate);
const result = decideTodo(state, command, meta);

// Avoid: 過度なモック
const mockState = { ...mocked };
const mockDecide = vi.fn().mockReturnValue(...);
```

### 3. ユビキタス言語

ドメイン用語でテストを記述する。
テストは仕様書としても機能する。

```typescript
// Good: ドメイン言語
describe("Scenario: Todoを完了にする", () => {});

// Avoid: 技術的な記述
describe("decideTodo returns TodoCompleted event", () => {});
```

### 4. Given-When-Then

自然言語に近いシナリオ構造で記述。

```typescript
describe("Scenario: Todoを完了にする", () => {
  // Given: 前提条件
  // When: アクション
  // Then: 期待する結果
});
```

## テスト階層

| 層 | 目的 | ファイル形式 | 優先度 |
|----|------|--------------|--------|
| **Scenario** | ユースケースの振る舞い | `*.scenario.test.ts` | 主 |
| **Unit** | 純粋関数の境界値・エッジケース | `*.test.ts` | 従 |
| **Integration** | 外部依存を含む結合 | `*.integration.test.ts` | 必要時 |

### ファイル配置

```
src/features/{feature}/
├── __tests__/
│   ├── {feature}.scenario.test.ts  ← シナリオテスト（メイン）
│   └── {feature}.test.ts           ← 単体テスト（必要時）
└── model/
    └── decide.ts                    ← ビジネスロジックのみ
```

**in-source testingは使用しない**: テストとプロダクションコードを分離し、関心の分離を明確にする。

## ES-lite での Given-When-Then パターン

CQRS + Event Sourcing アーキテクチャでのシナリオテストパターン。

### 基本構造

```typescript
import { replay } from "@/shared/lib/test/scenario";
import { testMeta, eventHistory } from "@/shared/lib/test/builders";
import { decideTodo } from "@/entities/todo/model/decide";
import { applyTodoEventToAggregate } from "@/entities/todo/model/evolve";

describe("Feature: Todo管理", () => {
  describe("Scenario: Todoを完了にする", () => {
    // Given: 過去のイベントで状態を構築
    const events = eventHistory()
      .created({ title: "買い物に行く" })
      .build();
    const state = replay(events, applyTodoEventToAggregate);
    const meta = testMeta({ aggregateId: state!.id, version: state!.version + 1 });

    // When: コマンドを実行
    const result = decideTodo(
      state,
      { type: "CompleteTodo", aggregateId: state!.id, expectedVersion: state!.version },
      meta
    );

    // Then: 期待するイベントが発生
    it("TodoCompletedイベントが発生する", () => {
      expect(result.isOk()).toBe(true);
      expect(result.value).toHaveLength(1);
      expect(result.value![0].type).toBe("TodoCompleted");
    });

    it("完了時刻が記録される", () => {
      expect(result.value![0].data.completedAt).toBe(meta.timestamp);
    });
  });

  describe("Scenario: 削除済みTodoは更新できない", () => {
    // Given: 削除済みのTodo
    const events = eventHistory()
      .created({ title: "古いTodo" })
      .thenDeleted()
      .build();
    const state = replay(events, applyTodoEventToAggregate);
    const meta = testMeta({ aggregateId: state!.id, version: state!.version + 1 });

    // When: 更新を試みる
    const result = decideTodo(
      state,
      { type: "UpdateTodo", aggregateId: state!.id, title: "新しいタイトル", expectedVersion: state!.version },
      meta
    );

    // Then: エラーが返される
    it("削除済みエラーが返される", () => {
      expect(result.isErr()).toBe(true);
      expect(result.error?.message).toContain("削除済み");
    });
  });
});
```

### シナリオテストのポイント

1. **Given**: `eventHistory()` と `replay()` で状態を構築
2. **When**: コマンド実行（`decideTodo`等）
3. **Then**: イベント発生または状態変化を検証

### 状態遷移の検証

イベント適用後の状態を検証する場合：

```typescript
describe("Scenario: Todo完了後の状態", () => {
  const events = eventHistory()
    .created({ title: "タスク" })
    .thenCompleted()
    .build();
  const state = replay(events, applyTodoEventToAggregate);

  it("isCompletedがtrueになる", () => {
    expect(state?.isCompleted).toBe(true);
  });

  it("statusがdoneになる", () => {
    expect(state?.status).toBe("done");
  });
});
```

## ペアワイズ法

テストケースの組み合わせ爆発を防ぎつつ網羅性を確保。
**シナリオテストのパラメータ組み合わせ**に適用する。

### 使い方

```bash
npx tsx .claude/skills/tdd/scripts/generate-pairwise.ts config.json
```

### 設定ファイル例

```json
{
  "parameters": {
    "todoStatus": ["todo", "in_progress", "done"],
    "action": ["complete", "delete", "update"],
    "isDeleted": [false, true]
  },
  "boundaries": {
    "expectedVersion": [0, -1, 999]
  }
}
```

### 出力

```json
{
  "stats": {
    "totalCases": 12,
    "fullCombinations": 18,
    "reduction": "33.3%"
  },
  "testCases": [
    { "id": 1, "params": { "todoStatus": "todo", "action": "complete", "isDeleted": false }, "isBoundary": false },
    ...
  ]
}
```

## テスト設計の原則

1. **シナリオ優先**: ユースケースをシナリオとしてテスト
2. **ペアワイズ**: パラメータ組み合わせはペアワイズ法で削減
3. **境界値**: 各パラメータの境界値は必ずテスト
4. **Intent → Test**: skeletonのintent commentsから直接テストケースを導出

## テストヘルパー

### replay

イベント配列から状態を再構築：

```typescript
import { replay } from "@/shared/lib/test/scenario";

const state = replay(events, applyTodoEventToAggregate);
```

### eventHistory

イベント履歴を流暢に構築：

```typescript
import { eventHistory } from "@/shared/lib/test/builders";

const events = eventHistory()
  .created({ title: "タスク" })
  .thenUpdated({ title: "更新後" })
  .thenCompleted()
  .build();
```

### testMeta

テスト用メタデータを生成：

```typescript
import { testMeta } from "@/shared/lib/test/builders";

const meta = testMeta({ aggregateId: "todo-1", version: 2 });
```