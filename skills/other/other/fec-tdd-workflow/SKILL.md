---
name: fec-tdd-workflow
description: Use when implementing new frontend behavior, fixing bugs, or refactoring logic where tests can describe the expected behavior first. Apply to components, hooks/composables, utilities, API clients, route guards, or user workflows; Chinese triggers include TDD, 测试驱动, 先写测试, 红绿重构, 回归测试.
---

# 前端 TDD 工作流

## Purpose

用“先写失败测试，再实现最小代码，再重构”的节奏交付前端功能，避免只在实现后补覆盖率。

## Procedure

1. 识别可观察行为：用户能看到的 UI、组件契约、hook/composable 返回值、路由守卫结果、API client 输出或错误状态。
2. 先写一个最小失败测试：
   - 纯逻辑优先单元测试。
   - 组件交互优先 Testing Library / Vue Test Utils。
   - 跨页关键流程优先 Playwright / Cypress。
3. 运行该测试并确认失败原因正确，失败应来自行为尚未实现，而不是语法、导入或测试环境错误。
4. 写刚好能通过测试的最小实现，不顺手扩大范围。
5. 重新运行测试，确认变绿。
6. 在测试保持通过的前提下重构命名、边界和重复逻辑。
7. 对 bug 修复，保留能复现问题的回归测试。

## Frontend Test Selection

| Risk | Preferred Test |
| ---- | -------------- |
| utils、schema、状态计算 | 单元测试 |
| hooks / composables | 单元或轻量集成测试 |
| 组件 props、emits、交互、状态 | 组件测试 |
| Router、Provider、Store 协作 | 轻量集成测试 |
| 登录、支付、权限、关键 CRUD | E2E 测试 |

## Constraints

- 不为了 TDD 引入项目没有使用且收益不清晰的新测试框架。
- 不测试实现细节、私有状态或脆弱 DOM 结构。
- 不把 E2E 当作所有风险的默认答案；优先选择离风险最近的测试层。
- 如果现有仓库没有测试基础设施，先输出最小测试落地建议，再请求用户确认是否引入。

## Expected Output

- 至少一个先失败后通过的测试覆盖新增或修复行为。
- 实现保持最小范围，重构只在测试通过后进行。
- 总结运行过的测试命令、覆盖的行为和未覆盖风险。

