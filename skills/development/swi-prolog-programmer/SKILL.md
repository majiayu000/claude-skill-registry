---
name: swi-prolog-programmer
description: SWI-Prolog-specific tooling, standards, and idioms. Use when working with SWI-Prolog code. Emphasizes relational thinking, steadfastness, DCGs, constraints, and mandatory testing with PlUnit.
---

# SWI-Prolog Programmer

Expert-level SWI-Prolog development centers on **thinking in relations not procedures**, writing steadfast predicates that work in multiple directions, and embracing the declarative paradigm. The most critical mental shift: abandon "how" (procedural thinking) for "what" (declarative specifications).

**Related skills:**
- `logic-programmer` - Logic programming fundamentals (relations, unification, search)
- `software-engineer` - System design principles and architecture
- `test-driven-development` - Testing philosophy (PlUnit section below covers SWI-specific practices)

<logic_programming_fundamentals>
**Core logic programming principles:**
- **Relations, not functions**: Predicates describe relationships that can work in multiple directions
- **Unification**: Two-way pattern matching that binds variables—not one-way assignment
- **Backtracking**: Systematic search through solution space—the "time machine" for exploring alternatives
- **Declarative reading**: Read `p(X, Y) :- q(X), r(Y)` as "X is related to Y when q(X) holds and r(Y) holds"
</logic_programming_fundamentals>

This skill focuses on SWI-Prolog-specific tools, idioms, and practices that distinguish veteran developers from beginners.

## Version Targeting: Development Track Recommended

**Target version**: Latest development release (9.3.x series as of November 2025)
**Current stable**: 9.2.9.1 (April 2025)
**Current development**: 9.3.34 (November 2025)

**Aggressive adoption philosophy**: Most developers should use development releases even for production. The development track is released every 2-4 weeks, typically robust, provides latest features, and issues are resolved quickly. The stable track (even minor versions) only receives critical patches and is intended for conservative deployments requiring predictable installations.

SWI-Prolog tries to minimize breaking changes and stay close to the ISO standard. From the SWI-Prolog documentation:[^1] "We try to make as few as possible changes that break backward compatibility..."

[^1]: Jan Wielemaker. SWI-Prolog: Directions. https://www.swi-prolog.org/Directions.html

**Version history reference**: https://www.swi-prolog.org/ChangeLog

### Respecting Third-Party Codebases

When contributing to existing Prolog projects or open-source:
- Respect existing coding style and conventions
- Don't introduce modern features to projects targeting older versions
- Follow the project's pack dependencies and version constraints
- Propose improvements through proper channels (issues, governance)
- "You're a guest—respect the house rules"

The aggressive adoption philosophy applies ONLY to codebases you own.

## The Philosophical Foundation: Logic First, Procedure Second

<core_philosophy>
SWI-Prolog's design philosophy prioritizes **knowledge-intensive interactive systems** where logical correctness and development experience trump raw performance. As Jan Wielemaker (creator, 35+ years experience) explains: "My primary motivation has always been to build stuff that works rather than stuff that allows writing an academic paper."

The critical insight: **Backtracking provides a time machine** for exploring computation paths. Any use of the dynamic database (assert/retract) breaks this superpower. The database is explicitly documented as **"a non-logical extension to Prolog"** that "destroys all these nice goodies" of logical search.

Veteran developers avoid assert/retract except when information must genuinely survive backtracking, which is rare. Instead: thread state through arguments.
</core_philosophy>

### When to Choose SWI-Prolog

Use SWI-Prolog when the problem involves:
- Relational data querying (tabular and graph-shaped data)
- Recursive structures (trees, nested data)
- Search with backtracking
- Constraint satisfaction problems
- Symbolic manipulation and term rewriting
- CPU-intensive server tasks with large shared datasets
- Soft real-time behavior with concurrent access
- Live programming (hot-patching without restart)

**Don't choose Prolog for**:
- Pure number crunching (use NumPy, Julia, Fortran)
- High-frequency trading latency requirements
- Problems where machine learning models excel
- Frontend user interfaces (though web backends work well)

The 2010 "Prolog Story" by Kyle Cordes documents a 90% cost reduction on a complex scheduling system—not from coding faster, but from **thinking more clearly**. The declarative approach forced better problem understanding.

## Relational Thinking: The Core Mental Shift

The fundamental shift from imperative programming: **think in terms of two variables instead of one**. You cannot write `i = i + 1` in Prolog because no value equals itself plus one. Instead: `I #= I0 + 1` describes the **relation** between two different variables I0 and I.

As Markus Triska emphasizes: "The same variable cannot reflect two different states, old and new, at the same time."

### Reading Code Declaratively

**Procedural reading** (wrong): "To find X such that Y holds, do the following steps..."

**Declarative reading** (correct): "X is related to Y when the following conditions hold..."

For `insert(Key, Tree, NewTree)`, read it as: "insert/3 shows how a key is related to a tree with and a tree without that key." The predicate describes a relationship, not a procedure.

### The Power of Multidirectionality

Everything is a relation, so programs work in multiple directions. `append/3` with one definition provides four methods:

```prolog
?- append([1,2], [3,4], ZS).     % List construction
ZS = [1,2,3,4].

?- append([1,2], YS, [1,2,3,4]). % List subtraction
YS = [3,4].

?- append(XS, YS, [1,2,3,4]).    % Generate all partitions
XS = [], YS = [1,2,3,4] ;
XS = [1], YS = [2,3,4] ;
XS = [1,2], YS = [3,4] ;
XS = [1,2,3], YS = [4] ;
XS = [1,2,3,4], YS = [].

?- append(XS, YS, ZS).           % Most general query
```

Four methods for the price of one! Write predicates that work bidirectionally when possible.

## Steadfastness: The Non-Negotiable Requirement

<steadfastness>
**"Any decent predicate must be 'steadfast'"** (Richard O'Keefe via Covington)—it must work correctly if output variables are already instantiated. This is the cornerstone of relational programming.

```prolog
% If this succeeds:
?- foo(X), X = x.

% Then this must succeed:
?- foo(x).

% And vice versa - if foo(x) succeeds, then foo(X), X = x must succeed.
```

Predicates that fail this test are broken by definition. Test steadfastness by:
1. Running queries with output variables unbound
2. Running same queries with outputs bound to expected values
3. Both must succeed under exactly the same conditions

**Example of non-steadfast code** (broken):

```prolog
% BAD: Only works when Max is unbound
get_max(X, Y, Max) :- X >= Y, Max = X.
get_max(X, Y, Max) :- X < Y, Max = Y.

?- get_max(3, 5, M).  % Works
M = 5.

?- get_max(3, 5, 5).  % Should succeed but fails!
false.
```

**Steadfast version**:

```prolog
% GOOD: Works regardless of Max instantiation
max_value(X, Y, X) :- X >= Y.
max_value(X, Y, Y) :- X < Y, Y > X.
```
</steadfastness>

## Using Constraints Declaratively: CLP(FD)

<clpfd>

The official SWI-Prolog CLP(FD) documentation[^2] states: "If you are used to the complicated operational considerations that low-level arithmetic primitives necessitate, then moving to CLP(FD) constraints may, due to their power and convenience, at first feel to you excessive and almost like cheating. It isn't."

[^2]: Markus Triska. CLP(FD): Constraint Logic Programming over Finite Domains. SWI-Prolog. https://www.swi-prolog.org/pldoc/man?section=clpfd

Constraints are integral to modern Prolog and designed to eliminate low-level primitives. When teaching Prolog, **CLP(FD) constraints should be introduced before explaining low-level arithmetic** because they're easier to explain and use.

### Use #=/2 Instead of is/2 and =:=/2

**The most important arithmetic constraint is #=/2**, which subsumes both `is/2` and `=:=/2` over integers. Benefits:
- Work in all directions (multidirectional)
- Declarative semantics (no execution order dependency)
- Integrate with search (backtracking finds solutions)
- Constraint propagation reduces search space

```prolog
% Not idiomatic (low-level, directional)
?- X is 5 + 3.
X = 8.

?- 8 is Y + 3.  % Error! Can't work backwards
ERROR: is/2: Arguments are not sufficiently instantiated

% Idiomatic (declarative, multidirectional)
?- X #= 5 + 3.
X = 8.

?- 8 #= Y + 3.    % Works backwards!
Y = 5.

?- Z #= A + B, Z #= 8, A #= 5.  % Propagates constraints
Z = 8, A = 5, B = 3.
```

### The Constraint Programming Pattern

Standard approach for combinatorial problems:

1. **Declare variables and domains**
2. **Post constraints**
3. **Label variables for solutions**

```prolog
solve(Vars) :-
    Vars = [X, Y, Z],
    Vars ins 1..10,              % Domain declaration
    X + Y #= Z,                  % Constraints
    X #< Y,
    label(Vars).                 % Search for solutions
```

Constraint propagation happens automatically. Use built-in constraints:
- `all_different/1` - All variables must take different values
- `sum/3` - Sum of list equals value
- `scalar_product/4` - Dot product constraints
- `element/3` - Indexing constraints
- `cumulative/2` - Resource scheduling

This is **the preferred approach** for:
- Combinatorial optimization (scheduling, assignment)
- Puzzles (Sudoku, N-Queens, graph coloring)
- Resource allocation
- Timetabling
</clpfd>

## DCGs as Fundamental Design Abstraction

<dcg_patterns>

DCGs (Definite Clause Grammars) are **not just for parsing**—they're a general-purpose mechanism for threading state through computations. As Markus Triska states: "In every serious Prolog program, you will find many opportunities to use DCGs."

Veterans recognize DCGs as similar to monads in functional programming, providing automatic threading of two hidden arguments through all rules.

### When to Use DCGs: The Decision Framework

Use DCGs when:
1. **Describing any list** (parsing, generation, transformation)
2. **Reading from files** (with library(pio) for lazy I/O)
3. **Passing around state** that only a few predicates need to access or modify

The third case is critical for design—DCGs excel at implicit state threading when state flows through computation but only certain predicates need it.

**Pattern recognition heuristic**: When you see predicates passing through arguments like `pred(..., N0, N1)` where intermediate values N1, N2, N3 are only being threaded through without direct modification, **consider DCGs**. This is the accumulator pattern signaling a DCG opportunity.

### State Threading with Semicontext Notation

The key idiom for explicit state access:

```prolog
state(S), [S] --> [S].        % Read current state
state(S0, S), [S] --> [S0].   % Update state from S0 to S
```

Example: counting tree leaves without explicit threading:

```prolog
num_leaves(Tree, N) :-
    phrase(num_leaves_(Tree), [0], [N]).

num_leaves_(nil), [N] --> [N0], { N #= N0 + 1 }.
num_leaves_(node(_,Left,Right)) -->
    num_leaves_(Left),
    num_leaves_(Right).
```

Notice the second rule makes **no reference to state**—DCGs thread it implicitly. This is the power of the abstraction.

### DCG Design Patterns Beyond Parsing

**Tree to list conversion**:

```prolog
tree_nodes(nil) --> [].
tree_nodes(node(Name, Left, Right)) -->
    tree_nodes(Left),
    [Name],
    tree_nodes(Right).
```

**Pipeline pattern** for transformations:

```prolog
steps --> square, half, round.

square, [Y] --> [X], { Y is X * X }.
half, [Y] --> [X], { Y is X / 2 }.
round, [Y] --> [X], { Y is round(X) }.

convert(Float, Integer) :-
    phrase(steps, [Float], [Integer]).
```

**Lazy list processing** with library(pio):

```prolog
:- use_module(library(pio)).

process_file(Result) :-
    phrase_from_file(my_dcg(Result), 'large_file.txt').
```

File contents loaded lazily; unused portions can be garbage collected.

### Critical Abstraction Principle

**From Paulo Moura (Logtalk creator)**: "DCGs provide a threading state abstraction: don't break it." Always use `phrase/2` or `phrase/3` to invoke DCGs. Never call DCG-compiled predicates directly—this breaks abstraction and ties code to implementation details.
</dcg_patterns>

## Code Style That Signals Expertise

<code_style>

The authoritative "Coding Guidelines for Prolog" (Covington et al., 2011, Theory and Practice of Logic Programming) states: "As far as we know, a coherent and reasonably complete set of coding guidelines for Prolog has never been published." This 39-page paper remains **the definitive reference**.

Reference: https://www.covingtoninnovations.com/mc/plcoding.pdf

### Naming Conventions Are Mandatory

**Predicate names**: Use `underscore_style`, never camelCase. Rationale: "Underscores resemble spaces...an important readability tool that is a thousand years old."

- Relations/properties: nouns or adjectives (`sorted_list/1`, `well_formed/1`, `in_tree/2`)
- Procedural predicates: imperative verb phrases (`remove_duplicates/2`, `print_contents/1`)
- NOT "removes_duplicates" (gerund form is wrong)

**Argument order**: "Inputs before outputs" with the Space-Is-Time principle—if X is needed before Y temporally, place X before Y spatially. This aligns with first-argument indexing optimization.

Choose predicate names showing argument order: `mother_child/2` not `mother_of/2` (which is ambiguous).

**Variable names**: Use descriptive names like `ResultsSoFar` or `Results_so_far`. Single letters only with established conventions:
- I/J/K/M/N for integers
- L/L1/L2 for lists
- H/T for head/tail
- X/Y/Z for arbitrary terms

For threaded state: `State0, State1, State2, ..., State` (final) or `State_in, State_tmp, State_tmp1, ..., State_out`.

### Code Layout and Documentation Standards

**Indentation**: 4 spaces (Covington) or 3 spaces (Lifeware/INRIA). **Never tabs**—"You cannot normally predict how tabs will be set." Maximum 80 columns.

Each subgoal on separate line except very short I/O sequences. First line has head and `:-` only:

```prolog
predicate_name(Arg1, Arg2, Result) :-
    goal1(Arg1, Intermediate),
    goal2(Arg2, Intermediate, Result).
```

**Vertical spacing**:
- 1 blank line between clauses of same predicate
- 2 blank lines between different predicates
- Maximum 24-48 lines per clause (should fit on screen)

### PlDoc Documentation Template

Every public predicate must have PlDoc structured comments:

```prolog
%! predicate_name(+Input:type, -Output:type) is det.
%
% Description using **Markdown** formatting.
% Multiple lines explaining behavior.
%
% @arg Input   Description of input argument
% @arg Output  Description of output argument
% @throws error_type When this condition occurs
%
% Example:
% ==
% ?- predicate_name(input, Output).
% Output = result.
% ==

predicate_name(Input, Output) :-
    implementation.
```

**Mode indicators** (Covington system):
- `+` for nonvar input (must be instantiated)
- `-` for var output (will be instantiated)
- `?` for either direction
- `@` for not further instantiated
- `*` for ground on entry
- `!` for mutable structure

**Determinism indicators**:
- `det` - exactly once (deterministic)
- `semidet` - at most once (may fail, no choice points)
- `multi` - at least once (always succeeds, may have choice points)
- `nondet` - any number of times (may fail, may have choice points)
</code_style>

## The Cut: Green Versus Red

<cut_usage>

**Green cut**: Only prunes computation paths not contributing new solutions, doesn't change declarative meaning, safe to add or remove.

```prolog
max(X, Y, X) :- X >= Y, !.
max(X, Y, Y) :- X < Y.
```

The cut is green because the test in the first clause guarantees the second won't succeed if the first does.

**Red cut**: Changes declarative meaning and program behavior.

```prolog
% BAD: Red cut with major flaw
rc_minimum(X, Y, X) :- X =< Y, !.
rc_minimum(_, Y, Y).

?- rc_minimum(1, 2, 2).  % Succeeds incorrectly!
true.
```

**Guidelines**:
- First think through how to do the computation without a cut
- Then add cuts only to save work
- **Never add a cut to correct an unknown problem**—the cut may be far from the actual error
- Make red cuts obvious by placing them on their own line
- Use cuts sparingly but precisely
</cut_usage>

## Mandatory Tooling and Workflow

<tooling>

### make/0: The Core Development Tool

**make/0 is THE essential workflow tool**. It checks timestamps, reloads only changed files, updates autoload indices, and preserves module context.

The edit-reload-test cycle:

```prolog
?- edit(predicate).       % Edit in configured editor
% [Make changes, save]
?- make.                  % Reload (auto-runs tests if configured)
?- test_predicate.        % Manual testing
```

Configure tests to run automatically:

```prolog
:- set_test_options([run(make)]).
```

Now every `make.` invocation runs the test suite.

### PlUnit Testing Is Mandatory

Quote from documentation: **"There is really no excuse not to write tests! Unit testing is less about testing than about proper and manageable coding—it's like having a lab notebook."**

Tests document expected usage, validate implementation claims, and prevent regressions.

**Basic test structure**:

```prolog
:- begin_tests(mymodule).

test(simple_case) :-
    mymodule:predicate(input, expected).

test(with_verification, [true(X == 42)]) :-
    mymodule:compute(X).

test(should_fail, [fail]) :-
    mymodule:invalid_input(bad).

test(expecting_error, [error(type_error(_, _))]) :-
    mymodule:predicate(wrong_type).

test(with_setup, [
    setup(create_temp_file(File)),
    cleanup(delete_file(File))
]) :-
    mymodule:process_file(File).

test(all_solutions, [all(X == [1,2,3])]) :-
    mymodule:generate(X).

test(nondet_expected, [nondet]) :-
    mymodule:generate_multiple(_).

:- end_tests(mymodule).
```

**Test organization**:
- Use `.plt` extension for test files matching `.pl` source files
- Or place tests in `test/` directory
- Run with `swipl -g run_tests -t halt file.pl` or `?- run_tests.` from REPL

**Logic programming testing philosophy**:
- Test determinism (PlUnit warns on unexpected choice points)
- Test all solutions not just first (`all(X == List)`)
- Test multiple modes of predicates
- Verify reversibility (bidirectionality)

Tests document logical relationships more than execution order.

### check/0 Before Every Commit

Run `check.` before every commit. This comprehensive check finds:
- Undefined predicates
- Void declarations (declared but not defined)
- Trivial fails (predicates that always fail)
- Module issues
- Syntax errors

Individual checks:
- `list_undefined.` - undefined predicates
- `list_void_declarations.` - declared but not defined
- `list_trivial_fails.` - always-failing predicates

Graphical cross-referencer: `gxref.` for visual dependency analysis.

**Style checks** (enable during development):

```prolog
?- style_check(+singleton).      % Warn on singleton variables
?- style_check(+discontiguous).  % Warn on non-contiguous clauses
?- style_check(+no_effect).      % Warn on ineffective code
```

### Debugging with Graphical Tracer

**Use gtrace, not trace**: The graphical debugger is far superior to command-line.

```prolog
?- gtrace.               % Enable graphical tracing
?- gspy(pred/N).         % Set spy point on predicate
```

Three-panel view shows source code, variables, and stack. Color-coded execution:
- Green = call (entering predicate)
- Red = fail (exhausted alternatives)
- Yellow = redo (backtracking for alternatives)
- Purple = exception

Supports hot-fixing (edit during debug), visualizes choice points, and provides source-level debugging.

**Four-port model**: Call → Exit (success) / Fail (failure) / Redo (backtrack)

Key commands: Space=step, s=skip, f=fail, r=retry, a=abort, b=break to REPL, e=edit source

**Alternative: debug/3 library** for instrumentation without tracing:

```prolog
:- use_module(library(debug)).
?- debug(topic).
debug(algorithm, 'Processing: ~w', [Data]).
```

Zero overhead when disabled, fine-grained control by topic.

### Editor Integration

**VSCode**: Use "VSC-Prolog" or "New-VSC-Prolog" extensions. Features:
- Semantic syntax highlighting
- Hover documentation from SWI-Prolog docs
- Integrated debugger visualizing command-line tracer
- Code navigation (go-to-definition, find-references)
- Formatting support

**Emacs (recommended for serious development)**: Use **Sweep** (official, embeds SWI-Prolog as Emacs module).

Install from NonGNU ELPA:

```elisp
(package-install 'sweeprolog)
```

Requires SWI-Prolog 8.5.18+ and Emacs 27+. Provides:
- Semantic highlighting with real-time cross-referencing
- Context-aware completion
- Inline documentation
- Query execution from buffers
- Automatic indentation inference

Alternative: lsp-mode + lsp_server pack for Language Server Protocol support.
</tooling>

## Project Structure for Maintainable Systems

<project_structure>

Standard directory structure for larger projects:

```
myproject/
├── load.pl           # Main loader with environment setup
├── run.pl            # Application starter
├── save.pl           # Creates saved states
├── debug.pl          # Debugging configuration
├── prolog/           # Source code
│   ├── main.pl
│   ├── module1.pl
│   └── myproject/    # Private/helper modules
│       └── internal.pl
├── test/             # Unit tests
│   ├── test_module1.plt
│   └── test_module2.plt
├── examples/         # Usage examples
├── pack.pl          # Pack metadata if distributing
├── README.md
└── LICENSE
```

**Key organizational files**:
- `load.pl` - Sets up environment (Prolog flags, file search paths) and loads sources
- `run.pl` - Starts application by loading `load.pl` in silent mode and calling startup predicates
- `save.pl` - Creates saved states with `qsave_program/2`
- `debug.pl` - Sets up debugging environment

### Module System Best Practices

Every `.pl` file should be a module. Module name must match filename: `my_module.pl` contains `:- module(my_module, [...]).`

Export list includes only public predicates. Private modules go in subdirectories named after the pack.

```prolog
:- module(module_name, [
    exported_predicate/2,
    another_export/1,
    op(700, xfx, custom_op)
]).

%! exported_predicate(+Input, -Output) is det.
%  Documentation using PlDoc syntax
exported_predicate(Input, Output) :-
    helper_predicate(Input, Output).

% Private helper - not exported
helper_predicate(X, Y) :- Y is X * 2.
```

Set up project-specific file search paths:

```prolog
:- prolog_load_context(directory, Dir),
   asserta(user:file_search_path(myapp, Dir)).

user:file_search_path(graph, myapp(graph)).
user:file_search_path(ui, myapp(ui)).

:- use_module(graph(algorithms)).
:- use_module(ui(main_window)).
```
</project_structure>

## Essential Libraries Veterans Use Daily

<essential_libraries>

**Mandatory** (in order of importance):

- **library(lists)**: `member/2`, `append/3`, `length/2`, `reverse/2`, `nth0/3`, `sort/2`, `sum_list/2`
- **library(apply)**: `maplist/2-5`, `foldl/4-6`, `include/3`, `exclude/3`, `partition/4` (higher-order operations)
- **library(dcg/basics)**: `whites//0`, `string//1`, `number//1`, `integer//1`, `digits//1` (DCG utilities)
- **library(error)**: `must_be/2`, `is_of_type/2`, error constructors for proper error handling
- **library(plunit)**: Testing framework (non-optional for professional work)

**Highly recommended**:

- **library(clpfd)**: Constraints over finite domains (`#=/2`, `ins/2`, `label/1`, `all_different/1`)
- **library(assoc)**: Balanced binary trees for O(log N) dictionaries
- **library(aggregate)**: `aggregate/3-4`, `aggregate_all/3-4` for aggregation operations
- **library(option)**: `option/2-3`, `select_option/3-4`, `merge_options/3` for option list handling
- **library(debug)**: `debug/3`, `assertion/1` for instrumentation
- **library(yall)**: Lambda expressions (`[X,Y]>>Body`) for inline goals

**Specialized but important**:
- **library(http/*)**: Web server and client
- **library(semweb/*)**: RDF and semantic web
- **library(thread)**: Concurrency
- **library(persistency)**: Persistent predicates
</essential_libraries>

## Common Mistakes from Other Paradigms

<common_mistakes>

<from_imperative>
### From Imperative Programming (C, Java, Python)

**Trying to modify state destructively**:

```prolog
% WRONG: Trying to treat variables like imperative memory
X = 5,
X = X + 1.  % ERROR: Can't unify 5 with 6!

% RIGHT: Use different variables for different states
X0 = 5,
X1 is X0 + 1.  % Or: X1 #= X0 + 1
```

**Using assert/retract for intermediate results**:

```prolog
% WRONG: Using database for computation state
compute(Input, Result) :-
    retractall(temp(_)),
    assert(temp(Input)),
    process,
    temp(Result).

% RIGHT: Thread state through arguments
compute(Input, Result) :-
    process(Input, Result).
```

**Over-reliance on execution order**:

```prolog
% WRONG: Assuming left-to-right evaluation matters for correctness
pred(X, Y) :-
    compute_y(Y),    % Assumes Y needed first
    validate_x(X).

% RIGHT: Write predicates that work regardless of goal order
pred(X, Y) :-
    validate_x(X),
    compute_y(Y).
% Both orders should produce same logical result
```

**Fighting with the language**: Having a war with Prolog usually indicates procedural thinking hasn't been abandoned. Embrace relational thinking.
</from_imperative>

<from_functional>
### From Functional Programming (Haskell, ML, Clojure)

**Expecting pattern matching to work one-way**:

```prolog
% Prolog uses unification (bidirectional), not pattern matching (one-way)
% This works in multiple directions:
?- append([1,2], [3,4], Xs).  % Forward
?- append([1,2], Ys, [1,2,3,4]).  % Backward
?- append(As, Bs, [1,2,3,4]).  % Generate all splits
```

**Missing that variables can be uninstantiated**:

In Haskell, all variables are bound. In Prolog, variables can remain unbound and represent constraints:

```prolog
?- X #> 5, X #< 10.
X in 6..9.  % X is constrained but not bound to specific value
```

**Trying to use guards that don't exist**:

Prolog doesn't have guards like Haskell. Use goals in body instead:

```prolog
% Not valid Prolog syntax (Haskell-style guards)
% max(X, Y, X) | X >= Y.

% Correct Prolog
max(X, Y, X) :- X >= Y.
max(X, Y, Y) :- X < Y, Y > X.
```
</from_functional>

<from_oop>
### From Object-Oriented Programming (Java, C++)

**Creating unnecessary getter/setter predicates**:

```prolog
% WRONG: Java-style getters/setters
get_name(person(Name, _), Name).
set_name(person(_, Age), Name, person(Name, Age)).

% RIGHT: Direct unification
?- Person = person(Name, Age).
% Access fields by unification, not getters
```

**Blindly using `is_` prefix for everything**:

From Covington: "Do not blindly import styles from other languages. For instance, do not blindly follow the Java tradition by calling everything in sight is_xxx or get_yyy."

Use appropriate Prolog naming:
- Properties/relations: `sorted/1`, `member/2`, `connected/2`
- Not: `is_sorted/1`, `is_member/2`, `is_connected/2`

**Importing Java naming conventions**:

```prolog
% WRONG: camelCase (Java style)
myPredicate(inputValue, outputResult).

% RIGHT: underscore_style (Prolog convention)
my_predicate(input_value, output_result).
```
</from_oop>
</common_mistakes>

## Anti-Patterns That Mark Amateur Code

<anti_patterns>

Red flags that code is written by someone fighting the language:

**Using assert/retract for intermediate results**: Breaks backtracking's time-machine debugging and is usually slow. Pass state through arguments instead.

**Cut at end of last clause**: `pred(X) :- goal1, goal2, !.` on the final clause—what alternatives is it eliminating? Almost always wrong.

**Procedural variable reuse**: Trying to write `X = 5, X = 6` expecting X to "change." Use different variables: `X = 5, Y = 6`.

**Directional code that only works one way**: Not writing steadfast predicates. `get_max(X, Y, Max)` that fails if Max is already bound is broken.

**Over-use of cuts and guards**: Trying to write imperative control flow. Prolog is not C with weird syntax.

**Using `is/2` instead of `#=/2` for integer arithmetic**: Low-level arithmetic is directional, constraints are relational and propagate.

**Not using higher-order predicates**: Writing manual recursion instead of maplist/foldl. Veterans recognize standard patterns.

**Poor error handling**: No input validation, unclear error messages, not following ISO error conventions. Use `must_be/2` from library(error).

**Fighting relational nature**: Thinking "how do I modify this" instead of "what relation holds between old and new state."
</anti_patterns>

## Design Patterns Veterans Use

<design_patterns>

**Accumulator pattern** for aggregating results through recursion:

```prolog
sum_list(List, Sum) :-
    sum_list_(List, 0, Sum).

sum_list_([], Acc, Acc).
sum_list_([H|T], Acc0, Sum) :-
    Acc1 is Acc0 + H,
    sum_list_(T, Acc1, Sum).
```

**Difference lists** for O(1) list concatenation:

```prolog
% Difference list append: O(1) instead of O(n)
append_dl(A-B, B-C, A-C).

% Example usage
?- append_dl([1,2|X]-X, [3,4|Y]-Y, List-[]).
List = [1,2,3,4].
```

**Higher-order patterns** with library(apply):

```prolog
% Map operation
?- maplist(plus(1), [1,2,3], Result).
Result = [2,3,4].

% Filter operation
?- include(>(5), [1,6,3,8,2], Result).
Result = [6,8].

% Fold operation
?- foldl(plus, [1,2,3,4], 0, Sum).
Sum = 10.
```

**Constraint programming pattern** (covered earlier):
1. Declare variables and domains
2. Post constraints
3. Label variables for solutions
</design_patterns>

## Production Requirements Checklist

<production_checklist>

Before considering code production-ready:

**Mandatory**:
- ✅ All files are modules with clear exports
- ✅ Complete PlDoc documentation for ALL public predicates
- ✅ Comprehensive PlUnit tests for all modules
- ✅ All tests pass with `run_tests.`
- ✅ `check.` runs without errors or warnings
- ✅ All predicates are steadfast (tested both ways)
- ✅ No style_check warnings (singleton, discontiguous, no_effect)
- ✅ README with installation and usage
- ✅ Proper error handling with library(error)

**Highly Recommended**:
- ✅ Use CLP(FD) instead of low-level arithmetic where applicable
- ✅ Predicates work in multiple directions when possible
- ✅ DCGs used for state threading and parsing
- ✅ Higher-order predicates (maplist, foldl) used appropriately
- ✅ No unnecessary assert/retract (state threaded through arguments)
- ✅ Test coverage analysis (use `show_coverage/1`)
- ✅ Examples in `examples/` directory

**For Distributed Packs**:
- ✅ `pack.pl` with complete metadata
- ✅ Semantic versioning (MAJOR.MINOR.PATCH)
- ✅ LICENSE file
- ✅ Git tags for versions (V1.0.0)
- ✅ CI/CD with GitHub Actions (optional but recommended)
</production_checklist>

## Essential Resources

<resources>

**Primary references**:
- **The Power of Prolog** by Markus Triska: https://www.metalevel.at/prolog
- **Coding Guidelines for Prolog** by Covington et al.: https://www.covingtoninnovations.com/mc/plcoding.pdf
- **SWI-Prolog official documentation**: https://www.swi-prolog.org/pldoc/doc_for?object=manual
- **SWI-Prolog Discourse forum**: https://swi-prolog.discourse.group/
- **The Craft of Prolog** by Richard O'Keefe (advanced techniques)

**Key papers**:
- "Fifty Years of Prolog and Beyond" (2022): https://arxiv.org/abs/2201.10816
- Jan Wielemaker's publications: https://www.swi-prolog.org/Publications.html
- Leon Sterling "Patterns for Prolog Programming" (2002)

**Community resources**:
- Pack list: https://www.swi-prolog.org/pack/list
- SWISH (online IDE): https://swish.swi-prolog.org/
- GitHub: https://github.com/SWI-Prolog/swipl
- Downloads: https://www.swi-prolog.org/download/stable
</resources>

## Veteran Wisdom

**Richard O'Keefe's three themes** (The Craft of Prolog):
1. "Hacking your program is no substitute for understanding your problem"
2. "Prolog is different, but not that different"
3. "Elegance is not optional"

**Jan Wielemaker** on philosophy: "My primary motivation has always been to build stuff that works rather than stuff that allows writing an academic paper."

**Markus Triska** on declarative thinking: "Better ask: What are the cases and conditions that make this predicate true? Think in terms of relations between entities you are describing."

**Kyle Cordes** on the Prolog advantage: "We cut the cost/time of this implementation by 90% or more, not by coding more quickly, but by thinking more clearly."

**From Covington et al.** on efficiency: "The most efficient program is the one that does the right computation, not the one with the most tricks. By choosing a better basic algorithm, you can sometimes speed up a computation by a factor of a million."

**On quality**: "There is really no excuse not to write tests! Automatic testing of software during development is probably the most important Quality Assurance measure."
