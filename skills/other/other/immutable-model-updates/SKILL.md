---
name: immutable-model-updates
description: "Use when designing Swift model structs that need predictable, thread-safe state updates without mutation."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-05"
---
# Immutable Model Updates with Factory Methods
# ファクトリメソッドを使ったイミュータブルなモデル更新

**Extracted / 抽出日:** 2026-02-05
**Context / コンテキスト:** Swift apps requiring predictable state management without mutations
ミューテーションなしで予測可能な状態管理が必要なSwiftアプリ

---

## Problem / 課題

Mutating shared state causes bugs:
- Race conditions in concurrent code
- Unexpected side effects
- Difficulty tracking state changes
- Hard to implement undo/redo

共有状態のミューテーションはバグを引き起こす：
- 並行コードでのレースコンディション
- 予期しない副作用
- 状態変更の追跡が困難
- Undo/Redoの実装が困難

---

## Solution / 解決策

Make all model types immutable (using `let` properties) and provide factory methods that return new instances with updated values.

すべてのモデル型をイミュータブルにし（`let`プロパティを使用）、更新された値を持つ新しいインスタンスを返すファクトリメソッドを提供。

### 1. Immutable Struct with Factory Methods / ファクトリメソッドを持つイミュータブル構造体

```swift
public struct ProgressRecord: Codable, Sendable, Identifiable, Equatable {
    public let questionId: String
    public let lastReviewed: Date?
    public let intervalDays: Int
    public let easeFactor: Double
    public let repetitions: Int
    public let nextReview: Date?

    public var id: String { questionId }

    // Private init for internal control
    // 内部制御用のプライベートinit
    private init(
        questionId: String,
        lastReviewed: Date?,
        intervalDays: Int,
        easeFactor: Double,
        repetitions: Int,
        nextReview: Date?
    ) {
        self.questionId = questionId
        self.lastReviewed = lastReviewed
        self.intervalDays = intervalDays
        self.easeFactor = easeFactor
        self.repetitions = repetitions
        self.nextReview = nextReview
    }

    // Factory: Create initial state / 初期状態を作成
    public static func initial(questionId: String) -> ProgressRecord {
        ProgressRecord(
            questionId: questionId,
            lastReviewed: nil,
            intervalDays: 0,
            easeFactor: 2.5,
            repetitions: 0,
            nextReview: nil
        )
    }

    // Factory: Create updated state / 更新された状態を作成
    public func updated(with result: ReviewResult, answeredOn date: Date = Date()) -> ProgressRecord {
        ProgressRecord(
            questionId: questionId,
            lastReviewed: date,
            intervalDays: result.interval,
            easeFactor: result.easinessFactor,
            repetitions: result.repetitions,
            nextReview: result.nextReviewDate
        )
    }

    // Factory: Update single field / 単一フィールドを更新
    public func withNextReview(_ date: Date?) -> ProgressRecord {
        ProgressRecord(
            questionId: questionId,
            lastReviewed: lastReviewed,
            intervalDays: intervalDays,
            easeFactor: easeFactor,
            repetitions: repetitions,
            nextReview: date
        )
    }
}
```

### 2. Usage Pattern / 使用パターン

```swift
// Create initial record / 初期レコードを作成
let record = ProgressRecord.initial(questionId: "q-001")

// Update returns NEW record (original unchanged)
// 更新は新しいレコードを返す（元のレコードは変更されない）
let updatedRecord = record.updated(with: reviewResult)

// Chain updates / 更新をチェーン
let finalRecord = record
    .updated(with: result1)
    .withNextReview(tomorrow)
```

### 3. Collection Updates (Immutable) / コレクションの更新（イミュータブル）

```swift
extension Array where Element == ProgressRecord {
    func updating(_ record: ProgressRecord) -> [ProgressRecord] {
        var result = self.filter { $0.questionId != record.questionId }
        result.append(record)
        return result
    }

    func removing(questionId: String) -> [ProgressRecord] {
        filter { $0.questionId != questionId }
    }
}

// Usage / 使用方法
let records = existingRecords.updating(newRecord)
```

### 4. ViewModel Integration / ViewModelとの統合

```swift
@Observable
@MainActor
public final class QuizViewModel {
    public private(set) var records: [ProgressRecord] = []

    public func recordAnswer(questionId: String, result: ReviewResult) {
        let existingRecord = records.first { $0.questionId == questionId }
            ?? ProgressRecord.initial(questionId: questionId)

        let updatedRecord = existingRecord.updated(with: result)

        // Immutable update - creates new array
        // イミュータブルな更新 - 新しい配列を作成
        records = records.updating(updatedRecord)
    }
}
```

---

## Key Benefits / 主なメリット

1. **Thread Safety / スレッドセーフ**: Immutable values can be shared across actors safely / イミュータブルな値はactor間で安全に共有可能
2. **Predictability / 予測可能性**: No hidden mutations, state changes are explicit / 隠れたミューテーションなし、状態変更は明示的
3. **Testability / テスト容易性**: Easy to create test fixtures, compare expected vs actual / テストフィクスチャの作成が容易、期待値と実際の比較が容易
4. **Debugging / デバッグ**: Can log/diff before and after states / 前後の状態をログ/差分比較可能
5. **Sendable / Sendable準拠**: Immutable structs automatically conform to Sendable / イミュータブルな構造体は自動的にSendableに準拠

---

## Factory Method Types / ファクトリメソッドの種類

| Method / メソッド | Purpose / 目的 | Example / 例 |
|--------|---------|---------|
| `static func initial(...)` | Create default state / デフォルト状態を作成 | `ProgressRecord.initial(questionId:)` |
| `func updated(with:)` | Major state transition / 主要な状態遷移 | Record after review / レビュー後のレコード |
| `func with[Field](...)` | Single field update / 単一フィールド更新 | `withNextReview(_:)` |
| `static func from(...)` | Create from external data / 外部データから作成 | `from(csvLine:)` |

---

## When to Use / 使用すべき場面

- Any model that represents state (user data, progress, settings) / 状態を表すモデル（ユーザーデータ、進捗、設定）
- Concurrent code where state is shared / 状態が共有される並行コード
- When you need change tracking or undo / 変更追跡やUndoが必要な場合
- SwiftUI apps (aligns with declarative UI model) / SwiftUIアプリ（宣言的UIモデルと整合）

---

## Anti-Patterns to Avoid / 避けるべきアンチパターン

```swift
// WRONG: Mutable struct / 間違い：ミュータブルな構造体
public struct Record {
    public var name: String  // Mutation allowed! / ミューテーション可能！
}

// WRONG: Mutating method / 間違い：mutatingメソッド
public mutating func update(name: String) {
    self.name = name  // Hidden mutation / 隠れたミューテーション
}

// WRONG: Modifying in place / 間違い：その場で変更
records[index].name = "new"  // Side effect! / 副作用！
```

---

## Related Patterns / 関連パターン

- Combine with Swift actors for thread-safe persistence / スレッドセーフな永続化のためにSwift actorと組み合わせる
- Use `Equatable` conformance for change detection / 変更検出のために`Equatable`準拠を使用
- Consider `Codable` for serialization / シリアライズのために`Codable`を検討
