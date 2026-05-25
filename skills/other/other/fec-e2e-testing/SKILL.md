---
name: fec-e2e-testing
description: Use when creating, maintaining, debugging, or reviewing real-browser end-to-end tests with Playwright or Cypress, including Page Object models, CI artifacts, traces, flaky tests, cross-page visual regression, and critical user journeys such as login, payment, permissions, or CRUD. Use testing-strategy for layer planning and component-testing for unit/component tests; Chinese triggers include E2E, 端到端测试, Playwright, Cypress.
---

# E2E 测试规范

## Purpose

用真实浏览器验证关键用户旅程，发现单元测试无法覆盖的集成风险。

## Procedure

1. 明确关键旅程：登录、购买、创建、搜索、权限、支付等跨页面流程优先；若只是选择测试层级，先用 `fec-testing-strategy`。
2. 新项目优先 Playwright；已有 Cypress 项目沿用 Cypress，不为迁移而迁移。
3. 用 Page Object 或 fixtures 封装登录、页面定位器和共享数据，spec 中避免裸选择器。
4. 断言用户可见结果，依赖 Locator 自动等待、网络响应或可见状态，不使用固定 sleep。
5. CI 必须上传 HTML report、截图、trace 或视频；flaky 用例要隔离、复现和关联 issue。

## Detailed References

- Load [references/playwright-patterns.md](references/playwright-patterns.md) for directory layout, Page Object, spec structure, config, flaky debugging, and artifact examples.
- Load [references/e2e-advanced.md](references/e2e-advanced.md) when the task needs CI examples, Markdown report templates, Web3/wallet flows, high-risk financial flows, or visual regression setup.

## Constraints

- 禁止依赖 `sleep` / 固定 `setTimeout` 作为主要同步手段。
- 不在生产环境跑真实 E2E。
- 避免在 E2E 中断言组件内部像素级样式；跨页面截图/视觉回归仅覆盖用户旅程中的关键页面状态。
- 失败必须能靠截图、trace 或视频定位。
- 组件内部契约测试分流到 `fec-component-testing`。

## Expected Output

关键用户旅程有稳定 E2E 覆盖，失败产物可定位问题，CI 中报告和 trace 可下载；flaky 用例有复现命令、隔离策略和后续 issue。

## Related Skills / Boundary

- `fec-testing-strategy` — testing layer selection and coverage matrix before writing tests.
- `fec-component-testing` — unit, component, and light integration tests close to UI code.
- `fec-storybook-component-doc` — component-state visual baselines and Storybook interaction tests.
- `fec-validation-fix` — run existing validation commands and fix failures.

## 与子代理的配合

需要实际执行 Playwright/Cypress、反复验证 flaky、整理 CI artifact 时，可委托 `fec-frontend-e2e-runner` 子代理。
