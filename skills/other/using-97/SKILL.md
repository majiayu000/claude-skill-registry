---
name: using-97
description: Use when starting any coding task — establishes the 97 trigger map so principles fire when relevant
---

## Overview

**97** distills established programming practice into trigger-based skills, in the spirit of *97 Things Every Programmer Should Know* (O'Reilly, ed. Kevlin Henney; CC-BY-3.0 originals at https://github.com/97-things/97-things-every-programmer-should-know). You have eleven themed skills plus this bootstrap. Each one activates on a specific situation — refactoring, writing tests, designing an API, reviewing code, committing — and brings the relevant principles to bear. Per-skill `principles.md` files list every source. Unofficial companion, not affiliated with O'Reilly or any contributor.

## **CRITICAL: invoke matching skills BEFORE any response or action**

When a user message matches a row in the Trigger Map, you MUST invoke the named skill before taking any other tool action and before writing your reply. Use the `Skill` tool with the **bare skill name** (e.g. `before-you-refactor`). This rule is not negotiable: even a 1% match means invoke. The skill carries the checklist; skipping it means doing the work the default way and losing the point of having 97 installed.

The trigger fires on user words, not on file size or task complexity. If the user says "refactor", invoke `before-you-refactor` — even for a one-line change. If the user says "clean", "test", or "commit", invoke the matching skill. Action-target prompts ("refactor file X", "clean up function Y", "write tests for Z") are the most common trigger and MUST NOT be treated as "just do it" requests.

## Trigger Map

| Skill | Trigger |
|---|---|
| `clean-code` | Writing or reviewing functions, classes, naming, or ≥3 lines of non-trivial logic (NOT typos, config, or test code) |
| `before-you-refactor` | Considering, evaluating, or performing a refactor, restructure, cross-file rename, or cleanup |
| `testing-discipline` | Writing or reviewing tests, designing test data, naming a test, choosing what to assert, or writing test helpers/mocks/fixtures |
| `api-design` | Designing or reviewing a public API, exported function signature, module boundary, exported type, or any contract other code depends on |
| `self-review` | About to commit, finish a task, open a PR, summarize work, or when asked for a review or hand-off of your own work |
| `correctness-traps` | Writing or reviewing error handling, floating-point math, concurrent code, remote calls, singletons/globals, hot-path data structures, or high-volume log statements |
| `security-and-trust-boundaries` | Writing or reviewing code that parses user input, builds SQL/shell commands, handles secrets/credentials, changes auth checks, deserializes untrusted data, or constructs paths/URLs from input |
| `observability` | Writing or reviewing request handlers, RPCs, or background jobs for production; adding tracing, metrics, or structured-log calls; or making diagnosability decisions |
| `build-deploy-and-tooling` | Writing, reviewing, or changing build scripts, CI config, deploy pipelines, repo setup, or evaluating a new tool/dependency |
| `domain-modeling` | Introducing, reviewing, or renaming a top-level type/table/domain concept, or deciding where state lives |
| `working-with-users-and-team` | Gathering or interpreting requirements, estimating effort, or communicating with stakeholders about what to build |

## Priority

1. Your human partner's instructions (CLAUDE.md, GEMINI.md, AGENTS.md, direct prompts) override everything below.
2. **Process and methodology skills run before content skills.** Whatever they live under (`superpowers/`, custom local skills, etc.), skills that decide *whether* and *how to approach* — debugging, verification, planning, TDD, brainstorming — run before 97. 97 skills decide *what makes the code good* once you're writing it. Example: a TDD skill decides whether to write a test; `97/testing-discipline` decides what makes it good. A verification skill decides whether the work is done; `97/self-review` decides whether it was well-considered.
3. **Triggers fire on both writing and reviewing.** When reviewing code without modifying it, run the same checks but report findings to the user rather than editing. When reviewing broadly, invoke the single most relevant skill for the dominant concern, not every possible match.
4. **More specific 97 skill > broader 97 skill.** `before-you-refactor` wins over `clean-code` when both could apply. `testing-discipline` wins over `clean-code` for test code.
5. **Before editing a file you haven't read this session, read it first — and as you read, scan for unsafe code adjacent to your edit** (hardcoded credentials, string-built SQL/shell, unsafe deserialization on untrusted input, swallowed exceptions). If you find one, surface it in your summary to the user; do not silently rewrite outside scope. Editing without reading is the most common avoidable failure mode; reading without scanning is how unsafe code next to your edit ships under your name.
6. **When debugging, defer to a systematic-debugging skill if one is available.** Otherwise fall back to `correctness-traps` for domain-specific bugs and `self-review` step 2 (suspect your own code first) for general debugging.
7. **Apply principles silently.** Do not surface source author names, book titles, or principle IDs (e.g. `97/74`, `Fowler/LongMethod`) in user-facing responses. Citations exist for repo provenance, not for user-facing authority.
8. **Match principle weight to stage and stakes.** Production discipline — resilience patterns, observability, deploy hygiene, security boundaries — matters most when code reaches real users. In MVPs, prototypes, internal dev tools, and one-off scripts, prefer the simplest thing that works. Don't retrofit production discipline onto code whose architecture isn't settled.

## Red Flags

These thoughts mean STOP — invoke the matching skill instead of acting:

| Thought | Reality |
|---|---|
| "This change is small enough that I'll just do it." | Small changes are exactly where the discipline pays off. Invoke. |
| "The user gave me a concrete file or function — I should just go edit it." | Action-target prompts are the most common trigger, not an excuse to skip. Invoke first, then act. |
| "I don't need the skill — I already know this one." | Skills evolve and the checklist matters. Invoke and read the current version. |
| "The trigger almost matches but not quite." | Almost-matches are the easiest to rationalize past. Invoke; the skill will tell you if it doesn't apply. |
| "Two skills could fit; I'll just pick one." | Priority rule 4 — more specific wins. Invoke that one. |

Principles are distilled in our own words from CC-BY-3.0 originals. Plugin code is MIT; see `CONTENT-LICENSE.md` for attribution and takedown policy.
