---
name: coding
description: Core engineering rules for implementation, refactors, bug fixes, SQL, docs/config edits, commands, and technical guidance, with indexed references for specialized workflows.
---

# Coding (Core + Indexed References)

Use this skill for most engineering work, including implementation, refactors, bug fixes, SQL, docs/config edits, commands, and technical guidance. When a task clearly matches a reference trigger, open that reference before drafting the substantive response (ask brief clarifying questions first if needed).

## Scope & routing
- Use this skill for code changes and technical guidance across languages/tools.
- Prefer to open this SKILL before providing concrete code, SQL, commands, or edits. If the user hasn't provided enough context, you may ask 1-2 clarifying questions first, then open the SKILL before drafting the solution.
- **Hard rule:** if the request mentions `skills/`, `SKILL.md`, or creating/updating a skill, do **not** open coding. Use `skill-creator` instead (including plans/specs unless explicitly plan-only). If coding is already open, stop and hand off.
- Never edit home-level agent instruction files (e.g., `~/.pi/agent/AGENTS.md`, `~/.claude/...`, `~/.codex/...`). Repo-local `AGENTS.md` or `CLAUDE.md` updates are OK only for durable repo-specific context.
- When opening references, use full repo paths like `skills/coding/references/...` (not `references/...`). If a reference read fails, retry once with the full path.
- When a trigger clearly matches, open the referenced file before drafting the substantive response. If you only need clarification, ask first.
- If the user provides a word/length limit, minimize extra reads and keep the response short.

## Quick topic scan (open refs when clearly relevant)
- UI/layout/styling or motion work
- Infra/platform/ops/deploy/secrets/storage work
- Auth/credentials/safety guidance
- PR review or CI failures
- JS/TS runtime or toolchain changes
- Framework-specific guidance (ask which stack if unclear)

## Reference triggers (open when clearly relevant)
If the request explicitly names a framework/tool or clearly falls into a category below, open the matching reference before drafting the substantive response. If the stack/tooling is unclear, ask 1-2 clarifying questions first.

- UI/layout/motion or component design -> `skills/coding/references/frontend-engineering/index.md`
- Infra/platform/ops/deploy/secrets/storage -> `skills/coding/references/platform-engineering/index.md`
- PR review/CI/GitHub -> `skills/coding/references/gh-pr-review-fix.md`
- JS/TS runtime or toolchain -> `skills/coding/references/bun.md`
- Auth/secrets/credentials -> `skills/coding/references/secrets-and-auth-guardrails.md`
- React/Next.js -> `skills/coding/references/react/index.md`
- SolidJS -> `skills/coding/references/solidjs/index.md` (and `skills/coding/references/solidjs/`)
- Utility-class styling (Tailwind) -> `skills/coding/references/frontend-engineering/tailwindcss-full.md`

## Conflicts & precedence

- Skill-creator takes precedence for skill creation/updates (anything under `skills/`).
- Security and secret guardrails override platform or tool-specific docs.
- Follow the repo’s established toolchain and lockfile when incompatible with general preferences.

## 1) Testing and bug fixes

- Every bug fix must include a test that fails before the fix and passes after.
- If a test is genuinely not feasible (rare), state why and how you verified the fix.
- Prefer minimal tests that reproduce the bug and lock in the expected behavior.

## 2) Async consistency

- If a function is async, all I/O inside it must be async.
- Avoid blocking calls in async code (`requests`, `open`, `psycopg2`, `time.sleep`).
- Sync is acceptable for CPU-bound or purely in-memory work.
- Use async equivalents: `httpx.AsyncClient`, `aiofiles`, `asyncpg`, `asyncio.sleep`.

## 3) Input validation at boundaries

- Validate all external input: request bodies, query params, path params, file uploads, webhooks, and external API responses.
- Prefer schema-based validation (Pydantic/Zod); keep validation at boundaries.

## 4) No code injection

- Never execute user-provided code or paths.
- No `eval`, `exec`, `new Function`, dynamic imports, or `shell=True` with user input.
- Sanitize paths; verify ownership before serving resources.

## 5) No secrets access

- Never read or print secrets in conversation context.
- Do not cat/grep `.env` files or secret stores.
- Refer to secret names only; check presence without echoing values.

## 6) Toolchain selection (must follow)

- If `uv.lock` or `pyproject.toml` exists, use `uv` for Python deps and tests (`uv sync`, `uv run pytest`).  
- Never use `pip install` or ad‑hoc venvs unless explicitly asked.  
- For JS/TS, prefer `bun` over npm/yarn/pnpm when possible.  

## 7) SQL safety and query limits

- Always use parameterized queries (no string concatenation or formatting).
- Every SELECT must be bounded (LIMIT, pagination, or a single-row predicate).
- Exceptions: `COUNT(*)`, aggregation with bounded cardinality, or `WHERE id = ?`.

## 8) Avoid race conditions

- Avoid check-then-act and read-modify-write without atomic guards.
- Use transactions, `ON CONFLICT`, `SELECT FOR UPDATE`, and constraints.

## 9) Error handling

- Never swallow exceptions. If you catch, log and re-raise or explain why continuing is safe.
- No empty or silent `except` blocks.

## 10) Configuration and constants

- Do not hardcode magic numbers, URLs, or config values.
- Centralize settings and use named constants.
- Avoid scattered `os.getenv()` calls outside the settings module.

## 11) Architecture and design

- Prefer composition over inheritance; inheritance only for true IS-A or framework requirements.
- Avoid circular imports; keep dependency direction one-way.
- Apply DRY and SOLID: small, focused functions and interfaces.

### DRY and SOLID quick reference

- **DRY**: Extract repeated logic into reusable functions
- **SRP**: One reason to change per function/class
- **OCP**: Extend via abstraction, don't modify existing code
- **LSP**: Subtypes must be substitutable for base types
- **ISP**: Small, focused interfaces - don't force unused methods
- **DIP**: Depend on abstractions, inject dependencies

Checklist:
1. Is this logic duplicated? → Extract it
2. Does this do one thing? → Split if not
3. Am I modifying existing code to extend? → Use abstraction
4. Could I use Protocol instead of ABC? → Prefer Protocol

### Composition over inheritance

Prefer composition (HAS-A) over inheritance (IS-A). Inject dependencies instead of extending classes.

Acceptable inheritance:
- ABCs for interface definition only
- Framework requirements (Django models, Exception subclasses)
- True IS-A relationships (rare)

Red flags:
- Hierarchy > 2 levels deep
- Overriding methods with different behavior
- Mixin classes
- `isinstance()` checks to determine behavior

### Core primitives first

- Prioritize fixes in core primitives (data models, invariants, core utilities, shared interfaces).
- Prefer additive, backward-compatible, reversible changes.
- Avoid patchwork (one-off conditionals, scattered flags, duplicated logic) unless no safe alternative exists.
- If a patch is required, say why the primitive-first path is blocked and propose a follow-up improvement.
- Always name the primitive being improved and how it reduces future patching.

## 12) Frontend safety

- No client-side console logging in production code.
- Frontend must not access databases or secrets; route privileged ops through a backend API.
- Do not use filesystem, process spawning, or dynamic code execution on the client.

## 13) Database changes

- Schema changes must update both schema and documentation.
- Avoid destructive migrations without explicit confirmation.
- Prefer reversible, incremental changes (add → migrate → remove).

## 14) Supabase local safety (if applicable)

- Never rename, delete, or edit applied migrations.
- Destructive commands (`db reset`, `db push --force`) require explicit confirmation.
- Create new migration files for changes instead of editing applied ones.

## 15) Type hints (Python)

- All Python functions require parameter and return type hints.
- Use modern syntax (`list[str]`, `dict[str, int]`, `X | None`).

## 16) Documentation hygiene

- Do not create unnecessary docs files.
- Necessary docs include user-requested docs, compliance/safety docs, spec-driven required specs for multi-step/exploratory work, and self-reporting logs when triggered.
- If spec-driven is active, the spec is required and does not violate this rule.

## References index (deep dives)

- `skills/coding/references/frontend-engineering/index.md` - UI craft, design system rules, components, SolidJS patterns
- `skills/coding/references/platform-engineering/index.md` - platform ops and data infra workflows (GCP, Supabase)
- `skills/coding/references/gh-pr-review-fix.md` - PR review triage + CI fix workflow
- `skills/coding/references/bun.md` - Bun runtime/tooling reference
- `skills/coding/references/secrets-and-auth-guardrails.md` - auth/secret handling and incident response
- `skills/coding/references/solidjs/index.md` and `skills/coding/references/solidjs/` - SolidJS performance and patterns
- `skills/coding/references/frontend-engineering/tailwindcss-full.md` - Tailwind CSS v4 reference
