---
name: parent-no-raw-loops
description: Write C++ code following Sean Parent's "No Raw Loops" philosophy. Emphasizes algorithm-based thinking, composition over iteration, and treating code as mathematical reasoning. Use when refactoring or writing new C++ to maximize clarity and correctness.
---

# Sean Parent Style Guide

## Overview

Sean Parent, former Principal Scientist at Adobe, transformed how many think about C++ with his "C++ Seasoning" and "Better Code" talks. His central thesis: raw loops are assembly language for algorithms. If you're writing a loop, you're probably missing an algorithm.

## Core Philosophy

> "No raw loops."

> "A goal of software engineering is to reduce code to its essence, to remove anything that doesn't contribute to the meaning."

Parent believes that **code should be a direct expression of intent**, and loops obscure intent by exposing mechanism.

## Design Principles

1. **No Raw Loops**: Every loop is a missed opportunity to use (or create) a named algorithm.

2. **Algorithms Express Intent**: `std::find_if` says "search"; a for-loop says "increment and compare."

3. **Composition Over Iteration**: Build complex operations from simple, well-named pieces.

4. **Seek the Essence**: Remove everything that doesn't contribute to meaning.

## When Writing Code

### Always

- Use standard algorithms when they fit exactly
- Create named algorithms when standard ones don't fit
- Prefer algorithms that express the operation's semantic meaning
- Use range-based operations (C++20 ranges when available)
- Compose simple operations rather than write complex loops
- Name intermediate variables to document intent

### Never

- Write raw `for` loops when an algorithm exists
- Nest loops when composition would work
- Inline complex logic that deserves a name
- Sacrifice clarity for cleverness
- Leave unnamed concepts in code

### Prefer

- `std::transform` over element-by-element loops
- `std::accumulate` over manual aggregation
- `std::partition` over manual reordering
- `std::remove_if` + erase over manual deletion
- Algorithm pipelines over nested loops

## The Algorithm Catalog

### Existence Queries
| Need | Algorithm |
|------|-----------|
| Does any element satisfy P? | `std::any_of` |
| Do all elements satisfy P? | `std::all_of` |
| Does no element satisfy P? | `std::none_of` |
| How many satisfy P? | `std::count_if` |

### Finding
| Need | Algorithm |
|------|-----------|
| Find first matching P | `std::find_if` |
| Find first mismatch | `std::mismatch` |
| Find subsequence | `std::search` |
| Binary search | `std::lower_bound`, `std::upper_bound` |

### Transforming
| Need | Algorithm |
|------|-----------|
| Apply f to each element | `std::transform` |
| Fill with value | `std::fill` |
| Generate values | `std::generate` |
| Copy with filter | `std::copy_if` |

### Reordering
| Need | Algorithm |
|------|-----------|
| Sort | `std::sort`, `std::stable_sort` |
| Partition by P | `std::partition`, `std::stable_partition` |
| Rotate | `std::rotate` |
| Remove matching P | `std::remove_if` |

## Code Patterns

### Before and After: The Transformation

```cpp
// RAW LOOP: What is this doing?
std::vector<int> result;
for (const auto& item : items) {
    if (item.isValid()) {
        result.push_back(item.getValue() * 2);
    }
}

// ALGORITHM: Intent is clear
auto result = items 
    | std::views::filter(&Item::isValid)
    | std::views::transform([](const Item& i) { return i.getValue() * 2; })
    | std::ranges::to<std::vector>();

// Or without C++20 ranges:
std::vector<int> result;
std::transform(
    items.begin(), items.end(),
    std::back_inserter(result),
    [](const Item& i) -> std::optional<int> {
        return i.isValid() ? std::optional{i.getValue() * 2} : std::nullopt;
    }
);
// (Then filter nullopt... or use a custom transform_if)
```

### The Erase-Remove Idiom

```cpp
// RAW LOOP: Error-prone, unclear intent
for (auto it = vec.begin(); it != vec.end(); ) {
    if (shouldRemove(*it)) {
        it = vec.erase(it);  // O(n) each time!
    } else {
        ++it;
    }
}

// ALGORITHM: O(n) total, clear intent
vec.erase(
    std::remove_if(vec.begin(), vec.end(), shouldRemove),
    vec.end()
);

// C++20: Even clearer
std::erase_if(vec, shouldRemove);
```

### Slide Algorithm (Parent's Signature)

```cpp
// Move a range to a new position within a sequence
template<typename I>  // I models RandomAccessIterator
auto slide(I first, I last, I pos) -> std::pair<I, I> {
    if (pos < first) return { pos, std::rotate(pos, first, last) };
    if (last < pos)  return { std::rotate(first, last, pos), pos };
    return { first, last };
}

// Usage: Move selected items to position
auto [new_first, new_last] = slide(
    selection_begin, selection_end, 
    drop_position
);
```

### Gather Algorithm

```cpp
// Move all elements satisfying predicate to position
template<typename I, typename P>
auto gather(I first, I last, I pos, P pred) -> std::pair<I, I> {
    return {
        std::stable_partition(first, pos, std::not_fn(pred)),
        std::stable_partition(pos, last, pred)
    };
}

// Usage: Gather all selected items around cursor
auto [sel_first, sel_last] = gather(
    items.begin(), items.end(),
    cursor_position,
    [](const Item& i) { return i.selected; }
);
```

## Mental Model

Parent thinks of code as **mathematical composition**:

1. **Name the operation**: What am I really doing?
2. **Find the algorithm**: Does this operation have a name?
3. **Compose primitives**: Can I build this from smaller operations?
4. **Factor out patterns**: Is this useful elsewhere?

## The Refactoring Test

When you see a loop, ask:
1. Is this searching? → `find`, `search`, `any_of`...
2. Is this transforming? → `transform`, `copy_if`...
3. Is this reordering? → `sort`, `partition`, `rotate`...
4. Is this aggregating? → `accumulate`, `reduce`...
5. Is this comparing? → `equal`, `mismatch`...

If none fit exactly, **write and name a new algorithm**.

