---
name: consult
description: AI consultation CLI quick reference. Use when running consult commands to check syntax for PR reviews, spec reviews, plan reviews, and general queries across Gemini, Codex, and Claude.
disable-model-invocation: false
---

# consult - AI Consultation CLI

## Synopsis

```bash
consult -m <model> <subcommand> [args] [options]
```

The `-m` / `--model` flag is **always required**.

## Models

| Model | Alias | Speed | Approach |
|-------|-------|-------|----------|
| `gemini` | `pro` | ~120-150s | Pure text analysis, fast |
| `codex` | `gpt` | ~200-250s | Shell command exploration, thorough |
| `claude` | `opus` | ~60-120s | Balanced tool use |

## Subcommands

```bash
consult -m gemini pr 42              # Review a pull request
consult -m codex spec 42             # Review a specification
consult -m gemini plan 42            # Review an implementation plan
consult -m claude general "query"    # General question (quoted string)
```

## Options

```bash
-n, --dry-run              # Show command without running
-t, --type <type>          # Review type (spec-review, plan-review, impl-review, pr-ready, integration-review)
-r, --role <role>          # Custom role from codev/roles/ (without .md extension)
```

## Review Types (--type)

| Type | Stage | Use Case |
|------|-------|----------|
| `spec-review` | conceived | Review spec completeness |
| `plan-review` | specified | Review implementation plan |
| `impl-review` | implementing | Review code implementation |
| `pr-ready` | implemented | Final check before PR |
| `integration-review` | committed | Architect's integration review |

Review type prompts live in `codev/consult-types/` and can be customized.

## Parallel Consultation (3-Way / cmap)

Run all three models in parallel for thorough reviews:

```bash
consult -m gemini spec 42 &
consult -m codex spec 42 &
consult -m claude spec 42 &
wait
```

Or from Claude Code, use **cmap** pattern: three parallel background Bash calls.

## Custom Roles

```bash
consult -m gemini --role security-reviewer pr 42
consult -m codex --role architect general "Review this design"
```

Roles are markdown files in `codev/roles/`. Create your own by adding `.md` files there.

## Common Mistakes

- The `-m` flag is **required** — `consult pr 42` will fail without it
- PR numbers are GitHub PR numbers, not spec numbers
- Spec/plan numbers match the `0042` prefix in filenames (pass just `42`, not `0042`)
- General queries must be **quoted**: `consult -m gemini general "your question here"`
