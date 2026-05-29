---
name: mfe-foundations
description: "Pure mathematical structure. Sets, groups, rings, fields, topology — the formal bedrock everything else rests on."
user-invocable: false
allowed-tools: Read Grep Glob
metadata:
  extensions:
    gsd-skill-creator:
      version: 1
      createdAt: "2026-02-26"
      triggers:
        intents:
          - "set"
          - "logic"
          - "proof"
          - "group"
          - "ring"
          - "field"
          - "topology"
          - "axiom"
          - "formal"
          - "abstract"
        contexts:
          - "mathematical problem solving"
          - "math reasoning"
---

# Foundations

## Summary

**Foundations** (Part VI: Defining)
Chapters: 18, 19, 20, 21
Plane Position: (-0.6, 0.6) radius 0.35
Primitives: 55

Pure mathematical structure. Sets, groups, rings, fields, topology — the formal bedrock everything else rests on.

**Key Concepts:** Set Definition (ZFC), Topological Space, Group Definition and Axioms, Propositional Logic (Boolean Operations), Predicate Logic (Quantifiers)

## Key Primitives



**Set Definition (ZFC)** (axiom): A set is a well-defined collection of distinct objects (elements). Membership is denoted x in S. Two sets are equal iff they have exactly the same elements (Axiom of Extensionality). Sets are the foundational objects of mathematics under ZFC.
  - Define a collection of mathematical objects
  - Establish the foundational objects for building mathematical structures
  - Work with membership, inclusion, and equality of collections

**Topological Space** (axiom): A topological space (X, tau) is a set X with a collection tau of subsets (called open sets) satisfying: (1) emptyset and X are in tau. (2) Any union of sets in tau is in tau. (3) Any finite intersection of sets in tau is in tau.
  - Define the concept of 'nearness' or 'openness' without a metric
  - Study properties preserved under continuous deformation
  - Generalize analysis to abstract settings

**Group Definition and Axioms** (axiom): A group (G, *) is a set G with a binary operation * satisfying: (1) Closure: a*b in G for all a,b in G. (2) Associativity: (a*b)*c = a*(b*c). (3) Identity: exists e in G such that e*a = a*e = a. (4) Inverses: for each a, exists a^{-1} with a*a^{-1} = a^{-1}*a = e.
  - Verify if a set with an operation forms a group
  - Identify symmetries of objects as group elements
  - Study algebraic structures with a single binary operation

**Propositional Logic (Boolean Operations)** (definition): Propositional logic deals with propositions (true/false statements) combined by logical connectives: AND (conjunction, p ^ q), OR (disjunction, p v q), NOT (negation, ~p), IMPLIES (conditional, p -> q), IFF (biconditional, p <-> q).
  - Combine simple statements into complex logical expressions
  - Determine the truth value of a compound proposition
  - Formalize arguments and reasoning

**Predicate Logic (Quantifiers)** (definition): Predicate logic extends propositional logic with variables, predicates P(x), and quantifiers: universal (forall x, P(x)) meaning P holds for all x, and existential (exists x, P(x)) meaning P holds for some x. Negation: ~(forall x, P(x)) iff (exists x, ~P(x)).
  - Express mathematical statements involving 'for all' or 'there exists'
  - Negate quantified statements correctly
  - Formalize mathematical definitions and theorems

**Homomorphism** (definition): A group homomorphism f: G -> H is a function satisfying f(a *_G b) = f(a) *_H f(b) for all a, b in G. It preserves the group operation. The kernel ker(f) = {a in G : f(a) = e_H} is a normal subgroup of G. The image im(f) is a subgroup of H.
  - Define a structure-preserving map between groups
  - Identify the kernel and image of a group map
  - Classify groups up to homomorphic relationships

**Open Set and Closed Set** (definition): In a topological space (X, tau), a set U is open if U in tau. A set C is closed if X \ C is open. The closure cl(A) is the smallest closed set containing A. The interior int(A) is the largest open set contained in A. A set can be both open and closed (clopen).
  - Determine if a set is open, closed, or neither in a given topology
  - Compute the closure, interior, and boundary of a set
  - Work with topological properties defined via open/closed sets

**Cartesian Product** (definition): The Cartesian product of A and B is A x B = {(a,b) : a in A, b in B}. For n sets: A_1 x ... x A_n = {(a_1,...,a_n) : a_i in A_i}. |A x B| = |A| * |B|. R^n = R x R x ... x R (n times).
  - Form all possible pairs from two sets
  - Construct the domain for relations and functions
  - Build multi-dimensional spaces from one-dimensional sets

**Relation** (definition): A relation R from A to B is a subset of A x B. We write aRb or (a,b) in R. Properties: reflexive (aRa), symmetric (aRb => bRa), antisymmetric (aRb and bRa => a=b), transitive (aRb and bRc => aRc).
  - Define a relationship between elements of two sets
  - Check if a relation has special properties (reflexive, symmetric, transitive)
  - Formalize order, equivalence, or other structural relationships

**Equivalence Relation** (definition): An equivalence relation ~ on set A is a relation that is reflexive (a ~ a), symmetric (a ~ b => b ~ a), and transitive (a ~ b and b ~ c => a ~ c). It partitions A into disjoint equivalence classes [a] = {x in A : x ~ a}.
  - Classify elements into groups where they are considered equivalent
  - Partition a set into disjoint equivalence classes
  - Define modular arithmetic or congruence relations

## Composition Patterns

- Set Definition (ZFC) + foundations-propositional-logic -> Set builder notation: {x in S : P(x)} uses logical predicates to define sets (parallel)
- Empty Set + foundations-set-definition -> Basis for inductive set construction: {}, {{}}, {{},{{}}}, ... (sequential)
- Set Union + foundations-set-intersection -> Boolean algebra of sets: union and intersection with complement form a complete Boolean algebra (parallel)
- Set Intersection + foundations-set-union -> Set algebra with distributive laws: A inter (B union C) = (A inter B) union (A inter C) (parallel)
- Set Complement + foundations-set-union -> De Morgan's laws for sets: (A union B)^c = A^c inter B^c and (A inter B)^c = A^c union B^c (parallel)
- Cartesian Product + foundations-relation -> Relations as subsets of Cartesian products: R subset A x B (sequential)
- Power Set + foundations-cardinality -> Cantor's theorem: |P(A)| > |A| for any set A, proving no largest cardinal (sequential)
- Relation + foundations-set-definition -> Relations as structured subsets of Cartesian products, enabling order theory (sequential)
- Equivalence Relation + foundations-group-definition -> Quotient group: G/N uses equivalence classes (cosets) as group elements (sequential)
- Equivalence Class / Partition Theorem + foundations-equivalence-relation -> Bijection between equivalence relations on A and partitions of A (parallel)

## Cross-Domain Links

- **structure**: Compatible domain for composition and cross-referencing
- **reality**: Compatible domain for composition and cross-referencing
- **mapping**: Compatible domain for composition and cross-referencing
- **unification**: Compatible domain for composition and cross-referencing
- **synthesis**: Compatible domain for composition and cross-referencing

## Activation Patterns

- set
- logic
- proof
- group
- ring
- field
- topology
- axiom
- formal
- abstract
