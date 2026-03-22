---
name: e2e-optimizer
description: Playwright E2E 敏捷测试优化：时间优先，精确打击。禁止全局运行，只测改动点，强制 Mock 外部依赖。触发词：E2E 测试、Playwright 测试、跑测试、测试优化。
version: 1.0
---

# E2E Optimizer - Playwright 敏捷测试规范

> **核心理念**：获取最快的反馈，而不是追求最严谨的测试覆盖率
>
> **公式**：精确打击 × Mock 依赖 = 秒级反馈

---

## 🎯 核心认知

在自主开发循环中，**时间是最宝贵的资源**。全局 E2E 测试极其耗时且脆弱。

| 传统测试思维 | 敏捷测试思维 |
|-------------|-------------|
| "运行全部测试确保没问题" | "只测改动点，秒级反馈" |
| 等待 30 秒跑完 100 个用例 | 3 秒内跑 1 个核心用例 |
| 追求 100% 覆盖率 | 追求 MVU 核心路径验证 |
| 测试失败就调试到底 | 连续失败 3 次就 skip 或降级 |

**根本解法**：用**测试金字塔**和**精确打击**强制收缩范围

---

## 🛑 绝对红线（禁止行为）

| 行为 | 为什么禁止 | 正确做法 |
|------|-----------|---------|
| ❌ `npx playwright test`（无参数） | 全局运行耗时太长 | `npx playwright test tests/login.spec.ts` |
| ❌ `page.waitForTimeout(5000)` | 硬编码死等，浪费时间 | `await page.waitForSelector('.success')` |
| ❌ 连续失败 3 次还执着调试 | 阻塞主流程推进 | 标记 `.skip` 或降级为单元测试 |
| ❌ 所有逻辑都用 E2E 测 | 测试金字塔倒置 | 纯逻辑用 Vitest/Jest 单元测试 |

---

## ✅ 智能体执行准则

### 1. 精确打击（只测改动点）

修改了某个组件或页面时，**只运行对应的单个测试文件/用例**：

```bash
# ✅ 只跑单个文件
npx playwright test tests/login.spec.ts

# ✅ 只跑特定用例 + 失败即停
npx playwright test tests/login.spec.ts -g "should login successfully" --max-failures=1

# ✅ 只跑改动的测试（配合 git diff）
npx playwright test --grep "@smoke"

# ✅ 限制并发数，避免资源竞争
npx playwright test --workers=2
```

### 2. 拥抱测试金字塔（Shift-Left Testing）

```
          ┌─────────────┐
          │   E2E 测试   │  ← 仅验证核心用户路径 (1-2 条)
          │  (Playwright)│     5-10 秒反馈
         ├───────────────┤
         │  组件/集成测试  │  ← 组件交互、模块集成
         │  (Testing Lib)│     1-3 秒反馈
        ├─────────────────┤
        │   单元测试       │  ← 纯逻辑、数据转换、工具函数
        │   (Vitest/Jest) │     毫秒级反馈
       └─────────────────┘
```

**决策树**：
```
要测试的代码是什么类型？
    │
    ├── 纯逻辑/数据转换/工具函数
    │   └──> Vitest/Jest 单元测试（毫秒级）
    │
    ├── 组件渲染/UI 交互
    │   └──> Testing Library 组件测试（秒级）
    │
    └── 完整用户路径/跨模块集成
        └──> Playwright E2E（只测 Happy Path）
```

### 3. 强制 Mock 外部依赖

E2E 耗时往往是因为等待后端 API 或第三方服务。**强制拦截并 Mock 网络请求**：

```javascript
// ✅ Mock API 响应，避免真实网络等待
await page.route('**/api/v1/data', async route => {
  const json = { mock: "data", status: "success" };
  await route.fulfill({ json });
});

// ✅ Mock 延迟响应，模拟慢速网络
await page.route('**/api/slow', async route => {
  await new Promise(resolve => setTimeout(resolve, 1000));
  await route.fulfill({ json: { data: "mocked" } });
});

// ✅ 阻断外部 CDN/统计脚本，避免拖慢测试
await page.route('**/analytics.js', route => route.abort());
```

**Mock 优先级**：
| 请求类型 | 策略 |
|---------|------|
| 后端 API | 全部 Mock，返回固定数据 |
| 第三方服务（支付/短信） | 全部 Mock |
| CDN/静态资源 | 允许或阻断（不等待） |
| 图片/字体 | 阻断（`route.abort()`） |

---

## 快速命令参考

### 运行测试

```bash
# 运行单个文件
npx playwright test tests/login.spec.ts

# 运行单个用例
npx playwright test -g "should login"

# 运行并生成报告
npx playwright test --reporter=html

# 调试模式（带 UI）
npx playwright test --debug

# 显示浏览器（有头模式）
npx playwright test --headed

# 限制失败次数，快速失败
npx playwright test --max-failures=1
```

### 代码生成

```bash
# 录制测试脚本
npx playwright codegen https://example.com

# 生成 TypeScript 测试
npx playwright codegen --language=typescript https://example.com
```

### 环境配置

```bash
# 使用特定环境配置
BASE_URL=http://localhost:3000 npx playwright test

# 使用 production 环境
BASE_URL=https://prod.example.com npx playwright test
```

---

## 测试文件结构规范

```
tests/
├── e2e/                    # E2E 测试（只测核心路径）
│   ├── login.spec.ts       # 登录流程
│   └── checkout.spec.ts    # 下单流程
├── integration/            # 集成测试（模块间交互）
│   └── api-integration.spec.ts
└── unit/                   # 单元测试（纯逻辑）
    └── utils.spec.ts
```

**单个测试文件模板**：
```typescript
import { test, expect } from '@playwright/test';

test.describe('登录模块', () => {
  // ✅ 只测试 Happy Path
  test('应该登录成功', async ({ page }) => {
    // Mock API
    await page.route('**/api/login', async route => {
      await route.fulfill({ json: { token: 'mock-token' } });
    });

    await page.goto('/login');
    await page.fill('#username', 'test');
    await page.fill('#password', 'test');
    await page.click('button[type="submit"]');

    // 用明确的条件等待，不要用 setTimeout
    await expect(page.locator('.welcome')).toBeVisible();
  });

  // ❌ 跳过不稳定测试
  test.skip('边界情况测试', async ({ page }) => {
    // 留到有时间再处理
  });
});
```

---

## 与时间盒 Skill 协作

### 工作流

```
时间盒启动（10-30 分钟）
    ↓
1. 定义 MVU 核心路径
2. 为 MVU 编写 1-2 个 E2E 测试（只测 Happy Path）
3. 运行测试验证
    ↓
时间盒执行
    ↓
- 测试失败 >3 次 → skip 或降级
- 测试通过 → 继续开发
- 新改动 → 只跑相关测试
    ↓
时间盒结束
    ↓
- 提交测试代码
- 记录 TODO（边界情况后续补充）
```

### 时间分配建议

| 任务类型 | E2E 测试时间 | 单元测试时间 |
|---------|------------|------------|
| 小功能/修复 | 2min（1 个用例） | 5min |
| 中等功能 | 5min（2-3 个用例） | 10min |
| 大功能 | 10min（核心路径） | 20min |

**原则**：
- E2E 测试数量 ≤ 3 个核心用例
- 单元测试覆盖所有逻辑分支
- 单个 E2E 测试运行时间 < 10 秒

---

## 调试故障排查

### 测试超时

```bash
# 检查是否使用了 waitForTimeout
grep -r "waitForTimeout" tests/

# 替换为条件等待
# ❌ await page.waitForTimeout(5000);
# ✅ await page.waitForSelector('.success');
```

### 测试不稳定（Flaky）

```typescript
// ✅ 使用重试机制（仅限已知不稳定测试）
test('不稳定测试', async ({ page }) => {
  // ...
}, { retries: 2 });

// ✅ 或标记为 skip，记录问题
test.skip('不稳定测试 - 待修复', () => {});
```

### 网络请求超时

```typescript
// 增加超时时间
test.setTimeout(30000);

// 或全局配置 playwright.config.ts
export default {
  timeout: 30000,
  expect: {
    timeout: 10000
  }
};
```

---

## 与其他 Skill 协作

| Skill | 协作方式 |
|-------|----------|
| **time-boxing** | 每个时间盒内只写 1-3 个核心 E2E 测试 |
| **git-commit** | 测试代码随功能一起提交 |
| **github** | PR 自动运行相关测试（CI 配置） |

---

## 触发词

| 优先级 | 触发词 | 动作 |
|--------|--------|------|
| **高** | E2E 测试、Playwright 测试、跑测试 | 运行指定测试 |
| **高** | 测试失败、又失败了 | 失败>3 次 → skip 或降级 |
| **高** | Mock API、拦截请求 | 添加 route.fulfill() |
| **中** | 测试太慢、优化测试 | 检查 waitForTimeout，替换为条件等待 |
| **中** | 只测这个、单跑 | 运行单个测试文件/用例 |

---

## Playwright 配置模板

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  // 超时设置
  timeout: 30000,
  expect: {
    timeout: 10000
  },

  // 并发设置
  fullyParallel: true,
  workers: 2,  // 限制并发数

  // 失败处理
  maxFailures: 3,  // 超过 3 个失败就停止

  // 重试设置
  retries: 1,  // 失败自动重试 1 次

  // 报告生成
  reporter: [
    ['list'],
    ['html', { open: 'never' }]
  ],

  // 全局 Mock（可选）
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure'
  }
});
```

---

## 反模式（禁止行为）

| 行为 | 为什么错 | 正确做法 |
|------|---------|---------|
| ❌ `npx playwright test` 无参数 | 全局运行耗时太长 | 指定文件或用例 |
| ❌ `waitForTimeout(5000)` | 死等，浪费时间 | `waitForSelector` 条件等待 |
| ❌ 所有逻辑都用 E2E 测 | 测试倒置，反馈慢 | 单元测试 + 组件测试 + E2E |
| ❌ 测试失败执着调试 | 阻塞主流程 | 失败>3 次就 skip 或降级 |
| ❌ 测试不 Mock 外部依赖 | 网络不稳定导致失败 | 强制 Mock API |
| ❌ 追求 100% 覆盖率 | 测试成本过高 | 只测核心路径（Happy Path） |

---

## 示例：登录功能测试

### ❌ 错误示例（慢 + 不稳定）

```typescript
test('登录', async ({ page }) => {
  await page.goto('/login');
  await page.fill('#username', 'test');
  await page.fill('#password', 'test');
  await page.click('button');

  // ❌ 硬编码等待
  await page.waitForTimeout(5000);

  // ❌ 没有 Mock，依赖真实后端
  await expect(page.locator('.dashboard')).toBeVisible();
});
```

### ✅ 正确示例（快 + 稳定）

```typescript
test('登录', async ({ page }) => {
  // ✅ Mock API
  await page.route('**/api/login', async route => {
    await route.fulfill({
      json: { token: 'mock-token', user: 'test' },
      status: 200
    });
  });

  await page.goto('/login');
  await page.fill('#username', 'test');
  await page.fill('#password', 'test');
  await page.click('button');

  // ✅ 条件等待
  await expect(page.locator('.welcome')).toBeVisible({ timeout: 5000 });
});

// 运行命令：
// npx playwright test tests/login.spec.ts
// 预期耗时：<3 秒
```

---

## 快速检查清单

运行 E2E 测试前，确认：

```bash
# 1. 是否只跑改动点？
npx playwright test tests/<changed-file>.spec.ts

# 2. 是否限制了失败次数？
npx playwright test --max-failures=1

# 3. 是否使用了 Mock？
grep -r "page.route" tests/

# 4. 是否有硬编码等待？
grep -r "waitForTimeout" tests/
```

---

## 核心原则

> **反馈速度优先，覆盖率其次**

1. **精确打击** - 只测改动点，不跑全局
2. **Mock 优先** - 拦截外部依赖，避免网络等待
3. **条件等待** - 用 `waitForSelector` 代替 `waitForTimeout`
4. **测试金字塔** - E2E 只测核心路径，逻辑用单元测试
5. **快速失败** - 失败>3 次就 skip 或降级
6. **秒级反馈** - 单个测试运行时间 <10 秒

---

*版本：v1.0 | 最后更新：2026-03-18*
