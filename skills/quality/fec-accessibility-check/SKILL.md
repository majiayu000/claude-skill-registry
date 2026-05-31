---
name: fec-accessibility-check
description: Use when reviewing or improving frontend accessibility, semantic structure, keyboard support, focus management, ARIA labels, screen reader behavior, WCAG 2.2 issues, touch accessibility, or assistive-technology regressions; Chinese triggers include 无障碍, accessibility, a11y, WCAG, 屏幕阅读器.
---

# 无障碍实现规范（WCAG 2.2 AA）

## Purpose

确保前端 UI 对残障用户可访问，满足 WCAG 2.2 AA 的核心要求，并能被键盘、屏幕阅读器、触控和缩放用户稳定使用。

## Procedure

1. 检查语义结构：landmark、标题层级、表单 label、按钮/链接可访问名称、表格语义和图片 alt。
2. 检查键盘路径：Tab 顺序、Enter/Space/Esc 行为、焦点可见、关闭后焦点恢复。
3. 检查复杂组件：对话框、菜单、标签页、树、抽屉、表格和自定义控件的 ARIA 状态。
4. 检查动态状态：loading、empty、error、toast 和异步更新需要被屏幕阅读器感知。
5. 检查视觉与触控可读性：文本/背景对比、focus ring、缩放到 200%、减少动效偏好、触摸目标尺寸和移动端虚拟键盘行为。
6. 用真实键盘路径复核关键流程，必要时补充屏幕阅读器或浏览器无障碍树观察；屏幕阅读器流程见 [references/screen-reader-testing.md](references/screen-reader-testing.md)。
7. 复核 WCAG 2.2 新增高频风险：可见焦点不被遮挡、拖拽操作有替代路径、目标尺寸过小、帮助入口和认证流程不依赖记忆负担。
8. 输出分级报告；报告格式见 [references/report-template.md](references/report-template.md)。

## Detailed References

撰写无障碍审查报告时，加载 [references/report-template.md](references/report-template.md)。需要验证屏幕阅读器公告、焦点读法和动态区域时，加载 [references/screen-reader-testing.md](references/screen-reader-testing.md)。

## Constraints

- 优先使用语义化 HTML，而不是 ARIA。
- `role` 不应覆盖原生语义。
- 交互元素必须可键盘访问。
- 表单错误必须与字段关联。
- 颜色对比度风险需要指出具体文本/背景组合。
- 不用 ARIA 弥补可以用原生 HTML 解决的问题。
- 不把浏览器自动可访问树当作最终结论；关键路径需要用键盘和至少一种辅助技术或等价检查验证。

## Expected Output

交互元素可键盘访问，语义和 ARIA 使用正确，焦点管理稳定；无障碍检查报告保存为 `reports/accessibility-review-YYYY-MM-DD-HHmmss.md`。
