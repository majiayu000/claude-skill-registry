---
name: debugging-testing
description: Use when the user reports a bug they can't reproduce, asks where to start debugging, or mentions a Heisenbug / production-only failure. Drives the observe→hypothesize→predict→test→iterate scientific method.
description-frequency: on-demand
type: skill
category: coding
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/coding/debugging-testing/SKILL.md
superseded_by: null
---
# Debugging & Testing

A program without tests is a hypothesis. A program with bugs and no debugging strategy is a mystery. This skill catalogs systematic approaches to both: finding defects (debugging) and preventing them (testing). The emphasis is on method over intuition -- debugging and testing are engineering disciplines with established techniques, not arts that depend on talent.

**Agent affinity:** hopper (coined "debugging" when she found a moth in the Mark II), dijkstra (program correctness as a mathematical property)

**Concept IDs:** code-debugging-strategies, code-iterative-development, code-peer-review

## Part 1 -- The Debugging Mindset

### Debugging as Scientific Method

A bug is a hypothesis falsifier: your mental model of the program says X should happen, but Y happens instead. Debugging is the process of updating your mental model until it matches reality.

1. **Observe** the symptom. What actually happened? What did you expect?
2. **Hypothesize.** What could cause the discrepancy? List at least three candidates.
3. **Predict.** If hypothesis H is true, what would happen if I do experiment E?
4. **Test.** Perform the experiment. Does the result match the prediction?
5. **Iterate.** If the prediction was wrong, the hypothesis is eliminated. Try the next one.

This is the scientific method applied to code. The most common debugging mistake is skipping step 2 -- changing things at random hoping the bug disappears. Random changes do not build understanding. They may mask the bug or introduce new ones.

### Grace Hopper's Debugging Legacy

In 1947, operators of the Harvard Mark II found a moth trapped in a relay, causing a malfunction. Grace Hopper taped the moth into the logbook with the note "First actual case of bug being found." The term "debugging" predates this incident, but Hopper's story crystallized the concept: finding and removing defects is a first-class engineering activity, not a sign of failure.

Hopper's broader contribution to debugging was the invention of the compiler. Before compilers, programs were written in machine code, and every error was a numerical one. Compilers introduced symbolic names, structured control flow, and -- critically -- error messages. The compiler was the first automated debugging tool.

## Part 2 -- Debugging Techniques

### 2.1 -- Printf / Logging Debugging

**Technique:** Insert print statements or log calls at strategic points to observe the program's state as it executes.

**When to use.** First response for any bug. Fast to deploy, works in any language, requires no special tools. Especially valuable in environments where interactive debuggers are impractical (distributed systems, embedded systems, CI pipelines).

**Best practices.**
- Log the function name, key variable values, and the decision path taken.
- Use structured logging (JSON) for production systems so logs are searchable.
- Remove or disable debug prints before committing. Use log levels (DEBUG, INFO, WARN, ERROR) to control verbosity without removing code.

**Limitation.** Heisenbug risk: adding print statements can change timing, which may mask concurrency bugs.

### 2.2 -- Interactive Debuggers

**Technique:** Pause execution at breakpoints, inspect variables, step through code line by line.

**Tools.** GDB (C/C++), LLDB (C/C++/Rust), pdb (Python), Chrome DevTools (JavaScript), VS Code debugger (multi-language).

**Key operations.**
- **Breakpoint:** Pause when execution reaches a specific line.
- **Conditional breakpoint:** Pause only when a condition is true (e.g., `i == 999`).
- **Watch expression:** Monitor a variable and pause when its value changes.
- **Step over:** Execute the current line, skip into function calls.
- **Step into:** Enter the function being called.
- **Step out:** Execute until the current function returns.

**When to use.** Complex control flow where printf would require dozens of statements. Inspecting data structures that are hard to print (circular references, large trees). Understanding unfamiliar code.

### 2.3 -- Binary Search Debugging

**Technique:** Narrow the problem to the smallest possible scope by halving the search space at each step.

**Application to time.** If a bug appeared recently, use git bisect to binary-search through commits: mark a known-good commit and a known-bad commit, test the midpoint, repeat. In O(log n) steps, find the exact commit that introduced the bug.

**Application to code.** Comment out half the code. Does the bug persist? If yes, the bug is in the remaining half. If no, the bug is in the commented half. Repeat.

**Application to data.** If the bug occurs with a large input, halve the input. Does the bug persist? Binary search to find the minimal reproducing input.

### 2.4 -- Rubber Duck Debugging

**Technique:** Explain the code, line by line, to an inanimate object (traditionally a rubber duck). The act of articulating your assumptions often reveals the one that is wrong.

**Why it works.** Reading code silently allows your brain to skip over details. Speaking forces you to process each line consciously. The mismatch between what you say and what the code does surfaces the bug.

**Formal variant.** Code review. Explaining your code to a colleague achieves the same effect with the added benefit of a second perspective.

### 2.5 -- Time-Travel Debugging

**Technique:** Record program execution and replay it, stepping backward and forward through time.

**Tools.** rr (Linux, C/C++/Rust), Replay.io (JavaScript), IntelliJ's step-back feature.

**When to use.** Concurrency bugs, non-deterministic failures, bugs that are hard to reproduce. Time-travel debugging eliminates the need to reproduce the bug -- you debug the exact execution that failed.

### 2.6 -- Git Bisect

**Technique:** Automated binary search through git history to find the commit that introduced a bug.

**Usage.**
```
git bisect start
git bisect bad              # Current commit has the bug
git bisect good abc1234     # This commit was known-good
# Git checks out the midpoint. Test it.
git bisect good             # or: git bisect bad
# Repeat until the first bad commit is found.
git bisect reset            # Return to original state
```

**Automation.** `git bisect run ./test.sh` -- provide a script that returns 0 for good and non-zero for bad. Git runs the binary search automatically.

**Prerequisite.** Each commit must be independently testable. This is one reason to keep commits small and atomic.

## Part 3 -- Testing Levels

### 3.1 -- Unit Tests

**Scope:** Test a single function, method, or class in isolation.

**Characteristics.** Fast (milliseconds per test), deterministic (no I/O, no network, no database), focused (one assertion per logical concept).

**Isolation techniques.** Mocks (simulate dependencies), stubs (provide canned answers), fakes (simplified implementations, e.g., in-memory database).

**When to use.** Every pure function. Every method with business logic. The foundation of the test pyramid.

### 3.2 -- Integration Tests

**Scope:** Test the interaction between two or more components (e.g., service + database, API + authentication).

**Characteristics.** Slower than unit tests, may require real infrastructure (database, message queue), tests contracts between components.

**When to use.** Validating that the database layer correctly persists and retrieves data. Ensuring that API endpoints handle real HTTP requests. Testing message serialization/deserialization across service boundaries.

### 3.3 -- End-to-End Tests

**Scope:** Test the entire system from the user's perspective. UI clicks through backend to database and back.

**Characteristics.** Slowest, most brittle (sensitive to UI changes, timing, environment), most realistic.

**Tools.** Playwright, Cypress, Selenium (web), Appium (mobile).

**When to use.** Sparingly. Cover the critical user journeys (signup, purchase, core workflow). Too many E2E tests create a slow, flaky test suite that developers learn to ignore.

### 3.4 -- Acceptance Tests

**Scope:** Verify that the system meets the business requirements as specified by stakeholders.

**Relationship to levels.** Acceptance tests can run at any level (unit, integration, E2E) depending on what is being verified. They are defined by intent (does the system do what the business needs?) rather than technique.

### The Test Pyramid

```
        /  E2E  \           Few, slow, brittle
       /----------\
      / Integration \       Some, medium speed
     /----------------\
    /    Unit Tests    \    Many, fast, focused
```

Invert the pyramid (many E2E, few units) and you get a slow, fragile, expensive test suite. The pyramid structure maximizes confidence per test-dollar.

## Part 4 -- Test-Driven Development (TDD)

### The Red-Green-Refactor Cycle

1. **Red.** Write a test for the next piece of functionality. Run it. It fails (because the functionality does not exist yet).
2. **Green.** Write the minimum code to make the test pass. No more.
3. **Refactor.** Clean up the code while keeping all tests green. Improve names, extract functions, remove duplication.

Repeat. Each cycle takes minutes, not hours. The test suite grows with the code, providing continuous regression protection.

### Why TDD Works

- **Design pressure.** Writing the test first forces you to think about the interface before the implementation. Hard-to-test code is usually hard-to-test because it is badly designed -- tight coupling, hidden dependencies, side effects. TDD makes these problems visible immediately.
- **Regression safety.** Every feature has tests from the moment it is written. Refactoring is safe because the tests catch regressions instantly.
- **Documentation.** Tests are executable documentation. They show how the code is intended to be used.

### When TDD Hurts

- **Exploratory work.** When you do not know what the interface should look like, writing tests first anchors you to a premature design. Spike first, then test.
- **UI code.** Rapidly changing UIs make tests brittle. Test the logic behind the UI, not the pixel positions.
- **Integration with external systems.** When the behavior depends on a third-party API you do not control, TDD requires extensive mocking that may not reflect real behavior.

## Part 5 -- Test Design Techniques

### 5.1 -- Equivalence Partitioning

**Technique:** Divide the input space into classes where the program should behave identically. Test one representative from each class.

**Example.** A function that grades scores 0-100: F (0-59), D (60-69), C (70-79), B (80-89), A (90-100). Test one value from each partition: 45, 65, 75, 85, 95.

### 5.2 -- Boundary Value Analysis

**Technique:** Test at the edges of equivalence partitions, where off-by-one errors concentrate.

**Example.** For the grading function above: 0, 59, 60, 69, 70, 79, 80, 89, 90, 100. Also test just outside the valid range: -1, 101.

### 5.3 -- Property-Based Testing

**Technique:** Instead of specifying individual test cases, specify properties that must hold for all inputs. The testing framework generates hundreds or thousands of random inputs and checks the property.

**Tools.** Hypothesis (Python), fast-check (JavaScript/TypeScript), QuickCheck (Haskell, original), proptest (Rust).

**Example properties.**
- `sort(list)` has the same length as `list`.
- `sort(list)` contains the same elements as `list`.
- `sort(list)` is non-decreasing.
- `reverse(reverse(list)) == list`.
- `parse(serialize(obj)) == obj` (round-trip).

**Shrinking.** When a failing input is found, the framework automatically simplifies it to the minimal reproducing case. This is enormously valuable for debugging.

### 5.4 -- Mutation Testing

**Technique:** Automatically introduce small changes (mutations) to the code -- change + to -, flip < to <=, delete a line. If the test suite still passes, it has a gap: the mutant "survived." Kill rate measures test suite thoroughness.

**Tools.** Stryker (JavaScript/TypeScript), mutmut (Python), pitest (Java).

**Interpretation.** A high kill rate (>80%) indicates thorough testing. Surviving mutants reveal specific untested behaviors.

## Part 6 -- Profiling and Performance Debugging

### CPU Profiling

**Sampling profiler.** Periodically records which function is executing. Low overhead, statistical accuracy. Identifies hot functions (where most time is spent).

**Instrumentation profiler.** Records entry and exit of every function. High overhead, exact counts. Identifies call frequency and per-call duration.

**Tools.** perf (Linux), Instruments (macOS), py-spy (Python), clinic.js (Node.js), cargo-flamegraph (Rust).

### Memory Profiling

**Heap profiling.** Track allocations, find memory leaks (objects that grow without bound), identify excessive allocation churn.

**Tools.** Valgrind/Massif (C/C++), tracemalloc (Python), Chrome DevTools heap snapshot (JavaScript), DHAT (Rust via Valgrind).

### Flame Graphs

**Visualization.** A flame graph shows the call stack with width proportional to time spent. Wide bars at the top are the hot functions. The shape reveals whether the time is spent in one deep call chain or spread across many.

**Reading a flame graph.** The x-axis is NOT time -- it is the alphabetical sort of stack frames at each depth. Width is the cumulative time. Look for wide plateaus (optimization targets) and unexpected width (functions that should be fast but are not).

## Debugging Strategy Selection

| Symptom | First technique | Why |
|---|---|---|
| Wrong output, simple function | Printf + unit test | Fast feedback, isolate the logic |
| Wrong output, complex flow | Interactive debugger | Step through the decision path |
| Recent regression | Git bisect | Find the exact commit |
| Intermittent failure | Logging + time-travel debug | Capture the non-deterministic execution |
| Performance degradation | CPU profiler + flame graph | Identify the hot path |
| Memory growth | Heap profiler | Find the leak |
| Concurrency bug | Thread sanitizer + rr | Detect races, replay exact execution |
| "It works on my machine" | Environment diff + integration test | Isolate the environmental dependency |

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Testing implementation, not behavior | Tests break on refactoring | Test the public interface, not internal details |
| 100% code coverage as a goal | Coverage measures lines executed, not correctness | Aim for meaningful coverage of behavior, not line count |
| Flaky tests left unfixed | Team learns to ignore test failures | Fix or delete flaky tests immediately |
| No test isolation | Tests depend on each other's state | Each test sets up and tears down its own state |
| Debugging by random changes | No understanding of the bug | Apply the scientific method: hypothesize, predict, test |
| Skipping the minimal reproduction | Debugging a complex system when the bug is in one function | Reduce to the smallest failing case before debugging |
| Over-mocking | Tests pass but code fails in production | Use integration tests for interaction boundaries |

## Cross-References

- **hopper agent:** Debugging heritage, compiler as debugging tool, practical language implementation.
- **dijkstra agent:** Program correctness proofs, structured programming as bug prevention.
- **papert agent:** Teaching debugging as a learning skill, not a punishment.
- **knuth agent:** Literate programming as a debugging aid -- code that is clear enough to read is easier to debug.
- **programming-fundamentals skill:** The constructs being debugged and tested.
- **software-design skill:** Design principles that make code testable.

## References

- Hopper, G. M. (1947). Mark II logbook entry. Naval Surface Warfare Center, Dahlgren, VA.
- Zeller, A. (2009). *Why Programs Fail*. 2nd edition. Morgan Kaufmann.
- Beck, K. (2002). *Test-Driven Development: By Example*. Addison-Wesley.
- Meszaros, G. (2007). *xUnit Test Patterns*. Addison-Wesley.
- Claessen, K. & Hughes, J. (2000). "QuickCheck: A Lightweight Tool for Random Testing of Haskell Programs." *ICFP 2000*.
- Gregg, B. (2020). *Systems Performance: Enterprise and the Cloud*. 2nd edition. Addison-Wesley.
- O'Callahan, R. et al. (2017). "Engineering Record And Replay For Deployability." *USENIX ATC 2017*.
