---
name: recording
description: 使用 Playwright 进行浏览器自动化录屏。当需要录制 Web 应用操作演示、生成带时间线的屏幕录像时使用。
argument-hint: [目标URL]
---

# 浏览器录屏技能

## 核心要求

1. **单次连续录制** - 不要分段录制
2. **记录时间线** - 每个操作的精确时间戳
3. **真实数据** - 使用真实或有意义的测试数据
4. **适当节奏** - 留足够时间让画面呈现

## 录屏脚本结构

```javascript
const { chromium } = require("playwright");
const path = require("path");
const fs = require("fs/promises");

const BASE_URL = "http://localhost:5173";
const OUTPUT_DIR = path.join(__dirname, "..", "public", "recordings");
const VIEWPORT = { width: 1920, height: 1080 };

// 测试数据 - 使用真实有意义的数据
const TEST_DATA = {
  // 定义测试数据
};

// 时间线记录器 - 关键组件
class TimelineRecorder {
  constructor() {
    this.startTime = Date.now();
    this.events = [];
  }

  mark(event) {
    const elapsed = (Date.now() - this.startTime) / 1000;
    this.events.push({ time: elapsed, event });
    console.log(`  [${elapsed.toFixed(1)}s] ${event}`);
    return elapsed;
  }

  getTimeline() {
    return this.events;
  }
}

async function recordDemo() {
  await fs.mkdir(OUTPUT_DIR, { recursive: true });

  const browser = await chromium.launch({
    headless: false,
    slowMo: 50,  // 稍微放慢操作，更自然
  });

  const context = await browser.newContext({
    viewport: VIEWPORT,
    recordVideo: {
      dir: OUTPUT_DIR,
      size: VIEWPORT,
    },
    locale: "zh-CN",
  });

  const page = await context.newPage();
  const timeline = new TimelineRecorder();

  try {
    // 场景录制...

  } finally {
    // 保存时间线
    const timelineData = {
      totalDuration: (Date.now() - timeline.startTime) / 1000,
      events: timeline.getTimeline(),
    };

    await fs.writeFile(
      path.join(OUTPUT_DIR, "timeline.json"),
      JSON.stringify(timelineData, null, 2)
    );

    await page.close();
    await context.close();
    await browser.close();
  }
}
```

## 录屏最佳实践

### 1. 等待时间设置

```javascript
// 页面加载后等待
await page.goto(url, { waitUntil: "networkidle" });
await page.waitForTimeout(1500);

// 点击后等待响应
await element.click();
await page.waitForTimeout(2000);

// 表单输入后等待
await input.fill(value);
await page.waitForTimeout(500);

// 弹窗打开后等待
await dialog.waitFor({ state: "visible" });
await page.waitForTimeout(1500);
```

### 2. 操作节奏

| 操作类型 | 建议等待时间 |
|----------|--------------|
| 页面加载 | 1.5-3 秒 |
| 点击按钮 | 1-2 秒 |
| 表单输入 | 0.5-1 秒 |
| 弹窗出现 | 1.5-2 秒 |
| 数据加载 | 2-3 秒 |
| 场景切换 | 2-3 秒 |

### 3. 悬停展示

```javascript
// 悬停显示 tooltip
await element.hover();
timeline.mark("悬停显示提示");
await page.waitForTimeout(3000);  // 留足时间让观众看清
```

### 4. 逐字输入效果

```javascript
// 更真实的输入效果
for (const char of text) {
  await input.type(char, { delay: 80 });
}
```

## 时间线记录规范

### 必须记录的事件

- 页面加载完成
- 主要区域就绪
- 每次点击操作
- 每次数据加载完成
- 弹窗打开/关闭
- 录制结束

### 事件命名规范

```javascript
timeline.mark("页面加载完成");
timeline.mark("点击[按钮名]按钮");
timeline.mark("输入用户名: xxx");
timeline.mark("[弹窗名]弹窗打开");
timeline.mark("显示查询结果");
timeline.mark("录制结束");
```

## 视频格式转换

录制完成后转换为 MP4：

```javascript
// 使用 FFmpeg 转换
const { execSync } = require("child_process");

execSync(`ffmpeg -y -i ${webmPath} -c:v libx264 -preset fast -crf 23 ${mp4Path}`);
```

## 故障排除

### Chromium 未安装

```bash
npx playwright install chromium
```

### 录制黑屏

确保 `headless: false`

### 操作太快

增加 `slowMo` 值或 `waitForTimeout`

### 元素未找到

使用更稳定的选择器：
```javascript
// 推荐
page.locator('button:has-text("查询")')
page.locator('.el-button--primary')

// 避免
page.locator('button:nth-child(2)')
```
