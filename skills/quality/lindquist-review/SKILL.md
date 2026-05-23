---
name: review
description: Centralizes persona-driven code reviews (Fowler, Torvalds, Carmack, React core, etc.) so Claude can pick or combine expert viewpoints when the user asks for a code review or perspective-specific critique.
allowed-tools: Read, Grep, Glob, Bash
---

# Review Skill

Unifies every reviewer persona into one Skill. Claude activates this Skill whenever code should be reviewed and then "lazy loads" the exact perspective by opening the reference docs linked below or by spawning persona-specific subagents.

## Critical Workflow

**REQUIRED**: Before conducting ANY code review, you MUST load the relevant persona reference file(s) using the Read tool. These references contain the specific review priorities, perspective, and evaluation criteria for each reviewer persona.

1. Collect the code/diff context plus the user's goals (bugs, architecture, performance, etc.).
2. **MANDATORY: Parse reviewer hints** (e.g., "perf, react, typescript") and **READ the matching reference file(s) directly using the Read tool** BEFORE reviewing:
   - AI/ML concerns → Read `references/ai-reviewer.md` FIRST
   - Type system concerns → Read `references/anders-reviewer.md` FIRST
   - Testing/TDD concerns → Read `references/beck-reviewer.md` FIRST
   - Performance/abstraction → Read `references/bjarne-reviewer.md` FIRST
   - Innovation/pragmatism → Read `references/brendan-reviewer.md` FIRST
   - Low-level performance → Read `references/carmack-reviewer.md` FIRST
   - Distributed systems → Read `references/dean-reviewer.md` FIRST
   - Convention/simplicity → Read `references/dhh-reviewer.md` FIRST
   - Refactoring/architecture → Read `references/fowler-reviewer.md` FIRST
   - Collaboration/CI/CD → Read `references/github-reviewer.md` FIRST
   - Abstraction/modularity → Read `references/grace-reviewer.md` FIRST
   - Readability/Python → Read `references/guido-reviewer.md` FIRST
   - Portability/Java → Read `references/james-reviewer.md` FIRST
   - Compiler/tooling → Read `references/lattner-reviewer.md` FIRST
   - Systems/rigor → Read `references/linus-reviewer.md` FIRST
   - Developer joy/Ruby → Read `references/matz-reviewer.md` FIRST
   - Observability/tracing → Read `references/perf-reviewer.md` FIRST
   - React patterns → Read `references/react-reviewer.md` FIRST
   - Go/concurrency → Read `references/rob-reviewer.md` FIRST
   - Unix philosophy → Read `references/unix-reviewer.md` FIRST
3. **Apply the reviewer persona's perspective** by following their specific guidance and priorities from the loaded reference.
4. Cite specific files/lines, flag issues, and provide concrete recommendations.

**DO NOT attempt to conduct a code review without first loading the appropriate persona reference file(s).**

## General Checklist

- Understand inputs/outputs, dependencies, and expected behavior before judging the change.
- Use the allowed tools (`Read`, `Grep`, `Glob`, `Bash`) to inspect implementation, history, and tests.
- Evaluate correctness, safety, performance, maintainability, and user impact.
- Flag missing tests, weak docs, regressions, or architectural drift; propose concrete fixes.
- Summarize findings in severity order, then note risks, questions, and verification steps.

## Multi-Perspective Reviews

When multiple personas are requested (e.g., "review this with Anders and React perspectives"):
- Read each relevant reference file from the list below
- Apply each perspective's priorities and concerns to the code
- Synthesize findings: highlight where perspectives agree or conflict
- Prioritize issues by severity across all perspectives

## Persona References (load on demand)

- **AI Visionaries** - adaptive systems, emergent behavior, data-driven design. [Open instructions](references/ai-reviewer.md)
- **Anders Hejlsberg** - strong typing, language/tooling ergonomics, structured APIs. [Open instructions](references/anders-reviewer.md)
- **Kent Beck** - TDD discipline, rapid feedback loops, adaptive design. [Open instructions](references/beck-reviewer.md)
- **Bjarne Stroustrup** - performance via abstraction, type safety, disciplined engineering. [Open instructions](references/bjarne-reviewer.md)
- **Brendan Eich** - rapid innovation, creative problem-solving, pragmatic experimentation. [Open instructions](references/brendan-reviewer.md)
- **John Carmack** - low-level excellence, graphics/perf tuning, precision thinking. [Open instructions](references/carmack-reviewer.md)
- **Jeff Dean** - planet-scale systems, efficiency, distributed reliability. [Open instructions](references/dean-reviewer.md)
- **DHH** - opinionated conventions, developer autonomy, simplicity over ceremony. [Open instructions](references/dhh-reviewer.md)
- **Martin Fowler** - refactoring readiness, evolutionary architecture, intentional design. [Open instructions](references/fowler-reviewer.md)
- **GitHub Generation** - collaboration hygiene, docs, CI/CD automation. [Open instructions](references/github-reviewer.md)
- **Grace Hopper & Barbara Liskov** - abstraction integrity, substitutability, modular design. [Open instructions](references/grace-reviewer.md)
- **Guido van Rossum** - readability, Pythonic simplicity, pragmatic clarity. [Open instructions](references/guido-reviewer.md)
- **James Gosling** - JVM portability, API stability, backward compatibility. [Open instructions](references/james-reviewer.md)
- **Chris Lattner** - compiler/toolchain innovation, language interoperability, performance. [Open instructions](references/lattner-reviewer.md)
- **Linus Torvalds** - kernel-level rigor, patch discipline, brutally honest feedback. [Open instructions](references/linus-reviewer.md)
- **Yukihiro \"Matz\" Matsumoto** - Ruby aesthetics, human-centric design, joy in code. [Open instructions](references/matz-reviewer.md)
- **Brendan Gregg & Liz Rice** - observability, tracing, data-first performance analysis. [Open instructions](references/perf-reviewer.md)
- **React Core Maintainer** - hooks, concurrent rendering, DX-focused component patterns. [Open instructions](references/react-reviewer.md)
- **Rob Pike** - Go/Unix minimalism, concurrency primitives, composable tooling. [Open instructions](references/rob-reviewer.md)
- **Unix Traditionalist** - small sharp tools, composability, text-first automation. [Open instructions](references/unix-reviewer.md)

Each reference stays out of context until explicitly opened, keeping Claude's context lean while still giving fast access to the original, detailed reviewer guidance.
