---
name: db-importer
description: 将 Grok 生成的 JSON 数据自动录入到 import_classifications.html 网页。
---

# 数据库录入器

将 Grok 生成的 JSON 数据自动录入到 import_classifications.html 网页。

## 使用场景

当你通过 Grok 生成结构化 JSON 后，需要将其录入到数据库时使用。

## 工作流程

1. **读取 JSON 文件**：从指定路径读取 Grok 生成的 JSON
2. **打开 import_classifications.html**：访问网页
3. **自动录入**：将 JSON 内容粘贴到网页
4. **点击提交**：触发数据库录入
5. **断点续跑**：支持从上次位置继续处理

## 快速开始

### 前置要求

- import_classifications.html 网页可访问
- JSON 文件已生成

### 运行方式

```bash
# 基础使用（默认文件）
node scripts/importer.js

# 指定 JSON 文件
node scripts/importer.js --input-file /Users/douba/twitter-output/grok-data-2026-01-13.json

# 断点续跑（从第 10 条开始）
node scripts/importer.js --input-file /Users/douba/twitter-output/grok-data-2026-01-13.json --start-index 10
```

## 可用参数

| 参数 | 说明 | 默认值 | 示例 |
|------|--------|---------|--------|
| `--input-file` | JSON 文件路径 | - | /Users/douba/twitter-output/grok-data.json |
| `--start-index` | 起始索引（断点续跑） | 0 | 10 |
| `--batch-size` | 每批处理数量 | 10 | 5 |
| `--delay` | 录入间隔（毫秒） | 1000 | 2000 |
| `--browser` | 浏览器类型 | chromium | chromium |

## 输出示例

```
🚀 数据库录入器启动...

📄 读取文件: /Users/douba/twitter-output/grok-data-2026-01-13.json
📊 总计: 10 条记录

📤 批次 1/2 (5 条)
  ✅ 第 1 条：https://x.com/user/status/1234567890
  ✅ 第 2 条：https://x.com/user/status/1234567891
  ✅ 第 3 条：https://x.com/user/status/1234567892
  ✅ 第 4 条：https://x.com/user/status/1234567893
  ✅ 第 5 条：https://x.com/user/status/1234567894

📤 批次 2/2 (5 条)
  ✅ 第 6 条：https://x.com/user/status/1234567895
  ✅ 第 7 条：https://x.com/user/status/1234567896
  ✅ 第 8 条：https://x.com/user/status/1234567897
  ✅ 第 9 条：https://x.com/user/status/1234567898
  ✅ 第 10 条：https://x.com/user/status/1234567899

✅ 录入完成
📁 进度文件: /Users/douba/twitter-output/importer-progress.json
```

## 技术实现

### 核心逻辑

1. **JSON 解析**
   - 读取并验证 JSON 格式
   - 提取数据数组

2. **批量处理**
   - 分批录入，避免一次性处理过多数据
   - 可配置批大小和延迟

3. **断点续跑**
   - 记录处理进度
   - 支持 `--start-index` 从指定位置继续

4. **自动录入**
   - 访问网页
   - 定位输入框
   - 粘贴 JSON
   - 等待处理完成
   - 保存进度

### 实现方式

```javascript
async function importToDatabase(browser, data, config) {
  const page = await browser.newPage();
  await page.goto('https://ttmouse.com/import_classifications.html', { waitUntil: 'domcontentloaded' });

  // 定位输入框并粘贴
  const input = page.locator('textarea, input[type="text"]');
  const jsonString = JSON.stringify(data, null, 2);
  await input.fill(jsonString);

  // 等待处理
  await page.waitForTimeout(config.delay);

  await browser.close();
}
```

## 注意事项

- 确保网页已加载完成
- 网络稳定，避免录入中断
- 断点续跑时确保 JSON 文件未变动

## 下一步

使用 `twitter-workflow` 技能可以串联整个流程：
采集 → 筛选 → Grok 转换 → 数据库录入
