---
name: agf-running-sit-tests
description: Use when an execution-layer dev (frontend-dev / backend-dev / ai-agent-dev / ml-engineer / miniapp-dev) has finished feature code + Unit tests and is about to enter code-review. Provides the SIT scope, environment, AC-driven integration walk, and evidence sink (progress/<role>.md). SIT is now a dev-owned step, not a separate QA stage.
---

# Running System Integration Tests (SIT)

Use this skill when:

- A dev finished feature code + Unit tests and is about to enter code-review
- A dev needs to verify a fix doesn't regress integration (API ↔ DB ↔ external)

## What SIT is — and is not

**SIT** verifies that **independently-developed components compose correctly** — frontend ↔ backend ↔ DB ↔ external services. It is NOT:

- Unit tests (already covered by `pytest` / `vitest` on the branch before SIT)
- E2E tests (real browser + real user journey — run downstream after code-review)
- UAT (business owner final sign-off — product-lead drives, downstream of E2E)

You just wrote the Unit tests, so you have the clearest picture of the unit-vs-integration boundary. If a failure reproduces by running just the backend unit tests with mocks, it's a unit-level miss, not a SIT finding; fold it back into the unit suite rather than writing it up as a SIT defect.

## Pre-conditions

- [ ] Feature branch is rebased onto `main`
- [ ] All Unit tests passing on the branch (pytest / vitest green) + lint + typecheck green
- [ ] PRD acceptance criteria (AC) accessible at `docs/prd/[feature]-[date].md`
- [ ] `.env.local` with SIT-mode flags configured (or `.env.sit` if a dedicated SIT config exists)
- [ ] **前端 SIT 专属**：MSW mock 来自 orval 生成产物（`*.msw.ts`），非手写——mock 与 OpenAPI 契约同源（见 ADR-006 / `coding.md` 契约纪律）

If any precondition fails: SendMessage product-lead, do not proceed.

## Environment

Default SIT environment is **local docker-compose**:

```bash
# from repo root
docker compose up -d postgres
pnpm install                              # frontend deps
python -m pip install -r backend/requirements.txt
alembic upgrade head                      # apply latest schema
pnpm --filter frontend dev &              # frontend on 5173
python -m uvicorn app.main:app --reload & # backend on 8000
```

For LLM-dependent features, set provider env vars per `agf-wiring-multi-llm-sdk` skill. Use a **dedicated SIT API key** with a hard daily spend cap so a runaway test doesn't drain the budget.

## Execution sequence

Walk every AC from `docs/prd/[feature].md`. For each AC at the integration layer:

1. **Setup** — record exact starting state (DB rows / fixture / user logged in)
2. **Action** — step-by-step what triggers the integration (frontend button click → API call → DB write → external service callback)
3. **Expected** — copy the AC verbatim
4. **Actual** — capture HTTP status, response body excerpt, DB row diff, log lines
5. **Verdict** — Pass / Fail / Blocked (with reason)

> **Verify, don't assume.** Don't write "Passed" because the code looks right. Run the action, capture the actual response, compare. Per `.claude/standards/coding.md` "Verify before assert" — paste the actual command output into the progress entry.

## Evidence collection

For each AC verdict:

- HTTP responses: `curl -i` output or browser DevTools Network export
- DB state changes: `psql -c "SELECT ..."` before/after dumps
- Logs: relevant lines from backend console + frontend console
- Screenshots: only when UI behavior is the subject of the AC

Keep evidence inline in the `**SIT 证据**` section of `progress/<role>.md` (small payloads). Large/binary artifacts → store under `progress/evidence/[feature]/` and reference by path.

## Evidence Output

SIT no longer produces a standalone report under `docs/qa/`. All evidence lives in `progress/<role>.md` under the `**SIT 证据**` section of the task entry — pass = single AC-tagged line (`✅ AC-N (integration): <一句话>`), fail/blocked expands命令 + 输出 + 偏差.

Format authority: `.claude/standards/ac-lifecycle.md` → **完整条目格式** (5-section format 状态 / Skills / SIT 证据 / 质量门 / 下一步 + the `**SIT 证据**` block rules). The progress file is archived into `docs/qa/[feature]-process-log.md` after UAT sign-off (product-lead), so SIT evidence survives without a separate report artifact.

## Hand-off

完成 SIT 自跑后，**先自检再报告**——跑 `bash .claude/scripts/agf-sit-precheck.sh progress/<role>.md` 机筛 placeholder / 漏证据 / pass 含失败 token / 质量门矛盾（advisory，不阻断），把 flag 的修掉再 SendMessage，省一轮 code-review 打回（同一脚本是 code-reviewer 的 SIT Audit step 0，ADR-011 决策 2）。然后：

- **All AC pass**: SendMessage product-lead — "Implementation + SIT done, ready for code-review"，引用 `progress/<role>.md` 条目路径 + 时间戳
- **Some AC fail / blocked**: 仍写完 `progress/<role>.md` 的 SIT 段（如实记录 fail / blocked），但 SendMessage 写明阻塞原因与影响范围，由 product-lead 决定本轮是否就修
- 不再直接 SendMessage 下游 QA 角色（已不参与 SIT）；E2E 由 product-lead 在 code-review (含 SIT Audit) 通过后单独启动

## Anti-patterns

- ❌ Marking AC as Pass without actually triggering the action
- ❌ Skipping ACs because "they look obviously fine"
- ❌ Lumping multiple ACs into one "Passed all" line — every AC needs its own verdict + evidence
- ❌ Running SIT against a stale environment (forgot to apply migrations / restart server)
- ❌ Using production API keys for SIT
- ❌ Skipping SIT to ship faster — code-reviewer will reject the SIT Audit (see `.claude/agents/code-reviewer.md` "SIT Audit" section) and you'll be sent back
- ❌ Treating a missing unit test as a SIT defect — fold it back into the unit suite, don't smuggle it through integration
