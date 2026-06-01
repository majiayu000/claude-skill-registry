---
name: anti-slop
description: >
  · Audit AI-generated code slop: hallucinated APIs, over-abstraction, duplicate code, test theater, noisy comments. Triggers: 'slop', 'AI-generated code', 'cleanup', 'overengineered'. Not for prose (use anti-ai-prose).
license: MIT
compatibility: "None - works on any codebase"
metadata:
  source: iuliandita/skills
  date_added: "2026-03-25"
  effort: medium
  argument_hint: "<file-or-pattern>"
---

# Anti-Slop: Polyglot Code Quality Audit

Detect and fix patterns that make code look machine-generated, over-abstracted, unnecessarily verbose, or fluently wrong. The goal is code that reads like a competent human wrote it - minimal, intentional, grounded, and clear.

This skill covers: **TypeScript/JavaScript**, **Python**, **Bash/Shell**, **Rust**, **Docker/Containers**, and **Infrastructure as Code** (Terraform, Ansible, Helm, Kubernetes manifests). The universal patterns apply everywhere; language-specific sections add targeted checks.

## When to use

- Reviewing code that feels machine-generated, bloated, or oddly generic
- Simplifying code after an AI-heavy implementation pass
- Auditing comment noise, naming quality, over-abstraction, and dependency creep
- Looking for "ugly but technically works" code that still hurts readability or maintainability
- Looking for AI-native tells: hallucinated APIs, schema drift, fallback laundering, and tests that only ratify the implementation

## The Three Axes of Slop

Every finding falls into one of three categories:

1. **Noise** - bulk without value (redundant comments, boilerplate, unnecessary types/annotations)
2. **Lies** - subtly wrong or outdated (hallucinated APIs, deprecated patterns, stale deps)
3. **Soul** - lacks taste (over-abstraction, generic names, defensive overkill)

## When NOT to use

- Correctness, logic, or race-condition bugs - use **code-review**
- Security vulnerabilities, secret scanning, or auth review - use **security-audit**
- One-off prompt authoring or prompt templates - use **prompt-generator**
- Session-end documentation maintenance - use **update-docs**
- Prose audit of docs, READMEs, wikis, emails, or creative writing - use **anti-ai-prose**
- Safe-deletion or LOC-slimming requests (removing dead code, shrinking file count) - use **code-slimming**

## AI Self-Check

Before returning any anti-slop audit, verify:

- [ ] **Rewrites compile/parse**: every "after" code snippet is syntactically valid in the target language
- [ ] **Security patterns not flagged**: auth, CORS, input validation, rate limiting, TLS - these are correct even if verbose (check the "What NOT to Flag" list)
- [ ] **Framework idioms respected**: what looks like over-abstraction might be the framework's expected pattern (e.g., Next.js layouts, Django class-based views, Terraform module structure)
- [ ] **Existing project conventions preserved**: the repo's naming style, comment density, and abstraction level take precedence over generic "clean code" preferences
- [ ] **Severity is honest**: don't inflate P3 findings to P2 to pad the report
- [ ] **No hallucinated replacements**: verify that suggested modern alternatives actually exist in the target language version (e.g., `match` requires Python 3.10+, `LazyLock` requires Rust 1.80+)
- [ ] **Test theater distinguished from correctness**: implementation-mirroring tests, mock-heavy ceremony, and snapshots with no semantic assertions belong here; actual failing behavior still belongs to code-review
- [ ] **Structural duplication sweep done**: compare same-role modules/classes across sibling dirs (`providers`, `targets`, `sources`, `clients`, `registry`) and either report near-twins or note why the duplication is intentional
- [ ] **Current source checked**: dated versions, CLI flags, API names, and support windows are verified against primary docs before repeating them
- [ ] **Hidden state identified**: local config, credentials, caches, contexts, branches, cluster targets, or previous runs are made explicit before acting
- [ ] **Verification is real**: final checks exercise the actual runtime, parser, service, or integration point instead of only linting prose or happy paths
- [ ] **Routing overlap checked**: overlapping skills, trigger terms, and "When NOT to use" boundaries are checked before returning guidance
- [ ] **Spec claims verified**: claims about tool behavior, output contracts, or repo conventions are checked against current docs, scripts, or skill files
- [ ] **API/grounding verified**: suspicious helpers, flags, imports, config keys, and schema claims are checked against local types, generated schema, lockfiles, `--help` output, or official docs before being called hallucinations
- [ ] **Test theater separated**: tests that assert mocks or snapshots only are distinguished from tests proving behavior

---

## Performance

- Focus review on changed files and shared abstractions before scanning unrelated code.
- Collapse repeated slop patterns into one finding with examples, not one finding per occurrence.
- Use cheap static checks first, then run expensive tests only where they can confirm a real risk.

---

## Best Practices

- Prefer deleting unnecessary abstraction over adding a new abstraction to hide it.
- Treat duplicate code as a finding only when it creates real divergence or maintenance risk.
- Require concrete failure modes; style dislike is not slop.

## Workflow

### Step 1: Scope the audit

Default scope based on context:
- If invoked right after writing code in this session -> **self-check** (review what you just wrote)
- If there are uncommitted changes (`git diff --name-only`) -> **recent changes**
- Otherwise -> ask the user

Available scopes:
- **Full codebase audit** - scan everything, report by category
- **Recent changes** - check git diff or recent commits
- **Specific files/dirs** - targeted review
- **Self-check** - review code you just wrote in this session

### Step 2: Detect languages

Scan the project to determine which languages are present. Apply the universal patterns to everything, then layer on language-specific checks. Don't apply TS checks to Python code or vice versa.

### Step 3: Run mechanical linters first (if available)

Before scanning for slop, run standard linters to clear the low-hanging fruit:
- **Shell**: `shellcheck`
- **Python**: `ruff check` / `mypy`
- **TypeScript**: `eslint` / `tsc --noEmit`
- **Terraform**: `terraform validate` / `tflint`
- **IaC schema tools**: `ansible-lint`, `helm lint`, `kubectl apply --dry-run=client`, `kubeconform` when available
- **Structural patterns**: `ast-grep` (tree-sitter powered AST search - write rules to catch restating comments, dead code, hallucinated imports across languages. Install: `npm i -g @ast-grep/cli`. If your tool ecosystem provides `ast-grep` helper skills or templates, use them.)

Linters handle syntax issues, unused imports, and known anti-patterns mechanically. This skill focuses on what linters can't catch: taste, over-abstraction, naming quality, unnecessary complexity, and stale idioms. Don't duplicate what a linter already covers.

**Per-project tools** (eslint, tsc, vitest, prettier) are project devDeps, not system tools. If they're not in the project's `package.json`/`devDependencies`, mention to the user what's missing and let them decide whether to install. Don't run linters that aren't set up.

### Step 4: Scan for patterns

Use Grep, Glob, and Read. Read files before flagging - context matters. A pattern that looks like slop in isolation might be justified.

Before finalizing, do one explicit structural pass:
- Compare same-role files across sibling directories (`foo/emby.ts` vs `foo/jellyfin.ts`, multiple `registry.ts` files, provider adapters, target wrappers)
- Look for near-twin modules/classes with the same method set and only renamed nouns, IDs, or client types
- If you find a repeated pattern across many files, report one representative example and mention the spread instead of silently dropping it

Classify each finding by axis (Noise/Lies/Soul - see above), action, and severity:

**Action:**
- **Fix** - clearly wrong or wasteful, should change
- **Consider** - judgment call, present it and let the user decide
- **Fine** - looks like slop but is justified (note why and move on)

**Severity** (determines report ordering - high first):
- **P1** - strongly suggests fabricated or ungrounded code (hallucinated APIs, schema drift, silent swallowing used to hide uncertainty, fallback laundering)
- **P2** - maintainability (over-abstraction, generic naming, missing error context, logic duplication)
- **P3** - style (verbose patterns, comment noise, redundant annotations, barrel files)

### Step 5: Report and fix

Present findings grouped by category. For each Fix-level item, show the concrete replacement. Don't just point at problems - show the better version.

---

## Universal Patterns (All Languages)

### 1. Comment Slop (Noise)

The single biggest tell. Comments that narrate what code does instead of why.

**Detect:**
- Comments restating the next line ("Initialize array", "Loop through items", "Return result", "Set variable")
- Hedging ("This should work", "This might need updating", "TODO: review this")
- Overconfident assertions ("This is the most efficient approach", "This handles all edge cases")
- Section dividers adding no information (`# --- Helper Functions ---` above obvious helpers)
- Docstrings/JSDoc on every function when signatures are self-documenting
- Inline comments on every block in a shell script or Terraform file

**AI agent tells** (rarely appear in human code):
- Docstrings on every function regardless of complexity (`add(a, b)` -> "Returns the sum")
- Restating the next line in English on every block; section headers in short functions
- `@param` descriptions repeating the parameter name; comments on obvious ops (`// increment counter`)
- Convention blindness: camelCase in a snake_case repo, JSDoc in a no-JSDoc project

**Fix:** Delete obvious comments. Keep only *why* comments - business logic, workarounds, gotchas, non-obvious decisions. If code needs a *what* comment, rewrite the code. A 20-line function needs zero comments if the names are good. A 200-line module might need 3-4.

**Exception:** Comments explaining workarounds for bugs, API quirks, or platform limitations are valuable. Also: shell scripts benefit from more comments than typical code because the syntax is less self-documenting.

### 2. Defensive Overkill (Soul)

Error handling or validation that protects against impossible scenarios.

**Detect:**
- Try/catch (or try/except) that catches, logs, and re-raises without adding context
- Null/nil/None checks after the type system or prior logic already guarantees non-null
- Input validation deep inside internal functions (validate at boundaries, trust internally)
- Fallback values for things that can't be missing
- Shell scripts wrapping every command in `if ... then ... fi` instead of using `set -e`
- Terraform `try()` / `can()` wrapping expressions that can't fail

**AI agent tells** (guardrails humans would never write):
- Try/catch wrapping every function body, catching `Error` with a generic log message
- Null checks on values from functions you control that never return null
- Input validation on internal helpers that only receive pre-validated data
- Fallback defaults for required config that should crash loudly if missing
- `if (!response.ok)` after every internal call, not just HTTP boundaries

**Fix:** Remove pointless error handling. Validate at system boundaries (user input, API responses, env vars, external data), not on every internal call. If a catch block doesn't add context, retry, or recover - delete it.

**Exception:** Defensive checks on external data (network responses, deserialized JSON, user input, third-party libraries) are correct. Security patterns (auth, CORS, SSRF protection, input sanitization) should never be flagged.

### 3. Over-Abstraction (Soul)

Creating abstraction layers for problems that need 10 lines of direct code.

**Detect:**
- Wrappers that just forward to one thing with no added logic
- Abstract/base classes with a single concrete implementation
- Factory functions that always produce the same type
- Separate files for types/interfaces only used in one place
- "Service" or "Manager" classes wrapping a single operation
- Terraform modules wrapping a single resource with no added logic
- Ansible roles with one task file
- Shell functions called exactly once

**Fix:** Inline small abstractions. Delete wrappers that add no logic. A little repetition beats a premature abstraction.

**Exception:** Abstractions for testing (dependency injection), multiple implementations, or isolating external deps are fine even with one current impl.

### 4. Verbose Patterns (Noise)

Using 10 lines where 3 would do.

**Detect (language-agnostic):**
- Unnecessary intermediate variables: `result = foo(); return result`
- Ternaries wrapping boolean returns: `return x ? true : false`
- Manual iteration that the language has built-ins for
- Copy-pasting code blocks with tiny variations instead of parameterizing

**Fix:** Use the idiomatic short form for the language. See language-specific sections for details.

### 5. Generic Naming (Soul)

Names that could mean anything: `data`, `result`, `response`, `item`, `temp`, `value`, `info`, `handler`, `manager`, `utils`, `helpers`, `common`, `misc`.

**Detect:**
- Variables with generic names outside tiny scopes (2-3 line lambdas are fine)
- Files named `utils.*`, `helpers.*`, `common.*`, `misc.*` (junk drawers)
- Functions named `handle_x`, `process_x`, `manage_x` without domain specificity
- Terraform resources named `this` or `main` when there are multiple of the same type
- Ansible variables named `item` or `result` in complex plays

**Fix:** Use domain-specific names. `data` -> `active_subscriptions`. `utils.sh` -> split by concern or inline.

**Exception:** Generic names in genuinely generic code (a `map()` callback, a type parameter `T`, a Terraform module's `this` when it's the only resource of that type).

#### Module-level smells

God modules are a structural form of generic naming: the file itself has no clear identity.

**Detect:**
- Files named `utils.*`, `helpers.*`, `common.*`, `misc.*` with 30+ functions
- A single module mixing unrelated domains (auth + formatting + DB queries + file I/O)
- `utils.py` with functions spanning 5+ distinct concerns

**Fix:** Split by domain concern, not by arbitrary grouping. A 47-function `utils.py` typically contains 3-5 coherent modules (`auth_utils.py`, `format_helpers.py`, `db_queries.py`). Steps: (1) cluster functions by what they operate on or what domain they serve, (2) create a module per cluster, (3) update imports. Do not create a new junk-drawer module - each split module should have a name that describes its single concern.

**Exception:** Genuinely cross-cutting helpers (e.g., a `retry()` decorator used by 8 modules) can stay in a small, tightly scoped `core.py` or `retry.py`.

### 6. Logic Duplication (Lies)

Same logic written slightly differently in multiple places - a telltale sign of context-free generation.

**Detect:**
- Near-identical helper functions in different files
- Near-twin modules for adjacent integrations/providers where only names, IDs, or injected client types change
- Registry classes with the same `Map` + `register/get/all|list/clear` shape repeated across domains
- Thin wrappers/adapters that repeat the same mapping code for multiple backends
- Same validation logic in multiple handlers/routes
- Repeated inline formatting/parsing across modules
- Terraform `locals` blocks computing the same thing in different modules
- Ansible tasks doing the same thing with different variable names

**Fix:** Consolidate into a shared helper/factory/base module or keep one representative implementation and parameterize the differences. But only if truly the same - slight variations might be intentional.

**Exception:** Sometimes duplication is clearer than a contorted abstraction, especially when integrations are likely to diverge. Still surface it as a **Consider** finding if the files/classes are near-twins today.

### 7. Stale Patterns (Lies)

Code that was fine 5 years ago but has better alternatives now.

**Fix:** Use the modern equivalent. Check compatibility (language version, runtime, provider versions) before changing. See language-specific sections for concrete examples.

### 8. Error Handling Anti-Patterns (Noise + Lies)

**Detect:**
- Catch/except blocks that log a generic message and continue (error is lost)
- Every function wrapped in its own error handler (handle at boundaries instead)
- Errors caught and re-raised as new exceptions, losing the original stack
- Silent swallowing: `.catch(() => {})`, `except: pass`, `2>/dev/null` on critical commands
- Shell scripts without `set -e` that check `$?` after every command manually

**Fix:** Handle errors at boundaries. Let errors propagate through internal code. When catching, either recover or add context and re-raise.

**Exception:** Fire-and-forget operations legitimately swallow errors. Comment why.

### 9. Cross-Language Leakage (Lies)

AI models trained on multiple languages bleed idioms across boundaries. A reliable tell for AI-generated code.

**Detect:**
- JavaScript patterns in Python: `.push()`, `.length`, `.forEach()`, `===`, `console.log()`
- Java patterns in non-Java: `.equals()`, `.toString()`, `System.out.println()`, `public static void`
- Python patterns in JavaScript: `len()`, `print()`, `elif`, `def `, using `#` comments in JS
- Shell patterns in Python: backtick usage, `$VARIABLE` syntax
- Go patterns elsewhere: `fmt.Println()`, `:=` assignment, `func ` in non-Go

**Fix:** Replace with the target language's idiom. This is almost always an AI generation artifact - humans don't accidentally write `.push()` in Python.

### 10. Plausible Hallucinations / Schema Drift (Lies)

Code that looks locally plausible because the names sound right, but it is not grounded in the actual API, schema, CLI, provider, or framework version in use.

**Detect:**
- Functions, methods, imports, CLI flags, config keys, or resource arguments that look real but are not in local types, tool help, or docs
- Mixing adjacent ecosystems: provider arguments from the wrong Terraform resource, Helm values keys that the chart never reads, Kubernetes fields from a different API version, Ansible params from the wrong module or collection
- Compatibility blind spots: using a modern API without checking the repo's runtime/tool version
- "Fixes" that paper over missing understanding with `try()`, optional chaining, default fallbacks, or broad catches instead of verifying the contract

**Fix:** Check the actual contract first - local types, generated schema, `--help`, provider docs, chart values, API version docs. Delete invented surface area. Prefer loud failure for required config over fantasy defaults.

**Exception:** Compatibility shims for multi-version support are fine when the codebase clearly supports multiple runtimes, provider versions, or API levels.

### 11. Test Theater / Self-Confirming Tests (Lies + Soul)

Tests can be slop too. A green test suite is not evidence if the tests were generated from the implementation and only mirror what already exists.

**Detect:**
- Tests written after implementation that assert the exact control flow, fixture data, or internal call graph of the current code
- Mock-heavy tests where every dependency is stubbed and the only assertions are call counts, method names, or log messages
- Snapshots or golden files used as a substitute for semantic assertions
- "Happy path only" tests paired with broad catches, default fallbacks, or defensive code that never gets exercised
- Generated tests with high coverage but no clear link to the spec, acceptance criteria, or boundary behavior

**Fix:** Prefer spec-driven tests, behavior-level assertions, and a real RED phase. Keep mocks at the edges. If the test would still pass when the implementation is wrong in the same way, it is ceremony, not protection.

**Exception:** Adapter tests, logging/metrics assertions, and contract tests may legitimately assert call shapes when that contract is the behavior under test.

---

## Language: TypeScript / JavaScript

Read `references/typescript.md` for the full TS/JS pattern catalog. Key highlights:

- **Type abuse**: redundant annotations where inference works, `any` instead of `unknown`, enums instead of const objects/unions, missing `satisfies` / `as const`
- **Stale patterns**: `require()` in ESM, `var`, `React.FC`, class components, `PropTypes` alongside TS, `.then()` chains, `namespace`
- **Verbose**: `for` loops that should be `.filter().map()`, `Object.keys().forEach()` instead of `for...of`, classes for stateless logic
- **Dependency creep**: `node-fetch` when `fetch` is global, `uuid` when `crypto.randomUUID()` exists, two libs for the same concern
- **AI-native tells**: `try/catch` around deterministic local code, `new Promise(async ...)`, fallback defaults for required env/config, tests that only assert mocks or snapshots
- **Barrel files**: `index.ts` re-exporting everything in small directories

## Language: Python

Read `references/python.md` for the full Python pattern catalog. Key highlights:

- **Class-for-everything disease**: stateless classes that should be plain functions/modules
- **Exception anti-patterns**: bare `except:` catching KeyboardInterrupt/SystemExit, `except Exception as e: logger.error(e); raise` (adds nothing), type/None checks on typed parameters (e.g., `if user_id is None` when the signature says `int`), broad try/except wrapping its own explicit `raise` statements
- **Stale patterns**: `os.path` instead of `pathlib`, `.format()` instead of f-strings, `%` formatting, `if/elif` chains instead of `match` (3.10+), `typing.Optional[X]` instead of `X | None` (3.10+)
- **Type hints**: `Any` used to bypass type errors, redundant hints on obvious assignments, overly complex `TypeVar` gymnastics
- **Verbose**: manual dict/list building instead of comprehensions, nested `if` instead of early returns, `lambda` assigned to a variable (just use `def`), redundant docstrings restating the function signature
- **Dependency creep**: `requests` for a single GET when `urllib` works, `python-dotenv` when `os.environ` is fine
- **AI-native tells**: `dict.get(..., {})` chains laundering missing invariants, catch-log-reraise noise, mock-heavy tests with no behavioral assertion

## Language: Bash / Shell

Read `references/shell.md` for the full Shell pattern catalog. Key highlights:

- **Missing safety**: no `set -euo pipefail`, unquoted variables, no `shellcheck` compliance
- **Useless use of cat**: `cat file | grep` instead of `grep file`
- **Stale patterns**: backticks instead of `$()`, `expr` instead of `$(())`, `[ ]` instead of `[[ ]]` in bash/zsh, parsing `ls` output
- **Over-defensive**: `if command; then ... fi` on every line instead of `set -e`, manual `$?` checks
- **Verbose**: `echo "$var" | grep` instead of `[[ "$var" == *pattern* ]]`, external tools for built-in operations
- **AI-native tells**: hallucinated flags/subcommands copied from adjacent CLIs, `2>/dev/null || true` used to hide uncertainty, heredoc-heavy automation instead of checked files/templates

## Language: Infrastructure as Code

Read `references/iac.md` for the full IaC pattern catalog covering Terraform, Ansible, Helm, and Kubernetes manifests. Key highlights:

- **Terraform**: over-modularizing, redundant `depends_on`, not using `locals`, unpinned provider versions, invented resource arguments, provider/version hallucinations
- **Ansible**: `command`/`shell` when a module exists, `ignore_errors: true` everywhere, registering variables never used, not using handlers, invented module params or wrong collections
- **Helm**: hardcoded values in templates, `tpl` for static strings, `.Values` spaghetti without defaults, chart version not pinned, values keys that the chart never consumes
- **Kubernetes**: no resource requests/limits, `latest` tags, no namespace, imperative `kubectl run/create` in automation, no probes, mismatched `apiVersion`/field combinations

## Language: Rust

Read `references/rust.md` for the Rust pattern catalog. Key highlights:

- **Clone abuse**: `.clone()` to dodge the borrow checker - the #1 AI-Rust tell
- **Error type proliferation**: custom error enums for every module instead of `anyhow`/`thiserror`
- **Overly generic trait bounds**: `T: Display + Debug + Clone + Send + Sync` when only `Display` is used
- **Verbose**: `match` with two arms instead of `if let`, explicit `return` at function end, manual Option/Result matching instead of combinators
- **Unsafe overuse**: `unsafe` blocks without `// SAFETY:` comments, `transmute` when `as` works
- **Stale**: `extern crate`, `#[macro_use]`, `try!()`, `lazy_static` instead of `std::sync::LazyLock` (1.80+)

## Language: Docker / Containers

Read `references/docker.md` for Dockerfile and Compose pattern catalog. Key highlights:

- **Fat images**: no multi-stage build, build tools in final stage, `COPY . .` before dep install (cache busting)
- **Layer waste**: separate `RUN` per package, `ADD` for local files, `RUN cd` instead of `WORKDIR`
- **Security**: running as root, `chmod 777`, secrets in build args/env, missing `.dockerignore`
- **Compose bloat**: `container_name` everywhere, `restart: always` without healthchecks, `depends_on` without conditions, hardcoded ports
- **Stale**: old base image versions, `MAINTAINER` directive, ENTRYPOINT+CMD confusion

## Other Languages

For Go and other languages without dedicated reference files: apply the universal patterns (sections 1-11) only. Note in the report that language-specific checks were skipped. Common cross-language tells still apply - over-abstraction, comment noise, cross-language leakage, schema drift, and error handling anti-patterns look similar everywhere.

## Research & Citations

Read `references/research-sources.md` for statistics, source citations, and deeper context on the "no soul" problem. Use when the user wants data to back up findings.

---

## What NOT to Flag

These look like slop but aren't:

- **Security patterns**: auth, CORS, SSRF protection, input validation at boundaries, rate limiting, TLS configuration, RBAC policies. Correct even if "defensive".
- **Explicit types/annotations on public interfaces**: function signatures, exported types, API contracts benefit from explicitness.
- **Abstractions that enable testing**: interfaces with one implementation for dependency injection.
- **Workaround comments**: "works around X bug", "API requires this", "platform-specific" - institutional knowledge.
- **Defensive checks on external data**: network responses, user input, deserialized data, third-party library output.
- **Shell verbosity for clarity**: complex pipelines benefit from intermediate variables and comments.
- **Terraform `count`/`for_each` on single resources**: might be conditional (`count = var.enabled ? 1 : 0`).
- **Ansible `when` conditions that seem obvious**: often guarding against cross-platform differences.
- **Compatibility shims**: version- or provider-specific branches may look repetitive because they support multiple real targets.
- **Contract-level tests**: asserting exact API payloads, SQL, CLI args, or emitted metrics is fine when that contract is the thing being tested.

---

## Output Contract

See `skills/_shared/output-contract.md` for the full contract.

- **Skill name:** ANTI-SLOP
- **Deliverable bucket:** `audits`
- **Mode:** always-on. Every invocation emits the full contract - boxed inline header, body summary inline plus per-finding detail in the deliverable file, boxed conclusion, conclusion table.
- **Deliverable path:** `docs/local/audits/anti-slop/<YYYY-MM-DD>-<slug>.md`
- **Severity scale:** reduced subset of the shared scale - `P1 | P2 | P3` with slop-specific meanings (P1 fabricated/ungrounded, P2 maintainability, P3 style; see the Workflow classification). No P0: slop is never a build or security breaker - route those to **code-review** / **security-audit**.

## Related Skills

- **code-review** - finds bugs and correctness issues. Anti-slop finds quality and style issues.
  If it would cause incorrect behavior, it's a code-review finding. If it's ugly but correct,
  it's anti-slop.
- **security-audit** - finds vulnerabilities. Defensive code that looks like "overkill" may be
  correct security practice. Check the "What NOT to Flag" list before flagging security patterns.
- **full-review** - orchestrates code-review, anti-slop, security-audit, and update-docs in
  parallel. Anti-slop is one of the four passes.
- **update-docs** - handles documentation maintenance. Anti-slop focuses on code quality;
  update-docs focuses on keeping docs accurate and trimmed.
- **anti-ai-prose** - audits prose for AI writing tells (vocabulary, syntax, tone, formatting).
  Anti-slop audits code. Together they cover "does this repo read as machine-generated" across
  both code and documentation.
- **code-slimming** - handles safe-deletion and LOC-slimming passes (removing dead code, shrinking
  file count). Use it when the goal is reducing volume; use anti-slop when the goal is quality.

---

## Reference Files

- `references/typescript.md` - TypeScript and JavaScript anti-slop patterns
- `references/python.md` - Python anti-slop patterns
- `references/shell.md` - shell and script anti-slop patterns
- `references/iac.md` - Terraform, Ansible, Helm, and Kubernetes anti-slop patterns
- `references/rust.md` - Rust anti-slop patterns
- `references/docker.md` - Dockerfile and Compose anti-slop patterns
- `references/research-sources.md` - supporting research, citations, and external context

---

## Output Format

````markdown
## Anti-Slop Audit: [scope]

### Findings

#### [Category Name] ([count] items)

**[action]** ([severity], [axis]) `path/to/file:line` - [description]
```[language]
// before
[code snippet]

// after
[improved code snippet]
```

### Summary
- X findings across Y files
- [top-level observations about codebase health]
````

Keep it concise. Show the diff, not a paragraph explaining it.

---

## Rules

- **Keep correctness out of scope.** If it would actually break behavior, route it to code-review instead of padding this report.
- **Flag AI-native lies even when they look polished.** Hallucinated APIs, schema drift, and self-confirming tests belong here when the problem is lack of grounding or taste rather than a demonstrated failing behavior.
- **Keep security out of scope.** Defensive code often looks verbose on purpose. Do not flag it casually.
- **Read before judging.** A pattern that looks generic in isolation may be justified by framework or project constraints.
- **Ground hallucination claims.** Use local types, schema, lockfiles, generated docs, or tool help before saying a flag/resource/API is fake.
- **Do not bury structural duplication.** If near-twin modules or repeated registry/wrapper shapes appear, surface at least one representative finding even when higher-severity hallucination findings dominate the report.
- **Prefer concrete rewrites.** If you flag a pattern, show the simpler version.
- **Run the AI Self-Check.** Verify findings against the checklist before returning the audit.
