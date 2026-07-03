---
name: agf-running-apple-sit
description: Use when apple-dev has finished feature code + Unit tests (Swift Testing) and is about to enter code-review. Provides the Apple SIT scope (xcodebuild test + simulator per declared target), the AC-driven integration walk, APIProtocol-mock discipline, and evidence sink (progress/apple-dev.md). SIT is dev-owned; apple-code-reviewer audits the evidence.
---

# Running Apple SIT (xcodebuild + simulator)

Use this skill when:

- apple-dev finished feature code + Unit tests and is about to enter code-review
- apple-dev needs to verify a fix doesn't regress integration（视图 ↔ AppCore ↔ 生成 client ↔ 后端契约）

## What Apple SIT is — and is not

**SIT** verifies that **independently-developed components compose correctly** at the app-integration layer — SwiftUI 视图 ↔ AppCore 业务层 ↔ swift-openapi-generator 生成的 client ↔（mock 后端）。It is NOT:

- Unit tests（Swift Testing，`swift test` 已在分支全绿）
- E2E（XCUITest 对**签名分发包**——apple-qa-engineer 在发布构建后跑）
- UAT（业务签字，product-lead 驱动）

If a failure reproduces in plain `swift test` with mocks, it's a unit-level miss — fold it back into the unit suite, don't write it up as a SIT defect.

## Pre-conditions

- [ ] Feature branch rebased onto `main`
- [ ] Unit 全绿：`cd apple/AppCore && swift test`，strict concurrency 零 warning
- [ ] PRD AC 可达：`docs/prd/[feature]-[date].md`，且每条 AC 的 **target 归属**清楚（macos / ios / universal）
- [ ] **契约 mock 纪律**：后端 mock 一律实现生成的 `APIProtocol`（ADR-008），**禁手写 JSON fixture**；`openapi.json` 与 main 上后端导出一致
- [ ] 模拟器就位：`xcrun simctl list devices available` 有目标 destination

If any precondition fails: SendMessage product-lead, do not proceed.

## Environment

SIT 在**模拟器 / 本机**层执行（非签名分发包——那是 E2E 的事）：

```bash
# iOS target
xcodebuild test -project apple/App.xcodeproj -scheme App \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -resultBundlePath sit-ios.xcresult

# macOS target
xcodebuild test -project apple/App.xcodeproj -scheme App \
  -destination 'platform=macOS' \
  -resultBundlePath sit-macos.xcresult
```

- **universal target 必须两个 destination 都跑**，缺一即 SIT 不完整（reviewer audit 会标 ❌）。
- 需要联真后端语义的 AC：本地起 FastAPI（`uvicorn app.main:app`）+ 真实 Postgres（`docker compose up -d postgres`），client 指向 localhost；LLM 类 AC 用 dedicated SIT key（参见 `agf-wiring-apple-llm` 的 env 契约）。

## Execution sequence

Walk every AC from the PRD. For each AC at the integration layer:

1. **Setup** — 起始状态（模拟器型号 / OS 版本 / 数据初态 / mock 配置）
2. **Action** — 触发集成的操作链（视图交互 → AppCore 调用 → client 请求 → mock/真后端响应）
3. **Expected** — copy the AC verbatim（含 target 标注）
4. **Actual** — 捕获真实输出：xcodebuild test 结果行 / xcresult 摘要（`xcrun xcresulttool get --path *.xcresult --format json` 关键段）/ 后端响应摘录
5. **Verdict** — Pass / Fail / Blocked (with reason)

> **Verify, don't assume.** 不许因为"代码看着对"写 Passed——跑命令、贴真实输出、对比。

## Evidence Output

证据全部进 `progress/apple-dev.md` 的 `**SIT 证据**` 段（pool 模式 `progress/apple-dev-<N>.md`）——pass = 单行 AC 标注（`✅ AC-N (integration, macos|ios): <一句话>`），fail/blocked 展开命令 + 输出 + 偏差。大体积 xcresult → `progress/evidence/[feature]/` 按路径引用。

Format authority: `.claude/standards/ac-lifecycle.md` → **完整条目格式**（5 段格式）。UAT 签字后由 product-lead 归档到 `docs/qa/[feature]-process-log.md`。

## Hand-off

- **All AC pass**: SendMessage product-lead — "Implementation + SIT done (target: …), ready for code-review"，引用 progress 条目路径 + 时间戳
- **Some AC fail / blocked**: 仍如实写完 SIT 段，SendMessage 写明阻塞原因与影响范围，由 product-lead 决定本轮是否就修
- 不直接 SendMessage apple-qa-engineer——E2E 由 product-lead 在 code-review（含 SIT Audit）通过 + 发布构建后启动

## Anti-patterns

- ❌ Marking AC as Pass without actually triggering the action
- ❌ universal target 只跑一个平台就声明完成 —— 两 destination 缺一不可
- ❌ 手写 JSON fixture 模拟后端 —— 必须实现生成的 `APIProtocol`（ADR-008）
- ❌ 对 Debug 本地构建测出的结论冒充 E2E —— SIT 只证集成层，分发包验证归 E2E
- ❌ Lumping multiple ACs into one "Passed all" line — every AC needs its own verdict + evidence
- ❌ Skipping SIT to ship faster —— apple-code-reviewer 的 SIT Audit 会打回 `❌ Redo SIT`
