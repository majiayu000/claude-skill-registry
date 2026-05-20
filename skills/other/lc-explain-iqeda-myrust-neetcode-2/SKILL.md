---
name: lc-explain
description: Generate markdown explanation for a LeetCode solution (project)
---

# LeetCode Explain

Generate a markdown explanation for a solved problem.

## Usage

`/lc-explain <problem_id>` - Generate explanation for the problem

## Instructions

1. Find the solution file in `problems/` directory (e.g., `problems/1.two-sum.rs`)
2. Read the solution code
3. Create explanation file at `explanation/problems/<problem_id>.<problem-name>.md`

## Explanation Format

```markdown
# <problem_id>. <Problem Title>

## 問題

<問題の簡潔な説明>

```
Input: ...
Output: ...
```

## 解法: <解法名>

### アイデア

<解法の核心を1-2文で>

### アルゴリズム

1. <ステップ1>
2. <ステップ2>
3. ...

### コード解説

```rust
<コードの重要部分を抜粋して解説>
```

### 計算量

- 時間: O(?) - <理由>
- 空間: O(?) - <理由>

### 別解との比較（任意）

| 解法 | 時間 | 空間 |
|------|------|------|
| ... | ... | ... |
```

## Notes

- 日本語で書く
- Rust の API（HashMap, entry, etc.）の使い方も解説する
- 初心者にもわかりやすく
