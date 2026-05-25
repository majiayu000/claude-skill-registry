---
name: fec-testing-strategy
description: Use when planning or reviewing a frontend testing strategy, selecting the right test layer by risk, mapping coverage across static checks, unit tests, component tests, integration tests, E2E, Storybook/visual regression, a11y, security, performance, or CI gates. Do not use to write individual component/E2E tests or merely run existing validation commands; Chinese triggers include 测试策略, 测试分层, 测试计划, 覆盖矩阵.
---

# 前端测试策略

## Purpose

按“离代码多近 / 覆盖风险层级”选择测试方法，避免把所有风险都塞进组件测试或 E2E。

## Procedure

1. 识别改动类型：纯逻辑、UI 组件、跨模块流程、浏览器能力、视觉稳定性、专项质量风险或发布门禁。
2. 建立测试层级矩阵，至少区分：
   - 静态检查：TypeScript、ESLint、格式、依赖安全、构建。
   - 单元测试：utils、hooks/composables、状态逻辑、schema、纯函数。
   - 组件测试：props/emits、用户交互、loading/error/empty、mock 边界。
   - 轻量集成测试：表单 + API mock + 路由/Store/Provider 上下文。
   - E2E：真实浏览器、跨页面关键旅程、鉴权、支付、权限、CI artifacts。
   - 视觉/交互文档：Storybook interaction、Chromatic、视觉回归基线。
   - 专项质量：a11y、安全、性能、兼容性。
3. 按风险分配覆盖：高频核心路径优先 E2E，复杂组件状态优先组件测试，纯逻辑优先单元测试，跨 provider 协作用轻量集成测试。
4. 检查是否已有命令、测试框架、目录约定和 CI 门禁；沿用项目现状，不为策略文档引入不必要工具。
5. 输出可执行的最小测试计划：每层覆盖什么、不覆盖什么、优先级、建议命令和责任 skill。

## Constraints

- 不把测试策略写成泛泛的“多写测试”；每个建议必须对应具体风险。
- 不要求所有项目都补齐完整测试金字塔；按业务风险和团队维护能力裁剪。
- 不把 E2E 当作单元/组件测试的替代品；不把组件测试当作真实浏览器兼容保证。
- 不为小改动强制引入新框架；优先复用仓库已有工具和脚本。

## Related Skills / Boundary

- `fec-component-testing` — author/review unit, component, and light integration tests close to UI code.
- `fec-e2e-testing` — author/review real-browser cross-page journeys and CI artifacts.
- `fec-storybook-component-doc` — component state docs, interaction tests, and visual baselines.
- `fec-validation-fix` — run existing lint/typecheck/test/build commands and fix failures.
- `fec-accessibility-check` / `fec-security-review` — deep specialty quality reviews.
- `fec-frontend-code-review` — general PR review when testing is only one dimension.

## Expected Output

输出测试分层建议、风险到测试层的映射、优先级、建议命令、需新增或调整的测试文件范围，以及明确分流到哪些专项 skill 或 agent。

## Related Agent

- [fec-frontend-test-planner](../../agents/fec-frontend-test-planner.md) - 为功能、PR 或里程碑制定测试分层与覆盖矩阵。
