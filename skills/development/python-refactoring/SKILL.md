---
name: python-refactoring
description: "Python refactoring catalog with 83 patterns covering immutability, class design, control flow, architecture, OO metrics, and Python idioms. Analyze code for smells and apply numbered refactoring patterns with before/after examples. Use when the user invokes /refactor or explicitly asks to refactor, clean up, or improve Python code quality."
---

# Python Refactoring Skill

83 refactoring patterns from Contieri's series, Fowler's catalog, OO metrics literature, and Python idioms.

## Modes

**Active Analysis** (default when given code): Identify smells -> map to patterns -> load relevant references -> apply refactorings with before/after -> note trade-offs.

**Reference Lookup** (when asked about a pattern by number/name): Load the relevant reference file -> present the pattern.

## Smell-to-Pattern Map

| Code Smell | Patterns | File |
|---|---|---|
| Setters / half-built objects | SC101, SC104 | state.md |
| Mutable default args | SC701 | idioms.md |
| Unprotected public attributes | SC103 | state.md |
| Magic numbers / constants | SC601 | hygiene.md |
| Variables that never change | SC102 | state.md |
| Boolean flags for roles/states | SC105 | state.md |
| Stale cached/derived attributes | 030 | state.md |
| Long function, multiple concerns | SC201, 010 | functions.md |
| Comments replacing code | 005 | functions.md |
| Comments explaining what code does | 011 | hygiene.md |
| Generic names (result, data, tmp) | SC202 | functions.md |
| Duplicated logic | SC606 | hygiene.md |
| Near-duplicate functions | 050 | functions.md |
| Long related parameter lists | SC206, 052 | functions.md |
| Query + modify in same function | SC207 | functions.md |
| Static functions hiding deps | 020 | functions.md |
| `input()` in business logic | SC203 | functions.md |
| Getters exposing data | 027 | functions.md |
| Need to test private methods | 037 | functions.md |
| Unused function parameters | SC208 | functions.md |
| Long lambda expressions | SC209 | functions.md |
| Type-checking if/elif chains | SC302 | types.md |
| `isinstance()` dispatch | 060 | idioms.md |
| Dicts as objects (stringly-typed) | 012 | types.md |
| Raw primitives with implicit rules | 019, 044 | types.md |
| Raw lists, no domain meaning | 038 | types.md |
| Boilerplate `__init__/__repr__/__eq__` | SC304 | idioms.md |
| Related functions without a class | SC301 | types.md |
| Sibling classes with duplicate behavior | 022 | types.md |
| Inheritance without "is-a" | 023 | types.md |
| Constructor needs descriptive name | 048 | types.md |
| Scattered `None` checks | 015, SC204 | types.md |
| Lazy class (too few methods) | SC306 | types.md |
| Temporary fields (used in few methods) | SC307 | types.md |
| Deep nesting | SC402 | control.md |
| Imperative loops with accumulation | SC403 | control.md |
| Complex boolean expressions | SC404 | control.md |
| Long expressions, no named parts | 043 | control.md |
| Loop doing two things | 046 | control.md |
| Parse/compute/format mixed | 047 | control.md |
| Clunky algorithm | 049 | control.md |
| Boolean flag controlling loop | SC405 | control.md |
| Complex if/elif dispatch | 056 | control.md |
| Related statements scattered | 053 | control.md |
| Missing default else branch | SC407 | control.md |
| Complex comprehensions | SC406 | control.md |
| Singleton / global state | SC303, SC106 | architecture.md |
| Same exception for biz + infra | 035 | architecture.md |
| Chained `.attr.attr.attr` | SC502 | architecture.md |
| No fail-fast assertions | 045 | architecture.md |
| Dead code / commented blocks | SC401 | hygiene.md |
| Unused exceptions | SC602 | hygiene.md |
| Empty catch blocks | SC605 | hygiene.md |
| Giant regex | 025 | hygiene.md |
| Excessive decorators | SC205 | hygiene.md |
| String concatenation for multiline | SC603 | hygiene.md |
| Inconsistent formatting | 032 | hygiene.md |
| Cryptic error messages | 031 | hygiene.md |
| Sequential IDs leaking info | SC107 | architecture.md |
| Error codes instead of exceptions | SC501 | architecture.md |
| Blocking calls in async functions | SC703 | idioms.md |
| Manual try/finally cleanup | SC702, SC604 | idioms.md |
| Full lists when streaming works | 059 | idioms.md |
| Indexing tuples by position | SC305 | idioms.md |
| Shotgun surgery (wide call spread) | SC505 | architecture.md |
| Deep inheritance tree | SC308 | types.md |
| Wide hierarchy (too many subclasses) | SC309 | types.md |
| Inappropriate intimacy | SC506 | architecture.md |
| Speculative generality (unused ABCs) | SC507 | architecture.md |
| Unstable dependency | SC508 | architecture.md |
| Low class cohesion (LCOM) | SC801 | metrics.md |
| High coupling between objects (CBO) | SC802 | metrics.md |
| Excessive fan-out | SC803 | metrics.md |
| High response for class (RFC) | SC804 | metrics.md |
| Middle man (excessive delegation) | SC805 | metrics.md |

## Reference Files

Load **only** the file(s) matching detected smells:

- `references/state.md` -- Immutability, setters, attributes (SC101, SC102, SC103, SC104, SC105, 030)
- `references/functions.md` -- Method extraction, naming, parameters, CQS (SC201, 005, SC202, 010, 020, SC203, 027, SC206, 037, SC207, 050, 052, SC208, SC209)
- `references/types.md` -- Class design, reification, polymorphism, nulls (SC301, 012, SC302, 015, 019, 022, 023, SC204, 038, 044, 048, SC306, SC307, SC308, SC309)
- `references/control.md` -- Guard clauses, pipelines, conditionals, phases (SC402-SC404, 043, 046, 047, 049, 053, SC405, 056, SC406, SC407)
- `references/architecture.md` -- DI, singletons, exceptions, delegates (SC303, SC106, SC107, 035, 045, SC501, SC502, SC505, SC506, SC507, SC508)
- `references/hygiene.md` -- Constants, dead code, comments, style (SC601, SC602, 011, SC606, SC401, 025, 031-032, SC205, SC603, SC605)
- `references/idioms.md` -- Context managers, generators, unpacking, protocols, async (SC701, SC702, SC703, 059, 060, SC304, SC305, SC604)
- `references/metrics.md` -- OO metrics: cohesion, coupling, fan-out, response, delegation (SC801, SC802, SC803, SC804, SC805)

## Automated Smell Detector

`scripts/detect_smells.py` runs the smell detector with 56 automated checks (41 per-file + 10 cross-file + 5 OO metrics). It ships with a bundled copy of the smellcheck package — no pip install required.

```bash
# Works immediately after skill install — no pip required
python3 scripts/detect_smells.py src/
python3 scripts/detect_smells.py myfile.py --format json

# Look up rule documentation (description + before/after example)
python3 scripts/detect_smells.py --explain SC701
python3 scripts/detect_smells.py --explain SC4    # list a family
python3 scripts/detect_smells.py --explain all    # list all rules

# Caching (enabled by default — skips unchanged files on repeat scans)
python3 scripts/detect_smells.py src/ --no-cache       # fresh scan
python3 scripts/detect_smells.py --clear-cache         # purge cache

# Or use the pip-installed CLI directly
pip install smellcheck
smellcheck src/ --min-severity warning --fail-on warning
```

**Per-file detections** (41): SC101 setters, SC201 long functions, SC601 magic numbers, SC602 bare except, SC202 generic names, SC301 extract class, SC102 UPPER_CASE without Final, SC103 public attrs, SC302 isinstance chains, SC104 half-built objects, SC105 boolean flags, SC303 singleton, SC401 dead code after return, SC106 global mutables, SC203 input() in logic, SC107 sequential IDs, SC204 return None|list, SC205 excessive decorators, SC206 too many params, SC603 string concatenation, SC402 deep nesting, SC403 loop+append, SC207 CQS violation, SC404 complex booleans, SC501 error codes, SC502 Law of Demeter, SC405 control flags, SC701 mutable defaults, SC702 open without with, SC703 blocking calls in async, SC304 dataclass candidate, SC305 sequential indexing, SC604 contextlib candidate, SC210 cyclomatic complexity, SC208 unused parameters, SC605 empty catch block, SC209 long lambda, SC406 complex comprehension, SC407 missing else, SC306 lazy class, SC307 temporary field.

**Cross-file detections** (10): SC606 duplicate functions (AST-normalized hashing), SC503 cyclic imports (DFS), SC504 god modules, SC211 feature envy, SC505 shotgun surgery, SC308 deep inheritance, SC309 wide hierarchy, SC506 inappropriate intimacy, SC507 speculative generality, SC508 unstable dependency.

**OO metrics** (5): SC801 lack of cohesion, SC802 coupling between objects, SC803 fan-out, SC804 response for class, SC805 middle man.

Run the detector first for a quick scan, then use the reference files to understand and apply the suggested refactorings.

## Guided Refactoring Workflow

smellcheck groups its 56 rules into 9 ordered phases with dependency chains. The `--plan` command generates a customized refactoring plan based on actual findings.

### Initialization

```bash
# Bundled (no pip install required)
python3 scripts/detect_smells.py <path> --plan
python3 scripts/detect_smells.py <path> --plan --format json

# Or via pip-installed CLI
smellcheck <path> --plan
smellcheck <path> --plan --format json
```

The plan auto-selects a strategy: **local_first** (default, phases 0-8) or **architecture_first** (reorders to [0,1,7,8,2,3,4,5,6]) when >30% of findings are cross-file or metric scoped.

### Phase Execution Loop

Each phase has three passes:

**Pass 1 — Automated scan**: Run the `--select` command printed in the plan output for the current phase. Fix each finding using the reference file for that rule's family.

**Pass 2 — Agent semantic review**: For candidate files (files with automated findings + changed files in branch + import neighbors for cross-file phases), check for manual patterns assigned to the current phase. Evidence requirements for every semantic finding:
- File path and line range
- Actual code snippet
- Pattern number and name
- Why it matches the heuristic
- Confidence score (>=0.8 auto-fix, 0.5-0.79 suggest+confirm, <0.5 don't emit)

**Pass 3 — Gate check**: If gate is `tests_pass`, run the test suite and do not proceed until green. If `rescan_after` is true, re-run `--plan` and re-bucket.

### Manual Pattern Assignments per Phase

For each manual pattern below, load the corresponding reference file from the Reference Files section to see full before/after examples.

| Phase | Patterns | Agent detection heuristics |
|-------|----------|---------------------------|
| 0 correctness | (none) | Fully automated |
| 1 dead_code | 005 | Comments that restate the next line — delete them |
| 2 clarity | 011, 031 | 011: comments explaining "what" not "why". 031: error messages missing context |
| 3 idioms | 059, 060 | 059: `list(gen)` where result is only iterated once. 060: single `isinstance()` dispatch |
| 4 control_flow | 043, 046, 047, 049, 053, 056 | 043: expression >80 chars with no named subparts. 046: loop body with 2+ concerns. 047: function that parses+computes+formats. 049: manual impl of stdlib op. 053: related lines separated by unrelated. 056: if/elif 4+ branches |
| 5 functions | 010, 020, 027, 037, 050, 052 | 020: function-scoped import. 027: `obj.get_x()` + logic → move to obj. 037: test accessing `._private`. 050: two functions >80% body similarity. 052: 3+ related params |
| 6 state_class | 012, 019, 022, 023, 030, 038, 044, 048 | 012: dict with 3+ consistent keys → dataclass. 019/044: primitive with constraints → value object. 022: siblings with duplicate methods. 023: inheritance for reuse not "is-a". 030: cached attr that drifts. 038: `list[str]` with domain meaning. 048: unclear constructor → factory |
| 7 architecture | 015, 025, 035, 045 | 015: `if x is not None` in 3+ sites → Null Object. 025: regex >80 chars → `re.VERBOSE`. 035: same exception for biz+infra. 045: broad input without precondition |
| 8 metrics | (none) | Fully automated; use results to revisit phase 6 |

**Pattern 032** (inconsistent formatting): Tool-enforced — run `black` or `ruff format` before starting workflow.

### Conditional Branching

- No classes detected → phases 6 and 8 skip automatically
- No async code (SC703 has 0 findings) → skip in phase 3
- Architecture-dominant (>30% cross-file) → plan reorders to architecture-first
- Single-file scan → cross-file phases will naturally have 0 findings
- Large backlog → generate baseline, gate only new findings

### Feedback Loops

- Phase 8 → Phase 6: under `local_first`, if metrics still high, loop back (max 2 iterations). Under `architecture_first`, phase 8 runs before phase 6, so this becomes forward flow — metrics inform the class design pass.
- Phase 5 → Phase 8: extraction changes cohesion, re-check metrics
- Any phase → tests: if tests break, pause and fix first

### Completion Criteria

All phases either skip (0 findings) or pass. Tests green. Feedback loops converged. `smellcheck --plan` shows all phases as skip.

## Guidelines

- Prioritize structural refactorings over cosmetic
- Preserve existing tests -- refactoring changes structure, not behavior
- Group related changes when multiple patterns apply
- Flag changes to public API (breaking vs non-breaking)
- For large code, suggest incremental order rather than all-at-once
- When patterns conflict, explain the trade-off and recommend
