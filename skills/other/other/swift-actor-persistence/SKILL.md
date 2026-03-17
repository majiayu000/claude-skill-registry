---
name: swift-actor-persistence
description: "Use when building a thread-safe data persistence layer in Swift using actors with in-memory cache and file storage."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-05"
---
# Swift Actors for Thread-Safe Persistence
# スレッドセーフな永続化のためのSwift Actor

**Extracted / 抽出日:** 2026-02-05
**Context / コンテキスト:** iOS/Swift apps requiring thread-safe data persistence with async/await
async/awaitを使用したスレッドセーフなデータ永続化が必要なiOS/Swiftアプリ

---

## Problem / 課題

Data persistence layers often face race conditions when multiple parts of an app read/write simultaneously. Traditional approaches (DispatchQueues, locks) are error-prone and verbose.

データ永続化レイヤーは、アプリの複数の部分が同時に読み書きする際にレースコンディションに直面することが多い。従来のアプローチ（DispatchQueues、ロック）はエラーが発生しやすく、冗長になりがち。

---

## Solution / 解決策

Use Swift actors to isolate all persistence state and operations. The actor model guarantees:
- No data races (compiler-enforced)
- Automatic serialization of access
- Async-first API that integrates with structured concurrency

Swift actorを使用して、すべての永続化状態と操作を分離する。actorモデルは以下を保証：
- データ競合なし（コンパイラによる強制）
- アクセスの自動シリアライズ
- 構造化並行性と統合されたasyncファーストAPI

```swift
public actor LocalRepository {
    private var cache: [String: Record] = [:]
    private let cacheFileURL: URL

    public init(directory: URL = .documentsDirectory) {
        self.cacheFileURL = directory.appendingPathComponent("cache.json")
        // Synchronous cache load during init (actor isolation not yet active)
        // init中の同期キャッシュ読み込み（actor分離がまだアクティブでないため）
        self.cache = Self.loadCacheSynchronously(from: cacheFileURL)
    }

    public func save(_ record: Record) throws {
        cache[record.id] = record
        try persistToFile()
    }

    public func loadAll() -> [Record] {
        Array(cache.values)
    }

    public func find(by id: String) -> Record? {
        cache[id]
    }

    private func persistToFile() throws {
        let data = try JSONEncoder().encode(Array(cache.values))
        try data.write(to: cacheFileURL)
    }

    private static func loadCacheSynchronously(from url: URL) -> [String: Record] {
        guard let data = try? Data(contentsOf: url),
              let records = try? JSONDecoder().decode([Record].self, from: data) else {
            return [:]
        }
        return Dictionary(uniqueKeysWithValues: records.map { ($0.id, $0) })
    }
}
```

---

## Key Patterns / 主要パターン

1. **In-memory cache + file persistence / インメモリキャッシュ + ファイル永続化**: Fast reads from cache, durable writes to disk / キャッシュからの高速読み取り、ディスクへの永続書き込み
2. **Synchronous init loading / 同期的な初期化読み込み**: Avoids async initialization complexity / 非同期初期化の複雑さを回避
3. **Dictionary keying / Dictionary型によるキー管理**: O(1) lookups by ID / IDによるO(1)の検索
4. **Private persistence / プライベートな永続化**: External callers only see domain operations / 外部呼び出し元はドメイン操作のみを参照

---

## Usage / 使用方法

```swift
let repository = LocalRepository()

// All calls are async due to actor isolation
// actor分離により、すべての呼び出しは非同期
let records = await repository.loadAll()
try await repository.save(newRecord)
let found = await repository.find(by: "question-1")
```

---

## When to Use / 使用すべき場面

- Building a data persistence layer in Swift 5.5+ / Swift 5.5以降でデータ永続化レイヤーを構築する場合
- Need thread-safe access to shared state / 共有状態へのスレッドセーフなアクセスが必要な場合
- Want to avoid manual synchronization (locks, queues) / 手動同期（ロック、キュー）を避けたい場合
- Building offline-first apps with local storage / ローカルストレージを使用したオフラインファーストアプリを構築する場合

---

## Related Patterns / 関連パターン

- Combine with `@Observable` ViewModels for UI binding / UIバインディング用に`@Observable` ViewModelと組み合わせる
- Use `Sendable` types for data crossing actor boundaries / actor境界を越えるデータには`Sendable`型を使用
- Consider `FileBasedSyncManager` actor for cloud sync operations / クラウド同期操作には`FileBasedSyncManager` actorを検討
