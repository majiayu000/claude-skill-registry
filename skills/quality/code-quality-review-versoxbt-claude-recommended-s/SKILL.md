---
name: code-quality-review
description: "Perform structured code reviews enforcing quality standards, naming conventions, architecture patterns, and team agreements. Use when the user says 'review this code', 'code review', 'check quality', 'review my PR', 'what's wrong with this', 'improve this code', 'review before merge', 'peer review', or 'audit this'. Also triggers on 'code quality', 'review standards', 'enforce conventions', 'tech debt check', 'lint review', or when user completes a significant code change."
version: 1.0.0
---

# Code Quality Review

## Purpose

Code review maintains codebase coherence: readability, convention adherence, appropriate abstraction, and knowledge sharing. The primary goal is **not** finding bugs — tests do that. Code review ensures that the code communicates intent clearly, follows team agreements, and remains maintainable as the codebase evolves.

A good review catches what automated tools cannot: misleading names, wrong abstractions, missing context, violated conventions, and architectural drift.

## When to Activate

- **Before a PR**: Review staged or committed changes before opening a pull request.
- **Reviewing specific files or diffs**: User points at code and asks for feedback.
- **Suspected code smells**: Something feels off — too complex, too long, unclear naming.
- **During refactoring**: Verify the refactor preserves intent and improves structure.
- **Onboarding**: Review code written by someone learning the codebase conventions.
- **Post-incident**: Review code involved in a production issue for contributing factors.

## Review Process (4 Passes)

Execute these passes sequentially. Each pass has a distinct focus — do not blend concerns across passes.

### Pass 1: Structural

Examine the shape of the code without reading logic deeply.

- **File organization**: Are files focused on a single responsibility? Are related files co-located?
- **File size**: Files under 400 lines? Over 800 lines is a hard flag.
- **Function size**: Functions under 50 lines? Can any be decomposed?
- **Naming**: Do file names, function names, and variable names communicate intent?
- **Nesting depth**: More than 4 levels of nesting? Consider early returns or extraction.
- **Exports**: Is the public API of each module minimal and intentional?
- **Dead code**: Commented-out code, unused imports, unreachable branches?
- **Organization pattern**: Does the file structure match the project's convention (feature-based, layer-based)?

### Pass 2: Logic

Read the code for correctness and robustness.

- **Happy path**: Does the core logic produce correct results for typical inputs?
- **Edge cases**: Empty arrays, null values, zero, negative numbers, unicode, concurrent access?
- **Error handling**: Are errors caught, logged with context, and re-thrown or handled appropriately?
- **Input validation**: Is user input validated at system boundaries? Are schemas used?
- **Race conditions**: Shared mutable state? Async operations that assume ordering?
- **Resource management**: Are connections, file handles, and subscriptions properly cleaned up?
- **Off-by-one errors**: Loop bounds, array indexing, pagination logic?
- **Type safety**: Are types narrow enough? Any `any` casts hiding potential issues?

### Pass 3: Convention

Check adherence to team agreements and codebase patterns.

- **Immutability**: Are objects and arrays created fresh rather than mutated? Spread operators, `map`/`filter`/`reduce` over `push`/`splice`?
- **Error patterns**: Do error handling patterns match the codebase convention (e.g., typed errors, error boundaries)?
- **Type definitions**: Are interfaces and types used consistently? Are they in the right location?
- **Import ordering**: Does import structure follow project conventions?
- **API response format**: Do new endpoints follow the established response shape?
- **Logging**: Are log statements structured and at appropriate levels?
- **Hardcoded values**: Are magic numbers and strings extracted to named constants?
- **Console statements**: Are `console.log` debugging statements cleaned up?

### Pass 4: Architecture

Step back and evaluate design decisions.

- **Coupling**: Does this change increase coupling between modules that should be independent?
- **Cohesion**: Does each module/class/function do one thing well?
- **Abstraction level**: Are abstractions at the right level — not too early, not too late?
- **Circular dependencies**: Does this introduce or worsen circular import chains?
- **Dependency direction**: Do dependencies flow from specific to general (not the reverse)?
- **Future readability**: Will someone unfamiliar with this context understand the code in 6 months?
- **API surface**: Does this change expand the public API? Is that expansion intentional?
- **Patterns consistency**: If the codebase uses Repository pattern, Observer pattern, etc., does new code follow suit?

## Severity Classification

Classify every finding into one of five levels. See `references/severity-classification.md` for the full decision tree.

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| **CRITICAL** | Breaks functionality, security vulnerability, data loss risk | Must fix before merge |
| **HIGH** | Violates team conventions in ways that compound, significant maintainability risk | Should fix before merge |
| **MEDIUM** | Improvement that reduces future maintenance cost | Consider fixing; discuss if unsure |
| **LOW** | Minor improvement, slightly better readability or consistency | Fix if convenient; fine to skip |
| **NIT** | Purely stylistic, personal preference territory | Optional; author's call |

## Review Output Format

Present findings in this structure:

```
CODE REVIEW REPORT
==================
Files reviewed: [N]

CRITICAL (must fix):
- [file:line] [description] — [why this matters]

HIGH (should fix):
- [file:line] [description]

MEDIUM (consider fixing):
- [file:line] [description]

LOW (nice to have):
- [file:line] [description]

NIT (optional):
- [file:line] [description]

Summary: [X critical, Y high, Z medium findings]
Recommendation: [APPROVE / REQUEST CHANGES / DISCUSS]
```

**Recommendation guidelines**:
- **APPROVE**: Zero critical, zero high. Medium findings are documented but non-blocking.
- **REQUEST CHANGES**: Any critical or high findings present.
- **DISCUSS**: Architectural concerns that need team input, or when context is missing to make a judgment.

Omit empty severity sections. If no findings at a level, do not include that heading.

## Review Principles

1. **Review the diff, not the entire file.** Focus on what changed. Pre-existing issues in unchanged code are tech debt tickets, not review findings — unless the change makes them worse.

2. **Don't rewrite code in reviews.** Suggest direction, not implementation. Say "consider extracting this into a helper" not "here's the 40-line refactored version." The author should own the solution.

3. **Distinguish personal preference from team convention.** If the team has agreed on a pattern, enforce it. If it's your personal taste, mark it as NIT and move on.

4. **Performance claims need evidence.** "This might be slow" is not a valid finding without measurement, profiling data, or a concrete scenario (e.g., "this runs per-row in a 100k-row table").

5. **Context matters.** A hotfix at 2am and a greenfield feature have different quality bars. Adjust severity accordingly — but document what you'd improve in a follow-up.

6. **Praise good patterns.** Call out clean abstractions, good names, thoughtful error handling. Reviews that only flag problems erode morale and miss the chance to reinforce good habits.

7. **Ask before assuming.** If something looks wrong but might be intentional, phrase it as a question: "Is this intentional? It looks like it might skip validation for admin users."

8. **One concern per finding.** Don't bundle multiple issues into a single comment. Each finding should be independently addressable.

## Gotchas

- **"This might be slow" without measurement is not valid.** Performance intuition is unreliable. Flag it only if you can articulate the scenario where it matters and estimate the impact.

- **What looks like a bug may be intentional.** Legacy systems, backwards compatibility, and business rules create code that looks wrong. Ask before flagging as critical.

- **Don't review generated code the same as hand-written.** Protobuf stubs, OpenAPI clients, ORM migrations, and similar artifacts have different quality expectations. Review the generator config, not the output.

- **Nitpicking erodes trust.** If you have more than 3 nits on a file, pick the most impactful one and drop the rest. A review full of nits signals that you couldn't find real issues.

- **Review fatigue is real.** Large PRs (>400 lines of changes) need focus breaks between passes. Do Pass 1 and 2, take a break, then do Pass 3 and 4. Rushed reviews miss more than they catch.

- **Don't flag TODOs unless they're blocking.** A TODO with a ticket number is fine. A bare TODO with no context deserves a question, not a severity flag.

- **Avoid reviewing in a vacuum.** If the PR description explains a deliberate trade-off, don't re-litigate it in the review. Address the description's context, not an imagined ideal.
