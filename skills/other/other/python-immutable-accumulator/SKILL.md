---
name: python-immutable-accumulator
description: "Use when building immutable state accumulators in Python. Frozen dataclass + tuple pattern with slots gotcha."
license: MIT
metadata:
  author: shimo4228
  version: "1.0"
  extracted: "2026-02-08"
---

# Python Immutable Accumulator
# Python不変蓄積パターン

**Extracted / 抽出日:** 2026-02-08
**Context / コンテキスト:** frozen dataclass + tupleで安全な状態蓄積を実現するパターン

---

## Problem / 課題

Mutableな状態蓄積はバグの温床：

```python
# WRONG: Mutable accumulation / 間違い：ミュータブルな蓄積
class Tracker:
    def __init__(self):
        self.records = []  # Shared mutable state!

    def add(self, record):
        self.records.append(record)  # Mutation → side effects
```

- 共有参照による予期しない変更
- 並行処理でのレースコンディション
- デバッグ時に「いつ変更されたか」の追跡が困難
- テストでの状態リセット漏れ

---

## Solution / 解決策

### Core Pattern / コアパターン

`frozen=True` + `slots=True` のdataclassで、`add()` が常に新しいインスタンスを返す。

```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Record:
    name: str
    value: float

@dataclass(frozen=True, slots=True)
class Accumulator:
    records: tuple[Record, ...] = ()

    def add(self, record: Record) -> "Accumulator":
        """Return a new Accumulator (never mutates self)."""
        return Accumulator(records=(*self.records, record))

    @property
    def total(self) -> float:
        return sum(r.value for r in self.records)

    def __len__(self) -> int:
        return len(self.records)
```

### Usage / 使用方法

```python
# Create → accumulate → use (all immutable)
acc = Accumulator()
acc = acc.add(Record("item1", 10.0))
acc = acc.add(Record("item2", 20.0))
print(acc.total)  # 30.0

# Original reference is never modified
empty = Accumulator()
with_one = empty.add(Record("x", 1.0))
assert len(empty) == 0      # Still empty!
assert len(with_one) == 1
```

### Pydantic Variant / Pydantic版

```python
from pydantic import BaseModel, Field

class AccumulatorModel(BaseModel, frozen=True):
    records: tuple[Record, ...] = Field(default=())

    def add(self, record: Record) -> "AccumulatorModel":
        return AccumulatorModel(records=(*self.records, record))
```

### Threading Through Functions / 関数間の受け渡し

```python
def process_item(item: str, tracker: Accumulator) -> tuple[Result, Accumulator]:
    """Process item and return updated tracker (functional style)."""
    result = do_work(item)
    record = Record(name=item, value=result.cost)
    return result, tracker.add(record)

# Chain through a pipeline
tracker = Accumulator()
for item in items:
    result, tracker = process_item(item, tracker)

print(f"Processed {len(tracker)} items, total: {tracker.total}")
```

---

## Key Design Choices / 設計上のポイント

| Choice / 選択 | Reason / 理由 |
|-------|--------|
| `frozen=True` | Hashable & prevents accidental mutation / ハッシュ可能＆意図しない変更を防止 |
| `slots=True` | Lower memory footprint / メモリ効率向上 |
| `tuple` (not `list`) | Immutable collection / 不変コレクション |
| `(*self.records, record)` | Tuple unpacking for append / タプル展開による追加 |
| Return `Self` type | Enables method chaining / メソッドチェーンを可能に |

---

## When to Use / 使用すべき場面

- コスト追跡、ログ蓄積、イベントソーシングなど累積データ
- 関数間で状態を受け渡す関数型スタイル
- テストで状態の再現性が必要な場合
- 並行処理での安全な状態管理

---

## When NOT to Use / 使用すべきでない場面

- 数百万レコードの蓄積（tupleコピーのO(n)コストが問題になる）
- パフォーマンスクリティカルなホットループ
- 単純なカウンターやフラグ（過剰設計）

---

## Gotcha: frozen+slots Testing (Python 3.12+)

When testing immutability of `frozen=True, slots=True` dataclasses, the exception type varies:

```python
@dataclass(frozen=True, slots=True)
class Section:
    heading: str
    level: int

section = Section(heading="test", level=1)
section.heading = "changed"    # AttributeError (via FrozenInstanceError)
section.extra = "not allowed"  # TypeError, NOT AttributeError!
```

- **Mutating existing field** → `AttributeError`
- **Setting non-existent attribute** → `TypeError` (Python 3.12+ with slots)

In tests, accept both:

```python
def test_slots_no_extra_attributes(self) -> None:
    section = Section(heading="test", level=1)
    with pytest.raises((AttributeError, TypeError)):
        section.extra_field = "not allowed"
```

**Root cause:** `frozen=True` uses `__setattr__` override with `super()`. Combined with `slots=True`, the C-level `super()` check fails with `TypeError` for attributes not in `__slots__`.

---

## Related Patterns / 関連パターン

- `immutable-model-updates.md` — Swift版の不変更新パターン（ファクトリメソッド）
- `cost-aware-llm-pipeline.md` — このパターンをLLMコスト追跡に適用した例
