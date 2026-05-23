---
name: comments-docs
description: Reviews comment quality and documentation practices. Use when the user asks to review comments or documentation, when comments just repeat the code, when something is hard to describe in a sentence, or when writing documentation before code to surface design problems. Evaluates the four comment types, comments-first workflow, and comment rot.
argument-hint: "[file or module path]"
metadata:
  allowed-tools: Read, Grep
---

# Comments & Documentation Review Lens

When invoked with $ARGUMENTS, focus the analysis on the specified file or module. Read the target code first, then apply the checks below.

**Comments are not recording a design that already exists. They are the medium in which the design is discovered.** Code captures mechanism. Comments capture meaning. Even a perfect programming language could not replace them. The information types are distinct.

## When to Apply

- Reviewing code with comments (or conspicuously lacking them)
- When writing new interfaces and considering documentation strategy
- When comments feel useless or redundant
- When a module is hard to use despite having documentation

## Core Principles

### The Guiding Principle

> "Comments should describe things that aren't obvious from the code." — John Ousterhout, _A Philosophy of Software Design_

"Obvious" is from the perspective of someone reading the code for the first time, not the author. If a reviewer says something isn't obvious, it isn't. Don't argue, clarify.

### Four Comment Types

#### 1. Interface Comments

_What_ and _why_ for callers. Must be sufficient to use the interface without reading implementation. Operate at two levels: **intuition** (a sentence giving the mental model) and **precision** (argument/return docs more specific than the code). A comment that says "offset" does not specify inclusive vs exclusive.

#### 2. Implementation Comments

_What_ a block does (high-level) and _why_, not line-by-line _how_. For variable comments, **think nouns, not verbs**: describe what the variable represents, not how it's manipulated.

#### 3. Cross-Module Comments

Document dependencies spanning module boundaries. Place at a convergence point, or maintain a central designNotes file with labeled sections per topic and short pointer comments in the code (`// See "Zombies" in designNotes`). Neither approach is perfect. This is a genuinely unsolved problem.

#### 4. Data Structure Member Comments

Each field should have a comment capturing what's not obvious from the type or name: what it represents, units, valid ranges, boundary conditions (inclusive/exclusive), nullability, resource ownership (who frees/closes), invariants and relationships to other fields.

### "Comment Repeats Code" Test

Useful comments say things the code does not. If another developer could write the same comment just by reading the surrounding code, it doesn't need to exist and should be deleted.

Rephrasing an entity name doesn't cut it. A comment about `fetchUserProfile` that says "Fetches the user profile" is still noise.

### Hard-to-Describe Signal

**When a comment must be long, qualified, or convoluted, that's a design problem, not a writing problem.** Simple descriptions come from well-designed abstractions.

| Comment                 | Implementation | Signal                                          |
| ----------------------- | -------------- | ----------------------------------------------- |
| Short, simple           | Substantial    | Deep — hides complexity well                    |
| Long, complicated       | Short          | Shallow — description nearly as complex as code |
| Must describe internals | Any            | Leaky abstraction                               |

### Comments-First Workflow

Write interface comments before method bodies. If a comment is hard to write, the abstraction is wrong, and you find out before writing the implementation. Comments written after-the-fact produce worse results. Your memory of your intent has faded and you end up justifying the code you wrote instead of capturing why you wrote it.

1. **Class interface comment**: purpose and abstraction, before anything else
2. **Public method comments + signatures**: bodies empty. Iterate until structure feels right
3. **Instance variable declarations + comments**: once interface stabilized
4. **Fill in method bodies**: implementation comments as needed. Comments are already done

See the [full workflow](references/comments-first-workflow.md) for the complexity canary tests and cost analysis.

### The Four Excuses

- **"Good code is self-documenting."** A signature gives you types and parameter names. It does not tell you when to call the method, what the return value means, or why the method exists. That information lives in comments. When readers must study an implementation to use it, a module offers no real abstraction.
- **"I don't have time."** Comments add at most 10% to typing time. Reframed: "I don't have time to design."
- **"Comments get out of date."** Manageable with discipline at the point of change and code review.
- **"All comments I've seen are worthless."** Solvable with technique, not intention.

### Why "Comments Are Failures" Is Wrong

Robert Martin argues in _Clean Code_ that comments are failures and signs that the code wasn't expressive enough. His alternative is **method extraction**: replace a commented block with a well-named method.

Method names work for simple operations. `extractSubstring` is better than a comment above a five-line block. But names can hit a ceiling. A name can say _what_ a method does but it won't say _why_, describe the preconditions or explain non-obvious constraints. A name alone cannot carry that, but a comment can. Taken to the extreme, method extraction encourages splitting code into infinite small methods, which can increase complexity rather than reduce it.

The issue ends up being cultural. If a team thinks comments are "junk" or fail to be "real documentation", then they avoid creating them and useful design context goes unrecorded. The best place for design context is right next to the code it describes, not in a separate document that the reader may never find or even know to look for.

## Review Process

1. **Classify existing comments**: Interface, implementation, cross-module, or data structure member?
2. **Check for repeats-code**: Same words as the entity name?
3. **Check for missing interface comments**: All public interfaces documented? Both intuition and precision?
4. **Evaluate hard-to-describe**: Long or convoluted comments? Investigate the design.
5. **Check cross-module docs**: Dependencies documented? Canonical location?
6. **Recommend**: Delete noise, add missing interface comments, flag hard-to-describe as design problems

Red flag signals for comments are cataloged in **red-flags** (Comment Repeats Code, Implementation Documentation Contaminates Interface, Hard to Describe, Information Leakage).

## References

For deeper coverage, load on demand:

- [Comments-first workflow](references/comments-first-workflow.md): Full 6-step process, complexity canary tests, cost analysis, and why after-the-fact comments are a red flag.
