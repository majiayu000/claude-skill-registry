---
name: twitter-collector
description: Twitter 数据采集到数据库的完整自动化工作流（采集→筛选→Grok 转换→数据库录入）
---

# Twitter 完整工作流

自动采集 Twitter 搜索结果，输出推文链接列表，可直接粘贴到筛选网页进行人工筛选。

## 使用场景

当你希望自动批量获取符合特定搜索参数的推文链接，而不是手动在浏览器中搜索和复制链接时使用。

## 使用方式

### 方式 A：MCP 驱动模式（推荐，免配置）
直接指令 AI 执行采集。AI 会自动调用内置的 `browser` 技能，同步您的 Profile 并处理所有搜索逻辑。
- **优点**：无需手动启动 Chrome 调试端口，全自动化。
- **指令示例**：`@twitter-collector 执行下，使用 nano-banana-pro 预设。`

### 方式 B：本地脚本模式（需开启调试端口）
如果您希望在本地终端手动运行：
1. **启动 Chrome 调试端口**：
   ```bash
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222
   ```
2. **运行脚本**：
   ```bash
   node scripts/collector.js --preset nano-banana-pro --output preview
   ```

## 工作流程
1. 基于搜索参数访问 Twitter 搜索页面
2. 自动滚动加载更多推文
3. 提取推文链接和基础信息
4. 去重和简单过滤
5. 输出链接列表（每行一个链接）或预览 HTML

## 快速开始

### 前置要求

```bash
npm install playwright
npx playwright install chromium
```

### 运行方式

```bash
# 基础使用（默认搜索参数）
node scripts/collector.js

# 自定义搜索参数
node scripts/collector.js --query "你的关键词" --since "24h"

# 生成可视化预览页面
node scripts/collector.js --preset nano-banana-pro --output preview

# 从筛选页导出完整文本（基于第三方解析）
node scripts/collector.js --preset nano-banana-pro --output filter-json
```

## 可用参数

- `--query`: 搜索关键词（支持 AND/OR 逻辑）
- `--since`: 时间范围（24h、7d、30d）
- `--min-likes`: 最小点赞数
- `--max-tweets`: 最大采集数量（默认 100）
- `--exclude`: 排除关键词（空格分隔）
- `--filter-content`: 内容类型过滤（media、videos、images）
- `--exclude-replies`: 排除回复
- `--exclude-retweets`: 排除转发
- `--score-keywords`: 评分关键词（逗号分隔）
- `--min-score`: 最低评分阈值（0-1）
- `--output`: 输出格式（console/file/preview/filter-json）
- `--filter-url`: 筛选页地址
- `--output-dir`: 输出目录

## 预设搜索参数

内置预设搜索配置，直接使用插件中的搜索参数：

### Nano Banana Pro

默认搜索参数（来自你的插件配置）：

```
#NanoBananaPro OR #NanoBanana OR "Nano Banana" OR "prompt"
AND -female -woman -hair -GEMINIFOURTH
since_time:{{NOW-24h}}
min_faves:50
filter:media
-filter:replies
```

**说明**：
- 关键词：Nano Banana Pro 相关 + prompt
- 排除：女性相关、GEMINIFOURTH
- 时间：最近 24 小时
- 最小点赞：50
- 内容：包含媒体
- 排除：回复

## 输出格式

### 链接列表格式

输出为纯文本，每行一个链接：

```
https://x.com/username/status/1234567890
https://x.com/username/status/1234567891
https://x.com/username/status/1234567892
```

**使用方法**：
1. 复制输出内容
2. 粘贴到筛选网页（`https://twitterhot.vercel.app/tweet-filter.html`）
3. 继续你现有的筛选流程

### 输出统计

运行结束后显示：

```
✅ 采集完成
📊 总计: 100 条
✅ 去重后: 95 条
🔗 链接已输出到控制台
```

## 技术实现

### 核心逻辑

1. **搜索页面导航**
   - 构建完整的 Twitter 搜索 URL
   - 支持时间变量（`{{NOW-24h}}`）

2. **自动滚动采集**
   - 模拟人工滚动行为
   - 等待内容加载
   - 停止条件：达到最大数量或到底部

3. **推文提取**
   - 选择器：`article[data-testid="tweet"]`
   - 提取：URL、ID、文本、点赞数

4. **去重机制**
   - 基于推文 ID
   - Set 数据结构去重

5. **输出处理**
   - 统一 URL 格式（`https://x.com/...`）
   - 每行一个链接
   - 可选：保存到文件

## 示例输出

```bash
$ node scripts/collector.js --preset "nano-banana-pro"

🔍 搜索参数：
#NanoBananaPro OR #NanoBanana OR "Nano Banana" OR "prompt"
AND -female -woman -hair -GEMINIFOURTH
since_time:{{NOW-24h}}
min_faves:50
filter:media
-filter:replies

📊 采集进度: ████████████████ 100/100
✅ 采集完成
📊 总计: 100 条
✅ 去重后: 95 条
🔗 链接列表:

https://x.com/username1/status/1234567890
https://x.com/username2/status/1234567891
https://x.com/username3/status/1234567892
...
```

## 优势

- **零配置**：内置搜索参数，开箱即用
- **完全自动化**：无需手动操作浏览器
- **兼容现有流程**：输出格式直接适配你的筛选网页
- **可扩展**：支持自定义搜索参数
- **轻量**：基于 Node.js + Playwright，无需额外依赖
