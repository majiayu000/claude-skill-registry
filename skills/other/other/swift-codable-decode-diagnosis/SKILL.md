---
name: swift-codable-decode-diagnosis
description: "Use when debugging Swift Codable JSON decode errors with vague localizedDescription messages."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-11"
---
# Swift Codable デコードエラーの診断手法

**Extracted:** 2026-02-11
**Context:** iOS アプリで JSON デコードエラーが発生した際の根本原因特定

## Problem

iOS アプリの `Codable` デコードで JSON 読み込みに失敗した場合、
シミュレータ上のエラーメッセージはローカライズされて抽象的になる。
例: `DecodingError.keyNotFound` → 「データが見つからないため、読み込めませんでした。」

アプリ内のエラーハンドリングでは `error.localizedDescription` しか表示されないため、
どのキーがどのパスで見つからないのか分からない。

## Solution

### スタンドアロン Swift スクリプトで詳細なエラーパスを取得する

```swift
// /tmp/test_decode.swift
import Foundation

// アプリと同じモデル定義をコピー
struct MyModel: Codable { /* ... */ }
struct Container: Codable { let items: [MyModel] }

do {
    let url = URL(fileURLWithPath: "path/to/data.json")
    let data = try Data(contentsOf: url)
    let container = try JSONDecoder().decode(Container.self, from: data)
    print("SUCCESS: \(container.items.count) items")
} catch let error as DecodingError {
    switch error {
    case .keyNotFound(let key, let context):
        print("KEY NOT FOUND: \(key.stringValue)")
        print("Path: \(context.codingPath.map { $0.stringValue })")
    case .typeMismatch(let type, let context):
        print("TYPE MISMATCH: expected \(type)")
        print("Path: \(context.codingPath.map { $0.stringValue })")
    case .valueNotFound(let type, let context):
        print("VALUE NOT FOUND: \(type)")
        print("Path: \(context.codingPath.map { $0.stringValue })")
    case .dataCorrupted(let context):
        print("DATA CORRUPTED: \(context.debugDescription)")
    @unknown default:
        print("Unknown: \(error)")
    }
} catch {
    print("ERROR: \(error)")
}
```

実行:
```bash
cd /path/to/project && swift /tmp/test_decode.swift
```

### ポイント

- `context.codingPath` がエラー発生箇所の正確なパスを教えてくれる
  - 例: `["questions", "Index 0", "enhancedExplanation", "contrastTable", "Index 0"]`
- Xcode やシミュレータを起動せずにターミナルで即座に実行できる
- アプリのモデル定義をそのままコピーして使うことで、正確な再現が可能
- `localizedDescription` ではなく `DecodingError` の switch で詳細を取得するのが鍵

## When to Use

- iOS アプリで JSON デコードエラーが発生したとき
- エラーメッセージが抽象的で原因が分からないとき
- JSON データの構造変更後のデグレ確認
- CI 環境でデコード互換性を検証するとき
