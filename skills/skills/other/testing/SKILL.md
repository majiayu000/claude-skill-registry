---
name: testing
description: "Testing strategies and methodologies including TDD and E2E testing. Use when writing tests, implementing TDD workflow, or setting up E2E test infrastructure."
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# 测试策略

> 关联 Agent: `tdd-guide`（测试驱动开发）、`code-reviewer`（可测试性评估）、`build-error-resolver`（修复后测试验证）

本技能提供测试策略选择指南，整合 TDD（测试驱动开发）和 E2E（端到端测试）最佳实践。

## 子文件

- [tdd.md](tdd.md) - 测试驱动开发工作流
- [e2e.md](e2e.md) - Playwright E2E 测试指南
- [tdd-example.md](tdd-example.md) - 完整 TDD 会话示例
- [frameworks.md](frameworks.md) - 测试框架配置与 Mock 模式
- [qa-methodology.md](qa-methodology.md) - QA 角色方法论与验证流程

## 测试金字塔

```
        ┌─────────┐
        │  E2E   │  少量：验证核心流程
        ├─────────┤
        │集成测试 │  中等：验证组件交互
        ├─────────┤
        │单元测试 │  大量：验证独立单元
        └─────────┘
```

## 测试策略选择

| 场景             | 推荐策略             | 参阅文件 |
| ---------------- | -------------------- | -------- |
| 新功能开发       | TDD（测试先行）      | `tdd.md` |
| Bug 修复         | 先写失败测试，再修复 | `tdd.md` |
| 核心用户流程验证 | E2E 测试             | `e2e.md` |
| 重构现有代码     | 先补测试，再重构     | `tdd.md` |
| UI 交互验证      | E2E + 视觉回归       | `e2e.md` |

## 覆盖率目标

| 代码类型     | 单元测试 | E2E 测试 |
| ------------ | -------- | -------- |
| 核心业务逻辑 | 100%     | 关键流程 |
| 普通业务代码 | 80%+     | 可选     |
| 工具函数     | 80%+     | 不需要   |
| UI 组件      | 70%+     | 关键交互 |

## 最佳实践

1. **测试先行** - TDD 循环：RED → GREEN → REFACTOR
2. **独立隔离** - 每个测试独立运行，无共享状态
3. **快速反馈** - 单元测试 < 50ms，E2E 适度控制
4. **语义命名** - 测试名称描述行为，不描述实现
5. **分层覆盖** - 单元测试多，E2E 测试精

## TDD 循环速览

```
RED → GREEN → REFACTOR → REPEAT

RED:      写一个失败的测试
GREEN:    写最少的代码使测试通过
REFACTOR: 改进代码，保持测试绿色
REPEAT:   下一个场景
```

详细指南参阅 `tdd.md`

## E2E 测试速览

```
tests/
├── e2e/                       # E2E 测试目录
│   ├── auth/                  # 认证流程
│   └── core/                  # 核心功能
├── pages/                     # Page Object Model
└── playwright.config.ts
```

详细指南参阅 `e2e.md`

## 测试命令

```bash
# 单元测试
npm test
npm test -- --coverage

# E2E 测试
npx playwright test
npx playwright test --headed  # 可视化
npx playwright test --debug   # 调试模式
```

---

> **记住**：测试不是可选项。它是支持自信重构、快速开发和生产可靠性的安全网。
