---
name: doc-generator
description: >-
  ユーザーが「ドキュメントを生成」「GoDocを追加」「README更新」「コメントを書いて」「使い方を説明して」等と要求した時に発動。
  コードから自動的にドキュメントを生成・更新する：
  - 関数/型のGoDocコメント
  - READMEのAPI仕様セクション
  - 使用例（Example）
  - CHANGELOG.md の更新
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

### 手順
1. **ドキュメント対象の特定**:
   - ユーザー指定がある場合: その関数/パッケージ
   - 指定がない場合: GoDocコメントが不足している公開関数を検出
2. **既存ドキュメントの分析**:
   - 既存のコメントスタイルを確認
   - README.md の構造を把握
   - CHANGELOG.md のフォーマットを確認
3. **GoDocコメントの生成**:
   - 公開関数（大文字始まり）に対してコメント追加
   - GoDocの規約に従う（関数名で始める）
   - パラメータ、戻り値、エラーの説明
4. **使用例の生成**:
   - `Example` テスト関数を作成（`go test` で検証可能）
   - 典型的なユースケースを示す
5. **README更新**:
   - API仕様セクションを更新/追加
   - インストール方法
   - クイックスタート
   - 使用例
6. **検証**:
   - `go doc` で生成結果を確認
   - `go test` でExampleが動作することを確認

### GoDocコメントのベストプラクティス

#### 関数コメント
```go
// Sum calculates the sum of all integers in the provided slice.
// It returns 0 for an empty or nil slice.
//
// Example:
//   result := Sum([]int{1, 2, 3}) // returns 6
func Sum(nums []int) int { ... }
```

#### パッケージコメント
```go
// Package calc provides basic mathematical calculation utilities.
//
// This package includes functions for arithmetic operations
// such as sum, average, and statistical calculations.
package calc
```

#### 型コメント
```go
// Calculator performs arithmetic operations with state management.
type Calculator struct {
    // Total holds the running sum
    Total int
}
```

### Example テストの生成
```go
func ExampleSum() {
    result := Sum([]int{1, 2, 3, 4, 5})
    fmt.Println(result)
    // Output: 15
}

func ExampleSum_empty() {
    result := Sum([]int{})
    fmt.Println(result)
    // Output: 0
}
```

### README.md テンプレート
```markdown
# Package Name

Brief description of what this package does.

## Installation

\`\`\`bash
go get github.com/user/repo/pkg/calc
\`\`\`

## Usage

\`\`\`go
package main

import "github.com/user/repo/pkg/calc"

func main() {
    result := calc.Sum([]int{1, 2, 3})
    fmt.Println(result) // 6
}
\`\`\`

## API Reference

### func Sum(nums []int) int

Calculates the sum of all integers in the slice.

**Parameters:**
- `nums`: Slice of integers to sum

**Returns:**
- Sum of all elements (0 for empty/nil slice)

## License

MIT
```

### CHANGELOG.md 更新
```markdown
# Changelog

## [Unreleased]
### Added
- GoDoc comments for all public functions
- Example tests for Sum function
- API reference in README

### Changed
- Improved documentation clarity
```

### ドキュメント品質チェック
- [ ] すべての公開関数にコメントがあるか
- [ ] コメントが関数名で始まっているか
- [ ] パラメータと戻り値が説明されているか
- [ ] 特殊なケース（nil, empty）が説明されているか
- [ ] `go doc` で正しく表示されるか
- [ ] Exampleテストが実行可能か（`go test`）

### ベストプラクティス
- 簡潔に（1-3文）
- 専門用語は避けるか、説明を添える
- コードを読まなくても使い方が分かるレベルで
- 「何をするか」だけでなく「いつ使うべきか」も含める
- Exampleは実際に動作するコードに
