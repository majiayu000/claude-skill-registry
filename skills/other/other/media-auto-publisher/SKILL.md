---
name: media-auto-publisher
description: 通用自媒体文章自动发布工具。支持百家号、搜狐号、知乎三个平台的自动化发布流程。使用Playwright MCP工具实现平台导航和发布页面进入，支持通过storageState管理Cookie实现账号切换。当用户需要发布文章到自媒体平台、打开平台发布页面、切换自媒体账号时使用此skill。工作流程：1)检查并打开指定平台 2)验证登录状态 3)自动关闭广告弹窗 4)导航到发布文章页面 5)收集发布信息 6)自动填写并发布。
---

# 媒体自动发布工具 (Media Auto Publisher)

通用自媒体文章自动发布助手，支持百家号、搜狐号、知乎三个平台。

## 快速开始

### 基本用法

```
用户: 打开百家号发布页面
用户: 帮我进入知乎写文章
用户: 切换到搜狐号发布文章
用户: 帮我发布文章到百家号
```

### 支持的平台

| 平台代码 | 平台名称 | 发布页面URL | 自动化状态 |
|----------|----------|-------------|-----------|
| `baijiahao` | 百家号 | https://baijiahao.baidu.com/builder/rc/edit?type=news | ✅ 完全支持 |
| `sohu` | 搜狐号 | https://mp.sohu.com/api/author/article/new | ✅ 完全支持 |
| `zhihu` | 知乎 | https://zhuanlan.zhihu.com/write | ✅ 支持Cookie登录 |

> **重大更新：** 使用 Playwright MCP 后，知乎可以通过 `storageState` 管理登录态，不再需要调试端口！

## 工作流程

### 标准发布流程

1. **确认平台** - 识别用户指定的平台（百家号/搜狐/知乎）
2. **打开平台** - 使用`mcp__plugin_playwright_playwright__browser_navigate`导航到平台首页
3. **检查登录** - 通过页面快照验证用户是否已登录
4. **关闭弹窗** - 自动检测并关闭广告/活动弹窗
5. **进入发布页** - 导航到文章发布页面
6. **收集信息** - 询问文章标题、内容、封面等信息
7. **自动填写** - 填写所有收集到的信息
8. **发布文章** - 点击发布按钮并验证成功

---

## 完整自动发布工作流 ⭐

### 工作流触发条件

当用户说以下任意指令时启动完整发布流程：
- "帮我发布文章到[平台]"
- "自动发布到[平台]"
- "我要发布文章"
- "[平台]发布文章"

### 发布前信息收集

在执行发布前，需要按顺序收集以下信息（使用AskUserQuestion工具）：

#### 第一阶段：基础内容（必填）

| 字段 | 说明 | 示例 |
|------|------|------|
| **文章标题** | 文章的标题 | "如何用Python自动化发布文章" |
| **正文内容** | Markdown格式的文章内容 | "# 引言\\n这是正文..." |

#### 第二阶段：增强内容（可选）

| 字段 | 说明 | 适用平台 |
|------|------|----------|
| **封面图片** | 本地图片路径或图片URL | 全平台 |
| **文章摘要** | 文章的简短摘要 | 百家号/搜狐号 |

#### 第三阶段：分类与标签（可选）

| 字段 | 说明 | 适用平台 |
|------|------|----------|
| **文章话题/标签** | 相关话题标签，多个用逗号分隔 | 全平台 |
| **投稿至问题** | 将文章投稿到的知乎问题 | 知乎 |
| **分类/栏目** | 文章所属分类 | 百家号/搜狐号 |

#### 第四阶段：发布设置（可选）

| 字段 | 说明 | 适用平台 |
|------|------|----------|
| **创作声明** | 原创声明/转载声明 | 全平台 |
| **可见性设置** | 公开/仅自己可见/定时发布 | 全平台 |
| **专栏** | 发布到指定专栏 | 知乎 |

---

## 各平台详细发布步骤

### 百家号完整发布流程

```
python
# 步骤1：导航到百家号首页
mcp__plugin_playwright_playwright__browser_navigate(url="https://baijiahao.baidu.com/")

# 步骤2：检查登录状态
mcp__plugin_playwright_playwright__browser_snapshot()

# 步骤3：关闭百家号特有弹窗
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const closeSelectors = ['下一步', '立即体验', '我知道了', '知道了'];
    for (const selector of closeSelectors) {
        try {
            const element = await page.getByText(selector).first();
            if (await element.isVisible()) {
                await element.click();
                await page.waitForTimeout(500);
            }
        } catch (e) {}
    }
    await page.evaluate(() => {
        document.querySelectorAll('dialog, [role="dialog"], .tooltip').forEach(el => el.remove());
    });
    return { success: true };
}
''')

# 步骤4：进入发布页面（直接导航）
mcp__plugin_playwright_playwright__browser_navigate(url="https://baijiahao.baidu.com/builder/rc/edit?type=news")

# 步骤5：填写文章标题
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const titleInput = await page.locator('input[placeholder*="请输入标题"]').first();
    await titleInput.fill('{文章标题}');
    return { success: true };
}
''')

# 步骤6：填写正文内容（百家号在iframe中）
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const frame = page.frame({ url: /editor/ }) || page.mainFrame();
    await frame.locator('[contenteditable="true"], .editor-body').first().fill('{正文内容}');
    return { success: true };
}
''')

# 步骤7：上传封面图（如果提供）
if 封面图片:
    mcp__plugin_playwright_playwright__browser_click(ref="三图模式")
    for 图片路径 in 封面图片列表:
        mcp__plugin_playwright_playwright__browser_file_upload(paths=["{图片路径}"])

# 步骤8：填写摘要（如果提供）
if 文章摘要:
    mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const summaryInput = await page.locator('textarea[placeholder*="摘要"]').first();
    await summaryInput.fill('{文章摘要}');
    return { success: true };
}
    ''')

# 步骤9：选择分类（如果提供）
if 文章分类:
    mcp__plugin_playwright_playwright__browser_click(ref="分类选择器")
    mcp__plugin_playwright_playwright__browser_click(ref="{分类}按钮")

# 步骤10：发布前确认
mcp__plugin_playwright_playwright__browser_take_screenshot(path="百家号发布前预览.png")

# 步骤11：点击发布
mcp__plugin_playwright_playwright__browser_click(ref="发布按钮")

# 步骤12：验证发布成功
mcp__plugin_playwright_playwright__browser_wait_for(element="发布成功提示", timeout=10000)
```

### 搜狐号完整发布流程

```
python
# 步骤1：导航到搜狐号发布页
mcp__plugin_playwright_playwright__browser_navigate(url="https://mp.sohu.com/api/author/article/new")

# 步骤2：检查登录状态
mcp__plugin_playwright_playwright__browser_snapshot()

# 步骤3：关闭弹窗（如有）
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const closeSelectors = ['我知道了', '知道了', '关闭'];
    for (const selector of closeSelectors) {
        try {
            await page.getByText(selector).first().click();
            await page.waitForTimeout(300);
        } catch (e) {}
    }
    return { success: true };
}
''')

# 步骤4：填写文章标题
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const titleInput = await page.locator('input[name="title"], input[placeholder*="标题"]').first();
    await titleInput.fill('{文章标题}');
    return { success: true };
}
''')

# 步骤5：填写正文内容
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const editor = await page.locator('#editor, .editor-content, [contenteditable="true"]').first();
    await editor.fill('{正文内容}');
    return { success: true };
}
''')

# 步骤6：上传封面图（如果提供）
if 封面图片:
    mcp__plugin_playwright_playwright__browser_click(ref="封面上传按钮")
    mcp__plugin_playwright_playwright__browser_file_upload(paths=["{封面图片路径}"])

# 步骤7：填写摘要（如果提供）
if 文章摘要:
    mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const summaryInput = await page.locator('textarea[name="summary"]').first();
    await summaryInput.fill('{文章摘要}');
    return { success: true };
}
    ''')

# 步骤8：选择栏目（如果提供）
if 文章栏目:
    mcp__plugin_playwright_playwright__browser_click(ref="栏目选择器")
    mcp__plugin_playwright_playwright__browser_click(ref="{栏目}按钮")

# 步骤9：设置原创声明（如果需要）
if 创作声明 == "原创":
    mcp__plugin_playwright_playwright__browser_click(ref="原创声明开关")

# 步骤10：发布前确认
mcp__plugin_playwright_playwright__browser_take_screenshot(path="搜狐号发布前预览.png")

# 步骤11：点击发布
mcp__plugin_playwright_playwright__browser_click(ref="发布按钮")

# 步骤12：验证发布成功
mcp__plugin_playwright_playwright__browser_wait_for(element="发布成功", timeout=10000)
```

### 知乎完整发布流程

```
python
# 步骤1：导航到知乎写文章页面
mcp__plugin_playwright_playwright__browser_navigate(url="https://zhuanlan.zhihu.com/write")

# 步骤2：检查登录状态
mcp__plugin_playwright_playwright__browser_snapshot()

# 步骤3：关闭弹窗（如有）
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const closeSelectors = ['跳过', '以后再说', '不再提示'];
    for (const selector of closeSelectors) {
        try {
            await page.getByText(selector).first().click();
            await page.waitForTimeout(300);
        } catch (e) {}
    }
    return { success: true };
}
''')

# 步骤4：填写文章标题
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const titleInput = await page.locator('.WriteIndex-titleInput, input[placeholder*="请输入标题"]').first();
    await titleInput.fill('{文章标题}');
    return { success: true };
}
''')

# 步骤5：填写正文内容
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const editor = await page.locator('.PublicDraftEditor-content, [contenteditable="true"]').first();
    await editor.fill('{正文内容}');
    return { success: true };
}
''')

# 步骤6：上传封面图（如果提供）
if 封面图片:
    mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    await page.locator('.UploadCoverButton, [class*="upload"]').first().click();
    return { success: true };
}
    ''')
    mcp__plugin_playwright_playwright__browser_file_upload(paths=["{封面图片路径}"])

# 步骤7：添加话题标签（如果提供）
if 文章话题:
    for 话题 in 文章话题列表:
        mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    await page.locator('text=添加话题, .TopicEditor-input').first().click();
    await page.locator('input[placeholder*="搜索话题"]').fill('{话题}');
    await page.waitForTimeout(500);
    await page.locator('.TopicItem, [role="option"]').first().click();
    return { success: true };
}
        ''')

# 步骤8：投稿至问题（如果提供）
if 投稿至问题:
    mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    await page.locator('text=投稿至问题, .PublishToQuestion').first().click();
    await page.locator('input[placeholder*="搜索问题"]').fill('{问题标题}');
    await page.waitForTimeout(500);
    await page.locator('.QuestionItem, [role="option"]').first().click();
    return { success: true };
}
    ''')

# 步骤9：设置创作声明（如果需要）
if 创作声明:
    mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    await page.locator('button[class*="setting"], text=设置').first().click();
    await page.locator('text={声明类型}').first().click();
    return { success: true };
}
    ''')

# 步骤10：选择专栏（如果提供）
if 发布专栏:
    mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    await page.locator('text=选择专栏, .ColumnSelector').first().click();
    await page.locator('text={专栏名称}').first().click();
    return { success: true };
}
    ''')

# 步骤11：发布前确认
mcp__plugin_playwright_playwright__browser_take_screenshot(path="知乎发布前预览.png")

# 步骤12：点击发布
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const publishBtn = await page.getByText('发布').first();
    await publishBtn.click();
    return { success: true };
}
''')

# 步骤13：验证发布成功
mcp__plugin_playwright_playwright__browser_wait_for(element="发布成功", timeout=10000)
```

### 各平台字段选择器速查表

| 字段 | 百家号选择器 | 搜狐号选择器 | 知乎选择器 |
|------|-------------|-------------|-----------|
| **标题输入框** | input[placeholder*="请输入标题"] | input[name="title"] | .WriteIndex-titleInput |
| **正文编辑器** | iframe .editor-body | #editor | .PublicDraftEditor-content |
| **封面上传** | .upload-cover-btn | .cover-upload | .UploadCoverButton |
| **摘要输入框** | textarea[placeholder*="摘要"] | textarea[name="summary"] | ❌ 不支持 |
| **分类选择器** | .category-select | .column-select | ❌ 用话题替代 |
| **话题输入框** | ❌ 不支持 | .tag-input | .TopicEditor-input |
| **投稿问题** | ❌ 不支持 | ❌ 不支持 | .PublishToQuestion |
| **发布按钮** | button:has-text("发布") | button.publish-btn | button:has-text("发布") |

---

### 账号切换流程（推荐）

Playwright MCP 支持通过 storageState 管理多个账号：

保存登录态（首次）：
```javascript
// 1. 手动登录一次平台
await page.goto("https://www.zhihu.com")
// ... 用户手动登录 ...

// 2. 保存登录状态
await context.storageState({ path: 'zhihu_account1.json' })
```

切换账号：
```javascript
// 加载已保存的登录态
const context = await browser.newContext({
  storageState: 'zhihu_account1.json'
})
```

## 关键文件

### scripts/media_publisher.py 主执行脚本

快速打开平台：
```bash
python scripts/media_publisher.py baijiahao
python scripts/media_publisher.py open baijiahao
```

查看平台信息：
```bash
python scripts/media_publisher.py info baijiahao
```

生成工作流程：
```bash
python scripts/media_publisher.py workflow baijiahao
python scripts/media_publisher.py workflow sohu --output workflow.json --format json
```

检查登录状态：
```bash
python scripts/media_publisher.py check-login baijiahao
python scripts/media_publisher.py check-login sohu --snapshot snapshot.txt
```

检测弹窗：
```bash
python scripts/media_publisher.py detect-popup baijiahao
python scripts/media_publisher.py detect-popup sohu --snapshot snapshot.txt
```

### scripts/cookie_manager.py

常用命令：
```bash
python scripts/cookie_manager.py save zhihu --account "账号1"
python scripts/cookie_manager.py list
python scripts/cookie_manager.py switch zhihu "账号1"
```

### scripts/platform_navigator.py

平台导航助手，提供各平台的导航配置和弹窗检测逻辑。

## 登录状态检测

百家号：检测页面中是否存在 头像、发布作品、内容管理 等元素

搜狐号：检测页面中是否存在 发布文章、内容管理、个人中心 等元素

知乎：检测页面中是否存在 写文章、首页、通知、私信 等元素

## 弹窗自动关闭

### 百家号特有弹窗处理

```
python
mcp__plugin_playwright_playwright__browser_run_code(code='''
async (page) => {
    const closeSelectors = ['下一步', '立即体验', '我知道了', '知道了'];
    for (const selector of closeSelectors) {
        try {
            const element = await page.getByText(selector).first();
            if (await element.isVisible()) {
                await element.click();
                await page.waitForTimeout(500);
            }
        } catch (e) {}
    }
    await page.evaluate(() => {
        document.querySelectorAll('dialog, [role="dialog"], .tooltip').forEach(el => el.remove());
    });
    return { success: true };
}
''')
```

### 各平台常见弹窗关键词

| 平台 | 关闭按钮关键词 |
|------|---------------|
| 百家号 | 我知道了、下一步、立即体验、关闭、× |
| 搜狐号 | 我知道了、知道了、关闭、× |
| 知乎 | 跳过、以后再说、不再提示、关闭 |

## MCP工具调用序列

### Playwright MCP 工具映射

| 功能 | Chrome DevTools MCP | Playwright MCP |
|------|---------------------|----------------|
| 导航 | navigate_page | browser_navigate |
| 快照 | take_snapshot | browser_snapshot |
| 点击 | click | browser_click |
| 填写 | fill | browser_fill_form / browser_type |
| 截图 | - | browser_take_screenshot |
| 等待 | - | browser_wait_for |
| 执行代码 | - | browser_run_code |
| 文件上传 | - | browser_file_upload |

## 知乎登录解决方案

### 方案一：使用 storageState（推荐）

```javascript
await browser.newContext({
  storageState: 'zhihu_cookies.json'
})
```

步骤：
1. 先用普通 Chrome 登录知乎
2. 使用 browser_run_code 导出 cookies
3. 保存为 storageState 文件
4. 后续直接加载该文件实现免登录

## 故障处理

| 问题 | 解决方案 |
|------|----------|
| 未登录 | 提示用户先登录并保存 storageState |
| Cookie失效 | 使用cookie_manager.py重新保存登录状态 |
| 弹窗无法关闭 | 手动截图，分析弹窗结构后更新关闭规则 |
| 页面加载超时 | 使用browser_wait_for增加等待时间 |
| 知乎反爬 | Playwright 的 storageState 可有效绕过检测 |
| 填写失败 | 使用browser_run_code直接执行JavaScript |

## Playwright MCP 优势

| 特性 | Chrome DevTools | Playwright |
|------|----------------|------------|
| 知乎登录 | 需要调试端口 | storageState 支持 |
| 多浏览器 | 仅 Chrome | Chrome/Firefox/Safari |
| Cookie管理 | 手动导入 | storageState() API |
| 反爬检测 | 自动化特征明显 | 可伪装真实浏览器 |
| 跨平台 | 依赖 Chrome | 多引擎支持 |
| 文件上传 | 需要特殊处理 | browser_file_upload |

## 注意事项

1. 首次登录 - 首次使用需要用户手动登录平台并保存 storageState
2. StorageState位置 - 登录态保存在 ~/.claude/media-auto-publisher/storage_states/
3. 平台更新 - 平台UI更新可能需要更新选择器和指示器
4. 频率限制 - 避免频繁操作触发平台反爬机制
5. 知乎支持 - Playwright 可以通过 storageState 实现知乎免登录发布
6. 内容预览 - 发布前务必截图预览，确认内容无误

## Playwright 高级用法

### 伪装真实浏览器

```javascript
async (page) => {
    await page.setExtraHTTPHeaders({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    });
    await page.addInitScript(() => {
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false
        });
    });
    await page.goto('https://zhuanlan.zhihu.com/write');
}
```

### 批量发布管理

```bash
python scripts/cookie_manager.py list
python scripts/cookie_manager.py save zhihu --account "主账号"
python scripts/cookie_manager.py save zhihu --account "小号"
```
