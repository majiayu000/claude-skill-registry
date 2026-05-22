---
name: reviewing-readability
description: >
  Code readability review based on "The Art of Readable Code" and Miller's Law (7±2).
  Use when reviewing code clarity, improving naming, or when user mentions
  可読性, 理解しやすい, わかりやすい, 明確, 命名, 変数名, 関数名,
  ネスト, 深いネスト, 関数設計, コメント, 複雑, 難しい, 難読,
  Miller's Law, ミラーの法則, 認知負荷, AI-generated, 過剰設計.
allowed-tools: [Read, Grep, Glob, Task]
agent: readability-reviewer
context: fork
user-invocable: false
---

# Readability Review

## Detection

| ID  | Pattern                       | Fix                              |
| --- | ----------------------------- | -------------------------------- |
| RD1 | `processData()` (vague)       | `validateUserEmail()`            |
| RD1 | Misleading identifiers        | Names reveal intent              |
| RD2 | Nesting > 3 levels            | Guard clauses, extract functions |
| RD2 | Function > 30 lines           | Decompose                        |
| RD3 | Comment: `// increment i`     | Delete (self-evident)            |
| RD3 | Comment: `// TODO: fix later` | Create issue or fix now          |
| RD4 | Interface for single impl     | Remove until 2nd impl            |
| RD4 | Class for stateless logic     | Pure function                    |
| RD5 | > 5 function parameters       | Config object or decompose       |

## Thresholds

| Metric             | Recommended | Maximum |
| ------------------ | ----------- | ------- |
| Function lines     | ≤30         | 50      |
| Nesting depth      | ≤3          | 4       |
| Function arguments | ≤3          | 5       |

## References

| Topic           | File                             |
| --------------- | -------------------------------- |
| Control Flow    | `references/control-flow.md`     |
| Comments        | `references/comments-clarity.md` |
| AI Antipatterns | `references/ai-antipatterns.md`  |
| Naming          | `references/naming.md`           |
