---
name: red-flags
description: Scans code against 17 named design smells and produces a structured diagnostic report. Use when reviewing a PR for design quality, evaluating unfamiliar code against a comprehensive checklist or when the user asks for a red flags scan. Not for diagnosing why code feels complex (use complexity-recognition) or evaluating whether a PR maintains design trajectory (use code-evolution).
argument-hint: "[file or directory]"
metadata:
  allowed-tools: Read, Grep
---

# Red Flags Diagnostic

When invoked with $ARGUMENTS, scope the scan to the specified file or directory. Read the target code first, then run every flag below against it. Each flag points to a deeper lens from Clairvoyance (https://clairvoyance.fyi). This skill works best when the full collection is installed.

A red flag is a signal, not a diagnosis. It tells you something is wrong but not why. Each flag below points to a deeper lens that identifies the root cause.

## When to Apply

- Before merging a PR or completing a design review
- When code "feels wrong" but the specific problem is unclear
- When evaluating unfamiliar code for design quality
- When asked for a "red flags check" or "design diagnostic"

## The Red Flags

### Structural (4)

#### 1. Shallow Module

Interface isn't much simpler than implementation.

- **Check:** → **deep-modules**
  - Could a caller skip this module and do the work directly?
- **Signals:**
  - More public methods than meaningful internal state
  - Abstract class with only one implementation and no prospect of more
  - Layer that exists "for testability" but adds no abstraction value
  - A split that created more total interface surface than the original
  - Error handling code longer than the happy path
  - Excessive exceptions in a method signature

#### 2. Pass-Through Method

Method forwards arguments to another with a similar signature, adding zero logic.

- **Check:** → **deep-modules**, **abstraction-quality**
  - Does removing the method lose any behavior?
- **Signals:**
  - Method takes N parameters, passes N-1 unchanged
  - Constructor injects collaborators just to delegate
  - Class API mirrors its dependency's API
  - Wrapper adds one behavior, delegates everything else
  - "Wrapper" or "Adapter" classes that add no functionality
  - Many thin layers providing the same abstraction
  - Decorator with nineteen pass-throughs for one behavior

#### 3. Conjoined Methods

Two separate pieces of code that can only be understood together.

- **Check:** → **module-boundaries**
  - Do you flip between two pieces of code to understand either?
- **Signals:**
  - Method A sets up state that method B reads with no interface between them
  - Splitting a method produced fragments that each require the others to make sense

#### 4. Temporal Decomposition

Structure follows execution order, not knowledge ownership.

- **Check:** → **information-hiding**
  - Are boundaries drawn around "steps" rather than "knowledge domains"?
- **Signals:**
  - Module named after a step in a process (Reader, Processor, Writer sharing format knowledge)
  - Decomposition by execution order rather than by knowledge

### Boundary (4)

#### 5. Information Leakage

When a design decision leaks across module boundaries, changing that decision often forces changes in every module that knows about it. The most dangerous leaks are invisible, where two modules share knowledge but no interface acknowledges the dependency.

- **Check:** → **information-hiding**
  - If this format/protocol/representation changes, how many modules need editing?
- **Signals:**
  - Two files that must always be edited together
  - Serialization/deserialization logic split across boundaries
  - Two modules changing in lockstep with no visible API dependency
  - Comments saying "don't forget to also update X"

#### 6. Overexposure

API forces callers to handle things they almost never need.

- **Check:** → **general-vs-special**, **pull-complexity-down**
  - Must callers configure or know about rarely-used features to use common ones?
- **Signals:**
  - Getter/setter pairs exposing internal representation
  - API requiring callers to pass values they don't understand
  - Config docs that say "use the default unless you know what you're doing"
  - Setup code that repeats across every call site
  - Builder requiring 10+ configuration calls
  - API with 5+ parameters when most callers pass the same values for 3
  - Method signature with 3+ exception types
  - Caller must catch an exception the module could have resolved
  - New parameter added to an already-long parameter list

#### 7. Repetition

Same logic appears in multiple places. The next change of this type will require edits everywhere.

- **Check:** → **code-evolution**
  - Would the next change of this type require edits in multiple locations?
- **Signals:**
  - Same change pattern applied in multiple places
  - Copy-pasted code with minor modifications
  - All callers wrapping the same call in identical try-catch blocks
  - Same constant or logic duplicated across many files

#### 8. Special-General Mixture

General mechanism contains knowledge specific to one use case.

- **Check:** → **general-vs-special**
  - Does this module have `if` branches or parameters serving only one caller?
- **Signals:**
  - Boolean parameter that changes behavior for one caller
  - `if` branch added for one specific caller's needs
  - Method name encoding a use case (e.g., `formatForEmailDisplay`)
  - Method designed for exactly one use case when a general-purpose method could replace several
  - "Utility" module that knows details of its callers

### Documentation (2)

#### 9. Comment Repeats Code

All information in the comment is obvious from the adjacent code.

- **Check:** → **comments-docs**
  - Does the comment add anything a competent reader wouldn't get from the code alone?
- **Signals:**
  - Comment using the same words as the entity name

#### 10. Implementation Documentation Contaminates Interface

Interface comment describes implementation details. Signals a leaky abstraction.

- **Check:** → **comments-docs**, **abstraction-quality**
  - Would the comment change if the implementation changed but behavior stayed the same?
- **Signals:**
  - Comment describes _how_ in the interface instead of _what_
  - Interface comment mentions internal data structures or algorithms

### Naming & Abstraction (4)

#### 11. Vague Name

Name so imprecise it doesn't convey useful information.

- **Check (isolation test):** → **naming-obviousness**
  - Seen without context, could this name mean almost anything?
- **Signals:**
  - Thin or generic names like `data`, `info`, `tmp`, `val` at module scope
  - Non-specific container return types where a named class would be self-documenting
  - Method name that doesn't predict what the method does

#### 12. Hard to Pick Name

Struggling to find a precise name isn't a vocabulary problem. It's design feedback.

- **Check:** → **naming-obviousness**
  - Is the item doing one thing but conflating multiple concepts? Doing multiple things but only implying one?
- **Signals:**
  - Name implies a higher-level concept than the implementation honors

#### 13. Hard to Describe

Complete documentation must be long and qualified. Short descriptions come from well-designed abstractions.

- **Check:** → **comments-docs**
  - Can you describe what this does in one sentence without qualifications?
- **Signals:**
  - Long, qualifying interface comment ("does X, except when Y, unless Z")
  - Method with no interface comment (nothing to say, or too much?)

#### 14. Non-obvious Code

This is the meta-flag because every other flag on this list is a specific cause of non-obvious code. When someone reads the code for the first time, they might not be able to tell what it does or why it does it.

- **Check:** → **naming-obviousness**
  - Would a competent developer reading this for the first time understand it?
- **Signals:**
  - Two different names for the same concept in the same module
  - Same name meaning different things in different contexts
  - Short names used far from their declaration
  - Variable reused to mean different things mid-function
  - Code where bugs keep appearing despite fixes
  - Method with visible archaeological layers of organic growth
  - Callers routinely reading the implementation to understand the interface

### Process (3)

#### 15. No Alternatives Considered

Design chosen without comparing meaningfully different approaches.

- **Check:** → **design-it-twice**
  - Were at least two fundamentally different approaches evaluated?
- **Signals:**
  - "This is obviously the right approach" with no alternatives documented
  - Design document with no "alternatives considered" section
  - Two alternatives that are minor variations of each other
  - A design chosen because it was first, not because it was compared
  - Interface defended as "the only way"

#### 16. Tactical Momentum

Changes optimize for speed over design quality.

- **Check:** → **strategic-mindset**, **code-evolution**
  - Does this change leave the system better or just different?
- **Signals:**
  - PR description with no design decisions
  - New feature bolted on rather than integrated
  - "Smallest possible change" treated as sufficient
  - TODO comments marking known shortcuts
  - "Workaround for..." comments

#### 17. Catch-and-Ignore

Error handling that suppresses or discards errors without meaningful action.

- **Check:** → **error-design**
  - Does the catch block do real work, or just make the compiler happy?
- **Signals:**
  - Catch block that only logs and rethrows
  - Caller handles an error by doing nothing or returning a default
  - A module that silently discards all errors from an external dependency

## Canary Flags

_Hard to Pick Name_, _Hard to Describe_, _Non-obvious Code_ and _No Alternatives Considered_ surface during writing, before code review. Catch them early and the structural flags never materialize.

## Review Process

1. **Identify scope**: file, module, PR diff, or class
2. **Scan all flags**: For each: CLEAR, TRIGGERED, or N/A. If triggered: location, principle violated, candidate fix
3. **Structure a report**: Group findings by category (Structural, Boundary, Documentation, Naming/Abstraction, Process). Summarize flags triggered, critical issues and recommended actions.
4. **Follow the arrows**: For each triggered flag, pull in the indicated lens for deeper analysis
5. **Check for syndromes**: Multiple triggered flags may share a root cause. See `references/flag-interaction-map.md` for named clusters. A syndrome points at an architectural issue. Fixing the root cause resolves all flags in the cluster.
6. **Prioritize**: Boundary flags compound over time and infect adjacent code, so fix those first. Canary flags are the cheapest to act on. Structural flags require refactoring but affect a bounded area.
7. **Recommend**: Create a report with prioritized, actionable fixes tied to specific principles.
