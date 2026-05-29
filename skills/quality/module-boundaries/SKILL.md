---
name: module-boundaries
description: Evaluates where module boundaries are drawn and whether modules should be merged or split. Use when deciding whether to combine or separate two specific modules, when two modules seem tightly coupled, or when a change to one module forces changes to another. Not for evaluating depth within a single module (use deep-modules) or quality of an abstraction layer (use abstraction-quality).
argument-hint: "[file or module path]"
metadata:
  allowed-tools: Read, Grep
---

# Module Boundaries Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file or module. Read the target code first, then apply the checks below.

Evaluate where module boundaries are drawn: are related things together and unrelated things apart?

## When to Apply

- Deciding whether to split a large class or merge small ones
- When two modules seem tightly coupled
- When a change to one module frequently requires changes to another
- When reviewing a decomposition decision

## Core Principles

### The Default Instinct Is Wrong

Most developers assume smaller is better, which produces systems full of shallow, pass-through components that increase cognitive load without hiding anything. The right answer is always whichever arrangement results in lower overall system complexity. Not smaller. Not more separated. Simpler.

### Merge Signals (Better Together)

- **They share information**: Same format, protocol, or data structure knowledge
- **They simplify each other**: Together, code is simpler than pieces apart
- **They always change together**: The boundary is fiction
- **One is incomplete without the other**: Callers must always use both
- **It eliminates duplication**: The same code appears in both places. Merging lets it exist once
- **It resolves pass-throughs**: A forwarding method adds a layer without adding an abstraction

Four costs of every split: more components to track, connective tissue to manage the boundary, separation of related code (producing unknown unknowns) and duplication.

### Split Signals (Better Apart)

- **Pieces are independent**: Can be understood and modified separately
- **Different knowledge domains**: No shared secrets
- **A clear, simple interface exists** at the boundary
- **Different rates of change**: One stable, one evolving
- **General-purpose from special-purpose**: Keep the general-purpose layer clean

### The Third Option

When combining doesn't simplify and separating doesn't either, look for the abstraction underneath both. Forcing a merge produces a module with two identities. Forcing a split produces conjoined modules. The relationship between the two things points at a concept that neither one is.

#### Discovery Process

1. **Name the shared concern**: What specific knowledge or capability do they share? Not "they're both used in X." Be precise.
2. **Ask what it looks like alone**: If you extracted just the shared concern, what would the type or interface be? Does it have a clean, simple API?
3. **Express the originals in terms of it**: Can each component be redefined as a use of the extracted concept?
4. **Verify simplification**: Does the new abstraction have a simple interface? Do the originals become simpler through it? Is duplicated knowledge now in one place? If not all three, the problem is elsewhere.

#### Recognizable situations

Two types sharing representation (extract a value type), two modules sharing a subroutine (extract a standalone utility, not a base class), two interfaces that overlap (factor out the shared surface), two workflows sharing a phase (extract the phase as an independent operation).

#### Validation

A genuine third option has its own identity (nameable without referencing either original), is simpler than either original, and is useful beyond the current context. If you can't name it precisely ("CommonStuff", "SharedUtils"), it's not a real abstraction.

### Conjoined Methods

Two methods are conjoined when you can't understand one without reading the other. This is a red flag that the split was wrong.

A 200-line method with a simple interface that reads top to bottom is deep and fine. Five 40-line methods that must be read together are shallow and worse. The test is never "is this method too long?" It is "can this method be understood independently?"

### Method Splitting

When splitting is warranted, the goal is for each resulting method to own a complete operation, not a fragment.

Two valid forms:

1. **Extract a subtask**: Factor out a child method that is general-purpose and independently understandable. The parent calls the child. Test: can someone read the child without knowing about the parent, and vice versa? If you find yourself flipping between them, the split was wrong.

2. **Divide into peer methods**: Split the original into two caller-visible methods, each with a simpler interface. Test: do most callers only need one of the new methods? If callers must invoke both, the split likely added complexity.

### Shared-Information Boundary Criterion

The most reliable criterion for drawing boundaries: which module is the authoritative owner of this piece of knowledge?

A well-placed boundary fully encloses a design decision. If two modules share knowledge about the same format or protocol, they belong together. If they happen to run one after the other but own unrelated knowledge, they belong apart. Execution order should never determine where a boundary goes.

## Review Process

1. **Map dependencies**: For each module pair, what knowledge do they share?
2. **Apply merge signals**: Should any modules be combined?
3. **Apply split signals**: Should any module be divided?
4. **Test for conjoined methods**: Can each be understood independently?
5. **Check boundary criterion**: Boundaries drawn around knowledge ownership?
6. **Recommend adjustments**: Specific merges, splits, or restructurings

Red flag signals for module boundaries are cataloged in **red-flags** (Conjoined Methods, Information Leakage, Shallow Module, Special-General Mixture).
