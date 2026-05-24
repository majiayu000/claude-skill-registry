---
name: algorithms-data-structures
description: Algorithms and data structures from first principles through advanced analysis. Covers sorting (bubble, insertion, selection, merge, quick, heap, radix), searching (linear, binary, BFS, DFS, Dijkstra, A*), fundamental data structures (arrays, linked lists, stacks, queues, hash tables, trees, heaps, graphs, tries), complexity analysis (Big-O, Big-Omega, Big-Theta, amortized), recurrence relations, and algorithm design paradigms (divide-and-conquer, greedy, dynamic programming, backtracking). Use when analyzing, selecting, implementing, or comparing algorithms and data structures.
type: skill
category: coding
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/coding/algorithms-data-structures/SKILL.md
superseded_by: null
---
# Algorithms & Data Structures

An algorithm is a finite, unambiguous sequence of well-defined instructions for solving a class of problems. A data structure is an organization of data that enables efficient access and modification. Together they form the mechanical foundation of all computation. This skill catalogs the canonical algorithms and data structures with complexity analysis, implementation notes, and selection heuristics.

**Agent affinity:** knuth (algorithm analysis, literate implementation), turing (computability, theoretical limits)

**Concept IDs:** code-sorting-algorithms, code-searching-algorithms, code-big-o-notation, code-dynamic-programming

## Complexity Analysis at a Glance

Before studying individual algorithms, internalize the complexity hierarchy. Every algorithm has a time cost and a space cost, each expressed as a function of input size n.

| Class | Name | Example |
|---|---|---|
| O(1) | Constant | Array index access, hash table lookup (average) |
| O(log n) | Logarithmic | Binary search, balanced BST lookup |
| O(n) | Linear | Linear search, single traversal |
| O(n log n) | Linearithmic | Merge sort, heap sort, efficient comparison sorts |
| O(n^2) | Quadratic | Bubble sort, insertion sort (worst), naive string matching |
| O(n^3) | Cubic | Naive matrix multiplication, Floyd-Warshall |
| O(2^n) | Exponential | Brute-force subset enumeration, naive recursive Fibonacci |
| O(n!) | Factorial | Brute-force permutation, naive TSP |

**Big-O** gives the asymptotic upper bound. **Big-Omega** gives the lower bound. **Big-Theta** gives the tight bound (both upper and lower). When we say "merge sort is O(n log n)," we mean its worst-case running time grows no faster than c * n * log(n) for some constant c and sufficiently large n. More precisely, merge sort is Theta(n log n) because its best, average, and worst cases all share this growth rate.

**Amortized analysis** applies when individual operations vary in cost but the average over a sequence is predictable. The classic example is dynamic array resizing: a single push may cost O(n) when the array doubles, but amortized over n pushes, each costs O(1).

## Part 1 -- Sorting Algorithms

Sorting is the most studied problem in computer science. Comparison-based sorting has a proven lower bound of Omega(n log n) -- no comparison sort can do better in the worst case. Non-comparison sorts (radix, counting, bucket) can beat this bound when the data admits it.

### 1.1 -- Bubble Sort

**Mechanism:** Repeatedly walk the array, swapping adjacent elements that are out of order. After pass k, the k-th largest element is in its final position.

**Complexity:** O(n^2) time worst/average, O(n) best (already sorted, with early-exit optimization). O(1) space. Stable.

**When to use:** Almost never in production. Its value is pedagogical -- it is the simplest sorting algorithm to understand and proves that sorting is achievable through local comparisons alone.

**The early-exit optimization.** If a full pass completes with zero swaps, the array is sorted. This gives O(n) best case, making bubble sort adaptive -- it benefits from pre-existing order.

### 1.2 -- Insertion Sort

**Mechanism:** Build the sorted portion one element at a time. For each new element, shift larger elements right and insert into the correct position.

**Complexity:** O(n^2) worst/average, O(n) best (nearly sorted). O(1) space. Stable. Adaptive.

**When to use:** Small arrays (n < 20-50), nearly sorted data, online sorting (elements arrive one at a time). Many optimized sort implementations (including Timsort) use insertion sort for small partitions.

**Why it beats bubble sort.** Insertion sort performs at most n-1 comparisons on sorted input and does fewer swaps on average because it moves elements directly to their correct position rather than bubbling them one step at a time.

### 1.3 -- Selection Sort

**Mechanism:** Find the minimum element in the unsorted portion and swap it to the front. Repeat.

**Complexity:** O(n^2) in all cases. O(1) space. Not stable (swaps can break equal-element ordering). Not adaptive.

**When to use:** When write operations are expensive (flash memory, EEPROM) -- selection sort performs exactly n-1 swaps regardless of input. This is its only practical advantage.

### 1.4 -- Merge Sort

**Mechanism:** Divide the array in half, recursively sort each half, merge the sorted halves.

**Complexity:** Theta(n log n) in all cases. O(n) auxiliary space (for the merge buffer). Stable.

**The merge operation.** Two pointers walk the two sorted halves. At each step, the smaller element is copied to the output. This is O(n) per level, and there are log(n) levels, giving n log n total.

**When to use:** When stability is required, when worst-case guarantees matter, when data is on disk (merge sort's sequential access pattern is cache-friendly for external sorting). Java's Arrays.sort for objects uses a merge sort variant (Timsort).

**Recurrence relation:** T(n) = 2T(n/2) + O(n). By the Master Theorem (case 2), T(n) = Theta(n log n).

### 1.5 -- Quick Sort

**Mechanism:** Choose a pivot, partition the array so all elements less than the pivot come before it and all greater come after, recursively sort the partitions.

**Complexity:** O(n log n) average, O(n^2) worst (pathological pivot choices). O(log n) space (recursion stack, in-place). Not stable (Lomuto/Hoare partition swaps non-adjacent elements).

**Pivot selection strategies.** Random pivot gives O(n log n) expected time. Median-of-three (first, middle, last) avoids worst case on sorted input. Introselect (switch to heap sort after recursion depth exceeds 2 log n) guarantees O(n log n) worst case -- this is introsort, used by C++ std::sort.

**When to use:** Default choice for in-memory sorting when stability is not required. Cache performance is excellent (sequential access within partitions). In practice, quicksort with good pivot selection beats merge sort due to lower constant factors.

**Why O(n^2) worst case is rare.** With random pivot selection, the probability of O(n^2) behavior is vanishingly small. The expected number of comparisons is 2n ln n, approximately 1.39 n log2 n.

### 1.6 -- Heap Sort

**Mechanism:** Build a max-heap from the array (O(n) via Floyd's algorithm), then repeatedly extract the maximum and place it at the end.

**Complexity:** Theta(n log n) in all cases. O(1) space. Not stable.

**When to use:** When guaranteed O(n log n) is needed without the O(n) auxiliary space of merge sort. The constant factor is larger than quicksort's, making it slower in practice for in-memory sorting. Used as the fallback in introsort.

### 1.7 -- Radix Sort (Non-Comparison)

**Mechanism:** Sort by each digit position, from least significant to most significant, using a stable sub-sort (counting sort) at each position.

**Complexity:** O(d * (n + k)) where d is the number of digits and k is the base. For fixed-width integers, this is O(n). Space: O(n + k).

**When to use:** When sorting integers or fixed-length strings where the number of digits d is small relative to log n. Radix sort is not comparison-based and therefore not subject to the Omega(n log n) lower bound.

### Sorting Selection Heuristic

| Situation | Algorithm | Reason |
|---|---|---|
| Small array (n < 50) | Insertion sort | Low overhead, adaptive |
| General purpose, stability needed | Merge sort / Timsort | Guaranteed O(n log n), stable |
| General purpose, in-place | Quicksort (introsort) | Best average-case cache behavior |
| Guaranteed worst-case, in-place | Heap sort | No auxiliary space, no pathological cases |
| Integers, fixed-width keys | Radix sort | O(n) when d is bounded |
| Nearly sorted | Insertion sort / Timsort | Adaptive algorithms exploit existing order |
| Minimizing writes | Selection sort | Exactly n-1 swaps |

## Part 2 -- Searching Algorithms

### 2.1 -- Linear Search

**Mechanism:** Walk the collection from start to end, checking each element.

**Complexity:** O(n) worst/average, O(1) best. Works on unsorted data.

**When to use:** Unsorted data, small collections, when the cost of sorting exceeds the cost of repeated linear searches (breakeven around log n searches).

### 2.2 -- Binary Search

**Mechanism:** Maintain low and high indices. Compare the target with the middle element. If less, search the left half; if greater, search the right half. Repeat.

**Complexity:** O(log n) worst/average. Requires sorted data.

**The off-by-one trap.** Binary search is notoriously error-prone to implement. The loop invariant must be stated explicitly: "the target, if present, lies in [low, high]." Use half-open intervals [low, high) to avoid confusion. Test on arrays of size 0, 1, 2, and 3.

**Variants.** Lower bound (first element >= target), upper bound (first element > target), and exact match. The C++ STL provides std::lower_bound and std::upper_bound. Python's bisect module provides bisect_left and bisect_right.

### 2.3 -- Graph Search: BFS and DFS

**BFS (Breadth-First Search).** Explore all neighbors at depth d before depth d+1. Uses a queue. Finds shortest paths in unweighted graphs. O(V + E) time, O(V) space.

**DFS (Depth-First Search).** Explore as deep as possible before backtracking. Uses a stack (explicit or call stack). Detects cycles, finds connected components, performs topological sort. O(V + E) time, O(V) space.

**When to use BFS vs DFS.** BFS for shortest path in unweighted graphs, level-order traversal. DFS for cycle detection, topological sort, strongly connected components, maze solving.

### 2.4 -- Dijkstra's Algorithm

**Mechanism:** Greedy single-source shortest path. Maintain a priority queue of (distance, vertex) pairs. Extract the minimum, relax all its edges.

**Complexity:** O((V + E) log V) with a binary heap. O(V^2) with a simple array (better for dense graphs).

**Constraint:** No negative edge weights. For graphs with negative edges, use Bellman-Ford (O(VE)).

### 2.5 -- A* Search

**Mechanism:** Like Dijkstra but guided by a heuristic h(n) estimating the cost from n to the goal. Expands the node with the lowest f(n) = g(n) + h(n).

**Complexity:** Depends on the heuristic. With an admissible (never-overestimates) and consistent heuristic, A* is optimal and complete.

**When to use:** Pathfinding in games, robotics, navigation -- any domain where a good heuristic is available.

## Part 3 -- Fundamental Data Structures

### 3.1 -- Arrays

Contiguous memory block with O(1) random access by index. O(n) insertion/deletion in the middle (shift required). Dynamic arrays (ArrayList, Vec, list) amortize append to O(1) via doubling.

### 3.2 -- Linked Lists

Nodes connected by pointers. O(1) insertion/deletion at known position. O(n) access by index. Singly linked (forward only), doubly linked (forward and backward), circular.

**When to prefer over arrays.** Frequent insertions/deletions at arbitrary positions with known references. In practice, arrays win due to cache locality -- linked lists have poor spatial locality.

### 3.3 -- Stacks and Queues

**Stack:** LIFO (Last In, First Out). Push and pop are O(1). Used for function call tracking, expression evaluation, undo systems, DFS.

**Queue:** FIFO (First In, First Out). Enqueue and dequeue are O(1). Used for BFS, task scheduling, buffering.

**Deque:** Double-ended queue. O(1) insert/remove at both ends. Used for sliding window problems.

### 3.4 -- Hash Tables

**Mechanism:** Map keys to array indices via a hash function. O(1) average lookup, insert, delete. O(n) worst case (all keys hash to the same bucket).

**Collision resolution.** Chaining (linked list per bucket) or open addressing (linear probing, quadratic probing, double hashing). Load factor management: resize when load factor exceeds threshold (typically 0.75).

**When to use.** Fast key-value lookup, membership testing (hash sets), counting (frequency maps). The single most important data structure in practical programming.

### 3.5 -- Trees

**Binary Search Tree (BST).** Left child < parent < right child. O(log n) average operations, O(n) worst (degenerate/linear tree).

**Balanced BSTs.** AVL trees (strict balance, O(log n) guaranteed), Red-Black trees (relaxed balance, O(log n) guaranteed, fewer rotations). Used in standard library ordered maps (C++ std::map, Java TreeMap).

**B-Trees.** Multi-way balanced trees optimized for disk access. Each node holds multiple keys and has multiple children. Used in databases and file systems.

### 3.6 -- Heaps

**Binary Heap.** Complete binary tree stored as an array. Max-heap: parent >= children. Min-heap: parent <= children. O(log n) insert, O(log n) extract-min/max, O(1) peek. Used for priority queues.

**Heap property maintenance.** Sift-up after insert, sift-down after extract. Floyd's build-heap is O(n), not O(n log n) -- a non-obvious result from the geometric series of sift-down costs at each level.

### 3.7 -- Graphs

**Representation.** Adjacency list: O(V + E) space, O(degree) edge lookup. Adjacency matrix: O(V^2) space, O(1) edge lookup. List is better for sparse graphs, matrix for dense.

**Key properties.** Directed vs undirected, weighted vs unweighted, cyclic vs acyclic, connected vs disconnected, bipartite.

### 3.8 -- Tries

Prefix tree for string storage. Each edge represents a character. O(m) lookup where m is the key length, independent of the number of stored keys. Used for autocomplete, spell checking, IP routing tables.

## Part 4 -- Algorithm Design Paradigms

### 4.1 -- Divide and Conquer

**Pattern:** Split the problem into independent subproblems of the same type, solve each recursively, combine the results.

**Examples:** Merge sort, quicksort, binary search, Strassen's matrix multiplication, closest pair of points.

**Recurrence analysis.** The Master Theorem handles recurrences of the form T(n) = aT(n/b) + f(n). Three cases based on the relationship between f(n) and n^(log_b a).

### 4.2 -- Greedy Algorithms

**Pattern:** At each step, make the locally optimal choice. Never reconsider.

**When it works.** When the problem has the greedy choice property (a locally optimal choice leads to a globally optimal solution) AND optimal substructure.

**Examples:** Dijkstra's shortest path, Huffman coding, Kruskal's and Prim's MST algorithms, activity selection.

**When it fails.** The 0/1 knapsack problem -- greedy by value-to-weight ratio does not guarantee optimal packing. Use dynamic programming instead.

### 4.3 -- Dynamic Programming

**Pattern:** Break the problem into overlapping subproblems. Solve each subproblem once, store the result, and reuse it.

**Two approaches.** Top-down (memoization): recursive with caching. Bottom-up (tabulation): iterative, filling a table from base cases.

**Identifying DP problems.** Two signals: (1) optimal substructure -- the optimal solution contains optimal solutions to subproblems, and (2) overlapping subproblems -- the same subproblem is solved multiple times.

**Classic examples.** Fibonacci (trivial), longest common subsequence, edit distance (Levenshtein), 0/1 knapsack, matrix chain multiplication, shortest paths (Floyd-Warshall, Bellman-Ford).

**State definition is the key insight.** The hardest part of DP is defining what the subproblem is. For the knapsack problem: dp[i][w] = maximum value achievable using items 1..i with capacity w. For edit distance: dp[i][j] = minimum edits to transform the first i characters of string A into the first j characters of string B.

### 4.4 -- Backtracking

**Pattern:** Build a solution incrementally, abandoning a candidate ("backtracking") as soon as it is determined to be unviable.

**Examples:** N-queens, Sudoku solver, constraint satisfaction, generating permutations and combinations.

**Pruning.** The power of backtracking comes from pruning -- cutting off branches of the search tree that cannot lead to valid solutions. Without pruning, backtracking degenerates to brute-force enumeration.

## Data Structure Selection Heuristic

| Need | Structure | Why |
|---|---|---|
| Fast lookup by key | Hash table | O(1) average |
| Ordered iteration | Balanced BST / sorted array | O(n) in-order traversal |
| Fast min/max extraction | Heap | O(log n) extract, O(1) peek |
| LIFO access | Stack | O(1) push/pop |
| FIFO access | Queue | O(1) enqueue/dequeue |
| Prefix matching | Trie | O(m) per query, independent of n |
| Graph connectivity | Adjacency list + BFS/DFS | O(V + E) traversal |
| Range queries | Segment tree / BIT | O(log n) query and update |

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Confusing O and Theta | O is an upper bound, not a tight bound | Use Theta when the bound is tight |
| Ignoring constant factors | O(n) with a constant of 10^6 beats O(n^2) only for large n | Profile, don't just analyze asymptotically |
| Using linked list by default | Poor cache locality makes it slower than arrays in practice | Default to arrays; use linked lists only when pointer-based insertion is critical |
| Quicksort on adversarial input | Sorted or nearly-sorted input with naive pivot = O(n^2) | Use random pivot or introsort |
| Hash table without collision handling | Degraded to O(n) in worst case | Implement proper chaining or open addressing |
| Forgetting base cases in DP | Infinite recursion or wrong answers | Define and verify base cases before writing the recurrence |
| Off-by-one in binary search | Infinite loop or missed elements | State the loop invariant explicitly, test on small arrays |

## Cross-References

- **knuth agent:** Algorithm analysis with literate programming rigor. Primary agent for complexity proofs and algorithm selection.
- **turing agent:** Computability theory -- which problems are algorithmically solvable and which are not.
- **hopper agent:** Practical implementation in real programming languages and systems.
- **dijkstra agent:** Software design principles that guide algorithm implementation.
- **programming-fundamentals skill:** Variables, control flow, recursion -- prerequisites for implementing algorithms.
- **computational-thinking skill:** Abstraction and decomposition that precede algorithm design.

## References

- Knuth, D. E. (1997). *The Art of Computer Programming, Volume 1: Fundamental Algorithms*. 3rd edition. Addison-Wesley.
- Knuth, D. E. (1998). *The Art of Computer Programming, Volume 3: Sorting and Searching*. 2nd edition. Addison-Wesley.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms*. 4th edition. MIT Press.
- Sedgewick, R. & Wayne, K. (2011). *Algorithms*. 4th edition. Addison-Wesley.
- Skiena, S. S. (2020). *The Algorithm Design Manual*. 3rd edition. Springer.
- Aho, A. V., Hopcroft, J. E., & Ullman, J. D. (1983). *Data Structures and Algorithms*. Addison-Wesley.
