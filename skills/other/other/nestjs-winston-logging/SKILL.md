---
name: winston-logging-on-change
description: Add, repair, and standardize concise Winston logging in changed NestJS backend code that already uses a shared LoggerService. Use when modifying controllers/services/guards/interceptors/strategies/handlers, improving observability quality, or enforcing safe logging that excludes secrets, tokens, and raw sensitive payloads.
---

# Winston Logging On Change

Apply high-signal, low-noise Winston logs when changing NestJS application logic in projects that already have Winston wiring.

## Workflow

1. Preflight project logger availability.
   - Confirm the project already uses a shared `LoggerService` (or equivalent injected logger wrapper).
   - If logger wiring is missing and the user did not ask for installation, stop and report that this skill only augments existing logging.

2. Locate code touched by the requested change.
   - Focus on changed NestJS runtime units: controllers, services, guards, interceptors, strategies, handlers, and background processors.
   - Do not add logs in unrelated files.

3. Identify meaningful log points introduced or affected by the change.
   - Add logs around operation outcomes, important branch decisions, external dependency calls, retries, and failures.
   - Skip trivial method entry/exit logs and passthrough helper noise.

4. Insert logs with consistent context and level selection.
   - Keep one stable class context per class (for example `AuthService`).
   - Use levels intentionally: `log`/`info` for successful outcomes, `warn` for degraded but handled states, `error` for failures, `debug`/`verbose` only for targeted diagnostics.

5. Enforce sensitive-data safety before finalizing.
   - Never log passwords, hashes, secrets, API keys, JWTs, refresh tokens, cookies, raw request/response bodies, or raw PII.
   - Prefer bounded metadata such as IDs, counts, booleans, operation names, and status codes.

6. Validate final diff quality.
   - Remove duplicate/noisy logs.
   - Ensure each added log helps triage or audit behavior.
   - Confirm no unsafe fields were introduced.

## Logger Usage Contract

Use project conventions for injection and method signatures. Expected common shape:

- `log(message, context?, meta?)` or `info(message, context?, meta?)`
- `warn(message, context?, meta?)`
- `error(message, trace?, context?, meta?)`
- `debug(message, context?, meta?)` or `verbose(message, context?, meta?)`

When logging errors, include a trace/stack string only when it materially improves diagnosis.

## Output Expectations

When applying this skill during a task:

1. Report which files received logging changes.
2. Summarize why each added log is high-signal.
3. Explicitly confirm sensitive fields were excluded.
4. Note any intentional omissions (for example, skipped noisy entry/exit logs).

## Deterministic Guardrails

- Do not introduce a new logging framework in this skill.
- Do not refactor unrelated business logic while adding logs.
- Keep edits minimal and localized to changed behavior paths.
- If logger APIs differ from expected signatures, adapt to project conventions without forcing a rewrite.

## Edit Checklist

- [ ] Confirm shared logger exists before edits
- [ ] Inject/use logger according to project convention
- [ ] Add only high-signal logs tied to changed behavior
- [ ] Include actionable failure logs where relevant
- [ ] Exclude secrets/tokens/raw sensitive payloads
- [ ] Verify final diff for noise and duplication