---
name: feishu-sync
description: 使用Playwright自动同步文档到飞书。Use for tasks like syncing markdown to Feishu, automating Feishu document updates, browser automation for Feishu. Keywords: 飞书同步, feishu sync, playwright, 文档同步, 自动化
---

# feishu-sync

> 使用Playwright自动化同步Markdown文档到飞书Wiki/文档

Use this skill for 飞书文档自动同步、Markdown到飞书的自动化、浏览器自动化操作飞书。

---

## 快速使用

### 前置条件

```bash
# 确保使用anaconda python（已安装playwright）
/opt/anaconda3/bin/python3 -c "from playwright.sync_api import sync_playwright; print('OK')"

# 如未安装，执行：
pip install playwright pyperclip
playwright install chromium
```

### 运行同步

```bash
/opt/anaconda3/bin/python3 scripts/sync_to_feishu.py
```

---

## 核心脚本

**位置**: `scripts/sync_to_feishu.py`

### 关键配置

```python
# 目标飞书文档URL
FEISHU_URL = "https://xxx.feishu.cn/wiki/xxxxxxx"

# 源文件路径
REPORT_PATH = Path("docs/research/your-report.md")
```

### 执行流程

```
1. 读取本地Markdown文件
2. 复制内容到系统剪贴板
3. 启动Chrome浏览器（非无头模式）
4. 导航到飞书文档
5. 检测登录状态，等待用户登录（5分钟超时）
6. 登录后自动点击编辑区域
7. 移动到文档末尾，添加分隔线
8. 自动粘贴内容（Cmd+V）
9. 等待用户确认后关闭浏览器
```

---

## 最佳实践

### 1. 使用系统Chrome而非下载Chromium

```python
# 推荐：使用系统安装的Chrome，避免下载超时
browser = await p.chromium.launch(
    headless=False,
    channel="chrome"  # 关键参数
)
```

**原因**: Chromium下载经常超时（30s），使用系统Chrome可跳过下载步骤。

### 2. 禁用输出缓冲

```python
# 在脚本开头添加，确保实时输出
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)
```

**原因**: 后台运行时输出会被缓冲，无法实时监控进度。

### 3. 设置足够的登录超时

```python
await page.wait_for_url(
    lambda url: "wiki" in url and "accounts" not in url,
    timeout=300000  # 5分钟，给用户足够时间扫码登录
)
```

**原因**: 扫码登录需要时间，2分钟可能不够。

### 4. 多种编辑区域选择器

```python
editor_selectors = [
    '[data-testid="doc-editor"]',
    '.doc-content',
    '.suite-markdown-container',
    '[contenteditable="true"]',  # 最通用
    '.editor-container',
    '.wiki-content',
    '.lark-editor',
]
```

**原因**: 飞书不同版本/页面的编辑器选择器可能不同。

### 5. 使用pyperclip处理剪贴板

```python
import pyperclip
pyperclip.copy(report_content)

# 然后用键盘快捷键粘贴
await page.keyboard.press('Meta+v')
```

**原因**: 直接用Playwright的fill()方法对富文本编辑器兼容性差。

---

## 常见问题

### Q1: Chromium下载超时

```
Error: Request to https://cdn.playwright.dev/... timed out after 30000ms
```

**解决**: 使用 `channel="chrome"` 参数使用系统Chrome。

### Q2: 登录超时

```
❌ 登录超时或失败: Timeout 120000ms exceeded
```

**解决**:
1. 增加timeout到300000ms（5分钟）
2. 确保浏览器窗口可见，及时完成登录

### Q3: 找不到编辑区域

```
⚠️ 未找到编辑区域，尝试点击页面中心...
```

**解决**:
1. 检查飞书文档是否有编辑权限
2. 尝试手动点击编辑区域后再运行脚本

### Q4: 粘贴失败

**解决**:
1. 确保pyperclip已安装
2. macOS需要授予终端剪贴板访问权限
3. 手动按Cmd+V作为备选

### Q5: 输出为空/无法监控进度

**解决**: 添加 `sys.stdout.reconfigure(line_buffering=True)`

---

## 扩展场景

### 同步到多个文档

```python
FEISHU_URLS = [
    "https://xxx.feishu.cn/wiki/doc1",
    "https://xxx.feishu.cn/wiki/doc2",
]

for url in FEISHU_URLS:
    await sync_to_document(page, url, content)
```

### 定时同步

```bash
# crontab -e
0 9 * * * /opt/anaconda3/bin/python3 /path/to/sync_to_feishu.py >> /var/log/feishu-sync.log 2>&1
```

### 替换而非追加

```python
# 全选后粘贴，替换全部内容
await page.keyboard.press('Meta+a')
await page.keyboard.press('Meta+v')
```

---

## 完整脚本模板

```python
#!/opt/anaconda3/bin/python3
"""飞书文档自动同步"""

import asyncio
import sys
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

from playwright.async_api import async_playwright
import pyperclip

FEISHU_URL = "https://xxx.feishu.cn/wiki/xxx"
SOURCE_FILE = Path("docs/your-file.md")

async def sync():
    content = SOURCE_FILE.read_text(encoding="utf-8")
    pyperclip.copy(content)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, channel="chrome")
        page = await (await browser.new_context()).new_page()

        await page.goto(FEISHU_URL)
        await page.wait_for_timeout(3000)

        # 等待登录
        if "accounts" in page.url:
            print("请登录飞书...")
            await page.wait_for_url(
                lambda u: "wiki" in u and "accounts" not in u,
                timeout=300000
            )

        # 点击编辑区域
        await page.wait_for_timeout(3000)
        await page.click('[contenteditable="true"]', timeout=5000)

        # 粘贴
        await page.keyboard.press('Meta+End')
        await page.keyboard.press('Enter')
        await page.keyboard.press('Meta+v')

        print("✅ 同步完成")
        await page.wait_for_event('close', timeout=300000)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(sync())
```

---

## 相关资源

- Playwright Python文档: https://playwright.dev/python/
- 飞书开放平台: https://open.feishu.cn/
- pyperclip: https://pypi.org/project/pyperclip/
