---
name: fec-refactor-clean
description: Use when safely removing dead frontend code, unused exports, stale components, obsolete routes, unused dependencies, or cleanup targets found by tools such as knip, depcheck, ts-prune, TypeScript, ESLint, or manual review. Do not use for feature rewrites that change behavior; Chinese triggers include 死代码, 清理未使用, refactor clean, 依赖清理, 删除无用代码.
---

# 重构清理

## Purpose

在验证保护下识别并清理无用前端代码，减少技术债，同时避免误删动态引用、路由入口、配置文件和运行时约定。

## Procedure

1. 先建立基线：运行或确认当前 lint、type-check、test、build 的状态。
2. 收集候选项：
   - 优先使用仓库已有工具，如 knip、depcheck、ts-prune、eslint、TypeScript。
   - 没有工具时，用 `rg` 检查引用、导出、路由、注册点和文档入口。
3. 按风险分类：
   - SAFE：测试夹具、未引用工具函数、明确未导出的私有组件。
   - CAUTION：共享组件、feature 入口、样式文件、Storybook stories。
   - DANGER：路由、配置、package scripts、运行时模板、动态 import、插件元数据。
4. 只自动处理 SAFE 项；CAUTION 和 DANGER 需输出建议和证据，不直接删除。
5. 每批清理后运行受影响验证命令。
6. 若验证失败，停止扩大清理范围，先定位该批次。

## Frontend-Specific Checks

- 检查 JSX/模板字符串、路由配置、barrel export、Storybook、测试、文档示例和动态组件注册。
- 样式文件需检查 className、CSS Modules、Tailwind safelist、全局选择器和主题变量。
- 依赖清理需检查构建插件、运行时模板、CLI scripts、monorepo 子包和 peer dependency。

## Constraints

- 不改变用户可见行为。
- 不删除无法证明无引用的公开 API、路由、模板或配置。
- 不用“一次大删除”替代可验证的小批次清理。
- 不把格式化、重命名或架构重写混入死代码清理。

## Expected Output

- 清理报告保存为 `reports/refactor-clean-YYYY-MM-DD-HHmmss.md`。
- 报告包含候选项、风险分类、已清理项、跳过原因、运行命令和剩余风险。
- 代码清理后相关验证命令通过，或明确说明阻塞原因。
