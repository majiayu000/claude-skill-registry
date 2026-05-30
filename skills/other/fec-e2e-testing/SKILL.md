---
name: fec-e2e-testing
description: Use when creating, maintaining, debugging, or reviewing real-browser end-to-end tests with Playwright or Cypress, including Page Object models, CI artifacts, traces, flaky tests, cross-page visual regression, and critical user journeys such as login, payment, permissions, or CRUD. For layer planning or tests close to UI components, choose the matching testing workflow first; Chinese triggers include E2E, 端到端测试, Playwright, Cypress.
---

# E2E 测试规范

## Purpose

用真实浏览器验证关键用户旅程，发现单元测试无法覆盖的集成风险。

## Procedure

1. 明确关键旅程：登录、购买、创建、搜索、权限、支付等跨页面流程优先；若只是选择测试层级，先做测试分层规划。
2. 新项目优先 Playwright；已有 Cypress 项目沿用 Cypress，不为迁移而迁移。
3. 用 Page Object 或 fixtures 封装登录、页面定位器和共享数据，spec 中避免裸选择器。
4. 断言用户可见结果，依赖 Locator 自动等待、网络响应或可见状态，不使用固定 sleep。
5. CI 必须上传 HTML report、截图、trace 或视频；flaky 用例要隔离、复现、标注来源并关联 issue。
6. 调试失败时先读 trace、console、network 和截图，再改测试；不要把真实产品缺陷误判成 flaky。
7. 对关键浏览器能力、支付、权限、上传和实时通信流程，记录测试环境、种子数据和清理策略。
8. 测试数据必须可重复：优先使用 API seed、数据库 fixture、测试账号或 mock 服务；随机数据需带唯一前缀并在 teardown 清理。

## Detailed References

- Load [references/playwright-patterns.md](references/playwright-patterns.md) for directory layout, Page Object, spec structure, config, flaky debugging, and artifact examples.
- Load [references/e2e-advanced.md](references/e2e-advanced.md) when the task needs CI examples, Markdown report templates, Web3/wallet flows, high-risk financial flows, or visual regression setup.

## Constraints

- 禁止依赖 `sleep` / 固定 `setTimeout` 作为主要同步手段。
- 不在生产环境跑真实 E2E。
- 避免在 E2E 中断言组件内部像素级样式；跨页面截图/视觉回归仅覆盖用户旅程中的关键页面状态。
- 失败必须能靠截图、trace 或视频定位。
- 组件内部契约测试分流到组件测试 workflow。
- 不把不稳定等待、随机数据或依赖测试顺序带入 CI。
- 不把重试次数当作 flaky 治理；重试只能保留证据，根因仍需定位。

## Expected Output

关键用户旅程有稳定 E2E 覆盖，失败产物可定位问题，CI 中报告和 trace 可下载；flaky 用例有复现命令、隔离策略和后续 issue。
