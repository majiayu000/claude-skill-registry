---
name: graph-algorithms
description: >-
  Reference patterns for graph algorithm problems including BFS, DFS, Dijkstra,
  topological sort, union-find, MST, Bellman-Ford, and bipartite checking. Provides
  recognition signals, Python templates, edge cases, and common mistakes for each
  technique. Use when solving problems involving graphs, trees, shortest paths,
  connectivity, or dependency ordering.
user-invocable: false
disable-model-invocation: false
---

# Graph Algorithm Patterns

Graph problems appear frequently in competitive programming and technical interviews. The key challenge is recognizing which technique fits the problem structure. This reference covers eight core patterns with recognition heuristics, templates, and pitfall guides.

---

## Pattern Recognition Table

| Trigger Signals | Technique | Typical Complexity |
|---|---|---|
| Shortest path, unweighted, fewest steps | BFS | O(V + E) |
| Explore all paths, connected components, backtracking | DFS | O(V + E) |
| Shortest path, weighted (non-negative) | Dijkstra | O((V + E) log V) |
| Dependencies, ordering, DAG | Topological Sort | O(V + E) |
| Dynamic connectivity, "are X and Y connected?" | Union-Find (DSU) | O(alpha(N)) per op |
| Minimum cost to connect all nodes | MST (Kruskal/Prim) | O(E log E) |
| Weighted shortest path with negative edges | Bellman-Ford | O(V * E) |
| Two groups, coloring, odd cycle | Bipartite Check | O(V + E) |

---

## Constraint-to-Technique Mapping

Use V (vertices) and E (edges) bounds to narrow viable algorithms:

| Constraint Range | Viable Techniques | Notes |
|---|---|---|
| V <= 20 | Bitmask DP, brute-force BFS/DFS | Exponential OK |
| V <= 1,000, E <= 10,000 | All techniques, Floyd-Warshall for APSP | O(V^3) still feasible |
| V <= 100,000, E <= 200,000 | BFS, DFS, Dijkstra, Topo Sort, DSU, MST | Standard competitive range |
| V <= 1,000,000 | BFS, DFS, DSU, Kahn's | Avoid O(V log V) heaps if possible |
| Negative weights present | Bellman-Ford, SPFA | Dijkstra invalid |
| Dense graph (E ~ V^2) | Prim (adj matrix), Floyd-Warshall | Adjacency list Dijkstra still works |
| Edges arrive online | Union-Find | Incremental connectivity |

---

## Individual Patterns

### BFS (Breadth-First Search)

**Recognition Signals**
- "Shortest path" or "minimum steps" in an unweighted graph or grid
- "Level-order traversal" or "distance from source"
- Multiple starting points (multi-source BFS)
- "Nearest" something in a grid

**Core Idea**

BFS explores nodes layer by layer from the source, guaranteeing that the first time a node is reached, it is via the shortest path (in terms of edge count). Use a queue (FIFO) to process nodes in discovery order. Multi-source BFS initializes the queue with all sources at distance 0, treating them as a virtual super-source.

**Python Template**

```python
from collections import deque

def bfs_shortest_path(graph: dict[int, list[int]], start: int) -> dict[int, int]:
    """Return shortest distance from start to all reachable nodes."""
    dist: dict[int, int] = {start: 0}
    queue: deque[int] = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if neighbor not in dist:
                dist[neighbor] = dist[node] + 1
                queue.append(neighbor)
    return dist
```

For multi-source BFS, initialize `dist` and `queue` with all sources at distance 0 instead of a single start node.

**Key Edge Cases**
- Disconnected graph: unreachable nodes never appear in `dist`
- Self-loops: handled naturally (node already visited)
- Start node with no edges: returns `{start: 0}`
- Grid BFS: encode `(row, col)` as queue elements, check bounds before enqueue

**Common Mistakes**
- Using a list as a queue (`.pop(0)` is O(N); use `deque`)
- Marking visited after popping instead of before enqueuing (causes duplicates)
- Forgetting to handle the case where start == target

---

### DFS (Depth-First Search)

**Recognition Signals**
- "Find all connected components" or "is there a path?"
- "Cycle detection" in directed or undirected graphs
- "Enumerate all paths" or backtracking required
- Tree traversal (pre-order, post-order, in-order)

**Core Idea**

DFS explores as deep as possible along each branch before backtracking. It naturally discovers connected components, detects cycles, and computes entry/exit times useful for subtree queries. Use iterative DFS with an explicit stack for large graphs to avoid Python's recursion limit.

**Python Template (Iterative)**

```python
def dfs_iterative(graph: dict[int, list[int]], start: int) -> list[int]:
    """Return all nodes reachable from start in DFS order."""
    visited: set[int] = set()
    stack: list[int] = [start]
    order: list[int] = []
    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                stack.append(neighbor)
    return order
```

**Cycle Detection (Directed Graph)**

```python
def has_cycle_directed(graph: dict[int, list[int]], n: int) -> bool:
    """Detect cycle in a directed graph with n nodes (0-indexed)."""
    WHITE, GRAY, BLACK = 0, 1, 2
    color: list[int] = [WHITE] * n
    for start in range(n):
        if color[start] != WHITE:
            continue
        stack: list[tuple[int, int]] = [(start, 0)]
        color[start] = GRAY
        while stack:
            node, idx = stack.pop()
            if idx < len(graph.get(node, [])):
                stack.append((node, idx + 1))
                neighbor = graph[node][idx]
                if color[neighbor] == GRAY:
                    return True
                if color[neighbor] == WHITE:
                    color[neighbor] = GRAY
                    stack.append((neighbor, 0))
            else:
                color[node] = BLACK
    return False
```

**Key Edge Cases**
- Self-loops count as cycles in directed graphs
- Undirected cycle detection must skip the parent edge (not just visited check)
- Single-node graph with no edges has no cycle
- Disconnected graph: must start DFS from every unvisited node

**Common Mistakes**
- Hitting Python recursion limit on deep graphs (use `sys.setrecursionlimit` or iterative)
- Confusing undirected vs directed cycle detection logic
- Forgetting to handle disconnected components (only running DFS from node 0)

---

### Dijkstra's Algorithm

**Recognition Signals**
- "Shortest path" with weighted edges (non-negative weights)
- "Minimum cost to reach target"
- Grid with varying movement costs
- "Cheapest" route or "minimum total weight"

**Core Idea**

Dijkstra greedily expands the closest unvisited node using a min-heap. Each node is finalized when popped from the heap, and relaxation updates neighbor distances. It fails with negative edge weights because a finalized node's distance may later be improvable. The 0-1 BFS variant handles graphs where edges have weight 0 or 1 using a deque instead of a heap.

**Python Template**

```python
import heapq

def dijkstra(graph: dict[int, list[tuple[int, int]]], start: int) -> dict[int, int]:
    """Return shortest distance from start. graph[u] = [(v, weight), ...]."""
    dist: dict[int, int] = {start: 0}
    heap: list[tuple[int, int]] = [(0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float("inf")):
            continue
        for neighbor, weight in graph[node]:
            new_dist = d + weight
            if new_dist < dist.get(neighbor, float("inf")):
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))
    return dist
```

For 0-1 BFS (weights are only 0 or 1), use a deque: `appendleft` for weight-0 edges, `append` for weight-1 edges. This avoids the heap overhead and runs in O(V + E).

**Key Edge Cases**
- Unreachable nodes: never appear in `dist`
- Multiple edges between same pair: all are considered during relaxation
- Zero-weight edges: Dijkstra handles them, but 0-1 BFS is faster when applicable
- Very large weights: use `float("inf")` sentinel, not a magic number

**Common Mistakes**
- Not skipping stale heap entries (the `if d > dist` guard is essential)
- Using Dijkstra with negative weights (silently gives wrong answers)
- Storing `visited` set and skipping revisits without the distance check

---

### Topological Sort

**Recognition Signals**
- "Order of dependencies" or "prerequisite chain"
- "Is the directed graph a DAG?"
- "Process tasks in valid order"
- Build systems, course scheduling, compilation order

**Core Idea**

Topological sort produces a linear ordering of vertices such that for every directed edge (u, v), u appears before v. It only exists for DAGs. Kahn's algorithm (BFS-based) processes zero-indegree nodes iteratively and naturally detects cycles when the output is shorter than V. DFS-based topo sort appends nodes in reverse finish order.

**Kahn's Algorithm (BFS)**

```python
from collections import deque

def topological_sort_kahn(graph: dict[int, list[int]], n: int) -> list[int] | None:
    """Return topo order for n nodes (0-indexed), or None if cycle exists."""
    indegree: list[int] = [0] * n
    for u in graph:
        for v in graph[u]:
            indegree[v] += 1
    queue: deque[int] = deque(v for v in range(n) if indegree[v] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == n else None
```

For DFS-based topo sort, use WHITE/GRAY/BLACK coloring. Append nodes to the order when they turn BLACK (all descendants processed), then reverse. A GRAY-to-GRAY back edge indicates a cycle.

**Key Edge Cases**
- Multiple valid orderings: Kahn's with a min-heap gives lexicographically smallest
- Isolated nodes (no edges): appear anywhere in the ordering
- Self-loops: always indicate a cycle
- Empty graph: returns empty list (valid)

**Common Mistakes**
- Forgetting to initialize indegree for nodes with no incoming edges
- Using Kahn's but not checking `len(order) == n` for cycle detection
- DFS-based: forgetting to reverse the order at the end

---

### Union-Find (Disjoint Set Union)

**Recognition Signals**
- "Are nodes X and Y connected?" with dynamic edge additions
- "Number of connected components" after a series of merges
- "Detect cycle in an undirected graph"
- "Group" or "cluster" elements incrementally

**Core Idea**

Union-Find maintains a forest of disjoint sets. Each element has a parent, and the root of the tree is the set representative. Path compression flattens the tree during `find`, and union by rank keeps the tree balanced. Together they achieve nearly O(1) amortized per operation. To detect a cycle in an undirected graph, check if both endpoints of an edge share the same root before merging.

**Python Template**

```python
class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent: list[int] = list(range(n))
        self.rank: list[int] = [0] * n
        self.components: int = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # path compression
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        """Merge sets of x and y. Return False if already in same set."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        self.components -= 1
        return True
```

**Key Edge Cases**
- Single-element sets: `find(x) == x` and `union(x, x)` returns False
- Weighted union-find: store additional data (e.g., edge weights) in the parent relation
- Rollback (offline): use union by rank without path compression for undo support
- Very large N (10^6+): iterative path compression avoids stack overflow

**Common Mistakes**
- Implementing path compression recursively in Python (stack overflow for large N)
- Forgetting `union by rank` (degrades to O(N) per find without it)
- Using union-find for directed graph connectivity (it only works for undirected)

---

### MST (Kruskal's and Prim's)

**Recognition Signals**
- "Minimum cost to connect all nodes"
- "Minimum spanning tree" or "cheapest network"
- "Remove maximum weight edges while keeping connectivity"
- Edge-centric optimization on undirected weighted graphs

**Core Idea**

A minimum spanning tree connects all vertices with the minimum total edge weight. Kruskal's sorts all edges by weight and greedily adds them using union-find to avoid cycles. Prim's grows the MST from a starting vertex, always adding the cheapest edge to an unvisited neighbor. Kruskal's is simpler for sparse graphs; Prim's with a heap suits dense graphs.

**Kruskal's Algorithm**

```python
def kruskal(n: int, edges: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
    """Return MST edges. edges = [(weight, u, v), ...]. Returns [] if disconnected."""
    edges.sort()
    uf = UnionFind(n)  # uses UnionFind class from above
    mst: list[tuple[int, int, int]] = []
    for weight, u, v in edges:
        if uf.union(u, v):
            mst.append((weight, u, v))
            if len(mst) == n - 1:
                break
    return mst if len(mst) == n - 1 else []
```

**Prim's Algorithm**

```python
import heapq

def prim(graph: dict[int, list[tuple[int, int]]], n: int) -> int:
    """Return total MST weight. graph[u] = [(v, weight), ...]. -1 if disconnected."""
    visited: set[int] = {0}
    heap: list[tuple[int, int]] = [(w, v) for v, w in graph.get(0, [])]
    heapq.heapify(heap)
    total = 0
    while heap and len(visited) < n:
        weight, node = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        total += weight
        for neighbor, w in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(heap, (w, neighbor))
    return total if len(visited) == n else -1
```

**Key Edge Cases**
- Disconnected graph: MST does not exist (check edge count or visited count)
- Multiple edges with equal weight: any valid MST is acceptable
- Single node: MST weight is 0, no edges needed
- Parallel edges: Kruskal handles naturally; Prim considers all during relaxation

**Common Mistakes**
- Kruskal: not sorting edges before processing
- Prim: not checking `if node in visited` after heap pop (processes stale entries)
- Assuming MST is unique (it is only unique when all edge weights are distinct)

---

### Bellman-Ford

**Recognition Signals**
- "Shortest path" with possible negative edge weights
- "Detect negative cycle"
- "At most K edges" shortest path constraint
- SPFA mentioned or arbitrage detection

**Core Idea**

Bellman-Ford relaxes all edges V-1 times, which is sufficient to propagate shortest distances through any simple path. If a V-th relaxation still improves a distance, a negative cycle exists. Unlike Dijkstra, it handles negative weights correctly. SPFA is a queue-based optimization that only relaxes edges from recently-updated nodes, offering better average-case performance but the same worst case.

**Python Template**

```python
def bellman_ford(n: int, edges: list[tuple[int, int, int]], start: int) -> list[float] | None:
    """Return distances from start, or None if negative cycle exists.
    edges = [(u, v, weight), ...]."""
    dist: list[float] = [float("inf")] * n
    dist[start] = 0
    for _ in range(n - 1):
        for u, v, w in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] + w < dist[v]:
            return None
    return dist
```

For K-edges variant (shortest path using at most K edges), run only K iterations instead of V-1, and copy `dist` before each round to prevent using current-round updates: `prev = dist[:]`, then relax using `prev[u]`.

**Key Edge Cases**
- Negative cycle reachable from start: return None (no valid shortest path)
- Negative cycle not reachable from start: distances to reachable nodes are still valid
- Zero-weight cycles: not negative, do not affect correctness
- K-edges variant: must copy `dist` before each round to avoid using current-round updates

**Common Mistakes**
- K-edges: relaxing with current-round distances instead of previous-round copy
- Not distinguishing between "negative cycle exists" and "negative cycle reachable from start"
- Running only N-2 iterations instead of N-1

---

### Bipartite Check

**Recognition Signals**
- "Divide into two groups with no intra-group edges"
- "2-colorable" or "two-coloring"
- "Odd-length cycle" detection
- Matching problems on bipartite graphs

**Core Idea**

A graph is bipartite if and only if it contains no odd-length cycle. This is equivalent to being 2-colorable: assign alternating colors via BFS or DFS, and if any edge connects two same-colored nodes, the graph is not bipartite. For disconnected graphs, check each component independently.

**Python Template (BFS)**

```python
from collections import deque

def is_bipartite(graph: dict[int, list[int]], n: int) -> bool:
    """Check if graph with n nodes (0-indexed) is bipartite."""
    color: list[int] = [-1] * n
    for start in range(n):
        if color[start] != -1:
            continue
        color[start] = 0
        queue: deque[int] = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in graph.get(node, []):
                if color[neighbor] == -1:
                    color[neighbor] = 1 - color[node]
                    queue.append(neighbor)
                elif color[neighbor] == color[node]:
                    return False
    return True
```

To extract the two partitions, collect nodes by their color value after a successful check: `group_a = [v for v in range(n) if color[v] == 0]`.

**Key Edge Cases**
- Disconnected graph: each component must be independently bipartite
- Self-loops: immediately make the graph non-bipartite
- Single node with no edges: trivially bipartite
- Tree: always bipartite (no cycles, so no odd cycles)

**Common Mistakes**
- Only checking one connected component instead of all
- Forgetting that self-loops violate bipartiteness
- Using DFS coloring but not checking the back-edge color correctly
