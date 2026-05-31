---
name: fec-code-review
description: Use when the user asks for general frontend code review, PR review, merge-readiness assessment, architecture maintainability, type-safety, rendering/state risks, style consistency, testability gaps, or a cross-cutting review summary. Delegate deep security, accessibility, E2E, or performance investigations to their specialized skills; Chinese triggers include 代码审查, 代码评审, review.
---

# 前端代码评审

## Purpose

从架构、类型安全、可访问性、样式一致性、性能和可测试性等 8 个维度审查前端代码质量，输出分级评审报告。

## Review Process

1. 先读项目事实：package scripts、框架、目录约定、最近 diff、现有测试和相关规则。
2. 按风险找问题，而不是按个人偏好挑风格；每个发现都要能指向具体文件、行号和用户影响。
3. 用五轴收敛结论：正确性、可维护性、类型/接口、用户体验、验证覆盖。
4. 对安全、无障碍、E2E、性能等深水区只做初筛；需要专项调查时明确分流。
5. 多维评审时先按职责拆分，再合并同类发现；同一文件同一根因只保留一条主发现，避免重复噪声。
6. 报告先列阻塞问题，再列建议项；没有证据的问题不要写成确定结论。

## 多维评审编排

当改动跨越多个质量维度时，按“主评审 + 专项分流”组织，而不是让所有维度重复检查同一处代码。

| 维度                | 触发条件                                             | 分流边界                             |
| ------------------- | ---------------------------------------------------- | ------------------------------------ |
| TypeScript 类型安全 | DTO、泛型、公共类型、类型守卫、`any`、断言           | 深入类型建模交给类型安全专项流程     |
| 状态管理            | 状态归属、全局 store、URL 状态、派生状态、跨页面同步 | 状态选型与迁移交给状态管理专项流程   |
| 安全                | 用户输入、HTML 渲染、token、上传、第三方脚本         | 漏洞级分析交给安全专项流程           |
| 无障碍              | 弹窗、菜单、表单、键盘操作、焦点管理                 | WCAG 细查交给无障碍专项流程          |
| 性能                | 大列表、重依赖、重复请求、长任务、包体积             | 性能证据与预算交给性能专项流程       |
| E2E                 | 关键用户路径、登录态、支付、跨页面流程               | 浏览器用例与 trace 交给 E2E 专项流程 |

发现合并规则：

- 同一根因出现在多个维度时，只保留最高严重级别，并在 `Dimension` 中列出相关维度。
- 同一文件多处重复模式，合并为一条模式级发现，列出代表性位置。
- 置信度不足的问题放入 Open Questions，不升级为阻塞项。
- 自动化可稳定捕获的格式问题交给 lint/format，不作为人工评审主发现。

## 评审维度

1. 架构

- 组件边界是否清晰
- 展示逻辑与业务逻辑是否分离
- 是否有可复用抽象
- 是否存在上帝组件

2. 类型安全

- 是否存在不必要的 `any`
- props 类型是否明确
- hooks/composables 返回值是否稳定
- 在可行情况下 API 契约是否有类型约束

3. 渲染与状态

- 是否存在不必要的重复渲染
- key 的使用是否稳定
- 可推导状态是否被重复存储
- 本地状态是否耦合过深
- 全局 store 是否只保存真正跨边界共享的客户端状态
- URL 状态、服务端状态、表单状态和浏览器持久化是否边界清晰

4. 样式

- 已有 Token 时是否还在使用 magic number
- 类名是否与仓库约定一致
- 响应式处理是否明确
- 是否无必要地混用了多套样式体系

5. 可访问性

- 语义结构是否合理
- 是否在需要时正确使用 label 和 aria
- 是否支持键盘操作
- 浮层和菜单的焦点管理是否正确

6. 可维护性

- 组件/页面文件规模是否合理（宜约 **300 行**内；逾 **500 行**或复杂度过高须拆分，见共享 React / Vue 规则中的「组件文件规模」）
- 命名质量是否良好
- 是否有应该提取的重复逻辑
- 是否存在死代码、过期注释或临时性 hack
- 业务状态、类型、标识是否用裸数字/裸字符串（应对齐 `templates/shared/rules/fec-typescript.md`「禁止 Magic Number / Magic String」）

7. 测试

- 是否缺少关键测试覆盖
- 是否存在脆弱的选择器或不稳定的测试模式

8. 安全

- 无明显 XSS 风险（dangerouslySetInnerHTML / v-html 必须审查）
- 无敏感信息硬编码
- 无未校验的用户输入直接渲染

9. 性能与体验证据

- 是否引入首屏重依赖、重复请求、大列表渲染或长任务
- loading、empty、error、disabled、focus 等状态是否完整
- 响应式布局是否有可验证断点和文本溢出保护

10. 必检项（阻塞合并）

- [ ] TypeScript 类型完整，无 `any`
- [ ] 外部输入、DTO、公共类型边界无无守卫断言
- [ ] 无 XSS 风险
- [ ] 无敏感信息硬编码
- [ ] 核心逻辑有单元测试

11. 质量项（建议修改）

- [ ] 组件文件规模符合约定（约 300 行内为佳；逾 500 行或高复杂度已拆子组件 / Hooks / Composables / utils）
- [ ] 无重复代码（DRY 原则）
- [ ] 无未使用的 import

12. 规范项（风格建议）

- [ ] 命名语义清晰
- [ ] 注释覆盖复杂逻辑

## Detailed References

撰写代码评审报告时，加载 [references/report-template.md](references/report-template.md)。发现必须具体且可操作；不要写"优化性能"等空泛建议而不指出具体代码模式。

## Expected Output

- 分级评审报告（CRITICAL / HIGH / MEDIUM / LOW）
- 每个问题关联具体文件和行号，附修复建议
- 阻塞项（CRITICAL）修复前不建议合并
- 评审报告保存为 `reports/code-review-YYYY-MM-DD-HHmmss.md`
- 多维评审要合并重复发现，并说明已分流到哪些专项能力
- 对不确定项标注需要的验证命令或补充上下文，不把猜测写成事实
