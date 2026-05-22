---
name: software-patterns
description: "Unified router for 7 canonical software engineering knowledge bases. Routes queries to appropriate underlying skills: gof-patterns (23 design patterns), clrs-algorithms (40 data structures), clean-code (SOLID + practices), ddia (distributed systems), pragmatic-programmer (craftsmanship), ddd (domain modeling), sicp (CS fundamentals). Auto-activates for architecture decisions, pattern selection, algorithm choice, and system design."
---

# Software Patterns - Unified Knowledge Router

A comprehensive software engineering knowledge base spanning 147 documentation files across 7 focused skills. This router intelligently directs queries to the appropriate underlying skill(s) and orchestrates cross-skill solutions when needed.

## When This Skill Activates

This skill automatically activates when you:
- Need to choose between design patterns or algorithms
- Design system architecture or data models
- Discuss code quality, refactoring, or best practices
- Select data structures for specific requirements
- Design distributed systems or databases
- Model complex business domains
- Apply fundamental programming concepts

## Quick Reference: What Each Skill Covers

| Skill | Files | Coverage | Use For |
|-------|-------|----------|---------|
| **gof-patterns** | 25 | 23 GoF design patterns + selection guides | Object creation, composition, behavior |
| **clrs-algorithms** | 40 | Data structures & algorithms | Performance optimization, algorithm selection |
| **clean-code** | 14 | SOLID principles + 8 practices | Code quality, refactoring, maintainability |
| **ddia** | 21 | Distributed systems concepts | Scalability, consistency, availability |
| **pragmatic-programmer** | 19 | 7 principles + 11 practices | Software craftsmanship, debugging, tooling |
| **ddd** | 15 | 4 strategic + 5 tactical patterns | Domain modeling, bounded contexts |
| **sicp** | 13 | 12 fundamental CS concepts | Abstraction, recursion, interpreters |

**Total: 147 documentation files**

## Query Commands

### Pattern Queries

```
/pattern <problem>
```

Find design patterns for a specific problem.

**Examples:**
- `/pattern create objects without knowing exact type` → Factory Method
- `/pattern add behavior dynamically` → Decorator
- `/pattern notify multiple objects of changes` → Observer
- `/pattern simplify complex subsystem` → Facade

**Routes to:** `gof-patterns` skill with pattern-selection.md

### Data Structure Queries

```
/ds <requirement>
```

Find data structures for specific requirements.

**Examples:**
- `/ds fast lookup by key` → Hash Table
- `/ds maintain sorted order` → Tree Set or Heap
- `/ds fast insert/delete at ends` → Deque
- `/ds priority queue` → Binary Heap

**Routes to:** `clrs-algorithms` skill with data-structure-selection.md

### Architecture Queries

```
/architecture <scenario>
```

Get multi-skill solution stacks combining patterns, data structures, and distributed systems concepts.

**Examples:**
- `/architecture e-commerce checkout` → State pattern + Command + Observer + distributed transactions
- `/architecture real-time leaderboard` → Sorted Set + Redis + Pub/Sub
- `/architecture multi-tenant SaaS` → Abstract Factory + Bounded Contexts + Partitioning

**Routes to:** Orchestrates across `gof-patterns`, `clrs-algorithms`, `ddia`, and `ddd`

### Implementation Queries

```
/implement <pattern> [language]
```

Generate implementation code for a pattern in a specific language.

**Examples:**
- `/implement factory method typescript`
- `/implement observer python`
- `/implement heap java`

**Routes to:** Appropriate skill with language-specific translation

### Comparison Queries

```
/compare <a> vs <b>
```

Trade-off analysis between two approaches.

**Examples:**
- `/compare factory method vs abstract factory`
- `/compare array vs linked list`
- `/compare postgres vs mongodb`
- `/compare event sourcing vs crud`

**Routes to:** Relevant skill(s) with comparison tables

## How the Router Works

### 1. Query Parsing

The router analyzes queries for problem indicators:

```yaml
patterns:
  - "create", "instantiate", "build" → Creational patterns
  - "structure", "compose", "organize" → Structural patterns
  - "behavior", "algorithm", "interact" → Behavioral patterns

data_structures:
  - "fast lookup", "search", "find" → Hash or Tree
  - "sorted", "ordered" → Tree or Heap
  - "insert", "delete", "add", "remove" → List or Tree
  - "queue", "stack", "priority" → Specialized structures

distributed_systems:
  - "scale", "partition", "shard" → ddia/partitioning
  - "replicate", "consistency" → ddia/replication
  - "distributed", "consensus" → ddia/consensus

domain_modeling:
  - "entity", "value object", "aggregate" → ddd/tactical
  - "bounded context", "ubiquitous language" → ddd/strategic
```

### 2. Skill Routing

Based on query type, routes to one or more skills:

| Query Type | Primary Skill | Supporting Skills |
|------------|--------------|-------------------|
| Design pattern | `gof-patterns` | `clean-code` (SOLID), `ddd` (patterns) |
| Data structure | `clrs-algorithms` | `ddia` (storage engines) |
| Code quality | `clean-code` | `pragmatic-programmer` |
| Distributed systems | `ddia` | `clrs-algorithms` (graphs), `ddd` (contexts) |
| Domain modeling | `ddd` | `gof-patterns` (tactical patterns) |
| Fundamentals | `sicp` | `pragmatic-programmer` |
| Architecture | ALL | Orchestrated solution |

### 3. Cross-Skill Orchestration

For complex problems, the router orchestrates multiple skills:

**Example: "Design a caching layer for a distributed system"**

```
1. clrs-algorithms → LRU cache data structure (Hash Table + Doubly Linked List)
2. gof-patterns → Proxy pattern (control access), Flyweight (share state)
3. ddia → Replication strategies, consistency models
4. clean-code → Interface design, SOLID principles
```

**Example: "Build an e-commerce order processing system"**

```
1. ddd → Order aggregate, bounded contexts (order, payment, shipping)
2. gof-patterns → State (order states), Command (payment actions), Observer (notifications)
3. clrs-algorithms → Priority Queue (order processing), Hash Table (inventory lookup)
4. ddia → Event sourcing, CQRS, distributed transactions
5. clean-code → SRP (one class per concern), DIP (depend on abstractions)
```

## Auto-Trigger Rules

This skill activates automatically when queries contain these indicators:

### Pattern/Design Indicators
- "which pattern", "design pattern", "should I use"
- "factory", "singleton", "observer", "decorator", "adapter"
- "create objects", "add behavior", "simplify interface"

### Data Structure Indicators
- "which data structure", "fast lookup", "sorted order"
- "array", "list", "tree", "hash", "graph", "heap"
- "O(1)", "O(log n)", "complexity", "time/space"

### Architecture Indicators
- "design", "architecture", "how should I structure"
- "scalable", "distributed", "high availability"
- "microservices", "event-driven", "domain model"

### Code Quality Indicators
- "refactor", "code smell", "clean up", "improve"
- "SOLID", "DRY", "naming", "function size"
- "test", "maintainable", "readable"

## Skill Coverage Details

### GoF Patterns (gof-patterns)

**Creational (5 patterns):**
- Abstract Factory, Builder, Factory Method, Prototype, Singleton

**Structural (7 patterns):**
- Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy

**Behavioral (11 patterns):**
- Chain of Responsibility, Command, Interpreter, Iterator, Mediator, Memento, Observer, State, Strategy, Template Method, Visitor

**Decision Guides:**
- [pattern-selection.md](../gof-patterns/pattern-selection.md) - Comprehensive selection guide
- Problem → Pattern mapping
- Common combinations
- Anti-patterns to avoid

### CLRS Algorithms (clrs-algorithms)

**Linear Structures (6):**
- Array, Dynamic Array, Linked List, Stack, Queue, Deque

**Trees (12):**
- Binary Tree, BST, AVL, Red-Black, B-Tree, Trie, Heap, Splay Tree, Treap, Interval Tree, Order-Statistic Tree, K-D Tree

**Hash-Based (3):**
- Hash Table, Hash Set, Bloom Filter

**Graphs (5):**
- Adjacency List/Matrix, Network Flow, Strongly Connected Components, plus algorithms (BFS, DFS, Dijkstra, etc.)

**Advanced (7):**
- Skip List, Disjoint Set, Segment Tree, Fenwick Tree, Fibonacci Heap, Binomial Heap, van Emde Boas Tree

**Strings (3):**
- String Algorithms (KMP, Rabin-Karp), Suffix Array, Suffix Tree

**Algorithms:**
- Sorting (QuickSort, MergeSort, HeapSort, RadixSort)

**Decision Guides:**
- [data-structure-selection.md](../clrs-algorithms/data-structure-selection.md) - "I need fast..." scenarios
- [complexity-cheat-sheet.md](../clrs-algorithms/complexity-cheat-sheet.md) - Big-O reference

### Clean Code (clean-code)

**SOLID Principles (5):**
- Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion

**Practices (8):**
- Meaningful Names, Functions, Comments, Formatting, Error Handling, Unit Testing, Code Smells, Boy Scout Rule

### DDIA (ddia)

**Data Models (3):**
- Relational, Document, Graph

**Storage (3):**
- B-Trees, LSM-Trees, Column Storage

**Replication (3):**
- Leader-Follower, Multi-Leader, Leaderless

**Partitioning (2):**
- Strategies, Rebalancing

**Transactions (3):**
- ACID, Isolation Levels, Distributed Transactions

**Consistency (2):**
- Models, Linearizability

**Consensus (1):**
- Algorithms (Paxos, Raft)

**Processing (3):**
- Batch, Stream, Event Sourcing/CQRS

### Pragmatic Programmer (pragmatic-programmer)

**Principles (7):**
- DRY, Orthogonality, Reversibility, Tracer Bullets, Prototypes, Domain Languages, Estimating

**Practices (11):**
- Plain Text, Shell Games, Debugging, Text Manipulation, Code Generators, Design by Contract, Assertive Programming, Decoupling, Refactoring, Testing, Automation

### Domain-Driven Design (ddd)

**Strategic Patterns (4):**
- Ubiquitous Language, Bounded Contexts, Context Mapping, Anti-Corruption Layer

**Tactical Patterns (5):**
- Entities, Value Objects, Aggregates, Domain Services, Domain Events

**Supporting Patterns (3):**
- Repositories, Factories, Specifications

**Practices (2):**
- Event Storming, Model Exploration

### SICP (sicp)

**Procedures (3):**
- Abstraction, Higher-Order Functions, Recursion Patterns (linear, tail, tree, mutual)

**Data (3):**
- Data Abstraction, Hierarchical Data, Symbolic Data

**Modularity (3):**
- Assignment and State, Environment Model, Streams

**Metalinguistic (3):**
- Interpreters, Lazy Evaluation, Register Machines

## Cross-Skill Solution Stacks

### Common Architecture Patterns

#### 1. The Cache Stack
```
Pattern: Caching layer with eviction policy

Skills Used:
- clrs-algorithms: Hash Table + Doubly Linked List (LRU)
- gof-patterns: Proxy (control access), Flyweight (share state)
- ddia: Replication (distributed cache), Consistency (cache coherence)
- clean-code: SRP (separate concerns), DIP (interface-based)

Implementation Guide:
1. Use Hash Table for O(1) key lookup
2. Use Doubly Linked List for O(1) LRU eviction
3. Apply Proxy pattern to control access and logging
4. Apply Flyweight to share immutable state
5. Consider replication strategy for distributed scenarios
```

#### 2. The Event Pipeline
```
Pattern: Event-driven system with processing pipeline

Skills Used:
- gof-patterns: Observer (event notification), Command (encapsulate actions)
- clrs-algorithms: Queue (FIFO processing), Priority Queue (prioritized events)
- ddia: Stream Processing (Kafka/Flink), Event Sourcing
- ddd: Domain Events, Aggregates (event producers)
- clean-code: SRP (one handler per event type)

Implementation Guide:
1. Use Observer for event subscription
2. Use Queue or Priority Queue for event buffer
3. Use Command pattern for event handlers
4. Apply Event Sourcing for audit trail
5. Define Domain Events in Ubiquitous Language
```

#### 3. The Multi-Tenant SaaS
```
Pattern: Isolated tenants with shared infrastructure

Skills Used:
- ddd: Bounded Contexts (per tenant or shared), Context Mapping
- gof-patterns: Abstract Factory (tenant-specific objects), Strategy (tenant policies)
- clrs-algorithms: Hash Table (tenant lookup), B-Tree (tenant data indexing)
- ddia: Partitioning (tenant sharding), Isolation Levels
- clean-code: OCP (extend without modifying), ISP (tenant-specific interfaces)

Implementation Guide:
1. Define Bounded Context boundaries (shared kernel vs separate)
2. Use Abstract Factory for tenant-specific object creation
3. Use Strategy for tenant-specific policies (pricing, limits)
4. Partition data by tenant ID for isolation
5. Choose appropriate isolation level (row-level, schema-level, database-level)
```

#### 4. The E-Commerce Order System
```
Pattern: Order processing with inventory, payment, shipping

Skills Used:
- ddd: Aggregates (Order, Inventory, Payment), Bounded Contexts
- gof-patterns: State (order lifecycle), Command (payment operations), Observer (notifications)
- clrs-algorithms: Priority Queue (order processing), Hash Table (inventory lookup)
- ddia: Distributed Transactions (Saga pattern), Event Sourcing
- clean-code: SRP (separate concerns), DIP (depend on repositories)

Implementation Guide:
1. Define Order Aggregate with invariants
2. Use State pattern for order states (cart → payment → processing → shipped)
3. Use Command for payment operations (process, refund, cancel)
4. Use Observer for notifications (customer, warehouse, shipping)
5. Apply Saga pattern for distributed transaction coordination
6. Use Event Sourcing for order history and replay
```

#### 5. The Real-Time Leaderboard
```
Pattern: Sorted rankings with fast updates

Skills Used:
- clrs-algorithms: Red-Black Tree or Skip List (sorted rankings), Hash Table (user lookup)
- gof-patterns: Observer (rank change notifications), Memento (snapshot rankings)
- ddia: Replication (read scaling), Partitioning (range-based)
- clean-code: Functions (small, focused), DRY (ranking logic)

Implementation Guide:
1. Use Sorted Set (Red-Black Tree) for O(log n) insert/delete/rank
2. Use Hash Table for O(1) user score lookup
3. Apply Observer for real-time rank change notifications
4. Use Read Replicas for scaling leaderboard queries
5. Partition by rank ranges for very large leaderboards
```

## Usage Examples

### Example 1: Pattern Selection

**Query:** "I need to create objects without specifying their concrete classes"

**Router Response:**
```
Primary Match: Creational Patterns (gof-patterns)

Recommendation: Factory Method Pattern

Routing to: gof-patterns/gof-creational/factory-method.md

Additional Considerations:
- If creating families of related objects → Abstract Factory
- If construction is complex → Builder
- See: gof-patterns/pattern-selection.md for decision tree
```

### Example 2: Data Structure Selection

**Query:** "What's the best data structure for fast lookup and maintaining sorted order?"

**Router Response:**
```
Primary Match: Data Structure Selection (clrs-algorithms)

Recommendation: Tree Map (Red-Black Tree or AVL Tree)

Comparison:
- Hash Table: O(1) lookup, NO sorted order
- Tree Map: O(log n) lookup, YES sorted order ✓
- Sorted Array: O(log n) search, O(n) insert ✗

Routing to: clrs-algorithms/data-structures/trees/red-black-tree.md

See also: clrs-algorithms/data-structure-selection.md
```

### Example 3: Architecture Design

**Query:** "Design a notification system that supports email, SMS, and push notifications"

**Router Response:**
```
Multi-Skill Solution:

1. Pattern Selection (gof-patterns):
   - Observer Pattern: Subscribe to events
   - Strategy Pattern: Switch between notification methods
   - Command Pattern: Queue notification actions

2. Data Structures (clrs-algorithms):
   - Priority Queue: Prioritize urgent notifications
   - Hash Table: User preference lookup

3. Distributed Systems (ddia):
   - Queue (Kafka/RabbitMQ): Async processing
   - Retry mechanisms: Handle failures

4. Code Quality (clean-code):
   - SRP: One class per notification channel
   - OCP: Add new channels without modifying existing

Implementation Stack:
Observer → Command → Priority Queue → Strategy → DIP
```

### Example 4: Code Quality Review

**Query:** "This function is 200 lines long and does too many things. How do I improve it?"

**Router Response:**
```
Primary Match: Code Quality (clean-code)

Violations Detected:
1. Single Responsibility Principle (SRP) - function does too many things
2. Function size - should be 5-20 lines

Refactoring Steps:
1. Extract methods for each responsibility (clean-code/practices/functions.md)
2. Apply SRP (clean-code/solid/single-responsibility.md)
3. Use meaningful names (clean-code/practices/meaningful-names.md)

Supporting Guidance:
- pragmatic-programmer/practices/refactoring.md: When and how to refactor
- gof-patterns: Consider Template Method or Strategy if algorithm varies

Tools:
- Extract Method refactoring
- Compose Method pattern
- Replace Temp with Query
```

## Language Translation Notes

All examples use language-agnostic pseudocode with these conventions:
- `class` for type definitions
- `function` for methods/functions
- `->` for method calls on objects
- `//` for comments
- Type hints shown as `name: Type`

### Translation Guide

| Language | Class | Method | Call | Comment | Types |
|----------|-------|--------|------|---------|-------|
| **PHP** | `class` | `function` | `->` | `//` | Docblocks or PHP 8+ |
| **JavaScript** | `class` | `function` / arrow | `.` | `//` | JSDoc or TypeScript |
| **TypeScript** | `class` | method / arrow | `.` | `//` | Native types |
| **Python** | `class` | `def` | `.` | `#` | Type hints |
| **Java** | `class` | method | `.` | `//` | Native types |
| **C#** | `class` | method | `.` | `//` | Native types |
| **Go** | `type` / `struct` | `func` | `.` | `//` | Native types |
| **Rust** | `struct` / `trait` | `fn` | `.` | `//` | Native types |

## Advanced Usage

### Combining Multiple Skills

For complex problems, explicitly request multi-skill analysis:

```
"I need a comprehensive solution for [problem] covering patterns, data structures, and distributed systems"
```

The router will orchestrate across all relevant skills and provide:
1. Pattern recommendations (gof-patterns)
2. Data structure choices (clrs-algorithms)
3. Scalability considerations (ddia)
4. Domain modeling (ddd if applicable)
5. Code quality guidelines (clean-code)
6. Implementation best practices (pragmatic-programmer)

### Deep Dives

Request detailed documentation from specific skills:

```
"Show me the full Observer pattern documentation"
→ Routes to: gof-patterns/gof-behavioral/observer.md

"Explain Red-Black Tree implementation with examples"
→ Routes to: clrs-algorithms/data-structures/trees/red-black-tree.md

"What are all SOLID principles?"
→ Routes to: clean-code/solid/ (all 5 principles)
```

### Comparison Queries

Request trade-off analysis:

```
"/compare singleton vs dependency injection"
→ Multi-skill analysis from gof-patterns + clean-code

"/compare b-tree vs lsm-tree"
→ Multi-skill analysis from clrs-algorithms + ddia

"/compare entity vs value object"
→ Analysis from ddd/tactical/
```

## Tips for Effective Use

### 1. Start with Problem, Not Solution

❌ "Show me the Singleton pattern"
✅ "I need exactly one instance of a configuration manager"

The router will recommend the right pattern and warn about potential issues.

### 2. Provide Context

❌ "Which data structure should I use?"
✅ "I need fast lookup by key and sorted iteration over 10,000 items"

Context enables better routing and recommendations.

### 3. Ask About Trade-offs

✅ "What are the trade-offs between Factory Method and Abstract Factory?"
✅ "When should I use Array vs Linked List?"
✅ "Compare event sourcing vs traditional CRUD"

Trade-off queries trigger comparison mode with tables and decision guides.

### 4. Request Implementation Guidance

✅ "How do I implement LRU cache in TypeScript?"
✅ "Show me Observer pattern in Python"
✅ "Implement Repository pattern in PHP"

Includes language-specific code generation with best practices.

### 5. Explore Related Concepts

After getting a recommendation, ask:
- "What patterns work well with [pattern]?"
- "What are common combinations with [data structure]?"
- "How does [concept] relate to [other concept]?"

## Contributing

To add new patterns, algorithms, or concepts to any skill:
1. Follow the established format in existing documentation
2. Include definition, when to use, implementation, examples, trade-offs
3. Update the relevant SKILL.md quick reference tables
4. Add decision guide entries if applicable

## Acknowledgments

This unified knowledge base is built on the shoulders of giants:

- **Gang of Four** (Gamma, Helm, Johnson, Vlissides): Design Patterns
- **CLRS** (Cormen, Leiserson, Rivest, Stein): Introduction to Algorithms
- **Robert C. Martin** (Uncle Bob): Clean Code
- **Martin Kleppmann**: Designing Data-Intensive Applications
- **Eric Evans**: Domain-Driven Design
- **Andrew Hunt & David Thomas**: The Pragmatic Programmer
- **Harold Abelson & Gerald Jay Sussman**: Structure and Interpretation of Computer Programs

---

**Made with Claude Code**

*Total: 147 documentation files across 7 focused skills*
