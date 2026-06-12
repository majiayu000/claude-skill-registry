---
name: fec-legacy-to-modern-migration
description: 用于规划或实施从 JavaScript、jQuery、HTML/CSS、服务端渲染模板、MPA 遗留前端代码或旧框架代码迁移到现代前端技术栈，同时保持行为一致。不要用于仍留在旧技术栈内的日常遗留 bug 修复；中文触发词包括 遗留项目、技术栈升级、jQuery 迁移。
---

# 传统前端到现代框架迁移

适用于将 JavaScript + jQuery + HTML/CSS 多页面应用（MPA）、服务端模板渲染项目或旧框架代码，渐进迁移到 React、Vue、Next.js、Nuxt、TypeScript，或保留 MPA 形态但现代化模块、构建、类型和测试的场景。

## 用途

指导传统前端项目渐进迁移到目标现代栈，提供迁移策略、概念映射、分阶段步骤和实施约束，确保功能等价和风险可控。

## 流程

1. 先识别目标栈、迁移边界和是否保留 MPA/服务端模板形态。
2. 加载 [references/migration-strategy-and-mapping.md](references/migration-strategy-and-mapping.md)，选择渐进式或一次性重写策略，并明确遗留模式到目标栈的映射。
3. 加载 [references/migration-execution-checklist.md](references/migration-execution-checklist.md)，完成存量盘点、依赖分析、优先级排序和分阶段迁移计划。
4. 撰写迁移分析或迁移计划报告时，加载 [references/migration-report-template.md](references/migration-report-template.md)。
5. 按准备、基础层、模块/页面迁移、收尾的顺序推进，每次迁移一个可验证单元。
6. 每个迁移单元验证功能等价、视觉一致、类型安全、可访问性、i18n、资源和样式边界。

## 约束

- 迁移前必须先输出迁移分析报告，明确策略、优先级和风险。
- 不要在一次迁移中同时改架构、改 UI、改接口。
- 优先保证功能等价，再考虑优化和现代化。
- 迁移过程中保持旧系统可运行，避免大爆炸式上线。
- 遇到 jQuery 插件无现成替代时，可暂时用 iframe 或微前端方式嵌入，待后续替换。
- 目标栈先识别 React/Vue/Next/Nuxt、现代 MPA 或局部现代化目标，不默认强制改成 SPA。
- 图片使用原项目资源；图标体系优先沿用原项目或目标项目规范；内联 SVG 例外需有可访问性、组件化或维护理由。
- 样式参考原项目效果但不照搬 CSS，优先使用目标项目样式体系；内联样式例外需局部、可解释。
- 目标是视觉与交互一致、代码更简洁易维护，业务功能不得缺失。
- 涉及页面、组件、路由、表单、弹窗、导航或关键用户流程的迁移，必须建立重构前后的行为清单，并使用 Playwright 或同等真实浏览器验证方式对关键路径做对比验证。
- 对视觉敏感页面，应补充截图对比或人工截图验收；动态内容、动画、字体和环境差异需明确屏蔽、稳定化或说明。
- 对纯逻辑、类型、构建或无 UI 的迁移，不强制 Playwright，应选择更贴近风险的验证层：type-check、unit test、component test、build 或 lint。
- 验证目标不是像素级完全一致，而是确认业务功能无缺失、关键交互等价、主要视觉布局无非预期偏差，并且代码比旧实现更清晰、可维护。

## 预期输出

- 迁移分析报告保存为 `reports/migration-plan-YYYY-MM-DD-HHmmss.md`，包含策略选择、存量盘点、依赖关系、分阶段步骤、风险与回滚方案。
- 迁移后的业务功能与原项目完全等价，无功能缺失。
- 视觉与交互与原项目一致，用户无感知差异。
- 类型定义完整，无 `any` 滥用，API 调用统一且类型安全。
- 图片使用原项目资源，样式进入目标项目样式体系，图标和内联样式例外有明确理由。
- 新代码文案已 i18n，关键路径有测试覆盖。
