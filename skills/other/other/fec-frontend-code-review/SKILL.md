---
name: fec-frontend-code-review
description: Use when the user asks for general frontend code review, PR review, merge-readiness assessment, architecture maintainability, type-safety, rendering/state risks, style consistency, testability gaps, or a cross-cutting review summary. Delegate deep security, accessibility, E2E, or performance investigations to their specialized skills; Chinese triggers include 代码审查, 代码评审, review.
---

# 前端代码评审

## Purpose

从架构、类型安全、可访问性、样式一致性、性能和可测试性等 8 个维度审查前端代码质量，输出分级评审报告。

## Procedure

1. 明确审查范围：git diff、指定文件、PR 或设计实现结果。
2. 按架构、类型安全、渲染与状态、样式、可访问性、可维护性、测试和安全做横向扫描。
3. 将安全、无障碍、E2E 或性能深水区分流到专项 skill。
4. 按严重程度输出具体文件、行号、风险和修复建议；报告格式见 [references/report-template.md](references/report-template.md)。

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

- 组件/页面文件规模是否合理（宜约 **300 行**内；逾 **500 行**或复杂度过高须拆分，见 `templates/rules/react.md` / `vue.md`「组件文件规模」）
- 命名质量是否良好
- 是否有应该提取的重复逻辑
- 是否存在死代码、过期注释或临时性 hack
- 业务状态、类型、标识是否用裸数字/裸字符串（应对齐 `templates/rules/typescript.md`「禁止 Magic Number / Magic String」）

7. 测试

- 是否缺少关键测试覆盖
- 是否存在脆弱的选择器或不稳定的测试模式

8. 安全

- 无明显 XSS 风险（dangerouslySetInnerHTML / v-html 必须审查）
- 无敏感信息硬编码
- 无未校验的用户输入直接渲染

9. 必检项（阻塞合并）

- [ ] TypeScript 类型完整，无 `any`
- [ ] 无 XSS 风险
- [ ] 无敏感信息硬编码
- [ ] 核心逻辑有单元测试

10. 质量项（建议修改）

- [ ] 组件文件规模符合约定（约 300 行内为佳；逾 500 行或高复杂度已拆子组件 / Hooks / Composables / utils）
- [ ] 无重复代码（DRY 原则）
- [ ] 无未使用的 import

11. 规范项（风格建议）

- [ ] 命名语义清晰
- [ ] 注释覆盖复杂逻辑

## Detailed References

Load [references/report-template.md](references/report-template.md) when writing the code review report. Findings must be specific and actionable; do not write vague advice such as "optimize performance" without identifying the concrete code pattern.

## 与子代理的配合

需要基于 **git diff**、按 **CRITICAL / HIGH / MEDIUM / LOW** 分级、合并同类问题并输出 **Review Summary 表** 时，可委托插件内置的 **`fec-frontend-code-reviewer`** 子代理；报告文件命名与本 Skill 相同（`code-review-YYYY-MM-DD-HHmmss.md`）。

## Related Skills / Boundary

- `fec-security-review` — XSS、CSRF、token、文件上传、第三方脚本、CSP 等安全深审。
- `fec-accessibility-check` — WCAG、键盘、焦点、语义和 ARIA 深审。
- `fec-e2e-testing` — 关键路径、flaky、trace、CI artifacts。
- `fec-validation-fix` — 运行验证命令并修复失败。

## Expected Output

- 分级评审报告（CRITICAL / HIGH / MEDIUM / LOW）
- 每个问题关联具体文件和行号，附修复建议
- 阻塞项（CRITICAL）修复前不建议合并
- 评审报告保存为 `reports/code-review-YYYY-MM-DD-HHmmss.md`
