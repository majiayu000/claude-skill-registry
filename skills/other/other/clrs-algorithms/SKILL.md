---
name: clrs-algorithms
description: "Data structures and algorithms reference based on CLRS. Use this skill when implementing, discussing, or choosing data structures or algorithms. Auto-activates for algorithm selection, complexity analysis, and performance optimization. Comprehensive coverage of fundamental and advanced data structures with pseudocode examples."
---

# CLRS Data Structures & Algorithms Reference

A comprehensive reference for data structures and algorithms based on "Introduction to Algorithms" (CLRS). This skill provides language-agnostic guidance with pseudocode examples that can be translated to any programming language.

## When This Skill Activates

This skill automatically activates when you:
- Ask about or need to implement a data structure
- Need to choose between data structures for a problem
- Discuss time/space complexity trade-offs
- Need algorithm implementations (sorting, searching, graph algorithms)
- Mention specific structures: B-tree, heap, hash table, graph, etc.

## Quick Data Structure Reference

### Linear Structures
| Structure | Access | Search | Insert | Delete | Use When |
|-----------|--------|--------|--------|--------|----------|
| [Array](data-structures/linear/array.md) | O(1) | O(n) | O(n) | O(n) | Known size, index access |
| [Dynamic Array](data-structures/linear/dynamic-array.md) | O(1) | O(n) | O(1)* | O(n) | Unknown size, frequent append |
| [Linked List](data-structures/linear/linked-list.md) | O(n) | O(n) | O(1) | O(1) | Frequent insert/delete |
| [Stack](data-structures/linear/stack.md) | O(1) | O(n) | O(1) | O(1) | LIFO needed |
| [Queue](data-structures/linear/queue.md) | O(1) | O(n) | O(1) | O(1) | FIFO needed |
| [Deque](data-structures/linear/deque.md) | O(1) | O(n) | O(1) | O(1) | Both ends access |

### Trees
| Structure | Search | Insert | Delete | Use When |
|-----------|--------|--------|--------|----------|
| [Binary Search Tree](data-structures/trees/bst.md) | O(log n)* | O(log n)* | O(log n)* | Ordered data, frequent search |
| [AVL Tree](data-structures/trees/avl-tree.md) | O(log n) | O(log n) | O(log n) | Guaranteed balance needed |
| [Red-Black Tree](data-structures/trees/red-black-tree.md) | O(log n) | O(log n) | O(log n) | Frequent inserts/deletes |
| [B-Tree](data-structures/trees/b-tree.md) | O(log n) | O(log n) | O(log n) | Disk-based storage |
| [Trie](data-structures/trees/trie.md) | O(m) | O(m) | O(m) | String/prefix operations |
| [Heap](data-structures/trees/heap.md) | O(1)/O(n) | O(log n) | O(log n) | Priority queue needed |
| [Splay Tree](data-structures/trees/splay-tree.md) | O(log n)* | O(log n)* | O(log n)* | Self-adjusting, temporal locality |
| [Treap](data-structures/trees/treap.md) | O(log n)* | O(log n)* | O(log n)* | Randomized balance, split/merge |
| [Interval Tree](data-structures/trees/interval-tree.md) | O(log n) | O(log n) | O(log n) | Interval overlap queries |
| [Order-Statistic Tree](data-structures/trees/order-statistic-tree.md) | O(log n) | O(log n) | O(log n) | Rank/select queries |
| [K-D Tree](data-structures/trees/kd-tree.md) | O(log n)* | O(log n)* | O(log n)* | Multi-dimensional spatial data |

### Hash-Based
| Structure | Search | Insert | Delete | Use When |
|-----------|--------|--------|--------|----------|
| [Hash Table](data-structures/hash-based/hash-table.md) | O(1)* | O(1)* | O(1)* | Fast key-value lookup |
| [Hash Set](data-structures/hash-based/hash-set.md) | O(1)* | O(1)* | O(1)* | Unique membership testing |
| [Bloom Filter](data-structures/hash-based/bloom-filter.md) | O(k) | O(k) | N/A | Probabilistic membership |

### Graphs
| Structure | Space | Add Edge | Query Edge | Use When |
|-----------|-------|----------|------------|----------|
| [Adjacency List](data-structures/graphs/adjacency-list.md) | O(V+E) | O(1) | O(degree) | Sparse graphs |
| [Adjacency Matrix](data-structures/graphs/adjacency-matrix.md) | O(V²) | O(1) | O(1) | Dense graphs |

### Graph Algorithms
| Algorithm | Time | Use When |
|-----------|------|----------|
| [Network Flow](data-structures/graphs/network-flow.md) | O(VE²) | Max flow, bipartite matching, min cut |
| [Strongly Connected Components](data-structures/graphs/strongly-connected-components.md) | O(V+E) | Find SCCs, 2-SAT, dependency analysis |

### Strings
| Structure | Build | Search | Use When |
|-----------|-------|--------|----------|
| [Suffix Array](data-structures/strings/suffix-array.md) | O(n log n) | O(m log n) | Space-efficient string matching |
| [Suffix Tree](data-structures/strings/suffix-tree.md) | O(n) | O(m) | Fast pattern matching, LCS |
| [String Algorithms](data-structures/strings/string-algorithms.md) | O(m) | O(n) | KMP, Rabin-Karp, Boyer-Moore, Aho-Corasick |

### Advanced
| Structure | Use When |
|-----------|----------|
| [Skip List](data-structures/advanced/skip-list.md) | Probabilistic balanced list |
| [Disjoint Set](data-structures/advanced/disjoint-set.md) | Union-find operations |
| [Segment Tree](data-structures/advanced/segment-tree.md) | Range queries with updates |
| [Fenwick Tree](data-structures/advanced/fenwick-tree.md) | Prefix sums with updates |
| [Fibonacci Heap](data-structures/advanced/fibonacci-heap.md) | Dijkstra, Prim with O(1) decrease-key |
| [Binomial Heap](data-structures/advanced/binomial-heap.md) | Mergeable priority queue |
| [van Emde Boas Tree](data-structures/advanced/van-emde-boas-tree.md) | Integer keys with O(log log u) operations |

### Algorithms
| Algorithm | Use When |
|-----------|----------|
| [Sorting Algorithms](data-structures/algorithms/sorting-algorithms.md) | QuickSort, MergeSort, HeapSort, RadixSort, and more |

*\* = amortized or average case*

## Decision Guides

- [Which Data Structure Should I Use?](data-structure-selection.md) - Decision guide by use case
- [Complexity Cheat Sheet](complexity-cheat-sheet.md) - Quick reference for Big-O

## How to Use This Reference

1. **Choosing a structure**: Start with the decision guides
2. **Learning a structure**: Read the full documentation with examples
3. **Quick reminder**: Use the tables above for at-a-glance reference
4. **Implementation**: Follow the pseudocode, adapt to your language

## Language Translation Notes

The pseudocode in this reference uses these conventions:
- `class` for type definitions
- `function` for methods/functions
- `->` for method calls on objects
- `//` for comments
- Type hints shown as `name: Type`

Translate to your language:
- **PHP**: `class`, `function`, `->`, `//`, type hints in docblocks or PHP 8+
- **JavaScript/TypeScript**: `class`, `function`/arrow, `.`, `//`, TS types
- **Python**: `class`, `def`, `.`, `#`, type hints
- **Java/C#**: Direct mapping with `new`, generics

---

*Based on concepts from "Introduction to Algorithms" by Cormen, Leiserson, Rivest, and Stein (CLRS), MIT Press.*
