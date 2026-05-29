---
name: notion-docs-enhancer
description: |
  使用 Playwright 浏览器自动化快速创建和完善 Notion 文档。
  触发场景：用户提到"Notion"、"完善文档"、"创建页面"、"填充内容"、"notion文档"。
  适用于：创建新页面、修改标题、粘贴 Markdown 内容、格式化文档。
---

# Notion 文档增强 Skill

## 概述

此 Skill 通过 Playwright 浏览器自动化帮助用户快速创建和完善 Notion 文档，无需 Notion API 授权。

## 核心能力

1. **创建/修改页面标题** - 自动导航到页面并修改标题
2. **粘贴 Markdown 内容** - 自动转换为 Notion 原生格式（标题、列表、表格、链接）
3. **清理冗余内容** - 删除多余的文本块
4. **截图验证** - 自动截图确认最终效果

## 使用方法

### 基本用法

```
帮我完善这个 Notion 文档：https://www.notion.so/xxx
内容：[你的 Markdown 内容]
```

### 快速创建

```
在我的 Notion 创建一个关于 [主题] 的文档，包含以下章节：
1. 概述
2. 功能说明
3. 使用指南
```

## 操作流程

### 步骤 1: 导航到页面

```javascript
// 使用 Playwright MCP 工具
await mcp__plugin_playwright_playwright__browser_navigate({
  url: "https://www.notion.so/page-id"
});
```

### 步骤 2: 等待页面加载

```javascript
await mcp__plugin_playwright_playwright__browser_wait_for({
  time: 3  // 等待 3 秒确保页面完全加载
});
```

### 步骤 3: 修改标题

```javascript
// 获取页面快照找到标题元素
await mcp__plugin_playwright_playwright__browser_snapshot();

// 点击标题按钮
await mcp__plugin_playwright_playwright__browser_click({
  element: "页面标题",
  ref: "title-ref"
});

// 输入新标题
await mcp__plugin_playwright_playwright__browser_type({
  element: "标题输入框",
  ref: "input-ref",
  text: "新标题"
});

// 确认
await mcp__plugin_playwright_playwright__browser_press_key({
  key: "Enter"
});
```

### 步骤 4: 粘贴内容（关键技巧）

```javascript
// 使用 browser_run_code 执行复杂操作
await mcp__plugin_playwright_playwright__browser_run_code({
  code: `async (page) => {
    const content = \`## 一、概述

你的 Markdown 内容...

## 二、功能说明

| 列1 | 列2 |
|-----|-----|
| 值1 | 值2 |
\`;

    // 写入剪贴板
    await page.evaluate((text) => {
      navigator.clipboard.writeText(text);
    }, content);

    // 等待
    await page.waitForTimeout(500);

    // 粘贴（Notion 会自动转换 Markdown）
    await page.keyboard.press('Meta+v');

    return 'Content pasted';
  }`
});
```

### 步骤 5: 清理和验证

```javascript
// 删除多余内容
await mcp__plugin_playwright_playwright__browser_click({
  element: "多余文本",
  ref: "ref"
});
await mcp__plugin_playwright_playwright__browser_press_key({
  key: "Backspace"
});

// 截图验证
await mcp__plugin_playwright_playwright__browser_take_screenshot({
  filename: "notion-result.png",
  fullPage: true
});

// 关闭浏览器
await mcp__plugin_playwright_playwright__browser_close();
```

## 重要技巧

### Markdown 自动转换

Notion 在粘贴时会自动转换以下 Markdown 语法：

| Markdown | Notion 效果 |
|----------|------------|
| `## 标题` | 二级标题 |
| `- 列表项` | 无序列表 |
| `1. 列表项` | 有序列表 |
| `| 表格 |` | 表格 |
| `[链接](url)` | 超链接 |
| `**粗体**` | 粗体文本 |
| `` `代码` `` | 行内代码 |

### 常见问题处理

**问题**: 内容输入到了标题中
**解决**: 使用 `Meta+z` 撤销，确保先移动光标到内容区域

**问题**: 菜单弹出阻挡输入
**解决**: 按 `Escape` 关闭菜单，或按 `ArrowDown` 移动到内容区

**问题**: 页面需要登录
**解决**: 确保浏览器中已登录 Notion 账号

## 模板内容

### 技术文档模板

```markdown
## 一、概述

[产品/功能简介]

## 二、核心功能

| 功能 | 说明 |
|------|------|
| 功能1 | 描述 |
| 功能2 | 描述 |

## 三、使用指南

1. 步骤一
2. 步骤二
3. 步骤三

## 四、最佳实践

- 建议一
- 建议二

## 五、参考资源

- [资源链接](url)
```

### 会议纪要模板

```markdown
## 会议信息

- 日期：YYYY-MM-DD
- 参会人：
- 主持人：

## 议程

1. 议题一
2. 议题二

## 讨论要点

### 议题一
- 要点

### 议题二
- 要点

## 行动项

| 任务 | 负责人 | 截止日期 |
|------|--------|----------|
| 任务1 | @人员 | 日期 |

## 下次会议

- 时间：
- 主题：
```

## 注意事项

1. **浏览器状态**: 确保 Playwright 浏览器已安装（`npx playwright install chromium`）
2. **登录状态**: 首次使用需要在浏览器中登录 Notion
3. **页面权限**: 确保你有编辑目标页面的权限
4. **网络连接**: 需要稳定的网络连接

## 详细参考

- 完整 API 参考见 [REFERENCE.md](REFERENCE.md)
- 更多使用示例见 [EXAMPLES.md](EXAMPLES.md)
