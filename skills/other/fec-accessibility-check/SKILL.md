---
name: fec-accessibility-check
description: Use when reviewing or improving frontend accessibility, semantic structure, keyboard support, focus management, ARIA labels, or WCAG-related UI issues; Chinese triggers include 无障碍, accessibility, a11y, WCAG.
---

# 无障碍实现规范（WCAG 2.1 AA）

## Purpose

确保前端 UI 对残障用户可访问，满足 WCAG 2.1 AA 标准。

## Procedure

1. 检查语义结构：landmark、标题层级、表单 label、按钮/链接可访问名称、表格语义和图片 alt。
2. 检查键盘路径：Tab 顺序、Enter/Space/Esc 行为、焦点可见、关闭后焦点恢复。
3. 检查复杂组件：对话框、菜单、标签页、树、抽屉、表格和自定义控件的 ARIA 状态。
4. 检查动态状态：loading、empty、error、toast 和异步更新需要被屏幕阅读器感知。
5. 输出分级报告；报告格式见 [references/report-template.md](references/report-template.md)。

## Detailed References

Load [references/report-template.md](references/report-template.md) when writing an accessibility review report.

## Constraints

- 优先使用语义化 HTML，而不是 ARIA。
- `role` 不应覆盖原生语义。
- 交互元素必须可键盘访问。
- 表单错误必须与字段关联。
- 颜色对比度风险需要指出具体文本/背景组合。

## Expected Output

交互元素可键盘访问，语义和 ARIA 使用正确，焦点管理稳定；无障碍检查报告保存为 `reports/accessibility-review-YYYY-MM-DD-HHmmss.md`。
