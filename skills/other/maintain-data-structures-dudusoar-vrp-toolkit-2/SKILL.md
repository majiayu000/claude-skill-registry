---
name: maintain-data-structures
description: Comprehensive reference documentation for all data structures in the VRP toolkit project. Use when needing to understand data structure definitions, attributes, formats, or representations to avoid repeatedly reading code. Covers Problem layer (Instance, Solution, Node), Algorithm layer (Solver, Operators, ALNS), Data layer (OSMnx, distance matrices), and runtime formats (routes as lists, time windows as tuples).
---

# Data Structures Reference

Quick access to all data structure definitions in the VRP toolkit. This skill saves tokens by providing pre-documented structures instead of reading source code repeatedly.

## Quick Navigation

Choose the appropriate reference based on what you're working with:

### By Layer

- **Problem Layer** → [problem_layer.md](references/problem_layer.md)
  - Instance, PDPTWInstance, Solution, Node, Constraint
  - When: Defining or working with problem instances

- **Algorithm Layer** → [algorithm_layer.md](references/algorithm_layer.md)
  - Solver, ALNSSolver, Operators, SearchState, ALNSConfig
  - When: Implementing or understanding algorithms

- **Data Layer** → [data_layer.md](references/data_layer.md)
  - OSMnx graphs, GeoDataFrame, distance matrices, data generators
  - When: Loading data, working with OSMnx, benchmarks

- **Runtime Formats** → [runtime_formats.md](references/runtime_formats.md)
  - How routes, time windows, coordinates are actually represented in code
  - When: Understanding how to work with data structures in Python

### By Common Questions

| Question | Reference | Section |
|----------|-----------|---------|
| "What attributes does Instance have?" | problem_layer.md | Instance |
| "How are routes represented?" | runtime_formats.md | Route Representation |
| "What's in an OSMnx Graph?" | data_layer.md | Graph (NetworkX) |
| "How do I configure ALNS?" | algorithm_layer.md | ALNSConfig |
| "What's the structure of a Node?" | problem_layer.md | Node |
| "How are time windows stored?" | runtime_formats.md | Time Window Representation |
| "How do destroy operators work?" | algorithm_layer.md | DestroyOperator |
| "What's in a distance matrix?" | runtime_formats.md | Distance Matrix |
| "How do I work with OSMnx nodes?" | data_layer.md | GeoDataFrame |
| "What's a Solution object?" | problem_layer.md | Solution |

### By Data Type

| Type | Reference | Description |
|------|-----------|-------------|
| `Instance` | problem_layer.md | Problem definition |
| `Solution` | problem_layer.md | Solution with routes |
| `Node` | problem_layer.md | Location/customer |
| `Route` | runtime_formats.md | `List[int]` format |
| `TimeWindow` | runtime_formats.md | `Tuple[float, float]` format |
| `ALNSConfig` | algorithm_layer.md | Algorithm configuration |
| `Operator` | algorithm_layer.md | Destroy/repair/local search |
| `nx.MultiDiGraph` | data_layer.md | OSMnx network graph |
| `np.ndarray` | runtime_formats.md | Distance/time matrices |
| `GeoDataFrame` | data_layer.md | OSMnx nodes/edges |

## When to Use This Skill

Trigger this skill when:

1. **Understanding structures**: "What attributes does X have?"
2. **Working with data**: "How do I access Y in Z?"
3. **Migrating code**: Need to understand existing data structures
4. **Implementing features**: Need to know structure interfaces
5. **Debugging**: Need to understand what data looks like
6. **Avoiding repeated reads**: Instead of reading source code files repeatedly

## Reference Files Overview

### [problem_layer.md](references/problem_layer.md)
**Size:** ~300 lines
**Contains:**
- Instance, PDPTWInstance classes
- Solution class with methods
- Node class with all attributes
- Constraint types
- Type aliases
- Common usage patterns

**Use when:** Defining problems, creating instances, working with solutions

### [algorithm_layer.md](references/algorithm_layer.md)
**Size:** ~350 lines
**Contains:**
- Solver interface
- ALNSSolver and ALNSConfig
- Destroy/Repair/LocalSearch operators
- SearchState tracking
- Operator statistics
- ALNS main loop pattern

**Use when:** Implementing algorithms, understanding operators, configuring ALNS

### [data_layer.md](references/data_layer.md)
**Size:** ~300 lines
**Contains:**
- OSMnx Graph structure (NetworkX)
- GeoDataFrame (nodes and edges)
- Distance/time matrix creation
- Data generators (OrderGenerator)
- Benchmark formats (Solomon)
- OSMnx → VRP conversions

**Use when:** Loading data, OSMnx integration, working with benchmarks

### [runtime_formats.md](references/runtime_formats.md)
**Size:** ~400 lines
**Contains:**
- Route as `List[int]` with examples
- TimeWindow as `Tuple[float, float]`
- Coordinates as tuples
- Distance matrices as NumPy arrays
- Pickup-delivery pairs as list of tuples
- Configuration dictionaries
- Common type conversions
- Memory efficiency tips

**Use when:** Understanding practical code representations, writing/reading routes

## Usage Examples

### Example 1: Understanding a Route

**Question:** "I see `route = [0, 5, 3, 7, 0]` in the code. What does this mean?"

**Action:** Load [runtime_formats.md](references/runtime_formats.md) → Route Representation

**Answer:**
- Route is a list of node IDs
- `0` = depot (start and end)
- `[5, 3, 7]` = customers visited in order
- This represents: Depot → Node 5 → Node 3 → Node 7 → Depot

### Example 2: Creating an Instance

**Question:** "How do I create a PDPTW instance?"

**Action:** Load [problem_layer.md](references/problem_layer.md) → PDPTWInstance

**Answer:**
```python
instance = PDPTWInstance(
    nodes=node_list,
    battery_capacity=100.0,
    max_route_time=480.0,
    vehicle_capacity=50.0
)
```

### Example 3: Configuring ALNS

**Question:** "What parameters can I configure for ALNS?"

**Action:** Load [algorithm_layer.md](references/algorithm_layer.md) → ALNSConfig

**Answer:** See all parameters with defaults, explanations, and usage example.

### Example 4: Working with OSMnx

**Question:** "What attributes does an OSMnx node have?"

**Action:** Load [data_layer.md](references/data_layer.md) → Node Attributes

**Answer:** `y` (lat), `x` (lon), `osmid`, `street_count`, etc.

## Benefits of This Skill

1. **Token Efficiency**: Read structured docs once instead of code files repeatedly
2. **Quick Reference**: Find information faster with organized structure
3. **Complete Coverage**: All data structures in one place
4. **Practical Examples**: Shows actual usage, not just definitions
5. **Cross-Referenced**: Easy to navigate between related structures

## Integration with Other Skills

This skill is referenced by:
- **migrate-module**: Understanding structures when migrating code
- **osmnx-integration**: OSMnx data structure details (when created)
- **add-algorithm**: Algorithm layer structures for new implementations

When other skills need data structure information, they reference this skill instead of reading source code.

## Maintenance

This reference should be updated when:
- New data structures are added to the codebase
- Existing structures change significantly
- New attributes or methods are added to core classes

Keep this as the single source of truth for data structure documentation.
