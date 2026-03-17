---
name: elixir-code-review
description: Reviews Elixir code for idiomatic patterns, OTP basics, and documentation. Use when reviewing .ex/.exs files, checking pattern matching, GenServer usage, or module documentation.
---

# Elixir Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| Naming, formatting, module structure | [references/code-style.md](references/code-style.md) |
| With clauses, guards, destructuring | [references/pattern-matching.md](references/pattern-matching.md) |
| GenServer, Supervisor, Application | [references/otp-basics.md](references/otp-basics.md) |
| @moduledoc, @doc, @spec, doctests | [references/documentation.md](references/documentation.md) |

## Review Checklist

### Code Style
- [ ] Module names are CamelCase, function names are snake_case
- [ ] Pipe chains start with raw data, not function calls
- [ ] Private functions grouped after public functions
- [ ] No unnecessary parentheses in function calls without arguments

### Pattern Matching
- [ ] Functions use pattern matching over conditionals where appropriate
- [ ] With clauses have else handling for error cases
- [ ] Guards used instead of runtime checks where possible
- [ ] Destructuring used in function heads, not body

### OTP Basics
- [ ] GenServers use handle_continue for expensive init work
- [ ] Supervisors use appropriate restart strategies
- [ ] No blocking calls in GenServer callbacks
- [ ] Proper use of call vs cast (sync vs async)

### Documentation
- [ ] All public functions have @doc and @spec
- [ ] Modules have @moduledoc describing purpose
- [ ] Doctests for pure functions where appropriate
- [ ] No @doc false on genuinely public functions

### Security
- [ ] No `String.to_atom/1` on user input (use `to_existing_atom/1`)
- [ ] No `Code.eval_string/1` on untrusted input
- [ ] No `:erlang.binary_to_term/1` without `:safe` option

## Valid Patterns (Do NOT Flag)

- **Empty function clause for pattern match** - `def foo(nil), do: nil` is valid guard
- **Using `|>` with single transformation** - Readability choice, not wrong
- **`@doc false` on callback implementations** - Callbacks documented at behaviour level
- **Private functions without @spec** - @spec optional for internals
- **Using `Kernel.apply/3`** - Valid for dynamic dispatch with known module/function

## Context-Sensitive Rules

| Issue | Flag ONLY IF |
|-------|--------------|
| Missing @spec | Function is public AND exported |
| Generic rescue | Specific exception types available |
| Nested case/cond | More than 2 levels deep |

## When to Load References

- Reviewing module/function naming → code-style.md
- Reviewing with/case/cond statements → pattern-matching.md
- Reviewing GenServer/Supervisor code → otp-basics.md
- Reviewing @doc/@moduledoc → documentation.md

## Before Submitting Findings

Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) before reporting any issue.
