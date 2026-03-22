---
name: logic-programmer
description: Logic programming thinking patterns and relational design principles. Use when working with logic languages (Prolog, miniKanren, Datalog, OWL2, Answer Set Programming) or applying declarative, constraint-based approaches in multi-paradigm systems.
---

# Logic Programmer

## Purpose

This skill provides guidance on logic programming thinking patterns and when relational, declarative approaches clarify problems. Logic programming expresses computation as logical inference over relations rather than procedural steps. This skill focuses on recognizing when problems are naturally relational, designing declarative specifications, and understanding the trade-offs of different logic programming approaches.

## When to Use This Skill

Use this skill when:
- Working with logic languages (Prolog, miniKanren, Datalog, OWL2, Mercury, Answer Set Programming)
- Solving constraint satisfaction or combinatorial search problems
- Designing knowledge bases, ontologies, or inference systems
- Applying relational thinking to queries and pattern matching
- Recognizing when declarative specification clarifies over procedural algorithm

<core_philosophy>
## Core Philosophy

<relational_thinking_decision>
### Relational Thinking: When It Clarifies vs When It Obscures

Logic programming thinks in terms of relationships that must hold, not steps to execute. The key question: does relational thinking make the problem clearer?

**Relational thinking clarifies when:**
- Problem is naturally expressed as constraints (what must be true, not how to compute)
- Multiple computational directions needed (bidirectional relations)
- Specification is more important than algorithm (declarative rules)
- Querying relationships in structured data
- Generating multiple solutions from constraints

**Relational thinking obscures when:**
- Clear, efficient procedural algorithm exists
- Single computational direction suffices
- Stateful, imperative operations required
- Performance-critical numeric computation
- Procedural version is obviously simpler

**Staff insight:** Don't force problems into relational form. The power of logic programming is clarity through declarative specification. If the relational version is harder to understand than the procedural version, you're using the wrong paradigm.
</relational_thinking_decision>

> "Algorithm = Logic + Control" — Robert Kowalski (1979)

An algorithm consists of logic (what to compute) and control (how to compute it). Ideal logic programming separates these; pragmatic logic programming often requires considering both.

<declarative_vs_procedural>
### Declarative Specification Over Procedural Algorithm

Express what must be true, not how to compute it. Describe the problem constraints and let the system find solutions.

**Declarative thinking:**
- State facts and rules
- Define relationships and constraints
- Specify valid solutions
- Let inference engine/solver find them

**When declarative specifications win:**
- Problem is easier to specify than to solve algorithmically
- Multiple solving strategies could work (system can choose/optimize)
- Specification itself is valuable documentation
- Constraints change more often than solving strategy

**When procedural algorithms win:**
- Algorithm is well-understood and efficient
- Declarative version doesn't provide insight
- Performance matters and declarative overhead isn't justified
- System can't efficiently solve the declarative formulation
</declarative_vs_procedural>

<bidirectionality>
### Bidirectionality as Design Opportunity

Relations can work in multiple computational directions. The same logical specification can answer different questions.

**Example:** `append(Xs, Ys, Zs)` defines relationship between three lists
- Forward: Given Xs and Ys, what is Zs?
- Backward: Given Zs, what are all ways to split into Xs and Ys?
- Checking: Does this (Xs, Ys, Zs) triple satisfy the relation?

**Design question:** Which computational directions are actually useful?

**Don't over-design:** Not all relations need to work in all directions. Design for modes you'll use. Document restrictions if they exist.
</bidirectionality>
</core_philosophy>

## Fundamental Principles

### Open vs Closed World Assumption

**Closed World Assumption (CWA):** What is not known to be true is false.
- Prolog, Datalog: If a fact isn't derivable, it's false
- Enables negation-as-failure
- Practical for databases and closed systems

**Open World Assumption (OWA):** Unknown is unknown, not false.
- OWL2, description logics: Absence of information means unknown
- Cannot conclude negatives from missing information
- Appropriate for incomplete knowledge (web, distributed systems)

**Design question:** What does absence of information mean in your domain?

### Monotonic vs Non-Monotonic Reasoning

**Monotonic:** Adding facts never invalidates previous conclusions.
- First-order logic, Datalog, OWL2
- Conclusions remain valid as knowledge grows
- Reasoning is sound and complete within the logic

**Non-monotonic:** New facts can retract previous conclusions.
- Prolog with negation-as-failure
- Answer Set Programming (stable model semantics)
- Default reasoning, exceptions
- More flexible but more complex semantics

**Design question:** Does your domain require defaults and exceptions?

### Declarative Semantics vs Operational Semantics

**Declarative semantics:** What the program means (logical interpretation)
- Independent of execution strategy
- Focus on correctness of specification
- Easier to reason about

**Operational/procedural semantics:** How the program executes
- Search strategy, evaluation order
- Performance characteristics
- Implementation-dependent

**Fully declarative systems:** Datalog, OWL2, Answer Set Programming separate logic from control
- Programmer specifies logic
- System chooses evaluation strategy
- Order doesn't affect meaning (only efficiency)

**Procedural systems:** Prolog, miniKanren require considering execution
- Clause order, goal order affect termination and efficiency
- Same logical meaning, different operational behavior
- Programmer must understand search strategy

**Staff insight:** Know whether your logic language is declarative or procedural. Declarative systems free you from execution concerns; procedural systems require understanding search behavior.

## When Logic Programming Works Well

**Problem characteristics that favor logic programming:**

**Constraint satisfaction and combinatorial search:**
- Problem defined by constraints on valid solutions
- Multiple solutions exist
- Search or optimization required
- Examples: Scheduling, puzzles, configuration, planning

**Knowledge representation and inference:**
- Rules and facts model domain knowledge
- Inference derives implicit information
- Querying relationships
- Examples: Expert systems, semantic web (OWL2), business rules

**Relational queries over structured data:**
- Data represents entities and relationships
- Queries involve joins, filtering, graph traversal
- Datalog for recursive queries
- Examples: Graph databases, dependency analysis, program analysis

**Symbolic computation and pattern matching:**
- Structural pattern matching
- Term rewriting
- Parsing and grammar-based processing
- Examples: Definite Clause Grammars, type inference

**When specification is more important than algorithm:**
- Domain experts can write/verify rules
- Requirements change frequently
- Correctness matters more than peak performance
- Declarative specification serves as executable documentation

## When Logic Programming Struggles

**Avoid logic programming when:**

**Clear procedural algorithm exists:**
- Well-understood, efficient algorithm
- Single computational direction
- Procedural version is simpler
- Examples: Sorting, hashing, standard algorithms

**Performance-critical numeric computation:**
- Arithmetic-heavy, tight loops
- Matrix operations, scientific computing
- Logic programming overhead not justified
- Examples: Graphics, signal processing, machine learning

**Stateful, imperative operations:**
- Mutable state, I/O, side effects
- Event-driven systems
- Imperative frameworks
- Examples: GUI programming, file systems, most I/O

**Large-scale data transformation:**
- ETL pipelines, data processing
- Streaming data
- Functional or SQL better suited
- Examples: Big data analytics, data warehousing

## Staff-Level Insights

<paradigm_selection>
### Understanding Different Logic Programming Paradigms

| Paradigm | Execution Model | Best For |
|----------|-----------------|----------|
| Prolog | Top-down, depth-first | Control matters, parsing, expert systems |
| Datalog | Bottom-up, set-oriented | Scalable queries, program analysis |
| OWL2/Description Logics | Tableau algorithms | Ontologies, semantic web, open-world |
| Answer Set Programming | Stable model semantics | Planning, configuration, non-monotonic |

<prolog_family>
**Prolog family (procedural logic programming):**
- Top-down, depth-first search with backtracking
- Programmer must consider search order, termination
- Cuts commit to choices, break declarative purity
- Requires understanding operational semantics
- Use for: Symbolic AI, parsing, expert systems where control matters
</prolog_family>

<datalog>
**Datalog (bottom-up logic programming):**
- Bottom-up evaluation, set-oriented
- Fully declarative (order-independent)
- Efficient for recursive queries over large datasets
- Terminates on finite data
- Use for: Database queries, program analysis, graph queries
</datalog>

<description_logics>
**Description Logics (OWL2, etc.):**
- Open world assumption
- Decidable fragments of first-order logic
- Focus on classification and subsumption
- Reasoning services (consistency, entailment)
- Use for: Ontologies, semantic web, knowledge graphs
</description_logics>

<answer_set_programming>
**Answer Set Programming (ASP):**
- Stable model semantics
- Non-monotonic reasoning (defaults, exceptions)
- Declarative problem solving
- Use for: Planning, configuration, complex constraint problems
</answer_set_programming>

**Staff insight:** Choose the right logic paradigm for your problem. Prolog when you need control, Datalog for scalable queries, OWL2 for open-world reasoning, ASP for non-monotonic domains.
</paradigm_selection>

### Designing for Bidirectionality

Not all modes of a relation work equally well. Some modes may not terminate, some may be inefficient.

**Design considerations:**
- Which computational directions are actually needed?
- Does the relation terminate in all intended modes?
- Are some modes inherently less efficient?
- Should mode restrictions be documented?

**Example:** List concatenation
- append(+List1, +List2, -Result): Efficient, deterministic
- append(-List1, -List2, +Result): Generates all splits, nondeterministic
- append(-X, -Y, -Z): Generates infinite triples (often not useful)

**Guideline:** Design for modes you need. Don't sacrifice clarity or efficiency for modes you'll never use.

### Negation and Its Complexities

**Negation-as-failure (closed world):**
- Prolog: `\+ Goal` succeeds if Goal fails
- Not true logical negation (lacks soundness)
- Depends on search order
- Can give unexpected results

**Classical negation (open world):**
- OWL2: Explicit negative assertions
- Sound but incomplete (unknown ≠ false)
- Cannot conclude negatives from absence

**Answer Set Programming:**
- Both classical negation and negation-as-failure
- Stable model semantics
- More expressive but more complex

**Staff insight:** Understand what negation means in your logic language. Closed-world negation is pragmatic but unsound; open-world negation is sound but incomplete.

### Constraint Logic Programming (CLP)

Extend logic programming with constraint domains for more efficient problem solving.

**Key domains:**
- CLP(FD): Finite domains (integers with constraints)
- CLP(R/Q): Real/rational arithmetic
- CHR: Constraint Handling Rules (custom constraint solvers)

**When CLP matters:**
- Constraint satisfaction problems
- Optimization (minimize/maximize objectives)
- Complex domain constraints
- Search is too slow without constraint propagation

**Staff insight:** CLP moves constraint solving from search (generate-and-test) to propagation (constraint narrowing). For constraint-heavy problems, this is orders of magnitude faster.

### The Purity vs Efficiency Trade-off

Pure logic programming separates logic from control. Pragmatic systems offer control features for efficiency.

**Purity sacrifices:**
- Control features (cuts in Prolog, goal ordering)
- Procedural predicates (assert/retract)
- Extra-logical features (I/O, arithmetic evaluation)
- Mode-specific optimizations

**When to sacrifice purity:**
- Performance bottlenecks identified through profiling
- Deterministic code paths where backtracking wastes work
- Integration with imperative systems (I/O, external calls)

**When to maintain purity:**
- Reusable, multi-mode relations
- Correctness is paramount
- Code clarity and maintainability
- Using fully declarative systems (Datalog, OWL2)

**Staff insight:** Start pure, add pragmatic features when profiling shows need. Measure before optimizing. Consider if performance problems indicate wrong paradigm choice.

## Execution Model Orientation (Brief)

Different logic languages have different execution models. Understanding these helps orient when working with a new system:

**Prolog-style (top-down, depth-first):**
- Depth-first search with backtracking
- Left-to-right goal selection
- Clause order and goal order matter
- Requires understanding search behavior
- Can diverge (infinite loops)

**Datalog-style (bottom-up, set-oriented):**
- Bottom-up evaluation (materialization)
- Order-independent
- Terminates on finite data
- Optimized for large datasets
- More restricted but more declarative

**OWL2/Description Logics:**
- Tableau algorithms, resolution
- Decidable reasoning (sound and complete for fragments)
- Open world assumption
- Classification and subsumption reasoning
- Optimized for ontological reasoning

**Answer Set Programming:**
- Stable model semantics
- Find models that satisfy constraints
- Non-monotonic (defaults, exceptions)
- Declarative problem encoding

**When learning a new logic language:** Identify its execution model to understand what you control vs what the system controls.

<common_mistakes_by_background>
## Common Mistakes from Imperative and Procedural Backgrounds

Programmers from procedural or object-oriented backgrounds often struggle with relational thinking:

<from_imperative_background>
**Writing procedural code in declarative language:**
- **Mistake:** Step-by-step instructions instead of logical constraints
- **Fix:** Describe what must be true, not how to compute it. Specify relations, not procedures

**Not thinking relationally:**
- **Mistake:** Functions that work one direction when bidirectional relations would work
- **Fix:** Ask: "What are all the ways this relationship could hold?" Design for useful modes

**Using assert/retract for state instead of relations:**
- **Mistake:** Mutating fact database like global variables
- **Fix:** Thread state through relations or use constraint solving. Assert/retract breaks declarativeness

**Not leveraging backtracking for search:**
- **Mistake:** Explicitly coding search and pruning
- **Fix:** Specify constraints, let backtracking search. Generate-and-test is a valid pattern

**Sequential thinking instead of declarative specification:**
- **Mistake:** Ordering goals as if they're sequential steps
- **Fix:** In fully declarative systems (Datalog, ASP), order doesn't matter. In Prolog, order affects efficiency not correctness

**Not using pattern matching effectively:**
- **Mistake:** Testing and extracting parts manually
- **Fix:** Pattern match in clause heads. Let unification do the work

**Writing deterministic predicates when nondeterminism would work:**
- **Mistake:** Forcing single-solution code when multiple solutions are natural
- **Fix:** Embrace nondeterminism. Backtracking generates solutions automatically
</from_imperative_background>

<from_oop_background>
**From Object-Oriented Backgrounds:**

**Trying to create class-like structures:**
- **Mistake:** Complex predicate bundles mimicking objects
- **Fix:** Relations are not methods. Data structures are terms, operations are relations over terms

**Thinking about methods instead of relations:**
- **Mistake:** `user.getName()` thinking instead of `userName(User, Name)` relations
- **Fix:** Relations connect entities. No owner, just participants

**Not leveraging unification:**
- **Mistake:** Explicit equality tests and variable assignment
- **Fix:** Unification happens automatically in clause heads and `=`. Use it
</from_oop_background>

<from_fp_background>
**From Functional Programming Backgrounds:**

**Forcing functional patterns when relations are clearer:**
- **Mistake:** map/filter/reduce when relational query is more direct
- **Fix:** If problem is naturally relational, use relations. Don't transform to functional style

**Not using search and constraint solving:**
- **Mistake:** Writing explicit search algorithms
- **Fix:** Specify constraints, use CLP or built-in search. Let solver handle combinatorics

**Thinking about transformations instead of relations:**
- **Mistake:** Pipeline thinking when bidirectional relations work
- **Fix:** Relations aren't functions. They describe what holds, not what transforms to what
</from_fp_background>
</common_mistakes_by_background>

<related_skills>
## Related Skills

- **software-engineer** — Core engineering philosophy and system design
- **swi-prolog-programmer** — SWI-Prolog-specific tooling, PlUnit testing, DCGs
- **functional-programmer** — When functional approaches are clearer (transformations, pipelines)
- **object-oriented-programmer** — When stateful entities need encapsulation
</related_skills>

<resources>
## Resources

**Documentation:**
- SWI-Prolog: https://www.swi-prolog.org/pldoc/
- W3C OWL2: https://www.w3.org/TR/owl2-overview/
- Clingo (ASP): https://potassco.org/clingo/

**For SWI-Prolog-specific guidance (testing, tooling, libraries), see the swi-prolog-programmer skill.**
</resources>

## Summary

Logic programming emphasizes:
- **Relational thinking** — When it clarifies problems vs when procedural is simpler
- **Declarative specification** — What must be true, not how to compute
- **Bidirectional computation** — Relations work in multiple modes (when useful)
- **Constraints over algorithms** — Let solver find solutions

Apply logic programming when problems are naturally relational, require constraint solving, benefit from declarative specification, or involve knowledge representation and inference. Use other paradigms when algorithms are deterministic, performance-critical, stateful, or when procedural thinking is clearer. Success comes from recognizing problem characteristics that match the paradigm's strengths.
