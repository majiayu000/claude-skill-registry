---
name: protocol-di-testing
description: "Use when testing Swift code that depends on file system, network, or external APIs via protocol-based dependency injection."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-05"
---
# Protocol Composition for Testable Dependency Injection
# テスト可能な依存性注入のためのプロトコル合成

**Extracted / 抽出日:** 2026-02-05
**Context / コンテキスト:** Swift apps requiring testable architecture with file system, network, or external dependencies
ファイルシステム、ネットワーク、または外部依存関係を持つテスト可能なアーキテクチャが必要なSwiftアプリ

---

## Problem / 課題

Code that directly accesses file system, iCloud, network, or other external resources is hard to test. You need to:
- Test without real file I/O
- Simulate error conditions
- Verify interactions without side effects

ファイルシステム、iCloud、ネットワーク、その他の外部リソースに直接アクセスするコードはテストが困難。以下が必要：
- 実際のファイルI/Oなしでテスト
- エラー条件のシミュレート
- 副作用なしでインタラクションを検証

---

## Solution / 解決策

Define small, focused protocols for each external dependency. Create default implementations for production and mock implementations for testing.

外部依存関係ごとに小さく焦点を絞ったプロトコルを定義。本番用のデフォルト実装とテスト用のモック実装を作成。

### 1. Define Protocols / プロトコルの定義

```swift
// Protocol for file system access / ファイルシステムアクセス用プロトコル
public protocol FileSystemProviding: Sendable {
    func containerURL(for purpose: Purpose) -> URL?
}

// Protocol for file read/write / ファイル読み書き用プロトコル
public protocol FileAccessorProviding: Sendable {
    func read(from url: URL) throws -> Data
    func write(_ data: Data, to url: URL) throws
    func fileExists(at url: URL) -> Bool
}

// Protocol for bookmark storage / ブックマーク保存用プロトコル
public protocol BookmarkStorageProviding: Sendable {
    func saveBookmark(_ data: Data, for key: String) throws
    func loadBookmark(for key: String) throws -> Data?
}
```

### 2. Create Default Implementations / デフォルト実装の作成

```swift
public struct DefaultFileSystemProvider: FileSystemProviding {
    public init() {}

    public func containerURL(for purpose: Purpose) -> URL? {
        FileManager.default.url(forUbiquityContainerIdentifier: nil)
    }
}

public struct DefaultFileAccessor: FileAccessorProviding {
    public init() {}

    public func read(from url: URL) throws -> Data {
        try Data(contentsOf: url)
    }

    public func write(_ data: Data, to url: URL) throws {
        try data.write(to: url, options: .atomic)
    }

    public func fileExists(at url: URL) -> Bool {
        FileManager.default.fileExists(atPath: url.path)
    }
}
```

### 3. Create Mock Implementations / モック実装の作成

```swift
public final class MockFileAccessor: FileAccessorProviding, @unchecked Sendable {
    public var files: [URL: Data] = [:]
    public var readError: Error?
    public var writeError: Error?

    public init() {}

    public func read(from url: URL) throws -> Data {
        if let error = readError { throw error }
        guard let data = files[url] else {
            throw CocoaError(.fileReadNoSuchFile)
        }
        return data
    }

    public func write(_ data: Data, to url: URL) throws {
        if let error = writeError { throw error }
        files[url] = data
    }

    public func fileExists(at url: URL) -> Bool {
        files[url] != nil
    }
}
```

### 4. Inject Dependencies / 依存性の注入

```swift
public actor SyncManager {
    private let fileSystem: FileSystemProviding
    private let fileAccessor: FileAccessorProviding

    public init(
        fileSystem: FileSystemProviding = DefaultFileSystemProvider(),
        fileAccessor: FileAccessorProviding = DefaultFileAccessor()
    ) {
        self.fileSystem = fileSystem
        self.fileAccessor = fileAccessor
    }

    public func sync() async throws {
        guard let containerURL = fileSystem.containerURL(for: .sync) else {
            throw SyncError.containerNotAvailable
        }
        let data = try fileAccessor.read(from: containerURL.appendingPathComponent("data.json"))
        // ... process data
    }
}
```

### 5. Test with Mocks / モックを使ったテスト

```swift
@Test("Sync manager handles missing container")
@Test("コンテナが見つからない場合の処理")
func testMissingContainer() async {
    let mockFileSystem = MockFileSystemProvider(containerURL: nil)
    let manager = SyncManager(fileSystem: mockFileSystem)

    await #expect(throws: SyncError.containerNotAvailable) {
        try await manager.sync()
    }
}

@Test("Sync manager reads data correctly")
@Test("データを正しく読み込む")
func testReadData() async throws {
    let mockFileAccessor = MockFileAccessor()
    mockFileAccessor.files[testURL] = testData

    let manager = SyncManager(fileAccessor: mockFileAccessor)
    let result = try await manager.loadData()

    #expect(result == expectedData)
}
```

---

## Key Principles / 主要原則

1. **Single Responsibility / 単一責任**: Each protocol handles one concern / 各プロトコルは1つの関心事を処理
2. **Default Parameters / デフォルトパラメータ**: Production code uses defaults, tests inject mocks / 本番コードはデフォルトを使用、テストはモックを注入
3. **Sendable Conformance / Sendable準拠**: Required for actor isolation / actor分離に必要
4. **Error Simulation / エラーシミュレーション**: Mocks can throw configurable errors / モックは設定可能なエラーをスロー可能

---

## When to Use / 使用すべき場面

- Any code that touches file system, network, or external APIs / ファイルシステム、ネットワーク、外部APIにアクセスするコード
- When you need to test error handling paths / エラーハンドリングパスをテストする必要がある場合
- When you want deterministic tests without I/O / I/Oなしで決定論的なテストが必要な場合
- Building modules that need to work in different environments (app, test, preview) / 異なる環境（アプリ、テスト、プレビュー）で動作する必要があるモジュールを構築する場合

---

## Anti-Patterns to Avoid / 避けるべきアンチパターン

- Don't create god protocols with many methods / 多くのメソッドを持つ神プロトコルを作らない
- Don't mock internal types - only external boundaries / 内部型をモックしない - 外部境界のみ
- Don't over-engineer: if a class has no external dependencies, no protocol needed / 過剰設計しない：外部依存がないクラスにはプロトコル不要
